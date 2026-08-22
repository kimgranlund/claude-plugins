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
  builder never renames it. The PRINTED/roster session name for that role is `{repo}-marshal`,
  not `{repo}-agent` (`team-scaffolding` Phase 1/2, `fleet-bootstrap` Phase 1): the seat's session
  identity matches the `teamwork:bind-team` contract it adopts (ADR-0020's marshal vocabulary —
  `{repo}-team-lead` was this same split's prior value, superseded 2026-08-17, issue #586), while
  the schema key stays the generic role bucket. Every other role's session name is its role token
  verbatim (`{repo}-reviewer`, `{repo}-planner`, `{repo}-product`) — only `agent` has this split.
  **Role-key migration considered and declined this wave (issue #586, 2026-08-17).** #586's
  acceptance criteria left the schema key's migration to the builder's own cheap/not-cheap call.
  Not cheap here: the key is a live data field read by every existing `.claude/ops/fleet.json`
  row across repos (including this repo's own — see below), by every sweepable-invariant grep
  this schema already documents (`justification_date` checks keyed on `seats.*.tier`), and
  potentially by other repos' own copies of this convention with no shared migration path: a
  rename would need a cross-repo sweep this ticket's blast radius never enumerated, not just a
  same-file text edit. The split stays as designed — schema key `agent`, printed name now
  `{repo}-marshal` — confirmed schema-stable, not migrated.
- **`seats.<role>.tier`** — the model/effort tier this seat runs at in THIS repo. Starts equal to
  the canonical seat ladder (`team-scaffolding`'s Phase 4 point 1: agent fable+low, reviewer
  fable+xhigh, planner fable+medium, product fable+high).
- **`seats.<role>.justification_date`** — **required whenever `tier` deviates from the canonical
  ladder value.** This is the sweepable invariant Kim's ruling calls for: a tier deviation with no
  justification date is a doctrine-audit-class finding, mechanically checkable — grep every
  `seats.*.tier` against the canonical table in `team-scaffolding`'s Phase 4; any mismatch missing
  a sibling `justification_date` is a finding, full stop, no judgment call needed.
- **`seats.<role>.mode`** — `"manual"` (a human-driven terminal), `"background"` (a spawned
  long-lived named `Agent`-tool dispatch — `planner` only, as of issue #853; see below),
  `"background-subprocess"` (a genuine `claude -p` OS process spawned with cwd already inside a
  pre-walled worktree — `reviewer` only, issue #853), or `"dispatched"` (a synchronous `Agent`
  call that already returned — today only the product seat's `/fleet-bootstrap` Phase 2 dispatch;
  distinct from `"manual"` so a reader never infers a live terminal session that isn't there).
  Reviewer and planner default to `"manual"` per #410 addendum 3; `/fleet-bootstrap`'s spawn-list
  argument is what flips one to `"background"`/`"background-subprocess"`. **`reviewer` and
  `planner` diverge on spawn mechanism (issue #853):** an in-process `Agent`-tool dispatch inherits
  the parent session's permission mode instead of re-deriving one from its own cwd, so it can never
  be a genuinely separate OS process — harmless for `planner` (carries no wall), disqualifying for
  `reviewer` (the wall's whole point is structural enforcement). `planner` keeps `"background"`;
  `reviewer` moved to `"background-subprocess"`, never `"background"` again — a `reviewer` row still
  reading `"background"` predates this fix (issue #850/#852's shipped shape) and its
  `wall_applied` field (below) must be read as unverified-by-today's-standard, not retroactively
  trusted.
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
- **`live_state.joined[].wall_applied`** — optional, present only on a `reviewer` row appended by
  `fleet-bootstrap` Phase 5's ORCHESTRATOR (the background-subprocess spawn, issue #853; formerly
  an in-process background spawn, issue #850/#852). **The manual `/team-scaffolding reviewer` path
  NEVER writes this field, on ANY outcome, including a declined restart** — a genuinely walled
  restarted session structurally cannot append structured JSON to `fleet.json` either (the same
  C1a escape-hatch charset gap issue #855 found: its positive charset excludes `{`/`}`, so no
  literal JSON-object append can ever pass, even the reviewer's own row). The manual path reports
  the identical vocabulary below strictly INLINE — printed to the human by `team-scaffolding`
  Phase 3 or `bind-review`'s Phase 0 — never as a `fleet.json` write; see "Absent", below, which
  covers it entirely. One of four values (issue #852 — content verification alone is never
  sufficient to write `true`):
  - `true` — the `deny-edit-write` wall was written and re-verified (`team-scaffolding` Phase 3's
    C1–C3 steps) by the ORCHESTRATOR, in a genuinely separate `claude -p` OS process already
    running with cwd inside the pre-walled worktree at start (issue #853), AND confirmed enforced
    by that process's own I2 live probe: a `Write` and a denied-pattern `Bash` attempt, run inside
    it, both came back DENIED, with an allowed `gh`-shaped `Bash` command still passing. Always
    carries a sibling `wall_verified_via` (below).
  - `"blocked-worktree"` — the orchestrator's own worktree precondition (Phase 5 step 1) found a
    shared checkout before any wall write or spawn was attempted; the orchestrator appends this row
    itself, immediately, with no wall write and no spawn ever attempted — unchanged from issue #852.
  - `"same-session-unenforced"` — background-subprocess path only: the wall write and grep-verify
    succeeded, but the spawned child's own I2 probe unexpectedly reported a `Write`/`Bash` attempt
    SUCCEEDING rather than denied (named honestly rather than silently promoted to `true`). The
    identical LABEL also names the manual path's own declined-restart outcome, but that occurrence
    is always inline prose (per the opening paragraph above), never this field.
  - `"spawn-unconfirmed"` (issue #853, new) — `fleet-bootstrap`'s background-subprocess spawn was
    attempted but never reported an I2 verdict within its monitoring budget (the process may still
    be running, or may have died silently) — distinct from `"same-session-unenforced"`: no session
    ever continued unwalled here, there is simply no confirmed evidence yet either way. Never
    promoted to `true` or `"same-session-unenforced"` on a guess; a later re-check that finds the
    process has since exited may confirm one of those instead.

  Absent covers both a manual `reviewer` join via `/team-scaffolding reviewer`/`/bind-review`
  directly (which ALWAYS reports its own wall outcome — including its own I2 probe result, and
  including a confirmed `true`-equivalent restart result — inline rather than through this field,
  per the opening paragraph above) and a background join predating this field — read as "unknown",
  never as "applied": a reader never infers success from a missing field (issue #850), and never
  infers success from `true` without I2's own probe having actually confirmed a denial (issue
  #852).
- **`live_state.joined[].wall_verified_via`** — optional, present only alongside `wall_applied:
  true` (issue #853). Since only `fleet-bootstrap`'s orchestrator ever writes `wall_applied` (see
  above — the manual path is always inline, never a field write), this field's only recorded value
  today is `"subprocess-spawn"` — `fleet-bootstrap` Phase 5's own `claude -p` child, spawned by the
  orchestrator with cwd already inside the pre-walled worktree. The manual path's own restart
  confirmation uses the identical "via restart" wording when `team-scaffolding`/`bind-review`
  report it, but strictly as spoken/printed text, never as this field's value — there is no
  `"restart"` entry to find in a real `fleet.json` file today, by design, not omission.
- **`live_state.loop_position`** — optional pointer to which of north star / foundation / releases
  loop (per `docs:product-lifecycle-rules`) the product seat currently has authority over; `null`
  until the product seat records one.

## Why there is no `builder` seat here (Kim's ruling, 2026-08-21 session)

The canonical roster is deliberately four singular roles — one live holder per role, collision-
checked. Build capacity doesn't fit that shape: a repo normally runs several build-leader
dispatches concurrently, one per in-flight ticket, not one standing "the builder" seat. Rather than
force a plural concept into this schema's singular-seat model, persistence for build work lives as
a naming CONVENTION at the dispatch site instead — `teamwork:mobilize-chores` step 5 names every
`build-leader` dispatch `build-<ticket-id>`, which keeps each one idle-and-resumable (`SendMessage`)
after its first return, the same named-`Agent`-dispatch mechanism as `planner`'s `"background"` mode
above, without needing a `fleet.json` row per build. This is not a gap to fill later; it's the
considered shape.

## Doctrine-audit hook

A future `authorkit:doctrine-audit` edge can point at this schema directly: read every
`fleet.json` under `.claude/ops/`, for each `seats.*` entry compare `tier` against the canonical
ladder, flag any mismatch with `justification_date` absent or null. This file documents the check
so that edge can be added without re-deriving the schema.
