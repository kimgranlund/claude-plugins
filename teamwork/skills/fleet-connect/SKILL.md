---
name: fleet-connect
description: >-
  The Terminal-A side handshake (#903): a user in a WORKING session runs /fleet-connect to wire
  this session to the repo's already-live marshal — read fleet.json's latest agent-role joined row,
  confirm liveness, SendMessage a handshake introducing this session, then adopt the working-session
  forwarding posture (fleet-shaped asks forward, milestone replies relay, everything else stays
  local) for the rest of the session. Run /fleet-connect, no arguments. NOT cold-starting the
  fleet itself or standing up the marshal seat (fleet-bootstrap — that command BECOMES the marshal;
  this one only CONNECTS an already-live one); NOT the marshal's own standing routing discipline
  (fleet-rules Section 7 — that's the marshal's side of the same handshake, cited not restated
  here); NOT binding any other seat (team-scaffolding).
disable-model-invocation: true
user-invocable: true
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

1. **Resolve the fleet SCOPE ROOT, then read `fleet.json` under it.** (#911 — supersedes the
   #906/#909 nearest-`fleet.json` ladder.) The scope root is the nearest ancestor directory,
   walking from the current working directory upward and BOUNDED at the repo root (cwd itself
   counts as a candidate; the walk never crosses the repo-root boundary — full definition in
   `fleet-bootstrap`'s `references/fleet-manifest-schema.md`, canonical there, cited not
   restated), that contains a `.claude` directory AT ALL — never the nearest directory that merely
   happens to already hold a `fleet.json`. The target path is always
   `<scope root>/.claude/ops/fleet.json`; an ancestor's `fleet.json` sitting ABOVE the resolved
   scope root is out of scope and never consulted, whatever it contains (the #909 bug: a
   repo-root copy shadowing an app's own scope produced a false "recorded-but-unresolvable
   marshal" — the #911 fix is that an app with its own `.claude/` is always its own scope,
   regardless of whether an ancestor `fleet.json` exists). App-scoped records are a ruled reality,
   not drift — the app-scoped bootstrap re-homing ruling (Kim 2026-08-23) deliberately homes a
   `fleet.json` at an app subdirectory; a legacy repo-root copy may coexist, unrelated.
   **Scope-pointer redirect (#915):** `fleet.json` absent at the resolved scope root but
   `<scope root>/.claude/ops/fleet-scope.json` present → re-resolve to the pointed directory and
   read ITS `ops/fleet.json` instead — one hop only, validity rules canonical in
   `references/fleet-manifest-schema.md` §Location and resolution (cited, not restated); a local
   `fleet.json` always wins over a pointer, and with neither present current behavior stands (no
   walk-up). Report the
   resolved scope root (both roots when a pointer redirected) and which path was used in step 5's
   report regardless of outcome. **Also read the top-level `expected_branch` field** (absent reads
   `"main"`, `references/fleet-manifest-schema.md`'s own default — canonical there, issue #932):
   step 3's branch reconcile diffs against this resolved value. Take
   `live_state.joined`'s entries for `role: "agent"` and select the LATEST one by array order.
   **Liveness is that row's `action` field** — `"joined"` or absent counts as live, `"released"`
   does not (the canonical rule, `fleet-bootstrap`'s `references/fleet-manifest-schema.md`, cited
   not restated). **No `.claude` directory found anywhere between cwd and the repo root
   (inclusive), no `fleet.json` under the resolved scope root, absent `agent` role entries, or
   the latest row's `action` is `"released"`** (all judged against the ONE resolved scope root,
   never a farther ancestor's file) → report "no live marshal (checked `<resolved path>`, or: no
   `.claude` directory found between `<cwd>` and the repo root) — run /fleet-bootstrap in a
   dedicated terminal" and stop. Do not proceed to step 2.

   **Live row but `agent_name` is `null`/absent** (a legacy pre-fix entry — team-scaffolding's
   manual-join path wrote `agent_name: null` unconditionally before this same change closed that
   gap) → this is a DISTINCT failure branch, never folded into "no live marshal": report "a live
   marshal is recorded in `<resolved path>` but its address never resolved (legacy entry, dated
   `<date>`) — cannot
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

3. **Branch reconcile, before the handshake goes out** (`references/fleet-manifest-schema.md`
   §"Branch reconcile on every bind", canonical there, issue #932). Capture THIS session's own
   `git rev-parse --abbrev-ref HEAD` (and, where cwd is a linked worktree rather than the primary
   checkout — `git rev-parse --git-common-dir` vs. `--git-dir` differ only inside one — this
   session's own worktree path), and diff against step 1's resolved `expected_branch`. **Match** →
   nothing printed here, folded silently into step 5's report. **Mismatch** → flag it plainly,
   held for step 5's report (`Session branch <actual> — fleet expects <expected_branch> —
   mismatch`) — never a hard stop: this command has no write path to `fleet.json` at all (never a
   `live_state.joined` row — a connecting working session is not itself a seat bind) and no
   standing to block a handshake over it, only to surface the drift for the human at this terminal
   to act on. **Handshake.** `SendMessage` the resolved `agent_name`, introducing THIS session by its own
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

5. **Report**: the marshal's resolved name, the `fleet.json` path step 1 resolved — both scope
   roots when a `fleet-scope.json` pointer redirected (#915) — (so a
   shadowed sibling copy is auditable), the ack line (or "sent, unacknowledged" per the
   failure branch), the roster it returned (or "not received" if the ack never landed), and step
   3's branch reconcile outcome (match, or the named mismatch — never omitted, stated even on a
   match so a reader never has to infer "checked" from silence).

## Failure branches

- **No `.claude` directory found anywhere between cwd and the repo root, no `fleet.json` under
  the resolved scope root, or the resolved file has absent `agent` role entries or the latest
  row's `action` is `"released"`** (step 1) → not a fleet repo/scope, or no live marshal yet.
  Report: "no live marshal — run /fleet-bootstrap in a dedicated terminal", naming the resolved
  scope root and path checked (or that no `.claude` directory exists between cwd and the repo
  root). Stop — never fall through to a handshake against nothing, and never re-try the verdict
  against an ancestor's `fleet.json` once a nearer scope root resolved (with or without a
  `fleet.json` of its own); a `fleet-scope.json` pointer at that scope root (#915, step 1) is
  the one sanctioned redirect, and its absence means the verdict stands.
- **Pointer present but invalid** (step 1, #915 — the target sits outside the repo-root boundary
  or lacks a `.claude/` directory, per the canonical validity rules) → report "pointer at
  `<pointer path>` names an invalid target (`<reason>`) — cannot resolve; fix or remove the
  pointer" and stop; never fall back silently to the pointerless verdict.
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
