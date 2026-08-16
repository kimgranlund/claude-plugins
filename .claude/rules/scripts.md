# Bundled scripts — selftest requirement

**Path scope:** `**/scripts/*.py`, `**/scripts/*.mjs`, `**/scripts/*.js` (every plugin's bundled
scripts).

Every `scripts/*.py|mjs|js` in every plugin carries a `selftest` mode and it stays green
(anatomy, exit tri-state, and placement: harness's `script-writing-rules`; the release gate's G4
check sweeps all three extensions).

Moved from the workspace CLAUDE.md's "Incident → infrastructure, same day" invariant (issue #262,
2026-08-16) — the general doctrine sentence stayed in CLAUDE.md as always-relevant core; this
file carries only the scripts-specific mechanics.
