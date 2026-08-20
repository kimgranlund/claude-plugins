# Sources and provenance

This pack distills three independent, dated read-only field-report corpora and their cited
source files — not a live re-audit. All three corpora were authored 2026-08-20, on a different
repo, by a dedicated reader session investigating the identical operator symptom ("there seems to
be a mix of implementations now"); this pack's own synthesis (2026-08-20) draws the cross-corpus
judgment calls out of all three.

## The three corpora

| Repo | Corpus | Files consulted for this pack |
|---|---|---|
| `nonoun/agent-ui` | `.claude/docs/reports/data-model-review-2026-08-20/` | `FINDINGS.md` (the incident spine), `agent-admin-app-state-audit.md` (primary — four-generations, sync-point map), `select-menu-name-bug.md` (primary — the tagged-union case study), `data-persistence-layers.md` (primary — adoption verdict), `framework-state-idioms.md` (primary — never-pulled trigger) |
| `adia/gen-ui-kit` | `.claude/docs/reports/2026-08-20-reactivity-review/` | `INDEX.md` (primary — the layered coherence map, the F1/F3 findings, R1–R8 recommendations), `04-doctrine-vs-practice.md` (primary — the ratified-rules inventory and the doctrine-internal contradictions), `03-app-layer-stores.md` (the duplicated-store/race-control detail behind INDEX.md's F2) |
| `adia/adia-v2` | `.claude/docs/reports/2026-08-20-reactivity-data-audit/` | `00-index.md` (primary — the "fixed once, not swept" meta-pattern and the confirmed live bug) |

This pack deliberately does NOT draw on the fourth wave-1 corpus (`nonoun/ultimate-tokens`'s
`reactivity-2026-08-20/`) — that corpus's synthesis is reactivity MECHANISM territory, already
distilled into the sibling pack `reactivity-facts`; re-citing it here would blur this pack's own
architecture-judgment boundary.

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary field-report file, or against the actual
  source file the report cites, on 2026-08-20 (this pack's authoring date). Every substantive
  claim in this pack's seven axis files carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated real-world case the source material itself
  investigated (e.g. the agent-select-menu stale-name bug, the `data-stream-src` double-fetch
  hazard, the comma-encoding URL-state bug). Distinguished from [verified] because the
  evidentiary weight is "this actually happened/broke," not just "this is what the report/code
  currently states."

No claim in this pack is [inferred] or [drift-prone] as of authoring — every axis traces to a
specific file:line or a corpus's own explicit verdict sentence, quoted or closely paraphrased. If
a cited repo's code or reports change after 2026-08-20, the specific file:line citations in this
pack become [drift-prone] and should be re-verified at the next refresh boundary rather than
assumed current.

## What this pack deliberately does NOT re-verify

This pack is a DISTILLATION of the three corpora's own judgment calls, not an independent
re-audit of the three cited repos. Where a corpus itself states a finding as its own verdict
(e.g. "the mix is real but concentrated in three places" — gen-ui-kit `INDEX.md`), this pack
cites that verdict rather than re-deriving it from a fresh read of the full source tree. A reader
who needs to confirm a specific claim against CURRENT code should re-read the cited file:line, not
treat this pack as a live source of truth for a moving codebase.

Extension: governed by [[make-pack]]
