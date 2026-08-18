# `in-flight` label semantics — Phase 3's full rationale (#199)

Cited from `dispatch-ticket/SKILL.md`'s Phase 3 "Once the claim wins, make it LIST-VISIBLE too"
bullet rather than restated inline (the same F6 split-to-references pattern as
`de-stale-premise-check.md`, `spec-lock-gate.md`, and `worktree-teardown.md`).

The claim comment is durable but invisible in the LIST view (Kim: "I cannot tell that Issues are
claimed"). Git-native only: `gh issue edit --add-label in-flight`. `in-flight` shares hex
`FBCA04` with `doing` by coincidence, not relation — a shared color is never evidence two labels
mean the same; a repo without `in-flight` creates it with that name and a distinct hex. Additive
to the assignee+comment claim (assignee stays required per ADR-0005) — the label only supplies
list-visibility.

**`in-flight` is the ONE canonical claim label — never mint a synonym.** `doing` is a DIFFERENT,
load-bearing label — the `open`→`doing`→`done` status verb, unrelated to claiming; #192 shows the
confusion: `doing` applied alongside `in-flight` mid-claim looked like a duplicate but wasn't. The
two coexist ("is this claimed" vs. "what lifecycle stage") — `doing` is never deleted or reused as
a claim signal.

**Label = display, comment = record.** `in-flight` is hand-editable and never the correctness gate
alone: `mobilize-chores` step 2 may read it as a cheap pre-filter, but the claim comment — plus,
once a PR exists, that step's own GraphQL PR-linkage check — stays authoritative.

**Removed on every terminal outcome:** Phase 5 stage 2 removes it the moment a PR opens (the open
PR becomes the visible signal instead — named explicitly in a task/big-feature dispatch's sealed
prompt, since the seat opening the PR never loaded this file); the Release-on-abandonment bullet
removes it on a mid-flight abandon and on Phase 6's recorded-loss ending (as dead as an
abandonment). A task SKIPPED in Phase 2 never reaches this bullet, so owes no removal. A
coordinator running a serial chain (`mobilize-chores`) may also carry the pre-existing `queued`
label (`C5DEF5`) for chain position ahead of its own claim — nothing here touches its lifecycle.
