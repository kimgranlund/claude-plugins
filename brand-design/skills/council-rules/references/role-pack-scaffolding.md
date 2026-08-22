# Role-pack scaffolding — the shared template behind the four `*-facts` grounding packs

`brand-advertising-facts`, `brand-identity-facts`, `brand-strategy-facts`, and `brand-voice-facts`
(S5, `#828`) are four instances of the same knowledge-pack shape: `make-critic`'s grounding corpus
for one role family of `check-brand-council` critics. This file states the shape ONCE — the
declared-axes framing, the retrieval discipline, and the Ask/Load table template — so the four
packs cite it instead of restating it byte-for-byte (centralized 2026-08-21, S2 of the
plan-2026-08-brand-design-bloat-overhaul dedup, `#845`).

## Declared-axes framing

The template's framing: "4 declared axes (pack-writing-rules' 3-7 threshold) across 4 axis files
(`lenses`/`failure-modes`/`canonical-tests`/`vocabulary`), plus `sources.md` for provenance — five
reference files total, flat corpus — this table is the retrieval map (no INDEX needed at this
size)." Identical across all four packs by design — the axis/file count is a property of the
shared TEMPLATE, not of any one pack's critic count.

## Retrieval discipline

The template supplies each pack's framing: "Enter by search: Grep the mapped file for the term,
then Read that section — never read the folder start-to-finish. Every consult answers as claim +
the cited reference file + its grounding marker (`[verified]` against a persona file, or
`[inferred]` and marked as such)." Each pack pairs this with its own one-line worked example,
cited near its Consult table pointer — the example is pack-specific and stays local, never
centralized here.

## Ask / Load table template

| Ask | Load |
|---|---|
| The **N** lenses themselves — what each critic interrogates and why | `references/lenses.md` |
| The specific defects this family catches | `references/failure-modes.md` |
| The concrete, repeatable diagnostic tests | `references/canonical-tests.md` |
| The family's shared working vocabulary | `references/vocabulary.md` |
| Provenance — trust order, what's verified vs. general knowledge | `references/sources.md` |

**N is the per-pack critic count — stated here once so it can never drift out of sync with the
roster again** (the live three-vs-four-lens copy-drift this centralization fixes):

| Pack | N (lenses = critics in that role family) | Critics |
|---|---|---|
| `brand-advertising-facts` | 3 | george-l, nick-l, rory-s |
| `brand-identity-facts` | 4 | jessica-w, massimo-v, matt-w, paula-s |
| `brand-strategy-facts` | 4 | brian-c, john-h, luke-s, mark-p |
| `brand-voice-facts` | 3 | david-a, mary-n, tim-d |

**This is a different grouping than the roster's own sub-council seating** (`check-brand-council`'s
`references/roster.md`): today the 14 ported critics sit in four ordinary sub-councils
(`strategy`: 5, `design`: 4, `voice`: 3, `creative`: 2) — `creative`, declared 2026-08-21 (`#840`)
seeded empty, is the roster's own slot for the advertising-creative role family this pack
(`brand-advertising-facts`) grounds; two of its three critics, george-l and nick-l, were re-seated
out of their legacy `voice`/`strategy` rows into `creative` 2026-08-22 (`#849`, Kim's vacancy
ruling lifted for those two seats). The third, rory-s, stays in `strategy` — not yet re-seated,
still a live call for a future ticket. `creative` carries no designated lead (VACANT). There is
also the reserved, non-voting `advisory` sub-council (seeded with zero critics on purpose). The two
axes are deliberately independent: role-family packs group by JUDGMENT LENS (what a critic reads
before drafting or overlap-checking), sub-councils group by VOTING MEMBERSHIP — `creative` now
seating two of its three role-family critics means the roster is most of the way to converging on
the same four-family shape once rory-s's re-seat lands, if it does. Neither table restates the
other; a "why isn't rory-s seated in `creative` yet" question routes to `roster-file-contract.md`'s
sub-council model and a live re-seat ticket, not here.

## Extending this template

A fifth role-family pack, or a change to the shared reference-file set (`lenses.md`/
`failure-modes.md`/`canonical-tests.md`/`vocabulary.md`/`sources.md`), updates this file first,
then each pack's one-line pointer. Never re-fork the paragraphs back into an individual pack.
