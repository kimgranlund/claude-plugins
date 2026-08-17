# harness — the skill-authoring family

One plugin, one domain (`skill-*`), every artifact type doing its own job:

> You run **`/make-skill`**, which interviews for intent, applies **`skill-writing-rules`**, and drafts the skill; **`skill-postwrite-invocation-lint`** objects to every malformed write until the frontmatter validates; the **`skill-checker`** — preloading **`check-skill`** and the standards — reports findings from a fresh context; the forge ships when all six gates read PASS.

And the control plane's other surfaces get the same treatment: **`/make-agent`**, **`/make-hook`**, **`/make-script`**, and **`/check-entry-file`** author against **`agent-writing-rules`**, **`hook-writing-rules`**, **`script-writing-rules`**, and **`entry-file-rules`**; **`/check-everything`** runs the outer loop — lint sweep, standards-preloading fan-out, terminal triage — over the whole surface on a cadence.

The plugin name (`harness`, distribution taxonomy) is deliberately disjoint from the domain prefix (`skill-`, domain taxonomy), so packaging renames nothing: `/harness:check-skill` locally shortens to `/check-skill`.

## Map

| Artifact | Type | Invocation | Job |
|---|---|---|---|
| `skills/skill-writing-rules` | Declarative skill | model-only | **The core artifact**: species, frontmatter discipline, body prose style, calibration, verified numbers (July 2026) |
| `skills/make-skill` | Orchestrator skill | user-only (`/make-skill`) | Six gated phases: route → intent interview → evals-first → draft → language pass → validate → ship |
| `skills/check-skill` | Procedural skill | both | Judgment-tier audit (R1–R8) with a schema'd report contract |
| `agents/skill-checker` | Agent | spawned | Fresh-context reviewer; preloads check-skill + standards; returns report by file |
| `skills/prompt-wording-rules` | Declarative skill (hybrid) | model-only | The language layer beneath every prompt-carrying artifact: twelve techniques, potency rubric (L1–L10), `potency_lint.py`; make-skill Phase 4 runs its Audit |
| `skills/find-intent` | Procedural skill | both (`/find-intent`) | Root-intent extraction: literal ask vs goal, delta taxonomy, batched multiple-choice forks, the Resolved Intent contract |
| `skills/find-open-questions` | Procedural skill | both (`/find-open-questions`) | Clears a session's backlog of unresolved items — an unanswered question, an unconfirmed assumption, a stray idea left undecided — into one batched AskUserQuestion round instead of a prose dump nobody actually resolves |
| `skills/break-down-problem` | Procedural skill | both (`/break-down-problem`) | Two-plane decomposition (OUTSIDE-IN × INSIDE-OUT) with five domain references and the deterministic `coverage_check.py` gate |
| `skills/agent-writing-rules` | Declarative skill | model-only | Agent files: thin-shell law, preload semantics, tool walls, cold-start language; doubles as fan-out audit criteria |
| `skills/make-agent` | Command | user-only (`/make-agent`) | Fork-vs-agent gate → dispatch interview → thin-shell draft → language pass → lint + spawn smoke test |
| `skills/hook-writing-rules` | Declarative skill | model-only | The check tier: routing test, event/output semantics, hook discipline, repair-affordance messages |
| `skills/make-hook` | Command | user-only (`/make-hook`) | Check-vs-judgment gate → interview → script + registration (selftest mandatory) → simulated-event validation |
| `skills/script-writing-rules` | Declarative skill | model-only | The deterministic tier: script anatomy, the selftest contract (negative control that bites, exit tri-state 0/1/2-skip), placement and pathing, the arithmetic-not-judgment boundary; canon for the audits' A4 dimension |
| `skills/make-script` | Procedural skill | both (`/make-script`) | Mechanize a hand-run check or prose checklist as `scripts/taskname.py\|mjs`: qualify → plan → confirm → author to the standard → validate (selftest green, negative control bites, caller wired, G4 sweeps it) |
| `skills/entry-file-rules` | Declarative skill | model-only | CLAUDE.md residency test, the routing table for evictions, the growing-dotfile physics |
| `skills/check-entry-file` | Command | user-only (`/check-entry-file`) | Classify every line → approval → migrate (landing artifact first) → cut → verify |
| `skills/check-everything` | Orchestrator | user-only (`/check-everything`) | Wave 2: inventory → lint sweep → standards-preloading fan-out → boundary-validated aggregation → terminal triage with three-strikes promotion |
| `skills/check-state` | Procedural skill | both (`/check-state`) | Read-only work-state report: four bundled collectors (git branches/worktrees/stashes · tickets/PRs via gh · ROADMAP/PLAN/TICKET docs · checkpoint delta) cross-referenced into Blocked-on-you → Ready-to-close → Drift → Delta → Counts, every finding naming its owning command; the run's one write is `.claude/ops/state-checkpoint.json` |
| `skills/what-shipped` | Procedural skill | both (`/what-shipped`) | Windowed activity report: bundled `collect_github.py` (PR merged/opened/open-now + issues, release-bot noise counted but excluded via `.author.type`, saturation-guarded, `## OK` trailer as the completeness signal) + the doc-writing-rules backend-resolver seam for tickets (local files / GitHub Issues / adapter), joined ticket↔PR with the residue — tickets with no PR — surfaced; report groups ≤5 workstreams with owners and grounded line counts |
| `skills/plugin-writing-rules` | Declarative skill | model-only | Plugins: atomic load, version-as-cache-key, reload semantics, paths/state, trust; the three load-failure classes as a ledger |
| `skills/adopt-plugin` | Procedural | both (`/adopt-plugin`) | Declare external plugins/marketplaces in a repo's `.claude/settings.json` (`extraKnownMarketplaces` + self-hosted marketplace.json wrapper for bare plugin repos) so contributors who trust the repo get the install prompt — portable past the authoring machine |
| `skills/ship-plugin` | Command | user-only (`/ship-plugin`) | Preflight (bump on approval) → release_gate.py → package to dist/ → report |
| `skills/clean-repo` | Command skill | user-only (`/clean-repo`) | Phased, evidence-driven, human-checkpointed alignment campaign for a drifted repo: inventory/reconcile → unify duplicates → orphan manifest → schema + standing guards → audit verdicts → work-package execution → lessons distillation; adopted 2026-07-12 from the user's proven repo-recalibrate; delegates canonical-map corpus relocation to docs' `/tidy-docs` |
| `skills/big-change-git-rules` | Declarative skill | model-only | The estate's own git operational lessons, citable: worktree placement/discard safety, merge semantics (the ten-branch delete-failure class), the silent-failure catalog (verify by re-reading, never a command's print), parallel-session reconcile, the ADR-0002 decision tree — five axes, each grounded in a dated 2026-07-16/17 incident; the three scripts below mechanize what it documents. Its consumer-side half, `fix-old-names` (+ `scripts/fix_old_names.py`, `renames.json`), moved to `authorkit` 2026-08-14 (issue #197, ADR-0011/D9 — a mechanically clean move, no shared-script dependency); still routing-collision-gated behind `naming-rules`' supersession note, since authorkit ships disabled in this workspace |
| `skills/plugin-install-facts` | Declarative skill | model-only | Verified per-channel install instructions for Claude Code plugins — the two-step marketplace-add→install rule with every accepted source form (github shorthand, git https/SSH, local dir/file, remote catalog), the documented npm/npx absence, `--plugin-dir` dev loads, CI forms, and the trust/scope/update lifecycle; 3-file corpus, all claims dated 2026-07-25. Person-side complement to `adopt-plugin` (repo-side declaration) and `plugin-writing-rules` (author-side shipping) |
| `skills/github-facts` | Declarative skill | model-only | GitHub's own Issue/PR/Discussion/Projects-v2 platform facts, cited and dated 2026-07-17 — deliberately disjoint from big-change-git-rules (that pack is OUR git mechanics; this one is GitHub's data model): Issue Types + Issue Fields vs. labels, sub-issues vs. the retired tasklist-block feature, the nine closing keywords and the one merge-strategy gap GitHub's own docs never closed, PR review/CODEOWNERS/merge-queue mechanics, Projects v2's GraphQL-only structure — seven axes plus a sources.md provenance file; the synthesis axis names where this workspace's own ADR-0002/doc-writing-rules convention aligns or diverges from the platform, without ratifying a change |
| `skills/naming-rules` | Declarative skill | model-only | The simple ("Fisher-Price") naming paradigm that governed this estate's names through 2026-08-13: five checkable tests (says-the-job, kind-audible, registry-verb, no-lore, loud-contrast), a per-kind shape table, the one-verb-per-concept registry. Carries an in-place supersession note as of ADR-0011 (2026-08-14): the GRAMMAR is superseded for new mints by `.claude/docs/spec/spec-naming-convention.md` (canon via authorkit's naming-audit validator), while every name this estate shipped before then is grandfathered verbatim (D8) — this file stays their accurate historical record, and its symmetry-hardline enforcement (skill_lint F9/A6) is unaffected; the full-estate rename map ships as an illustrative worked example at `references/estate-rename-map.md` |
| `skills/watch-tickets` | Procedural skill | model-only | issue-sorter's own per-firing procedure (issue #205, extracted from a 235-line agent body): discover/classify/trust-check/mint-or-hold, the REQ-011/REQ-013 first-firing interviews, the full failure catalog |
| `agents/issue-sorter` | Agent | spawned (scheduled + on-demand) | Standing intake/triage seat: classifies, dedupes, and routes features/bugs/tasks/issues/PRs onto the resolved ticketing backend per the watch/triage/trust SPEC (`.claude/docs/spec/spec-ticketing-watch-triage.md`); trust-gates unknown filers behind a durable friendlies allow-list; structurally barred from source edits, merges, or closes beyond the ticket record. Thin shell: preloads its own procedure (`watch-tickets`) + the write-sandbox contract (`ops-write-sandbox-rules`) + `github-facts` + `find-intent` — docs' `doc-writing-rules` is a different plugin, so the TICKET shape it needs is stated inline rather than preloaded (the hard plugin-preload boundary, not a soft mention) |
| `skills/sort-issues` | Command skill | user-only (`/sort-issues`) | Dispatches the `issue-sorter` agent above for an on-demand run; states the agent's own capture/author-only contract as a fixed banner before the first CONFIRMED-roster dispatch (never mere file existence — an unattended firing seeds the allow-list too, evidence-only), and — since the agent has no `AskUserQuestion` of its own — runs the REQ-011/REQ-013 interview here, in this command's own session, whenever the agent's report surfaces one pending. This workspace's first case of a skill and an agent sharing one name (a command dispatching its own-named standing seat), deliberate, not yet a rule |
| `skills/clean-git` | Procedural skill | model-only | repo-cleaner's own per-firing procedure (issue #205, extracted from a 167-line agent body): inventory/classify/execute-only-what's-gated, the abbreviated-report diff, the full failure catalog |
| `agents/repo-cleaner` | Agent | spawned (scheduled + on-demand) | Standing repo-hygiene seat: inventories worktrees/branches/PRs, executes cleanup ONLY through this plugin's own gated scripts (`campaign_close.py`/`gitignore_check.py`/`sync_main.py`) on independently-verified-merged findings, proposes (never mutates) everything else. Thin shell: preloads its own procedure (`clean-git`) + `ops-write-sandbox-rules` + `big-change-git-rules` + `github-facts` |
| `skills/watch-adrs` | Procedural skill | model-only | decision-watcher's own per-firing procedure (issue #205, extracted from a 240-line agent body): classify/judge/queue/advance across the three supported ADR-corpus dialects, the full failure catalog |
| `agents/decision-watcher` | Agent | spawned (scheduled + on-demand) | Standing periodic ADR-review seat: `scripts/adr_checkpoint.py` diffs the ADR corpus by content hash since the last firing (new/amended/newly-superseded, cost proportional to the delta not the corpus), each changed Decision judged against `save-lessons`'s own bar, candidates queued via `scripts/adr_queue.py` for ONE batched confirm round rather than blocking on a live human; structurally barred from authoring — a confirmed candidate's next step is a named `/make-pack`/`/make-skill`/`save-lessons` Phase-6 command, never a write this agent performs. Thin shell: preloads its own procedure (`watch-adrs`) + `ops-write-sandbox-rules` + `save-lessons` + `pack-writing-rules` — docs' `doc-writing-rules` is a different plugin, so the ADR frontmatter contract (`doc-type`/`id`/`status`/`supersedes`) is stated inline rather than preloaded |
| `skills/ops-write-sandbox-rules` | Declarative skill | model-only | The `.claude/ops/` write-sandbox contract (issue #125, canonicalized issue #205): why the four compute-only ops seats carry no `Write` tool, the fenced target-pathed payload shape, and how the dispatching session applies it (`/sweep-chores`'s own procedure, via `scripts/chore_sweep_apply.mjs`) — one statement, preloaded by all four ops-family agents instead of restated 90-110 words per file |
| `agents/chore-planner` | Agent | spawned (on-demand + by `/sweep-chores`) | The ops-family prioritization seat: turns seat reports (sweep mode) or durable `.claude/ops` state + live `gh` evidence (standalone) into ONE prioritized queue at `.claude/ops/plan.md` — every entry action·owner·evidence·size, the prior plan read on every dispatch as the carry-forward source, never evidence; fable+high (a queue verdict never rides the caller's tier). Preloads `write-handoff` + `ops-write-sandbox-rules` + `github-facts` |
| `skills/sweep-chores` | Procedural skill (both) | both (`/sweep-chores`, and `Skill(harness:sweep-chores)` cross-plugin) | Runs the ops-* family sweep directly: fans out decision-watcher + issue-sorter + repo-cleaner (Workflow tool preferred — `workflows/chore-sweep.js` — with an Agent-dispatch fallback identical in shape), applies every returned payload via `scripts/chore_sweep_apply.mjs`, hands the bundle to chore-planner. Issue #266 retired the `chore-lead` coordinator agent this used to dispatch (nothing non-mechanical survived — deterministic choreography, not a job for a model in the loop; #265 measured the old chain at 1.92x tokens/3.6x wall-clock vs. solo); reclassified from command-only to this species specifically so `teamwork:mobilize-chores` can invoke the identical procedure without duplicating it. Banner-before-sweep on the shared first-queue marker, scope instructions passed verbatim, single-seat asks redirected to their direct door |
| `workflows/chore-sweep.js` | Workflow script | invoked by `sweep-chores` (Workflow tool, when available) | Fans out the in-scope ops seats in parallel (`parallel()` + `agent()`, barrier-waited), then hands the bundle to chore-planner — the deterministic half of the former `chore-lead` choreography, as real reviewable code instead of a model-in-the-loop coordinator (issue #266). No filesystem access (platform constraint) — returns raw report text; applying any payload block stays `sweep-chores`'s own job |
| `scripts/chore_sweep_apply.mjs` | Script | CLI + selftest, invoked by `sweep-chores` | Extracts every fenced, target-pathed `.claude/ops/` payload block from a seat/planner report and writes it to its named path verbatim; flags a narrated-but-absent write claim (a wrote/emitted/produced/saved verb paired with a `.claude/ops/...` path, no matching block) and refuses any block whose target falls outside the sandbox — `chore-lead`'s own former step 3, mechanized (issue #266) |
| `skills/plan-chores` | Command skill | user-only (`/plan-chores`) | Dispatches the chore-planner agent above standalone — same pairing; banner-before-dispatch on the same marker, focus instructions passed verbatim (an emphasis, never a new entry contract), fresh-sweep asks redirected to `/sweep-chores` |
| `scripts/release_gate.py` | Script | CLI + selftest | G1–G11: manifest, structure, full lint (composes skill_lint), bundled selftests (py+js, exit tri-state), phantom sweep, package + same-version refusal, eval validation (composes eval_check), sibling names, packs (composes corpus_check), docs freshness (composes docs_check), style lint (ruff/eslint, ADR-0002) |
| `skills/check-routing` | Procedural skill | both (`/check-routing`) | Blind fresh-context routing simulation over the eval suites: menu → fan-out → routing matrix → tuning targets (stolen/leaked/dead); model-invocable since 1.41.0 (per explicit user direction, the 1.24.0 make-skill precedent) so "prove the routing" asks fire it directly. Runs against a plugin (`skills/*/evals/`) OR a project estate — a repo with its own `.claude/skills/*/evals/` and no plugin manifest, e.g. agent-ui's own `.claude/` tree — auto-detected by `eval_check.py`'s `detect_skills_root()`, `--estate` forces the latter (issue #253) |
| `skills/plan-skill-split` | Procedural | both (`/plan-skill-split`) | Imported family (source-corpus lineage): four evidence tests deciding whether a knowledge corpus splits — manifest + repair map or an honest no-split; `manifest_check.py` as gate |
| `skills/plan-skill-merge` | Procedural | both (`/plan-skill-merge`) | The formal inverse: four inverse tests + the plan-skill-split self-check deciding a merge; `consolidation_check.py` as gate |
| `skills/reshape-skill` | Command | user-only (`/reshape-skill`) | The executor sibling: applies validated decompose/synthesize manifests — plan→approve→apply→sweep proof; `refactor_apply.py` attics, never deletes |
| `skills/make-plugin` | Orchestrator | user-only (`/make-plugin`) | Domain → released plugin: the four decomposition tests run forward as design gates, family manifest ratified before scaffold, per-member forge loop, fence-graph closure, /check-routing proof |
| `skills/pack-writing-rules` | Declarative skill | model-only | Corpus doctrine: ask-shaped files, 3–7 axes, INDEX contract, grounding markers, research waves, snapshot freshness |
| `skills/make-pack` | Command | user-only (`/make-pack`) | Question-led research waves, one axis per wave: charter → question set → dated gather → distill → register → corpus_check |
| `scripts/corpus_check.py` | Script | CLI + selftest + hook (INDEX writes) + gate G9 | K1–K5: INDEX↔tree both directions, load budgets, grounding coverage, axis count |
| `skills/plan-plugin-split` | Procedural | both (`/plan-plugin-split`) | Distribution-layer partitioning: jobs-to-be-done clustering, hard/soft dependency edges, namespace separability, lifecycle ledger → 1–5 plugin manifest for /make-plugin; `surface_map.py` extracts the graph, kills hard-edge cuts, and surfaces negative space (`gaps`: dangling references + family matrix) |
| `skills/thinking-depth-rules` | Declarative skill | model-only | The n-order spectrum operationalized: escalation triggers, forge-scale worked cases per order, the rent rule (higher-order claims pay in checks and numbers), anti-pattern table (order cosplay, tidying-as-transformation) |
| `skills/checking-rules` | Declarative skill | model-only | Discipline for how a review actually runs: evidentiary rigor for dismissals, runtime checks over claims (not a changelog), steelmanning before filing a finding |
| `agents/routing-judge` | Agent | dispatch-only (/check-routing) | Blind routing judge; empty tool allowlist as the epistemic guarantee — cannot read what it must not see |
| `agents/fact-finder` | Agent | dispatch-only (/make-pack) | Gather-phase researcher; WebSearch/WebFetch/Read/Write only, preloads pack-writing-rules; the allowlist enforces gather≠distill |
| `skills/write-handoff` | Declarative skill (hybrid) | both | The team-report layer beneath every agent dispatch: Status·Summary·Files changed·Tests/checks run·Evidence·Risks·Open questions·Recommended next action, `handoff_check.py` as the mechanical gate; every reviewer agent below returns through it |
| `agents/agent-checker` | Agent | spawned | Fresh-context critic for one subagent file; preloads agent-writing-rules + write-handoff; gates on skill_lint's A1-A5 |
| `agents/hook-checker` | Agent | spawned | Fresh-context critic for one hook (registration + handler pair); preloads hook-writing-rules + write-handoff; gates on skill_lint's H1-H5, probes stdin adversarially |
| `agents/plugin-checker` | Agent | spawned | Fresh-context critic for one plugin's packaging; preloads plugin-writing-rules + write-handoff; gates on release_gate's G1-G10, holds the content boundary |
| `agents/wording-checker` | Agent | spawned | Fresh-context critic for the language layer of any prompt-carrying artifact; preloads prompt-wording-rules + write-handoff; leads with the instantiate-over-describe test |
| `skills/check-all-agents` | Declarative skill | both | The estate-level sibling to check-everything's outer loop: CORPUS pass (naming/language/frontmatter/skill-leverage, one sweep, `agent_corpus_index.py`) + DEEP-review CAMPAIGN (M1/M2/N/A/L/S dimensions against `references/standard-of-excellence.md`, portfolio verdicts); `agent-checker` and `skill-checker` gained a DEEP tier to serve this campaign |
| `skills/check-all-skills` | Declarative skill | both | The skill-corpus counterpart: CORPUS pass (naming/language/frontmatter/peer-composition, `corpus_index.py`) + DEEP-review CAMPAIGN against its own `references/standard-of-excellence.md`; ported alongside `harness_checks.py` + `routing_eval.py`, the shared M1/M2 gate scripts both audits depend on |
| `scripts/docs_check.py` | Script | CLI + selftest + gate G10 | R1–R5: README/MANUAL cover every skill, ledger version = manifest version, CLAUDE.md counts, script mentions — docs freshness as a ship invariant, deliberately not a per-write hook |
| `scripts/gitignore_check.py` | Script | CLI + selftest | G1/G2: a `.gitignore` rule matching nothing in the tree is stale (retire it); a known generated/tool-output dir (`.claude/worktrees`, `dist`, `__pycache__`, …) existing on disk with no ignore coverage is one `git add -A` from being committed — clean-repo's razor, mechanized |
| `scripts/campaign_close.py` | Script | CLI + selftest | The post-merge ritual, mechanized: PR state == MERGED (never touch the branch otherwise) → delete the remote branch AND REVERIFY it's gone (the ten-branch silent-delete-failure class, 2026-07-16) → gate the touched plugins (warn, not fail) |
| `scripts/sync_main.py` | Script | CLI + selftest | Pulling onto a possibly-dirty main without clobbering a parallel session: classify dirty-vs-incoming overlap → quarantine as a named stash → `--ff-only` pull → reverify HEAD by SHA (never trust a command's print alone — the 2026-07-17 truncated-pipe incident) |
| `scripts/adr_checkpoint.py` | Script | CLI + selftest | Cheap, deterministic ADR-corpus diff by content hash against a checkpoint: new / amended / newly-superseded (read from a declared field or table row, never inferred from loose prose) / unchanged — cost stays proportional to what changed, never to corpus size; `decision-watcher`'s only economic lever. Parses three dialects (`status:` frontmatter · an `# ADR-NNNN` H1 + blockquote status table · one file of `## ADR-NNN` sections) and FAILS LOUDLY (exit 1, "unsupported shape") rather than reporting a clean empty delta when non-empty input yields zero ADRs |
| `scripts/adr_queue.py` | Script | CLI + selftest | Durable held-queue for ADR-review candidates: append-or-update by (adr, kind) — a re-detected candidate updates in place, never duplicates — so a scheduled firing never blocks on a live human; one batched confirm round clears however many accumulated |
| `scripts/eval_check.py` | Script | CLI + selftest | E1–E6: suite schema, id/owner identity, prompt dedup, case-mix floors, plugin-wide coverage |
| `scripts/skill_lint.py` | Script | CLI + selftest + gate G3 (PostToolUse hook retired 2026-08-17, #466 — remove-all-hooks directive) | Check tier: skill F/W rules; agent A1–A5 (YAML shape, thin shell, allowlist); hooks H1–H5 (wrapper, shape, portable paths); CLAUDE.md C1–C2 in CLI mode only |

Check/judgment split by design: everything mechanically decidable lives in `skill_lint.py` (run `python3 scripts/skill_lint.py selftest` to prove the counters); `check-skill` scores only what requires a model.

## Evals

Every model-invocable skill carries `evals/evals.json` — should-trigger prompts from its description's phrasings plus near-miss should-nots aimed at the sibling that owns them, so the suites double as routing regressions for the whole family. Run them via skill-creator's description-tuning loop or the fresh-session baseline procedure in `skill-writing-rules`.

For a human-facing guide to every skill with example prompts, see `MANUAL.md` (ships in the artifact; the harness never loads it).

## Developing harness itself

The repo carries its own dev harness: a root `CLAUDE.md` (invariants + map for Claude Code sessions editing this repo) and `.claude/settings.json` registering the same post-write lint repo-locally — so the guard fires even when the plugin isn't installed. Both are excluded from the packaged `.plugin` (gate G6): dev harness is not a distribution component. Suites in `skills/*/evals/evals.json` are now also linted at write time via the hook (E-rules delegated to `eval_check.py`).

## Install

```bash
# local development
claude --plugin-dir /path/to/harness

# or install the packaged .plugin / add to a marketplace, then
/plugin install harness
/reload-plugins
```

After installing into a large skill library, run `/doctor` — descriptions share a 1%-of-context listing budget.

## Load-bearing facts encoded here (verified 2026-07, drift-prone)

- **`disable-model-invocation: true` blocks subagent preloading** (and scheduled tasks, v2.1.196+). Preloadable modules are therefore *model-only* (`user-invocable: false`), which is exactly how `skill-writing-rules` and `check-skill` are flagged. The "both flags = library-only preload module" pattern is falsified — both flags set is unreachable by menu, discovery, *and* preloads.
- **The plugin version is the update cache key** — an edited plugin re-shipped under the same version is skipped by `/plugin update` as already installed. `release_gate.py` G6 refuses a same-version artifact.
- **Skill names cannot contain `claude` or `anthropic`** — reserved words rejected at install, failing the whole plugin load. Hence `/check-entry-file`, not `/claude-md-audit`; lint F8 now blocks the class at write time (incident 2026-07-06, the third metabolized into infrastructure).
- **Agent `<example>` blocks must live inside a block scalar** (`description: |`, indented). Schema examples that show them bare at column 0 produce frontmatter a strict YAML parser rejects, which fails the whole plugin load. The lint's A2 rule now blocks this class at write time (incident 2026-07-06, metabolized per the outer loop).
- Plugin `hooks.json` needs the outer `"hooks"` wrapper (plain `settings.json` snippets pasted without it fail silently).
- `allowed-tools` grants without prompting; it restricts nothing.
- Listing caps: 1% aggregate budget, 1,536-char per-entry cap, 1,024-char portability cap; body ≤500 lines; compaction keeps the first 5,000 tokens per skill, 25,000 combined.

On a Claude Code version bump, re-verify the standards' physics table against `/doctor` and the changelog.

## Snapshot rule

This plugin is the **source of record** for the `skill-*` family *and*, as of v1.1.0, for the absorbed packs `prompt-wording-rules`, `find-intent`, and `break-down-problem`. Copies placed in project knowledge (e.g. the corpus canon files) are snapshots: refresh them from here; never edit the copy. One canonical direction, chosen once.

**Self-sufficiency assumption (v1.1.0):** harness operates as the *only* installed skill surface. Every cross-skill reference resolves inside this plugin; references to retired sibling packs (`grill-the-ask`, `prd/spec/lld-author`, `layout/break-down-flow`, `component-author`, `agent/entry-file/rubric/knowledge-author`, and the `doc-checker` agent) were removed or redirected — semantic fences kept, phantom owners dropped, `break-down-problem`'s layout/components/ux references flipped from sibling-canon adapters to self-canonical (with an honest note on depth not carried). CHANGELOGs and `routing-corpus.json` eval data are historical/test artifacts and were vendored verbatim. **Amended 2026-07-07 (v1.15.0):** `wording-checker` is un-retired — a `plan-plugin-split` gap analysis against the pre-migration corpus found harness's own standards skills (agent/hook/plugin-writing-rules, prompt-wording-rules) each lacked the fresh-context reviewer agent every one of them already proved out; `agent-checker`, `hook-checker`, `plugin-checker`, and `wording-checker` close that gap, each re-pointed at harness's own tooling (`skill_lint.py`, `release_gate.py`) rather than the legacy corpus's incompatible scripts. `write-handoff` — needed by every one of them, and by every agent across the wider corpus — is absorbed as harness's fourth cross-cutting layer alongside find-intent, break-down-problem, and prompt-wording-rules.

If a skill is vendored out of the plugin (losing `${CLAUDE_PLUGIN_ROOT}`), the lint path from a skill body becomes `${CLAUDE_SKILL_DIR}/../../scripts/skill_lint.py`.

Directories align with plugin names (ADR-0007).

v3.8.28 · 2026-08-17 · `release_gate.py`'s G8 allowlist gains 14 entries clearing the standing warn (closes #488, surfaced by #483): retired-agent citations, a live-agent name, per-unit prose compounds, a measured literal, and a report-dir convention — zero repoints, all fencing. `release_gate.py harness` now reports 0 warn on G8. (Rebumped from 3.8.27 to 3.8.28: open PR #493 already claims 3.8.27 — rebase-and-rebump rather than race it.)

v3.8.27 · 2026-08-17 · `routing-judge` states its inlined-input contract loudly and refuses path-shaped dispatches instead of fabricating verdicts (closes #489).
v3.8.26 · 2026-08-17 · `find-open-questions` Step 1 sweeps dispatched seats' handback Open-questions blocks + needed-input items too (closes #483); batched-round mechanics untouched.

v3.8.25 · 2026-08-17 · closes #478, #479 (#295's ablation follow-ups): `thinking-depth-rules` dieted to its uniquely-owned content, reciprocal NOT-fence vs `docs:research-methods` added both sides; `find-intent`'s description broadened for a raw under-specified ask (rt1-class), guarded by no-theft cases. Routing-judge proof clean on all three touched suites.

v3.8.24 · 2026-08-17 · plugin-shipped hook retired (#466, Kim's remove-all-hooks directive): `hooks/hooks.json` (the `skill_lint.py` PostToolUse wiring) deleted; the script is unaffected and still runs via G3/G4 and CLI. No gate check asserted a hook must exist, so no gate amendment was needed.

v3.8.23 · 2026-08-17 · agent-description diet (closes #461, #373 Wave-2 S7): 8 agent frontmatter
descriptions (`agent-checker`, `chore-planner`, `decision-watcher`, `hook-checker`,
`issue-sorter`, `plugin-checker`, `repo-cleaner`, `skill-checker`) carrying a trailing NOT-for
disambiguation sentence had it moved into an exhaustive body NOT-for paragraph — `agent-checker`,
`hook-checker`, `plugin-checker` were already done; `skill-checker` had none at all, so one was
authored fresh — plus a reciprocal `watch-adrs` ↔ `watch-tickets` fence. `/check-routing harness`
ran 20/20 clean on the two touched suites, no stolen/leaked/dead/hung.

v3.8.22 · 2026-08-16 · `release_gate.py`'s G8 allowlist gains 9 entries surfaced by #433's
renames (closes #450): `lead-planning`/`lead-review`/`lead-product` (teamwork commands, not
skills), `product-leader-agent` (docs' agent name), `product-authoring` (leading-product's
pre-rename name, historical citation), `same-plugin`/`big-feature`/`index-bootstrap`/
`fleet-state` (prose compounds) — all false positives against the skill-only inventory.

v3.8.21 · 2026-08-17 · `naming-rules`' estate-rename-map.md paradigm-name table updated to
`leading-teams` (was `lead-team`), reflecting #433's rename (mechanical, no doctrine change).

v3.8.20 · 2026-08-16 · closes #443: the stacked-PR merge rule (PR #437 auto-closed as child of
#424 when its parent branch was deleted, re-opened as PR #439) is now recorded in
`big-change-git-rules/references/merge-semantics.md` (new section + failure-catalog row, consult
table and description gain the routing phrase) — retarget the child to `main` + `git rebase
--onto origin/main <parent-old-tip>` BEFORE deleting the parent branch, since squash-merge also
orphans the child's copy of the parent's commits. `campaign_close.py` gains C4 (warn-only,
never blocks the delete): `gh pr list --base <branch> --state open` before the branch-delete
step names any open child PR still based on it; selftest covers the warning and the clean case.
Teamwork's `parallel-work-rules` mention deferred until PR #442 (teamwork's version slot) lands.

v3.8.19 · 2026-08-16 · `release_gate.py` gains G14 (closes #445): a touched plugin's version must
strictly exceed `origin/main`'s, and the README ledger's newest line must name that version — the
pre-merge, CI-visible tier `version_claim_check.py`'s cross-open-PR tier (#311/PR #329) cannot
fill on its own. New `scripts/version_monotonic_check.py` (selftest-proven on real git plumbing:
strictly-greater PASS, equal-version FAIL — the #425/#430 `2.16.3` collision as the negative
control — lower-version FAIL, ledger-mismatch FAIL, and origin/main-missing/untouched/new-plugin
all SKIP clean, never a false red) reuses `version_claim_check.py`'s `parse_version`/
`version_tuple` rather than restating them; `gate.yml` inherits G14 since CI runs the same script
(gains `fetch-depth: 0` so `origin/main` is resolvable). `dispatch-ticket`'s build path gains a
one-line note to re-read the plugin's version on `origin/main` right before opening the PR.
v3.8.18 · 2026-08-16 · `chore_sweep_apply.mjs` entry guard: `import.meta.url === \`file://${argv[1]}\`` was silently false under an install path with a space (Cowork's `~/Library/Application Support/...` — URL side percent-encodes, argv does not): `main()` never ran, exit 0, no output (seen live in an agent-ui `/sweep-chores` fallback). Now compares both sides via `realpathSync` (also covers macOS `/var`→`/private/var`); selftest gains a spaced-path negative control. No other harness script has the pattern; screens' `ui-probe.mjs` is space-safe, symlink-fragile (noted only).
v3.8.17 · 2026-08-16 · issue #402 (doctrine edge D06, live finding): make-agent's Phase-1 naming step gains a pointer to `naming-rules` — the forge previously taught only the legacy agentive-head check with no route to the naming paradigm, or (per naming-rules' own supersession note) the ADR-0011 spec a NEW name is actually checked against.
v3.8.16 · 2026-08-16 · issue #382: `write-handoff` states the sealed-vs-messaging handoff-channel precedence once — a sealed, record-first dispatch (`dispatch-ticket`'s Findings write-back) carries the block's routing-relevant subset inside its dated Findings entry instead of a separate mailbox message; a named teammate-mode seat still sends the full block. `team-or-solo-rules` (teamwork) gains a pointer to that rule.
v3.8.15 · 2026-08-16 · issue #380: make-agent Phase-2 skeleton fixed to match agent-writing-rules (ADR/#80) — `<example>` block moved out of the description scalar into a `## Dispatch examples` body section; line-45 instruction rewritten to state the routing-contract-only description rule. Rebased onto 3.8.14 and rebumped by PR #383's takeover session (coordinator dispatch, 2026-08-16) — 3.8.13 stayed reserved/skipped per the 3.8.14 note above; supersedes that note, this is the actual #383 rebump.
v3.8.14 · 2026-08-16 · DE-standards adoption (#377): `checking-rules` gains a semantic-diff soft size budget; `write-handoff` gains an optional review-path line + a medium-specific Evidence table; `merge_when_clean.py` passes the PR body as the squash commit's `--body` (Beams/Google practice), degrading to a bare `--squash` on an empty body — selftest gains `build_merge_cmd` coverage. 3.8.13 intentionally skipped, reserved for PR #383's own rebump (comment-coordinated to avoid a version-claim collision).
v3.8.12 · 2026-08-16 · new `scripts/merge_when_clean.py` (closes #371): mechanizes the coordinator's pre-merge CI wait — polls `gh pr view` for OPEN + MERGEABLE + `mergeStateStatus` CLEAN (the #364 incident's actual gap: the hand-run loop grepped for any SUCCESS check instead of requiring GitHub's own composite verdict), then `gh pr merge --squash`, then composes (imports, doesn't reimplement) `campaign_close.py` for the post-merge branch-delete-verify + optional gate sweep; selftest's negative control is the #371 mergeStateStatus-UNSTABLE-waved-through fixture
v3.8.11 · 2026-08-16 · #348 footer sweep: 3 harness packs' (big-change-git-rules, github-facts, prompt-wording-rules) stamped "Extending this pack" paragraph replaced with the one-line `Extension: governed by [[make-pack]]` citation per pack-writing-rules' new Extension-citation rule (3.8.9) — mechanical, bodies otherwise untouched
v3.8.10 · 2026-08-16 · `check-state`'s description gains a one-line disambiguation naming `docs:check-stage` (issue #336, `prd-lifecycle-stage-awareness.md`) as the sibling owning the lifecycle-position axis, reciprocal eval n13 added
v3.8.9 · 2026-08-16 · `pack-writing-rules` gains the "Extension citation" rule (closes #338): a
pack's growth-routing footer is a one-line citation — `Extension: governed by [[make-pack]]` —
stated once here instead of the ~150-char stamped paragraph copied across 28 pack SKILL.md files;
`make-pack`'s Phase 5 points to it. Existing footers left unswept (recorded choice, PR body) —
28-file/5-plugin sweep deferred to the overhaul.
v3.8.8 · 2026-08-16 · `make-plugin`'s Phase 3 gains the OUT-02 bootstrap step deferred from #316
(closes #333): new `scripts/mint_idr_bootstrap.py`, idempotent by construction (glob-detects an
existing `idr-0001*`, so the founding IDR draft + the product-brief living-index stub mint on a
target repo's genuine first bootstrap only, never duplicated on a repo's Nth `/make-plugin` run)
— `make-plugin` was confirmed the ill-fitting surface (a plugin skeleton owns no `.claude/docs/`
tree of its own) but the idempotent check is what keeps OUT-02's "exactly one" true regardless,
since no better-fitting whole-project bootstrap command exists yet in this workspace.
v3.8.7 · 2026-08-16 · Cross-PR version-claim coordination encoded (closes #311, evidence: the
#284/#285/#290 collision cluster): `big-change-git-rules/references/who-ships-what.md` gains a
"Cross-PR version-claim coordination" section — ONE version-bumping build in flight per plugin at
a time, a rebump stacks its predecessor's ledger entry byte-identically — plus a new script,
`scripts/version_claim_check.py` (selftest-proven, incl. the #284/#289 `3.6.2 -> 3.6.2` collision
as its own negative control fixture), the pre-merge coordinator-run tier release_gate/CI/
campaign_close each structurally cannot fill. Consult table and script list updated to match.
v3.8.6 · 2026-08-15 · `agent-writing-rules`' "Checker-seat consolidation" section repointed
post-execution (issue #293, cross-plugin): the section narrated authorkit's three
single-instrument batch-audit agents as the pending merge candidate; now records the merge as
executed — `estate-audit-agent` (one agent, `instrument`-parameterized) replaces
`naming-audit-agent`/`bloat-audit-agent`/`attention-audit-agent`, with `pattern-audit` joining as
a fourth instrument on the same merge. Narrative/reference update only — no description, frontmatter,
or behavioral change to this skill.
v3.8.5 · 2026-08-16 · F4 measured (issue #308, #274 follow-up): a live `claude -p` fork dispatch with a conflicting skill/agent `model:` pair proved the skill's `model:` deterministically wins (the spawn record's own `subagents/*.meta.json`, not self-report) — `skill-writing-rules`' Delegation-mechanics fact block gains the dated result and `check-skill`'s DM-R6 is un-capped from WARN to FAIL on a skill/agent model conflict
v3.8.4 · 2026-08-15 · `skill-writing-rules`' Delegation-mechanics fact block gains the F5 re-verify result (issue #309, #274 follow-up): a live `claude -p` run measured a `context: fork` skill blocking foreground exactly per R5's documented exception list (marker landed ~8.4s before process exit); F4/R6 precedence stays open, tracked separately at #308
v3.8.3 · 2026-08-16 · `agent-writing-rules`' seat-ladder section gains the model-inheritance-leak discipline (issue #313): an ad-hoc (no-definition) dispatch states its model explicitly, defaulting to the seat ladder's routine tier (`sonnet`); the fork-inheritance fact (a `context: fork` skill is always priced at the session's model, unpinnable) lands as a dated note beside it, plus a Failure-catalog row recording why no `A7`-sibling lint can see either class (prompt-time, not file-time)
v3.8.2 · 2026-08-16 · `agent-writing-rules` gains a Failure-catalog row for the nested-dispatch-and-wait stall (issue #310): a fork skill or NAMED dispatch from inside an already-dispatched agent completes to the ROOT session, never back to it — cites the four measured `teamwork:build-lead` incidents (#257/#282/#269/#280) and the teamwork fix
v3.8.1 · 2026-08-16 · checker retier (Kim's ruling): 5 *-checker agents move effort high→medium, model fable unchanged — review quality held at medium across the 2026-08-15/16 rounds while inherited-xhigh runs added cost, not findings; agent-writing-rules' seat-ladder review row updated with the dated ruling
v3.8.0 · 2026-08-16 · `chore-lead` RETIRED (issue #266, nothing non-mechanical survived — #265 measured 1.92x tokens/3.6x wall-clock vs. solo); choreography ported into `sweep-chores` (now "both"-invocable, own eval suite), new `workflows/chore-sweep.js` + selftested `scripts/chore_sweep_apply.mjs`; every live `chore-lead` reference repointed estate-wide
v3.7.5 · 2026-08-16 · `big-change-git-rules`' who-ships-what.md gains ADR-0013's harvest (batched confirm): dispatch-tier BLOCKED (measured), merge-tier still UNMEASURED for `autoMode.allow`; the stale ADR-0012 provenance citation is re-grounded in ADR-0013 with a dated amendment note
v3.7.4 · 2026-08-16 · Delegation-Mechanics Review Gate v2 (issue #274): `skill_lint.py` mechanizes R1/R2/R3 with F1-F3 negative-control fixtures proven biting; `check-skill` gains judgment-tier DM-R4/DM-R5/DM-R6 (DM-R6 WARN-capped pending the F4 fixture); `make-skill`'s interview gains the fork self-sufficiency/background questions; `skill-writing-rules` gains the dated fact block. F4/F5 are named live-harness follow-up experiments, not run here
v3.7.3 · 2026-08-16 · `checking-rules` gains the generator≠critic invariant's UNIT calibration (issue #272): semantic edits earn a critic dispatch at any diff size, mechanical edits (ledger trims, version renumbers) ride floor-tier verification; `agent-writing-rules` gains a checker-seat consolidation merge test, citing #293 as the one confirmed candidate
v3.7.2 · 2026-08-16 · `plugin-writing-rules`' Reload semantics gains prompt-cache reload hygiene (issue #271): a mid-session reload or description edit invalidates the ~26k-token always-on-description cache prefix, re-read uncached until the next boundary — batch reloads there instead, plus a matching Failure-catalog row
v3.7.1 · 2026-08-16 · `agent-writing-rules` gains the "delegate, don't dictate" dispatch-prompt rule (issue #267) — cold-start language item 8: state the goal + non-discoverable constraints + verify-against target, enumerate steps only where a named incident proved the seat gets them wrong; cites the #259–#264 label/size-mismatch dispatch as the worked example, plus a matching Failure-catalog row
v3.7.0 · 2026-08-15 · `agent-writing-rules` gains the dispatch-only one-sentence resident-description rule (issue #260) + `skill_lint.py` A8 flagging a dispatch-only marker paired with an oversized description; `fact-finder`/`routing-judge` swept and trimmed (~460/~660 chars down to one sentence each, detail moved to their bodies)
v3.6.4 · 2026-08-15 · two boilerplate-ref centralizations (issue #280): `ops-write-sandbox-rules` now owns the ops-family description template, `watch-adrs`/`watch-tickets`/`clean-git` fence back by name; `plan-skill-split` states its canonical split/merge-decision ownership once, `break-down-problem`/`make-skill`/`pack-writing-rules` trim to a name-only reference. Eval notes/comments updated same-change, no new fences so no new cases (renumbered from 3.6.3 — that slot went to PR #284's rebump)
v3.6.3 · 2026-08-15 · `big-change-git-rules`' who-ships-what.md gains ADR-0012's quick-build auto-merge exception (decision-watcher harvest): a dispatched subagent may `gh pr merge` only when the full QB0–QB7 predicate is all-green AND the sealed prompt carries the explicit `auto-merge: authorized` grant line — everything else still requires a human (rebumped from 3.6.2 — that number shipped via PR #289 mid-flight)
v3.6.2 · 2026-08-15 · reciprocal NOT-fences close the two remaining harness-side collision-baseline twins (issue #282, PR #278's recipe): `naming-rules` ↔ authorkit's `naming-conventions`, `check-skill` ↔ authorkit's `bloat-audit`, `break-down-problem` ↔ screens' `break-down-layout` — each gains a NOT-clause + a reciprocal eval case (new or a dated owner-comment on an existing one); attention-audit's LLM-tier-exemplar classification of these pairs stands unchanged
v3.6.1 · 2026-08-15 · save-lessons gains the make-reference fence (NOT authoring/reviewing the reference doc itself — this skill judges the bar, docs make-reference writes the doc) + reciprocal eval n14; the unfenced cross-plugin twin was found by authorkit attention-audit's first live run (PR #275 behavior check, score 42.3) — the collision the per-plugin eval runs structurally can't see
v3.6.0 · 2026-08-15 · `check-routing` gains estate-mode (issue #253): `eval_check.py`'s `detect_skills_root()` auto-detects a project ESTATE (`.claude/skills/*/evals/`, no plugin manifest — agent-ui's own layout) alongside the existing plugin convention, `--estate` forces it, new E7 (neither convention found); same skill, same phases 3-5, only root discovery is new
v3.5.4 · 2026-08-14 · release_gate's G8 allow-set gains `auto-merge` and `quick-build` (issue #244, ADR-0012): both are prose terms of art in teamwork's new quick-build path — `auto-merge` is also the literal `auto-merge: authorized` grant line dispatch-ticket greps for, so neither is renameable; standing suffix false-positive class (`-merge`/`-build`)
v3.5.3 · 2026-08-14 · `plan-plugin-split`'s evals gain n08 (issue #245) — the reciprocal-fence mirror closing authorkit's `overhaul-planning` n05 steal from this suite's side; eval-only, no description change here (no steal measured in this direction)
v3.5.2 · 2026-08-14 · release_gate gains G13 marketplace-coverage (the authorkit-invisible-in-/plugin incident: gated plugin must appear in the root marketplace.json when one exists; selftest fixtures prove fail/pass/not-applicable)
v3.5.1 · 2026-08-14 · `watch-adrs`/`adr_checkpoint.py` gain a second supersession signal (issue #221): an accepted ADR's own body prose (active-voice `supersedes ADR-NNNN`/`the *scope* halves of ADR-NNNN`) fires `newly_superseded_edges` when frontmatter `supersedes:` is permanently null (ADR-0011's case, T4-hook-frozen) — scope carried through, never a bare id; selftest uses ADR-0011's real body as positive control
v3.5.0 · 2026-08-14 · ADR-0011/D9 execution (issue #197): `fix-old-names` + `fix_old_names.py` + `renames.json` moved to `authorkit` (mechanically clean, no shared-script dependency); `skill_lint`'s retired W4/W5 naming-grammar checks removed (successor: authorkit's naming-audit validator, `--scope grammar`); `release_gate.py` gains G12 (naming grammar, feature-detected on the repo-root manifest); `naming-rules` carries an in-place supersession note
v3.4.0 · 2026-08-13 · new `blocked-by-rules` skill (issue #193, preloaded by `chore-planner`; disable-model-invocation: false, eval suite included) gives `chore-planner` the read/order steps for teamwork's `Blocked-by: #NN` ticket convention — agent stays thin-shell, cites the skill rather than absorbing the logic
v3.3.1 · 2026-08-13 · chore-lead.md step 5 nested-coordinator branch names its SendMessage delivery target (issue #214) — dispatching coordinator by name in teammate mode, host session otherwise — citing agent-writing-rules' Failure catalog (gh#154/gh#157 misaddress class)
v3.3.0 · 2026-08-13 · ops-family thin-shell fix (issue #205): decision-watcher/issue-sorter/repo-cleaner's inline procedures extracted to preloaded skills (watch-adrs/watch-tickets/clean-git, 240/235/167 lines -> 70/78/66), the ops-write-sandbox rationale and bare-name-dispatch mechanism deduped to one canonical citation each (ops-write-sandbox-rules; agent-writing-rules' own Failure catalog)
v3.2.2 · 2026-08-13 · footer ledger contract capped at one line per entry (issue #203); harness/docs ledgers regenerated to this format, plugin-writing-rules' §Release discipline states the cap and the compress-never-delete rotation rule
v3.2.1 · 2026-08-12 · `campaign_close.py` arg parsing hardened (issue #188)
v3.1.31 · 2026-08-12 · big-change-git-rules' evals re-judged for t15 (issue #179) — steal did not reproduce, single-judge noise annotated, no SKILL.md touched
v3.1.30 · 2026-08-12 · `skill_lint.py`'s `classify()` fix (issue #178, root-caused upstream in adiahealth/gen-ui-kit#1071)
v3.1.29 · 2026-08-12 · skill-writing-rules' evals re-judged for t01 (issue #177) — steal did not reproduce, single-judge noise annotated, no SKILL.md touched
v3.1.28 · 2026-08-12 · naming-rules' evals annotated for n02 (issue #176) — accepted-leak class noted, no fence added, no SKILL.md touched
v3.1.27 · 2026-08-12 · make-script gains a NOT-for one-off-script fence (issue #175), merged into its existing NOT clauses; t04 re-judge closes clean
v3.1.26 · 2026-08-12 · find-open-questions' evals annotated for n11 (issue #174) — accepted-leak class (owner: teamwork's close-session, off-menu)
v3.1.25 · 2026-08-12 · check-state's description gains a NOT-clause fencing out single-PR/issue status questions (issue #173), fence-grammar reworded to parse
v3.1.24 · 2026-08-12 · 3.1.23's labeled-counterexample exemption dated precisely
v3.1.23 · 2026-08-12 · rename sweeps stop eating their own counterexamples (issue #171)
v3.1.22 · 2026-08-12 · README Map artifact-name repair
v3.1.21 · 2026-08-12 · the adr-0010 harvest lands (both asks Kim-confirmed in one batched round; queue row cleared) plus the labels-only ruling
v3.1.20 · 2026-08-11 · first /check-everything estate audit's harness fixes — agent-writing-rules routing gap closed, chore-lead's unclosed paren fixed, G8 allow-set gains four triaged terms
v3.1.19 · 2026-08-10 · fixes issue #157 — chore-lead's fanned-out dispatches drop the `name` arg so reports return to the true dispatcher, not a stranded `team-lead` default
v3.1.18 · 2026-08-10 · fixes issue #156 (two incidents, `/mobilize-chores` sweeps #21/#22 in adiahealth/gen-ui-kit, 2026-08-10)
v3.1.17 · 2026-08-10 · save-lessons harvest
v3.1.16 · 2026-08-10 · the intent-record exclusion goes suffix-only, and the canonical home moves out of agents/ for good
v3.1.15 · 2026-08-10 · the agent intent record's canonical home moves to `agents/intents/`
v3.1.14 · 2026-08-10 · G8 allow-set gains `nested-intake`
v3.1.13 · 2026-08-10 · skill_lint learns the agent intent record
v3.1.12 · 2026-08-10 · ADR-0010 rename sweep
v3.1.11 · 2026-08-10 · fixes issue #154 (live in adiahealth/gen-ui-kit, sweep #21 of `/mobilize-chores`, 2026-08-10)
v3.1.10 · 2026-08-09 · `agent-writing-rules`' Preload semantics gains the fix pattern for a command skill (`disable-model-invocation: true`) that needs a programmatic entry point too
v3.1.9 · 2026-08-08 · fixes issue #144 (save-lessons harvest, this session's own close-session pass)
v3.1.8 · 2026-08-08 · two issue-driven fixes, plus a caught-and-reverted own mistake. Fixes #138
v3.1.7 · 2026-08-08 · fixes issue #131 (mobilize-chores' live run this session)
v3.1.6 · 2026-08-08 · adr_checkpoint gains a third directory dialect
v3.1.5 · 2026-08-07 · sweep-chores' description gains a one-line discoverability pointer to teamwork's new `/mobilize-chores` (which wraps this command and adds a human-gated build step)
v3.1.4 · 2026-08-05 · silent-failure-catalog gains its sixth dated instance (save-lessons harvest, closing the loop on issue #125/PR #126)
v3.1.3 · 2026-08-05 · skill_lint gains A7
v3.1.2 · 2026-08-05 · the ops-write sandbox split (issue #125)
v3.1.1 · 2026-08-04 · adr_checkpoint parses the H1+status-table ADR dialect (agent-ui's shape) alongside frontmatter, auto-detected per file, and 0 parsed ADRs from a non-empty corpus now exits 1 'unsupported shape'
v3.1.0 · 2026-07-30 · what-shipped
v3.0.1 · 2026-07-30 · docs' file-leftovers fence closure
v3.0.0 · 2026-07-30 · ADR-0009
v2.6.1 · 2026-07-30 · plugin-install-facts enablement-merge correction lands (PR #109, merged 2026-07-30)
v2.6.0 · 2026-07-29 · the bare-minimum entry-file arc (user-ruled edits-to-the-owner, not a new skill — the anti-matrix/drift-twin razor applied to the pair itself).
v2.5.0 · 2026-07-29 · check-state
v2.4.5 · 2026-07-29 · silent-failure-catalog gains its fifth dated instance
v2.4.4 · 2026-07-27 · naming-rules gains one rationale line
v2.4.3 · 2026-07-26 · issue #95
v2.4.2 · 2026-07-26 · issue #102
v2.4.1 · 2026-07-26 · incident → infrastructure, same day, from a live `--write` run against THIS repo that falsified 190 lines across 12 files
v2.4.0 · 2026-07-26 · the alias-guard layer retired as INFEASIBLE — Task/Skill already validate names before PreToolUse fires, so the hook could never see a retired dispatch; 2.2.0/2.3.0 claims retracted
v2.3.0 · 2026-07-26 · the retired-name guard becomes standing infrastructure
v2.2.1 · 2026-07-26 · incident → infrastructure, same day.
v2.2.0 · 2026-07-26 · the consumer-side half of a rename wave (issue #97).
v2.1.2 · 2026-07-25 · `adr_checkpoint.py` gains a single-file scan mode
v2.1.1 · 2026-07-25 · description diet (PR #92)
v2.1.0 · 2026-07-25 · new `plugin-install-facts` knowledge pack
v2.0.12 · 2026-07-25 · adr_checkpoint.py's classify_delta fixed to key on the bare adr-NNNN token, not the whole annotated supersedes string, so newly_superseded stops false-refiring
v2.0.11 · 2026-07-25 · adopt-plugin's marketplace-source guidance corrected — SSH URL form preferred over HTTPS, npm source documented; G11 ruff select-line gap fixed estate-wide
v2.0.10 · 2026-07-23 · the naming-symmetry hardline
v2.0.9 · 2026-07-22 · issue #79's resident-cost diet, skill half — 31 harness descriptions trimmed (27,642→15,654 chars), skill_lint gains the W8 budget-warn ratchet
v2.0.8 · 2026-07-22 · issue #80's resident-cost diet, the agent half
v2.0.7 · 2026-07-21 · the #78 ship-leg capture
v2.0.6 · 2026-07-22 · two knowledge captures from the ADR-0008 close-out
v2.0.5 · 2026-07-21 · two script-CLI hardening fixes — sync_main.py's strict parse_cli rejects bad argv, skill_lint's classify() absolutizes paths before keying on parent dir names
v2.0.4 · 2026-07-21 · ADR-0008 design-merge sweep
v2.0.3 · 2026-07-21 · entry-file-rules' operating-contract seed names `doc-writing-rules` explicitly (was the vague post-rename "docs' standards")
v2.0.2 · 2026-07-21 · ADR-0007 dir alignment
v2.0.1 · 2026-07-21 · release_gate G2 gains the broken-symlink FAIL with selftest controls (the ADR-0006 docs-rename symlink incident that crashed Linux CI)
v2.0.0 · 2026-07-21 · ADR-0006 rename PR 9/9
v1.42.8 · 2026-07-21 · ADR-0006 docs-rename sweep
v1.42.7 · 2026-07-21 · ADR-0006 teamwork-rename sweep
v1.42.6 · 2026-07-21 · ADR-0006 screens-rename sweep
v1.42.5 · 2026-07-21 · ADR-0006 design-kits-rename sweep
v1.42.4 · 2026-07-21 · ADR-0006 agent-protocols-rename sweep
v1.42.3 · 2026-07-21 · ADR-0006 llm-rename sweep
v1.42.2 · 2026-07-21 · ADR-0006 typography-rename sweep
v1.42.1 · 2026-07-21 · ADR-0006 color-rename sweep
v1.42.0 · 2026-07-21 · ADR-0006 Phase 0
v1.41.0 · 2026-07-20 · eval-run converted command species to procedural, gains its own evals/evals.json; naming-rules' n05 leak and git-campaign-workflows' t08 dead case fixed in the same wave
v1.40.0 · 2026-07-20 · naming-rules
v1.39.0 · 2026-07-20 · the ops-family grows its coordination pair
v1.38.0 · 2026-07-20 · `/ops-issues`
v1.37.0 · 2026-07-20 · `ops-issues` gains REQ-013
v1.36.0 · 2026-07-20 · ops-adr — a new standing agent closing the periodic-ADR-review gap: adr_checkpoint.py/adr_queue.py diff by content hash, queue durably, never author
v1.35.0 · 2026-07-19 · absorbed knowledge-forge (retired, duplicated pack-forge with no corpus-integrity gate); skill-authoring-standards gains a Knowledge pack body-style subsection
v1.34.14 · 2026-07-19 · fixed a stale, actively-misleading claim in `system-decompose`'s domain references, found by a `plugin-decompose` gap analysis run against a candidate "consolidate the two-plane decomposition method"
v1.34.13 · 2026-07-19 · `open-questions-sweep` gains a reciprocal NOT-for fence pointing at orchestration's new `session-close` skill
v1.34.12 · 2026-07-19 · ADR-0004 dual-write, corrected
v1.34.11 · 2026-07-19 · ADR-0005 ticket-claim protocol
v1.34.10 · 2026-07-19 · ADR-0004 dual-write, implemented (Issue #44)
v1.34.9 · 2026-07-18 · eval-run forge + orchestration tuning — 493-case blind-judge sweep found 16 failures, 9 fixed at the description layer, 15/15 non-judgment-call re-verified
v1.34.8 · 2026-07-18 · pack-authoring-standards' canonical-reachability check (Issue #48, a same-day `/review` follow-up to #45/#40)
v1.34.7 · 2026-07-18 · reviewer-discipline (Issue #39)
v1.34.6 · 2026-07-18 · pack-authoring-standards gains a canonical-reachability check (Issue #40)
v1.34.5 · 2026-07-18 · xhigh code review of open-questions-sweep's own PR found 6 real defects the P5 FLOOR audit missed, all fixed same-change
v1.34.4 · 2026-07-18 · ops-issues' minted-record-shape restatement gained the git-native labeling clause it was missing
v1.34.3 · 2026-07-18 · open-questions-sweep
v1.34.2 · 2026-07-18 · ops-issues first-run bootstrap contract (spec-ticketing-watch-triage 0.2.0, REQ-011/REQ-012) — evidence-only friendlies seeding, one AskUserQuestion round, hold-first-filing ruled
v1.34.1 · 2026-07-18 · ops-repo's session-scoped `CronCreate` deployment ruled (Issue #32)
v1.34.0 · 2026-07-17 · reciprocal no-trigger fences added for orchestration's new concurrency-design skill; G8 allow-set gains `self-report`
v1.33.0 · 2026-07-17 · ops-issues + ops-repo
v1.32.0 · 2026-07-17 · github-issue-pr-primitives
v1.31.0 · 2026-07-17 · git-campaign-workflows (Issue #24)
v1.30.0 · 2026-07-17 · the git mechanization wave (Issues #19 + #23)
v1.29.0 · 2026-07-16 · harness-audit fixes
v1.28.1 · 2026-07-16 · G8 allow set gains order-vs-task-flow
v1.28.0 · 2026-07-16 · the six standards amendments from the external-skill review (Issue #11, each citing its repo@sha evidence)
v1.27.0 · 2026-07-15 · /plugin-onboard
v1.26.4 · 2026-07-15 · the 1.26.3 razor's placement claim amended in place (dated note)
v1.26.3 · 2026-07-15 · repo-alignment gains the .gitignore-is-a-record razor (ruled 2026-07-15)
v1.26.2 · 2026-07-15 · release_gate G8 allow set gains transport-and-streaming (a2a-protocol references file, the standing false-positive class)
v1.26.1 · 2026-07-15 · subfolder conformance (ruled 2026-07-15) — sanctioned skill-subfolder set is evals/references/scripts/assets, G2 warns on any other; linguistic-techniques' resources/-vs-references/ split retired
v1.26.0 · 2026-07-15 · gate G11
v1.25.1 · 2026-07-15 · release_gate G8 allow set gains three new-plugin tokens (container-patterns, scale-theory, design-systems) plus three prose compounds — the standing false-positive class
v1.25.0 · 2026-07-14 · displayName 'Forge' added to the manifest (plugin naming hygiene ruled 2026-07-14: Title Case display names estate-wide, UI/LLM acronyms uppercased; plugin-authoring-standards records the verified field semantics).
v1.24.0 · 2026-07-14 · skill-forge converted command species → procedural (disable-model-invocation: true → false, per explicit user direction)
v1.23.0 · 2026-07-12 · entry-file-standards ships its seed
v1.22.0 · 2026-07-12 · the seat ladder
v1.21.0 · 2026-07-12 · /repo-alignment
v1.20.4 · 2026-07-12 · skill-authoring-standards gains the edit-tier ladder ('What an edit owes')
v1.20.3 · 2026-07-10 · author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder)
v1.20.2 · 2026-07-09 · pack-authoring-standards INDEX ruling
v1.20.1 · 2026-07-09 · release_gate G8 allow set gains `attributes-as-api`
v1.20.0 · 2026-07-09 · description-hygiene convergence
v1.19.1 · 2026-07-09 · entry-file-standards suite annotated for the accepted command-off-menu leak class
v1.19.0 · 2026-07-09 · ADR-0001 executed
v1.18.1 · 2026-07-09 · eval-run tuning
v1.18.0 · 2026-07-09 · first harness-audit + estate-wide /eval-run fix wave
v1.17.0 · 2026-07-07 · closed the last confirmed pre-migration gap
v1.16.0 · 2026-07-07 · model-tiering doctrine in agent-authoring-standards (mechanical/judgment/capable-execution); pilot-slice guidance, /schedule cadence recipes, and the shared goal-condition doctrine
v1.15.0 · 2026-07-07 · handoff-compose absorbed as the fourth cross-cutting layer; four fresh-context reviewer agents close forge's own reviewer-agent gap
v1.14.0 · 2026-07-07 · declared agents where structure beats spawning (eval-judge: no-tools blindness; pack-researcher: phase-boundary allowlist)
v1.13.0 · 2026-07-07 · gap analysis (plugin-decompose Phase 2.6 + surface_map gaps; anti-matrix guard: absence needs job evidence; plugin-forge charter-coverage line)
v1.12.0 · 2026-07-07 · reasoning-orders knowledge skill + plugin-decompose escalation phase (partition as refactor opportunity; anti-tidying isomorphism test; routed refactor-opportunities ledger)
v1.11.0 · 2026-07-07 · plugin-decompose + surface_map.py (partition an existing surface into 1–5 plugins; direction-agnostic, no synthesize sibling needed)
v1.10.0 · 2026-07-07 · docs_check.py + gate G10 (docs freshness as a ship invariant)
v1.9.0 · 2026-07-07 · knowledge family (pack-authoring-standards, /pack-forge, corpus_check.py, gate G9, INDEX write-hook)
v1.8.0 · 2026-07-07 · /plugin-forge composer, gate G8 (stale sibling names), skill-forge fence-closure step + knowledge-grounding handoff
v1.7.0 · 2026-07-07 · /skill-refactor executor (closes the decompose/synthesize hand-off hole; refactor_apply.py with plan/apply/attic/sweep)
v1.6.1 · 2026-07-07 · MANUAL.md user guide (ships in artifact)
v1.6.0 · 2026-07-07 · eval-suite write-hook coverage + dev harness (CLAUDE.md + .claude/settings.json, packaging-excluded)
v1.5.0 · 2026-07-07 · imports skill-decompose + skill-synthesize (reviewed: dials declared, phantoms repointed, lexical-router claim amended to model-as-router, routing corpora converted to eval suites, reciprocal fences)
v1.4.0 · 2026-07-07 · eval family (/eval-run routing simulation, eval_check.py, gate G7)
v1.3.0 · 2026-07-07 · plugin family (/plugin-release, release_gate.py, P-rules), trigger-eval suites for all 9 model-invocable skills
v1.2.1 · 2026-07-07 · reserved-word rename + F8
v1.2.0 · 2026-07-07 · Waves 1+2
v1.1.0 · 2026-07-07 · absorbs the three packs
v1.0.1 · 2026-07-07 · agent frontmatter fix
