# Claude Code System Prompts

**Version**: 2.1.100 (April 2026)

---

## What Changed in v2.1.100

### Architecture

- **ToolSearch auto mode** (`ENABLE_TOOL_SEARCH=auto`, default): activates when tool definitions exceed ~10% of context window. On Opus 4.6 (1M context), built-in tools (~45K tokens = 4.5%) don't trigger the threshold, so all 29 tools load directly. On smaller context windows (e.g. 200K Sonnet, ~22.5%) or with many MCP tools, ToolSearch activates and defers to 9 core tools.
- **29 total tools** for the main agent (9 core + 20 deferred when ToolSearch is active).
- **New tools**: `ListMcpResourcesTool`, `Monitor`, `ReadMcpResourceTool`, `RemoteTrigger` — added to main and most sub-agents.
- **Removed from observed set**: `LSP` tool (may still exist as deferred for smaller context windows).

### Main Agent System Prompt

- **"Doing tasks" section rewritten**: Removed old guidance about reading before editing, avoiding time estimates, avoiding brute-forcing. Added new specific guidance about exploratory questions (2-3 sentence replies), no-comment defaults, no backwards-compat hacks.
- **New "Executing actions with care" section**: Detailed guidance on reversibility, blast radius, risky actions requiring confirmation (destructive ops, hard-to-reverse ops, shared-state actions). Replaces the old brief caution note.
- **New "Communication style" section**: Strict brevity rules — 25-word limit between tool calls, 100-word limit for final responses. "Brief is good — silent is not."
- **New "auto memory" system**: Persistent file-based memory with 4 types (user, feedback, project, reference). Includes what NOT to save, how to save (frontmatter + MEMORY.md index), verification before recommending.
- **Model info updated**: Claude 4.6 family (Opus 4.6, Sonnet 4.6, Haiku 4.5). Opus 4.6 with 1M context. Knowledge cutoff May 2025.
- **New "Session-specific guidance"**: `! <command>` prefix for user-run commands, Agent tool guidance, Explore agent threshold (>3 queries).
- **Removed AskUserQuestion references**: Permission denial no longer suggests using AskUserQuestion.

### Sub-Agents

- **Explore agent**: Now has Write, Edit, NotebookEdit tools — **no longer fully read-only**! 23 tools total (was 8 + 15 deferred).
- **File Search agent**: Expanded from 19 specialized tools to 20 general tools (Bash, Cron*, Worktree, Monitor, etc.). Still enforces READ-ONLY in prompt.
- **Plan agent**: Same tool expansion as File Search (20 tools). Still enforces READ-ONLY.
- **Code Guide agent**: Massively expanded prompt (~28K chars). Now includes documentation URLs (code.claude.com, platform.claude.com), user's custom skills list, MCP server config, plugin skills, and settings.json.
- **Status Line agent**: Added `rate_limits` (5-hour/7-day), `vim` mode, `agent`, and `worktree` fields to JSON schema.
- **summarize_conversation**: Updated from v2.1.12 format.

---

## Architecture Overview

Claude Code uses a multi-agent architecture. The **main agent** (Opus 4.6) orchestrates work and can spawn specialized **sub-agents**. Tool loading uses `ENABLE_TOOL_SEARCH` (default: `auto`) — when tool definitions exceed ~10% of the context window, ToolSearch activates and defers most tools behind on-demand loading:

### ToolSearch auto mode (`ENABLE_TOOL_SEARCH=auto`, default)

Default behavior. ToolSearch activates when total tool definition tokens exceed **~10% of the context window**:

| Context Window | Tool Tokens (~29 tools) | Ratio | ToolSearch? |
|---------------|------------------------|-------|-------------|
| 1M (Opus 4.6) | ~45K | 4.5% | No — all 29 tools load directly |
| 200K (Sonnet) | ~45K | 22.5% | **Yes** — 9 core + deferred |
| 1M + many MCP tools | >100K | >10% | **Yes** — 9 core + deferred |

Without ToolSearch (threshold not met):

```
Main Agent (claude-opus-4-6, 1M context)
  |-- 29 tools (all loaded directly, no ToolSearch)
  |-- spawns --> Explore Agent (opus, 23 tools)
  |-- spawns --> File Search Agent (haiku, 20 tools)
  |-- spawns --> Plan Agent (opus, 20 tools)
  |-- spawns --> Code Guide Agent (haiku, 5 tools)
  |-- spawns --> Status Line Agent (sonnet, 2 tools)
```

### With ToolSearch (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered)

Only core tools load upfront. Remaining tools are deferred and must be fetched via `ToolSearch` before use. Saves ~44K tokens of initial context.

```
Main Agent (claude-opus-4-6, 1M context)
  |-- 9 core tools: Agent, Bash, Edit, Glob, Grep, Read, Skill, ToolSearch, Write
  |-- 20 deferred tools (loaded on demand via ToolSearch):
  |     AskUserQuestion, CronCreate/Delete/List, EnterPlanMode,
  |     EnterWorktree, ExitPlanMode, ExitWorktree, ListMcpResourcesTool,
  |     Monitor, NotebookEdit, ReadMcpResourceTool, RemoteTrigger,
  |     TaskCreate/Get/List/Output/Stop/Update, WebFetch, WebSearch
  |-- MCP tools also deferred behind ToolSearch
  |
  |-- spawns --> Explore Agent (opus, 8 core + ToolSearch)
  |-- spawns --> File Search Agent (haiku, 20 tools, NO ToolSearch)
  |-- spawns --> Plan Agent (opus, 6 core + ToolSearch)
  |-- spawns --> Code Guide Agent (haiku, 5 tools, NO ToolSearch)
  |-- spawns --> Status Line Agent (sonnet, 2 tools, NO ToolSearch)
```

### Common auxiliary triggers (both modes)

```
  |-- triggers --> auxiliary/compact (context compression)
  |-- triggers --> auxiliary/suggestion_mode (input prediction)
  |-- triggers --> auxiliary/new_topic (topic detection)
  |-- triggers --> auxiliary/summarize_conversation (title generation)
  |-- triggers --> auxiliary/insights (usage analysis)
```

---

## Directory Structure

```
claudecode/
  README.md
  ClaudeCodeSystem-2-1-100.md          # Main agent system prompt (v2.1.100)
  ClaudeCodeTools-2-1-100.md           # Main agent tools (readable, v2.1.100)
  tools-2-1-100.json                   # All 29 tools JSON (without ToolSearch)
  core-tools-2-1-100.json             # 9 core tools JSON (with ToolSearch enabled)
  system-reminders-2-1-100.md         # Runtime system-reminder templates (v2.1.100)
  code_guide/                          # Code Guide sub-agent
  explore/                             # Explore sub-agent
    core-tools-2-1-100.json           #   8 core tools (with ToolSearch)
    tools-2-1-100.json                #   23 tools (without ToolSearch)
  file_search/                         # File Search sub-agent (no ToolSearch)
  plan/                                # Plan sub-agent
    core-tools-2-1-100.json           #   6 core tools (with ToolSearch)
    tools-2-1-100.json                #   20 tools (without ToolSearch)
  status_line/                         # Status Line sub-agent (no ToolSearch)
  auxiliary/                           # Non-agent functional prompts
```

---

## File Index

### Main Agent (root) — v2.1.100


| File                                                       | Description                                                                                                                                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ClaudeCodeSystem-2-1-100.md](ClaudeCodeSystem-2-1-100.md) | Main agent system prompt. Major additions: "Executing actions with care", "Communication style" (25/100 word limits), "auto memory" (persistent file-based memory with 4 types). Model: Opus 4.6, 1M context. |
| [ClaudeCodeTools-2-1-100.md](ClaudeCodeTools-2-1-100.md)   | Human-readable description of all 29 main agent tools.                                                                                                                                                        |
| [tools-2-1-100.json](tools-2-1-100.json)                   | JSON schema of all 29 tools (without ToolSearch — all loaded directly).                                                                                                                                       |
| [core-tools-2-1-100.json](core-tools-2-1-100.json)         | JSON schema of 9 core tools when ToolSearch is active: Agent, Bash, Edit, Glob, Grep, Read, Skill, **ToolSearch**, Write. The remaining 20 tools are deferred.                                                |
| [system-reminders-2-1-100.md](system-reminders-2-1-100.md) | Runtime `<system-reminder>` templates: deferred tools list, CLAUDE.md/memory context, MCP server instructions.                                                                                                |


### Sub-Agents — v2.1.100


| Directory                    | Agent       | Model  | Tools (no ToolSearch)                     | Tools (with ToolSearch) | Key Changes from v2.1.78                            |
| ---------------------------- | ----------- | ------ | ----------------------------------------- | ----------------------- | --------------------------------------------------- |
| [explore/](explore/)         | Explore     | opus   | 23 (includes Edit, Write)                 | 8 core + ToolSearch     | **No longer read-only** — can now write files       |
| [file_search/](file_search/) | File Search | haiku  | 20 (Bash, Cron*, etc.)                    | 20 (no ToolSearch)      | Expanded from 19 specialized to 20 general tools    |
| [plan/](plan/)               | Plan        | opus   | 20 (same as File Search)                  | 6 core + ToolSearch     | Expanded tools, still read-only                     |
| [code_guide/](code_guide/)   | Code Guide  | haiku  | 5 (Glob, Grep, Read, WebFetch, WebSearch) | 5 (no ToolSearch)       | Prompt expanded to ~28K chars with doc URLs         |
| [status_line/](status_line/) | Status Line | sonnet | 2 (Read, Edit)                            | 2 (no ToolSearch)       | Added rate_limits, vim, agent, worktree JSON fields |


### Auxiliary Prompts (auxiliary/)


| File                                                                                       | Trigger              | Description                                               |
| ------------------------------------------------------------------------------------------ | -------------------- | --------------------------------------------------------- |
| [auxiliary/compact-2-1-100.md](auxiliary/compact-2-1-100.md)                               | Context window limit | Context compression (added CRITICAL no-tool-use preamble) |
| [auxiliary/summarize_conversation-2-1-100.md](auxiliary/summarize_conversation-2-1-100.md) | Session end          | Title generation                                          |


