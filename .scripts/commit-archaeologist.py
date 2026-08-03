#!/usr/bin/env python3
"""
Commit Archaeologist
====================
On-demand investigation of a file's Git history.

This tool is MANUAL USE ONLY -- it is never run automatically.

Usage
-----
    python .scripts/commit-archaeologist.py <file-path>
    python .scripts/commit-archaeologist.py --file <file-path>

    # Limit history depth:
    python .scripts/commit-archaeologist.py <file-path> --max-commits 20

    # Write report to a file:
    python .scripts/commit-archaeologist.py <file-path> --output report.md

    # Markdown output:
    python .scripts/commit-archaeologist.py <file-path> --format markdown

Example
-------
    python .scripts/commit-archaeologist.py .scripts/idxtool.py

    This will produce a report explaining:
    - When idxtool.py was introduced and by whom
    - Which commits established key behaviours (--toc, --find-gpt, --template, --rename)
    - Which files historically change together with idxtool.py
    - Whether changes appear deliberate or temporary workarounds
    - What issue/PR/commit context explains the current design

Output sections
---------------
    1. Direct Git Evidence      -- commits, dates, authors, file stats
    2. Commit-Message Evidence  -- issues, PRs, keywords, stated rationale
    3. Inferred Intent          -- pattern-based interpretation (clearly labelled)
    4. Unknowns                 -- gaps in the Git history

IMPORTANT: This tool will not fabricate historical intent when the Git history
does not support it.  Inferences are always labelled as inferences.
"""

import argparse
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
class CommitEntry:
    sha: str
    short_sha: str
    author: str
    date: datetime
    message: str
    insertions: int = 0
    deletions: int = 0
    files_changed: List[str] = field(default_factory=list)


@dataclass
class ArchaeologyReport:
    file_path: str
    file_exists: bool
    # Section 1 – direct evidence
    total_commits: int = 0
    first_commit: Optional[CommitEntry] = None
    last_commit: Optional[CommitEntry] = None
    largest_change: Optional[CommitEntry] = None
    co_changed_files: List[tuple] = field(default_factory=list)  # (file, count)
    commit_timeline: List[CommitEntry] = field(default_factory=list)
    # Section 2 – message evidence
    issue_refs: List[str] = field(default_factory=list)
    pr_refs: List[str] = field(default_factory=list)
    fix_keywords: List[str] = field(default_factory=list)
    workaround_signals: List[str] = field(default_factory=list)
    # Section 3 – inferences (always labelled)
    inferences: List[str] = field(default_factory=list)
    # Section 4 – unknowns
    unknowns: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

ISSUE_REF_PATTERN = re.compile(r"#(\d{1,6})\b")
PR_KEYWORDS = re.compile(r"\b(pull request|merge|PR)\b", re.IGNORECASE)
FIX_KEYWORDS = re.compile(
    r"\b(fix|fixes|fixed|bug|bugfix|hotfix|patch|repair|correct)\b", re.IGNORECASE
)
WORKAROUND_KEYWORDS = re.compile(
    r"\b(workaround|hack|temp|temporary|todo|fixme|kludge|quick.?fix|wip)\b",
    re.IGNORECASE,
)
FEATURE_KEYWORDS = re.compile(
    r"\b(add|added|feat|feature|implement|introduce|support|enable)\b",
    re.IGNORECASE,
)
REFACTOR_KEYWORDS = re.compile(
    r"\b(refactor|cleanup|clean.?up|restructure|reorganize|simplify|rename)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def analyse_file(file_path_str: str, max_commits: int = 50) -> ArchaeologyReport:
    file_path = Path(file_path_str)
    report = ArchaeologyReport(
        file_path=str(file_path),
        file_exists=file_path.exists(),
    )

    if not HAS_GITPYTHON:
        report.unknowns.append(
            "GitPython is not installed -- git history unavailable.  "
            "Install with: pip install GitPython"
        )
        return report

    try:
        repo = git.Repo(str(file_path.parent.resolve()), search_parent_directories=True)
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        report.unknowns.append(
            f"No git repository found containing '{file_path}'"
        )
        return report

    # Resolve path relative to repo root
    repo_root = Path(repo.working_tree_dir)
    try:
        rel_path = file_path.resolve().relative_to(repo_root)
    except ValueError:
        rel_path = file_path
    # Normalise to forward slashes for matching against git output
    rel_path_str = str(rel_path).replace("\\", "/")

    # Collect commits that touched this file
    try:
        raw_commits = list(
            repo.iter_commits(paths=str(rel_path), max_count=max_commits)
        )
    except Exception as e:
        report.unknowns.append(f"Could not retrieve git log: {e}")
        return report

    if not raw_commits:
        report.unknowns.append(
            "No commits found for this file.  "
            "It may be untracked, newly added, or the path may be incorrect."
        )
        return report

    # Build commit entries
    entries: List[CommitEntry] = []
    co_change_counter: dict = {}

    for c in raw_commits:
        try:
            stats = c.stats
            file_stats = stats.files.get(rel_path_str, {})
            ins = file_stats.get("insertions", 0)
            dels = file_stats.get("deletions", 0)
            changed_files = list(stats.files.keys())
        except Exception:
            ins, dels, changed_files = 0, 0, []

        entry = CommitEntry(
            sha=c.hexsha,
            short_sha=c.hexsha[:8],
            author=f"{c.author.name} <{c.author.email}>",
            date=datetime.fromtimestamp(c.committed_date, tz=timezone.utc),
            message=c.message.strip(),
            insertions=ins,
            deletions=dels,
            files_changed=changed_files,
        )
        entries.append(entry)

        for f in changed_files:
            if f != rel_path_str:
                co_change_counter[f] = co_change_counter.get(f, 0) + 1

    report.total_commits = len(entries)
    report.commit_timeline = entries
    report.first_commit = entries[-1]
    report.last_commit = entries[0]

    if entries:
        report.largest_change = max(
            entries, key=lambda e: e.insertions + e.deletions
        )

    # Co-changed files (top 10)
    report.co_changed_files = sorted(
        co_change_counter.items(), key=lambda x: x[1], reverse=True
    )[:10]

    # Message analysis
    all_messages = " ".join(e.message for e in entries)

    report.issue_refs = list(set(ISSUE_REF_PATTERN.findall(all_messages)))
    report.pr_refs = list(set(
        m.group(0) for e in entries
        for m in [PR_KEYWORDS.search(e.message)] if m
    ))

    for e in entries:
        msg = e.message
        if FIX_KEYWORDS.search(msg):
            report.fix_keywords.append(f"{e.short_sha}: {msg.splitlines()[0][:80]}")
        if WORKAROUND_KEYWORDS.search(msg):
            report.workaround_signals.append(f"{e.short_sha}: {msg.splitlines()[0][:80]}")

    # Inferences (always labelled as such)
    if entries:
        first = entries[-1]
        last_entry = entries[0]

        feature_commits = [e for e in entries if FEATURE_KEYWORDS.search(e.message)]
        refactor_commits = [e for e in entries if REFACTOR_KEYWORDS.search(e.message)]

        if feature_commits:
            report.inferences.append(
                f"INFERRED: File appears to have been developed incrementally -- "
                f"{len(feature_commits)} commit(s) with feature/add language found."
            )

        if refactor_commits:
            report.inferences.append(
                f"INFERRED: File has been refactored or reorganised {len(refactor_commits)} time(s). "
                f"The current structure may differ significantly from the original design intent."
            )

        if report.workaround_signals:
            report.inferences.append(
                f"INFERRED: {len(report.workaround_signals)} commit(s) suggest temporary workarounds. "
                f"Review these commits for unresolved TODOs or technical debt."
            )

        if report.co_changed_files:
            top_co, top_count = report.co_changed_files[0]
            if top_count >= 3:
                report.inferences.append(
                    f"INFERRED: '{top_co}' is frequently changed alongside this file "
                    f"({top_count} times). They may be tightly coupled."
                )

        # Introduction context
        intro_msg = first.message.splitlines()[0]
        if FEATURE_KEYWORDS.search(intro_msg):
            report.inferences.append(
                f"INFERRED: Initial commit message suggests the file was introduced "
                f"as a deliberate feature: \"{intro_msg[:100]}\""
            )
        else:
            report.inferences.append(
                f"INFERRED: Introduction commit message does not clearly indicate "
                f"the reason: \"{intro_msg[:100]}\""
            )

    # Unknowns
    if not report.issue_refs:
        report.unknowns.append(
            "No issue references (#NNN) found in commit messages -- "
            "original motivation may not be traceable from Git history alone."
        )
    if report.total_commits == max_commits:
        report.unknowns.append(
            f"History was capped at {max_commits} commits.  Older context may exist.  "
            f"Use --max-commits to increase the limit."
        )
    if not report.file_exists:
        report.unknowns.append(
            "File does not exist in the current working tree.  "
            "It may have been deleted or renamed."
        )

    return report


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_report(report: ArchaeologyReport, fmt: str = "text") -> str:
    if fmt == "markdown":
        return render_markdown(report)
    return render_text(report)


def render_text(report: ArchaeologyReport) -> str:
    sep = "=" * 60
    lines = [
        sep,
        f"COMMIT ARCHAEOLOGIST: {report.file_path}",
        sep,
        f"Total commits : {report.total_commits}",
        f"File exists   : {'yes' if report.file_exists else 'no (deleted or renamed)'}",
        "",
    ]

    # Section 1
    lines.append("-- 1. DIRECT GIT EVIDENCE ------------------------------------------")
    if report.first_commit:
        fc = report.first_commit
        lines.append(
            f"  Introduced : {fc.date.strftime('%Y-%m-%d')} by {fc.author}"
        )
        lines.append(f"  Intro SHA  : {fc.short_sha}")
        lines.append(f"  Intro msg  : {fc.message.splitlines()[0][:80]}")
    if report.last_commit:
        lc = report.last_commit
        lines.append(
            f"  Last touch : {lc.date.strftime('%Y-%m-%d')} by {lc.author}"
        )
        lines.append(f"  Last SHA   : {lc.short_sha}")
        lines.append(f"  Last msg   : {lc.message.splitlines()[0][:80]}")
    if report.largest_change:
        big = report.largest_change
        lines.append(
            f"  Largest    : {big.short_sha} (+{big.insertions}/-{big.deletions}) "
            f"on {big.date.strftime('%Y-%m-%d')}"
        )
    if report.co_changed_files:
        lines.append("  Co-changed files:")
        for f, n in report.co_changed_files[:5]:
            lines.append(f"    {n:3}x  {f}")
    lines.append("")
    lines.append("  Commit timeline (most recent first):")
    for e in report.commit_timeline[:10]:
        lines.append(
            f"    {e.short_sha}  {e.date.strftime('%Y-%m-%d')}  "
            f"+{e.insertions:4}/-{e.deletions:4}  "
            f"{e.message.splitlines()[0][:60]}"
        )
    if report.total_commits > 10:
        lines.append(f"    ... ({report.total_commits - 10} more commits not shown)")
    lines.append("")

    # Section 2
    lines.append("-- 2. COMMIT-MESSAGE EVIDENCE ---------------------------------------")
    if report.issue_refs:
        lines.append(f"  Issue refs   : #{', #'.join(sorted(report.issue_refs))}")
    else:
        lines.append("  Issue refs   : none found")
    if report.fix_keywords:
        lines.append(f"  Fix commits  : {len(report.fix_keywords)}")
        for f in report.fix_keywords[:3]:
            lines.append(f"    - {f}")
    if report.workaround_signals:
        lines.append(f"  Workarounds  : {len(report.workaround_signals)}")
        for w in report.workaround_signals[:3]:
            lines.append(f"    - {w}")
    lines.append("")

    # Section 3
    lines.append("-- 3. INFERRED INTENT -----------------------------------------------")
    if report.inferences:
        for inf in report.inferences:
            lines.append(f"  {inf}")
    else:
        lines.append("  No inferences available from the commit history.")
    lines.append("")

    # Section 4
    lines.append("-- 4. UNKNOWNS ------------------------------------------------------")
    if report.unknowns:
        for u in report.unknowns:
            lines.append(f"  ? {u}")
    else:
        lines.append("  No gaps identified in the available history.")
    lines.append("")

    lines.append(sep)
    return "\n".join(lines)


def render_markdown(report: ArchaeologyReport) -> str:
    lines = [
        f"# Commit Archaeology: `{report.file_path}`",
        "",
        f"- **Total commits analysed**: {report.total_commits}",
        f"- **File exists**: {'yes' if report.file_exists else 'no (deleted or renamed)'}",
        "",
    ]

    # Section 1
    lines += ["## 1. Direct Git Evidence", ""]
    if report.first_commit:
        fc = report.first_commit
        lines += [
            f"**Introduced**: {fc.date.strftime('%Y-%m-%d')} by `{fc.author}`  ",
            f"**Intro commit**: `{fc.short_sha}` -- {fc.message.splitlines()[0][:80]}",
            "",
        ]
    if report.last_commit:
        lc = report.last_commit
        lines += [
            f"**Last modified**: {lc.date.strftime('%Y-%m-%d')} by `{lc.author}`  ",
            f"**Last commit**: `{lc.short_sha}` -- {lc.message.splitlines()[0][:80]}",
            "",
        ]
    if report.largest_change:
        big = report.largest_change
        lines += [
            f"**Largest single change**: `{big.short_sha}` "
            f"(+{big.insertions}/−{big.deletions}) on {big.date.strftime('%Y-%m-%d')}",
            "",
        ]
    if report.co_changed_files:
        lines += ["**Frequently co-changed files**:", ""]
        for f, n in report.co_changed_files[:5]:
            lines.append(f"- `{f}` ({n} times)")
        lines.append("")

    lines += ["**Commit timeline** (most recent first):", "", "| SHA | Date | +/- | Message |", "|-----|------|-----|---------|"]
    for e in report.commit_timeline[:10]:
        lines.append(
            f"| `{e.short_sha}` | {e.date.strftime('%Y-%m-%d')} "
            f"| +{e.insertions}/−{e.deletions} "
            f"| {e.message.splitlines()[0][:60]} |"
        )
    if report.total_commits > 10:
        lines.append(f"| … | | | {report.total_commits - 10} more commits |")
    lines.append("")

    # Section 2
    lines += ["## 2. Commit-Message Evidence", ""]
    if report.issue_refs:
        lines.append(f"**Issue references**: #{', #'.join(sorted(report.issue_refs))}")
    else:
        lines.append("**Issue references**: none found")
    lines.append("")
    if report.fix_keywords:
        lines += [f"**Fix/bug commits** ({len(report.fix_keywords)}):"]
        for f in report.fix_keywords[:5]:
            lines.append(f"- {f}")
        lines.append("")
    if report.workaround_signals:
        lines += [f"**Workaround/temp signals** ({len(report.workaround_signals)}):"]
        for w in report.workaround_signals[:5]:
            lines.append(f"- {w}")
        lines.append("")

    # Section 3
    lines += ["## 3. Inferred Intent", ""]
    if report.inferences:
        for inf in report.inferences:
            lines.append(f"- {inf}")
    else:
        lines.append("_No inferences available from the commit history._")
    lines.append("")

    # Section 4
    lines += ["## 4. Unknowns", ""]
    if report.unknowns:
        for u in report.unknowns:
            lines.append(f"- {u}")
    else:
        lines.append("_No gaps identified in the available history._")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Commit Archaeologist -- investigate a file's git history.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File path to investigate.",
    )
    parser.add_argument(
        "--file",
        dest="file_flag",
        metavar="FILE",
        help="Alternative way to specify file path.",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=50,
        help="Maximum number of commits to analyse (default: 50).",
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

    target = args.file_flag or args.file
    if not target:
        parser.print_help()
        print(
            "\nERROR: file path is required.\n"
            "Example: python .scripts/commit-archaeologist.py .scripts/idxtool.py",
            file=sys.stderr,
        )
        sys.exit(2)

    if not HAS_GITPYTHON:
        print(
            "ERROR: GitPython is not installed.  "
            "Install with: pip install GitPython",
            file=sys.stderr,
        )
        sys.exit(1)

    report = analyse_file(target, max_commits=args.max_commits)
    output = render_report(report, fmt=args.format)

    if args.output:
        from pathlib import Path as _Path
        _Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
