# FLOOR audit — docs:file-leftovers

Auditor: skill-checker seat (fresh context) · 2026-07-30 · against harness:skill-writing-rules
Scope: SKILL.md, intent.md, evals/evals.json, plus the cross-plugin seam edits in this worktree.
Mechanics: `skill_lint.py` clean · `eval_check.py` clean.

**Verdict: ship-ready at FLOOR. No blocking findings.** The three focus questions all pass;
three minor items are owed before or at ship.

## Focus answers

**(a) Substrate restatement — clean.** Phase 4 points instead of copying: backend resolution,
dedup, and the TICKET payload contract are named as sibling-owned, and raw `gh issue create` /
hand-written ticket files are banned. Phase 1's "already recorded" pre-search is a legitimate
table pre-filter, and it explicitly subordinates itself ("the sibling's own dedup at mint time
stays the authoritative gate"). No drift pair created.

**(b) Host-context-only sweep — stated where it binds.** The constraint sits in the identity
paragraph (SKILL.md line 20–21): "The sweep runs in THIS context — a subagent or fork cannot
see the conversation, so the sweep is never dispatched." That is the compaction-surviving head
and the exact point where a future editor would be tempted to "optimize" the sweep into a
dispatch. The P0 ruling in intent.md (2026-07-30) records the why. No further placement needed.

**(c) find-open-questions seam — crisp, and reciprocal.** One criterion — needs a ticket vs
needs only a decision — appears identically in this skill's description fence, in Phase 3
("decision-shaped leftovers that need resolving but no ticket route to find-open-questions"),
in FOQ's updated description ("NOT sweeping the session's dropped work into tickets (docs'
file-leftovers)"), and in reciprocal eval cases on both sides (this suite's n01; FOQ's new
sweep-prompt no-trigger cases). The three file-* siblings also gained reciprocal no-trigger
cases in the same change. The seam is closed in both directions.

## Findings

### Minor

1. **Phase 1 presumes a backend this skill never resolves** (SKILL.md:30–32). "one light
   search of the resolved backend, e.g. `gh issue list --search <nouns>`" — backend resolution
   is the siblings' Phase 0 and happens at mint time, after this sweep; at Phase 1 nothing is
   resolved yet, and the example command is only correct on the git-native backend (wrong on
   Option A file backend and Option C adapters). Low risk (the "e.g." hedges and dedup
   authority is correctly delegated), but reword to something like "one light search of the
   backend the siblings will resolve (git-native: `gh issue list --search <nouns>`; file
   backend: `docs/tickets/`)" or point at doc-writing-rules' backend resolver.

2. **intent.md gates are stale relative to the tree** (intent.md:45–48). P2 evals and P3 draft
   are marked PENDING while `evals/evals.json` and the full body exist in the same worktree.
   Mid-forge this is expected (the forge tasks are still open), but the stale-context invariant
   says the record advances in the same change as the artifact — flip P2/P3 with dates now, and
   P4/P5 plus `status: forging` before ship.

3. **Cross-plugin ship debt.** This change edits a model-invocable description in harness
   (find-open-questions) and suites in harness, teamwork, and docs. At ship that owes: version
   bump + README ledger line for **each** touched plugin (harness and teamwork, not only docs),
   and one `/check-routing` wave over the touched suites (boundary-tier edits share one run).

### Notes

4. **Suite reformat churn.** The four sibling evals.json files were rewritten from the house
   compact one-line-per-case JSON to expanded multi-line objects, turning a 1–2 case delta into
   ~100-line diffs per file. eval_check doesn't care, but it obscures review and breaks style
   symmetry with the rest of the estate's suites. Consider restoring the compact form.

5. **FOQ description re-budget recorded.** The new file-leftovers fence replaced FOQ's
   `issue-sorter` fence (the re-budget-before-adding rule was followed). FOQ's suite still holds
   its issue-sorter no-trigger case, so routing coverage survives. Deliberate trade; no action.

6. **`$ARGUMENTS` on model invocation** substitutes empty; the body treats the scope hint as
   optional and failure branch 4 handles scoped runs, so no action needed.

## Standard-by-standard (pass record)

- **Description as trigger contract**: what + when, five verbatim phrasings front-loaded, three
  parseable NOT-for fences with owners, ~700 chars (under 1,024 / 1,536). Pass.
- **Species/dials coherence**: procedural · `disable-model-invocation: false` ·
  `user-invocable: true`, both explicit; verb-head family name matching the file-* siblings;
  `argument-hint` present. One story, told three ways. Pass.
- **Body as standing instructions**: spec-present tense throughout; identity line → phases with
  done-conditions → output contract (table schema + report format) → named failure branches
  (4) → checkable stopping predicate ("done when every table row carries a terminal
  disposition… NOT done while…"). Pass.
- **Deletion test**: 99 lines, tight; no restated model knowledge found. The evidence-quote
  rule, one-round batching, approval gate, and sibling-delegation lines are all behavior
  deltas. Pass.
- **Hard-gate budget**: zero uppercase NEVER/MUST NOT; the two locks ("never dispatched",
  "never bypasses them with a raw `gh issue create`") are lowercase and name their forbidden
  neighbors. Pass.
- **Contracts first, examples last**: contract/gates in the head, the labeled contrastive
  row pair in the tail. Numeric anchors on the load-bearing dims (≤10-word item, ≤15-word
  quote). Empty-result branch explicit. Pass.
- **Evals**: 10 trigger / 10 no-trigger, every no-trigger names its owner, near-misses cover
  all five fenced neighbors plus issue-sorter, save-lessons, and a plain-recap control. Pass.
