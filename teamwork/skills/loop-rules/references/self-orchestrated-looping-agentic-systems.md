# Self-Orchestrated Looping Agentic Systems

**Best practices for nimble, efficient host/planner/creator architectures with hermetically sealed context**

Scope: systems where a central orchestrator (host) agent runs a loop, delegating planning-family work (decomposition, specification, low-level design) and creation-family work (execution, evaluation) to dedicated sub-agents, with skills as the policy layer. Companion documents: *Linguistic Techniques for Agents and Context*, the three *Naming Conventions* documents.

---

## 0. The Two Scarce Resources

Every design decision in this document optimizes one of two resources:

1. **Orchestrator context.** The host's context window is the system's most expensive real estate. It persists across the entire run, it conditions every routing decision, and everything that enters it stays (until compaction, which is lossy). The design goal: the orchestrator's context grows **linearly in decisions, not in work** — it accumulates plan states, verdicts, and pointers, never transcripts, diffs, or raw output.

2. **Verification signal.** A loop is only as good as its stopping test. Every cycle burns tokens; a cycle whose evaluation is weak, contaminated, or misrouted burns them for nothing. The design goal: every loop closes against an **independent, checkable oracle**, and every failure is attributed to the artifact that actually caused it.

Everything else — hermetic sealing, typed contracts, role separation, spawn discipline — is machinery for protecting these two resources.

---

## 1. Architecture: Planes, Not a Pipeline

Model the system as planes with distinct authority, not as a linear pipeline. A pipeline implies each stage trusts the previous; planes make authority explicit and give failures a place to be routed *back to*.

```
ORCHESTRATION   the host: holds goal, plan-state, budgets; routes; never does work
PLANNING        decomposer, spec-author, lld-designer: produce typed plan artifacts
CREATION        executors/generators: produce work artifacts + evidence
VERIFICATION    evaluators/verifiers: score artifacts against contracts; independent
STATE           the ledger: plan, artifacts, verdicts, budgets — the durable substrate
```

Two structural rules:

- **Authority flows down; artifacts flow up; verdicts flow sideways.** The orchestrator authorizes work; workers return artifacts; verifiers judge artifacts without the orchestrator's or generator's framing. No plane writes into another plane's inputs except through typed artifacts in the ledger.
- **The pipeline is a projection of the planes, not the architecture.** decompose → spec → lld → execute → evaluate is the happy path. The architecture is defined by what happens off it: a failed evaluation must be routable to *any* upstream plane (§7), which a pure pipeline cannot express.

---

## 2. Hermetic Context

A sub-agent invocation is a **fresh distribution with a sealed input set**. Hermetic means:

**Inbound seal.** The sub-agent receives exactly: its charter (identity + return contract), the typed input artifacts for this task, and the skills its charter names. Not the conversation history. Not the orchestrator's deliberation. Not sibling transcripts. Every extra token is a contamination vector — it biases the fresh distribution toward the host's framing, and it silently couples agents that the architecture claims are independent.

**Outbound seal.** The sub-agent returns a **bounded, typed result** — a verdict, an artifact reference, a findings list with a declared maximum size. Its working transcript (tool calls, dead ends, intermediate reasoning) dies with it. If the transcript might matter for debugging, it is written to the ledger as a file and returned *by reference*, never inlined into the host.

```
Spawn contract (every delegation, no exceptions):

  charter:   who you are, what you return, when you are done
  inputs:    [artifact refs]           — the complete world, enumerated
  skills:    [skill names]             — policy modules to load
  budget:    max tool calls / tokens / wall time
  returns:   <typed schema>            — size-bounded

  Explicitly absent: history, host reasoning, sibling output.
```

Three consequences worth internalizing:

- **Hermetic context is what makes parallelism safe.** Agents that share no mutable context cannot race except through the ledger, and ledger writes are explicit and inspectable. Fan-out (§8) is only correct because of this seal.
- **Hermetic context is what makes verification honest.** An evaluator that has seen the generator's reasoning inherits the generator's blind spots — it checks the *rationalization*, not the artifact. Oracle independence (§6) is the hermetic seal applied to the verification plane, and it is an invariant, not an optimization.
- **Sealing forces contract quality.** If the sub-agent can't do its job from the enumerated inputs alone, the instinct is to leak more context in. Resist it: the failure means the input artifact is underspecified, and the fix belongs in the planning plane. Context leakage is how systems paper over bad contracts until the contracts are unrecoverable.

---

## 3. The Contract Layer: Everything That Crosses a Boundary Is Typed

Prose handoffs are interpretation debt: every reader re-derives the meaning, and each re-derivation drifts. The rule: **any artifact crossing a context boundary conforms to a schema that fails loudly.**

Minimum artifact set for this architecture:

```
Goal            what done means, stated as checkable predicates + constraints
Plan            DAG of TaskSpecs with explicit dependency edges
TaskSpec        id, inputs (refs), acceptance criteria (predicates),
                assigned role family, budget
WorkArtifact    the produced thing + provenance (task id, inputs used, skill versions)
Evidence        what the creator claims and how it can be checked
                (test output, rendered result, diff) — claims without evidence
                are not accepted into the ledger
Verdict         pass | fail(findings[]) | blocked(reason), each finding bound
                to a locus (§7)
```

Practices:

- **Acceptance criteria are written by planners, before creation, as machine-or-cheaply-checkable predicates.** "Done when tests X, Y pass, bundle < N kb, no new dependencies" — never "done when good." A TaskSpec without checkable criteria is not a task; it is a wish, and the loop that consumes it cannot terminate honestly.
- **Schemas fail loudly and the loop repairs the artifact, not the output.** When a Verdict rejects a WorkArtifact, the repair target is chosen by fault locus — sometimes the artifact, sometimes the TaskSpec that under-specified it, sometimes the Plan that mis-decomposed it. Repairing the surface output while the upstream artifact stays wrong guarantees the same failure next cycle. This is the single most common structural defect in looping systems.
- **Push validation into generation where the artifact type allows it.** A planner emitting Plan-JSON against a schema, constrained decoding for structured artifacts, typed generation grammars for UI payloads — every construct-by-construction move shrinks the verification plane's burden and removes a class of loop iterations entirely. Generate-then-check is the fallback, not the default.

---

## 4. The Orchestrator: A Router With a Ledger, Not a Worker

The host's charter is deliberately thin: **interpret the goal, maintain the plan-state, route tasks, enforce budgets, integrate verdicts, decide continuation.** Its prohibitions matter more than its permissions:

- **The orchestrator never does object-level work.** The moment it "quickly fixes" a file or "just drafts" a spec inline, three failures land at once: its context absorbs work-product (violating the linear-growth rule), the work bypasses verification (nobody evaluates the host), and its routing judgment is now biased by being the author of what it routes. If a task is too small to delegate, it was too small to be a task — fold it into an existing TaskSpec.
- **The orchestrator holds pointers, not payloads.** Artifacts live in the ledger (filesystem, store); the host's context holds ids, statuses, and verdict summaries. A host that inlines a 400-line diff to "keep it handy" has spent context it can never reclaim on information it will never re-read.
- **The orchestrator re-anchors itself each cycle.** Long loops drift. Every iteration begins with a forced state echo — restate the goal predicates, the current plan frontier, remaining budgets — in fresh tokens near the action point. This is prefill-as-loop-discipline: recency dominates, so the loop's invariants must be *re-committed*, not merely present 40k tokens upstream.
- **Continuation is a decision, not a default.** Each cycle ends with an explicit choice from a closed set: `advance | repair(locus) | replan | escalate | halt(done) | halt(budget)`. A loop without a named decision point runs on momentum, and momentum always chooses "one more cycle."

---

## 5. The Planning Plane: Plans Are Artifacts, Not Intentions

Planning-family agents (decomposer, spec-author, lld-designer) exist to convert a goal into contracts the creation plane can execute *without interpretation*. Practices:

- **Decomposition targets independence, not smallness.** The unit of decomposition is "executable hermetically from its enumerated inputs" — a task that needs to peek at a sibling's work is mis-cut. Independence is what parallelism, sealed context, and honest credit assignment all rest on; size is just a budget parameter.
- **The dependency DAG is explicit and minimal.** Every edge in the plan is a serialization constraint and a context-handoff cost. Planners should justify edges, not independence — the default topology is parallel, and edges are added only where a real data dependency exists.
- **Specs encode intent at the depth the executor lacks.** A spec's job is to make the creator's interpretation space small: types, contracts, acceptance predicates, named failure branches ("if the API is unreachable → stub and flag, do not mock silently"). Every unstated assumption in a spec is a decision delegated to a sealed agent that cannot ask follow-up questions cheaply.
- **The plan is a living, versioned artifact.** Replanning is a first-class verdict outcome, and it produces plan-v(n+1) with a stated diff and reason — never in-place mutation the ledger can't reconstruct. But replan cadence is budgeted like everything else: a system that replans every cycle has an orchestrator laundering its indecision through the planning plane.
- **Plan validation before creation spends anything.** Cheap checks — DAG acyclicity, every task has acceptance predicates, every input ref resolves, budget sums within the run budget — run as a gate the moment a plan is emitted. Measure twice: unwinding three executed tasks costs orders of magnitude more than rejecting a malformed plan.

---

## 6. The Creation Plane: Generators and Verifiers Are Different Species

**Generators/executors** consume a TaskSpec and return WorkArtifact + Evidence. Their discipline:

- **Evidence is mandatory, and it is checkable, not narrative.** "Tests pass" is a claim; the test runner's output is evidence. An artifact arriving without evidence is `blocked`, not `pending review` — the creator's contract includes producing the means of its own verification.
- **Named failure branches, not improvisation.** A sealed agent hitting an unhandled state invents the most fluent-looking continuation. The spec names the branches; the creator's charter ends with "any state not covered → return blocked(reason)."

**Verifiers/evaluators** consume artifact + acceptance criteria and return a Verdict. Their invariants:

- **Oracle independence.** The verifier shares *no context* with the generator beyond the artifact and the criteria: not the generator's reasoning, not its self-assessment, not the orchestrator's hopes. A verifier prompted with "the executor believes this is complete" has been pre-loaded with the conclusion. Independence is structural (hermetic seal), not attitudinal ("be critical").
- **Mechanical checks before model judgment, always.** Order verification by cost: schema validation → compilation → tests → lint → *then* model-graded rubric review for what machines can't check. A model verifier re-deriving what a type-checker knows is the system's most expensive way to be less reliable.
- **Verdicts localize.** `fail` without findings-bound-to-loci is useless to the loop; the orchestrator can't route a repair it can't aim. Each finding names the artifact, the violated criterion, and the suspected locus (execution | spec | plan).
- **Chain reviewers into verifiers when stakes warrant.** A reviewer (open-ended findings) followed by a verifier (pass/fail against the now-explicit findings) converts subjective critique into a checkable gate — the reviewer discovers the criteria the spec missed; the verifier holds the line on them. Use the chain for novel or high-risk artifacts; a chain on every task is ceremony.
- **Never let the generator self-certify.** Self-evaluation is a smoke test the creator may run privately to avoid embarrassing submissions; it never substitutes for the verification plane. The system's honesty lives entirely in this separation.

---

## 7. Loop Design: Termination, Budgets, Credit Assignment

The loop is where systems die — by running forever, by converging on the wrong thing, or by repairing the wrong layer.

**Stopping is a predicate, owned by the goal.** `done := all acceptance predicates true ∧ no open findings ∧ within budget`. Stated declaratively at plan time, checked mechanically each cycle. "Looks done" is not a state.

**Budgets are hierarchical and enforced at spawn.** Run budget → per-task budget → per-repair-attempt budget. Every sub-agent receives its budget in its charter and self-terminates against it; the orchestrator enforces the outer envelope. A budget the agent doesn't know about is a budget enforced only by surprise.

**Repair attempts are bounded per locus with escalation, not retry.**

```
attempt 1 fail  → repair at reported locus (usually execution)
attempt 2 fail,
  same finding  → escalate locus: the spec is now suspect, not the executor
attempt 3 fail  → replan or halt(escalate to human)
```

The anti-pattern is the flat retry: re-running the same executor against the same spec expecting different results. Two identical failures are evidence about the *contract*, not the worker.

**Credit assignment is a routing function, not blame theater.** Given findings, choose the repair plane:

- artifact violates a stated criterion → **execution** repairs;
- artifact satisfies the spec but the spec permits the defect → **spec** repairs (the spec-author gets the finding, not the executor);
- the task shouldn't exist in this shape / dependencies were wrong → **plan** repairs;
- the goal predicates themselves are unsatisfiable or contradictory → **escalate** — no plane below the goal can fix the goal.

Route to the *highest* plane the evidence implicates, then regenerate downstream from there. Repairing an artifact whose spec is wrong produces an artifact that passes the wrong test.

**Detect thrash structurally.** Oscillation (A's fix reintroduces B's finding), monotone non-convergence (findings count not decreasing across attempts), and budget burn without frontier movement are ledger-computable signals. Each maps to a forced decision: oscillation → the two criteria conflict, route to spec; non-convergence → escalate locus; burn-without-progress → halt and surface. A loop that can't see its own thrash will narrate progress until the budget dies.

---

## 8. Spawn Discipline and Parallelism

Sub-agents are not free: each spawn costs a cold-start charter, an input serialization, and a result integration. Spend them where they buy something.

**Spawn when** the work would pollute the host's context (bulk reading, long generation, exploratory search), when the role must be independent (all verification), when tasks are parallel, or when a different policy bundle (skills, model) fits the task. **Don't spawn** for a lookup the host can do in two tool calls, or to launder a decision the orchestrator is charged with making — delegation of judgment the host owns is abdication, and it re-enters the host's context as a summary it must then re-judge anyway.

**Fan-out on the DAG's independent frontier; join on typed results.** The synthesizer that merges fan-out results is itself a sealed agent with a contract ("given N verdicts/artifacts, return merged artifact + conflict list") — merging in the host's context is object-level work (§4).

**Fan-out for diversity is a different pattern from fan-out for throughput.** N executors on N independent tasks is throughput. N executors on the *same* task with a selector verifier is best-of-N sampling — legitimate for high-variance creative generation, waste for deterministic work. Name which one you're doing; the budgets differ by N×.

**Depth discipline.** Every nesting level adds a serialization boundary and a place for intent to decay — the sub-agent's sub-agent has never seen the goal, only a charter derived from a charter. Two levels (host → specialist) covers almost everything; three needs justification; four is a smell that the planning plane under-decomposed and a worker is compensating by becoming an orchestrator.

**Model routing is a spawn parameter.** Verification-by-checklist, formatting, extraction, and mechanical transforms route to small/fast models; planning, spec authorship, and novel generation route to strong models. The charter, not the agent, owns the routing hint — it's part of the task's type.

---

## 9. Skills: Policy Injected at Spawn, Not Baked Into Agents

Keep agents **monolithic in mechanism, modular in policy.** The agent file is a thin engine — identity, return contract, loop discipline. Everything domain-specific — procedures, rubrics, failure-mode catalogues, house conventions — lives in skills, loaded by name at spawn.

- **The charter names its skills; the manifest binds them.** Which skills a role family loads is declared configuration, not per-spawn improvisation by the host. Changing a reviewer's rubric is a manifest edit with a diff, not a prompt tweak lost in a transcript.
- **Version skills like dependencies.** WorkArtifact provenance records skill versions used. When output quality shifts, the ledger can answer whether the policy changed — without provenance, skill edits are invisible confounders in every regression.
- **Rubric-manifest verification.** Verifiers in particular should be thin engines over pluggable rubric skills: the verifier procedure ("check each rubric item, emit findings with loci") never changes; the rubric library grows. This keeps the verification plane's behavior legible and its evolution auditable.
- **Skills are also how you keep charters short.** A charter that inlines its procedures is a charter that drifts from the canonical procedure the day the skill updates. Charters point; skills define.

---

## 10. State: The Ledger Is the System

Agent context is volatile by design — the seal (§2) guarantees it. Therefore **all durable truth lives in the ledger**: goal, plan versions, TaskSpecs, artifacts, evidence, verdicts, budget counters, decisions log.

- **The run is resumable from the ledger alone.** Test this property explicitly: kill the host mid-run, respawn it with only the ledger, and it should reconstruct the frontier and continue. If resumption needs the dead host's context, undocumented state was living in the transcript — find it and move it.
- **Decisions are append-only records.** Every `advance | repair | replan | halt` the orchestrator takes is logged with its evidence refs. This is what makes post-hoc credit assignment and system improvement possible: the loop's judgment becomes data.
- **Checkpoint at plane boundaries.** Plan accepted, task verified, replan issued — these are the natural commit points. Checkpointing mid-creation buys little (the artifact isn't trustworthy until verified) and costs serialization.
- **Compaction is a ledger operation, not a context operation.** When the host's context approaches limits, it doesn't summarize in place — it writes a state snapshot to the ledger and re-anchors from it. Summarize-in-context is lossy compression applied by the party with the least incentive to preserve inconvenient details.

---

## 11. Anti-Patterns

**The omniscient host.** Everything flows through and stays in the orchestrator's context "for awareness." The system works beautifully for forty minutes, then routing quality collapses as the context saturates — and the collapse is blamed on the model.

**Prose handoffs.** "Here's roughly what I found, you take it from here." Every boundary crossing without a schema is interpretation debt collected downstream with interest.

**The self-certifying creator.** Generator marks its own work done; verification plane exists on the org chart only. The loop terminates fast and wrong.

**Contaminated oracles.** The verifier gets the generator's transcript "for context." It now verifies the rationalization. Independence is structural or it is absent.

**Flat retries.** Same executor, same spec, third attempt. Identical failures are evidence about the contract; spending them on repetition is the loop refusing to learn.

**Surface repair.** Patching the artifact each cycle while the spec that permits the defect stays untouched. The findings count oscillates forever; the ledger shows motion without progress.

**Context leakage as contract subsidy.** The sub-agent keeps failing, so the host leaks more history in until it succeeds. The task now works and is unreproducible — its real spec is an undocumented transcript.

**Spawn theater.** Sub-agents for two-tool-call lookups; a "researcher" spawned to read one file. Cold-start costs exceed the work; the ledger fills with ceremony.

**Unbounded improvisation.** No named failure branches in charters; sealed agents inventing fluent continuations for states nobody specified. The system's behavior in edge cases is whatever the prior finds plausible.

**Momentum loops.** No explicit continuation decision, no thrash detection, budgets checked only at the end. The loop narrates progress until the money runs out.

---

## 12. Quick Reference

| Principle | Statement |
|---|---|
| Two resources | Orchestrator context and verification signal; everything protects these |
| Planes | Orchestration / planning / creation / verification / state — authority explicit, failures routable upstream |
| Hermetic seal | Sub-agents get charter + enumerated inputs + skills; return bounded typed results; transcripts die |
| Typed boundaries | Every crossing artifact has a schema that fails loudly; repair the artifact, not the output |
| Thin host | Routes, budgets, integrates verdicts; never does object-level work; holds pointers, not payloads |
| Plans as contracts | Independence-targeted decomposition; explicit DAG; acceptance predicates written before creation |
| Oracle independence | Verifiers share nothing with generators but artifact + criteria; mechanical checks before model judgment |
| Loop honesty | Stopping predicates; hierarchical budgets; escalate locus on repeated failure; detect thrash structurally |
| Credit assignment | Route repairs to the highest implicated plane, regenerate downstream |
| Spawn discipline | Spawn for context protection, independence, parallelism, policy fit; two levels deep by default |
| Skills as policy | Thin engines, pluggable rubrics; versioned, declared in manifests, recorded in provenance |
| Ledger is the system | Durable truth outside all contexts; resumable-from-ledger is a tested property |

*The reduction: a looping agentic system is a ledger of typed artifacts, a thin router that spends its context only on decisions, sealed specialists that spend theirs only on their task, and an independent oracle that decides what's true — with every failure routed to the plane that caused it.*
