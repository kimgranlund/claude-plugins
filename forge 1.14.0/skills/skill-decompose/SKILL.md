---
name: skill-decompose
description: >-
  Decide whether a sprawling knowledge corpus should split into a family of knowledge skills, and
  into which ones. Use when a pack outgrows one entry surface: "this skill has gotten huge, break it
  up", "turn this reference dump into several packs", "is one entry surface still enough for all
  these reference files", "we're loading way too much context for one simple question, split this
  pack". Runs four evidence tests (sizing, ask co-occurrence, vocabulary separability, cost ledger)
  — keeping a cohesive cluster unified — to produce a reconciled file-mapping manifest, per-child
  descriptions, and a referrer repair map; or a no-split verdict when the corpus doesn't earn one.
  NOT for authoring a single skill or growing one reference file (skill-forge); NOT for executing an
  already-decided split or rename (skill-refactor executes; this skill decides and designs); NOT a
  UI/technical-architecture/goal breakdown (system-decompose); NOT consolidating several
  already-separate skills into one (skill-synthesize).
disable-model-invocation: false
user-invocable: true
argument-hint: "[corpus-path]"
---

# skill-decompose — decide the family, don't assume it

The decision layer of a knowledge-corpus split: this skill tests whether a family is earned and, if
so, designs it — it never moves a file itself. Execution is downstream of the verdict: minting or
growing each child pack is `/pack-forge`'s (research waves per axis; `/skill-forge` covers each
child's SKILL.md surface), and the move/rewire/prove pass is a
refactor executed by `/skill-refactor` from the validated manifest. The method below is the one the source corpus ran
twice in one session on real packs: `color-science` (159 files) genuinely split into four
(`color-space-facts/-perception/-accessibility/-materials`); `color-theory-facts` (28 files) was tested
against the identical four tests and **failed** every one — the honest answer was no-split. Both
outcomes are correct uses of this skill; the second is not a lesser result.

## The four tests, in order

Tests 1–3 gate whether a split is even worth pricing; test 4 prices it. A corpus that fails 1–3
does not reach test 4 — state the no-split verdict there and stop.

1. **Sizing** — the imported pack doctrine's healthy range is 3–7 retrieval axes per pack (the
   reference instances are `ui-pattern-facts`, hand-authored, and the `color-*-facts` family,
   research-wave scale). Is one entry surface actually straining — INDEX line count, load-discipline
   pressure (files >1000 lines forcing Grep-first warnings), a stated file count that has drifted
   from the tree? `color-science` at 159 files / ~10 axes was straining; `color-theory-facts` at 28 files
   / 4 axes was not — the same size as `ui-pattern-facts`, the source corpus's own model of a healthy
   single pack.
2. **Ask co-occurrence** — pull the corpus's own `evals/evals.json` trigger prompts (or a legacy
   `scripts/routing-corpus.json` / `evals/task-prompts.md` if that's what it has); for each, name
   every candidate axis it actually needs to answer. If a majority need two or more, a split makes
   cross-pack consult the *common* case — that is a kill, not a caveat. `color-theory-facts`: 6 of 12
   positives spanned two axes ("should I use complementary colors" needs Wheel *and* Harmony
   simultaneously) — rejected. `color-science`'s 72-file compute cluster stayed unified for the
   identical reason: its files "cross-cite densely… splitting it would make cross-pack consults the
   common case."
3. **Vocabulary separability** — do candidate children have orthogonal trigger tokens, or do they
   share one token field that would make sibling descriptions compete for the same words (the model
   routes on the description menu; siblings with identical vocabulary steal from each other —
   `/eval-run`'s *stolen* failure shape, measured)? `color-contrast-facts` survived at only
   8 files because APCA/WCAG/CVD/contrast is orthogonal to its siblings' vocabulary.
   `color-theory-facts`'s four axes all trigger on one field — clash/harmony/wheel/mood/communicate —
   entangled, not separable.
4. **Cost ledger** — only price this once 1–3 clear. Each new child costs: a description (≤1024
   chars, the open-standard cap) with NOT-clauses fencing every sibling; a re-derived eval suite; a
   CHANGELOG; and — the line most often skipped — every external referrer to the parent handle
   re-pointed by meaning (grep the whole corpus for the parent's handle *before* proposing anything;
   this is the blast-radius map `/skill-refactor` will need). Net the total against an
   identified retrieval benefit. No identified benefit plus a real cost is a no-split, regardless of
   how the request was phrased.

`references/foundations.md` derives why these four tests are the right ones (the router reads
descriptions, so vocabulary separability is not optional); `references/best-practices.md` walks
both worked cases in full, cited to their archival source plan documents.

## Procedure

1. **Survey before proposing anything.** Inventory the corpus (file count, dir structure, any
   existing axis table, INDEX size) and grep every external referrer to the parent handle across
   `skills/`, `agents/`, `CLAUDE.md`, `settings*.json`, and memory. This survey is deliverable even
   under a no-split verdict — it is the corpus's current blast-radius map either way.
2. **Run tests 1–3** against the corpus's actual content, citing files and lines — never impressions.
   Where an eval suite or routing corpus exists, build the query → axes-engaged table exactly as in
   `references/best-practices.md`'s worked example.
3. **If 1–3 clear**, propose N candidate packs: one line each (identity, file range, axis list, one
   worked consult). Explicitly test and reject over-fragmentation the same way the precedent did — a
   thin candidate axis, a candidate whose files pair densely with a sibling's, is named and killed,
   not silently dropped. Draft each child's description (≤1024 chars) and decide its invocation
   posture deliberately (skill-authoring-standards' dials — both, explicitly) — never leave it at
   the accidental default. Write the full file-mapping manifest: every source file assigned to
   exactly one child.
4. **Price the cost ledger** (test 4) and state the verdict — `split` (N packs, named), `no-split`,
   or `partial` (fewer packs than the axis table suggests) — with a "rejected alternatives" section
   naming every sub-split considered and why it failed, even under a `split` verdict (name what you
   did *not* further fragment).
5. **Validate mechanically before handing off:**
   `python3 scripts/manifest_check.py <manifest.json>` — every file assigned exactly once, no
   orphans, no duplicates, counts reconcile, each description ≤1024 chars, each pack's axis count
   flagged if outside 3–7. Fix and re-run until clean; never hand off an unreconciled manifest.
6. **Hand off, never execute.** The manifest + repair map go to `/pack-forge` (mint/grow each
   child's references/INDEX, wave by wave) and `/skill-forge` (each child's surface) and `/skill-refactor` (move, rewire every referrer, prove the sweep — from this manifest). For high-stakes splits, the `skill-auditor` agent scores the
   manifest against `references/rubric.md` before the host ratifies (generator ≠ critic).

## Worked precedent

Two dated, verified cases anchor this method — read in full via `references/best-practices.md`
(archival source docs cited there, external to this plugin):

- **Split warranted:** `color-science` (159 files) → four packs sized 72/49/8/30, with two candidate
  5th packs (a `palette` cluster, a `naming` cluster) explicitly rejected for routing dilution and
  shared-file coupling.
- **Split rejected:** `color-theory-facts` (28 files) tested against the identical four tests and failed
  1–3; the one arguable seam (wheel/history, the axis with the crispest independent vocabulary) was
  still rejected because the flagship ask spans it.

## Manifest schema

```jsonc
{
  "source_corpus": { "path": "skills/color-science", "total_files": 159 },
  "verdict": "split",                                    // "split" | "no-split" | "partial"
  "packs": [
    { "name": "color-space-facts", "files": ["references/techniques/oklab-xyz-math.md", "..."],
      "axes": ["spaces & conversions", "gamut & interpolation", "..."],
      "description": "...", "invocation_posture": "default" }
  ],
  "rejected_alternatives": [
    { "candidate": "color-science-palettes", "reason": "seam cuts through interpolation files shared with spaces; routing dilution against make-palette" }
  ],
  "referrer_repair_map": [
    { "file": "skills/check-colors/SKILL.md", "line": 3, "old": "color-science", "new": "color-space-facts" }
  ]
}
```

## Boundaries

- **This skill decides and designs; it never moves a file.** Authoring a child's actual
  references/INDEX is `/pack-forge`'s; executing the move, fence
  transfers, and referrer rewire is a refactor executed by `/skill-refactor` from the validated manifest.
- **Not a general decomposer.** A UI layout, technical architecture, or goal breakdown is
  `system-decompose`'s domain table — this skill is specific to knowledge-pack corpora being
  tested for a knowledge-family split.
- **Not its own inverse.** Consolidating several existing skills into one is `skill-synthesize`.

## Routing

| Peer | For |
|---|---|
| `skill-synthesize` | the inverse operation — merging several packs into one |
| `system-decompose` | a non-knowledge-pack decomposition (layout, architecture, goals) |
| `harness-audit` | the corpus-wide sweep that surfaces strained packs in the first place |
| `pack-forge` | minting or growing each resulting child's corpus |
| `skill-refactor` | executing this skill's manifest — moves, rewires, sweep proof |
| `skill-forge` | authoring each resulting child's SKILL.md surface |
| `skill-review` | scoring a child skill once authored |

## Done / NOT done

**Done** = every test run in order with cited evidence (not impressions), the manifest reconciles
(`manifest_check.py` clean), every external referrer enumerated even under a no-split verdict, each
child's description and invocation posture explicitly decided, and the handoff names both
downstream steps. **NOT done** = a split proposed without running tests 1–3 first, an unreconciled
manifest, a description over 1024 chars, an invocation posture left at the accidental default, or a
verdict that ignores what the corpus's own eval data says about ask co-occurrence.
