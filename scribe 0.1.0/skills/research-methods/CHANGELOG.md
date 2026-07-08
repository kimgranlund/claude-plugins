# Changelog — research-methods

## 2026-07-04 — net-new authoring (v1.0)

Authored net-new from the legacy `skills/_incoming/research` multi-skill as **source material**
(never copied — per the net-new-over-port standing rule). The legacy skill bundled six investigation
procedures + a selector under one SKILL.md, ran inline in the host thread, and carried no rubric.
This split fixes all three:

- **One knowledge pack, not a multi-skill.** `research-methods` is a noun-compound knowledge skill
  (the method library); the six procedures are `references/<method>.md`, each with when-to-use,
  protocol, and its own rubric section. Running an investigation in isolation is the paired
  **`researcher`** agent's job — the skill it preloads.
- **Investigation-quality rubric.** `references/rubric.md` — the shared spine (R1 scorer-first ·
  R2 method-fit · R3 single-variable · R4 clean-state · R5 grounding · R6 journaling · R7 termination
  · R8 reporting), gate R1/R3/R7. Each method file adds its method-specific gates on top.
- **House-style output.** The legacy ASCII box-art cards were dropped for clean fenced structured
  output; the folded description leads with the use-condition and carries a real routing fence
  (web-lookup / reviewers / authors).

The six methods, unchanged in essence from the source: autoresearch · hill-climb · ablation · sweep ·
bisect · adversarial. Once this + `researcher` are validated, `skills/_incoming/research` is retired.

## 2026-07-04 — deep-review fix wave

Independent deep review (`skill-reviewer`, fresh context, against the skills-audit standard) — verdict
KEEP, with a fix wave applied:

- **A3-a (the big one): command-era residue removed from all six method files.** `$ARGUMENTS`, "override
  in the arguments", and "Default: the most recently edited file" were carried over from the legacy
  slash-command form — dead machinery in a *preloaded* reference, and the "most-recent-file" fallback
  directly contradicted the sealed-dispatch canon. All six Input/Configuration sections are now
  dispatch-shaped ("the dispatch names what to …; no fallback").
- **S1 / N2: species declared.** Added the declared-hybrid paragraph (a knowledge pack that carries an
  execution spine, like linguistic-techniques) and `references/sources.md` — one grounded citation per
  method (Karpathy autoresearch, git-bisect, ablation-study methodology, hill-climbing/AIMA, Bergstra &
  Bengio sweep, OWASP/property-based adversarial). Provenance was previously missing entirely.
- **S5: the run's critic is named.** The report is scored by the dispatching seat that receives the
  handoff (consumer-as-critic); the earlier "whoever reads it" was vague and doc-reviewer's charter
  doesn't cover investigation reports.
- **A3-b / S3: rubric.md hardened.** The per-method gate summary (a diverged twin — its autoresearch line
  wrongly listed shared R3 as an additive gate) is cut to a pointer; the `[gate]` tier is now honestly
  flagged as judgment-checked (not lint-backed), with a journal shape-checker as the standing follow-up.
- **M2: routing corrected AND re-dispositioned.** The initial CHANGELOG claim ("all 6 misses are proxy
  artifacts") was measured false: 2 were fence-repelled positives (fenced `skill`/`scoring` repelling
  owned vocabulary → fixed by adding `skill, agent` to the scorable-system list + a `scoring checks`
  trigger) and 2 were lexical holes (missing `regression` / `used-to-work` triggers → added); only the
  residual 3 (bisect-regression dilution, stress-test, adversarially) are genuine inflection/stemmer
  artifacts. Corpus hardened with the improve-family siblings; an improve-family fence
  (linguistic-techniques / rubric-author / loop-design) added after `agent` entered the scorable list.
- **L: added a dated worked example** (autoresearch on this skill's own routing) + a done/NOT-done close.

Post-wave: harness 14/14 · routing **F1 0.889, precision 1.000** over the hardened corpus (3 residual
misses are inflection/stemmer artifacts, human-read). Two claims routed to skills-audit: a hybrid /
method-library species row for §S1, and registering the "experiment" instrument (mutate-and-measure loop
over a scorer) in the naming canon.

## 2026-07-04 — first live dispatch (shakedown) · the "experiment" instrument registered

The `researcher` seat ran its first real investigation: a SWEEP of `routing_eval`'s hand-picked
`threshold=0.34` over all 55 checked-in corpus pairs. The pack's protocol held end-to-end — Phase −1
grounding shaped the range, scorer + baseline fixed before the loop, coarse+fine grid, a named stop
predicate, measure-only honored, a complete journal. Result: **0.34 is the joint optimum** (macro-F1
0.8699, plateau 0.34–0.36, estate peaked not flat), and the run surfaced one real defect no threshold
rescues (orchestration-reviewer's routing, F1 ≤ 0.57 at every t — filed to its owner). The journal is
preserved as `examples/threshold-sweep-2026-07-04.md`: the dated real-session worked example the deep
review asked for, and the reference journal fixture the shape-checker was then built against.
`scripts/journal_check.py` (same day) closes that standing follow-up — the R1/R3/R7 gates now run
arithmetically (three-valued, selftest-locked, the real journal as the pass fixture), upgrading
rubric.md's `[gate]` tier from judgment-checked to checker-backed for the three line-checkable gates.
Same day, the **experiment** instrument (mutation; substrate: researcher + this pack) was registered as
the instrument registry's fifth row — the canon claim from the deep review, now closed.
