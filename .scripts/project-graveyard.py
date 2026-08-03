#!/usr/bin/env python3
"""
Project Graveyard
=================
Audit one or more project directories for dormancy, duplication, and unclear status.

This tool is DRY-RUN ONLY — it never deletes, archives, moves, or modifies projects.

Usage
-----
    # Audit projects configured in PROJECT_AUDIT_ROOTS (colon-separated on Unix,
    # semicolon-separated on Windows, or one path per line):
    python .scripts/project-graveyard.py

    # Audit specific roots passed on the command line:
    python .scripts/project-graveyard.py --roots /path/to/projects /another/path

    # Audit the current repository only:
    python .scripts/project-graveyard.py --roots .

    # Write report to a file:
    python .scripts/project-graveyard.py --output graveyard-report.md

Classifications
---------------
    ACTIVE           — recently active, clear purpose
    MAINTAIN         — moderately active, stable maintenance mode
    REVIEW           — mixed signals, needs human review
    DORMANT          — no recent activity but may still be relevant
    ARCHIVE_CANDIDATE — prolonged inactivity, low signals of ongoing use
    UNKNOWN          — insufficient data to classify

IMPORTANT: A classification of ARCHIVE_CANDIDATE does NOT mean the project is
worthless or safe to delete.  It means a human should review it.
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

try:
    import git
    HAS_GITPYTHON = True
except ImportError:
    HAS_GITPYTHON = False


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ProjectSignals:
    path: Path
    name: str
    is_git_repo: bool = False
    last_commit_date: Optional[datetime] = None
    days_since_last_commit: Optional[int] = None
    uncommitted_changes: bool = False
    open_branches: List[str] = field(default_factory=list)
    todo_fixme_count: int = 0
    has_readme: bool = False
    has_purpose_statement: bool = False
    is_archived: bool = False
    file_count: int = 0
    has_sensitive_indicators: bool = False
    recent_pr_branches: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class ProjectReport:
    signals: ProjectSignals
    classification: str
    confidence: str  # HIGH / MEDIUM / LOW
    evidence: List[str] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    recommended_next_action: str = ""
    review_owner: str = "— (unassigned)"
    review_date: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Signal collection
# ---------------------------------------------------------------------------

SENSITIVE_PATTERNS = [
    re.compile(r"\.env$"),
    re.compile(r"secrets?/"),
    re.compile(r"credentials?"),
    re.compile(r"private[-_]key"),
    re.compile(r"\.pem$"),
    re.compile(r"\.p12$"),
]

PURPOSE_KEYWORDS = [
    "purpose", "overview", "what is", "this project", "this repo",
    "description", "about", "introduction", "summary",
]


def collect_signals(project_path: Path) -> ProjectSignals:
    signals = ProjectSignals(path=project_path, name=project_path.name)

    if not project_path.exists():
        signals.error = f"Path does not exist: {project_path}"
        return signals

    # File count (fast approximation — count immediate children)
    try:
        signals.file_count = sum(1 for _ in project_path.iterdir())
    except PermissionError:
        signals.error = "Permission denied"
        return signals

    # README and purpose statement
    for readme_name in ("README.md", "README.rst", "README.txt", "README"):
        readme = project_path / readme_name
        if readme.exists():
            signals.has_readme = True
            content = readme.read_text(encoding="utf-8", errors="replace").lower()
            signals.has_purpose_statement = any(
                kw in content for kw in PURPOSE_KEYWORDS
            )
            break

    # TODO/FIXME count (scan non-binary files ≤ 3 dirs deep)
    todo_count = 0
    try:
        for p in project_path.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".js", ".ts", ".md", ".txt", ".sh", ".go", ".rb"}:
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                    todo_count += len(re.findall(r"\b(TODO|FIXME)\b", text))
                except OSError:
                    pass
    except OSError:
        pass
    signals.todo_fixme_count = todo_count

    # Sensitive indicators
    try:
        for p in project_path.iterdir():
            if p.is_file():
                if any(pat.search(p.name) for pat in SENSITIVE_PATTERNS):
                    signals.has_sensitive_indicators = True
                    break
    except OSError:
        pass

    if not HAS_GITPYTHON:
        signals.error = "GitPython not installed — git signals unavailable"
        return signals

    # Git signals
    try:
        repo = git.Repo(str(project_path), search_parent_directories=True)
        signals.is_git_repo = True

        # Last commit date
        try:
            last_commit = next(repo.iter_commits())
            signals.last_commit_date = datetime.fromtimestamp(
                last_commit.committed_date, tz=timezone.utc
            )
            delta = datetime.now(timezone.utc) - signals.last_commit_date
            signals.days_since_last_commit = delta.days
        except StopIteration:
            pass

        # Uncommitted changes
        signals.uncommitted_changes = repo.is_dirty(untracked_files=True)

        # Open branches (excluding HEAD and remote-tracking)
        try:
            signals.open_branches = [
                b.name for b in repo.branches
                if b.name not in ("main", "master", "HEAD")
            ]
        except Exception:
            pass

        # Is archived (GitHub stores this in the repo, not accessible via GitPython)
        # We can't detect this without GitHub API access; leave False
        signals.is_archived = False

    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        signals.is_git_repo = False
    except Exception as e:
        signals.error = f"Git error: {e}"

    return signals


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(signals: ProjectSignals) -> ProjectReport:
    evidence = []
    questions = []

    if not signals.is_git_repo:
        evidence.append("Not a git repository")
        return ProjectReport(
            signals=signals,
            classification="UNKNOWN",
            confidence="LOW",
            evidence=evidence,
            unresolved_questions=["Is this a git repo?  Is it under version control?"],
            recommended_next_action="Investigate manually — no git history available",
        )

    days = signals.days_since_last_commit

    # Last-commit scoring
    if days is None:
        evidence.append("No commits found")
        classification = "UNKNOWN"
        confidence = "LOW"
    elif days <= 30:
        evidence.append(f"Last commit {days}d ago — recently active")
        classification = "ACTIVE"
        confidence = "HIGH"
    elif days <= 90:
        evidence.append(f"Last commit {days}d ago — moderate activity")
        classification = "MAINTAIN"
        confidence = "MEDIUM"
    elif days <= 180:
        evidence.append(f"Last commit {days}d ago — slowing down")
        classification = "REVIEW"
        confidence = "MEDIUM"
    elif days <= 365:
        evidence.append(f"Last commit {days}d ago — low activity")
        classification = "DORMANT"
        confidence = "MEDIUM"
    else:
        evidence.append(f"Last commit {days}d ago — prolonged inactivity")
        classification = "ARCHIVE_CANDIDATE"
        confidence = "MEDIUM"

    # Modifiers
    if signals.uncommitted_changes:
        evidence.append("Has uncommitted changes — work may be in progress")
        if classification in ("DORMANT", "ARCHIVE_CANDIDATE"):
            classification = "REVIEW"
            confidence = "MEDIUM"
            questions.append("Why are there uncommitted changes in a dormant project?")

    if signals.open_branches:
        n = len(signals.open_branches)
        evidence.append(f"{n} open branch(es): {', '.join(signals.open_branches[:5])}")
        if classification in ("DORMANT", "ARCHIVE_CANDIDATE") and n > 0:
            classification = "REVIEW"
            confidence = "MEDIUM"
            questions.append("Are open branches abandoned or awaiting merge?")

    if not signals.has_readme:
        evidence.append("No README found")
        questions.append("What is the purpose of this project?")
        if confidence == "HIGH":
            confidence = "MEDIUM"
    elif not signals.has_purpose_statement:
        evidence.append("README lacks a clear purpose statement")
        questions.append("Is the project purpose documented elsewhere?")

    if signals.todo_fixme_count > 0:
        evidence.append(f"{signals.todo_fixme_count} TODO/FIXME marker(s) found")
        if signals.todo_fixme_count > 20:
            questions.append("Are there unfinished tasks blocking completion?")

    if signals.has_sensitive_indicators:
        evidence.append("Sensitive file indicators found (.env, secrets, keys)")
        questions.append("Does this project contain active secrets or live credentials?")
        if classification == "ARCHIVE_CANDIDATE":
            # Sensitive projects need explicit human review before any action
            classification = "REVIEW"
            confidence = "HIGH"

    if signals.is_archived:
        evidence.append("Repository is marked archived on the host")
        classification = "ARCHIVE_CANDIDATE"
        confidence = "HIGH"

    # Recommended actions
    actions = {
        "ACTIVE": "No action required — continue normal development",
        "MAINTAIN": "Review roadmap; ensure issues are triaged",
        "REVIEW": "Schedule a 30-minute review to clarify status and next steps",
        "DORMANT": "Decide: resume, hand off, or archive — requires human decision",
        "ARCHIVE_CANDIDATE": (
            "Human review required before any archiving — "
            "verify no active users, outstanding work, or sensitive data"
        ),
        "UNKNOWN": "Investigate manually to determine project status",
    }

    return ProjectReport(
        signals=signals,
        classification=classification,
        confidence=confidence,
        evidence=evidence,
        unresolved_questions=questions,
        recommended_next_action=actions.get(classification, "Review manually"),
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

CLASSIFICATION_EMOJI = {
    "ACTIVE": "[ACTIVE]",
    "MAINTAIN": "[MAINTAIN]",
    "REVIEW": "[REVIEW]",
    "DORMANT": "[DORMANT]",
    "ARCHIVE_CANDIDATE": "[ARCHIVE?]",
    "UNKNOWN": "[UNKNOWN]",
}


def render_report(reports: List[ProjectReport], fmt: str = "text") -> str:
    if fmt == "markdown":
        return render_markdown(reports)
    return render_text(reports)


def render_text(reports: List[ProjectReport]) -> str:
    lines = ["=" * 60, "PROJECT GRAVEYARD AUDIT REPORT (DRY RUN)", "=" * 60, ""]
    for r in reports:
        emoji = CLASSIFICATION_EMOJI.get(r.classification, "")
        lines.append(f"{emoji}  {r.signals.name}")
        lines.append(f"   Path            : {r.signals.path}")
        lines.append(f"   Classification  : {r.classification} (confidence: {r.confidence})")
        lines.append(f"   Evidence:")
        for e in r.evidence:
            lines.append(f"     - {e}")
        if r.unresolved_questions:
            lines.append(f"   Open questions:")
            for q in r.unresolved_questions:
                lines.append(f"     ? {q}")
        lines.append(f"   Next action     : {r.recommended_next_action}")
        lines.append(f"   Review owner    : {r.review_owner}")
        lines.append(f"   Review date     : {r.review_date}")
        if r.signals.error:
            lines.append(f"   Error           : {r.signals.error}")
        lines.append("")
    lines.append("=" * 60)
    lines.append(
        "NOTE: ARCHIVE_CANDIDATE does NOT mean safe to delete.  Human review required."
    )
    lines.append("=" * 60)
    return "\n".join(lines)


def render_markdown(reports: List[ProjectReport]) -> str:
    lines = [
        "# Project Graveyard Audit Report (Dry Run)",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "> **Dry run only.** This report does not modify any projects.",
        "",
        "| Project | Classification | Confidence | Last Commit | Next Action |",
        "|---------|---------------|-----------|------------|------------|",
    ]
    for r in reports:
        days = r.signals.days_since_last_commit
        last = f"{days}d ago" if days is not None else "unknown"
        lines.append(
            f"| {r.signals.name} | {r.classification} | {r.confidence} "
            f"| {last} | {r.recommended_next_action[:60]} |"
        )
    lines += [""]

    for r in reports:
        emoji = CLASSIFICATION_EMOJI.get(r.classification, "")
        lines += [
            f"## {emoji} {r.signals.name}",
            "",
            f"**Path**: `{r.signals.path}`  ",
            f"**Classification**: {r.classification} _(confidence: {r.confidence})_",
            "",
            "### Evidence",
            "",
        ]
        for e in r.evidence:
            lines.append(f"- {e}")
        if r.unresolved_questions:
            lines += ["", "### Unresolved Questions", ""]
            for q in r.unresolved_questions:
                lines.append(f"- {q}")
        lines += [
            "",
            "### Report",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Recommended next action | {r.recommended_next_action} |",
            f"| Review owner | {r.review_owner} |",
            f"| Review date | {r.review_date} |",
            "",
        ]
        if r.signals.error:
            lines.append(f"> ⚠️ Error during analysis: {r.signals.error}")
            lines.append("")

    lines += [
        "---",
        "",
        "**Important**: `ARCHIVE_CANDIDATE` does not mean the project is worthless or",
        "safe to delete. It means a human should review it before taking any action.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Root discovery
# ---------------------------------------------------------------------------


def resolve_roots(cli_roots: List[str]) -> List[Path]:
    if cli_roots:
        return [Path(r).resolve() for r in cli_roots]

    env_val = os.environ.get("PROJECT_AUDIT_ROOTS", "")
    if env_val:
        sep = ";" if sys.platform == "win32" else ":"
        paths = [p.strip() for p in env_val.split(sep) if p.strip()]
        return [Path(p).resolve() for p in paths]

    return [Path(".").resolve()]


def expand_roots(roots: List[Path]) -> List[Path]:
    """
    For each root, if it looks like a projects container (many subdirs, no .git),
    expand to its immediate children.  Otherwise use it directly.
    """
    projects = []
    for root in roots:
        if not root.exists():
            print(f"WARNING: root path does not exist: {root}", file=sys.stderr)
            continue
        git_dir = root / ".git"
        if git_dir.exists():
            # root is itself a git repo
            projects.append(root)
        else:
            # treat root as a container of project subdirectories
            try:
                children = sorted(
                    p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
                )
                if children:
                    projects.extend(children)
                else:
                    projects.append(root)
            except PermissionError:
                projects.append(root)
    return projects


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Project Graveyard — audit project directories for dormancy.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--roots",
        nargs="+",
        metavar="PATH",
        help="Project root directories to audit. "
             "Defaults to PROJECT_AUDIT_ROOTS env var, then current directory.",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write report to FILE instead of stdout.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Output format (default: text).",
    )
    args = parser.parse_args()

    if not HAS_GITPYTHON:
        print(
            "WARNING: GitPython is not installed.  "
            "Git signals will be unavailable.\n"
            "Install with: pip install GitPython",
            file=sys.stderr,
        )

    roots = resolve_roots(args.roots or [])
    projects = expand_roots(roots)

    if not projects:
        print("No project directories found to audit.", file=sys.stderr)
        sys.exit(1)

    print(f"Auditing {len(projects)} project(s)...", file=sys.stderr)

    reports = []
    for project_path in projects:
        signals = collect_signals(project_path)
        report = classify(signals)
        reports.append(report)

    output = render_report(reports, fmt=args.format)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
