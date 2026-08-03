# Project Graveyard

Audits project directories for dormancy, duplication, and unclear status.

This is a DRY-RUN ONLY tool.  It never deletes, archives, moves, or modifies any project.

## Usage

```bash
# Audit the current repository:
python .scripts/project-graveyard.py --roots .

# Audit a folder that contains multiple project subdirectories:
python .scripts/project-graveyard.py --roots /path/to/projects

# Use the PROJECT_AUDIT_ROOTS environment variable:
PROJECT_AUDIT_ROOTS=/path/to/projects python .scripts/project-graveyard.py

# Write a Markdown report:
python .scripts/project-graveyard.py --roots . --format markdown --output graveyard-report.md
```

## Classifications

| Label | Meaning |
|-------|---------|
| ACTIVE | Recently active (last commit ≤ 30 days), clear purpose |
| MAINTAIN | Moderately active (≤ 90 days), stable maintenance mode |
| REVIEW | Mixed signals — needs human review |
| DORMANT | No recent activity (≤ 365 days) but may still be relevant |
| ARCHIVE_CANDIDATE | Prolonged inactivity (> 365 days) — human review required |
| UNKNOWN | Insufficient data to classify |

## Important

- `ARCHIVE_CANDIDATE` does NOT mean the project is worthless or safe to delete.
- Never archive or delete a project based solely on this output.
- A human must review any project before taking action.
- Sensitive-data indicators automatically promote a project to REVIEW even if dormant.

## Configuration

Set `PROJECT_AUDIT_ROOTS` in your `.env` file or environment:

```bash
# Unix (colon-separated):
export PROJECT_AUDIT_ROOTS=/home/user/projects:/home/user/work

# Windows (semicolon-separated):
set PROJECT_AUDIT_ROOTS=C:\projects;C:\work
```
