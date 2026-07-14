# Codex Desktop GPT-5.6 Sol Prompt Snapshot

This directory preserves the GPT-5.6 Sol Codex Desktop snapshot published in
[`elder-plinius/CL4R1T4S`](https://github.com/elder-plinius/CL4R1T4S/tree/34d6ca0e16217d62727c16ba1f30265540abaa9d/OPENAI/Codex_Desktop)
at upstream commit `34d6ca0e16217d62727c16ba1f30265540abaa9d`.
The two capture files are copied byte-for-byte; this README adds provenance and
scope notes only.

## Contents

| File | Scope | Size |
| --- | --- | ---: |
| `5.6-Sol_SystemPrompt.md` | Composed Codex Desktop system prompt | 4,270 lines / 300,534 bytes |
| `5.6-Sol_Tools.json` | Tool catalog JSON | 148 entries / 394,539 bytes |
| `LICENSE-AGPL-3.0.txt` | Copy of the upstream repository license | 661 lines / 34,523 bytes |

The tool catalog contains 146 named records plus the `web_search` and
`tool_search` descriptors. It includes core runtime tools, Codex Desktop app
tools, MCP tools, plugin tools, deferred tools, and compatibility aliases; it
should not be read as a minimal catalog available in every session.

## Model identification

The upstream filenames identify this snapshot as **GPT-5.6 Sol**. The tool
catalog independently contains the runtime model ID `gpt-5.6-sol` and lists the
Sol, Terra, and Luna GPT-5.6 variants in Codex thread-management schemas. The
system prompt itself uses the broader opening `an agent based on GPT-5` and does
not state `GPT-5.6 Sol`.

This is an archival copy of a third-party extraction, not an independently
verified OpenAI release artifact. Model identity, capture completeness, and
whether a section is invariant across Codex Desktop sessions have not been
verified against a second capture.

## Capture caveats

- The system prompt is a composed runtime prompt, not only a model-level base
  prompt. It includes desktop app context, permission policy, skills, plugins,
  connector guidance, memory instructions, and visualization guidance.
- Dynamic values are represented by placeholders such as `[CURRENT_DATE]`,
  `[TIMEZONE]`, `[SKILL_PATH]`, and sandbox configuration markers.
- Tool availability is profile-dependent. Some records are duplicated across
  namespaced and compatibility surfaces, while deferred tools may require
  discovery before use.
- No local user path, email address, API key, bearer token, or GitHub token was
  found by the import-time residual-secret scan.

## Integrity

SHA-256 checksums of the imported capture files:

```text
b247f30e23380fc48794756f3ee0ee7e370d008967bca7ae2a13efe3f160c51e  5.6-Sol_SystemPrompt.md
bad68475f1f20cc001850e83d440dd16d3c9ea29b4fe66ea6d97bafdf072c0ef  5.6-Sol_Tools.json
```

The upstream repository is distributed under the GNU Affero General Public
License v3. A copy is included as `LICENSE-AGPL-3.0.txt`; review the upstream
terms before redistributing or modifying these imported files.
