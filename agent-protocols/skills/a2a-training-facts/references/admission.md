# Admission — codes, pipeline, quarantine, the single writer, the standing gate

Estate root: the `agent-ui` repo; paths under `packages/agent-ui/a2a/` unless noted.

## The four codes and who owns them

`E_SCHEMA · E_PIN · E_CITE · E_REPLAY` `[estate — src/corpus/record.ts:61-66]`. One concern, one
code — so a firing fixture per code stays clean `[estate — src/corpus/record.ts:8-21]`:

| Code | Owner | Fires on |
|---|---|---|
| `E_SCHEMA` | `validateCorpusRecord` (pure) | container shape: unknown keys, bad vocab, malformed `wire[]` discriminators `[estate — src/corpus/record.ts:90-141,187-215]` |
| `E_PIN` | `validateCorpusRecord` | `meta.protocolVersion` missing OR ≠ the family pin — presence is deliberately E_PIN, not E_SCHEMA `[estate — src/corpus/record.ts:143-158]` |
| `E_CITE` | shape arm in `validateCorpusRecord`; RESOLUTION arm in admission | missing/empty/malformed `citations`; a dangling HV row or repo path `[estate — src/corpus/record.ts:160-185 · src/corpus/admit.ts:43-49]` |
| `E_REPLAY` | admission only (needs I/O + the shared validators) | an inline artifact failing `validateA2a`; a transcript that is unreadable, schema-invalid, or whose isolation verdict mismatches its declared `expect` `[estate — src/corpus/admit.ts:51-117]` |

No healer exists anywhere: a malformed candidate is rejected, never repaired — seeds are typed,
authored TS, not mined model output `[estate — src/corpus/record.ts:20-21 · src/corpus/admit.ts:10-12]`.

## The pipeline (`admitRecord` — pure function of `(candidate, deps)`)

Batch WITHIN a stage, short-circuit BETWEEN stages `[estate — src/corpus/admit.ts:5-9,30-72]`:

1. **Schema + pin + citation shape** — `validateCorpusRecord`.
2. **Citation resolution** — every citation through `deps.resolveCitation` (hv → the SPEC §2 ledger
   read; repo → `existsSync`).
3. **Replay** — per wire artifact: inline → the SAME shared `validateA2a`, with `expect` passed
   EXPLICITLY as the declared kind (never `'auto'` — a mislabeled artifact fails rather than being
   re-classified) `[estate — src/corpus/admit.ts:57-68]`; transcript → read, `validateTranscript`
   (re-checks the header pin), then the arena's own `checkIsolation`, and the verdict must MATCH the
   declared `expect` in BOTH directions — an `expect:'contaminated'` fixture that passes clean is a
   STALE NEGATIVE CONTROL, exactly as much a defect as a clean match that starts failing
   `[estate — src/corpus/admit.ts:78-117]`.

## Quarantine semantics

- A `status:'quarantined'` line is LEGAL in a shard: stage 1 always runs; stages 2–3 are SKIPPED
  (a quarantined record may legitimately no longer replay — that is what quarantine records)
  `[estate — src/corpus/admit.ts:38-40]`.
- Consumption excludes it: `admittedRecords` filters quarantined lines, so the page never renders
  them `[estate — src/corpus/shard.ts:69-72]`.
- The skip is proven load-bearing, and never a blanket exemption: a planted quarantined record with
  a dangling citation still admits; one with a schema defect still fails
  `[estate — src/corpus/corpus-data.test.ts:218-235]`.
- Quarantining IS a curator edit: flip `status` in `seeds.ts`, re-import.

## The single writer (`import-seeds.ts`)

Only this tool writes `corpus/`. It wires the real deps (ledger read via the shared path constant;
`existsSync`; `readFileSync`) around the pure pipeline and is ALL-OR-NOTHING: any failure prints
EVERY `CorpusFailure` across every seed and exits non-zero writing NOTHING; re-running on unchanged
seeds is byte-idempotent `[estate — tools/corpus/import-seeds.ts:1-8,62-101]`. A missing/unreadable
SPEC ledger fails loudly NAMING the dependency, never a bare ENOENT
`[estate — tools/corpus/import-seeds.ts:41-53]`.

**The ledger coupling:** `LEDGER_PATH = '.claude/docs/spec/a2a-foundations.spec.md'` lives in ONE
exported constant imported by both the tool and the gate — a SPEC move is a one-line greppable fix
`[estate — tools/corpus/ledger-path.ts:10]`. `isHvRowResolved` requires the row to carry a BOLDED
`**CONFIRMED**`/`**CORRECTED**` marker — a row present but never resolved does NOT count
`[estate — tools/corpus/ledger-path.ts:19-28]`.

## The standing gate (`corpus-data.test.ts` — every `npm test`)

Re-validates the COMMITTED shards through the SAME `admitRecord` + real deps the import tool uses —
no forked reader `[estate — src/corpus/corpus-data.test.ts:60-78,135-139]`:

- floors: concept ≥ 6, demo ≥ 1 (the PRD target as an executable predicate)
  `[estate — src/corpus/corpus-data.test.ts:92-95]`;
- `name` unique across BOTH shards; facet-per-shard
  `[estate — src/corpus/corpus-data.test.ts:108-116]`;
- canonical-line identity per line: `serializeRecord(JSON.parse(line)) === line` — byte-stability
  enforced directly, no stored hash `[estate — src/corpus/corpus-data.test.ts:131-133 · src/corpus/shard.ts:8-11]`;
- the `isolation-gate` record carries BOTH arena contaminated fixtures as `expect:'contaminated'`,
  so every test run re-proves the arena's must-fail controls still fail
  `[estate — src/corpus/corpus-data.test.ts:142-154]`;
- red-control legs prove the gate itself bites: a stale re-keyed line, a dangling HV cite, a
  dangling repo path, a flipped transcript expectation — each asserted to FAIL, in the same file
  `[estate — src/corpus/corpus-data.test.ts:179-216]`.

## "Why was this record rejected" — triage by code

`E_SCHEMA` → the record/meta shape or a `wire[]` discriminator (`record.ts`) · `E_PIN` → the
`meta.protocolVersion` literal · `E_CITE` → a citation's shape, an unresolved HV row, or a
nonexistent repo path · `E_REPLAY` → the artifact itself: run the failing artifact through
`validateA2a` (its `detail` carries the underlying `code@path` list
`[estate — src/corpus/admit.ts:61-67]`), or re-check the transcript's declared expectation.
