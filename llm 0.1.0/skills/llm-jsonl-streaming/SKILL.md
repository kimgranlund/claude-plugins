---
name: llm-jsonl-streaming
description: >-
  Streaming structured output from an LLM safely — project-agnostic. Use for "parse a chunked SSE
  stream correctly", "why my SSE parser drops or duplicates text", "the Anthropic Messages API's
  exact streaming event contract", "stream JSON output without rendering an invalid partial",
  "what is validate-then-stream", "bound a self-correct retry loop against invalid model output",
  "signal a mid-stream error without throwing inside a generator", "is an empty model response the
  same as an invalid one". Covers SSE chunk-buffering (partial-frame handling, event-boundary
  framing), the Anthropic SSE contract as a worked instance, an error-sentinel technique, and
  validate-then-stream (bounded self-correct, halt-and-report). Grounded in the SSE spec, Anthropic's
  docs, and a shipped example. ANSWERS from a cited corpus; does not build. NOT for the
  provider/trust-boundary/session pattern this sits behind (llm-provider-gateway); NOT for the
  A2UI wire MESSAGE shape (agentic-ui); NOT for a vendor's contract beyond Anthropic.
disable-model-invocation: false
user-invocable: false
---

# llm-jsonl-streaming — streaming structured output safely

Answers how to consume a chunked LLM response stream correctly, and how to turn a model's raw
text output into structured (JSONL, one-object-per-line) data without ever handing a caller a
partial or invalid record. Two distinct layers, often confused: **transport framing** (how do I
even get whole events out of a chunked byte stream — SSE's job) and **content validity** (given
the accumulated text, is it a well-formed structured record yet, and what do I do if the model
got it wrong — validate-then-stream's job). This pack is grounded in the platform SSE spec +
Anthropic's public API contract (facts, verify against current docs if stale-sensitive) and a
real worked instance (`@agent-ui/a2ui`'s live-agent system) cited as proof of the pattern working,
not as the only valid implementation.

| Ask | Load |
|---|---|
| The chunk-buffering technique — "my SSE parser drops text", "how do I handle a frame split across two reads", "the blank-line event boundary" | `references/sse-chunk-parsing-technique.md` |
| The Anthropic contract, worked — "what's the exact event sequence", "message_start/content_block_delta/...", "the error-sentinel technique" | `references/anthropic-sse-worked-example.md` |
| Validate-then-stream — "never emit invalid structured output", "the self-correct retry loop", "halt-and-report", "feed failures back to the model" | `references/validate-then-stream-self-correct.md` |
| Provenance — spec/vendor-doc fact vs worked-example source | `references/sources.md` |

## Consult procedure

1. Classify the ask by axis, then **Grep the matching file for the term first** (`content_block_delta`,
   `ANTHROPIC_SSE_ERROR_PREFIX`, `maxRounds`, `ProduceHalt`, …) and Read that section — the files
   are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its grounding (the SSE/HTTP spec, the vendor's
   published API docs, or the worked example's `file:line`) + the failure mode it prevents**. A
   streaming-technique claim without the failure mode is half an answer — every technique here
   exists because of something that goes silently wrong without it.
3. **Distinguish the transport layer (SSE framing — any vendor using SSE shares this) from the
   content layer (validate-then-stream — applies to structured output over ANY transport, SSE or
   otherwise).** A question about "why is text getting dropped" is almost always transport-layer;
   a question about "why did an invalid surface render" is almost always content-layer.
4. Route output work at the boundary (see below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its grounding + the failure mode/caveat, and any
build ask is routed to the consumer's own build seat. **NOT done** while a claim ships without
the failure mode it prevents, or a vendor-specific detail (Anthropic's exact event names) is
presented as if every SSE-streaming vendor shares it verbatim.

## The core invariants (why these patterns exist)

- **A chunk boundary is not an event boundary** — nothing about a `ReadableStream`'s chunking
  guarantees one network `read()` lands on a whole SSE frame; a parser that assumes otherwise will
  intermittently corrupt or drop text, and the bug will be nearly impossible to reproduce because
  it depends on network-level chunking that varies run to run.
- **An error mid-stream must be observable without forcing every caller into try/catch** — a
  sentinel VALUE through the same iterable contract a normal fragment rides is cheaper and safer
  than an exception that has to unwind through a generator's consumers.
- **Nothing invalid should ever be handed downstream, no matter how the model misbehaves** — a
  structured-output stream (JSONL or otherwise) that CAN emit a syntactically-broken or
  schema-invalid record puts the burden of defending against that on every consumer, forever;
  validating BEFORE the first byte streams down puts the burden in exactly one place, once.
- **A retry loop must be bounded and must report cleanly on exhaustion** — an unbounded
  self-correct loop against a model that never gets it right is an outage waiting to happen; a
  bounded loop that raises a distinguishable, structured failure (not a raw exception, not a
  silently-empty response) is what lets a caller show something reasonable to a user.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Implement an SSE parser, a validate-then-stream loop, or a specific vendor's adapter in YOUR
  project** → your project's own build seat/agent (this pack teaches the technique, it owns no
  codebase's source).
- **The provider-adapter seam this streaming logic lives BEHIND, the secret trust boundary, the
  registry, or the conversation/session model** → [[llm-provider-gateway]] (the sibling pack in
  this plugin).
- **The A2UI wire MESSAGE shape** (what a `createSurface`/`updateComponents` line actually
  contains, as opposed to how the bytes carrying it were streamed) → the `agentic-ui` plugin's
  `a2ui-protocol` pack; that repo's own produce-loop implementation, documented as a dated,
  exhaustive answer about THAT system → `a2ui-conversational-agent`'s `produce-loop.md` and
  `anthropic-sse-wire-contract.md`.

## Extending this pack

A missing axis (a second vendor's SSE contract fully worked through, a non-SSE streaming
transport), a stale spec/vendor-doc citation, or a second worked example from a different
codebase — route to `knowledge-forge` where installed; otherwise apply its discipline inline: one
reference per distinct class of ask, every claim grounded, never an uncited file bolted on.
