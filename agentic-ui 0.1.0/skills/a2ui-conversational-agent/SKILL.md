---
name: a2ui-conversational-agent
description: >-
  Explains the A2UI LIVE-AGENT system in @agent-ui/a2ui — a real LLM emitting A2UI over the wire.
  Use for "how does the transport swap from recorded to live work", "how does a UI click become a
  chat turn", "wire a new LLM provider / add a model", "where does the API key live / is it safe",
  "why can't the agent explain why it chose X not Y", "what is the produce() self-correct loop",
  "how is the system prompt built", "what does the provider switcher do", "why did every click
  trigger a turn". Covers the AgentTransport isolation seam (backbone vs dev-only live overlay,
  zero-edit swap), the Turn/Session/TurnInput model + the pure reducer (intent vs client turns),
  the bounded generate→heal→validate→self-correct produce() loop + the catalog-derived drift-gated
  prompt, the multi-provider seam (AgentProvider, providers.json, the dev-proxy trust boundary, the
  PAIR-allowlist, the VITE_ footgun), the in-chat switcher, and the OPEN gap (ADR-0088, proposed):
  no natural-language note channel yet, wantResponse wired but unused for click routing. ANSWERS
  from a cited repo corpus; it does not build. NOT for the A2UI wire shape / renderer mechanics
  (a2ui-protocol); NOT for catalog design or coverage (a2ui-catalog-design); NOT for corpus records
  / retrieve() internals (a2ui-training-corpus — this layer CALLS it); NOT for composing a payload
  (the a2ui-composer agent); NOT for writing live-agent/renderer/catalog SOURCE (the a2ui-builder
  agent); NOT for authoring the ADRs/SPEC (system-planner).
disable-model-invocation: false
user-invocable: false
---

# a2ui-conversational-agent — the live-agent world model

Answers how `@agent-ui/a2ui`'s live-agent demo works: a real LLM prompted → a validated A2UI stream
→ a rendered surface → the human interacts → client messages return → the agent continues. It
documents THIS repo's shipped implementation (as of 2026-07-07), not a generic tutorial — every
claim cites its source file:line or an ADR/SPEC clause.

| Ask | Load |
|---|---|
| Transport swap — "how does recorded↔live work?", "the zero-edit seam", "what does CI run?" | `references/agent-transport-seam.md` |
| Turn model — "how does a click become a turn?", "intent vs client turn", "the reducer", "the agent continues" | `references/turn-session-and-input-intent.md` |
| The runtime loop — "the produce() self-correct loop", "validate-then-stream", "how is the prompt built?", "halt-and-report" | `references/produce-loop.md` |
| Providers & keys — "wire a new provider", "add a model", "where's the key?", "is it safe?", "the trust boundary", "the VITE_ footgun" | `references/provider-model-seam-and-trust-boundary.md` |
| The switcher & overlay — "the in-chat provider/model picker", "how the live overlay is wired dev-only" | `references/switcher-and-live-overlay.md` |
| The open gap — "why can't the agent explain itself?", "why did every click talk back?", "the note channel / wantResponse routing (ADR-0088)" | `references/conversational-reasoning-and-click-routing-gap.md` |
| Provenance — where a claim comes from | `references/sources.md` |

## Consult procedure

1. Classify the ask against the table above, then **Grep the matching file for the term first**
   (`wantResponse`, `resolvePair`, `produce`, `AgentTransport`, …) and Read that section — the
   files are cited catalogs, not linear reads.
2. Answer on the **answer contract**: the **claim + its cited source (file:line or ADR/SPEC clause)
   + the failure mode or caveat**. A live-agent claim without its caveat is half an answer. Worked
   shape:
   > *"Can I make a slider drag not spam the agent with turns?"* → open-gap ask →
   > **Claim (PROPOSED, ADR-0088 part 3):** route `handleClientMessage` on the action's
   > `wantResponse` — `false` → silent apply, `true`/absent → a turn. **Cited:** shipped today every
   > client message turns unconditionally (`a2ui-live.ts:224-229`); the routing is `Status: proposed`,
   > not built. **Caveat:** the default must be opt-out because the committed seed sets no
   > `wantResponse` (`canvas-button.ts:27`), so "absent ⇒ silent" would regress the demo — and this
   > is the one fork awaiting Kim's ruling.
3. **Distinguish SHIPPED from PROPOSED.** The transport/turn/loop/provider/switcher axes document
   accepted, built behavior. The open-gap axis is ADR-0088 (`proposed`, unbuilt, unratified) — flag
   it as a design record; never grant it authority it does not have.
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
- **Prose rides BESIDE the A2UI stream, never inside a server message** *because* the shared
  validator + judged corpus demand wire purity (SPEC-N3 / ADR-0070 clause 3). A "just add a Text
  component with the explanation" shortcut violates it.
- **The key is read server-side, non-`VITE_`-prefixed** *because* Vite inlines `VITE_*` into the
  static build (SPEC-N2). Any deviation that reaches for `import.meta.env.VITE_*` must live only in
  a dev-only-guarded, tree-shaken overlay module.

## Boundaries — this pack ANSWERS; it routes ALL making

- **Build/fix live-agent, renderer, or catalog SOURCE** (the transport, the `produce()` loop, the
  proxy, a new provider adapter) → the **[[a2ui-builder]]** agent.
- **Compose an actual A2UI payload** (message stream / node shapes, e.g. one that sets
  `wantResponse`) → the **[[a2ui-composer]]** agent.
- **Author or revise ADR-0088 (or any ADR/SPEC/LLD in this space)** → **[[system-planner]]** (via
  [[adr-author]] / [[spec-author]] / [[lld-author]]). Grading or ratifying a design doc routes
  there too, not here.
- **Sibling knowledge packs** (answers, like this one): the A2UI wire shape + renderer mechanics →
  [[a2ui-protocol]]; catalog design + coverage → [[a2ui-catalog-design]]; the corpus records +
  `retrieve()` internals → [[a2ui-training-corpus]]. **This pack is a CALLER of `retrieve()`, not
  an owner of retrieval internals** — a "how is the shard scored/admitted" question is
  a2ui-training-corpus's, not this pack's.

## Extending this pack

A missing axis, a stale reference (a canon ADR/SPEC moved, or ADR-0088 flips to `accepted`/built),
or "add X to this pack" is authoring work — route to [[knowledge-author]] (axis decomposition,
grounded research waves, index discipline). Never bolt an uncited file onto the corpus inline. The
pack's routing corpus of record lives at `scripts/routing-corpus.json`.
