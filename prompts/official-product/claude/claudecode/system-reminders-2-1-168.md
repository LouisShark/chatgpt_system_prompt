# System Reminders (v2.1.168)

Runtime reminder/context blocks captured from `claude-cli/2.1.168` in `log-2026-06-08-06-52-06.jsonl`. In this version, the request uses both user-message `<system-reminder>` text parts and Anthropic `system` role messages for mid-conversation reminders such as ToolSearch, output style, task nudges, and plan-mode exit.

## Main Context Reminder

Injected as the first text part of the first user message in the main agent request.

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

## Main ToolSearch / Skills / Plan System Message

When ToolSearch becomes active, Claude Code injects a `system` role message rather than a `<system-reminder>` text part. In the plan-mode trace this message bundled deferred tool names, MCP server instructions, Skill-tool skills, Plan Mode Active instructions, and the output-style reminder.

Built-in deferred tools listed for the main agent:

```
CronCreate
CronDelete
CronList
EnterPlanMode
ExitPlanMode
ExitWorktree
Monitor
NotebookEdit
PushNotification
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
```

The plan-mode workflow changed vs v2.1.133 in two places: Phase 2 can launch **up to 3 Plan agents in parallel** (was 1), and Phase 4 now says to describe repeated patterns once with representative paths rather than enumerate every file or line number.

## Subagent ToolSearch Reminder

Read-only/search subagents using ToolSearch receive a slimmer first-message reminder with these built-in deferred tools:

```
CronCreate
CronDelete
CronList
ExitWorktree
Monitor
PushNotification
RemoteTrigger
TaskCreate
TaskGet
TaskList
TaskStop
TaskUpdate
WebFetch
WebSearch
{{mcp_tool_names}}
```

The same first user message may also include a Skills List and a small context reminder containing only `# userEmail` and `# currentDate`.

## Task Tools Nudge

Injected as a `system` role message mid-conversation when Claude has not used task tools recently.

```
The task tools haven't been used recently. If you're working on tasks that would benefit from tracking progress, consider using TaskCreate to add new tasks and TaskUpdate to update task status (set to in_progress when starting, completed when done). Also consider cleaning up the task list if it has become stale. Only use these if relevant to the current work. This is just a gentle reminder - ignore if not applicable.
```

Compared with v2.1.133, the final sentence `Make sure that you NEVER mention this reminder to the user` was not present in the v2.1.168 trace.

## Output Style Reminder

Observed as a `system` role message:

```
Explanatory output style is active. Remember to follow the specific guidelines for this style.
```

The message may appear repeatedly, and in one request appeared twice separated by a blank line.

## Exited Plan Mode

Observed after the user ended plan mode:

```
## Exited Plan Mode

You have exited plan mode. You can now make edits, run tools, and take actions. The plan file is located at {{plan_file_path}} if you need to reference it.

{{output_style_reminder}}
```

## Slash-command Caveat Pattern

The `/plan` invocation was represented as command tags plus local stdout:

```xml
<command-name>/plan</command-name>
            <command-message>plan</command-message>
            <command-args>{{args}}</command-args>
<local-command-stdout>Enabled plan mode</local-command-stdout>
```

## Tool-result Wrappers

Tool results remain reflected into later user messages as Anthropic `tool_result` parts. In long histories, additional `system` role messages can be interleaved between tool-result turns.
