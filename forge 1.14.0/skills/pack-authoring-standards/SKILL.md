---
name: pack-authoring-standards
description: >-
  Standards for authoring knowledge-pack corpora — the references/ content behind a knowledge
  skill: retrieval axes, the INDEX file, load discipline, citation and grounding rules, research
  waves, and snapshot freshness. Use when the user asks how to structure a reference corpus or
  INDEX, how many axes or files a pack should have, how to ground or cite reference content, how to
  run a research wave to fill a corpus, why retrieval from a pack feels muddy, or how to keep
  corpus snapshots from going stale. NOT for the pack's SKILL.md surface, description, or dials
  (skill-authoring-standards); NOT for deciding a split or merge (skill-decompose /
  skill-synthesize); NOT the workflow that executes a research wave (pack-forge runs it; this
  carries the rules it runs under).
disable-model-invocation: false
user-invocable: false
---

# Pack Authoring Standards

A knowledge pack is a corpus with a retrieval contract: `references/` files organized by *question
type*, an INDEX that maps asks to files, and a SKILL.md surface (owned by
`skill-authoring-standards`) thin enough to point rather than carry. This is the standard
`/pack-forge` builds against, `corpus_check.py` enforces the checkable slice of, and the
decompose/synthesize tests presuppose. Provenance: the axis and wave doctrine is imported from the
source-corpus lineage (the `color-science`/`ui-patterns` practice, worked cases in
`skill-decompose/references/`); the freshness and grounding rules are this project's own earned
practice — none of it is platform-verified fact, all of it is [battle-tested convention]
(amended 2026-07-15: the [incident] class and severity-ranked INDEX ordering are grounded in
external type specimens, cited inline at their rules — no longer solely this project's practice).

## The unit is the question type

Files are ask-shaped, never literature-shaped. "Which contrast standard applies" is a file;
"WCAG 2.2 (notes)" is a dump. The test before writing any file: *what question does a reader arrive
with, and does this file answer it without forcing three sibling loads?* Four lenses on one
question are one axis, however many sources they cite; two genuinely different question types never
share a file, however related their subject.

## Axes: 3–7, declared, drift-checked

A pack holds 3–7 retrieval axes — below 3 it's usually one axis padded (or a merge candidate,
`skill-synthesize`); above 7 the entry surface strains (a split signal, `skill-decompose`). Axes
are declared in the INDEX as its section headings, and the SKILL.md consult table mirrors the axis SET (ordering is INDEX-local; see below). A
stated axis or file count that has drifted from the tree is the first strain signal — which is why
`corpus_check.py` reconciles counts mechanically instead of trusting prose.

## INDEX.md: the retrieval map — when the consult table stops being one

The threshold is **enumerability, not authoring method** (ruled 2026-07-09, reconciling this
standard with knowledge-forge's scaling note and the shipped practice — ui-patterns,
motion-design, iconography): when the SKILL.md consult table lists every reference file 1:1
(a flat corpus of ≤~7 files), the table IS the retrieval map and a separate INDEX would be a
second copy that drifts — ship no INDEX. An INDEX.md earns its keep the moment files outgrow
what the table enumerates or `references/` grows subdirectories (the color-science family,
ui-genres). Then: one line per reference file — `path — the question it answers (≤ 1 line)` —
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

## Snapshots and freshness

When a corpus is mirrored outward (project knowledge, docs bundles), the pack is the source of
record and every copy is a headed snapshot naming its source path and refresh date. Snapshots
refresh at release boundaries — a stale snapshot is worse than none, because it answers with
authority it no longer has. The [drift-prone] inventory is the refresh checklist.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Literature-shaped files | Organized by source, not ask → every query loads everything | Rewrite by question type; the ask is the filename test |
| INDEX drift | Tree changed, map didn't → ghost routes and unreachable files | `corpus_check.py` reconciles both directions; run at write and gate time |
| Orphan claims | No source, date, or confidence marker → unverifiable authority | Grounding markers on every claim; waves gather with dates |
| Corpus-less knowledge skill | Description promises what references/ can't back | skill-forge flags the gap; `/pack-forge` fills it before ship |
| Heroic single wave | Gathering outruns distillation → dump with citations | One axis per wave; register before starting the next |
| Stale snapshot | Copy outlives its source's truth | Headed snapshots, refresh at release, [drift-prone] as the checklist |
| Axis sprawl | 8+ axes accrete silently | Declared axes + count reconciliation; past 7, run skill-decompose |

## Provenance

Axis/wave doctrine: imported from the source-corpus lineage 2026-07-07 (worked cases:
`skill-decompose/references/best-practices.md`). Grounding, amendment, and snapshot rules: this
project's practice, 2026-07; amended 2026-07-15 — the [incident] class and severity-ranked INDEX
ordering enter from the external-skill review's type specimens, cited inline. Surface rules: `skill-authoring-standards`. Split/merge decisions:
`skill-decompose` / `skill-synthesize`. The executing workflow: `pack-forge`.
