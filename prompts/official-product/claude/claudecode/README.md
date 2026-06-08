# Claude Code System Prompts

**Version**: 2.1.168 (June 2026)  
**Captured from**: `claude-cli/2.1.168` trace `log-2026-06-08-06-52-06.jsonl` (83 logged HTTP calls: 79 Messages API calls, 2 count_tokens calls, and 2 HEAD probes).

## Upgrade at a Glance

This directory was upgraded from the previous v2.1.133 capture to the v2.1.168 request surface observed in the June 8, 2026 trace.

- Main model surface is now `claude-opus-4-8` with 64k max output and adaptive summarized thinking for the main agent.
- Main built-in catalog changed from **9 core + 21 deferred** tools to **12 core + 18 deferred** tools in the captured ToolSearch mode.
- Newly loaded main core tools: `EnterWorktree`, `SendUserFile`, and `Workflow`.
- `EnterWorktree` moved from deferred to core; MCP resource built-ins from v2.1.133 were not observed as built-in deferred names in this trace.
- File Search changed from direct-loading many deferred schemas to a smaller 6-tool ToolSearch-enabled surface.
- Several mid-conversation reminders now arrive as Anthropic `system` role messages, not only as `<system-reminder>` text parts.
- `summarize_conversation`, `summarize_transcript_chunk`, and `analyze_session_facets` were **not invoked** in this v2.1.168 trace; those files are carried forward from v2.1.133 and marked as not re-captured.
- `custom_agents/*` and `claude/*` are included because they appeared as real request parameters in this local trace. They should not be read as Claude Code core default agents unless verified in another clean trace.

## Audit Method

This update was not a filename-only bump. The trace was walked request-by-request and grouped by normalized system prompt + loaded tool names + request-body parameters.

Trace anchors used for the published files:

| Surface | Trace line(s) | Published files |
| --- | ---: | --- |
| Main agent | 5, 6, 7, 11, 53-60, 62-67, 74, 78, 82, 83 | `ClaudeCodeSystem-2-1-168.md`, `core-tools-2-1-168.json` |
| File Search / read-only search agent | 8-52, 71 | `file_search/ClaudeCodeFileSearchSpecialist-2-1-168.md`, `file_search/tools-2-1-168.json` |
| Code Guide | 68 | `code_guide/ClaudeCodeGuideAgent-2-1-168.md`, `code_guide/tools-2-1-168.json` |
| Wiki ingest custom agent | 69 | `custom_agents/claude_obsidian_wiki_ingest/*` |
| Wiki lint custom agent | 70 | `custom_agents/claude_obsidian_wiki_lint/*` |
| Background `claude` agent | 72 | `claude/*` |
| Codex rescue custom agent | 73 | `custom_agents/codex_rescue/*` |
| Plan agent | 75 | `plan/*` |
| Status line setup agent | 76 | `status_line/*` |
| General-purpose / Explore-style agent | 77 | `explore/*` |
| Job label auxiliary | 61 | `auxiliary/slug_name-2-1-168.md` |
| Compact auxiliary | 79 | `auxiliary/compact-2-1-168.md` |

Lines 80-81 are `/v1/messages/count_tokens` calls over project files, not prompt templates, and are intentionally excluded.

## Summary of Changes vs v2.1.133

### Main Agent Prompt

The main prompt changed substantially, not cosmetically:

- Model moved from Opus 4.7-era documentation to **Claude Opus 4.8** (`claude-opus-4-8`; the captured session uses a 1M context setup in the headers/body).
- The long v2.1.133 software-engineering prompt was collapsed into a shorter structure:
  - `# Harness`
  - `# Session-specific guidance`
  - `# Memory`
  - `# Environment`
  - `# Output Style: Explanatory`
  - `# Background Session`
  - `# Context management`
- The old broad sections (`# System`, `# Doing tasks`, `# Using your tools`, `# Tone and style`, `# Text output`, `# auto memory`) no longer appear in that form.
- Memory changed from the older auto-memory wording to a file-based frontmatter format with `user | feedback | project | reference` memory types.
- The captured main prompt includes background-job behavior and `result:` / `needs input:` / `failed:` classifier conventions.
- Environment guidance now includes:
  - latest model family note: Claude 4.X, Opus 4.8 / Sonnet 4.6 / Haiku 4.5 IDs
  - Claude Code surfaces: CLI, desktop app, web app, IDE extensions
  - Fast mode behavior: Opus fast output, not a smaller-model downgrade

### Main Tool Catalog

v2.1.133 had **9 core + 21 deferred** built-ins. v2.1.168 has **12 core + 18 deferred** built-ins in the captured main-agent ToolSearch mode.

| Category | v2.1.133 | v2.1.168 | Delta |
| --- | --- | --- | --- |
| Main core tools | Agent, AskUserQuestion, Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write | Agent, AskUserQuestion, Bash, Edit, **EnterWorktree**, Read, ScheduleWakeup, **SendUserFile**, Skill, ToolSearch, **Workflow**, Write | +EnterWorktree, +SendUserFile, +Workflow |
| Main deferred tools | Cron*, EnterPlanMode, EnterWorktree, ExitPlanMode, ExitWorktree, ListMcpResourcesTool, Monitor, NotebookEdit, PushNotification, ReadMcpResourceTool, RemoteTrigger, Task*, WebFetch, WebSearch | Cron*, EnterPlanMode, ExitPlanMode, ExitWorktree, Monitor, NotebookEdit, PushNotification, RemoteTrigger, Task*, WebFetch, WebSearch | EnterWorktree promoted to core; MCP resource tools not observed/listed as built-ins in this trace |
| Root JSON schema coverage | 27 verified schemas | 14 verified schemas | Stricter capture: File Search no longer direct-loads 21 deferred schemas |

Important boundary: `tools-2-1-168.json` contains only schemas actually loaded somewhere in this trace: the 12 main core schemas plus `WebFetch` / `WebSearch` from Code Guide. The other 16 deferred built-ins were listed by name but never schema-loaded, so they are not asserted in root JSON.

### How Deferred Tools Work

In the captured ToolSearch mode, deferred tools are visible by name before they are callable. The runtime first injects a deferred tool name list, then Claude must call `ToolSearch` to fetch the matching full JSON schema.

Example direct selection query:

```json
{
  "query": "select:NotebookEdit,TaskCreate,WebFetch",
  "max_results": 5
}
```

`ToolSearch` returns matching schemas inside a `<functions>` block using the same function encoding as the top-level tool list. A deferred tool becomes callable only after its schema appears in that result.

This trace captured the deferred names but did not capture `ToolSearch` responses for 16 of the 18 deferred built-ins. For that reason, this directory records those 16 tools as observed names only, not verified schemas.

### Subagents and Modes

| Surface | v2.1.133 tools | v2.1.168 tools | Prompt/model delta |
| --- | --- | --- | --- |
| File Search | 21 direct-loaded tools, no ToolSearch | 6 core tools: Bash, EnterWorktree, Read, SendUserFile, Skill, ToolSearch | Prompt body effectively same aside from env/model placeholders; loading strategy changed heavily |
| Plan | 5 core: Bash, Read, ScheduleWakeup, Skill, ToolSearch | 6 core: Bash, EnterWorktree, Read, SendUserFile, Skill, ToolSearch | Model text updated to Opus 4.8 |
| Explore / general-purpose | 7 core: Bash, Edit, Read, ScheduleWakeup, Skill, ToolSearch, Write | 8 tools: Bash, Edit, EnterWorktree, Read, SendUserFile, Skill, ToolSearch, Write | Model text updated to Opus 4.8 |
| Code Guide | 4 tools: Bash, Read, WebFetch, WebSearch | same 4 tools | Adds stale-doc warning and `Available plugin skills` placeholder |
| Status Line | 2 tools: Read, Edit | same 2 tools | Adds `workspace.repo` and `pr` fields plus examples |

Newly captured agent prompt files:

- `claude/ClaudeCodeClaudeAgent-2-1-168.md` — background catch-all `claude` subagent.
- `custom_agents/claude_obsidian_wiki_ingest/ClaudeCodeWikiIngestAgent-2-1-168.md` — environment/plugin-specific wiki ingest agent.
- `custom_agents/claude_obsidian_wiki_lint/ClaudeCodeWikiLintAgent-2-1-168.md` — environment/plugin-specific wiki lint agent.
- `custom_agents/codex_rescue/ClaudeCodeCodexRescueAgent-2-1-168.md` — environment/plugin-specific Codex forwarding agent.

Those custom agent files are included because the user asked for request-parameter completeness. They are real trace parameters, but not necessarily Claude Code core defaults.

### Tool Description Deltas

The most important tool-level changes observed:

- `Agent`: available agent types now include local/plugin subagents in the captured description (`claude`, `claude-obsidian:*`, `codex:*`) in addition to built-in types. The Explore description was shortened to “read-only search agent for broad fan-out searches”.
- `Bash`: description is rewritten around persistent working directory, dedicated-tool preference, sandbox retry behavior, `$TMPDIR`, and foreground `sleep` blocking. Sandbox config is placeholdered as `{{user_sandbox_filesystem_config}}`.
- `EnterWorktree`: now a main core tool in this trace.
- `SendUserFile`: new loaded core tool, used to send local files back to the user.
- `Workflow`: new loaded core tool. It introduces deterministic multi-agent orchestration gated behind explicit user opt-in or slash/skill instructions.
- `WebFetch` / `WebSearch`: only captured via Code Guide in this trace, not via root deferred ToolSearch loading.
- `Glob` / `Grep`: only appeared in custom wiki ingest tools; they are not added to the root built-in JSON.

### System Reminders / Mid-Conversation System Messages

v2.1.168 uses `mid-conversation-system-2026-04-07`; several reminders that v2.1.133 documented as `<system-reminder>` text parts now appear as `system` role messages.

Observed changes:

- Main first user message carries the context reminder (`CLAUDE.md`, imported instructions, project instructions, email, date).
- ToolSearch deferred list + MCP server instructions + skills + plan-mode instructions were observed as a `system` role message after the first tool result.
- Main deferred built-in list now has 18 entries:
  `CronCreate`, `CronDelete`, `CronList`, `EnterPlanMode`, `ExitPlanMode`, `ExitWorktree`, `Monitor`, `NotebookEdit`, `PushNotification`, `RemoteTrigger`, `TaskCreate`, `TaskGet`, `TaskList`, `TaskOutput`, `TaskStop`, `TaskUpdate`, `WebFetch`, `WebSearch`.
- Plan workflow changed:
  - Phase 2 can launch **up to 3 Plan agents in parallel**; v2.1.133 said up to 1.
  - Final plan should describe repeated file patterns once and list representative paths, rather than enumerate every file/line.
- Task Tools Nudge still exists, but the v2.1.133 final sentence `Make sure that you NEVER mention this reminder to the user` was not present in the v2.1.168 trace.
- Output style reminder is injected as a repeated `system` message:
  `Explanatory output style is active. Remember to follow the specific guidelines for this style.`
- Exiting plan mode is now a `system` message headed `## Exited Plan Mode`.

### Auxiliary Prompts

| Prompt | v2.1.133 | v2.1.168 |
| --- | --- | --- |
| `compact` | Context summary prompt, trace-verified in separate v2.1.133 compact trace | Changed: now explicitly says to preserve security-relevant instructions/constraints verbatim |
| `slug_name` | Kebab-case JSON name generator | Changed: plain-text 2-4 word lowercase job label generator, max_tokens 32, Opus 4.8 |
| `summarize_conversation` | Captured in v2.1.133 | Not invoked in this v2.1.168 trace; carried forward and marked as not re-captured |
| `summarize_transcript_chunk` | Captured in v2.1.133 | Not invoked in this v2.1.168 trace; carried forward and marked as not re-captured |
| `analyze_session_facets` | Captured in v2.1.133 | Not invoked in this v2.1.168 trace; carried forward and marked as not re-captured |

### Request Body / Header Changes

Observed v2.1.168 request-body patterns:

| Call type | model | max_tokens | tools | thinking | effort | notes |
| --- | --- | ---: | --- | --- | --- | --- |
| Main agent | `claude-opus-4-8` | 64000 | 12 core | adaptive summarized | max | Some requests set `speed: "fast"` |
| Main compact | `claude-opus-4-8` | 20000 | 12 core | adaptive summarized | max | Same main system/tool surface, compact prompt appended in conversation |
| File Search | `claude-haiku-4-5-20251001` | 32000 | 6 core | disabled | none | 45 repeated calls in this trace |
| Code Guide | `claude-haiku-4-5-20251001` | 32000 | 4 | disabled | none | Official-doc oriented |
| Plan | `claude-opus-4-8` | 64000 | 6 core | disabled | max | ToolSearch enabled |
| Explore / general-purpose | `claude-opus-4-8` | 64000 | 8 | disabled | max | Write-capable general-purpose agent |
| Status line setup | `claude-sonnet-4-6` | 32000 | 2 | disabled | max | StatusLine config agent |
| Custom wiki/codex agents | Sonnet 4.6 or Opus 4.8 | 32000/64000 | agent-specific | disabled | max | Environment/plugin-specific |
| Job label | `claude-opus-4-8` | 32 | none | disabled | none | Plain-text label |
| count_tokens | `claude-opus-4-8` | n/a | none | n/a | n/a | Not a prompt capture |

Notable `anthropic-beta` differences vs the v2.1.133 README:

- New / now-observed broadly: `thinking-token-count-2026-05-13`, `mid-conversation-system-2026-04-07`, `fast-mode-2026-02-01`.
- Main regular calls include `extended-cache-ttl-2025-04-11`; subagents generally do not.
- count_tokens calls use `token-counting-2024-11-01`.

## Directory Structure

```text
claudecode/
  README.md
  ClaudeCodeSystem-2-1-168.md
  ClaudeCodeTools-2-1-168.md
  core-tools-2-1-168.json
  tools-2-1-168.json
  system-reminders-2-1-168.md
  auxiliary/
  claude/
  code_guide/
  custom_agents/
    claude_obsidian_wiki_ingest/
    claude_obsidian_wiki_lint/
    codex_rescue/
  explore/
  file_search/
  plan/
  status_line/
```

## Capture Caveats

- This was a real local trace. It reflects the user's enabled skills, MCP servers, plugins, output style, auto mode, plan-mode flow, and background job behavior.
- User-specific values were replaced with placeholders: `{{working_directory}}`, `{{memory_directory}}`, `{{claude_job_tmp_dir}}`, `{{plan_file_path}}`, `{{user_email}}`, `{{user_settings_json}}`, `{{user_skills_list}}`, `{{plugin_skills}}`, `{{user_mcp_servers}}`, `{{codex_companion_script_path}}`, sandbox config placeholders, and environment placeholders.
- Deferred schemas for 16 built-ins were listed but not loaded, so they are not included in `tools-2-1-168.json`.
- `summarize_conversation`, `summarize_transcript_chunk`, and `analyze_session_facets` are carried over from v2.1.133 because this trace did not invoke them.
- A strict grep for the user's real path, email, trace session IDs, and obvious API-token forms was run after generation.
