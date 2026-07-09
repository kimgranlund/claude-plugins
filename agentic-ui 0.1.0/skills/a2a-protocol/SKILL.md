---
name: a2a-protocol
description: >-
  Explains the A2A (Agent2Agent) wire protocol + this estate's zero-dependency implementation
  (@agent-ui/a2a, pinned spec v0.3.0). Use to answer "what is an AgentCard / where does discovery
  look", "Message vs Task vs Artifact — when is a task minted", "which TaskState transitions are
  legal", "what goes in a TextPart / DataPart / FilePart", "which JSON-RPC method sends a message /
  polls a task", "how does SSE streaming work", "how do A2A extensions negotiate", "how is A2UI
  carried over A2A", "why does the v1.0 spec break our wire" (the PascalCase method rename — version
  drift is wire-breaking), "why did validateA2a reject this". ANSWERS from a cited, host-verified
  corpus (the HV ledger); it does not build. NOT for rendering payload content — surfaces, catalogs,
  bindings (a2ui-protocol / a2ui-catalog-design); NOT for building an A2A server or client
  (a2a-agent-design); NOT for proving agent-vs-agent isolation (a2a-isolation-verify); NOT for the
  concept/demo corpus record format or admission (a2a-training-corpus).
disable-model-invocation: false
user-invocable: false
---

# a2a-protocol — the agent-to-agent wire model

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
4. **Route builds outward**: shaping a server/client → `a2a-agent-design`; proving isolation →
   `a2a-isolation-verify`; payload content questions → the `a2ui-*` siblings.
