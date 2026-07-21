# Best practices — filling the eight fields

Write the block *for the reader who must act on it*: the orchestrator routing, the critic grading, the host committing. Each field has a failure mode; avoid it.

## Per-field how-to

- **Status** — the routing enum, alone on the first line: `done`, `partial <what remains>`, or `blocked(<the missing input or decision>)`. Never `done` on work with a failing gate — a dishonest Status corrupts every routing decision downstream. `blocked` is a legitimate, cheap outcome; an improvised continuation is an expensive one.
- **Summary** — state the *outcome* in 1–3 sentences ("the positional list reconciler ships; reorders preserve node identity"), not the journey ("first I tried X, then Y broke, so…"). The reader wants what is now true, not how you got there.
- **Files changed** — list *every* path, marked created / edited / deleted, one per line. A missing path hides blast radius. `(none)` for a pure investigation/review.
- **Tests/checks run** — name the **command** and its **verdict** (`pass | fail | UNMEASURED — skipped-not-passed`), never a bare "tests pass". `npm run check && npm test` → "check clean, 1043 passed". A gate you *didn't* run is `UNMEASURED — skipped-not-passed`, stated, never silently omitted — the reader must know the coverage you actually have (e.g. "browser smoke UNMEASURED — no runner here").
- **Evidence** — the *checkable* proof: gate exit codes, the pass count, `file:line` citations for a claim, the coverage result. The test: could the reader confirm your Summary in under a minute from this field alone? If not, it's too thin. Make it **non-vacuous** — "the negative control fails when the fix is reverted" beats "the test passes". Raw output past ~10 lines goes to a file and is cited by path — the block routes, it does not carry payloads.
- **Risks** — name what could be wrong, the assumptions you made, and the blast radius — *honestly*, max ~5, each tagged with its suspected locus (`execution | spec | plan`) so the coordinator can aim the repair at the right seat. "None" is rarely true; a deferred edge, an untested combination, a schema you didn't extend all belong here. A reassuring Risks field is a failed Risks field.
- **Open questions** — only *real* unresolved forks that need a human or another role to decide. Not rhetorical, not already-answered. Each should be answerable with a decision, and routing-shaped ("input target: reuse the control's user-invalid timing, or a new channel?").
- **Recommended next action** — exactly **one** best next step **and its owner**. "planner designs the error-vocab ADR" routes; "various follow-ups remain" does not. If the work is done and verified, say so plainly and name the owner of the commit.

## Per-seat notes

- **planner** — *Files changed* = the docs authored (PRD / SPEC / LLD / ADR). *Tests/checks run* = `harness_checks.py <type>`, `coverage_check.py`, `trace_check.py`. *Recommended next action* often = "ratify ADR-NNNN, then dispatch the build".
- **builder** — *Files changed* = code / scaffold / tests. *Tests/checks run* = `npm run check && npm test` (+ any browser gate). Map each DoD proof point to its test name in *Evidence*. Surface a discovered constraint as an *Open question* / *Risk* rather than editing the contract.
- **team-lead** — a **rollup**: the same eight fields aggregated across the team (*Status* = the worst seat's status: one blocked seat makes the rollup `partial` or `blocked`). *Recommended next action* = the dispatch-or-ratify decision the host acts on.
- **docs-writer** — *Files changed* = site pages / CSS / tests. *Tests/checks run* = the seat's drift gates (e.g. `descriptor/site-canon.test.ts` — a project example, not canon; name your project's own) + `npm run check && npm test`; a browser smoke you wrote but couldn't run is UNMEASURED. *Risks* = the soft content drift a static test can't see.
- **reviewer seats** (doc-checker, skill-checker, agent-checker, wording-checker, component-/layout-/wiring-checker — whichever of these the estate carries) — *Files changed* = `(none)`: a critic grades, it does not build. *Evidence* = the gap-map's citations (file:line or quoted text per scored dimension, gate verdicts first). *Recommended next action* = "maker applies the fix" — the maker is the recipient-owner.
- **token-builder** (the `color` plugin's seat, where installed) — *Files changed* = the token files (`tokens.css` / `dimensions.css`). *Evidence* = the WCAG-AA + forced-colors result across *both* schemes, and that no role ladder collapsed to one step.

## Do / don't

- **Do** drain the inbox before composing when you run in a messaging team (see `foundations.md` §5) — freshness is a correctness property. A sealed subagent has no inbox; its freshness is consistency with its dispatched inputs.
- **Do** keep the read-then-commit ordering. **Don't** chain a commit onto a gate with `&&`.
- **Don't** omit a field — `(none)` is information; a missing field is ambiguity.
- **Don't** narrate process where outcome + evidence belong.
- **Don't** mark a maker's own work "verified" — verification is the critic's / coordinator's step. Hand back *gated state* with the evidence; let the gate be read by the next seat.
- **Don't** hand back a block a reviewer would have to re-do the work to trust.
