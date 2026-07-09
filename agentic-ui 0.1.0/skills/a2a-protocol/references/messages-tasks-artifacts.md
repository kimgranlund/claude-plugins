# Lifecycle — Message vs Task vs Artifact, and the TaskState machine

Estate paths relative to `agent-ui/packages/agent-ui/`; HV rows live in SPEC §2
(`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## The three nouns

**Message** — one conversational turn `[spec — HV-4, [T] Message]`: required `kind: "message"`
(a REQUIRED discriminator — "Always 'message' for a Message"; round-trip fails without it) ·
`role: "user" | "agent"` · `parts: Part[]` · `messageId`; optional `taskId` · `contextId` ·
`referenceTaskIds` · `extensions` · `metadata` `[estate — a2a/src/protocol/types.ts:29-39]`.

**Task** — server-minted work with a lifecycle `[spec — HV-5, [T] Task]`: required `kind: "task"` ·
`id` · `contextId` · `status: TaskStatus`; optional `history?: Message[]` · `artifacts?` ·
`metadata?` `[estate — a2a/src/protocol/types.ts:78-86]`. `TaskStatus = { state: TaskState;
message?: Message; timestamp?: string }` — timestamp is "an ISO 8601 datetime string"
`[spec — HV-11]`.

**Artifact** — a task's produced output `[spec — HV-11, [T] Artifact]`: required `artifactId`
("unique … within the scope of the task") · `parts: Part[]`; optional `name? · description? ·
metadata? · extensions?: string[]` `[estate — a2a/src/protocol/types.ts:94-101]`.

## When is a task minted?

The server decides, per response: `message/send` returns `Message | Task` — "a direct reply
Message or the initial Task object" `[spec — HV-12, [T] SendMessageSuccessResponse]`. A bare
message exchange needs no task. Correlation `[spec — HV-10, life-of-a-task@v0.3.0]`: "For the
first message, the agent responds with a server-generated `contextId`. If the agent creates a
task, it will also include a server-generated `taskId`. Subsequent client messages can include the
same `contextId` to continue the interaction, and optionally the `taskId` to continue a specific
task." Both ids are SERVER-generated; `contextId` groups related tasks/interactions.

## The TaskState machine — EXACT

**Upstream normative facts** `[spec — HV-5]`: the state set is exactly these 9 —
`submitted · working · input-required · completed · canceled · failed · rejected · auth-required ·
unknown` — and the four terminals admit no restart: "A task which has reached a terminal state
(completed, canceled, rejected, or failed) can't be restarted." ([S] §6.1).

**Upstream defines NO full transition matrix.** The edge table below is FAMILY POLICY — the estate
is the owning record for it (`[estate — a2a/src/protocol/task-state.ts:1-6]`, LLD §4). Never cite
these edges as spec.

| From | Legal successors `[estate — a2a/src/protocol/task-state.ts:10-36]` |
|---|---|
| `submitted` | `submitted · working · auth-required · canceled · rejected · failed · unknown` |
| `working` | `working · input-required · auth-required · completed · canceled · failed · unknown` |
| `input-required` | `input-required · working · completed · canceled · failed · unknown` |
| `auth-required` | `auth-required · working · canceled · rejected · failed · unknown` |
| `unknown` | all 9 (the indeterminacy wildcard — knowledge lost and regained) |
| `completed` / `canceled` / `rejected` / `failed` | — none (terminals sealed) |

Reading the policy: no `input-required`/`completed` before work starts; no regression to
`submitted`; no post-acceptance `rejected` (only `submitted`/`auth-required` may reject);
`auth-required` never goes directly to `input-required`; non-terminal self-loops are legal
(status re-emission with a fresh `status.message`). Of the 81 ordered pairs, **35 are legal, 46
illegal** — asserted exactly by the standing 9×9 matrix test (LLD §4).

## What `guardTransition` rejects `[estate — a2a/src/protocol/task-state.ts:44-53]`

```ts
guardTransition(from, to)  // [] if legal; else:
// [{ code: 'A2A_STATE', path: '/status/state', detail: 'illegal transition: <from> -> <to>' }]
```

- Never throws; returns the shared `A2aFailure` shape.
- `A2A_STATE` is emitted ONLY here — `validateA2a` never emits it. An out-of-union state STRING
  (`"paused"`) is a SHAPE defect: the validator reports `A2A_SCHEMA` at `/status/state`
  `[estate — a2a/src/protocol/validate.ts:170-176]`. Lifecycle legality vs shape validity are two
  different codes from two modules sharing one failure type.
- Any exit from a terminal state is rejected (terminal rows are empty by construction).

## Worked example — the arena's per-seat task lanes `[estate]`

The tic-tac-toe referee models EACH SEAT as one task-state lane, advanced only through
`guardTransition` (every transition the referee makes is re-asserted against the guard —
`[estate — a2a/src/arena/referee.ts:81-84]`):

- The seat that owes a move sits at `input-required`; the idle seat sits at `working`
  `[estate — a2a/src/arena/referee.ts:14-15]`.
- A legal reply moves the replying seat `input-required → working`
  `[estate — a2a/src/arena/referee.ts:163]`; the referee then puts the next seat at
  `input-required` `[estate — a2a/src/arena/referee.ts:184]`.
- Forfeit while a move is still pending exercises the policy's arena-driven direct edge
  `input-required → completed` `[estate — a2a/src/arena/referee.ts:142-145]` — the reason that
  edge exists in the table at all.

Fixtures: `task.input-required.json` (`status: { state: "input-required", timestamp: … }`) and
`task.completed.json` `[estate — a2a/src/protocol/fixtures/]`.
