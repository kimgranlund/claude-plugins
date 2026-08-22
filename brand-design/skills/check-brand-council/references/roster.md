# check-brand-council — roster

Schema: `council-rules`' `references/roster-file-contract.md` (cited, not restated). This file is
the single source of truth for this council's membership; `SKILL.md`'s "Roster" section cites it
rather than restating the table. Seating a new critic is a row appended here (`make-critic` step
5) — a data edit, verified by `roster_check.py`, never a SKILL.md semantic edit.

| handle | sub-councils | role | status | seated | fixture |
|---|---|---|---|---|---|
| luke-s | strategy | lead | active | ported — brand-forge migration | unpromoted, inline |
| john-h | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| mark-p | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| brian-c | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| rory-s | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| paula-s | design | lead | active | ported — brand-forge migration | unpromoted, inline |
| massimo-v | design | member | active | ported — brand-forge migration | unpromoted, inline |
| matt-w | design | member | active | ported — brand-forge migration | unpromoted, inline |
| jessica-w | design | member | active | ported — brand-forge migration | unpromoted, inline |
| david-a | voice | lead | active | ported — brand-forge migration | unpromoted, inline |
| tim-d | voice | member | active | ported — brand-forge migration | unpromoted, inline |
| mary-n | voice | member | active | ported — brand-forge migration | unpromoted, inline |
| george-l | creative | member | active | ported — brand-forge migration; reseated voice→creative 2026-08-22 (#849) | unpromoted, inline |
| nick-l | creative | member | active | ported — brand-forge migration; reseated strategy→creative 2026-08-22 (#849) | unpromoted, inline |

`full` = the union of every active row above (`council-rules`' reserved-name convention — never a
literal value in the `sub-councils` column).

## `advisory` — reserved, seeded empty

`advisory` is this roster's second reserved sub-council (`roster-file-contract.md`'s `advisor`
role semantics) — **seeded with zero rows on purpose.** Unlike `strategy`/`design`/`voice`,
advisory personas are not shipped with the plugin: they are minted by the USER via `/make-critic`,
one at a time, as the standing home for a lens that doesn't fit an existing sub-council's family.
`roster_check.py` reports this as an INFO line, never a warning or failure — do not invent a row
here to make the table look populated. When a user mints their first advisor, its row lands here
with `role: advisor`, `sub-councils: advisory`, and nowhere else.

## `creative` — ordinary sub-council, partially seated

`creative` is an **ordinary** sub-council, unlike `advisory` — it is not a reserved name. Declared
2026-08-21 (`#840`) seeded empty, bench-seating ownership left open (Kim seats it later via
`/make-critic` or by reseating existing personas). Kim's 2026-08-21 vacancy ruling lifted for two
seats 2026-08-22 (`#849`): `george-l` (voice→creative) and `nick-l` (strategy→creative) are now
seated here — both lenses are structurally advertising-creative-direction (Big Idea concepting,
applied-creativity/creative-infrastructure), per the candidate mapping on `#849`'s own Findings.
`john-h` and `tim-d` were assessed as borderline creative-direction candidates in that same mapping
but stay in their current sub-councils (`strategy`, `voice`) — not seated. `rory-s` (`strategy`)
is the third member of `brand-advertising-facts`' role family (`role-pack-scaffolding.md`) and
still hasn't been re-seated — a future ticket's call, not this one's. `roster_check.py` no longer
reports `creative` as an empty-bench WARNING now that it seats two active members; `creative`
still has no designated `lead` (see Groups below), which remains its own separate `VACANT` warning.

## Groups

- leads: strategy=luke-s, design=paula-s, voice=david-a, creative=VACANT

Design (`paula-s`) and voice (`david-a`) leads designated 2026-08-21 (`#840`, post-build scope
addition). `creative` carries no designated lead — the LEAD seat stays VACANT even though the
bench itself is no longer empty (two members seated 2026-08-22, `#849`) — Kim assigns a lead
separately, later — do not invent one to fill the cell.

## Role agents

- chair: council-chair-agent
- strategy: strategy-convener
- design: design-convener
- voice: voice-convener
- creative: creative-convener

One addressable agent per council role (`council-rules`' `references/role-agents.md` — concept and
convene semantics, cited not restated): the Chair, plus one convener per ordinary sub-council.
`advisory` never appears here — it has no lead and no role agent of its own
(`role-agents.md`'s reserved-name rule). `creative-convener` now convenes a bench seating
`george-l` and `nick-l` (2026-08-22, `#849`) — no longer the empty-bench "no seats" case.
