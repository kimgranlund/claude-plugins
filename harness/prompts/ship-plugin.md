---
description: "Release a Claude Code plugin through the full gate: preflight (version bump, changelog), release_gate.py (structure, manifest, full lint, bundled selftests, phantom sweep), evals check, package to dist/. Run /ship-plugin [plugin-root, default .]. Human-timed; edits the manifest on approval and writes the .plugin artifact."
argument-hint: "[plugin-root]"
---

# ship-plugin

ship-plugin ships a plugin only through the gate — the ritual that, run by memory, skips exactly the step that ships the incident. Root: `$ARGUMENTS` (default `.`).

Invoke `plugin-writing-rules` now — the gate order and every rule below are its §Release discipline; not restated here.

## Phase 1 — Preflight

1. Read `.claude-plugin/plugin.json`; read the README footer's version ledger. State the delta being shipped in one sentence (from conversation, git log, or by asking — one question).
2. Docs freshness is scripted — the gate's G10 (`docs_check.py`) fails an undocumented skill or a ledger/manifest version mismatch; what it cannot check is whether the *descriptions* are still true, so re-read the README rows touched by this delta before proposing the bump.
3. Propose the bump (patch = fixes; minor = new skills/rules; major = breaking renames or contract changes) and the footer ledger line. **Apply both only on the user's approval** — the manifest is the release; editing it is the side effect this command exists to time.
4. Evals check: now scripted — the gate's G7 validates every suite via `eval_check.py` and warns per coverage gap (new skills forged via `/make-skill` carry theirs from Phase 2). Deep routing validation is `/check-routing`, recommended before a minor/major bump, not enforced here.
5. Once the manifest/version bump above lands, regenerate this plugin's harness overlays:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_emit.py" <root>` — writes `.codex-plugin/`, per-skill `agents/openai.yaml`, `plugin.yaml`, `__init__.py`, `hermes-mcp.yaml` (where `.mcp.json` exists), `package.json`, `prompts/<name>.md` (one per command-only skill), and `HARNESS-NOTES.md` in-tree (LLD-0025, all three harnesses as of W3/#891). Skip this step only if step 3's bump was declined; any other edit to `plugin.json` or a skill's frontmatter needs it too, since Phase 2's G15 fails a stale or hand-edited overlay against whatever's on disk.

## Phase 2 — The gate

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" <root>` — structure, manifest, full lint over every SKILL.md / agent / hooks.json / plugin.json, bundled-script selftests, phantom sweep. Findings are fixed and the gate re-run; the same finding failing 3 times → stop and hand it to the user (`teamwork`'s `loop-rules` names this exact gate as a goal condition, where installed). The gate's own counters are proven by `release_gate.py selftest` — run it first if the gate itself was edited this cycle.

## Phase 3 — Package

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" <root> --package` → `dist/<name>-<version>.plugin`. The gate refuses a same-version artifact (the version is the update cache key; a same-version ship is a release nobody receives) — that refusal routes back to Phase 1, never to deleting the old artifact.

## Phase 4 — Report

The `Cross-harness` line's `<d>` is Phase 2's own G15b WARN count (`0` when it stayed `ok`) —
a count of skills whose bodies carry a Claude-only token
(`${CLAUDE_PLUGIN_ROOT}`, `$ARGUMENTS`), each one already named in `HARNESS-NOTES.md`'s own
degradation-inventory section (issue #1008). "Behavioral verification: none (structural only)"
is a fixed, honest caveat, not a variable to fill in — G15/G15b prove the overlay FILES are
fresh and every token degradation is recorded; neither one loads a skill inside a real Codex,
Hermes, or Pi session (that's `--probe`'s job, run separately, never folded into this report).

```
ship-plugin · <name> <old> → <new>
Gate: clean (<n> files linted, <m> selftests green) · Evals: <present/missing per skill>
Cross-harness: overlays fresh (codex,hermes,pi) · degradations: <d> (HARNESS-NOTES.md) · behavioral verification: none (structural only)
Artifact: dist/<name>-<version>.plugin
Delta: <the one-sentence delta>
Reminders: consumers run /reload-plugins; SKILL.md edits hot-reload, nothing else does.
```

Failure branches: gate unfixably red → no artifact, the report says why; user declines the bump → stop cleanly, nothing edited. Done when the artifact exists at the versioned path, the manifest and footer carry the new version, and the report is delivered. NOT done if any step was vouched for instead of run — the ritual exists because vouching is how the last three incidents shipped.
