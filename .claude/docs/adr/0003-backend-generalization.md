---
doc-type: adr
id: adr-0003
status: accepted
date: 2026-07-17
ratified: 2026-07-17 (maintainer, in-session AskUserQuestion — two rulings, one session; a post-ratification doc-review pass then fixed wording/factual errors only — GraphQL vs. REST, a missing Alternative, a duplicated-phrasing bullet — no change to either ratified decision's substance)
owner: kim.granlund
supersedes: null
---
# ADR-0003 — Backend generalization: a three-way work-item backend (local / git-native / external) behind one resolver seam

## Context

scribe's `bug-report`, `feature`, and `issue` skills each carry an identical "Phase 0, decided
once per run" backend seam: a workspace picks the **file backend** (a `docs/tickets/` TICKET,
doc-forge's path) unless its entry file rules a **git-native backend** (`gh issue`, the pattern
this workspace itself adopted in ADR-0002) — the same prose, hand-duplicated across three
SKILL.md files (the `issue` skill's own header already names this as "shared verbatim," a
duplication risk, not a feature).

A 2026-07-17 `/scribe:issue` seed asked for a third option — routing work items into an external
tracker (Linear/Jira/Notion/a custom system) via MCP or REST — plus watching that tracker for
items filed by other people. `system-decompose` ran against both asks
(`.claude/docs/decompositions/ticketing-backend-watch-manifest-v1.json`, coverage-clean, fresh-context
critic reviewed) and found they cross-check as two independent concerns: **which backend holds
the record** (this ADR) and **how items enter the system** — pull vs. watch-and-triage — which
only matters for non-local backends and carries its own trust/security surface (deferred to
`spec-ticketing-watch-triage`, gated on this ADR). A same-day follow-up named Linear specifically
and, asked to disambiguate "add Linear as an option," chose a real shipped adapter over a
menu-only label — the manifest replanned to v2
(`.claude/docs/decompositions/ticketing-backend-watch-manifest-v2.json`, coverage-clean, diff and
reason recorded in its `_meta`) to add that structure before this Decision was finalized. A
fresh-context review of the resulting SPECs then caught a further gap the manifest itself had
missed — the watch loop needs a "list what changed since X" adapter operation neither v1 nor v2
defined — replanned again to v3
(`.claude/docs/decompositions/ticketing-backend-watch-manifest-v3.json`) before this ADR's own
review findings were applied.

## Decision

1. **Three backend options, one resolver.** The binary seam generalizes to a named choice per
   repo: **Option A — local** (today's file-backend default, unchanged), **Option B —
   git-native** (today's `gh issue` path; ADR-0002 is this workspace's own ruled instance),
   **Option C — external** (a typed adapter interface — create, dedup-search, update, close —
   realized via MCP or REST), with **Linear as a named, scribe-shipped Option-C adapter**
   distinct from a bring-your-own external adapter against the same interface (see Decision 3). A
   repo rules its choice once, the same way ADR-0002 ruled git-native for this workspace: a
   routing-table row in the entry file, never guessed at invocation time.
2. **A shared backend resolver replaces the three hand-duplicated Phase-0 checks.** `bug-report`,
   `feature`, and `issue` each call one resolver that reads the entry-file ruling and returns the
   active adapter — closing the duplication named in Context, not just extending it a third way.
3. **Scribe ships one concrete Option-C adapter — Linear — everything else is bring-your-own.**
   Linear's MCP server (preferred) or GraphQL API (fallback — Linear has no REST surface) becomes
   a first-class adapter alongside the local and git-native ones, carrying the same
   create/dedup-search/update/close/discover contract and the same findings-first close rule
   (contracted in full in `spec-linear-adapter`). Any other external tracker (Jira, Notion, a
   custom system) still authors or installs its own adapter against the published interface and
   rules it in its entry file — the division of labor ADR-0002 already draws between scribe's
   portable skill behavior and a workspace's own routing override, now narrowed to "everything
   except Linear."

**Alternative considered — bolt Option C on as a per-skill special case:** rejected; it reproduces
the exact three-way duplication this ADR exists to close, just with a third branch.
**Alternative considered — resolve the backend per invocation instead of once per repo:**
rejected; it breaks the existing "Phase 0, decided once per run" contract and ADR-0002's own
precedent of a durable, inspectable ruling, for no offsetting benefit — a repo's backend does not
change invocation to invocation.
**Alternative considered — ship Linear as a menu-only label over the generic interface:**
rejected (the same-day follow-up this Decision was revised for); it renames Option C without
shipping anything real, and doesn't meet the ask that prompted this Decision in the first place.

## Consequences

- `bug-report`/`feature`/`issue`'s Phase-0 sections collapse from three near-identical prose
  blocks to "call the resolver" — a real de-duplication, and doc-authoring-standards' backend
  delegation clause (currently written as a binary) needs the same three-way update in the same
  change.
- A workspace choosing Option C for anything other than Linear still takes on adapter-authoring
  responsibility scribe does not provide out of the box; this is a real cost, stated here rather
  than discovered mid-build.
- Shipping a real Linear adapter is a real, ongoing cost of its own: scribe now owns keeping that
  adapter working as Linear's MCP surface or GraphQL API changes, distinct from (and larger than)
  the interface-only maintenance Option C otherwise implies — the tradeoff a "real adapter"
  commits to over a "menu-only label."
- Nothing about watching a backend for externally-filed items, triage classification, or a
  trust/friendlies gate is decided by this ADR — that capability is scoped in
  `spec-ticketing-watch-triage` and applies only when the resolved backend is Option B or C
  (only external systems have actors filing items nobody in this workspace typed).
- Existing Option A and Option B behavior is unchanged; this ADR is additive at the seam, not a
  breaking change to either path.
