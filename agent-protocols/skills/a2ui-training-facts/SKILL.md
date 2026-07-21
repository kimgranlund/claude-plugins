---
name: a2ui-training-facts
description: >-
  The A2UI training-corpus subsystem in @agent-ui/a2ui — the curated store conditioning and
  measuring generation. Use for "how do I curate/admit a corpus record", "why was this
  record quarantined/rejected", "what error code does admission raise" (E_SCHEMA, E_PIN, E_DUP,
  E_LEAK …), "how does retrieval pick exemplars", "what does the healer fix",
  "what happens on a catalog/protocol version change". Covers the record schema (ADR-0063), two sub-corpora + no-leak
  invariant, canonicalization+dedup, the two-tier admission gate + form-only
  healer, the judge adapter (qualityScore = min) + quarantine, top-k retrieval +
  export, version-change repair. ANSWERS from a cited corpus; it does not build.
  NOT for the wire protocol (a2ui-protocol-facts); NOT for catalog design / coverage
  (a2ui-catalog-facts); NOT for the live demo's retrieval use (a2ui-chat-agent-facts);
  NOT for RUNNING curation — importing, back-scoring, quarantining
  (a2ui-corpus-curate); NOT for pipeline SOURCE (a2ui-builder) or judging a record
  (a2ui-reviewer).
disable-model-invocation: false
user-invocable: false
---

# a2ui-training-facts — the corpus subsystem world model

The training corpus is the artifact that turns "an agent *can* emit A2UI" into "an agent *reliably*
emits valid, idiomatic A2UI" (PRD-G5): a curated store of exemplar records that condition generation
(few-shot / retrieval / fine-tune) and eval records that measure it. This pack explains **this repo's
realized implementation** — `packages/agent-ui/a2ui/src/corpus/**` + `tools/corpus/**`, governed by
ADR-0060/0061/0062/0063/0064/0068 and the corpus SPEC. It ANSWERS with cited claims; it never curates,
admits, judges, or edits pipeline source (see Boundaries).

| Ask | Load |
|---|---|
| Record shape — what a record MUST carry, required/optional fields, provenance, pins, single-surface, upstream alignment | `references/record-schema-and-provenance.md` |
| Exemplar vs eval — the two facets, the no-leak invariant, why the eval facet fail-closes | `references/exemplar-eval-split-and-no-leak.md` |
| Canonical form + dedup — what normalizes vs what's preserved, exact-hash + MinHash near-dup, determinism | `references/canonicalization-and-dedup.md` |
| Admission + healing — the 11-stage pipeline, tier-1 vs tier-2, error codes, the closed form-only healer | `references/admission-gate-and-healing.md` |
| Judge / verdict adapter — critic-authored verdicts, qualityScore=min, fail-closed, quarantine, rescore, --replace | `references/judge-and-verdict-adapter.md` |
| Retrieval / export / repair loop — top-k by intent, few-shot + fine-tune export, version-change coherence (+ what's designed-not-built) | `references/retrieval-and-repair-loop.md` |
| Provenance — where a claim comes from (file:line, ADR/SPEC clause, verified upstream) | `references/sources.md` |

## Load discipline (read before opening a reference)

The references are **catalogs to consult, not books to read**. Classify the ask, open the ONE matching
file, **Grep it for the term** (an error code, a function name, a SPEC-R#) and Read around the match —
targeted, not a start-to-finish read. Seven files total (six axes + `sources.md`); each claim carries
its `file:line` or ADR/SPEC clause so an answer is checkable, not asserted.

**An answer is complete when it carries all three:** the claim, its `file:line` / ADR/SPEC clause cite,
and the failure mode / caveat it triggers. Without the caveat it is half an answer.

## Consult procedure

1. Classify the ask against the seven rows above; load only the matching reference. If it spans two
   (e.g. "why was this quarantined *and* can it come back" → judge + retrieval), load both.
2. Answer with the **claim, its cited source, and the failure mode / caveat it carries** — a corpus
   answer without the caveat is half an answer. Worked shape:
   > *"Our judge is grading records against `target` and some come back scoring garbage — bug?"*
   > → judge/schema ask → `record-schema-and-provenance.md`: `target` is **optional**; when absent the
   > effective target IS `description` (ADR-0063, verified upstream). **The trap:** the fallback is a
   > *consumer* rule — every judge MUST read `target ?? description`, never `target` raw (SPEC-R2;
   > `record.ts:105`). A judge reading `target` directly grades `undefined` when it's omitted — that's
   > the bug, not the corpus. Fix the judge's read; validation deliberately doesn't enforce the fallback
   > because with `description` always required, an effective target always exists (`E_NO_TARGET` was
   > retired, ADR-0063 clause 3).
3. Check the boundary before answering: if the ask turned into the wire shape a payload conforms to,
   it was `a2ui-protocol-facts`'s; catalog rows/coverage, `a2ui-catalog-facts`'s; the live demo's use of
   `retrieve()`, `a2ui-chat-agent-facts`'s. Route it to the owner rather than answering past the seam.
4. Route making at the boundary (below) — never curate, admit, judge, or edit source from this pack.

## Deviation doctrine (every default carries its rationale)

A corpus rule is a *default with a reason*, so a consumer can tell a legal deviation from drift. Three
carry named widening/activation triggers — cite the trigger, don't invent a workaround:
- **Single-surface** (ADR-0064) is a deliberate YAGNI narrowing; the first real multi-surface exemplar
  reverses it by ADR (surface-scoped folding). Don't pre-emptively "fix" the global fold.
- **The eval facet fail-closes** (ADR-0060); it opens when LLD-C8 lands the contamination mechanism.
  Never admit eval records unencrypted "temporarily".
- **The healer's repair list is closed** (ADR-0061); a new arm is an amendment to clause 1 that must
  argue it is *form, not semantics* — never an ad-hoc module patch, or it launders invalidity into a
  corpus whose whole point is provable validity.

Frontier — specced, not shipped: the SPEC-R13 `repair()` orchestrator, `score()` (SPEC-R14), and lift
measurement (SPEC-R15) are **contract-only** — the state machine + the standing re-validation gate do
the SPEC-R13 work today; the orchestrator lands with the deferred eval wave (ADR-0068 clause 7). Say
"designed, not shipped" for these — never describe them as working (`retrieval-and-repair-loop.md`).

## Boundaries — this pack ANSWERS; it routes ALL making

- **Curating / admitting an actual record, back-scoring, resolving an admission HALT** → the
  `a2ui-corpus-curate` skill (the thin procedure over this shipped mechanism; repo-local to agent-ui).
- **Building or fixing pipeline SOURCE** (record/heal/canonical/dedup/admit/judge/retrieve/export/store,
  or the Node shell) → the `a2ui-builder` agent. It builds; this pack explains.
- **Judging a record against its rubric / emitting the VerdictsFile** → the `a2ui-reviewer` agent
  (generator ≠ critic — the verdict this pack's adapter consumes is authored there, never here).
- **Sibling knowledge packs** (answer their asks, don't answer past the seam): `a2ui-protocol-facts` (the wire
  shape a record's `a2uiOutput` conforms to), `a2ui-catalog-facts` (catalog rows + coverage the tier-1
  check validates against), `a2ui-chat-agent-facts` (the live demo that CALLS `retrieve()`).

## Extending this pack

A missing axis, a stale reference (a SPEC/ADR revision, a pipeline change), or "add X to this pack" is
authoring work — route to [[make-pack]] (axis decomposition, grounded research waves against real
source, index + cite discipline). Never bolt an uncited file onto the corpus inline; a claim without a
`file:line` or ADR/SPEC clause does not belong here. The routing corpus of record is
`scripts/routing-corpus.json`.
