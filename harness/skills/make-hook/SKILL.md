---
name: make-hook
description: >-
  Forge a Claude Code hook through five gated phases: check-vs-judgment route, event/matcher
  interview, script + registration draft, repair-message language pass, simulated-event
  validation with a shipped selftest. Run /make-hook [hook-name or the rule to enforce].
  Human-timed; writes files. NOT for skills (make-skill) or agents (make-agent).
disable-model-invocation: true
user-invocable: true
argument-hint: "[hook-name or the rule to enforce]"
---

# make-hook

make-hook turns a rule into an enforced hook through five gated phases; a failed gate stops the forge. Seed: `$ARGUMENTS`

Invoke `hook-writing-rules` now — it governs every phase and is not restated here.

## Phase 0 — Route: is this a check?

Write the pass/fail function in one sentence: "given <event input>, fail when <condition>". Can't be written without a model weighing it → it's judgment → route to `/make-skill` (or a criterion in an existing standards skill) and stop. Partially checkable → split: the mechanical slice forges here, the judgment residue routes out, and the two reference each other.

**Gate H0:** the pass/fail sentence recorded, plus the event input it reads.

## Phase 1 — Interview

One question per turn; record lands as `<name>.intent.md` beside the script. Slots:

- **Event + matcher** — which lifecycle moment, scoped how (`Write|Edit`, `Bash`, `^mcp__` for MCP tools). The narrowest matcher that still catches the class.
- **Consequence** — block (exit 2 / `decision: block`) or warn-and-continue? Blocking is for invariants; style feedback that interrupts mid-flow degrades the work — consider gating at the commit/stop boundary instead.
- **Repair message** — what the model needs to fix it: evidence shape (`file:line`), the affirmative fix per finding class, the disagreement branch.
- **Scope filter** — which inputs the script exits 0 on silently, so the matcher can stay broad and cheap.
- **Home** — plugin `hooks/hooks.json` (shipped, wrapped, `${CLAUDE_PLUGIN_ROOT}` paths) or project/user settings. Name it now; the registration snippet differs.

Name check: `<domain>-<event>-<check>` — the name must answer *what blocked me* when it appears alone in a log.

**Gate H1:** every slot filled; the repair message drafted verbatim.

## Phase 2 — Draft

Two artifacts, one skeleton each:

**Script** (any language; python3/stdlib is the house default): reads stdin JSON → scope-filters (wrong class → exit 0, silent) → runs the check → clean: exit 0, silent → findings: emit the repair affordance and the consequence chosen in H1. Ships a `selftest` mode with one passing and one failing embedded fixture — no selftest, no hook. CLI mode (`script <path>`) included so humans and `/check-everything` can run it outside the event.

**Registration**:

```json
{
  "hooks": {
    "<Event>": [
      { "matcher": "<matcher>",
        "hooks": [ { "type": "command",
                     "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/<name>.py\" --hook",
                     "timeout": 20, "statusMessage": "<name>" } ] }
    ]
  }
}
```

Settings-scope homes drop nothing but the wrapper stays mandatory for plugins — the bare snippet registers *silently never* (lint H2).

**Gate H2:** script + registration exist; selftest passes; `skill_lint.py <hooks.json>` H-rules clean.

## Phase 3 — Language pass

Invoke `prompt-wording-rules` on the repair message only — it is the hook's entire prompt surface, injected at the highest-recency position in the loop. Handle first, `file:line` evidence, affirmative fixes, one named disagreement branch; zero output on success.

**Gate H3:** the message instantiates the repair; success is silent.

## Phase 4 — Validate

1. **Simulated events**, three minimum, piped as stdin JSON: a failing input (consequence fires, message renders exactly as drafted), a passing input (exit 0, zero bytes of output), an out-of-scope input (exit 0, silent). Malformed JSON is a fourth: the script stays quiet — a flaky hook is worse than none.
2. **Live registration check:** install to the chosen home, `/reload-plugins` (plugin) or restart, trip the hook once for real. Firing observed → pass. Silent → the wrapper, the matcher, or workspace trust; check in that order.
3. **Prose sweep:** if the rule this hook enforces also lives as prose in CLAUDE.md or a skill, the hook is now canonical — delete the prose, leave a one-line pointer. A check enforced twice drifts twice.

**Gate H4:** all simulated events green · live fire observed · no prose duplicate remains.

Done when H0–H4 read PASS in the intent record and script + registration + selftest are on disk. Close with the operational note: hook config is not live-reloaded — every future edit to the registration needs `/reload-plugins`.
