# Rubric — Vision Memo Quality

Scores a vision memo — a document whose purpose is to change how the reader *thinks* about a problem,
not to describe what to build. Built via `make-rubric`; scored by **doc-checker** against this file.
`[gate]` = inspection-checkable (a presence / one-sentence-ness check on the draft, no judgment);
`[review]` = judgment with cited evidence from the draft. The **ship gate** (below) names the
dimensions that block shipping — and per make-rubric D8 that set may include a `[review]` dimension
whose failure is *definitional* for the genre (here V6, voice).

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| V1 | Thesis | [gate] | A single thesis sentence is stated and quotable — one arguable claim the reader probably doesn't hold (the gate is presence + one-sentence-ness; sharpness rides the anchor) | 1: no thesis is statable — a topic, not a claim (a survey) · 3: a thesis is present but diffuse across several sentences, or hedged · 5: exactly one sharp, quotable thesis sentence the reader doesn't yet hold, and every section earns it |
| V2 | Reduction | [review] | Strips the problem to irreducible atoms that CONSTRAIN what follows — not an abstract platitude | 1: jumps to solutions (no reduction), OR a "reduction" that is just a definition and rules nothing out · 3: a genuine reduction is stated, but only loosely constrains what follows · 5: a concrete reduction that immediately constrains the solution space ("software is encoded intent") |
| V3 | Reframe (conditional) | [review] | If a genuine received-wisdom misdiagnosis exists, it is surfaced; never manufactured | 1: a straw-man reframe forced where none exists · 3: a reframe present but weakly motivated · 5: a real received wisdom overturned — OR correctly SKIPPED when there is no genuine misdiagnosis (n/a is a pass, not a miss) |
| V4 | Primitives | [review] | 3–7 named, opinionated, individually-justified, composable units carry the argument | 1: 10+ diluted, or 1–2 shallow (the reduction wasn't deep enough) · 3: the right count but generically named · 5: 3–7 opinionatedly-named units, each justified standalone, removing one leaves a gap |
| V5 | Arc & elevation | [review] | Reduction → structure → elevation; the close lifts the topic to a larger meta-point | 1: ends tactical, no elevation · 3: an elevation that merely restates the topic · 5: the close lifts from the stated topic to a principle the reader can carry elsewhere |
| V6 | Opinionated voice | [review] | Takes positions; not a balanced, hedged survey | 1: "explores tradeoffs" neutrally — the genre's core failure; a balanced vision memo has no vision · 3: mostly opinionated, pockets of hedging · 5: stakes throughout; alternatives named only to explain why they are wrong |
| V7 | Physics-literal | [review] | Physical / mathematical framings are literal and computable, not decorative metaphor | 1: metaphor without mechanics ("like a factory") · 3: some framings compute, some are merely evocative · 5: every physics framing is literal — you can compute with it (the 0.9ⁿ pipeline math, invariants, closed loops), OR n/a — a memo with no physics framing is not penalized (score n/a as a pass, as with V3) |
| V8 | Density | [review] | Every paragraph advances the argument; distillation tables compress at boundaries; no filler | 1: filler paragraphs that would fit any memo on any topic · 3: mostly dense, some slack · 5: nothing is cuttable — a lot of thinking per page; tables re-express the argument in compressed form |
| V9 | Archetype fit | [review] | The right archetype for the argument's size, and the structure matches it | 1: a surgical reframe bloated into a manifesto (or a system crammed into a reframe) · 3: right archetype, some section drift · 5: archetype fits the argument size; structure matches it (a manifesto carries a roadmap; a reframe stays surgical) |

**Gate to ship: V1 (thesis, inspection) and V6 (opinionated voice, judgment) each ≥ 3.** These are
definitional — a memo with no statable thesis is a survey; a memo in a balanced, hedged voice has no
vision — either fails the genre however polished the rest is. V6 is a `[review]` dimension carried in the
ship set, sanctioned by make-rubric D8 (the gate set may name a review dimension whose failure is
definitional). V2 (reduction) is the first review dimension to check: "reduction precedes construction"
— a memo that skips it asserts rather than earns.

**Mechanization (A4 exception).** A vision memo's only mechanizable surfaces — the archetype word band,
the `{topic}-{archetype}.md` filename, the 3–7 primitive count — are *advisory* ranges, not hard gates
(a reframe that lands may run short; the primitive count is a soft 3–7). There is no card+checker
because there is no hard mechanical gate to check: the ship gates are inspection (V1) and judgment (V6),
argued here per the maker species' A4 exception.

**Top failures to look for first:** (1) **no thesis** (V1) — a memo that leaves the reader with new
facts but the same mental model failed its one job; (2) **balanced, hedged voice** (V6) — trained
neutrality is the default this genre must actively defeat; (3) **metaphor without mechanics** (V7) — a
physics word invoked for gravitas, where you cannot actually compute with the framing.
