---
name: pack-writing-rules
description: >-
  Standards for authoring a knowledge skill's references/ corpus. Use when structuring a corpus
  or INDEX, sizing axes, citing/grounding reference content, how to run a research wave, muddy
  retrieval, or keeping snapshots from going stale. NOT for the pack's SKILL.md surface
  (skill-writing-rules); NOT a split/merge decision (plan-skill-split); NOT for executing a
  research wave (make-pack).
disable-model-invocation: false
user-invocable: false
---

# Pack Authoring Standards

A knowledge pack is a corpus with a retrieval contract: `references/` files organized by *question
type*, an INDEX that maps asks to files, and a SKILL.md surface (owned by
`skill-writing-rules`) thin enough to point rather than carry. This is the standard
`/make-pack` builds against, `corpus_check.py` enforces the checkable slice of, and the
decompose/synthesize tests presuppose. Provenance: the axis and wave doctrine is imported from the
source-corpus lineage (the `color-science`/`ui-pattern-facts` practice, worked cases in
`plan-skill-split/references/`); the freshness and grounding rules are this project's own earned
practice — none of it is platform-verified fact, all of it is [battle-tested convention]
(amended 2026-07-15: the [incident] class and severity-ranked INDEX ordering are grounded in
external type specimens, cited inline at their rules — no longer solely this project's practice;
amended 2026-07-18: the canonical-reachability check is translated from an external type specimen
the same way, cited inline where it lives).

## The unit is the question type

Files are ask-shaped, never literature-shaped. "Which contrast standard applies" is a file;
"WCAG 2.2 (notes)" is a dump. The test before writing any file: *what question does a reader arrive
with, and does this file answer it without forcing three sibling loads?* Four lenses on one
question are one axis, however many sources they cite; two genuinely different question types never
share a file, however related their subject.

## Axes: 3–7, declared, drift-checked

A pack holds 3–7 retrieval axes — below 3 it's usually one axis padded (or a merge candidate,
`plan-skill-merge`); above 7 the entry surface strains (a split signal, `plan-skill-split`). Axes
are declared in the INDEX as its section headings, and the SKILL.md consult table mirrors the axis SET (ordering is INDEX-local; see below). A
stated axis or file count that has drifted from the tree is the first strain signal — which is why
`corpus_check.py` reconciles counts mechanically instead of trusting prose.

## INDEX.md: the retrieval map — when the consult table stops being one

The threshold is **enumerability, not authoring method** (ruled 2026-07-09, reconciling this
standard with the shipped practice — ui-pattern-facts, motion-rules, icon-rules — and, historically,
docs' now-retired knowledge-forge's scaling note, folded in here 2026-07-19): when the SKILL.md consult table lists every reference file 1:1
(a flat corpus of ≤~7 files), the table IS the retrieval map and a separate INDEX would be a
second copy that drifts — ship no INDEX. An INDEX.md earns its keep the moment files outgrow
what the table enumerates or `references/` grows subdirectories (the color-science family,
ui-genre-facts). Then: one line per reference file — `path — the question it answers (≤ 1 line)` —
grouped under axis headings; the INDEX loads *first*, files load on demand from it. Where the
axes have a natural severity or impact order (a rules corpus tiered CRITICAL→LOW), the INDEX
orders its axis headings by that severity — triage order becomes structural instead of a
convention the reader must remember (added 2026-07-15; type specimen:
vercel-labs/agent-skills@f8a72b960's async-CRITICAL → advanced-LOW prefix ladder); topic-only
corpora keep topical order, never a faked ranking.

Budget: an INDEX pushing past ~150 lines is a pack answering too many kinds of question. Every file in
`references/` appears in the INDEX and every INDEX line names a real file — zero tolerance both
directions, because a ghost line misroutes and an unlisted file is unreachable.

## Load discipline

Files stay under ~1000 lines; past that, retrieval degrades into Grep-first archaeology and the
file is flagged for an ask-shaped split. The SKILL.md body carries a consult table (ask-pattern →
INDEX section), never content — under compaction only a skill's head survives, so a body that
points survives compaction intact while a body that carries gets truncated mid-claim.

## Grounding: every claim wears its grounding marker

Reference content states where each claim came from and how much to trust it:

- **[verified]** — checked against a primary source, dated. Cite the source and the check date.
- **[inferred]** — derived, not confirmed; say from what.
- **[drift-prone]** — true now, expiring; these are the refresh list at every release boundary.
- **[incident]** — a dated real-world failure grounding a rule: who, when, what broke, what the
  rule would have prevented (added 2026-07-15; type specimen: the Vercel dropped-frames incident
  cited in emilkowalski/skills@6bf24434f). Not decoration — an incident is causal evidence a rule
  paid rent, and survives the deletion test on evidentiary value; an undated anecdote is not this
  class, it is an orphan wearing a story.

A claim with none of these is an orphan; a corpus of orphans is vibes with a directory structure.
When a claim is corrected, the old text is amended in place with a dated note (the correction is
itself auditable), never silently rewritten — this project's own §6.6 falsification is the model.

## Research waves: how corpora get filled

A wave is the unit of corpus growth, and it is question-led, not source-led:

1. **Question set first** — the wave's deliverable list is the asks the new files must answer,
   written before any searching (the evals-first principle at corpus scale).
2. **Gather with dates** — sources collected per question cluster; every capture carries its date
   and origin, because ungrounded gathering produces orphan claims by construction.
3. **Distill ask-shaped** — one file per question type, grounding-marked, within load budgets.
4. **Register** — INDEX lines, consult-table row, and the pack's eval suite gains the new axis's
   trigger phrasings in the same change (an unregistered file is unreachable; an unrouted axis is
   invisible).

Wave sizing: one axis per wave is the healthy default; a whole-pack mint is 3–7 waves, not one
heroic pass — distillation quality collapses when gathering outruns it.

## Extension citation

A pack's own SKILL.md states, once, where growth requests route: "a missing axis, a stale
reference, or 'add X to this pack' is authoring work — route to `/make-pack`." Every pack cites
that routing rule with a one-line footer — `Extension: governed by [[make-pack]]` — never restates
it as a paragraph. The rule lives here, once; a pack's footer points to it. Restating the paragraph per pack is how it silently re-diverges the
next time either source changes wording (found via the #258 bloat-audit sweep, 2026-08-16: 28
packs across five plugins carrying a byte-identical stamped paragraph).

## Snapshots and freshness

When a corpus is mirrored outward (project knowledge, docs bundles), the pack is the source of
record and every copy is a headed snapshot naming its source path and refresh date. Snapshots
refresh at release boundaries — a stale snapshot is worse than none, because it answers with
authority it no longer has. The [drift-prone] inventory is the refresh checklist.

## Canonical means reachable from every surface the estate builds

A "canonical" artifact — a spec, a decision, a reference file, a corpus entry — that isn't actually
*reachable* is canon in name only. The check translates five generic surfaces into this estate's
own equivalents: a sitemap/nav (the SKILL.md consult table), a corpus/search index (INDEX.md, where
one ships), a harvester/generator's input list (the eval suite's trigger phrasings), the
import/mention graph (`[[handle]]`/preload references), and self-documentation (the file naming
itself canonical in frontmatter or a header). An artifact reachable from every surface the estate
actually builds for its class is canon; missing one of *those* ⇒ treat it as a draft, a dead
branch, or a currency lapse (canon that fell off a surface and was never refreshed), not canon —
the label alone never carries the artifact's weight. A surface the estate doesn't build for that
class at all (a flat ≤~7-file pack ships no INDEX by the 2026-07-09 ruling above; packs have no
standing harvester; no reference file anywhere in this workspace currently self-documents as
canonical — verified against the full corpus, not assumed — so self-documentation is N/A estate-wide
until a convention for it exists) is N/A, not a miss — the detector counts what should exist, never
penalizes an absence this standard itself already sanctions. The moment any class adopts one of
these surfaces for real (an INDEX ships, a self-canonical header convention starts), that surface
stops being N/A for that class and starts counting.

This composes with, not replaces, the estate's existing single-surface reachability checks (the
INDEX/tree reconciliation above, `corpus_check.py`'s K1, `release_gate.py`'s G5/G8/G9,
`plan-plugin-split`'s `surface_map.py` orphan sweep) — each of those enforces *one* surface; this is
the threshold for how many of the applicable surfaces a claim of canonicity actually needs before it
counts (added 2026-07-18; type specimen: adia-ui-kit v3.7.13's
`references/reasoning-methodologies.md` method #5, via kimgranlund/claude-plugins#40 — the source
estate's docs monolith carried a real sitemap, search index, and harvester, so its literal ≥5
threshold is translated here, not copied verbatim).

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Literature-shaped files | Organized by source, not ask → every query loads everything | Rewrite by question type; the ask is the filename test |
| INDEX drift | Tree changed, map didn't → ghost routes and unreachable files | `corpus_check.py` reconciles both directions; run at write and gate time |
| Orphan claims | No source, date, or confidence marker → unverifiable authority | Grounding markers on every claim; waves gather with dates |
| Corpus-less knowledge skill | Description promises what references/ can't back | make-skill flags the gap; `/make-pack` fills it before ship |
| Heroic single wave | Gathering outruns distillation → dump with citations | One axis per wave; register before starting the next |
| Stale snapshot | Copy outlives its source's truth | Headed snapshots, refresh at release, [drift-prone] as the checklist |
| Axis sprawl | 8+ axes accrete silently | Declared axes + count reconciliation; past 7, run plan-skill-split |
| Fake-canonical artifact | Labeled canon but missing an applicable surface: sitemap/nav, corpus index, harvester input, import graph, self-doc | Treat as draft/dead-branch/currency-lapse; don't cite as authority until every surface the estate builds for its class reaches it |

## Provenance

Axis/wave doctrine: imported from the source-corpus lineage 2026-07-07 (worked cases:
`plan-skill-split/references/best-practices.md`). Grounding, amendment, and snapshot rules: this
project's practice, 2026-07; amended 2026-07-15 — the [incident] class and severity-ranked INDEX
ordering enter from the external-skill review's type specimens, cited inline. Amended 2026-07-18 —
the canonical-reachability check enters from adia-ui-kit v3.7.13's `reasoning-methodologies.md`
method #5 (harvested via kimgranlund/claude-plugins#40), its literal ≥5 threshold translated to this
estate's own surfaces rather than copied verbatim. Amended 2026-07-18 (same day, a fresh `/review`
pass on that change) — the self-documentation surface named a third N/A example, verified against
the full `references/*.md` corpus: no file anywhere currently satisfies it, and the original edit's
N/A carve-out named only two of the three surfaces the estate doesn't yet build (issue #48). Surface rules: `skill-writing-rules`. Split/merge decisions:
`plan-skill-split` / `plan-skill-merge`. The executing workflow: `make-pack`.
