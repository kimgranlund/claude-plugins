# forge — the skill-authoring family

One plugin, one domain (`skill-*`), every artifact type doing its own job:

> You run **`/skill-forge`**, which interviews for intent, applies **`skill-authoring-standards`**, and drafts the skill; **`skill-postwrite-invocation-lint`** objects to every malformed write until the frontmatter validates; the **`skill-auditor`** — preloading **`skill-review`** and the standards — reports findings from a fresh context; the forge ships when all six gates read PASS.

And the control plane's other surfaces get the same treatment: **`/agent-forge`**, **`/hook-forge`**, **`/script-forge`**, and **`/entry-file-audit`** author against **`agent-authoring-standards`**, **`hook-authoring-standards`**, **`script-authoring-standards`**, and **`entry-file-standards`**; **`/harness-audit`** runs the outer loop — lint sweep, standards-preloading fan-out, terminal triage — over the whole surface on a cadence.

The plugin name (`forge`, distribution taxonomy) is deliberately disjoint from the domain prefix (`skill-`, domain taxonomy), so packaging renames nothing: `/forge:skill-review` locally shortens to `/skill-review`.

## Map

| Artifact | Type | Invocation | Job |
|---|---|---|---|
| `skills/skill-authoring-standards` | Declarative skill | model-only | **The core artifact**: species, frontmatter discipline, body prose style, calibration, verified numbers (July 2026) |
| `skills/skill-forge` | Orchestrator skill | user-only (`/skill-forge`) | Six gated phases: route → intent interview → evals-first → draft → language pass → validate → ship |
| `skills/skill-review` | Procedural skill | both | Judgment-tier audit (R1–R8) with a schema'd report contract |
| `agents/skill-auditor` | Agent | spawned | Fresh-context reviewer; preloads skill-review + standards; returns report by file |
| `skills/linguistic-techniques` | Declarative skill (hybrid) | model-only | The language layer beneath every prompt-carrying artifact: twelve techniques, potency rubric (L1–L10), `potency_lint.py`; skill-forge Phase 4 runs its Audit |
| `skills/intent-extract` | Procedural skill | both (`/intent-extract`) | Root-intent extraction: literal ask vs goal, delta taxonomy, batched multiple-choice forks, the Resolved Intent contract |
| `skills/open-questions-sweep` | Procedural skill | both (`/open-questions-sweep`) | Clears a session's backlog of unresolved items — an unanswered question, an unconfirmed assumption, a stray idea left undecided — into one batched AskUserQuestion round instead of a prose dump nobody actually resolves |
| `skills/system-decompose` | Procedural skill | both (`/system-decompose`) | Two-plane decomposition (OUTSIDE-IN × INSIDE-OUT) with five domain references and the deterministic `coverage_check.py` gate |
| `skills/agent-authoring-standards` | Declarative skill | model-only | Agent files: thin-shell law, preload semantics, tool walls, cold-start language; doubles as fan-out audit criteria |
| `skills/agent-forge` | Command | user-only (`/agent-forge`) | Fork-vs-agent gate → dispatch interview → thin-shell draft → language pass → lint + spawn smoke test |
| `skills/hook-authoring-standards` | Declarative skill | model-only | The check tier: routing test, event/output semantics, hook discipline, repair-affordance messages |
| `skills/hook-forge` | Command | user-only (`/hook-forge`) | Check-vs-judgment gate → interview → script + registration (selftest mandatory) → simulated-event validation |
| `skills/script-authoring-standards` | Declarative skill | model-only | The deterministic tier: script anatomy, the selftest contract (negative control that bites, exit tri-state 0/1/2-skip), placement and pathing, the arithmetic-not-judgment boundary; canon for the audits' A4 dimension |
| `skills/script-forge` | Procedural skill | both (`/script-forge`) | Mechanize a hand-run check or prose checklist as `scripts/taskname.py\|mjs`: qualify → plan → confirm → author to the standard → validate (selftest green, negative control bites, caller wired, G4 sweeps it) |
| `skills/entry-file-standards` | Declarative skill | model-only | CLAUDE.md residency test, the routing table for evictions, the growing-dotfile physics |
| `skills/entry-file-audit` | Command | user-only (`/entry-file-audit`) | Classify every line → approval → migrate (landing artifact first) → cut → verify |
| `skills/harness-audit` | Orchestrator | user-only (`/harness-audit`) | Wave 2: inventory → lint sweep → standards-preloading fan-out → boundary-validated aggregation → terminal triage with three-strikes promotion |
| `skills/plugin-authoring-standards` | Declarative skill | model-only | Plugins: atomic load, version-as-cache-key, reload semantics, paths/state, trust; the three load-failure classes as a ledger |
| `skills/plugin-onboard` | Procedural | both (`/plugin-onboard`) | Declare external plugins/marketplaces in a repo's `.claude/settings.json` (`extraKnownMarketplaces` + self-hosted marketplace.json wrapper for bare plugin repos) so contributors who trust the repo get the install prompt — portable past the authoring machine |
| `skills/plugin-release` | Command | user-only (`/plugin-release`) | Preflight (bump on approval) → release_gate.py → package to dist/ → report |
| `skills/repo-alignment` | Command skill | user-only (`/repo-alignment`) | Phased, evidence-driven, human-checkpointed alignment campaign for a drifted repo: inventory/reconcile → unify duplicates → orphan manifest → schema + standing guards → audit verdicts → work-package execution → lessons distillation; adopted 2026-07-12 from the user's proven repo-recalibrate; delegates canonical-map corpus relocation to scribe's `/docs-alignment` |
| `skills/git-campaign-workflows` | Declarative skill | model-only | The estate's own git operational lessons, citable: worktree placement/discard safety, merge semantics (the ten-branch delete-failure class), the silent-failure catalog (verify by re-reading, never a command's print), parallel-session reconcile, the ADR-0002 decision tree — five axes, each grounded in a dated 2026-07-16/17 incident; the three scripts below mechanize what it documents |
| `skills/github-issue-pr-primitives` | Declarative skill | model-only | GitHub's own Issue/PR/Discussion/Projects-v2 platform facts, cited and dated 2026-07-17 — deliberately disjoint from git-campaign-workflows (that pack is OUR git mechanics; this one is GitHub's data model): Issue Types + Issue Fields vs. labels, sub-issues vs. the retired tasklist-block feature, the nine closing keywords and the one merge-strategy gap GitHub's own docs never closed, PR review/CODEOWNERS/merge-queue mechanics, Projects v2's GraphQL-only structure — seven axes plus a sources.md provenance file; the synthesis axis names where this workspace's own ADR-0002/doc-authoring-standards convention aligns or diverges from the platform, without ratifying a change |
| `skills/naming-rules` | Declarative skill | model-only | The simple ("Fisher-Price") naming paradigm for NEW harness artifacts: five checkable tests (says-the-job, kind-audible, registry-verb, no-lore, loud-contrast), a per-kind shape table, the one-verb-per-concept registry; coexists with the legacy grammar (the `*-authoring-standards` §Naming sections keep governing shipped names — names are APIs); the full-estate rename map ships as an illustrative worked example at `references/estate-rename-map.md`, explicitly not a ratified plan |
| `agents/ops-issues` | Agent | spawned (scheduled + on-demand) | Standing intake/triage seat: classifies, dedupes, and routes features/bugs/tasks/issues/PRs onto the resolved ticketing backend per the watch/triage/trust SPEC (`.claude/docs/spec/spec-ticketing-watch-triage.md`); trust-gates unknown filers behind a durable friendlies allow-list; structurally barred from source edits, merges, or closes beyond the ticket record. Preloads `github-issue-pr-primitives` + `intent-extract` only — scribe's `doc-authoring-standards` is a different plugin, so the TICKET shape it needs is stated inline rather than preloaded (the hard plugin-preload boundary, not a soft mention) |
| `skills/ops-issues` | Command skill | user-only (`/ops-issues`) | Dispatches the `ops-issues` agent above for an on-demand run; states the agent's own capture/author-only contract as a fixed banner before the first CONFIRMED-roster dispatch (never mere file existence — an unattended firing seeds the allow-list too, evidence-only), and — since the agent has no `AskUserQuestion` of its own — runs the REQ-011/REQ-013 interview here, in this command's own session, whenever the agent's report surfaces one pending. This workspace's first case of a skill and an agent sharing one name (a command dispatching its own-named standing seat), deliberate, not yet a rule |
| `agents/ops-repo` | Agent | spawned (scheduled + on-demand) | Standing repo-hygiene seat: inventories worktrees/branches/PRs, executes cleanup ONLY through this plugin's own gated scripts (`campaign_close.py`/`gitignore_check.py`/`sync_main.py`) on independently-verified-merged findings, proposes (never mutates) everything else. Preloads `git-campaign-workflows` + `github-issue-pr-primitives` |
| `agents/ops-adr` | Agent | spawned (scheduled + on-demand) | Standing periodic ADR-review seat: `scripts/adr_checkpoint.py` diffs the ADR corpus by content hash since the last firing (new/amended/newly-superseded, cost proportional to the delta not the corpus), each changed Decision judged against `knowledge-harvest`'s own bar, candidates queued via `scripts/adr_queue.py` for ONE batched confirm round rather than blocking on a live human; structurally barred from authoring — a confirmed candidate's next step is a named `/pack-forge`/`/skill-forge`/`knowledge-harvest` Phase-6 command, never a write this agent performs. Preloads `knowledge-harvest` + `pack-authoring-standards` (both same-plugin) — scribe's `doc-authoring-standards` is a different plugin, so the ADR frontmatter contract (`doc-type`/`id`/`status`/`supersedes`) is stated inline rather than preloaded |
| `agents/ops-orchestrator` | Agent | spawned (on-demand) | Standing sweep coordinator for the ops-* family: fans out ops-adr + ops-issues + ops-repo in parallel (or a scoped subset), hands the returned handoffs to ops-planner, relays the queue plus per-seat status (returned · UNMEASURED · refused); Read+Task allowlist — coordination is its entire surface, a zero-return sweep never dispatches the planner. Preloads `handoff-compose` |
| `agents/ops-planner` | Agent | spawned (on-demand + by ops-orchestrator) | The ops-family prioritization seat: turns seat reports (sweep mode) or durable `.claude/ops` state + live `gh` evidence (standalone) into ONE prioritized queue at `.claude/ops/plan.md` — every entry action·owner·evidence·size, the prior plan read on every dispatch as the carry-forward source, never evidence; fable+high (a queue verdict never rides the caller's tier). Preloads `handoff-compose` + `github-issue-pr-primitives` |
| `skills/ops-orchestrator` | Command skill | user-only (`/ops-orchestrator`) | Dispatches the ops-orchestrator agent above for an on-demand sweep — the /ops-issues same-name pairing; banner-before-dispatch on the shared first-queue marker (`.claude/ops/plan.md` absent — the sweep itself creates that file, so the check precedes the dispatch), scope instructions passed verbatim, single-seat asks redirected to their direct door |
| `skills/ops-planner` | Command skill | user-only (`/ops-planner`) | Dispatches the ops-planner agent above standalone — same pairing; banner-before-dispatch on the same marker, focus instructions passed verbatim (an emphasis, never a new entry contract), fresh-sweep asks redirected to `/ops-orchestrator` |
| `scripts/release_gate.py` | Script | CLI + selftest | G1–G11: manifest, structure, full lint (composes skill_lint), bundled selftests (py+js, exit tri-state), phantom sweep, package + same-version refusal, eval validation (composes eval_check), sibling names, packs (composes corpus_check), docs freshness (composes docs_check), style lint (ruff/eslint, ADR-0002) |
| `skills/eval-run` | Procedural skill | both (`/eval-run`) | Blind fresh-context routing simulation over the eval suites: menu → fan-out → routing matrix → tuning targets (stolen/leaked/dead); model-invocable since 1.41.0 (per explicit user direction, the 1.24.0 skill-forge precedent) so "prove the routing" asks fire it directly |
| `skills/skill-decompose` | Procedural | both (`/skill-decompose`) | Imported family (source-corpus lineage): four evidence tests deciding whether a knowledge corpus splits — manifest + repair map or an honest no-split; `manifest_check.py` as gate |
| `skills/skill-synthesize` | Procedural | both (`/skill-synthesize`) | The formal inverse: four inverse tests + the skill-decompose self-check deciding a merge; `consolidation_check.py` as gate |
| `skills/skill-refactor` | Command | user-only (`/skill-refactor`) | The executor sibling: applies validated decompose/synthesize manifests — plan→approve→apply→sweep proof; `refactor_apply.py` attics, never deletes |
| `skills/plugin-forge` | Orchestrator | user-only (`/plugin-forge`) | Domain → released plugin: the four decomposition tests run forward as design gates, family manifest ratified before scaffold, per-member forge loop, fence-graph closure, /eval-run proof |
| `skills/pack-authoring-standards` | Declarative skill | model-only | Corpus doctrine: ask-shaped files, 3–7 axes, INDEX contract, grounding markers, research waves, snapshot freshness |
| `skills/pack-forge` | Command | user-only (`/pack-forge`) | Question-led research waves, one axis per wave: charter → question set → dated gather → distill → register → corpus_check |
| `scripts/corpus_check.py` | Script | CLI + selftest + hook (INDEX writes) + gate G9 | K1–K5: INDEX↔tree both directions, load budgets, grounding coverage, axis count |
| `skills/plugin-decompose` | Procedural | both (`/plugin-decompose`) | Distribution-layer partitioning: jobs-to-be-done clustering, hard/soft dependency edges, namespace separability, lifecycle ledger → 1–5 plugin manifest for /plugin-forge; `surface_map.py` extracts the graph, kills hard-edge cuts, and surfaces negative space (`gaps`: dangling references + family matrix) |
| `skills/reasoning-orders` | Declarative skill | model-only | The n-order spectrum operationalized: escalation triggers, forge-scale worked cases per order, the rent rule (higher-order claims pay in checks and numbers), anti-pattern table (order cosplay, tidying-as-transformation) |
| `agents/eval-judge` | Agent | dispatch-only (/eval-run) | Blind routing judge; empty tool allowlist as the epistemic guarantee — cannot read what it must not see |
| `agents/pack-researcher` | Agent | dispatch-only (/pack-forge) | Gather-phase researcher; WebSearch/WebFetch/Read/Write only, preloads pack-authoring-standards; the allowlist enforces gather≠distill |
| `skills/handoff-compose` | Declarative skill (hybrid) | both | The team-report layer beneath every agent dispatch: Status·Summary·Files changed·Tests/checks run·Evidence·Risks·Open questions·Recommended next action, `handoff_check.py` as the mechanical gate; every reviewer agent below returns through it |
| `agents/agent-reviewer` | Agent | spawned | Fresh-context critic for one subagent file; preloads agent-authoring-standards + handoff-compose; gates on skill_lint's A1-A5 |
| `agents/hook-reviewer` | Agent | spawned | Fresh-context critic for one hook (registration + handler pair); preloads hook-authoring-standards + handoff-compose; gates on skill_lint's H1-H5, probes stdin adversarially |
| `agents/plugin-reviewer` | Agent | spawned | Fresh-context critic for one plugin's packaging; preloads plugin-authoring-standards + handoff-compose; gates on release_gate's G1-G10, holds the content boundary |
| `agents/linguistics-reviewer` | Agent | spawned | Fresh-context critic for the language layer of any prompt-carrying artifact; preloads linguistic-techniques + handoff-compose; leads with the instantiate-over-describe test |
| `skills/agents-audit` | Declarative skill | both | The estate-level sibling to harness-audit's outer loop: CORPUS pass (naming/language/frontmatter/skill-leverage, one sweep, `agent_corpus_index.py`) + DEEP-review CAMPAIGN (M1/M2/N/A/L/S dimensions against `references/standard-of-excellence.md`, portfolio verdicts); `agent-reviewer` and `skill-auditor` gained a DEEP tier to serve this campaign |
| `skills/skills-audit` | Declarative skill | both | The skill-corpus counterpart: CORPUS pass (naming/language/frontmatter/peer-composition, `corpus_index.py`) + DEEP-review CAMPAIGN against its own `references/standard-of-excellence.md`; ported alongside `harness_checks.py` + `routing_eval.py`, the shared M1/M2 gate scripts both audits depend on |
| `scripts/docs_check.py` | Script | CLI + selftest + gate G10 | R1–R5: README/MANUAL cover every skill, ledger version = manifest version, CLAUDE.md counts, script mentions — docs freshness as a ship invariant, deliberately not a per-write hook |
| `scripts/gitignore_check.py` | Script | CLI + selftest | G1/G2: a `.gitignore` rule matching nothing in the tree is stale (retire it); a known generated/tool-output dir (`.claude/worktrees`, `dist`, `__pycache__`, …) existing on disk with no ignore coverage is one `git add -A` from being committed — repo-alignment's razor, mechanized |
| `scripts/campaign_close.py` | Script | CLI + selftest | The post-merge ritual, mechanized: PR state == MERGED (never touch the branch otherwise) → delete the remote branch AND REVERIFY it's gone (the ten-branch silent-delete-failure class, 2026-07-16) → gate the touched plugins (warn, not fail) |
| `scripts/sync_main.py` | Script | CLI + selftest | Pulling onto a possibly-dirty main without clobbering a parallel session: classify dirty-vs-incoming overlap → quarantine as a named stash → `--ff-only` pull → reverify HEAD by SHA (never trust a command's print alone — the 2026-07-17 truncated-pipe incident) |
| `scripts/adr_checkpoint.py` | Script | CLI + selftest | Cheap, deterministic ADR-corpus diff by content hash against a checkpoint: new / amended / newly-superseded (read from `supersedes:` frontmatter, never inferred from prose) / unchanged — cost stays proportional to what changed, never to corpus size; `ops-adr`'s only economic lever |
| `scripts/adr_queue.py` | Script | CLI + selftest | Durable held-queue for ADR-review candidates: append-or-update by (adr, kind) — a re-detected candidate updates in place, never duplicates — so a scheduled firing never blocks on a live human; one batched confirm round clears however many accumulated |
| `scripts/eval_check.py` | Script | CLI + selftest | E1–E6: suite schema, id/owner identity, prompt dedup, case-mix floors, plugin-wide coverage |
| `hooks/hooks.json` + `scripts/skill_lint.py` | Hook + script | fires on `Write\|Edit` of any `SKILL.md`, `agents/*.md`, or `hooks.json` | Check tier: skill F/W rules; agent A1–A5 (YAML shape, thin shell, allowlist); hooks H1–H5 (wrapper, shape, portable paths); CLAUDE.md C1–C2 in CLI mode only |

Check/judgment split by design: everything mechanically decidable lives in `skill_lint.py` (run `python3 scripts/skill_lint.py selftest` to prove the counters); `skill-review` scores only what requires a model.

## Evals

Every model-invocable skill carries `evals/evals.json` — should-trigger prompts from its description's phrasings plus near-miss should-nots aimed at the sibling that owns them, so the suites double as routing regressions for the whole family. Run them via skill-creator's description-tuning loop or the fresh-session baseline procedure in `skill-authoring-standards`.

For a human-facing guide to every skill with example prompts, see `MANUAL.md` (ships in the artifact; the harness never loads it).

## Developing forge itself

The repo carries its own dev harness: a root `CLAUDE.md` (invariants + map for Claude Code sessions editing this repo) and `.claude/settings.json` registering the same post-write lint repo-locally — so the guard fires even when the plugin isn't installed. Both are excluded from the packaged `.plugin` (gate G6): dev harness is not a distribution component. Suites in `skills/*/evals/evals.json` are now also linted at write time via the hook (E-rules delegated to `eval_check.py`).

## Install

```bash
# local development
claude --plugin-dir /path/to/forge

# or install the packaged .plugin / add to a marketplace, then
/plugin install forge
/reload-plugins
```

After installing into a large skill library, run `/doctor` — descriptions share a 1%-of-context listing budget.

## Load-bearing facts encoded here (verified 2026-07, drift-prone)

- **`disable-model-invocation: true` blocks subagent preloading** (and scheduled tasks, v2.1.196+). Preloadable modules are therefore *model-only* (`user-invocable: false`), which is exactly how `skill-authoring-standards` and `skill-review` are flagged. The "both flags = library-only preload module" pattern is falsified — both flags set is unreachable by menu, discovery, *and* preloads.
- **The plugin version is the update cache key** — an edited plugin re-shipped under the same version is skipped by `/plugin update` as already installed. `release_gate.py` G6 refuses a same-version artifact.
- **Skill names cannot contain `claude` or `anthropic`** — reserved words rejected at install, failing the whole plugin load. Hence `/entry-file-audit`, not `/claude-md-audit`; lint F8 now blocks the class at write time (incident 2026-07-06, the third metabolized into infrastructure).
- **Agent `<example>` blocks must live inside a block scalar** (`description: |`, indented). Schema examples that show them bare at column 0 produce frontmatter a strict YAML parser rejects, which fails the whole plugin load. The lint's A2 rule now blocks this class at write time (incident 2026-07-06, metabolized per the outer loop).
- Plugin `hooks.json` needs the outer `"hooks"` wrapper (plain `settings.json` snippets pasted without it fail silently).
- `allowed-tools` grants without prompting; it restricts nothing.
- Listing caps: 1% aggregate budget, 1,536-char per-entry cap, 1,024-char portability cap; body ≤500 lines; compaction keeps the first 5,000 tokens per skill, 25,000 combined.

On a Claude Code version bump, re-verify the standards' physics table against `/doctor` and the changelog.

## Snapshot rule

This plugin is the **source of record** for the `skill-*` family *and*, as of v1.1.0, for the absorbed packs `linguistic-techniques`, `intent-extract`, and `system-decompose`. Copies placed in project knowledge (e.g. the corpus canon files) are snapshots: refresh them from here; never edit the copy. One canonical direction, chosen once.

**Self-sufficiency assumption (v1.1.0):** forge operates as the *only* installed skill surface. Every cross-skill reference resolves inside this plugin; references to retired sibling packs (`grill-the-ask`, `prd/spec/lld-author`, `layout/break-down-flow`, `component-author`, `agent/entry-file/rubric/knowledge-author`, and the `doc-reviewer` agent) were removed or redirected — semantic fences kept, phantom owners dropped, `system-decompose`'s layout/components/ux references flipped from sibling-canon adapters to self-canonical (with an honest note on depth not carried). CHANGELOGs and `routing-corpus.json` eval data are historical/test artifacts and were vendored verbatim. **Amended 2026-07-07 (v1.15.0):** `linguistics-reviewer` is un-retired — a `plugin-decompose` gap analysis against the pre-migration corpus found forge's own standards skills (agent/hook/plugin-authoring-standards, linguistic-techniques) each lacked the fresh-context reviewer agent every one of them already proved out; `agent-reviewer`, `hook-reviewer`, `plugin-reviewer`, and `linguistics-reviewer` close that gap, each re-pointed at forge's own tooling (`skill_lint.py`, `release_gate.py`) rather than the legacy corpus's incompatible scripts. `handoff-compose` — needed by every one of them, and by every agent across the wider corpus — is absorbed as forge's fourth cross-cutting layer alongside intent-extract, system-decompose, and linguistic-techniques.

If a skill is vendored out of the plugin (losing `${CLAUDE_PLUGIN_ROOT}`), the lint path from a skill body becomes `${CLAUDE_SKILL_DIR}/../../scripts/skill_lint.py`.

v1.42.7 · assembled 2026-07-21 · 1.42.7: ADR-0006 teamwork-rename sweep — live references rewritten (handoff-compose's coordinator seat, ops agents' owner labels, loop-rules/close-session pointers, standards exemplars). Incident → infrastructure, same change: the sweep rewrote agent_corpus_index.py's bare-role selftest FIXTURE (code-reviewer → code-checker), splitting the same-role pair the control needs — G4 caught it; fixture renamed to the phantom widget-reviewer with a dated comment so no future rename sweep can break the control's premise. G8 allow-set gains the -session/-ask/-team suffix wave (future-/per-/this-/cross-/same-/authoring-/mid-session, making-ask, resolve-vs-ask, subagent-vs-team, whole-team) · v1.42.6 · assembled 2026-07-21 · 1.42.6: ADR-0006 screens-rename sweep — live references rewritten (skills-audit's audit-diff pointer, standards examples, suites); pointer updates only · v1.42.5 · assembled 2026-07-21 · 1.42.5: ADR-0006 design-kits-rename sweep — live references + G8 allow-set updated (material-color-facts pruned: now a real skill); pointer updates only · v1.42.4 · assembled 2026-07-21 · 1.42.4: ADR-0006 agent-protocols-rename sweep — live references rewritten; pointer updates only · v1.42.3 · assembled 2026-07-21 · 1.42.3: ADR-0006 llm-rename sweep — live references to llm's old member handles rewritten (G8 allow-set comment, corpus references); pointer updates only · v1.42.2 · assembled 2026-07-21 · 1.42.2: ADR-0006 typography-rename sweep — live references rewritten; pointer updates only · v1.42.1 · assembled 2026-07-21 · 1.42.1: ADR-0006 color-rename sweep — G8 allow-set prose tokens and corpus_index's CRITIC handle pattern track the renamed color members; skill-decompose/skill-synthesize/audit references updated; pointer updates only · v1.42.0 · assembled 2026-07-21 · 1.42.0: ADR-0006 Phase 0 — the standards flip that precedes
every rename PR: naming-rules becomes the estate's naming canon (agent-authoring-standards
§Naming carries the dated supersession note; skill-authoring-standards' scope line repoints its
naming-grammar pointer from corpus Vol 2 to naming-rules); skill_lint W5's KNOWLEDGE_NOUNS gains
`facts` + `rules` with two new selftest fixtures (a `-facts` head with user-invocable true warns,
a model-only `-writing-rules` passes clean) so the ~40 knowledge renames keep their model-only
check on arrival; root CLAUDE.md's Naming invariant gains the canon pointer and the Decision-7
term-of-art shelf exception (color/llm) · v1.41.0 · assembled 2026-07-20 · 1.41.0: eval-run converted command species → procedural
(disable-model-invocation: true → false, per explicit user direction — the 1.24.0 skill-forge
precedent): description rewritten from slash-menu documentation into a real trigger contract
("prove the routing after a description edit", "did my description change break routing", the
wave-boundary check), gains its own evals/evals.json (9 trigger / 6 no-trigger, accepted-leak
class annotated for the off-menu commands harness-audit/plugin-release); reciprocal no-trigger
cases added to skill-authoring-standards and skill-review per the fence-closure rule. Landed
mid-wave inside the naming-rules eval-run itself, so the same wave's blind-judge pass covers it:
suites B/C/D/E scored 14/14 · 10/11+1 accepted-leak · 29/30 · 15/16+1 accepted-leak on the
naming-rules menu; the two real findings fixed same change (naming-rules' n05 leak → the
legacy-grammar fence now names "why the EXISTING estate's names are structured the way they
are"; git-campaign-workflows' t08 dead case → its description gains the verbatim "was requiring
PRs on main ever considered here"), each re-judged post-fix · v1.40.0 · assembled 2026-07-20 · 1.40.0: naming-rules — knowledge skill carrying the simple
("Fisher-Price") naming paradigm for NEW harness artifacts: five checkable tests (says-the-job ·
kind-audible · registry-verb · no-lore · loud-contrast), a per-kind shape table (verb-first
runnables, `-rules`/`-facts` knowledge, person-word seats, plain-noun shelves), the
one-verb-per-concept registry (make/check/plan/split/merge/… with retired synonyms), and the
design session's refinement set — activity-carrying `-rules` (`doc-writing-rules`, never bare
`doc-rules`), `-facts` vs `-rules`, verb↔noun twins (`/sort-issues` ↔ `issue-sorter`),
plan-decides/bare-verb-does. Scoped to coexist: shipped names are APIs and the legacy grammar
(agent-authoring-standards §Naming, skill_lint's checkable slice) keeps governing them; the
full-estate map (9 plugins, ~130 members; plugin layer settled with the user —
harness/docs/teamwork/screens + color/typography kept + design-kits/agent-protocols/llm-facts)
ships as an illustrative worked example at references/estate-rename-map.md, explicitly not a
ratified rename plan. Forged through all six gates: fresh-session baselines demonstrated the
delta (contrast-verify → check-contrast · issue-triage×2 → /sort-issues ↔ issue-sorter ·
doc-authoring-standards → doc-writing-rules); fresh-context FLOOR audit PASS, 0 blocking (two
minors — a half-stale fence citation, two drift-pair restatements — fixed same change);
reciprocal naming fences closed in the skill-/agent-authoring-standards, git-campaign-workflows,
and plugin-decompose suites; /eval-run at the wave boundary owed as the follow-up. G8 allow set
gains the paradigm's six illustrative names (doc-rules · doc-writing-rules · entry-file-rules ·
icon-rules · file-feature · sort-issues) plus seven pre-existing prose compounds newly caught by
recent suffix growth (-rules here, -routing/-sweep/-orchestrator from earlier ships:
path-scoped-rules, folder-taxonomy, system-planner, three-hard-rules, mis-routing,
threshold-sweep, repo-orchestrator — the standing false-positive class, 1.25.1 precedent),
restoring the estate-wide sweep to 0 fail / 0 warn across all nine plugins · v1.39.0 · assembled 2026-07-20 · 1.39.0: the ops-family grows its coordination pair —
`ops-orchestrator` (sweep seat: fans out ops-adr + ops-issues + ops-repo in parallel, hands the
returned handoffs to the planner, relays one queue + per-seat status; Read+Task wall, sonnet+high)
and `ops-planner` (prioritization seat: one queue at `.claude/ops/plan.md`, every entry
action·owner·evidence·size, sweep-reports or durable-state+live-gh input modes; single-write wall,
fable+high), each with a same-named dispatch command per the /ops-issues pairing ruling. Sweep
shape ruled at intake: the planner IS the sweep's roll-up — the orchestrator never authors a queue.
Fresh-context reviews: both agents PASS-with-fixes (all closed, confirmed); the orchestrator
command FAILED its first audit on a banner-ordering blocking finding — the first-run banner check
ran AFTER the dispatch that creates `.claude/ops/plan.md`, the very file the condition reads, so
the disclosure could never fire on the happy path; both commands' checks moved pre-dispatch with
the timing pinned in their stopping predicates, re-audit PASS. Reciprocal sweep/backlog fences
added to ops-adr/ops-issues/ops-repo descriptions in the same change (agent descriptions carry no
eval suites — the estate's known agent-routing-eval gap, unchanged). Smoke evidence: sibling-seat
dispatch from a subagent context proven live (forge:ops-repo returned through a simulated
orchestrator); planner happy path wrote the repo's first real plan (7 entries, all fully typed);
both named failure branches fired as written (missing sweep reports → stop, no fallback; planner
unregistered → raw handoffs relayed, no improvised queue) ·

v1.38.0 · assembled 2026-07-20 · 1.38.0: `/ops-issues` — a new command skill dispatching the
`ops-issues` agent on demand, and stating its own capture/author-only contract as a fixed banner
before the first CONFIRMED-roster dispatch. Prompted by a user question ("can we make ops-issues
ask if it should only capture and never do the work") that turned out to already be answered
structurally by REQ-012 — there was nothing to ask, since the boundary isn't configurable. The
genuinely missing piece was disclosure, not a choice: a command entry point that states the
contract plainly before dispatching, rather than leaving it buried in the agent's own file. First
case in this workspace of a skill and an agent sharing one name (a command dispatching its
own-named standing seat) — noted as a deliberate choice, not yet a rule. Fresh-context
`skill-auditor` FLOOR pass found 1 blocking + 2 major-class findings, all fixed: the first draft's
banner claimed "the dispatched agent asks itself" for the REQ-011/REQ-013 interviews — backwards,
since the agent's own `tools` carries no `AskUserQuestion` (verified against `agents/ops-issues.md`
directly) and the SPEC assigns that question to "the dispatching session," which on this path IS
this command's own session; rewritten so the command runs the interview itself and re-dispatches
carrying the confirmed answer. The first-invocation detection was also wrong: keying the banner on
bare `friendlies.json` absence misses that an UNATTENDED hourly firing already writes that file via
REQ-011's evidence-only seed, so the banner would have silently never shown in the primary
(scheduled) deployment shape — corrected to key on whether a CONFIRMED roster is on record in the
file's own `policy` block, not mere file existence. `release_gate` G8's own suffix-inventory
mechanism caught two consequences of this change: adding `ops-issues` as a skill name newly matched
`github-issue-pr-primitives`' pre-existing "sub-issues" prose (a real GitHub term, cited from its
own references file) against the new `-issues` suffix; the fix draft's own "model-routing" phrase
tripped a second suffix — the first was allowlisted (dated, cited comment, the standing
false-positive class), the second was reworded instead, since avoiding a fresh false-positive by
rephrasing is cheaper than growing the allowlist for a sentence that reads fine either way ·
v1.37.0 · assembled 2026-07-20 · 1.37.0: `ops-issues` gains REQ-013 — a one-time, interactive-only
offer on a GitHub-backed (Option B) repo's first interactive firing to declare a project-scoped
GitHub MCP server (`.mcp.json`) for richer session browsing, recommended default a read-only-scoped
fine-grained PAT so REQ-012's no-widened-action guarantee holds by construction of the credential's
own scope, not agent discipline — the write path for issues/PRs stays the existing capture skills
exclusively. Governing SPEC `spec-ticketing-watch-triage.md` bumped 0.2.0 → 0.3.0 (new REQ-013 +
AC-013, three new Non-goals bullets: no webhook receiver, no full-write default credential, no
revoking a recorded decision). Grounded via WebFetch against Claude Code's own `.mcp.json`/`claude
mcp add` docs before designing (the earlier, unverified assumption — a webhook receiver — was
already ruled out by this SPEC's own REQ-002/Non-goals; the real mechanism is a project-scoped
config file Claude Code approves automatically on first checkout, not custom infrastructure).
Fresh-context `agent-reviewer` FLOOR pass: 1 Moderate fixed (step 8 read as if the watch seat asks
the question itself — `tools` carries no `AskUserQuestion`; corrected to mirror REQ-011's own
dispatch-carrier pattern, and the SPEC's REQ-013 text amended to stop implying it must fire in the
SAME firing as REQ-011's bootstrap, matching AC-013's actual any-interactive-firing gate) and 3
minors (description said "first firing," corrected to "first interactive firing"; no failure
branch named the pre-existing-`.mcp.json` clobber risk, added — merge, never overwrite; the
stopping predicate's outcome enum couldn't express an offer surfaced but not yet confirmed by a
carrying dispatch, added as a fourth named state). A4 thin-shell WARN (agents/ops-issues.md, cap
60, 145 lines) — accepted precedent, unchanged in kind from the file's own prior state (the
cross-plugin TICKET-shape restatement, not today's delta, is the bulk of it) · v1.36.0 · assembled 2026-07-20 · 1.36.0: `ops-adr` — a new standing agent closing the periodic-
ADR-review gap, sibling to `ops-issues`/`ops-repo`: `scripts/adr_checkpoint.py` diffs the ADR
corpus by content hash against a checkpoint (new/amended/newly-superseded, read from `supersedes:`
frontmatter rather than inferred from prose), keeping judgment cost proportional to the delta,
never the corpus; `scripts/adr_queue.py` holds candidates durably so a scheduled firing never
blocks on a live human, idempotent by (adr, kind) so a re-detected candidate updates in place
instead of piling up. Structurally barred from authoring: a confirmed harvest candidate's next
step is a named `/pack-forge`/`/skill-forge` command, a confirmed stale-citation candidate's is
`knowledge-harvest`'s own Phase 6 — this agent runs neither itself, only names it, mirroring
`ops-repo`'s propose-don't-mutate posture. Preloads `knowledge-harvest` + `pack-authoring-standards`
(both same-plugin, both `disable-model-invocation: false` and therefore preloadable — unlike
`ops-issues`/`ops-repo`'s scribe dependencies, which are cross-plugin and must be restated).
Designed via a `system-decompose` PLAN-mode manifest (technical-architecture domain, 11 leaf nodes
across 5 subsystems, `coverage_check.py` clean on the second pass — checkpoint-store needed a
`shared-util` justify) before either script was written. Both scripts' selftests include a
negative control apiece: `adr_checkpoint.py` proves an already-recorded supersession never
re-fires, and that a 500-ADR fixture with one new entry costs the same as a 1-ADR corpus would;
`adr_queue.py` proves a re-added (adr, kind) pair never duplicates a row. Fresh-context
`agent-reviewer` FLOOR pass: 4 majors fixed — the Write-tool-scope claim read as structural but
wasn't (corrected to "contract, not a tool wall," matching `ops-issues`/`ops-repo`'s own honest
phrasing); `adr_checkpoint.py` split into separate `classify`/`advance` calls after the review
found the original single-call version advanced the checkpoint before judgment ran, so a crash
mid-firing would have silently lost the unjudged delta forever; a missing report-destination
default (added, matching the siblings' own `.claude/ops/reports/<UTC-timestamp>.md` convention);
and the body's restatement of `knowledge-harvest`'s own Phase 1/2/6 content trimmed to cite by
phase name. Plus 3 minors: script paths repointed to `${CLAUDE_PLUGIN_ROOT}` (were cwd-relative,
which only happened to work from the plugin root); `adr_queue.py clear` gained an `id:kind` precise
form (a bare id was dropping a deferred sibling candidate's row); one clause added scoping the
schedule-as-consent argument OFF `knowledge-harvest`'s own separately-worded Phase 6 constraint —
detection/queueing runs on schedule, Phase 6 execution is always named for a human. A4 thin-shell
WARN (agents/ops-adr.md, cap 60, 118 lines after the fixes) — accepted precedent, same kind as
`ops-issues` (102) and `ops-repo` (97): all three restate cross-plugin content they can't preload.
Wired: README/MANUAL entries, root CLAUDE.md routing row · v1.35.0 · assembled 2026-07-19 · 1.35.0: absorbed scribe's `knowledge-forge` skill, retired as
part of a workspace-wide `plugin-decompose` gap analysis (job-to-be-done test: it duplicated this
plugin's own `pack-forge` end to end, while shipping no mechanical corpus-integrity gate of its
own — `pack-forge` carries `corpus_check.py` + a dedicated `pack-researcher` agent, `knowledge-forge`
explicitly deferred that job to this plugin's `skills-audit`). `skill-authoring-standards` gains a
new "Knowledge pack" body-style subsection — the entry-surface conventions `pack-authoring-standards`
deliberately excludes (answers-only boundary, Grep-first consult discipline, deviation doctrine,
corpus-of-record rule, the answer-contract format) had no home in this plugin before now; a genuine
content gap, not a restatement. Two hardcoded `"knowledge-forge"` string dependencies fixed
(`skills-audit/scripts/corpus_index.py`'s factory-route advisory now checks for `pack-forge`;
`skill-decompose/scripts/manifest_check.py`'s axis-count warning re-attributed to
`pack-authoring-standards`, the doctrine's actual home even before this retirement). `knowledge-harvest`,
`git-campaign-workflows`, and `github-issue-pr-primitives` repointed their own routing. This is the
forge leg of a workspace-wide rename campaign — every knowledge-pack skill across
color/ui/typography/llm/agentic-ui/design-systems/scribe that named `knowledge-forge` as its own
factory route is repointed to `pack-forge` in the same change, each plugin versioned and ledgered
separately. Fresh-context review (skill-auditor): 1 blocking finding fixed (this ledger entry itself
— the first-pass campaign left forge unbumped despite 13 changed files), 1 major fixed (the
Grep-first/Read-the-section consult discipline was genuinely lost in the first-pass migration, not
just moved — added back as skill-authoring-standards' fifth knowledge-pack bullet), 2 minors fixed
(a systematic off-by-one-day date across ~20 files; a "two pieces" vs. four-item list count
mismatch in scribe's own ledger entry) · v1.34.14 · assembled 2026-07-19 · 1.34.14: fixed a stale, actively-misleading claim in
`system-decompose`'s domain references, found by a `plugin-decompose` gap analysis run against a
candidate "consolidate the two-plane decomposition method" reorg (verdict: no-partition — the three
"-decompose"-named skills share a narrative skeleton but not a mechanism, and unifying them would
cross a hard plugin boundary via `layout-reviewer`/`flow-reviewer`'s own agent dependencies).
`references/layout.md` previously called `ui:layout-decompose`'s richer archetype/rubric apparatus
"the retired sibling pack" — it is alive, not retired, and is the deliberate landing spot for live
UI design/critique work this thin manifest-adapter deliberately doesn't carry; corrected to name it
explicitly instead of leaving a stale retirement claim standing. `references/ux-architecture.md`'s
two "model the journey separately" deferral lines now name `ui:flow-decompose` explicitly rather
than leaving an unnamed pointer. Both are soft `mention`-only edges — no preload, no script
coupling, fully compatible with the plugin boundary · v1.34.13 · assembled 2026-07-19 · 1.34.13: `open-questions-sweep` gains a reciprocal NOT-for fence
pointing at orchestration's new `session-close` skill — a git worktree's own uncommitted state,
findings, or knowledge capture before a session ends is a different axis (repo state) from this
skill's own unresolved conversational loose ends. One no-trigger eval case added
(`evals/evals.json` n11: "wrap up this session... check for anything left to capture in the
worktree") and verified clean via `eval_check.py`. No behavior change to this skill's own trigger
logic otherwise · v1.34.12 · assembled 2026-07-19 · 1.34.12: ADR-0004 dual-write, corrected — v1.34.10 (below)
shipped a real bug, found and fixed same-day: a combined `gh issue create --type <Kind>` call was
verified to create the issue and only THEN fail the type-attach step, silently (no URL printed on
that error) — proven by a leftover test issue (`#51`, closed once found). That makes "retry the
same create without `--type`" unsafe: a partially-succeeded create retried blind mints a
duplicate. `ops-issues` and all three scribe capture skills (`bug-report`/`feature`/`issue`) are
rewritten to two separate calls, never combined: the existing `gh issue create` (unchanged, no
`--type`, ever), then — once the id is known — a second, independent `gh issue edit <id> --type
Bug|Feature|Task`; a failure there leaves the already-created issue with the label alone, no
duplication risk, since the create step never carries the parameter that could partially fail.
`github-issue-pr-primitives`'s `bug-task-feature-mapping-nuances.md` and `doc-authoring-standards`
both corrected to match. This landed as a follow-up PR rather than a v1.34.10 amendment: v1.34.10
was already merged (by the maintainer, from a green CI run) before this fix could be pushed to the
same PR — the ledger entry below is left as an accurate record of what v1.34.10 actually shipped,
not rewritten · v1.34.11 · assembled 2026-07-19 · 1.34.11: ADR-0005 ticket-claim protocol —
ops-repo gains a read-only, propose-only stale-claim check (where the workspace rules ADR-0005):
inventory now also reads claimed-ticket state, a new `stale-claim` classification joins
stale-open/orphaned, never auto-reclaimed. Prompted by a same-day near-miss (two independent
sessions almost duplicating Issue #44's own implementation, caught only by incidental worktree
inspection) — the ADR adds `claim` as a seventh backend-resolver operation (scribe) and
cross-references concurrency-design (orchestration) as the ticket-layer check beneath its existing
git-tree collision response · v1.34.10 · assembled 2026-07-19 · 1.34.10: ADR-0004 dual-write,
implemented (Issue #44) — `ops-issues`' own mint call gains the same Issue-Type-alongside-label
treatment its sibling scribe skills now carry (`--type Bug|Feature|Task`, fallback to label-only
if the org's type schema doesn't resolve, skipped type noted in the sweep report).
`github-issue-pr-primitives`' `bug-task-feature-mapping-nuances.md` gains a dated update answering
ADR-0004's own two "Open verification items": `gh issue create --type` is directly supported, and
Issue Types is organization-scoped — this workspace's repo is personal-account-owned with zero
types configured, confirmed via a live probe. An independent agent-reviewer FLOOR pass (fresh
context) found the sibling scribe skills' own fallback wording too narrow — "the org's type schema
doesn't resolve" missed an older `gh` that doesn't recognize `--type` at all — broadened here too
(and across the three scribe skills, same-change): a `--type` resolution failure, whichever cause,
is its own fallback (retry without the flag, stay git-native), distinct from `gh` itself being
unreachable. **Superseded same-day by v1.34.12 above** — this design turned out unsafe; see that
entry. Pre-existing A4 thin-shell WARN (agents/ops-issues.md, cap 60) unchanged in kind, 95→100
lines — a WARN, not a gate FAIL; same precedent as 1.34.4's own labeling fix, the added lines are
load-bearing, not restatable knowledge · v1.34.9 · assembled 2026-07-18 · 1.34.9: `/eval-run forge` + `/eval-run orchestration` tuning —
a 493-case blind-judge routing simulation across all 9 installed plugins found 16 failures across
10 suites (477/493 passed, 18/28 suites clean). Fixed 9 of them at the description layer: three
`git-campaign-workflows` leaks (bare action-imperatives — "delete this branch", "pull the
latest", "merge and clean up" — now excluded); one `plugin-decompose` build-vs-partition leak
("create a plugin with X") and one audit-scope leak ("audit my whole harness surface", now
fenced to harness-audit); one `github-issue-pr-primitives` decision-phrased leak ("should this
repo use X backend"); one `script-authoring-standards` bare-imperative leak ("run the release
gate"); one `entry-file-standards` steal (reworded "how big the file" → "how big CLAUDE.md
itself" to stop losing to skill-authoring-standards' body-length coverage); a reciprocal
`plugin-onboard`/`plugin-authoring-standards` fence (declared-but-invisible vs. installed-but-
failing); a reciprocal `reasoning-orders`/scribe's `research-methods` fence (judging whether a
claim is a genuine higher-order gain vs. measuring one empirically); and `knowledge-harvest`
gained its own three stolen trigger phrasings verbatim (a stale citation, a dedup check, "propose
a plan before we write"). All 15 non-judgment-call failures
re-verified passing post-fix via a second blind-judge pass against the corrected menu. One
finding left as a judgment call, not a bug: `agent-authoring-standards` leaking on "forge me a
reviewer agent" is arguably correct degradation — `agent-forge` is deliberately off-menu
(command species, human-timed), so no router-discoverable owner exists for that ask · v1.34.8 · assembled 2026-07-18 · 1.34.8: pack-authoring-standards' canonical-reachability check
(Issue #48, a same-day `/review` follow-up to #45/#40) — the self-documentation surface named as a
third N/A example alongside INDEX-absence and harvester-absence: verified against the full
`references/*.md` corpus that no file anywhere currently self-documents as canonical, so applying
the rule literally would have flagged every reference file in the estate as "fake-canonical" on
that one axis, contradicting the rule's own stated intent. N/A is now framed as reversible — the
moment any class actually adopts a surface (an INDEX ships, a self-canonical header convention
starts), that surface stops being N/A and starts counting · v1.34.7 · assembled 2026-07-18 · 1.34.7: reviewer-discipline (Issue #39) — a new cross-cutting
skill piloted on 5 forge reviewer agents (agent-reviewer, plugin-reviewer, hook-reviewer,
linguistics-reviewer, skill-auditor), encoding three reviewer-conduct priors confirmed absent from
every reviewer/auditor agent in this workspace: evidentiary symmetry (a dismissal costs the same
evidence as a confirmation), runtime over claim (a "fixed/shipped" claim is checked against the
artifact, never accepted from a changelog), and steelman before filing (draft the maker's rebuttal
before a finding ships; revise or drop what wouldn't survive it). A fourth candidate prior — an
emoji verdict taxonomy — was explicitly rejected as competing with the estate's own ratified
🟢/🟡/🔴 convention. Minted via skill-forge's full 6-phase gate: fresh-context FLOOR audit (PASS,
4 minors triaged — a letter-vs-spirit gap between the Procedure and Output contract, a missing
good-dismissal exemplar, a stale workspace-coupled identity clause, a naming-grammar nuance
recorded not fixed since the name was already user-ratified); linguistic-techniques' potency pass
(L1/L3/L6 gates, prohibition density more than halved with identical semantics); a 4-prompt
behavior check comparing fresh-session baselines against with-skill reruns, including one
genuinely neutral-framed prompt (no explicit "verify this" cue) that cleanly demonstrated all
three disciplines firing unprompted — the real bar a preloaded skill needs to clear. The three
target agents' pre-existing generic "verify claims with tools, not trust" steps now name the skill
by handle instead of restating it (agent-reviewer.md, plugin-reviewer.md, skill-auditor.md);
handoff-compose's eval suite gained the reciprocal fence-closure case (n14, renumbered same-change
to avoid an id collision with open-questions-sweep's own n13 landed moments earlier) · v1.34.6 · assembled 2026-07-18 · 1.34.6: pack-authoring-standards gains a canonical-reachability
check (Issue #40) — a "canonical" artifact must be reachable from every surface the estate actually
builds for its class (consult table ≈ nav, INDEX ≈ corpus index, eval trigger phrasings ≈ generator
input, `[[handle]]`/preload graph, frontmatter self-claim); a surface the estate doesn't build (a
flat pack's absent INDEX, the fact packs have no harvester) is N/A, not a miss. Translated, not
copied, from adia-ui-kit v3.7.13's `reasoning-methodologies.md` method #5 — its literal ≥5-of-5
threshold would have falsely flagged this estate's own compliant flat packs (scoring ~2/5) as
fake-canonical, caught by a fresh-context FLOOR audit before ship (F1) and fixed by translating the
threshold to applicable-surfaces-only instead of a raw count; four minor register/consistency fixes
alongside (header Provenance parity, house "(added ...; type specimen: ...)" marker convention,
"currency lapse" gloss for imported jargon, dropped the redundant "≥5 of 5" phrasing) · v1.34.5 · assembled 2026-07-18 · 1.34.5: a workflow-backed xhigh code review of open-questions-
sweep's own PR (generator-independent — the maker did not author or see the run mid-flight) found
6 real defects the P5 FLOOR audit missed, all fixed same-change: open-questions-sweep's step 3
forced a fabricated "recommended" marking onto stray-idea items with no stated assumption (now
conditional); its on-its-own trigger had no unattended/scheduled-firing fence, risking an
unanswerable AskUserQuestion hang (added, mirroring ops-issues' own convention); its stopping
predicate didn't recognize a user decline as terminal despite the failure branch requiring one
(reconciled); its P5 fence-closure step missed scribe's issue/feature/bug-report suites (reciprocal
cases added there too); its own intent.md P2 gate line overclaimed eval-fencing coverage
(corrected); and ops-issues.md overclaimed that bug-report/feature share `issue`'s missing-label-
creation fallback when only `issue` documents it (scoped accurately). intent.md's rulings section
records the generator-fixes-own-findings deviation and why it doesn't violate generator≠critic
here · v1.34.4 · assembled 2026-07-18 · 1.34.4: ops-issues' minted-record-shape restatement gained the
git-native labeling clause it was missing — the Scope section named `kind: bug`/`kind: feature`
(TICKET frontmatter, file-backend vocabulary only) but never said how that classification lands on
today's actually-resolved backend: as a GitHub label (`bug`+severity, `feature`+size, `task`+size),
exactly as `bug-report`/`feature`/`issue` already apply it. Found while answering a direct question
about whether the issue/ticket-writing skills use labels for bug/feature/task context — the three
scribe capture skills already did; this standing intake agent, the other place that mints directly
against the resolved backend, had an incomplete restatement of the same contract. `issue` added to
the named cross-plugin skill list alongside doc-authoring-standards/bug-report/feature. Pre-existing
A4 thin-shell WARN (agents/ops-issues.md, cap 60) unchanged in kind, 87→92 lines — a WARN, not a
gate FAIL; the added lines are the load-bearing fix, not restatable knowledge · v1.34.3 · assembled 2026-07-18 · 1.34.3: open-questions-sweep — a new procedural skill closing a
gap this session's own baseline test confirmed: without it, Claude correctly recalls a session's
unanswered questions and unconfirmed assumptions but dumps them as prose plus one open-ended
follow-up instead of resolving them; the skill batches every qualifying item into ONE
AskUserQuestion round (built via `/forge:intent-extract` → `/skill-forge`, which corrected the
original ask's "knowledge skill" framing to procedural — it changes behavior, it isn't reference
content). Reciprocal no-trigger fences added to intent-extract and orchestration's loop-design
(both named in its own NOT-clauses) plus handoff-compose (an auditor-flagged near-miss on
session-close vocabulary); ops-issues is an agent, not a skill, so that fence stands
unreciprocated by mechanism, not oversight. FLOOR audit: PASS, two minor fixes applied (the
ops-issues fence broadened to cover backlog queries, a user-declines-the-round failure branch
added) · v1.34.2 · assembled 2026-07-18 · 1.34.2: ops-issues first-run bootstrap contract (spec-ticketing-
watch-triage 0.2.0, REQ-011/REQ-012) — a firing with no `friendlies.json` seeds evidence-only (the
repo owner/maintainer when historical authorship proves it, never a guessed second author) and
returns roster candidates for the DISPATCHING session's one AskUserQuestion round (private repo →
approved collaborators; public → historical issue/PR authors + owners), with the confirmed roster
plus a future-collaborator standing rule (`auto-friendly-on-access` | `hold-first-filing`)
persisted in the file's `policy` block, never re-asked; REQ-012 makes explicit that trust never
widens action — a friendly skips only the hold, never the execution barrier. Ruled during the
first live bootstrap (kimgranlund/claude-plugins, 2026-07-18): owner-only roster confirmed,
hold-first-filing chosen · v1.34.1 · assembled 2026-07-18 · 1.34.1: ops-repo's session-scoped `CronCreate` deployment ruled
(Issue #32) — accepted as this seat's intended mechanism rather than a standing OS-level crontab:
re-armed per work session, each firing bounded and idempotent so a lapse between sessions costs
only a delayed sweep. Description updated to say so plainly instead of implying an unfinished gap;
field evidence backing the ruling: 6 real firings observed across ~15 hours from one long-lived
session-scoped job, 5 landing committed reports on `origin/main` · v1.34.0 · assembled 2026-07-17 · 1.34.0: reciprocal no-trigger fences added to
agent-authoring-standards/entry-file-standards/hook-authoring-standards for orchestration's new
concurrency-design skill (worktree/session-collision asks are that skill's territory, not these
standards'). G8 allow-set gains `self-report` — prose ("never act on either side's self-report"),
not a skill name, tripping the `-report` suffix handoff-compose already owns · v1.33.0 · assembled 2026-07-17 · 1.33.0: ops-issues + ops-repo — the two standing operational agents (scheduled + on-demand) closing the ticketing-backend arc: ops-issues implements the watch/triage/trust SPEC (spec-ticketing-watch-triage.md) as a real dispatched seat — discover-since-checkpoint, classify (github-issue-pr-primitives' Bug/Task/Feature axis), trust-check against a durable friendlies allow-list, mint/resume trusted items directly, hold unknowns to a ledger, never execute the work itself; ops-repo inventories worktrees/branches/PRs and executes cleanup ONLY through this plugin's own gated scripts (campaign_close.py/gitignore_check.py/sync_main.py) on independently-verified-merged findings, proposes everything else. A real structural bug caught by G4's own reverse control before shipping: ops-issues' first draft preloaded scribe's doc-authoring-standards directly — a hard cross-plugin preload violation (CLAUDE.md's own invariant: preloads are plugin-hard, mentions are plugin-soft) invisible to release_gate's other checks but caught by agent_corpus_index.py's DANGLING flag; fixed by dropping the preload and stating the needed TICKET shape inline, with doc-authoring-standards kept as a soft, named mention. Both agents pin sonnet+high (orchestration/coordination seat class, per the model-tiering ladder) and route their reports through handoff-compose · v1.32.0 · assembled 2026-07-17 · 1.32.0: github-issue-pr-primitives — the sibling knowledge pack to git-campaign-workflows, GitHub's platform facts instead of our own git mechanics: seven axes (issue/PR/discussion, Issue Types + the four-days-old Issue Fields GA vs. labels, sub-issues vs. the retired tasklist-block feature, the nine closing keywords + the one merge-strategy gap GitHub's own docs never close, PR/review/CODEOWNERS/merge-queue mechanics, Projects v2's GraphQL-only structure, and a synthesis axis naming where this workspace's own ADR-0002/doc-authoring-standards kind:bug/kind:feature-as-label convention aligns with and diverges from GitHub's native Issue Types) plus a sources.md provenance file, all research dated 2026-07-17 via six parallel pack-researcher dispatches. Commissioned after a fresh-context review caught two unverified-platform-fact errors in a sibling SPEC (spec-linear-adapter, REST-vs-GraphQL and an impossible 1:1 state mapping) the same week — this pack exists so the same failure class doesn't recur on GitHub's own primitives. G8 allow-set gains `lifecycle-and-review` (a references-file mention whose 2-char prefix falls under the token regex's floor, same class as merge-semantics) and `sub-issue` (GitHub's own singular terminology colliding with scribe's no-hyphen `issue` skill name) · v1.31.0 · assembled 2026-07-17 · 1.31.0: git-campaign-workflows (Issue #24) — the knowledge pack closing the arc: five reference axes (worktree mechanics, merge semantics, the silent-failure catalog, parallel-session reconcile, the ADR-0002 decision tree), every claim grounded in a dated 2026-07-16/17 incident this workspace actually hit — the ten-branch silent-delete-failure, the truncated-pipe pull abort, two str.replace silent misses, the sync_main stash-verification TOCTOU the fresh-context audit caught pre-ship, and the branch-protection rejection recorded so it is never re-litigated. Flat 5-file corpus (no INDEX per the enumerability ruling); trigger evals adversarial against the *-authoring-standards siblings + repo-alignment + a build/implement ask · v1.30.0 · assembled 2026-07-17 · 1.30.0: the git mechanization wave (Issues #19 + #23) — three new scripts closing the estate's hand-run git rituals: gitignore_check.py (G1/G2 — stale rules + unignored generated dirs, repo-alignment's razor mechanized, pointed to from the razor's own prose), campaign_close.py (C1-C3 — merged-state gate, delete-then-REVERIFY the remote branch is gone, the ten-branch silent-delete-failure as the negative control), sync_main.py (S1-S4 — dirty-vs-incoming classification, named-stash quarantine with a verify_stash_created check, --ff-only pull, HEAD-by-SHA reverification). CLAUDE.md's campaign row gains the close/sync verbs; G4 sweeps all three for free. A fresh-context audit against script-authoring-standards ran each selftest live and reproduced three real bugs by direct repro before they shipped: sync_main's stash-verification would have misattributed a FOREIGN stash to this run on the exact 'nothing to stash' race its own docstring warns about (fixed: verify_stash_created checks list-growth + label match, not the exit code); campaign_close's branch-existence check used an unauthenticated path while its delete used an authenticated one, so a private repo closed via --repo would silently skip the delete and report false-clean (fixed: both share one gh api path); gitignore_check's fnmatch approximation false-flagged the `**/node_modules`-style idiom — exactly the shape its own GENERATED_DIR_CANDIDATES would want written — as stale (fixed: leading `**/` unwraps before matching). Every fix carries the negative control that reproduces the audit's own repro, not just the original happy-path selftest · v1.29.0 · assembled 2026-07-16 · 1.29.0: harness-audit fixes — skill_lint A4 gains the dual-depth reviewer allowance (ruled 2026-07-16: -reviewer/-auditor seats warn past 75, everyone else 60; selftest controls prove both sides), agent-authoring-standards documents it (allowance covers contract, never knowledge); agent-reviewer deflated 101→75 body lines per its own deep review — the ~35 lines restating its preload and standard-of-excellence (with live drift) became pointers · v1.28.1 · assembled 2026-07-16 · 1.28.1: G8 allow set gains order-vs-task-flow — the verify-family judgment rule-ID class (Issue #8), findings vocabulary not skill names · v1.28.0 · assembled 2026-07-16 · 1.28.0: the six standards amendments from the external-skill review (Issue #11, each citing its repo@sha evidence) — skill-authoring-standards: parameter locks distinguished from procedural gates (lowercase always/never + backticked values, uncapped, must name forbidden neighbors; the uppercase ≤3 cap stands), coverage-forcing enumerations scored on the list not per line in the deletion test, lifecycle-moment trigger vocabulary named alongside feature nouns and symptoms, term-of-art naming exception for verbatim-typed catalog names; pack-authoring-standards: [incident] citation class (dated real-world failures as causal evidence), severity-ranked INDEX axis ordering for tiered rules corpora; skill_lint selftest pins W7's case-sensitivity (lowercase locks never trip the salience warn) · v1.27.0 · assembled 2026-07-15 · 1.27.0: /plugin-onboard — declare external plugins/marketplaces in a repo's .claude/settings.json (extraKnownMarketplaces; self-hosted marketplace.json wrapper for bare plugin repos) so contributors who trust the repo get the install prompt; authored with its own intent record + eval suite (audited); shipping discipline (map row, MANUAL entry, this ledger line) completed by the coordinating session · v1.26.4 · assembled 2026-07-15 · 1.26.4: the 1.26.3 razor's placement claim amended in place (dated note) — EnterWorktree's own contract creates worktrees IN-repo at .claude/worktrees/, falsifying the out-of-repo-default assumption hours after it shipped; the razor now says verify the ignore rule, never assume placement · v1.26.3 · assembled 2026-07-15 · 1.26.3: repo-alignment gains the .gitignore-is-a-record razor (ruled 2026-07-15) — sweep both directions: rules naming retired paths are stale context repaired by the invalidating change; in-repo worktrees/generated dirs must be ignored the moment they exist (worktrees belong outside the repo root by default) · v1.26.2 · assembled 2026-07-15 · 1.26.2: release_gate G8 allow set gains transport-and-streaming (a2a-protocol references file, the standing false-positive class) — retiring the estate's LAST standing gate warning: all nine plugins now sweep 0 fail / 0 warn · v1.26.1 · assembled 2026-07-15 · 1.26.1: subfolder conformance (ruled 2026-07-15: the sanctioned skill-subfolder set is evals/references/scripts/assets — release_gate G2 now warns on any other): G2 gains the subfolder-conformance warn with rogue-dir/clean selftest controls; skill-authoring-standards codifies the sanctioned set in its portable-core paragraph; linguistic-techniques' deliberate `resources/`-vs-`references/` directory split retired — the consulted-vs-enforced distinction is real but now carried per-file inside references/, matching the estate's one canonical home for consulted content · v1.26.0 · assembled 2026-07-15 · 1.26.0: gate G11 — the style-lint tier (ADR-0002): ruff over .py and eslint over .mjs|.js with workspace-root, dependency-free configs (ruff.toml / eslint.config.mjs; E702/E731 configured out as deliberate house idiom — compact semicolon one-liners and lambda helpers), run-if-reachable/WARN-if-absent locally (the G4 node-leg posture), enforced in CI (.github/workflows/gate.yml runs G1–G11 across all nine plugins + the gate scripts' own selftests on push/PR). Selftest gains the G11 ruff controls (F401 fixture bites, clean restores). The layer paid rent on arrival: 13 real defects fixed estate-wide (4 unused imports, 3 multi-imports, 2 unused variables, 4 ambiguous names) — one fix's incomplete rename was itself caught by the target script's selftest before landing, the generator≠critic loop working at the script tier · v1.25.1 · assembled 2026-07-15 · 1.25.1: release_gate G8 allow set gains `container-patterns`, `scale-theory`, `box-model-and-flow` (references files in ui 0.6.0's new knowledge packs), `design-systems` (the sibling PLUGIN's name, newly caught as a token once geometry-systems added the `-systems` suffix to the estate inventory), and the prose compounds `mid-flow` (hook skills), `cross-flow` (ui's flow-decompose), and `self-orchestrated-looping-agentic-systems` (orchestration's loop-design) — all three pre-existing prose newly flagged once dom-block-flow/geometry-systems added the `-flow`/`-systems` suffixes to the estate inventory, found by this very release's own estate-wide gate sweep and fixed same-change — the standing false-positive class (1.20.1 precedent), selftest green · v1.25.0 · assembled 2026-07-14 · 1.25.0: displayName 'Forge' added to the manifest (plugin naming hygiene ruled 2026-07-14: Title Case display names estate-wide, UI/LLM acronyms uppercased; plugin-authoring-standards records the verified field semantics). Also: the mechanization pair — script-authoring-standards (the deterministic tier's canon: script anatomy, selftest contract with a negative control that bites, exit tri-state 0/1/2-skip, placement/pathing, the arithmetic-not-judgment boundary; + references/selftest-patterns.md) and /script-forge (qualify → plan → confirm → author → validate; procedural, so the model can catch itself writing a prose checklist), designed via a system-decompose manifest (.claude/docs/decompositions/mechanization-manifest-v1.json, coverage clean). Grounding the standard found and closed a live gate hole the same day: G4 swept only scripts/*.py, so every .mjs selftest in the estate shipped unrun — G4 now sweeps *.py|*.mjs|*.js (node-guarded, WARN when node absent), ratifies ui-probe.mjs's pioneering exit-2 SKIP as the house tri-state (disclosed in the ok line, never failed), with failing/passing/skip .mjs controls added to the gate's selftest; the sweep immediately surfaced ui-probe.mjs's dependency-skip as intended. A4 canon repoint: skills-audit + agents-audit standards-of-excellence now cite script-authoring-standards for what a compliant instrument IS; reciprocal fences in knowledge-harvest (n13) + skill-forge (n09) suites; workspace CLAUDE.md routing row + selftest invariant widened to all three extensions. Independent FLOOR audits: both PASS, no blocking — minors applied (value-pointers over restated anatomy, Phase-5 report contract, drift-prone marker on the G4 mirror, normative/illustrative labels). Targeted /eval-run (4 suites, blind judges): round 1 exposed a symmetric intra-pair steal — each sibling's "is this mechanizable?" case routed to the other; fixed by ceding the interrogative to the standard via script-forge's fence ("owns the test; this workflow runs it on the way to writing"), t07 made imperative + n07 interrogative no-trigger added. Final: script-forge 14/14 · script-authoring-standards 13/13 · knowledge-harvest 29/29 (n13 routes to script-forge as intended) · skill-forge 18/18 (one judge skipped two ids despite the count clause — resumed, both pass; the 1.18.0 answer-count incident class, judge-side not suite-side). Known follow-up: four design-systems/typography .mjs checkers still carry no selftest — retrofit candidates for /script-forge, owned by their plugins · v1.24.0 · assembled 2026-07-14 · 1.24.0: skill-forge converted command species → procedural (disable-model-invocation: true → false, per explicit user direction) — description rewritten from slash-menu documentation into a real trigger contract (build/create/author/scaffold-a-new-skill phrasings), gains its own evals/evals.json (9 trigger / 8 no-trigger, floor-clear); reciprocal no-trigger cases (skill-forge's flagship phrasing) added to skill-decompose and skill-synthesize per skill-forge's own Phase 5 fence-closure rule. agent-forge/hook-forge/pack-forge/entry-file-audit stay command-only — asymmetry is deliberate, not yet reconciled; flagged for the user. eval_check + skill_lint clean; release_gate's one FAIL/WARN (knowledge-harvest docs+phantom-name) is pre-existing unrelated drift, left untouched · v1.23.0 · assembled 2026-07-12 · 1.23.0: entry-file-standards ships its seed — assets/engineering-operating-contract.md, the ~20-line global CLAUDE.md distilled by the standard's first full audit of the live 49-line operating contract (loop identity + four standing convictions + doctrine-skill pointer block); canonical direction recorded (installed copies refresh from the asset, never the reverse), scribe's project-docs-skill-template assets/ precedent followed · v1.22.0 · assembled 2026-07-12 · 1.22.0: the seat ladder — agent-authoring-standards §Model tiering rewritten from the 1.16.0 three-tier doctrine to the estate's adaptive ceiling ladder (planning fable+high, range high–xhigh · review/hard-bug analysis fable+high, range low–xhigh · coding opus+xhigh with sonnet/haiku step-downs · orchestration sonnet+high · mechanical haiku), frontmatter ruled the seat's DEFAULT with adaptivity at dispatch time (Agent-tool `model` override / Workflow `model`+`effort` opts; a plain Agent dispatch cannot vary effort — recorded as drift-prone mechanics); the five forge reviewers pinned inherit→fable+high (a verdict must not depend on the caller's tier); agent-forge's Config slot + skeleton repointed at the ladder (was `model: inherit` / 'only where the default is wrong') · v1.21.0 · assembled 2026-07-12 · 1.21.0: /repo-alignment — the user's proven repo-recalibrate campaign adopted into forge (renamed; body's phased methodology as-is): inventory/reconcile → unify → orphan manifest → schema + standing guards → audit verdicts → work packages → lessons distillation; integration edits only — fences to harness-audit (report-only vs committing campaign) and scribe's docs-alignment (grammar decided here, canonical-map migration delegated there, the campaign commits the staged result). FLOOR audit: pass, commit-ownership seam + self-name fixed pre-ship · v1.20.4 · assembled 2026-07-12 · 1.20.4: skill-authoring-standards gains the edit-tier ladder ('What an edit owes') — mechanical → lint only; description/boundary → lint + suite same-change + /eval-run at the wave boundary; semantic/new → the full critic loop — codifying the estate's proven practice as the forge-side twin of orchestration's solo-first floors, plus the fence-costs-characters re-budget clause and the tier-escalation rule · v1.20.3 · assembled 2026-07-10 · 1.20.3: author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder) · assembled 2026-07-09 · 1.20.2: pack-authoring-standards INDEX ruling — the threshold is enumerability, not authoring method: a flat ≤~7-file corpus whose consult table lists every reference 1:1 ships NO INDEX (a duplicate map drifts); INDEX.md earns its keep when files outgrow the table or subdirs exist (reconciles with scribe knowledge-forge's scaling note and blesses the shipped ui-patterns/motion-design/iconography practice) · 1.20.1: release_gate G8 allow set gains `attributes-as-api` — figma-plugin-api joining the estate added the -api suffix to the sibling inventory, false-flagging component-forge's references file; second batch same day: the a2a-* digit-prefix tokenizer artifact (agent-design/isolation-verify/agent-to-agent seen inside full a2a-* names — the regex skips digit-bearing segments) + agentic-ui prose compounds (selftest green) · · assembled 2026-07-09 · 1.20.0: description-hygiene convergence — G5 and G8 made sibling-aware (cross-plugin mentions and resolving `[[handles]]` no longer masquerade as rot; the sharpened G5 found the estate's ONE true dangling handle) + verified prose-compound allowlist; phantom legacy fences repointed (skill-synthesize rubric, intent-extract t04 rephrased — 'prompt brief' was itself the ambiguity); ADR-0001 sweep's corruption of the v1.1.0 historical note restored · assembled 2026-07-09 · 1.19.1: entry-file-standards suite annotated for the accepted command-off-menu leak class · assembled 2026-07-09 · 1.19.0: ADR-0001 executed — skill_lint W4 gains a genuine-verb allowlist (refactor et al., selftest-locked: verb heads pass, agentive 'author' still warns); all cross-plugin references to the eight renamed skills swept · assembled 2026-07-09 · 1.18.1: eval-run tuning — linguistic-techniques fenced off the ask/brief itself (intent-extract's territory), plugin-authoring-standards gained 'where a plugin's state or config lives'; the command-off-menu accepted-leak class annotated across five standards/decompose suites · assembled 2026-07-09 · 1.18.0: first harness-audit + estate-wide /eval-run fix wave — agent-reviewer/skill-auditor's DEEP tier dropped its dead `skills:` preloads (agents-audit/skills-audit are command-only, which blocks preloading — the audit's one blocking finding, caught by the audit's own fresh-context review) in favor of Read-by-path; Failure-branches sections added to both audit skills; eval-run's judge contract gained the answer-count clause (metabolized incident: skipped ids read as false failures); handoff-compose's best-practices repointed skill-reviewer→skill-auditor; the inline handoff fallback 'Tests run'→'Tests/checks run' (failed handoff_check's own H1 gate as written) · assembled 2026-07-07 · 1.17.0: closed the last confirmed pre-migration gap — `agents-audit` and `skills-audit` ported (CORPUS pass + DEEP-review CAMPAIGN against each estate's own standard-of-excellence.md), `harness_checks.py`+`routing_eval.py` absorbed as the shared M1/M2 gate scripts both depend on; `agent-reviewer` and `skill-auditor` regained the DEEP tier they were stripped of when first built (agents-audit didn't exist yet); fixed a real bug found while porting — `agent_corpus_index.py`'s frontmatter parser silently corrupted any multi-line `skills:` YAML list (forge's own house style, including its pre-existing skill-auditor) to a single dash-prefixed dangling entry, now handles both YAML shapes with a regression test · 1.16.0: model-tiering doctrine in agent-authoring-standards (mechanical/judgment/capable-execution, with `eval-judge`+`pack-researcher` pinned to a small model as the worked example); pilot-slice guidance in harness-audit + plugin-forge before a large fan-out; MANUAL's cadence habits sharpened into concrete `/schedule` recipes; skill-forge/plugin-release cross-reference orchestration's loop-design as the shared goal-condition doctrine · 1.15.0: handoff-compose absorbed as the fourth cross-cutting layer; four fresh-context reviewer agents (agent-/hook-/plugin-/linguistics-reviewer) close forge's own reviewer-agent gap, found via plugin-decompose against the pre-migration corpus · 1.14.0: declared agents where structure beats spawning (eval-judge: no-tools blindness; pack-researcher: phase-boundary allowlist) — everything else stays ad-hoc per the fork-vs-agent gate · 1.13.0: gap analysis (plugin-decompose Phase 2.6 + surface_map gaps; anti-matrix guard: absence needs job evidence; plugin-forge charter-coverage line) · 1.12.0: reasoning-orders knowledge skill + plugin-decompose escalation phase (partition as refactor opportunity; anti-tidying isomorphism test; routed refactor-opportunities ledger) · 1.11.0: plugin-decompose + surface_map.py (partition an existing surface into 1–5 plugins; direction-agnostic, no synthesize sibling needed) · 1.10.0: docs_check.py + gate G10 (docs freshness as a ship invariant) · 1.9.0: knowledge family (pack-authoring-standards, /pack-forge, corpus_check.py, gate G9, INDEX write-hook) — every 'no forge owner yet' handoff now owned · 1.8.0: /plugin-forge composer, gate G8 (stale sibling names), skill-forge fence-closure step + knowledge-grounding handoff · 1.7.0: /skill-refactor executor (closes the decompose/synthesize hand-off hole; refactor_apply.py with plan/apply/attic/sweep) · 1.6.1: MANUAL.md user guide (ships in artifact) · 1.6.0: eval-suite write-hook coverage, dev harness · 1.6.0: write-hook coverage for eval suites (lint evals class), repo dev harness (CLAUDE.md + .claude/settings.json, packaging-excluded) · 1.5.0: imports skill-decompose + skill-synthesize (reviewed: dials declared, phantoms repointed, lexical-router claim amended to model-as-router, routing corpora converted to eval suites, reciprocal fences) · 1.4.0: eval family (/eval-run routing simulation, eval_check.py, gate G7) · 1.3.0: plugin family (/plugin-release, release_gate.py, P-rules), trigger-eval suites for all 9 model-invocable skills · 1.2.1: reserved-word rename + F8 · 1.2.0: Waves 1+2 · 1.1.0: absorbs the three packs · 1.0.1: agent frontmatter fix
