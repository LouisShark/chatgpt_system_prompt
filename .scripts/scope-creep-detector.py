#!/usr/bin/env python3
"""
Scope Creep Detector
====================
Read-only analysis of a Git diff versus a stated intended change.

Usage
-----
    python .scripts/scope-creep-detector.py --intended-change "Fix typo in README"
    # or
    INTENDED_CHANGE="Fix typo in README" python .scripts/scope-creep-detector.py

    # Compare staged changes against HEAD:
    python .scripts/scope-creep-detector.py --intended-change "..." --staged

    # Compare working tree + staged against a base branch:
    python .scripts/scope-creep-detector.py --intended-change "..." --base main

Output
------
    PASS   — change is consistent with stated intent
    WARN   — potential scope creep; review recommended
    FAIL   — significant scope creep; change should be reviewed before merging

This tool is READ-ONLY.  It never modifies files or reverts changes unless the
user explicitly invokes --revert (which it refuses, since revert is not supported
by design — use `git checkout` or `git restore` manually).

Adapted from the concept described in the chatgpt_system_prompt AI-harness spec.
Source repository: LouisShark/chatgpt_system_prompt
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEPENDENCY_FILES = {
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "Pipfile",
    "Pipfile.lock",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Gemfile",
    "Gemfile.lock",
    "pom.xml",
    "build.gradle",
}

CI_DIRS = {".github/workflows", ".circleci", ".travis.yml", "Jenkinsfile", ".drone.yml"}

GENERATED_PATTERNS = [
    re.compile(r"TOC\.md$"),
    re.compile(r"\.svg$"),
    re.compile(r"__pycache__"),
    re.compile(r"\.pyc$"),
    re.compile(r"dist/"),
    re.compile(r"build/"),
    re.compile(r"node_modules/"),
    re.compile(r"\.lock$"),
]

CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf", ".env"}

WARN_FILE_COUNT = 10
FAIL_FILE_COUNT = 25
WARN_LINE_CHANGE = 300
FAIL_LINE_CHANGE = 800


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    level: str  # WARN or FAIL
    category: str
    message: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class DiffStats:
    changed_files: List[str] = field(default_factory=list)
    insertions: int = 0
    deletions: int = 0
    raw_diff: str = ""


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _run(cmd: List[str], cwd: Optional[str] = None) -> Tuple[int, str]:
    """Run a git command and return (returncode, stdout)."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, (result.stdout or "").strip()


def find_repo_root() -> Path:
    code, out = _run(["git", "rev-parse", "--show-toplevel"])
    if code != 0:
        print("ERROR: not inside a git repository", file=sys.stderr)
        sys.exit(1)
    return Path(out)


def get_diff(repo_root: Path, base: Optional[str], staged: bool) -> DiffStats:
    """Collect changed files and diff statistics."""
    cwd = str(repo_root)

    if base:
        # diff between base branch and HEAD + working tree
        name_cmd = ["git", "diff", "--name-only", base]
        stat_cmd = ["git", "diff", "--stat", base]
        diff_cmd = ["git", "diff", base]
    elif staged:
        name_cmd = ["git", "diff", "--name-only", "--cached"]
        stat_cmd = ["git", "diff", "--stat", "--cached"]
        diff_cmd = ["git", "diff", "--cached"]
    else:
        # default: everything uncommitted (staged + unstaged) vs HEAD
        name_cmd = ["git", "diff", "--name-only", "HEAD"]
        stat_cmd = ["git", "diff", "--stat", "HEAD"]
        diff_cmd = ["git", "diff", "HEAD"]

    _, names_out = _run(name_cmd, cwd=cwd)
    _, stat_out = _run(stat_cmd, cwd=cwd)
    _, diff_out = _run(diff_cmd, cwd=cwd)

    changed_files = [f for f in names_out.splitlines() if f.strip()]

    insertions = 0
    deletions = 0
    for match in re.finditer(r"(\d+) insertion", stat_out):
        insertions += int(match.group(1))
    for match in re.finditer(r"(\d+) deletion", stat_out):
        deletions += int(match.group(1))

    return DiffStats(
        changed_files=changed_files,
        insertions=insertions,
        deletions=deletions,
        raw_diff=diff_out,
    )


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_file_count(stats: DiffStats) -> Optional[Finding]:
    n = len(stats.changed_files)
    if n >= FAIL_FILE_COUNT:
        return Finding(
            level="FAIL",
            category="file-count",
            message=f"{n} files changed — unusually large change set",
            evidence=stats.changed_files[:20],
        )
    if n >= WARN_FILE_COUNT:
        return Finding(
            level="WARN",
            category="file-count",
            message=f"{n} files changed — review for unrelated modifications",
            evidence=stats.changed_files,
        )
    return None


def check_line_volume(stats: DiffStats) -> Optional[Finding]:
    total = stats.insertions + stats.deletions
    if total >= FAIL_LINE_CHANGE:
        return Finding(
            level="FAIL",
            category="line-volume",
            message=f"{total} lines changed (+{stats.insertions} / -{stats.deletions})",
        )
    if total >= WARN_LINE_CHANGE:
        return Finding(
            level="WARN",
            category="line-volume",
            message=f"{total} lines changed (+{stats.insertions} / -{stats.deletions})",
        )
    return None


def check_dependency_changes(stats: DiffStats) -> Optional[Finding]:
    dep_files = [
        f for f in stats.changed_files
        if Path(f).name in DEPENDENCY_FILES
    ]
    if dep_files:
        return Finding(
            level="WARN",
            category="dependency-changes",
            message="Dependency manifest(s) modified — verify intent",
            evidence=dep_files,
        )
    return None


def check_ci_changes(stats: DiffStats, intended: str) -> Optional[Finding]:
    ci_files = []
    for f in stats.changed_files:
        if any(f.startswith(d) or f == d for d in CI_DIRS):
            ci_files.append(f)
    if not ci_files:
        return None
    # If the intended change explicitly mentions CI, workflows, or automation, it's expected
    ci_keywords = {"ci", "workflow", "action", "pipeline", "automation", "github"}
    if any(kw in intended.lower() for kw in ci_keywords):
        return None
    return Finding(
        level="WARN",
        category="ci-changes",
        message="CI/automation configuration modified — not mentioned in intended change",
        evidence=ci_files,
    )


def check_config_changes(stats: DiffStats, intended: str) -> Optional[Finding]:
    config_files = [
        f for f in stats.changed_files
        if Path(f).suffix.lower() in CONFIG_EXTENSIONS
        and not any(f.startswith(d) for d in CI_DIRS)
        and Path(f).name not in DEPENDENCY_FILES
    ]
    if not config_files:
        return None
    config_keywords = {"config", "setting", "option", "environment", "env", "mcp"}
    if any(kw in intended.lower() for kw in config_keywords):
        return None
    return Finding(
        level="WARN",
        category="config-changes",
        message="Configuration file(s) modified — verify scope",
        evidence=config_files,
    )


def check_generated_files(stats: DiffStats) -> Optional[Finding]:
    generated = [
        f for f in stats.changed_files
        if any(p.search(f) for p in GENERATED_PATTERNS)
    ]
    if generated:
        return Finding(
            level="WARN",
            category="generated-files",
            message="Auto-generated file(s) in diff — usually safe if updated by CI, not manual edits",
            evidence=generated,
        )
    return None


def check_api_expansion(stats: DiffStats, repo_root: Path) -> Optional[Finding]:
    """Detect new public function/class definitions added to non-test Python files."""
    new_public_symbols = []
    # Only scan .py additions
    for line in stats.raw_diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            m = re.match(r"^\+\s*(def |class )([A-Z_a-z]\w*)", line)
            if m and not m.group(2).startswith("_"):
                new_public_symbols.append(m.group(2))

    if len(new_public_symbols) > 3:
        return Finding(
            level="WARN",
            category="public-api-expansion",
            message=f"{len(new_public_symbols)} new public Python symbol(s) introduced",
            evidence=new_public_symbols[:10],
        )
    return None


def check_unrelated_docs(stats: DiffStats, intended: str) -> Optional[Finding]:
    doc_files = [
        f for f in stats.changed_files
        if Path(f).suffix.lower() in {".md", ".rst", ".txt"}
        and not any(p.search(f) for p in GENERATED_PATTERNS)
    ]
    if not doc_files:
        return None
    doc_keywords = {"doc", "readme", "changelog", "contribut", "license", "usage"}
    if any(kw in intended.lower() for kw in doc_keywords):
        return None
    if len(doc_files) > 3:
        return Finding(
            level="WARN",
            category="documentation-changes",
            message=f"{len(doc_files)} documentation file(s) changed — verify they are related to stated intent",
            evidence=doc_files,
        )
    return None


def check_scattered_changes(stats: DiffStats) -> Optional[Finding]:
    """Warn if changes span many unrelated directories."""
    dirs = set()
    for f in stats.changed_files:
        parts = Path(f).parts
        dirs.add(parts[0] if len(parts) > 1 else ".")
    if len(dirs) >= 6:
        return Finding(
            level="WARN",
            category="scattered-changes",
            message=f"Changes span {len(dirs)} top-level directories — unusually broad",
            evidence=sorted(dirs),
        )
    return None


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def verdict(findings: List[Finding]) -> str:
    levels = {f.level for f in findings}
    if "FAIL" in levels:
        return "FAIL"
    if "WARN" in levels:
        return "WARN"
    return "PASS"


def print_report(
    intended: str,
    stats: DiffStats,
    findings: List[Finding],
) -> str:
    result = verdict(findings)
    sep = "=" * 60

    lines = [
        sep,
        f"SCOPE CREEP DETECTOR -- {result}",
        sep,
        f"Intended change : {intended}",
        f"Files changed   : {len(stats.changed_files)}",
        f"Lines +/-       : +{stats.insertions} / -{stats.deletions}",
        "",
    ]

    if not findings:
        lines.append("  No scope-creep signals detected.")
    else:
        for f in findings:
            lines.append(f"  [{f.level}] {f.category}: {f.message}")
            for e in f.evidence:
                lines.append(f"         • {e}")
            lines.append("")

    lines.append(sep)
    lines.append(
        "PASS: consistent with intent. "
        "WARN: review recommended. "
        "FAIL: significant scope creep detected."
    )
    lines.append(sep)

    report = "\n".join(lines)
    print(report)
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Scope Creep Detector — compare stated intent against actual diff.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--intended-change",
        default=os.environ.get("INTENDED_CHANGE", ""),
        help="One-sentence description of the intended change "
             "(or set INTENDED_CHANGE env var).",
    )
    parser.add_argument(
        "--base",
        default=None,
        help="Base branch or commit to diff against (e.g. 'main'). "
             "Defaults to HEAD.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Only analyse staged (cached) changes.",
    )
    parser.add_argument(
        "--revert",
        action="store_true",
        help=argparse.SUPPRESS,  # exists to warn users; not implemented by design
    )
    args = parser.parse_args()

    if args.revert:
        print(
            "ERROR: --revert is not supported.  This tool is read-only.\n"
            "Use 'git checkout <file>' or 'git restore <file>' to revert changes.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not args.intended_change:
        print(
            "ERROR: --intended-change is required (or set INTENDED_CHANGE env var).\n"
            "Example: python .scripts/scope-creep-detector.py "
            '--intended-change "Fix typo in README"',
            file=sys.stderr,
        )
        sys.exit(2)

    repo_root = find_repo_root()
    stats = get_diff(repo_root, base=args.base, staged=args.staged)

    if not stats.changed_files:
        print("No changes detected in the diff.  Nothing to analyse.")
        sys.exit(0)

    findings: List[Finding] = []
    for check in [
        lambda: check_file_count(stats),
        lambda: check_line_volume(stats),
        lambda: check_dependency_changes(stats),
        lambda: check_ci_changes(stats, args.intended_change),
        lambda: check_config_changes(stats, args.intended_change),
        lambda: check_generated_files(stats),
        lambda: check_api_expansion(stats, repo_root),
        lambda: check_unrelated_docs(stats, args.intended_change),
        lambda: check_scattered_changes(stats),
    ]:
        result = check()
        if result:
            findings.append(result)

    result = print_report(args.intended_change, stats, findings)
    sys.exit(0 if result == "PASS" else (1 if result == "WARN" else 2))


if __name__ == "__main__":
    main()
