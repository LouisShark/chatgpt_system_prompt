# Rollback Instructions

This document explains how to undo each part of the `chore/claude-code-harness-upgrade` changes.

---

## 1. Disable Scope Creep Detector

**Temporary disable (keep files)**:

Remove or rename the optional CI workflow:
```bash
git mv .github/workflows/scope-creep-check.yml .github/workflows/scope-creep-check.yml.disabled
git commit -m "chore: disable scope-creep CI check"
```

The scripts and commands remain available for manual use.

**Full removal** (see §7 for complete removal of all harness files).

---

## 2. Disable Project Graveyard

The graveyard script is manual-only — there is no CI workflow to disable.

To remove the Claude Code command:
```bash
git rm .claude/commands/graveyard.md
git commit -m "chore: remove graveyard Claude Code command"
```

---

## 3. Disable Commit Archaeologist

The archaeologist is manual-only — no automation to disable.

To remove the Claude Code command:
```bash
git rm .claude/commands/archaeologist.md
git commit -m "chore: remove archaeologist Claude Code command"
```

---

## 4. Disable Supermemory (keep config)

To stop Supermemory from loading without removing configuration:

1. Open `.mcp.json`.
2. Comment out or remove the `supermemory` server entry.
3. Restart Claude Code.

No commit required unless you want to persist the change.

---

## 5. Fully Remove Supermemory

```bash
# Remove MCP configuration:
git rm .mcp.json

# Remove environment template:
git rm .env.example

# Delete your local .env (already gitignored, not tracked):
rm .env        # Unix
del .env       # Windows

git commit -m "chore: remove Supermemory MCP pilot"
```

To also delete stored memories, log in to
[console.supermemory.ai](https://console.supermemory.ai) and delete all
memories associated with this repository, or call `delete_memory` for each
stored item via the MCP tool before removing the configuration.

**Verify removal**: Open Claude Code; confirm Supermemory tools are no longer
listed in available MCP tools.

---

## 6. Remove CLAUDE.md

Only remove `CLAUDE.md` if you want to restore the pre-upgrade state entirely.
If Claude Code behaviour needs adjusting, edit the file rather than deleting it.

```bash
git rm CLAUDE.md
git commit -m "chore: remove CLAUDE.md (harness rollback)"
```

---

## 7. Complete Rollback (all files)

```bash
git rm CLAUDE.md
git rm .mcp.json
git rm .env.example
git rm .claude/commands/scope-creep.md
git rm .claude/commands/graveyard.md
git rm .claude/commands/archaeologist.md
git rm .scripts/scope-creep-detector.py
git rm .scripts/project-graveyard.py
git rm .scripts/commit-archaeologist.py
git rm -r docs/ai-harness/
git commit -m "chore: revert Claude Code harness upgrade"
```

Then undo the `.gitignore` addition manually by removing the `.env` line that
was appended at the end of the file, and commit:

```bash
git add .gitignore
git commit -m "chore: revert .env gitignore entry (harness rollback)"
```

---

## 8. Verify Removal

After rollback, confirm:

```bash
# No harness files remain:
git ls-files CLAUDE.md .mcp.json .env.example .claude/ docs/ai-harness/ \
    .scripts/scope-creep-detector.py \
    .scripts/project-graveyard.py \
    .scripts/commit-archaeologist.py

# Should print nothing.

# Supermemory not in MCP servers:
# Open Claude Code → MCP tools panel → confirm no 'supermemory' entry.
```

---

## 9. Restoring Modified Files

The only existing file modified by this upgrade (beyond new files) is `.gitignore`
(one `.env` line appended).

To restore it:

```bash
git show main:.gitignore > .gitignore
git add .gitignore
git commit -m "chore: restore .gitignore to pre-upgrade state"
```
