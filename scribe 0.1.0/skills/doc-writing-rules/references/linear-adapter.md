# The Linear adapter — docs' shipped Option-C realization (spec-linear-adapter)

Realizes `backend-resolver.md`'s seven-operation interface against Linear specifically. Grounded
2026-07-18 (claim: 2026-07-19, ADR-0005) against Linear's own developer docs and changelog — the
facts below carry the standard
grounding-marker classes (`pack-authoring-standards`): `[verified]` (checked directly against a
first-party Linear doc page), `[drift-prone]` (verified but likely to move — re-check before
trusting past this quarter), and `[inferred]` (standard GraphQL/Relay convention, not itself
fetched from a Linear page — confirm via live introspection before depending on the exact field
name).

## Transport resolution (REQ-002)

Resolved at call time, never hardcoded:

1. **MCP preferred** — `[verified]` Linear ships an official, remote MCP server at
   `https://mcp.linear.app/mcp` (Streamable HTTP; the older `/sse` endpoint is deprecated), using
   OAuth 2.1 with dynamic client registration — the first connection opens a browser window to
   sign in and authorize, then reuses the credentials. Claude Code is named as a directly
   compatible MCP client. When the workspace has this connector attached, every operation below
   routes through the connected MCP tools.
2. **GraphQL fallback** — `[verified]` Linear has no REST surface; when no MCP connection is
   available, the adapter calls Linear's GraphQL API directly at `https://api.linear.app/graphql`,
   authenticating with header `Authorization: <API_KEY>` (the raw key — no `Bearer` prefix, per
   Linear's own documented convention) using the workspace-supplied key from Configuration below.

The caller code path is identical either way (AC-002) — only which transport actually executes the
operation differs.

## Configuration (REQ-003)

Captured once during repo configuration, persisted alongside the entry-file's `backend: C ·
adapter: linear` row (`backend-resolver.md`), never re-prompted per invocation:

- **Transport credential** — an MCP connector reference (nothing to store beyond "MCP is
  connected"; OAuth tokens live in the MCP client, not this repo) OR a Linear API key for the
  GraphQL fallback path.
- **Target scope** — the Linear team (and, optionally, project) records are created/searched
  against, e.g. `team: ENG`.
- **Status-type → state-id map** (REQ-007, below) — resolved once per team and cached in the
  ruling, not re-queried on every operation; re-resolve if the adapter starts getting `stateId`
  errors (a sign the team's workflow states were reconfigured).

## The seven operations

- **create** — `[verified]` the `issueCreate` mutation, input at minimum `title`, `description`,
  `teamId`; response `{ success, issue { id, title } }`. `title` = the record's Summary line;
  `description` = the rest of the payload contract rendered as markdown (Acceptance · Links ·
  kind-specific sections · an empty Findings heading) — REQ-004's full mapping, below. `[inferred]`
  label assignment (`kind: bug`/`kind: feature`, severity, size) likely takes a `labelIds` array on
  the same mutation or a separate label-attach step — confirm the exact field via live
  introspection before the first real create call; do not hardcode a guessed field name into a
  script that ships unverified.
- **dedup-search** — `[inferred]` the `issues` query with a `filter` argument (team + a text/title
  match), standard Relay-style GraphQL — exact filter input shape not independently confirmed by
  this pack; introspect (`__type(name: "IssueFilter")`) or consult
  `https://linear.app/developers/graphql` at call time rather than trusting a memorized shape.
  Sweep before minting, same discipline as the local/git-native adapters (REQ-005): a match updates
  that issue's fields instead of minting a duplicate.
- **claim** (REQ-011, ADR-0005) — `[inferred]` the `issueUpdate` mutation, input `id` plus
  `assigneeId` (the caller's own Linear user id) plus `stateId` set to the team's configured
  `started`-type state (REQ-007's cached map) — the same mutation `update` uses, since Linear has
  no separate "claim" or "assign" mutation; claiming a ticket and starting it are the same
  `started`-type transition. `assigneeId` is not independently confirmed against a first-party
  schema page in this research pass — introspect (`__type(name: "IssueUpdateInput")`) before the
  first real call. Immediately followed by a comment recording the caller's identity, a timestamp,
  and the branch it is about to create (the same `issueCommentCreate`-shaped call `update` already
  uses for a Findings entry), then a **read** (REQ-010, below) to confirm the claim landed and
  wasn't outraced by a different identity's earlier-timestamped claim comment on the same issue —
  Linear's GraphQL API gives no atomic check-then-set here, so the write-then-re-read discipline is
  the adapter's only race guard, identical in shape to the git-native realization.
- **update** — `[verified]` the `issueUpdate` mutation, input `id` plus whatever changed (e.g.
  `stateId`, or a comment create for a Findings entry — Linear separates issue-field updates from
  comments; a dated Findings entry is a **comment**, not a description edit, mirroring how the
  git-native adapter appends `gh issue comment` rather than rewriting the issue body); response
  `{ success, issue { id, title, state { id, name } } }`.
- **close** — realized as **update** setting `stateId` to the team's configured `done` or
  `wontfix`-mapped state (REQ-007) — Linear has no separate "close" mutation; closing IS a state
  transition. Findings-first (REQ-006): the dated Findings comment is posted **before** the state
  transition lands, so a close never completes with an empty Findings trail, identical to the
  local/git-native ordering.
- **discover** — `[inferred]` the `issues` query filtered by team and `updatedAt` past the given
  checkpoint, paginated via the standard GraphQL cursor pattern (`first`, `after`,
  `pageInfo { hasNextPage, endCursor }`) — not independently confirmed against a first-party page
  in this research pass; introspect before the first real call. Returns every issue created or
  updated since the checkpoint, plus a new checkpoint (the last page's `endCursor`, or the latest
  `updatedAt` seen) to persist for next time — the shape `spec-ticketing-watch-triage` REQ-003's
  watch loop consumes.
- **read** (REQ-010) — `[inferred]` the `issue(id: ...)` query (Linear's single-item lookup,
  distinct from the `issues` list query `dedup-search`/`discover` use), requesting the issue's
  fields plus its `comments` connection — response shape `{ id, title, description, state { id,
  name }, comments { nodes { body, createdAt } } }`; not independently confirmed against a
  first-party page in this research pass, introspect (`__type(name: "Issue")`) before the first
  real call. An id with no matching issue on the configured team returns `null`/an empty result,
  not an error — the caller (a capture skill's resume-by-id branch) treats that identically to an
  unresolved `tkt-####`/`#NN` id: a fresh item, never a crash (AC-010). This is the operation
  Phase 1's resume-by-id branch and Phase 6's post-dispatch Findings check both call under Option
  C, mirroring the local adapter's plain file read and the git-native adapter's `gh issue view
  --comments`.

## Payload-contract mapping (REQ-004)

The contract is backend-invariant; only its storage shape differs:

| Contract element | Linear field |
|---|---|
| Summary | `title` |
| Acceptance, Links, kind-specific sections (Repro/Expected-vs-actual/Classification/Severity for `kind: bug`; Scope/Open for `kind: feature`) | rendered as markdown inside `description`, same `##` heading shape as the git-native adapter's issue body |
| `kind: bug`/`kind: feature`, Severity, Size | Linear labels |
| Findings (dated entries) | comments, one per dated entry — never folded into `description`, matching the "append-only, never rewritten" discipline the other two backends already apply |

No section is dropped or silently merged into another (REQ-004) — a `kind: bug` fixture round-trips
Repro/Expected-vs-actual/Classification/Severity; a `kind: feature` fixture round-trips Scope/Open;
both alongside Summary/Acceptance/Links/Findings (AC-004).

## Status mapping (REQ-007)

`[drift-prone, verified against two first-party sources that disagree on the tail of the list]`
Linear groups a team's own named states into a fixed set of underlying **types**; state *names* are
per-team and configurable (e.g. "In Progress", "In Review", and "Ready to Merge" can all be
distinct named states of type `started`), so the mapping below binds each shared-vocabulary status
to a state **type**, then to that team's specific state of that type — never to a hardcoded name:

| Shared status | Linear state type(s) |
|---|---|
| `open` | `triage` (only on teams with Triage enabled — an opt-in per-team feature, off by default), `backlog`, `unstarted` |
| `doing` | `started` |
| `done` | `completed` |
| `wontfix` | `canceled` |

Two first-party Linear doc pages disagree on the exact tail of the type enumeration: one lists
`triage/backlog/unstarted/started/completed/canceled` (six, with triage); another lists
`backlog/unstarted/started/completed/canceled/duplicate` (six, with duplicate, no triage) —
`triage` is confirmed genuinely distinct but **opt-in per team** (`Team Settings → Triage`, off by
default); `duplicate` was not independently confirmed as a true fourth+ `type` value versus simply
a *named state* living under the `canceled` type (Linear's own worked example lists "Canceled,
Could not reproduce, Won't Fix" as three named states all of type `canceled`, which is exactly the
shape a "Duplicate" named state under `canceled` would take). **Resolve this by querying the
team's actual `workflowState.type` values at Configuration time (REQ-003), never by trusting this
table's enumeration as exhaustive** — the mapping above is the best-available grounding for the
four shared statuses this adapter needs to write; it is not a claim that Linear has exactly four,
five, six, or seven total types.

Writing a status (`open`/`doing`/`done`/`wontfix`) always sets the exact configured state for that
type (REQ-003's cached map). Reading a Linear issue back that sits in a state the adapter never
itself wrote (a human moved it manually — e.g. to a custom "Blocked" state of type `started`)
reports the shared vocabulary's nearest covering status by state **type** — `started` → `doing`,
`completed` → `done`, `canceled` → `wontfix`, anything else (`triage`/`backlog`/`unstarted`) →
`open` — a best-effort type-level classification (AC-007), never a claim of exact reversibility for
states the adapter didn't itself set, and never a fifth status value.

## Failure fallback (REQ-008)

Realizes `backend-resolver.md`'s shared fallback rule: an auth failure, API error, or MCP
disconnect mid-operation falls back to the file backend for that one operation, reporting the
fallback in the close-out — never a silent failure or an unhandled exception (AC-008).

## Provenance

Endpoint, MCP server URL/transport, `issueCreate`/`issueUpdate` mutation shapes, and the
opt-in-per-team nature of Triage: verified against `linear.app/developers/graphql`,
`linear.app/docs/mcp`, `linear.app/docs/triage`, and `linear.app/docs/configuring-workflows`,
2026-07-18. Filter/pagination/label field names, and the single-item `issue(id: ...)` read query
(REQ-010, added 2026-07-18 in this SPEC's v0.2.0 amendment): inferred from standard GraphQL/Relay
convention, not independently fetched from a Linear schema page in this research pass — verify via
live introspection (`__type(name: "IssueFilter")`, `__type(name: "WorkflowState")`, `__type(name:
"Issue")`) before the first real call in any implementation, not assumed from this file alone.
`claim`'s `assigneeId` field (REQ-011, added 2026-07-19 in this SPEC's v0.3.0 amendment, ADR-0005):
inferred from the same standard `issueUpdate` mutation shape already verified for status/comment
writes — not itself confirmed against a schema page; introspect (`__type(name:
"IssueUpdateInput")`) before the first real claim call.
