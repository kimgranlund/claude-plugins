# Mapping Bug/Task/Feature onto Issues/PRs — synthesis, and where this workspace's own convention stands

This axis is different from the other six: it doesn't introduce new platform facts, it connects
them to this workspace's own ADR-0002 (git-native execution) and doc-authoring-standards' TICKET
contract, cited by ID rather than restated. **This pack answers what the platform supports — it
does not amend ADR-0002 or doc-authoring-standards.** Any divergence noted below is a finding for
a future decision, not a ruling made here.

## The routing funnel, GitHub's shape

Per `issue-vs-pr-vs-discussion.md`: an unscoped idea → Discussion; a scoped, actionable item →
Issue; a code change resolving an Issue → PR, linked back via `linking-and-closing-keywords.md`'s
keyword contract. This workspace's `issue` skill's own Phase 2 ("A defect... stop and point:
`/bug-report`. A feature idea... `/feature`. Neither — capture here as `task`") is a **finer-grained
version of the same funnel**, one level *inside* "this is Issue-shaped work" — it doesn't conflict
with GitHub's Discussion/Issue/PR split, it operates entirely within the Issue side of it.

## Finding 1 — `kind: bug`/`kind: feature` is a label; GitHub has shipped a native alternative

doc-authoring-standards' TICKET contract encodes `kind: bug`/`kind: feature` **as a label** on the
git-native (Option B) backend. Per `issue-types-and-labels.md`: GitHub's native **Issue Types**
reached GA 2025-04-09, ships **exactly three default types — Task, Bug, Feature** — the same three
shapes this workspace already names, and is org-wide, validated, and REST/GraphQL-queryable in a
way a label is not (`type:"Bug"` vs. `label:bug`, with no cross-repo consistency guarantee for the
latter).

**Alignment:** the *taxonomy* already matches exactly (bug/feature/task, three shapes, same
names). **Divergence:** the *mechanism* doesn't — this workspace encodes the taxonomy in the
weaker of the two primitives GitHub offers for exactly this purpose, on a platform where the
stronger one has been GA for over a year. This is not this pack's call to make; it's the specific,
citable fact a future ADR revision would need.

## Finding 2 — `size: small`/`size: big` is also a label; Issue Fields is an even newer typed alternative

The `feature` skill's `size: small`/`size: big` label has the same shape as Finding 1, but the
platform-native alternative is newer and less proven: **Issue Fields** (GA 2026-07-02, per
`issue-types-and-labels.md`) adds typed, per-Issue-Type-pinned metadata fields — a custom
single-select field mapped to an issue's Type could carry `size` the same way Priority/Effort ship
by default. [drift-prone] This feature is 15 days old at this pack's research date; treat this
finding as directional, not yet a mature migration target the way Finding 1 is.

## Finding 3 — Scope/Open's listed follow-ons are a sub-issues candidate, not just prose

A TICKET's Scope/Open section (feature-shaped tickets) names gaps as prose. Per
`sub-issues-and-task-lists.md`: GitHub's sub-issues (GA 2025-04-09) formalizes exactly this —
each named gap becomes its own Issue, hierarchically linked, individually dedup-able and
closeable, with native progress rollup — instead of a flat list inside one Issue's body that never
gets its own status. The now-retired tasklist-block feature (discontinued 2025-04-30) was the
transitional mechanism; plain Markdown checkboxes still work but carry none of the hierarchy or
rollup benefit.

## Finding 4 — ADR-0002's PR-as-merge-gate assumption has one unverified precondition

ADR-0002 rules PRs as the merge gate and (implicitly, via the git-native backend) relies on
merging a PR to close its linked work item. Per `linking-and-closing-keywords.md`: this behavior
is a **repository-level toggle**, on by default, but disable-able — and the exact behavior across
all three merge strategies (`pr-lifecycle-and-review.md`) is [inferred, not verified] rather than
directly confirmed by GitHub's docs. This is an operational check (confirm the toggle, confirm the
house merge strategy doesn't strip the keyword), not a design flaw — but it's a check, not an
assumption, per this session's own governing incident (two unverified platform-API facts already
turned out wrong once this week).

## Finding 5 — Projects v2 is not a competing backend, so ADR-0003's choice is unaffected

Per `projects-v2.md`: a Project wraps an Issue/PR/draft-stub, it never stores a work item on its
own. **No divergence here** — ADR-0003's three-way backend choice (local / git-native /
external-with-Linear-shipped) stays exactly as ratified; a git-native (Option B) repo could
optionally layer Projects v2 on top of its Issues without changing which system of record holds
the work item. The one fact worth carrying forward if that layering ever happens: Projects v2 is
GraphQL-only, so any tooling that writes Project fields needs a GraphQL path the REST-based
git-native adapter doesn't currently have.

## What this axis is NOT saying

Not "switch to Issue Types," not "adopt Issue Fields," not "restructure Scope/Open as sub-issues."
Each Finding states the platform fact and the specific divergence point; whether and how to act on
any of them is a decision for an ADR, made with this pack cited as the grounding — the same
separation this workspace already draws between decompose/decide (ADR) and describe (a knowledge
pack that answers).
