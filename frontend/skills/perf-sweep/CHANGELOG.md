# Changelog

## 2026-09-05 · initial release (frontend 2.7.0)
- New skill: route inventory (`routes.json` tagged by surface, canary per surface), `scripts/lh-scoreboard.mjs <dir> [--routes routes.json] [--out scoreboard] [--budgets-out budgets.json]` writing the per-route scoreboard (JSON + markdown: category scores, six metrics, transfer bytes, requests, top 3 failing audits, families) and the family -> audit -> routes cluster table, and seeding preserve-not-regress budget cards in check-speed's `{page, metrics, budget}` shape for `lh-diff --budgets`. Selftest builds the scoreboard from the two fixtures, checks tags, clusters, budget arithmetic and the empty-dir negative control.
