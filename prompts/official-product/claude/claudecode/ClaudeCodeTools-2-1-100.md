# Claude Code Tools (v2.1.100)

All 29 tools observed loaded directly with Opus 4.6 (1M context). ToolSearch auto-threshold (~10% of context window) is not triggered at this context size, so no core/deferred split is needed. ToolSearch still exists for sessions with many MCP tools or smaller context windows.

---

## Agent

Launch a new agent to handle complex, multi-step tasks. Each agent type has specific capabilities and tools available to it.

Available agent types and the tools they have access to:

- general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: *)
- statu

...(truncated)

**Parameters:**

- `description` (string (required)): A short (3-5 word) description of the task
- `prompt` (string (required)): The task for the agent to perform
- `subagent_type` (string): The type of specialized agent to use for this task
- `model` (string): Optional model override for this agent. Takes precedence over the agent definition's model frontmatter. If omitted, uses the agent definition's model, or inherits from the parent.
- `run_in_background` (boolean): Set to true to run this agent in the background. You will be notified when it completes.
- `isolation` (string): Isolation mode. "worktree" creates a temporary git worktree so the agent works on an isolated copy of the repo.

---

## AskUserQuestion

Use this tool when you need to ask the user questions during execution. This allows you to:

1. Gather user preferences or requirements
2. Clarify ambiguous instructions
3. Get decisions on implementation choices as you work
4. Offer choices to the user about what direction to take.

Usage notes:

- Users will always be able to select "Other" to provide custom text input
- Use multiSelect: true to allow multiple answers to be selected for a question
- If you recommend a specific option, make that

...(truncated)

**Parameters:**

- `questions` (array (required)): Questions to ask the user (1-4 questions)
- `answers` (object): User answers collected by the permission component
- `annotations` (object): Optional per-question annotations from the user (e.g., notes on preview selections). Keyed by question text.
- `metadata` (object): Optional metadata for tracking and analytics purposes. Not displayed to user.

---

## Bash

Executes a given bash command and returns its output.

The working directory persists between commands, but shell state does not. The shell environment is initialized from the user's profile (bash or zsh).

IMPORTANT: Avoid using this tool to run `find`, `grep`, `cat`, `head`, `tail`, `sed`, `awk`, or `echo` commands, unless explicitly instructed or after you have verified that a dedicated tool cannot accomplish your task. Instead, use the appropriate dedicated tool as this will provide a much b

...(truncated)

**Parameters:**

- `command` (string (required)): The command to execute
- `timeout` (number): Optional timeout in milliseconds (max 600000)
- `description` (string): Clear, concise description of what this command does in active voice. Never use words like "complex" or "risk" in the description - just describe what it does.

For simple commands (git, npm, standard...

- `run_in_background` (boolean): Set to true to run this command in the background. Use Read to read the output later.
- `dangerouslyDisableSandbox` (boolean): Set this to true to dangerously override sandbox mode and run commands without sandboxing.
- `rerun` (string): Rerun a prior command exactly by passing the alias from a previous result's [rerun: bN] footer (e.g. 'b3'). Mutually exclusive with 'command'.

---

## CronCreate

Schedule a prompt to be enqueued at a future time. Use for both recurring schedules and one-shot reminders.

Uses standard 5-field cron in the user's local timezone: minute hour day-of-month month day-of-week. "0 9 * * *" means 9am local — no timezone conversion needed.

## One-shot tasks (recurring: false)

For "remind me at X" or "at , do Y" requests — fire once then auto-delete.
Pin minute/hour/day-of-month/month to specific values:
  "remind me at 2:30pm today to check the deploy" → cr

...(truncated)

**Parameters:**

- `cron` (string (required)): Standard 5-field cron expression in local time: "M H DoM Mon DoW" (e.g. "*/5 * * * *" = every 5 minutes, "30 14 28 2 *" = Feb 28 at 2:30pm local once).
- `prompt` (string (required)): The prompt to enqueue at each fire time.
- `recurring` (boolean): true (default) = fire on every cron match until deleted or auto-expired after 7 days. false = fire once at the next match, then auto-delete. Use false for "remind me at X" one-shot requests with pinne...
- `durable` (boolean): true = persist to .claude/scheduled_tasks.json and survive restarts. false (default) = in-memory only, dies when this Claude session ends. Use true only when the user asks the task to survive across s...

---

## CronDelete

Cancel a cron job previously scheduled with CronCreate. Removes it from the in-memory session store.

**Parameters:**

- `id` (string (required)): Job ID returned by CronCreate.

---

## CronList

List all cron jobs scheduled via CronCreate in this session.

---

## Edit

Performs exact string replacements in files.

Usage:

- You must use your `Read` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: line number + tab. Everything after that is the actual file content to match. Never include any part of the line numbe

...(truncated)

**Parameters:**

- `file_path` (string (required)): The absolute path to the file to modify
- `old_string` (string (required)): The text to replace
- `new_string` (string (required)): The text to replace it with (must be different from old_string)
- `replace_all` (boolean): Replace all occurrences of old_string (default false)

---

## EnterPlanMode

Use this tool proactively when you're about to start a non-trivial implementation task. Getting user sign-off on your approach before writing code prevents wasted effort and ensures alignment. This tool transitions you into plan mode where you can explore the codebase and design an implementation approach for user approval.

## When to Use This Tool

**Prefer using EnterPlanMode** for implementation tasks unless they're simple. Use it when ANY of these conditions apply:

1. **New Feature Impleme

...(truncated)

---

## EnterWorktree

Use this tool ONLY when the user explicitly asks to work in a worktree. This tool creates an isolated git worktree and switches the current session into it.

## When to Use

- The user explicitly says "worktree" (e.g., "start a worktree", "work in a worktree", "create a worktree", "use a worktree")

## When NOT to Use

- The user asks to create a branch, switch branches, or work on a different branch — use git commands instead
- The user asks to fix a bug or work on a feature — use normal git wo

...(truncated)

**Parameters:**

- `name` (string): Optional name for the worktree. Each "/"-separated segment may contain only letters, digits, dots, underscores, and dashes; max 64 chars total. A random name is generated if not provided.

---

## ExitPlanMode

Use this tool when you are in plan mode and have finished writing your plan to the plan file and are ready for user approval.

## How This Tool Works

- You should have already written your plan to the plan file specified in the plan mode system message
- This tool does NOT take the plan content as a parameter - it will read the plan from the file you wrote
- This tool simply signals that you're done planning and ready for the user to review and approve
- The user will see the contents of your pl

...(truncated)

**Parameters:**

- `allowedPrompts` (array): Prompt-based permissions needed to implement the plan. These describe categories of actions rather than specific commands.

---

## ExitWorktree

Exit a worktree session created by EnterWorktree and return the session to the original working directory.

## Scope

This tool ONLY operates on worktrees created by EnterWorktree in this session. It will NOT touch:

- Worktrees you created manually with `git worktree add`
- Worktrees from a previous session (even if created by EnterWorktree then)
- The directory you're in if EnterWorktree was never called

If called outside an EnterWorktree session, the tool is a **no-op**: it reports that no wo

...(truncated)

**Parameters:**

- `action` (string (required)): "keep" leaves the worktree and branch on disk; "remove" deletes both.
- `discard_changes` (boolean): Required true when action is "remove" and the worktree has uncommitted files or unmerged commits. The tool will refuse and list them otherwise.

---

## Glob

- Fast file pattern matching tool that works with any codebase size
- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead

**Parameters:**

- `pattern` (string (required)): The glob pattern to match files against
- `path` (string): The directory to search in. If not specified, the current working directory will be used. IMPORTANT: Omit this field to use the default directory. DO NOT enter "undefined" or "null" - simply omit it f...

---

## Grep

A powerful search tool built on ripgrep

  Usage:

- ALWAYS use Grep for search tasks. NEVER invoke `grep` or `rg` as a Bash command. The Grep tool has been optimized for correct permissions and access.
- Supports full regex syntax (e.g., "log.*Error", "function\s+\w+")
- Filter files with glob parameter (e.g., "*.js", "**/*.tsx") or type parameter (e.g., "js", "py", "rust")
- Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows

...(truncated)

**Parameters:**

- `pattern` (string (required)): The regular expression pattern to search for in file contents
- `path` (string): File or directory to search in (rg PATH). Defaults to current working directory.
- `glob` (string): Glob pattern to filter files (e.g. "*.js", "*.{ts,tsx}") - maps to rg --glob
- `output_mode` (string): Output mode: "content" shows matching lines (supports -A/-B/-C context, -n line numbers, head_limit), "files_with_matches" shows file paths (supports head_limit), "count" shows match counts (supports ...
- `-B` (number): Number of lines to show before each match (rg -B). Requires output_mode: "content", ignored otherwise.
- `-A` (number): Number of lines to show after each match (rg -A). Requires output_mode: "content", ignored otherwise.
- `-C` (number): Alias for context.
- `context` (number): Number of lines to show before and after each match (rg -C). Requires output_mode: "content", ignored otherwise.
- `-n` (boolean): Show line numbers in output (rg -n). Requires output_mode: "content", ignored otherwise. Defaults to true.
- `-i` (boolean): Case insensitive search (rg -i)
- `type` (string): File type to search (rg --type). Common types: js, py, rust, go, java, etc. More efficient than include for standard file types.
- `head_limit` (number): Limit output to first N lines/entries, equivalent to "| head -N". Works across all output modes: content (limits output lines), files_with_matches (limits file paths), count (limits count entries). De...
- `offset` (number): Skip first N lines/entries before applying head_limit, equivalent to "| tail -n +N | head -N". Works across all output modes. Defaults to 0.
- `multiline` (boolean): Enable multiline mode where . matches newlines and patterns can span lines (rg -U --multiline-dotall). Default: false.

---

## ListMcpResourcesTool

List available resources from configured MCP servers.
Each returned resource will include all standard MCP resource fields plus a 'server' field 
indicating which server the resource belongs to.

Parameters:

- server (optional): The name of a specific MCP server to get resources from. If not provided,
resources from all servers will be returned.

**Parameters:**

- `server` (string): Optional server name to filter resources by

---

## Monitor

Start a background monitor that streams events from a long-running script. Each stdout line is an event — you keep working and notifications arrive in the chat. Events arrive on their own schedule and are not replies from the user, even if one lands while you're waiting for the user to answer a question.

Monitor is for the **streaming** case: "tell me every time X happens." For one-shot "wait until X is done," use Bash with run_in_background instead — you'll get a completion notification when i

...(truncated)

**Parameters:**

- `description` (string (required)): Short human-readable description of what you are monitoring (shown in notifications).
- `timeout_ms` (number (required)): Kill the monitor after this deadline. Default 300000ms, max 3600000ms. Ignored when persistent is true.
- `persistent` (boolean (required)): Run for the lifetime of the session (no timeout). Use for session-length watches like PR monitoring or log tails. Stop with TaskStop.
- `command` (string (required)): Shell command or script. Each stdout line is an event; exit ends the watch.

---

## NotebookEdit

Completely replaces the contents of a specific cell in a Jupyter notebook (.ipynb file) with new source. Jupyter notebooks are interactive documents that combine code, text, and visualizations, commonly used for data analysis and scientific computing. The notebook_path parameter must be an absolute path, not a relative path. The cell_number is 0-indexed. Use edit_mode=insert to add a new cell at the index specified by cell_number. Use edit_mode=delete to delete the cell at the index specified by cell_number.

**Parameters:**

- `notebook_path` (string (required)): The absolute path to the Jupyter notebook file to edit (must be absolute, not relative)
- `cell_id` (string): The ID of the cell to edit. When inserting a new cell, the new cell will be inserted after the cell with this ID, or at the beginning if not specified.
- `new_source` (string (required)): The new source for the cell
- `cell_type` (string): The type of the cell (code or markdown). If not specified, it defaults to the current cell type. If using edit_mode=insert, this is required.
- `edit_mode` (string): The type of edit to make (replace, insert, delete). Defaults to replace.

---

## Read

Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:

- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning of the file
- When you already know which part of the file yo

...(truncated)

**Parameters:**

- `file_path` (string (required)): The absolute path to the file to read
- `offset` (integer): The line number to start reading from. Only provide if the file is too large to read at once
- `limit` (integer): The number of lines to read. Only provide if the file is too large to read at once.
- `pages` (string): Page range for PDF files (e.g., "1-5", "3", "10-20"). Only applicable to PDF files. Maximum 20 pages per request.

---

## ReadMcpResourceTool

Reads a specific resource from an MCP server, identified by server name and resource URI.

Parameters:

- server (required): The name of the MCP server from which to read the resource
- uri (required): The URI of the resource to read

**Parameters:**

- `server` (string (required)): The MCP server name
- `uri` (string (required)): The resource URI to read

---

## RemoteTrigger

Call the claude.ai remote-trigger API. Use this instead of curl — the OAuth token is added automatically in-process and never exposed.

Actions:

- list: GET /v1/code/triggers
- get: GET /v1/code/triggers/{trigger_id}
- create: POST /v1/code/triggers (requires body)
- update: POST /v1/code/triggers/{trigger_id} (requires body, partial update)
- run: POST /v1/code/triggers/{trigger_id}/run

The response is the raw JSON from the API.

**Parameters:**

- `action` (string (required)): 
- `trigger_id` (string): Required for get, update, and run
- `body` (object): JSON body for create and update

---

## Skill

Execute a skill within the main conversation

When users ask you to perform tasks, check if any of the available skills match. Skills provide specialized capabilities and domain knowledge.

When users reference a "slash command" or "/" (e.g., "/commit", "/review-pr"), they are referring to a skill. Use this tool to invoke it.

How to invoke:

- Use this tool with the skill name and optional arguments
- Examples:
  - `skill: "pdf"` - invoke the pdf skill
  - `skill: "commit", args: "-m

...(truncated)

**Parameters:**

- `skill` (string (required)): The skill name. E.g., "commit", "review-pr", or "pdf"
- `args` (string): Optional arguments for the skill

---

## TaskCreate

Use this tool to create a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.
It also helps the user understand the progress of the task and overall progress of their requests.

## When to Use This Tool

Use this tool proactively in these scenarios:

- Complex multi-step tasks - When a task requires 3 or more distinct steps or actions
- Non-trivial and complex tasks - Tasks that require careful pla

...(truncated)

**Parameters:**

- `subject` (string (required)): A brief title for the task
- `description` (string (required)): What needs to be done
- `activeForm` (string): Present continuous form shown in spinner when in_progress (e.g., "Running tests")
- `metadata` (object): Arbitrary metadata to attach to the task

---

## TaskGet

Use this tool to retrieve a task by its ID from the task list.

## When to Use This Tool

- When you need the full description and context before starting work on a task
- To understand task dependencies (what it blocks, what blocks it)
- After being assigned a task, to get complete requirements

## Output

Returns full task details:

- **subject**: Task title
- **description**: Detailed requirements and context
- **status**: 'pending', 'in_progress', or 'completed'
- **blocks**: Tasks waiting on

...(truncated)

**Parameters:**

- `taskId` (string (required)): The ID of the task to retrieve

---

## TaskList

Use this tool to list all tasks in the task list.

## When to Use This Tool

- To see what tasks are available to work on (status: 'pending', no owner, not blocked)
- To check overall progress on the project
- To find tasks that are blocked and need dependencies resolved
- After completing a task, to check for newly unblocked work or claim the next available task
- **Prefer working on tasks in ID order** (lowest ID first) when multiple tasks are available, as earlier tasks often set up context f

...(truncated)

---

## TaskOutput

DEPRECATED: Prefer using the Read tool on the task's output file path instead. Background tasks return their output file path in the tool result, and you receive a  with the same path when the task completes — Read that file directly.

- Retrieves output from a running or completed task (background shell, agent, or remote session)
- Takes a task_id parameter identifying the task
- Returns the task output along with status information
- Use block=true (default) to wait for task

...(truncated)

**Parameters:**

- `task_id` (string (required)): The task ID to get output from
- `block` (boolean (required)): Whether to wait for completion
- `timeout` (number (required)): Max wait time in ms

---

## TaskStop

- Stops a running background task by its ID
- Takes a task_id parameter identifying the task to stop
- Returns a success or failure status
- Use this tool when you need to terminate a long-running task

**Parameters:**

- `task_id` (string): The ID of the background task to stop
- `shell_id` (string): Deprecated: use task_id instead

---

## TaskUpdate

Use this tool to update a task in the task list.

## When to Use This Tool

**Mark tasks as resolved:**

- When you have completed the work described in a task
- When a task is no longer needed or has been superseded
- IMPORTANT: Always mark your assigned tasks as resolved when you finish them
- After resolving, call TaskList to find your next task
- ONLY mark a task as completed when you have FULLY accomplished it
- If you encounter errors, blockers, or cannot finish, keep the task as in_progre

...(truncated)

**Parameters:**

- `taskId` (string (required)): The ID of the task to update
- `subject` (string): New subject for the task
- `description` (string): New description for the task
- `activeForm` (string): Present continuous form shown in spinner when in_progress (e.g., "Running tests")
- `status` (any): New status for the task
- `addBlocks` (array): Task IDs that this task blocks
- `addBlockedBy` (array): Task IDs that block this task
- `owner` (string): New owner for the task
- `metadata` (object): Metadata keys to merge into the task. Set a key to null to delete it.

---

## WebFetch

IMPORTANT: WebFetch WILL FAIL for authenticated or private URLs. Before using this tool, check if the URL points to an authenticated service (e.g. Google Docs, Confluence, Jira, GitHub). If so, look for a specialized MCP tool that provides authenticated access.

- Fetches content from a specified URL and processes it using an AI model
- Takes a URL and a prompt as input
- Fetches the URL content, converts HTML to markdown
- Processes the content with the prompt using a small, fast model
- Return

...(truncated)

**Parameters:**

- `url` (string (required)): The URL to fetch content from
- `prompt` (string (required)): The prompt to run on the fetched content

---

## WebSearch

- Allows Claude to search the web and use the results to inform responses
- Provides up-to-date information for current events and recent data
- Returns search result information formatted as search result blocks, including links as markdown hyperlinks
- Use this tool for accessing information beyond Claude's knowledge cutoff
- Searches are performed automatically within a single API call

CRITICAL REQUIREMENT - You MUST follow this:

- After answering the user's question, you MUST include a "

...(truncated)

**Parameters:**

- `query` (string (required)): The search query to use
- `allowed_domains` (array): Only include search results from these domains
- `blocked_domains` (array): Never include search results from these domains

---

## Write

Writes a file to the local filesystem.

Usage:

- This tool will overwrite the existing file if there is one at the provided path.
- If this is an existing file, you MUST use the Read tool first to read the file's contents. This tool will fail if you did not read the file first.
- Prefer the Edit tool for modifying existing files — it only sends the diff. Only use this tool to create new files or for complete rewrites.
- NEVER create documentation files (*.md) or README files unless explicitly re

...(truncated)

**Parameters:**

- `file_path` (string (required)): The absolute path to the file to write (must be absolute, not relative)
- `content` (string (required)): The content to write to the file

---