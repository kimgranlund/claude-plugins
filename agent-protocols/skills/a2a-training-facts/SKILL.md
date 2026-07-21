---
name: a2a-training-facts
description: >-
  Answers how the A2A concept/demo teaching corpus is structured, cited, and admitted
  (@agent-ui/a2a's corpus shards — the a2ui-training-facts sibling for the agent-to-agent layer).
  Use for "what does an A2A corpus record contain", "how do I add a concept record", "what makes a
  record admissible", "why was this record rejected", "how do citations work" (HV rows + repo
  paths), "how does the concepts page derive from the shard", "what facets exist" (concept vs
  demo), "why is authoring order load-bearing" (shard line order IS the teaching order). ANSWERS
  from the cited corpus; it does not curate. NOT for the A2UI exemplar corpus — seeds, admission,
  judging (a2ui-training-facts); NOT for protocol facts the records teach (a2a-protocol-facts); NOT for
  running an actual import/admission (the repo's tools + the repo-local curation seat).
disable-model-invocation: false
user-invocable: false
---

# a2a-training-facts — the A2A teaching-record world model

Ground truth (the `agent-ui` repo): `packages/agent-ui/a2a/tools/corpus/seeds.ts` (the authored
records — line order IS teaching order), `src/corpus/{record,admit,shard}.ts` (schema + admission +
store), the committed shards (`corpus/{concept,demo}/v0_3_0/a2a.jsonl` — 15 concept + 2 demo
records), the derivation lib + drift gate (`site/lib/a2a-concepts.{ts,test.ts}`), and
`.claude/docs/lld/a2a-corpus-docs.lld.md`. Answer from the cited references below — never restate
the schema from memory; `record.ts` owns it.

Answer classes (one reference each):

- **[record-anatomy](references/record-anatomy.md)** — the record shape (name · description · body ·
  citations ≥1 · wire ≥1 · meta), facet (concept | demo), status (valid | quarantined), citation
  kinds (HV-row vs repo-path), inline wire kinds vs by-path transcript references, the `seeds.ts`
  authoring surface — AND why authoring order is load-bearing: seeds array order → shard line order
  → the page's pedagogic order; a new record's POSITION is a content decision, not an append
  default.
- **[admission](references/admission.md)** — the four codes (`E_SCHEMA · E_PIN · E_CITE ·
  E_REPLAY`) and their ownership split, the three-stage pipeline (batch within, short-circuit
  between), citation resolution against the SPEC §2 HV ledger, the replay gate (inline artifacts
  through the real `validateA2a`; transcript references through `validateTranscript` +
  `checkIsolation` with expectation matching BOTH directions), quarantine semantics, the
  all-or-nothing single-writer import tool, and the standing `corpus-data` gate with its
  red-control legs.
- **[derivation](references/derivation.md)** — the concepts page derives from
  `admittedRecords(parseShard(raw))`, never hand-listed; card anatomy (every string read off the
  record, in-page `validateA2a` verdicts, transcript links to the arena with no in-page replay);
  the drift-gate legs and what each actually buys (set equality = a refactor tripwire; the real
  coverage = parse-clean, per-card verdicts, anti-hand-duplication sampling, bite-proven negative
  controls).
