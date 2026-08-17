# Unstick ordering — classifying and sequencing a `Blocked-by:` chain (issue #558)

Step 2's existing `Blocked-by:` exclusion (#193) stops at "any named blocker still open excludes
the candidate this run." This file is the small, buildable-prose algorithm that replaces the bare
skip with dependency-first ordering: which blocker shapes are safely auto-resolvable (mobilize the
blocker), which stay report-only, and how a multi-level chain gets walked, ordered, and — within
one run's own bound — chained. It carries ONLY the mobilization-side classification/ordering
logic; the `Blocked-by:` line's own format and per-backend read mechanics stay
`references/blocked-by-convention.md`'s ONE canonical definition, cited below rather than
restated (that file's own charter: "neither's own read/exclude/order logic is restated here").
harness's `chore-planner` (via its `blocked-by-rules` skill) is the sibling consumer with its own
ordering doctrine over the same convention — a cross-plugin mention only, never a shared
implementation; this file's algorithm is mobilize-chores' own, not a fork of that one.

## C1 — Blocker classification (fail-closed, first match wins)

For each candidate ticket A that step 2's `Blocked-by:` exclusion catches, resolve each named
blocker id B per `blocked-by-convention.md`'s realization table, then classify B into exactly one
class, evaluated top-down:

| # | Class | Predicate (git-native realization) | Disposition |
|---|---|---|---|
| B0 | CLOSED | `gh issue view <B> --json state` reads CLOSED | Not blocking — unchanged existing behavior; all-closed → A proceeds through step 2 normally |
| B1 | UNRESOLVABLE | The id fails to resolve (deleted, typo, cross-repo ref, `gh` error) | Treated OPEN, report-only — the existing fail-closed branch, unchanged. A → still-stuck |
| B2 | CYCLE / TOO-DEEP | B is already on the current resolution path, or chain depth from the original candidate exceeds 5 | Report-only; name every member of the cycle (or the too-deep chain) in one paragraph. Nothing on a cycle is ever dispatched. A → still-stuck |
| B3 | IN-FLIGHT | B has an open PR (the GraphQL `closedByPullRequestsReferences` check — never the flattened form) OR a non-empty `assignees`/`claimed-by` (#184) | Someone owns it — A → sequenced-for-next-run; B reported as the awaited work. No dispatch, no check-in comment |
| B4 | HUMAN-SHAPE | B is unlabeled, ambiguously labeled (not exactly one of feature/bug/task), sweep-flagged human-decision/blocker, an ops/hygiene item, or matches any of step 6's five blocker shapes | Report-only, step 6's existing classified-paragraph discipline. A → still-stuck |
| B5 | MOBILIZABLE | B passes step 2's FULL existing mobilizable predicate (exactly one of feature/bug/task, no active claim, no open PR, not sweep-excluded) AND B's own `Blocked-by:` line is absent, all-closed, or resolvable within this same walk (depth ≤ 5, no cycle) | Unstick candidate — dispatch B (subject to the one confirm round); A → sequenced, conditionally dispatchable per the wave loop below |

Two invariants:

- **The mobilizable predicate is reused, never forked or relaxed.** B5 cites step 2's own checks
  verbatim — a blocker earns zero exemptions from the label, claim, PR, or sweep-judgment gates.
- **Only one verb exists.** The unstick action set is exactly `{dispatch to build-lead}`. Never
  granted: editing or removing a `Blocked-by:` line, relabeling a ticket into mobilizability,
  reclaiming a stale claim, or posting a ratification/sign-off comment — each stays whatever it
  already was (a human act, or `repo-cleaner`'s own ruled territory).

## C2 — Chain walk, ordering, waves, and outcome classes

- **Walk**: depth-first from each `Blocked-by:`-excluded candidate, resolving each blocker per C1
  above, carrying a path-visited set for cycle detection and a depth counter capped at 5. Memoize
  every resolved id in a per-run, in-memory cache — an id is read once per run, never re-fetched
  (the same batching discipline `blocked-by-rules` already applies on its own side).
- **Order**: dependency-first — a B5 blocker dispatches before (or without) its dependents; among
  unrelated chains, ordering falls back to step 5's existing serial/parallel target-overlap rules,
  unchanged. This is a topological order over the resolved chain fragments; a cycle (B2) is
  removed whole and never enters the order.
- **Waves (the within-run chaining bound)**: after all of a wave's dispatches RETURN, one
  read-only re-check pass over the sequenced dependents — re-read each named blocker's state once.
  All-CLOSED → dispatchable in the next wave (already confirmed conditionally in step 4). Max 3
  waves total; a pass that unlocks nothing ends the loop immediately. Never sleep, never watch a
  PR (`gh pr checks --watch` or equivalent), never re-poll an id already re-read this pass. On the
  default PR-opened ceiling nothing closes in-run except via an ADR-0012 quick-build merge, so the
  recheck ordinarily finds nothing and the loop ends after wave 1 — next-run-only behavior by
  construction, not a separate mode.
- **Outcome classes for step 6**: `unstuck-this-run` (a dependent actually dispatched in wave ≥ 2,
  or a blocker whose own dispatch and dependent's dispatch both landed this run); `sequenced-for-
  next-run` (a blocker dispatched or in-flight; the dependent waits on its close); `still-stuck-
  and-why` (B1, B2, or B4 — carrying step 6's existing classified paragraph).

```
wave = 1; confirmed = plain mobilizable set + unstick blockers (topo order)
repeat:
  dispatch confirmed per step 5 (serial/parallel rules); collect ALL returns
  recheck: for each sequenced dependent, re-read each named blocker's state ONCE
  newly-unblocked (all CLOSED) -> confirmed for wave+1
  stop when: nothing newly unblocked, or wave == 3
remaining sequenced dependents -> sequenced-for-next-run (step 6)
```

## Non-goals

No graph tooling, no visualization, no persistence across runs (the cache is in-run memory only),
no new authority beyond the one dispatch verb already named. `blocked-by-convention.md`'s format
and non-goals are untouched by this file.
