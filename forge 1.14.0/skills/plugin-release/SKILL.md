---
name: plugin-release
description: >-
  Release a Claude Code plugin through the full gate: preflight (version bump, changelog),
  release_gate.py (structure, manifest, full lint, bundled selftests, phantom sweep), evals check,
  package to dist/. Run /plugin-release [plugin-root, default .]. Human-timed; edits the manifest
  on approval and writes the .plugin artifact.
disable-model-invocation: true
user-invocable: true
argument-hint: "[plugin-root]"
---

# plugin-release

plugin-release ships a plugin only through the gate — the ritual that, run by memory, skips exactly the step that ships the incident. Root: `$ARGUMENTS` (default `.`).

Invoke `plugin-authoring-standards` now — the gate order and every rule below are its §Release discipline; not restated here.

## Phase 1 — Preflight

1. Read `.claude-plugin/plugin.json`; read the README footer's version ledger. State the delta being shipped in one sentence (from conversation, git log, or by asking — one question).
2. Docs freshness is scripted — the gate's G10 (`docs_check.py`) fails an undocumented skill or a ledger/manifest version mismatch; what it cannot check is whether the *descriptions* are still true, so re-read the README rows touched by this delta before proposing the bump.
3. Propose the bump (patch = fixes; minor = new skills/rules; major = breaking renames or contract changes) and the footer ledger line. **Apply both only on the user's approval** — the manifest is the release; editing it is the side effect this command exists to time.
4. Evals check: now scripted — the gate's G7 validates every suite via `eval_check.py` and warns per coverage gap (new skills forged via `/skill-forge` carry theirs from Phase 2). Deep routing validation is `/eval-run`, recommended before a minor/major bump, not enforced here.

## Phase 2 — The gate

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" <root>` — structure, manifest, full lint over every SKILL.md / agent / hooks.json / plugin.json, bundled-script selftests, phantom sweep. Findings are fixed and the gate re-run; the same finding failing 3 times → stop and hand it to the user (`orchestration`'s `loop-design` names this exact gate as a goal condition, where installed). The gate's own counters are proven by `release_gate.py selftest` — run it first if the gate itself was edited this cycle.

## Phase 3 — Package

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" <root> --package` → `dist/<name>-<version>.plugin`. The gate refuses a same-version artifact (the version is the update cache key; a same-version ship is a release nobody receives) — that refusal routes back to Phase 1, never to deleting the old artifact.

## Phase 4 — Report

```
plugin-release · <name> <old> → <new>
Gate: clean (<n> files linted, <m> selftests green) · Evals: <present/missing per skill>
Artifact: dist/<name>-<version>.plugin
Delta: <the one-sentence delta>
Reminders: consumers run /reload-plugins; SKILL.md edits hot-reload, nothing else does.
```

Failure branches: gate unfixably red → no artifact, the report says why; user declines the bump → stop cleanly, nothing edited. Done when the artifact exists at the versioned path, the manifest and footer carry the new version, and the report is delivered. NOT done if any step was vouched for instead of run — the ritual exists because vouching is how the last three incidents shipped.
