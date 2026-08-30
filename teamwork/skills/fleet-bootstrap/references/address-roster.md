# Phase 6's address roster (F6 split)

**Close with the address roster (Kim's ruling, 2026-08-22) — every seat, one line each, in this
exact shape, so a human knows who can be messaged by name right now:**

```
- `@{scope}-marshal` — this fleet's orchestrator agent (this session; fleet.json role `agent`) — SendMessage: `<agent_name>`
- `@{scope}-planner` — this fleet's planner agent — SendMessage: `<agent_name>`
- `@{scope}-reviewer` — this fleet's review agent — SendMessage: `<agent_name>`
- `@{scope}-product` — this fleet's product agent — SendMessage: `<agent_name>`
```

Each line carries its live addressability, classified from `fleet.json`'s LATEST row for that
role (its `mode` + `action` — `fleet.json` governs, never the roster file, per Phase 4's own
source-of-truth rule) — never assumed from the convention alone, since a printed name that
silently drops messages is worse than no name. Four classes, exactly one per seat:
- **addressable** — a live named `Agent`-tool dispatch (`mode: "background"`, latest action
  `joined`: `planner` spawned this run, or a prior run's still-live one — confirm a prior-run
  seat's liveness via `ListAgents`, the one sanctioned liveness-confirm use), or a live human
  terminal (`mode: "manual"`, latest action `joined`). `{scope}-marshal` is always this session
  and always addressable.
- **not live — returned dispatch** — `mode: "dispatched"` (the `product` seat's Phase 2 call: a
  synchronous, unnamed `Agent` call that has already returned by now; nothing to message).
- **not messageable — subprocess** — `mode: "background-subprocess"` (`reviewer` spawned as a
  `claude -p` child: one-shot, no messaging identity; name its log path as the pointer instead).
- **not live — bind it with `/team-scaffolding <role>`** — no row at all, or latest action
  `released`.

The `@{scope}-<role>` label is a display sigil for the human's eye only — **it is never itself a
reachable `SendMessage` target**, since no session is ever registered under that printed string
(`fleet-rules` Section 7, #902: routing on the label alone sends a message nowhere). The real
`SendMessage` target is each row's resolved `agent_name` field — the harness-assigned session
name (e.g. `plugins-75`), read from `fleet.json`'s LATEST row for that role
(`fleet-manifest-schema.md`'s own canonical field) — printed as the `SendMessage:` value above,
never the label standing in for it. A row with no `agent_name` (a legacy pre-#902 entry, or one
of the three non-addressable classes above) prints `SendMessage: none` rather than falling back
to the label. A seat with no live holder is listed so the human sees the gap, not omitted.
