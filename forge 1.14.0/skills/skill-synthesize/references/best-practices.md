# Best practices — two worked cases, cited to source

Both cases below are dated, verified deliverables from this corpus's own history — not
illustrations. Read the canonical docs for full depth; this file distills the *method* lesson each
one teaches.

## Case 1 — split warranted: `color-science` (159 files → 4 packs)

Canonical source: `~/.claude/.claude/docs/color-science-extraction-plan.md`.

The corpus was a research-wave-scale monolith: 159 reference files, a working TypeScript library
(`src/`), a 54-page interactive demo site (`examples/`), and an `evals/` folder — 4.0 MB total,
roughly ten distinguishable question types. Running the four tests:

- **Sizing** — straining: INDEX at ~300 lines, several reference files over 1000 lines forcing a
  Grep-first load-discipline warning, well past the 3–7 axis comfort zone.
- **Ask co-occurrence** — the corpus's own routing positives clustered cleanly into four families:
  compute (spaces/gamut/CSS), contrast standards (APCA/WCAG/CVD), physical/materials
  (pigment/print/naming), and vision science (appearance/perception) — each answerable without
  reaching into the others.
- **Vocabulary separability** — each cluster's trigger tokens were orthogonal: nobody asking about
  Kubelka-Munk pigment mixing is also asking about APCA contrast thresholds.
- **Cost ledger** — four new descriptions, four routing corpora, and a real referrer-rewire cost
  (~30 external referrers across sibling skills) — priced and paid, because the retrieval benefit
  was concrete: a query about contrast math no longer loads pigment-mixing reference files.

**The recursive check, inside an already-justified split:** the plan did not stop at four packs. It
tested a 5th `palette`-generation pack (rejected — "the seam cuts through the interpolation files…
splitting it would make cross-pack consults the common case") and a 5th `naming` pack (rejected —
"shares its paint-dataset files with pigment; one pack avoids splitting those pairs"). It also
explicitly kept its largest single cluster — 72 files under `color-space-facts` — unified,
because those files cross-cite densely. **A pack having the most files does not mean it should split
further; it means its internal cohesion earned it that size.**

Manifest discipline: every one of the 159 files was assigned to exactly one child, reconciled by a
mechanical count (`find … | wc -l` = 159, sorted-basename diff against the pre-move list empty).
This is exactly what `scripts/manifest_check.py` automates.

## Case 2 — split rejected: `color-theory-facts` (28 files, stays one pack)

Canonical source: `~/.claude/.claude/docs/color-theory-facts-partition-assessment.md`.

The literal request was "break this into a family." The corpus: 28 reference files, no `src/`, no
demo site, no `evals/` — a lean, hand-authored-scale pack with four axes already declared in its
SKILL.md (Harmony, Wheel & history, Programmes, Meaning). Running the identical four tests:

- **Sizing** — not straining: 28 files / 4 axes is inside the healthy range, the same scale as
  `ui-patterns`, the corpus's own model of a single healthy pack. No INDEX bloat, no load-discipline
  pressure, no count drift.
- **Ask co-occurrence** — the corpus's own 12-item routing corpus, mapped query-by-query:

  | Positive | Axes engaged |
  |---|---|
  | "explain why complementary color schemes are supposed to work" | Harmony **+** Wheel |
  | "does this palette read as calm and trustworthy" | Meaning (via Harmony's character claim) |
  | "my brand colors feel garish together" | Meaning **+** Harmony |
  | "was Itten right about the seven contrasts" | Wheel **+** Harmony |
  | "should I use a triadic scheme for my poster" | Harmony **+** Wheel |

  6 of 12 positives demanded two axes at once. **A 4-way router would misroute the cross-axis
  majority or force every child to duplicate the keystone Harmony file.**
- **Vocabulary separability** — failed: all four axes trigger on one shared token field (clash,
  harmony, wheel, mood, communicate). Candidate children would compete for identical tokens — the
  same routing-dilution failure mode that killed color-science's 5th palette/naming packs, but here
  affecting the *whole* proposed split, not one candidate within it.
- **Test 4 never priced** — 1–3 failed, so the cost ledger was academic. (It would have been
  lopsided anyway: the pack had just been re-serviced hours earlier during the color-science
  referrer rewire, making a split's re-invalidation cost especially high for zero identified
  benefit.)

**The one arguable seam, tested and still rejected:** wheel/history (11 files) has the crispest
independent vocabulary of the four — the closest thing to a defensible split candidate. It still
fails, because the corpus is deliberately revisionist: the historical files are the *evidence* for
the harmony corrections ("the RYB wheel is a 1769 error" is the direct backing for "hue-interval
harmony is a weak predictor"). Splitting history from harmony would sever the correction chain that
is the pack's entire charter. **A vocabulary argument alone does not clear the bar if the seam cuts
through an evidentiary dependency.**

## The lesson across both cases

The same four tests, applied with the same rigor, produced opposite verdicts on two real corpora.
Neither result was decided in advance; both were earned by evidence. That is the method working
correctly in both directions — a decomposition skill that always finds a family, or one that never
does, has stopped testing and started confirming a bias.
