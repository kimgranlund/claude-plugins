# `.claude/ops/fleet.json` — the per-repo fleet manifest

Per-repo variation in how the standing fleet is run is DATA, not a duplicated command copy
(design ruling, #410, 2026-08-16: `/fleet-bootstrap` and `/team-scaffolding` are plugin commands;
this file is the only thing that varies per repo). `/team-scaffolding <role>` seeds/updates it on
first use in a virgin repo; `/fleet-bootstrap` reads and extends it across a full cold start.

## Shape

```json
{
  "version": 1,
  "seats": {
    "agent":    { "tier": "fable+low",    "justification_date": "2026-08-16", "mode": "manual" },
    "reviewer": { "tier": "fable+xhigh",  "justification_date": "2026-08-16", "mode": "manual" },
    "planner":  { "tier": "fable+medium", "justification_date": "2026-08-16", "mode": "manual" },
    "product":  { "tier": "fable+high",   "justification_date": "2026-08-16", "mode": "manual" }
  },
  "permission_profiles": {
    "reviewer": "deny-edit-write"
  },
  "live_state": {
    "joined": [
      { "role": "agent", "mode": "manual", "date": "2026-08-16", "action": "joined", "agent_name": null },
      { "role": "reviewer", "mode": "manual", "date": "2026-08-16", "action": "joined", "agent_name": null },
      { "role": "reviewer", "mode": "manual", "date": "2026-08-20", "action": "released", "agent_name": null, "reason": "handed off to plugins-review" },
      { "role": "reviewer", "mode": "manual", "date": "2026-08-20", "action": "joined", "agent_name": null }
    ],
    "loop_position": null,
    "gate": null
  }
}
```

The trailing three `reviewer` rows show a full retire/takeover cycle: joined, then released
(`/team-scaffolding retire reviewer`, `references/fleet-manifest-schema.md`'s own consumer,
`team-scaffolding`'s Phase 6), then a fresh `joined` row for the taking-over session — no separate
"takeover" action exists; a `joined` row appended after a `released` row for the same role IS the
takeover record.

## Fields

- **Schema key vs. printed session name (`agent` role only).** `fleet.json`'s role key stays
  `agent` everywhere in this schema — `seats.agent`, `live_state.joined[].role: "agent"` — and a
  builder never renames it. The PRINTED/roster session name for that role is `{repo}-team-lead`,
  not `{repo}-agent` (`team-scaffolding` Phase 1/2, `fleet-bootstrap` Phase 1): the seat's session
  identity matches the `teamwork:bind-team` contract it adopts, while the schema key stays the
  generic role bucket. Every other role's session name is its role token verbatim
  (`{repo}-reviewer`, `{repo}-planner`, `{repo}-product`) — only `agent` has this split.
- **`seats.<role>.tier`** — the model/effort tier this seat runs at in THIS repo. Starts equal to
  the canonical seat ladder (`team-scaffolding`'s Phase 4 point 1: agent fable+low, reviewer
  fable+xhigh, planner fable+medium, product fable+high).
- **`seats.<role>.justification_date`** — **required whenever `tier` deviates from the canonical
  ladder value.** This is the sweepable invariant Kim's ruling calls for: a tier deviation with no
  justification date is a doctrine-audit-class finding, mechanically checkable — grep every
  `seats.*.tier` against the canonical table in `team-scaffolding`'s Phase 4; any mismatch missing
  a sibling `justification_date` is a finding, full stop, no judgment call needed.
- **`seats.<role>.mode`** — `"manual"` (a human-driven terminal), `"background"` (a spawned
  long-lived named agent), or `"dispatched"` (a synchronous `Agent` call that already returned —
  today only the product seat's `/fleet-bootstrap` Phase 2 dispatch; distinct from `"manual"` so a
  reader never infers a live terminal session that isn't there). Reviewer and planner default to
  `"manual"` per #410 addendum 3; `/fleet-bootstrap`'s spawn-list argument is what flips one to
  `"background"`.
- **`permission_profiles`** — which structural wall (per `lld-0006-fleet-permission-profile.md`)
  applies to which seat in this repo. Today only `reviewer` carries one (`deny-edit-write`); the
  key exists so a future seat's profile has a place to record without a schema change.
- **`live_state.joined`** — the orientation record a rejoining session reads: which roles have
  joined, in what mode, when, and (for background seats) under what agent name. Append-only —
  never rewritten in place; a seat rejoining after a restart appends a new row rather than editing
  its old one, so the history of who has held a seat stays intact.
- **`live_state.joined[].action`** — **this field's semantics are canonical here; `team-scaffolding`'s
  Phases 1/2/6 cite this entry rather than restating it.** `"joined"` (a seat bound this row,
  either a fresh bind or a takeover of a previously-released seat) or `"released"` (the seat
  holder retired via `/team-scaffolding retire <role>`, `team-scaffolding`'s Phase 6). Absent on a
  row is read as `"joined"` — every entry written before this field existed predates it and was
  always a join. **Liveness for a role is the `action` of its LATEST row, not the row's mere
  presence**: a role whose latest row is `"released"` is open (a following
  `/team-scaffolding <role>` binds without collision); a role whose latest row is `"joined"` (or
  has no `action` field) is live and collides. There is no separate "takeover" action — an
  ordinary `joined` append made after a role's latest row was `"released"` IS the takeover record;
  the two rows read together tell the whole story.
- **`live_state.joined[].reason`** — optional, present only on a `"released"` row: the free-text
  reason argument passed to `/team-scaffolding retire <role> [reason]`, or `null` if none was
  given.
- **`live_state.loop_position`** — optional pointer to which of north star / foundation / releases
  loop (per `docs:product-lifecycle-rules`) the product seat currently has authority over; `null`
  until the product seat records one.

## Doctrine-audit hook

A future `authorkit:doctrine-audit` edge can point at this schema directly: read every
`fleet.json` under `.claude/ops/`, for each `seats.*` entry compare `tier` against the canonical
ladder, flag any mismatch with `justification_date` absent or null. This file documents the check
so that edge can be added without re-deriving the schema.
