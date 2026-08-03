# Memory Policy

Repository: `LouisShark/chatgpt_system_prompt`  
Pilot: Supermemory MCP (repository-scoped)

---

## 1. Authority Order

When information from multiple sources conflicts, prefer sources higher in this list:

1. **Checked-in source files and project specifications** (highest authority)
2. **CLAUDE.md and repository-level AI instructions**
3. **Reviewed project documentation or approved canonical documents**
4. **Supermemory repository-session recall**
5. **Model inference** (lowest authority)

**Memory does not override source code, tests, specifications, or current user
instructions.**  Captured conversations are context, not canon.

---

## 2. What May Be Saved

Memories are written **explicitly** — automatic capture of full conversations is
not enabled.  Only save information that meets all of the following:

- It is a confirmed, reviewed decision (not a guess or debugging hypothesis).
- It is not already expressed in a checked-in file.
- It would provide genuine onboarding value in a future session.
- It contains no secrets, credentials, personal data, or private file paths.

### Required fields when saving a decision

```
Decision:      <what was decided, in one or two sentences>
Date:          <YYYY-MM-DD>
Repository:    LouisShark/chatgpt_system_prompt
Supporting:    <file path, commit SHA, or issue/PR URL>
Status:        active | superseded
Confidence:    high | medium | low
Superseded-by: <identifier of the later decision, or "n/a">
```

---

## 3. What Must Never Be Saved

- API keys, tokens, passwords, or any credential.
- `.env` contents or any secret-file contents.
- Private URLs, internal hostnames, or IP addresses.
- Personal data (names, emails, home directories, account details).
- Local absolute file paths (use repo-relative paths only).
- Speculative conclusions or temporary debugging guesses.
- Unreviewed architectural decisions made under time pressure.
- Full conversation transcripts (save only the reviewed conclusion).
- Content from `prompts/**` — these are community-contributed files and must
  not be ingested into a memory system without explicit contributor consent.

---

## 4. Handling Stale Memories

A memory is stale when it describes a decision that has since been superseded by
a checked-in change, a later architectural decision, or a user correction.

**Detection**: When a retrieved memory conflicts with a checked-in file or current
instructions, treat the checked-in file as authoritative.

**Action**: When a stale memory is identified, delete it immediately using the
`delete_memory` MCP tool, then optionally save a replacement with `Status: active`
and `Superseded-by: <previous memory ID>`.

---

## 5. Correcting Incorrect Memories

1. Identify the incorrect memory using `search_memory` or `list_memories`.
2. Note its memory ID.
3. Delete it using `delete_memory`.
4. Save a corrected replacement if the underlying information is still valid.

Do not leave an incorrect memory in place even if it seems minor — memory
authority conflicts can propagate across sessions.

---

## 6. Deleting Memories

Use the `delete_memory` MCP tool with the memory's ID.

```
# Via MCP tool call:
delete_memory({ "id": "<memory-id>" })
```

If you do not have the memory ID, use `list_memories` or `search_memory` first.

---

## 7. Inspecting Stored Memories

```
# List all memories for this repository:
list_memories({ "filter": "LouisShark/chatgpt_system_prompt" })

# Search by keyword:
search_memory({ "query": "idxtool architecture" })
```

---

## 8. Disabling the Pilot

To stop using Supermemory in Claude Code without removing configuration:

1. Remove or comment out the `supermemory` entry in `.mcp.json`.
2. Restart Claude Code.

The configuration file is preserved so it can be re-enabled by reverting step 1.

---

## 9. Fully Removing the Integration

See [`rollback.md`](rollback.md) for complete removal instructions.

Short version:
1. Delete `.mcp.json`.
2. Delete `.env` (already gitignored).
3. Optionally delete all stored memories via the Supermemory console at
   [console.supermemory.ai](https://console.supermemory.ai) or by calling
   `delete_memory` for each stored item.

---

## 10. What Memory Does Not Do

- Memory does not override checked-in source code.
- Memory does not override tests or specifications.
- Memory does not override the current user's instructions in a session.
- Memory does not constitute approval of an architectural decision — only a
  confirmed and reviewed decision may be saved.
- Memory does not replace reading the repository — it supplements onboarding.

---

## 11. Data Residency and Privacy

| Question | Answer |
|----------|--------|
| Where is data stored? | Supermemory cloud infrastructure (supermemory.ai) |
| Self-hosted option? | Available at Scale/Enterprise tier only |
| Retention | Indefinite until explicitly deleted |
| Deletion | `delete_memory` tool or Supermemory console |
| Data leaving the machine | Yes — memories are sent to `api.supermemory.ai` |
| Authentication | API key from `console.supermemory.ai` |
| Automatic session capture | Disabled — explicit writes only (no auto-ingest hook) |

Review Supermemory's privacy policy and terms before ingesting any sensitive data:
[https://supermemory.ai](https://supermemory.ai)
