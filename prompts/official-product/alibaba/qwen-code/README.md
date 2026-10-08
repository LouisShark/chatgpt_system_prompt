# Qwen Code System Prompt

**Captured**: 2026-09-03, non-interactive (`-p`) mode. 28,266 characters, 23 tool definitions as sent.
**Captured from**: a local reverse proxy in front of the model API, recording the request the CLI actually sent while it ran unmodified.

| File | Contents |
| --- | --- |
| `QwenCodeSystem-gpt-5.6-sol-20260903.md` | The system prompt as sent |
| `tools-20260903.json` | The 23 tool definitions that travelled with it |

## The model is not the author

The model behind this capture is `gpt-5.6-sol`, not a Qwen model. The prompt still opens:

> You are Qwen Code, a non-interactive CLI agent developed by Alibaba Group, specializing in software engineering tasks.

That is why this is filed under Alibaba rather than under the model's vendor. Qwen Code drives whatever model it is pointed at, and the identity, the tool set and the instructions are the harness's, not the model's. A system prompt belongs to whoever assembled it.

## Provenance

Machine-identifying strings are replaced with placeholder tokens; nothing else is reworded or reordered. The prompt as sent is a few hundred characters longer than the count above, because the placeholders are shorter than the paths and names they replace.

- Source archive, with the capture method recorded per artifact: <https://github.com/Continuum-AI-Corp/OrcaPromptVault> (`Qwen/`)
- Capture tool: <https://github.com/Continuum-AI-Corp/OrcaReplay>
