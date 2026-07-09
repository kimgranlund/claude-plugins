# Content — Parts, media types, and metadata

Estate paths relative to `agent-ui/packages/agent-ui/`; HV rows live in SPEC §2
(`agent-ui/.claude/docs/spec/a2a-foundations.spec.md`).

## The Part union

"export type Part = TextPart | FilePart | DataPart;" with per-part discriminator field **`kind`** ∈
`"text"` / `"file"` / `"data"` `[spec — HV-4, [T]]`. Every part also carries an optional open
`metadata?: Record<string, unknown>` `[estate — a2a/src/protocol/types.ts:41-59]`.

| Part | Required body | When it's right |
|---|---|---|
| `TextPart` | `text: string` | human-readable prose — a turn's spoken content |
| `DataPart` | `data: Record<string, unknown>` | structured machine JSON — closed schemas ride here |
| `FilePart` | `file: FileWithBytes \| FileWithUri` | file content, inline or by reference |

Worked DataPart examples `[estate]`: the arena's board-state message
(`a2a/src/protocol/fixtures/message.data.json` — board cells, mark, legal moves) and the bridge's
A2UI envelopes (one envelope per tagged DataPart — see `extensions-and-bridging.md`).

## FilePart — the exact contract `[spec — HV-4/HV-11]`

Both variants extend upstream's `FileBase { name?: string; mimeType?: string }` ("An optional name
for the file (e.g., \"document.pdf\").") `[spec — HV-11]`:

- `FileWithBytes`: `bytes: string` — "The `uri` property must be absent when `bytes` is present."
- `FileWithUri`: `uri: string` — "The `bytes` property must be absent when `uri` is present."

Mutual exclusion is typed upstream via `never`; the estate flattens the `FileBase` idiom into two
interfaces with `uri?: never` / `bytes?: never` — no shared base needed
`[estate — a2a/src/protocol/types.ts:61-74]`. Fixtures: `message.file-bytes.json` /
`message.file-uri.json`. (The HV ledger does not quote the `bytes` encoding — do not assert
base64 without a spec fetch.)

## What the validator enforces per part `[estate — a2a/src/protocol/validate.ts:105-129]`

| Defect | Verdict |
|---|---|
| unknown `kind` | `A2A_SCHEMA` at `/parts/i/kind` — never a throw (SPEC-R3 AC2) |
| `text` not a string | `A2A_SCHEMA` at `/parts/i/text` |
| `data` not an object | `A2A_SCHEMA` at `/parts/i/data` |
| file with BOTH `bytes`+`uri`, or neither | `A2A_SCHEMA` at `/parts/i/file` ("exactly one of bytes\|uri") |

Part `metadata` contents are never validated — deliberately an open map (see
`versioning-and-conformance.md`, "deliberately unvalidated").

## Where media types go

- **FilePart**: `mimeType?` on the file object itself `[spec — HV-11, FileBase]`.
- **DataPart**: upstream v0.3.0 defines no media-type field on the part — the tagging idiom is
  part-level `metadata` with a `mimeType` key; the A2UI v1.0 A2A extension registers
  `metadata.mimeType: "application/a2ui+json"` `[spec — HV-8]`; the bridge dispatches on exactly
  that key `[estate — a2ui/tools/pipeline/transports/a2a.ts:36-47]`.
- **Mode declarations** (media-type strings, not per-part): card-level
  `defaultInputModes`/`defaultOutputModes` and per-skill `inputModes?`/`outputModes?`
  `[spec — HV-7/HV-11]`; per-request `configuration.acceptedOutputModes?` on `message/send`
  `[spec — HV-12, MessageSendConfiguration]`. The estate's cards declare `["application/json"]`
  `[estate — a2a/src/protocol/fixtures/card.referee.json]`.

A receiver dispatches on `kind` first, then (for DataParts) on the metadata tag: the bridge's
`partToEnvelope` returns `undefined` for any part that is not `kind: 'data'` or not
mimeType-tagged — foreign parts are tolerated, never thrown on
`[estate — a2ui/tools/pipeline/transports/a2a.ts:43-47]`.

## Metadata scoping — part-level vs message-level

Both levels are open `Record<string, unknown>` maps upstream `[spec — HV-4]`. The estate's earned
division of labor:

- **Part-level `metadata`** — facts about THIS part's content: the media-type tag
  (`mimeType: "application/a2ui+json"`) that makes one DataPart self-describing
  `[estate — a2ui/tools/pipeline/transports/a2a.ts:37]`.
- **Message-level `metadata`** — facts about the TURN/session: per-message capability
  re-declaration (`a2uiClientCapabilities` on EVERY client→server message — a stateless server
  must re-derive the capability set from any single message; the bridge lesson, HV-8)
  `[estate — a2ui/tools/pipeline/transports/a2a.ts:109-124]`.
- Task-level and artifact-level `metadata?` also exist `[spec — HV-5/HV-11]`.

Rule of thumb: if removing the part would make the metadata meaningless, it belongs on the part;
if it governs how the whole exchange is interpreted, it belongs on the message.
