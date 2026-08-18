# Orchestration rubric — A1: solo host + inline skills

One of eight per-archetype rubrics scoring an orchestration INSTANCE against its OWN
architecture and intended use (ADR/ratification: issue #666, find-intent round, Kim
2026-08-18) — never a generic "good orchestration" bar. Consumed by authorkit's
`orchestration-audit` instrument (mechanical sweep + judgment-queue render), reaching this
file by path — no new description/evals surface rides with it (2026-08-18 marshal fold-in
on #666). `wiring-checker` judges ONE arrangement's own composition against its OWN rubric
(`fleet-rules/references/rubric.md`) and does not currently cite these per-archetype files —
a future wiring could point it here, not claimed as already wired (2026-08-18 code-checker
review: an earlier draft claimed this pointer existed; it didn't).

Verdicts: 🟢 pass · 🟡 attention · 🔴 fail. Every criterion below is falsifiable and cites
its evidence source (an incident, an ADR/IDR, or a named doctrine skill). Three tags, never
conflated (2026-08-18 code-checker review: an earlier draft's binary tagging overclaimed
what the driver script actually runs, silently — this three-way split is the fix):
- **judgment** — no lexical/structural anchor a script can grade; reported "queued, not
  built" to its named owning checker, same discipline as `doctrine-audit`'s own 4th edge
  type.
- **mechanizable — built** — `orchestration-audit`'s `scripts/audit.py` computes this
  criterion TODAY. Exactly six criteria across all eight files carry this tag as of
  2026-08-18: X-R3 (review-coverage existence), A3-R2 (fleet.json↔roster reconciliation —
  the durable-channel READER only, never a comment-trail cross-reference), A4-R1 (roster
  row count), A5-R3 (resume-command presence), A6-R2 (grant-literal presence), A7-R4
  (workflows/*.js syntax lint). No other criterion in any of the eight files is currently
  computed, whatever its own table row's prose describes as a plausible check.
- **mechanizable — not built** — a real script COULD compute this (a structural/lexical
  anchor exists), but `audit.py` does not yet; reported "queued, not built" identically to a
  judgment criterion until a future change implements it. Never rendered as a pass.

## Architecture & intended use

One context, procedural/command skills run inline, no isolation boundary. Intended use: any
task one context can hold (IDR-0007 solo-first; #265 measured a coordinator hop at 1.92×
tokens / 3.6× wall-clock for equal quality on a quiet estate).

## Criteria

| ID | Criterion | Evidence | Mechanizable |
|---|---|---|---|
| A1-R1 | Solo-first honored: fan-out only where a named coordination need exists | IDR-0007 | judgment |
| A1-R2 | Reachability: skills reachable by every caller class that needs them — `dmi:true` blocks BOTH the Skill-tool and model routes | #134/#266 class | mechanizable — not built (would grep the skill's frontmatter for `disable-model-invocation: true` cross-referenced against a caller that needs Skill-tool reach) |
| A1-R3 | Shared-state guard: anything touching `.claude/ops` concurrently carries a live guard | `sweep_guard`; the 2026-08-17 duplicate-firing pre-emption | mechanizable — not built (would grep the touching script for the guard call) |
| A1-R4 | Context economy: preload/menu rent measured, not assumed | `attention-audit` family | mechanizable — not built (delegates conceptually to `attention-audit`'s own `rent.py`; this instrument never re-derives that measurement, and does not yet dispatch it either) |
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
