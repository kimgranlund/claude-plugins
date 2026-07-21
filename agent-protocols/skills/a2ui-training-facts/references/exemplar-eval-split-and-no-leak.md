# Exemplar vs eval sub-corpora & the no-leak invariant

> Source of truth: `.claude/docs/specs/specs/a2ui-training-facts.spec.md` §2 / SPEC-R2/R3/R4, `packages/agent-ui/a2ui/src/corpus/admit.ts`, `store.ts`, ADR-0060. Verified 2026-07-07.

The single most load-bearing decision in the corpus SPEC (SPEC §2): **two facets that must never be conflated**, and the invariant that keeps measurement honest.

## The two facets

| Facet | Purpose | Carries | Visibility |
|---|---|---|---|
| `exemplar` | *Condition* generation — few-shot, retrieval, fine-tune | prompt + **ground-truth `a2uiOutput`** | public / model-visible by design |
| `eval` | *Measure* generation — held-out scoring | prompt + judge `target` (optional; falls back to `description`) | held-out / contamination-protected |

`meta.facet ∈ {exemplar, eval}` (`record.ts:70`). The facet decides two things: whether `a2uiOutput` is required (exemplar only — `record.ts:119-121`), and where the record shelves on disk (`store.ts:67-71`: `exemplar/…/*.jsonl` vs `eval/…/*.jsonl.enc`).

**Why the split exists:** A2UI's own eval framework encrypts its eval datasets at rest precisely because public "gold" answers get ingested by training crawlers and inflate scores — data contamination (SPEC §2). An exemplar's whole job is to be model-visible; an eval record's whole job is to stay unseen so the score it produces is honest.

## The no-leak invariant (SPEC-R3)

No eval-corpus `promptText` — or a near-duplicate of it, by the `references/canonicalization-and-dedup.md` similarity measure — may appear in the exemplar corpus (SPEC-R3). A leak means the model has effectively seen a held-out prompt, so its eval score is inflated.

Two enforcement points:
- **Admission-time** (`admit.ts:139-142`, `checkLeakGate` at `admit.ts:249-257`): an *exemplar* candidate's `promptText` is checked (MinHash near-match, `DEFAULT_THETA_DUP = 0.9`) against every already-admitted `facet:"eval"` record's `promptText`. A collision rejects `E_LEAK` naming the eval record. Note this uses `promptText` alone, not the full dedup recipe — an eval record may carry no `a2uiOutput` (`admit.ts:245-248`).
- **A standing leak gate** (SPEC-R3 AC1): reports the count of eval prompts whose similarity to any exemplar prompt exceeds the dedup threshold; a nonzero count fails CI with `E_LEAK`.

**Caveat — the leak gate is vacuously satisfied today.** Because the eval facet fail-closes (below), the eval corpus is always empty in phase 1, so `checkLeakGate` iterates an empty set and returns `null` (`admit.ts:250-251`). The stage runs *real logic* — it is not special-cased away — it simply has nothing to match against until a caller seeds an eval record directly or LLD-C8 lands (`admit.ts:246-248` note). This is the recurring "phase by refusing the unprotected case, not by pretending the requirement doesn't apply" pattern.

## The eval facet fail-closes (ADR-0060)

Admission **rejects every `facet:"eval"` candidate** with `E_LEAK` (`admit.ts:112-114`), detail: "eval facet fail-closed: the LLD-C8 contamination mechanism is unbuilt". This is stage 3 of the pipeline, right after the schema check.

**Why:** SPEC-R4 requires the eval corpus to be contamination-protected at rest (encryption-at-rest or a private split — the mechanism is an LLD-C8 choice, deferred until the first eval record exists, ADR-0060 Context). Until that mechanism exists, admitting an eval record would write unprotected gold to a git-committed shard — and *contamination cannot be un-published later* (ADR-0060 Alternatives). So SPEC-R4/N3 ("a public clone reveals no gold") holds **vacuously and honestly**: no eval record can enter unprotected storage.

The `.jsonl.enc` extension the store computes for eval shards (`store.ts:69`) is **pure path arithmetic, not the encryption mechanism** — the mechanism itself is unbuilt (`store.ts:66` note). Do not mistake the extension for a shipped encryption feature.

**Deviation doctrine / activation trigger:** this is a named reserved seam (ADR-0031/0051/0058 precedent — ship the seam, activate on the first real consumer). The eval facet opens when corpus LLD-C8 lands the contamination mechanism (ADR-0060 Consequences). Do not admit eval records "temporarily" unencrypted — ADR-0060 rejected that outright.

## Consumption is exemplar-only, defensively

Every consumption surface hard-filters to exemplars and excludes quarantine, *regardless of what the caller passes*:
- `retrieve()` — `r.meta.facet === 'exemplar' && r.meta.status !== 'quarantined'` (`retrieve.ts:62-68`), a defensive invariant the retriever imposes even though LLD-C9 didn't repeat it (`retrieve.ts:11-18` note).
- `exportCatalogExamples` / `exportFineTune` — the same hard invariant (`export.ts:22-24`): an eval-facet or quarantined record can never leak into an export artifact (SPEC-R3/R13).
- `store.all()` — excludes `status:"quarantined"` by default (`store.ts:124`); `get()` does not (it is an audit accessor, `store.ts:47`).

**Failure mode this closes:** a leak by *export*. Even if an eval record somehow reached the store (a direct seed), the exemplar-only export filter prevents it surfacing in a few-shot artifact, retrieval result, or fine-tune pair. The invariant is enforced at each consumption site, not just at admission — belt and suspenders.
