# intent — check-state
status: forging
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: low (collectors) / medium (cross-reference pass)
type: capability-uplift

## trigger
should:      ["what's the state of the project", "where are we", "what's blocked on me",
              "give me a project state report", "/check-state", "what can be merged or deleted",
              "review all roadmap, plan, and backlog items and open tickets"]
should_not:  ["what should I work on next / prioritize the backlog (chore-planner seat)",
              "clean up these stale branches (repo-cleaner executes)",
              "is the plugin estate healthy (/check-everything)",
              "file this as a task (file-task)"]

## delta
Proven live 2026-07-29 (evals/baseline/): the no-skill baseline reported "12 merged remote
branches waiting on cleanup" by reading stale local `origin/*` tracking refs; origin actually
held 2 heads — every one of those branches was already deleted. The with-skill run (ls-remote
via ticket_state.py) reported zero survivors, correctly. Ad-hoc git evidence hallucinates
state; the collectors don't.

Without the skill, Claude answers state questions by ad-hoc `git branch` / `gh issue list`
dumps: unordered raw counts, no cross-referencing between the doc layer (ROADMAP/PLAN/TICKET
ID spine) and the git/ticket layers, no knowledge of sync_main quarantine stashes or the
merged-PR-surviving-branch failure class, no delta since last look, and blocked-on-user items
buried mid-list instead of leading. Desired: verdict-first 🟢🟡🔴 report ordered
Blocked-on-you → Ready-to-close → Drift → Delta → raw counts, every 🟡/🔴 naming its owning
command, mutating nothing.

## fences
- NOT for producing the prioritized action queue (chore-planner / plan-chores)
- NOT for executing any cleanup — branch deletes, stash pops, closes (repo-cleaner, campaign_close.py)
- NOT for plugin health — lint, gates, routing (/check-everything)
- NOT for filing or triaging work items (issue-sorter / file-bug / file-feature / file-task)

## assertions
1. The report's first section is Blocked-on-you; if empty it says so explicitly ("nothing blocked on you").
2. Every 🟡/🔴 line names the owning command or seat that would act on it (e.g. campaign_close.py, repo-cleaner, /file-task); the run itself performs zero mutations (no git/gh write commands issued).
3. The report contains a Drift section cross-referencing layers (plan↔ticket↔branch orphans), not just per-source lists.
4. A repeat run contains a Delta section computed from the checkpoint snapshot at .claude/ops/state-checkpoint.json (section 4 of the contract's fixed order).
5. Each collector script exits 0/1/2 (ok/fail/skip) and passes its own `selftest` mode.

## gates
P0 route:      PASS 2026-07-29 — knowledge+procedure on demand; not a hook (cross-reference pass is judgment), not entry-file (on-demand, not every-turn), not an agent (no tool walls; read-only lives in procedure+scripts)
P1 intent:     PASS 2026-07-29 — species=procedural chosen by user (AskUserQuestion); all slots filled from the agreed design
P2 evals:      PASS 2026-07-29 — evals.json 10t/10n; 5 assertions; 2 baseline outputs in evals/baseline/
P3 draft:      PASS 2026-07-29 — SKILL.md (procedural skeleton) + 4 scripts, selftests green; two smoke-test noise bugs (worktree branch as delete candidate, absent-dist false drift) fixed same-day with reverse controls
P4 language:   PASS 2026-07-29 — potency_lint within budget (0 hedges, 3 NEVER, 0 vague); load-bearing lines instantiate
P5 validate:   PASS 2026-07-29 — skill_lint clean (after W8 description diet); fresh-context FLOOR audit (evals/audit-report.md): 1 blocking + 5 minor + 6 notes, ALL fixed same-day with incident fixtures (B1 unmeasured-slot sentinel in state_diff; M1 arg parse; M2 measured ownership via author/reviewRequests/viewer; M3 letter-bounded doc matcher + templates/adr exclusions; M4 corrupt/unwritable checkpoint; M5 assertion reword; N1–N6 wording/docstring/timeout/auth-probe/glob); behavior check: with-skill fresh session produced the exact contract (evals/baseline/with-skill-state-question.md) and exposed the no-skill baseline's stale-tracking-ref hallucination; fences unreciprocated by mechanism (see rulings)

## rulings
- 2026-07-29 fence closure: all three NOT-clause owners lack trigger suites by mechanism — chore-planner and repo-cleaner are agents, /check-everything is command species (description never reaches the model). Fences stand unreciprocated by mechanism, not oversight (the v1.34.3 ops-issues precedent).
- 2026-07-29 baseline note: in THIS workspace the no-skill baseline already produces a decent report (CLAUDE.md + .claude/ops context carry it); the skill's delta is deterministic evidence (collectors + selftests), the checkpoint delta, the doc-layer parse, and portability to repos without this workspace's standing context.
- 2026-07-29: user ruled this is a harness skill (vs. a report mode on chore-planner); harness owns cross-plugin repo/ops tooling.
- 2026-07-29: user chose procedural over command (recommended option) — state-shaped questions should auto-trigger it.
- Deliverable gap: none — no references/ corpus needed; the knowledge is in the three collectors + the body's cross-reference procedure.
