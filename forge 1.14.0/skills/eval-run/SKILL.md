---
name: eval-run
description: >-
  Run the plugin's trigger-eval suites as a fresh-context routing simulation: static validation via
  eval_check.py, then blind fan-out where judges pick a skill (or none) for each prompt given only
  the description menu, then a routing matrix with description-tuning recommendations. Run
  /eval-run [plugin-root, default .]. Read-only; writes only the report.
disable-model-invocation: true
user-invocable: true
argument-hint: "[plugin-root]"
---

# eval-run

eval-run answers one question per suite: **do the descriptions alone route these prompts to the right skill?** It is a routing simulation, not a harness test — real trigger behavior also depends on the live session, the 1% listing budget, and competing skills outside this plugin, so a clean run here is necessary, never sufficient. What it does prove: routing *confusions inside the family*, which is where description tuning actually operates. Root: `$ARGUMENTS` (default `.`).

## Phase 1 — Static gate

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eval_check.py" <every skills/*/evals/evals.json>` and `--coverage <root>`. Any FAIL stops the run — executing a malformed suite produces numbers that mean nothing. Coverage warns are carried into the report, not fixed here.

## Phase 2 — The menu

Build the router's world: every model-invocable skill's `name` + `description`, verbatim, from frontmatter — plus the entry **`none — no skill fires`**. Nothing else: no bodies, no this-conversation context, no knowledge of which suite is under test. The menu is the *only* information a judge receives, because it is the only information the real router has at discovery time.

## Phase 3 — Blind fan-out

One `eval-judge` agent per suite, ≤5 concurrent (the harness-audit ceiling) — the declared agent's empty tool allowlist is the blindness guarantee: a judge that cannot Read cannot peek. Each dispatch carries the menu, that suite's prompts **stripped of their `expect` fields and shuffled**, and this contract:

> For each prompt, answer with exactly one menu entry — the skill whose description you would invoke, or `none`. Output only `id → choice`, one per line. Do not explain, do not hedge with two names, do not infer a theme from the prompt set.

The judge never sees expectations (an answer key in context is a leading question), and never sees which skill's suite it is scoring — the suite's own no-trigger cases must be free to route to their true owners.

## Phase 4 — Scoring

Rejoin choices to expectations mechanically, not by rereading:

- `expect: trigger` → pass iff choice = the suite's skill.
- `expect: no-trigger` → pass iff choice ≠ the suite's skill (`none` and sibling owners both pass; record which).

Build the routing matrix: suite × chosen-skill counts. Every failure is one of three tunable shapes — **stolen** (a sibling won a trigger case: this description is underspecified or the sibling's overreaches), **leaked** (this skill won another suite's no-trigger case: this description overreaches), **dead** (`none` won a trigger case: the prompt's phrasing appears in no description — add it verbatim).

## Phase 5 — Report

```
eval-run · <root> · <passed>/<total> cases · <n> suites clean
Static: <clean | findings carried>   Coverage: <gaps or none>
Matrix: <suite × winner counts, failures only>
Failures: <id · prompt · expected · got · shape (stolen/leaked/dead)>
Tuning: <per shape: the phrasing to add, or the description whose scope to cut — pointed at a file>
```

Every tuning line names the file and the edit direction; recommendations without a target are the report equivalent of a phantom reference. Done when the matrix is printed and each failure carries a shape and a target. NOT done on a summary sentence — the matrix is the deliverable; a prose "mostly routed fine" hides exactly the confusion pairs this command exists to expose.

Judgment boundary: this skill owns *running* evals. Authoring them is `skill-authoring-standards` (the suite conventions live there); a failing suite that needs its skill redesigned routes to `skill-review`.
