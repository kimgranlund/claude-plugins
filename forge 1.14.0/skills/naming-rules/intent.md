# intent — naming-rules
status: shipped
species: knowledge
dials: { disable-model-invocation: false, user-invocable: false }
freedom: medium
type: encoded-preference

## trigger
should:      ["what should we name this new skill", "create a naming paradigm that is fisher-price level simple", "is this name too vague", "propose a simple name for this plugin", "review these names for simplicity", "name this agent and the command that dispatches it"]
should_not:  ["why won't my skill trigger", "which plugins should these skills become", "rename this variable"]

## delta
Without this skill, new harness artifacts get legacy-grammar names: synonym sprawl (one
"check" concept spelled review/audit/verify/judge across ~20 estate names), lore heads
(forge, scribe — 12 `-forge` skills for "make"), `decompose` carrying two unrelated meanings,
verb-less runnables (`build`, `feature`, `issue`), and skill↔agent twins that share one name
(`ops-issues` ×2). Evidence: the 2026-07-20 full-estate review (references/estate-rename-map.md).
With it, a proposed name passes five checkable tests (completes "I want to ___", kind audible
in shape, registry verb, no lore, loud sibling contrast).

## fences
- NOT for the legacy estate grammar as currently enforced (skill-authoring-standards / agent-authoring-standards §Naming, corpus Vol 2)
- NOT for executing renames across an estate (a campaign — git-campaign-workflows, ADR-0002; names are APIs)
- NOT for deciding plugin partitioning (plugin-decompose)
- NOT for code identifiers — variables, functions, classes (general engineering, no skill)

## assertions
1. Every proposed runnable name is verb-first and completes "I want to ___" read aloud.
2. Proposed names draw verbs only from the registry table; lore verbs (forge, audit, synthesize, decompose, harvest, orchestrate) appear only as counter-examples.
3. A knowledge-name proposal ends in `-facts` or `-rules`, and `-rules` carries its activity (`doc-writing-rules`, never `doc-rules`).
4. A skill↔agent twin is proposed as verb↔noun of the same words (`sort-issues` ↔ `issue-sorter`).
5. No proposed name contains `claude`/`anthropic` (install-rejected, lint F8).

## gates
P0 route:      PASS 2026-07-20 — knowledge needed on demand; not mechanically checkable (hook), not always-true-every-turn (entry file), no tool walls needed (agent)
P1 intent:     PASS 2026-07-20 — paradigm + plugin layer confirmed by user in session ("ok I like that"); refinements from user's doc-rules vagueness note
P2 evals:      PASS 2026-07-20 — evals.json (15 trigger / 7 no-trigger) + 5 assertions + 3 fresh-context baselines (b1: `contrast-verify`, b2: `issue-triage` twin, b3: `doc-authoring-standards` — all legacy-grammar, delta demonstrated)
P3 draft:      PASS 2026-07-20 — SKILL.md (knowledge skeleton, dials explicit, ~120 lines) + references/estate-rename-map.md
P4 language:   PASS 2026-07-20 — potency_lint within budget (nevers 4→2 after affirmative rewrite of test 5 + one lock dedup); L1 self-check: declarative catalog, zero imperatives, contrasts labeled
P5 validate:   PASS 2026-07-20 — skill_lint clean; fresh-context skill-auditor FLOOR verdict PASS (0 blocking / 0 major / 2 minor / 1 nit; minors fixed same change: fence citation repointed to agent-authoring-standards §Naming + skill_lint's checkable slice, two drift-pair restatements compressed to rule + owner pointer; nit accepted, see rulings); behavior check 3/3 with-vs-without (contrast-verify → check-contrast · issue-triage×2 → /sort-issues ↔ issue-sorter · doc-authoring-standards → doc-writing-rules); assertion-5 grep clean over all proposals; reciprocal fences closed in 4 sibling suites (skill-/agent-authoring-standards, git-campaign-workflows, plugin-decompose)

## rulings
- Species/dials chosen from the standards' species table (knowledge → model-only) without a live
  user confirm — session ran autonomously; flagged in the PR for override.
- llm plugin recorded as `llm-facts` (truer to contents) over user's proposed `llm-protocols`;
  open for override, noted in the estate map.
- Estate rename map ships as a worked example under references/ — it is review output, NOT a
  ratified rename campaign; executing it needs its own ADR + campaign branch.
- Open member-map rows the user has not ruled on: `checker-rules`, `chore-lead`/`sweep-chores`,
  `where-agents-live`, `break-down-*` — marked ⚠ in the map.
- Auditor nit accepted: the name `naming-rules` self-instantiates the new paradigm inside a
  legacy-grammar estate (legacy-conformant would be `naming-standards`) — deliberate
  self-demonstration; the skill is the paradigm's first artifact.
- Description-tier fix (fence citation) lands in this same change per the edit ladder.
- Wave-boundary eval-run executed 2026-07-20 (user: "proceed"): first pass 21/22 — n05 ("why are
  our existing naming conventions structured the way they are") leaked to naming-rules; fence
  rewritten to name the EXISTING-estate question explicitly; re-judge 22/22 clean.
