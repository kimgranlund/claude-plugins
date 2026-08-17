# Sources — provenance for the live-agent claims

Every claim in this pack is grounded in THIS repo (`/Users/kimba/Projects/nonoun/agent-ui`), not a
generic tutorial. The pack documents `@agent-ui/a2ui`'s actual live-agent implementation as of
2026-07-07. In trust order:

## Ground truth — the shipped source (highest trust)

The code IS the contract; when a doc and the source disagree, the source wins and the doc is
repaired.

- **`packages/agent-ui/a2ui/tools/agent/`** — the Node-scoped live-agent harness:
  `agent-transport.ts` (the seam + `Turn`/`Session`/`TurnInput`/`AgentProvider`),
  `session.ts` (the pure reducer + framing), `produce.ts` (the bounded loop),
  `system-prompt.ts` (the drift-gated derived prompt), `providers-config.ts` (`resolvePair` — the
  trust boundary), `providers.json` (the registry), `dev-proxy-plugin.ts` (the dev-only proxy),
  `transcript.ts` (the recorded backbone data), `providers/anthropic.ts` (the implemented
  `AgentProvider` adapter — the SSE wire contract, `parseAnthropicSSE`/`splitFrames` — see
  anthropic-sse-wire-contract).
- **`packages/agent-ui/a2ui/src/live-agent/anthropic-sse.test.ts`** — the fixture suite proving
  `parseAnthropicSSE` (SPEC-R11 AC3); the anthropic-sse-wire-contract axis's non-network ground
  truth.
- **`site/`** — the browser side: `lib/agent-runtime.ts` (the re-export shim),
  `lib/live-proxy-transport.ts` (the dev-only overlay transport),
  `lib/provider-switcher.ts` (the in-chat switcher), `pages/a2ui-live.ts` (the demo page —
  `handleClientMessage`, `runTurn`, `summarize`, `wireLiveOverlay`).
- **`packages/agent-ui/a2ui/src/renderer/`** — the wire-side reads the page depends on:
  `action.ts` (`emitAction`, `wantResponse` stamping + RPC correlation), `dispatch.ts` (the
  version-gate discriminator), `renderer.ts` (`readActionSpec` reading `wantResponse`).
- **`packages/agent-ui/a2ui/src/examples/canvas-button.ts`** — the committed seed proving the
  no-`wantResponse` baseline.

## The behavior contract (SPEC) — normative requirements

- **`.claude/docs/specs/specs/a2ui-live-agent.spec.md`** (accepted, v0.1, 2026-07-04) — the
  authoritative requirement IDs this pack cites: SPEC-R1 (transport isolation), R2/R3 (backbone +
  secret-free CI), R4 (bounded loop), R5 (validate-then-stream), R6 (derived prompt), R7
  (retrieval), R8 (multi-turn round-trip), R9 (dev-only overlay), R10 (site page), R11 (provider
  seam), R12 (switcher + allowlist), N1–N5 (zero-dep, the `VITE_` footgun, validator parity,
  progressive paint, per-provider isolation).

## The decision records (ADR) — ratified changes + one proposal

- **ADR-0069** (demo shape + the `AgentTransport` seam + the transport-identical invariant) ·
  **ADR-0070** (runtime loop scope — deterministic gate only, validate-then-stream) ·
  **ADR-0071** (the derived, drift-gated system prompt) · **ADR-0072** (the multi-turn session
  model + stateless proxy) · **ADR-0073** (the model-provider seam + the trust boundary) —
  all accepted (ratified 2026-07-04, per the SPEC header).
- **ADR-0011** (the canonical `action` prop shape — the origin of `wantResponse`) — accepted.
- **ADR-0088** (`0088-a2ui-live-conversational-channel.md`) — the note channel + decision-trace +
  `wantResponse` routing. **`Status: proposed` (2026-07-07), NOT built, NOT ratified** — a design
  record only; see conversational-reasoning-and-click-routing-gap for the shipped/proposed split.

## Terminology note — A2UI v1.0 Candidate rename (2026-08-17, issue #482)

This pack's own narrative (SKILL.md, this file) uses A2UI v1.0 Candidate's protocol role names:
**client → renderer**, **server → agent**. Mirrors adiahealth/gen-ui-kit's own in-repo sweep
(issue #1354, PR #1472 — open/review-pending, not yet merged). Two things this sweep deliberately
did NOT touch:

1. **This repo's literal TypeScript identifiers** — `A2uiClientMessage`, `A2uiServerMessage`,
   `handleClientMessage`, `frameClientMessage`, the `kind: "client"` discriminant
   (`turn-session-and-input-intent.md`), and `handleClientMessage`/`runTurn`/`summarize`/
   `wireLiveOverlay` above — because those names have not themselves been renamed in the cited
   source (gen-ui-kit's own code-level sweep is the unmerged PR above); inventing a rename in the
   citation text would misrepresent what the file actually contains.
2. **The dev-proxy's OWN "client"/"server" vocabulary** (`provider-model-seam-and-trust-boundary.md`,
   `produce-loop.md`'s `input.model` precedence claim) — that is plain HTTP client/server language
   for the Vite dev-proxy's backend process and the request body it receives, a different system
   layer entirely (it would exist with or without A2UI), not the A2UI protocol's role vocabulary —
   so it is out of scope for this rename and left as written.

## Boundary — layers owned elsewhere

This pack answers the live-agent system; it does not restate its neighbors. The A2UI wire shape
(`action`/`wantResponse`/error codes) is [[a2ui-protocol-facts]]; catalog design + the derived prompt's
component authority is [[a2ui-catalog-facts]]; the corpus + `retrieve()` internals the loop CALLS
is [[a2ui-training-facts]]. A claim here that drifts from those owners is a bug to fix HERE — they
own their layers; this pack owns how the live agent composes them.
