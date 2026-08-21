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

`full` = the union of all 14 active rows above (`council-rules`' reserved-name convention — never
a literal value in the `sub-councils` column).

## Groups

- leads: strategy=luke-s, design=VACANT, voice=VACANT

Design and voice carry no designated lead as of this roster's creation (2026-08-21, `#838`) — Kim
designates them later; do not invent a lead to fill the cell.
