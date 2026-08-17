# Sources — provenance for the corpus claims

This pack documents **THIS repo's realized implementation** of the A2UI training-corpus subsystem, not a generic tutorial. Every claim traces to real source in `/Users/kimba/Projects/nonoun/agent-ui`, verified 2026-07-07 against the working tree. Sources in trust order:

## Primary — the shipped code (the ground truth)

The pure core, `packages/agent-ui/a2ui/src/corpus/` (zero-dep, platform-neutral, exposed via the `"./corpus"` subpath — ADR-0062):
- **`record.ts`** — `CorpusRecord` model + `validateRecord` (schema/field `E_SCHEMA`, pin `E_PIN`, single-surface). The `AdmitCode` union (8 members).
- **`heal.ts`** — the ONE shared healer, closed form-only repair list.
- **`canonical.ts`** — the canonicalizer (fold → DFS → renumber → stable-serialize → SHA-256).
- **`dedup.ts`** — exact-hash + MinHash(128, k=3) near-dup index; `DEFAULT_THETA_DUP=0.9`.
- **`admit.ts`** — the ONE write path; the 11-stage pipeline; `AdmitDeps`, `Judge`, `JudgeVerdict`; pointer resolution.
- **`judge.ts`** — `parseVerdictsFile`, `createVerdictJudge`, `UnjudgedCandidateError` (the ADR-0068 verdict adapter).
- **`retrieve.ts`** — TF-IDF cosine top-k; the two builder escalations (signature, facet/status).
- **`export.ts`** — `exportCatalogExamples` (few-shot) + `exportFineTune`.
- **`store.ts`** — pure store core; `all()` / `get()` / `put()` / `serialize()`; `includeQuarantined`.
- **`validate.ts`** — re-exports the shared `renderer/validate.ts` `validateA2ui` (validator parity).
- **`corpus-data.test.ts`** — the LLD-C15 standing gate (re-validates the committed shard every `npm test`).

The Node shell, `packages/agent-ui/a2ui/tools/corpus/` (the only writer of the data dir — ADR-0062):
- **`import-seeds.ts`** — the ADR-0055 seed import; `--verdicts` / `--replace`; `warmDedupIndex`.
- **`rescore.ts`** — the ADR-0068 back-scoring shell (quarantine, all-or-nothing, one-way).
- **`fs-store.ts`** — `loadStore` / `saveStore` over the data dir.

The committed data: `packages/agent-ui/a2ui/corpus/exemplar/v1_0/*.jsonl` (the seed shard, exemplar-only in phase 1).

## Primary — the governing design records (`.claude/docs/`)

Read the ADR/SPEC clause a code comment cites before repeating it (verify-cited-authorities discipline):
- **`specs/specs/a2ui-training-facts.spec.md`** — the behavior + data/schema contract (SPEC-R1…R16, N1…N6, §5 typed contracts, §5.3 error codes). Status: proposed, v0.5, 2026-07-03.
- **ADR-0060** — corpus store phase 1: the tier-2 judge is an injected seam; the eval facet fail-closes. Accepted 2026-07-04.
- **ADR-0061** — the ONE shared healer's contract: closed, form-only; healed → `status:"repaired"`. Accepted.
- **ADR-0062** — packaging: pure core behind `"./corpus"`; Node shell in `tools/corpus/`; data in-package. Accepted.
- **ADR-0063** — record aligns to the *verified* upstream `dataset_schema.json`: unconditional `description`, `target ?? description`, `E_NO_TARGET` retired, interop = projection. Accepted.
- **ADR-0064** — a v1 corpus record is single-surface. Accepted.
- **ADR-0068** — the corpus-quality judge is a deterministic verdict-adapter; `createVerdictJudge` fails closed; back-scoring quarantines; the gate + import path learn quarantine in the same change. Accepted.
- **`.claude/docs/rubrics/a2ui-corpus.md`** — the corpus-quality rubric the `a2ui-reviewer` critic scores against; owns the `qualityScore = MIN over [gate] dimensions` aggregation and the `≥ 4` bar; carries the `version:` marker every verdicts file cites (currently `1.0`). Cited, never copied.
- **`.claude/docs/specs/llds/a2ui-corpus-store.lld.md`** — storage substrate, the LLD-C# slice numbers, the §6 pipeline, §4 canonical algorithm.

## External (verified upstream, via host fetch — the repo does not vendor it)

- **`google/A2UI@main`** (Apache-2.0) — `eval/datasets/dataset_schema.json` (the record superset; fetched 2026-07-03 per ADR-0063), `schema/manager.py` / `schema/catalog.py` (the few-shot example-file shape; fetched per `export.ts:3-19`), and the `parse_response` / `payload_fixer` healing pair the closed healer mirrors. **Caveat:** these are external facts (SPEC Constraint C1) — this repo conforms to them, does not redefine them. A claim about upstream must be re-verified against the current upstream artifact, not a paraphrase (the repo-absence-≠-spec-absence discipline that drove ADR-0063's reversal).

## Terminology note — A2UI v1.0 Candidate rename (2026-08-17, issue #482)

This pack's two `callFunction` mentions (record-schema-and-provenance.md's single-surface exclusion,
canonicalization-and-dedup.md's fold-stream exclusion) were renamed to the Candidate wire term
**`callRendererFunction`** — this pack only ever documented the envelope key as the one A2UI kind
excluded from single-surface counting / canonicalization, not the RPC's direction or
`callableFrom` semantics, so the rename is mechanical here. Mirrors adiahealth/gen-ui-kit's own
in-repo Candidate-terms sweep (issue #1354, PR #1472 — open/review-pending, not yet merged); the
`record.ts`/`canonical.ts` `file:line` citations still name the repo's actual pre-Candidate field
spelling until that PR lands — re-Grep before trusting the exact spelling at a cited line. No
client/server role-vocabulary claim existed anywhere in this pack to sweep (grepped, none found).

## What is corpus-backed vs general knowledge

Everything in this pack's references is corpus-backed (file:line or ADR/SPEC clause). Where an answer leans on general knowledge — e.g. what MinHash/TF-IDF *are* as algorithms — say so and keep the corpus-specific parameters (128 perms, k=3, θ=0.9, TF-IDF-not-embeddings) as the cited part. Anything the code marks "designed but not built" (the `repair()` orchestrator, `score()`, lift measurement — see `references/retrieval-and-repair-loop.md`) must be flagged as specced-not-shipped, never described as working.
