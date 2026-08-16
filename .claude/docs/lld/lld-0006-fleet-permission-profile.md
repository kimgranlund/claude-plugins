---
doc-type: lld
id: lld-0006-fleet-permission-profile
status: draft
version: 0.1.0
date: 2026-08-16
owner: kim.granlund
ticket: nonoun-plugins#404
adr: none
---
# LLD — Fleet-seat permission-profile mechanism (#404)

**Verdict, head-first: a HOST session adopting a contract has no agent frontmatter to wall with,
so the reviewer seat's structural read-only wall is a new mechanism — `.claude/settings.local.json`
`permissions.deny`, written per-worktree by `/team-scaffolding` itself, never merely asserted in prose.**

No existing ADR governs host-session structural tool walls; this LLD is the first record of the
mechanism — a future ADR may ratify it if a second consumer appears.

## Non-goals

- Not a platform-enforced session rename (D1) — no mechanism is proposed for that.
- Not defending against a future platform change that makes `deny` advisory (R2) — out of scope;
  I2's live smoke test targets the platform's actual behavior, not this LLD's assumption.
- Not granting the reviewer seat any write path today (R3) — left to a future revision.

## Why this is a genuinely new decision, not a restatement of intake-lead

`ops-write-sandbox-rules` and `docs:intake-lead` both wall a **dispatched agent** — the wall lives
in that agent's own frontmatter (`tools:` / `disallowedTools:`), enforced the moment the platform
loads the agent definition. `teamwork:lead-review` is the opposite shape by design (issue #404's
seat 4 spec correction 3, and `lead-review`'s own SKILL.md): the reviewer is a **host session**
the human types into directly, adopting a desk contract with no separate `Agent` spawn — there is
no agent file for the platform to wall. A prose instruction ("don't Write/Edit outside your
sandbox") is exactly what spec correction 3 rules out as insufficient — SKILL.md, PLAN, ADR are
uniformly not read for permission enforcement; they only wall an obedient adopter, not the
platform's own Edit/Write path.

## Components

### C1 — The mechanism: `.claude/settings.local.json` `permissions.deny`, worktree-scoped

`/team-scaffolding reviewer` writes (or verifies, if already present and correctly shaped)
`.claude/settings.local.json` in the CURRENT worktree:

```json
{
  "permissions": {
    "deny": ["Edit", "Write"],
    "allow": [
      "Bash(gh issue *)",
      "Bash(gh pr comment *)",
      "Bash(gh pr view *)",
      "Bash(gh api *)",
      "Read",
      "Grep",
      "Glob"
    ]
  }
}
```

`deny` on the bare tool names `Edit`/`Write` blocks every path, not a glob subset — the reviewer
seat has no legitimate local-file-write path at all (its output is GitHub Issues/PR comments, a
platform API call via `Bash(gh ...)`, never a filesystem mutation), so an allow-list carve-out
(the `ops-write-sandbox-rules` scoped allow-list pattern) is the wrong shape here: that pattern exists for
seats that DO need one scoped write path. The reviewer needs zero.

Settings precedence (platform-documented): project `.claude/settings.local.json` layers over
`.claude/settings.json`, and `deny` always wins over any `allow` at any layer — so this profile is
tamper-resistant against the seat's own later prose even if the adopted contract tried to grant
Write back.

### C2 — Why per-worktree, not a checked-in fleet profile

A checked-in `.claude/settings.json` deny rule would block Edit/Write for EVERY session in the
repo, including the agent/planner/product seats that legitimately write. The reviewer's wall must
apply to exactly the one worktree that session is running in — `settings.local.json` is
gitignored by the platform's own convention (never committed) and inherently per-checkout, which
is exactly the scope needed. `/team-scaffolding` writes it as a side effect of the `reviewer` role
branch; the other three roles never touch this file.

### C3 — Verification, not blind trust

After writing the profile, `/team-scaffolding` re-reads the file back and greps for the two deny
entries before printing the comms charter — a write that silently failed (permission prompt
declined, disk error) must not let the seat believe it is walled when it isn't. If verification
fails, the seat reports the failure and does NOT proceed to adopt the reviewer contract — an
unverified wall is worse than an explicit refusal, per the same "narrated-but-absent" defect class
`ops-write-sandbox-rules` names for its own mechanism.

## Interfaces

### I1 — `/team-scaffolding reviewer [charter]` sequence

1. Write `.claude/settings.local.json` per C1 (merge if the file already exists — never clobber
   unrelated keys).
2. Verify per C3.
3. Print the comms charter (parallel-work-rules doctrine, peer roster, empty-roster fallback).
4. Invoke `/lead-review` (Skill tool) with `charter` as its argument — the desk contract this
   session now runs under, now backed by a platform-enforced wall instead of a stated one.

### I2 — Demonstrating the wall is structural (acceptance criterion)

A live smoke test: after `/team-scaffolding reviewer` completes, attempt a trivial `Write` to any path
in the worktree — the platform denies it without a permission prompt reaching the human (a `deny`
entry is a hard block, not a promptable `ask`). Record the denial text in the build's Findings
write-back as the structural-wall proof, mirroring `docs:intake-lead`'s A4 smoke-test precedent
for its own agent-level wall.

## Data

### D1 — Seat-naming convention (Scope/Open item 2): convention, not enforced

`{repo}-agent` / `{repo}-reviewer` / `{repo}-planner` / `{repo}-product` names the SESSION, not a
file or a git ref — there is no platform hook that renames a live session, and inventing one
(e.g. requiring a specific tmux/terminal title) would add mechanism no other fleet function
depends on. `/team-scaffolding` prints the expected name as the first line of its output and appends it
to `.claude/ops/fleet-roster.md` (the durable discovery channel, D2) so a peer session can read
the convention even if the human never renamed their terminal tab. Ruling: convention, socially
enforced by the printed instruction + the roster record; not a platform-enforced identity.

### D2 — Peer discovery: `.claude/ops/fleet-roster.md`, durable-channel fallback

Each `/team-scaffolding <role>` run appends one dated line (`role · session-name-if-known · date`) to
`.claude/ops/fleet-roster.md`, committed like any other `.claude/ops/` state file. Empty-roster
case (spec correction 4): a seat finding no roster file, or a roster with no live peers, proceeds
anyway — it never blocks on discovery. SendMessage is the liveness nudge for a peer known to be
live in-session; the roster plus GitHub Issues/PR comments are the durable truth channel a cloud
session (which cannot message back) still reaches.

### D3 — Reviewer instrument roster (Scope/Open item 3): yes, include doctrine-audit/estate-audit

The reviewer's review-flow roster includes authorkit's read-only instruments
(`naming-audit`, `doctrine-audit`, `bloat-audit`, `attention-audit`, `estate-audit`) alongside the
doc/code checkers already named in `/lead-review`'s routing table — all are read-only sweeps
consistent with the seat's wall (C1 blocks Edit/Write, not Bash/Read), and the seat already cites
doc IDs in its Issues, which is exactly what a doctrine-audit finding needs to reference. Ruling:
yes; `/team-scaffolding reviewer`'s printed charter names these five instruments as in-roster.

## Risks

- **R1 — `settings.local.json` merge clobbers a human's own local overrides.** Mitigated by C1's
  "merge if exists, never clobber unrelated keys" rule; `/team-scaffolding` reads-modifies-writes rather
  than overwriting the file wholesale.
- **R2 — a future platform change makes `deny` advisory instead of a hard block.** Out of scope
  to defend against; I2's live smoke test is the acceptance gate specifically because it tests the
  platform's actual behavior, not this LLD's assumption about it.
- **R3 — the reviewer seat legitimately needs one write path later (e.g. its own scratch
  notes).** Not addressed here — Scope/Open leaves this to a future revision; the current profile
  denies Edit/Write outright per C1's reasoning that the seat has no such path today.
