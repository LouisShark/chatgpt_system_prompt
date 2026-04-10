# System Reminders (v2.1.100)

Runtime `<system-reminder>` blocks injected into the **first user message** (`msg[0]`) of each API request. These are NOT part of the system prompt — they appear as multiple content parts prepended to the user's actual message.

**Injection pattern:** All system-reminders are packed into `msg[0]` as separate content parts, followed by the user's actual text as the final part. Subsequent user messages (`msg[2]`, `msg[4]`, etc.) carry no system-reminders. Since the Anthropic API sends the full conversation history on every request, `msg[0]`'s reminders are always visible to the model.

```
msg[0] (user):
  part[0]: <system-reminder> Deferred Tools List     (only when ToolSearch active)
  part[1]: <system-reminder> MCP Server Instructions  (when MCP servers configured)
  part[2]: <system-reminder> Skills List              (always)
  part[3]: <system-reminder> Context (CLAUDE.md + date + memory)  (always)
  part[4]: (actual user message text)
msg[1] (assistant): ...
msg[2] (user): (no system-reminders, just user text)
...
```

---

## Part 0: Deferred Tools List

**Condition:** Only present when ToolSearch is active (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered).

```xml
<system-reminder>
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query "select:<name>[,<name>...]" to load tool schemas before calling them:
AskUserQuestion
CronCreate
CronDelete
CronList
EnterPlanMode
EnterWorktree
ExitPlanMode
ExitWorktree
ListMcpResourcesTool
Monitor
NotebookEdit
ReadMcpResourceTool
RemoteTrigger
TaskCreate
TaskGet
TaskList
TaskOutput
TaskStop
TaskUpdate
WebFetch
WebSearch
{{mcp_tool_names}}
</system-reminder>
```

---

## Part 1: MCP Server Instructions

**Condition:** Present when MCP servers are configured and provide usage instructions.

```xml
<system-reminder>
# MCP Server Instructions

The following MCP servers have provided instructions for how to use their tools and resources:

## {{server_name_1}}
{{server_instructions_1}}

## {{server_name_2}}
{{server_instructions_2}}
</system-reminder>
```

---

## Part 2: Skills List

**Condition:** Always present. Lists all available skills (built-in + user custom + plugin skills) for the `Skill` tool.

```xml
<system-reminder>
The following skills are available for use with the Skill tool:

- update-config: Use this skill to configure the Claude Code harness via settings.json. Automated behaviors ("from now on when X", "each time X", "whenever X", "before/after X") require hooks configured in settings.json...
- keybindings-help: Use when the user wants to customize keyboard shortcuts...
- debug: Enable debug logging for this session and help diagnose issues
- simplify: Review changed code for reuse, quality, and efficiency, then fix any issues found.
- batch: Research and plan a large-scale change, then execute it in parallel across 5–30 isolated worktree agents...
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo, defaults to 10m)
- schedule: Create, update, list, or run scheduled remote agents (triggers) that execute on a cron schedule.
- claude-api: Build Claude API / Anthropic SDK apps.
{{user_custom_skills}}
- init: Initialize a new CLAUDE.md file with codebase documentation
- statusline: Set up Claude Code's status line UI
- review: Review a pull request
- security-review: Complete a security review of the pending changes on the current branch
- insights: Generate a report analyzing your Claude Code sessions

Available plugin skills:
{{plugin_skills}}
</system-reminder>
```

**Notes:**
- Built-in skills (init, statusline, review, security-review, insights) are always listed
- User custom skills come from `.claude/skills/` directories and CLAUDE.md skill definitions
- Plugin skills come from enabled plugins in `settings.json`
- Each skill entry includes a description and trigger conditions (truncated with `…` if too long)

---

## Part 3: Context (CLAUDE.md + Date + Memory)

**Condition:** Always present. Combines multiple context sources into one system-reminder.

```xml
<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of {{user_global_claude_md_path}} (user's private global instructions for all projects):

{{global_claude_md_content}}

Contents of {{project_claude_md_path}} (project-specific instructions):

{{project_claude_md_content}}

# currentDate
Today's date is {{YYYY/MM/DD}}.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

**Notes:**
- CLAUDE.md files are loaded in order: global (`~/.claude/CLAUDE.md`) → project root → subdirectories
- `@import` directives in CLAUDE.md (e.g. `@other-file.md`) are resolved and inlined
- When auto memory is active, a `# memory` section with MEMORY.md contents may also be included
- The trailing `IMPORTANT` disclaimer is always appended at the end

---

## Part 4: User's Actual Message

The user's actual input text. No `<system-reminder>` tags.

---

## Sub-agent System Reminders

Sub-agents receive their own context via system-reminders in their first user message, with a slightly different structure:

```xml
<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
{{claude_md_content}}

# currentDate
Today's date is {{YYYY/MM/DD}}.

# memory
Contents of MEMORY.md from {{memory_directory}}:
{{memory_index_content}}
</system-reminder>
```

Sub-agents do NOT receive the Skills List or MCP Server Instructions — those are main-agent only.
