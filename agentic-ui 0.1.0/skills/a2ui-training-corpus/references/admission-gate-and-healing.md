# The two-tier admission gate & the shared healer

> Source of truth: `packages/agent-ui/a2ui/src/corpus/admit.ts`, `heal.ts`, `validate.ts`, SPEC-R8, ADR-0060/0061. Verified 2026-07-07.

`admit(candidate, deps)` is the corpus's **ONE write path** (`admit.ts:1-10`, LLD §2 invariant iv). It is `async` (canonicalize rides `crypto.subtle`), accepts `candidate: unknown` (the single gateway all untrusted input passes through, `admit.ts:79-80`), and short-circuits on the first failure.

## The pipeline order (this order is load-bearing)

Every stage is independently testable; failures return a typed `AdmitResult` (`admit.ts:64-76`). The exact order (`admit.ts:5-9`):

1. **heal** (`admit.ts:82-93`) — LLD-C7 / ADR-0061. Only `a2uiOutput` is healable; its absence is legal (an eval candidate carries none). `heal` failure → `E_SCHEMA`.
2. **schema/field** (`admit.ts:102-105`) — `validateRecord`'s `E_SCHEMA` failures (see `references/record-schema-and-provenance.md`).
3. **facet gate** (`admit.ts:112-114`) — reject `facet:"eval"` with `E_LEAK` (fail-closed, see `references/exemplar-eval-split-and-no-leak.md`).
4. **pin check** (`admit.ts:117-118`) — `validateRecord`'s `E_PIN` failures.
5. **tier-1 deterministic** (`admit.ts:128-129`) — the shared `validateA2ui`.
6. **pointer RESOLUTION** (`admit.ts:133-136`) — corpus-only, `E_POINTER`.
7. **leak gate** (`admit.ts:139-142`) — `E_LEAK` vs the eval corpus.
8. **canonical + hash** (`admit.ts:145-154`) — fills `canonicalHash`/`componentsUsed`.
9. **dedup** (`admit.ts:168-174`) — `E_DUP`, checks only.
10. **tier-2 rubric** (`admit.ts:178-185`) — the injected judge, `E_QUALITY`.
11. **write** (`admit.ts:187-190`) — `store.put()` + dedup registration.

**Why healing is first, before tier-1** (SPEC-R8): grading must target intent, not formatting — a healable formatting defect must not fail tier-1. **Why dedup registration is deferred to the write stage** (`admit.ts:166-167`, `admit.ts:187-190`): a candidate that fails a *later* stage (the judge) must never pollute the dedup index with a record that was never admitted. **Why the schema and pin failures are split** even though `validateRecord` returns them together: they report at different stages with different codes (`admit.ts:104`, `admit.ts:117` filter the same `recordFailures` by code).

## Tier 1 (deterministic) — the SHARED validator, never a fork

Tier 1 is `validateA2ui` (`admit.ts:128`), which corpus `validate.ts` **re-exports from `renderer/validate.ts`** (`validate.ts:7`) — one implementation, so admission and the runtime return identical verdicts (validator parity, SPEC-N1/R8-AC3, SPEC-N1 "0 disagreements"; the parity is itself a standing test). It checks: schema, catalog-conformance (every component/property exists in the pinned catalog), single-`root` + acyclic ID graph, valid JSON-Pointer bindings.

**The tier-1 → admission code map** (`mapTier1Code`, `admit.ts:214-231`): `PARSE`/`SCHEMA`→`E_SCHEMA`; `VERSION_UNSUPPORTED`→`E_PIN`; `CATALOG`/`CATALOG_UNKNOWN`→`E_CATALOG`; `IDGRAPH`→`E_IDGRAPH`; `POINTER`→`E_POINTER`. `FUNCTION` is a render-time-only code (never emitted by the static validator) and has no row — defaulted to `E_SCHEMA` defensively (`admit.ts:211-213`, `admit.ts:228`).

**Non-obvious — pointer RESOLUTION is a corpus-only stage layered ON TOP of tier-1** (`admit.ts:131-136`, `findUnresolvedPointers` at `admit.ts:384-412`). Tier-1 checks pointer *syntax*; the corpus additionally checks that every `{path}` binding actually *resolves* against the record's own bundled data model — an exemplar bundles its complete data model, so resolution is checkable here (unlike the streaming runtime, where the model arrives incrementally). It mirrors the renderer's list-scope semantics exactly (`admit.ts:333-372`): an absolute path resolves against root; a relative path resolves only inside a dynamic-list item's subtree through element 0 (the witness element). A relative binding with no enclosing list scope is reported unresolved (`admit.ts:401-403`).

## Tier 2 (judgment) — an INJECTED seam, phase-1 skipped

Tier 2 runs only if `deps.judge` is present (`admit.ts:179`). Below-bar → `E_QUALITY` with `failingDimensions` (`admit.ts:181-183`); at/above-bar → sets `meta.qualityScore` (`admit.ts:184`). **Absent → the stage is skipped and `qualityScore` stays unset — the honest, queryable marker of an unjudged record** (`admit.ts:176-177`, ADR-0060 Decision clause 1).

Why injected, not inline: judgment is a document-scored rubric run by a critic seat, and `admit()` is pure Node-side pipeline code where no Claude seat can be dispatched mid-call. Full detail — the verdict adapter, back-scoring, quarantine — is `references/judge-and-verdict-adapter.md`. **Caveat:** SPEC-R8 AC2 (`E_QUALITY`) is proven with a *fake* judge in the test matrix (`admit.ts:46-47`); a real rubric gates production admission only once the harness wave wires one (ADR-0060 Consequences).

## `AdmitDeps` — the shipped seam (ADR-0060 realization note)

`AdmitDeps` (`admit.ts:52-62`): `catalog` (the pinned catalog tier-1 validates against — the caller resolves it by `meta.catalogId`; admission does not own catalog lookup), `store` + `dedupIndex` (stateful, shared across calls in one admission session), `judge?` (the optional seam). The ADR-0060 Decision snippet `{ judge?: Judge }` was an abbreviation — the full seam is exactly this (ADR-0060 Realization note, `admit.ts:63-67` of that ADR).

## The candidate/record bridge

A "candidate" differs from a full `CorpusRecord` in exactly the ways admission fills in (`admit.ts:18-24`): `a2uiOutput` may be raw text needing heal, and `meta.status`/`canonicalHash`/`componentsUsed`/`qualityScore` don't exist yet. Admission defaults a **placeholder** `meta.status:"valid"` only so `validateRecord` (which checks a complete record) can run (`admit.ts:98-100`), then **overwrites it unconditionally** at the write stage — `status: changed ? 'repaired' : 'valid'` (`admit.ts:162`), computed from heal's real `changed` flag. Admission is the sole authority over the final status; a caller-supplied value is never trusted.

## The ONE shared healer (ADR-0061)

`heal(input: string | A2uiOutput, pin?)` (`heal.ts:46-89`) is text-first and per-line-capable — the **same** function serves corpus admission (a whole output, or the raw text an LLM emitted) AND the future streaming codec (one JSONL line at a time). Two healers is the exact fork the streaming v0.2 reconciliation excised (`heal.ts:4-7`, ADR-0061 Alternatives).

**The repair list is CLOSED and form-only** (`heal.ts:10-15`, mirroring A2UI's `parse_response` + `payload_fixer`):
- **(a)** markdown-fence / surrounding-prose stripping → `'fence-strip'` (`heal.ts:99-113`).
- **(b)** trailing-comma removal, string-state-aware so a comma inside a string value is never touched → `'trailing-comma'` (`heal.ts:122-158`).
- **(c)** single-object → array envelope normalization → `'single-object-envelope'` (`heal.ts:67-74`).
- **(d)** a missing per-message `version` filled from the caller's pin → `'version-fill'` (`heal.ts:78-86`).

Structured `A2uiOutput` input skips the text arms (a)/(b) — only (c)/(d) can apply, so an already-array, already-versioned seed heals to `changed:false` (`heal.ts:14-15`, `heal.ts:60-62`).

**NOTHING SEMANTIC IS EVER HEALED** (`heal.ts:17-21`). Unknown components, malformed pointers, missing/duplicate roots, wrong catalogs — none are form defects, so heal leaves them untouched to flow to tier-1 and reject there. **This is the load-bearing contract:** an over-eager healer would *launder invalidity* into a corpus whose whole point is provable validity (PRD-G4). Arm (d) fills only an *absent* version; a *present-but-wrong* version is left for tier-1's `VERSION_UNSUPPORTED` → `E_PIN` (`heal.ts:77`, `heal.ts:44-45`).

`HealResult` is verdict-neutral (`heal.ts:38-40`): `ok:true` always carries a `messages` array (even when `changed:false` — the next stage always runs against `messages`, never raw `input`); `ok:false` means the input couldn't be coerced to JSON at all. Each caller maps `ok:false` to its own vocabulary — admission → `E_SCHEMA` (`admit.ts:89`), the streaming codec → `PARSE` (`heal.ts:36`). A healed admission is marked `status:"repaired"`; the `repairs` list travels in `AdmitResult`, not on the record (the schema is closed — ADR-0061 rejected a `meta.repairs` field; see `references/record-schema-and-provenance.md`).

**Deviation doctrine:** the closed list "will feel too small" the first time a new common LLM defect appears (e.g. smart quotes) — that is deliberate (ADR-0061 Consequences). Widening it is an **amendment to ADR-0061 clause 1**, and each new arm must argue it is *form, not semantics* — never an ad-hoc addition in the module (`heal.ts:19-21`).
