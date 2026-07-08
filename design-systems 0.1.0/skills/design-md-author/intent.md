# intent.md — design-md-author

Forged via skill-forge (adapted run inside Claude Design: no skill_lint.py, no skill-auditor agent, no fresh-session runner — replaced by manual audit + in-context validation, noted at P5).

## Record
- **Trigger (verbatim):** "based on {corpus of design files, css, descriptions, etc} create a design system for use in claude design and claude code"
- **Behavior delta:** Untrained Claude produces a decent DESIGN.md from prior art but lacks ground-truth knowledge of the format; it does not know how open-ended the file can be, and does not treat the file as a SKILL (a prompt with knowledge, rules, and procedures) — it writes documentation instead.
- **Species + dials:** procedure/workflow skill; `user-invocable: true`, `disable-model-invocation: true` (command).
- **Freedom:** medium — phases are gated, but section inventory and brand judgment are open.
- **Type:** writes files (DESIGN.md + preview cards).
- **Fences:** NOT for format Q&A without a writing run (design-md-format); NOT for consuming/applying an existing design system; never steers toward a UI framework (React/Svelte/etc.); never enforces accessibility standards — measures and discloses only.
- **Done-when:** (1) enough Root Brand Architecture captured for generation — values, voice, visual territories, cultural references; (2) comprehensive tactical system for colors, geometry, typography.
- **Audience:** public distribution — assume no context.

## Gates
- P0 route: PASS — on-demand multi-step procedure → skill. 2026-07-08
- P1 interview: PASS — slots filled via user form; scope ruling: DESIGN.md = the spec file Claude Design consumes; Ultimate Tokens is the reference dialect; openness is normative. 2026-07-08
- P2 evals: PASS-with-note — user-only skill → trigger evals skipped (recorded); 4 behavioral assertions in evals/assertions.md; baseline = user-attested failure mode (fresh-session baseline runs deferred to Claude Code /eval-run). 2026-07-08
- P3 draft: PASS — description front-loads verbatim trigger + fences; body < 500 lines; dials explicit. 2026-07-08
- P4 language: PASS — manual instantiation pass; ≤3 hard gates; numeric anchors; one good/bad pair. 2026-07-08
- P5 validate: PASS-with-note — no lint script in this environment (accepted); manual audit clean; fence closure: reciprocal no-trigger eval added to design-md-format/evals/evals.json. 2026-07-08
