# skill-review — orchestration-coordinator (FLOOR)

```
Skill: orchestration 0.1.0/skills/orchestration-coordinator/SKILL.md · Standards: skill-authoring-standards · Lint: clean (0 fail / 1 warn)
Verdict: PASS
```

Lint verdict line: `skill-postwrite-invocation-lint · 0 fail / 1 warn` — the one warn is W4
(agentive head `coordinator` on a skill), dismissed under R3 below with its check cited.

Reviewed 2026-07-20. Dispatch context honored: the exact-name skill/agent pairing and the
no-dispatch host-adoption design are confirmed intent (not findings); the absence of a
revert-to-solo-first escape hatch is confirmed intent (not a finding). Both were still verified
against the tree rather than taken from the dispatch alone (checks cited below).

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | SKILL.md:71-75 (host never Write/Edits deliverables — delete it and the host does small pieces itself); SKILL.md:77-81 (solo-first override — delete it and orchestration-design's default reasserts); SKILL.md:103-106 (repair-by-locus, twice-indicts-the-contract — delete it and the naive same-seat re-dispatch loop returns) | None — all 3 sampled lines survive the deletion test |
| R2 | N/A | — | SKILL.md:14 `disable-model-invocation: true` — the description never enters model context; per standards it is menu documentation, and it reads correctly as such (states the override semantics and the three non-uses a human scanning `/` needs) | None |
| R3 | PASS | nit | Species = command (side-effectful, human-timed phase entry); both dials explicit (SKILL.md:14-15); `argument-hint` present (SKILL.md:16). Lint W4 (agentive `-or` head) **dismissed with check**: SKILL.md:27-31 states the deliberate agent-name mirror, and the precedent is real — read forge's `ops-issues/SKILL.md:25-26`, which records the identical same-name skill/agent pairing "as a ruling, not drift", with the same `disable-model-invocation: true` containment. The dispatch's claim of the ops-issues contrast (that one DOES dispatch its agent) also verified: ops-issues SKILL.md:33,46 dispatches the agent; this skill spawns no coordinator seat | None. (Nit: SKILL.md:28-29 calls ops-issues "the first instance" — a prose claim that will silently stale if a third pairing lands; harmless) |
| R4 | PASS | — | Standing spec-present register throughout (e.g. SKILL.md:71-75, 85-88); zero uppercase hard gates in the body (lint W7 silent — under the ≤3 cap); the two bolded discipline blocks (SKILL.md:71-75, 77-81) commit rather than describe | None |
| R5 | FAIL | **major** | SKILL.md:41-43 claims the eight priorities are "restated here as the host's hard commitments, not re-derived" — but the copy **already drifted at birth** against `agents/orchestration-coordinator.md:22-69`. Dropped clauses, each verified by side-by-side read: (a) agent:23 routes "doc work → system-planner"; SKILL.md:45 drops "doc" (design-doc authoring has no route in the adopted copy); (b) agent:30-31 "never your deliberation or a sibling's transcript" in enumerated inputs — absent from SKILL.md:50-51 and 86-87; (c) agent:34-37 the disjoint fan-out default + serial integration slice + worktree-only-for-same-file doctrine — absent entirely; (d) agent:47-48 "a green per-part gate proves the parts, not the whole" + "require the honest verify tier be stated" — absent from SKILL.md:52-55; (e) agent:54-55 "oscillating findings or budget burn without frontier movement force the decision now" — absent from SKILL.md:56-57; (f) agent:65 "stand up a fresh seat rather than re-dispatching a stood-down one" — absent from SKILL.md:63-65; (g) agent:28 "a repo carrying its own review seat keeps its own standard — defer there" — absent (SKILL.md:46 keeps only the build-seat half). This is the drift pair skill-authoring-standards' rule 8 names, and the fidelity claim at :43 is currently false | Primary fix: replace the inline restatement (SKILL.md:45-69) with "Read `${CLAUDE_PLUGIN_ROOT}/agents/orchestration-coordinator.md:22-69` and hold those eight priorities as this session's own operating rules", keeping inline only the genuine host deltas — the P8 audience rewrite (SKILL.md:66-69, correct and necessary), the Write/Edit discipline (:71-75), and the solo-first override (:77-81). Fallback if inline survival is preferred: restore clauses (a)-(g) verbatim and add a drift check between the two files to the plugin's gate |
| R6 | PASS | — | 125-line body, well inside the 5,000-token head; discipline gates at SKILL.md:71-81, output-contract shape at :66-69 and :93-96, failure branches at :98-111, done predicate at :120-124; no references dir needed at this size; relative-path caveat filed under R7c | None |
| R7 | FAIL | **major** | (a) **Preload gap.** The agent seat this contract comes from carries `skills: [orchestration-design, loop-design]` (agent:15) — the seat never runs without loop-design's closed set in context. The host adopting the same contract is never told to load either: yet SKILL.md:56, :92, and the done predicate at :120 all bind to "a named `loop-design` decision". Both siblings are model-invocable (loop-design SKILL.md:13, orchestration-design SKILL.md:16 — `disable-model-invocation: false`, verified), so auto-discovery *may* rescue it, but mention-routed discovery is exactly the unreliability the agent's preload exists to bypass. Steelman ("the mention will route the host there") fails on that point — finding survives | Add to Phase 2, first line: the host invokes `loop-design` (its closed decision set is the close condition) and `orchestration-design` (the sealed-contract doctrine) before the first dispatch — mirroring agent:15 |
| R7 | FAIL | minor | (b) **Missing failure branch: re-invocation mid-charter.** SKILL.md:113-118 covers only a new charter *after* close; no branch governs `/orchestration-coordinator` fired while a charter is still open (fold into the open charter? close it first? two concurrent charters?). Steelman ("When this rule ends implies one at a time") — it implies, it doesn't branch; kept as minor | Add a branch: a second invocation while a charter is open → name the open charter and require an explicit close-or-fold decision; never run two implicit charters |
| R7 | FAIL | minor | (c) **Unresolvable citation path + one unfenced cross-plugin seat.** SKILL.md:23 and :42 cite `agents/orchestration-coordinator.md` as a bare relative path — resolves against an arbitrary session cwd, not the plugin root (standards: bundled paths go through `${CLAUDE_PLUGIN_ROOT}`); becomes load-bearing under the R5 primary fix. And `doc-reviewer` (SKILL.md:12, :48) is scribe's agent, not this plugin's (verified: only `scribe 0.1.0/agents/doc-reviewer.md` declares it; this plugin's agents/ has no doc-reviewer) — a legal soft mention, but unlike the `handoff_check.py` mention (:53-54, which states its degraded path) it names no fallback when scribe is absent. The agent file shares this gap (agent:27), so the root fix belongs there too | Prefix both citations with `${CLAUDE_PLUGIN_ROOT}/`; give the doc-reviewer mention a degradation clause (e.g. "where scribe isn't installed, adversarial doc review routes to `code-reviewer`'s sibling discipline or is named as an uncovered gate in the rollup") |
| R8 | PASS | — | Numeric anchors where load-bearing: "one sentence" restatement (SKILL.md:36-37), "≥2 seats" charter floor (:101), "never … twice" repair bound (:103-106). Per-dispatch budgets are charter-parameterized by design; the anchor is the *stating requirement* (:50-51), matching the agent's own form (agent:38-39) | None |

Verdict on the whole: **PASS** — no blocking finding; two majors, both with one-move fixes.

Reviewer-discipline compliance: every dismissal above cites its check (R3's W4 dismissal cites
ops-issues SKILL.md:25-26 read in full; R2's N/A cites the dial at :14); no "fixed/shipped" claims
were accepted — the ops-issues precedent, the sibling dials, and doc-reviewer's home were verified
against the tree, not the dispatch prose; the steelman pass ran on all findings, with R7(a)'s and
R7(b)'s surviving rebuttals recorded inline and R5's fallback fix shaped by its strongest rebuttal
(deliberate compression) — which fails against the explicit fidelity claim at SKILL.md:43.

Top 3:
1. **R5 major** — the "not re-derived" restatement has seven birth-drift deletions against
   agent:22-69; either point at the agent file via `${CLAUDE_PLUGIN_ROOT}` and keep only the three
   host deltas inline, or restore clauses (a)-(g) and gate the pair for drift.
2. **R7(a) major** — Phase 2 must mirror the agent's `skills:` preloads: invoke `loop-design`
   (the done predicate binds to its closed set) and `orchestration-design` before the first
   dispatch.
3. **R7(b)+(c) minor** — add the re-invocation-mid-charter failure branch; make the two agent-file
   citations `${CLAUDE_PLUGIN_ROOT}`-rooted; give the cross-plugin `doc-reviewer` mention its
   degradation clause.
