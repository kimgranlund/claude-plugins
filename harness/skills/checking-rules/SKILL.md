---
name: checking-rules
description: >-
  Discipline for how a review runs: evidentiary rigor for dismissals, runtime checks over claims
  not a changelog, and steelmanning before filing. Use when reviewing a diff for real bugs, a
  too-fast dismissal, confirming a claim, or grading a review pre-ship. NOT for the return-block
  (write-handoff); NOT for a bound rubric (reviewer/auditor); NOT for DEEP-tier campaign scoring
  (check-all-agents/check-all-skills).
disable-model-invocation: false
user-invocable: true
---

# Reviewer Discipline

A finding that survives only because nobody checked the dismissal is worse than no review at all —
it launders a false "all clear" through a real reviewer's authority. This skill governs three
conduct rules a reviewer applies to every finding: dismissals earn the same evidentiary bar as
confirmations, a "fixed" claim is checked against the artifact instead of taken from a changelog,
and every finding survives one self-directed rebuttal before it ships.

## The invariant's unit — what earns a fresh-context dispatch

Generator ≠ critic is not up for repeal — the 2026-08-11 estate audit's finding stands: every
recent unaudited SEMANTIC edit to a prompt-carrying artifact carried a real gap. What calibrates is
the invariant's UNIT: not "one touched file of the right type," but one build/PR slice (the
changeset that closes together — the PR, or a solo loop's single commit), and within it, whether an
edit is semantic (changes what the artifact tells the model to do or decide) or mechanical (fully
specified and fully checked by an existing automated gate: a version bump, a README ledger line, an
ID renumber, a punctuation/lint-only fix).

- **Semantic → the dispatch earns its cost, every time, regardless of diff size.** A three-line
  change to a hook's fail-open branch, a guard's operator-attachment check, or a selftest fixture's
  assertion is exactly the class the 2026-08-11 finding names — a fresh-context critic pass catches
  what the maker's own context is structurally blind to (confirmed again in a 2026-08-15 review
  round: three fresh-context critic passes each caught a real defect the maker missed — a fail-open
  contract breach in a hook, an attached-operator bypass class in a guard, a tautological selftest
  fixture — none of which the repo's own gates would have caught, since the gates test mechanics,
  not the interpretation a semantic edit changes).
- **Mechanical → floor-tier verification (the repo's own automated gates — `skill_lint`,
  `docs_check`, the version-format check) in the same loop suffices, no separate dispatch.** A
  ledger-line trim, a version renumber, a citation-only fix — the same 2026-08-15 round showed
  per-edit critic dispatches on these added nothing beyond what those gates already catch. These
  edits carry no interpretive content for a critic to grade; dispatching one anyway pays the
  spin-up cost for a verdict the gate already delivered.
- **The UNIT is the slice, not the touch.** One fresh-context critic dispatch covers every semantic
  edit inside one build/PR slice together — batching them never weakens the finding, since each
  edit still gets independent eyes before the loop closes; splitting hairs over line-count to dodge
  the dispatch does. A slice containing even one semantic edit to a prompt-carrying artifact still
  owes the dispatch; a slice containing only mechanical edits to such a file owes none.
- **The test, in one line:** would a human reviewing this diff need to think about whether the
  BEHAVIOR is correct (semantic), or does an existing automated check already fully specify
  correctness for this exact edit (mechanical)? The gates prove mechanics; this line is what still
  needs a second mind.

This section is the referenced "unit" for the standing invariant recorded in this repo's own
CLAUDE.md ("a semantic edit rides with a critic") and in the per-flow contracts that apply it
(`dispatch-ticket`'s build path, `make-skill`'s P5, `file-bug`'s fix-inline branch) — those flows
still own WHEN in their own procedure the check runs; this section owns the calibration test
itself, in one place, so it isn't re-derived differently by each flow.

## Semantic-diff soft size budget

A semantic PR (carries ≥1 semantic edit per the unit above) also carries a soft size budget —
past it, split into serialized waves or justify the size in the PR body; a mechanical-only sweep
(version bumps, ledger lines, a repo-wide rename's enumerated edits) is exempt, since a critic
already reads the whole slice as one unit regardless of file count. The overhaul family's wave
serialization (`authorkit`'s `overhaul-execute`) is the in-house prior art this budget
generalizes: a big semantic change lands as bounded waves a single critic pass can hold in
context, not one unreviewable mega-diff. No fixed file count is prescribed — the budget is
qualitative ("a reviewer can hold the whole slice's semantic content in one pass"), so a PR
author who doubts that of their own slice names the doubt in the PR body and either splits or
justifies staying whole, rather than leaving the size unaddressed for the critic to discover.

## Procedure

Every review this discipline governs runs all three — no precondition skips one:

1. **Evidentiary symmetry.** A dismissal ("this is fine," "false positive," "not a real issue")
   costs the same evidence as a confirmation: name the specific check performed — a command run, a
   file:line read, a case in the input space walked through. A dismissal with no cited check is not
   yet a dismissal; it is an unexamined finding wearing one.
2. **Runtime over claim.** A "fixed / shipped / done" claim under review is checked against the
   actual artifact — read the file, run the command, build it — before it's treated as true. A
   changelog line, a commit message, or the maker's own summary is the CLAIM being reviewed; the
   runtime check alone is what clears it.
3. **Steelman before filing.** Before a finding ships, draft the rebuttal its author would write
   back. If that rebuttal would legitimately survive — the finding rests on a wrong assumption, or
   misses context the artifact actually handles — revise or drop the finding now. Filing the weak
   version and waiting for the maker's pushback to fix it later is the failure mode this step
   exists to catch before it costs a review cycle.

## Output contract

The filed review's per-finding shape, whatever artifact-specific rubric governs its content:
- Every **dismissed** finding names the check that cleared it — a command run, a file:line, a case
  walked — not an unsupported verdict like "looks fine."
- Every **"fixed/shipped" claim taken as true** in the review cites the runtime check that
  confirmed it — a command's real output, or a file read, not the claim's own wording restated.
- The steelman pass covers every finding; at least one finding's entry cites its own rebuttal —
  revised, dropped, or explicitly confirmed to survive it — as proof the pass happened, not just a
  claim that it did.

## Failure branches

- Can't cite a specific check for a dismissal → the finding stays **open**, not dismissed; report
  it unresolved rather than silently cleared.
- Can't check the runtime artifact (tool unavailable, nothing built yet) → the claim is
  **UNVERIFIED**, stated explicitly in the review; it earns "true" only once a check confirms it.
- Steelmanning surfaces a real hole in a finding's own reasoning → fix it before filing; do not ship
  the weaker version and rely on the maker to catch it.

Done when every dismissal in the filed review cites its check, every accepted "fixed" claim cites
its runtime verification, and the review shows a pre-filing self-check took place. NOT done while a
dismissal reads as an opinion with no check behind it, a "shipped" claim is repeated from its own
source with no independent verification, or the first pushback a finding receives is the maker's.

## Example

**Bad (counter-example — do not imitate):** "`_remote_branch_exists` looks fine — the early-return
covers the real failure mode." — a bare verdict, no check named, nothing to verify against.

**Good (confirmation):** "Walked the truth table over `(existed_before, exists_after)`: case
`(False, True)` — branch appears where it didn't before — reports `\"handled correctly\"`,
identical to the true no-op case. That's the silent-failure class this function exists to catch,
just inverted. Not fine as written; case 3 needs its own message or a `False` return before this
ships."

**Good (dismissal):** "The `git ls-remote --heads origin {branch}` path looked like it could have
the same prefix-match risk as the `gh api` path — checked `git-ls-remote(1)`: an unqualified
pattern is tail-anchored, exact match only. Not a bug; dismissing this one." — a dismissal that
survives because the check is named, not because the finding felt implausible.
