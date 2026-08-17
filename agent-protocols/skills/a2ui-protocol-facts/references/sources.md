# Sources — provenance for the protocol claims

This pack documents **this repo's implementation** of the A2UI protocol, not a generic tutorial.
Every claim traces to one of two authorities, in trust order. Grounding date: **2026-07-07** (repo
HEAD after the expert-harness wave; ADRs through 0068, protocol/renderer files last touched
2026-07-02..04).

## 1. This repo's source of record (primary — the implementation)

The renderer package **is** the ground truth for how `@agent-ui/a2ui` behaves. Cited by `file:line`.

- **`packages/agent-ui/a2ui/src/protocol.ts`** — the wire contracts (envelopes, `Binding` union,
  `FunctionCall`, `A2uiChildTemplate`, the error types + `toWireError`, `SUPPORTED_VERSIONS`).
- **`packages/agent-ui/a2ui/src/renderer/*.ts`** — the behavior: `dispatch.ts`, `surface.ts`,
  `binding.ts`, `list.ts`, `action.ts`, `input.ts`, `functions.ts`, `interpolate.ts`, `fn-expr.ts`,
  `checks.ts`, `call-function.ts`, `validate.ts`, `tree.ts`, `parser.ts`.
- Co-located `*.test.ts` files pin the behavior each reference asserts.

## 2. This repo's design record (primary — the WHY + the ratified decisions)

The SPEC owns behavior contracts; ADRs record ratified *changes*. Cited by requirement ID / clause.

- **`.claude/docs/specs/specs/a2ui-runtime.spec.md`** — SPEC-R1…R14, SPEC-N1…N6 (the renderer's
  behavior + message contract). The catalog type→widget mapping is owned by `a2ui-catalog.spec.md`
  (out of this pack's scope).
- **ADRs** (`.claude/docs/adr/`): **0024** (positional dynamic lists, no key; + write-side / subtree /
  per-item-listener amendments) · **0026** (`{call,args}` binding kind + `@index`) · **0027/0028**
  (`${…}` DynamicString interpolation + function-expression grammar) · **0029** (`checks` inline
  validation) · **0031** (error-vocab reconciliation → the two-code wire map) · **0034** (agent-
  initiated `callRendererFunction` RPC + the `callableFrom` hard-floor amendment) · **0011** (action-prop
  shape) · **0019/0053** (the input `value` mark + catalog naming law).

## Terminology note — A2UI v1.0 Candidate rename (2026-08-17, issue #482)

This pack's taught vocabulary was swept to A2UI v1.0 Candidate terminology: the protocol's role
names **client → renderer** and **server → agent** throughout prose; the RPC kind **`callFunction`
→ `callRendererFunction`** (this pack documents only the agent-initiates/renderer-executes
direction — the Candidate spec's mirror `callAgentFunction`/`agentFunctionResponse`, for a
renderer-initiated call executing on the agent, is a new capability not yet covered here); the
reply key **`functionResponse` → `rendererFunctionResponse`**; and the `callableFrom` enum
**`clientOnly`/`remoteOnly`/`clientOrRemote` → `rendererOnly`/`agentOnly`/`rendererOrAgent`**. This
mirrors adiahealth/gen-ui-kit's own in-repo Candidate-terms sweep (issue #1354, PR #1472 — open/
review-pending as of this writing, not yet merged). **Caveat this creates:** every `file:line`
citation in this pack still names the repo's ACTUAL (pre-Candidate) TypeScript identifiers and
JSON field names — `handleCallFunction`, `call-function.ts`, `catalog.ts:182-185`'s literal
`clientOnly` default, etc. — because those identifiers have not themselves been renamed in the
cited source yet (gen-ui-kit's own code-level sweep is the unmerged PR above). Read this pack's
prose in Candidate vocabulary; read a cited `file:line`'s literal contents in whatever vocabulary
the source currently uses, and re-verify before acting on it (see "Verifying a claim" below) — this
is the same drift this pack's re-sync duty already anticipates, now with a named cause. The two
other Candidate changes named in issue #482 — catalog resolution moving to STRICT (no silent
fallback) and `ValidationResult` gaining severity levels — have no existing pre-Candidate claim
anywhere in this pack to correct (grepped, none found); adding them would be new, ungrounded
protocol-behavior claims, not a terminology rename, so they are deliberately OUT of this sweep's
scope pending a real research wave (`/make-pack`) grounded in the actual spec text.

## 3. The external protocol (authority for "the spec requires X" vs "this repo chose Y")

- **A2UI v1.0 — Google, Apache-2.0, [a2ui.org/specification/v1.0-a2ui/](https://a2ui.org)** (+ the
  data-binding / functions / expression concept pages). This repo conforms to v1.0 (Constraint C1;
  v0.9.1 also supported via the version pin). The pack reaches the external spec's exact wording
  **through the ADRs**, which host-verified verbatim quotes from a2ui.org at authoring time and
  attribute them explicitly (e.g. ADR-0031 fact 1 on the two-code wire contract; ADR-0034 facts 1-6
  on `callRendererFunction`; ADR-0024 on positional matching; ADR-0026 fact 4 on `@index` innermost-only).
  When a reference says "verbatim from a2ui.org," the quote lives in the cited ADR.

**Where the spec-vs-repo line falls (worth stating once):** v1.0 governs **only the wire** — the
message envelopes, the two-code error contract, positional list matching, `@index` semantics, the
`callableFrom` default. The repo **chose** everything internal: the 8-code diagnostic taxonomy, the
signals-based per-path reactive resolver, the bespoke positional reconcile (vehicle B2 over `repeat`),
`setPointer`'s structural sharing, the single shared validator. A "does the protocol require this"
question turns on that line — if it's a wire fact, it's in an ADR quoting a2ui.org; if it's a
mechanism, it's a repo design decision recorded in an ADR's Decision/Alternatives.

## Verifying a claim (do this before recommending an action on it)

A claim naming a `file:line` or an ADR clause was true at the grounding date above. Before acting on
it: for a `file:line`, open the file (line numbers drift as the renderer evolves — grep the symbol);
for an ADR clause, confirm the clause still says what the reference claims. A superseded ADR or a
renamed symbol makes a citation stale — fix it here, don't step over it (this pack's re-sync duty).

## Out of scope — routed to sibling owners

Catalog authoring / coverage policy / type→widget resolution → the **`a2ui-catalog-facts`** pack
(live; over `a2ui-catalog.spec.md` + the a2ui-builder seat) · the live agent's session/turn/provider
model → the **`a2ui-chat-agent-facts`** pack (live; over `a2ui-live-agent.spec.md`) · corpus
record format / admission / retrieval → the **`a2ui-training-facts`** pack (live; over
`a2ui-training-facts.spec.md`) · transport interop (AG-UI/A2A/MCP) →
`a2ui-streaming-pipeline.spec.md` (mostly unbuilt, ADR-0067).
