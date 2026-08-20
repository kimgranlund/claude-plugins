---
name: data-wiring-facts
description: >-
  Answers how declarative data actually gets WIRED into a UI, from a cited field-report corpus —
  the 3-tier streaming stack (attribute-driven transport, refcounted shared signal, one-way bridge)
  and its double-ownership hazard, the postMessage bridge protocol and its
  every-busy-flag-needs-a-reset-path rule, the no-DI four-substitute taxonomy (typed handles,
  re-derive helpers, callback injection, documented soft globals), and the six-pattern
  need→pattern menu + Wiring Record gates. Use for "should this element use data-stream-* or its
  own fetch", "is mixing an imperative
  fetch with a declarative stream a bug", "does this busy flag have a guaranteed reset path",
  "what's our pattern for passing this dependency down without a DI container", "which of the six
  wiring patterns fits this need", "what counts as a done Wiring Record row". ANSWERS data-WIRING
  facts; NOT reactivity MECHANISM (reactivity-facts), NOT app-tier state ARCHITECTURE judgment
  (state-model-rules), NOT client-PERSISTENCE (persistence-facts).
user-invocable: false
disable-model-invocation: false
---

# data-wiring-facts — the data-wiring world model

Answers how data actually gets wired into a UI — the transport/signal/bridge stack a live element
sits on top of, the postMessage protocol a sandboxed bridge speaks, the substitutes a framework
with no DI container reaches for, and the ratified need→pattern menu that picks among them — from
a corpus grounded in real field reports across four repos (gen-ui-kit, ultimate-tokens, adia-v2,
agent-ui), not general data-fetching-library folklore.

| Ask | Load |
|---|---|
| Attribute-driven transport → refcounted signal → one-way bridge; mixing an imperative fetch with a managed stream | `references/streaming-stack.md` |
| A sandboxed/iframe bridge's request/reply shape; does this busy flag always reset | `references/bridge-protocol.md` |
| No DI container here — what's the sanctioned substitute for passing a dependency down | `references/no-di-taxonomy.md` |
| Which of the six wiring patterns fits this need; what a done Wiring Record row requires | `references/wiring-menu.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask against the four axes above; load only the matching reference (or
   `sources.md` for provenance). Hunting one specific claim inside a file: Grep for the term first
   rather than reading the whole file.
2. Answer on the contract: **claim + cited file:line/report + the grounding marker
   ([verified]/[incident])**. Worked shape:
   > *"Our Cleanup panel's Scan/Delete buttons are stuck disabled — the busy flag never cleared."*
   → bridge-protocol ask → `bridge-protocol.md` — the bridge's own `apply` request has a
   guaranteed-reply carve-out in its sandbox-side catch block, but `sweep-scan`/`sweep-delete`
   don't: a throw in the sandbox handler leaves `sweepBusy=true` with no reply ever posted, wedging
   the buttons for the rest of the session — a real, confirmed incident, not a hypothetical
   [incident].
3. State which axis the answer draws from, and its grounding marker — never present a corpus
   citation as live-verified-today code if `sources.md`'s own disclosure says otherwise.
4. Route reactivity-mechanism, architecture-judgment, or persistence work at the boundary
   (below) — this pack answers data-wiring facts, it never explains a reactivity kernel, judges
   whether a store is architecturally coherent, or rules on what gets written to storage.

## Boundaries

- **This skill answers data-WIRING facts — how data gets connected to a UI element or across a
  bridge; it does not explain reactivity MECHANISM.** "Why did this effect refire twice", "computed
  vs signal vs effect", "guard a stale async response" are `reactivity-facts`' law — that pack
  explains the kernel that decides WHEN a write fires; this pack explains what gets CONNECTED and
  how. A question naming a kernel primitive (signal/computed/effect/scope/sequence token) is
  `reactivity-facts`'; a question naming a stream, a bridge message, a DI substitute, or a wiring
  pattern is this pack's.
- **This skill does not judge app-tier state ARCHITECTURE generally.** "Why is our state a mix of
  implementations", "is this store actually used or just built", "two places both claim to own
  this field" are `state-model-rules`' law — that pack judges whether a store/layer/convention is
  architecturally coherent over time; this pack answers whether one specific wiring choice (a
  stream, a bridge message, a DI substitute) is disciplined right now. A question naming stacked
  generations or a whole app's drift is `state-model-rules`'; a question naming one wiring decision
  is this pack's.
- **Client-persistence facts — storage discipline tiers, dual sync/async persistence contracts,
  the storage-specific bypass-inventory shape, URL-state sync — belong to `persistence-facts`.**
  What gets WRITTEN to storage and when that's disciplined is that pack's law, unrelated to how
  data gets wired INTO a live element or across a bridge in the first place. A question naming a
  storage key, schemaVersion, or URL param is `persistence-facts`'; a question naming a stream,
  bridge, or DI substitute is this pack's.
- **UI pattern naming and the screen-state grammar** (loading/empty/error) stay
  `ui-pattern-facts`' law — unrelated territory.
- **Production streaming/bridge code, a DI substitute module, or a wiring implementation from
  scratch** → no owning builder skill in this plugin (the same gap `reactivity-facts` and
  `state-model-rules` name for their own territory) — derive the implementation inline against
  whichever axis file names the pattern or failure mode to follow, rather than treating this pack
  as a builder.

## Extending this pack

Extension: governed by [[make-pack]]
