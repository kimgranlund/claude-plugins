---
name: make-a2a-agent
description: >-
  Design and build an A2A-conformant agent — server or client side. Use for "make two agents
  talk", "build an A2A server", "write the AgentCard", "expose my agent over A2A", "wire the
  task lifecycle", "add SSE streaming to my agent", "my agent fails the other side's
  validation". Method: outside-in from the card's capabilities, inside-out from the Message/Task
  state machine, reconciled before code — conformance is a gate. NOT protocol facts
  (a2a-protocol-facts answers; this skill builds); NOT proving two agents are isolated
  (check-a2a-isolation); NOT the payload an agent RENDERS (a2ui-* siblings); NOT intake-schema
  fields (screens:feature-intake-rules / design:token-feature-intake-rules).
disable-model-invocation: false
user-invocable: true
---

# make-a2a-agent — build an agent that speaks A2A

The estate's reference implementation is `agent-ui/packages/agent-ui/a2a/` — the arena's
referee/seat pair, the pure framing core (`src/rpc/{frame,errors}.ts` + the socket-free
`tools/http/core.ts` `handleRpc` engine), the thin `tools/http/server.ts` shell, and the fail-fast
card gate in `tools/wellknown.ts`. The guided tour, in build order and with file:line cites:
[references/reference-implementation.md](references/reference-implementation.md).

## Method — two directions, reconciled before code

**Outside-in (the contract):**
1. Write the **AgentCard first** — identity, endpoint, capabilities, skills. The card is the API
   surface; everything the card claims becomes a conformance obligation. Validate it at
   construction time and refuse to start on an invalid card (the estate's fail-fast precedent:
   `serveAgentCard` throws — the one deliberate exception to its never-throw posture — and the
   shell calls it before it ever listens; tour §1). Keep `protocolVersion` (the pin) and `version`
   (the agent's own) distinct — two required fields, never conflated.
2. Decide the **interaction class**: bare message exchange, or task-minting work (long-running,
   cancellable, artifact-producing)? This decides half the server's shape.
3. Decide **transport posture**: request/response only, SSE streaming, push — driven by the
   consumer's latency needs, not by what's fun to build. Claiming less is fine; answer what you
   know but don't serve with `-32004` (known-unsupported) and what you don't know with `-32601` —
   the two-method-table honesty rule (tour §2).

**Inside-out (the mechanics):**
4. Implement the **RPC core as a pure function** (`(body) → response`), no socket knowledge —
   the estate's `handleRpc` pattern: parse → validate → dispatch → handler → framed response,
   TOTAL (handler throws caught → `-32603`). The socket shell stays thin (~40 lines) and manually
   smoked; the core gets the standing tests through injectable seams (tour §§2–3, 6).
5. Honor the **TaskState machine** with a transition guard — illegal transitions are bugs at the
   guard, never surprises on the wire. Separate upstream fact (the state set, the sealed terminals)
   from your own transition policy, and own the policy in one table (tour §4).
6. Content via **typed Parts**; anything non-text rides a DataPart with a declared media type. Keep
   ONE wrap/unwrap point for your domain payload (the arena's `wireMessage`/`readWireData`
   precedent; tour §4).

**Reconcile:** every card claim maps to an implemented method + a test; every implemented behavior
is either card-advertised or deliberately internal. A gap in either direction is an unresolved
assumption.

## Conformance gates (the definition of done)

- Card validates clean; served at the well-known path.
- Wire fixtures round-trip through the validator (`validateA2a` or equivalent at the consumer's pin).
- Version pin stated explicitly (see a2a-protocol-facts's versioning axis — the method names are
  pin-specific and wire-breaking across 0.3.0/1.0.x).
- If the agent will face untrusted peers: hand off to `check-a2a-isolation` for the provenance/
  containment proof — conformance ≠ isolation.
