# Claude Code System Prompts

**Version**: 2.1.118 (April 2026)
**Captured from**: `claude-cli/2.1.118` — two live traces (`log-2026-04-23-11-26-38.jsonl` partial, `log-2026-04-23-12-00-42.jsonl` full ToolSearch dump)

> All previous version archives (v2.1.114, v2.1.100) have been replaced in-place. The repo now tracks one canonical version; the v2.1.114 → v2.1.118 diff lives in this README.

---

## What Changed in v2.1.118 (vs v2.1.114)

### 1. Tool catalog overhaul — only `Glob` / `Grep` removed (MCP resource tools stay)

`Glob` and `Grep` have been **removed entirely** from every agent's tool catalog. Their functionality migrates to `find` / `grep` invoked through the `Bash` tool. The MCP resource tools (`ListMcpResourcesTool`, `ReadMcpResourceTool`) are **unchanged** — they remain in the main agent's deferred list and in the File Search agent's direct-load set.

| Agent              | v2.1.114 core tools                                                    | v2.1.118 core tools                                          | Diff                                                  |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------- |
| Main               | 10 (Agent, Bash, Edit, **Glob, Grep**, Read, ScheduleWakeup, Skill, ToolSearch, Write) | **8** (Agent, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write) | −Glob, −Grep                                          |
| Explore            | 9 (+Glob, Grep)                                                        | **7**                                                        | −Glob, −Grep                                          |
| Plan               | 7 (+Glob, Grep)                                                        | **5**                                                        | −Glob, −Grep                                          |
| File Search        | 22 (no ToolSearch — direct load)                                       | **21** (no ToolSearch — direct load)                         | −Glob, −Grep, +(implicit) `find` / `grep` via Bash    |
| Code Guide         | 5 (Glob, Grep, Read, WebFetch, WebSearch)                              | **4** (**Bash**, Read, WebFetch, WebSearch)                  | −Glob, −Grep, **+Bash**                               |
| Status Line        | 2 (Read, Edit)                                                         | 2                                                            | unchanged                                             |

Main-agent **deferred list** is unchanged at **22 built-in entries**. The full v2.1.118 deferred list (built-in only — MCP tool names append at runtime) is:

```
AskUserQuestion, CronCreate, CronDelete, CronList, EnterPlanMode, EnterWorktree,
ExitPlanMode, ExitWorktree, ListMcpResourcesTool, Monitor, NotebookEdit,
PushNotification, ReadMcpResourceTool, RemoteTrigger,
TaskCreate, TaskGet, TaskList, TaskOutput, TaskStop, TaskUpdate, WebFetch, WebSearch
```

So **8 core + 22 deferred = 30 built-in tools** for the main agent (v2.1.114 had 10 core + 22 deferred = 32; the −2 net change is just `Glob`/`Grep`).

### 2. Bash schema additions / changes (4 changes)

- **IMPORTANT redirect list** dropped `find` and `grep` (they're now first-class via Bash, not redirected to Glob/Grep). The "File search" / "Content search" guidance bullets that pointed at Glob/Grep are gone.
- **New** in Instructions: *"Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of `cd`. ... In particular, never prepend `cd <current-directory>` to a `git` command — `git` already operates on the current working tree, and the compound triggers a permission prompt."*
- **New** in Instructions: *"When using `find -regex` with alternation, put the longest alternative first. Example: use `'.*\.\(tsx\|ts\)'` not `'.*\.\(ts\|tsx\)'` — the second form silently skips `.tsx` files."*
- **New** in Committing-changes-with-git: *"Do not use --no-edit with git rebase commands, as the --no-edit flag is not a valid option for git rebase."*

The `## Command sandbox` section, `dangerouslyDisableSandbox` parameter, and `$TMPDIR` guidance are unchanged from v2.1.114.

### 3. Main agent prompt — three small edits

- **`# Using your tools`** — `Prefer dedicated tools over Bash when one fits (Read, Edit, Write, Glob, Grep)` → `... (Read, Edit, Write)`. Glob/Grep dropped.
- **`# Session-specific guidance`** —
  - Bullet 3: `Otherwise use the Glob or Grep directly.` → `Otherwise use \`find\` or \`grep\` via the Bash tool directly.`
  - **New bullet (5th item):**
    > If the user asks about "ultrareview" or how to run it, explain that /ultrareview launches a multi-agent cloud review of the current branch (or /ultrareview <PR#> for a GitHub PR). It is user-triggered and billed; you cannot launch it yourself, so do not attempt to via Bash or otherwise. It needs a git repository (offer to "git init" if not in one); the no-arg form bundles the local branch and does not need a GitHub remote.
- **End of prompt** — the line `Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail.` has been **removed**.
- **`# auto memory` → `## What NOT to save in memory`** — single-word grammar fix: `These exclusions apply even when the user explicitly asks to save.` → `... explicitly asks you to save.`

All other sections (`# System`, `# Doing tasks`, `# Executing actions with care`, `# Tone and style`, `# Text output (does not apply to tool calls)`, the rest of `# auto memory`, `# Environment`) are byte-identical.

### 4. Sub-agent prompt micro-edits

- **Plan agent** — Phase 2 step: `using Glob, Grep, and Read` → `using \`find\`, \`grep\`, and Read`. Read-only Bash whitelist now includes `grep` (previously omitted).
- **File Search agent** — first two Guidelines bullets:
  - `Use Glob for broad file pattern matching` → `Use \`find\` via Bash for broad file pattern matching`
  - `Use Grep for searching file contents with regex` → `Use \`grep\` via Bash for searching file contents with regex`
  - Read-only Bash whitelist also adds `grep`.
- **Code Guide agent** — Approach step 7: `using Read, Glob, and Grep` → `using Read, \`find\`, and \`grep\``. Tool list shifts from `[Glob, Grep, Read, WebFetch, WebSearch]` to `[Bash, Read, WebFetch, WebSearch]` (Bash gained, Glob/Grep lost).
- **Status Line agent** — `vim.mode` JSON enum: `"INSERT" | "NORMAL"` → `"INSERT" | "NORMAL" | "VISUAL" | "VISUAL LINE"` (added two visual modes).
- **Explore agent** — prompt body byte-identical.

### 5. New `<system-reminder>` blocks (2 new)

Two reminder templates that did not exist in v2.1.114:

- **Plan File Exists** — emitted when continuing a session that already has a saved plan file (after a prior `EnterPlanMode` → `ExitPlanMode` cycle). Inlines the **full plan markdown verbatim** so the model has the canonical approach without a separate Read call.

  ```xml
  <system-reminder>
  A plan file exists from plan mode at: {{plan_file_path}}

  Plan contents:

  {{plan_contents}}
  </system-reminder>
  ```

- **Auto Mode Still Active** — slim follow-up reminder injected into **subsequent** user messages (`msg[1]`+) when auto mode is still active, replacing repetition of the full 6-rule directive.

  ```xml
  <system-reminder>
  Auto mode still active (see full instructions earlier in conversation). Execute autonomously, minimize interruptions, prefer action over planning.
  </system-reminder>
  ```

The other five reminder templates (Deferred Tools List, MCP Server Instructions, Skills List, Plan Mode Active, Auto Mode Active, Context) are structurally unchanged — including the Deferred Tools List, which still enumerates all 22 built-in deferred tools (the MCP resource tools `ListMcpResourcesTool` / `ReadMcpResourceTool` were never removed; an earlier draft of these notes claimed they had been, based on a single first-turn capture where MCP servers hadn't initialized yet — see `system-reminders-2-1-118.md` "Initial-session caveat").

### 6. New auxiliary prompt: `slug_name`

Trace captured a haiku-4.5 call with a 263-char system prompt that did not exist in v2.1.114:

```
Generate a short kebab-case name (2-4 words) that captures the main topic of this conversation. Use lowercase words separated by hyphens. Examples: "fix-login-bug", "add-auth-feature", "refactor-api-client", "debug-test-failures". Return JSON with a "name" field.
```

Saved as [`auxiliary/slug_name-2-1-118.md`](auxiliary/slug_name-2-1-118.md). Used by the harness to generate slugs for plan-file paths (e.g. `~/.claude/plans/<slug>.md`) and similar internal naming. The companion title generator (`summarize_conversation-2-1-118.md`) is byte-identical to v2.1.114 (verified against the trace).

### 7. `compact` (`/compact`) — observed mechanism

The compact prompt text is in [`auxiliary/compact-2-1-118.md`](auxiliary/compact-2-1-118.md) (5581 chars, captured byte-exact from the trace).

**How it's invoked in v2.1.118**: the compact prompt is **appended as a plain `user` string** to the **end of the existing main-agent (opus-4-7) conversation**. Same model, same system prompt, same tool catalog (10 tools at the time of `/compact`) — the model is asked to summarize the conversation it just had with itself in-place. The next API call (post-compact) sees a 2-message thread where the entire prior conversation has been replaced by the model's own `<analysis>` + `<summary>` output, prefixed with `"This session is being continued from a previous conversation that ran out of context."`

Captured in `log-2026-04-23-11-26-38.jsonl` `req_23 msg[26]` (5581-char user string) → `req_24 msg[1]` (post-compact continuation, 2 messages total).

### 8. Transparently unobserved / partial captures

- **All 30 main-agent built-in schemas captured** (8 core + 22 deferred). The second trace explicitly invoked ToolSearch with `select:` for every deferred tool, including the previously-missing `EnterPlanMode`, `NotebookEdit`, `TaskOutput`. Schemas now live in [`tools-2-1-118.json`](tools-2-1-118.json) without placeholders.
- **No "without ToolSearch" capture** for Explore / Plan sub-agents in v2.1.118: both traces used `ENABLE_TOOL_SEARCH=true`. Therefore there is no `tools-2-1-118.json` (full enumeration) under `explore/` or `plan/` — only their `core-tools-2-1-118.json`. The total tool counts (Explore: 7 core + ~16 deferred ≈ 23; Plan: 5 core + ~15 deferred ≈ 20) are inferred from the deferred list inside the main-agent system-reminder (sub-agents inherit it minus the tools they explicitly exclude).
- **`TaskOutput`** description was rewritten in v2.1.118 to differentiate bash / `local_agent` / `remote_agent` task types — the `local_agent` `.output` file is now a JSONL transcript (do NOT Read it directly, it overflows context). Only documented after the fuller trace was captured.

---

## Architecture Overview

Claude Code uses a multi-agent architecture. The **main agent** (Opus 4.7) orchestrates work and can spawn specialized **sub-agents**. Tool loading uses `ENABLE_TOOL_SEARCH` (default: `auto`) — when tool definitions exceed ~10% of the context window, ToolSearch activates and defers most tools behind on-demand loading.

### Without ToolSearch (`ENABLE_TOOL_SEARCH=false` or below threshold)

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 30 built-in tools (all loaded directly) + N MCP tools
  |-- spawns --> Explore Agent (opus-4-7, 23 tools)
  |-- spawns --> File Search Agent (haiku-4-5, 21 tools)
  |-- spawns --> Plan Agent (opus-4-7, 20 tools)
  |-- spawns --> Code Guide Agent (haiku-4-5, 4 tools)
  |-- spawns --> Status Line Agent (sonnet-4-6, 2 tools)
```

### With ToolSearch (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered)

Only core tools load upfront. Remaining tools are deferred and must be fetched via `ToolSearch` before use. Saves ~45K tokens of initial context.

```
Main Agent (claude-opus-4-7, 1M context)
  |-- 8 core tools: Agent, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write
  |-- 22 deferred built-in tools (loaded on demand via ToolSearch):
  |     AskUserQuestion, CronCreate/Delete/List, EnterPlanMode,
  |     EnterWorktree, ExitPlanMode, ExitWorktree,
  |     ListMcpResourcesTool, Monitor, NotebookEdit,
  |     PushNotification, ReadMcpResourceTool, RemoteTrigger,
  |     TaskCreate/Get/List/Output/Stop/Update, WebFetch, WebSearch
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
  |-- triggers --> auxiliary/compact (context compression)
  |-- triggers --> auxiliary/summarize_conversation (session title generation)
  |-- triggers --> auxiliary/slug_name (kebab-case slug, NEW v2.1.118)
```

---

## Directory Structure

```
claudecode/
  README.md
  ClaudeCodeSystem-2-1-118.md            # Main agent system prompt
  ClaudeCodeTools-2-1-118.md             # Main agent tools (human-readable, 30 built-in tools)
  tools-2-1-118.json                     # All 30 built-in tool schemas (full)
  core-tools-2-1-118.json                # 8 core tools JSON (with ToolSearch active)
  system-reminders-2-1-118.md            # Runtime <system-reminder> templates
  code_guide/                            # Code Guide sub-agent (haiku-4-5)
  explore/                               # Explore sub-agent (opus-4-7)
    core-tools-2-1-118.json              #   7 core tools (with ToolSearch)
  file_search/                           # File Search sub-agent (haiku-4-5, no ToolSearch)
  plan/                                  # Plan sub-agent (opus-4-7)
    core-tools-2-1-118.json              #   5 core tools (with ToolSearch)
  status_line/                           # Status Line sub-agent (sonnet-4-6, no ToolSearch)
  auxiliary/                             # Non-agent functional prompts
    compact-2-1-118.md
    summarize_conversation-2-1-118.md
    slug_name-2-1-118.md                 #   NEW in v2.1.118
```

---

## File Index

### Main Agent (root)

| File | Description |
| --- | --- |
| [ClaudeCodeSystem-2-1-118.md](ClaudeCodeSystem-2-1-118.md) | Main agent system prompt. Model: Opus 4.7, 1M context. Knowledge cutoff January 2026. Section "Text output (does not apply to tool calls)" name preserved. Glob/Grep references replaced with `find`/`grep` via Bash; ultrareview clarification added; final "Length limits" line removed. |
| [ClaudeCodeTools-2-1-118.md](ClaudeCodeTools-2-1-118.md) | Human-readable description of all **30 built-in main-agent tools**. Glob/Grep removed; Bash description has new git/cd/find-regex/--no-edit guidance; TaskOutput description rewritten for new task types. |
| [tools-2-1-118.json](tools-2-1-118.json) | Full JSON schemas for all 30 built-in tools (8 core + 22 deferred). Captured from `log-2026-04-23-12-00-42.jsonl` where ToolSearch was explicitly invoked to load every deferred schema. |
| [core-tools-2-1-118.json](core-tools-2-1-118.json) | JSON schema for the 8 core tools when ToolSearch is active: Agent, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write. The remaining 22 deferred tools are fetched on demand. |
| [system-reminders-2-1-118.md](system-reminders-2-1-118.md) | Runtime `<system-reminder>` templates: Deferred Tools, MCP, Skills, Plan Mode Active, Auto Mode Active, **Plan File Exists (NEW)**, **Auto Mode Still Active (NEW)**, Context (with `# userEmail`). |

### Sub-Agents

| Directory | Agent | Model | Tools (no ToolSearch) | Tools (with ToolSearch) | v2.1.118 changes |
| --- | --- | --- | --- | --- | --- |
| [explore/](explore/) | Explore | opus-4-7 | 23 (inferred — not captured) | **7 core + ToolSearch** (captured) | −Glob, −Grep |
| [file_search/](file_search/) | File Search | haiku-4-5 | **21** (captured — direct load, no ToolSearch) | n/a | −Glob, −Grep |
| [plan/](plan/) | Plan | opus-4-7 | 20 (inferred — not captured) | **5 core + ToolSearch** (captured) | −Glob, −Grep |
| [code_guide/](code_guide/) | Code Guide | haiku-4-5 | **4** (Bash, Read, WebFetch, WebSearch) | n/a | −Glob, −Grep, **+Bash** |
| [status_line/](status_line/) | Status Line | sonnet-4-6 | **2** (Read, Edit) | n/a | unchanged (vim mode enum widened) |

### Auxiliary Prompts (`auxiliary/`)

| File | Trigger | Description |
| --- | --- | --- |
| [auxiliary/compact-2-1-118.md](auxiliary/compact-2-1-118.md) | `/compact` | Context-compression prompt (5581 chars). Injected as a plain `user` message at the end of the main agent's own conversation — the main `opus-4-7` agent self-summarizes in-place, no separate model call. See section 7 of the changelog. |
| [auxiliary/summarize_conversation-2-1-118.md](auxiliary/summarize_conversation-2-1-118.md) | Session start | Session-title generator (3-7 words, sentence case). Verified byte-identical to v2.1.114. |
| [auxiliary/slug_name-2-1-118.md](auxiliary/slug_name-2-1-118.md) | Plan-file / memory-file slug | **NEW in v2.1.118.** Generates a 2-4 word kebab-case slug for plan files (`~/.claude/plans/<slug>.md`) and similar internal naming. |

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
