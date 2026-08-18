# Orchestration rubric — A1: solo host + inline skills

One of eight per-archetype rubrics scoring an orchestration INSTANCE against its OWN
architecture and intended use (ADR/ratification: issue #666, find-intent round, Kim
2026-08-18) — never a generic "good orchestration" bar. Consumed by `wiring-checker`
(fleet-arrangement judgment) and authorkit's `orchestration-audit` instrument (mechanical
sweep + judgment-queue render), both reaching this file by path — no new
description/evals surface rides with it (2026-08-18 marshal fold-in on #666).

Verdicts: 🟢 pass · 🟡 attention · 🔴 fail. Every criterion below is falsifiable and cites
its evidence source (an incident, an ADR/IDR, or a named doctrine skill). A criterion
tagged **judgment** has no lexical/structural anchor a script can grade — it is reported
"queued, not built" to its named owning checker, same discipline as `doctrine-audit`'s own
4th edge type; a criterion tagged **mechanizable** is exactly what `orchestration-audit`'s
`scripts/audit.py` computes.

## Architecture & intended use

One context, procedural/command skills run inline, no isolation boundary. Intended use: any
task one context can hold (IDR-0007 solo-first; #265 measured a coordinator hop at 1.92×
tokens / 3.6× wall-clock for equal quality on a quiet estate).

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A1-R1 | Solo-first honored: fan-out only where a named coordination need exists | IDR-0007 | judgment |
| A1-R2 | Reachability: skills reachable by every caller class that needs them — `dmi:true` blocks BOTH the Skill-tool and model routes | #134/#266 class | mechanizable — grep the skill's frontmatter for `disable-model-invocation: true` cross-referenced against a caller that needs Skill-tool reach |
| A1-R3 | Shared-state guard: anything touching `.claude/ops` concurrently carries a live guard | `sweep_guard`; the 2026-08-17 duplicate-firing pre-emption | mechanizable — grep the touching script for the guard call |
| A1-R4 | Context economy: preload/menu rent measured, not assumed | `attention-audit` family | mechanizable — delegate to `attention-audit`'s own `rent.py`; this instrument never re-derives that measurement |
| A1-R5 | Degraded paths named: script-not-found / not-installed branches explicit, never silent | this skill's own cross-plugin soft-mention convention | judgment |

## Cross-cutting (applies to every archetype — cited by file, never restated)

The three X-criteria below are the ONE canonical copy; every sibling rubric file (A2–A8)
cites this section by path rather than repeating it.

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| X-R1 | Intent traceability: an IDR/ADR names when this archetype is the right tool | — | judgment |
| X-R2 | Incident→infrastructure closure: each incident on this archetype produced a guard/lint/fixture the same day, or has an open tracked record | CLAUDE.md's "Incident → infrastructure, same day" invariant | judgment |
| X-R3 | Review coverage: a checker/audit exists that can grade an instance of this archetype | — | mechanizable — the named owning-checker file exists on disk (per archetype, see each file's own "Owning checker" row) |
| X-R4 | Plan-holder axis honored: the arrangement's own "who holds the plan" answer (plan holder · worker↔worker comms · file isolation · lifetime) plus the 6-line topology decision tree are consulted at design time | #671 (canon text lands there; cited here, not restated) | judgment |

**Owning checker for A1:** none dedicated — A1 instances ride the repo's own standing gates
(release_gate.py, skill_lint.py) rather than a bespoke reviewer; X-R3 for this archetype
checks that those gate scripts exist and are wired into CI, not that a NEW checker exists.
