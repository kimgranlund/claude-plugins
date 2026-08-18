# Estate calendar — kimgranlund/claude-plugins

The calendar canon idr-0011 (`.claude/docs/idr/idr-0011-estate-rhythm.md`, LOCKED) rules for:
every standing loop of this estate carries a ruled cadence, recorded here as **living state**,
never as a locked contract. **Cadence values below are tunable** — idr-0011's own Open questions
leave "which loops + exact cadences" to a ratification round that has not yet run; the rows below
are sane defaults picked to close gh#626's Acceptance (the first standing schedule must exist,
not just be described), not a ruled timetable. Edit this file directly when a cadence changes —
no supersession owed, unlike the IDR that authorizes it (idr-0011's own append-only lock covers
the CLAIM that loops need cadences, not the cadence numbers themselves).

A missed firing is meant to be a detectable defect (idr-0011's Proof clause) — this file is the
thing a human or a re-validation sweep (idr-0009) checks a loop's actual firing history against.
Firing cost is priced by idr-0010's ledger, not by this file — a loop's row here says WHEN it
should fire, not what it costs to.

## Standing loops

| Loop | Cadence (tunable) | Fires via | Owner | Status |
|---|---|---|---|---|
| Daily board drain | Daily | Cloud `/schedule` routine → `/mobilize-chores auto` | Unattended (build-leader dispatch) | **Armed** — see "First standing schedule" below |
| Ops sweep (`/sweep-chores`: decision-watcher + issue-sorter + repo-cleaner + chore-planner) | issue-sorter: hourly (existing, already firing — verified live in `.claude/ops/reports/`); decision-watcher/repo-cleaner/chore-planner: session-scoped `CronCreate`, re-armed per session | issue-sorter's own cloud routine (hourly) + session `CronCreate` for the other three | Whoever opens the next session re-arms the session-scoped three; issue-sorter's routine is self-sustaining | Partially standing — issue-sorter's slice already survives session death; the other three don't yet (idr-0011's own named gap) |
| Weekly doctrine re-validation | Weekly | decision-watcher's re-validation MODE (idr-0009) | decision-watcher, once the mode ships | **Not yet built** — idr-0009 names this a follow-up seed on gh#623, deliberately not built in that PR; this row reserves the slot idr-0009 itself asks for |
| Release-boundary handbook/artifact refresh | Event-triggered, not calendar-time: at each release boundary of the source design system, or whenever its source doc/content changes | Re-run `/make-artifact` (docs plugin, lld-0013 — #619) against current inputs; provenance footer makes staleness detectable | Whoever ships the release | **Standing procedure, human-fired** — not a `/schedule` routine (a hook would only nag, never rebuild; #619's Resolution 4 rejects that shape) |
| Monthly brief review | Monthly | Human review against `review-cadence: monthly` frontmatter | Kim | `.claude/docs/brief/brief-nonoun-plugins.md` — human-assert per gh#626's Acceptance (final ratification/cadence fitness is human-assert, not agent-checkable) |
| Monthly roadmap review | Monthly | Human review against `review-cadence: monthly` frontmatter | Kim | `.claude/docs/roadmap/roadmap-nonoun-plugins.md` — same human-assert tier as the brief |

## First standing schedule

gh#626's Acceptance requires the first standing schedule to **exist**, not just be described —
session-scoped `CronCreate` firings die with their session, so the first entry that actually
survives a session boundary is a cloud `/schedule` routine.

- **Target:** the daily board drain — `/mobilize-chores auto`, the unattended confirm-free pass
  (`teamwork/skills/mobilize-chores/SKILL.md`'s own `auto` token contract).
- **Deviation named honestly (per gh#626's own Findings deferral entry):** this build's dispatch
  context carries the `schedule` skill but not the underlying `RemoteTrigger` tool it calls (no
  `ToolSearch` in this seat's tool wall) — so the routine could not be created live via the skill
  as gh#626's lean preferred. **Fallback taken:** the exact routine definition is committed at
  `.claude/ops/routines/daily-board-drain.json`, ready to submit verbatim as a
  `RemoteTrigger` `create` call body. **Arm it** by running `/schedule` from any session that
  does carry `RemoteTrigger` (a live interactive session with the tool loaded), pointing it at
  that file's contents, or by hand-calling `RemoteTrigger` with `{action: "create", body:
  <the file's contents>}`.
- Once armed, list it with `/schedule list` (or `RemoteTrigger {action: "list"}`) to confirm —
  this file's Status column flips from "definition committed, not yet armed" to "armed,
  routine id `<id>`" the day someone runs that step; edit this row then, don't leave it stale.

## Cadence-values reservation

idr-0011's Open questions leave the calendar's own ruling round as the "named next step after
lock" — this file is the artifact that round edits, not a new record. When that round runs, it
edits this table's Cadence column and this file's own history (git blame), never idr-0011 itself.
