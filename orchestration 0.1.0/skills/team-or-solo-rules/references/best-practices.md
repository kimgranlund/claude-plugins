# Best Practices — Orchestration, Integration & YAML Frontmatter

> `team-or-solo-rules` domain reference. Foundations in `foundations.md`; scored by `rubric.md`. · 2026-06-27

Covers how subagents, skills, and teams discover and compose with each other, and the productive expressions of the frontmatter that wires them. Assumes the models in `foundations.md`. Scored by `rubric.md`.

## Choosing the unit of work

Three primitives, three different jobs. Pick by the shape of the task, not by habit.

A **skill** is a *procedure* — a repeatable workflow loaded on demand. Use it when the same multi-step method recurs.

A **subagent** is *delegation with isolation* — a focused worker in its own context window that returns a bounded, typed result to the caller (the `handoff-compose` block), its working transcript dying with it. Use it when a task is scoped, isolatable, and only the result matters ("research X and report back"). Cost is lower because only the result returns — and a large artifact comes back by reference (a path), never inlined.

An **agent team** is *collaboration* — multiple full Claude instances that message each other and self-coordinate through a shared task list. Use it only when workers need to share findings and challenge each other ("investigate this bug from three angles and debate"). Cost is higher (each teammate is a separate instance); justify the fan-out with genuine parallel value.

The decision rule: result-only → subagent; discussion required → team; recurring method → skill. Reaching for a team when a subagent would do is the most common over-spend.

## How they discover each other (the connective tissue)

Skills and subagents do not read each other's files. The connective tissue is that **every capability's description is concatenated into the system prompt at startup**, and the orchestrator — not the skills or agents — holds them all and routes by relevance. This is the dynamic, implicit layer.

There is also a static, explicit layer: a subagent can preload skills via a `skills:` frontmatter field, injecting that skill's content at the subagent's startup so it never has to discover its core expertise. (Verify the exact key against your installed build — subagent frontmatter drifts.)

Three tiers, used deliberately:
- **Descriptions** = dynamic connective tissue the orchestrator resolves per turn.
- **`skills:` preload** = static hard-wiring when a specialist must always have certain expertise.
- **CLAUDE.md** = the human-authored standing index of what exists.

## How teams are described vs. subagents

A subagent is *authored statically* as a reusable file (`.claude/agents/*.md`) discovered by its description. An agent-team teammate is *described in natural language at runtime* — you enable the feature with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and then describe the teammates you want in the prompt; Claude spawns them dynamically. There is no team file you author; the team config is machine-generated runtime state and pre-authoring it is unsupported. To define reusable team *roles*, you still write subagent definitions — teams compose them at runtime.

## The dispatch is a sealed contract

A subagent invocation is a fresh distribution with a sealed input set. Every delegation carries, explicitly:

- **charter** — who the worker is, what it returns, when it is done
- **inputs** — the complete world, enumerated: the plan node, file paths, doc/decision IDs
- **skills** — the policy the role loads (its `skills:` manifest)
- **budget** — tool calls / tokens / attempts it self-terminates against
- **returns** — the typed handback (`handoff-compose`)

Explicitly absent: conversation history, the host's deliberation, sibling transcripts. Every leaked token biases the fresh context toward the host's framing and silently couples workers the architecture claims are independent. When a worker can't succeed from its enumerated inputs alone, the fix is a better input artifact, not more leaked context — leakage is how systems paper over bad contracts until the contracts are unrecoverable.

Consequences:

- **Depth ≤ 2.** Host → specialist covers almost everything; a third level needs justification; a fourth means the decomposition under-cut and a worker is compensating by becoming an orchestrator.
- **`skills:` is the role's policy manifest.** What a role loads is declared configuration — changing a reviewer's standard is an edit to the skill it preloads, with a diff, not a per-dispatch prompt tweak. Name the skills the work leaned on in the handback, so a quality shift is traceable to a policy change.
- **`model` in frontmatter is the default, not the routing.** Route by the task's type at dispatch — mechanical checks and extraction to a fast model, novel design to a strong one — overriding the role default when the task class differs.
- **Planes, not a pipeline.** Authority flows down (the host authorizes), artifacts flow up (workers return), verdicts flow sideways (verifiers judge without the maker's framing) — and a failed verdict routes to the plane that caused it: the artifact, the spec that permitted it, or the plan that mis-cut it. Loop mechanics — hierarchical budgets, locus escalation, durable state — are owned by `loop-rules` and its self-orchestrated-looping canon.

## Executing a parallel build: the disjoint same-tree fan-out

When an agent team's job is to BUILD — apply many edits across one repository — the default execution model is a **disjoint same-tree fan-out**: dispatch file- and import-disjoint slices CONCURRENTLY into ONE working tree, with no merge step. Proven on the doctrine-hardening build (~18 concurrent slices, zero collisions, no integration merge).

It works because the slices are disjoint by construction — that is the decomposition side (slice by owning file so each file has exactly one writer), owned by `system-decompose`; do not re-derive it here. Given disjoint slices, the execution discipline is:

- **Each worker self-gates only its own path.** A worker confirms `npm run check 2>&1 | grep <own-path>` comes back empty and runs its own targeted test — it NEVER runs the whole-tree gate. Siblings are mid-write, so a whole-tree `npm run check && npm test` during the wave reports their half-finished state and is meaningless. The worker's contract is "my path is clean," nothing wider.
- **The host runs the authoritative whole-tree gate at the wave boundary.** Only once every worker in the wave has handed back does the host run `npm run check && npm test` over the whole tree, plus the negative controls for any governance code, and THEN commit. The wave boundary is the only place a whole-tree gate is meaningful. The host's role there is mechanical — run the gate, read the verdict, commit; a failure routes back as a dispatched repair slice, never an inline host fix.
- **A serial PREP slice pins shared interfaces before a wide fan-out.** When the parallel writers depend on a shared contract — a signature, a cross-reference wording, a canonical home — run ONE serial slice first that fixes it, so the concurrent workers build against a settled base instead of diverging (the B0 / wave-prep pattern).
- **Defer every barrel/shared-file edit to a single serial integration slice.** A file two slices would both touch is not fanned out; it is collected into one serial slice, keeping the fan-out collision-free.

**Worktrees are the fallback, not the default.** Reach for git-worktree isolation ONLY when slices genuinely must mutate overlapping files and cannot be made disjoint. For a properly file-disjoint fan-out, a worktree per slice adds merge cost for no isolation benefit — one tree is correct.

This pairs with `system-decompose`, which owns the decomposition side: the file-disjoint slicing test (single writer per file; shared edits deferred) and the serial-PREP pattern that make this execution model safe. This skill owns the execution model; that skill owns the slicing that feeds it.

## Frontmatter: productive expressions

Frontmatter is the integration contract. Treat each field as load-bearing.

**Skill frontmatter** — `name` and `description`. The description is the whole trigger: state what it does *and* when to use it, in third-person natural language ("This skill should be used when…"), carrying the intent keywords a user would actually say. No keyword dumps; a few representative anchors generalize better than an exhaustive list.

**The fence is part of the interface.** A description does two routing jobs: PULL the asks it owns (the trigger vocabulary) and REPEL the asks a neighbor owns — a NOT-clause at description altitude ("NOT for X (neighbor)") is how adjacent capabilities keep from grabbing each other's work. Fences live where routing happens: a body cross-reference is composition, not a fence. They are reciprocal — every NOT-clause names a neighbor whose own description claims that territory, and a neighbor fencing toward this capability gets fenced back (the corpus-level law is `skills-audit/references/standard-of-excellence.md` §S2). A truthful fence never weakens the positive vocabulary; it counterbalances it.

**Subagent frontmatter** — `name`, `description` (the auto-delegation trigger; write it as a use condition, add a proactive nudge like "Use PROACTIVELY immediately after writing code" when warranted), `tools` (whitelist to the verbs the role needs — omitting it inherits the full toolset including MCP, which is unsafe for a read-only role), `model` (set deliberately: a fast model for search, a stronger one for implementation), and optionally `skills:` to preload standing expertise.

## Do

- Treat every description as a precise interface; review it whenever behavior changes.
- Scope `tools` to the role's actual needs.
- Use `skills:` preload for a specialist that should never have to "discover" its expertise.
- Keep discovery dynamic; only hard-wire what genuinely must always be present.
- Solo-first: the host inline is the null unit — dispatch a seat only for isolation,
  parallelism, or independence the host can't provide.
- Match the unit to the task: subagent for results, team for collaboration, skill for procedures.
- Dispatch sealed: enumerate the inputs, state the budget, name the typed return — never leak history or sibling output.
- For a parallel build, fan file-disjoint slices into one tree; let each worker self-gate its own path and the host gate the whole tree at the wave boundary.

## Don't

- Rely on files cross-referencing each other by name as the wiring — the orchestrator routes on descriptions, not file mentions.
- Write vague descriptions ("helps with documents") — that starves the router and silently disables the capability.
- Inherit the full toolset by omitting `tools` on a constrained role.
- Reach for a team when a subagent's summary would do.
- Dispatch a seat for work the host finishes inline faster than the dispatch round-trips —
  "multi-step" alone never earns a team.
- Nest delegation past host → specialist without justification — depth is a smell of under-decomposition.
- Conflate discovery with continuation (see foundations).
- Spin up a worktree per slice for a file-disjoint fan-out — it adds merge cost for no isolation gain; worktrees are the overlap-only fallback.

## Best-in-class example

A reviewer subagent with a precise trigger, scoped tools, deliberate model, and a preloaded standard:

```markdown
---
name: security-reviewer
description: Reviews code for security exposure and hardening gaps. Use
  PROACTIVELY immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: fable
effort: high
skills: [clinical-coding-standards]
---
You are a senior code reviewer. When invoked: run `git diff`, focus on changed
files, skip anything the linter already enforces. Report by priority —
Critical / Warnings / Suggestions — each with a concrete fix. If nothing is
Critical or Warning, say so in one line and stop.
```

The description routes it, the tools box its blast radius, the model fits the task, and `skills:` gives it standing expertise without discovery.
