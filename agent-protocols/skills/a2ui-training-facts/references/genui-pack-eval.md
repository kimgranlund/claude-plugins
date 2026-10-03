# The judged pack-idiom eval (corpus-genui B3) is a separate harness

> Source of truth: agent-ui `src/corpus-genui/index-shape.ts` (`floorMet`), `tools/corpus-genui/legs/report.ts`
> (`runReportLeg`), `src/corpus-genui/corpus-genui-data.test.ts` (`promptSetVersion` 2). Verified 2026-10-03
> (first recorded 2026-08-24).

## One harness per judged thing

**Claim, the pack-idiom eval does not ride the exemplar shard.** `corpus-genui` B3 is its own
harness: rubric `genui-pack-idiom.md` v1.0, a verdicts file of type `GenuiVerdictsFile`, and a
five-leg `eval:genui-corpus` run. The exemplar shard and its `VerdictsFile` (see
`references/judge-and-verdict-adapter.md`) are untouched by it. **Failure mode:** looking for these
verdicts in the exemplar archive, or reusing the exemplar rubric to grade them.

## The pass criterion is `floorMet`, and a miss counts against the cell

**Claim, a cell passes when at least 2 of its (at most 3) records score `qualityScore >= 4`.** A
cell is one (prompt, pack) pair: 12 cells today (4 prompts x 3 packs). A generation miss
(`E_NO_GENUI`, the model produced no genui line) counts AGAINST the cell. **Why:** the v0.1 reading,
"every judged record is >= 4", was blind to misses (an unjudged absence cannot fail it) and got
harder to meet as `--runs` grew. `floorMet` and its comment in `src/corpus-genui/index-shape.ts` own the rule.

## `E_CELL_OVERFLOW` is a rejection, not a miss

**Claim, a cell holding more than 3 records makes the report leg refuse to compute a floor.**
`E_CELL_OVERFLOW` means a prior run was never cleared, so the cell is inflated and any floor over it
would be wrong (`runReportLeg`). It is NOT a generation miss and must not be tallied as one.
**Failure mode:** reading overflow as a model failure and tuning prompts, when the fix is clearing
the stale run. `promptSetVersion` is pinned (2) in `src/corpus-genui/corpus-genui-data.test.ts`: change the prompt
set and the pin has to move with it.
