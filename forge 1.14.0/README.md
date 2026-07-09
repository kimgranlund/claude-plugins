# forge — the skill-authoring family

One plugin, one domain (`skill-*`), every artifact type doing its own job:

> You run **`/skill-forge`**, which interviews for intent, applies **`skill-authoring-standards`**, and drafts the skill; **`skill-postwrite-invocation-lint`** objects to every malformed write until the frontmatter validates; the **`skill-auditor`** — preloading **`skill-review`** and the standards — reports findings from a fresh context; the forge ships when all six gates read PASS.

And the control plane's other surfaces get the same treatment: **`/agent-forge`**, **`/hook-forge`**, and **`/entry-file-audit`** author against **`agent-authoring-standards`**, **`hook-authoring-standards`**, and **`entry-file-standards`**; **`/harness-audit`** runs the outer loop — lint sweep, standards-preloading fan-out, terminal triage — over the whole surface on a cadence.

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
| `skills/system-decompose` | Procedural skill | both (`/system-decompose`) | Two-plane decomposition (OUTSIDE-IN × INSIDE-OUT) with five domain references and the deterministic `coverage_check.py` gate |
| `skills/agent-authoring-standards` | Declarative skill | model-only | Agent files: thin-shell law, preload semantics, tool walls, cold-start language; doubles as fan-out audit criteria |
| `skills/agent-forge` | Command | user-only (`/agent-forge`) | Fork-vs-agent gate → dispatch interview → thin-shell draft → language pass → lint + spawn smoke test |
| `skills/hook-authoring-standards` | Declarative skill | model-only | The check tier: routing test, event/output semantics, hook discipline, repair-affordance messages |
| `skills/hook-forge` | Command | user-only (`/hook-forge`) | Check-vs-judgment gate → interview → script + registration (selftest mandatory) → simulated-event validation |
| `skills/entry-file-standards` | Declarative skill | model-only | CLAUDE.md residency test, the routing table for evictions, the growing-dotfile physics |
| `skills/entry-file-audit` | Command | user-only (`/entry-file-audit`) | Classify every line → approval → migrate (landing artifact first) → cut → verify |
| `skills/harness-audit` | Orchestrator | user-only (`/harness-audit`) | Wave 2: inventory → lint sweep → standards-preloading fan-out → boundary-validated aggregation → terminal triage with three-strikes promotion |
| `skills/plugin-authoring-standards` | Declarative skill | model-only | Plugins: atomic load, version-as-cache-key, reload semantics, paths/state, trust; the three load-failure classes as a ledger |
| `skills/plugin-release` | Command | user-only (`/plugin-release`) | Preflight (bump on approval) → release_gate.py → package to dist/ → report |
| `scripts/release_gate.py` | Script | CLI + selftest | G1–G7: manifest, structure, full lint (composes skill_lint), bundled selftests, phantom sweep, same-version refusal, eval validation (composes eval_check) |
| `skills/eval-run` | Command | user-only (`/eval-run`) | Blind fresh-context routing simulation over the eval suites: menu → fan-out → routing matrix → tuning targets (stolen/leaked/dead) |
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

**Self-sufficiency assumption (v1.1.0):** forge operates as the *only* installed skill surface. Every cross-skill reference resolves inside this plugin; references to retired sibling packs (`intent-grill`, `prd/spec/lld-author`, `layout/flow-decompose`, `component-author`, `agent/entry-file/rubric/knowledge-author`, and the `doc-reviewer` agent) were removed or redirected — semantic fences kept, phantom owners dropped, `system-decompose`'s layout/components/ux references flipped from sibling-canon adapters to self-canonical (with an honest note on depth not carried). CHANGELOGs and `routing-corpus.json` eval data are historical/test artifacts and were vendored verbatim. **Amended 2026-07-07 (v1.15.0):** `linguistics-reviewer` is un-retired — a `plugin-decompose` gap analysis against the pre-migration corpus found forge's own standards skills (agent/hook/plugin-authoring-standards, linguistic-techniques) each lacked the fresh-context reviewer agent every one of them already proved out; `agent-reviewer`, `hook-reviewer`, `plugin-reviewer`, and `linguistics-reviewer` close that gap, each re-pointed at forge's own tooling (`skill_lint.py`, `release_gate.py`) rather than the legacy corpus's incompatible scripts. `handoff-compose` — needed by every one of them, and by every agent across the wider corpus — is absorbed as forge's fourth cross-cutting layer alongside intent-extract, system-decompose, and linguistic-techniques.

If a skill is vendored out of the plugin (losing `${CLAUDE_PLUGIN_ROOT}`), the lint path from a skill body becomes `${CLAUDE_SKILL_DIR}/../../scripts/skill_lint.py`.

v1.20.0 · assembled 2026-07-09 · 1.20.0: description-hygiene convergence — G5 and G8 made sibling-aware (cross-plugin mentions and resolving `[[handles]]` no longer masquerade as rot; the sharpened G5 found the estate's ONE true dangling handle) + verified prose-compound allowlist; phantom legacy fences repointed (skill-synthesize rubric, intent-extract t04 rephrased — 'prompt brief' was itself the ambiguity); ADR-0001 sweep's corruption of the v1.1.0 historical note restored · assembled 2026-07-09 · 1.19.1: entry-file-standards suite annotated for the accepted command-off-menu leak class · assembled 2026-07-09 · 1.19.0: ADR-0001 executed — skill_lint W4 gains a genuine-verb allowlist (refactor et al., selftest-locked: verb heads pass, agentive 'author' still warns); all cross-plugin references to the eight renamed skills swept · assembled 2026-07-09 · 1.18.1: eval-run tuning — linguistic-techniques fenced off the ask/brief itself (intent-extract's territory), plugin-authoring-standards gained 'where a plugin's state or config lives'; the command-off-menu accepted-leak class annotated across five standards/decompose suites · assembled 2026-07-09 · 1.18.0: first harness-audit + estate-wide /eval-run fix wave — agent-reviewer/skill-auditor's DEEP tier dropped its dead `skills:` preloads (agents-audit/skills-audit are command-only, which blocks preloading — the audit's one blocking finding, caught by the audit's own fresh-context review) in favor of Read-by-path; Failure-branches sections added to both audit skills; eval-run's judge contract gained the answer-count clause (metabolized incident: skipped ids read as false failures); handoff-compose's best-practices repointed skill-reviewer→skill-auditor; the inline handoff fallback 'Tests run'→'Tests/checks run' (failed handoff_check's own H1 gate as written) · assembled 2026-07-07 · 1.17.0: closed the last confirmed pre-migration gap — `agents-audit` and `skills-audit` ported (CORPUS pass + DEEP-review CAMPAIGN against each estate's own standard-of-excellence.md), `harness_checks.py`+`routing_eval.py` absorbed as the shared M1/M2 gate scripts both depend on; `agent-reviewer` and `skill-auditor` regained the DEEP tier they were stripped of when first built (agents-audit didn't exist yet); fixed a real bug found while porting — `agent_corpus_index.py`'s frontmatter parser silently corrupted any multi-line `skills:` YAML list (forge's own house style, including its pre-existing skill-auditor) to a single dash-prefixed dangling entry, now handles both YAML shapes with a regression test · 1.16.0: model-tiering doctrine in agent-authoring-standards (mechanical/judgment/capable-execution, with `eval-judge`+`pack-researcher` pinned to a small model as the worked example); pilot-slice guidance in harness-audit + plugin-forge before a large fan-out; MANUAL's cadence habits sharpened into concrete `/schedule` recipes; skill-forge/plugin-release cross-reference orchestration's loop-design as the shared goal-condition doctrine · 1.15.0: handoff-compose absorbed as the fourth cross-cutting layer; four fresh-context reviewer agents (agent-/hook-/plugin-/linguistics-reviewer) close forge's own reviewer-agent gap, found via plugin-decompose against the pre-migration corpus · 1.14.0: declared agents where structure beats spawning (eval-judge: no-tools blindness; pack-researcher: phase-boundary allowlist) — everything else stays ad-hoc per the fork-vs-agent gate · 1.13.0: gap analysis (plugin-decompose Phase 2.6 + surface_map gaps; anti-matrix guard: absence needs job evidence; plugin-forge charter-coverage line) · 1.12.0: reasoning-orders knowledge skill + plugin-decompose escalation phase (partition as refactor opportunity; anti-tidying isomorphism test; routed refactor-opportunities ledger) · 1.11.0: plugin-decompose + surface_map.py (partition an existing surface into 1–5 plugins; direction-agnostic, no synthesize sibling needed) · 1.10.0: docs_check.py + gate G10 (docs freshness as a ship invariant) · 1.9.0: knowledge family (pack-authoring-standards, /pack-forge, corpus_check.py, gate G9, INDEX write-hook) — every 'no forge owner yet' handoff now owned · 1.8.0: /plugin-forge composer, gate G8 (stale sibling names), skill-forge fence-closure step + knowledge-grounding handoff · 1.7.0: /skill-refactor executor (closes the decompose/synthesize hand-off hole; refactor_apply.py with plan/apply/attic/sweep) · 1.6.1: MANUAL.md user guide (ships in artifact) · 1.6.0: eval-suite write-hook coverage, dev harness · 1.6.0: write-hook coverage for eval suites (lint evals class), repo dev harness (CLAUDE.md + .claude/settings.json, packaging-excluded) · 1.5.0: imports skill-decompose + skill-synthesize (reviewed: dials declared, phantoms repointed, lexical-router claim amended to model-as-router, routing corpora converted to eval suites, reciprocal fences) · 1.4.0: eval family (/eval-run routing simulation, eval_check.py, gate G7) · 1.3.0: plugin family (/plugin-release, release_gate.py, P-rules), trigger-eval suites for all 9 model-invocable skills · 1.2.1: reserved-word rename + F8 · 1.2.0: Waves 1+2 · 1.1.0: absorbs the three packs · 1.0.1: agent frontmatter fix
