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

**Estate scoping stops at the detected root — deliberately, not as a gap (issue #957).** The menu never reaches past `<root>/.claude/skills/*`: an installed plugin's skills (e.g. `docs:doc-writing-rules`) never join an estate's menu, even when the live session has that plugin on hand and even when a repo-local skill's own description carries a reciprocal fence naming it. Pulling in "whatever's installed" would break this fan-out's own determinism — installed plugins are a session/environment fact, not something the repo's own tree commits to, so the same suite would grade differently run to run depending on what happens to be installed elsewhere. The consequence is a real, permanent gap in what this fan-out can prove: a reciprocal fence pointing outside the detected root can never be exercised here — the sibling it names is structurally absent from the menu the judge sees, the same category mismatch Phase 3 documents below for command-only suites. Record that on the case itself with a `note` field (the estate's existing re-judge annotation convention, Phase 4 below; schema-tolerant either way — `eval_check.py`'s E1/E2 read only `skill`/`cases`/`id`/`prompt`/`expect`, so an extra key never fails validation) rather than leaving it undocumented case-by-case; the case still runs and still scores against whatever the estate's own menu offers, it just cannot stand as proof of that particular boundary.

## Runner contract

Every `routing-judge` dispatch — Phase 3's fan-out and Phase 4's vote round alike — is an unnamed, synchronous `Agent` tool call: no `name:` parameter, and the call's own return value IS the verdict, never a mailbox delivery to wait on (harness `agent-writing-rules`' never-name rule). The runner executing this skill never yields between issuing a dispatch and collecting its result — the synchronous call already blocks the runner's own turn until the judge returns, so there is nothing "pending" to report and no nudge to wait for; a runner that answers "Judge C reported; judges A and B still pending, nothing to do until they report" has misread its own blocking tool call as background work it structurally is not (issue #959).

**When the caller itself runs this skill as a background `Agent` dispatch** (a marshal's scoped routing pass is the measured case behind issue #959), the runner is now a nested dispatch, and a nested dispatch that names or backgrounds its OWN judge children strands their verdicts at the root session instead of returning them to the runner — the same structural class `dispatch-ticket`'s no-nested-wait rule names for gh#154/gh#157, one level up. The caller's own dispatch prompt for that runner must forbid it from reporting a partial matrix or going idle before Phase 5's report is ready; the unnamed/synchronous shape above is this skill's own contract regardless of caller, so the caller owes only not overriding it with a conflicting "report progress as you go" instruction.

## Phase 3 — Blind fan-out

One `routing-judge` agent per suite **belonging to a model-invocable skill** (`disable-model-invocation` unset or `false`), ≤5 concurrent (the check-everything ceiling) — the declared agent's empty tool allowlist is the blindness guarantee: a judge that cannot Read cannot peek. Each dispatch is unnamed and synchronous (Runner contract above). Each dispatch carries the menu, that suite's prompts **stripped of their `expect` fields and shuffled**, and this contract:

> For each prompt, answer with exactly one menu entry — the skill whose description you would invoke, or `none`. There are exactly N prompts; return exactly N answers, one per id, no id skipped — count your answers before returning. Output only `id → choice`, one per line. Do not explain, do not hedge with two names, do not infer a theme from the prompt set.

(The answer-count clause is metabolized incident 2026-07-09: without it, judges skipped ~1.2% of ids, and every skipped id reads as a false routing failure. A skipped id is not resumed by hand — Phase 4 folds it straight into the contested set below, since a judge that couldn't answer is the same failure mode as a judge that answered wrong.)

**Command-only suites are excluded from this fan-out, never dispatched and never scored (issue #593).** A skill with `disable-model-invocation: true` never enters Phase 2's menu at all (`skill-writing-rules`' Command species: "it never enters model context") — a blind judge picking from that menu structurally cannot select an entry that isn't on it, so every one of that suite's `expect: trigger` cases would read as a permanent, untunable `dead` failure. That's not a description gap the matrix exists to surface; it's a category mismatch between the suite and the simulation, and no amount of tuning fixes it. A command-only skill's suite is verified two other ways instead, neither of them this fan-out: Phase 1's `eval_check.py` static schema pass, which still runs against every `evals.json` handed to it regardless of model-invocability (E1–E5 stay meaningful — id uniqueness, non-empty prompts, honest `skill` ownership, case mix — even though the skill never reaches a menu); and the suite itself, standing as the command's own documented invocation-phrasing record for a human reading the slash menu — never a blind-router proof, since there is no router to simulate for a human-timed entry. Phase 5's report states the excluded count and names each excluded suite, so a shrunk case total is never misread as coverage loss.

The judge never sees expectations (an answer key in context is a leading question), and never sees which skill's suite it is scoring — the suite's own no-trigger cases must be free to route to their true owners.

## Phase 4 — Scoring

Rejoin choices to expectations mechanically, not by rereading:

- `expect: trigger` → pass iff choice = the suite's skill.
- `expect: no-trigger` → pass iff choice ≠ the suite's skill (`none` and sibling owners both pass; record which).

**Contested-case voting round.** Single-judge routing carries measured noise — three consecutive audits on 2026-08-12 found marginal cases flip run-to-run (stolen one pass, clean the next) while load-bearing cases held steady across all three. Before any case's verdict is final, check whether it is contested — any of:

- it failed under the Phase 3 judge just dispatched (a pass/fail per the rules above),
- its evals.json entry already carries a note recording a prior flip (the estate's existing re-judge annotation convention — a note containing wording like "re-judged" or "single-judge noise", e.g. big-change-git-rules t15),
- the Phase 3 judge skipped it outright (the count-miss class, folded in per the Phase 3 note above).

A clean, never-flipped case never gets a second look — voting is scoped to the contested ids only, never the whole suite. Every contested id needs three verdicts before it can be voted, not just two more dispatches: if a Phase 3 verdict exists for it (the first two bullets), dispatch two more `routing-judge` agents against the Phase 2 menu and just the contested ids, same blind contract as Phase 3 (fresh shuffle, expectations stripped, unnamed and synchronous per the Runner contract above) — that Phase 3 verdict plus these two make three. If no Phase 3 verdict exists (the skip bullet — there is nothing to combine with), dispatch three fresh judges for it instead. If a vote-round judge itself skips a contested id, re-dispatch once for that id alone; a second skip stops the wait and the id logs hung with whatever verdicts it has. Once three verdicts exist, the majority (2-of-3) is the case's final choice; if all three differ, log it as a **hung** vote (its own shape, below).

Build the routing matrix: suite × chosen-skill counts, using each case's final (post-vote, where voted) choice. Every failure is one of four tunable shapes — **stolen** (a sibling won a trigger case: this description is underspecified or the sibling's overreaches), **leaked** (this skill won another suite's no-trigger case: this description overreaches), **dead** (`none` won a trigger case: the prompt's phrasing appears in no description — add it verbatim), **hung** (a contested case's three judges split three ways: report it, do not resolve it by fiat — it is evidence the case itself is ambiguous, not a description gap to tune).

## Phase 5 — Report

```
check-routing · <root> · <passed>/<total> cases · <n> suites clean
Static: <clean | findings carried>   Coverage: <gaps or none>
Excluded: <n> command-only suites (schema-checked only, no blind menu — <names>) — or "none"
Matrix: <suite × winner counts, failures only>
Failures: <id · prompt · expected · got · shape (stolen/leaked/dead/hung)> — a voted case marks its tally (e.g. "2-of-3")
Tuning: <per shape: the phrasing to add, or the description whose scope to cut — pointed at a file>
```

Every tuning line names the file and the edit direction; recommendations without a target are the report equivalent of a phantom reference. Hung votes carry no tuning line — there is no file to point at for a 3-way split — report it and stop; chasing it with a description edit is exactly the single-judge-noise-chasing this voting round exists to contain. Done when the matrix is printed and each failure carries a shape, plus a target for every shape but hung. NOT done on a summary sentence — the matrix is the deliverable; a prose "mostly routed fine" hides exactly the confusion pairs this command exists to expose.

## Phase 6 — Persist (single-plugin runs only)

The Phase 4 matrix computes exactly the three numbers `authorkit:attention-audit`'s trend
capture wants (its own `scripts/trend.py --routing-report <path>` reads a JSON shaped
`{"<plugin>": {"dead": n, "stolen": n, "leaked": n}}`) — until this phase existed, check-routing
never wrote them anywhere, so every attention-trend row recorded those columns `absent` (issue
#693). Closing that gap is this phase's only job; it changes nothing about Phases 1-5's own
procedure.

**Plugin-rooted run** (the usual `/check-routing <plugin>` invocation, a `<root>` carrying its
own `.claude-plugin/plugin.json`) → count this run's total failures by shape across every suite
(dead/stolen/leaked; hung is not one of the three tracked columns and is never counted here),
then:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/check-routing/scripts/write_routing_report.py" <plugin-name> \
  --dead <n> --stolen <n> --leaked <n> --out <git-root>/.claude/ops/routing-report.json
```

`<git-root>` is this plugin's enclosing git repository root (`git rev-parse --show-toplevel`),
never `<root>` itself — `<root>` may be the plugin directory or a bare `.claude/skills` tree
(Phase 1), and in either case the workspace's `.claude/ops/` sits above it, not under it.

One stable, non-dated, git-tracked file — never the gitignored `harness-audit-*/` family (that
convention is `check-everything`'s own dated, local-only audit scratch space, per its own
`.gitignore` line; it was never check-routing's own path and stays out of scope here). Each run
overwrites only its own plugin's entry, so the file holds the latest known counts for every
plugin that has ever run this phase, with no dated-directory globbing required on the reading
side. (The script's own on-disk shape also carries an `as_of` date per plugin — the illustrative
JSON above elides it since `trend.py`'s reader ignores extra keys.)

**Estate run** (`--estate`, no single owning plugin) → skip this phase; name it skipped in the
report ("Persist: skipped, estate run has no single plugin key") rather than inventing one.

Done (this phase) when a plugin-rooted run's three counts are written and the report names the
path, or an estate run states the skip plainly.

Judgment boundary: this skill owns *running* evals. Authoring them is `skill-writing-rules` (the suite conventions live there); a failing suite that needs its skill redesigned routes to `check-skill`.
