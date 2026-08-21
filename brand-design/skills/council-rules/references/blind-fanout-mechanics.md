# Blind fan-out mechanics

## The dispatch shape: unnamed, synchronous, inlined

Every critic dispatch in the blind phase is an **unnamed** `Agent`-tool call to the domain's
critic-shell agent (brand's is `brand-judge`) — no `name:` field. A named (teammate-mode) dispatch
switches to mailbox delivery, and a further-nested dispatch made from inside an already-dispatched
seat completes to the ROOT session, never back to the dispatching orchestrator — the callback
structurally never arrives (`teamwork:fleet-rules` orchestration-rubric-a2, A2-R1; the same
mechanical fact `teamwork:dispatch-ticket`'s own no-nested-wait section documents for build
dispatches). An unnamed dispatch has no such failure mode: its own synchronous tool-result IS the
return value the orchestrating procedure reads directly, in the same turn.

The sealed prompt for each dispatch carries, inlined — never a path the critic reads itself:

1. The full persona file content for that one named critic.
2. The artifact under review (inlined or its path, per the domain instance's own convention).
3. Whatever context the domain instance requires before a critique is specific rather than
   generic (a brand's corpus context; a different domain's own equivalent).

## Same-turn concurrency

Every dispatch for a selected sub-council issues in the **same turn**, not one critic at a time.
Sequencing critics serially lets an earlier critic's findings bias a later one even without an
explicit deliberation round — the entire point of the blind phase is independence, and issuing
serially quietly reintroduces the anchoring effect the two-phase model's ordering exists to
prevent (`two-phase-model.md`). Each critic runs in its own context window with no visibility into
any sibling dispatch.

## Bounded rejection

A critic's return that doesn't match the critic-shell's own output contract (a missing findings
table, a missing severity tag, no verdict line) gets exactly **one** re-dispatch of that same
critic under the same sealed contract. A second miss is not a second re-dispatch — record that
critic's slot **UNMEASURED**, name it explicitly wherever the synthesis is reported, and proceed
without it (`harness:agent-writing-rules`' fan-out contract, A2-R6). The same rule covers an
outright dispatch failure (no return at all), not only a malformed one.

## Verbatim collection

Collect every critic's findings **verbatim** — relay the returned table/verdict exactly as
returned, never lossily paraphrased (A2-R5). A critic's typed return IS the record the synthesis
step reads; summarizing it down before synthesis loses exactly the cited evidence synthesis needs
to resolve contested findings (`severity-and-voting.md`) and name convergence
(`synthesis-shapes.md`).

## Why this stays host-side (or chair-side) rather than a further-nested orchestrator

A council's fan-out runs directly inside the procedure that owns it (the domain action-twin for
phase 1; the Chair for phase 2 — `two-phase-model.md`) rather than through an intermediate
coordinating agent that itself dispatches the critics. Introducing a coordinator layer between the
orchestrating procedure and the critic dispatches adds exactly the nesting depth that produces the
stranded-report failure above, for no compensating benefit — the fan-out is not so large or so
long-running that it needs its own isolated context.
