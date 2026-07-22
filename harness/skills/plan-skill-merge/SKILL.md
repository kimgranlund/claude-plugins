---
name: plan-skill-merge
description: >-
  Decide whether several thin, overlapping, or porous knowledge skills should merge into one
  context-efficient pack — packs that step on each other's routing, or scattered siblings with
  gaps. Runs the inverse test battery into a consolidation manifest. NOT for authoring a
  single skill (make-skill); NOT for executing an already-decided merge (reshape-skill); NOT
  for splitting a corpus into a family (plan-skill-split).
disable-model-invocation: false
user-invocable: true
argument-hint: "[candidate-skill-paths]"
---

# plan-skill-merge — consolidate, but earn it

The decision layer of a knowledge-skill merge: this skill tests whether consolidation is earned and,
if so, designs the merged pack — it never executes the move itself. Execution is downstream:
authoring the merged pack and any flagged research wave is `/make-pack`'s (`/make-skill` covers
the SKILL.md surface), and the
merge mechanics — fence transfers, referrer rewire — are a manual refactor until an executor sibling
ships; note that a merge, unlike a rename, is **not** git-reversible. This skill is the formal
inverse of `plan-skill-split` and shares its evidence lineage, run backwards, plus one test specific
to merging: porosity (are the candidates individually too thin to sustain a pack, but a real pack
together?).

## The inverse tests, in order

1. **Redundancy / overlap** — do the candidate skills answer overlapping ask classes? Check whether
   their `evals/evals.json` suites (or legacy routing corpora) share trigger prompts, or whether a
   user/model would have to guess which sibling to consult for the same question. High overlap is
   evidence *for* merging — read `../plan-skill-split/references/foundations.md`'s
   vocabulary-separability test in reverse: a shared token field that plan-skill-split treats as a
   kill reason for splitting is, read backwards, the positive signal for synthesis (if the router
   already can't reliably tell two skills apart, they were never separable — `/check-routing`'s *stolen*
   and *leaked* shapes appearing between two siblings are this test, already measured).
2. **Shared-audience vocabulary** — do the candidates' descriptions already compete for the same
   trigger words? The same signature that makes two candidate *children* fail a split (test 3 of
   plan-skill-split) is the signature that makes two *existing* skills a merge candidate.
3. **Thin / porous corpus** — is any candidate below the healthy floor (a 2–3 file axis, a gap its
   own maker has already flagged, a corpus a `plan-skill-split` run would itself reject as too small
   to earn its own pack)? A candidate that is thin *alone* may be exactly right *combined* with a
   sibling covering an adjacent question.
4. **Context-efficiency delta** — quantify, don't assert: sum today's cost (N descriptions × their
   char counts, N eval suites, N CHANGELOGs, N SKILL.md bodies) against the ONE projected
   consolidated surface. State the number. "More efficient" with no arithmetic behind it fails this
   test by default.

**The asymmetry that makes this more than plan-skill-split in reverse:** passing 1–4 is necessary but
not sufficient. Before finalizing, run the *proposed merged pack* through plan-skill-split's own four
tests (procedure step 4) — a synthesis that immediately re-qualifies for a future split has not
solved anything; it has relabeled a monolith as an efficiency win. A good synthesis produces a pack
that a fresh `plan-skill-split` run would not flag.

`../plan-skill-split/references/foundations.md` derives the shared mechanics (why the router routes
on descriptions, why ask co-occurrence is the empirical proof); `references/best-practices.md`
(this pack) walks the reverse-reading worked example in full.

## Procedure

1. **Survey every candidate.** File/axis counts, current descriptions with char counts, eval suites
   if present, and every external referrer to *each* candidate handle — the merge's blast radius is
   the union of all candidates' referrer sets, not just the survivor's.
2. **Run the four inverse tests.** Where eval suites exist, build the same query → axes-engaged
   table `plan-skill-split` uses, but read it for *overlap*: shared axis hits across two candidate
   suites are merge evidence, not a routing bug to fix in place.
3. **If tests clear, design the ONE consolidated pack** per the axis-decomposition discipline
   (3–7 axes, ask-shaped, never literature-shaped) — fold the candidates' existing axes together,
   de-duplicate files that cover the same claim (keep the better-cited or more current version;
   note the discarded one in the manifest as `superseded_by`, never silently drop it), and flag any
   real gap for a `/make-pack` research wave to fill (the fill is make-pack's job, not this
   skill's). Draft the ONE description (≤1024 chars, the open-standard cap) and decide its
   invocation posture — both dials, explicitly.
4. **Self-check against plan-skill-split before finalizing.** Run the proposed merged pack's own file
   list and axis table through `../plan-skill-split/scripts/manifest_check.py`'s sizing logic (or a
   direct read of its four tests) — if the merged pack would itself qualify as a `split` candidate,
   the axes are still too heterogeneous; iterate the design rather than ship a monolith wearing an
   efficiency label.
5. **Validate mechanically:**
   `python3 scripts/consolidation_check.py <manifest.json>` — every source file from every candidate
   accounted for (moved / cited-as-superseded-duplicate / flagged-as-gap), no orphans, the new
   description ≤1024 chars, and the context-efficiency delta computed and printed. Fix and re-run
   until clean.
6. **State the verdict** — `consolidate` (name the one new pack) or `keep-separate` — with the full
   ledger. Hand off the manifest + repair map to `/make-pack` and the executing refactor
   (`/reshape-skill` executes it from the validated manifest; it attics rather than deletes because a merge is not git-reversible).
   For high-stakes merges, the `skill-checker` agent scores the manifest against
   `references/rubric.md` before the host ratifies (generator ≠ critic).

## Worked precedent (read in reverse)

The source corpus's own `color-theory-facts` no-split verdict (archival:
`~/.claude/docs/color-theory-facts-partition-assessment.md`, external to this plugin) is the clearest
available worked example, read backwards. Its four axes — Harmony, Wheel/history, Programmes,
Meaning — were never actually shipped as separate skills, but the exact reasoning that kept them one
pack (entangled shared vocabulary, a cross-axis majority of real asks, a 3-file Meaning axis too
thin to stand alone) is precisely the *positive* signal this skill looks for. Had someone mistakenly
shipped those four as separate thin packs, `plan-skill-merge`'s inverse tests would catch the
identical signal from the other direction and recommend re-merging them into one `color-theory-facts`
pack — which is exactly the pack that already exists today. `references/best-practices.md` walks
this reverse reading in full, plus a second, hypothetical worked case.

## Manifest schema

```jsonc
{
  "source_candidates": [
    { "name": "old-skill-a", "path": "skills/old-skill-a", "files": ["ref1.md", "ref2.md"],
      "description_chars": 640 },
    { "name": "old-skill-b", "path": "skills/old-skill-b", "files": ["ref3.md"],
      "description_chars": 510 }
  ],
  "verdict": "consolidate",                              // "consolidate" | "keep-separate"
  "target_pack": {
    "name": "new-consolidated-pack",
    "axes": ["axis-one", "axis-two", "axis-three"],
    "file_map": [
      { "file": "ref1.md", "from": "old-skill-a", "axis": "axis-one" },
      { "file": "ref2.md", "from": "old-skill-a", "superseded_by": "ref3.md", "reason": "ref3 covers the same claim, more current" }
    ],
    "flagged_gaps": ["axis-two has no file backing 'X' — route to a pack-authoring research wave"],
    "description": "...", "invocation_posture": "default"
  },
  "context_efficiency_delta": { "before_chars_total": 1150, "after_chars_total": 700, "packs_before": 2, "packs_after": 1 },
  "referrer_repair_map": [
    { "file": "skills/some-sibling/SKILL.md", "line": 12, "old": "old-skill-a", "new": "new-consolidated-pack" }
  ]
}
```

## Boundaries

- **This skill decides and designs; it never executes the merge.** Authoring the merged pack's
  references/INDEX (and any research wave filling a flagged gap) is `/make-pack`'s; executing the merge — fence transfers, referrer rewire, proving the sweep — is a
  refactor executed by `/reshape-skill` from the validated manifest.
- **Not a candidate-finder.** Surfacing that a corpus-wide duplicate/drift problem exists in the
  first place is `check-everything`'s job; this skill takes named candidates and designs a specific
  merge, it does not sweep the whole corpus looking for them.
- **Not its own inverse.** Splitting one corpus into a family is `plan-skill-split`.

## Routing

| Peer | For |
|---|---|
| `plan-skill-split` | the inverse operation; also the self-check this skill runs before finalizing |
| `check-everything` | finding merge candidates across the whole corpus before this skill is dispatched |
| `make-pack` | authoring the merged pack's corpus; running flagged research waves |
| `reshape-skill` | executing this skill's manifest — moves, rewires, sweep proof |
| `make-skill` | authoring the merged pack's SKILL.md surface |
| `check-skill` | scoring the merged pack once authored |
| `check-routing` | the measured overlap evidence (stolen/leaked shapes between candidate siblings) |

## Done / NOT done

**Done** = all four inverse tests run with cited evidence, the proposed merged pack self-checked
against plan-skill-split's tests (and passes — would not itself qualify for a future split), the
consolidation manifest reconciles (`consolidation_check.py` clean) with every source file accounted
for, the context-efficiency delta stated as a number, and the handoff names both downstream steps.
**NOT done** = a merge proposed without checking overlap against real eval data, a discarded
duplicate file dropped without a `superseded_by` note, an efficiency claim with no computed delta,
or a merged pack that skipped the plan-skill-split self-check and shipped a disguised monolith.
