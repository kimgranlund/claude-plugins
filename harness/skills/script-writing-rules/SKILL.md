---
name: script-writing-rules
description: >-
  Standards for bundled scripts — code instead of prose, shipped as scripts/taskname.py|mjs
  with a selftest that proves it. Covers structure, skill- vs plugin-level scripts/, python vs
  js, negative controls, the exit-code contract (0/1/2), and whether something is
  mechanizable. NOT for the authoring workflow (make-script); NOT for hooks.json
  (hook-writing-rules); NOT for the calling SKILL.md (skill-writing-rules).
disable-model-invocation: false
user-invocable: false
---

# Script Authoring Standards

If it can be mechanized, mechanize it as `scripts/taskname.py|mjs` — a prose checklist re-judged
by eye every run is a hallucination surface; a script is the same judgment made once, then proved
forever by its selftest. This is the standard `make-script` authors against, the audits' A4
Mechanization dimension scores against, and `release_gate.py` G4 enforces the checkable slice of.

## The mechanization test — can vs. should

Mechanize when you can write the pass/fail function: counts, pointer/count integrity, schema
conformance, threshold comparisons, table lookups, deterministic derivations ("arithmetic, not
judgment"). Keep judgment in prose only where the checker can never see the property — and state
that boundary explicitly in the owning skill ("accuracy stays human", "the proxy is
lexical-overlap only, so the scorer judges real ambiguity"). Two disqualifiers:

- **A checker already owns it.** The check tier composes — `release_gate` runs `skill_lint`, it
  does not restate it. A second linter for an existing check is drift with a countdown.
- **The property is judgment wearing a costume.** A script that scores "clarity" or "quality" by
  keyword count mechanizes the *look* of the judgment, not the judgment; it will be trusted and
  wrong. Mechanize the countable substrate, keep the verdict human.

## Anatomy (the contract every script ships with)

- **Invocation**: `script.py <target> [flags]` positional-first; no args → print `__doc__`, exit 2.
  The docstring is the manual: usage lines, what each check asserts, exit meanings.
- **Exit codes**: `0` clean · `1` findings/failure · `2` usage error, or — in selftest mode —
  SKIP (see tri-state below). Machine-readable verdict line first (NORMATIVE shape:
  `name · verdict · N fail / M warn`), findings as `file:line` where the target admits them.
- **`selftest` mode, mandatory**: `script.py selftest` proves the counters on bundled or inline
  fixtures and exits 0. A selftest that only feeds a good input proves nothing — it needs a
  **negative control that bites** (a wrong input the check must catch) and a **reverse control**
  (a right input it must not flag). Shapes in `references/selftest-patterns.md`.
- **Tri-state skip**: a selftest whose runtime dependency is absent here (a browser, a heavyweight
  package) exits **2** with a one-line reason and the install hint — never 0 (a broken
  environment must not look green) and never 1 (absence is not failure). Ratified 2026-07-14 from
  `ui-probe.mjs`, which pioneered it.
- **Dependencies**: python scripts are stdlib-only — every script in this workspace runs on a bare
  `python3`. Node scripts prefer zero-dependency; an unavoidable dependency resolves from the
  *target repo's* node_modules and triggers the tri-state skip when absent.
- **Determinism**: no network calls in a check; no unseeded randomness; selftest completes well
  under G4's 120s subprocess timeout.

## Placement and pathing

- **Skill-level `scripts/`** when one skill owns the check — invoked as
  `${CLAUDE_SKILL_DIR}/scripts/taskname.py`.
- **Plugin-level `scripts/`** when it is shared across skills or composed by the gate
  (`skill_lint`, `eval_check`) — invoked as `${CLAUDE_PLUGIN_ROOT}/scripts/taskname.py`.
- Path portability and the hard plugin boundary are owned elsewhere (`skill-writing-rules`'
  pathing rule; the workspace's `surface_map.py check` invariant) — they apply to scripts as to
  any bundled asset, unrestated here. `taskname` is a verb-bearing task name (illustrative:
  `coverage_check`, `ramp_build`, `contrast-check`); snake_case is the majority form, kebab-case
  legal — match the owning plugin's local grammar.
- Every script is named in its owner's prose: an orphan script no SKILL.md invokes is dead
  automation the docs gate should question.

## Enforcement (verified July 2026) [drift-prone: mirrors release_gate.py's G4 — an edit there owes this section]

`release_gate.py` **G4** sweeps `scripts/*.py|*.mjs|*.js` (excluding `dist/`), runs `selftest` on
every file containing the word — py via the gate's interpreter, js via `node` (node absent → the
js scripts WARN as unproven). Exit 0 passes, exit 2 is disclosed as a dependency-skip in the ok
line, anything else fails the gate: a shipped script proves its counters or does not ship. A
script *without* a selftest mode is silently skipped by G4 — which is why the selftest is a
standard, not merely a gate: the gate cannot demand what it cannot see. The workspace's same-day
incident→fixture rule applies (worked through in `references/selftest-patterns.md` §Incident →
fixture).

**Style tier (G11, ADR-0002, 2026-07-15):** where the workspace root carries `ruff.toml` /
`eslint.config.mjs`, the gate also style-lints — ruff over `.py`, eslint over `.mjs|.js` — for the
defect classes selftests can't see (unused imports/variables, ambiguous/undefined names, dead
code). Run-if-reachable, WARN-if-absent locally; CI enforces. Two ruff rules are configured out as
deliberate house idiom (E702 compact semicolon one-liners, E731 lambda helpers) — a new exclusion
needs the same argued-in-config treatment, never an inline `# noqa` scattered per site.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Prose checklist re-run by eye | Judgment re-made every run, drifts silently | Mechanize; the prose becomes one pointer line |
| Selftest with no negative control | Proves the happy path only; a dead check stays green | Inversion fixture that must bite (`references/selftest-patterns.md`) |
| Exit 0 on missing dependency | Broken environment looks green | Tri-state: exit 2 + reason + install hint |
| Second linter for an existing check | Two canons, one will lie | Compose the existing checker; delete the twin |
| Mechanized judgment | Keyword-counting "quality" trusted as a verdict | Mechanize the countable substrate; verdict stays human, stated explicitly |
| Orphan script | No SKILL.md invokes it; rots unexercised | Name it in the owner's prose or delete it |
| pip/npm dependency in a check | Fails on every machine but the author's | stdlib-only (py); target-repo resolution + skip (js) |
