# leading-builds — behavioral assertions (Phase 2)

Checked with/without in Phase 5. "The session" = a session that ran /leading-builds.

1. **Adoption acknowledgment:** immediately after /leading-builds, the session's reply names the
   adopted contract file, the three host deltas, and the duration rule — before any target is
   processed.
2. **Record-first + state check:** a ticket id given to the session runs dispatch-ticket's
   Phase 1 as written — a closed ticket is reported closed and STOPPED on (reopening is the
   user's call), never silently picked up; an open one has its kind/size read before any build
   effort.
3. **Interactive branches alive:** an ambiguous target (two plausible records, or a vague
   task-kind brief) gets the ONE live question dispatch-ticket's interactive branch defines —
   not the agent path's blocker/SKIPPED.
4. **Record-first on raw asks:** a raw non-ticket ask ("trim the READMEs when you get a
   chance") is routed through intake first (dispatch-ticket Phase 1's no-match branch → the
   file-* intake, or the named redirect for non-feature shapes) — never built without a record
   existing first.
