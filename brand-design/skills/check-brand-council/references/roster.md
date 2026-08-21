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
| nick-l | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| brian-c | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| rory-s | strategy | member | active | ported — brand-forge migration | unpromoted, inline |
| paula-s | design | member | active | ported — brand-forge migration | unpromoted, inline |
| massimo-v | design | member | active | ported — brand-forge migration | unpromoted, inline |
| matt-w | design | member | active | ported — brand-forge migration | unpromoted, inline |
| jessica-w | design | member | active | ported — brand-forge migration | unpromoted, inline |
| david-a | voice | member | active | ported — brand-forge migration | unpromoted, inline |
| george-l | voice | member | active | ported — brand-forge migration | unpromoted, inline |
| tim-d | voice | member | active | ported — brand-forge migration | unpromoted, inline |
| mary-n | voice | member | active | ported — brand-forge migration | unpromoted, inline |

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

## `creative` — ordinary sub-council, seeded empty

`creative` is an **ordinary** sub-council, unlike `advisory` — it is not a reserved name, it is
just newly declared with nobody minted into it yet (ruled 2026-08-21, `#840`: bench-seating
ownership stays open, Kim seats it later via `/make-critic` or by reseating existing personas).
`roster_check.py` reports its emptiness as a **named WARNING**, the same severity a `VACANT` lead
already gets — never the quieter INFO `advisory` gets, since `advisory`'s emptiness is that
reserved sub-council's own permanent normal state where `creative`'s is an ordinary sub-council
expected to fill. Do not invent a row here to clear the warning.

## Groups

- leads: strategy=luke-s, design=VACANT, voice=VACANT, creative=VACANT

Design, voice, and creative carry no designated lead as of this roster's creation/extension
(2026-08-21, `#838`/`#840`) — Kim designates them later; do not invent a lead to fill the cell.

## Role agents

- chair: council-chair-agent
- strategy: council-strategy-agent
- design: council-design-agent
- voice: council-voice-agent
- creative: council-creative-agent

One addressable agent per council role (`council-rules`' `references/role-agents.md` — concept and
convene semantics, cited not restated): the Chair, plus one per ordinary sub-council. `advisory`
never appears here — it has no lead and no role agent of its own
(`role-agents.md`'s reserved-name rule). `council-creative-agent` convenes a bench that is
currently empty — dispatched today, it reports "no seats" and stops cleanly, exactly as
`check-brand-council` already does when `advisory` is convened directly with zero seated critics.
