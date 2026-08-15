---
name: check-routing
description: >-
  Run a plugin's trigger-eval suites, or a project ESTATE's (no plugin manifest — a bare
  `.claude/skills/*/evals/` tree, auto-detected), as a blind routing simulation: a no-tools
  judge picks from the description menu, then a routing matrix with tuning targets
  (stolen/leaked/dead). Use to rerun the evals, or prove routing after a description edit,
  in either a plugin or a project estate. NOT for authoring a suite's cases or live trigger
  debugging (skill-writing-rules); NOT for judging a skill's content (check-skill); NOT for
  the release gate (ship-plugin).
disable-model-invocation: false
user-invocable: true
argument-hint: "[root] [--estate]"
---

# check-routing

check-routing answers one question per suite: **do the descriptions alone route these prompts to the right skill?** It is a routing simulation, not a harness test — real trigger behavior also depends on the live session, the 1% listing budget, and competing skills outside the detected root, so a clean run here is necessary, never sufficient. What it does prove: routing *confusions inside the family*, which is where description tuning actually operates. Root: `$ARGUMENTS` (default `.`).

Two target conventions, auto-detected from `<root>` — never a separate command, never a separate skill:

- **Plugin** — `<root>/skills/*/evals/` (a `.claude-plugin/plugin.json` sibling is the usual signal but not required; the pre-existing behavior, unchanged).
- **Project estate** — no `<root>/skills/` tree, but a project's own `.claude/skills/*/evals/` tree (the convention `overhaul-execute`/`overhaul-planning` rely on for a repo that isn't a plugin, e.g. agent-ui's own `.claude/` — issue #253). Pass `--estate` to force this convention on a root that happens to carry both.

Everything past Phase 1 is convention-blind: a menu of name+description pairs and a judge that never learns which tree they came from.

## Phase 1 — Static gate

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eval_check.py" <every evals.json under the detected skills root>` and `--coverage <root> [--estate]` — the script does the same plugin-vs-estate detection (`detect_skills_root`) so this phase and Phase 2 always agree on which tree they're reading. Any FAIL stops the run — executing a malformed suite produces numbers that mean nothing, and E7 (neither convention found under `<root>`) is exactly that. Coverage warns (E6) are carried into the report, not fixed here.

## Phase 2 — The menu

Build the router's world: every model-invocable skill's `name` + `description`, verbatim, from frontmatter, under the same detected skills root as Phase 1 (`<root>/skills/` for a plugin, `<root>/.claude/skills/` for an estate) — plus the entry **`none — no skill fires`**. Nothing else: no bodies, no this-conversation context, no knowledge of which suite is under test. The menu is the *only* information a judge receives, because it is the only information the real router has at discovery time. An estate has no single plugin name to load a menu from — the menu IS the estate's own skill set, discovered the same way.

## Phase 3 — Blind fan-out

One `routing-judge` agent per suite, ≤5 concurrent (the check-everything ceiling) — the declared agent's empty tool allowlist is the blindness guarantee: a judge that cannot Read cannot peek. Each dispatch carries the menu, that suite's prompts **stripped of their `expect` fields and shuffled**, and this contract:

> For each prompt, answer with exactly one menu entry — the skill whose description you would invoke, or `none`. There are exactly N prompts; return exactly N answers, one per id, no id skipped — count your answers before returning. Output only `id → choice`, one per line. Do not explain, do not hedge with two names, do not infer a theme from the prompt set.

(The answer-count clause is metabolized incident 2026-07-09: without it, judges skipped ~1.2% of ids, and every skipped id reads as a false routing failure. A skipped id is not resumed by hand — Phase 4 folds it straight into the contested set below, since a judge that couldn't answer is the same failure mode as a judge that answered wrong.)

The judge never sees expectations (an answer key in context is a leading question), and never sees which skill's suite it is scoring — the suite's own no-trigger cases must be free to route to their true owners.

## Phase 4 — Scoring

Rejoin choices to expectations mechanically, not by rereading:

- `expect: trigger` → pass iff choice = the suite's skill.
- `expect: no-trigger` → pass iff choice ≠ the suite's skill (`none` and sibling owners both pass; record which).

**Contested-case voting round.** Single-judge routing carries measured noise — three consecutive audits on 2026-08-12 found marginal cases flip run-to-run (stolen one pass, clean the next) while load-bearing cases held steady across all three. Before any case's verdict is final, check whether it is contested — any of:

- it failed under the Phase 3 judge just dispatched (a pass/fail per the rules above),
- its evals.json entry already carries a note recording a prior flip (the estate's existing re-judge annotation convention — a note containing wording like "re-judged" or "single-judge noise", e.g. big-change-git-rules t15),
- the Phase 3 judge skipped it outright (the count-miss class, folded in per the Phase 3 note above).

A clean, never-flipped case never gets a second look — voting is scoped to the contested ids only, never the whole suite. Every contested id needs three verdicts before it can be voted, not just two more dispatches: if a Phase 3 verdict exists for it (the first two bullets), dispatch two more `routing-judge` agents against the Phase 2 menu and just the contested ids, same blind contract as Phase 3 (fresh shuffle, expectations stripped) — that Phase 3 verdict plus these two make three. If no Phase 3 verdict exists (the skip bullet — there is nothing to combine with), dispatch three fresh judges for it instead. If a vote-round judge itself skips a contested id, re-dispatch once for that id alone; a second skip stops the wait and the id logs hung with whatever verdicts it has. Once three verdicts exist, the majority (2-of-3) is the case's final choice; if all three differ, log it as a **hung** vote (its own shape, below).

Build the routing matrix: suite × chosen-skill counts, using each case's final (post-vote, where voted) choice. Every failure is one of four tunable shapes — **stolen** (a sibling won a trigger case: this description is underspecified or the sibling's overreaches), **leaked** (this skill won another suite's no-trigger case: this description overreaches), **dead** (`none` won a trigger case: the prompt's phrasing appears in no description — add it verbatim), **hung** (a contested case's three judges split three ways: report it, do not resolve it by fiat — it is evidence the case itself is ambiguous, not a description gap to tune).

## Phase 5 — Report

```
check-routing · <root> · <passed>/<total> cases · <n> suites clean
Static: <clean | findings carried>   Coverage: <gaps or none>
Matrix: <suite × winner counts, failures only>
Failures: <id · prompt · expected · got · shape (stolen/leaked/dead/hung)> — a voted case marks its tally (e.g. "2-of-3")
Tuning: <per shape: the phrasing to add, or the description whose scope to cut — pointed at a file>
```

Every tuning line names the file and the edit direction; recommendations without a target are the report equivalent of a phantom reference. Hung votes carry no tuning line — there is no file to point at for a 3-way split — report it and stop; chasing it with a description edit is exactly the single-judge-noise-chasing this voting round exists to contain. Done when the matrix is printed and each failure carries a shape, plus a target for every shape but hung. NOT done on a summary sentence — the matrix is the deliverable; a prose "mostly routed fine" hides exactly the confusion pairs this command exists to expose.

Judgment boundary: this skill owns *running* evals. Authoring them is `skill-writing-rules` (the suite conventions live there); a failing suite that needs its skill redesigned routes to `check-skill`.
