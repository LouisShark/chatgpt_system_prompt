# System Reminders (v2.1.201, partial — SDK-CLI capture)

Runtime reminder/context blocks observed in `claude-cli/2.1.201` `cc_entrypoint=sdk-cli` (`claude -p`) traces. This is a **partial** capture: some reminder classes were confirmed in the `-p` trace and updated below; classes that a short non-interactive `-p` run never triggers are carried over from v2.1.168 and marked as not re-captured.

## Capture status

| Reminder class | 2.1.201 `-p` capture | Change vs 2.1.168 |
| --- | --- | --- |
| Main Context Reminder | ✅ confirmed | Structure unchanged |
| Deferred tool list (main) | ✅ confirmed | **Names changed** (see below) |
| Output Style Reminder | ✅ confirmed (6×) | Text unchanged |
| MCP Server Instructions | ✅ confirmed (7×) | Env-specific, placeholdered |
| Task Tools Nudge | ❌ not triggered in `-p` | Carried over from 2.1.168 |
| Exited Plan Mode | ❌ no plan mode in `-p` | Carried over from 2.1.168 |
| Slash-command Caveat | ❌ not in these traces | Carried over from 2.1.168 |

## Main Context Reminder

Injected as the first text part of the first user message. Structure is unchanged from v2.1.168.

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
Today's date is {{YYYY/MM/DD}}.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

## Deferred tool list (main agent) — CHANGED

Injected via `system` role message when ToolSearch is active. The full 2.1.201 preamble:

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

Delta vs the v2.1.168 main deferred list (18 built-ins):

| Change | Tools |
| --- | --- |
| **Added** | `DesignSync`, `SendMessage`, `EnterWorktree` |
| **Removed** | `EnterPlanMode`, `ExitPlanMode` |

Notes:
- `EnterWorktree` was a **core** tool in the v2.1.168 interactive capture; in this `-p` main agent it appears as **deferred** — another SDK-CLI vs interactive tool-placement difference.
- `EnterPlanMode` / `ExitPlanMode` drop out because `-p` mode has no plan-mode flow.
- `DesignSync` and `SendMessage` are new deferred built-ins in 2.1.201.

## Output Style Reminder

Confirmed as a `system` role message (appeared 6× across the traces; text unchanged from v2.1.168):

```
Explanatory output style is active. Remember to follow the specific guidelines for this style.
```

## MCP Server Instructions

Confirmed present as part of the ToolSearch/skills `system` message (7×). Content is user-environment-specific (enabled MCP servers and their usage notes) and is placeholdered:

```
{{mcp_server_instructions}}
```

---

## Carried over from v2.1.168 (not re-captured in these `-p` traces)

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
