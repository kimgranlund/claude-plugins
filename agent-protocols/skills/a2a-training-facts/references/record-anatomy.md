# Record anatomy — and why authoring order is load-bearing

Estate root: the `agent-ui` repo; paths under `packages/agent-ui/a2a/` unless noted. The schema's
owning module is `src/corpus/record.ts`; the authoring surface is `tools/corpus/seeds.ts` (typed TS
literals, never raw JSON). Current census: 15 concept + 2 demo records
(`corpus/{concept,demo}/v0_3_0/a2a.jsonl`, one line each — verified 2026-07-08).

## The record shape

`A2aCorpusRecord` `[estate — src/corpus/record.ts:47-59]`:

| Field | Meaning |
|---|---|
| `name` | unique join key across BOTH shards |
| `description` | one-line summary — becomes the page card's subtitle |
| `body` | the teaching prose — the ONE home for concept prose (SPEC-R15) |
| `citations` | ≥ 1 — "a record with no resolvable grounding is not documented" |
| `wire` | ≥ 1 wire artifacts |
| `meta` | `{facet, protocolVersion, provenance: {source, origin}, status}` |

Closed key sets on the record AND on `meta` — an unknown key is `E_SCHEMA`
`[estate — src/corpus/record.ts:68-69,97-99,118-121]`.

- **Facets:** `concept | demo` `[estate — src/corpus/record.ts:26]` — one facet per shard file.
- **Status:** `valid | quarantined` `[estate — src/corpus/record.ts:27]` (see admission.md for what
  quarantine changes).
- **Provenance source:** `authored | distilled | mined` — every current record is `authored` with
  `origin: 'tools/corpus/seeds.ts'` `[estate — src/corpus/record.ts:28 · tools/corpus/seeds.ts:19]`.
- **Pin:** `meta.protocolVersion` must equal the family pin (`'0.3.0'`)
  `[estate — src/corpus/record.ts:143-158 · src/protocol/types.ts:8]`.

## Citations (the grounding arm)

Two kinds `[estate — src/corpus/record.ts:35-38]`:
- `{kind: 'hv', row: 'HV-n'}` — a row of the SPEC §2 host-verification ledger (the verbatim-quote
  substrate); must exist there WITH a resolution marker.
- `{kind: 'repo', path}` — a committed artifact (module, fixture, ADR); must exist on disk.

Shape is checked here; RESOLUTION is admission's job — never trusted at the schema layer
`[estate — src/corpus/record.ts:30-33,160-185]`.

## Wire artifacts

`[estate — src/corpus/record.ts:40-45]`:
- **Inline** — `kind ∈ {message, task, card, rpc-request, rpc-response}`: exactly the shared
  validator's own artifact vocabulary, `artifact` carrying the literal.
- **Transcript reference** — `{kind: 'transcript', path, expect: 'clean' | 'contaminated'}`: a
  committed match fixture BY PATH, never inlined (one fact, one home — the fixture stays owned by
  the arena), declaring the isolation verdict it expects.

## The authoring surface (`seeds.ts`)

- Seeds are TYPED literals against the real protocol types, so the type gate covers them; the
  standing drift check for the literals' VALIDITY is the replay arm re-run over the committed shards
  on every `npm test` `[estate — tools/corpus/seeds.ts:1-14]`.
- Tiny helper constructors keep each record readable (`inlineMessage`, `transcriptRef`, …)
  `[estate — tools/corpus/seeds.ts:21-38]`.
- Worked example — record #1 `message-parts`: name/description/body, two HV cites, three inline
  messages (one per part kind) `[estate — tools/corpus/seeds.ts:56-84]`.
- Reuse over re-authoring: `REFEREE_CARD` mirrors the committed, gate-green protocol fixture and is
  shared by records #6 and #7 — one fixture, two teaching angles
  `[estate — tools/corpus/seeds.ts:40-52]`. Nothing is authored speculatively: every wire artifact
  is grounded in an already-validated committed artifact `[estate — tools/corpus/seeds.ts:10-14]`.
- Records may cross-reference each other BY NAME in prose (#17 `canary-mechanism` ↔ #10
  `isolation-gate`) `[estate — tools/corpus/seeds.ts:236-238,352-355]`.

## Teaching order — line order IS the curriculum

The chain, each link cited:
1. Array order in `seeds.ts` IS authoring order — the header says so explicitly
   `[estate — tools/corpus/seeds.ts:7-8]`.
2. `serializeShard` writes one line per record IN GIVEN ORDER + trailing newline — determinism
   comes from seeds being code, never from sorting `[estate — src/corpus/shard.ts:61-67]`.
3. The page renders one card per admitted record in SHARD order — `buildCardsFrom` maps in given
   order, never sorted or hand-listed `[estate — site/lib/a2a-concepts.ts:199-203,211-221]`.

Consequence: a new record's POSITION in the seeds array is a CONTENT decision, not an append
default. Precedent: the four coordinator-ruled additions (#14–17) were appended as a deliberate
late-curriculum cluster after the core protocol→arena arc (#1–11), while the two demo records live
in their own shard/array (`demoSeeds`) `[estate — tools/corpus/seeds.ts:12-14,267,372]`. Inside a
record, `citations`/`wire` array order is semantic too (authoring order, preserved by the canonical
serializer) `[estate — src/corpus/shard.ts:53-59]`.
