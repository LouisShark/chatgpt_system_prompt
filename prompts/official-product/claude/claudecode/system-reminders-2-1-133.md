# System Reminders (v2.1.133)

Runtime `<system-reminder>` blocks injected into the **first user message** (`msg[0]`) of each API request. These are NOT part of the system prompt — they appear as multiple content parts prepended to the user's actual message.

**Injection pattern:** All system-reminders are packed into `msg[0]` as separate content parts, followed by the user's actual text as the final part. Subsequent user messages (`msg[2]`, `msg[4]`, ...) carry no system-reminders **except** the slim "Auto Mode still active" follow-up (introduced in v2.1.118) and the post-`/compact` continuation block. Since the Anthropic API sends the full conversation history on every request, `msg[0]`'s reminders are always visible to the model.

```
msg[0] (user):
  part[0]: <system-reminder> Deferred Tools List          (only when ToolSearch active)
  part[1]: <system-reminder> MCP Server Instructions      (when MCP servers configured)
  part[2]: <system-reminder> Skills List                  (always)
  part[3]: <system-reminder> Plan Mode Active             (when EnterPlanMode triggered; replaces Auto Mode block in plan mode)
  part[3 alt]: <system-reminder> Auto Mode Active         (when permissions.defaultMode == "auto" AND not in plan mode)
  part[3 alt]: <system-reminder> Plan File Exists         (when continuing a session that has a saved plan file)
  part[4]: <system-reminder> Context (CLAUDE.md + memory + userEmail + currentDate)  (always)
  part[5]: (actual user message text, possibly preceded by /<command> caveat blocks)
msg[1] (assistant): ...
msg[2] (user):
  part[0..n-1]: tool-result wrappers, possibly the slim "Auto Mode Still Active" reminder
  part[n]: (user text)
...
```

> **Plan mode vs Auto mode coexistence:** when both apply, `Plan Mode Active` and `Auto Mode Active` reminders are both emitted (Plan first, Auto second). Plan mode supersedes any conflict.

---

## Part 0: Deferred Tools List

**Condition:** Only present when ToolSearch is active (`ENABLE_TOOL_SEARCH=true` or auto-threshold triggered).

```xml
<system-reminder>
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query "select:<name>[,<name>...]" to load tool schemas before calling them:
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
PushNotification
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

**v2.1.133 changes vs v2.1.118:**

- **Built-in deferred list is now 21 entries** (down from 22). `AskUserQuestion` was promoted to **core** in v2.1.133 — it now loads upfront with `Agent`, `Bash`, `Edit`, `Read`, `ScheduleWakeup`, `Skill`, `ToolSearch`, and `Write` and is no longer enumerated in this reminder.
- `ListMcpResourcesTool` and `ReadMcpResourceTool` remain in the deferred list (no change from v2.1.118).
- The `{{mcp_tool_names}}` line is replaced at runtime with one entry per available MCP tool, in the form `mcp__{{server_name}}__{{tool_name}}` (one per line). When the user has no MCP servers configured, it expands to nothing.

**Initial-session caveat:** The very first deferred-list reminder of a fresh session sometimes omits both the MCP resource tools and the `mcp__*` per-tool enumeration if MCP servers haven't completed their handshake yet. From the second turn onward (and for any new session where MCP is healthy), the list contains all 21 built-in entries plus per-MCP-tool names. (In the v2.1.133 capture trace, `log-2026-05-08-06-36-15.jsonl` req 2, every MCP resource tool and the user's six MCP servers are listed in full because MCP had completed its handshake before the first request.)

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

(structure unchanged from v2.1.114)

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
- fewer-permission-prompts: Scan transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist...
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo). Omit the interval to let the model self-pace.
- schedule: Create, update, list, or run scheduled remote agents (triggers) that execute on a cron schedule.
- claude-api: Build, debug, and optimize Claude API / Anthropic SDK apps.
{{user_custom_skills}}
- init: Initialize a new CLAUDE.md file with codebase documentation
- statusline: Set up Claude Code's status line UI
- review: Review a pull request
- security-review: Complete a security review of the pending changes on the current branch
- insights: Generate a report analyzing your Claude Code sessions
- team-onboarding: Help teammates ramp on Claude Code with a guide from your usage

Available plugin skills:
{{plugin_skills}}
</system-reminder>
```

(structure unchanged from v2.1.114; the same built-in skill list is observed.)

---

## Part 3a: Plan Mode Active

**Condition:** Present after `EnterPlanMode` is called. Stays active until `ExitPlanMode` is called or the session leaves plan mode. Always appears **before** the Auto Mode reminder when both apply.

```xml
<system-reminder>
Plan mode is active. The user indicated that they do not want you to execute yet -- you MUST NOT make any edits (with the exception of the plan file mentioned below), run any non-readonly tools (including changing configs or making commits), or otherwise make any changes to the system. This supercedes any other instructions you have received.

## Plan File Info:
No plan file exists yet. You should create your plan at {{plan_file_path}} using the Write tool.
You should build your plan incrementally by writing to or editing this file. NOTE that this is the only file you are allowed to edit - other than this you are only allowed to take READ-ONLY actions.

## Plan Workflow

### Phase 1: Initial Understanding
Goal: Gain a comprehensive understanding of the user's request by reading through code and asking them questions. Critical: In this phase you should only use the Explore subagent type.

1. Focus on understanding the user's request and the code associated with their request. Actively search for existing functions, utilities, and patterns that can be reused — avoid proposing new code when suitable implementations already exist.

2. **Launch up to 3 Explore agents IN PARALLEL** (single message, multiple tool calls) to efficiently explore the codebase.
   - Use 1 agent when the task is isolated to known files, the user provided specific file paths, or you're making a small targeted change.
   - Use multiple agents when: the scope is uncertain, multiple areas of the codebase are involved, or you need to understand existing patterns before planning.
   - Quality over quantity - 3 agents maximum, but you should try to use the minimum number of agents necessary (usually just 1)
   - If using multiple agents: Provide each agent with a specific search focus or area to explore. Example: One agent searches for existing implementations, another explores related components, a third investigating testing patterns

### Phase 2: Design
Goal: Design an implementation approach.

Launch Plan agent(s) to design the implementation based on the user's intent and your exploration results from Phase 1.

You can launch up to 1 agent(s) in parallel.

**Guidelines:**
- **Default**: Launch at least 1 Plan agent for most tasks - it helps validate your understanding and consider alternatives
- **Skip agents**: Only for truly trivial tasks (typo fixes, single-line changes, simple renames)

In the agent prompt:
- Provide comprehensive background context from Phase 1 exploration including filenames and code path traces
- Describe requirements and constraints
- Request a detailed implementation plan

### Phase 3: Review
Goal: Review the plan(s) from Phase 2 and ensure alignment with the user's intentions.
1. Read the critical files identified by agents to deepen your understanding
2. Ensure that the plans align with the user's original request
3. Use AskUserQuestion to clarify any remaining questions with the user

### Phase 4: Final Plan
Goal: Write your final plan to the plan file (the only file you can edit).
- Begin with a **Context** section: explain why this change is being made — the problem or need it addresses, what prompted it, and the intended outcome
- Include only your recommended approach, not all alternatives
- Ensure that the plan file is concise enough to scan quickly, but detailed enough to execute effectively
- Include the paths of critical files to be modified
- Reference existing functions and utilities you found that should be reused, with their file paths
- Include a verification section describing how to test the changes end-to-end (run the code, use MCP tools, run tests)

### Phase 5: Call ExitPlanMode
At the very end of your turn, once you have asked the user questions and are happy with your final plan file - you should always call ExitPlanMode to indicate to the user that you are done planning.
This is critical - your turn should only end with either using the AskUserQuestion tool OR calling ExitPlanMode. Do not stop unless it's for these 2 reasons

**Important:** Use AskUserQuestion ONLY to clarify requirements or choose between approaches. Use ExitPlanMode to request plan approval. Do NOT ask about plan approval in any other way - no text questions, no AskUserQuestion. Phrases like "Is this plan okay?", "Should I proceed?", "How does this plan look?", "Any changes before we start?", or similar MUST use ExitPlanMode.

NOTE: At any point in time through this workflow you should feel free to ask the user questions or clarifications using the AskUserQuestion tool. Don't make large assumptions about user intent. The goal is to present a well researched plan to the user, and tie any loose ends before implementation begins.
</system-reminder>
```

**Notes:**

- `{{plan_file_path}}` is auto-generated under `~/.claude/plans/<kebab-case-slug>.md`. The slug itself is generated by the `slug_name` auxiliary haiku call (see `auxiliary/slug_name-2-1-133.md`).
- While in plan mode, the main agent's available tools (with ToolSearch active) are: `Agent, AskUserQuestion, Bash, Edit, ExitPlanMode, Read, ScheduleWakeup, Skill, ToolSearch, Write` (10 total — same composition as v2.1.118, but `AskUserQuestion` is now **core** rather than fetched via ToolSearch). Per the prompt, `Edit`/`Write` are restricted to the designated plan file only.
- Triggered by the deferred `EnterPlanMode` tool (the tool name appears in the deferred-tools list of every ToolSearch-active request).

---

## Part 3b: Auto Mode Active

**Condition:** Present in `msg[0]` when `permissions.defaultMode == "auto"` in `settings.json` (or `--auto` flag is set). Coexists with Plan Mode reminder when both apply (Plan rules take priority).

```xml
<system-reminder>
## Auto Mode Active

Auto mode is active. The user chose continuous, autonomous execution. You should:

1. **Execute immediately** — Start implementing right away. Make reasonable assumptions and proceed on low-risk work.
2. **Minimize interruptions** — Prefer making reasonable assumptions over asking questions for routine decisions.
3. **Prefer action over planning** — Do not enter plan mode unless the user explicitly asks. When in doubt, start coding.
4. **Expect course corrections** — The user may provide suggestions or course corrections at any point; treat those as normal input.
5. **Do not take overly destructive actions** — Auto mode is not a license to destroy. Anything that deletes data or modifies shared or production systems still needs explicit user confirmation. If you reach such a decision point, ask and wait, or course correct to a safer method instead.
6. **Avoid data exfiltration** — Post even routine messages to chat platforms or work tickets only if the user has directed you to. You must not share secrets (e.g. credentials, internal documentation) unless the user has explicitly authorized both that specific secret and its destination.
</system-reminder>
```

(structure unchanged from v2.1.114)

---

## Part 3c: Plan File Exists

**Condition:** Present when continuing a session where a plan file was already saved during a prior plan-mode invocation. Replaces the Plan Mode Active reminder once plan mode is exited but the plan file remains on disk; the model is reminded of the plan it produced so subsequent execution turns can refer back to it.

```xml
<system-reminder>
A plan file exists from plan mode at: {{plan_file_path}}

Plan contents:

{{plan_contents}}
</system-reminder>
```

**Notes:**

- The full plan markdown is inlined verbatim into the reminder (not a file pointer), so the model always has the canonical approach in context without needing a separate Read call.
- Observed in post-`/compact` continuation requests where the prior turns had used `EnterPlanMode` → wrote a plan → `ExitPlanMode` → started implementation.
- Coexists with `Auto Mode Active` (or its slim follow-up) when auto mode is also on.

---

## Part 3d: Auto Mode Still Active

**Condition:** Slim follow-up reminder injected into **subsequent** user messages (`msg[1]`, `msg[2]`, ... — i.e., any user turn after the first one) while auto mode remains active. Saves tokens vs. re-emitting the full 6-rule directive.

```xml
<system-reminder>
Auto mode still active (see full instructions earlier in conversation). Execute autonomously, minimize interruptions, prefer action over planning.
</system-reminder>
```

**Notes:**

- Acts as a one-line refresher pointing back to the full `Auto Mode Active` block from `msg[0]`.
- Helps long sessions stay in auto mode after `/compact` truncations or after many turns push the original directive deep into history.

---

## Part 3e: Task Tools Nudge (NEW capture, mid-conversation)

**Condition:** Injected into a mid-conversation user message (alongside tool-result wrappers, not at `msg[0]`) when the harness detects that **`TaskCreate` / `TaskUpdate` haven't been used recently** but the conversation is doing multi-step work that would benefit from tracking. Observed at `req 14 msg[10]` and `req 15 msg[10]` of the v2.1.133 trace, both times after the main agent had run multiple `Agent` sub-agent calls without tracking them as tasks.

```xml
<system-reminder>
The task tools haven't been used recently. If you're working on tasks that would benefit from tracking progress, consider using TaskCreate to add new tasks and TaskUpdate to update task status (set to in_progress when starting, completed when done). Also consider cleaning up the task list if it has become stale. Only use these if relevant to the current work. This is just a gentle reminder - ignore if not applicable. Make sure that you NEVER mention this reminder to the user
</system-reminder>
```

**Notes:**

- Carries an explicit *"NEVER mention this reminder to the user"* instruction — the model should silently consider whether tasks would help, not announce that it received the nudge.
- Trigger heuristic isn't visible in the trace, but observed firing only after several minutes of work without a `TaskCreate` call. Likely a debounced timer or a tool-call-count threshold in the harness.

---

## Part 4: Context (CLAUDE.md + memory + userEmail + currentDate)

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

Contents of {{memory_directory}}/MEMORY.md (user's auto-memory, persists across conversations):

{{memory_index_content}}

# userEmail
The user's email address is {{user_email}}.

# currentDate
Today's date is {{YYYY/MM/DD}}.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

**v2.1.133 vs v2.1.118:** structure unchanged. Still includes `# userEmail` and `# currentDate` at the bottom. MEMORY.md is inlined under the same `# claudeMd` umbrella as the global/project CLAUDE.md (the v2.1.133 trace `log-2026-05-08-06-36-15.jsonl` req 2 confirms this).

**Notes:**

- CLAUDE.md files are loaded in order: global (`~/.claude/CLAUDE.md`) → project root → subdirectories.
- `@import` directives in CLAUDE.md (e.g. `@some-other.md`) are resolved and inlined.
- The trailing `IMPORTANT` disclaimer is always appended at the end.

---

## Part 5: User's Actual Message (and slash-command caveats)

The user's actual input text. No `<system-reminder>` tags.

When the user invokes a slash command (e.g. `/compact`, `/help`, custom skills), the message content is preceded by:

```xml
<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>
<command-name>/{{name}}</command-name>
<command-message>{{name}}</command-message>
<command-args>{{args}}</command-args>
<local-command-stdout>{{output_of_local_command}}</local-command-stdout>
{{actual_user_text}}
```

The `<local-command-stdout>` carries the output of any local-side command the harness ran (e.g. `Compacted` after `/compact`). Treat it as informational — the actual user instruction is the trailing plain text.

---

## Tool-result wrappers (always-on)

Every assistant tool call is reflected back into subsequent user messages as paired wrappers:

```xml
<system-reminder>
Called the {{tool_name}} tool with the following input: {{tool_input_json}}
</system-reminder>
```

```xml
<system-reminder>
Result of calling the {{tool_name}} tool:
{{tool_result_text}}
</system-reminder>
```

After `/compact`, the same pattern is preserved for the still-relevant tool calls that survived compaction; long stale tool-result bodies may be elided.

---

## Sub-agent System Reminders

Sub-agents (Explore, File Search, Plan, Code Guide, Status Line) receive their own context via system-reminders in their first user message, with a slimmer structure:

```xml
<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
{{claude_md_content}}

# memory
Contents of MEMORY.md from {{memory_directory}}:
{{memory_index_content}}

# userEmail
The user's email address is {{user_email}}.

# currentDate
Today's date is {{YYYY/MM/DD}}.
</system-reminder>
```

Sub-agents do NOT receive:

- The Skills List (main-agent only — sub-agents can't invoke skills directly).
- The MCP Server Instructions (only main agent and File Search agent).
- The Auto Mode reminder (sub-agents inherit the parent's permission mode but don't re-emit the directive).
- The Plan Mode Active / Plan File Exists reminders.
