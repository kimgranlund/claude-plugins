# Changelog — rubric-author (formerly authoring-rubrics)

## 2026-07-03 — excellence-campaign batch 2 fixes
Deep-review fixes against `skills-audit/references/standard-of-excellence.md` v2 (ledger: `skills-audit/campaign/batch-2/rubric-author.findings.jsonl`):
- **S2** description gains its outbound fence: NOT for the skill/agent carrying the rubric (skill-author / agent-author) nor the /goal loop itself (loop-design — this skill owns only the completion condition's quality).
- **M2** the rubric's own vocabulary added to the triggers ("which dimensions should gate promotion and at what threshold", "re-anchor this rubric — the artifact standard changed", "the level descriptors are vague — fix the anchors"); routing corpus of record checked in (`scripts/routing-corpus.json`, 12 pos / 12 neg) — F1 0.880, every miss/grab read and dispositioned (all proxy artifacts; fences intact).
- **A3** `references/rubric.md`'s dead `README.md` pointer removed — scoring method + promote rule are self-contained; corpus-level severity ordering repointed to the standard-of-excellence.
- **S5** the generator ≠ critic rule now names its critic: Evaluate dispatches the shared **doc-reviewer** agent (standalone rubrics are in its charter) instead of an unowned "independent read".
- **L** SKILL.md closes on the done/NOT-done predicate.
