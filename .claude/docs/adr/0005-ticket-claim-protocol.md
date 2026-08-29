---
doc-type: adr
id: adr-0005
status: accepted
date: 2026-07-19
ratified: 2026-07-19 (maintainer, in-session AskUserQuestion — three of four proposed items selected: add the claim operation, cross-reference concurrency-design, add ops-repo stale-claim detection; the fourth option, ADR-only with no implementation, was not chosen)
owner: kim.granlund
supersedes: null
intent-refs: idr-0002    # part of the same explicit chain idr-0002 names (the claim protocol against duplicate agent work)
---
# ADR-0005 — A `claim` backend operation: preventing duplicate work between independent agents before a git-tree collision exists

## Context

`PARALLEL-AGENTS-PLAYBOOK.md` (merged same-day) documents how to run independent coding agents —
no shared session, no message channel — against one repo, coordinating only through a ticket
backend and git history. Its central mechanism is a claim: an agent writes its identity onto a
ticket before starting work, then re-reads to confirm the claim wasn't outraced.

This workspace had no such mechanism when the playbook shipped, and the gap was not
hypothetical: within the hour, a background session started auditing toward Issue #44 with no
claim-check step at all, and only discovered — by incidental inspection of `git worktree list`,
not by any systematic check — that a separate, parallel session had already completed and was
mid-flight opening a PR for the identical work (PR #53). Nothing in this workspace would have
stopped a second independent agent from duplicating that work outright had the collision not
happened to surface early.

ADR-0003 already generalizes work-item backends behind a shared resolver with six operations
(`create · dedup-search · update · close · discover · read`, `references/backend-resolver.md`,
realized for local/git-native/Linear). None of the six is "take ownership of an existing record
before starting execution work against it" — the resolver lets an agent file or read a ticket, not
claim one.

`concurrency-design` (orchestration) already owns collision response once a git-tree collision
exists or is imminent (its three-actor-type classification, its verify-independently-then-escalate
protocol). It does not, and was never scoped to, prevent two agents from starting the *same
ticket* before either has touched a file — that is a ticket-layer problem, one level above the
git-tree layer it operates on.

## Decision

1. **Add `claim` as a seventh backend operation**, alongside the six ADR-0003 already ratified.
   Shape: the caller writes its own identity as the record's owner/assignee, moves it to an
   in-progress state, and posts a claim comment carrying its identity, a timestamp, and the branch
   name it is about to create — then **re-reads the record before proceeding**. A re-read that
   shows an earlier-timestamped claim from a different identity (tie-break: lower identity string
   wins on an exact tie) means this caller lost the race; it abandons the claim and selects a
   different record. A wasted read is the cost of losing; a duplicate PR is the cost of not
   checking at all.
2. **Staleness.** A claim with no linked open PR and no update past a repo-configured window is
   reclaimable by a later `discover` pass. Reclaiming requires posting a comment stating the
   reclaim; the previous claimant's branch or commits, if any exist, are not touched — only the
   claim's exclusivity is superseded. The window itself is a per-repo ruling (recorded alongside
   the backend choice, the same way ADR-0003's own ruling is recorded), not a platform-wide
   constant.
3. **Each backend realizes `claim` natively:** git-native — an assignee edit plus a comment
   (`references/backend-resolver.md`); Linear — assignee plus a workflow-state transition plus a
   comment (`references/linear-adapter.md`, `spec-linear-adapter.md` REQ-011); local/file — a
   `claimed-by`/`claimed-at` frontmatter pair, since a plain file has no native assignee concept.
4. **Scope boundary: this ADR defines the primitive, it does not mandate a caller.**
   `bug-report`/`feature`/`issue` capture and file tickets; they do not execute them, so nothing
   requires them to call `claim`. Adoption by whatever eventually plays the "discover an open
   ticket and build it" role (today, at most, a human-launched session following the playbook
   manually; no autonomous executor agent exists in this workspace) is a separate, later decision.
5. **`concurrency-design` (orchestration) gets a boundary cross-reference, not a rewrite.** Its
   existing collision-response scope (three actor types, verify-independently, escalate-by-type)
   is unchanged; it gains one pointer distinguishing what it already does (react to a git-tree
   collision) from what `claim` does (prevent a ticket-level collision earlier, before either
   agent has touched a file).
6. **`ops-repo` (forge) gains a read-only, propose-only stale-claim check**, added to its existing
   worktree/branch/PR inventory — flagging, never reclaiming, a claim past the staleness window
   with no linked PR. This is the same "propose only, mutate only through a gated script" contract
   ops-repo already applies to every other finding it can't independently verify as safe to act on.

**Alternative considered — rely solely on `concurrency-design`'s existing git-tree collision
response, add nothing at the ticket layer:** rejected. That response is reactive: it verifies and
escalates *after* a collision has already produced a diff or an imminent mutation. It could not
have caught the Issue #44/PR #53 case any earlier than it actually surfaced, because no file
collision had happened yet — both agents had done complete, non-overlapping work. Only a
ticket-layer check, run before either agent starts, prevents the duplication itself rather than
discovering it after the fact.

**Alternative considered — hardcode one global staleness window in this ADR:** rejected, for the
same reason ADR-0003 records the backend choice per repo rather than picking one for every
workspace — what counts as "stale" depends on how fast a given repo's agents typically turn work
around; a platform-portable primitive should not embed one repo's operational tempo.

**Alternative considered — require every capture skill to call `claim` immediately:** rejected.
`bug-report`, `feature`, and `issue` are capture-only; they mint or update a record, they never
start execution work against one. Forcing a claim call into a filing-only flow would conflate two
responsibilities ADR-0003 already deliberately separated (the resolver vs. whatever eventually
executes a ticket), for no present caller that needs it.

## Consequences

- `references/backend-resolver.md` gains a seventh operation row; `references/linear-adapter.md`
  gains Linear's realization; `spec-linear-adapter.md` is amended to v0.3.0 (REQ-011/AC-011) — the
  first amendment to that SPEC since REQ-010/AC-010 (read) landed in v0.2.0.
- The local/file backend gains its first claim-shaped state (`claimed-by`/`claimed-at`
  frontmatter) — a new convention with no prior precedent in this workspace's TICKET contract,
  since nothing on the file backend previously needed to express "someone is working on this."
- `concurrency-design`'s own scope, actor classification, and worked example are unchanged — the
  addition is one cross-reference, not a redesign; no description edit, so no eval-run obligation
  follows from this ADR for that skill.
- `ops-repo`'s narrow-execution contract (propose only, mutate only through
  `campaign_close.py`/`sync_main.py`) is unchanged in kind — stale-claim is a new finding
  *category*, reported exactly like every other finding it cannot independently verify safe to
  act on. Its description gains one clause naming the new capability; this workspace's agents
  carry no `evals.json` (verified: none exists under any agent path in forge or orchestration), so
  no eval-run follows from this change.
- No existing skill's behavior changes as a direct, immediate result of this ADR —
  `bug-report`/`feature`/`issue`/`ops-issues` are untouched. The primitive exists for a future
  caller to adopt; closing that adoption gap (an actual ticket-executing agent) is explicitly
  out of scope here and left as an open question for whoever designs that agent next.
