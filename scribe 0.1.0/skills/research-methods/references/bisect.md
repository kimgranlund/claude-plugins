# Bisect — binary search for a root cause

Halve the search space each round to find the *exact* change that introduced a regression —
logarithmic convergence instead of a linear hunt. Answers: *"it used to work; what broke it, and
when?"* This method **finds**; it does not fix.

## When to use
- A regression with a **known-good prior state** and a reproducible good/bad test.
- "It worked on <date/version>, now it doesn't" — a boundary exists to search for.
- Not this method when: there's no known-good prior → **adversarial** (find what's fragile); nothing
  broke and you want to improve → **autoresearch**.

## Input
The dispatch names the regression — a description, a version range (`v2.1..HEAD`, `abc..def`), a config
that stopped working after a change, or an API/behavior that changed — plus the known-good state and the
good/bad test. (Sealed dispatch: the caller enumerates the bounds; no implicit "diff since last good".)

## Configuration
- `MAX_ROUNDS` 100 · `MODE` `git` | `code` | `config` (auto-detected) — defaults; the dispatch may override any.

## Phase −1 · Research (mandatory)
Web-search the *symptom* before searching the space — it often shortcuts the whole bisect: (1) what
this error/behavior change typically indicates and its known causes; (2) whether anyone has reported
this regression in the tools/libs/platforms involved; (3) what *class* of change tends to introduce
it (dependency bumps, config drift, API contract changes). Form a hypothesis; it lets you test the
likely half first, and a direct hit ends the search early.

## Phase 0 · Establish bounds
1. **GOOD state** — the last known-working commit/tag/snapshot/config. "It worked on <date>" → find
   the boundary in history.
2. **BAD state** — the current broken state.
3. **The test** — the exact good/bad discriminator: a passing/failing test, a behavioral check, a
   scorer threshold, a specific assertion. This test is *frozen* and reused unchanged at every midpoint.
4. **Count the space** — how many changes/commits/steps between good and bad → estimated rounds
   ≈ ⌈log2(count)⌉.

## Phase 1 · Loop
- **git mode** — `git bisect` (or manual checkout) to test the midpoint commit.
- **code mode** — split the good→bad diff in half; apply half the hunks; test; the bug is in whichever
  half tests bad; recurse on it.
- **config mode** — start from all-bad values; flip half back to good; test; narrow to the half that
  still carries the regression.

Each round: `Round n: testing midpoint (<remaining> candidates) · <description> · good|bad · → <remaining/2>`.
Preserve a clean state at every midpoint — no leftover build artifacts.

## Phase 2 · Report
```
Bisect · <description>  ·  good <ref> → bad <ref>  ·  space <count>
Root cause: <exact change / commit / line>
Rounds: <n> of <⌈log2⌉ possible>
Introduced by: <commit/change>
Proposed fix: <what to change — handed off, not applied here>
```

## Rules
- Always halve the space — test the midpoint, never a random point. · One test per round.
- Preserve the exact test at every midpoint — a changed test invalidates the search.
- **Don't fix during bisect** — find the cause first; the fix is a separate step (chain to
  autoresearch). · Start each midpoint from a clean state.
- **Web-search on inconclusive/intermittent results** — a midpoint that's neither clearly good nor
  bad, or a flaky regression, is better explained by a known bug / timing issue / platform quirk than
  by more bisecting. Look up the symptom before splitting again.

## Rubric — bisect conducted well
Inherits **R1 · R3 · R7** from `references/rubric.md` (R1 here = the frozen good/bad test; R3 = one
midpoint per round). Additive method checks:
- **Always-halve** — 1: linear or random probing · 5: true midpoint each round, ~⌈log2⌉ convergence.
- **Frozen test** — 1: the discriminator drifted between rounds · 5: the identical test at every
  midpoint, on a clean state.
- **Find-not-fix separation** — 1: patched mid-search, losing the cause · 5: the exact introducing
  change isolated and reported; the fix deferred to a follow-up.

**Gate:** R1 (frozen test) · R3 (one midpoint/round) · R7 (converged to a single cause) ≥ 3, **and**
no fix was applied during the search (fixing mid-bisect destroys the very signal being narrowed).
