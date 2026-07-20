# forge — user manual

The plugin-authoring plugin: skills, agents, hooks, entry files, eval suites, and plugin releases, each with a standard that teaches it, a workflow that builds it, and a check that enforces it. This file is documentation for humans — the harness never loads it. The engineering ledger (versions, incidents, sharp edges) lives in `README.md`.

Install, then `/reload-plugins`. Everything below is invoked as `/forge:<name>` when unqualified names collide.

---

## Slash commands (you invoke these; the model never fires them on its own)

**`/plugin-forge [domain or charter]`** — forge a whole plugin from a domain: charter interview, family design (question types, projected routing prompts, vocabulary separability, rejected-members ledger), scaffold, a /skill-forge pass per member, fence-graph closure, /eval-run proof, release.
> `/plugin-forge "a plugin with all the skills related to UI design"` · `/plugin-forge api-review`

**`/skill-forge [name or one-line intent]`** — forge a new skill end-to-end through six gated phases: route check, intent interview (the grilling), evals-first, species-template draft, language pass, validation.
> `/skill-forge migration-runbook` · `/skill-forge "a skill that reviews SQL migrations before they ship"`

**`/agent-forge [name or job]`** — forge a subagent through five gated phases, starting with the fork-vs-agent route check (many "agents" should just be `context: fork`).
> `/agent-forge changelog-writer` · `/agent-forge "something that reviews PRs against our style guide"`

**`/hook-forge [name or the rule to enforce]`** — forge a hook: check-vs-judgment gate, event/matcher interview, script + registration, simulated-event validation with a shipped selftest.
> `/hook-forge "block commits that touch dist/"` · `/hook-forge post-edit-prettier`

**`/entry-file-audit [path]`** — classify every CLAUDE.md line against the residency test and migrate evictions down-stack (checks→hooks, procedures→skills, subtree truths→rules). Edits only on approval.
> `/entry-file-audit` · `/entry-file-audit packages/api/CLAUDE.md`

**`/harness-audit [root]`** — the recurring outer loop: lint sweep, standards-preloading fresh-context reviews of every artifact, triage table routing each finding to a fix, a decision, or permanent infrastructure.
> `/harness-audit` · `/harness-audit ~/projects/monorepo`

**`/repo-alignment [repo path] [--phases 0-6 | audit-only]`** — the committing campaign for a drifted repo (where `/harness-audit` only reports): phased inventory → unify duplicates → orphan manifest → schema + standing guards → audit verdicts → work-package execution → lessons distillation; human-checkpointed at every destructive step.
> `/repo-alignment .` · `/repo-alignment ~/projects/app audit-only`

**`/eval-run [plugin-root]`** — run the trigger-eval suites as a blind routing simulation: judges pick a skill from the description menu alone; you get a routing matrix and per-failure tuning targets (stolen / leaked / dead).
> `/eval-run .` — worth running after any description edit

**`/skill-refactor [manifest.json]`** — execute a validated skill-decompose or skill-synthesize manifest: plan shown for approval, files moved, old surfaces retired to an attic (never deleted), referrers rewritten, sweep proven (zero live references to retired handles).
> `/skill-refactor split-manifest.json` — always after the decision skill's checker runs clean

**`/pack-forge [skill-dir | new pack: domain]`** — mint or grow a knowledge pack's reference corpus through question-led research waves: ratified question set, dated gathering, ask-shaped distillation with confidence markers, INDEX/evals registration, corpus_check validation. One axis per wave.
> `/pack-forge skills/ui-patterns` · `/pack-forge "new pack: design tokens"`

**`/plugin-release [plugin-root]`** — release through the full gate: version bump on approval, `release_gate.py` (structure, manifest, full lint, bundled selftests, phantom sweep, eval validation), package to `dist/`.
> `/plugin-release` · run `python3 scripts/release_gate.py . ` alone for a dry gate

---

## Procedures (ask in plain language, or invoke explicitly)

**`skill-decompose`** — should a sprawling knowledge corpus split into a family, and into which packs? Four evidence tests; an honest no-split is a first-class verdict. Produces a reconciled manifest + referrer repair map, validated by `manifest_check.py`.
> "this skill has gotten enormous, break it up" · "is one entry surface enough for all these reference files" · `/skill-decompose skills/color-science`

**`skill-synthesize`** — the formal inverse: should several thin/overlapping skills merge into one pack? Inverse test battery plus the self-check (a merge must survive skill-decompose's own tests or it's a relabeled monolith). Validated by `consolidation_check.py`.
> "these three skills all overlap, should they be one" · "we're loading five packs for basically one question, merge them"

**`plugin-decompose`** — analyze an existing surface (skills + agents + hooks + scripts; frontmatter and structure suffice) and decide its partition into 1–5 portable plugins: dependency graph via surface_map.py, four distribution-layer tests, rejected-alternatives ledger, mechanically validated manifest handed to /plugin-forge. Direction-agnostic — merging scattered plugins is the same partition with fewer groups. Also runs negative-space analysis: dangling handoffs and the family matrix surface what might be missing, under the anti-matrix guard (absence + job evidence = gap; absence alone = correctly absent).
> "which plugins should these skills become" · "should this mega-plugin be several smaller ones" · `/plugin-decompose ~/.claude`

**`plugin-onboard`** — declare an external plugin or marketplace repo in a project's `.claude/settings.json` so every contributor who trusts the repo is prompted to install it: classifies each URL (marketplace repo → `extraKnownMarketplaces` entry; bare plugin repo → a self-hosted `marketplace.json` wrapper first), then verifies via `/plugin`. Project-scoped and portable — never an operator-local install masquerading as project config.
> "add this plugin repo so contributors can install it" · "declare a marketplace in settings.json" · `/plugin-onboard <url>`

**`skill-review`** — audit an existing SKILL.md against the standards; verdict-first findings report. The mechanical half runs first via `skill_lint.py`.
> "review this skill" · "this skill misfires constantly — what's wrong with it"

**`intent-extract`** — separate the literal ask from the root goal before acting: surface ambiguities and conflicting signals, resolve them with low-effort multiple-choice questions, restate the task sharper.
> "figure out what this ticket is actually asking for" · "improve this prompt brief" · `/intent-extract`

**`open-questions-sweep`** — clears a session's backlog of unresolved items (an unanswered question, an unconfirmed assumption, a stray idea left undecided) into one batched AskUserQuestion round, instead of a prose dump nobody actually resolves. Fires on its own at a session's natural closing point; also invocable directly.
> "before we wrap up, is there anything still open" · "any decisions still open before we close this out" · `/open-questions-sweep`

**`system-decompose`** — break any system down along two crossing planes (whole→parts × actions→surfaces) and verify they cover each other. For architectures, UX, goals — not for knowledge-pack split decisions (that's skill-decompose).
> "decompose this feature into parts" · "my acceptance criteria don't map to any task"

**`knowledge-harvest`** — detects when a fact crosses the bar for durable project knowledge (a correction restated a third time, a ratified ADR/ticket/SPEC decision never captured, a high-impact convention worth keeping on first mention) and turns it into a knowledge-pack entry — always via an AskUserQuestion confirmation carrying the concrete plan before writing, never silently. Also runs a later, separately-invoked staleness pass that re-verifies a landed citation still holds. Orchestrates `pack-forge` (authors), `release_gate.py` (structural gate), and `/eval-run` (routing gate) rather than reimplementing them.
> "this is the third time I've explained this" · "is this actually project knowledge or just noise" · "check if our harvested knowledge is still accurate"

**`agents-audit`** — audit a whole `agents/` team as one system, two modes: a CORPUS pass (naming coherence, linguistic potency, front-matter as an interface, skill-leverage graph — one sweep) or a DEEP-review CAMPAIGN against the standard of excellence (measured delegation, role-family templates, portfolio verdicts KEEP/MERGE/SPLIT/RETIRE/RE-CHARTER). Dispatches `agent-reviewer`/`linguistics-reviewer`/`skill-auditor` at DEEP depth per member; never fixes.
> "review all my agents" · "are my agent names consistent" · "review this agent against the standard of excellence"

**`skills-audit`** — the skill-corpus counterpart: a CORPUS pass (naming grammar, linguistic potency, front-matter routing, peer composition) or a DEEP-review CAMPAIGN against its own standard of excellence. Dispatches `skill-auditor` at DEEP depth per member; never fixes.
> "audit the skill corpus" · "do my skills actually compose" · "run a deep-review campaign batch"

**`script-forge`** — mechanize a hand-run check, eyeballed gate, or prose checklist as a bundled `scripts/taskname.py|mjs` with a selftest that proves it: qualify (arithmetic or judgment?) → plan (name, language, home, selftest shape) → confirm → author to `script-authoring-standards` → validate (negative control bites, caller wired, the gate's G4 sweeps it). Also retrofits an existing script shipping without a selftest.
> "turn this checklist into a script" · "mechanize this check — we keep eyeballing it every release" · "add a selftest to this script" · `/script-forge "the contrast check we run by hand"`

---

## Knowledge (loads itself when your question matches; never a command)

Ask naturally — these are the standards the workflows above enforce, available as direct answers:

- **`skill-authoring-standards`** — "why does my skill never trigger?" · "what belongs in the description vs the body?" · "how do the two invocation flags interact?"
- **`agent-authoring-standards`** — "why is my agent fat and drifting?" · "how does the skills: preload work?" · "agent or context: fork?"
- **`hook-authoring-standards`** — "hook or skill for this rule?" · "why does my hook fire twice / never?" · "how do exit codes work?"
- **`script-authoring-standards`** — "what does a selftest need?" · "skill scripts/ or plugin scripts/?" · "python or js for this check?" · "is this even mechanizable, or judgment?" — the deterministic tier's canon; the audits' A4 dimension scores against it.
- **`entry-file-standards`** — "what belongs in CLAUDE.md?" · "why is an instruction that's right there being ignored?"
- **`plugin-authoring-standards`** — "why does my plugin fail to load?" · "my users aren't getting the update I shipped" (the version-cache-key trap) · "where does plugin state live?"
- **`pack-authoring-standards`** — "how do I structure a reference corpus / INDEX?" · "how many axes should a pack have?" · "how do I ground claims?" · "how do research waves work?"
- **`reasoning-orders`** — "what order of reasoning does this need?" · "this feels like tidying, push further" · "should we question the rules themselves?" — the escalation ladder with the rent rule; invoked by plugin-decompose's refactor phase.
- **`linguistic-techniques`** — "the model keeps ignoring this instruction — fix the wording" · "harden this tool description" — the language layer beneath every artifact above.
- **`handoff-compose`** — "how do I hand this back" · "report my results" · "is this handoff complete" — the standard block (Status·Summary·Files changed·Tests/checks run·Evidence·Risks·Open questions·Recommended next action) every reviewer agent below returns through.
- **`reviewer-discipline`** — "review this diff for real bugs, not just the happy path" · "before you file this review, steelman what the author would say back" · "did I actually check it runs, or just read the diff" — the conduct layer beneath a review's content: a dismissal costs the same evidence as a confirmation, a "fixed" claim is checked against the artifact not a changelog, and every finding survives a self-directed rebuttal before it ships. Piloted on the five forge reviewer agents below.
- **`git-campaign-workflows`** — "why did that merge's branch never actually get deleted?" · "a git command said it worked but nothing changed" · "how do I pull without clobbering a parallel session's work?" · "solo commit or a full campaign?" — five axes, every claim traced to a dated 2026-07-16/17 incident; `gitignore_check.py`/`campaign_close.py`/`sync_main.py` mechanize what it documents.
- **`github-issue-pr-primitives`** — "does GitHub have native issue types now?" · "sub-issue or task-list checkbox?" · "does Closes #N survive a squash merge?" · "is Projects v2 a real backend or just a view?" — GitHub's own platform facts (not our git mechanics — that's the sibling above), cited and dated 2026-07-17; the synthesis axis names where this workspace's `kind: bug`/`kind: feature` label convention aligns with and diverges from GitHub's native, GA Issue Types, without deciding whether to migrate.

---

## The rest of the machinery

- **Agents `eval-judge` and `pack-researcher`** — dispatch-only, declared because their tool allowlists ARE the contract: the judge has no tools (structural blindness for /eval-run), the researcher can't Edit (gather≠distill for /pack-forge). All other parallel work self-spawns ad-hoc, per the fork-vs-agent gate.
- **Agent `skill-auditor`** — fresh-context reviewer preloading skill-review + the standards; used by `/harness-audit`'s fan-out and for generator≠critic scoring of decompose/synthesize manifests. Dispatched by workflows; you rarely call it directly.
- **Agents `agent-reviewer`, `hook-reviewer`, `plugin-reviewer`, `linguistics-reviewer`** — the same fresh-context pattern as `skill-auditor`, one per remaining artifact type: each preloads its matching `*-authoring-standards` (or `linguistic-techniques`) plus `handoff-compose` and `reviewer-discipline`, gates on `skill_lint.py`'s or `release_gate.py`'s real rule codes, and returns a severity-ordered gap-map. Dispatch after authoring or editing the matching artifact type; you rarely call them directly.
- **Agents `ops-issues`, `ops-repo`, and `ops-adr`** — the estate's standing operational seats, a different character from the review agents above: fired on a schedule (CronCreate) or dispatched on demand, not dispatched by a review workflow. `ops-issues` implements the watch/triage/trust SPEC to intake and route work items, gated by a durable friendlies allow-list; `ops-repo` inventories and cleans repo hygiene, executing ONLY through this plugin's own gated scripts; `ops-adr` periodically diffs the ADR corpus by checkpoint, judges each changed Decision against `knowledge-harvest`'s bar, and queues candidates for one batched confirm — never authoring, only naming the `/pack-forge`/`/skill-forge` command a human runs next. None of the three ever edits source or merges/deletes/authors a knowledge-pack file outside its own narrow, script-backed allowance.
- **Hook (PostToolUse on Write|Edit)** — lints every skill, agent, hooks.json, plugin.json, and eval suite the moment it's written. Silent when clean; blocking with a repair message when not.
- **Scripts** (`scripts/`, all with `selftest` modes): `skill_lint.py` (F/W/A/H/C/P/E/K rules), `release_gate.py` (G1–G11: manifest, structure, lint, bundled selftests, phantom sweep, package, evals, docs, packs, sibling names, ruff/eslint style lint), `eval_check.py` (suite schema + coverage), `corpus_check.py` (pack INDEX reconciliation), `docs_check.py` (README/MANUAL freshness, gate G10). Per-skill: `manifest_check.py`, `consolidation_check.py`.
- **Eval suites** (`skills/*/evals/evals.json`) — trigger-routing regression tests for every model-invocable skill; the example prompts in this manual are drawn from them. Execute via `/eval-run`.

## Three habits that keep it healthy

1. After editing any model-invocable description, update its eval suite and run `/eval-run`. Don't
   rely on remembering — `/schedule nightly: if any skill description changed today, run /eval-run
   on its plugin` catches the ones you forget; match the interval to how often descriptions
   actually change, not tighter.
2. Ship only through `/plugin-release` — a same-version re-ship is silently skipped by updates.
3. Run `/harness-audit` on a cadence, not "when I remember": `/schedule weekly: run /harness-audit .
   and report the triage table` — weekly matches how fast this surface actually drifts; route every
   recurring finding into a hook or lint rule instead of fixing it twice.
