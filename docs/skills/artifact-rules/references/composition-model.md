# Composition model — record layers to chapter/section patterns

The question this file answers: **when the content source is a project's own records tree rather
than a prose draft, how does `make-artifact` compose page content from those records?** This is
the third content-source class, alongside a report/retro draft and pre-written handbook chapters
(`content-structure.md`'s classification test) — the composition phase READS the target project's
`.claude/docs/` records and GENERATES the section structure from them; it never renders prose it
wasn't given. The Estate Handbook is the reference shape (lld-0013's v2 extension, Resolution 8,
#649).

## Where this runs

`make-artifact`'s **Phase 1b** — after input location (Phase 1), before the CSS build (Phase 2).
Fires only when the content source IS a records tree; a prose draft or pre-written handbook
chapters skip this phase entirely and proceed straight to Phase 2 exactly as before.

## The layer → section map

| Record layer | Sources read | Section pattern |
|---|---|---|
| Intent | brief, `idr-*` | Opening chapter — thesis/why (hero-as-thesis, per `design:artifact-styling-rules`' `shells-and-genres.md`) |
| User Stories | `prd-*`, `rdd-*` | Capability chapters, one section per story/commitment |
| Concepts | `adr-*`, reference docs | Concept chapters — one mechanism-first mermaid per resolved decision fork, never a chip-wall of decisions |
| Systems & Architectures | `spec-*`, `lld-*`, plus harness-facts/project-facts harvest output **where present** | Architecture chapters — mechanism diagrams over inventory walls |

- **Hard inputs are the record types themselves** — brief/IDR/PRD/ADR/SPEC/LLD. Harvest output
  (#612/#613's capability) is **optional-where-present, never a hard edge** — ratified in #649's
  Findings (2026-08-18, Q2): a project with no harvest output still composes fully from the record
  types alone; harvest output, where it exists, folds into the Architecture chapters as additional
  source material, not a gate on whether composition runs at all.
- **Diagrams are mechanism-first**, per `design:artifact-styling-rules`' `mermaid-reference.md`
  (the styling doctrine, cited not restated here) — this phase decides
  WHICH mechanism earns a diagram (one per resolved decision fork or architecture, never a diagram
  per record just because a record exists); the styling pack owns how it renders. A concept or
  system chapter with nothing mechanism-shaped to diagram stays prose-only rather than manufacturing
  a diagram to fill the slot.
- **One section per story/commitment, one mermaid per resolved fork** — the map is a *pattern*, not
  a fixed page count: a project with three ADRs gets three concept sections (or fewer, where two
  ADRs resolve the same fork and read better merged — named in the Done report either way), not a
  padded four.

## Degradation: a non-canonical records tree

A target project's records tree that doesn't follow the canonical `.claude/docs/` type-prefix
layout (`adr-*`/`idr-*`/`prd-*`/`rdd-*`/`spec-*`/`lld-*`) starves this phase — there is nothing
typed to scan. The composition phase then degrades to the **prose-draft path** (Phase 2 runs
directly against whatever content was actually supplied), with the degradation **named in the
page's provenance footer** (`refresh-procedure.md`'s footer contract) — never a silent fallback and
never a build failure (R-6, lld-0013 v2).

## Interface

- **Consumes:** read-only globs over the target project's `.claude/docs/**` (plus harvest output
  where present); no writes, no schema demanded beyond the canonical type prefixes.
- **Feeds:** the assembled section outline handed to Phase 3 (shell choice) and Phase 4 (assembly +
  mermaid) exactly as a prose draft would — the composition phase's job ends at producing that
  outline; it never chooses the shell itself (`content-structure.md`'s classification stays the
  authority for that).
- **Relationship to `content-structure.md`:** that file classifies WHICH shell one already-given
  content source gets (report/retro vs handbook vs both); this file GENERATES the content in the
  first place, once per section, from typed records — `content-structure.md` line 22's own forward
  pointer names this file as the seam it reserved.

Extension: governed by [[make-pack]].
