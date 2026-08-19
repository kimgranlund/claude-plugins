# Rubric — Research-leader deliverable

Scores one `research-leader` deliverable file — a typed, dated, sourced findings record, one
row per finding — against the four axes `lld-0023-research-specialist-deliverable-plan` closed
(Resolution 2). Built via `make-rubric`. All four dimensions are `[review]`: no dimension here is
mechanically gate-able — `doc_lint.py`'s own T-checks (where the deliverable is stored under
`.claude/docs/`) cover the document's *shape*, never a finding's substance.

| # | Dimension | Type | What it checks | How to check (measurement plan) | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|---|
| K1 | Knowledge | [review] | Findings carry real substance — best practices, case studies, practitioner conversations, unique insights — not generic restatement | Tally the `category` field across all rows; read the 3 highest-category rows in full | 1: Findings are generic or restate the obvious; no real-result, case-study, or practitioner-conversation entries present. · 3: A mix of facts and at least one real-result or case-study entry; some best-practice claims present but thinly sourced. · 5: Multiple categories represented (facts + real-results + at least one unique insight or practitioner-conversation entry) with specific, checkable substance — not summary-of-summaries. |
| A1 | Actionable | [review] | Every finding's `actionable-note` names a concrete, builder-facing implication, or is honestly `none` | Read every `actionable-note`; flag any that restate the finding instead of naming a next step | 1: Every `actionable-note` reads `none` or restates the finding with no builder-facing implication. · 3: Most findings carry a concrete note, but several are vague ("consider this") rather than a specific next step. · 5: Every non-`none` note names a specific, checkable action a builder could take today, and a genuine `none` appears only where the finding truly has no build implication. |
| G1 | Grounding | [review] | Sources are primary-preferred, dated, and the `confidence` marker matches its own stated definition | Spot-check any 3 rows: open the `source`, confirm `access-date` is plausible, confirm the marker (`[verified]`/`[inferred]`/`[drift-prone]`) matches what the source actually is | 1: Sources are aggregator/secondary, dates absent or stale, `[verified]` claimed without a primary source backing it. · 3: Sources are mostly primary; dates present; confidence markers used but not always matched to their own definition (e.g. `[verified]` on a source that's actually secondary). · 5: Every source primary-preferred, every entry dated, every confidence marker matches its own stated definition — a spot-check of any three rows confirms the marker. |
| N1 | Novelty-vs-known | [review] | Every finding's `novelty` flag is checkable against a named citation or a stated negative-search scope | For each `already-documented-at` row, confirm the citation exists and actually documents the claim; for a sample of `new-to-corpus` rows, confirm a real search scope is named, not asserted bare | 1: No novelty check performed, or every entry marked `new-to-corpus` with no evidence a search against the existing corpus ran. · 3: Some entries correctly flagged `already-documented-at`, but the check reads shallow (one keyword search, not a real sweep). · 5: Every entry's novelty flag is checkable against a named citation (for `already-documented-at`) or a stated, specific negative-search scope (for `new-to-corpus`) — a reviewer can verify either claim directly. |

**Gate to accept a deliverable: K1, A1, G1, N1 each ≥ 3.** All four are load-bearing — a
deliverable that fails any one of them (generic findings, padded or absent actionable notes,
unsourced/misdated/mismarked claims, or an unchecked novelty flag) is not the typed, sourced,
graded record `lld-0023-research-specialist-deliverable-plan` specifies, however good the rest
of the row looks. There is no partial-credit promote tier below this: `doc-checker`'s dispatch at
this rubric either converges on all four ≥ 3 or names which axis failed and why.

**Top failures to look for first:** (1) **an unverifiable `[verified]` marker** (G1) — the
single highest-cost failure, since a downstream builder trusts it without re-checking; (2) **a
padded `actionable-note`** (A1) that restates the finding instead of naming what a builder
actually does with it; (3) **a `new-to-corpus` flag with no real search behind it** (N1) — the
one failure mode raw web search has no structural defense against on its own
(`lld-0023-research-specialist-deliverable-plan`'s own R-2).

**Confidence-marker vocabulary** (reused verbatim from `harness:fact-finder`, never reinvented):
`[verified]` only for a primary, current source; `[inferred]` or `[drift-prone]` (+ a one-line
reason) otherwise. G1 fails the moment a marker is used loosely against this definition.
