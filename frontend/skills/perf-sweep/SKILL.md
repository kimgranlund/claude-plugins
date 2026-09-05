---
name: perf-sweep
description: >-
  System-wide performance sweep: route inventory, per-route scoreboard, preserve-not-regress
  budgets, cause-family clusters across routes, a canary set for a fast gate and a full nightly
  sweep. Use when the user asks to "audit the whole site", "Lighthouse every route", "build a
  perf scoreboard", "set performance budgets from the baseline", "which pages share this
  failure". NOT for one page's audit (perf-audit), brief (perf-triage), or fix loop
  (perf-fix-loop); NOT for a perceived-latency budget card on one surface (check-speed).
disable-model-invocation: false
user-invocable: true
---

# perf-sweep, the whole product, one scoreboard

A single page's score says nothing about the routes that share its shell. The sweep
enumerates routes, audits the set, clusters failures by cause family so one fix is validated on
every route that has it, and seeds budgets that hold the baseline.

## Procedure

1. **Route inventory.** Enumerate routes from the app's own manifest, router table, or
   sitemap into `routes.json`: `[{"route": "/site/playground/chat", "surface": "playground",
   "canary": true}, ...]`. Tag every route with its surface (docs, playground, examples, app
   shell, marketing); pick one canary per surface. A route list typed from memory is a
   finding, not an inventory.
2. **Audit the set.** Run `perf-audit`'s `lh-run.mjs` per route into one directory
   (`--out perf-reports`), same preset across the set. The canary set runs on every change;
   the full set runs nightly.
3. **Scoreboard.** `node scripts/lh-scoreboard.mjs perf-reports --routes routes.json --out scoreboard --budgets-out budgets.json`
   writes `scoreboard.json` and `scoreboard.md`: per route the category scores, the six core
   metrics, transfer bytes, request count, the top 3 failing audit ids and the cause families;
   then the clusters, family -> failing audit -> routes, largest first.
4. **Budgets.** `budgets.json` is seeded from the baseline as preserve-not-regress: one card
   per route in `check-speed`'s shape (`page`, `metrics`, `budget`), budget = current metric
   plus `lh-brief`'s tolerance, plus the performance score floor and the passing audit ids.
   Unknown keys are ignored by `budget-check.py`, so a card also runs through check-speed's
   own gate unchanged.
5. **Gate per route.** `node ../perf-fix-loop/scripts/lh-diff.mjs --budgets budgets.json perf-reports/*.json`
   compares every report against its card by page path; a metric over budget, a score under
   its floor, or a budgeted passing audit now failing exits 1. A route with no card is a
   reported skip, never a silent pass.
6. **Fix by cluster.** Take the largest cluster (a shared fix, usually transport or build),
   run `perf-fix-loop` on its canary route, then re-run `lh-diff --budgets` over every route in
   the cluster before calling the fix done. Page-local clusters go to `perf-playbook`'s fan-out.
7. **Ratchet.** After a fix lands across the set, re-seed budgets from the new baseline so the
   improvement is held; never loosen a card by hand.

## Done

`routes.json` tagged, a scoreboard for the full set, `budgets.json` seeded, the canary gate
green, and the largest cluster either fixed on every route it touches or named as the next
campaign. NOT done: a scoreboard for the routes that happened to be handy, or budgets edited to
match a regression.

## Provenance

- 1tfjlbk (linked source): the shared-vs-page split ("don't redo shared stuff that was
  already fixed"), the reason clusters are fixed once and validated everywhere.
- 1tewaoi (r/TheFounders): the DO NOT BREAK list the budgets generalise across routes.
- 1taw297 (r/ClaudeCode), commenter: "re-audit only changed surfaces + previous findings", the
  canary-vs-nightly split follows from it.
- No thread runs a multi-route scoreboard or budgets; the inventory, the scoreboard, the
  cluster table, the budget cards, and the canary/nightly split are this repo's additions,
  built on `check-speed`'s existing budget-card shape.
