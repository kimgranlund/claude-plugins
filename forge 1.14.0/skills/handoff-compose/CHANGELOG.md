# Changelog — handoff-compose

## 2026-07-03 — excellence-campaign batch 2 fixes
Deep-review fixes against `skills-audit/references/standard-of-excellence.md` v2 (ledger: `skills-audit/campaign/batch-2/handoff-compose.findings.jsonl`):
- **A3** foundations §4's rollup count corrected: the coordinator returns the same **eight** fields, not seven; best-practices' `descriptor/site-canon.test.ts` citation marked a project example, not canon.
- **N3** the reviewer seats now have their per-seat note in best-practices (*Files changed* = `(none)` — a critic grades, it does not build; *Evidence* = the gap-map's citations; *Recommended next action* = "maker applies the fix"), and SKILL.md's owner enum widened to include the maker-as-recipient.
- **S3** the house handles adopted in the contract: *Tests/checks run* admits `pass | fail | UNMEASURED — skipped-not-passed` (SKILL.md + best-practices); rubric.md's dimensions typed — `[gate]` H1/H2, `[review]` H3–H5, table and section headers both. (`handoff_check.py` gates field presence/order + the Status enum only — no script change needed; the script is owned by the harness workstream.)
- **S1** the write-once rule stated: a shipped handoff is never edited in place — the recipient may already have routed on it; repair = re-dispatch + re-compose.
- **S5** the consumer-as-critic corollary stated in one clause: the recipient is fresh-context by construction — deliberate, sanctioned by the standard (§S5), not a missing reviewer seat.
- **S2** the description fences back toward orchestration-design: "NOT for designing how the seats compose … this owns only the return block".
- **M2** routing corpus of record checked in (`scripts/routing-corpus.json`, 12 pos / 12 neg) — F1 0.960, recall 1.000, the one grab dispositioned (orchestration-design's verbatim trigger; surface-overlap proxy artifact against fenced territory).
- **L** SKILL.md closes on the done/NOT-done predicate.
