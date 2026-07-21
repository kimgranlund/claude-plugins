# Audit report — ops-orchestrator (command skill, FLOOR)

Skill: `forge 1.14.0/skills/ops-orchestrator` · Standards: skill-authoring-standards · Lint: 0 fail / 1 warn (W4)
Verdict: **PASS** (re-audit 2026-07-20; round 1 verdict FAIL, all findings resolved)

Lint verdict line (rerun on the revised file):

```
skill-postwrite-invocation-lint · 0 fail / 1 warn · /Users/kimba/Projects/nonoun/plugins/forge 1.14.0/skills/ops-orchestrator/SKILL.md
  L2    WARN W4  agentive head 'orchestrator' on a skill -> agents take -er/-or; a skill takes the verb or knowledge-noun form
```

W4 is the deliberate skill↔agent same-name pairing (normative precedent:
`skills/ops-issues/SKILL.md`); the body cites the ruling's home rather than restating it
(SKILL.md:17-20) — adequate, and the round-1 drift-pair nit is gone.

## Criteria (round 2)

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | pass | — | Sampled: pre-dispatch rationale ("a post-dispatch check destroys its own condition", SKILL.md:26-27), never-fabricate branch (SKILL.md:49-50), inline banner re-read ("never costs a three-seat sweep", SKILL.md:55-56) — each survives the deletion test | — |
| R2 trigger fidelity | n/a | — | `disable-model-invocation: true` (SKILL.md:9); description judged as slash-menu documentation — states action, target, banner behavior, argument shape (SKILL.md:3-8). Fit | — |
| R3 species/dial agreement | pass (ruled) | — | Command species, both dials explicit (SKILL.md:9-10), `allowed-tools` scoped to the three verbs used (SKILL.md:12); W4 covered by the cited pairing ruling (SKILL.md:17-20) | — |
| R4 register | pass | — | Spec-present throughout; single uppercase gate (`NOT done`, SKILL.md:59-61); locks lowercase | — |
| R5 no restatement | pass | — | Pairing mechanics now cited to `/ops-issues`'s body, not restated (SKILL.md:18-20); banner text is owned disclosure content | — |
| R6 position | pass | — | 61 lines; procedure, banner, branches, stopping predicate all in the head | — |
| R7 contracts | pass | — | Relay contract (SKILL.md:33-34), three named failure branches (SKILL.md:49-56), stopping predicate pinning pre-dispatch banner timing with a NOT-done clause for the post-dispatch ordering (SKILL.md:58-61) | — |
| R8 quantities | pass | — | Banner text fixed verbatim (SKILL.md:38-45) | — |

## Fix verification (round 1 → round 2)

- **F1 (blocking, banner ordering) — RESOLVED.** Step 1 is now "Banner check, before anything"
  (SKILL.md:24-27) with the causal rationale stated in place — "the sweep itself is what creates
  that file, so a post-dispatch check destroys its own condition" — dispatch moved to step 2, and
  the stopping predicate both requires "the banner was shown before the dispatch" and names the
  post-dispatch check as NOT done (SKILL.md:58-61). The failure mode is now grammatically hard to
  reach.
- **F2 (major, no-classify contradiction) — RESOLVED.** The commitment is scoped to seat-name
  judgment ("Which seats a scope instruction names is the agent's judgment, never validated
  here") and failure branch 2's redirect is explicitly named as "the one screening judgment this
  command owns" (SKILL.md:30-32). The two instructions now compose instead of colliding.
- **F3 (minor, repeat-disclosure) — RESOLVED.** New branch answers a banner re-read inline
  without dispatching (SKILL.md:55-56), matching the precedent (ops-issues/SKILL.md:69-72).
- **R5 nit (drift pair) — RESOLVED.** The mechanics are cited to `/ops-issues`'s body with a
  parenthetical gloss (model-routing exclusion; disjoint tool namespaces), not restated
  (SKILL.md:17-20). One canonical home remains.
- **Banner gloss reword — sound.** "No ops queue has ever been produced here" (SKILL.md:24-25)
  makes the condition and its meaning coincide, including when a standalone `/ops-planner` run
  creates `plan.md` first — the plan file is the ops family's shared once-ever disclosure marker,
  and whichever door first produces the queue carries the disclosure. Coherent as a deliberate
  cross-skill semantics shared with `skills/ops-planner`.

## Remaining nit (non-blocking)

The description still reads "States the agent's operating contract as a fixed banner before the
first-ever completed sweep" (SKILL.md:6-7). Under the shared-marker semantics that is now two
shades off: (a) if a standalone `/ops-planner` run produced `plan.md` first, no banner precedes
this command's first sweep; (b) after a planner-failed sweep (no queue written) the banner
correctly re-shows on run two. Since this description is menu documentation only (never model
context), it's a nit — "before the first ops queue exists here" would say it exactly. Fix at the
next description-tier edit; not worth a round on its own.

## Verdict history

- 2026-07-20 round 1: FAIL — F1 blocking (banner check ordered after the dispatch that creates
  its own condition), F2 major (no-classify commitment vs failure-branch-2 redirect), F3 minor
  (no repeat-disclosure branch), R5 nit (pairing-mechanics drift pair).
- 2026-07-20 round 2: PASS — all four resolved as verified above; one description-wording nit
  carried, non-blocking.

---

## agent-forge gate record — the ops-orchestrator pairing (2026-07-20)

- **A0 route:** agent-only properties named — parallel fan-out (Task), tool wall as guarantee
  (Read+Task, no Write: coordination-only enforced structurally), distinct config (sonnet+high,
  the coordination ladder row). PASS
- **A1 interview:** decisions on record — planner-as-roll-up sweep shape; ladder defaults;
  command-only deployment (no cron arming this campaign). Preload (`handoff-compose`) verified
  preloadable. PASS
- **A2 draft:** thin shell; knowledge via preload, contract in body. PASS
- **A3 language + fresh-context review:** agent-reviewer FLOOR — PASS-with-fixes, all five
  findings closed and confirmed by the reviewer; this skill's own audit — FAIL → PASS on
  re-audit (blocking banner-ordering finding: the check ran after the dispatch that creates its
  own condition; moved pre-dispatch, predicate pinned). PASS
- **A4 validate:** skill_lint clean (agent) / 0 fail + 1 ruled W4 (this skill). Smoke test,
  scoped sweep "repo hygiene only": scope narrowed to exactly ops-repo; sibling-seat dispatch
  (`forge:ops-repo`) mechanically proven from a subagent context (settles the Task-resolution
  question, consistent with the orchestration-coordinator precedent); planner-failure branch
  relayed raw handoffs and named the missing queue without improvising one. PASS
