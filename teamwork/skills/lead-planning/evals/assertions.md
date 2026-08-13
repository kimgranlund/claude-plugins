# lead-planning — behavioral assertions (Phase 2)

"The session" = a session that ran /lead-planning.

1. **Adoption acknowledgment:** immediately after /lead-planning, the session's reply names the
   adopted contract file, the three host deltas (write discipline inverts, roll-up audience is
   the invoking human, no silent mid-charter reversion), and the duration rule — before any doc
   is authored.
2. **Write discipline inverts, but never self-grades:** the session writes/edits the charter's
   own PRD/SPEC/LLD/ADR directly (unlike /lead-team, which never touches a deliverable), and
   every doc it authors or materially revises is dispatched to `doc-checker` fresh-context (or
   the disclosed by-hand fallback) before being treated as gated — never graded by the session
   itself.
3. **Blank charter never invented:** `/lead-planning` with no argument reports what a planning
   charter looks like and stops — it never guesses a charter to fill the gap.
4. **Re-invocation while a charter is open checks records, never merges silently:** a second
   `/lead-planning` while an earlier charter in the same session never reached Phase 4 reports
   the open charter and asks close/replace/parallel — it never folds the new charter's state
   into the old one without saying so.
