# Claude Code System Prompts

**Version**: 2.1.133 (May 2026)
**Captured from**: `claude-cli/2.1.133` — two live traces.
- **Trace 1**: `log-2026-05-08-06-36-15.jsonl` (70 API calls, cc_version `2.1.133.4b3` and related `2.1.133.*` sub-revisions). Covers the main agent (with ToolSearch active, including a mid-session `ToolSearch select:ExitPlanMode`) plus first-turn invocations of every published sub-agent: Plan, Explore, File Search, Code Guide, Status Line. Auxiliary calls captured in this trace: `summarize_conversation` (haiku-4-5), `slug_name` (haiku-4-5), and the two newly-discovered `summarize_transcript_chunk` / `analyze_session_facets` opus-4-7 prompts.
- **Trace 2**: `log-2026-05-08-09-01-48.jsonl` (5 API calls). A separate session that fired a `/compact` invocation — captured at `req 3` (with retry at `req 4`). This trace is what makes the `/compact` auxiliary prompt **trace-verified** for v2.1.133 (it had been carried over from v2.1.118 unverified after trace 1).

## Summary of Changes (this update)

A one-shot audit-honest update of every file in this directory, derived from a single v2.1.133 trace, after **two audit passes**: the first pass missed 3 things (`ExitPlanMode` schema and the two `summarize_transcript_chunk`/`analyze_session_facets` auxiliary prompts), all caught and corrected on a second pass that walked all 70 requests in the trace instead of just the first 13.

### Files renamed (18) — `*-2-1-118.* → *-2-1-133.*`

All eight `.md` prompts and ten `.json` tool catalogs across the root, sub-agent, and auxiliary directories were renamed via `git mv` so version history follows.

### Files added (2) — net-new auxiliary prompts

Discovered on the second audit pass:

- [`auxiliary/summarize_transcript_chunk-2-1-133.md`](auxiliary/summarize_transcript_chunk-2-1-133.md) — runs on `claude-opus-4-7` with system greeting "You are a Claude agent, built on Anthropic's Claude Agent SDK." Asks the model to summarize a session transcript chunk in 3-5 sentences. Captured byte-exact from req 16, with 4 total invocations (req 16, 64-66) all sharing the same boilerplate.
- [`auxiliary/analyze_session_facets-2-1-133.md`](auxiliary/analyze_session_facets-2-1-133.md) — same greeting / model. Asks the model to extract structured JSON facets (goal categories, satisfaction signals, friction types, etc.) from a session dump. Captured from req 17-63 + 67-69 (50 invocations, all sharing the same boilerplate around `{{session_dump}}`).

### Substantive content changes (trace-verified)

| Layer | Change | Source |
|---|---|---|
| **Main agent system prompt** | `# Executing actions with care` collapsed from a 5-paragraph block to **a single paragraph**. New clarifying-question paragraph appended to `# Text output`. Trailing context-management line wrapped in a new `# Context management` heading. Section-bullet style re-indented (` - …`). | `req 2` body, byte-exact |
| **Main agent tool catalog** | `AskUserQuestion` promoted from **deferred → core**: catalog now 9 core + 21 deferred (was 8 + 22). Total built-in count still 30. Deferred-tools `<system-reminder>` enumerates 21 entries. | `req 2` core dump |
| **Tool schemas** | All 26 captured schemas gained top-level `"eager_input_streaming": true` exactly as observed. | `req 2`, `req 9-13` |
| **Tool description deltas** | `Agent`: Explore subagent description rewritten with stricter guard rails ("Do NOT use it for code review …"). `Bash`: new `find from .` instruction; `run_in_background` description simplified. `Monitor`: rewritten as a "Pick by how many notifications you need" decision matrix with a `gh pr checks` example. `EnterWorktree`: added `worktree.baseRef` semantics. `RemoteTrigger`: appended summary-line + claude.ai URL note. `WebSearch`: month roll April → May 2026. | `req 2` + `req 10` |
| **Status Line agent JSON spec** | `total_input_tokens` / `total_output_tokens` descriptions reworded; **new** `effort.level` block (low/medium/high/xhigh/max) and `thinking.enabled` block added to the documented stdin schema. | `req 11` body |
| **Code Guide template** | Removed the `**Available plugin skills:**` section that no longer appears in the v2.1.133 trace. | `req 9` body |
| **System reminders** | Deferred Tools List dropped `AskUserQuestion` (now 21 entries). All 7 reminder templates structurally unchanged. | `req 2` `msg[0]` |
| **Plan / Explore / File Search prompts** | Byte-identical to v2.1.118 — only the version tag in the filename changed. | `req 12, 13, 10` |
| **Auxiliary prompts** | `summarize_conversation` and `slug_name` byte-identical to v2.1.118. `compact` not invoked this trace; carried over. | `req 3, 7` |

### Audit corrections (caught and fixed during multi-pass review)

Three over-reaches and three omissions were found across two audit passes; all corrected before final publication:

**First-pass over-reaches (corrected on second pass):**

1. **Originally claimed all 30 tool schemas were captured; actually only 26 were directly observed in req 2 + req 10.** The first pass carried v2.1.118 schemas forward for the unobserved tools with `eager_input_streaming` stamped on top, which would have looked like a v2.1.133 capture without being one. Those entries were **excluded** from the JSON; their sections in `ClaudeCodeTools-2-1-133.md` were tagged with a `⚠️ Schema NOT verified for v2.1.133` warning.
2. **`**Available plugin skills:**` section in `code_guide/ClaudeCodeGuideAgent-2-1-133.md` is absent from the trace and absent from the published file.** The v2.1.118 template carried this block; the v2.1.133 trace does not. There are two possible explanations and we cannot distinguish them from a single trace: (a) the template was removed in v2.1.133, or (b) the harness conditionally renders the section and omits it when the plugin-skills list is empty (the user has `pyright-lsp` enabled, but `pyright-lsp` is an LSP and likely ships no skills). The published file follows the trace literally — no plugin-skills block — so it stays byte-exact with what was actually transmitted. A future trace from a user whose plugin ships at least one skill would settle (a) vs (b).

**Second-pass omissions (only caught after the user pushed me to verify exhaustively):**

3. **`ExitPlanMode` schema was actually captured in the trace** — req 5 invoked `ToolSearch select:ExitPlanMode` and req 6 onward carried the schema. I had skipped req 14+ on the first pass because their `sys_chars=143` looked uninteresting; on the second pass I walked every tools array and found `ExitPlanMode` had been loaded. It is now in `tools-2-1-133.json` (27/30) and the warning was removed from its section in `ClaudeCodeTools-2-1-133.md`.
4. **Two entire auxiliary prompts were missing from the published files** — req 16 (`summarize_transcript_chunk`) and req 17-69 (`analyze_session_facets`, 53 invocations). Both run on `claude-opus-4-7` with the system greeting *"You are a Claude agent, built on Anthropic's Claude Agent SDK."* (different from the main Claude Code prompts). I had skipped req 16+ initially because the *system* prompt was tiny (62 chars) and looked like noise — but the actual prompt body lives in the user message, not the system field. Both files were added on the second pass.

### Final audit verdict (18 / 18 byte-exact across both traces)

```
SYSTEM PROMPTS (7/7)              TOOL JSON FILES (8/8)
  ClaudeCodeSystem-2-1-133.md       core-tools-2-1-133.json (9)
  plan/ClaudeCodePlanMode           plan/core-tools (5)
  explore/ClaudeCodeExplore         explore/core-tools (7)
  file_search/ClaudeCodeFile…       code_guide/tools (4)
  status_line/ClaudeCodeStatus…     status_line/tools (2)
  code_guide/ClaudeCodeGuide…       file_search/tools (21)
                                    tools-2-1-133.json (27 verified)
AUXILIARY (5/5)                     tools-2-1-133.json correctly
  summarize_conversation              excludes 3 unverified tools
  slug_name                           (EnterPlanMode, NotebookEdit, TaskOutput)
  summarize_transcript_chunk
  analyze_session_facets
  compact (TRACE-VERIFIED via trace 2 — was carried over before)
```

### Privacy

User-specific values (working dir, MCP servers, settings.json, email, sandbox JSON) were replaced with `{{...}}` placeholders. The user's 17 `mcp__claude_ai_*` tools were stripped from the published `file_search/tools-2-1-133.json` snapshot. A repo-wide grep for the user's name, email, and project paths confirms zero leaks.

---

## What Changed in v2.1.133 (vs v2.1.118)

### 1. `AskUserQuestion` promoted from deferred → core (main agent)

The main agent now ships **9 core tools** instead of 8. `AskUserQuestion` no longer appears in the deferred-tools list — it loads upfront with the rest of the core set, removing one ToolSearch round-trip whenever the model wants to surface a multiple-choice question. The total built-in catalog stays at **30** (now **9 core + 21 deferred**, was 8 core + 22 deferred).

| Agent       | v2.1.118 core tools                                                | v2.1.133 core tools                                                                | Delta              |
| ----------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------ |
| Main        | 8 (Agent, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write) | **9** (Agent, **AskUserQuestion**, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write) | +AskUserQuestion   |
| Explore     | 7                                                                  | 7                                                                                  | unchanged          |
| Plan        | 5                                                                  | 5                                                                                  | unchanged          |
| File Search | 21                                                                 | 21                                                                                 | unchanged          |
| Code Guide  | 4 (Bash, Read, WebFetch, WebSearch)                                | 4                                                                                  | unchanged          |
| Status Line | 2 (Read, Edit)                                                     | 2                                                                                  | unchanged          |

The deferred-tools `<system-reminder>` likewise drops AskUserQuestion. The full v2.1.133 deferred list (21 built-in entries — MCP tool names append at runtime) is:

```
CronCreate, CronDelete, CronList, EnterPlanMode, EnterWorktree,
ExitPlanMode, ExitWorktree, ListMcpResourcesTool, Monitor,
NotebookEdit, PushNotification, ReadMcpResourceTool, RemoteTrigger,
TaskCreate, TaskGet, TaskList, TaskOutput, TaskStop, TaskUpdate,
WebFetch, WebSearch
```

### 2. Tool schemas: every captured tool gained `"eager_input_streaming": true`

Every tool schema observed in this trace — across every agent — carries a top-level `"eager_input_streaming": true` field. This is a hint to the Anthropic API that the harness will stream the model's tool input back to the user as it is produced rather than buffering until the call is fully serialized. No behavioral effect on the model's prompt; it only affects how the harness renders streaming tool calls in the UI.

> Whether the four uncaptured deferred tools (`EnterPlanMode`, `ExitPlanMode`, `NotebookEdit`, `TaskOutput`) also gained the field is **not confirmed**. The audit refuses to assert it on their behalf.

### 3. Tool description changes (4 tools with substantive edits)

- **`Agent` (Explore subagent description)** — rewritten with stronger guard rails. v2.1.118 said *"Fast agent specialized for exploring codebases ... search code for keywords ... answer questions about the codebase ('how do API endpoints work?')."* v2.1.133 narrows the role: *"Fast read-only search agent for locating code. ... Do NOT use it for code review, design-doc auditing, cross-file consistency checks, or open-ended analysis — it reads excerpts rather than whole files and will miss content past its read window."* The thoroughness labels are reworded: *"specify search breadth: 'quick' for a single targeted lookup, 'medium' for moderate exploration, or 'very thorough' to search across multiple locations and naming conventions."*
- **`Bash`**:
  - **Added** under `# Instructions`: *"When running `find`, search from `.` (or a specific path), not `/` — scanning the full filesystem can exhaust system resources on large trees."*
  - `run_in_background` parameter description simplified: `"Set to true to run this command in the background. Use Read to read the output later."` → `"Set to true to run this command in the background."`
  - The git/cd/`find -regex`/`--no-edit` guidance from v2.1.118 carries over unchanged.
- **`Monitor`** — significantly rewritten. The old "streaming case" framing is replaced with a "Pick by how many notifications you need" decision matrix that explicitly steers single-shot waits to `Bash run_in_background` and gives Monitor a per-occurrence-with-natural-end example using `gh pr checks` polling. New cautionary line: *"Don't use an unbounded command for a single notification."*
- **`EnterWorktree`** — clarified `worktree.baseRef` setting. Old: *"creates a new git worktree inside `.claude/worktrees/` with a new branch based on HEAD"*. New: *"creates a new git worktree inside `.claude/worktrees/` on a new branch. The base ref is governed by the `worktree.baseRef` setting: `fresh` (default) branches from origin/<default-branch>; `head` branches from your current local HEAD."*
- **`RemoteTrigger`** — appended a sentence about the response now including a server-parsed run-time line and the routine's claude.ai URL: *"For create/update, a summary line is appended with the server-parsed run time and the routine's claude.ai URL — relay both to the user so they can confirm the time is right and know where the result will appear."*
- **`WebSearch`** — date roll: `"The current month is April 2026."` → `"The current month is May 2026."` (rest is byte-identical).
- **`EnterPlanMode`, `ExitPlanMode`, `NotebookEdit`, `TaskOutput`** — **not re-captured**. The trace did not call `ToolSearch select:` on any of them, so neither the description text nor the parameter schema can be confirmed for v2.1.133. They are excluded from `tools-2-1-133.json` and tagged with a "schema NOT verified" warning in `ClaudeCodeTools-2-1-133.md`.

### 4. Main-agent prompt — three section-level changes

- **`# Executing actions with care`** is **dramatically shortened**.
  - v2.1.118 had two long paragraphs plus a bulleted list of risky-action examples and an obstacle-handling addendum.
  - v2.1.133 collapses the whole section to a single paragraph: *"Read, search, and investigate freely — looking is not acting. For actions that are hard to reverse, affect shared systems, or are otherwise risky (deleting data, force-pushing, sending messages, modifying shared infrastructure), confirm with the user before proceeding unless durably authorized. Approval in one context doesn't extend to the next."*
- **`# Text output (does not apply to tool calls)`** — adds a **new clarifying-question paragraph** at the end:

  > Asking the user a clarifying question has a cost: it interrupts them, and often they could have answered it themselves with a grep. Before asking, spend up to a minute on read-only investigation (grep the codebase, check docs, search memory) so your question is specific. "I found tunnels X and Y in the config — which one?" beats "what tunnel?"

- **End of prompt** — the trailing line *"When working with tool results, write down any important information you might need later in your response, as the original tool result may be cleared later."* is now wrapped under a new `# Context management` heading (in v2.1.118 it was a bare line below `# Environment`).
- Bullet style: section bullets are formatted with a leading single space (` - All text...`) rather than no leading space, with no blank line under each `# Section` heading. This is a cosmetic re-indentation only.

All other sections (`# System`, `# Doing tasks`, `# Using your tools`, `# Tone and style`, `# Session-specific guidance`, `# auto memory`, `# Environment`) are byte-identical to v2.1.118.

### 5. Sub-agent prompt micro-edits

- **Status Line agent (sonnet-4-6)** — three changes to the JSON schema documentation:
  - `total_input_tokens` description: *"Total input tokens used in session (cumulative)"* → *"Input tokens currently in the context window (incl. cache reads/writes)"*
  - `total_output_tokens` description: *"Total output tokens used in session (cumulative)"* → *"Output tokens from the most recent API response"*
  - **New** `effort` block: `"effort": { "level": "low" | "medium" | "high" | "xhigh" | "max" }` — only present when the model supports reasoning effort (e.g. extended-thinking-enabled models).
  - **New** `thinking` block: `"thinking": { "enabled": boolean }` — flags whether extended thinking is on for the session.
- **Plan / Explore / File Search / Code Guide agents** — system prompt bodies are byte-identical to v2.1.118. Tool catalogs unchanged. (Code Guide agent's `{{user_skills_list}}`, `{{user_mcp_servers}}`, `{{user_settings_json}}` injection points are still populated at runtime; the trace shows a 30 KB body once those expand.)

### 6. Auxiliary prompts

- `auxiliary/summarize_conversation-2-1-133.md` — byte-identical to v2.1.118 (verified against trace 1 `req 3`, which still asks for a 3-7 word sentence-case title).
- `auxiliary/slug_name-2-1-133.md` — byte-identical to v2.1.118 (verified against trace 1 `req 7`, still produces 2-4 word kebab-case slugs for plan files).
- `auxiliary/compact-2-1-133.md` — **trace-verified by trace 2 `req 3` (and its retry at `req 4`)**. The 5581-character compact prompt is byte-identical to v2.1.118 — the prompt itself didn't change between versions, but it now carries a v2.1.133-confirmed signature. The harness mechanism (append the compact prompt as a `text` content part to the **last existing user turn** alongside any trailing `tool_result`; same opus-4-7 instance summarizes its own conversation in-place; same system prompt, same 9-tool catalog) is unchanged. The compact call drops `extended-cache-ttl-2025-04-11` and `afk-mode-2026-01-31` from the beta header, and uses `max_tokens: 20000` instead of the regular main-agent's 64,000.

### 7. System reminders (`<system-reminder>`)

The seven v2.1.118 reminder templates (Deferred Tools List, MCP Server Instructions, Skills List, Plan Mode Active, Auto Mode Active, Plan File Exists, Auto Mode Still Active, Context) all behave the same. The deltas:

- The **Deferred Tools List** drops `AskUserQuestion` (now core), so it now enumerates **21** built-in tools instead of 22. MCP tool names still append at runtime.
- The **Plan Mode Active** reminder still ends with the `Phase 5: Call ExitPlanMode` instruction that mandates ending the turn with either `AskUserQuestion` or `ExitPlanMode`. Because `AskUserQuestion` is now a core tool, plan-mode flows no longer pay a ToolSearch round-trip the first time the model wants to ask the user something.
- **NEW reminder template captured for the first time: "Task Tools Nudge"** (Part 3e in `system-reminders-2-1-133.md`). Fires mid-conversation when the harness sees the model doing multi-step work without using `TaskCreate` / `TaskUpdate`. Carries an explicit *"NEVER mention this reminder to the user"* instruction. Observed at `req 14 msg[10]` and `req 15 msg[10]` after several `Agent` sub-agent spawns.

### 8. Capture caveats (audit summary)

- **9 of 9 core schemas captured.** The trace includes the full `req 2` (main-agent ToolSearch-active turn). Each schema is byte-exact in `core-tools-2-1-133.json` and at the top of `tools-2-1-133.json`.
- **18 of 21 deferred schemas captured.** 17 came from the File Search agent's direct-load set (`req 10`): `CronCreate`, `CronDelete`, `CronList`, `EnterWorktree`, `ExitWorktree`, `ListMcpResourcesTool`, `Monitor`, `PushNotification`, `ReadMcpResourceTool`, `RemoteTrigger`, `TaskCreate`, `TaskGet`, `TaskList`, `TaskStop`, `TaskUpdate`, `WebFetch`, `WebSearch`. The 18th — `ExitPlanMode` — was loaded mid-session by the main agent in `req 5` (`ToolSearch select:ExitPlanMode`) and appeared in the tools array of `req 6` onward. (Originally I overlooked this because I only audited the first 13 requests; caught on a second pass that walked all 70 requests.)
- **3 of 21 deferred schemas unconfirmed and excluded.** `EnterPlanMode`, `NotebookEdit`, `TaskOutput` were never invoked via `ToolSearch select:` in this trace. Those three entries are **omitted from `tools-2-1-133.json`** and tagged with a *"⚠️ Schema NOT verified for v2.1.133"* warning in [ClaudeCodeTools-2-1-133.md](ClaudeCodeTools-2-1-133.md). A future trace that explicitly runs `ToolSearch select:EnterPlanMode,NotebookEdit,TaskOutput` would close this gap.
- **No "without ToolSearch" capture** for any opus-4-7 sub-agent — both Explore and Plan ran with `ENABLE_TOOL_SEARCH=true` in this trace. Their `core-tools-2-1-133.json` files are real captures (`req 12`, `req 13`); a "full enumeration" `tools-2-1-133.json` exists only for the Main agent (`tools-2-1-133.json` at the root) and the File Search agent (`file_search/tools-2-1-133.json`).
- **The user's MCP catalog leaks** into File Search's tool list (17 `mcp__claude_ai_*` tools alongside the 21 built-ins, plus the user's six MCP server names enumerated in the Code Guide skills block). The published `file_search/tools-2-1-133.json` snapshot has the per-user MCP entries stripped — only the 21 built-in tools remain.
- **Code Guide template — `Available plugin skills:` section absent from trace, absent from published file.** The v2.1.118 template had an `**Available plugin skills:**\n{{user_plugin_skills}}` block between MCP servers and `User's settings.json`. The v2.1.133 trace shows MCP servers going **directly** to `User's settings.json` with no plugin-skills block. The user does have a plugin enabled (`pyright-lsp@claude-plugins-official: true`), but `pyright-lsp` is an LSP and probably ships zero skills, so we cannot tell whether the v2.1.133 template removed the block outright or whether the harness conditionally hides empty lists (in which case a different user would still see the heading). Following the byte-exact-vs-trace rule, the published file matches what was transmitted: no plugin-skills block. A future trace where the user has a skill-shipping plugin would distinguish "removed" from "conditionally rendered".
- **Two new auxiliary prompts** caught on the second audit pass: `summarize_transcript_chunk` (req 16) and `analyze_session_facets` (req 17-69, 53 invocations). Both run on `claude-opus-4-7` with the *Claude Agent SDK* greeting (`"You are a Claude agent, built on Anthropic's Claude Agent SDK."`) rather than the Claude Code greeting, suggesting they're invoked by harness-side `/insights`-class flows rather than by the main interactive agent.

---

## Architecture Overview

Claude Code uses a multi-agent architecture. The **main agent** (Opus 4.7) orchestrates work and can spawn specialized **sub-agents**. Tool loading uses `ENABLE_TOOL_SEARCH` (default: `auto`) — when tool definitions exceed ~10% of the context window, ToolSearch activates and defers most tools behind on-demand loading.

### Without ToolSearch (`ENABLE_TOOL_SEARCH=false` or below threshold)

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 30 built-in tools (all loaded directly) + N MCP tools
  |-- spawns --> Explore Agent (opus-4-7, ~23 tools)
  |-- spawns --> File Search Agent (haiku-4-5, 21 tools)
  |-- spawns --> Plan Agent (opus-4-7, ~20 tools)
  |-- spawns --> Code Guide Agent (haiku-4-5, 4 tools)
  |-- spawns --> Status Line Agent (sonnet-4-6, 2 tools)
```

### With ToolSearch (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered)

Only core tools load upfront. Remaining tools are deferred and must be fetched via `ToolSearch` before use. Saves ~45K tokens of initial context.

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 9 core tools: Agent, AskUserQuestion, Bash, Edit, Read,
  |                 ScheduleWakeup, Skill, ToolSearch, Write
  |-- 21 deferred built-in tools (loaded on demand via ToolSearch):
  |     CronCreate/Delete/List, EnterPlanMode, EnterWorktree,
  |     ExitPlanMode, ExitWorktree, ListMcpResourcesTool, Monitor,
  |     NotebookEdit, PushNotification, ReadMcpResourceTool,
  |     RemoteTrigger, TaskCreate/Get/List/Output/Stop/Update,
  |     WebFetch, WebSearch
  |-- MCP tools also deferred behind ToolSearch (enumerated by name in same reminder)
  |
  |-- spawns --> Explore Agent (opus-4-7, 7 core + ToolSearch)
  |-- spawns --> File Search Agent (haiku-4-5, 21 tools, NO ToolSearch)
  |-- spawns --> Plan Agent (opus-4-7, 5 core + ToolSearch)
  |-- spawns --> Code Guide Agent (haiku-4-5, 4 tools, NO ToolSearch)
  |-- spawns --> Status Line Agent (sonnet-4-6, 2 tools, NO ToolSearch)
```

### Common auxiliary triggers (both modes)

```
  |-- triggers --> auxiliary/compact                     (context compression — same opus-4-7, in-place)
  |-- triggers --> auxiliary/summarize_conversation      (session title gen — haiku-4-5)
  |-- triggers --> auxiliary/slug_name                   (kebab-case slug — haiku-4-5)
  |-- triggers --> auxiliary/summarize_transcript_chunk  (transcript chunk summary — opus-4-7,
  |                                                        Claude Agent SDK greeting)
  |-- triggers --> auxiliary/analyze_session_facets      (session facets JSON extract — opus-4-7,
                                                          Claude Agent SDK greeting; powers /insights)
```

---

## Directory Structure

```
claudecode/
  README.md
  ClaudeCodeSystem-2-1-133.md            # Main agent system prompt
  ClaudeCodeTools-2-1-133.md             # Main agent tools (human-readable, 30 built-in tools)
  tools-2-1-133.json                     # All 30 built-in tool schemas (full)
  core-tools-2-1-133.json                # 9 core tools JSON (with ToolSearch active)
  system-reminders-2-1-133.md            # Runtime <system-reminder> templates
  code_guide/                            # Code Guide sub-agent (haiku-4-5)
  explore/                               # Explore sub-agent (opus-4-7)
    core-tools-2-1-133.json              #   7 core tools (with ToolSearch)
  file_search/                           # File Search sub-agent (haiku-4-5, no ToolSearch)
  plan/                                  # Plan sub-agent (opus-4-7)
    core-tools-2-1-133.json              #   5 core tools (with ToolSearch)
  status_line/                           # Status Line sub-agent (sonnet-4-6, no ToolSearch)
  auxiliary/                             # Non-agent functional prompts
    compact-2-1-133.md
    summarize_conversation-2-1-133.md
    slug_name-2-1-133.md
    summarize_transcript_chunk-2-1-133.md     # NEW (added on second audit pass)
    analyze_session_facets-2-1-133.md         # NEW (added on second audit pass)
```

---

## File Index

### Main Agent (root)

| File | Description |
| --- | --- |
| [ClaudeCodeSystem-2-1-133.md](ClaudeCodeSystem-2-1-133.md) | Main agent system prompt. Model: Opus 4.7, 1M context. Knowledge cutoff January 2026. `# Executing actions with care` collapsed to one paragraph; new clarifying-question paragraph in `# Text output`; trailing context-management line moved under a `# Context management` heading; bullet style re-indented. |
| [ClaudeCodeTools-2-1-133.md](ClaudeCodeTools-2-1-133.md) | Human-readable description of all **30 built-in main-agent tools**, with the 3 unverified ones (`EnterPlanMode`, `NotebookEdit`, `TaskOutput`) clearly tagged "⚠️ Schema NOT verified for v2.1.133". AskUserQuestion is now core; Bash gains `find from .` instruction and the `run_in_background` parameter description was simplified; Agent's Explore description rewritten; Monitor/EnterWorktree/RemoteTrigger/WebSearch text edited as documented above. |
| [tools-2-1-133.json](tools-2-1-133.json) | JSON schemas for **the 27 trace-verified built-in tools** (9 core from `req 2`, 17 deferred from File Search's `req 10`, plus `ExitPlanMode` from `req 6` after the main agent invoked `ToolSearch select:ExitPlanMode` in `req 5`). Each carries `"eager_input_streaming": true` exactly as observed. The 3 deferred tools `EnterPlanMode`, `NotebookEdit`, `TaskOutput` are intentionally **omitted** because the trace did not call `ToolSearch select:` on them — they will be added back when a fresh capture confirms the v2.1.133 schemas. |
| [core-tools-2-1-133.json](core-tools-2-1-133.json) | JSON schema for the 9 core tools when ToolSearch is active: Agent, AskUserQuestion, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write. The remaining 21 deferred tools are fetched on demand. |
| [system-reminders-2-1-133.md](system-reminders-2-1-133.md) | Runtime `<system-reminder>` templates. Deferred Tools list now 21 entries (AskUserQuestion removed). All other templates unchanged from v2.1.118. |

### Sub-Agents

| Directory | Agent | Model | Tools (no ToolSearch) | Tools (with ToolSearch) | v2.1.133 changes |
| --- | --- | --- | --- | --- | --- |
| [explore/](explore/) | Explore | opus-4-7 | ~23 (inferred) | **7 core + ToolSearch** (captured req 13) | system prompt unchanged; `eager_input_streaming` added to all schemas |
| [file_search/](file_search/) | File Search | haiku-4-5 | **21** (captured req 10 — direct load, no ToolSearch) | n/a | system prompt unchanged; `eager_input_streaming` added; Bash/Monitor/EnterWorktree/RemoteTrigger/WebSearch description deltas |
| [plan/](plan/) | Plan | opus-4-7 | ~20 (inferred) | **5 core + ToolSearch** (captured req 12) | system prompt unchanged; `eager_input_streaming` added |
| [code_guide/](code_guide/) | Code Guide | haiku-4-5 | **4** (Bash, Read, WebFetch, WebSearch) | n/a | system prompt unchanged; WebSearch month rolled to May 2026; `eager_input_streaming` added |
| [status_line/](status_line/) | Status Line | sonnet-4-6 | **2** (Read, Edit) | n/a | token-field descriptions reworded; **new `effort` and `thinking` JSON blocks**; `eager_input_streaming` added |

### Auxiliary Prompts (`auxiliary/`)

| File | Trigger | Model | Description |
| --- | --- | --- | --- |
| [auxiliary/compact-2-1-133.md](auxiliary/compact-2-1-133.md) | `/compact` | opus-4-7 | Context-compression prompt (5581 chars). Appended as a `text` content part to the **last existing user turn** (alongside any trailing `tool_result`) so the main `opus-4-7` agent self-summarizes its own conversation in-place — same system prompt, same tool catalog (9 core tools), no separate model call. Trace-verified byte-identical to v2.1.118 against trace 2 `log-2026-05-08-09-01-48.jsonl` `req 3` (req 4 is a retry of the same call). |
| [auxiliary/summarize_conversation-2-1-133.md](auxiliary/summarize_conversation-2-1-133.md) | Session start | haiku-4-5 | Session-title generator (3-7 words, sentence case). Verified byte-identical to v2.1.118 against `req 3` of the trace. |
| [auxiliary/slug_name-2-1-133.md](auxiliary/slug_name-2-1-133.md) | Plan-file / memory-file slug | haiku-4-5 | 2-4 word kebab-case slug generator for plan files (`~/.claude/plans/<slug>.md`) and similar internal naming. Verified byte-identical to v2.1.118 against `req 7` of the trace. |
| [auxiliary/summarize_transcript_chunk-2-1-133.md](auxiliary/summarize_transcript_chunk-2-1-133.md) | Insights / retro chunk processing | opus-4-7 | **NEW capture.** Summarize a transcript chunk into 3-5 sentences focused on user request, Claude's actions, friction, and outcome. Uses the *Claude Agent SDK* greeting (`"You are a Claude agent, built on Anthropic's Claude Agent SDK."`), not the standard Claude Code greeting. Captured from `req 16, 64, 65, 66` (4 invocations). |
| [auxiliary/analyze_session_facets-2-1-133.md](auxiliary/analyze_session_facets-2-1-133.md) | Insights / retro facet extraction | opus-4-7 | **NEW capture.** Extract structured JSON facets (goal categories, satisfaction signals, friction types, primary success type, etc.) from a session dump. Same Claude Agent SDK greeting as above. Powers the `/insights` skill's session-by-session analysis. Captured from `req 17-63` + `req 67-69` (50 invocations, all sharing the same boilerplate around `{{session_dump}}`). |

---

## Harness Request-Body Parameters (per call type)

Beyond `system`, `messages`, and `tools`, every Claude Code request carries harness-side configuration in the API request body. These were observed verbatim across the v2.1.133 trace and are documented here for completeness — they are part of the v2.1.133 contract even though they don't live in any prompt file.

| Call type                  | model                       | max_tokens | output_config.effort | thinking                                       | context_management                                              | stream | temperature |
|----------------------------|-----------------------------|-----------:|----------------------|------------------------------------------------|-----------------------------------------------------------------|:------:|------------:|
| Main agent                 | `claude-opus-4-7`           |     64,000 | `xhigh`              | `{type: "adaptive", display: "summarized"}`    | `{edits: [{type: "clear_thinking_20251015", keep: "all"}]}`     |   ✓    |       (—)   |
| Main agent (`/compact`)    | `claude-opus-4-7`           |     20,000 | `xhigh`              | `{type: "adaptive", display: "summarized"}`    | `{edits: [{type: "clear_thinking_20251015", keep: "all"}]}`     |   ✓    |       (—)   |
| Plan sub-agent             | `claude-opus-4-7`           |     64,000 | `xhigh`              | (—)                                            | (—)                                                             |   ✓    |       (—)   |
| Explore sub-agent          | `claude-opus-4-7`           |     64,000 | `xhigh`              | (—)                                            | (—)                                                             |   ✓    |       (—)   |
| File Search sub-agent      | `claude-haiku-4-5-20251001` |     32,000 | (—)                  | (—)                                            | (—)                                                             |   ✓    |        1    |
| Code Guide sub-agent       | `claude-haiku-4-5-20251001` |     32,000 | (—)                  | (—)                                            | (—)                                                             |   ✓    |        1    |
| Status Line sub-agent      | `claude-sonnet-4-6`         |     32,000 | `high`               | (—)                                            | (—)                                                             |   ✓    |        1    |
| `summarize_conversation`   | `claude-haiku-4-5-20251001` |     32,000 | (—)                  | (—)                                            | (—)                                                             |   ✓    |        1    |
| `slug_name`                | `claude-haiku-4-5-20251001` |     32,000 | (—)                  | (—)                                            | (—)                                                             |   ✓    |        1    |
| `summarize_transcript_chunk` | `claude-opus-4-7`         |        500 | `xhigh`              | (—)                                            | (—)                                                             |   ✓    |       (—)   |
| `analyze_session_facets`   | `claude-opus-4-7`           |      4,096 | `xhigh`              | (—)                                            | (—)                                                             |   ✓    |       (—)   |

**Key observations:**

- **Only the main agent (including the `/compact` call)** carries `thinking` (adaptive, summarized display) and `context_management` (`clear_thinking_20251015` edit keeping all messages). Sub-agents and auxiliary calls do not — they are short-form, non-thinking calls.
- **`output_config.effort`** is set on the opus-4-7 surfaces (Main, Main /compact, Plan, Explore, both new auxiliary prompts) at `xhigh`, and on Status Line at `high`. The Status Line agent's documented stdin schema includes an `effort.level` field (`"low" | "medium" | "high" | "xhigh" | "max"`) that mirrors this exact enum — this is the field that hosts the value.
- **`max_tokens` is heavily call-specific:** opus-4-7 main/Plan/Explore get 64k; the `/compact` call drops to **20,000** (a summary fits comfortably under that cap); haiku-4-5 surfaces get 32k; the new `summarize_transcript_chunk` auxiliary is capped at **500** (3-5 sentence target); `analyze_session_facets` is capped at **4096** (one JSON object).
- **Haiku sub-agents and haiku auxiliaries set `temperature: 1`**; opus sub-agents and the main agent omit `temperature` entirely (relying on adaptive/effort settings).
- **Every call has `stream: true`.**
- **`metadata.user_id`** carries `device_id` / `account_uuid` / `session_id`. Those are user-specific identifiers and are not reproduced in this README.

### Cache control on `system` parts

For requests with structured `system` arrays (the main agent and every sub-agent), both `system[1]` (the `"You are Claude Code…"` greeting) and `system[2]` (the agent body) carry an `ephemeral` cache_control. The exact form depends on the call:

- **Main agent (regular turn)**: `cache_control: { type: "ephemeral", ttl: "1h" }` — the `1h` TTL is enabled by the `extended-cache-ttl-2025-04-11` beta flag.
- **Main agent (`/compact` call)**: `cache_control: { type: "ephemeral" }` — **no `ttl` field**, because the compact call drops the `extended-cache-ttl-2025-04-11` beta. Confirmed by trace 2 `req 3` and `req 4`.
- **Sub-agents and other typed-system calls**: ephemeral with no `ttl`.

The billing-header line at `system[0]` is never cached. Auxiliary calls that use the Claude Agent SDK greeting (trace 1 `req 16-69`) carry no cache-control entries at all — they're one-shot.

### `anthropic-beta` request headers

The `anthropic-beta` request header carries a comma-separated list of opt-in API features. Across both traces, **9 distinct combinations** are observed, keyed by call type:

| Call type | Beta flags |
|---|---|
| Main agent (regular turn) | `claude-code-20250219, oauth-2025-04-20, context-1m-2025-08-07, interleaved-thinking-2025-05-14, context-management-2025-06-27, prompt-caching-scope-2026-01-05, advisor-tool-2026-03-01, advanced-tool-use-2025-11-20, effort-2025-11-24, afk-mode-2026-01-31, extended-cache-ttl-2025-04-11` |
| Main agent (`/compact` call) | (regular set **minus** `extended-cache-ttl-2025-04-11` and `afk-mode-2026-01-31`) — explains why the compact call's `cache_control` lacks `ttl: "1h"` |
| Plan / Explore sub-agent (opus-4-7) | (regular main set minus `extended-cache-ttl-2025-04-11`) |
| File Search / Code Guide sub-agent (haiku-4-5) | (regular main set minus `context-1m-2025-08-07, advanced-tool-use-2025-11-20, effort-2025-11-24, extended-cache-ttl-2025-04-11`) |
| Status Line sub-agent (sonnet-4-6) | (regular main set minus `context-1m-2025-08-07, advanced-tool-use-2025-11-20, extended-cache-ttl-2025-04-11`) |
| `summarize_conversation` / `slug_name` (haiku-4-5) | drops `claude-code-20250219, advanced-tool-use, effort, afk-mode, extended-cache-ttl, context-1m`; **adds `structured-outputs-2025-12-15`** (these calls return JSON-only output) |
| `summarize_transcript_chunk` / `analyze_session_facets` (opus-4-7) | (Plan/Explore set minus `advanced-tool-use, context-1m, extended-cache-ttl`); keeps `effort` and `afk-mode` |

**Notable beta flags:**

- `claude-code-20250219` — gates Claude Code-specific server behavior. Present on every CC-originating call; **absent** from the haiku title/slug auxiliaries.
- `context-1m-2025-08-07` — enables the 1M-token context window. Only on opus-4-7 main / Plan / Explore (since the model ID `claude-opus-4-7[1m]` requires it). Present on `/compact` too.
- `effort-2025-11-24` — enables `output_config.effort`. Present on Main, Plan, Explore, Status Line, both new auxiliary prompts, and `/compact`. Absent on haiku sub-agents and haiku auxiliaries.
- `interleaved-thinking-2025-05-14` and `context-management-2025-06-27` — universal across all calls.
- `extended-cache-ttl-2025-04-11` — only on the main agent's regular turns (which carry the `1h` TTL on system parts). **Dropped on `/compact` calls**, hence the missing `ttl` on those system parts.
- `structured-outputs-2025-12-15` — only on the haiku JSON-output auxiliaries (`summarize_conversation`, `slug_name`).
- `advanced-tool-use-2025-11-20` — only on the opus-4-7 surfaces that actually call tools (Main regular + `/compact`, Plan, Explore).
- `afk-mode-2026-01-31` — present on Main regular, sub-agents, and the new auxiliary opus prompts; absent on title/slug haiku and **on `/compact` calls**.

The beta header is sent at the HTTP level (not in the body), so it isn't captured in any of the published prompt/JSON files in this directory — it's documented here for completeness as part of the v2.1.133 contract.

### Endpoint

All calls go to `POST https://api.anthropic.com/v1/messages?beta=true` (the trace also captures one `HEAD https://api.anthropic.com/` health probe at the very start, but that carries no model or prompt).

---

## Privacy / Anonymization Conventions

The trace was captured from a real user session, so all user-specific data has been replaced with placeholders before being committed:

| Placeholder | Replaces |
| --- | --- |
| `{{working_directory}}`, `{{is_git_repo}}`, `{{platform}}`, `{{shell}}`, `{{os_version}}` | Per-session environment values |
| `{{memory_directory}}` | `~/.claude/projects/<slug>/memory/` path |
| `{{user_email}}` | Authenticated email surfaced in the Context reminder |
| `{{global_claude_md_content}}`, `{{project_claude_md_content}}` | CLAUDE.md inlined contents |
| `{{memory_index_content}}` | MEMORY.md body |
| `{{user_settings_json}}`, `{{user_skills_list}}`, `{{user_mcp_servers}}`, `{{user_plugin_skills}}` | Code Guide template injection points |
| `{{user_sandbox_filesystem_config}}`, `{{user_sandbox_network_config}}` | Bash sandbox JSON config (per-session allow/deny lists) |
| `{{plan_file_path}}`, `{{plan_contents}}` | Plan-file path + body when reinjected via the Plan File Exists reminder |
| `{{server_name_*}}`, `{{server_instructions_*}}`, `{{mcp_tool_names}}` | MCP server identifiers and per-server instructions |
| `{{user_global_claude_md_path}}`, `{{project_claude_md_path}}` | CLAUDE.md paths |

The user's MCP server names (`claude.ai Consensus`, `claude.ai Context7`, `claude.ai Gmail`, `claude.ai Google Drive`, `claude.ai Google Calendar`, `computer-use`) and the 17 per-user `mcp__claude_ai_*__*` tool names appeared in the raw trace's File Search tool list and Code Guide skills enumeration; both have been stripped from the published JSON snapshots so only built-in tools and structural template placeholders remain.
