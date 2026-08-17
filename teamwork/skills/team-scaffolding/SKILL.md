---
name: team-scaffolding
description: >-
  Bootstraps this session as one seat of the standing 4-session fleet (`{repo}-team-lead` /
  `{repo}-reviewer` / `{repo}-planner` / `{repo}-product`): names the session, writes or verifies
  the seat's permission profile, prints the comms charter (peer roster + SendMessage-is-a-nudge
  doctrine + durable-channel fallback), then names the matching lead-* command for the human to
  run next. Run
  /team-scaffolding, first argument agent, reviewer, planner, or product, then an optional
  charter — or bare with no role: asks one question offering only missing seats (or seeds a
  virgin repo's fleet manifest first), never re-asking once a role is bound. Also runs the
  reverse: /team-scaffolding retire ROLE releases the retiring session's own seat (un-walls
  settings.local.json, releases fleet.json, syncs fleet-roster.md). NOT a one-off adoption of a
  single lead-* contract with no fleet bootstrap (/lead-team, /lead-review, /lead-planning,
  /lead-product directly); NOT for a task one context can hold (team-or-solo-rules).
disable-model-invocation: true
user-invocable: true
argument-hint: "agent|reviewer|planner|product [charter], or retire ROLE [reason] — bare asks which seat"
---

# team-scaffolding — name the seat, wall it, brief it, then name the lead-* command

Four standing sessions run one project: `{repo}-team-lead` (orchestrator — role key `agent` in
`fleet.json`; Phase 1 covers the schema-key/session-name split), `{repo}-reviewer`
(read-only review seat), `{repo}-planner` (design docs), `{repo}-product` (WHY/WHAT and loop
authority). Each already has an owning contract — `teamwork:leading-teams`, `teamwork:leading-review`,
`teamwork:leading-planning`, `docs:leading-product` — but none of those commands name the session, wall
it, or brief it on its peers; that bootstrap layer is this command, run once per session before
the matching `/lead-*` contract takes over. `$ARGUMENTS`: the role, first token — or bare, see
Phase 1's interactive branch — and an optional charter (the rest, passed straight through to the
adopted contract).

## Phase 1 — Bind the role

Valid roles: `agent`, `reviewer`, `planner`, `product`. Branch on `$ARGUMENTS` (#410
bare-invocation-UX addendum):

- **First token is `retire`** → this is the reverse flow, not a role bind. Skip straight to Phase
  6 with the second token as the role to release and the remainder as an optional reason; Phases
  1–5 (bind/name/wall/brief/hand-off) never run for a retire invocation.
- **A role token given** (`$ARGUMENTS`'s first token is one of the four): **zero questions.**
  Validate against `.claude/ops/fleet.json` — an unrecognized token is a Failure branch. Manifest
  absent (virgin repo, role given directly) → seed it now with the canonical seat ladder (Phase 4
  point 1), today's date as every seat's `justification_date`, `mode: "manual"` for all four —
  canonical defaults, no interview, because an explicit role token is itself the human declining
  the interview. Manifest present → read this role's `live_state.joined` entries and take the
  LATEST one's `action` field (liveness rule and field semantics: `fleet-bootstrap`'s
  `references/fleet-manifest-schema.md`, the canonical home). Live (`"joined"`, or absent) → a
  collision, not a choice: report the existing entry's date and stop (Failure branches) rather
  than layering a second holder over it. Released (`"released"`), or no entry exists yet for this
  role → not a collision; bind immediately — for `reviewer`, after the worktree precondition
  below; every other role goes straight to Phase 2.
- **Bare invocation (no `$ARGUMENTS`)**:
  1. Read `.claude/ops/fleet.json`. **Absent** (virgin repo) → run the manifest-seeding interview
     as ONE BATCHED `AskUserQuestion` round (never sequential — exactly these three questions,
     asked together, no follow-up round): (a) seat set, default the canonical quartet; (b)
     manned-vs-background, one multi-select — which of the seats picked in (a) run background; (c)
     tier ladder — accept the canonical ladder (Phase 4 point 1) as-is, or name per-seat
     deviations with their justification inline in the same answer (a deviation given with no
     justification text is treated as declined — that seat stays canonical, per the schema's own
     mechanizable-sweep requirement in `fleet-bootstrap`'s `references/fleet-manifest-schema.md`).
     Seed the manifest from the answers — this is the same "explicit act, no further interview"
     shape Phase 2 relies on for the role-token branch — then fall through to the role question
     below (step 3) recommending `agent` (orchestrator) first, since nothing has joined yet.
  2. **Present, not virgin** → read `live_state.joined`. All four roles already held (live
     entries, no role missing) → ask nothing; report the roster (who holds what, since when) and
     stop — there is no seat left to bind this session to.
  3. **Otherwise** (present, at least one role missing) → ONE `AskUserQuestion` offering only the
     MISSING seats as options (a held seat is never offered — joining it would be the collision
     Phase 1's role-token branch already rejects, not a live choice here). Recommendation is
     derived from standing-up order, first match wins **among the missing seats only** (a matched
     but already-held seat is skipped, never recommended — it isn't an offerable option): no file
     matches `.claude/docs/prd/*.md` or `.claude/docs/decompositions/*.md` (Phase 4 point 5's own
     intent-layer check) and `product` is missing → `product`; a match exists and `planner` is
     missing → `planner`; `planner` is held and `reviewer` is missing → `reviewer`; otherwise →
     `agent`. The human's pick becomes the bound role; proceed to Phase 2 as if it had been the
     `$ARGUMENTS` token — for `reviewer`, after the worktree precondition below.

**`reviewer`-only precondition (issue #427, C2 amendment in
`.claude/docs/lld/lld-0006-fleet-permission-profile.md`): the reviewer's wall must land in an
isolated worktree, never the shared primary checkout.** Run `git rev-parse --git-common-dir` and
`git rev-parse --git-dir` — they differ only inside a linked worktree (never in the primary
checkout). Different → isolated, proceed. Same → **stop here**, before naming or walling anything:
report that the reviewer seat requires its own worktree (the real fleet runs multiple seats in one
shared checkout by default, and a wall written there would govern every session in it, not just
this one — the exact scope leak #427 found), name `EnterWorktree` as the fix, and instruct
re-running `/team-scaffolding reviewer` from the resulting worktree. This check never runs for the
other three roles — `agent`/`planner`/`product` write no deny profile (Phase 3) and have no
scope-leak risk to guard against.

State the bound role and repo name (basename of `git rev-parse --show-toplevel`, or the worktree
root if inside one) back in one line before proceeding: `Seat: {repo}-<role>` — except role
`agent`, which prints `Seat: {repo}-team-lead` (the session-name/role-key split: the `agent` role
key is schema-stable in `fleet.json`, only the printed/roster session name reads `team-lead`).

## Phase 2 — Name the session (convention, not platform-enforced)

Print `{repo}-<role>` as the session's expected identity — except role `agent`, which is named
`{repo}-team-lead` (never `{repo}-agent`); every other role prints its role token verbatim. There
is no platform hook to rename a live session, so this is a printed instruction plus a durable
record, not an enforced rename (reasoning: `.claude/docs/lld/lld-0006-fleet-permission-profile.md`
D1). Append one dated line to
`.claude/ops/fleet-roster.md` (create it if absent, one Markdown table row: role · session-name ·
date · repo) — this is the roster peers read for discovery (Phase 3).

`.claude/ops/fleet.json` (the structured fleet manifest — schema and rationale in
`teamwork:fleet-bootstrap`'s `references/fleet-manifest-schema.md`, shared by both commands) is
already seeded by now — either Phase 1's bare-invocation branch seeded it via the batched
interview before any role bound, or its role-token branch seeded it with canonical defaults
directly (the explicit token stood in for the interview). Either way seeding never runs twice: an
absent manifest at this point is a Phase 1 defect, not something Phase 2 re-derives. Append this
role's `live_state.joined` entry (role, mode, date, `action: "joined"`, `agent_name: null` for a
manual seat) — field semantics: `fleet-manifest-schema.md`. Every other role's existing entry and
the seat-tier table are read-only from here.

## Phase 3 — Write or verify the permission profile

Branch on role:

- **`reviewer`** — the wall must be STRUCTURAL, not stated (issue #404 spec correction 3), and must
  cover the `Bash` write hole (issue #427, C1a). Follow
  `.claude/docs/lld/lld-0006-fleet-permission-profile.md` C1–C1a exactly:
  1. Merge (never clobber) `deny: ["Edit", "Write"]` plus the `gh`/Read/Grep/Glob allow-list into
     `.claude/settings.local.json` in this worktree.
  2. Merge (never clobber existing `hooks.PreToolUse` entries) a `PreToolUse` hook, matcher
     `Bash`, into the same file: a `command`-type hook denying any `Bash` invocation that doesn't
     match C1a's allowlist — the exact command shape (charset, escape-hatch pattern, JSON) is
     canonical there and never restated here.
  3. Re-read the file and grep for both deny entries AND the hook entry before continuing. If
     verification fails, STOP here and report the failure — do not proceed to Phase 4 believing the
     seat is walled when it might not be.
- **`agent` / `planner` / `product`** — no additional deny profile; these seats need their normal
  write access to dispatch, author docs, or maintain product records. State this explicitly
  (`No permission-profile deviation for this role — full write access retained`) so a reader never
  has to wonder whether the branch was skipped by omission.

## Phase 4 — Print the comms charter

State, as one standing block before any real work:

1. **Seat-tier deviation, dated** (doctrine-audit-class tooling checks for this line; issue #404
   spec correction 2, precedent D08/#395): print the tier this role runs at against the canonical
   seat ladder, with the 2026-08-16 justification date —
   - `agent` — fable+low (canonical orchestration tier: sonnet+high). Justification: forks are
     unpinnable (#313); this seat's `context: fork` dispatches ride fable+low by construction, so
     anything needing a different tier routes through a pinned `Agent` dispatch instead of relying
     on the seat's own tier.
   - `reviewer` — fable+xhigh (vs. the *-checker agent family's fable+medium baseline). Justification: this
     seat spans EVERY artifact class in one project, not one bounded checker
     rubric — the broader judgment surface earns the higher tier the same way `team-lead` runs
     sonnet+high above the checker baseline.
   - `planner` — fable+medium (canonical planning tier). No deviation.
   - `product` — fable+high (planning-tier, outermost slow-turning judgments — loop authority and
     spec-lock gating span the other three seats' work, one tier above the design-grain planner).
2. **SendMessage is the liveness nudge; records are the durable truth channel** (parallel-work-rules).
   A relayed claim from a peer is never trusted over the record it claims to describe — re-read
   the record.
3. **Peer roster**, read from `.claude/ops/fleet-roster.md`: list any other live-dated rows. Empty
   roster (file absent, or no peer rows) → proceed anyway; this seat never blocks on discovery
   (spec correction 4 — a cloud session cannot message back, so blocking on liveness would strand
   it). Fall back to durable records (Issues, PR comments) as the coordination channel regardless
   of roster state.
4. **`reviewer` only** — name the review instrument roster: the doc/code checkers `/lead-review`
   already routes to, plus authorkit's read-only sweeps — `naming-audit`, `doctrine-audit`,
   `bloat-audit`, `attention-audit`, `estate-audit` (ruling: `.claude/docs/lld/lld-0006-fleet-permission-profile.md`
   D3).
5. **`planner` only — standing-order self-check (#410 addendum 3, level 1).** Check
   `.claude/docs/prd/*.md` and `.claude/docs/decompositions/*.md` (IDRs); any file present there
   counts as an intent layer. Neither glob matches → print, as a WARNING (never a block): "No
   intent layer found (`.claude/docs/prd/`, `.claude/docs/decompositions/` — both empty or absent)
   — an ADR or LLD authored from this seat now risks becoming an orphan, with no ratified WHY
   behind it. The `product` seat is the prerequisite: run `/team-scaffolding product` first, or
   proceed at your own risk if the human overrides." A match exists → state that plainly (`Intent
   layer found — orphan-ADR check clear`) and proceed with no warning.
6. **`reviewer` only — standing-order self-check (#410 addendum 3, level 1).** Check for a locked
   spec: any `.claude/docs/spec/*.md` or `.claude/docs/lld/*.md` with frontmatter `status: locked`.
   None found → print, as a NOTICE (never a block): "No spec is locked yet — this session runs
   STYLE-REVIEW-ONLY (formatting, doctrine, naming, obvious defects) until a spec locks;
   contract-correctness review resumes once one does." A locked spec exists → state that plainly
   (`Locked spec found — full contract-correctness review in scope`) and proceed with no notice.
7. **Introduce this seat to the live orchestrator (every role except `agent` — the orchestrator
   never introduces itself to itself; issue #429).** Re-read `.claude/ops/fleet-roster.md` (already
   loaded for point 3) and cross-check `.claude/ops/fleet.json`'s `live_state.joined` entries for
   `role: "agent"`, taking the latest one's `action` — only a `"joined"` (or absent-`action`) row
   counts as live, the same liveness rule Phase 1's collision check uses. On disagreement between
   the two sources (the exact drift class issue #426 found — e.g. the roster still shows a live
   row but `fleet.json`'s latest entry is `"released"`), `fleet.json`'s latest `action` governs;
   the roster is a discovery convenience, `fleet.json` the structured record. **Fleet-scoped only**:
   this step discovers exclusively from these two registered-fleet records — never `ListAgents`,
   which would surface arbitrary unregistered peers (other repos' sessions, other worktrees) that
   issue #429 explicitly rules out as introduction targets; `ListAgents` is legitimate only to
   confirm liveness of a session already named in the roster, never to find one. No live `agent`
   row in either source → skip this step and state so plainly (`No live orchestrator seat —
   skipping introduction`); this never blocks the bootstrap (Phase 4 point 3's own no-blocking
   rule for discovery applies here too). A live row exists → `SendMessage` to its recorded session
   name — `{repo}-team-lead` by convention (lld-0006 D1), never the roster row's literal text,
   which on rows written before #434 may still read `{repo}-agent` — introducing this seat: role,
   session name (`{repo}-<role>`), and the
   charter (the remainder of `$ARGUMENTS` after the role token, or "no charter given" if blank).
   This is the same one-way liveness nudge as point 2, not a request-response handshake — no reply
   is awaited, and a delivery failure (recipient session gone) is reported but does not fail the
   bootstrap; the roster/manifest rows already written in Phase 2 are the durable truth regardless
   of whether the nudge landed.

## Phase 5 — Name the matching lead-* command for the human

Every lead-* target carries `disable-model-invocation: true` by design (adoption is a human's
session, never model-routed — see the rejected alternative below), so this phase can never invoke
one via the Skill tool. Instead, print the exact command the HUMAN types next, with the charter
(the remainder of `$ARGUMENTS` after the role token) appended verbatim, as the final bootstrap
step — mirroring how `authorkit:overhaul-execute` hands a merge/split off as a command-only
`/reshape-skill …` invocation for a human to run, never a Skill-tool call:

| Role | Command to print | Home plugin |
|---|---|---|
| `agent` | `/lead-team` | teamwork |
| `reviewer` | `/lead-review` | teamwork |
| `planner` | `/lead-planning` | teamwork |
| `product` | `/lead-product` | teamwork (`skills/lead-product`, moved from docs — issue #433) |

`product`'s handoff is now a same-plugin command (the `product-authoring` skill, now `leading-product`
here, and its `product-leader-agent` full-moved from docs to teamwork under issue #433's ruling); the prior
cross-plugin degrade branch is retired along with the docs-absent case it existed for.

This session does NOT adopt the contract itself. `team-scaffolding`'s own discipline (Phases 1–4)
has already run and does not repeat; the printed command is what carries the session forward once
the human types it.

## Phase 6 — Retire a seat (`/team-scaffolding retire <role> [reason]`)

The RETIRING session runs this itself, before it stops — never the taking-over session (it has no
standing to un-wall a seat it never held) and never a bystander orchestrator (issue #426's Open
item: who executes the un-wall must be stated, not implied). **A `reviewer` session's own
`deny: ["Edit", "Write"]` wall (Phase 3) covers exactly the `Edit`/`Write` tools, not `Bash`** —
every write in this phase (all three steps, not step 1 alone: `fleet.json` and
`fleet-roster.md` are ordinary worktree files the reviewer wall also blocks via Edit/Write) runs
as a `Bash` command (`sed`/`cat`/`printf`, whatever's surgical) for that reason, with a `Read`
re-check after each write (`Read` is never denied either) — stating the mechanism here so the
model's first attempt isn't an `Edit` call that walks straight into the wall it's trying to
remove. **This does not self-lock against issue #427's `Bash`-gating `PreToolUse` hook (Phase
3/C1a)**: that hook's allowlist carries a deliberate, narrow escape hatch for exactly this
step — `sed`/`cat`/`printf` commands naming one of the three fleet-state files, no chaining
metacharacters — documented in `lld-0006-fleet-permission-profile.md` C1a, never re-derived here.
Run these three steps in order; a failure at any step stops there and is reported (Failure
branches) rather than silently skipped:

1. **Un-wall, `reviewer` only.** Remove exactly the entries Phase 3/C1–C1a added to
   `.claude/settings.local.json` (`deny: ["Edit", "Write"]`, the `gh`/Read/Grep/Glob allow-list,
   and the `PreToolUse`/`Bash` hook) — surgical removal via `Bash`, never a wholesale file delete,
   since the file may carry unrelated keys the human added by hand (the same merge-never-clobber
   discipline C1 uses going in applies going out). Re-read the file and confirm the deny entries
   AND the hook entry are gone before continuing. Other roles (`agent`/`planner`/`product`) never
   wrote a deny profile (Phase 3), so this step is a no-op for them — state that plainly rather
   than skipping silently, and use the normal `Edit`/`Write` tools for steps 2-3 (nothing walls
   those roles). The seat is deliberately left un-walled, not re-walled to some default: the next
   session to bind `reviewer` re-runs Phase 3 fresh and re-writes its own wall — no session
   inherits another's wall.
2. **Append the release record.** In `.claude/ops/fleet.json`, append (never rewrite) a
   `live_state.joined` entry for this role: `{ "role": "<role>", "mode": "<from the entry being
   released>", "date": "<today>", "action": "released", "agent_name": null, "reason":
   "<the optional reason argument, or null>" }` — same append-only discipline as every other
   `live_state.joined` write (field semantics: `fleet-manifest-schema.md`'s `action`/`reason`
   entries, the canonical home for this rule).
3. **Sync the roster.** Append one dated row to `.claude/ops/fleet-roster.md` recording the
   release (role · `RETIRED` · date · repo) — this is what keeps the roster (Phase 2's discovery
   file) and `fleet.json` (Phase 1's collision check) agreeing on who currently holds the seat,
   closing the exact drift issue #426 found (a hand-edited roster row with no matching manifest
   record). Never hand-edit an existing roster row in place — append, matching the file's own
   append-only convention.

Report the three steps' outcomes in one line (`Retired: {repo}-<role> — wall removed (or n/a) ·
fleet.json released · roster synced`) — role `agent` reports `Retired: {repo}-team-lead` (same
exception as Phase 1/2) — and stop; retiring never hands off to a `/lead-*` command
(Phase 5 is bind-only, not part of this flow).

## Failure branches

- **Unrecognized role token** → report the four valid roles and stop; no session naming, no
  profile write, no adoption.
- **Bare invocation with all four roles already held** → report the roster and stop (Phase 1); no
  question asked, nothing to bind this session to.
- **A role (given or picked via Phase 1's question) whose `live_state.joined` already carries a
  still-live entry** → report the existing holder's date and stop; never layer a second holder.
- **Phase 3's `settings.local.json` write or verification fails for `reviewer`** → stop at Phase 3;
  never silently downgrade to a stated-only wall.
- **`docs` not installed and role is `product`** → name the gap plainly (Phases 1–4 still ran; only
  Phase 5's command names an uninstalled plugin) and point at installing `docs`.
- **Re-invoked in a session that already bootstrapped a different role** → name the existing role
  and require an explicit close-or-switch decision from the human before re-running; never silently
  layer a second role's profile over the first.
- **`retire <role>` given no role token, or an unrecognized one** → report the four valid roles
  and stop; no fleet.json write, no roster write.
- **`retire <role>` where the role's latest `live_state.joined` entry is already `"released"` (or
  no entry exists at all)** → nothing live to release; report that and stop rather than appending
  a redundant release record.
- **Phase 6's `settings.local.json` un-wall or its re-verification fails for `reviewer`** → stop at
  step 1; do not proceed to append the fleet.json release record while the wall's true state is
  unknown.

## Done

Done when Phases 1–4 have completed for the bound role (profile verified where applicable, roster
row appended, charter printed, orchestrator introduction sent, explicitly skipped, or n/a for the
`agent` seat itself) and Phase 5
has named the matching lead-* command for the human to run next — never when only the bootstrap
layer ran with no command named, and never claiming the session itself adopted the contract
(Skill-tool invocation is structurally impossible against a `disable-model-invocation` target).
For a `retire` invocation: done when all three Phase 6 steps have completed (or been reported as
no-ops) and the one-line outcome is printed — never when only the un-wall ran with fleet.json or
the roster left unsynced.

## Rejected alternatives

Flipping the four lead-* skills' `disable-model-invocation` flag so Phase 5 could invoke them via
the Skill tool was considered and rejected: command-only adoption is deliberate — a seat contract
is adopted by a human's session, never model-routed (`leading-teams`'s own body defends this flag for
the same reason). The fix stays scoped to Phase 5's own false claim, not the target skills'
invocation contract.
