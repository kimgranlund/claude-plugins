# harness — user manual

The plugin-authoring plugin: skills, agents, hooks, entry files, eval suites, and plugin releases, each with a standard that teaches it, a workflow that builds it, and a check that enforces it. This file is documentation for humans — the harness never loads it. The engineering ledger (versions, incidents, sharp edges) lives in `README.md`.

Install, then `/reload-plugins`. Everything below is invoked as `/harness:<name>` when unqualified names collide.

---

## Slash commands (you invoke these; the model never fires them on its own)

**`/make-plugin [domain or charter]`** — forge a whole plugin from a domain: charter interview, family design (question types, projected routing prompts, vocabulary separability, rejected-members ledger), scaffold, a /make-skill pass per member, fence-graph closure, /check-routing proof, release.
> `/make-plugin "a plugin with all the skills related to UI design"` · `/make-plugin api-review`

**`/make-skill [name or one-line intent]`** — forge a new skill end-to-end through six gated phases: route check, intent interview (the grilling), evals-first, species-template draft, language pass, validation.
> `/make-skill migration-runbook` · `/make-skill "a skill that reviews SQL migrations before they ship"`

**`/make-agent [name or job]`** — forge a subagent through five gated phases, starting with the fork-vs-agent route check (many "agents" should just be `context: fork`).
> `/make-agent changelog-writer` · `/make-agent "something that reviews PRs against our style guide"`

**`/make-hook [name or the rule to enforce]`** — forge a hook: check-vs-judgment gate, event/matcher interview, script + registration, simulated-event validation with a shipped selftest.
> `/make-hook "block commits that touch dist/"` · `/make-hook post-edit-prettier`

**`/check-entry-file [path]`** — classify every CLAUDE.md line against the residency test and migrate evictions down-stack (checks→hooks, procedures→skills, subtree truths→rules). Edits only on approval.
> `/check-entry-file` · `/check-entry-file packages/api/CLAUDE.md`

**`/check-everything [root]`** — the recurring outer loop: lint sweep, standards-preloading fresh-context reviews of every artifact, triage table routing each finding to a fix, a decision, or permanent infrastructure.
> `/check-everything` · `/check-everything ~/projects/monorepo`

**`/clean-repo [repo path] [--phases 0-6 | audit-only]`** — the committing campaign for a drifted repo (where `/check-everything` only reports): phased inventory → unify duplicates → orphan manifest → schema + standing guards → audit verdicts → work-package execution → lessons distillation; human-checkpointed at every destructive step.
> `/clean-repo .` · `/clean-repo ~/projects/app audit-only`

**`/fix-old-names [repo-root]`** — run this in a repo that INSTALLS these plugins, after a rename wave: it sweeps `.claude/**`, `CLAUDE.md`, and docs for retired plugin/skill/agent/command names from the shipped `renames.json`, and rewrites the ones that must still resolve. Reports first and writes only on `--write`; ADR bodies, ledgers, changelogs and dated records come back byte-identical; a name that became both a command and an agent is escalated to you rather than guessed. Exits 1 on live stale names, so the bare invocation doubles as a CI gate. Offers a `PreToolUse` guard for the runtime dispatches a file sweep can never see.
> `/fix-old-names .` · `/fix-old-names ~/projects/app` — then re-run to confirm zero live hits

**`/check-routing [plugin-root]`** — run the trigger-eval suites as a blind routing simulation: judges pick a skill from the description menu alone; you get a routing matrix and per-failure tuning targets (stolen / leaked / dead). Also model-invocable (1.41.0): "prove the routing after that description change" fires it without the slash.
> `/check-routing .` — worth running after any description edit

**`/reshape-skill [manifest.json]`** — execute a validated plan-skill-split or plan-skill-merge manifest: plan shown for approval, files moved, old surfaces retired to an attic (never deleted), referrers rewritten, sweep proven (zero live references to retired handles).
> `/reshape-skill split-manifest.json` — always after the decision skill's checker runs clean

**`/make-pack [skill-dir | new pack: domain]`** — mint or grow a knowledge pack's reference corpus through question-led research waves: ratified question set, dated gathering, ask-shaped distillation with confidence markers, INDEX/evals registration, corpus_check validation. One axis per wave.
> `/make-pack skills/ui-pattern-facts` · `/make-pack "new pack: design tokens"`

**`/ship-plugin [plugin-root]`** — release through the full gate: version bump on approval, `release_gate.py` (structure, manifest, full lint, bundled selftests, phantom sweep, eval validation), package to `dist/`.
> `/ship-plugin` · run `python3 scripts/release_gate.py . ` alone for a dry gate

---

## Procedures (ask in plain language, or invoke explicitly)

**`plan-skill-split`** — should a sprawling knowledge corpus split into a family, and into which packs? Four evidence tests; an honest no-split is a first-class verdict. Produces a reconciled manifest + referrer repair map, validated by `manifest_check.py`.
> "this skill has gotten enormous, break it up" · "is one entry surface enough for all these reference files" · `/plan-skill-split skills/color-science`

**`plan-skill-merge`** — the formal inverse: should several thin/overlapping skills merge into one pack? Inverse test battery plus the self-check (a merge must survive plan-skill-split's own tests or it's a relabeled monolith). Validated by `consolidation_check.py`.
> "these three skills all overlap, should they be one" · "we're loading five packs for basically one question, merge them"

**`plan-plugin-split`** — analyze an existing surface (skills + agents + hooks + scripts; frontmatter and structure suffice) and decide its partition into 1–5 portable plugins: dependency graph via surface_map.py, four distribution-layer tests, rejected-alternatives ledger, mechanically validated manifest handed to /make-plugin. Direction-agnostic — merging scattered plugins is the same partition with fewer groups. Also runs negative-space analysis: dangling handoffs and the family matrix surface what might be missing, under the anti-matrix guard (absence + job evidence = gap; absence alone = correctly absent).
> "which plugins should these skills become" · "should this mega-plugin be several smaller ones" · `/plan-plugin-split ~/.claude`

**`adopt-plugin`** — declare an external plugin or marketplace repo in a project's `.claude/settings.json` so every contributor who trusts the repo is prompted to install it: classifies each URL (marketplace repo → `extraKnownMarketplaces` entry; bare plugin repo → a self-hosted `marketplace.json` wrapper first), then verifies via `/plugin`. Project-scoped and portable — never an operator-local install masquerading as project config.
> "add this plugin repo so contributors can install it" · "declare a marketplace in settings.json" · `/adopt-plugin <url>`

**`check-skill`** — audit an existing SKILL.md against the standards; verdict-first findings report. The mechanical half runs first via `skill_lint.py`.
> "review this skill" · "this skill misfires constantly — what's wrong with it"

**`find-the-ask`** — separate the literal ask from the root goal before acting: surface ambiguities and conflicting signals, resolve them with low-effort multiple-choice questions, restate the task sharper.
> "figure out what this ticket is actually asking for" · "improve this prompt brief" · `/find-the-ask`

**`find-open-questions`** — clears a session's backlog of unresolved items (an unanswered question, an unconfirmed assumption, a stray idea left undecided) into one batched AskUserQuestion round, instead of a prose dump nobody actually resolves. Fires on its own at a session's natural closing point; also invocable directly.
> "before we wrap up, is there anything still open" · "any decisions still open before we close this out" · `/find-open-questions`

**`break-down-problem`** — break any system down along two crossing planes (whole→parts × actions→surfaces) and verify they cover each other. For architectures, UX, goals — not for knowledge-pack split decisions (that's plan-skill-split).
> "decompose this feature into parts" · "my acceptance criteria don't map to any task"

**`save-lessons`** — detects when a fact crosses the bar for durable project knowledge (a correction restated a third time, a ratified ADR/ticket/SPEC decision never captured, a high-impact convention worth keeping on first mention) and turns it into a knowledge-pack entry — always via an AskUserQuestion confirmation carrying the concrete plan before writing, never silently. Also runs a later, separately-invoked staleness pass that re-verifies a landed citation still holds. Orchestrates `make-pack` (authors), `release_gate.py` (structural gate), and `/check-routing` (routing gate) rather than reimplementing them.
> "this is the third time I've explained this" · "is this actually project knowledge or just noise" · "check if our harvested knowledge is still accurate"

**`check-all-agents`** — audit a whole `agents/` team as one system, two modes: a CORPUS pass (naming coherence, linguistic potency, front-matter as an interface, skill-leverage graph — one sweep) or a DEEP-review CAMPAIGN against the standard of excellence (measured delegation, role-family templates, portfolio verdicts KEEP/MERGE/SPLIT/RETIRE/RE-CHARTER). Dispatches `agent-checker`/`wording-checker`/`skill-checker` at DEEP depth per member; never fixes.
> "review all my agents" · "are my agent names consistent" · "review this agent against the standard of excellence"

**`check-all-skills`** — the skill-corpus counterpart: a CORPUS pass (naming grammar, linguistic potency, front-matter routing, peer composition) or a DEEP-review CAMPAIGN against its own standard of excellence. Dispatches `skill-checker` at DEEP depth per member; never fixes.
> "audit the skill corpus" · "do my skills actually compose" · "run a deep-review campaign batch"

**`make-script`** — mechanize a hand-run check, eyeballed gate, or prose checklist as a bundled `scripts/taskname.py|mjs` with a selftest that proves it: qualify (arithmetic or judgment?) → plan (name, language, home, selftest shape) → confirm → author to `script-writing-rules` → validate (negative control bites, caller wired, the gate's G4 sweeps it). Also retrofits an existing script shipping without a selftest.
> "turn this checklist into a script" · "mechanize this check — we keep eyeballing it every release" · "add a selftest to this script" · `/make-script "the contrast check we run by hand"`

---

## Knowledge (loads itself when your question matches; never a command)

Ask naturally — these are the standards the workflows above enforce, available as direct answers:

- **`skill-writing-rules`** — "why does my skill never trigger?" · "what belongs in the description vs the body?" · "how do the two invocation flags interact?"
- **`agent-writing-rules`** — "why is my agent fat and drifting?" · "how does the skills: preload work?" · "agent or context: fork?"
- **`hook-writing-rules`** — "hook or skill for this rule?" · "why does my hook fire twice / never?" · "how do exit codes work?"
- **`script-writing-rules`** — "what does a selftest need?" · "skill scripts/ or plugin scripts/?" · "python or js for this check?" · "is this even mechanizable, or judgment?" — the deterministic tier's canon; the audits' A4 dimension scores against it.
- **`entry-file-rules`** — "what belongs in CLAUDE.md?" · "why is an instruction that's right there being ignored?"
- **`plugin-writing-rules`** — "why does my plugin fail to load?" · "my users aren't getting the update I shipped" (the version-cache-key trap) · "where does plugin state live?"
- **`pack-writing-rules`** — "how do I structure a reference corpus / INDEX?" · "how many axes should a pack have?" · "how do I ground claims?" · "how do research waves work?"
- **`thinking-depth-rules`** — "what order of reasoning does this need?" · "this feels like tidying, push further" · "should we question the rules themselves?" — the escalation ladder with the rent rule; invoked by plan-plugin-split's refactor phase.
- **`prompt-wording-rules`** — "the model keeps ignoring this instruction — fix the wording" · "harden this tool description" — the language layer beneath every artifact above.
- **`write-handoff`** — "how do I hand this back" · "report my results" · "is this handoff complete" — the standard block (Status·Summary·Files changed·Tests/checks run·Evidence·Risks·Open questions·Recommended next action) every reviewer agent below returns through.
- **`checking-rules`** — "review this diff for real bugs, not just the happy path" · "before you file this review, steelman what the author would say back" · "did I actually check it runs, or just read the diff" — the conduct layer beneath a review's content: a dismissal costs the same evidence as a confirmation, a "fixed" claim is checked against the artifact not a changelog, and every finding survives a self-directed rebuttal before it ships. Piloted on the five harness reviewer agents below.
- **`big-change-git-rules`** — "why did that merge's branch never actually get deleted?" · "a git command said it worked but nothing changed" · "how do I pull without clobbering a parallel session's work?" · "solo commit or a full campaign?" — five axes, every claim traced to a dated 2026-07-16/17 incident; `gitignore_check.py`/`campaign_close.py`/`sync_main.py` mechanize what it documents.
- **`naming-rules`** — "what should we name this new skill / plugin / agent?" · "is this name too vague?" · "name this so it reads like plain English" — the simple naming paradigm for NEW artifacts: five tests, shapes by kind, the verb registry; shipped estate names stay governed by the `*-authoring-standards` until a rename campaign rules otherwise.
- **`plugin-install-facts`** — "how do I install this plugin?" · "can I install it with npx or npm?" · "install from a local path" · "which install method for a private repo?" · "write the README install section" — verified per-channel install commands (dated 2026-07-25): the marketplace-add→install two-step, every accepted source form, the documented npm/npx absence, dev-checkout loads, CI forms, trust/scope/update lifecycle. Answers only; repo-side wiring is `adopt-plugin`, author-side shipping is `plugin-writing-rules`.
- **`github-facts`** — "does GitHub have native issue types now?" · "sub-issue or task-list checkbox?" · "does Closes #N survive a squash merge?" · "is Projects v2 a real backend or just a view?" — GitHub's own platform facts (not our git mechanics — that's the sibling above), cited and dated 2026-07-17; the synthesis axis names where this workspace's `kind: bug`/`kind: feature` label convention aligns with and diverges from GitHub's native, GA Issue Types, without deciding whether to migrate.

---

## The rest of the machinery

- **Agents `routing-judge` and `fact-finder`** — dispatch-only, declared because their tool allowlists ARE the contract: the judge has no tools (structural blindness for /check-routing), the experiment-runner can't Edit (gather≠distill for /make-pack). All other parallel work self-spawns ad-hoc, per the fork-vs-agent gate.
- **Agent `skill-checker`** — fresh-context reviewer preloading check-skill + the standards; used by `/check-everything`'s fan-out and for generator≠critic scoring of decompose/synthesize manifests. Dispatched by workflows; you rarely call it directly.
- **Agents `agent-checker`, `hook-checker`, `plugin-checker`, `wording-checker`** — the same fresh-context pattern as `skill-checker`, one per remaining artifact type: each preloads its matching `*-authoring-standards` (or `prompt-wording-rules`) plus `write-handoff` and `checking-rules`, gates on `skill_lint.py`'s or `release_gate.py`'s real rule codes, and returns a severity-ordered gap-map. Dispatch after authoring or editing the matching artifact type; you rarely call them directly.
- **Agents `issue-sorter`, `repo-cleaner`, and `decision-watcher`** — the estate's standing operational seats, a different character from the review agents above: fired on a schedule (CronCreate) or dispatched on demand, not dispatched by a review workflow. `issue-sorter` implements the watch/triage/trust SPEC to intake and route work items, gated by a durable friendlies allow-list; `repo-cleaner` inventories and cleans repo hygiene, executing ONLY through this plugin's own gated scripts; `decision-watcher` periodically diffs the ADR corpus by checkpoint, judges each changed Decision against `save-lessons`'s bar, and queues candidates for one batched confirm — never authoring, only naming the `/make-pack`/`/make-skill` command a human runs next. None of the three ever edits source or merges/deletes/authors a knowledge-pack file outside its own narrow, script-backed allowance.
- **Command `/sort-issues`** — a thin dispatcher for the agent above, run on demand. On a repo's very first invocation it states the agent's own operating contract as a fixed banner (capture/classify/dedupe/route only, never executes — structural, not configurable) before dispatching, so the boundary is disclosed up front instead of left for a human to go find in the agent's own file. Never re-shows the banner once the repo's friendlies allow-list exists.
- **Agents `chore-lead` and `chore-planner`** — the family's coordination pair. `chore-lead` runs one bounded sweep: fans out the three standing seats above in parallel (or a scoped subset), then hands their reports to `chore-planner`, which turns them into ONE prioritized action queue at `.claude/ops/plan.md` — every entry naming its action, owner, evidence, and size. The orchestrator never authors a queue and never mutates anything; the planner executes nothing it queues and writes exactly that one plan file. `chore-planner` also runs standalone, planning from durable `.claude/ops` state plus live `gh` evidence when no fresh sweep exists.
- **Commands `/sweep-chores [scope]` and `/plan-chores [focus]`** — thin dispatchers for the pair above, run on demand. Each states its seat's operating contract as a fixed banner before the repo's first ops queue exists (checked before the dispatch — the dispatch itself is what creates `plan.md`), then relays the seat's own report unmodified. `/sweep-chores "repo hygiene only"` scopes the fan-out; `/plan-chores "branches and PRs first"` shifts emphasis without changing the entry contract.
- **Hook (PostToolUse on Write|Edit)** — lints every skill, agent, hooks.json, plugin.json, and eval suite the moment it's written. Silent when clean; blocking with a repair message when not.
- **Scripts** (`scripts/`, all with `selftest` modes): `skill_lint.py` (F/W/A/H/C/P/E/K rules), `release_gate.py` (G1–G11: manifest, structure, lint, bundled selftests, phantom sweep, package, evals, docs, packs, sibling names, ruff/eslint style lint), `eval_check.py` (suite schema + coverage), `corpus_check.py` (pack INDEX reconciliation), `docs_check.py` (README/MANUAL freshness, gate G10). Per-skill: `manifest_check.py`, `consolidation_check.py`.
- **Eval suites** (`skills/*/evals/evals.json`) — trigger-routing regression tests for every model-invocable skill; the example prompts in this manual are drawn from them. Execute via `/check-routing`.

## Three habits that keep it healthy

1. After editing any model-invocable description, update its eval suite and run `/check-routing`. Don't
   rely on remembering — `/schedule nightly: if any skill description changed today, run /check-routing
   on its plugin` catches the ones you forget; match the interval to how often descriptions
   actually change, not tighter.
2. Ship only through `/ship-plugin` — a same-version re-ship is silently skipped by updates.
3. Run `/check-everything` on a cadence, not "when I remember": `/schedule weekly: run /check-everything .
   and report the triage table` — weekly matches how fast this surface actually drifts; route every
   recurring finding into a hook or lint rule instead of fixing it twice.
