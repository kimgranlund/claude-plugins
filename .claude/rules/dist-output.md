# dist/ — release-gate output, read-only

**Path scope:** `**/dist/**` (any plugin's build-output directory).

`release_gate.py <plugin-root> --package` (see the workspace CLAUDE.md's Common commands) is
plugin-agnostic; artifacts land at `<plugin>/dist/<name>-<version>.plugin`. `dist/` is gate
OUTPUT: read-only. Never hand-zip a plugin package, and never hand-edit or hand-create anything
under `dist/` directly — regenerate it via the gate.

Moved from the workspace CLAUDE.md's "Ship only through the gate" invariant (issue #262,
2026-08-16) — the version-bump/README-ledger discipline stayed in CLAUDE.md as always-relevant
core; this file carries only the part that's true specifically inside `dist/`.
