# lead-review — forge intent record

Forged 2026-08-10 via /make-skill, fourth artifact of the /lead-* family. Slots ruled during
the family design (Kim's AskUserQuestion round ruled the self-authored-work guard IN and the
agent twin OUT); recorded, not re-asked.

## Gate P0 — Route (PASS)

Primitive = **skill, command species**. Deliberately NO agent twin — the family's one asymmetric
member: the estate already carries MANY fresh-context review seats (code-checker, doc-checker,
skill-checker, agent-checker, hook-checker, plugin-checker, wording-checker, wiring-checker,
screens' component/layout/flow-checkers), each fresh-context by construction. A single "review
agent" would either duplicate them or launder their rubrics through one accumulating context.
The command therefore adopts a REVIEW DESK contract: route each target to its owning checker,
dispatch-only.

## Gate P1 — Interview slots (PASS, pre-ruled)

- **Trigger:** human types `/lead-review` when converting a session into a dedicated review
  desk (Kim's REVIEW sessions, formalized). Command species — menu-register description.
- **Behavior delta:** an ad-hoc-primed REVIEW session reviews INLINE — its own single
  accumulating context, no owning rubric, no generator≠critic separation, and nothing stopping
  it reviewing work it authored earlier in the same session (baseline evidence in
  `evals/baseline/`). With the skill: every target is dispatched to its owning fresh-context
  checker; the desk routes and relays, never grades.
- **Species + dials:** Command — `disable-model-invocation: true`, `user-invocable: true`.
- **Freedom:** medium — the routing table is the contract; dispatch mechanics per
  agent-writing-rules' sealed-dispatch discipline.
- **Fences:** NOT a one-off checker dispatch (dispatch the owning checker directly); NOT a
  coordination charter (/lead-team); NOT the standing intake/build seats (/lead-intake,
  /lead-build); NOT the review procedures themselves (check-skill, check-doc — the checkers
  preload those).
- **Done-when:** adoption acknowledged; every target since routed to its owning checker (or
  the named degradation), verdict relayed verdict-first; zero inline reviews; self-authored
  targets disclosed.

**The self-authored-work guard (Kim's explicit ruling, 2026-08-10):** dispatch-only mechanics
already keep the GRADING fresh-context, but a session that authored the artifact can still bias
the dispatch prompt. The guard: a target this session (or its own subagents) authored gets a
NEUTRAL dispatch — artifact pointer + rubric owner only, zero rationale, zero framing, zero
self-defense — and the authorship is disclosed in the relay alongside the verdict.

**Degradation rule (lead-team's precedent):** the owning checker's plugin absent → reviewing by hand
against the owning rubric inline is permitted ONLY then, with the generator≠critic loss
disclosed in the relay — never silently.

## Gate P2 — Evals (PASS)

- Trigger evals: skipped, recorded — command species, house precedent.
- Behavioral assertions: `evals/assertions.md` (4).
- Baseline: `evals/baseline/` — ad-hoc-primed REVIEW session vs a merged PR and a
  quick-look skill review ask.

## Gate P3 — Draft (PASS)

SKILL.md on disk; dials explicit; the routing table by artifact class; body lean.

## Gate P4 — Language pass (PASS)

Instantiation core applied: routing table declarative, dispatch discipline imperative with
checkable objects, guard and degradation as named branches, predicate checkable.

## Gate P5 — Validate

- Lint: clean, first pass and after fixes.
- Fresh-context audit (`evals/audit-report.md`, 2026-08-10): verdict PASS, ship-ready; all 11
  routing-table checkers verified to exist with matching charters. M1 (doc-checker row
  under-listed its charter — a CLAUDE.md would have hit a false gap) — FIXED, row now carries
  the full rubric-bearing set. M2 (absent-plugin degradation inherited lead-team's silent
  from-memory rubric problem) — FIXED, both losses now disclosed. N2 (FLOOR/DEEP depth should
  survive into the seal) — ADOPTED into the dispatch line. W1 double negative — fixed in the
  same line. N1 (code-checker's own-review-seat fence) — accepted as-is for a generic desk,
  noted.
- Behavior check (`evals/behavior-check.md`, 2026-08-10): all four assertions PASS — incl.
  the guard's sharpest evidence (the self-authored dispatch structurally identical to a
  neutral one, disclosure deferred to relay) and the pressure probe declined with the
  installed-plugin check correctly run.

- Fence closure: all fenced siblings command-species or agents; no routing collision from
  dmi:true — recorded disposition.

**Gate summary: P0 PASS · P1 PASS · P2 PASS · P3 PASS · P4 PASS · P5 PASS. Forge complete
2026-08-10.**

## Gate P6 — Ship

teamwork 2.1.0 → 2.2.0, README row, ledger, gate, branch + PR.
