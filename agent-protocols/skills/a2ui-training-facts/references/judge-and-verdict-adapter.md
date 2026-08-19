# The judge / verdict adapter & quarantine

> Source of truth: `packages/agent-ui/a2ui/src/corpus/judge.ts`, `tools/corpus/rescore.ts`, `import-seeds.ts`, `store.ts`, ADR-0068, SPEC-R8/R13. Verified 2026-07-07.

The corpus-quality judge is a **deterministic verdict-adapter over critic-authored verdicts** — NOT a judge that runs inside `admit()` (ADR-0068 clause 2; `judge.ts:1-8`). This is the resolution of the "how do you run judgment inside a pure Node pipeline" problem: you don't — judgment happens in a critic seat, and the pipeline consumes its authored artifact.

## The split: judgment in a critic seat, plumbing in code

- **The critic authors verdicts** (ADR-0068 clause 1). The `a2ui-reviewer` agent grades each record against the rubric document `.claude/docs/rubrics/a2ui-corpus.md` (repo-owned; cited here, never copied — that doc owns the dimensions and the bar) and emits ONE verdicts file.
- **The adapter is deterministic** (ADR-0068 clause 2). `judge.ts` is pure core (zero-dep, no filesystem — ADR-0062) that *looks up* the critic's verdict; it never scores anything itself (`judge.ts:2-4`, `judge.ts:149-152`).

Why not score inside `admit()`: a heuristic scorer (length/complexity proxies) would be *scripts impersonating judgment* — the exact placement violation `process.md` rule 1 bans (ADR-0068 Alternatives); an LLM API call would add a secret + a dependency to a zero-dep core and make admission non-deterministic and unrunnable in CI.

## `qualityScore = MIN over gate dimensions` — and where that rule lives

The aggregation is: **`qualityScore` = the MINIMUM across the `[gate]`-typed dimensions** on the 1–5 scale; **`passed` = `qualityScore ≥ 4`** (the SPEC-R8 bar) — ADR-0068 clause 1.

**Critical caveat about ownership:** this MIN-and-bar rule is defined in the **rubric document** and applied by the **critic seat** when it authors the verdict. `judge.ts` does NOT compute the min — it only *reads* the `passed`/`qualityScore` the critic already wrote (`admit.ts:37-38`, `judge.ts:154-162`). So "why is this record's score the min of its dimensions?" is answered by the rubric (`a2ui-corpus.md`), not by any code in `src/corpus/`. The `JudgeVerdict` the code consumes is `{ qualityScore, passed, failingDimensions? }` (`admit.ts:39-44`).

## The verdicts file (ADR-0068 clause 1, SPEC §5.3)

`VerdictsFile` (`judge.ts:15-21`): `{ rubric: 'a2ui-corpus', rubricVersion, judgedBy, date, verdicts: Record<record.name, JudgeVerdict> }`. `parseVerdictsFile(text, expectedRubricVersion)` (`judge.ts:46-99`) is **total** — it batches every issue (malformed JSON, missing/wrong `rubric`, unknown top-level or per-verdict key, malformed per-name verdict) into a structured `issues[]`, never short-circuiting (mirrors `validateRecord`).

**`rubricVersion` MUST equal the rubric document's `version:` marker** (`judge.ts:60-67`) — a verdict is meaningless without the standard it scored against (ADR-0068 clause 1). The pure core never reads the rubric file itself (ADR-0062): the **caller** supplies `expectedRubricVersion` — the Node shell reads `a2ui-corpus.md`'s `^version:\s*(\S+)$` marker and passes it in (`rescore.ts:36-50`, `import-seeds.ts:62-76`; the marker is currently `version: 1.0`). This is why the rubric-home path is duplicated across both shells rather than factored out — each shell independently owns "where the rubric doc lives" (`import-seeds.ts:56-60`).

## `createVerdictJudge` fails CLOSED on an unjudged candidate

`createVerdictJudge(file)` (`judge.ts:154-162`) returns a `Judge` whose `score(record)` is a name lookup. **A candidate ABSENT from the file makes `score()` THROW** `UnjudgedCandidateError` (`judge.ts:140-147`, `judge.ts:158`) — with a judge wired, *every* candidate must be judged; there is no silent unjudged admit into a judged-era corpus (ADR-0068 clause 2). `import-seeds --verdicts` catches the throw and reports+halts (`import-seeds.ts:245-248`) — the θ_dup escalation precedent, never a silent skip. **Skip-on-absent was explicitly rejected** (ADR-0068 Alternatives): it would silently mix judged and unjudged records and destroy the query value of the absent-`qualityScore` marker.

## Three asymmetric outcomes — admission rejects, back-scoring quarantines, replacement re-admits

This asymmetry is the design's spine (ADR-0068 Consequences):

1. **Admission** below-bar → **`E_QUALITY`** (rejected entry, `admit.ts:181-183`). A candidate can be refused the door.
2. **Back-scoring** (`rescore.ts`) below-bar → **`status:"quarantined"`** (`rescore.ts:120-122`). A *stored* record is never erased by a grade — quarantine is SPEC-R13's honest state: excluded from consumption by `store.all()` (`store.ts:124`), kept in the shard for audit. Deletion was rejected (it erases the audit trail + dedup identity, ADR-0068 Alternatives).
3. **Replacement** (`import-seeds --replace <name>`) → judged re-admission through the full pipeline. Leaving quarantine is deliberate, judged, and logged.

## `rescore` — all-or-nothing, one-way, deliberately partial

`rescore.ts` (the ADR-0068 clause 4 back-scoring shell) applies a verdicts file **only to records with no prior judged outcome** — `qualityScore` absent AND `status !== 'quarantined'` (`isAlreadyJudged`, `rescore.ts:65-67`). Semantics:
- **All-or-nothing**: the whole file is validated and every update computed before one `serialize()` call (`rescore.ts:96-131`). A verdict naming a record not in the store → halt (`rescore.ts:105-107`); a *different* verdict for an already-judged record → halt (`rescore.ts:112-118`) — a re-judge is the deliberate `--replace` path, never a drive-by.
- **Idempotence**: an *identical* verdict for an already-judged record is a no-op (`verdictMatchesCurrent`, `rescore.ts:74-77`); zero updates skips the write entirely (`rescore.ts:137-141`).
- **Deliberately partial**: records not named in the file are untouched and reported still-unjudged (`rescore.ts:133`). Only *admission* fails closed on the unjudged; rescore does not.
- **One-way**: `quarantined` never un-quarantines under rescore (`rescore.ts:5-6`). The stored record cannot honestly recover `valid` vs `repaired` (heal's `changed` fact lived at admission time; re-healing an already-healed form is always `changed:false`), so rescore would have to guess — the `--replace` re-admission recomputes it truthfully through the single write path (ADR-0068 Alternatives, last bullet).

## Quarantine survives the import path — two guards + one sanctioned exit (ADR-0068 clause 5)

Without these, a plain re-import would silently erase a quarantine: `warmDedupIndex` iterated `store.all()` (which skips quarantined), and `store.put()` upserts by name — so a re-run found no `E_DUP` and overwrote the quarantined line unjudged (ADR-0068 Context (2)). The fix:

- **(a) Dedup warming sees quarantined records** — `store.all()` gained an `includeQuarantined?: boolean` flag (default `false`, so every existing consumer is unchanged — it is a storage-integrity read, `store.ts:38-44`), and `warmDedupIndex` passes it (`import-seeds.ts:159`). A re-imported identical seed now hits `E_DUP` against the quarantined line.
- **(b) A name collision HALTS** — a candidate that clears dedup whose `name` matches a stored quarantined record halts with nothing written (`import-seeds.ts:252-265`); `store.get()` sees all statuses (`store.ts:47`).
- **(c) `--replace <name>` is the sanctioned exit** — a deliberate, judge-required re-admission through the full pipeline (`import-seeds.ts:204-207` requires `--verdicts`). Because an improved seed is near-identical to its predecessor **by construction**, `--replace` omits *that one record's* signatures from warming for that run (`warmDedupIndex(store, index, replaceName)`, `import-seeds.ts:158`, `import-seeds.ts:211`) — otherwise it would `E_DUP` against the very record it replaces. The run report logs the prior status + `canonicalHash` (`import-seeds.ts:313-315`); the git-committed shard preserves the replaced line in history.

## The standing gate learned quarantine in the same change (ADR-0068 clause 6)

`corpus-data.test.ts` (LLD-C15) re-validates the committed shard on every `npm test`. It was **amended** so `status:"quarantined"` lines are legal: parse + `validateRecord` + the facet assertion run for every line; the tier-1 + hash-recomputation legs run for **non-quarantined lines only** — a quarantined record may legitimately no longer validate against the current catalog (that is what quarantine records, SPEC-R13). The old `not.toBe('quarantined')` assertion cited "LLD §2 invariant ii", which is actually *facet-only* (a shard holds one facet); consumption-exclusion belongs to `store.all()`, not the gate. **The gate got stronger, not weaker** — a hand-edited `status` flip is still caught by `validateRecord`'s enum.

## The phase-1 debt this clears

Before this wave, 11 seed-imported records sat honestly unjudged (absent `qualityScore` — ADR-0060's marker). After the back-score run the "absent `qualityScore`" count goes 11 → 0 (or the quarantine delta is itemized), and the ADR-0060 marker retires from active duty (ADR-0068 Consequences).

---

## UPDATE 2026-08-19 — the refusal becomes durable (ADR-0165), the importer fails closed (GH #1346), and the MIN-fold in the field

**[verified]** 2026-08-19 against ADR-0165's accepted text (fetched verbatim from
`kimgranlund/agent-ui`), the repo-local `a2ui-corpus-curation` skill's halt catalog at head
`26742a9c`, and GH #1262 / PR #1326 / PR #1342 bodies. The 2026-07-07 sections above still hold;
these extend them.

**The `VerdictsFile` is now a COMMITTED artifact, and archive precedence is dated (ADR-0165).**
ADR-0068's Consequences claimed all three outcomes "are queryable" — verified FALSE for the
admission-reject arm: an `E_QUALITY` refusal returned from `admit()` before any store write, so it
was recorded NOWHERE (the named casualty: `retreat-reschedule`, rejected `qualityScore 2`, surviving
only as prose in three source comments). The repair: a judged run ARCHIVES its own verdicts file
verbatim into `corpus/verdicts/<date>--<slug>.json` in the same all-or-nothing step as `saveStore` —
"zero admissions is not zero record" (an all-refused wave still archives; that is the single
highest-value archive in the design). Read side: one pure merge (`verdict-archive.ts`), precedence =
**latest `date` wins**; two same-date files disagreeing on one name = structured error, halt.
**An archived refusal does not expire** — a `passed:false` scored against an OLDER `rubricVersion`
still blocks and still reds; clearing it takes a fresh judged run whose newer-dated verdict wins by
precedence. And the coverage gate now reads JUDGED-ness off the shard (the `unjudgedAdmissions`
leg), so a silent re-admission can no longer turn the gate green — the refused seed is RED on both
branches of its future.

**The fail-closed importer law (GH #1346).** ADR-0068 cl.2's fail-closed only bit when a judge WAS
wired; a BARE run (no `--verdicts`) used to pass unchecked. The closed form: a bare run is legal only as the
all-`E_DUP` no-op — the moment ANY candidate clears dedup (a new seed, OR the **source-drifted
content of an already-admitted name**), the run HALTS with nothing written ("N candidate(s) reached
the judge tier with no judge wired"). Without this, routine re-imports silently re-admit
source-drifted seeds unjudged — exactly the class the archive exists to catch, arriving through the
front door. Resolve by re-running with `--verdicts`; a bare run can never admit anything.

**MIN-fold consequences, worked (GH #1262).** `qualityScore = MIN over gate dimensions` means one
weak dimension sinks the record — and it also means the RUBRIC's dimension list is load-bearing
shared state: the payload rubric grew P9 (card anatomy) without the corpus rubric bumping, so
judges graded P1–P8 and could only report P9 advisory. Kim's ruling folded P9 in (corpus rubric →
1.2, `D1 = MIN P1–P9`) and re-judged ONLY the affected seeds; `frontier-image-hero-card` — a
5-scoring record on every other dimension — failed D1 on P9 alone (action Button in CardContent,
no footer). Conduct: a judge that grades against a stale dimension list reports the gap to the
RUBRIC owner; it never averages, and never scores a dimension the rubric version doesn't carry.

**Repair-then-replace over discard, worked (PR #1326).** The nine Tier-A back-scored records were
repaired AT SOURCE (actions into CardFooter; gated records to FormProvider-as-root with gating
verified preserved), re-validated (`validate-payload 9/9 exit 0`), then re-admitted through the
FULL judged pipeline via `--replace` — never hand-edited in the shard, never discarded. The shard
diff + run report + git history stay the audit trail; `status` is recomputed honestly by admission.
