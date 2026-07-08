# Retrieval (top-k by intent), export, & the repair loop

> Source of truth: `packages/agent-ui/a2ui/src/corpus/retrieve.ts`, `export.ts`, `store.ts`, `corpus-data.test.ts`, SPEC-R10/R11/R12/R13, ADR-0063/0068. Verified 2026-07-07.

How the exemplar corpus is *consumed* (three modes) and how it stays coherent when the catalog or protocol version moves. **This axis carries the pack's one honest "more designed than built" flag** — see the repair-loop section.

## Three exemplar consumption modes (SPEC PRD-D1)

The SPEC frames three conditioning modes, all exemplar-only, all excluding quarantine:

1. **Few-shot export** — `exportCatalogExamples(records, scope)` (`export.ts:67`, SPEC-R10). Emits a **set of files-to-be** (`name → content`), one example per file, that upstream's `A2uiSchemaManager.generate_system_prompt(include_examples=True)` consumes. `content` is the record's `a2uiOutput` **verbatim** — no `---BEGIN/---END` markers, no `### Examples:` heading (upstream's loader adds those at load time; the file never carries them, `export.ts:16-20`). This shape was host-fetched from `google/A2UI@main` (`schema/manager.py`, `schema/catalog.py`, a real fixture — `export.ts:3-19`), the repo-absence-≠-spec-absence discipline again.
2. **Dynamic retrieval** — `retrieve(records, query)` (`retrieve.ts:59`, SPEC-R11). Below.
3. **Fine-tune export** — `exportFineTune(records, scope)` (`export.ts:111`, SPEC-R12). Instruction/output pairs, excluding all eval content.

## Retrieval — zero-dep TF-IDF cosine top-k

`retrieve(records, query)` (`retrieve.ts:59-118`) ranks by **TF-IDF cosine similarity** over `promptText + " " + meta.componentsUsed` (`documentText`, `retrieve.ts:37-40`), scoped to a `catalogId`/`protocolVersion` pin. `RetrieveQuery = { intent, k, catalogId, protocolVersion }` (`retrieve.ts:24-29`). The relevance method (TF-IDF vs embeddings) was the LLD's call to close PRD-D1 (SPEC §7); TF-IDF is what shipped — zero-dep, no model.

**Never throws; returns `[]` for** (`retrieve.ts:48-58`): empty `records`, empty scope after filtering (SPEC-R11 AC2), `k <= 0` (`retrieve.ts:60`), or a query sharing zero vocabulary with the scope (a zero-norm query vector makes cosine undefined — treated as genuine "no match", `retrieve.ts:99`). Ties break by ascending `name` for a deterministic order (`retrieve.ts:112-115`). NFR: `retrieve()` returns within ≤ 200 ms p95 for ≤ 10⁴ exemplars (SPEC-N2).

**Two escalations the builder flagged, both still open** (read these before wiring retrieval):
- **Signature reconciliation** (`retrieve.ts:6-11`): the LLD §9 prose describes `retrieve(store, query)` over a store *handle*, but the shipped signature takes a plain `records` array — the build-dependency graph had `record.ts` but not `store.ts` at this slice's dispatch. A caller composes `retrieve(store.all(...), query)` once the store lands. Flagged to the team lead as a signature reconciliation point for whoever wires this into `admit.ts` / the streaming driver.
- **Facet/status exclusion not LLD-C9-explicit** (`retrieve.ts:12-18`): the exemplar-only, non-quarantined filter is implemented as a **hard defensive invariant** regardless of caller input (`retrieve.ts:62-68`), even though the LLD-C9 bullet didn't repeat it (the exporter bullet, LLD-C10, did). Flagged in case the LLD should state it explicitly.

The live conversational agent CALLS `retrieve()` (its `produce()` loop sources a few-shot block) — but that consumer, its system-prompt derivation, and the drift gate over it belong to the `a2ui-conversational-agent` pack, not here.

## Version pinning is what makes a mixed-version corpus legal

Every record pins `protocolVersion` + `catalogId` (SPEC-R9; see [[record-schema-and-provenance]]). The default pin for new records is A2UI **v1.0** (SPEC §7, resolved 2026-06-26), but a mixed v0.9/v1.0 corpus is legal — only the default pin is v1.0. Retrieval and export scope by that pin, so a consumer only ever sees records for its exact catalog/version. This is the substrate the repair loop acts on.

## The repair loop (SPEC-R13) — DESIGNED, only PARTIALLY built

SPEC-R13 requires: when a pinned `catalogId`/version or `protocolVersion` changes, re-validate every affected record and mark each `valid` / `repaired` / `quarantined` — **never silently stale**. The SPEC §5.2 operation surface types this as `repair(change): RepairReport`.

**Honest status — verified 2026-07-07: no `repair()` function and no `RepairReport` type exist in the codebase** (grep-clean across `src/corpus/**` and `tools/corpus/**`). The SPEC-R13 *orchestrator* — the thing that walks the affected records on a version bump and drives each to a terminal state — is **designed but not built**. What actually exists and does the SPEC-R13 *work* today:

1. **The state machine** — `status ∈ {valid, repaired, quarantined}` (`record.ts:19`), the three terminal states SPEC-R13 names. `quarantined` is excluded from consumption (`store.all()`, `store.ts:124`), kept in the shard for audit.
2. **Back-scoring** (`rescore.ts`) drives records into `quarantined` when a critic verdict falls below bar — this "rides repair-loop semantics" (ADR-0068 clause 4; `rescore.ts:4-6`), one-way. See [[judge-and-verdict-adapter]].
3. **The sanctioned re-entry** — `import-seeds --replace <name>` re-admits an improved record through the full pipeline, recomputing its status honestly. This is the manual analogue of "repair a stale record".
4. **The standing re-validation gate** — `corpus-data.test.ts` (LLD-C15) re-validates the committed exemplar shard on **every `npm test`**: every non-quarantined line must pass tier-1 (`validateA2ui`) against the *current* default catalog, and its stored `meta.canonicalHash` must match a fresh recomputation (`corpus-data.test.ts:1-15`). **This is the de-facto "never silently stale" enforcement today** — a catalog change that invalidates a stored record fails CI loudly, rather than a `repair()` run auto-transitioning it. A quarantined line's tier-1/hash legs are skipped (it may legitimately no longer validate — ADR-0068 clause 6).

**Why the orchestrator is deferred:** ADR-0068 clause 7 split corpus LLD-C12 — the judge half activated (this is [[judge-and-verdict-adapter]]); the Inspect-AI **scoring/lift half stays deferred** with LLD-C8 (trigger: the first eval record), and that wave must first host-verify upstream `eval/a2ui_eval/scorers.py` + `dataset.py` (unverified C1 facts). The full automated repair loop lands with that eval wave.

## Also designed-not-built in this consumption/eval region (flag, don't fabricate)

- **`score(gen, against): {tier1, tier2}`** (SPEC-R14, dual-tier scoring of a *generated* output against an eval record) — no such function in `src/corpus/`. Distinct from the admission judge: this scores generation at eval time. Deferred with LLD-C12/C8 (ADR-0068 clause 7).
- **`leakCheck()` as a standing CI gate** (SPEC-R3 AC1) — the *admission-time* leak gate is built (`admit.ts`), but the eval corpus is empty (fail-closed), so the standing CI leak gate waits for LLD-C8 (ADR-0060 Consequences; see [[exemplar-eval-split-and-no-leak]]).
- **Lift measurement** (SPEC-R15, with-vs-without-corpus over a fixed eval set) — the flagship PRD-G5 metric; needs the eval corpus, so deferred.

If asked about any of these, say plainly: the *contract* is specced, the *mechanism* is not yet built, and the named activation trigger is the first eval record + the harness eval wave. Do not describe them as shipped.
