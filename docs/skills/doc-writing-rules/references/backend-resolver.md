# The backend resolver — one seam, three options (ADR-0003)

`file-bug`, `file-feature`, and `file-task` each used to carry a hand-duplicated "Phase 0, decided once
per run" check (file backend vs. a ruled git-native backend). ADR-0003 replaces that binary with a
named three-way choice and one shared resolver every capture skill calls instead of re-deriving the
check itself — closing the duplication, not just extending it a third way.

## The three options

A repo rules exactly one, once, the same way ADR-0002 ruled git-native for this workspace — a
routing-table row in the entry file, never guessed at invocation time:

| Option | What it is | Where it's realized |
|---|---|---|
| **A — local** | Today's default: a `doc-type: ticket` file under `docs/tickets/` (make-doc's TICKET path) | Inline in each capture skill's own Record phase — unchanged from before this ADR |
| **B — git-native** | `gh issue` — the record lives as a GitHub Issue with the same section contract (ADR-0002's own ruled instance) | Inline in each capture skill's own Record phase — unchanged from before this ADR |
| **C — external** | A typed adapter interface (this file) realized via MCP or REST/GraphQL against a third-party tracker. **Linear ships as a concrete, scribe-authored Option-C adapter** (`references/linear-adapter.md`, this same skill); any other tracker (Jira, Notion, a custom system) is bring-your-own against the same interface | Linear: `references/linear-adapter.md`. Anything else: the workspace's own adapter, ruled in its entry file the same way |

No ruling, or the ruled option's tooling is unreachable (`gh` unavailable for Option B; the
configured adapter unreachable for Option C) → **Option A**, exactly as always — consumers of the
capture skills outside a ruled workspace see no change from before this ADR.

## The ruling shape

The entry file's routing-table row names the option and, for Option C, which adapter:

```
backend: A            # local (default — no row needed; this is what "no ruling" means)
backend: B            # git-native (gh issue) — ADR-0002's own instance
backend: C · adapter: linear · transport: mcp (fallback: graphql) · team: ENG
backend: C · adapter: <bring-your-own-name>    # a workspace's own adapter
```

Option C additionally persists whatever its adapter needs (Linear: an MCP connector reference or
API key, plus the target team/project — `linear-adapter.md`'s Configuration section) alongside this
row, captured once during repo configuration, never re-prompted per invocation, never guessed.

## The resolver's contract

Given a repo's entry file, the resolver returns exactly one of: **local**, **git-native**, or a
**named Option-C adapter** (`linear`, or a bring-your-own name) — plus, for Option C, whatever
adapter-specific configuration that option's row carries. A capture skill calls the resolver once
per run (Phase 0), then follows the returned option's own Record/Close realization — this file
documents the interface every adapter (including the two already inline in each skill) implicitly
satisfies; `linear-adapter.md` documents Linear's concrete realization of it.

## The seven-operation adapter interface (REQ-001, spec-linear-adapter; claim, ADR-0005)

Every backend — local, git-native, or an Option-C adapter — realizes the same seven operations, so
a capture skill's own call sequence never branches on which backend is active:

| Operation | What it does | Local (Option A) | Git-native (Option B) |
|---|---|---|---|
| **create** | Mint a new record carrying the full payload contract for its type/kind | Write a TICKET file, `doc_lint.py` clean | `gh issue create`, section contract is the skill's own gate |
| **dedup-search** | Sweep for an already-open match before minting | Search `docs/tickets/` for the item's nouns | `gh issue list --search` |
| **claim** (REQ-011, ADR-0005) | Take ownership of an already-existing record before starting execution work against it — write the caller's identity + an in-progress state + a dated claim comment (identity, timestamp, branch name), then **re-read to confirm the claim wasn't outraced**. A re-read showing an earlier-timestamped competing claim means this caller lost the race and abandons it. Distinct from `create` (which mints a new record) — `claim` only ever targets one that already exists | Set `claimed-by`/`claimed-at` in the record's frontmatter, then re-read the file | `gh issue edit --add-assignee <id>` + `gh issue comment` (identity, timestamp, branch), then re-read via `read` |
| **update** | Fold new detail into an existing record, or advance status | Edit the file's frontmatter/sections | `gh issue comment` / relabel |
| **close** | Close with a Findings-first guarantee — an empty Findings section takes the close-out line as its first entry | Frontmatter `status: done`/`wontfix`, Findings entry written first | `gh issue close` (+ `wontfix` label where applicable), Findings entry as a comment written first |
| **discover** | List records created or updated since a checkpoint — the primitive `spec-ticketing-watch-triage`'s watch loop calls; distinct from dedup-search (matches one candidate, not "everything since X") | `docs/tickets/` mtimes since checkpoint | `gh issue list --search "updated:>=<checkpoint>"` |
| **read** (REQ-010) | Resolve one already-known native id to its current record + full Findings/comment trail — what a resume-by-id branch, a post-dispatch Findings check, and `claim`'s own re-read step all need | Read the TICKET file directly | `gh issue view --comments` |

**`claim` has its first real caller (2026-08-12, teamwork's `dispatch-ticket` Phase 3 — issue
#183/#184).** ADR-0005 defined the primitive because `PARALLEL-AGENTS-PLAYBOOK.md` needs it and
nothing in this workspace prevented the near-duplicate-work incident that ADR documents, but named
no caller of its own — it does not require `file-bug`/`feature`/`issue` (capture-only, they never
execute a ticket) to call it. `dispatch-ticket`'s build path is the "discover an open ticket and
build it" role ADR-0005 anticipated: it takes `claim` (git-native: assignee + timestamped comment;
file: `claimed-by`/`claimed-at`) before any build effort starts, re-reads to confirm the race
wasn't lost, and releases it on a mid-flight abandonment — the shape this row already specified,
unchanged by adopting it.

Linear's realization of all seven lives in `references/linear-adapter.md`; a bring-your-own
Option-C adapter documents its own realization the same way, in its own workspace.

## Provenance tagging — user signal (idr-0008, adr-0021)

Option B (git-native) only — Option A has no filing-author concept to compare against, and
Option C is a named gap (its adapter's own `create`/`read` operations don't yet surface a
foreign-author field) rather than something built around. **Foreign-origin**, for this tagging
purpose, is operationalized as: the record's filing author's login (`gh issue view --json
author`) differs from the estate operator's own login, recorded at `.claude/ops/friendlies.json`'s
existing `policy.confirmed_by` field — the narrowest, zero-new-state proxy for idr-0008's Claim
("any trace from a party other than this estate's own seats"), deliberately not the full claim
(a future second trusted, non-operator collaborator is still foreign by that fuller reading —
out of scope for this proxy, `lld-0017`'s own Risk R-2).

Wherever a `create` or `read`(-resume) operation runs against the git-native backend and the
result is foreign by that check, apply the `user-signal` label if it is not already present:
`gh issue edit <id> --add-label user-signal`; if the label does not exist yet in the repo, `gh
label create user-signal --color 1D76DB --description "provenance: filed by a login other than
the estate operator (idr-0008, adr-0021)"` once, then retry the edit — the same missing-label
create-once fallback `file-task` already documents for its own kind label and `harness:watch-tickets`
applies for this very label (neither `file-bug` nor `file-feature` documents a missing-label path
of their own, so this convention owns the fallback uniformly rather than assuming those two
self-heal it), never worked around or silently skipped. A held item (ADR-0021's T3: an author outside
`friendlies.json`, held for a human decision rather than minted) was foreign at filing time by
construction — no login comparison is needed once it is later approved and minted; tag it
unconditionally at that mint.

`harness:watch-tickets` cannot preload this file across the plugin boundary (same limit its own
text already states for the payload contract one paragraph above this convention in that skill) —
it carries its own short restatement of this exact rule, citing `idr-0008`/`adr-0021` by id
rather than this file by path.

## Failure fallback (REQ-008)

If the resolved backend is Option C and any operation fails partway through (auth failure, API
error, MCP disconnect), the caller falls back to the file backend for **that one operation** and
reports the fallback in its close-out — the same discipline `file-task`'s own git-native-backend
fallback already documents (a partway `gh` failure falls back to file, notes the migration),
applied uniformly to any Option-C adapter. Never leave an item uncaptured because the preferred
store was unreachable.
