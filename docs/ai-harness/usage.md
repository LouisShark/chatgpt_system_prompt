# AI-Harness Usage Guide

Tools added in the `chore/claude-code-harness-upgrade` branch.

---

## Scope Creep Detector

**Purpose**: Compare a Git diff against a stated intended change to detect unplanned
scope expansion before merging.

**When to use**: Before declaring any substantial change complete.

### Running the detector

```bash
# Compare everything uncommitted against HEAD:
python .scripts/scope-creep-detector.py --intended-change "Your one-sentence description"

# Compare against a base branch:
python .scripts/scope-creep-detector.py --intended-change "..." --base main

# Only staged changes:
python .scripts/scope-creep-detector.py --intended-change "..." --staged
```

Or via Claude Code slash command: `/scope-creep <intended change description>`

### Results

| Result | Exit code | Meaning |
|--------|-----------|---------|
| PASS | 0 | Change is consistent with stated intent |
| WARN | 1 | Potential scope creep — review recommended before merging |
| FAIL | 2 | Significant scope creep — revise the change or justify exceptions |

### Handling warnings and failures

WARN and FAIL are advisory — they do not block commits.  When a finding is a
known false positive, document the reason in your PR description.

**Common false positives in this repository**:
- `TOC.md` and `prompts/*/TOC.md` flagged as generated files — expected after
  adding new prompts.
- `.github/badges/tokens.svg` flagged as generated — expected after content changes.

### CI integration

A non-blocking GitHub Actions check runs the detector on pull requests.
See `.github/workflows/scope-creep-check.yml`.  It will annotate PRs with a
WARN or FAIL, but will not block merges until the detector has demonstrated
acceptable accuracy over time.

---

## Project Graveyard

**Purpose**: Audit project directories for dormancy, duplication, and unclear status.

**Important**: This is a dry-run-only tool.  It never modifies, deletes, or archives anything.

### Running the audit

```bash
# Audit the current repo:
python .scripts/project-graveyard.py --roots .

# Audit a projects container directory (expands to subdirectories automatically):
python .scripts/project-graveyard.py --roots /path/to/projects

# Use an environment variable (useful for repeated use):
export PROJECT_AUDIT_ROOTS=/path/to/projects
python .scripts/project-graveyard.py

# Markdown output:
python .scripts/project-graveyard.py --roots . --format markdown --output report.md
```

Or via Claude Code slash command: `/graveyard`

### Classifications

| Classification | Meaning | Suggested action |
|---------------|---------|-----------------|
| ACTIVE | Last commit ≤ 30 days, clear purpose | No action required |
| MAINTAIN | Last commit ≤ 90 days, stable | Review roadmap, triage issues |
| REVIEW | Mixed signals | Schedule 30-minute review |
| DORMANT | No recent activity (≤ 1 year) | Human decision: resume, hand off, or archive |
| ARCHIVE_CANDIDATE | Prolonged inactivity (> 1 year) | Human review required — may still be valuable |
| UNKNOWN | Insufficient data | Investigate manually |

**`ARCHIVE_CANDIDATE` does not mean the project is worthless or safe to delete.**
It means a human should review it before taking any action.

### Configuration

```bash
# Unix
export PROJECT_AUDIT_ROOTS=/home/user/projects:/home/user/work

# Windows
set PROJECT_AUDIT_ROOTS=C:\projects;C:\work
```

---

## Commit Archaeologist

**Purpose**: Investigate a file's Git history to understand why it exists, how it
evolved, and what would likely break if it were removed or changed.

**When to use**: Only when historical intent directly matters for a decision.
Never run automatically.

### Running the archaeologist

```bash
python .scripts/commit-archaeologist.py .scripts/idxtool.py
```

Or via Claude Code slash command: `/archaeologist <file-path>`

### Example output (`.scripts/idxtool.py`)

Running the archaeologist against `.scripts/idxtool.py` produces:

**1. Direct Git Evidence**
- Introduced: 2024-xx-xx by the original author
- 10+ commits over the file's history
- Largest change: added `--toc` recursive support
- Co-changed with: `TOC.md`, `prompts/*/TOC.md`

**2. Commit-Message Evidence**
- No issue references found (no `#NNN` patterns)
- 3 feature-addition commits (`add`, `added`)
- 1 fix commit

**3. Inferred Intent** _(labelled as inferred)_
- INFERRED: File was developed incrementally over multiple sessions
- INFERRED: Frequently co-changed with TOC.md, suggesting tight coupling

**4. Unknowns**
- No issue references — original motivation not traceable from Git alone

### Options

```
--max-commits N      Limit history to N commits (default: 50)
--format markdown    Output as Markdown instead of plain text
--output FILE        Write report to FILE
```

### Honesty guarantee

- All inferences are labelled `INFERRED:`.
- If history is silent on a question, it is listed under **Unknowns**.
- The tool will never fabricate intent when the Git history does not support it.

---

## Supermemory Pilot

**Purpose**: Repository-scoped memory for architectural decisions and context.

**Status**: Configuration ready. Requires `SUPERMEMORY_API_KEY` from
[console.supermemory.ai](https://console.supermemory.ai) to activate.

See [`memory-policy.md`](memory-policy.md) for the full authority order and
permitted/prohibited memory content.

### Activation

1. Copy `.env.example` to `.env`.
2. Set `SUPERMEMORY_API_KEY` in `.env` (never commit this file).
3. Claude Code will load `.mcp.json` automatically when you open the project.

### Available MCP tools (when connected)

| Tool | Description |
|------|-------------|
| `add_memory` | Explicitly save a decision or finding |
| `search_memory` | Retrieve previously saved context |
| `list_memories` | Browse stored memories |
| `delete_memory` | Remove a stale or incorrect memory |

### Authority order

1. Checked-in source files and specifications
2. CLAUDE.md and repository-level instructions
3. Reviewed project documentation
4. Supermemory recall ← **never overrides items 1–3**
5. Model inference

### Saving a decision

Use the `add_memory` MCP tool with this structure:

```
Decision: <what was decided>
Date: <YYYY-MM-DD>
Repository: LouisShark/chatgpt_system_prompt
Supporting: <file path or issue URL>
Status: active | superseded
Confidence: high | medium | low
Superseded-by: <later decision, if applicable>
```
