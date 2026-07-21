# Derivation — how the concepts page derives from the shard, and the drift gates

Estate root: the `agent-ui` repo. The derivation lib is `site/lib/a2a-concepts.ts`; its drift gate
is `site/lib/a2a-concepts.test.ts` (the site vitest project). Sister precedent:
`site/lib/a2ui-gallery.ts`.

## The rule: membership IS the shard

- The lib holds NO record literals — a record added via the import tool appears on the page with
  ZERO site edits `[estate — site/lib/a2a-concepts.ts:1-9,211-221]`.
- Both shards arrive as Vite `?raw` STATIC imports (zero network, zero fetch — the arena page's
  `matches/*.jsonl?raw` precedent) `[estate — site/lib/a2a-concepts.ts:34-35]`.
- Parsed with the package's OWN `parseShard`, filtered with its OWN `admittedRecords` — the same
  zero-dep functions the import tool and the standing corpus gate use; no forked reader
  `[estate — site/lib/a2a-concepts.ts:29,213-221 · packages/agent-ui/a2a/src/corpus/shard.ts:33-72]`.
- Cards render in SHARD order (`buildCardsFrom` maps IN GIVEN order, never sorted) — shard line
  order = seed authoring order = the page's pedagogic order; the authoring side of that chain lives
  in record-anatomy.md §Teaching order `[estate — site/lib/a2a-concepts.ts:199-203]`.

## Card anatomy — every string read off the record

`buildRecordCard(record)` `[estate — site/lib/a2a-concepts.ts:131-197]`: head (`name` + facet badge
+ derived artifact count) → `description` → `body` prose rendered via `textContent`, never
`innerHTML` (paragraph-split on `\n\n`) `[estate — site/lib/a2a-concepts.ts:154-164]` → the
citations list rendered as provenance (`hv` → "Ledger HV-n (a2a-foundations SPEC §2)", `repo` → the
path in `<code>`) `[estate — site/lib/a2a-concepts.ts:46-66]` → one entry per wire artifact.
Nothing is hand-transcribed — SPEC-R15's one-home rule held mechanically.

## The two artifact renderings

- **Inline** → a collapsed JSON `<details>` disclosure PLUS an IN-PAGE VERDICT: the card runs the
  REAL `validateA2a` right there (`expect` = the artifact's declared kind, never `'auto'` — the
  admission pipeline's never-re-classify discipline), reflected onto `data-validated` — computed,
  never a precomputed/hardcoded badge `[estate — site/lib/a2a-concepts.ts:95-118]`.
- **Transcript reference** → a LINK to the arena page (`./a2a-tic-tac-toe.html`), labeled with the
  fixture name + its declared expectation ("a must-fail negative control" for
  `expect:'contaminated'`). Deliberately NO in-page replay: re-importing the raw match text would
  double-ship the fixture bytes, and the arena page + the standing gate already run those exact
  checks — the card states that honestly instead of implying a replay it does not perform
  `[estate — site/lib/a2a-concepts.ts:17-23,71-93]`.
- A failing record is SHOWN, not papered over: `data-validated="false"` + a defect note naming the
  failing `kind@wire[i]` `[estate — site/lib/a2a-concepts.ts:177-194]`.

## The drift gates — and what each leg actually buys

The gate file opens with the honesty note: the set-equality legs (card count/names ≡ the admitted
shard set) are TAUTOLOGICAL against the current derivation — both sides read the same shard — so
they exist as a TRIPWIRE against a future hand-listed refactor, not as proof against a shard edit
`[estate — site/lib/a2a-concepts.test.ts:6-15]`. The REAL coverage:

| Leg | Assertion | Cite |
|---|---|---|
| parse-clean | `parseShard` over both committed raws yields zero failures | `[estate — site/lib/a2a-concepts.test.ts:20-24]` |
| anti-vacuous floor | ≥ 6 concept + ≥ 1 demo cards rendered | `[estate — site/lib/a2a-concepts.test.ts:26-31]` |
| in-page verdict | EVERY card asserts `data-validated === 'true'`, no defect note — a record OR validator regression fails here | `[estate — site/lib/a2a-concepts.test.ts:33-40]` |
| anti-hand-duplication | sampled card text `===` the record's own fields (name/desc/facet/count; citation rows) | `[estate — site/lib/a2a-concepts.test.ts:42-62]` |
| arena links | every transcript artifact renders the `./a2a-tic-tac-toe.html` href | `[estate — site/lib/a2a-concepts.test.ts:64-77]` |
| derivation bites | `buildCardsFrom` over a doctored membership yields exactly one more card carrying the planted name — membership → cards is genuinely 1:1 | `[estate — site/lib/a2a-concepts.test.ts:83-91]` |
| quarantine bites | a planted quarantined record never reaches the rendered set | `[estate — site/lib/a2a-concepts.test.ts:94-108]` |
| broken-artifact bites | `buildRecordCard` over a broken inline artifact flags `data-validated="false"` + the defect note naming `message@wire[0]` | `[estate — site/lib/a2a-concepts.test.ts:111-131]` |

The negative controls drive the PARAMETERIZED seams (`buildCardsFrom`/`buildRecordCard`) with
synthetic records — never the committed shard `[estate — site/lib/a2a-concepts.ts:127-131,199-203]`.

## Extending the page — the zero-edit recipe

1. Author the seed at its curricular POSITION in `seeds.ts` (record-anatomy.md).
2. Run the import tool; admission must pass all-or-nothing (admission.md).
3. Done — the page picks the record up from the shard; the drift gate and the standing corpus gate
   re-verify it on the next `npm test`. Any hand-edit to the page's member list instead of the
   shard is exactly what the tripwire legs exist to catch.
