# Roster file contract

A council instance's roster — who sits on it, which sub-councils they belong to, who leads each
one, and any named groups — lives in ONE data file, `references/roster.md`, inside that council's
own skill directory (e.g. `check-brand-council/references/roster.md`). The convening skill's own
SKILL.md **cites this file** for its roster instead of restating the table in prose — seating a
new critic becomes a row appended to `roster.md`, a data edit, never a SKILL.md semantic edit
(`plugin-authoring.md`'s checker-pass invariant does not fire on a data-only change).

## Format: a table, plus a `## Groups` section

```
| handle | sub-councils | role | status | seated | fixture |
|---|---|---|---|---|---|
| luke-s | strategy | lead | active | 2026-08-13 | calibration/critic-luke-s.md |
| ...
```

- **`handle`** — the persona's roster handle. Must satisfy the bijection: a roster row's handle
  has a matching `references/critics/critic-<handle>.md` file, and every persona file in that
  directory has a matching roster row. No orphan file, no phantom row.
- **`sub-councils`** — comma-separated sub-council names this handle sits in (e.g. `strategy`, or
  `strategy,voice` for a handle spanning two). **Never empty** — every seated handle sits in at
  least one sub-council. **`full` is RESERVED** and never appears as a value in this column: it is
  the computed union of every active row (`roster-and-personas.md`'s reserved-name convention),
  not a membership a row opts into. **`advisory` is the second RESERVED sub-council name** — unlike
  `full`, it DOES appear as a literal value, but only on `advisor`-role rows — see "Reserved:
  `advisory` and the `advisor` role" below.
- **`role`** — `lead`, `member`, or `advisor`. At most one `lead` row per sub-council. A sub-council
  may legitimately have no `lead` row (an unfilled seat) — see Groups below for how that's
  declared, never left implicit. `role: advisor` is reserved for `advisory`-seated rows — see
  below; it never appears alongside `lead`/`member`'s ordinary sub-councils.
- **`status`** — `active` or `retired`. A `retired` handle's persona file stays on disk as
  history but is excluded from `full` and from every sub-council's live fan-out.
- **`seated`** — the date or provenance note this critic joined (`2026-08-13`, or a migration note
  like `ported — brand-forge`). Never empty; every seat states its own origin.
- **`fixture`** — the calibration fixture proving this critic's lens (`make-critic` step 6): a
  path, or an explicit `unpromoted, inline` note. Never empty.

### `## Groups`

A second section lists named handle-sets that are not sub-councils. The contract's one required
group is **`leads`** — one entry per sub-council, naming that sub-council's lead handle, or the
literal `VACANT` when the seat is unfilled:

```
## Groups

- leads: strategy=luke-s, design=VACANT, voice=VACANT
```

A group entry resolves only to handles already present in the table (or the literal `VACANT`) —
never a bare sub-council name, never an invented handle not seated in the table above.

## Reserved: `advisory` and the `advisor` role

`advisory` is a second reserved sub-council name, alongside `full`, but with the opposite default:
where `full` is always non-empty (the union of everything else), `advisory` is legitimately —
and, until a user mints its first member, expectedly — **empty**. It exists for personas a USER
mints via `make-critic` rather than ones the plugin ships seated: a lens that doesn't fit an
existing sub-council's own family lands here by default (`make-critic`'s own procedure), never
forced into an ill-fitting `strategy`/`design`/`voice` row and never left unminted for want of a
home.

A row seated in `advisory` carries `role: advisor` — and the pairing is exact and bidirectional: a
row's `sub-councils` cell contains `advisory` **if and only if** its `role` is `advisor` (an
advisor never also carries `lead`/`member` in some other sub-council on the same row; a
`lead`/`member` row never lists `advisory`). There is no `advisory` lead — the sub-council is not
adversarial, so it has no seat to contest for leadership.

An advisor rides along in the fan-out whenever `full` is convened (an active `advisory` row is an
active roster row like any other) and whenever `advisory` is convened directly. Its findings are
marked **ADVISORY** at collection and feed every domain instance's synthesis shapes on the same
footing as any other finding — advisory informs the verdict. But an advisor's finding is **excluded
from 2-of-3 contested-severity voting** (`references/severity-and-voting.md`) — never itself the
contested finding, never one of the three votes cast to resolve a peer's — and excluded from
whatever adversarial-calibration floor a domain instance's own severity section states (e.g. a
"push for ≥1 Critical + 2 Major" convention): advisory never gates the verdict, it only informs it.

## `## Role agents` — the second required section

A second required section, alongside `## Groups`, names which addressable **role agent**
(`role-agents.md` — concept and convene semantics, cited not restated) an external caller
dispatches for each council role: the Chair, plus one per **ordinary** sub-council.

```
## Role agents

- chair: council-chair-agent
- strategy: strategy-convener
- design: design-convener
- voice: voice-convener
- creative: creative-convener
```

- **Keys** — the literal `chair`, plus one row per ordinary sub-council, using the exact same
  lowercase tokens the `sub-councils` column and the `## Groups` `leads:` entry already use. The
  set of ordinary sub-councils this section may name is exactly the set of keys the `leads:` entry
  declares (`## Groups`, above) — a sub-council present in one but not the other is a schema
  mismatch. **`full` and `advisory` are never keys here** — the same reservation
  `role-agents.md`'s "reserved-name rule" states, applied to this section: neither has a role agent
  of its own.
- **Value** — the agent's `name:` handle (e.g. `strategy-convener`), resolved against that
  handle's own file, `agents/<handle>.md`, **under the council skill's own plugin root** (a sibling
  of the plugin's `skills/` directory, never a path written here) — a handle with no matching file
  is a **dangling handle: FAIL**.
- **A role with no row at all is legal but surfaced** — an addressable seat nobody has minted yet
  (a hand-authored roster.md predating this section, or a domain instance that deliberately hasn't
  wired one role's agent) is reported as a **named WARNING**, never a FAIL — the same severity a
  `VACANT` lead already gets in `## Groups`, never blocking the check.
- A row naming `advisory` (or any value other than `chair` or a declared ordinary sub-council) as
  its key is a **FAIL** — the reserved-name rule is mechanically enforced here, not just stated in
  prose.

## Bijection & mechanical validation

This plugin's `scripts/roster_check.py` (selftest-carrying, per this workspace's semantic-edit
invariant for bundled scripts) is the exit-code proof — invoked as
`roster_check.py <council-skill-dir>` (the council's own skill directory, e.g.
`check-brand-council`; never the `roster.md` path itself), it validates that directory's
`references/roster.md` against its `references/critics/` directory, and its `## Role agents`
section against that instance's own `agents/` directory (the council skill's plugin root, e.g.
`brand-design/agents/`):

- handle ↔ persona-file bijection (both directions),
- every row's `sub-councils` cell is non-empty,
- `full` never appears as a literal value in the `sub-councils` column,
- every `## Groups` entry resolves to a seated, active handle or the literal `VACANT` — a dangling
  handle fails,
- `role` and `status` values are drawn from their fixed enums (`lead`/`member`/`advisor`,
  `active`/`retired`),
- the `advisory`↔`advisor` pairing holds exactly: a row naming `advisory` in `sub-councils` but not
  `role: advisor` fails, and a `role: advisor` row whose `sub-councils` is anything other than
  exactly `advisory` fails.
- every `## Role agents` value resolves to a real `agents/<handle>.md` file under the council's
  own plugin root — a dangling handle fails; a role (`chair` or a declared ordinary sub-council)
  with no `## Role agents` row at all warns; a row keyed to `advisory`, or to anything that is
  neither `chair` nor a `leads:`-declared ordinary sub-council, fails.

A `VACANT` slot in ANY `## Groups` entry (not only `leads`) is reported as a **named warning**, not
a failure — an unfilled seat is a fact to surface, never a defect that blocks the check. **An
ordinary sub-council with zero seated active critics** (declared via a `leads:` entry — e.g. a
newly-declared `creative` sub-council nobody has minted into yet) is reported at the **same WARNING
severity as a `VACANT` lead** — an empty bench is exactly that: an unfilled seat, not a defect,
mirroring the vacant-lead convention rather than inventing a new severity for it. This is distinct
from `advisory`'s own empty-is-normal case, one tier lower: `advisory` is RESERVED and legitimately
never seeded by the plugin itself (INFO, the quietest tier), where an ordinary sub-council is
expected to fill eventually and its emptiness is worth a WARNING's visibility. A zero-member
`advisory` sub-council is reported as a **named INFO line** — narrower than a warning, since it is
the reserved sub-council's normal steady state, not a gap anyone needs to fill — never a warning and
never a failure. Everything else above fails the check on violation.

## Why a data edit, not a semantic edit

Before this contract, seating a critic meant hand-editing SKILL.md's own prose roster table — a
semantic edit to a prompt-carrying artifact, earning `plugin-authoring.md`'s mandatory
fresh-context checker pass. `roster.md` is data: appending one row and re-running
`roster_check.py` is floor-tier verification. The SKILL.md that cites `roster.md` does not change
when a critic is seated, so it never re-triggers that invariant on its own account — only an
actual edit to the convening skill's own prose (its Phase 1/2 procedure, its trust-boundary
statement, etc.) still earns the checker pass it always did.

## What a domain instance supplies vs. inherits

Same split `roster-and-personas.md` already states, sharpened for the file itself: the roster
**content** (which handles, which sub-councils, who leads, what groups exist, whether any
`advisory` seats are filled yet, and which agent handles which role) is the domain instance's own
data in its own `roster.md`; the **schema** above — column set, the `full` and `advisory`
reservations, the `advisor` role's voting exclusion, the bijection, the `VACANT`/
zero-advisor-is-not-a-failure conventions, and the `## Role agents` section's own shape and
reserved-name enforcement — is this pack's machinery, cited by every instance's SKILL.md, never
restated as a second copy of the rules. What a role agent actually IS and does when dispatched is
`role-agents.md`'s own axis, cited from here rather than restated.
