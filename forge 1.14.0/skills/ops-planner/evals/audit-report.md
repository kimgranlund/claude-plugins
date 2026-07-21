# FLOOR audit — ops-planner command skill

Skill: forge 1.14.0/skills/ops-planner/SKILL.md · Standards: skill-authoring-standards · Lint: clean — `skill-postwrite-invocation-lint · 0 fail / 1 warn` (W4 agentive head `planner`; ruled, see R3)
Verdict: **PASS** (no blocking findings; 1 major, 1 minor, 2 nits)

Audited: 2026-07-20 · Auditor: aud-skill-plan (fresh context) · Depth: FLOOR
Inputs read: the target SKILL.md; `agents/ops-planner.md` (the dispatched seat); `skills/ops-issues/SKILL.md` (normative pairing precedent); `skills/ops-orchestrator/SKILL.md` (same-change sibling).

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | PASS | — | Banner one-shot condition (SKILL.md:29-30), no-pre-validation clause (SKILL.md:26-28), sweep-redirect branch (SKILL.md:48-50) all fail the deletion test in the right direction — removing any one changes behavior (banner repeats or never shows; host starts classifying args; fan-out gets chained from the wrong home) | — |
| R2 trigger fidelity | N/A | — | `disable-model-invocation: true` (SKILL.md:9) — description never reaches the router. Judged instead as slash-menu documentation per the command-species rule: it states what the dispatch does, the write surface, the banner, and the arg shape (SKILL.md:3-8). Meets that bar | — |
| R3 species/dial agreement | PASS | nit | Command species: dispatch side effect, human-timed, both dials explicit (SKILL.md:9-10), `allowed-tools` exactly the three verbs the workflow needs (SKILL.md:12 — Read/Glob for the plan-file check, Agent for the dispatch; correctly omits ops-issues' AskUserQuestion since no interview exists here). W4 name-head deviation (agentive `planner` on a skill) is the deliberate skill↔agent same-name pairing; the body records the ruling adequately by reference — names the pairing, cites `/ops-issues` as where it was ruled, notes `/ops-orchestrator` shares it, restates both load-bearing mechanics (SKILL.md:17-20). Nit: "the two tool namespaces never compete" (SKILL.md:20) compresses the sibling's more precise "the Agent tool's `subagent_type` namespace is disjoint from the Skill tool's" (ops-orchestrator/SKILL.md:20-21) — resolvable from context, and the /ops-issues pointer carries the full text | Optional: name the two namespaces as the siblings do |
| R4 register | PASS | — | Load-bearing lines commit rather than describe ("Return the agent's own final report unmodified" SKILL.md:31; "never fabricate a plan or a report" SKILL.md:47). Zero uppercase hard gates spent; lowercase nevers used as locks. Internal tension between step 1 and branch 2 filed under the minor below | — |
| R5 no restatement | FAIL | **major** | **Phantom citation / substrate in the wrong home.** Step 1 defines a focus instruction "(an emphasis, never a new entry contract) exactly as the agent's own description describes" (SKILL.md:26-28), and the description + argument-hint advertise the mode (SKILL.md:7-8, 11). But `agents/ops-planner.md` never mentions a focus instruction anywhere — its description names exactly two input modes, sweep reports vs standalone (agents/ops-planner.md:6-8), and its body's input-precedence and failure branches (agents/ops-planner.md:45-47, 54-61) carry no contract for a focus arg. The citation is false as written, and the guardrail ("never a new entry contract") lives only in this command body, which the dispatched agent never loads — so the semantics bind nothing. Damage is bounded: the agent's own Done gate pins the entry contract regardless (agents/ops-planner.md:63-66), so a focus arg can't corrupt the plan shape; the agent will improvise the emphasis. Still a false citation that rots and an advertised mode the executor never heard of | Agent-side (correct home): add one clause to `agents/ops-planner.md` defining standalone focus-emphasis semantics; the skill's pointer then becomes true. Skill-side fallback: reword step 1 to own the definition and drop "exactly as the agent's own description describes". Coordinate with rev-agent-plan's audit of the agent file |
| — internal consistency | — | minor | Step 1's prohibition is unscoped: "This command never pre-validates the instruction" (SKILL.md:27-28), yet failure branch 2 inspects `$ARGUMENTS` and refuses to dispatch on a sweep-shaped ask (SKILL.md:48-50). Both siblings scope the prohibition so their redirect branch stays legal — ops-issues: "never classifies or pre-validates *an agent-owned instruction shape*" (ops-issues/SKILL.md:35-37); ops-orchestrator: "never classifies or pre-validates *a scope instruction*" (ops-orchestrator/SKILL.md:28-29). Read literally, ops-planner's branch 2 violates its own step 1 | Adopt the sibling qualifier: "never pre-validates an agent-owned instruction shape" |
| R6 position | PASS | — | 55-line body, ~2.8 KB — entire skill inside the first 5,000 tokens; contract, banner, failure branches, stopping predicate all in the head; no references/ needed at this size | — |
| R7 contracts | PASS | — | Output contract: relay the agent's report unmodified (SKILL.md:31-32). Two named failure branches: dispatch tool failure → report plainly, never fabricate (SKILL.md:46-47); sweep-shaped ask → name `/ops-orchestrator`, do not dispatch, with the rationale that chaining would duplicate the orchestrator's contract in a second home (SKILL.md:48-50) — the exact redirect the sibling runs in mirror image. Stopping predicate checkable, with a NOT-done clause pinning the two failure-mode confusions (SKILL.md:52-55). The no-ops-state-at-all case is correctly NOT duplicated here — the agent owns it (agents/ops-planner.md:58-59) | — |
| R8 quantities | PASS | nit | Step 3's "verdict line plus its top entries" (SKILL.md:31) drops the agent's numeric anchor "the top three entries" (agents/ops-planner.md:64-65). Harmless — the relay is "unmodified", so the agent's contract governs — but the gloss inherits the verbose prior | Say "top three entries" |

## Banner logic (dispatch-specific check)

Correct. The condition is pure file existence — `.claude/ops/plan.md` absent → show; present → never again (SKILL.md:29-30) — and the stopping predicate hard-forbids checking anything else (SKILL.md:54-55). The gloss "this seat has never written a plan here" is *accurate* for this command, because only the ops-planner seat writes plan.md on any dispatch path (orchestrator-driven or standalone). Note the banner legitimately repeats on consecutive runs while the agent's "no ops state at all" branch keeps declining to write a plan — consistent with the stated contract ("Once it exists, never show it again"), not a defect. The banner restating the agent's contract is the ruled disclosure shape from /ops-issues, accepted drift pair.

## Cross-boundary observation (sibling-owned, not scored here)

`/ops-orchestrator` keys its banner on the same file with the gloss "no sweep has ever completed against this repo" (ops-orchestrator/SKILL.md:30-32) — a standalone `/ops-planner` first run creates plan.md without any sweep completing, making that gloss inaccurate and suppressing the orchestrator's first-run banner. ops-planner's own gloss survives this interaction; the orchestrator's doesn't. Flagged for aud-skill-orch.

## Top 3

1. **major** — Step 1 cites the agent's description for focus-instruction semantics the agent file never defines (SKILL.md:26-28 vs agents/ops-planner.md:6-8); the "(an emphasis, never a new entry contract)" guardrail lives only where the agent can't see it. Fix belongs agent-side.
2. **minor** — Unscoped "never pre-validates the instruction" (SKILL.md:27-28) contradicts the sweep-redirect branch (SKILL.md:48-50); both siblings scope the prohibition and this file should adopt their qualifier.
3. **nit** — "top entries" (SKILL.md:31) vs the agent's "top three entries"; and the namespace-ruling compression at SKILL.md:20 could name the two namespaces as ops-orchestrator does.

---

## agent-forge gate record — the ops-planner pairing (2026-07-20)

- **A0 route:** agent-only properties named — tool restriction as guarantee (single-write
  discipline on `.claude/ops/plan.md`), multi-skill preload, distinct config (fable+high, the
  planning/judgment ladder row — a queue verdict never rides the caller's tier). PASS
- **A1 interview:** decisions on record — planner is the sweep's roll-up seat; standalone input
  = durable `.claude/ops` state + live `gh`; focus instruction = emphasis only, never a new
  entry contract. Both preloads verified preloadable. PASS
- **A2 draft:** queue-order rubric ruled earned contract by the fresh-context reviewer (no
  owning skill exists to drift-pair against; two spawners make the body the single home). PASS
- **A3 language + fresh-context review:** agent-reviewer FLOOR — PASS-with-fixes, all applied
  (carry-forward made mode-independent; preload over-claim on worktrees/branches corrected;
  terminal failure states added to the Done predicate); this skill's own audit — PASS (focus
  contract defined agent-side, closing the phantom citation). PASS
- **A4 validate:** skill_lint clean (agent) / 0 fail + 1 ruled W4 (this skill). Smoke happy
  path: `.claude/ops/plan.md` written, 7 entries all carrying action·owner·evidence·size,
  verdict-first return. Smoke failure branch: sweep dispatch naming nonexistent reports →
  missing input named, stopped, no standalone fallback, no write. PASS
