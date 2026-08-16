---
name: team-scaffolding
description: >-
  Bootstraps this session as one seat of the standing 4-session fleet (`{repo}-agent` /
  `{repo}-reviewer` / `{repo}-planner` / `{repo}-product`): names the session, writes or verifies
  the seat's permission profile, prints the comms charter (peer roster + SendMessage-is-a-nudge
  doctrine + durable-channel fallback), then names the matching lead-* command for the human to
  run next. Run
  /team-scaffolding, first argument agent, reviewer, planner, or product, then an optional
  charter — or bare with no role: asks one question offering only missing seats (or seeds a
  virgin repo's fleet manifest first), never re-asking once a role is bound. NOT a one-off
  adoption of a single lead-* contract with no fleet bootstrap (/lead-team,
  /lead-review, /lead-planning, /product-authoring directly); NOT for a task one context can hold
  (team-or-solo-rules).
disable-model-invocation: true
user-invocable: true
argument-hint: "[agent|reviewer|planner|product [charter]] — bare asks which seat"
---

# team-scaffolding — name the seat, wall it, brief it, then name the lead-* command

Four standing sessions run one project: `{repo}-agent` (orchestrator), `{repo}-reviewer`
(read-only review desk), `{repo}-planner` (design docs), `{repo}-product` (WHY/WHAT and loop
authority). Each already has an owning contract — `teamwork:lead-team`, `teamwork:lead-review`,
`teamwork:lead-planning`, `docs:product-authoring` — but none of those commands name the session, wall
it, or brief it on its peers; that bootstrap layer is this command, run once per session before
the matching `/lead-*` contract takes over. `$ARGUMENTS`: the role, first token — or bare, see
Phase 1's interactive branch — and an optional charter (the rest, passed straight through to the
adopted contract).

## Phase 1 — Bind the role

Valid roles: `agent`, `reviewer`, `planner`, `product`. Branch on `$ARGUMENTS` (#410
bare-invocation-UX addendum):

- **A role token given** (`$ARGUMENTS`'s first token is one of the four): **zero questions.**
  Validate against `.claude/ops/fleet.json` — an unrecognized token is a Failure branch. Manifest
  absent (virgin repo, role given directly) → seed it now with the canonical seat ladder (Phase 4
  point 1), today's date as every seat's `justification_date`, `mode: "manual"` for all four —
  canonical defaults, no interview, because an explicit role token is itself the human declining
  the interview. Manifest present and this role's `live_state.joined` already carries a still-live
  manual/dispatched entry → a collision, not a choice: report the existing entry's date and stop
  (Failure branches) rather than layering a second holder over it. Otherwise (valid, unheld role)
  → bind immediately, straight to Phase 2.
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
     `$ARGUMENTS` token.

State the bound role and repo name (basename of `git rev-parse --show-toplevel`, or the worktree
root if inside one) back in one line before proceeding: `Seat: {repo}-<role>`.

## Phase 2 — Name the session (convention, not platform-enforced)

Print `{repo}-<role>` as the session's expected identity — there is no platform hook to rename a
live session, so this is a printed instruction plus a durable record, not an enforced rename
(reasoning: `.claude/docs/lld/lld-0006-fleet-permission-profile.md` D1). Append one dated line to
`.claude/ops/fleet-roster.md` (create it if absent, one Markdown table row: role · session-name ·
date · repo) — this is the roster peers read for discovery (Phase 3).

`.claude/ops/fleet.json` (the structured fleet manifest — schema and rationale in
`teamwork:fleet-bootstrap`'s `references/fleet-manifest-schema.md`, shared by both commands) is
already seeded by now — either Phase 1's bare-invocation branch seeded it via the batched
interview before any role bound, or its role-token branch seeded it with canonical defaults
directly (the explicit token stood in for the interview). Either way seeding never runs twice: an
absent manifest at this point is a Phase 1 defect, not something Phase 2 re-derives. Append this
role's `live_state.joined` entry (role, mode, date, `agent_name: null` for a manual seat); every
other role's existing entry and the seat-tier table are read-only from here.

## Phase 3 — Write or verify the permission profile

Branch on role:

- **`reviewer`** — the wall must be STRUCTURAL, not stated (issue #404 spec correction 3). Follow
  `.claude/docs/lld/lld-0006-fleet-permission-profile.md` C1–C3 exactly: merge (never clobber) `deny: ["Edit",
  "Write"]` plus the `gh`/Read/Grep/Glob allow-list into `.claude/settings.local.json` in this
  worktree, then re-read the file and grep for both deny entries before continuing. If
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
     seat is the review DESK across every artifact class in one project, not one bounded checker
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
| `product` | `/product-authoring` | docs (soft cross-plugin mention) |

`product`'s handoff is a soft cross-plugin mention — it degrades to "install docs to bootstrap
the product seat" if `docs` isn't installed (Failure branches, below).

This session does NOT adopt the contract itself. `team-scaffolding`'s own discipline (Phases 1–4)
has already run and does not repeat; the printed command is what carries the session forward once
the human types it.

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

## Done

Done when Phases 1–4 have completed for the bound role (profile verified where applicable, roster
row appended, charter printed) and Phase 5 has named the matching lead-* command for the human to
run next — never when only the bootstrap layer ran with no command named, and never claiming the
session itself adopted the contract (Skill-tool invocation is structurally impossible against a
`disable-model-invocation` target).

## Rejected alternatives

Flipping the four lead-* skills' `disable-model-invocation` flag so Phase 5 could invoke them via
the Skill tool was considered and rejected: command-only adoption is deliberate — a seat contract
is adopted by a human's session, never model-routed (`lead-team`'s own body defends this flag for
the same reason). The fix stays scoped to Phase 5's own false claim, not the target skills'
invocation contract.
