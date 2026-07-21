# Rubric — Typography System Decision

Scores ONE typography system decision: the per-voice font-and-rationale document
pick-fonts produces before handoff to [[font-token-rules]]. `[gate]` = non-negotiable
at promote (score ≥ 3 or the decision doesn't ship) — S5 and S6 happen to be mechanically checkable
via `scripts/typeface-check.py pair <fontA> <weightA> <fontB> <weightB>` over every same-baseline
pairing; S1 is a judgment call that gates just as hard, since a fuzzy territory poisons every
downstream decision. `[review]` = judgment with cited evidence against the 1–5 anchors, scored but
not gating. Used by both the authoring loop in SKILL.md and the independent
`font-choice-checker` agent.

| # | Dimension | Type | What it checks | 1 (fail) → 3 (adequate) → 5 (excellent) |
|---|---|---|---|---|
| S1 | Territory interpretation | [gate] | The input territory reads as a specific point in design space (a named brand, decade, or aesthetic movement) rather than a vague adjective region ("modern and clean") — `make-design-kit/references/context-potency.md`'s presupposition principle applied to a typographic brief | 1: adjectives only, no named reference, the skill proceeded without pushing back · 3: a named reference given but thin (one bare word, e.g. "Swiss," with no further specificity) · 5: a concrete, specific reference point (a named brand, era, or aesthetic) a generating model could act on without guessing |
| S2 | Per-voice justification | [review] | Each of the five concrete font-family decisions (and any stated per-voice exception) carries a rationale that ties back to the interpreted territory from S1, not a generic aesthetic claim | 1: fonts named with no rationale, or the same rationale copy-pasted across voices · 3: rationale present but its link to the stated territory is vague or implicit · 5: every decision's rationale names the specific element of the territory it serves |
| S3 | Coherence across the 11 voices | [review] | The system reads as ONE opinionated voice end to end, not a grab-bag of individually-reasonable, collectively-incoherent picks — the named failure mode this skill exists to prevent | 1: voices contradict each other in register with no bridging logic (e.g. a brutalist display over a soft rounded UI face) · 3: mostly coherent, one or two slots feel bolted on · 5: every slot reads as an inevitable consequence of the same interpreted territory |
| S4 | Expressiveness / commitment | [review] | Voices earmarked for distinctiveness actually commit — real weight/size extremes, real classification distance — rather than hedging into safe, middle-of-the-road choices | 1: every "distinctive" choice is a safe, moderate, default-adjacent pick · 3: some real contrast, but at least one distinctive voice pulls its punch · 5: every voice earmarked for distinctiveness is pushed to a real, stated extreme (weight, size-jump, or classification distance) |
| S5 | Craft correctness | [gate] | Metric compatibility (x-height/cap-height ratio) is computed for every same-baseline pairing and sits within ±10% or carries an explicit `font-size-adjust` compensation; the accessibility floor (`label`/`body`/`tiny`) is respected unless deliberately overridden with a stated reason | 1: a same-baseline pairing with no ratio ever computed, or an accessibility-floor voice went distinctive with no stated reason · 3: ratios computed, one gap left unexplained · 5: every same-baseline pairing's ratio is computed and in tolerance (or compensated), every accessibility-floor override is named and justified |
| S6 | Verified before handoff | [gate] | The metric/axis checks were actually run through `scripts/typeface-check.py`, not eyeballed, before the decision reaches font-token-rules | 1: no checker run — claims asserted only · 3: checker run but not every same-baseline pairing covered · 5: checker run over every same-baseline pairing in the system, its output cited in the decision doc |

**Gate to promote: S1, S5, S6 must each score ≥ 3.** A territory that's still a region (S1) means
every downstream decision is guessing at an unstated target; craft that was never computed (S5) or
never run (S6) means the "verified before handoff" contract to font-token-rules is a claim, not a
fact. These three are non-negotiable regardless of how confident the rest of the write-up reads.
