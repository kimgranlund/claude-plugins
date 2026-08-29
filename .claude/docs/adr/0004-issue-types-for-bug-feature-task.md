---
doc-type: adr
id: adr-0004
status: accepted
date: 2026-07-18
ratified: 2026-07-18 (maintainer, in-session AskUserQuestion — accepted as drafted: dual-write the
  native Issue Type alongside the existing kind: label, no dedup-search change, size/Issue Fields
  named a non-goal; implementation across the four consuming files follows as a separate change)
owner: kim.granlund
supersedes: null
intent-refs: idr-0002    # part of the same explicit chain idr-0002 names (native issue types on the git substrate)
---
# ADR-0004 — Adopt GitHub's native Issue Types alongside the existing kind: bug/feature/task labels

## Context

doc-authoring-standards' TICKET contract encodes `kind: bug`/`kind: feature`/`kind: task` as
frontmatter on the file backend (Option A), or as a GitHub **label** on the git-native backend
(Option B, ratified by ADR-0002/ADR-0003): `bug-report` applies `bug` + a severity label,
`feature` applies `feature` + `size:small`/`size:big`, `issue` applies `task` + the same size
scale, and the `ops-issues` agent mints against the identical convention (forge 1.34.4 closed a
gap where its own restatement of this contract had fallen behind the label mechanism the sibling
skills already use).

forge's `github-issue-pr-primitives` knowledge pack researched the platform fact behind this and
deliberately declined to rule on it (`references/bug-task-feature-mapping-nuances.md`, Finding 1):
GitHub's native **Issue Types** reached GA 2025-04-09 — over a year old, not a beta feature to
hedge against — and ships exactly three default types, **Task, Bug, Feature**, the identical three
shapes this workspace already names. Unlike a label, a type is organization-scoped, validated,
exactly one per issue, and queryable with dedicated syntax (`type:"Bug"`) with full REST API CRUD
since 2025-03-18. The taxonomy already matches exactly; only the *mechanism* diverges — this
workspace currently encodes it in the weaker of the two primitives GitHub offers for precisely
this question.

The same finding's Finding 2 flags a related-but-separate question — migrating `size:
small`/`size:big` to the newer **Issue Fields** feature (GA only 15 days before that pack's
research date) — as immature and directional, explicitly NOT a mature migration target yet. This
ADR does not decide that question; it stays a label, and Issue Fields is named here only as a
future follow-on once it has more runway.

This decision does not reopen ADR-0002 (git-native execution) or ADR-0003 (the three-way backend
choice) — both stand; this ADR only asks whether the *classification mechanism* on the
already-ratified git-native backend should change.

## Decision

**We will dual-write: every new git-native issue carries BOTH the existing `kind` label AND the
matching native Issue Type, starting immediately — we will NOT remove the label or migrate dedup
search in this change.**

1. `bug-report`, `feature`, `issue`, and `ops-issues` set the native Issue Type (`Bug` / `Feature`
   / `Task`) at `gh issue create` time, in addition to the label each already applies — same
   payload contract, one more field, additive rather than a rewrite.
2. `size:small`/`size:big` stays a label; Issue Fields migration is an explicit non-goal here (see
   Context) — revisit only once that feature has more runway.
3. Dedup search (`gh issue list --search`) is unchanged for this decision — it is already a
   free-text sweep, not a label-filtered query, so nothing breaks by leaving it as-is; a follow-up
   may tighten it to `type:` filtering once Issue Types have run in production for a while.
4. The label stays as the fallback of record: if a repo's org has renamed, disabled, or exhausted
   its Issue Type schema (types are org-admin-controlled, not guaranteed present or named exactly
   `Bug`/`Feature`/`Task` in every org), the create call still succeeds on the label alone and
   reports the Issue Type as skipped — never blocks or fails a mint over a missing type.

**Alternative considered — full migration now (Issue Type replaces the label entirely):**
rejected for this change. Two facts this ADR could not verify going in — whether `gh issue
create` exposes a `--type` flag directly or requires a raw `gh api`/GraphQL call, and whether
every consumer that greps or searches on `label:bug`-style text elsewhere in this workspace would
need updating — are exactly the kind of unverified platform-API claim this session's own governing
incident (two such claims already turned out wrong once this week, per
`bug-task-feature-mapping-nuances.md` Finding 4) says to check before committing to, not after.
Dual-write captures the taxonomy benefit now while that verification happens in the open, in
production, at zero switching cost.

**Alternative considered — keep labels only, do nothing:** rejected; the taxonomy already matches
GitHub's own native types exactly (same three names), so the platform-native, stronger-querying
mechanism is a close enough fit that not adopting it at least additively leaves a real capability
on the table for free (no known cost).

## Consequences

- `doc-authoring-standards`' TICKET contract gains a line: on Option B, `kind:` also sets the
  matching native Issue Type at create time, label unchanged.
- `bug-report`, `feature`, `issue` (scribe), and `ops-issues` (forge) each need their Phase-4 /
  mint-step "labels `X`" line to become "labels `X` + sets Issue Type `X'` (fallback: label only if
  the org's type schema doesn't resolve)" — four files, one line each, same shape.
- **Open verification items, before or during that implementation work** (name them here rather
  than discover them mid-build, per this ADR's own reasoning above):
  - Does `gh issue create` support a `--type` flag directly, or does setting Issue Type require
    `gh api graphql`/REST instead of the simple CLI path the label call already uses?
  - Does this workspace's GitHub org actually have the three default Issue Types present and
    named `Bug`/`Feature`/`Task` (unrenamed, undisabled) — verify once, record the answer, don't
    assume the GA default survived org configuration.
- Nothing about dedup search, existing open issues (no backfill of Issue Type onto already-filed
  issues), or `size:`/Issue Fields is touched by this change — all named non-goals, explicitly
  out of scope, revisit separately if ever.
- Reversible at zero cost: dropping the Issue Type write-side is a one-line revert per file: the
  label remains the system of record until a future ADR says otherwise.
