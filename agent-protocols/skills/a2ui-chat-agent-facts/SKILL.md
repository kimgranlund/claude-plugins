---
name: a2ui-chat-agent-facts
description: >-
  The A2UI LIVE-AGENT in @agent-ui/a2ui — a real LLM emitting A2UI. Use for "swap
  recorded → live transport", "how does a UI click become a chat turn", "wire a new provider / add a model",
  "the produce() self-correct loop", "what is validate-then-stream", "the dev-proxy / PAIR
  trust boundary", "why can't the agent explain its choice". Covers the AgentTransport seam,
  Turn/Session + reducer, the provider seam + dev-proxy, the Anthropic SSE contract, the
  conversational channel (ADR-0088). ANSWERS; does not build. NOT for the wire shape/renderer
  (a2ui-protocol-facts), catalog design (a2ui-catalog-facts), corpus records
  (a2ui-training-facts), or live-agent SOURCE (a2ui-builder).
disable-model-invocation: false
user-invocable: false
---

# a2ui-chat-agent-facts — the live-agent world model

Answers how `@agent-ui/a2ui`'s live-agent demo works: a real LLM prompted → a validated A2UI stream
→ a rendered surface → the human interacts → renderer messages return → the agent continues. It
documents THIS repo's shipped implementation (as of 2026-07-07), not a generic tutorial — every
claim cites its source file:line or an ADR/SPEC clause.

> **UPDATE 2026-07-08.** The ADR-0088 family (0088/0089/0090/0091/0097 — note channel, asks, mode
> axis, mini-skills, feed asks) shipped, and the gap axis was rewritten as shipped-system
> documentation (`references/conversational-reasoning-and-click-routing-gap.md`).

| Ask | Load |
|---|---|
| Transport swap — "how does recorded↔live work?", "the zero-edit seam", "what does CI run?" | `references/agent-transport-seam.md` |
| Turn model — "how does a click become a turn?", "intent vs renderer turn (code: 'client')", "the reducer", "the agent continues" | `references/turn-session-and-input-intent.md` |
| The runtime loop — "the produce() self-correct loop", "validate-then-stream", "how is the prompt built?", "halt-and-report" | `references/produce-loop.md` |
| Providers & keys — "wire a new provider", "add a model", "where's the key?", "is it safe?", "the trust boundary", "the VITE_ footgun" | `references/provider-model-seam-and-trust-boundary.md` |
| The Anthropic SSE wire contract — "why did my SSE parsing break", "what's the exact event sequence", "why is text getting dropped mid-stream", "the buffering assumption", "the error sentinel" | `references/anthropic-sse-wire-contract.md` |
| The switcher & overlay — "the in-chat provider/model picker", "how the live overlay is wired dev-only" | `references/switcher-and-live-overlay.md` |
| The conversational channel & asks — "the note beside the stream", "clarify/boundary asks", "the mode axis", "mini-skills", "wantResponse routing" (ADR-0088..0091/0097), the meta-line's SIX reserved arms (ask/plan/personaPatch/flowEnd/team/target — ADR-0174/0178/0198/0204/0206) + flow-completion conduct | `references/conversational-reasoning-and-click-routing-gap.md` |
| Provenance — where a claim comes from | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`wantResponse`, `resolvePair`, `produce`, `AgentTransport`, …) and Read that section — the
   files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its cited source (file:line or ADR/SPEC clause)
   + the failure mode or caveat**. A live-agent claim without its caveat is half an answer.
   *(The pre-2026-07-08 worked example here — the wantResponse fork "awaiting Kim's ruling" — is
   retired: ADR-0088 was ratified and built; re-derive the current routing from `a2ui-live.ts` +
   the accepted ADR before answering.)*
3. **Distinguish SHIPPED from PROPOSED — and check the Status cell, don't trust this pack's
   snapshot.** All seven axes document accepted, built behavior; when an ADR's Status cell and an
   axis body disagree, the shipped sources outrank both (e.g. ADR-0091 is built and gated while its
   cell still reads `proposed`).
4. Route output work at the boundary (see below) — this pack answers; it does not build.

**Done when** the answer carries the claim + its cited `file:line`/ADR/SPEC clause + the caveat,
and any make/build/ratify ask is routed to its owning agent. **NOT done** while a claim ships
without its caveat, a SHIPPED and a PROPOSED behavior read alike, or a making-ask is answered with
content instead of a routed peer.

## Deviation doctrine

Every default in this system carries a rationale, so the consumer knows when deviating is legal —
answer with the *why*, not just the rule:

- **The recorded backbone is the default and the only CI-exercised path** *because* a live call
  cannot be a standing gate (non-deterministic, key-requiring) — SPEC-R3. Deviating (a live gate)
  breaks that invariant; don't.
- **The routing default is opt-out** *because* the committed seed + corpus set no `wantResponse`
  (`canvas-button.ts:27`) — opt-in is a legal deviation only if you also re-seed transcript +
  corpus + prompt (the open fork).
- **Prose rides BESIDE the A2UI stream, never inside an A2UI stream message** *because* the shared
  validator + judged corpus demand wire purity (SPEC-N3 / ADR-0070 clause 3). A "just add a Text
  component with the explanation" shortcut violates it.
- **The key is read server-side, non-`VITE_`-prefixed** *because* Vite inlines `VITE_*` into the
  static build (SPEC-N2). Any deviation that reaches for `import.meta.env.VITE_*` must live only in
  a dev-only-guarded, tree-shaken overlay module.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build/fix live-agent, renderer, or catalog SOURCE** (the transport, the `produce()` loop, the
  proxy, a new provider adapter) → the **`a2ui-builder`** agent.
- **Compose an actual A2UI payload** (message stream / node shapes, e.g. one that sets
  `wantResponse`) → the **`a2ui-composer`** agent.
- **Author or revise ADR-0088 (or any ADR/SPEC/LLD in this space)** → **`planner`** (via
  docs' `make-doc`, where installed). Grading or ratifying a design doc routes
  there too, not here.
- **Sibling knowledge packs** (answers, like this one): the A2UI wire shape + renderer mechanics →
  [[a2ui-protocol-facts]]; catalog design + coverage → [[a2ui-catalog-facts]]; the corpus records +
  `retrieve()` internals → [[a2ui-training-facts]]. **This pack is a CALLER of `retrieve()`, not
  an owner of retrieval internals** — a "how is the shard scored/admitted" question is
  a2ui-training-facts's, not this pack's.

## Extending this pack

Extension: governed by [[make-pack]]
