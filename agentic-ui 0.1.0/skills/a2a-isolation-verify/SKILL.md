---
name: a2a-isolation-verify
description: >-
  Prove that two (or more) agents interact ONLY over the declared wire — no shared context, no
  prompt leakage, no side-channel. Use for "prove no cross-contamination", "are these agents really
  isolated", "verify the seats can't see each other's context", "audit this multi-agent setup for
  leakage", "make the isolation claim testable". Emits an isolation proof: per-seat canaries +
  wire-origin audit + closed message schemas + provenance whitelist + byte-complete boundary
  recording + committed NEGATIVE CONTROLS proving every instrument bites. The method generalizes to
  any multi-agent system claiming context separation — A2A is the transport it was minted on, not a
  precondition. NOT for protocol facts (a2a-protocol); NOT for building the agents themselves
  (a2a-agent-design); NOT for payload-content security — catalog allowlists, callableFrom
  (a2ui-catalog-design). VERIFIES and reports; it does not build the system under test.
disable-model-invocation: false
user-invocable: true
---

# a2a-isolation-verify — the no-cross-contamination proof kit

An isolation CLAIM without instruments is a hope. This skill installs five instruments, then proves
each one bites with a deliberately contaminated negative control — the proof is the pair
(clean run passes + poisoned run fails), never the clean run alone. The method is the arena-minted
procedure (`agent-ui/packages/agent-ui/a2a/src/arena/isolation.ts` + `tools/arena/`, proven on a
real recorded flagship match); [references/instruments.md](references/instruments.md) carries each
instrument AS IMPLEMENTED with file:line cites and its negative control.

## The five instruments

1. **Per-seat canaries** — plant a distinct token in each agent's private context and scan the
   OTHER seats' recorded context AND every wire message addressed to them. Derive it
   DETERMINISTICALLY (the arena: FNV-1a over matchId+seat), not crypto-randomly — determinism keeps
   scripted reruns byte-identical, and a derivation collision can only ever false-positive, never
   hide a leak (guard it fail-fast, don't retry). A canary crossing seats is contamination caught
   red-handed.
2. **Wire-origin audit** — every message a seat RECEIVES must originate from the mediator (the
   referee): the audit walks every recorded wire event and fails any seat-inbound message with a
   non-mediator origin. Sufficient only under a star topology where no seat→seat channel exists —
   state that structural premise. ("Every fact traces to a received message" is instrument 4's job,
   not this one's.)
3. **Closed message schemas** — the inter-agent message type is CLOSED (no free-form fields, nested
   payloads hardened): fail extra keys at the top level AND one level into allowed nested objects
   (a top-level filter never looks inside an allowed key), and pin verbatim any nested string the
   mediator authors deterministically. Free text the mediator merely relays cannot be
   content-validated — that surface rides on the canaries; say so.
4. **Context provenance** — audit each seat's recorded context against the recorded wire: every
   system entry sits at position 0 (no hidden mid-history preamble), every user-role entry
   byte-identically frames a message the transcript shows was ACTUALLY sent to that seat. The
   seat's own free-form output has no authored form to check — it rides on instruments 1 and 3.
5. **Byte-complete boundary recording** — record EVERYTHING crossing each adapter boundary,
   byte-exact, AT the boundary (a tap around the provider call), never reconstructed from the
   agent's own session afterward; diff the full recorded request (system + every historical
   message) against the agent's own ground truth each call, so below-seam injection surfaces in the
   record where instruments 1 and 4 fail it.

## The negative controls (non-optional)

Commit at least one deliberately contaminated fixture per LEAK CLASS — in-transcript (a leak baked
into the recorded wire/context) and out-of-transcript (a provider/session mechanism bleeding context
below the agent seam) — plus a hand-built poisoned input per instrument in the test suite, and a
standing test proving each FAILS. A green run over a control is itself a suite failure. Poisoned
fixtures should stay SCHEMA-valid (the leak is semantic — catching it is exactly the gate's job) and
be regenerable by script, not hand-authored. An instrument never proven to bite is decoration (the
vacuous-pass lesson, learned repeatedly).

## The proof artifact

The output is a report: system identification (who, which providers, scripted vs real) · instruments
installed · clean-run evidence · per-instrument negative-control evidence · residual channels named
honestly (relayed free text, adversarial canary evasion, adapter-statelessness preconditions, timing
side-channels — typically OUT of scope; say so). Structural isolation (separate processes/contexts)
is an INPUT to this proof, not a substitute for it. Full shape with cites:
[references/report-format.md](references/report-format.md).
