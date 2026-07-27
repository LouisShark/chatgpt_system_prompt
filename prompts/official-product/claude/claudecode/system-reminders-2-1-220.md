# System Reminders (v2.1.220, partial — SDK-CLI capture)

Runtime reminder/context blocks observed in `claude-cli/2.1.220` `cc_entrypoint=sdk-cli` (`claude -p`) traces. This is a **partial** capture: classes that a short non-interactive `-p` run never triggers are carried over from earlier versions and marked as not re-captured.

## Capture status

| Reminder class | 2.1.220 `-p` capture | Change vs 2.1.201 |
| --- | --- | --- |
| Main Context Reminder | ✅ confirmed | Structure unchanged; `currentDate` format is `YYYY-MM-DD` |
| Deferred tool list (main) | ✅ confirmed | **Names unchanged** (19 built-ins); now observed as part of a `role:"system"` mid-conversation message |
| Tool roster system message (agents/skills) | ✅ confirmed | Documented as one combined `system` message (see below) |
| ToolSearch load result | ✅ confirmed | New section: `tool_reference` blocks + `Tool loaded.` |
| Output Style Reminder | ✅ confirmed | Text unchanged |
| MCP Server Instructions | ❌ not present | No MCP servers in this headless env (`ANTHROPIC_API_KEY` set → claude.ai connectors disabled) |
| Task Tools Nudge | ❌ not triggered in `-p` | Carried over from 2.1.168 |
| Exited Plan Mode | ❌ no plan mode in `-p` | Carried over from 2.1.168 |
| Slash-command Caveat | ❌ not in these traces | Carried over from 2.1.168 |

## Main Context Reminder

Injected as the first text part of the first user message. Structure unchanged from v2.1.201; this capture ran in a non-git temp directory so no project-CLAUDE.md section appeared (placeholder kept below for completeness).

```xml
<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of {{user_global_claude_md_path}} (user's private global instructions for all projects):

{{global_claude_md_content}}

Contents of {{resolved_imported_claude_md_path}} (user's private global instructions for all projects):

{{imported_claude_md_content}}

Contents of {{project_claude_md_path}} (project instructions, checked into the codebase):

{{project_claude_md_content}}

# userEmail
The user's email address is {{user_email}}.

# currentDate
Today's date is {{YYYY-MM-DD}}.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

Note: v2.1.201 documented the date placeholder as `{{YYYY/MM/DD}}`; the actual captured value uses dashes (`2026-07-27`).

## Tool roster system message (deferred tools + agents + skills) — mid-conversation `system` role

With ToolSearch active, the harness injects a **`role:"system"` message** into `messages` (the request carries the `mid-conversation-system-2026-04` beta). One combined message contains, in order: the deferred tool list, the Agent-tool agent types, the Skill-tool skills list, and the output-style reminder line.

### Part 1 — Deferred tool list (names unchanged vs 2.1.201)

```
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query "select:<name>[,<name>...]" to load tool schemas before calling them:
CronCreate
CronDelete
CronList
DesignSync
EnterWorktree
ExitWorktree
Monitor
NotebookEdit
PushNotification
RemoteTrigger
SendMessage
TaskCreate
TaskGet
TaskList
TaskOutput
TaskStop
TaskUpdate
WebFetch
WebSearch
{{mcp_tool_names}}
```

### Part 2 — Agent types roster

```
Available agent types for the Agent tool:
- claude: Catch-all for any task that doesn't fit a more specific agent. FleetView's default when no agent name is typed. (Tools: *)
- Explore: Read-only search agent for broad fan-out searches — when answering means sweeping many files, directories, or naming conventions and you only need the conclusion, not the file dumps. It reads excerpts rather than whole files, so it locates code; it doesn't review or audit it. Specify search breadth: "medium" for moderate exploration, "very thorough" for multiple locations and naming conventions. (Tools: All tools except Agent, Artifact, ExitPlanMode, Edit, Write, NotebookEdit)
- general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: *)
- Plan: Software architect agent for designing implementation plans. Use this when you need to plan the implementation strategy for a task. Returns step-by-step plans, identifies critical files, and considers architectural trade-offs. (Tools: All tools except Agent, Artifact, ExitPlanMode, Edit, Write, NotebookEdit)
- statusline-setup: Use this agent to configure the user's Claude Code status line setting. (Tools: Read, Edit)
{{plugin_and_custom_agents}}

When you launch multiple agents for independent work, send them in a single message with multiple tool uses so they run concurrently.
```

(The capture also contained machine-specific plugin agents, e.g. `codex:codex-rescue` — placeholdered above.)

### Part 3 — Skills roster

```
The following skills are available for use with the Skill tool:

{{skills_list_with_one_line_descriptions}}
```

(Environment-specific: mixes built-in skills — e.g. `loop`, `schedule`, `claude-api`, `run`, `init`, `review`, `security-review`, `dataviz`, `update-config`, `keybindings-help`, `simplify`, `fewer-permission-prompts` — with the user's plugin/custom skills.)

### Part 4 — trailing output-style line

```
Explanatory output style is active. Remember to follow the specific guidelines for this style.
```

## ToolSearch load result — NEW section

When ToolSearch loads deferred tools, its `tool_result` content is **one `tool_reference` block per loaded tool** (expanded into the full definition server-side; the matching full schemas are simultaneously added to the request `tools` array with `defer_loading: true`, keeping the cached prompt prefix untouched):

```json
{"type": "tool_reference", "tool_name": "CronCreate"}
```

The tool_result is followed by a fixed user-visible text part:

```
Tool loaded.
```

## Output Style Reminder

Confirmed, also as a standalone `system` role message after tool results (text unchanged from v2.1.168/2.1.201):

```
Explanatory output style is active. Remember to follow the specific guidelines for this style.
```

## MCP Server Instructions

Not present in this capture: with `ANTHROPIC_API_KEY` set, headless runs print `claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set` and no MCP servers load. See v2.1.201 for the `{{mcp_server_instructions}}` form.

---

## Carried over from v2.1.168/v2.1.201 (not re-captured in these `-p` traces)

### Task Tools Nudge

Injected as a `system` role message mid-conversation when task tools have not been used recently.

```
The task tools haven't been used recently. If you're working on tasks that would benefit from tracking progress, consider using TaskCreate to add new tasks and TaskUpdate to update task status (set to in_progress when starting, completed when done). Also consider cleaning up the task list if it has become stale. Only use these if relevant to the current work. This is just a gentle reminder - ignore if not applicable.
```

### Exited Plan Mode

```
## Exited Plan Mode

You have exited plan mode. You can now make edits, run tools, and take actions. The plan file is located at {{plan_file_path}} if you need to reference it.

{{output_style_reminder}}
```

### Slash-command Caveat Pattern

```xml
<command-name>/{{command}}</command-name>
            <command-message>{{command}}</command-message>
            <command-args>{{args}}</command-args>
<local-command-stdout>{{stdout}}</local-command-stdout>
```
