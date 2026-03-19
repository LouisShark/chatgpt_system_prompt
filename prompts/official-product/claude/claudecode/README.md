# Claude Code System Prompts

Extracted from Claude Code CLI (Anthropic's official agentic coding tool).

**Version**: 2.1.78 / 2.1.79 (March 2026)
**Source**: API traffic capture (MITM proxy on `api.anthropic.com`)

---

## Architecture Overview

Claude Code uses a multi-agent architecture. The **main agent** (Opus) orchestrates work and can spawn specialized **sub-agents** (Opus/Haiku/Sonnet) for specific tasks. Tools are split into 9 always-loaded core tools and 20+ deferred tools loaded on demand via `ToolSearch`.

```
User Input
  |
  v
Main Agent (claude-opus-4-6)
  |-- 9 core tools (always loaded)
  |-- 20 deferred tools (loaded via ToolSearch)
  |-- system-reminders (injected at runtime)
  |
  |-- spawns --> File Search Agent (haiku)
  |-- spawns --> Explore Agent (opus)
  |-- spawns --> Plan Agent (opus)
  |-- spawns --> Code Guide Agent (haiku)
  |-- spawns --> Status Line Agent (sonnet)
  |
  |-- triggers --> auxiliary/compact (context compression)
  |-- triggers --> auxiliary/suggestion_mode (input prediction)
  |-- triggers --> auxiliary/new_topic (topic detection)
  |-- triggers --> auxiliary/summarize_conversation (title generation)
  |-- triggers --> auxiliary/insights (9-stage usage analysis)
```

---

## Directory Structure

```
claudecode/
  README.md
  ClaudeCodeSystem-2-1-78.md           # Main agent system prompt
  ClaudeCodeTools-2-1-78.md            # Main agent tools (readable)
  tools-2-1-78.json                    # Main agent core tools (9)
  deferred-tools-2-1-78.json           # Main agent deferred tools (20)
  system-reminders-2-1-78.md           # Runtime system-reminder templates
  code_guide/                          # Code Guide sub-agent
  explore/                             # Explore sub-agent
  file_search/                         # File Search sub-agent
  plan/                                # Plan sub-agent
  status_line/                         # Status Line sub-agent
  auxiliary/                           # Non-agent functional prompts
```

---

## File Index

### Main Agent (root)

| File | Description |
|------|-------------|
| [ClaudeCodeSystem-2-1-78.md](ClaudeCodeSystem-2-1-78.md) | Main agent system prompt. Defines core behavior: task execution, tool usage, tone/style, output efficiency, memory system (updated with 2.1.79 memory verification rules). Sent as the `system` parameter on every main-thread API call. |
| [ClaudeCodeTools-2-1-78.md](ClaudeCodeTools-2-1-78.md) | Human-readable description of all main agent tools (core + deferred). Markdown format with parameter docs. |
| [tools-2-1-78.json](tools-2-1-78.json) | JSON schema of the 9 core tools always loaded: Agent, Bash, Glob, Grep, Read, Edit, Write, Skill, ToolSearch. |
| [deferred-tools-2-1-78.json](deferred-tools-2-1-78.json) | JSON schema of 20 deferred tools loaded on demand via ToolSearch: AskUserQuestion, TaskCreate/Get/List/Update/Output/Stop, WebFetch, WebSearch, EnterPlanMode, ExitPlanMode, EnterWorktree, ExitWorktree, LSP, NotebookEdit, CronCreate/Delete/List, mcp__ide__getDiagnostics, mcp__ide__executeCode. |
| [system-reminders-2-1-78.md](system-reminders-2-1-78.md) | Runtime `<system-reminder>` templates injected into conversation messages. Includes: plan mode workflow (5 phases), skill list, CLAUDE.md loading, task tool reminders, IDE file-open notifications, deferred tool lists per agent type. |

### Sub-Agents

Each sub-agent has its own system prompt, tool set, and (for some) deferred tools. Spawned by the main agent via the `Agent` tool.

| Directory | Agent | Model | Trigger | Files |
|-----------|-------|-------|---------|-------|
| [code_guide/](code_guide/) | Code Guide | haiku | User asks "How do I...", "Can Claude..." about Claude Code, Agent SDK, or Claude API | system prompt + tools (5). All tools loaded directly, no deferred tools. |
| [explore/](explore/) | Explore | opus | `subagent_type=Explore` or broad codebase research | system prompt + tools (8) + deferred-tools (15). Read-only. Missing vs main: AskUserQuestion, EnterPlanMode, ExitPlanMode, TaskOutput, TaskStop. |
| [file_search/](file_search/) | File Search | haiku | Internal file search operations | system prompt + tools (19). All tools loaded directly, no deferred tools. |
| [plan/](plan/) | Plan | opus | `EnterPlanMode` or non-trivial implementation tasks | system prompt + tools (6) + deferred-tools (14). Read-only. Missing vs main: AskUserQuestion, EnterPlanMode, ExitPlanMode, TaskOutput, TaskStop, NotebookEdit. |
| [status_line/](status_line/) | Status Line | sonnet | `subagent_type=statusline-setup` | system prompt + tools (2: Read, Edit). No deferred tools. |

### Auxiliary Prompts (auxiliary/)

Non-agent functional prompts triggered by specific system events.

| File | Trigger | Description |
|------|---------|-------------|
| [auxiliary/compact-2-1-79.md](auxiliary/compact-2-1-79.md) | Context window approaching limit | Injected as a user message to compress conversation history. Claude produces a `<summary>` block capturing: primary request, technical concepts, files/code, errors, user messages, pending tasks, current work, next step. |
| [auxiliary/suggestion_mode-2-1-62.md](auxiliary/suggestion_mode-2-1-62.md) | After each assistant turn | Predicts what the user would naturally type next (2-12 words). Used for input auto-suggestion UI. |
| [auxiliary/new_topic-2-1-12.md](auxiliary/new_topic-2-1-12.md) | Each user message | Detects if a message starts a new conversation topic. Returns JSON `{isNewTopic, title}`. |
| [auxiliary/summarize_conversation-2-1-12.md](auxiliary/summarize_conversation-2-1-12.md) | Session end or title generation | Generates a 5-10 word title for the conversation. |
| [auxiliary/insights-2-1-78.md](auxiliary/insights-2-1-78.md) | `/insights` command | 9-stage analysis pipeline for user usage reports. Stages: facets extraction, memorable moment, what's working, project areas, friction points, interaction style, future opportunities, suggestions, at-a-glance summary. |
