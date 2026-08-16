---
doc-type: lld
id: lld-0006-fleet-permission-profile
status: draft
version: 0.2.0
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

**2026-08-16 amendment (issue #427; this LLD's `status: draft` is editable, not append-only).**
C1's original "blocks every path" claim was falsified live and is corrected below, not restated.
Two edges broke: (a) C2's per-worktree scoping assumed a topology — one reviewer session per
worktree — the real fleet doesn't have; multiple seats routinely share one checkout, so the wall
governed every session in that checkout, not only the reviewer's. (b) `deny: ["Edit", "Write"]`
blocks those two TOOLS, not the write CAPABILITY — a `Bash` redirect or a Python file write is
neither tool and passed straight through under the machine's global `bypassPermissions` default.
C1a and C2 below are the fix; Phase 6's retirement step (`/team-scaffolding retire`, #426/PR #430)
closes the persistence half of edge (a). The corrected enforcement claim is stated plainly at the
end of this amendment instead of re-asserting "blocks every path."

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

`deny` on the bare tool names `Edit`/`Write` blocks every path THROUGH THOSE TWO TOOLS, not a glob
subset of them — the reviewer seat has no legitimate local-file-write path at all (its output is
GitHub Issues/PR comments, a platform API call via `Bash(gh ...)`, never a filesystem mutation),
so an allow-list carve-out (the `ops-write-sandbox-rules` scoped allow-list pattern) is the wrong
shape here: that pattern exists for seats that DO need one scoped write path. The reviewer needs
zero writes through `Edit`/`Write`. **This does not block writes issued through `Bash`** — see C1a;
the corrected, non-falsified claim is "blocks the Edit/Write tool paths," not "blocks every write
path."

Settings precedence (platform-documented): project `.claude/settings.local.json` layers over
`.claude/settings.json`, and `deny` always wins over any `allow` at any layer — so this profile is
tamper-resistant against the seat's own later prose even if the adopted contract tried to grant
Write back. This is a layer-precedence rule (a *later* layer's `deny` beats an *earlier* layer's
`allow`), not a same-layer specificity rule — see C1a for why that distinction rules out a bare
`Bash` deny as a fix for the Bash hole.

### C1a — The Bash hole and why `permissions.deny` alone cannot close it

`permissions.deny` walls TOOL NAMES/patterns, not the write CAPABILITY. `Bash` is
Turing-complete — redirects (`echo x > file`), `python3 -c "open(..., 'w')"`, `sed -i`, `dd`, `tee`,
`cp`/`mv` onto a tracked path, are all `Bash`, none are `Edit`/`Write`, and C1's deny list never
named `Bash` — under this machine's global `bypassPermissions` default they ran with no prompt at
all (issue #427's live repro).

**Why "just deny bare `Bash` too" doesn't work**: within one settings layer, `deny` is checked
unconditionally against every matching rule — a `deny: ["Bash"]` entry blocks ALL `Bash`,
including the `Bash(gh issue *)` / `Bash(gh pr comment *)` / `Bash(gh pr view *)` / `Bash(gh api
*)` calls the reviewer's own charter requires (Interface I1). Deny-wins-over-allow is not scoped
to "more specific allow beats less specific deny" — a bare `Bash` deny and a scoped `Bash(gh ...)`
allow in the same file would leave the reviewer unable to do its job, not selectively walled.
`permissions.deny`/`allow` cannot express "block Bash except these four gh shapes" — there is no
tool-name-pattern mechanism for that carve-out.

**What actually closes the hole: a `PreToolUse` hook, matcher `Bash`, that inspects the literal
command string.** Unlike a permission pattern, a hook script sees `tool_input.command` and can
apply real logic: allow only if the command matches one of the four `gh` shapes above (against a
POSITIVE allowlist charset — letters, digits, and `` _.,:/'"() %=?!#- `` — wide enough for
realistic `gh pr comment`/`gh api` bodies and query strings), or the retirement escape hatch below
(a narrower charset, `` _.,:/'"() %- ``, deliberately excluding `=?!#`). Chaining/substitution
characters (`;`, `&`, `|`, `` ` ``, `$`, `<`) are excluded by construction (not present in either
allowed set), not by enumerating them, which is the correct direction for an allowlist and avoids
the enumeration bugs a negated character class invites; `>` is excluded from both charsets too and
re-admitted only as the fixed, literal `" >> "` token immediately before one of the three exact
retirement paths (never bare — append only, never truncate). A literal newline anywhere in the
command is checked and rejected explicitly (a regex character class alone does not reliably
exclude one against multi-line input; `grep`/`[[ =~ ]]` match per line, not per whole string, so
this needs its own check) — and `hookSpecificOutput.permissionDecision: "deny"` covers everything
else. Shape (merged into the same `.claude/settings.local.json`, never a separate file — one place
to un-wall on retirement; **verified end-to-end with `bash`/`python3 re` against the ALLOW/DENY
cases below before this amendment shipped, not merely inspected** — three drafts each had a real
bug caught only by running them):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "CMD=$(jq -r '.tool_input.command'); ALLOW=\"^gh (issue|pr comment|pr view|api) [A-Za-z0-9_.,:/'\\\"() %=?!#-]*\\$\"; ESCAPE=\"^(sed|cat|printf) [A-Za-z0-9_.,:/'\\\"() %-]*( >> )?\\\\.claude/(settings\\\\.local\\\\.json|ops/fleet\\\\.json|ops/fleet-roster\\\\.md)\\$\"; if [[ \"$CMD\" != *$'\\n'* ]] && { [[ \"$CMD\" =~ $ALLOW ]] || [[ \"$CMD\" =~ $ESCAPE ]]; }; then echo '{}'; else echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"reviewer seat: Bash is gh-only, plus surgical edits to the three fleet-state files for retirement (lld-0006 C1a)\"}}'; fi"
          }
        ]
      }
    ]
  }
}
```

`$ESCAPE` is the retirement escape hatch, deliberate and narrow: **the trailing fleet-state path is
now mandatory, not optional** — only `>>` is optional (present for the append shape `printf ... >>
<path>`, absent for the in-place shape `sed -i ... <path>`) — an earlier draft made the whole
`( >> path)` group optional, which let bare `sed -i '...' /etc/passwd` through: same-charset,
no fleet path, still matched. That's fixed: every `sed`/`cat`/`printf` invocation this hook allows
must end in one of the three literal paths, full stop. `$CMD` is captured once and tested against
both patterns from the variable — the command is never re-read from stdin a second time, which
would silently starve the second test (an earlier draft piped `jq` into two chained `grep`s and
had exactly that bug). **Known residual gap, named rather than hidden**: `fleet.json`'s append is a
structured JSON array entry (Phase 6 step 2), not a flat text append — a real `sed -i`/`printf >>`
invocation big enough to do that safely may need characters this charset doesn't admit (e.g. `jq`
piped through a temp-file-and-`mv` shape). If Phase 6's live execution finds the charset too narrow
for that one step, widening it is a follow-up, done deliberately and re-verified the same way, not
silently worked around with a broader escape hatch.

`/team-scaffolding reviewer` now writes this hook into the same `.claude/settings.local.json`
(Phase 3), verified the same way as C3 verifies the deny entries. **Residual risk, stated honestly
rather than glossed over**: this is a regex-shaped allowlist over an honest, cooperative session —
it structurally stops the reviewer from *habitually* reaching for `Bash` to write (the actual
failure mode #427 found, not an adversarial one), and the positive-charset design closes the
concrete gaps a negated-class version had (no stray `<`/`>`/`\n` bypass). It is still not proven
sound against a determined adversarial payload constructed specifically to defeat this exact
regex — no stronger, general-purpose Bash-content sandbox is available in this platform's
permission model today; see Risks, R4.

### C2 — Why per-worktree, not a checked-in fleet profile

A checked-in `.claude/settings.json` deny rule would block Edit/Write for EVERY session in the
repo, including the agent/planner/product seats that legitimately write. The reviewer's wall must
apply to exactly the one worktree that session is running in — `settings.local.json` is
gitignored by the platform's own convention (never committed) and inherently per-checkout, which
is exactly the scope needed. `/team-scaffolding` writes it as a side effect of the `reviewer` role
branch; the other three roles never touch this file.

**2026-08-16 correction (issue #427, edge 1 — C2 falsified as originally written)**: "per-worktree"
described the file's SCOPE mechanism correctly but silently assumed a topology that doesn't hold —
that a reviewer session always runs in its OWN worktree, one seat per checkout. The real fleet
runs multiple seats in ONE shared checkout by default; `settings.local.json` written there governs
every session in that checkout, including seats that join later and legitimately need to write.
**C2 is now a stated PRECONDITION, not an assumption**: `/team-scaffolding reviewer`'s Phase 1
verifies the session is in an isolated worktree (`git rev-parse --git-common-dir` differs from
`--git-dir` — true only inside a linked worktree, never the primary checkout) before Phase 3 writes
anything. Not isolated → Phase 1 stops and names `EnterWorktree` as the fix (never auto-invokes it
— switching cwd mid-bootstrap out from under a session already in Phase 1 is a bigger surprise than
asking the human to re-run the command from the resulting worktree). This makes the reviewer's
wall genuinely worktree-scoped in practice, closing edge 1's scope leak; Phase 6 (#426/PR #430)
closes edge 1's persistence half (the wall no longer outlives the reviewer's own session in that
checkout).

### C3 — Verification, not blind trust

After writing the profile, `/team-scaffolding` re-reads the file back and greps for the two deny
entries AND the C1a hook entry (2026-08-16 amendment, issue #427 — the hook is part of the wall,
not a separate mechanism) before printing the comms charter — a write that silently failed
(permission prompt declined, disk error) must not let the seat believe it is walled when it
isn't. If verification
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

A live smoke test, two paths (2026-08-16 amendment, issue #427 — the original single-path test
covered only the first and let the second edge ship unverified):

1. **Edit/Write path**: after `/team-scaffolding reviewer` completes, attempt a trivial `Write` to
   any path in the worktree — the platform denies it without a permission prompt reaching the
   human (a `deny` entry is a hard block, not a promptable `ask`).
2. **Bash path**: attempt a trivial write-shaped `Bash` command (e.g. `echo x > /tmp/probe`) —
   C1a's `PreToolUse` hook must deny it (`permissionDecision: "deny"`), and a legitimate allowed
   command (`gh pr view <n>`) must still pass.

Record both denial texts (and the one allowed-command pass) in the build's Findings write-back as
the structural-wall proof, mirroring `docs:intake-lead`'s A4 smoke-test precedent for its own
agent-level wall.

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
- **R4 — C1a's Bash-command hook is a regex allowlist, not a proven-sound sandbox (2026-08-16,
  issue #427).** It stops the failure mode actually observed (an honest session reaching for
  `Bash` as an Edit/Write workaround) and rejects shell-metacharacter chaining onto an allowed
  `gh` prefix, but a determined adversarial payload designed specifically to evade the regex is
  not proven unreachable — no stronger general-purpose Bash-content sandbox exists in this
  platform's permission model today. Accepted as the honest residual risk rather than papered over
  with a stronger claim; a future revision may tighten the allowlist further or adopt a
  platform-level content sandbox if one ships.
- **R5 — the worktree precondition (C2 amendment) depends on the session actually running
  `/team-scaffolding reviewer` from inside a linked worktree; nothing stops a human from typing the
  command from the primary checkout and then declining to run `EnterWorktree` when told to.**
  Phase 1 stops and states the requirement rather than writing a wall it knows is mis-scoped, but
  it cannot force the human's next action — the same "printed instruction, not platform-enforced"
  shape D1 already accepts for session naming.
