# Orchestration rubric — A7: workflow scripts (deterministic orchestration)

One of eight per-archetype rubrics — see `orchestration-rubric-a1-solo-host.md`'s header for
the shared method statement, verdict scale, and the cross-cutting X-R1..X-R4 criteria
(cited there, not restated here).

**Priority axis G2** (2026-08-18 fold-in): the `workflows/*.js` tier had ZERO lint/rubric/
checker coverage — `eslint.config.mjs` deliberately EXCLUDES `**/workflows/*.js` (issue #529:
the Workflow tool's own loader extracts a leading `meta` object literal then runs the
remainder as the body of an async function it supplies itself; the file legally carries both
a top-level `export const meta = {...}` AND a top-level `return {...}`, a combination no
standard ECMAScript `sourceType` — `module` or `script` — can parse as one whole file, so
reusing the existing `**/scripts/*.mjs|js` config block is not an option, confirmed
empirically 2026-08-18 against `harness/workflows/chore-sweep.js` (`'import' and 'export' may
appear only with 'sourceType: module'` under `commonjs`; the mirror failure under `module`
sourceType is the well-known "illegal return statement" one). Resolution (build judgment,
ratified acceptance allows either lint-tier or a stated exemption ADR): **lint tier**, realized
in `orchestration-audit`'s `a7-workflow-syntax` check (A7-R4 below) — not a repo-root
`eslint.config.mjs` edit, since the check needs the loader's own meta/body SPLIT semantics,
which a single eslint `languageOptions.sourceType` cannot express. Escalates to a ratified
exemption ADR only if this check proves disproportionate to the `workflows/` surface (one file
today: `harness/workflows/chore-sweep.js`) — not reached at this size.

## Architecture & intended use

JS script drives `agent()` fan-out with loops/barriers; journaled, resumable. Intended use:
dispatch graphs with NO judgment in the control flow (the `chore-lead` retirement standard,
#266).

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A7-R1 | Mechanization test: control flow contains zero judgment calls; judgment lives in the dispatched agents | the `chore-lead` retirement standard, #266 | judgment |
| A7-R2 | Pipeline over barrier; every cap/truncation logged, never silent | — | judgment |
| A7-R3 | Resumability preserved: no wall-clock/randomness in-script; journal read before diagnosing empty results | — | judgment |
| A7-R4 | **(G2)** Bundled-script discipline: selftest green (G4); `apply-scripts` refuse out-of-sandbox writes — realized here as the workflow-file SYNTAX lint tier, since standard `**/scripts/*` eslint coverage cannot reach `workflows/*.js` (see above) | G4; `chore_sweep_apply`'s `.claude/ops` fence; issue #529 | **mechanizable** — `orchestration-audit`'s `a7-workflow-syntax` check: for each `**/workflows/*.js` file, splits at the `export const meta = {…}` boundary (brace-balanced), syntax-validates the meta half as an ES module (`node --check`, `.mjs`) and the body half wrapped in an async function (`node --check`, `.js`) — a real parse failure in either half is a finding, never a silent pass |
| A7-R5 | Portability disclosed: workspace-relative paths stated as this-repo-scoped, with the fallback branch named | — | judgment |
| A7-R6 | Permission-model note: workflow subagents run `acceptEdits` with the inherited allowlist, piloted on one directory first | #671 (canon text lands in the A7/workflow-guidance home #671 names; cited here, not restated) | judgment |

**Owning checker for A7:** `orchestration-audit` itself is A7's first review surface (A7-R4);
A7-R1/A7-R2/A7-R3/A7-R5/A7-R6 stay judgment-queued to a human or `code-checker` read of the
script's actual control flow.
