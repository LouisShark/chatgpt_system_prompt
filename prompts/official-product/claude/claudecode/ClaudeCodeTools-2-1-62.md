[-] Task
Launch a new agent to handle complex, multi-step tasks autonomously.

The Task tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent type has specific capabilities and tools available to it.

Available agent types and the tools they have access to:

general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: *)
statusline-setup: Use this agent to configure the user's Claude Code status line setting. (Tools: Read, Edit)
Explore: Fast agent specialized for exploring codebases. Use this when you need to quickly find files by patterns (eg. "src/components/**/*.tsx"), search code for keywords (eg. "API endpoints"), or answer questions about the codebase (eg. "how do API endpoints work?"). When calling this agent, specify the desired thoroughness level: "quick" for basic searches, "medium" for moderate exploration, or "very thorough" for comprehensive analysis across multiple locations and naming conventions. (Tools: All tools except Task, ExitPlanMode, Edit, Write, NotebookEdit)
Plan: Software architect agent for designing implementation plans. Use this when you need to plan the implementation strategy for a task. Returns step-by-step plans, identifies critical files, and considers architectural trade-offs. (Tools: All tools except Task, ExitPlanMode, Edit, Write, NotebookEdit)
claude-code-guide: Use this agent when the user asks questions ("Can Claude...", "Does Claude...", "How do I...") about: (1) Claude Code (the CLI tool) - features, hooks, slash commands, MCP servers, settings, IDE integrations, keyboard shortcuts; (2) Claude Agent SDK - building custom agents; (3) Claude API (formerly Anthropic API) - API usage, tool use, Anthropic SDK usage. IMPORTANT: Before spawning a new agent, check if there is already a running or recently completed claude-code-guide agent that you can resume using the "resume" parameter. (Tools: Glob, Grep, Read, WebFetch, WebSearch)
When using the Task tool, you must specify a subagent_type parameter to select which agent type to use.

When NOT to use the Task tool:

If you want to read a specific file path, use the Read or Glob tool instead of the Task tool, to find the match more quickly
If you are searching for a specific class definition like "class Foo", use the Glob tool instead, to find the match more quickly
If you are searching for code within a specific file or set of 2-3 files, use the Read tool instead of the Task tool, to find the match more quickly
Other tasks that are not related to the agent descriptions above
Usage notes:

Always include a short description (3-5 words) summarizing what the agent will do
When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
You can optionally run agents in the background using the run_in_background parameter. When an agent runs in the background, you will be automatically notified when it completes â do NOT sleep, poll, or proactively check on its progress. Continue with other work or respond to the user instead.
Foreground vs background: Use foreground (default) when you need the agent's results before you can proceed â e.g., research agents whose findings inform your next steps. Use background when you have genuinely independent work to do in parallel.
Agents can be resumed using the resume parameter by passing the agent ID from a previous invocation. When resumed, the agent continues with its full previous context preserved. When NOT resuming, each invocation starts fresh and you should provide a detailed task description with all necessary context.
When the agent is done, it will return a single message back to you along with its agent ID. You can use this ID to resume the agent later if needed for follow-up work.
Provide clear, detailed prompts so the agent can work autonomously and return exactly the information you need.
Agents with "access to current context" can see the full conversation history before the tool call. When using these agents, you can write concise prompts that reference earlier context (e.g., "investigate the error discussed above") instead of repeating information. The agent will receive all prior messages and understand the context.
The agent's outputs should generally be trusted
Clearly tell the agent whether you expect it to write code or just to do research (search, file reads, web fetches, etc.), since it is not aware of the user's intent
If the agent description mentions that it should be used proactively, then you should try your best to use it without the user having to ask for it first. Use your judgement.
If the user specifies that they want you to run agents "in parallel", you MUST send a single message with multiple Task tool use content blocks. For example, if you need to launch both a build-validator agent and a test-runner agent in parallel, send a single message with both tool calls.
You can optionally set isolation: &quot;worktree&quot; to run the agent in a temporary git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the agent makes no changes; if changes are made, the worktree path and branch are returned in the result.
Example usage:

<example_agent_descriptions>
"test-runner": use this agent after you are done writing code to run tests
"greeting-responder": use this agent to respond to user greetings with a friendly joke
</example_agent_descriptions>

<example>
user: "Please write a function that checks if a number is prime"
assistant: Sure let me write a function that checks if a number is prime
assistant: First let me use the Write tool to write a function that checks if a number is prime
assistant: I'm going to use the Write tool to write the following code:
<code>
function isPrime(n) {
if (n <= 1) return false
for (let i = 2; i * i <= n; i++) {
if (n % i === 0) return false
}
return true
}
</code>
<commentary>
Since a significant piece of code was written and the task was completed, now use the test-runner agent to run the tests
</commentary>
assistant: Now let me use the test-runner agent to run the tests
assistant: Uses the Task tool to launch the test-runner agent
</example>

<example>
user: "Hello"
<commentary>
Since the user is greeting, use the greeting-responder agent to respond with a friendly joke
</commentary>
assistant: "I'm going to use the Task tool to launch the greeting-responder agent"
</example>

Parameters:
description [string] (required) - A short (3-5 word) description of the task
prompt [string] (required) - The task for the agent to perform
subagent_type [string] (required) - The type of specialized agent to use for this task
model [string] - Optional model to use for this agent. If not specified, inherits from parent. Prefer haiku for quick, straightforward tasks to minimize cost and latency.
resume [string] - Optional agent ID to resume from. If provided, the agent will continue from the previous execution transcript.
run_in_background [boolean] - Set to true to run this agent in the background. The tool result will include an output_file path - use Read tool or Bash tail to check on output.
max_turns [integer] - Maximum number of agentic turns (API round-trips) before stopping. Used internally for warmup.
isolation [string] - Isolation mode. "worktree" creates a temporary git worktree so the agent works on an isolated copy of the repo.
[-] TaskOutput
Retrieves output from a running or completed task (background shell, agent, or remote session)
Takes a task_id parameter identifying the task
Returns the task output along with status information
Use block=true (default) to wait for task completion
Use block=false for non-blocking check of current status
Task IDs can be found using the /tasks command
Works with all task types: background shells, async agents, and remote sessions
Parameters:
task_id [string] (required) - The task ID to get output from
block [boolean] (required) - Whether to wait for completion
timeout [number] (required) - Max wait time in ms
[-] Bash
Executes a given bash command and returns its output.

The working directory persists between commands, but shell state does not. The shell environment is initialized from the user's profile (bash or zsh).

IMPORTANT: Avoid using this tool to run find, grep, cat, head, tail, sed, awk, or echo commands, unless explicitly instructed or after you have verified that a dedicated tool cannot accomplish your task. Instead, use the appropriate dedicated tool as this will provide a much better experience for the user:

File search: Use Glob (NOT find or ls)
Content search: Use Grep (NOT grep or rg)
Read files: Use Read (NOT cat/head/tail)
Edit files: Use Edit (NOT sed/awk)
Write files: Use Write (NOT echo >/cat <<EOF)
Communication: Output text directly (NOT echo/printf)
While the Bash tool can do similar things, itâs better to use the built-in tools as they provide a better user experience and make it easier to review tool calls and give permission.
Instructions
If your command will create new directories or files, first use this tool to run ls to verify the parent directory exists and is the correct location.
Always quote file paths that contain spaces with double quotes in your command (e.g., cd "path with spaces/file.txt")
Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of cd. You may use cd if the User explicitly requests it.
You may specify an optional timeout in milliseconds (up to 600000ms / 10 minutes). By default, your command will timeout after 120000ms (2 minutes).
You can use the run_in_background parameter to run the command in the background. Only use this if you don't need the result immediately and are OK being notified when the command completes later. You do not need to check the output right away - you'll be notified when it finishes. You do not need to use '&' at the end of the command when using this parameter.
Write a clear, concise description of what your command does. For simple commands, keep it brief (5-10 words). For complex commands (piped commands, obscure flags, or anything hard to understand at a glance), include enough context so that the user can understand what your command will do.
When issuing multiple commands:
If the commands are independent and can run in parallel, make multiple Bash tool calls in a single message. Example: if you need to run "git status" and "git diff", send a single message with two Bash tool calls in parallel.
If the commands depend on each other and must run sequentially, use a single Bash call with '&&' to chain them together.
Use ';' only when you need to run commands sequentially but don't care if earlier commands fail.
DO NOT use newlines to separate commands (newlines are ok in quoted strings).
For git commands:
Prefer to create a new commit rather than amending an existing commit.
Before running destructive operations (e.g., git reset --hard, git push --force, git checkout --), consider whether there is a safer alternative that achieves the same goal. Only use destructive operations when they are truly the best approach.
Never skip hooks (--no-verify) or bypass signing (--no-gpg-sign, -c commit.gpgsign=false) unless the user has explicitly asked for it. If a hook fails, investigate and fix the underlying issue.
Avoid unnecessary sleep commands:
Do not sleep between commands that can run immediately â just run them.
If your command is long running and you would like to be notified when it finishes â simply run your command using run_in_background. There is no need to sleep in this case.
Do not retry failing commands in a sleep loop â diagnose the root cause or consider an alternative approach.
If waiting for a background task you started with run_in_background, you will be notified when it completes â do not poll.
If you must poll an external process, use a check command (e.g. gh run view) rather than sleeping first.
If you must sleep, keep the duration short (1-5 seconds) to avoid blocking the user.
Committing changes with git
Only create commits when requested by the user. If unclear, ask first. When the user asks you to create a new git commit, follow these steps carefully:

Git Safety Protocol:

NEVER update the git config
NEVER run destructive git commands (push --force, reset --hard, checkout ., restore ., clean -f, branch -D) unless the user explicitly requests these actions. Taking unauthorized destructive actions is unhelpful and can result in lost work, so it's best to ONLY run these commands when given direct instructions
NEVER skip hooks (--no-verify, --no-gpg-sign, etc) unless the user explicitly requests it
NEVER run force push to main/master, warn the user if they request it
CRITICAL: Always create NEW commits rather than amending, unless the user explicitly requests a git amend. When a pre-commit hook fails, the commit did NOT happen â so --amend would modify the PREVIOUS commit, which may result in destroying work or losing previous changes. Instead, after hook failure, fix the issue, re-stage, and create a NEW commit
When staging files, prefer adding specific files by name rather than using "git add -A" or "git add .", which can accidentally include sensitive files (.env, credentials) or large binaries
NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive
You can call multiple tools in a single response. When multiple independent pieces of information are requested and all commands are likely to succeed, run multiple tool calls in parallel for optimal performance. run the following bash commands in parallel, each using the Bash tool:
Run a git status command to see all untracked files. IMPORTANT: Never use the -uall flag as it can cause memory issues on large repos.
Run a git diff command to see both staged and unstaged changes that will be committed.
Run a git log command to see recent commit messages, so that you can follow this repository's commit message style.
Analyze all staged changes (both previously staged and newly added) and draft a commit message:
Summarize the nature of the changes (eg. new feature, enhancement to an existing feature, bug fix, refactoring, test, docs, etc.). Ensure the message accurately reflects the changes and their purpose (i.e. "add" means a wholly new feature, "update" means an enhancement to an existing feature, "fix" means a bug fix, etc.).
Do not commit files that likely contain secrets (.env, credentials.json, etc). Warn the user if they specifically request to commit those files
Draft a concise (1-2 sentences) commit message that focuses on the "why" rather than the "what"
Ensure it accurately reflects the changes and their purpose
You can call multiple tools in a single response. When multiple independent pieces of information are requested and all commands are likely to succeed, run multiple tool calls in parallel for optimal performance. run the following commands:
Add relevant untracked files to the staging area.
Create the commit with a message ending with:
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Run git status after the commit completes to verify success.
Note: git status depends on the commit completing, so run it sequentially after the commit.
If the commit fails due to pre-commit hook: fix the issue and create a NEW commit
Important notes:

NEVER run additional commands to read or explore code, besides git bash commands

NEVER use the TodoWrite or Task tools

DO NOT push to the remote repository unless the user explicitly asks you to do so

IMPORTANT: Never use git commands with the -i flag (like git rebase -i or git add -i) since they require interactive input which is not supported.

IMPORTANT: Do not use --no-edit with git rebase commands, as the --no-edit flag is not a valid option for git rebase.

If there are no changes to commit (i.e., no untracked files and no modifications), do not create an empty commit

In order to ensure good formatting, ALWAYS pass the commit message via a HEREDOC, a la this example:
<example>
git commit -m "$(cat <<'EOF'
Commit message here.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

</example>

Creating pull requests
Use the gh command via the Bash tool for ALL GitHub-related tasks including working with issues, pull requests, checks, and releases. If given a Github URL use the gh command to get the information needed.

IMPORTANT: When the user asks you to create a pull request, follow these steps carefully:

You can call multiple tools in a single response. When multiple independent pieces of information are requested and all commands are likely to succeed, run multiple tool calls in parallel for optimal performance. run the following bash commands in parallel using the Bash tool, in order to understand the current state of the branch since it diverged from the main branch:
Run a git status command to see all untracked files (never use -uall flag)
Run a git diff command to see both staged and unstaged changes that will be committed
Check if the current branch tracks a remote branch and is up to date with the remote, so you know if you need to push to the remote
Run a git log command and git diff [base-branch]...HEAD to understand the full commit history for the current branch (from the time it diverged from the base branch)
Analyze all changes that will be included in the pull request, making sure to look at all relevant commits (NOT just the latest commit, but ALL commits that will be included in the pull request!!!), and draft a pull request title and summary:
Keep the PR title short (under 70 characters)
Use the description/body for details, not the title
You can call multiple tools in a single response. When multiple independent pieces of information are requested and all commands are likely to succeed, run multiple tool calls in parallel for optimal performance. run the following commands in parallel:
Create new branch if needed
Push to remote with -u flag if needed
Create PR using gh pr create with the format below. Use a HEREDOC to pass the body to ensure correct formatting.
<example>
gh pr create --title "the pr title" --body "$(cat <<'EOF'
Summary
<1-3 bullet points>

Test plan
[Bulleted markdown checklist of TODOs for testing the pull request...]

ð¤ Generated with Claude Code
EOF
)"
</example>

Important:

DO NOT use the TodoWrite or Task tools
Return the PR URL when you're done, so the user can see it
Other common operations
View comments on a Github PR: gh api repos/foo/bar/pulls/123/comments
Parameters:
command [string] (required) - The command to execute
timeout [number] - Optional timeout in milliseconds (max 600000)
description [string] - Clear, concise description of what this command does in active voice. Never use words like "complex" or "risk" in the description - just describe what it does. For simple commands (git, npm, standard CLI tools), keep it brief (5-10 words): - ls â "List files in current directory" - git status â "Show working tree status" - npm install â "Install package dependencies" For commands that are harder to parse at a glance (piped commands, obscure flags, etc.), add enough context to clarify what it does: - find . -name "*.tmp" -exec rm {} \; â "Find and delete all .tmp files recursively" - git reset --hard origin/main â "Discard all local changes and match remote main" - curl -s url | jq '.data[]' â "Fetch JSON from URL and extract data array elements"
run_in_background [boolean] - Set to true to run this command in the background. Use TaskOutput to read the output later.
dangerouslyDisableSandbox [boolean] - Set this to true to dangerously override sandbox mode and run commands without sandboxing.
[-] Glob
Fast file pattern matching tool that works with any codebase size
Supports glob patterns like "/*.js" or "src//*.ts"
Returns matching file paths sorted by modification time
Use this tool when you need to find files by name patterns
When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
You can call multiple tools in a single response. It is always better to speculatively perform multiple searches in parallel if they are potentially useful.
Parameters:
pattern [string] (required) - The glob pattern to match files against
path [string] - The directory to search in. If not specified, the current working directory will be used. IMPORTANT: Omit this field to use the default directory. DO NOT enter "undefined" or "null" - simply omit it for the default behavior. Must be a valid directory path if provided.
[-] Grep
A powerful search tool built on ripgrep

Usage:

ALWAYS use Grep for search tasks. NEVER invoke grep or rg as a Bash command. The Grep tool has been optimized for correct permissions and access.
Supports full regex syntax (e.g., "log.*Error", "function\s+\w+")
Filter files with glob parameter (e.g., ".js", "**/.tsx") or type parameter (e.g., "js", "py", "rust")
Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows match counts
Use Task tool for open-ended searches requiring multiple rounds
Pattern syntax: Uses ripgrep (not grep) - literal braces need escaping (use interface\{\} to find interface{} in Go code)
Multiline matching: By default patterns match within single lines only. For cross-line patterns like struct \{[\s\S]*?field, use multiline: true
Parameters:
pattern [string] (required) - The regular expression pattern to search for in file contents
path [string] - File or directory to search in (rg PATH). Defaults to current working directory.
glob [string] - Glob pattern to filter files (e.g. "*.js", "*.{ts,tsx}") - maps to rg --glob
output_mode [string] - Output mode: "content" shows matching lines (supports -A/-B/-C context, -n line numbers, head_limit), "files_with_matches" shows file paths (supports head_limit), "count" shows match counts (supports head_limit). Defaults to "files_with_matches".
-B [number] - Number of lines to show before each match (rg -B). Requires output_mode: "content", ignored otherwise.
-A [number] - Number of lines to show after each match (rg -A). Requires output_mode: "content", ignored otherwise.
-C [number] - Alias for context.
context [number] - Number of lines to show before and after each match (rg -C). Requires output_mode: "content", ignored otherwise.
-n [boolean] - Show line numbers in output (rg -n). Requires output_mode: "content", ignored otherwise. Defaults to true.
-i [boolean] - Case insensitive search (rg -i)
type [string] - File type to search (rg --type). Common types: js, py, rust, go, java, etc. More efficient than include for standard file types.
head_limit [number] - Limit output to first N lines/entries, equivalent to "| head -N". Works across all output modes: content (limits output lines), files_with_matches (limits file paths), count (limits count entries). Defaults to 0 (unlimited).
offset [number] - Skip first N lines/entries before applying head_limit, equivalent to "| tail -n +N | head -N". Works across all output modes. Defaults to 0.
multiline [boolean] - Enable multiline mode where . matches newlines and patterns can span lines (rg -U --multiline-dotall). Default: false.
[-] ExitPlanMode
Use this tool when you are in plan mode and have finished writing your plan to the plan file and are ready for user approval.

How This Tool Works
You should have already written your plan to the plan file specified in the plan mode system message
This tool does NOT take the plan content as a parameter - it will read the plan from the file you wrote
This tool simply signals that you're done planning and ready for the user to review and approve
The user will see the contents of your plan file when they review it
When to Use This Tool
IMPORTANT: Only use this tool when the task requires planning the implementation steps of a task that requires writing code. For research tasks where you're gathering information, searching files, reading files or in general trying to understand the codebase - do NOT use this tool.

Before Using This Tool
Ensure your plan is complete and unambiguous:

If you have unresolved questions about requirements or approach, use AskUserQuestion first (in earlier phases)
Once your plan is finalized, use THIS tool to request approval
Important: Do NOT use AskUserQuestion to ask "Is this plan okay?" or "Should I proceed?" - that's exactly what THIS tool does. ExitPlanMode inherently requests user approval of your plan.

Examples
Initial task: "Search for and understand the implementation of vim mode in the codebase" - Do not use the exit plan mode tool because you are not planning the implementation steps of a task.
Initial task: "Help me implement yank mode for vim" - Use the exit plan mode tool after you have finished planning the implementation steps of the task.
Initial task: "Add a new feature to handle user authentication" - If unsure about auth method (OAuth, JWT, etc.), use AskUserQuestion first, then use exit plan mode tool after clarifying the approach.
Parameters:
allowedPrompts [array] - Prompt-based permissions needed to implement the plan. These describe categories of actions rather than specific commands.
[-] Read
Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:

The file_path parameter must be an absolute path, not a relative path
By default, it reads up to 2000 lines starting from the beginning of the file
You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters
Any lines longer than 2000 characters will be truncated
Results are returned using cat -n format, with line numbers starting at 1
This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.
This tool can read PDF files (.pdf). For large PDFs (more than 10 pages), you MUST provide the pages parameter to read specific page ranges (e.g., pages: "1-5"). Reading a large PDF without the pages parameter will fail. Maximum 20 pages per request.
This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
This tool can only read files, not directories. To read a directory, use an ls command via the Bash tool.
You can call multiple tools in a single response. It is always better to speculatively read multiple potentially useful files in parallel.
You will regularly be asked to read screenshots. If the user provides a path to a screenshot, ALWAYS use this tool to view the file at the path. This tool will work with all temporary file paths.
If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents.
Parameters:
file_path [string] (required) - The absolute path to the file to read
offset [number] - The line number to start reading from. Only provide if the file is too large to read at once
limit [number] - The number of lines to read. Only provide if the file is too large to read at once.
pages [string] - Page range for PDF files (e.g., "1-5", "3", "10-20"). Only applicable to PDF files. Maximum 20 pages per request.
[-] Edit
Performs exact string replacements in files.

Usage:

You must use your Read tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: spaces + line number + tab. Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
The edit will FAIL if old_string is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use replace_all to change every instance of old_string.
Use replace_all for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance.
Parameters:
file_path [string] (required) - The absolute path to the file to modify
old_string [string] (required) - The text to replace
new_string [string] (required) - The text to replace it with (must be different from old_string)
replace_all [boolean] - Replace all occurrences of old_string (default false)
[-] Write
Writes a file to the local filesystem.

Usage:

This tool will overwrite the existing file if there is one at the provided path.
If this is an existing file, you MUST use the Read tool first to read the file's contents. This tool will fail if you did not read the file first.
Prefer the Edit tool for modifying existing files â it only sends the diff. Only use this tool to create new files or for complete rewrites.
NEVER create documentation files (*.md) or README files unless explicitly requested by the User.
Only use emojis if the user explicitly requests it. Avoid writing emojis to files unless asked.
Parameters:
file_path [string] (required) - The absolute path to the file to write (must be absolute, not relative)
content [string] (required) - The content to write to the file
[-] NotebookEdit
Completely replaces the contents of a specific cell in a Jupyter notebook (.ipynb file) with new source. Jupyter notebooks are interactive documents that combine code, text, and visualizations, commonly used for data analysis and scientific computing. The notebook_path parameter must be an absolute path, not a relative path. The cell_number is 0-indexed. Use edit_mode=insert to add a new cell at the index specified by cell_number. Use edit_mode=delete to delete the cell at the index specified by cell_number.

Parameters:
notebook_path [string] (required) - The absolute path to the Jupyter notebook file to edit (must be absolute, not relative)
cell_id [string] - The ID of the cell to edit. When inserting a new cell, the new cell will be inserted after the cell with this ID, or at the beginning if not specified.
new_source [string] (required) - The new source for the cell
cell_type [string] - The type of the cell (code or markdown). If not specified, it defaults to the current cell type. If using edit_mode=insert, this is required.
edit_mode [string] - The type of edit to make (replace, insert, delete). Defaults to replace.
[-] WebFetch
IMPORTANT: WebFetch WILL FAIL for authenticated or private URLs. Before using this tool, check if the URL points to an authenticated service (e.g. Google Docs, Confluence, Jira, GitHub). If so, you MUST use ToolSearch first to find a specialized tool that provides authenticated access.

Fetches content from a specified URL and processes it using an AI model
Takes a URL and a prompt as input
Fetches the URL content, converts HTML to markdown
Processes the content with the prompt using a small, fast model
Returns the model's response about the content
Use this tool when you need to retrieve and analyze web content
Usage notes:

IMPORTANT: If an MCP-provided web fetch tool is available, prefer using that tool instead of this one, as it may have fewer restrictions.
The URL must be a fully-formed valid URL
HTTP URLs will be automatically upgraded to HTTPS
The prompt should describe what information you want to extract from the page
This tool is read-only and does not modify any files
Results may be summarized if the content is very large
Includes a self-cleaning 15-minute cache for faster responses when repeatedly accessing the same URL
When a URL redirects to a different host, the tool will inform you and provide the redirect URL in a special format. You should then make a new WebFetch request with the redirect URL to fetch the content.
For GitHub URLs, prefer using the gh CLI via Bash instead (e.g., gh pr view, gh issue view, gh api).
Parameters:
url [string] (required) - The URL to fetch content from
prompt [string] (required) - The prompt to run on the fetched content
[-] WebSearch
Allows Claude to search the web and use the results to inform responses
Provides up-to-date information for current events and recent data
Returns search result information formatted as search result blocks, including links as markdown hyperlinks
Use this tool for accessing information beyond Claude's knowledge cutoff
Searches are performed automatically within a single API call
CRITICAL REQUIREMENT - You MUST follow this:

After answering the user's question, you MUST include a "Sources:" section at the end of your response

In the Sources section, list all relevant URLs from the search results as markdown hyperlinks: Title

This is MANDATORY - never skip including sources in your response

Example format:

[Your answer here]

Sources:

Source Title 1
Source Title 2
Usage notes:

Domain filtering is supported to include or block specific websites
Web search is only available in the US
IMPORTANT - Use the correct year in search queries:

The current month is February 2026. You MUST use this year when searching for recent information, documentation, or current events.
Example: If the user asks for "latest React docs", search for "React documentation" with the current year, NOT last year
Parameters:
query [string] (required) - The search query to use
allowed_domains [array] - Only include search results from these domains
blocked_domains [array] - Never include search results from these domains
[-] TaskStop
Stops a running background task by its ID
Takes a task_id parameter identifying the task to stop
Returns a success or failure status
Use this tool when you need to terminate a long-running task
Parameters:
task_id [string] - The ID of the background task to stop
shell_id [string] - Deprecated: use task_id instead
[-] AskUserQuestion
Use this tool when you need to ask the user questions during execution. This allows you to:

Gather user preferences or requirements
Clarify ambiguous instructions
Get decisions on implementation choices as you work
Offer choices to the user about what direction to take.
Usage notes:

Users will always be able to select "Other" to provide custom text input
Use multiSelect: true to allow multiple answers to be selected for a question
If you recommend a specific option, make that the first option in the list and add "(Recommended)" at the end of the label
Plan mode note: In plan mode, use this tool to clarify requirements or choose between approaches BEFORE finalizing your plan. Do NOT use this tool to ask "Is my plan ready?" or "Should I proceed?" - use ExitPlanMode for plan approval. IMPORTANT: Do not reference "the plan" in your questions (e.g., "Do you have feedback about the plan?", "Does the plan look good?") because the user cannot see the plan in the UI until you call ExitPlanMode. If you need plan approval, use ExitPlanMode instead.

Preview feature:
Use the optional markdown field on options when presenting concrete artifacts that users need to visually compare:

ASCII mockups of UI layouts or components
Code snippets showing different implementations
Diagram variations
Configuration examples
When any option has a markdown, the UI switches to a side-by-side layout with a vertical option list on the left and preview on the right. Do not use previews for simple preference questions where labels and descriptions suffice. Note: previews are only supported for single-select questions (not multiSelect).

Parameters:
questions [array] (required) - Questions to ask the user (1-4 questions)
answers [object] - User answers collected by the permission component
annotations [object] - Optional per-question annotations from the user (e.g., notes on preview selections). Keyed by question text.
metadata [object] - Optional metadata for tracking and analytics purposes. Not displayed to user.
[-] Skill
Execute a skill within the main conversation

When users ask you to perform tasks, check if any of the available skills match. Skills provide specialized capabilities and domain knowledge.

When users reference a "slash command" or "/<something>" (e.g., "/commit", "/review-pr"), they are referring to a skill. Use this tool to invoke it.

How to invoke:

Use this tool with the skill name and optional arguments
Examples:
skill: &quot;pdf&quot; - invoke the pdf skill
skill: &quot;commit&quot;, args: &quot;-m &#39;Fix bug&#39;&quot; - invoke with arguments
skill: &quot;review-pr&quot;, args: &quot;123&quot; - invoke with arguments
skill: &quot;ms-office-suite:pdf&quot; - invoke using fully qualified name
Important:

Available skills are listed in system-reminder messages in the conversation
When a skill matches the user's request, this is a BLOCKING REQUIREMENT: invoke the relevant Skill tool BEFORE generating any other response about the task
NEVER mention a skill without actually calling this tool
Do not invoke a skill that is already running
Do not use this tool for built-in CLI commands (like /help, /clear, etc.)
If you see a <command-name> tag in the current conversation turn, the skill has ALREADY been loaded - follow the instructions directly instead of calling this tool again
Parameters:
skill [string] (required) - The skill name. E.g., "commit", "review-pr", or "pdf"
args [string] - Optional arguments for the skill
[-] EnterPlanMode
Use this tool proactively when you're about to start a non-trivial implementation task. Getting user sign-off on your approach before writing code prevents wasted effort and ensures alignment. This tool transitions you into plan mode where you can explore the codebase and design an implementation approach for user approval.

When to Use This Tool
Prefer using EnterPlanMode for implementation tasks unless they're simple. Use it when ANY of these conditions apply:

New Feature Implementation: Adding meaningful new functionality

Example: "Add a logout button" - where should it go? What should happen on click?
Example: "Add form validation" - what rules? What error messages?
Multiple Valid Approaches: The task can be solved in several different ways

Example: "Add caching to the API" - could use Redis, in-memory, file-based, etc.
Example: "Improve performance" - many optimization strategies possible
Code Modifications: Changes that affect existing behavior or structure

Example: "Update the login flow" - what exactly should change?
Example: "Refactor this component" - what's the target architecture?
Architectural Decisions: The task requires choosing between patterns or technologies

Example: "Add real-time updates" - WebSockets vs SSE vs polling
Example: "Implement state management" - Redux vs Context vs custom solution
Multi-File Changes: The task will likely touch more than 2-3 files

Example: "Refactor the authentication system"
Example: "Add a new API endpoint with tests"
Unclear Requirements: You need to explore before understanding the full scope

Example: "Make the app faster" - need to profile and identify bottlenecks
Example: "Fix the bug in checkout" - need to investigate root cause
User Preferences Matter: The implementation could reasonably go multiple ways

If you would use AskUserQuestion to clarify the approach, use EnterPlanMode instead
Plan mode lets you explore first, then present options with context
When NOT to Use This Tool
Only skip EnterPlanMode for simple tasks:

Single-line or few-line fixes (typos, obvious bugs, small tweaks)
Adding a single function with clear requirements
Tasks where the user has given very specific, detailed instructions
Pure research/exploration tasks (use the Task tool with explore agent instead)
What Happens in Plan Mode
In plan mode, you'll:

Thoroughly explore the codebase using Glob, Grep, and Read tools
Understand existing patterns and architecture
Design an implementation approach
Present your plan to the user for approval
Use AskUserQuestion if you need to clarify approaches
Exit plan mode with ExitPlanMode when ready to implement
Examples
GOOD - Use EnterPlanMode:
User: "Add user authentication to the app"

Requires architectural decisions (session vs JWT, where to store tokens, middleware structure)
User: "Optimize the database queries"

Multiple approaches possible, need to profile first, significant impact
User: "Implement dark mode"

Architectural decision on theme system, affects many components
User: "Add a delete button to the user profile"

Seems simple but involves: where to place it, confirmation dialog, API call, error handling, state updates
User: "Update the error handling in the API"

Affects multiple files, user should approve the approach
BAD - Don't use EnterPlanMode:
User: "Fix the typo in the README"

Straightforward, no planning needed
User: "Add a console.log to debug this function"

Simple, obvious implementation
User: "What files handle routing?"

Research task, not implementation planning
Important Notes
This tool REQUIRES user approval - they must consent to entering plan mode
If unsure whether to use it, err on the side of planning - it's better to get alignment upfront than to redo work
Users appreciate being consulted before significant changes are made to their codebase
Parameters:
[-] TaskCreate
Use this tool to create a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.
It also helps the user understand the progress of the task and overall progress of their requests.

When to Use This Tool
Use this tool proactively in these scenarios:

Complex multi-step tasks - When a task requires 3 or more distinct steps or actions
Non-trivial and complex tasks - Tasks that require careful planning or multiple operations
Plan mode - When using plan mode, create a task list to track the work
User explicitly requests todo list - When the user directly asks you to use the todo list
User provides multiple tasks - When users provide a list of things to be done (numbered or comma-separated)
After receiving new instructions - Immediately capture user requirements as tasks
When you start working on a task - Mark it as in_progress BEFORE beginning work
After completing a task - Mark it as completed and add any new follow-up tasks discovered during implementation
When NOT to Use This Tool
Skip using this tool when:

There is only a single, straightforward task
The task is trivial and tracking it provides no organizational benefit
The task can be completed in less than 3 trivial steps
The task is purely conversational or informational
NOTE that you should not use this tool if there is only one trivial task to do. In this case you are better off just doing the task directly.

Task Fields
subject: A brief, actionable title in imperative form (e.g., "Fix authentication bug in login flow")
description: Detailed description of what needs to be done, including context and acceptance criteria
activeForm: Present continuous form shown in spinner when task is in_progress (e.g., "Fixing authentication bug"). This is displayed to the user while you work on the task.
IMPORTANT: Always provide activeForm when creating tasks. The subject should be imperative ("Run tests") while activeForm should be present continuous ("Running tests"). All tasks are created with status pending.

Tips
Create tasks with clear, specific subjects that describe the outcome
Include enough detail in the description for another agent to understand and complete the task
After creating tasks, use TaskUpdate to set up dependencies (blocks/blockedBy) if needed
Check TaskList first to avoid creating duplicate tasks
Parameters:
subject [string] (required) - A brief title for the task
description [string] (required) - A detailed description of what needs to be done
activeForm [string] - Present continuous form shown in spinner when in_progress (e.g., "Running tests")
metadata [object] - Arbitrary metadata to attach to the task
[-] TaskGet
Use this tool to retrieve a task by its ID from the task list.

When to Use This Tool
When you need the full description and context before starting work on a task
To understand task dependencies (what it blocks, what blocks it)
After being assigned a task, to get complete requirements
Output
Returns full task details:

subject: Task title
description: Detailed requirements and context
status: 'pending', 'in_progress', or 'completed'
blocks: Tasks waiting on this one to complete
blockedBy: Tasks that must complete before this one can start
Tips
After fetching a task, verify its blockedBy list is empty before beginning work.
Use TaskList to see all tasks in summary form.
Parameters:
taskId [string] (required) - The ID of the task to retrieve
[-] TaskUpdate
Use this tool to update a task in the task list.

When to Use This Tool
Mark tasks as resolved:

When you have completed the work described in a task

When a task is no longer needed or has been superseded

IMPORTANT: Always mark your assigned tasks as resolved when you finish them

After resolving, call TaskList to find your next task

ONLY mark a task as completed when you have FULLY accomplished it

If you encounter errors, blockers, or cannot finish, keep the task as in_progress

When blocked, create a new task describing what needs to be resolved

Never mark a task as completed if:

Tests are failing
Implementation is partial
You encountered unresolved errors
You couldn't find necessary files or dependencies
Delete tasks:

When a task is no longer relevant or was created in error
Setting status to deleted permanently removes the task
Update task details:

When requirements change or become clearer
When establishing dependencies between tasks
Fields You Can Update
status: The task status (see Status Workflow below)
subject: Change the task title (imperative form, e.g., "Run tests")
description: Change the task description
activeForm: Present continuous form shown in spinner when in_progress (e.g., "Running tests")
owner: Change the task owner (agent name)
metadata: Merge metadata keys into the task (set a key to null to delete it)
addBlocks: Mark tasks that cannot start until this one completes
addBlockedBy: Mark tasks that must complete before this one can start
Status Workflow
Status progresses: pending â in_progress â completed

Use deleted to permanently remove a task.

Staleness
Make sure to read a task's latest state using TaskGet before updating it.

Examples
Mark task as in progress when starting work:

{&quot;taskId&quot;: &quot;1&quot;, &quot;status&quot;: &quot;in_progress&quot;}
Mark task as completed after finishing work:

{&quot;taskId&quot;: &quot;1&quot;, &quot;status&quot;: &quot;completed&quot;}
Delete a task:

{&quot;taskId&quot;: &quot;1&quot;, &quot;status&quot;: &quot;deleted&quot;}
Claim a task by setting owner:

{&quot;taskId&quot;: &quot;1&quot;, &quot;owner&quot;: &quot;my-name&quot;}
Set up task dependencies:

{&quot;taskId&quot;: &quot;2&quot;, &quot;addBlockedBy&quot;: [&quot;1&quot;]}
Parameters:
taskId [string] (required) - The ID of the task to update
subject [string] - New subject for the task
description [string] - New description for the task
activeForm [string] - Present continuous form shown in spinner when in_progress (e.g., "Running tests")
status - New status for the task
addBlocks [array] - Task IDs that this task blocks
addBlockedBy [array] - Task IDs that block this task
owner [string] - New owner for the task
metadata [object] - Metadata keys to merge into the task. Set a key to null to delete it.
[-] TaskList
Use this tool to list all tasks in the task list.

When to Use This Tool
To see what tasks are available to work on (status: 'pending', no owner, not blocked)
To check overall progress on the project
To find tasks that are blocked and need dependencies resolved
After completing a task, to check for newly unblocked work or claim the next available task
Prefer working on tasks in ID order (lowest ID first) when multiple tasks are available, as earlier tasks often set up context for later ones
Output
Returns a summary of each task:

id: Task identifier (use with TaskGet, TaskUpdate)
subject: Brief description of the task
status: 'pending', 'in_progress', or 'completed'
owner: Agent ID if assigned, empty if available
blockedBy: List of open task IDs that must be resolved first (tasks with blockedBy cannot be claimed until dependencies resolve)
Use TaskGet with a specific task ID to view full details including description and comments.

Parameters:
[-] LSP
Interact with Language Server Protocol (LSP) servers to get code intelligence features.

Supported operations:

goToDefinition: Find where a symbol is defined
findReferences: Find all references to a symbol
hover: Get hover information (documentation, type info) for a symbol
documentSymbol: Get all symbols (functions, classes, variables) in a document
workspaceSymbol: Search for symbols across the entire workspace
goToImplementation: Find implementations of an interface or abstract method
prepareCallHierarchy: Get call hierarchy item at a position (functions/methods)
incomingCalls: Find all functions/methods that call the function at a position
outgoingCalls: Find all functions/methods called by the function at a position
All operations require:

filePath: The file to operate on
line: The line number (1-based, as shown in editors)
character: The character offset (1-based, as shown in editors)
Note: LSP servers must be configured for the file type. If no server is available, an error will be returned.

Parameters:
operation [string] (required) - The LSP operation to perform
filePath [string] (required) - The absolute or relative path to the file
line [integer] (required) - The line number (1-based, as shown in editors)
character [integer] (required) - The character offset (1-based, as shown in editors)
[-] EnterWorktree
Use this tool ONLY when the user explicitly asks to work in a worktree. This tool creates an isolated git worktree and switches the current session into it.

When to Use
The user explicitly says "worktree" (e.g., "start a worktree", "work in a worktree", "create a worktree", "use a worktree")
When NOT to Use
The user asks to create a branch, switch branches, or work on a different branch â use git commands instead
The user asks to fix a bug or work on a feature â use normal git workflow unless they specifically mention worktrees
Never use this tool unless the user explicitly mentions "worktree"
Requirements
Must be in a git repository, OR have WorktreeCreate/WorktreeRemove hooks configured in settings.json
Must not already be in a worktree
Behavior
In a git repository: creates a new git worktree inside .claude/worktrees/ with a new branch based on HEAD
Outside a git repository: delegates to WorktreeCreate/WorktreeRemove hooks for VCS-agnostic isolation
Switches the session's working directory to the new worktree
On session exit, the user will be prompted to keep or remove the worktree
Parameters
name (optional): A name for the worktree. If not provided, a random name is generated.
Parameters:
name [string] - Optional name for the worktree. A random name is generated if not provided.