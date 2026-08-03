# Commit Archaeologist

Investigates the Git history of a specific file to answer questions like:

- Why was this file introduced?
- Which commits established this behaviour?
- Which files historically change together with this one?
- Was this a deliberate decision or a temporary workaround?
- Which issue, PR, or commit explains the current design?

**Manual use only.** Never run automatically on every session or commit.

## Usage

```bash
python .scripts/commit-archaeologist.py <file-path>
```

### Examples

```bash
# Investigate the main indexing tool:
python .scripts/commit-archaeologist.py .scripts/idxtool.py

# Limit to the 20 most recent commits:
python .scripts/commit-archaeologist.py .scripts/idxtool.py --max-commits 20

# Write a Markdown report:
python .scripts/commit-archaeologist.py .scripts/idxtool.py --format markdown --output arch-idxtool.md
```

## Output sections

| Section | Content |
|---------|---------|
| 1. Direct Git Evidence | Commits, dates, authors, file stats, co-changed files |
| 2. Commit-Message Evidence | Issue/PR references, fix keywords, workaround signals |
| 3. Inferred Intent | Pattern-based interpretation — always labelled as INFERRED |
| 4. Unknowns | Gaps where the history is silent |

## Honesty guarantee

This tool will not fabricate historical intent.
- All inferences are explicitly labelled `INFERRED:`.
- If the history is silent on a question, it is listed under **Unknowns**.
- Commit messages are reproduced verbatim — not paraphrased.

## When to use

Use Commit Archaeologist when historical intent matters for a decision, for example:
- Deciding whether a file can safely be deleted or refactored.
- Understanding why a seemingly odd implementation choice exists.
- Attributing a design decision to a specific issue or discussion.
- Investigating a regression — which commits changed the relevant behaviour.
