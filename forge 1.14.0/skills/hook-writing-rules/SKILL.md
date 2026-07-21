---
name: hook-writing-rules
description: >-
  Standards for writing Claude Code hooks — the enforced, zero-token tier. Use when the user asks
  how to write, structure, review, or fix a hook or hooks.json; which lifecycle event or matcher
  to use; how exit codes and JSON decisions work; why a hook fires never, twice, or silently fails
  to register; whether a rule belongs in a hook or a skill; how a hook's message should read.
  Carries verified event and output semantics (July 2026).
disable-model-invocation: false
user-invocable: false
---

# Hook Authoring Standards

A hook is the harness enforcing what prose can only suggest: it runs outside the model's context, cannot be overridden, and costs zero tokens unless it deliberately injects output. Ecosystem measurement puts hook compliance at ~100% against 70–90% for entry-file instructions — that gap is the entire reason this tier exists. This is the standard `/make-hook` authors against and `/check-everything` scores against; `skill_lint.py` (rules H1–H5) enforces the checkable slice of `hooks.json`.

## The routing test — the one decision that matters

A rule expressible as a program returning pass/fail is a **check** → hook. A rule requiring a model to weigh it is **judgment** → skill. Both misroutes are toxic: checks in prose are probabilistic, token-costly, and drift; judgment in a hook is wrong often and unoverridable always — the worst combination. Write the pass/fail function or admit there isn't one.

```
Check    (hook):  "every SKILL.md declares both invocation dials"        → skill_lint F2
Judgment (skill): "does this body carry a genuine behavior delta?"       → check-skill R1
```

## Mechanics — verified 2026-07 [drift-prone]

- **Events:** `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`, and more; matchers scope firing (`Write|Edit`, `Bash`, `^mcp__` regexes for MCP tools).
- **Handler types:** `command` (the production default), `prompt`, `http`, `mcp_tool`, `agent` — deterministic checks take `command`; a prompt-type hook is judgment wearing a hook's config and gets the routing test applied to it.
- **Input:** the event arrives as JSON on stdin — `hook_event_name`, `tool_name`, `tool_input` (`.file_path` for file tools, `.command` for Bash), `session_id`, `cwd`.
- **Output:** exit 0 = success, silent; exit 2 = block, stderr fed to Claude; or structured stdout JSON — `{"decision": "block", "reason": …}` (PostToolUse/Stop) and `hookSpecificOutput.permissionDecision: allow|deny|ask` (PreToolUse). Unmatched files and malformed events exit 0 quietly.
- **Layering:** hooks from enterprise, project, user, local, and plugin scopes merge additively — everything that matches runs; nothing overrides. Workspace trust gates all of it.
- **Plugin registration:** plugin `hooks/hooks.json` requires the outer `"hooks"` wrapper — a bare settings-style snippet fails *silently* (lint H2). Paths go through `${CLAUDE_PLUGIN_ROOT}`; persistent state goes to `${CLAUDE_PLUGIN_DATA}`, because updates wipe the plugin root. Hook config changes need `/reload-plugins`; SKILL.md live-reloads, hooks do not.

## Hook discipline

Fast, deterministic, **quiet on success**. A slow hook taxes every loop iteration; a flaky one is worse than none — intermittent false failures train the model to discount hook feedback generally, corroding the repair loop hooks exist to power. Consequences:

1. Every hook script ships a `selftest` mode proving its counters on embedded fixtures (`skill_lint.py`, `potency_lint.py`, `coverage_check.py` are the house pattern) — an untested hook is a flake in waiting.
2. The script filters its own scope first (wrong file class → exit 0, no output) so one registration can watch broad matchers cheaply.
3. Timeouts declared; long work forked async; state written only to `${CLAUDE_PLUGIN_DATA}` or the repo.

## The message is the loop's best real estate

A hook's output lands adjacent to the model's next action — the highest-recency, highest-potency position in the whole system (`prompt-wording-rules` §9). Most teams spend it on `exit 1`. Spend it as a **repair affordance**: the hook's name (handle), `file:line` evidence, each fix stated affirmatively, and a named branch for disagreement.

```
Bad  (compiler noise):      ✗ lint failed (exit 2)
Good (repair affordance):   skill-postwrite-invocation-lint · 2 fail · path
                              L4  missing `user-invocable` -> declare it explicitly
                            If a finding seems wrong -> report it against the standard; do not suppress it.
```

## Naming

`<domain>-<event>-<check>` with compact event tokens: `ui-postedit-lint`, `skill-postwrite-invocation-lint`, `env-preread-guard`. The name appears alone in logs and failure output — domain groups it, the event answers *when*, the check answers *what just blocked me*. Hooks fire; they are never "used" — a hook name that reads as a wieldable tool wanted to be a skill.

## The three load-bearing patterns

1. **Repair loop** — `PostToolUse` on hot paths runs the check and feeds concrete failures back; editing becomes self-correcting with zero prompt engineering.
2. **Guard** — `PreToolUse` blocks writes to protected paths, dangerous verbs, credential reads (`.env`); the one defense that survives every permission mode.
3. **Automation trigger** — a lifecycle event fires a workflow entry point, converting "remember to X" into "X happens".

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Judgment in a hook | Wrong often, unoverridable always | Route to a skill; hooks keep the pass/fail residue |
| Missing outer `"hooks"` wrapper | Plugin hook silently never registers | Wrap it; lint H2 blocks the class |
| Hardcoded home paths | Works on one machine | `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}`; lint H5 |
| Noisy success | Output on every pass numbs the signal | Silent exit 0; speak only to repair |
| Flaky check | False failures corrode trust in the whole tier | Deterministic script + shipped selftest |
| Blocking mid-flow on style | Constant interruption degrades the agent's work | Block on invariants; warn-and-continue on style; consider gate-at-commit |
| Prose duplicate of a hook | Drift pair; the prose version rots | The hook is canonical; delete the prose, keep a pointer |
| Config edited, nothing changes | Plugin hooks aren't live-reloaded | `/reload-plugins` or restart |

## Provenance

Event set, output semantics, layering, and the wrapper trap verified against code.claude.com/docs (hooks, plugins-reference) and this plugin's own build incidents, 2026-07. All mechanics [drift-prone]: re-verify on a version bump. Message language: `prompt-wording-rules` (§5, §9, §10). Routing: `skill-writing-rules` carries the skill side of the boundary.
