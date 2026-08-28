# `.claude/ops/fleet.json` — the per-repo fleet manifest

Per-repo variation in how the standing fleet is run is DATA, not a duplicated command copy
(design ruling, #410, 2026-08-16: `/fleet-bootstrap` and `/team-scaffolding` are plugin commands;
this file is the only thing that varies per repo). `/team-scaffolding <role>` seeds/updates it on
first use in a virgin repo; `/fleet-bootstrap` reads and extends it across a full cold start.

**Location and resolution (scope root, #911 — supersedes the #906/#909 nearest-`fleet.json`
ladder).** The fleet SCOPE ROOT is the nearest ancestor directory, walking from the current
working directory upward and BOUNDED at the repo root (`git rev-parse --show-toplevel`, or the
current worktree's own root — the walk never crosses that boundary in either direction), that
contains a `.claude` directory AT ALL — never the nearest directory that happens to already hold
a `fleet.json`. cwd itself counts as a candidate; the walk does not require a strict parent. The
canonical path is always `<scope root>/.claude/ops/fleet.json`. This fixes the shadowing bug
#909's own ladder produced: an app with its own `.claude/` (e.g. `frontend/apps/<app>/.claude/`)
is its own scope root the moment that directory exists, whether or not `fleet.json` has been
seeded under it yet — an ancestor's `fleet.json` (e.g. the repo root's) sitting ABOVE that scope
root is out of scope, never consulted and never written, however populated it is. A legacy
repo-root copy may still coexist beside an app-scoped one; the two are unrelated records, never
merged or compared. **No `.claude` directory found anywhere between cwd and the repo root
(inclusive)** → there is no scope root to resolve at all; a reader stops and reports that
explicitly rather than falling back to the repo root by silent default or continuing to walk past
it (a repo with genuinely no `.claude/` anywhere is not itself a fleet-shaped case). Readers
report the resolved scope root (its basename) and the `fleet.json` path under it.

**Scope-pointer redirect (#915, Kim's ruling 2026-08-23 — opt-in, one hop).** The nearest-`.claude`
rule above rests on the assumption that a `.claude/` directory implies fleet intent; #915 falsified
that in monorepos where an app dir's `.claude/` exists only for path-scoped skills. The opt-in fix
is a pointer file at `<scope root>/.claude/ops/fleet-scope.json`, shape
`{"scope_root": "<path relative to the repo root, \".\" for the repo root itself>"}`. Resolution
order at the walk's resolved scope root: (1) `ops/fleet.json` PRESENT there → it wins; the pointer,
even if also present, is never consulted — a scope that has its own manifest is its own scope.
(2) `ops/fleet.json` ABSENT and `ops/fleet-scope.json` present → re-resolve the scope root to the
pointed directory (which must itself contain a `.claude/` directory and sit within the repo-root
boundary; a pointer naming a dir outside the boundary or without `.claude/` is a reported error,
never a silent fallback) and proceed against `<pointed root>/.claude/ops/fleet.json` — ONE hop
only: a pointer found at the pointed root is never followed (no chains). Readers report both roots:
the walk's own resolved root and the pointer target actually used. (3) BOTH absent → current
behavior stands unchanged: no walk-up, no ancestor consultation — this preserves the #909/#911
anti-shadowing guarantee for genuinely-fresh app-scope seeds. Each participating app dir needs its
pointer seeded deliberately (by a human or an explicitly instructed session); nothing seeds
pointers automatically.

**The same rule governs a virgin SEED, not only a read (#909, refined #911).** `/fleet-bootstrap`
Phase 0 resolves the scope root by this identical `.claude`-directory walk before deciding
whether there is anything to read. `<scope root>/.claude/ops/fleet.json` absent → this is a fresh
seed AT THAT SCOPE ROOT — never fall through to an ancestor's existing `fleet.json` just because
one exists farther up, and never default to the repo root when a nearer `.claude` directory was
found. The resolved seed root is named in the Phase 6 report so a later reader knows where to
look without re-walking.

## Shape

The `cross_repo_coordination` array below is illustrative, shown populated with this repo's own
real standing channel (issue #866) for concreteness rather than a placeholder — most repos'
`fleet.json` carry no such array at all, and a fresh entry names its own repos/roles/date/
authorizer, never copies this one's values.

```json
{
  "version": 1,
  "expected_branch": "main",
  "seats": {
    "agent":    { "tier": "sonnet+high",  "justification_date": "2026-08-22", "mode": "manual" },
    "reviewer": { "tier": "sonnet+high",  "justification_date": "2026-08-22", "mode": "manual" },
    "planner":  { "tier": "fable+medium", "justification_date": "2026-08-22", "mode": "manual" },
    "product":  { "tier": "sonnet+xhigh", "justification_date": "2026-08-22", "mode": "manual" }
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
  },
  "cross_repo_coordination": [
    {
      "participants": [
        { "repo": "gen-ui-kit", "role": "gen-ui-kit-marshal" },
        { "repo": "plugins", "role": "plugins-marshal" },
        { "repo": "adiav2", "role": "adiav2-marshal" },
        { "repo": "adiav2", "app": "frontend/apps/signup", "role": "signup-marshal" }
      ],
      "established": "2026-08-22",
      "authorized_by": "Kim, confirmed live in the plugins mobilize-chores session (issue #866); motivating example gen-ui-kit gh#1836/#1839; participant-object shape ruled 2026-08-22, issue #878"
    }
  ]
}
```

The trailing three `reviewer` rows show a full retire/takeover cycle: joined, then released
(`/team-scaffolding retire reviewer`, `references/fleet-manifest-schema.md`'s own consumer,
`team-scaffolding`'s Phase 6), then a fresh `joined` row for the taking-over session — no separate
"takeover" action exists; a `joined` row appended after a `released` row for the same role IS the
takeover record.

## Fields

- **`expected_branch`** — the fleet's own expected branch, top-level (sibling to `seats`/
  `live_state`), read/diffed at every bind this schema's "Branch reconcile on every bind" section
  below governs. **Absent reads as `"main"`** — the canonical default per `fleet-rules`'s own
  "shared primary checkout stays on `main`, always" doctrine (cited, not restated): an ordinary
  fleet cold-started in the primary checkout expects every seat on `main`. A fleet cold-started
  inside an already-checked-out campaign worktree seeds this explicitly with that branch name
  instead (`fleet-bootstrap` Phase 0). Never inferred after the fact from a majority vote across
  already-joined seats' own branches — it is seeded once at cold-start and stays authoritative
  until a human deliberately changes it.
- **Schema key vs. printed session name (`agent` role only).** `fleet.json`'s role key stays
  `agent` everywhere in this schema — `seats.agent`, `live_state.joined[].role: "agent"` — and a
  builder never renames it. The PRINTED/roster session name for that role is `{scope}-marshal`,
  not `{scope}-agent` (`team-scaffolding` Phase 1/2, `fleet-bootstrap` Phase 1), where `{scope}`
  is the resolved fleet SCOPE ROOT's own directory basename (#911 — `signup-marshal` for a fleet
  scoped to `frontend/apps/signup`, plain `{repo}-marshal` when the scope root IS the repo root,
  the common case and the one most of this schema's prose still writes out for brevity): the
  seat's session identity matches the `teamwork:bind-team` contract it adopts (ADR-0020's marshal
  vocabulary — `{repo}-team-lead` was this same split's prior value, superseded 2026-08-17, issue
  #586), while the schema key stays the generic role bucket. Every other role's session name is
  its role token verbatim relative to the same scope (`{scope}-reviewer`, `{scope}-planner`,
  `{scope}-product`) — only `agent` has the `-marshal` split.
  **Role-key migration considered and declined this wave (issue #586, 2026-08-17).** #586's
  acceptance criteria left the schema key's migration to the builder's own cheap/not-cheap call.
  Not cheap here: the key is a live data field read by every existing `.claude/ops/fleet.json`
  row across repos (including this repo's own — see below), by every sweepable-invariant grep
  this schema already documents (`justification_date` checks keyed on `seats.*.tier`), and
  potentially by other repos' own copies of this convention with no shared migration path: a
  rename would need a cross-repo sweep this ticket's blast radius never enumerated, not just a
  same-file text edit. The split stays as designed — schema key `agent`, printed name now
  `{scope}-marshal` — confirmed schema-stable, not migrated.
- **`seats.<role>.tier`** — the model/effort tier this seat runs at in THIS repo. Starts equal to
  the canonical seat ladder (`team-scaffolding`'s Phase 4 point 1; retiered 2026-08-22, Kim's
  ruling: agent sonnet+high, reviewer sonnet+high, planner fable+medium, product sonnet+xhigh —
  the prior 2026-08-16 fable-heavy ladder is superseded). **A manifest seeded under a prior
  ladder is NOT silently correct**: the reconcile step below is what surfaces it.
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
- **`live_state.joined[].mode: "skipped"`** — `product` role only (issue #977, `fleet-bootstrap`
  Phase 2's throttle). Distinct from `"dispatched"`: no `Agent` call was made this run because the
  throttle found no real signal since `live_state.gate.since_commit` (below). Same row shape as a
  real dispatch — `agent_name: null`, a `note` naming the checked baseline and that neither signal
  fired — so a later reader distinguishes "checked this run, nothing changed" (a `"skipped"` row
  exists for the date) from "never checked" (no row at all) without re-deriving anything. Never a
  `seats.product.mode` value — the seat's own configured mode stays `"dispatched"`, since that is
  still what happens whenever the throttle does find a signal; `"skipped"` only ever appears on a
  `live_state.joined` row.
- **`live_state.joined[].agent_name`** — **the `SendMessage` address for this row's holder.**
  Read from `ListAgents` at bind time — the harness-assigned session name the holder is actually
  reachable at (e.g. `"plugins-75"`) — never the printed/aspirational role label
  (`"{scope}-marshal"`, `"agent"`). `#902` fixed `fleet-bootstrap`'s own Phase 1 `agent`-seat bind
  (fresh-join and takeover) to write this field rather than leave it `null`, since a `null` here on
  a still-live row is what stranded every peer trying to route a fleet-shaped ask back to this
  repo's marshal (`fleet-rules` Section 7 resolves its routing target off this exact field). **Now
  universal (#903)**: `team-scaffolding`'s own manual-join path (Phase 2 — the sole bind for
  `reviewer`/`planner`, and for a direct `/team-scaffolding agent` join) also resolves and writes
  this field, mirroring `fleet-bootstrap` Phase 1 step 5's mechanic, closing the gap #902 itself
  left open. A `null`/absent `agent_name` on a `mode: "manual"`, live (`action: "joined"`) row is
  now reliably a legacy pre-fix entry, not an expected ongoing writer gap — `fleet-connect`'s
  own Failure branches treat that case explicitly rather than folding it into "no live marshal." A
  background/background-subprocess row's `agent_name` keeps its existing meaning (the dispatched
  `Agent`-tool name, or the subprocess's log-path/PID pointer).
- **`live_state.joined[].branch`** — the binding session's own `git rev-parse --abbrev-ref HEAD`
  at bind time (issue #932). Written today only by `fleet-bootstrap` Phase 1's `agent`/marshal
  bind — the only role a `fleet-bootstrap` run itself binds as a live terminal inheriting a
  human's own cwd; a dispatched/spawned seat (`planner`, `reviewer`, `product`) means something
  different by "which branch" and is out of scope here, left for a future ticket rather than
  guessed at. See "Branch reconcile on every bind" below for the diff this field feeds.
- **`live_state.joined[].worktree_path`** — optional, present only when the binding session's cwd
  is a linked worktree rather than the primary checkout (`git rev-parse --git-common-dir` vs.
  `--git-dir` — differ only inside a linked worktree, the same test `fleet-bootstrap` Phase 5's
  reviewer precondition already runs) — the worktree's absolute path. Absent means the primary
  checkout.
- **`live_state.joined[].branch_mismatch`** — optional, present only when "Branch reconcile on
  every bind" (below) found `branch` diverging from the resolved `expected_branch` at bind time:
  the resolved `expected_branch` value itself, so a later reader isn't left re-deriving what
  "expected" meant at that moment — `expected_branch` can change after the fact. Absent means no
  mismatch was found (or this row predates issue #932 and was never checked).
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
  the two rows read together tell the whole story. **A second, narrower `joined`-atop-`joined`
  shape exists for the `agent` role only** (`fleet-bootstrap` Phase 1 step 1's own takeover path,
  cited there): a still-live (never-`released`) `agent` row found at bind time is a takeover of
  THIS session's own seat, never a second session double-booking it (Phase 1 step 1's accepted-risk
  framing), so the binding session appends a fresh `joined` row directly atop the prior one — with
  no `released` row between — to record its own resolved `agent_name`. Liveness still reads as the
  LATEST row per role, so this never produces two rows read as distinct live holders; it only means
  a raw scan for a `released` row between two `agent`-role `joined` rows is not a reliable way to
  detect this particular takeover shape.
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
- **`live_state.gate`** — the intent-layer ratification record, written by `fleet-bootstrap` Phase
  3 on every hard-gate outcome (`ratified` / `revised-and-reratified` / `rejected-stopped-here`).
  **`null`** until Phase 3 has ever run. **A bare string** (e.g. `"ratified"`) is the pre-#977
  shape — every record written before issue #977 — read as "no throttle baseline available", never
  reinterpreted or migrated in place; Phase 3's next write upgrades it to the object shape below
  the same way `expected_branch`/`branch_mismatch` migrate forward additively elsewhere in this
  schema (no `version` bump, same posture as "No `version` bump for this addition" below).
  **The object shape (#977):**
  ```json
  { "outcome": "ratified", "date": "2026-08-28", "since_commit": "8ed3f7f3a8417f87b46c362c0d11387c2e1b47ea" }
  ```
  - `outcome` — identical vocabulary to the pre-#977 bare string (`ratified` /
    `revised-and-reratified` / `rejected-stopped-here`).
  - `date` — the gate's own date, same value a bare-string-era row's surrounding context would have
    carried only informally.
  - `since_commit` — `git rev-parse HEAD` taken at THIS gate, after whatever commits its own review
    already reflects. This is `fleet-bootstrap` Phase 2's own throttle baseline for the *next* cold
    start: Phase 2 diffs `since_commit..HEAD` for ADR/IDR/PRD filename edits and checks
    `revalidation-queue.json` for a queued falsification before deciding whether dispatching the
    product seat again is worth it, skipping the dispatch (and recording the skip on a
    `live_state.joined` row, `mode: "skipped"` — above) when neither signal fired. **Overwritten
    only by REPLACING the whole `live_state.gate` value at the next Phase 3 run** — unlike
    `live_state.joined`, this field is not append-only; there is exactly one current gate record at
    any time, and its history lives in `live_state.joined`'s own dated `product`-role rows instead.
- **`cross_repo_coordination`** (optional, defaults absent/empty — most repos never carry a
  standing cross-repo channel) — an array of standing coordination channels this repo's fleet
  participates in, alongside other repos' own fleets. Each entry:
  - `participants` — an array of participant objects, one per authorized relay, each
    `{ "repo": <repo name>, "app"?: <sub-app path>, "role": <session name> }`:
    - `repo` — the participating repo name (e.g. `"gen-ui-kit"`, `"plugins"`, `"adiav2"`).
    - `app` — **optional.** Present only when this participant's authority is scoped to a
      sub-app inside `repo` rather than the whole repo — a path relative to the repo root (e.g.
      `"frontend/apps/signup"`). Absent means the participant speaks for the whole repo.
    - `role` — the session name authorized to relay for this participant (mirrors the printed
      orchestrator session name, not the schema's `agent` role key — see the "Schema key vs.
      printed session name" field above; an app-scoped participant's `role` is its own distinct
      session name, e.g. `"signup-marshal"`, not `"{repo}-marshal"`).
  - `established` — the date the channel was stood up.
  - `authorized_by` — free text naming who/what ratified standing the channel up (a human's own
    words, a ticket id, or both).

  Scope: **per-repo local**, matching `live_state.joined`'s existing pattern — each participating
  repo's own `fleet.json` carries its own entry naming the same channel, rather than one shared
  cross-repo store. A shared/synced surface across repos is a bigger design question, deliberately
  out of scope here (issue #866's own Scope/Open). Append-only, same discipline as `live_state.joined` —
  a channel that lapses gets a new entry noting it, never a silent deletion of the old one.

  **Ruling: participant objects, not parallel arrays (Kim, live, 2026-08-22, issue #878).** The
  shape landed at #871/#866 — a flat `repos[]` + `marshal_roles[]` pair — could not express the
  real four-marshal channel: "signup" is not a fifth repo, it is `frontend/apps/signup` inside
  `adiav2`, and session `signup-66` (printed role `signup-marshal`) holds adiav2's `agent` seat
  scoped to that app rather than a seat of its own. Carrying "signup" as a pseudo-repo in the old
  arrays was a workaround, not a model. The `participants[]` shape above is the fix: each entry
  names its own `repo`, an optional `app` when the authority is sub-app-scoped, and its own
  `role`. The old `repos[]`/`marshal_roles[]` pair is **retired, not kept as an alias** — every
  existing copy migrates to `participants[]` in the same wave (this repo's own `fleet.json`,
  below; adiav2's; gen-ui-kit's once its entry is recorded), never a mixed fleet where some
  copies read the old shape and some the new.

  **Two-holder liveness rule for `participants[]` (issue #878).** This is a rule about the
  `cross_repo_coordination` bookkeeping itself, distinct from — and never to be confused with —
  `live_state.joined`'s own collision check above, which governs THIS repo's four canonical local
  seats (`agent`/`reviewer`/`planner`/`product`) and carries no `app` field at all; a
  cross-repo-participant collision is never read off `live_state.joined`, and `live_state.joined`
  is never extended to cover it. Within one `cross_repo_coordination` entry's `participants[]`
  array, a given `repo` may appear **once with no `app`** (its repo-scoped holder) **plus any
  number of times with a distinct `app` each** (its app-scoped holders) — these are different
  participants, not contenders for one slot. Two participant objects collide only when their
  `(repo, app)` pair matches exactly (both absent counts as matching — two repo-scoped entries for
  the same `repo` do collide); a channel author appending a new participant checks the existing
  array for this before adding one. Under this rule, `{repo: "adiav2", role: "adiav2-marshal"}`
  (repo-scoped, no `app`) and `{repo: "adiav2", app: "frontend/apps/signup", role:
  "signup-marshal"}` do **not** collide — their `(repo, app)` pairs differ.

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

## Tier reconcile on every bind (2026-08-22 — the previously-future audit, now wired)

The root cause this closes: the ladder is copied into each repo's `fleet.json` at seed time and
was then treated as a read-only record forever — a doctrine retier stranded every existing
manifest on the old tiers with nothing ever flagging it. Now, EVERY `fleet-bootstrap` Phase 0
read of an existing manifest, and every `team-scaffolding` bind against one, diffs each
`seats.<role>.tier` against the canonical ladder above:

- **Match** → nothing printed; correct is quiet.
- **Mismatch WITH a `justification_date` ON OR AFTER the ladder ruling date** (below) → a known,
  deliberate per-repo deviation; print it as such, leave it. ("On or after", not strictly after —
  a keep recorded on the ruling day itself must not re-flag forever.)
- **Mismatch with a stale or absent justification** (the stranded-old-ladder case) → flag it to
  the human with the diff, and — interactive runs only — offer the correction via one
  `AskUserQuestion` (update to canon / keep as a dated deviation, recording today's
  `justification_date` and the human's reason). Never silently rewritten; unattended runs report
  the mismatch and leave the file untouched.

**Ladder ruling date: `2026-08-22`** — the single labeled comparand for the staleness test above;
a future ladder retier updates this one line in the same change. Note `justification_date` is
also written on CANONICAL rows at seed/update time (the example above dates every seat), so its
mere presence never implies a deviation — only a tier MISMATCH starts this classification at all.

**Reality check — the live BINDING session's own resolved model vs. its seat's `tier` (issue
#919, closes the gap this section left open: the diff above only ever compared the manifest
against the ladder, never against what actually ran).** The manifest-vs-ladder diff above proves
`fleet.json` carries the *right recorded intent*; it proves nothing about whether the session
actually binding a role right now is running AS that intent — a `fleet.json` seeded correctly at
sonnet+high says nothing about a marshal terminal someone happened to launch on Fable. Whenever
this reconcile step runs at an actual bind (`team-scaffolding` Phase 1 for any role;
`fleet-bootstrap` Phase 1 for `agent` specifically — the only role a fleet-bootstrap run itself
binds as a live terminal), the binding session also states its OWN resolved model — a session
already knows this about itself (its own system context states the model it's running as; no
external introspection tool is needed) — and diffs that stated value against `seats.<role>.tier`
for the role being bound. **Match** → nothing printed, same as the manifest-vs-ladder case.
**Mismatch** → flag it plainly as a **deviation-in-fact**, distinct from the manifest-vs-ladder
mismatch above (a manifest can read correctly while the live session running it still doesn't
match): `Session runs <resolved model> — seat tier is <seats.<role>.tier> — deviation-in-fact,
<justified/unjustified>`. Never silently accepted and never blocked — this reconcile step has no
enforcement power over which model a human happened to launch their terminal on — but it is the
one place this fact gets a durable, discoverable record instead of surfacing only when a
downstream spend audit stumbles onto it after the fact (the #919 incident's own origin: an
adia-pay session's roster had to hand-log "session runs Fable, deviation-in-fact" with no
skill-level check ever prompting it). **This is a distinct failure mode from an unpinned
DOWNSTREAM dispatch** (`references/best-practices.md`'s own "sealed contract" bullet, and
`fleet-bootstrap`/`team-scaffolding`'s own dispatch sites) — a live terminal running the wrong
model for ITS OWN seat is a human-launch fact this step can only surface, never fix; a dispatch
that fails to pass `model` explicitly from `seats.<role>.tier` (and `effort` too, on a mechanism
that actually takes it per-dispatch — `Workflow`'s `agent()`, a `claude -p` subprocess spawn;
`effort` rides frontmatter unconditionally on a plain `Agent` dispatch) is a skill-authoring gap
that step fixes directly. Both matter: the marshal terminal itself running Fable IS every
unpinned fork's price (issue #313), so this reality check is also the earliest point that class
of downstream leak becomes visible.

## Branch reconcile on every bind (issue #932)

The root cause this closes: `fleet.json` tracks WHO has joined and at what tier, but never
WHERE — a seat can bind on the wrong branch or a stale worktree entirely and nothing catches it
until a downstream merge conflict or wrong-base PR surfaces the drift, sometimes days later.

**Capture, at every bind this section governs**: `git rev-parse --abbrev-ref HEAD` (the branch)
and, where the binding session's cwd is a linked worktree rather than the primary checkout (the
`--git-common-dir` vs. `--git-dir` test, cited above), that worktree's absolute path. Write both
to the bind's own `live_state.joined` row (`branch` always, `worktree_path` only when linked).

**Diff `branch` against `expected_branch`** (top-level field, above; absent reads as `"main"`):

- **Match** → nothing printed; correct is quiet, same posture as the tier reconcile's own
  manifest-vs-ladder comparison.
- **Mismatch** → flag it plainly — `Session branch <actual> — fleet expects <expected_branch> —
  mismatch` — and write `branch_mismatch: "<expected_branch>"` on that same `live_state.joined`
  row. **This is a flag, never a hard stop**, the identical never-silent/never-blocked posture the
  tier reconcile's own "Reality check" subsection already takes for a model-tier deviation-in-fact:
  a real branch mismatch is exactly the kind of drift a human notices and corrects, or
  deliberately accepts (a seat intentionally working a sub-branch for one slice), not a condition
  severe enough to block a bind the way Phase 3's intent-layer gate does. `fleet-rules` Section
  7's routing/escalation discipline, not this schema, decides what happens next once the flag is
  visible.

**Today's writers.** `fleet-bootstrap` Phase 1 (the `agent`/marshal bind) runs the capture-and-diff
above and writes both new `live_state.joined` fields. `fleet-connect` reads `expected_branch` and
runs the identical comparison against the CONNECTING working session's own branch, but never
writes to `fleet.json` at all — it has no write path today, full stop — so its outcome surfaces
only in that command's own report, never as a `live_state.joined` row (a connecting working
session is not itself a seat bind). Extending this to `planner`/`reviewer`/`product` binds is
deliberately out of scope here — each is a dispatched or spawned process rather than a live
terminal inheriting a human's own cwd, so "which branch is this session on" means something
different there — left for a future ticket rather than guessed at.

**No `version` bump for this addition.** Both new fields are additive and optional with a sensible
default when absent (`expected_branch` absent reads as `"main"`; `branch`/`worktree_path`/
`branch_mismatch` absent on a `live_state.joined` row simply means "not checked" — the same
posture `cross_repo_coordination` already established for an earlier additive field), so an
existing `fleet.json` written before this change keeps reading correctly with no migration step;
a `version` bump is reserved for a change that breaks an existing reader, which this isn't.

## Milestone-report threshold (stretch, gh#896 — not yet wired)

`fleet-rules` Section 3's no-op-silence rule fixes user-facing reporting at "milestone-only"
(gate reached, PR opened, merged, blocked, needs-input) but leaves what counts as a milestone to
per-turn judgment. A future `fleet.json` field — e.g. `report_milestones: [...]` naming the
event set a given repo's marshal narrates to the user — would make that bar config instead,
letting a repo widen or narrow it without re-deriving the judgment call each session. Not wired
here: no field is read or written by this schema today: name it explicitly if a future change
adds one, so a bare mention here doesn't get mistaken for an already-live default.

## Doctrine-audit hook

A future `authorkit:doctrine-audit` edge can point at this schema directly: read every
`fleet.json` under `.claude/ops/`, for each `seats.*` entry compare `tier` against the canonical
ladder, flag any mismatch with `justification_date` absent or null. This file documents the check
so that edge can be added without re-deriving the schema.
