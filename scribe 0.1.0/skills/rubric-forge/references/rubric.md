# Rubric — Rubric

The rubric for rubrics. Scores whether a rubric is well-constructed enough to produce consistent, actionable judgments. Scoring method and promote rule are self-contained below; corpus-level finding-severity ordering lives in `skills-audit/references/standard-of-excellence.md`. (Grounded in the rubric-quality dimensions: a rubric is criteria × levels × descriptors × aggregation.)

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| D1 | Label completeness | [gate] | Every dimension is named, typed `[gate]`/`[review]`, and scaled | 1: untyped or unscaled dims · 3: mostly complete · 5: all named, typed, scaled |
| D2 | Label accuracy | [review] | `[gate]` dims are genuinely mechanically checkable; `[review]` genuinely need judgment | 1: "gates" that need judgment · 3: mostly right · 5: every type tag correct |
| D3 | Behavioral anchors | [gate] | 1–5 levels have concrete descriptors, not "good/adequate/poor" | 1: bare scale · 3: anchors at some levels · 5: concrete anchors that a reviewer can match to evidence |
| D4 | Criterion independence | [review] | Dimensions don't overlap or double-count | 1: heavy overlap · 3: minor · 5: each dimension measures one distinct thing |
| D5 | Measurement plan | [gate] | Each dimension states *how* to check it (the evidence) | 1: criteria with no method · 3: some · 5: every dimension names its evidence |
| D6 | Calibration potential | [review] | Two reviewers would score similarly | 1: anchors so vague scores diverge · 3: roughly · 5: anchors tight enough to converge |
| D7 | Actionability | [review] | Failing a dimension implies a specific fix | 1: failing tells you nothing to do · 3: implied · 5: each failure maps to a concrete remedy |
| D8 | Aggregation/gating rule | [gate] | States which dimensions gate promotion and the threshold | 1: no rule · 3: a rule · 5: explicit gate set + threshold + top-failure pointer |

**Gate to promote:** D1, D3, D5, D8 must each score ≥ 3. A rubric without anchors (D3), measurement plans (D5), or a gating rule (D8) produces inconsistent scores and is not usable for review.

**D8 note — the ship-gate set may name a `[review]` dimension.** D8 states *which* dimensions gate; it does not require them to be `[gate]`-typed (mechanically checkable). A genre rubric can have a **definitional-but-judgment** ship-blocker — a dimension whose failure means the artifact is not the thing at all, yet which only judgment can score (e.g. a vision memo's *opinionated voice*: a balanced one is not a vision memo, but "balanced vs. opinionated" is a `[review]` call). Name it in the gate set and mark it, e.g. "V6 (`[review]`, definitional)"; do NOT retype it `[gate]` to make it eligible — that overloads the tier and lies about its checkability (`vision-memo-forge`'s rubric is the reference instance, 2026-07-04).

**Top failure to look for first:** bare scales with no behavioral anchors (D3 = 1) — every reviewer scores differently, so the rubric measures nothing.
