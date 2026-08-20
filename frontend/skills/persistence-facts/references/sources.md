# Sources and provenance

This pack distills four independent, dated, read-only field-report corpora — not a live re-audit
of the four cited repos. Each corpus was authored 2026-08-20 by a dedicated reader session in its
own repo; this pack's own synthesis (2026-08-20) draws one axis apiece from four of them, per the
frontend knowledge series' master outline (ticket #807, itself citing the 2026-08-20 synthesis of
the same four report corpora that seeded `reactivity-facts` and `state-model-rules`).

## The four grounding files

| Axis | Repo | File consulted |
|---|---|---|
| `discipline-tiers.md` | `nonoun/ultimate-tokens` | `.claude/docs/reports/reactivity-2026-08-20/03-stores-and-persistence.md` |
| `dual-contracts.md` | `nonoun/agent-ui` | `.claude/docs/reports/data-model-review-2026-08-20/data-persistence-layers.md` |
| `persistence-audit-shape.md` | `nonoun/agent-ui` + `adia/gen-ui-kit` | `data-persistence-layers.md` (bypass table) + `.claude/docs/reports/2026-08-20-reactivity-review/02-web-modules-state.md` + `INDEX.md` (F8) |
| `url-state-sync.md` | `adia/adia-v2` | `.claude/docs/reports/2026-08-20-reactivity-data-audit/06-url-state-sync-patterns.md` |

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary field-report file cited above, on
  2026-08-20 (this pack's authoring date). Every substantive claim in this pack's four axis files
  carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated, real (not hypothetical) failure the source
  material itself documents as having actually occurred or as currently, confirmedly live in
  production code (e.g. the pre-RENAME_MAPS voice-taxonomy data loss; the confirmed live
  multi-value-comma bug). Distinguished from [verified] because the evidentiary weight is "this
  actually broke or is still broken," not just "this is what the code currently does."

No claim in this pack is [inferred] as of authoring — every axis traces to a specific report
section or file:line the source corpus itself cites. If a cited repo's code changes after
2026-08-20, this pack's specific file:line citations become [drift-prone] and should be
re-verified at the next refresh boundary rather than assumed current.

## What this pack deliberately does NOT re-verify

This pack distills the four corpora's own stated findings; it does not independently re-read the
full source tree of any of the four repos. Where a corpus states a verdict in its own words (e.g.
agent-ui's "built-but-unadopted" / "load-bearing, real" classification), this pack cites that
verdict rather than re-deriving it from a fresh read. A reader confirming one specific claim
against CURRENT code should re-read the cited file:line in the named repo, not treat this pack as
a live source of truth for a moving codebase.

## Fence provenance

The persistence-vs-state-architecture and persistence-vs-reactivity fences in this pack's SKILL.md
were negotiated against the two sibling packs already shipped in this series
(`reactivity-facts`, wave 1; `state-model-rules`, wave 2) — see this pack's own Boundaries section
and each sibling's own updated Boundaries bullet naming this pack in return.

Extension: governed by [[make-pack]]
