---
name: team-or-solo-rules
description: >-
  Design or review orchestration — how skills, subagents, and teams compose, and their
  wiring frontmatter. Use when deciding skill vs subagent vs team, wiring
  capabilities, planning a fan-out worth its token cost, skills: preloads, or auditing
  an agent system's wiring — "should this be a subagent or a team", "how do my skills
  and agents connect". NOT a whole-corpus/team audit — "audit the agent team
  for duplicates", "do my agents leverage the right skills" (check-all-agents /
  check-all-skills);
  NOT a single agent definition (make-agent / agent-writing-rules); NOT next-turn
  timing (loop-rules).
disable-model-invocation: false
user-invocable: false
---

# Harness — Orchestration & Frontmatter Design & Review

Design how capabilities compose, or review an arrangement. The unit is chosen by task shape: skill (procedure), subagent (result-only delegation), team (collaboration).

## Operating model (essentials; depth in `references/foundations.md`)
- Discovery (descriptions select, every turn) vs continuation (`/goal`,`/loop`,hooks decide when the next turn fires) — never conflated.
- Descriptions are the connective tissue: the orchestrator routes on them, not on file cross-references.
- Static vs dynamic wiring: `skills:` preload hard-wires standing expertise; leave the rest to discovery.
- Composition is planes, not a pipeline: authority flows down, artifacts flow up, verdicts flow sideways — a failed verdict routes to the plane that caused it (loop mechanics live in `[[loop-rules]]`).
- Every dispatch is a sealed contract: charter + enumerated inputs + budget + typed return (`references/best-practices.md` "The dispatch is a sealed contract"); the worker never sees the host's deliberation or sibling transcripts.
- The return channel is session-bound, durable state isn't: a completion notification reaches only the live session that made that dispatch, and dies with it. A durable-effect dispatch (PR, branch, ticket) must be discoverable from that state alone by a later session — never solely from having witnessed the notification (`references/best-practices.md` "The return channel doesn't survive the session").

## Design
1. **Solo-first — the host inline is the null unit and wins by default.** A seat must buy
   something the host cannot provide: isolation (fresh context), parallelism (genuinely
   concurrent slices), or independence (generator≠critic on a high-stakes artifact). A team must
   buy it twice. A dispatch that costs more context and latency than doing the work inline is
   over-orchestration, whatever the task's step count — then match the unit to the task and
   justify team fan-out by genuine parallel value.
2. Each description a precise interface; `tools` scoped, `model` to task class, `skills:` only for standing expertise; verify keys against the installed build.
3. Keep teammate roles as subagent definitions (teams compose them at runtime).
4. Dispatch sealed and shallow: enumerate inputs, state the budget, name the typed return; depth ≤ 2 (host → specialist) — a third level needs justification, a fourth means the decomposition under-cut.
5. For a parallel BUILD team, dispatch the disjoint same-tree fan-out (`references/best-practices.md`): file- and import-disjoint slices concurrently in one tree, each worker self-gating its own path, the host running the whole-tree gate + negative controls at the wave boundary; worktrees only when slices must mutate overlapping files. **Precondition — the HOST owns git; workers only edit files.** A worker that drives its own branch/commit/PR lifecycle (e.g. a `build-lead`/`dispatch-ticket` dispatch) is outside this shape entirely: two such workers race on the shared index/HEAD regardless of file disjointness, so they take per-worker worktree isolation whenever concurrent — file-disjointness licenses parallel timing there, never same-tree sharing (incident 2026-08-11: this step's conclusion copied without the precondition shipped a blocking same-tree race in a sibling skill).
6. Self-score (below); fix until every gate dimension (D2, D4) ≥ 3.

## Review
1. This skill's gates are systemic judgment, not a single-file mechanical check — there is no `harness_checks` subcommand: D2 is judgment because whether a description is a precise interface only shows against the sibling set (no string test sees it); D4's YAML-validity half IS mechanizable — its checker is queued, not built — so until it lands, score D4 by inspection and mark uninspected fields skipped-not-passed. Score against `references/rubric.md`, citing evidence on the 1–5 anchors.
2. Check plane separation first (the top failure: expecting `/goal` to select capabilities).
3. Findings by severity; gate verdict; top issues with a concrete fix each. **Generator ≠ critic:** for a high-stakes system dispatch the independent **`wiring-checker`** (fresh context, scores this same rubric by inspection) rather than grading your own arrangement.

## Improve (repair an arrangement)
Review first, then close the gap — plane separation and connective tissue before polish. Fix the wiring, re-score, finalize only when every gate dimension (D2, D4) ≥ 3. (Improve = review + targeted redesign.)

## Update (re-sync after drift)
Wiring drifts two ways. The BUILD moves: frontmatter keys and `skills:` preload semantics change — re-verify every field against the installed build (the rubric's D4 "verified against build" anchor is the check). The CAPABILITY SET moves: a skill or agent is added, renamed, or retired — re-review every description, preload, and fence that referenced it. Either change re-opens the gate dimensions.

## Output contract (review)
```
Artifact: <system/frontmatter>  ·  Rubric: rubric-orchestration
| Dim | Type | Score | Finding | Evidence |
Gate (D2,D4): <pass/fail>
Top issues: 1) … — fix: …
```

## References & tools
| Path | Use when |
|---|---|
| `references/rubric.md` | Scoring dimensions and anchors (judgment-based) |
| `references/best-practices.md` | Design guidance / explaining a finding |
| `references/foundations.md` | When a finding turns on a shared model (discovery vs continuation) |
| `[[write-handoff]]` | The return contract a composed agent hands back — the other half of composition |
| `[[loop-rules]]` | Continuation mechanics (`/goal`, `/loop`, hooks) and loop discipline — owns the self-orchestrated-looping canon (budgets, locus escalation, durable state) |
| `[[parallel-work-rules]]` | A relayed report needs the same independent-verification discipline as a self-report — this skill's "verify independently" rule extends to any intermediary, including your own dispatcher |

**Done** when every unit matches its task shape (the null unit respected — no seat doing host-inline work), every description is a precise fenced interface, frontmatter is verified against the build, dispatches are sealed and typed, both gate dimensions (D2, D4) score ≥ 3, and a high-stakes arrangement carries its independent wiring-checker pass. **NOT done** while any description starves the router, a fence is one-way, a dispatch leaks history or lacks a budget, planes are conflated — or the only score the arrangement has is its designer's.
