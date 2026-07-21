---
name: checking-rules
description: >-
  Cross-cutting discipline for HOW a review gets conducted, not what it checks — evidentiary
  symmetry for dismissals, verifying a "fixed/shipped" claim against the runtime artifact instead
  of a changelog, and a steelman self-review pass before filing. Use when reviewing a diff for real
  bugs and not just the happy path, before filing a review to steelman what the author would say
  back, when checking whether a dismissal was too fast, or when grading a review before it ships.
  NOT for the return-block format a reviewer hands back (harness:write-handoff); NOT for one
  artifact type's own rubric — a component's anatomy, a layout's structure, a document's ID spine
  (the bound *-reviewer/*-auditor agent's own preloaded standard); NOT for portfolio/DEEP-tier
  campaign scoring across a whole corpus (check-all-agents/check-all-skills).
disable-model-invocation: false
user-invocable: true
---

# Reviewer Discipline

A finding that survives only because nobody checked the dismissal is worse than no review at all —
it launders a false "all clear" through a real reviewer's authority. This skill governs three
conduct rules a reviewer applies to every finding: dismissals earn the same evidentiary bar as
confirmations, a "fixed" claim is checked against the artifact instead of taken from a changelog,
and every finding survives one self-directed rebuttal before it ships.

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
