# Claude Code System Prompts

**Latest version**: 2.1.114 (April 2026)
**Previous version**: 2.1.100 (April 2026, kept for diff reference)

---

## What Changed in v2.1.114

### Models

- **Opus 4.7** (`claude-opus-4-7`) replaces Opus 4.6 as the main agent model. Still 1M context.
- Knowledge cutoff updated: **May 2025 → January 2026** (Opus). Sonnet 4.6 / Haiku 4.5 cutoffs unchanged.
- Model family wording updated: "Claude 4.6 and 4.5" → **"Claude 4.X"**.
- **Fast mode** description tightened: "Fast mode for Claude Code uses Claude Opus 4.6 with faster output (it does not downgrade to a smaller model). It can be toggled with `/fast` and is **only available on Opus 4.6**." (Fast mode stays on the older Opus 4.6 — Opus 4.7 has no fast variant yet.)

### New Tools

| Tool | Where | What it does |
|------|-------|--------------|
| **`ScheduleWakeup`** | Core tool for main, Plan, Explore, File Search agents | Schedule when to resume work in `/loop` dynamic mode (model self-paces). Required params: `delaySeconds` (60–3600), `reason`, `prompt`. Sentinel `<<autonomous-loop-dynamic>>` for autonomous loops. |
| **`PushNotification`** | Deferred (main) / direct (File Search, Explore) | Send a desktop / Remote Control phone notification. Use sparingly — pulls user attention. Params: `message` (≤200 chars), `status: "proactive"`. |

### New System-Reminder Blocks

- **`Plan Mode Active`** — injected after `EnterPlanMode` is called. Defines a strict 5-phase workflow: Initial Understanding (Explore agents) → Design (Plan agent) → Review → Final Plan → Call ExitPlanMode. While active, the agent is READ-ONLY except for one designated plan file (`~/.claude/plans/<slug>.md`).
- **`Auto Mode Active`** — injected into `msg[0]` when `permissions.defaultMode == "auto"`. Six-rule directive: execute immediately, minimize interruptions, prefer action over planning, expect course corrections, do NOT take overly destructive actions, avoid data exfiltration. Coexists with Plan Mode (Plan rules win).
- See `system-reminders-2-1-114.md` for the full verbatim text of both.

### New Context Field

- The `Context` system-reminder (last `msg[0]` part) now includes a **`# userEmail`** section with the authenticated user's email — useful for commit attribution, addressing the user, or correlating with external tools.

### Tool Schema Changes

- **`Bash`** — significant additions:
  - New **`## Command sandbox`** section in the description: declares the per-session filesystem allow/deny lists and the `dangerouslyDisableSandbox` parameter.
  - New `dangerouslyDisableSandbox` boolean parameter (was already in v2.1.100 schema, now formally documented in description).
  - Removed the `rerun` parameter (the `[rerun: bN]` footer feature is no longer surfaced).
  - Tightened the `sleep` rule: long leading `sleep` commands are **blocked** — must use `Monitor` with an until-loop instead of chaining shorter sleeps.
  - New guidance against `cd <current-directory>` prefixes in git commands (triggers permission prompts).
  - New guidance to use `$TMPDIR` (sandbox-writable) instead of `/tmp` directly.
- **New `defer_loading: true` metadata flag** on tool schemas. When ToolSearch is active on the main agent, deferred tools carry this flag (observed on `AskUserQuestion` and `ExitPlanMode`; presumably present on all 22 deferred tools). The flag is absent on agents that don't use ToolSearch (file_search, code_guide, status_line).
- **`ExitPlanMode`** description tightened with explicit `AskUserQuestion` vs `ExitPlanMode` boundary and a third example for "use AskUserQuestion first to clarify, then ExitPlanMode" workflow.

### Main Agent Prompt Changes

- Renamed section: **"Communication style" → "Text output (does not apply to tool calls)"**.
- New "Doing tasks" bullet: **"For UI or frontend changes, start the dev server and use the feature in a browser before reporting the task as complete."** Type/test only verify code correctness, not feature correctness.
- Skill-invocation example simplified: `/<skill-name>` (e.g. `/commit`)` → `/<skill-name>``.
- All other guidance in *Doing tasks*, *Executing actions with care*, *Tone and style*, *Session-specific guidance*, and *auto memory* is preserved verbatim from v2.1.100.

### Skills List Additions

- New built-in skill: **`team-onboarding`** — packages a user's Claude Code setup (skills, hooks, settings) into a teammate-ready guide.
- The `fewer-permission-prompts` skill is now consistently emitted in the Skills List.

### Sub-Agent Changes

- **All sub-agents using opus** (Explore, Plan) now run on **`claude-opus-4-7`**. Haiku 4.5 / Sonnet 4.6 sub-agents unchanged.
- **All sub-agents** gained the `ScheduleWakeup` core tool (and `PushNotification` for File Search / Explore).
- **Status Line** prompt is unchanged structurally but model display updated.
- **Code Guide** template body unchanged — still expanded with documentation URLs, user skills, MCP servers, plugin skills, and `settings.json` at runtime.

---

## Architecture Overview

Claude Code uses a multi-agent architecture. The **main agent** (Opus 4.7) orchestrates work and can spawn specialized **sub-agents**. Tool loading uses `ENABLE_TOOL_SEARCH` (default: `auto`) — when tool definitions exceed ~10% of the context window, ToolSearch activates and defers most tools behind on-demand loading.

### ToolSearch auto mode (`ENABLE_TOOL_SEARCH=auto`, default)

ToolSearch activates when total tool definition tokens exceed **~10% of the context window**:

| Context Window | Tool Tokens (~31 tools v2.1.114) | Ratio | ToolSearch? |
| --- | --- | --- | --- |
| 1M (Opus 4.7) | ~50K | 5.0% | No — all 31 tools load directly |
| 200K (Sonnet) | ~50K | 25% | **Yes** — 10 core + deferred |
| 1M + many MCP tools | >100K | >10% | **Yes** — 10 core + deferred |

Without ToolSearch (threshold not met):

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 31 tools (all loaded directly, no ToolSearch)
  |-- spawns --> Explore Agent (opus-4-7, 25 tools)
  |-- spawns --> File Search Agent (haiku-4-5, 22 tools)
  |-- spawns --> Plan Agent (opus-4-7, 22 tools)
  |-- spawns --> Code Guide Agent (haiku-4-5, 5 tools)
  |-- spawns --> Status Line Agent (sonnet-4-6, 2 tools)
```

### With ToolSearch (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered)

Only core tools load upfront. Remaining tools are deferred and must be fetched via `ToolSearch` before use. Saves ~45K tokens of initial context.

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 10 core tools: Agent, Bash, Edit, Glob, Grep, Read, ScheduleWakeup, Skill, ToolSearch, Write
  |-- 22 deferred tools (loaded on demand via ToolSearch):
  |     AskUserQuestion, CronCreate/Delete/List, EnterPlanMode,
  |     EnterWorktree, ExitPlanMode, ExitWorktree, ListMcpResourcesTool,
  |     Monitor, NotebookEdit, PushNotification, ReadMcpResourceTool,
  |     RemoteTrigger, TaskCreate/Get/List/Output/Stop/Update, WebFetch, WebSearch
  |-- MCP tools also deferred behind ToolSearch
  |
  |-- spawns --> Explore Agent (opus-4-7, 9 core + ToolSearch)
  |-- spawns --> File Search Agent (haiku-4-5, 22 tools, NO ToolSearch)
  |-- spawns --> Plan Agent (opus-4-7, 7 core + ToolSearch)
  |-- spawns --> Code Guide Agent (haiku-4-5, 5 tools, NO ToolSearch)
  |-- spawns --> Status Line Agent (sonnet-4-6, 2 tools, NO ToolSearch)
```

### Common auxiliary triggers (both modes)

```
  |-- triggers --> auxiliary/compact (context compression)
  |-- triggers --> auxiliary/summarize_conversation (title generation)
  |-- triggers --> auxiliary/suggestion_mode (input prediction, unchanged)
  |-- triggers --> auxiliary/new_topic (topic detection, unchanged)
  |-- triggers --> auxiliary/insights (usage analysis, unchanged)
```

---

## Directory Structure

```
claudecode/
  README.md
  ClaudeCodeSystem-2-1-114.md            # Main agent system prompt (v2.1.114, current)
  ClaudeCodeSystem-2-1-100.md            # Main agent system prompt (v2.1.100, archived)
  ClaudeCodeTools-2-1-114.md             # Main agent tools (readable, v2.1.114)
  ClaudeCodeTools-2-1-100.md             # Main agent tools (readable, v2.1.100, archived)
  tools-2-1-114.json                     # All 31 tools JSON (without ToolSearch)
  tools-2-1-100.json                     # All 29 tools JSON (v2.1.100, archived)
  core-tools-2-1-114.json                # 10 core tools JSON (with ToolSearch active)
  core-tools-2-1-100.json                # 9 core tools JSON (v2.1.100, archived)
  system-reminders-2-1-114.md            # Runtime system-reminder templates (v2.1.114)
  system-reminders-2-1-100.md            # Runtime system-reminder templates (v2.1.100)
  code_guide/                            # Code Guide sub-agent
  explore/                               # Explore sub-agent
    core-tools-2-1-114.json              #   9 core tools (with ToolSearch)
    tools-2-1-114.json                   #   25 tools (without ToolSearch)
  file_search/                           # File Search sub-agent (no ToolSearch)
  plan/                                  # Plan sub-agent
    core-tools-2-1-114.json              #   7 core tools (with ToolSearch)
    tools-2-1-114.json                   #   22 tools (without ToolSearch)
  status_line/                           # Status Line sub-agent (no ToolSearch)
  auxiliary/                             # Non-agent functional prompts
```

---

## File Index

### Main Agent (root) — v2.1.114

| File | Description |
| --- | --- |
| [ClaudeCodeSystem-2-1-114.md](ClaudeCodeSystem-2-1-114.md) | **Current** main agent system prompt. Section "Communication style" renamed to "Text output (does not apply to tool calls)". Adds UI/frontend dev-server testing guidance. Model: Opus 4.7, 1M context. Knowledge cutoff January 2026. |
| [ClaudeCodeTools-2-1-114.md](ClaudeCodeTools-2-1-114.md) | Human-readable description of all 32 main agent tools (31 + ToolSearch). |
| [tools-2-1-114.json](tools-2-1-114.json) | JSON schema of 31 tools (without ToolSearch — all loaded directly). |
| [core-tools-2-1-114.json](core-tools-2-1-114.json) | JSON schema of 10 core tools when ToolSearch is active: Agent, Bash, Edit, Glob, Grep, Read, **ScheduleWakeup**, Skill, **ToolSearch**, Write. The remaining 22 tools are deferred. |
| [system-reminders-2-1-114.md](system-reminders-2-1-114.md) | Runtime `<system-reminder>` templates: Deferred Tools, MCP, Skills, **Auto Mode Active (NEW)**, Context (with **`# userEmail` NEW**). |

### Main Agent (root) — v2.1.100 (archived)

| File | Description |
| --- | --- |
| [ClaudeCodeSystem-2-1-100.md](ClaudeCodeSystem-2-1-100.md) | Main agent system prompt for v2.1.100. Model: Opus 4.6, 1M context. |
| [ClaudeCodeTools-2-1-100.md](ClaudeCodeTools-2-1-100.md) | Human-readable description of 29 main agent tools. |
| [tools-2-1-100.json](tools-2-1-100.json) | JSON schema of all 29 tools. |
| [core-tools-2-1-100.json](core-tools-2-1-100.json) | JSON schema of 9 core tools when ToolSearch is active. |
| [system-reminders-2-1-100.md](system-reminders-2-1-100.md) | Runtime `<system-reminder>` templates for v2.1.100. |

### Sub-Agents — v2.1.114

| Directory | Agent | Model | Tools (no ToolSearch) | Tools (with ToolSearch) | v2.1.114 changes |
| --- | --- | --- | --- | --- | --- |
| [explore/](explore/) | Explore | opus-4-7 | 25 (added ScheduleWakeup, PushNotification) | 9 core + ToolSearch | Model bump 4.6→4.7; +2 tools |
| [file_search/](file_search/) | File Search | haiku-4-5 | 22 (added ScheduleWakeup, PushNotification) | 22 (no ToolSearch) | +2 tools |
| [plan/](plan/) | Plan | opus-4-7 | 22 (added ScheduleWakeup, PushNotification) | 7 core + ToolSearch | Model bump 4.6→4.7; +2 tools |
| [code_guide/](code_guide/) | Code Guide | haiku-4-5 | 5 (Glob, Grep, Read, WebFetch, WebSearch) | 5 (no ToolSearch) | Unchanged |
| [status_line/](status_line/) | Status Line | sonnet-4-6 | 2 (Read, Edit) | 2 (no ToolSearch) | Unchanged |

### Sub-Agents — v2.1.100 (archived)

Each sub-agent directory also retains its `*-2-1-100.md` and `tools-2-1-100.json` (and where applicable `core-tools-2-1-100.json`) files for diff reference.

### Auxiliary Prompts (auxiliary/)

| File | Trigger | Description |
| --- | --- | --- |
| [auxiliary/compact-2-1-114.md](auxiliary/compact-2-1-114.md) | Context window limit | Context compression. Identical to v2.1.100. |
| [auxiliary/compact-2-1-100.md](auxiliary/compact-2-1-100.md) | Context window limit | v2.1.100 archive. |
| [auxiliary/summarize_conversation-2-1-114.md](auxiliary/summarize_conversation-2-1-114.md) | Session end | Title generation. Identical to v2.1.100. |
| [auxiliary/summarize_conversation-2-1-100.md](auxiliary/summarize_conversation-2-1-100.md) | Session end | v2.1.100 archive. |

---
