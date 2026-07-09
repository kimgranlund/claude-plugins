# Canonicalization & deduplication on admission

> Source of truth: `packages/agent-ui/a2ui/src/corpus/canonical.ts`, `dedup.ts`, SPEC-R6/R7/N6, corpus LLD-C3/C4. Verified 2026-07-07.

**Canonicalization precedes dedup** (SPEC-R6): reduce an `a2uiOutput` to a deterministic canonical form, hash it, *then* compare. Two outputs that mean the same thing must collide; two that differ in meaning must not.

## Canonical form — what it normalizes and what it preserves

`canonicalize(out)` (`canonical.ts:75-89`) is **async** (it rides `crypto.subtle` for SHA-256 — see below). Algorithm (`canonical.ts:1-24`, LLD §4):

1. **Fold the stream** (`foldStream`, `canonical.ts:93-111`): upsert every `updateComponents` component into one id-keyed map (last write wins per id); apply `updateDataModel` writes in stream order into one data-model value (whole-doc replace when no `path`, else an immutable RFC-6901 write via `setAtPointer`, `canonical.ts:124-139`). `createSurface`/`deleteSurface`/`actionResponse`/`callFunction` carry no tree/data content and don't participate.
2. **DFS from `root`** (`computeVisitOrder`, `canonical.ts:149-182`) via `child` then `children` in **declared field order**, assigning canonical ids `c0=root, c1, c2, …` in visit order. A node reached through two parents is visited once (`canonical.ts:159`).
3. **Rewrite id references** (`buildCanonicalComponent`, `canonical.ts:186-208`): `child`, `children: string[]`, and a children-template's `componentId` are rewritten to canonical ids.
4. **Serialize + hash** (`stableStringify`/`encode`, `canonical.ts:215-232`; `sha256Hex`, `canonical.ts:234-240`).

**What is INSIGNIFICANT (normalized away)** — SPEC-R6 AC1, so these collide:
- Component *declaration order* across `updateComponents` messages (refs are by id, `canonical.ts:5`).
- Object *key order* — `encode` sorts keys recursively (`canonical.ts:220`).
- Insignificant *whitespace* — the encoder emits none.
- *ID spelling* — every id is renumbered `c0…cN` (`canonical.ts:79`).

**What is SIGNIFICANT (preserved)** — SPEC-R6 AC2, so these differ:
- **Child order WITHIN a container** — declared order is semantic and preserved (`canonical.ts:171`, `canonical.ts:6`).
- **Array element order** in the data model — `encode` preserves it (`canonical.ts:217`).
- A changed bound `path`, component type, or tree structure.

**Non-obvious caveat — JSON-Pointer paths are NEVER rewritten.** A `{path}` / `{call}` binding, and a children-template's `path`, address the *data model or a function*, not a component id, so they are copied verbatim (`canonical.ts:196`, `canonical.ts:201-206`, step 4). Renumbering them would break the binding's meaning.

## Determinism (SPEC-N6) — same input, same hash, every platform

Hashing is SHA-256 over the stable serialization, via `globalThis.crypto.subtle` (`canonical.ts:234-240`) — **not `node:crypto`** (that would break zero-dep/platform-neutrality, ADR-0062). This is *why* `canonicalize` is async and admission is async end-to-end (ADR-0062 Consequences). The `encode` writer mirrors `JSON.stringify`'s `undefined` handling: an object property holding `undefined` is omitted, an array element becomes `null` (`canonical.ts:214-227`).

## The disconnected / root-cycle backstop

`CanonicalizeError` (code `IDGRAPH`, `canonical.ts:66-72`) is thrown if `root` is missing (`canonical.ts:151`) or a cycle is detected (`canonical.ts:161`). **Caveat: this is a defensive backstop, not a reachable validation surface** — tier-1 (`validateA2ui`) already rejects a missing/duplicate root, a cycle, and dangling refs *before* admission's canonical stage runs (`canonical.ts:60-64`, and the admission ordering in `references/admission-gate-and-healing.md`). Admission maps a `CanonicalizeError` to `E_IDGRAPH` (`admit.ts:152`) but comments it as a totality guard, not a live path. A component declared but unreachable from `root` is dropped and reported in `disconnected` (`canonical.ts:81`, `canonical.ts:48-50`) — noted, not an error.

## Deduplication — two independent checks (SPEC-R7)

`DedupIndex` (`dedup.ts:129-138`) holds two checks in one object:

- **EXACT**: `canonicalHash` (the SHA-256 above) equality — a byte-for-byte identical output however it was spelled. `exact(hash)` returns the colliding record's name or `null` (`dedup.ts:153`). Backed by `addExact(name, hash)` (`dedup.ts:147`).
- **NEAR**: MinHash(128 permutations) estimate of Jaccard similarity over **k=3 token shingles** of `promptText + " " + canonicalSerialized` (`dedup.ts:2-9`, `MINHASH_PERMS=128`, `SHINGLE_K=3`). `near(sig, theta)` returns the best match with similarity **`>= theta`** (inclusive — SPEC-R7 AC2's bound is `≥`, `dedup.ts:160-161`) or `null`.

`DEFAULT_THETA_DUP = 0.9` (`dedup.ts:27`) — the named default (SPEC-R7: "SHOULD be documented and tunable"; callers pass their own `theta` to `near()`, so the threshold is never a literal buried in admission code).

**The near-dup recipe lives in the CALLER, not this module.** `dedup.ts` only turns text into a signature and signatures into a similarity estimate (`dedup.ts:7-9`, `dedup.ts:98-100`); `admit.ts` composes the exact text `` `${promptText} ${canonical.serialized}` `` (`admit.ts:170`). Any tool that warms the index must use the *identical* recipe or its warmed signatures won't match what `admit()` would produce — `warmDedupIndex` does exactly this (`import-seeds.ts:158-166`); see `references/admission-gate-and-healing.md` and `references/judge-and-verdict-adapter.md`.

## Determinism of the MinHash family (SPEC-N6-adjacent)

The 128 permutation coefficients are generated **once at module load from a FIXED-seed 64-bit LCG** (Knuth/PCG constants, `dedup.ts:77-92`) — **never `Math.random`**. Same coefficients every run, every platform, so a near-dup signature is reproducible across processes, not just self-consistent within one (`dedup.ts:16-18`, `dedup.ts:74-76`). The per-shingle base hash is FNV-1a 32-bit (`dedup.ts:60-67`) — fast and synchronous; the cryptographic hash is `canonical.ts`'s job alone. `tokenize` is `\w+`, case-sensitive, no invented normalization (`dedup.ts:41-43`); text with fewer than `k` tokens degrades to one shingle so short/empty text still yields a well-defined signature (`dedup.ts:51-56`).

**Caveat:** `jaccardEstimate` returns 0 for mismatched-length or empty signatures (`dedup.ts:121-125`) — an undefined-overlap guard, not a real similarity. An empty `DedupIndex` returns `null` from both checks, so the first record admitted never collides (`dedup.ts:140-141`).
