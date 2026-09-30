# MiniMax Code System Prompts

**Version**: `mcode` 0.4.12, captured 2026-09-20.
**Captured from**: a local reverse proxy in front of the model API, recording the request the CLI actually sent while it ran unmodified. Model that answered: `deepseek-v4-flash-free`.

> **MiniMax Code ships three system prompts, not one.** `mcode` picks one per `--prompt-mode`, and they are three separate documents rather than one document with a conditional inside it. All three are here.

## Prompt matrix

| `--prompt-mode` | File | Characters | Opening identity |
| --- | --- | --: | --- |
| `tui` (default) | `MiniMaxCodeSystem-tui-0-4-12.md` | 14,675 | "a coding agent running in the MiniMax Code terminal" |
| `coding` | `MiniMaxCodeSystem-coding-0-4-12.md` | 16,055 | "You run inside MiniMax Code, a workspace… software engineering" |
| `work` | `MiniMaxCodeSystem-work-0-4-12.md` | 17,619 | "You run inside MiniMax Code, a workspace… research, analyze" |

What actually differs between them: `coding` swaps the `Deliverable Files` section for `Media Output`, and `work` adds an `Artifact Completion Contract` on top of that. The rest is shared.

## Tools

`tools-0-4-12.json` — 18 tool definitions. The three modes declare the **same** tool set; the three captures came out byte-identical, so one file covers all three. The surface changes what the agent is told to produce, not what it can reach.

## The model is not the variable

Seven models across six labs — MiniMax, DeepSeek, OpenAI, Kimi, GLM, Hunyuan — driven through the same surface produced prompts identical line for line, except for one line, `- Model: <id>`. The tool set never moved.

That is expected once you look at the package: the prompts are Handlebars templates shipped inside `mcode` at `assets/agents/_v2/*/SYSTEM.md.hbs`, not fetched from a server, and none of their conditionals branches on a model or a provider. The model named in a capture is the one that answered, not a variant of the prompt.

## Provenance

Machine-identifying strings are replaced with placeholder tokens; nothing else is reworded or reordered. The prompt as sent is a few hundred characters longer than the counts above, because the placeholders are shorter than the paths and names they replace.

- Source archive, with the capture method recorded per artifact: <https://github.com/Continuum-AI-Corp/OrcaPromptVault> (`MiniMax-Code/`)
- Capture tool: <https://github.com/Continuum-AI-Corp/OrcaReplay>
- Upstream package: <https://github.com/MiniMax-AI/minimax-code>
