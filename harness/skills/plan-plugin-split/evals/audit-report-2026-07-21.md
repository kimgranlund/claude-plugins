# Floor audit — plan-plugin-split (merge-seam-remeasure capture), 2026-07-21

Skill: harness/skills/plan-plugin-split · Standards: skill-writing-rules · Lint: clean
Verdict: PASS (no blocking findings; 1 minor, 1 nit)

Scope (per dispatch): the Phase-5 pointer sentence (SKILL.md:137–140) and the new
`references/merge-seam-remeasure.md` (64 lines). Description and frontmatter unchanged — routing
out of scope, R2 spot-checked only.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | merge-seam-remeasure.md:45 (2-of-3 = noise, never chase), :53–55 (compare fail counts — denominators shift), :18–19 (Decision 5: union steals are NEW seams, not regressions) — each deletion changes the executor's disposition of a real failure class; none is model knowledge | — |
| R2 | PASS | — | Description unchanged (SKILL.md:3–14); "should this mega-plugin be several smaller ones", "partition our .claude folder", "gap analysis on this plugin family" all verbatim; fences intact | — |
| R3 | PASS | — | Procedural species, both dials explicit (SKILL.md:15–16), verb-head name; reference one level deep | — |
| R4 | PASS | — | Pointer is standing-instruction spec-present: "A MERGE verdict's executor additionally owes…" (SKILL.md:137) — presupposes the obligation, no one-time phrasing; reference is declarative method register; no new uppercase hard gates | — |
| R5 | FAIL | minor | merge-seam-remeasure.md:57–64 "The run mechanics" restates check-routing's blind-judge substrate — menu from live descriptions, expectation-stripped, shuffled, blind no-tools judges = check-routing/SKILL.md:29–39 (Phases 2–3). Drift already visible: check-routing's answer-count clause (metabolized incident 2026-07-09, its :35–37) isn't mirrored here and won't be on the next contract change | Rewrite the section as "per check-routing Phases 2–4, with these merge deltas:" keeping only what differs — union menu, all suites pooled + fixed-seed shuffle across ~5 judges (vs one per suite), source-plugin baselines as per-suite floors, one full round per heal wave |
| R6 | PASS | — | Pointer sits in Phase 5 (the verdict/handoff phase, where the executor obligation belongs); SKILL.md is 157 lines — whole body inside the 5,000-token head; reference 64 lines < 100, no TOC owed | — |
| R7 | PASS | nit | Done predicate (SKILL.md:153–155) says "handoff names /make-plugin" but carries no merge-branch clause — an executor handoff that dropped the re-measure obligation would still satisfy Done as written | Optional: append "…and, on a merge verdict, the re-measure obligation (references/merge-seam-remeasure.md)" to the Done line |
| R8 | PASS | — | Numeric anchors throughout: 2-of-3/3-of-3 round thresholds, ~1.5% noise (7–10 misses per ~520 cases), 22 splits, 8 fences, 9 reciprocals (merge-seam-remeasure.md:40–55) | — |

## Pointer ↔ reference drift check (dispatch item 1)

No drift. The pointer's four-item method summary (SKILL.md:139–140: ordered context splits,
thief-side fences, reciprocal cases, noise calibration) maps 1:1 to the reference's three healing
instruments (:23–36) + noise section (:38–55). The pointer's rationale clause ("seams the source
plugins' green baselines cannot predict") duplicates the reference's opening (:4–5) — dismissed,
not filed: a pointer owes one motivating clause to route the executor, and deleting either copy
changes behavior at its own site. "MERGE verdict" vocabulary checked against the description —
SKILL.md:9 "fewer plugins is a merge verdict" establishes it; not a phantom term.

## Citation verification (dispatch item 2 — runtime over claim, all checked)

- PR #73: `gh pr view 73` → "design 1.0.0: ADR-0008 — merge design-kits + color + typography",
  MERGED 2026-07-21T17:04:46Z. Confirms :7 (PR #73, 2026-07-21, the trio merge).
- ADR-0008 Decision 5: `.claude/docs/adr/0008-merge-design-plugins.md:43–47` — "steals across the
  former plugin boundaries are NEW seams to fence (not regressions)". Matches :18–19 verbatim in
  substance.
- Numbers vs design/README.md:52 (v1.0.0 ledger): 508/515 baseline, 515→488 raw (94.8%),
  524→515 healed (98.3%), 22 splits, 8 thief-side fences, 9 reciprocal cases, material-token n07
  known-ambiguous 3/3 rounds — every figure in :7–8, :29, :36, :50–51 matches.
- "never tune to chase" color-baseline ruling: design/legacy/README-color.md:53 (v0.1.3 line,
  "KNOWN AMBIGUOUS SEAM … never tune to chase"). Confirms :43.
- make-stitch-kit fence claim (:32–34): design/skills/make-stitch-kit/SKILL.md:15 carries the
  `(design-md-rules)` fence. Fixed-claim verified against the artifact.

## Steelman record (checking-rules)

R5's author rebuttal — "the section is deliberately self-contained because the pooled ~5-judge
fan-out is NOT check-routing's per-suite dispatch, and a bare pointer would mislead the executor
into per-suite dispatch" — survives partially: it caps the finding at minor and shapes the fix
(deltas stay explicit; only the shared base becomes a pointer). It does not clear the finding: the
shared base (blind/strip/shuffle) is exactly the slice that will drift, and one omission
(answer-count clause) is already observable.

Top 3: 1) R5 minor — repoint the run-mechanics base at check-routing, keep only the merge deltas.
2) R7 nit — merge-branch clause in the Done predicate, optional. 3) Nothing else: citations are
fully grounded and the pointer/reference pair is drift-free.
