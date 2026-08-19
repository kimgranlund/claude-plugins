# UX flow intake schema

Fields lifted verbatim from `screens:break-down-flow`'s own task → journey (outside-in) ×
transitions → whole (inside-out) axes (`break-down-flow/SKILL.md`) — reframed as intake
QUESTIONS, never a second copy of the axis doctrine or the flow-card schema itself.

## Outside-in (journey) — task → journey

| Field | Question | Owning concept |
|---|---|---|
| Journey placement | What task does this journey serve, and where does it sit relative to sibling flows? | task → journey |
| Entries | Where can a user enter this journey — one entry, or several (deep link, resume, cross-flow handoff)? | entry states |
| Sequencing | What stages does the task require, in what order, and no more than that? | stage inventory |
| Effort shape | Linear wizard, hub-and-spoke, or something else — and does the shape match the task's own effort profile? | archetype fit |

## Inside-out (machine) — transitions → whole

| Field | Question | Owning concept |
|---|---|---|
| Per-transition mechanics | For every state, what verbs move the user out of it — including back and abandon? | transitions |
| Exit asserts | What must be TRUE at each exit (success/abandon/error) for the task to actually be done? | exits[].asserts |
| Failure/interrupt states | What's the recovery path from a fallible/destructive transition — does input survive? | recovery |
| Resume/persistence | Can the user leave and come back? Does the journey resume where they left off? | persistence |

## Scope frontmatter this shape stamps

```
scope: flow
build-owner: break-down-flow
dod-checker: flow-checker
```

## Both-planes note

Outside-in-filled/Inside-out-empty is `break-down-flow`'s own "right-journey-wrong-machine"
quadrant (stages right, transitions dead-end/lose input/exit without truth); the reverse — a
flawless machine walking stages the task never needed — is "wrong-journey-right-machine" (see the
pack's own both-planes rule for the general statement; not restated per file below).
