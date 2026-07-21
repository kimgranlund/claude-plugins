# Discovery & identity — the AgentCard and the well-known path

Estate paths below are relative to `agent-ui/packages/agent-ui/` (see `sources.md`); HV rows live in
SPEC §2 (`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## What an AgentCard declares

**Required fields at v0.3.0** `[spec — HV-7, [T] AgentCard]`:
`protocolVersion` (the protocol pin, upstream default `"0.3.0"`) · `name` · `description` · `url` ·
`version` · `capabilities` · `defaultInputModes` · `defaultOutputModes` · `skills`.

**Optional fields** `[spec — HV-7]`: `preferredTransport` (default `"JSONRPC"`) ·
`additionalInterfaces` · `securitySchemes` / `security` · `supportsAuthenticatedExtendedCard` ·
`signatures`.

**Two version fields, never conflated** `[spec — HV-7; estate — a2a/src/protocol/types.ts:106,110]`:
`protocolVersion` is the PROTOCOL pin; `version` is the AGENT's own release version. Both are
required; the estate's fixtures carry both and the validator checks both presences independently
(SPEC-R2 reconcile note).

**Capabilities** `[spec — HV-7]`: `{ streaming?, pushNotifications?, stateTransitionHistory?,
extensions? }` — all optional booleans/arrays. The estate types `extensions?` as `unknown[]`
(declared, unconsumed) `[estate — a2a/src/protocol/types.ts:123-128]`.

**Skills** `[spec — HV-11, [T] AgentSkill]`: required `id · name · description · tags: string[]`;
optional `examples? · inputModes? · outputModes? · security?: { [scheme: string]: string[] }[]`
("Security schemes necessary for the agent to leverage this skill."). The `security?` field is the
one addition B0's belief missed `[estate — a2a/src/protocol/types.ts:130-139]`.

## The well-known path

- `https://{server_domain}/.well-known/agent-card.json` — "the recommended location for an agent's
  Agent Card" `[spec §5.3 — HV-7]`. **Renamed from `agent.json` BY v0.3.0** (a listed breaking
  change); the same path holds in v1.0.1 `[spec — HV-7]`.
- Estate constant: `wellKnownAgentCardPath = '/.well-known/agent-card.json'`
  `[estate — a2a/tools/wellknown.ts:10]`. The dev HTTP shell serves it on GET
  `[estate — a2a/tools/http/server.ts:19-24]`.

## Serving a card — validity is a construction-time gate `[estate]`

`serveAgentCard(card)` validates via `validateA2a(…, { expect: 'card' })` and **throws** on any
failure — the ONE deliberate exception to the package's never-throw posture, fail-fast at startup:
"a lying card is worse than no card" `[estate — a2a/tools/wellknown.ts:16-25]`. `serveA2a(core,
card)` therefore refuses to start with an invalid card `[estate — a2a/tools/http/server.ts:16-17]`.
Card validity is never a request-time discovery surprise (LLD-C9).

## Discovering a peer — the client arm `[estate — a2a/tools/wellknown.ts:39-55]`

`discoverAgent(baseUrl, { get? })` fetches `${baseUrl}${wellKnownAgentCardPath}` and returns
`{ ok: true, card } | { ok: false, failures }`. It **never throws**, and a card with failures is
never returned as usable:

| Failure mode | Result |
|---|---|
| fetch throws (network) | `A2A_CARD` at `/`, detail `fetch failed: …` |
| non-200 status | `A2A_CARD` at `/`, detail `unexpected HTTP status N` |
| unparseable / invalid body | the decode's `A2A_SCHEMA`/`A2A_CARD`/`A2A_PIN` failures |

The `get` parameter is an injectable seam so tests stay socket-free (same pattern as the HTTP
transport's `post`) `[estate — a2a/tools/wellknown.ts:1-5]`.

## How a card is validated

`validateA2a` with `expect: 'card'` (auto-detection keys off `protocolVersion` + `url` both being
strings `[estate — a2a/src/protocol/validate.ts:75]`):

- Every missing/mistyped required field → `A2A_CARD` at its JSON-Pointer path (`/name`,
  `/skills/0/id`, …) `[estate — a2a/src/protocol/validate.ts:180-223]`.
- Skills entries checked for required `id/name/description/tags`
  `[estate — a2a/src/protocol/validate.ts:215-223]`.
- Pin: `protocolVersion !== opts.protocolVersion` → `A2A_PIN` at `/protocolVersion`
  `[estate — a2a/src/protocol/validate.ts:255-270]`.

## Selecting an agent from a card

The declared decision surface at v0.3.0 is: the capability flags (`streaming`,
`pushNotifications`), the skills list (with per-skill `inputModes`/`outputModes`), the card-level
`defaultInputModes`/`defaultOutputModes`, and `preferredTransport` `[spec — HV-7]`. Version
compatibility is the pin check: a consumer encountering an unsupported `protocolVersion` MUST fail
coded, never silently proceed (SPEC-R2) — the estate realizes this as `A2A_PIN` with nothing
downstream consuming the artifact `[estate — a2a/src/protocol/validate.ts:255-270]`.

> GAP RESOLVED (spec fetch 2026-07-09 — one trust rung below the HV ledger). **Caching**: v0.3.0
> carries exactly ONE rule — clients retrieving the authenticated extended card SHOULD replace
> their cached public card with it for the duration of the authenticated session
> `[fetch — S §7.10]`; the spec is otherwise **VERIFIED SILENT** on card caching (no TTL,
> invalidation, storage, or conditional-request guidance — sections 5, 5.2, 5.3, 7.10 checked; do
> not assert any). **Selection**: the normative guidance is transport selection, §5.6.3's five
> client rules `[fetch — S §5.6.3]` — parse transports from `url`/`preferredTransport` +
> `additionalInterfaces`; SHOULD use the main `url` when the preferred transport is supported;
> MAY pick any supported transport from `additionalInterfaces` otherwise; SHOULD implement
> fallback on failure; MUST use the URL matching the selected transport.

## Worked example

`card.referee.json` — the arena referee's validator-clean card fixture
`[estate — a2a/src/protocol/fixtures/card.referee.json]`: carries BOTH `protocolVersion: "0.3.0"`
and `version: "1.0.0"`, `capabilities: { streaming: false, pushNotifications: false }`, modes
`["application/json"]`, and one skill. The seat cards (`card.seat-x.json` / `card.seat-o.json`)
are the SPEC-R5 AC1 trio; a standing test re-validates every committed fixture under the pin.
