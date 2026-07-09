# Extensions & bridging — carrying a payload protocol over A2A

> **GAP LARGELY RESOLVED (spec fetch 2026-07-09, `[fetch — S §5.5.2.1]` + `[fetch — S1 §4.4.4,
> §4.6.3]` — one trust rung below the HV ledger):** at the estate's pin **v0.3.0, the
> AgentExtension object is `name` + `description` + `documentation` — there is NO `required`
> field, no activation handshake, and no unsupported-extension mandate** (VERIFIED at §5.5.2.1;
> required-extension semantics simply don't exist at this pin — don't assert them). v1.0.1
> reshapes it to `uri` (globally unique) + `description` + `required` (boolean), and §4.6.3 adds
> the one normative rule: an agent SHOULD ignore an unsupported extension request **unless marked
> required — then return an error**. Honest residual: v1.0.1's activation mechanism (header or
> otherwise) was not retrievable this fetch — still open, now narrowly.

Estate paths relative to `agent-ui/packages/agent-ui/`; HV rows live in SPEC §2
(`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## The extension surface that IS grounded

- `AgentCard.capabilities.extensions?` exists at v0.3.0 `[spec — HV-7, [T] AgentCapabilities]`
  (estate types it `unknown[]`, declared-unconsumed `[estate — a2a/src/protocol/types.ts:127]`).
- `Message.extensions?: string[]` and `Artifact.extensions?: string[]` exist
  `[spec — HV-4/HV-11; estate — a2a/src/protocol/types.ts:37,100]` — extension URIs ride
  per-message/per-artifact.
- The A2UI extension is identified by a **URI** and binds via message **metadata** + tagged
  DataParts `[spec — HV-8]` (details next). v0.3.0's seven A2A error codes include NO
  extension-specific code; `-32008 ExtensionSupportRequiredError` appears only at v1.0
  `[spec — HV-9]`.

## The worked exemplar — A2UI over A2A

Bridge module: `a2ui/tools/pipeline/transports/a2a.ts` (pure + browser-safe; type-only imports
both ways, zero runtime deps; never exported from either package barrel)
`[estate — a2ui/tools/pipeline/transports/a2a.ts:1-17]`. Verified facts:

- Extension URI: `https://a2ui.org/a2a-extension/a2ui/v1.0` `[spec — HV-8; estate — a2a.ts:21]`;
  DataPart tag `A2UI_MIME = 'application/a2ui+json'` at `metadata.mimeType` `[estate — a2a.ts:20,37]`.
- **One A2UI envelope per tagged DataPart** — "Each A2UI envelope (e.g., `updateComponents`)
  corresponds to the payload of a single A2A message Part." `[spec — HV-8]`; never batched into
  one part, never split across parts `[estate — a2a.ts:36-38,59-71]`.
- Capabilities: "The `a2uiClientCapabilities` object is placed in the `metadata` field of **every**
  A2A `Message` sent from the client to the server" `[spec — HV-8]`, value **version-keyed**
  `"v1.0": { supportedCatalogIds: string[] }` (required; `inlineCatalogs` optional upstream)
  `[spec — HV-8]`. `DEFAULT_CAPS = { 'v1.0': { supportedCatalogIds: ['agent-ui'] } }`
  `[estate — a2a.ts:31]`. The "every message" clause is enforced BY CONSTRUCTION: `wrapClientTurn`
  is the only client-composition path and always sets `metadata.a2uiClientCapabilities` (`caps ??
  DEFAULT_CAPS`) AND declares the URI in `extensions: [A2UI_A2A_EXTENSION_URI]`
  `[estate — a2a.ts:111-125]`. Rationale: a stateless server must re-derive the capability set
  from any single message — resumability beats handshake state.
- Mapping surface (pure functions, no I/O): `envelopeToPart` / `partToEnvelope` /
  `wrapServerTurn` / `unwrapTurn` / `wrapClientTurn` / `DEFAULT_CAPS`
  `[estate — a2a.ts:36-125]`. Note the asymmetry: only CLIENT turns carry the `extensions` URI
  declaration and capabilities; `wrapServerTurn` emits role `'agent'` with a leading prose
  TextPart (optional) then one DataPart per envelope, order preserved — SPEC-R16 AC1's
  "identical to the loopback baseline" rides on that ordering `[estate — a2a.ts:59-71]`.

## Tolerating the foreign — the unwrap contract `[estate — a2a.ts:43-47,77-95]`

- `partToEnvelope` returns `undefined` for any part not `kind: 'data'` or not mimeType-tagged; no
  shape validation at this seam (`validateA2ui`'s job downstream).
- `unwrapTurn` routes TextParts to `prose` (a turn's own spoken content, never "foreign"); an
  untagged DataPart or a FilePart is a foreign part — **skipped + counted**
  (`foreignParts: number`), never a throw.
- Negotiation failure modes the estate gates (SPEC-R16 AC2 negative controls): untagged part ·
  invalid payload · caps-less client message · wrong pin — each must fail the standing gate.
  At v0.3.0 the spec itself mandates nothing on unsupported extensions (resolved banner above) —
  the estate's gates are stricter than the pin requires, by design.

## Design lessons the exemplar teaches (for ANY extension)

1. Content rides **DataParts with a registered media type** in part metadata — the A2A layer stays
   payload-agnostic `[spec — HV-8; estate — a2a.ts:36-38]`.
2. Capability declarations ride **message metadata, repeated per message** — stateless resumability
   over handshake state `[spec — HV-8; estate — a2a.ts:97-124]`.
3. The bridge is a **pure mapping module** at the boundary; neither protocol imports the other's
   runtime (type-only imports both ways) `[estate — a2a.ts:15-17]`.
4. Version the VALUE, not just the URI: the capabilities object is keyed `"v1.0"`, so a server can
   dispatch across extension versions from the payload alone `[spec — HV-8]`.
