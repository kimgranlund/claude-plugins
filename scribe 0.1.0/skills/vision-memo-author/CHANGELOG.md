# Changelog — vision-memo-author

## 2026-07-04 — net-new authoring (v1.0)

Authored net-new from the legacy `skills/_incoming/vision-memo-writer` as source material (per the
net-new-over-port rule). The legacy skill was strong on craft but had four defects the new shape fixes:

- **Name.** `vision-memo-writer` used `-writer` — an *agent* role suffix — on a skill; renamed to
  `vision-memo-author`, the doc-authoring verb, joining the prd-/spec-/lld-/adr-author family.
- **No rubric → not gradable, not reviewable.** Added `references/rubric.md` (V1–V9, gate V1 thesis +
  V6 opinionated voice), normalized to the rubric-author shape so **doc-reviewer** can score a memo as
  its 12th artifact type — the same generator≠critic route every other authored document has.
- **Monolithic body.** The 368-line SKILL.md is split for progressive disclosure: a lean method +
  archetype selector + output contract in SKILL.md; the six principles / voice / anti-patterns / worked
  example in `references/craft.md`; the four archetype templates carried forward in
  `references/archetypes.md` (harvestable reference material).
- **Weak fence + legacy eval harness.** Description now leads with the use-condition and fences in the
  house form against what-to-build docs (prd-/spec-/lld-/adr-author) and non-argument genres; the legacy
  `evals/evals.json` cases are harvested into `scripts/routing-corpus.json` (four archetypes) and the
  thesis-missing case is preserved as the Step-2 clarification behavior.

The genre substance is unchanged: the argument-not-description thesis, reduction-precedes-construction,
reframe, physics-beats-metaphor, opinionated-beats-balanced, density — and the four archetypes
(manifesto · reframe · case-for · synthesis).

Wired: **doc-reviewer** extended to cover the vision memo (12th type — description, identify-owning-skill
map, and sidecar corpus). Retires `skills/_incoming/vision-memo-writer` — and with it the whole
`_incoming/` staging dir, now empty (research was ported earlier the same day).

## 2026-07-04 — deep-review fix wave

Two independent fresh-context reviews (skill-reviewer on this skill; agent-reviewer on the doc-reviewer
extension) — both KEEP, fixes applied:

- **Retirement made true.** The v1.0 CHANGELOG claimed it retired the legacy source, but the directory
  still stood (and its 396-line `archetypes.md` was a diverged twin of the new 186-line one). Deleted
  `_incoming/` — one deletion closed both.
- **Rubric mis-calibration (would mis-bless a failure).** V2's "3" anchor scored "a definition that
  rules nothing out" as *adequate* while the skill's own text calls that a failure — recalibrated (that
  case now sits in the 1-band; "3" is "a genuine reduction that only loosely constrains").
- **`[gate]` tier honesty.** V6 (opinionated voice) was mis-typed `[gate]`; retyped `[review]` (it's
  irreducibly judgment) and kept in the ship set — sanctioned by a new rubric-author D8 note (the ship
  gate may name a definitional `[review]` dimension; don't overload `[gate]`). V1 recast to an
  inspection gate (a single quotable thesis sentence); V7 gained an n/a clause (a memo with no physics
  framing isn't penalized).
- **Species organs.** Added the missing Update organ (a memo is write-once — re-run the loop, never
  patch prose) and widened the description to the family "author OR evaluate/improve" form; added a
  done/NOT-done close; argued the A4 mechanization exception (a memo's only mechanizable surfaces are
  advisory ranges, not hard gates).
- **Fences/corpus.** Added the "product brief" fence token (prd-author reciprocity grab); added
  symptom/diagnostic + improve-phrased positives and the review-intent boundary negative to the corpus.

Post-wave: harness 14/14 · routing **F1 0.880, precision 0.917** (the lone grab is the maker↔critic
type-name boundary, dispositioned). doc-reviewer re-measured F1 0.786 over its hardened corpus (the
author/reviewer type-name sharing, same structural limit). Standard claims applied: rubric-author D8
(review-dim ship-gates) and the agents-audit N3 citation de-counted to "document-artifact family".
