---
doc-type: spec
id: spec-linear-adapter
status: draft
version: 0.2.0
date: 2026-07-18
owner: kim.granlund
prd: null   # no PRD — descends directly from ADR-0003's Decision 3 (Linear ships as a concrete,
            # scribe-shipped Option-C adapter, everything else Option-C stays bring-your-own)
---
# SPEC — The Linear adapter (scribe's shipped Option-C backend)

Precondition: **ADR-0003** must be `accepted` — this SPEC contracts the one concrete Option-C
adapter ADR-0003 Decision 3 commits scribe to shipping. It is a sibling of, not a dependency of,
`spec-ticketing-watch-triage`: that SPEC's watch/triage/trust behavior applies to *any* Option B/C
backend, including this one, without change.

**v0.2.0 amendment (2026-07-18):** REQ-010/AC-010 added. Three independent fresh-context audits of
the implementing skills (`bug-report`/`feature`/`issue`) converged on the same gap: AC-004 and
AC-007 already required "read back through the adapter," and every capture skill's resume-by-id
and post-dispatch status-check logic needs to resolve an adapter-native id to a record, but no
REQ named the operation that does this — the five-operation list (REQ-001) was silently missing
its sixth, load-bearing member. v0.1.0's REQ-001 through REQ-009 are otherwise unchanged.

## Requirements

- **REQ-001** — Interface conformance. The Linear adapter implements the same six operations the
  local and git-native adapters implement — create, dedup-search, update, close, discover
  (REQ-009), and read (REQ-010) — behind the backend resolver (ADR-0003 Decision 2), so capture
  skills (`bug-report`/`feature`/`issue`) and the watch loop (`spec-ticketing-watch-triage`
  REQ-003) call it identically to the other two adapters, with no Linear-specific branch in their
  own logic.
- **REQ-002** — Transport preference. The adapter uses Linear's MCP server when the workspace has
  it connected; it falls back to Linear's GraphQL API (with a workspace-supplied API key) when no
  MCP connection is available — Linear has no REST surface, so GraphQL is the only fallback.
  Which transport is active is resolved at call time, not hardcoded.
- **REQ-003** — Configuration capture. Linear-specific configuration (an API key or MCP connector
  reference, and the target Linear workspace/team/project) is captured once during repo
  configuration and persisted in the entry-file ruling alongside the backend choice — never
  re-prompted per invocation, never guessed.
- **REQ-004** — Payload-contract fidelity. A record created via the Linear adapter carries the
  full payload contract for its type and kind, per doc-authoring-standards — the TICKET base
  (Summary · Acceptance · Links) plus whatever kind-specific sections apply (`kind: bug`'s Repro ·
  Expected-vs-actual · Classification · Severity; `kind: feature`'s Scope/Open) — plus Findings,
  mapped onto Linear's native fields (title, description, labels, comments); the contract is
  backend-invariant, only its storage shape differs. No section is dropped or silently merged into
  another.
- **REQ-005** — Dedup search. Before create, the adapter searches existing Linear issues for a
  match using the same "sweep before minting" discipline the local and git-native adapters already
  apply. A create call matching an already-open issue updates that issue (REQ-007's fields) instead
  of minting a duplicate; the same item is never captured twice through this adapter.
- **REQ-006** — Findings-first close. Closing a Linear-backed record follows the same rule as the
  other two adapters: a close with an empty Findings section takes the close-out line as its first
  entry — a record never closes silent, regardless of which backend holds it.
- **REQ-007** — Status mapping. The shared work-item status vocabulary (open/doing/done/wontfix)
  maps onto Linear's native workflow **state types** — Linear groups a team's own named states
  into six fixed types (triage, backlog, unstarted, started, completed, canceled); actual state
  names are per-team and configurable, so the mapping (REQ-003) binds each status to a state
  *type*, then to that team's specific state of that type, never to a hardcoded name. Writing a
  status (`open`/`doing`/`done`/`wontfix`) always sets the exact configured state (REQ-003).
  Reading a Linear issue back that is currently in a state the adapter never wrote (a human moved
  it manually, e.g. to a team's custom "In Review" state) reports the shared vocabulary's nearest
  covering status by state *type* (started → `doing`, completed → `done`, canceled → `wontfix`,
  triage/backlog/unstarted → `open`) — a best-effort type-level classification, not a hard failure
  and not a claim of exact reversibility for states the adapter didn't itself set.
- **REQ-008** — Failure fallback. If the Linear adapter fails partway through an operation (auth
  failure, API error, MCP disconnect), the caller falls back to the file backend for that one
  operation and reports the fallback — the same failure-branch discipline the `issue` skill's own
  git-native-backend fallback already documents, applied to Option C.
- **REQ-009** — Discovery. The adapter exposes a fifth operation beyond create/dedup-search/
  update/close: list issues created or updated in the configured team/project since a given
  checkpoint (a timestamp or cursor) — the primitive `spec-ticketing-watch-triage` REQ-003's watch
  loop calls. It is its own operation with its own pagination/checkpoint contract, not a filtered
  call to dedup-search (REQ-005), which matches one candidate record rather than enumerating every
  change since a point in time.
- **REQ-010** — Record read-back. The adapter exposes a `read` operation: fetch one record, by its
  adapter-native id, together with its Findings/comment trail — the same primitive the local
  adapter realizes as a plain file read and the git-native adapter realizes as `gh issue view
  --comments`. Every capture skill's resume-by-id branch (Phase 1) resolves an id in the resolved
  adapter's own native format through this operation before falling through to "fresh item," and
  the post-dispatch close-out (bug-report Phase 6) uses it to check whether a dispatched
  investigation posted a Findings entry while it ran. Distinct from dedup-search (REQ-005, matches
  a candidate by content) and discover (REQ-009, enumerates by checkpoint): read resolves one
  already-known id to its full record.

## Non-goals

- Any other external tracker's concrete adapter (Jira, Notion, a custom system) — ADR-0003
  Decision 3 keeps those bring-your-own; only Linear ships.
- Two-way sync back from a manual edit made directly in Linear's UI outside the adapter — this
  SPEC contracts scribe's write/read path through the adapter, not a general Linear-sync engine.
- Linear-specific features with no analogue in the shared payload contract (custom fields, Linear
  Cycles/Projects hierarchy, Linear-native automations) — out of scope until a future SPEC extends
  the shared contract itself to name them.
- Choosing Linear as the auto-detected default when a workspace has a Linear MCP connection but
  hasn't explicitly ruled Option C — REQ-003's explicit configuration capture is required; nothing
  here auto-opts a repo in.

## Examples

**[NORMATIVE]** A repo rules Option C / Linear during configuration, with an MCP connector already
attached. `/bug-report` runs, dedup-searches Linear via MCP (REQ-005), finds no match, creates a
Linear issue whose description carries its full kind-appropriate section set (REQ-004), and later
a `/issue <id> done` close leaves a dated Findings entry even though none existed before (REQ-006).

**[NORMATIVE]** The same repo's MCP connector is disconnected mid-session. The next capture
attempt's Linear call fails (REQ-008); the caller falls back to a file-backend ticket for that one
operation and reports the fallback in its close-out — no operation is silently dropped.

**[ILLUSTRATIVE]** A resolved backend ruling after configuration:
`backend: C (external) · adapter: linear · transport: mcp (fallback: graphql) · team: ENG` — the
same shape ADR-0003's resolver reads for any Option C choice, with `adapter: linear` selecting
this SPEC's implementation over a bring-your-own one.

**[ILLUSTRATIVE]** Discovery in action: the watch loop calls the adapter's discover operation
(REQ-009) with the checkpoint from its last successful run; the adapter returns every issue
created or updated in team `ENG` since that checkpoint, plus a new checkpoint to persist for next
time — the shape `spec-ticketing-watch-triage` REQ-003 consumes.

## Acceptance

- **AC-001** (↔ REQ-001) — A capture skill's call sequence against the Linear adapter and against
  the local adapter are structurally identical (same five operations, same call sites); no
  Linear-only conditional exists in the capture skills' own code.
- **AC-002** (↔ REQ-002) — With an MCP connector present, a fixture create call routes over MCP;
  with it absent but an API key configured, the identical call routes over GraphQL; the caller
  code path is the same either way.
- **AC-003** (↔ REQ-003) — Linear config captured during setup round-trips unchanged through the
  entry-file ruling on a subsequent resolver read; no invocation re-prompts for it.
- **AC-004** (↔ REQ-004) — A record minted via the Linear adapter, read back through the adapter,
  exposes its full kind-appropriate section set with their original content intact — a `kind: bug`
  fixture exposes Repro/Expected-vs-actual/Classification/Severity, a `kind: feature` fixture
  exposes Scope/Open, both alongside Summary/Acceptance/Links/Findings.
- **AC-005** (↔ REQ-005) — Creating with an intentionally-duplicated fixture title/body against an
  already-existing Linear issue updates that existing issue's fields, not a second issue.
- **AC-006** (↔ REQ-006) — Closing a fixture record with an empty Findings section produces exactly
  one Findings entry equal to the close-out line.
- **AC-007** (↔ REQ-007) — Writing each of open/doing/done/wontfix through the adapter, then
  reading back through the adapter, returns the exact same status for every value written by the
  adapter itself. Separately, a fixture issue moved to a team's custom state outside the adapter
  (e.g. a "Blocked" state of type `started`) reads back as `doing` — the type-level bucket, never
  an error and never a fifth status value.
- **AC-008** (↔ REQ-008) — A fixture run with the MCP connector forcibly disconnected mid-call
  completes with a file-backend record created for that operation and a fallback line in the
  close-out report, not a silent failure or an unhandled exception.
- **AC-009** (↔ REQ-009) — Given a checkpoint and one issue created plus one issue updated in the
  configured team after it, a discover call returns exactly those two issues and a new checkpoint;
  a second discover call using the new checkpoint returns nothing until a further change occurs.
- **AC-010** (↔ REQ-010) — Given the native id of a record already created via the adapter, a read
  call returns that record's current fields and its full Findings/comment trail; given an id that
  does not exist on the configured team, read reports not-found rather than throwing an unhandled
  exception, and the calling skill treats that exactly as it treats an unresolved `tkt-####`/`#NN`
  id — a fresh item, never a crash.
