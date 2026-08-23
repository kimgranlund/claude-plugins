# dist/ — release-gate output, read-only

**Path scope:** `**/dist/**` (any plugin's build-output directory).

`release_gate.py <plugin-root> --package` (see the workspace CLAUDE.md's Common commands) is
plugin-agnostic; artifacts land at `<plugin>/dist/<name>-<version>.plugin`. `dist/` is gate
OUTPUT: read-only. Never hand-zip a plugin package, and never hand-edit or hand-create anything
under `dist/` directly — regenerate it via the gate. Harness overlay files (`.codex-plugin/`,
`skills/*/agents/openai.yaml`, `plugin.yaml`, `__init__.py`, `hermes-mcp.yaml`, `package.json`,
`prompts/<name>.md`, `HARNESS-NOTES.md`) are the opposite case — derived but committed IN-TREE,
never `dist/`, because every verified harness install path reads a checkout directory and
`dist/` is gitignored (LLD-0025 Resolution 4); regenerate them via `harness_emit.py`, verified
fresh by G15.

Split from CLAUDE.md (issue #262, 2026-08-16).
