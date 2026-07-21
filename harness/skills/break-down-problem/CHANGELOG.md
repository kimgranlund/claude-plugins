# Changelog — system-decompose

Format: [Keep a Changelog](https://keepachangelog.com/). Versioning: [SemVer](https://semver.org/).

## [0.2.0] — 2026-07-03

Excellence-campaign batch-3 fix wave (spine skill — template escalation applied). Ledger:
`skills-audit/campaign/batch-3/system-decompose.findings.jsonl`.

### Changed
- **Description (M2/S2)** — the "for a UI layout use layout-decompose…" parenthetical parsed as
  POSITIVE routing tokens (measured grabs 0.40–0.60); rewritten as real NOT-for fences
  (layout-decompose · component-author · flow-decompose · prd/spec/lld-author · intent-grill),
  the body's signature symptoms hoisted into the triggers ("actions with no home", "needs that have
  nowhere to live", "acceptance criteria that don't map to any task"), and the crossing named up
  front ("the node tree hosts the action set"). routing_eval: F1 0.741 → 0.963 (recall 1.000) on
  the checked-in corpus.
- **`references/layout.md` + `references/components.md` (A3)** — were diverged shallow twins of
  [[layout-decompose]]'s and [[component-author]]'s canon; reduced to a declared-canon pointer +
  the manifest-schema adapter that is genuinely this skill's own (restated ladders and the geometry
  formula deleted; worked manifests kept byte-identical).
- **`references/ux-architecture.md` (S2)** — its `journey → flows → …` axis claimed
  [[flow-decompose]]'s charter; re-scoped to within-product IA (`product → sections → screens →
  states`) with the journey handed across, and the worked pass's hosting-vs-justify contradiction
  fixed (prose now matches its own manifest: `sent-screen` hosts no task, `justify:"confirmation"`).
  Reciprocal flow-decompose edge added under the SKILL.md domain table.
- **`references/technical-architecture.md` (A3)** — dangling repo-relative LLD pointer relativized
  to the project's `.claude/docs/llds/`.
- **`scripts/coverage_check.py` (A4/S3)** — now selftest-locked: `coverage_check.py selftest` runs
  one passing fixture, one mutation per emitted code (UNHOSTED · DANGLING · DUP-ID · EDGE-DANGLING ·
  EDGE-CYCLE · NO-ACCEPT · UNJUSTIFIED-LEAF · EDGE-UNJUSTIFIED), a negative control proving the
  suppressors (justify/why/accept) suppress, and the exit-tier semantics. Verdict labels renamed
  FAIL/WARN → **gate/advisory** (exit codes unchanged). Behavior verified byte-identical on the five
  embedded reference manifests (plain + `--strict`) before/after.
- **SKILL.md (S1/S3/S5)** — added the species organs: a Modes line (DECOMPOSE · PLAN `plan:true` ·
  STRICT `--strict`), a Report block (quadrant verdict + per-plane findings), and a closing Verify
  Target (done/NOT-done); the manifest named as this skill's card; the fresh-context critic named
  (`doc-reviewer` agent). `references/_template.md` extended with the same organs (canon-check
  first, manifest-adapter form, done/NOT-done close) so new domains don't stamp the gaps.

### Added
- **`scripts/routing-corpus.json`** — the M2 test of record (13 positives / 12 negatives drawn from
  the graph neighbors' trigger vocabulary).

## [0.1.0] — 2026-06-26

Initial cut (predates this changelog). The generic two-plane decomposition spine: OUTSIDE-IN ×
INSIDE-OUT, the defect quadrant (UNHOSTED / UNJUSTIFIED-LEAF), five domain references
(layout · components · technical-architecture · ux-architecture · goals), `coverage_check.py`
(the deterministic coverage gate incl. plan-mode NO-ACCEPT and build-order EDGE checks),
`references/` method/foundations/best-practices/rubric, and the `_template.md` domain factory.
