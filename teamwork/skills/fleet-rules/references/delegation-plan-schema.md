# Delegation-plan schema — a citable task-graph shape for multi-seat fan-out

> `fleet-rules` domain reference (Part B, Design step 5). Adapted from disler/fusion-harness's
> collaboration mode (`USER_PROMPT_COLLAB_DELEGATE.md`, `USER_PROMPT_COLLAB_PROPOSE.md`),
> 2026-08-25. The task-graph fields (`id`/`depends_on[]`/`outputs[]`/`mode`) formalize what
> Design step 5 and `[[parallel-work-rules]]` already say in prose — disjoint fan-out, host owns
> git, serial default on unconfirmed disjointness. The propose→merge→delegate→execute flow below
> is a new pattern this skill didn't carry before; it's captured here because it's the concrete
> procedure that produces a graph in this shape, not restated doctrine elsewhere.

## The shape

A delegation plan is a JSON task graph. Each task carries:

```json
{
  "id": "1.a",
  "assignee": "<seat-id-from-roster>",
  "description": "<what this task does>",
  "depends_on": [],
  "outputs": ["<path-or-evidence>"],
  "mode": "read"
}
```

- **`id`** — dependency-grouped: `1.a`/`1.b` run in the same wave, `2.a` waits on wave 1. The
  number is the wave, the letter distinguishes concurrent tasks within it.
- **`assignee`** — an exact seat id drawn from a STATED roster (`fleet.json`/`fleet-roster.md`,
  Section 3's own record).
- **`description`** — the charter, same discipline as any sealed dispatch (`references/
  best-practices.md` "The dispatch is a sealed contract").
- **`depends_on[]`** — authoritative and acyclic. Two tasks with no dependency edge between them
  run concurrently by default — **maximize parallelism**: add an edge only when a task genuinely
  needs another's output, never as a default-safe hedge. An edge that isn't load-bearing is a
  bottleneck the schema itself makes visible and checkable (a reviewer can trace the graph and
  challenge an edge that doesn't correspond to a real data dependency).
- **`outputs[]`** — paths or evidence the task produces; this is what a downstream task's
  `depends_on` is actually waiting on, and what a reviewer checks landed.
- **`mode`** — `read` or `write`. Read tasks overlap anything, including each other and any write
  task, and stay unserialized against the tree. Write tasks serialize against a shared tree:
  two write-mode tasks in the same wave with no dependency edge is a graph defect, not a
  schedulable pair — Design step 5's own same-tree-write precondition ("the HOST owns git;
  workers only edit files") applies per-task here, not just per-wave.

## Ownership and handoffs

Ownership is stated concretely per task, not implied by proximity in the graph — the `outputs[]`
field IS the handoff: a task consumes another's declared outputs, staying clear of its sibling's
undeclared side effects. A task that needs something not in any upstream `outputs[]` is missing a
`depends_on` edge or the plan is wrong; fix the plan, don't paper over it with leaked context
(the same discipline `best-practices.md`'s sealed-contract section already states for any
dispatch: "when a worker can't succeed from its enumerated inputs alone, the fix is a better
input artifact, not more leaked context").

## Propose → merge → delegate → execute

The plan is produced by **one coordinator merging N independent read-only proposals** — never a
vote, never a single proposer:

1. **Propose** — N seats each read the same brief in isolation and each return a candidate task
   graph. A proposal dispatch is READ-ONLY BY TOOL ALLOWLIST, not by instruction: give the seat
   `Read`/`Grep`/`Glob` only, exactly as a sealed-dispatch's `tools` field would scope any other
   role (`SKILL.md` Design step 2, "`tools` scoped, `model` to task class"). An instruction saying
   "propose only, don't write" is not the control — the allowlist is; the same generator≠critic
   discipline this skill already applies to review (Section 10.3) applies here to proposal purity.
2. **Merge** — the coordinator reads every proposal and produces ONE graph, taking the best idea
   from each rather than picking a winner wholesale ("take the best ideas from every proposal;
   the plan is yours, not a vote"). This is a judgment step, not a mechanical union — a naive
   union of N proposals' edges can introduce a cycle or a false write/write overlap that no single
   proposal contained.
3. **Delegate** — the merged graph is what gets sealed and dispatched, wave by wave, task by
   task, exactly as any other sealed dispatch (charter + inputs + budget + typed return).
4. **Execute** — waves run in `id`-number order; within a wave, every task with no unresolved
   `depends_on` runs concurrently; the host (or coordinator) gates the wave boundary before
   opening the next wave, same shape as Design step 5's own same-tree fan-out wave gate.

## Mapping onto sealed dispatch

fusion-harness enforces "read-only" on its propose phase by handing the proposing agent a
restricted tool surface — not a prompt instruction it could ignore. The direct mapping onto this
plugin's own dispatch contract: a **proposal dispatch** (`Agent` tool or `context: fork`) states
`tools: Read, Grep, Glob` explicitly, the same mechanism `references/best-practices.md`'s sealed
contract already names for scoping any role's budget — no new dispatch primitive, just this one
concrete instance of "tools scoped" applied to the propose step specifically. A **delegate/execute
dispatch** downstream of the merge is a normal sealed dispatch under this graph's own `mode`:
`write`-mode tasks get the tool surface their work needs; `read`-mode tasks stay restricted the
same way the proposal phase was.

## When to use this over prose fan-out

Design step 5's disjoint same-tree fan-out already covers the common case (file-disjoint slices,
no formal graph needed) — reach for this schema when a fan-out has real cross-task dependencies
(some tasks need others' outputs before they can start), a roster wider than "the obvious
disjoint slices," or when a reviewer needs a citable artifact to check the dependency claims
against rather than trusting the coordinator's own account. A single wave of genuinely
independent slices doesn't need this schema — that's exactly the case Design step 5 already
handles in prose.
