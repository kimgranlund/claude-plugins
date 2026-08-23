---
description: "The Terminal-A side handshake (#903): a user in a WORKING session runs /fleet-connect to wire this session to the repo's already-live marshal — read fleet.json's latest agent-role joined row, confirm liveness, SendMessage a handshake introducing this session, then adopt the working-session forwarding posture (fleet-shaped asks forward, milestone replies relay, everything else stays local) for the rest of the session. Run /fleet-connect, no arguments. NOT cold-starting the fleet itself or standing up the marshal seat (fleet-bootstrap — that command BECOMES the marshal; this one only CONNECTS an already-live one); NOT the marshal's own standing routing discipline (fleet-rules Section 7 — that's the marshal's side of the same handshake, cited not restated here); NOT binding any other seat (team-scaffolding)."
---

# fleet-connect — wire this working session to the repo's live marshal

A working session (a human typing directly at a terminal, not a fleet seat) often needs to forward
fleet-shaped asks — a mobilize, a merge decision, a dispatch, a seat-status question — to the
repo's already-running `{repo}-marshal` rather than acting on them itself. `/fleet-bootstrap` and
`/team-scaffolding agent` both **become** the marshal; neither is right for a session that just
wants to **talk to** one that already exists. This command is that explicit, human-typed handshake
— the working-session-side twin of `fleet-rules` Section 7's own marshal-side routing sentence
("a non-marshal session with a live `{repo}-marshal` forwards a fleet-shaped ask via `SendMessage`
rather than applying this section itself").

## Procedure

1. **Read `.claude/ops/fleet.json`.** Take `live_state.joined`'s entries for `role: "agent"` and
   select the LATEST one by array order. **Liveness is that row's `action` field** — `"joined"` or
   absent counts as live, `"released"` does not (the canonical rule, `fleet-bootstrap`'s
   `references/fleet-manifest-schema.md`, cited not restated). **Absent file, absent `agent` role
   entries, or the latest row's `action` is `"released"`** → report "no live marshal — run
   /fleet-bootstrap in a dedicated terminal" and stop. Do not proceed to step 2.

   **Live row but `agent_name` is `null`/absent** (a legacy pre-fix entry — team-scaffolding's
   manual-join path wrote `agent_name: null` unconditionally before this same change closed that
   gap) → this is a DISTINCT failure branch, never folded into "no live marshal": report "a live
   marshal is recorded but its address never resolved (legacy entry, dated `<date>`) — cannot
   SendMessage it; a human should confirm it's still running and re-bind via /team-scaffolding
   agent to record a resolved address, or take over via /fleet-bootstrap only once confirmed
   gone." Never auto-suggest a takeover on an unresolved-but-possibly-live row — that risks a
   second competing marshal. Stop; do not proceed to step 2.

   A live row with a resolved `agent_name` → proceed to step 2.

2. **Confirm liveness via `ListAgents`** — the one legitimate use of `ListAgents` for peer
   discovery (`fleet-rules` Section 1's own narrow exception: confirming liveness of a session
   ALREADY named in a durable record, never using `ListAgents` to go find one). Match the resolved
   `agent_name` against the `ListAgents` listing.
   - **Listed and live** → proceed to step 3.
   - **Not listed** (joined but no matching live session) → this is the stale-seat failure branch
     below, not step 3.

3. **Handshake.** `SendMessage` the resolved `agent_name`, introducing THIS session by its own
   real name (never a role label), and requesting a one-line status ack plus the `@`-address
   roster (`fleet-bootstrap` Phase 6's own roster shape — every seat, one line, live/dead
   classified). This is a request-response handshake, unlike `team-scaffolding` Phase 4 point 7's
   one-way introduction nudge — wait for the reply within this turn where the harness allows it.
   - **Ack received in-turn** → proceed to step 4 with the ack line and roster in hand.
   - **No ack within the turn** → the sent-unacknowledged failure branch below; still proceed to
     step 4 (the posture is adopted regardless of whether the ack has landed yet — the marshal
     replies async, per `fleet-rules` Section 3's own nudge-not-channel-of-record doctrine).

4. **Adopt the working-session forwarding posture for the rest of THIS session** (the session-side
   twin of `fleet-rules` Section 7's marshal-side routing sentence):
   - A fleet-shaped ask arriving at this session (a mobilize decision, a merge/dispatch call, a
     seat-status question, anything `fleet-rules` Section 7's own triage table would route) is
     forwarded to the marshal via `SendMessage`, never absorbed or answered locally.
   - A milestone reply arriving back from the marshal is relayed to the human in one line
     (`fleet-rules` Section 3's own no-op-silence rule: milestone-only, never routine-wake noise).
   - Everything else — ordinary work this session was already doing — stays local; this posture
     changes routing for fleet-shaped items only, not a wholesale handoff of the session's own
     work. Re-running this command in an already-connected session simply re-confirms and re-states
     the posture — harmless, never an error.

5. **Report**: the marshal's resolved name, the ack line (or "sent, unacknowledged" per the
   failure branch), and the roster it returned (or "not received" if the ack never landed).

## Failure branches

- **No `fleet.json`, no live `agent` row (latest row's `action` is `"released"` or absent
  entirely)** (step 1) → not a fleet repo, or no live marshal yet. Report: "no live marshal — run
  /fleet-bootstrap in a dedicated terminal." Stop — never fall through to a handshake against
  nothing.
- **Live `agent` row but `agent_name` is `null`/absent** (step 1, a legacy pre-fix entry) →
  report the row as recorded-but-unresolvable and stop; never treat this the same as "no live
  marshal" and never auto-suggest a takeover — the seat may genuinely still be live.
- **Seat joined but `ListAgents` shows no matching live session** (step 2, a stale seat) → report
  the stale entry (role, date, recorded `agent_name`) and suggest a takeover via
  `/fleet-bootstrap` in a dedicated terminal. **Never reap the entry** — this command has no
  standing to release another session's seat; that's `team-scaffolding retire`'s own act, run by
  the retiring session itself.
- **No ack within the turn** (step 3) → report "sent, unacknowledged" plainly rather than
  claiming a handshake completed. The posture (step 4) is still adopted — a fleet-shaped ask sent
  after this point still forwards; the marshal's async reply, when it lands, is relayed at that
  later point.

## Done

Done when step 5's report has printed — one of three shapes: a completed handshake (marshal name,
ack, roster), a stale-seat report (never a completed handshake), or the no-live-marshal stop (never
proceeding past step 1). Never done while still holding a role-label address instead of the
resolved `agent_name`, and never done having adopted the forwarding posture (step 4) without
stating so in the report.
