# Bundled scripts — selftest requirement

**Path scope:** `**/scripts/*.py`, `**/scripts/*.mjs`, `**/scripts/*.js` (every plugin's bundled
scripts).

Every `scripts/*.py|mjs|js` in every plugin carries a `selftest` mode and it stays green
(anatomy, exit tri-state, and placement: harness's `script-writing-rules`; the release gate's G4
check sweeps all three extensions).

Split from CLAUDE.md (issue #262, 2026-08-16).
