# Claude Code System Prompts

**Current capture: 2.1.293 — 2026-10-08.** Captured from local `claude-trace` reverse-proxy JSONL of a `claude -p` (SDK-CLI) session. Main model: `claude-opus-5-5`; configured output style: **Explanatory**; CLI permission allowlist: `--allowedTools Agent` (this authorizes calls, but does not remove other schemas from the request).

This is a **mixed-version directory**, not a clean default interactive baseline. Six available subagent types were greeted and their replies summarized by the main agent. Every one returned `Hello!`. See `capture-summary-2-1-293.md` and `capture-manifest-2-1-293.json` for results and capture provenance.

## Current surfaces

| Surface | Version | Files |
| --- | --- | --- |
| Main system prompt | 2.1.293 | `ClaudeCodeSystem-2-1-293.md` |
| Main SDK loaded tools (11; placeholder excluded) | 2.1.293 | `core-tools-2-1-293.json` |
| Tool documentation (36 interactive built-ins + SubagentHandback) | 2.1.293 | `ClaudeCodeTools-2-1-293.md` |
| ReportFindings standalone schema | 2.1.293 | `ReportFindings-2-1-293.json` |
| Interactive core and full aggregate (14 + 22 = 36) | 2.1.293 | `core-tools-interactive-2-1-293.json`, `tools-2-1-293.json` |
| Interactive deferred names and all 22 full schemas | 2.1.293 | `deferred-tool-names-2-1-293.json`, `deferred-tools-2-1-293.json` |
| SDK deferred names and all 17 full schemas | 2.1.293 | `deferred-tool-names-sdk-2-1-293.json`, `deferred-tools-sdk-2-1-293.json` |
| Session title generator (automatically triggered) | 2.1.293 | `auxiliary/summarize_conversation-2-1-293.md` |
| Interactive static system prompt | 2.1.293 | `ClaudeCodeSystem-interactive-2-1-293.md` |
| Code Guide (interactive only in these tests) | 2.1.293 | `code_guide/*-2-1-293.*` |
| Runtime system message (partial) | 2.1.293 | `system-reminders-2-1-293.md` |
| Explore type: file search specialist | 2.1.293 | `file_search/*-2-1-293.*` |
| general-purpose type: generic task agent | 2.1.293 | `explore/*-2-1-293.*` |
| Plan type | 2.1.293 | `plan/*-2-1-293.*` |
| statusline-setup type | 2.1.293 | `status_line/*-2-1-293.*` |
| Background claude type | 2.1.293 | `claude/*-2-1-293.*` |
| codex:codex-rescue plugin type | 2.1.293 | `custom_agents/codex_rescue/*-2-1-293.*` |
| Wiki ingest and wiki lint (session-only plugin) | 2.1.293 | `custom_agents/claude_obsidian_wiki_{ingest,lint}/*-2-1-293.*` |
| Compact and job slug naming | 2.1.293 | `auxiliary/compact-2-1-293.md`, `auxiliary/slug_name-2-1-293.md` |
| Background result summary | 2.1.293 | `auxiliary/background_result_summary-2-1-293.md` |
| Safety evaluation wire protocol (not full monitor prompt) | 2.1.293 | `auxiliary/security-safeguards-2-1-293.{md,json}` |

Each subagent directory pairs its system prompt with the tools actually present in its captured request. `Explore` maps to `file_search/`; `general-purpose` maps to `explore/`.

## Retained legacy surfaces

| Surface | Last captured version | Why retained |
| --- | --- | --- |
| Security monitor system prompt | 2.1.220 | Latest tests exercised API safeguards but did not expose a separate monitor prompt |
| summarize_transcript_chunk, analyze_session_facets | 2.1.168 | Isolated synthetic insights capture still awaits authentication authorization |

Superseded 2.1.220 main/subagent files are replaced by their 2.1.293 captures. Earlier content remains in git history. The old 2.1.168 Code Guide and interactive aggregate are also replaced by successful 2.1.293 interactive captures.

## Observed changes from 2.1.220

- Main loaded catalog now includes `ListAgents` (11 callable schemas, versus 10 in the prior SDK-CLI capture).
- Child catalogs include `SubagentHandback`; all six children used it to return their reply. Child catalogs also changed; consult each JSON rather than assuming the main catalog applies to children.
- Main model was `claude-opus-5-5`; codex-rescue/statusline-setup used `claude-sonnet-5-5`.
- Per-session environment details and the Explanatory output-style blocks appear in the runtime `role: system` message. The static main prompt still has an Environment section describing models; read the static prompt and runtime message together.
- A supplemental ToolSearch `select:` call loaded all 17 advertised deferred built-ins. Their full descriptions, input schemas and request flags are preserved. The prior 19-schema 2.1.220 catalog is superseded; differences reflect this observed SDK surface, not proof of product-wide tool removal.

## Capture scope and normalization

This is a targeted hello session in SDK-CLI mode with local plugins/settings and Explanatory output style. The SDK and interactive captures include every advertised deferred built-in schema in each mode. The interactive session retained the configured Explanatory style and local plugins/settings, so it is not a clean default baseline; disabled agent availability and untriggered auxiliary prompts remain unverified. The Agent schema mentions `fork`, but that type was absent from the available-type roster and was not called.

Only successful request bodies are used for prompt/schema extraction. The reserved `DeferredToolPlaceholder` is omitted from exported catalogs, as in prior captures. JSON preserves flags such as `eager_input_streaming`.

Local paths become `{{working_directory}}`, `{{memory_directory}}`, `{{claude_config_dir}}`, and `{{home}}`; billing-header request suffixes become `cc_version=2.1.293.XXX`. Installation-specific MCP context/ready tools and the skill roster are placeholdered in runtime reminders. Private global CLAUDE.md contents, user identity, git history, authentication headers and raw responses are not copied into prompt snapshots.

Raw JSONL/HTML stay local outside the tracked project. `capture-manifest-2-1-293.json` records the trace SHA-256 and request row references; `capture-summary-2-1-293.md` records the greeting outcome. No commit or publication is performed by this update.

## Interactive follow-up: Code Guide and full deferred schemas

Code Guide is **available in the interactive CLI**: an actual `Agent` call loaded its specialist prompt on `claude-haiku-5-5` and returned `Hello` via `SubagentHandback`. The same agent type returned a local not-found error in SDK-CLI mode. This is an observed mode difference, not product-wide removal. The configuration section of the guide prompt is placeholdered.

Interactive mode advertises 22 deferred built-ins; all 22 were loaded without executing them. Five are additional to the SDK set: `ArtifactComments`, `ArtifactData`, `EndConversation`, `EnterPlanMode`, `ExitPlanMode`. Interactive core also includes `Artifact`, `AskUserQuestion`, `SendFeedback`. The 36-tool aggregate is taken from an actual fully loaded interactive request, rather than combining unrelated catalogs.

## Auxiliary/plugin follow-up

The local Obsidian plugin 1.6.0 was explicitly loaded only for the capture session using `--plugin-dir`; global plugin settings were not changed. Both wiki-ingest and wiki-lint ran on `claude-sonnet-5-5` and returned `Hello` via SubagentHandback without accessing a vault.

`/compact` was invoked against the dedicated Code Guide/schema-loading test conversation. Its summarization instructions are a **user-message suffix**, while the normal agent system prompt and existing tool schemas remain in the request; only that actual compact suffix is saved in the auxiliary prompt file. Its custom instructions are placeholdered.

The slug prompt was captured by keeping claude-trace's native reverse proxy alive for a background Hello job. That same test also triggered a background result-summary prompt. User/agent text and existing job labels are placeholdered. All created background tests were stopped after capture.

The safe temporary-file test exercised the `dangerous_tool_use` API safeguard. Its configuration and evaluated result are captured; no separate security-monitor system prompt was transmitted, so the old prompt remains explicitly historical. Insights analysis and chunk-summary fixtures are prepared in an isolated config directory containing no real user history; they have not yet run because using the existing credential in that isolated process requires a separate authorization.
