---
name: a2a-protocol-facts
description: >-
  Explains the A2A (Agent2Agent) wire protocol + this estate's zero-dep implementation
  (@agent-ui/a2a, spec v0.3.0). Use for "what is an AgentCard", "Message vs Task vs Artifact",
  "which TaskState transitions are legal", "what goes in a TextPart/DataPart/FilePart", "which
  JSON-RPC method sends/polls", "how does SSE streaming work", "why does v1.0 break our wire".
  ANSWERS from a cited corpus; does not build. NOT for rendering payload content
  (a2ui-protocol-facts); NOT for building an agent (make-a2a-agent); NOT for isolation proofs
  (check-a2a-isolation); NOT for corpus record format (a2a-training-facts).
disable-model-invocation: false
user-invocable: false
---

# a2a-protocol-facts — the agent-to-agent wire model

> Corpus distilled 2026-07-08 from the local ground truth: the host-verification ledger
> **HV-1..HV-12** (SPEC §2, `agent-ui/.claude/docs/spec/a2a-foundations.spec.md` —
> character-verified A2A v0.3.0 quotes; transcribed into `…/lld/a2a-protocol-core.lld.md`) · the
> shipped code (`agent-ui/packages/agent-ui/a2a/src/{protocol,rpc,channel}/`, `tools/wellknown.ts`,
> `tools/http/`) · the bridge (`a2ui/tools/pipeline/transports/a2a.ts` +
> `.claude/docs/lld/a2a-a2ui-bridge.lld.md`). Four references carry a named residual GAP note
> (push/resubscribe semantics · the full 1.0 method-rename table · the generic A2A extension
> mechanism · card-caching/selection guidance in discovery) — each needs a spec fetch, never a
> memory fill.

Names and explains how two agents talk over A2A — discovery, lifecycle, content, transport,
extensions — so an integrator, a debugger, or a reviewer reasons from the protocol instead of
guessing. Six retrieval axes, one per reference.

| Ask | Load |
|---|---|
| Discovery & identity — "what is an AgentCard?", "the well-known path?", "what capabilities does a card declare?", "how does a client pick an agent?" | `references/discovery-and-agent-card.md` |
| Lifecycle — "Message vs Task vs Artifact?", "when is a Task minted vs a bare message exchange?", "which TaskState transitions are legal?", "how does a task complete/fail/cancel?" | `references/messages-tasks-artifacts.md` |
| Content — "TextPart vs DataPart vs FilePart?", "where do media types go?", "part-level vs message-level metadata?" | `references/parts-and-content.md` |
| Transport — "which JSON-RPC method?", "message/send vs streaming?", "how does SSE deliver task updates?", "push notifications?" | `references/transport-and-streaming.md` |
| Extensions & bridging — "how does an extension declare itself?", "capability negotiation via metadata?", "how is A2UI carried over A2A?" (the worked exemplar) | `references/extensions-and-bridging.md` |
| Versioning & conformance — "why pin v0.3.0?", "what breaks against 1.0.x?" (PascalCase RPC rename), "what does validateA2a enforce?" | `references/versioning-and-conformance.md` |
| Provenance — spec-fact vs estate-choice, the HV ledger map | `references/sources.md` |

## Consult procedure

1. **Classify the ask** by axis (discovery · lifecycle · content · transport · extension · version),
   then **Grep the term** in the matching reference and **Read that section** — never load all six.
2. **Separate spec-fact from estate-choice.** Every claim is tagged: `[spec §…]` (v0.3.0, HV-cited) or
   `[estate]` (a choice `@agent-ui/a2a` made where the spec is silent). When asked "is this required?",
   the tag IS the answer.
3. **Version questions get the pin stated first**: this estate speaks v0.3.0; upstream 1.0.x renamed
   the JSON-RPC methods (PascalCase) — wire-breaking, not cosmetic. Never answer from the newest spec
   without naming the pin.
4. **Route builds outward**: shaping a server/client → `make-a2a-agent`; proving isolation →
   `check-a2a-isolation`; payload content questions → the `a2ui-*` siblings.
