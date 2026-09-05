---
name: perf-loop
description: >-
  The loop contract for fixing against a perf brief: one cause family per iteration, evidence
  recorded before the fix, re-audit of the changed surfaces plus every previous finding, an
  lh-diff gate against the DO NOT BREAK list, revert on regression, stop after two failed
  attempts on one family. Use when the user asks to "fix and re-audit", "work through the
  Lighthouse findings", "get the score green without breaking anything", "iterate on the perf
  brief". NOT for producing the brief (perf-triage); NOT for fanning fixes out to other pages
  (perf-playbook); NOT for perceived-latency recipes (check-speed).
disable-model-invocation: false
user-invocable: true
---

# perf-loop, fix one family, prove it, keep the rest

Input: a brief from `perf-triage` and the before-report it was built from. Output: a
re-audited report with no regression against the DO NOT BREAK list, and a playbook entry per
fix. The loop is deliberately narrow; an open-ended audit "can invent a new class of concern"
every run (thread 1taw297's commenter), so the scope is fixed by the brief.

## The contract

1. **One cause family per iteration.** Take the first family in the brief's fix order that
   still has failing audits. Do not mix families in one change; a mixed change cannot be
   reverted by family.
2. **Record evidence before the fix.** For every audit in the family: the audit id, the item
   the report names (url, selector, snippet or `file:line:col`), and the owning source file
   found in perf-triage step 2. A finding with no item is skipped as `research`, not guessed.
3. **Fix in the source**, never in the build output. Keep the change set to the files the
   family owns (headers config for transport, bundler config for build, and so on).
4. **Re-audit only the changed surfaces plus every previous finding**, never a fresh
   whole-product audit (1taw297's commenter: "re-audit only changed surfaces + previous
   findings, not the whole product from scratch"). Run `perf-audit` on the same URL and
   preset as the before-report.
5. **Gate.** `node scripts/lh-diff.mjs <before.json> <after.json>` prints regressions
   (a passing audit now failing, an audit newly failing that was not scored before, a metric
   past its tolerance, a category score down by more than one point), improvements, and
   unchanged. Exit 1 on any regression. This is the DO NOT BREAK list from the brief, made
   mechanical: same pass threshold, same tolerances (both come from `lh-brief.mjs`).
6. **On regression: revert the change.** The list is never edited to make a red run green. A
   passing audit that regressed is the signal that the fix was "holding three passing audits
   together" (thread 1tewaoi); undo it and re-diagnose.
7. **Stop rule.** Stop when every family is green, or when the same family fails the gate
   twice. On the second failure, escalate with both attempts recorded (what changed, what
   regressed) instead of trying a third variant.
8. **Every iteration appends to the playbook** (`perf-playbook`'s template): audit id, cause
   in this codebase, files touched, the verification command, shared vs page-local.

## Reading the diff

- `audit X: passing (1) -> failing (0)`: revert.
- `audit X: new failure (0), not scored before`: the change surfaced a new audit (a widget
  that was notApplicable is now present); treat as a regression, revert or fix in the same
  iteration.
- `metric lcp_ms: 2368 ms -> 2916 ms (tolerance +237 ms)`: revert; a metric drift inside the
  tolerance is listed under unchanged and is not a block.
- `audit X: passing (1) -> missing from the after report` or `score seo: 91 -> missing`: the
  after run did not measure what the before run did (a dropped category, a changed config, an
  audit gone notApplicable); a regression until the run is repeated with the same config. The
  gate also prints both urls and form factors and warns when they differ.
- `score performance: 78 -> 44`: revert, and expect one of the lines above to name why.

## Done

Every family in the brief is green, or the escalation record names the family, the two
attempts, and what each regressed. `lh-diff` exits 0 against the original before-report, not
only against the last iteration. NOT done: a green score with the DO NOT BREAK list edited,
or a fix applied to `dist/`.

## Provenance

- 1taw297 (r/ClaudeCode), commenter only: "re-audit only changed surfaces + previous findings,
  not the whole product from scratch", "for each real finding, require a failing test, repro
  step, or screenshot before fixing", "every run can invent a new class of concern". The OP's
  "fix it, and then re-run the same prompt" eleven times is the loop shape; the eleven reports,
  findings, and commits are not in the thread and the count is unverified.
- 1tewaoi (r/TheFounders): the regression the guard exists for, "Claude regressed passing
  audits when fixing failing ones", and the framing "here's what's already right and must stay
  right"; the LCP fix that could be "holding three passing audits together". The code change
  itself is not stated.
- 1rn63fb (r/ClaudeAI): the loop terminus "keep going until the numbers were green".
  Unverified: what was changed, the regression guard (none stated).
- 1tfjlbk (linked source): "fixed them one by one until the score was good", the per-fix
  record shape the playbook step inherits.
- The one-family rule, the revert rule, the two-failure stop, and the tolerances are this
  repo's additions.
