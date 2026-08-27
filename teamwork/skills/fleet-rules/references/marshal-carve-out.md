# Marshal carve-out on the live lane (Kim's ruling, 2026-08-27)

F6 split from `SKILL.md` §7 to keep the body under the 500-line budget. Cited from `SKILL.md`
§7, `agents/fleet-marshal.md`, `skills/bind-team/SKILL.md`, and the workspace `CLAUDE.md`'s
"Live lane first" row — read this file once for the full rule, never restated inline.

Root cause (issue #949): the live lane's text names "a LIVE human prompt" / "the host" as the
executor, with no carve-out for a host that is ALSO the fleet's router. A `/bind-team`-held
marshal (or the dispatched `agents/fleet-marshal.md`) read that as license to execute multi-file
build work inline, blocking the fleet's flow for the duration. The lane's size tripwires (>3
substantive files, a second plugin) only fire post-hoc, at merge time — nothing sized the ask
from its shape before execution started.

## The rule

A session holding this seat — via `/bind-team` (door 1) or the dispatched
`agents/fleet-marshal.md` (door 3) — never executes the live lane's work itself. It keeps
ONE-FILE MECHANICAL latitude only (a version renumber, a ledger line, a one-line stale citation)
inline; anything semantic or touching more than one file is a named `build-<slug>` build-leader
dispatch (`Agent` tool, model from `fleet.json` seats), with the live prompt passed in as the
dispatch's own authorization (skip intake mint/claim/write-gate per the lane) — the marshal stays
free to keep routing, gating, and merging within the same turn.

**Up-front sizing, marshal-only.** Before any inline action, read the ask's shape — naming a new
skill/agent/plugin, or "plan + checklist + evals" (or any make-* forge), trips the multi-file
tripwire AT DISPATCH TIME, never waiting on the post-hoc file count in §7's Tripwires paragraph.
A non-marshal live session (the solo live lane, no `bind-team` held) is unaffected — it keeps
today's post-hoc merge-time tripwire exactly as written.

## Kim's two rulings (posted on #949, the owed clarifying questions)

1. **Latitude.** A bind-team marshal keeps ONE-FILE MECHANICAL latitude only (a version renumber,
   a ledger line, a one-line stale citation). Anything semantic or multi-file is a named
   build-seat dispatch.
2. **Sizing scope.** The up-front sizing read (ask names a new skill/agent/plugin, or "plan +
   checklist + evals" → multi-file tripwire fires at dispatch time) applies to the MARSHAL ONLY.
   Non-marshal live sessions keep today's post-hoc merge-time tripwire.
