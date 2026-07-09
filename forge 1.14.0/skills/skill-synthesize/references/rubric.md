# Rubric — skill-decompose

Scores a decomposition **verdict** (the manifest + its reasoning), not the resulting child skills —
each child, once authored, is scored on its own terms by `skill-review`.
`[gate]` = mechanically checkable (`scripts/manifest_check.py`); `[review]` = judgment with cited
evidence on the 1–5 anchors.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| D1 | Test completeness | [review] | All four tests run, in order, with cited evidence | 1: verdict asserted with no test trail · 3: tests named but thinly evidenced · 5: each test cites specific files/lines/routing-corpus rows; a failed test stops the chain (no test-4 pricing after a 1–3 failure) |
| D2 | Manifest reconciliation | [gate] | Every source file assigned exactly once; counts match | 1: orphaned or duplicated files, count mismatch · 3: reconciles but unverified by script · 5: `manifest_check.py` clean, pre/post counts both stated |
| D3 | Rejection rigor | [review] | Rejected alternatives (sub-splits, thin candidates) are named with reasons | 1: no rejected-alternatives section · 3: alternatives named, reasons generic · 5: each rejection cites the specific failing test and evidence, mirroring the precedent's explicit reject-log |
| D4 | Naming compliance | [gate] | Each child name follows `skill-forge/references/skill-naming-conventions.md` (domain-verb or noun-compound, no verb inflation, no collision) | 1: invented grammar or a collision · 3: compliant, unchecked against existing directory names · 5: compliant and explicitly checked against the corpus |
| D5 | Invocation posture decided | [gate] | Each child's posture (`disable-model-invocation` / `user-invocable` / default) is stated with a one-line rationale | 1: left unstated · 3: stated, no rationale · 5: stated and traceable to the child's own description, per skill-rubric D11 |
| D6 | Referrer completeness | [gate] | Every external referrer to the parent handle is enumerated BEFORE the verdict, regardless of outcome | 1: no survey · 3: partial grep · 5: full corpus-wide grep (skills/agents/CLAUDE.md/settings/memory), persisted as the repair map |
| D7 | Cost-ledger honesty | [review] | Costs stated even under a `split` verdict; benefit stated as a number, not an adjective | 1: benefit asserted ("cleaner", "more efficient") with no measure · 3: costs listed, benefit vague · 5: both costs and benefit quantified (referrer count, description-char totals, or a stated retrieval-reduction estimate) |

**Gate to promote:** D2, D4, D5, D6 must each score ≥ 3. A manifest that doesn't reconcile (D2), names
a child that collides or breaks grammar (D4), ships an undecided invocation posture (D5), or was
never checked against the corpus's actual referrers (D6) is not a deliverable regardless of how
compelling the prose reasoning reads.

**Top failures to look for first:** (1) a verdict reached by vibes rather than the four tests in
order (D1 low) — the single most common failure, since "split it up" is easy to agree with without
testing; (2) a manifest that reconciles on paper but was never run through `manifest_check.py` (D2);
(3) a rejected-alternatives section that is missing entirely, which usually means the recursive
check (testing sub-splits within an already-justified split) was skipped (D3).
