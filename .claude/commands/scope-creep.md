# Scope Creep Detector

Compares the current Git diff against a stated intended change and reports PASS, WARN, or FAIL.

Run this before declaring any substantial change complete.

## Usage

```bash
python .scripts/scope-creep-detector.py --intended-change "$ARGUMENTS"
```

Or, if you have a base branch to compare against:

```bash
python .scripts/scope-creep-detector.py --intended-change "$ARGUMENTS" --base main
```

## What it checks

- Number of files changed
- Line-volume of changes
- Dependency file modifications (`requirements.txt`, `package.json`, etc.)
- CI/workflow configuration changes (`.github/workflows/`)
- Non-CI configuration file changes (`.yaml`, `.json`, `.toml`, etc.)
- Auto-generated files in the diff
- New public Python symbols introduced
- Unrelated documentation changes
- Changes scattered across many unrelated directories

## How to state the intended change

Pass a single concise sentence describing what the change is supposed to do.

```
--intended-change "Add --template flag to idxtool.py for creating new GPT stubs"
```

## Output codes

| Result | Meaning | Action |
|--------|---------|--------|
| PASS | Change is consistent with stated intent | Proceed |
| WARN | Potential scope creep detected | Review before merging |
| FAIL | Significant scope creep detected | Revise change or justify exceptions |

## Handling false positives

A WARN or FAIL does not block you — it is advisory.  If the finding is a false
positive (e.g. generated files like `TOC.md` are expected), document the reason
in your PR description.

Common false positives:
- `TOC.md` changes flagged as "generated files" — expected after prompts/ additions.
- `.github/badges/tokens.svg` flagged as generated — expected.
- Docs changes flagged when the change genuinely improves documentation.

## Examples

**Acceptable**:
- Intended: "Fix sorting bug in idxtool.py" → 2 files changed in `.scripts/` → PASS

**Requires review**:
- Intended: "Fix typo in README" → 15 files changed including `.scripts/` → WARN

**Scope creep**:
- Intended: "Add GPT template" → CI workflows, requirements.txt, and 30 docs files changed → FAIL
