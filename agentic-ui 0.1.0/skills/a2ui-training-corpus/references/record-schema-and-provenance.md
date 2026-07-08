# Record schema & provenance

> Source of truth: `packages/agent-ui/a2ui/src/corpus/record.ts`, `.claude/docs/specs/specs/a2ui-training-corpus.spec.md` §5.1 / SPEC-R1/R5/R9, ADR-0063, ADR-0064. Verified 2026-07-07 against the repo.

What one corpus record is, what it MUST carry, and why the schema is shaped the way it is. Every claim traces to the hand-rolled validator `validateRecord` in `record.ts` — there is no JSON-Schema library in the pipeline (zero-dep, SPEC-N5), so the draft-07 schema in SPEC §5.1 is transcribed field-by-field in code.

## The record shape (the typed contract)

`CorpusRecord` (`record.ts:22-42`) is a **superset of A2UI's upstream `dataset_schema.json`** plus one curation block, `meta`:

- Top-level A2UI fields: `name` (unique id), `description`, `promptText` (the user input to the LLM), optional `target`, `catalog`, `role_description`, `workflow_description` — these mirror upstream's dataset schema (SPEC-R1).
- `a2uiOutput` — the ordered A2UI message stream (the exemplar's ground truth); optional at the type level, **required iff `meta.facet === 'exemplar'`** (`record.ts:30`, enforced at `record.ts:119-121`).
- `meta` — the curation block (`record.ts:31-41`): `facet`, `protocolVersion`, `catalogId`, optional `catalogVersion`, `provenance {source, origin}`, optional `canonicalHash`, `componentsUsed`, `status`, `qualityScore`.

**Both key sets are closed.** `KNOWN_RECORD_KEYS` (`record.ts:62-65`) and `KNOWN_META_KEYS` (`record.ts:66-69`) drive an unknown-key rejection (`record.ts:95-97`, `record.ts:130-131`) — this is the code realization of the schema's `additionalProperties: false`. **Caveat:** you cannot stash extra fields on a record. This is deliberate and load-bearing — see the `meta.repairs` rejection in [[admission-gate-and-healing]] (ADR-0061 rejected adding a field; the audit trail rides `AdmitResult`, not the record).

`validateRecord(r: unknown)` is **pure and TOTAL** (`record.ts:78-86`): it never throws, always returns a (possibly empty) `RecordFailure[]` — a code + offending field path. It batches every failure it finds rather than short-circuiting (`record.ts:88-127`). The `try/catch` safety net maps any unforeseen input to `E_SCHEMA` at path `''` (`record.ts:81-85`), mirroring the shared renderer validator's totality stance.

## `description` is unconditionally required — the verified upstream rule (ADR-0063)

`description` is required for **every** facet, exemplar and eval alike (`record.ts:103`, top-level `required: ["name","description","promptText","meta"]` in SPEC §5.1:134).

This overturns an earlier design. SPEC v0.3 (the same day) had carved out an eval-facet exception — `description` required *except* on an eval record carrying `target`. ADR-0063 **reversed it** after the host fetched the authoritative upstream artifact, `google/A2UI@main eval/datasets/dataset_schema.json`, whose verbatim rule is `"required": ["name", "description", "promptText"]` (ADR-0063 Context clause 1). **Failure mode this closes:** building to a *paraphrase* of an external contract instead of the fetched artifact — the "repo-absence ≠ spec-absence" discipline. The lesson generalizes: a C1-touching (external-fact) resolution should trigger the host fetch *before* the SPEC encodes it (ADR-0063 Consequences).

## `target` is optional — and the fallback is a CONSUMER rule, not a validation rule

`target` (the judge's grading criteria) is optional; `validateRecord` only type-checks it when present (`record.ts:105`, `optionalStr`). **When absent, the effective target IS `description`** — upstream's verbatim semantic, "If omitted, defaults to the value of `description`" (ADR-0063 Context clause 2; SPEC-R2).

**The critical caveat (this is where scorers go wrong):** the fallback is a *consumer* rule. Every judge/scorer MUST read `target ?? description`, **never `target` raw** (SPEC-R2; ADR-0063 Decision clause 2). A judge reading `target` directly would silently grade against `undefined`. Validation does not enforce the fallback because there is nothing to enforce — with `description` always present, an effective target always exists.

Consequence: **`E_NO_TARGET` was retired** (ADR-0063 Decision clause 3). It appears nowhere in the `AdmitCode` union (`record.ts:46-54`) — the union has 8 members, not 9. A missing-target failure mode is unreachable by construction; a code that can never fire is dead vocabulary.

## Interop = a PROJECTION onto the upstream 7 fields (not just "strip meta")

To validate a record against upstream, project it onto the upstream field set by dropping **`meta` AND (for exemplars) `a2uiOutput`** (SPEC-R1 AC1; ADR-0063 Decision clause 4). Because upstream sets `additionalProperties: false` on items, `a2uiOutput` violates upstream validation for *every* exemplar — so the old "strip the curation-metadata block" (strip `meta` only) never actually validated upstream. **Caveat:** the exporter/interop surfaces own this projection; the stored record is a *superset*, not the interop record. Upstream dataset files are one JSON **array** of samples (`"type": "array"`), not JSONL (ADR-0063 Context clause 4, SPEC-R16).

## Version pinning → `E_PIN`, deliberately NOT `E_SCHEMA`

Every record MUST pin `protocolVersion` and `catalogId`, both non-empty (SPEC-R9 AC1). `checkPins` (`record.ts:184-205`) raises **`E_PIN`** — not `E_SCHEMA` — for a missing/empty pin, and for any `a2uiOutput` message whose `version` disagrees with the pin (`record.ts:197-199`) or any `createSurface.catalogId` that disagrees (`record.ts:200-203`).

**Non-obvious placement:** `protocolVersion`/`catalogId` are in the same `meta.required` list as the other fields, but the LLD deliberately reassigns their presence/value checks to the *pin stage* (`E_PIN`), not the schema stage (`record.ts:165-167` NOTE). So a missing pin is `E_PIN`, a missing `provenance.origin` is `E_SCHEMA` — the codes are not interchangeable, and the admission pipeline filters failures by code and reports them at different stages (see [[admission-gate-and-healing]]).

## Provenance (SPEC-R5)

`meta.provenance` is `{ source, origin }`. `source ∈ {authored, distilled, mined}` (`record.ts:72`, `record.ts:156-158`). `origin` MUST be a **non-empty** string (`record.ts:161-163`) — this is the one explicitly-AC'd emptiness rule besides the pin fields; every other string field is type-only per §5.1 (`record.ts:159-160` NOTE). **Caveat:** provenance records *where a record came from*, never *how good it is* — ADR-0060 explicitly rejected treating `authored` provenance as satisfying the quality gate (that conflates provenance with quality). Quality lives in `qualityScore`; see [[judge-and-verdict-adapter]].

## Single-surface (ADR-0064) — a corpus-only narrowing

An exemplar's `a2uiOutput` MUST address **exactly one** surface: every surface-bearing envelope carries the same `surfaceId`, and at least one exists (SPEC-R2; `checkSingleSurface`, `record.ts:218-245`). Surface-bearing keys are `createSurface`/`updateComponents`/`updateDataModel`/`deleteSurface`/`actionResponse` (`record.ts:216`); `callFunction` is the one envelope with no `surfaceId` and is **excluded from the count, not banned** (`record.ts:228`).

**Why this rule exists (the hazard it closes):** the shared validator judges id-graphs *per surface* (so a multi-surface stream is tier-1-legal), but the canonicalizer folds **globally** (`canonical.ts:93-99`) — two surfaces each legally declaring `id:"root"` would silently last-write-wins into a chimera before hashing (ADR-0064 Context). Rejecting at the record schema (`E_SCHEMA` at the second surface's message path, `record.ts:236`) — not at an admission stage — means the standing corpus-data gate (LLD-C15) catches a hand-edited multi-surface line in a *stored* shard too, not only a freshly-admitted one (ADR-0064 Decision clause 2). The **exactly-one** (not at-most-one) bound also closes the `callFunction`-only hole: an output with zero surfaces renders nothing and rejects `E_SCHEMA` at path `a2uiOutput` (`record.ts:244`).

**Deviation doctrine:** this is a deliberate YAGNI narrowing — the corpus is narrower than the protocol. The widening trigger is named (ADR-0064 Decision clause 4): the first real multi-surface exemplar reverses it by ADR, delivering surface-scoped folding and a defined multi-surface hash semantic. Until a consumer exists, that machinery is speculative. Do not "fix" the global fold pre-emptively.
