# Supermemory Pilot Log

Repository: `LouisShark/chatgpt_system_prompt`  
Pilot start: 2026-08-03  
Pilot end: _(fill in after session 10)_

## Setup Notes

**API key type**: Personal app token (`sm_*`) from `app.supermemory.ai`.  
**Observation**: Personal app tokens work for `/v3/documents` (ingest) but the
`/v3/memories` endpoint requires a developer console key from `console.supermemory.ai`.
For full MCP tool access (add_memory, search_memory, list_memories, delete_memory),
use a developer console key.

**Documents ingested during setup** (2026-08-03):
- `vPkZZehdpKnJgzy6EDjs5i` — Python+GitPython runtime decision (status: done)
- `i9VuPm61Y8A1ZSu2jBga19` — Scope Creep Detector local implementation decision
- `CNr3Y35uNwa8G6utouAABB` — Supermemory authority order decision
- `Hhdq9UTFnnuCXWxBL37VTQ` — Project context (files not to modify, CI workflows)
- `5Mq2ND5B426PtgnXww6k9w` — Runtime architecture decision (instant mode)

**Search test**: Returned 0 results at time of setup. Documents still indexing or
search requires developer console key scope. Re-test after obtaining a developer key.

---

## Acceptance Conditions

The pilot is accepted when ALL of the following are met after ten complete sessions:

| Condition | Threshold | Status |
|-----------|-----------|--------|
| Known decisions correctly recalled | ≥ 8 of 10 | ⏳ pending |
| Stale decision presented as binding | 0 | ⏳ pending |
| Sensitive-data incidents | 0 | ⏳ pending |
| Unresolved authority conflicts | 0 | ⏳ pending |
| Materially incorrect injected memories | ≤ 1 | ⏳ pending |
| Avg. onboarding savings (substantial sessions) | ≥ 10 minutes | ⏳ pending |

**Do not claim the pilot succeeded before ten sessions have been recorded.**

---

## Evaluation Table

| # | Task | Decisions available | Correctly recalled | Stale injected | Materially incorrect | Onboarding saved (min) | Authority conflicts | Sensitive-data incidents | User correction required | Recommendation |
|---|------|--------------------|--------------------|---------------|---------------------|----------------------|-------------------|------------------------|------------------------|---------------|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |
| 6 | | | | | | | | | | |
| 7 | | | | | | | | | | |
| 8 | | | | | | | | | | |
| 9 | | | | | | | | | | |
| 10 | | | | | | | | | | |
| **Total** | | | | | | | | | | |

---

## Column Definitions

| Column | Definition |
|--------|-----------|
| Task | One-line description of the work done in the session |
| Decisions available | Number of relevant stored memories available at session start |
| Correctly recalled | Memories that were accurate and surfaced at the right moment |
| Stale injected | Memories that were outdated but presented as current |
| Materially incorrect | Memories that contained factually wrong information that influenced the session |
| Onboarding saved | Estimated minutes saved vs. starting cold (only count substantial sessions) |
| Authority conflicts | Cases where memory was used in conflict with a checked-in file or explicit instruction |
| Sensitive-data incidents | Any case where a secret, credential, or personal datum appeared in a memory |
| User correction required | Times the user had to explicitly correct a memory-derived claim |
| Recommendation | keep / modify / remove |

---

## Notes and Observations

_(Add session notes here as you complete each session.)_

---

## Intermediate Assessment (after session 5)

_(Fill in after session 5.)_

---

## Final Assessment (after session 10)

_(Fill in after session 10.)_

**Verdict**: _(ACCEPTED / REJECTED / EXTENDED — record date and rationale)_
