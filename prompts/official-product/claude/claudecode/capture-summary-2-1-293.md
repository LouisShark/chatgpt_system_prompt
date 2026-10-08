# Subagent hello capture — Claude Code 2.1.293

Captured on 2026-10-08 (Asia/Shanghai) using local `claude-trace --include-all-requests --run-with -p` with `--allowedTools Agent` and JSON output. Default configured model/style were preserved.

The main agent was asked to greet every available subagent, wait for every reply, and summarize their original responses; no project file reads/writes, shell execution or external-service tool calls were requested.

| Agent type | Model | Original reply |
| --- | --- | --- |
| `Plan` | `claude-opus-5-5` | `Hello!` |
| `codex:codex-rescue` | `claude-sonnet-5-5` | `Hello!` |
| `Explore` | `claude-opus-5-5` | `Hello!` |
| `statusline-setup` | `claude-sonnet-5-5` | `Hello!` |
| `general-purpose` | `claude-opus-5-5` | `Hello!` |
| `claude` | `claude-opus-5-5` | `Hello!` |

All six types completed successfully. The main agent's final response confirmed six successes, no failures and no refusals. Wire responses show each child returning `Hello!` via `SubagentHandback`; only the background `claude` agent additionally emitted a visible `Hello!` text block. No child response in this trace called Bash/Read/Edit/Write. The main response called only Agent.

`fork` is mentioned in the Agent schema but was not in the advertised available-type roster, so it was not invoked. Disabled wiki agents and unavailable Code Guide were not invoked. Plugin security-guidance generated additional zero-tool review requests; these are not additional spawned subagents and are not classified as the legacy security-monitor surface.

Raw JSONL/HTML contain local context and remain outside the tracked prompt directory. The manifest records its SHA-256 and source row numbers (one-based); sanitized prompt/tool files are derived directly from successful request bodies.

## Supplemental deferred/Code Guide capture

All 17 advertised built-in deferred tools were force-loaded in one ToolSearch `select:` query. The next successful request carries all 17 full schema objects marked `defer_loading: true`. None of those tools was executed. See `deferred-tools-2-1-293.json`.

An actual Agent call with `subagent_type: "claude-code-guide"` failed locally in SDK-CLI mode:

```text
Agent type 'claude-code-guide' not found. Available agents: claude, codex:codex-rescue, Explore, general-purpose, Plan, statusline-setup
```

This proves the type was unavailable in this SDK session; it does not prove Code Guide was removed from Claude Code. Its implementation remains present in the installed 2.1.293 native binary.

## Interactive verification

Code Guide remains available in the interactive CLI. Its actual specialist prompt was captured on `claude-haiku-5-5`, with Bash, Read, WebFetch, WebSearch and SubagentHandback schemas; it returned `Hello` using SubagentHandback and performed no research/file tool call. The SDK-CLI not-found result is therefore a mode-specific limitation.

All 22 interactive deferred built-ins were loaded without execution. A subsequent successful request contains the 36 built-in schemas (14 core + 22 deferred) exported in `tools-2-1-293.json`. The 17-schema SDK deferred catalog remains separately preserved.

The interactive session automatically triggered the session-title generator. Its new prompt and placeholdered user template replace the 2.1.168 title prompt.

## Remaining auxiliary/plugin follow-up

Both temporarily loaded Wiki Agent types replied `Hello`, calling only SubagentHandback. The compact operation completed on the synthetic Code Guide/ToolSearch session with text-only output. The background Hello test produced the latest slug prompt plus a result-summary prompt. These replace the old compact/slug/wiki snapshots with actual 2.1.293 captures.

The safety fixture's Bash action was evaluated by the API `dangerous_tool_use` safeguard and returned `not_flagged`. The complete sanitized request safeguard object and evaluated response result are preserved separately. No full security-monitor system prompt was observed; the 2.1.220 prompt remains historical.

The prepared insights fixture is artificial and isolated from real history. Facet-analysis and transcript-chunk-summary captures are pending separate authorization for in-memory use of the existing Claude credential. No Keychain credential has been extracted for that fixture.
