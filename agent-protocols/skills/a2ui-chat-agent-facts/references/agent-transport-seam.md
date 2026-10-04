# The AgentTransport isolation seam — backbone vs live overlay, zero-edit swap

> Axis: the ONE interface the live-agent page binds to, its two implementations (the
> deterministic recorded backbone and the dev-only live overlay), and why swapping one for the
> other is a single construction-site edit with a byte-identical browser ingest path. Grounded in
> `packages/agent-ui/a2ui/src/agent/agent-transport.ts`, `site/lib/agent-runtime.ts`,
> `site/lib/live-proxy-transport.ts`, `site/pages/a2ui-live.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R1/R2/R3/R5). ADR-0069 = the demo
> shape + the transport-identical invariant. Verified against source as of 2026-07-07.

## The seam is one method (SPEC-R1 / ADR-0069)

```ts
interface AgentTransport { turn(input: TurnInput): AsyncIterable<string> }
```

One agent turn in, an ordered stream of A2UI JSONL lines out (`agent-transport.ts:67-69`). **Claim
— the page consumes ONLY this.** No `fetch`, proxy URL, or concrete-transport internal may appear
in the page's rendering/round-trip/loop/prompt logic (`agent-transport.ts:61-66`, SPEC-R1 AC1).
**Failure mode:** SPEC-R1 AC1 is a standing grep gate — if the page imports a transport internal
(a `RecordedTransport`/`LiveProxyTransport` concrete or a bare `fetch`), the gate fails. The swap
point is the construction site alone.

## Two implementations behind the one seam

- **The recorded backbone** — `createRecordedTransport()` (`recorded-transport.ts`, via the
  `site/lib/agent-runtime.ts` shim). Replays a committed transcript with **no network, no key**
  (see turn-session-and-input-intent for the transcript). **It is the default the built static
  site runs AND the only shape CI exercises** (SPEC-R2/R3).
- **The live overlay** — `createLiveProxyTransport(selection)` (`live-proxy-transport.ts:37`).
  A real model call through the dev proxy; **dev-only**, reached solely via an
  `import.meta.env.DEV`-guarded dynamic `import()` so `vite build` tree-shakes it out
  (`a2ui-live.ts:286`, SPEC-R9/N2). See switcher-and-live-overlay and
  provider-model-seam-and-trust-boundary.

**Claim — no standing gate (`npm run check`, `npm test`, `npm run test:browser`) may ever invoke
a live model call or require a key** (SPEC-R3). The live overlay is strictly opt-in and dev-only;
a live call is never CI-gated.

## The zero-edit swap, concretely

The page constructs the backbone at module load — `let transport = createRecordedTransport()`
(`a2ui-live.ts:154`) — and later, under the DEV-guarded overlay wiring, reassigns the SAME
variable: `transport = overlay.createLiveProxyTransport(selection)` (`a2ui-live.ts:291`).
Everything downstream reads `transport.turn(input)` (`a2ui-live.ts:200`) with no knowledge of the
origin. **This is the entire swap** — SPEC-R1 AC2's "no other page line changes" proof.

## Transport-identical: one browser ingest path (SPEC-R5 / SPEC-N4 / ADR-0069)

**Claim — the browser transport is IDENTICAL for the recorded and live paths.** Both yield
already-validated A2UI JSONL, one message per line, and the browser ingests them through one code
path: `for await (const line of transport.turn(input)) { … host.ingest(line) }`
(`a2ui-live.ts:200-203`). The live overlay reads the proxy's streamed ndjson and **re-yields it
line by line specifically so the two stream shapes match** (`live-proxy-transport.ts:49-50`,
`54-67`). ADR-0069 pins this as an invariant: the browser transport stays identical between the
recorded backbone and the live overlay. **Why it matters:** validate-then-stream (see produce-loop)
guarantees every emitted line already passed `validateA2ui`, so the page never renders an invalid
partial surface regardless of which transport is live.

## Placement, a node-first package subpath export, `./agent` (ADR-0137)

*(Corrected 2026-10-03: this section previously read "Node-scoped, no package export (SPEC-N1)",
claiming the package surface stays `.`/`./examples`/`./corpus`. That is stale.)* The seam types +
the backbone + the reducer + the producer toolkit live under `packages/agent-ui/a2ui/src/agent/*`
and ship as a package subpath export: `./agent`, plus `./agent/meta-line`, `./agent/genui-line` and
`./agent/agent-transport`. They are NOT on the root barrel. The toolkit is node-first:
`system-prompt.ts` and `mini-skills.ts` `readFileSync` their prompt files at module load, so a
browser bundle does not import the whole toolkit; the transport seam types and the session reducer
are platform-neutral. The key-holding dev proxy and the provider registry stay site-internal
(`tools/agent/*`, ADR-0073 trust boundary) and are not exported. [verified] agent-ui
`a2ui/src/agent/index.ts` header (ADR-0137 cl.1 and cl.4), `a2ui/package.json` exports, 2026-10-03. The browser page reaches it through ONE thin re-export
shim, `site/lib/agent-runtime.ts`, which re-exports only browser-safe, zero-dep material (the
transport types, `createRecordedTransport`, the `session.ts` reducer helpers, the transcript). The
**live overlay is a separate, dev-only import** — never in the shim (`agent-runtime.ts:1-7`).
**Caveat:** the shim re-exports the seam **types**; `A2uiClientMessage` rides the package's public
`@agent-ui/a2ui` surface, and types erase at build, so importing them into the browser adds no
runtime bytes.

## What this file does NOT cover

The `Turn`/`Session`/`TurnInput` shapes + the reducer (turn-session-and-input-intent) · the
`produce()` generate→validate loop that fills the backbone/overlay stream (produce-loop) · the
proxy trust boundary + provider seam behind the live overlay
(provider-model-seam-and-trust-boundary) · the switcher UI + the DEV-guarded wiring
(switcher-and-live-overlay) · the PROPOSED meta-line that would ride this same
`AsyncIterable<string>` without changing the `turn` signature
(conversational-reasoning-and-click-routing-gap).
