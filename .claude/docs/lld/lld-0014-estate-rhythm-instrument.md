---
doc-type: lld
id: lld-0014-estate-rhythm-instrument
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#626
spec: none — the ticket's own Acceptance section carries the checkable criteria, and idr-0011
  (LOCKED) already carries the ruled claim and its named leans; a standalone SPEC would restate
  what the ticket and the locked IDR already state (same routing test lld-0008/lld-0009/lld-0013
  applied).
---
# LLD — Estate rhythm: the calendar instrument + the first standing schedule (#626)

**Verdict, head-first:** three lean deliverables, all living state under `.claude/ops/`, plus one
`fleet-rules` bullet: (a) `.claude/ops/calendar.md` — the calendar canon idr-0011 rules must
exist, listing every standing loop with a tunable cadence + owner; (b) a new "Kim's ruling/merge
queue" section inside the existing `.claude/ops/held-items.md` (idr-0011's own named lean channel)
plus a `fleet-rules` Section 3 bullet making batching-not-interrupting the default; (c) the first
standing schedule itself — gh#626's Acceptance requires it to actually EXIST, not just be
described. This build's dispatch context carries the `schedule` skill but not the `RemoteTrigger`
tool it needs to call live (no `ToolSearch` in this seat's tool wall) — so (c) ships as the exact
routine-create-body committed at `.claude/ops/routines/daily-board-drain.json`, with a one-line
arm instruction, and the deviation from the live-armed lean is named here and on the ticket
rather than silently substituted.

## Resolution 1 — Calendar canon location and shape: a lean living-state ops file

**Resolved:** `.claude/ops/calendar.md`, exactly idr-0011's own stated lean (its Open questions:
"Calendar canon location — lean: a living-state ops file"). Rejected: folding the calendar into
the IDR itself (idr-0011 is LOCKED, append-only — a cadence tweak would owe a supersession per
edit, the exact failure mode idr-0011's own Record-type note names for why this is an IDR and not
an ADR in the first place) or into `fleet.json` (that file is fleet REGISTRATION state — seats,
roster, live_state — a different axis from WHEN a loop fires; conflating the two would make
`fleet.json` do two jobs).

**Rows populated (sane defaults, explicitly marked tunable, per gh#626's Scope/Open item 1 —
"which loops + exact cadences… needs the ruling round"):**

| Loop | Default cadence | Evidence for the default |
|---|---|---|
| Daily board drain | Daily | `/mobilize-chores auto`'s own existence as the unattended confirm-free pass names it as the natural daily unit; gh#626's seed comment names this as the routine to build |
| Ops sweep | issue-sorter hourly (verified live — `.claude/ops/reports/*.md` shows hourly firings back to 2026-07-18); decision-watcher/repo-cleaner/chore-planner session-scoped, re-armed per session (verified: their own agent descriptions say so) | This is the CURRENT state, not a proposal — the row records what already fires, and names which slice (issue-sorter) already survives a session boundary and which three don't |
| Weekly doctrine re-validation | Weekly | idr-0009's own Open questions: "cadence… the rhythm ruling (idr-0011) assigns"; weekly is idr-0009's own instrument (decision-watcher's re-validation mode) not-yet-built — this row reserves the slot idr-0009 asks for, it does not build the mode |
| Release-boundary artifact refresh | Event-triggered (source doc/content change or release boundary), not calendar-time | lld-0013 Resolution 4 (#619) already rules this as a named procedure, never a hook; the calendar records it as a loop even though it isn't clock-driven, since idr-0011's claim is "every standing loop," not "every clock-driven loop" |
| Monthly brief + roadmap review | Monthly | Both docs' own `review-cadence: monthly` frontmatter (verified: `.claude/docs/brief/brief-nonoun-plugins.md`, `.claude/docs/roadmap/roadmap-nonoun-plugins.md`) — idr-0011's own Why cites this exact frontmatter as "a stated cadence nothing fires"; the calendar is what a re-validation sweep or a human checks these against |

**Agent-verifiability split (per gh#626 Acceptance):** the file's existence and doc_lint-clean
shape is payload/API-layer checkable; cadence FITNESS (is weekly the right cadence for doctrine
re-validation) is human-assert, named as such in the file's own header rather than presented as
ratified.

## Resolution 2 — Kim's ruling/merge queue: a section inside `held-items.md`, not a new file

**Resolved:** add a "Kim's ruling/merge queue" section to the EXISTING `.claude/ops/held-items.md`
rather than minting a new file, per idr-0011's own named lean ("channel: `held-items.md`",
gh#626's seed comment) and per the seed comment's explicit instruction. `held-items.md` already
exists as a human-gate-item ledger (filing-author holds for `ops-issues`) with a proven
append-then-resolve shape; the new section reuses that shape for a structurally different but
conceptually adjacent class of item — "something only Kim can decide" — under its own entry
template so the two never collide. The file's own top-of-file note is edited to disclose the
two-section split explicitly (never a silent repurposing of a narrowly-scoped file).

**Rejected:** a new `.claude/ops/ruling-queue.md`. Two files that both mean "things pending Kim's
decision," landing in the same daily scan, is the exact "arriving ad hoc across scattered
channels" failure idr-0011's claim names — one file, two sections, one scan.

**`fleet-rules` bullet (Resolution complement):** Section 3 (Communication routing) of
`teamwork/skills/fleet-rules/SKILL.md` gains one bullet naming the batching default explicitly —
placed immediately after the existing T2 quote-not-obey bullet (same section, same
never-escalate-straight-to-the-human family of defaults), citing `held-items.md`'s queue section
and `calendar.md` as canon rather than restating cadence numbers inline. This is the "fleet-rules
bullet that human-gate items batch into it rather than interrupting piecemeal" gh#626's own
seed comment names.

## Resolution 3 — First standing schedule: committed routine definition, live-arm deviation named

**Resolved, with a named deviation from the stated lean.** gh#626's seed comment leans "created
via the schedule skill if reachable from your context, else the exact routine definition
committed under `.claude/ops/`". Both branches were tried, in order:

1. **`schedule` skill invocation** (Skill tool) — reachable and functional; it launched and
   returned its full workflow (RemoteTrigger action shapes, cron rules, environment id
   `env_01EHSARYCEQf7X8tiCZJbNV6`, model default `claude-sonnet-5`).
2. **`RemoteTrigger` tool itself** — NOT reachable. The skill's own first instruction is `load it
   first with ToolSearch select:RemoteTrigger`; this build dispatch's tool wall (Read, Grep, Glob,
   Edit, Write, Bash, Skill, Agent — `build-leader`'s own frontmatter) carries no `ToolSearch` and
   no `RemoteTrigger`. The skill loading successfully is not the same as the mechanism it drives
   being reachable — confirmed by attempting the call and finding no such tool in this seat's
   available set, not assumed.

**Fallback taken (the ticket's own named "else"):** `.claude/ops/routines/daily-board-drain.json`
carries the EXACT `RemoteTrigger` `create`-body — name, cron (`0 9 * * *` UTC, a sane daily
default, tunable), the repo source, tool allowlist, environment id, model, and a
self-contained prompt (the cloud session starts with zero context, per the schedule skill's own
note) instructing the fired session to run `/mobilize-chores auto` and report plainly if nothing
was buildable. A `_comment` key inside the file states the deviation and the one-line arm
instruction (`RemoteTrigger {action: "create", body: <this file, minus _comment>}`, or `/schedule`
pointed at the file, from any session that DOES carry the tool) — never silently presented as an
armed routine.

**gh#626's Acceptance line — "the schedule's existence is checkable via CronList / `/schedule`
listing"** is honestly NOT satisfied by this fallback until a human or a future session with
`RemoteTrigger` actually runs the arm step; `calendar.md`'s own "First standing schedule" section
states this explicitly and names the exact command that flips its Status column once armed. This
is disclosed as a deviation on the ticket's own dated comment and in the closing Findings entry,
per this workspace's stale-context-is-a-defect doctrine — never silently reported as "done."

## Components

1. **`.claude/ops/calendar.md`** (new) — Resolution 1.
2. **`.claude/ops/held-items.md`** (edited) — top-of-file split note + new "Kim's ruling/merge
   queue" section, own entry template — Resolution 2.
3. **`teamwork/skills/fleet-rules/SKILL.md`** (edited, body-only, no frontmatter/description
   change) — one new Section 3 bullet — Resolution 2's complement. Rides a fresh-context
   `harness:skill-checker` pass before merge (`.claude/rules/plugin-authoring.md`'s semantic-edit
   invariant — this is a body edit to a prompt-carrying artifact).
4. **`.claude/ops/routines/daily-board-drain.json`** (new) — Resolution 3.
5. **`teamwork/.claude-plugin/plugin.json`** — version bump (re-read off `origin/main`
   immediately before bump, per G14/#445's value-race discipline) + `teamwork/README.md` ledger
   line naming #626, the calendar file, the queue section, and the schedule deviation.
6. **This LLD** (`lld-0014-estate-rhythm-instrument.md`) — doc_lint-clean.

No `object_vocab`/naming-manifest change: `calendar`, `routines`, and `held-items` are plain
ops-file names, not skill/agent/plugin names under ADR-0011's grammar.

## Interfaces

- **`calendar.md` → `idr-0011`:** cited, never restated — the IDR carries the ruled claim and its
  falsification clause; the calendar carries the living cadence values the claim covers.
- **`held-items.md`'s new section → `fleet-rules` Section 3:** the new bullet names the file as
  the landing channel; the file's own header names `fleet-rules` as the citing skill. Two-way
  cross-reference, neither restates the other's content.
- **`daily-board-drain.json` → `/mobilize-chores auto`:** the routine's prompt invokes the command
  string verbatim (`teamwork/skills/mobilize-chores/SKILL.md`'s own `auto` token contract) — the
  routine names the entry point, it does not reimplement any of `mobilize-chores`' own logic.
- **`daily-board-drain.json` → `RemoteTrigger`:** the file's shape IS the tool's own `create` body
  contract (per the `schedule` skill's documented API field reference) — arming it is a direct,
  unmodified submission, not a translation step.

## Data

Static markdown + one JSON routine definition; no runtime store, no migration, no schema beyond
what `RemoteTrigger`'s own API already defines for a routine-create body.

## Risks

- **R-1 (the named deviation itself — schedule not live-armed).** Detection:
  `calendar.md`'s own Status column names it un-armed; the ticket's dated comment and Findings
  entry both disclose it. Fallback: arm on the next session carrying `RemoteTrigger` — a single
  copy-paste of the committed JSON body, no re-authoring needed. Residual risk: the daily drain
  does not actually fire until that arm step runs — accepted, disclosed, not hidden behind
  "instrument shipped."
- **R-2 (cadence defaults are guesses, not a ruling).** Detection: every cadence in `calendar.md`
  is marked tunable inline; idr-0011's own Open questions are cited as the reason. Fallback: the
  ratification round idr-0011 names as its own next step edits this file directly — no
  supersession, no new record, per Resolution 1.
- **R-3 (`held-items.md` scope creep).** Adding an unrelated-seeming section to a narrowly-titled
  file risks confusing a future reader. Detection/fallback: the file's own top note discloses the
  split explicitly and the new section carries its own scoped template — a reader hitting either
  section gets a self-contained contract, no cross-reading required.
- **R-4 (the ops sweep row overclaims "standing").** issue-sorter's slice survives session death;
  decision-watcher/repo-cleaner/chore-planner's don't. Detection: the calendar row states this
  split explicitly ("Partially standing") rather than reporting the whole sweep as fixed —
  idr-0011's own named gap, not resolved by this build (out of scope; #626's Acceptance only
  requires the first schedule to exist, singular).

## Rejected alternatives

- **A new `ruling-queue.md` file for Kim's queue** instead of a `held-items.md` section — rejected
  per Resolution 2 (two files meaning the same thing recreates the ad-hoc-arrival problem idr-0011
  names).
- **Editing idr-0011 itself to carry the cadence table.** Rejected: idr-0011 is LOCKED
  (append-only); a cadence tweak would owe a supersession per edit, which is precisely why the
  Record-type note on idr-0011 chose IDR over ADR in the first place (cited, Resolution 1).
- **Building decision-watcher's weekly re-validation MODE in this build.** Out of scope — that
  instrument belongs to gh#623/idr-0009, named there as its own deliberately-deferred follow-up;
  this LLD only reserves the calendar slot idr-0009 asks for, it does not implement the mode.
- **A hook-based daily drain instead of a cloud `/schedule` routine.** Rejected on the same
  grounds lld-0013's Resolution 4 already ruled for artifact refresh: hooks are fully retired in
  this workspace (#466) and a hook can at best nag, never actually run an unattended multi-hour
  sweep-and-build pass.
- **Silently treating the schedule skill's successful launch as "the schedule exists.**" Rejected
  outright — the skill launching proves the PROCEDURE is reachable, not that the underlying
  `RemoteTrigger` tool is; conflating the two would misreport gh#626's own Acceptance criterion
  (Resolution 3).

## Agent verification

Per `docs:agent-harness-rules`, split as gh#626's own Acceptance states it: **payload/API layer**
— `calendar.md` exists and is well-formed markdown (doc_lint-adjacent, though it is not itself a
doc-type-frontmatter file — an ops file, checked by existing; `held-items.md`'s new section
parses under its own template); the schedule's existence is checkable via `RemoteTrigger
{action: "list"}` / `/schedule list` — **not yet green**, named as R-1 above, checkable the moment
a human runs the arm step. **Mechanical layer:** `release_gate.py teamwork` (the `fleet-rules`
body edit rides the plugin's own gate); `doc_lint.py` on this LLD. **Fresh-context checker:**
`harness:skill-checker` on the `fleet-rules` diff (semantic body edit, per
`.claude/rules/plugin-authoring.md`). **Human/final-ratification layer, stated exception:**
cadence fitness (idr-0011's own Open question 1) and the schedule's live-arm step are both
human-assert, named here rather than silently absent.
