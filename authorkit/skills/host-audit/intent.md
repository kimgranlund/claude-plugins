# intent — host-audit

Forged 2026-08-20 from the agent-ui load-108 incident (2026-08-19/20): a live investigation on
Kim's M4 MacBook Air found load 108–180 while agent fleets ran, root-caused to FIVE compounding,
individually non-obvious causes — macOS Spotlight (mds_stores 127% + corespotlightd + mds)
indexing per-lane `npm install` churn in `.claude/worktrees`; Time Machine including ~/Projects;
7 concurrent gate-running lanes on 10 cores; vitest spawning workers-per-core × N lanes; and 14
finished worktrees parked for hours, each a full re-indexed tree. Ten test suites red IDENTICALLY
on a clean main (hook timeouts) — pure contention masquerading as regression.

## Slots
- **Trigger (verbatim, Kim):** "how can users and devs run this locally to figure out how to
  improve performance" · "why is my machine slow" · "load average is huge" · "my laptop is on
  fire while agents run" · "audit my host/machine" · "everything times out when I run parallel
  agents".
- **Behavior delta:** without the skill, the model answers "why is my dev machine slow" with
  generic advice (Activity Monitor, close apps, restart) and misses every cause the incident
  actually had — the Spotlight/worktree interaction, `.metadata_never_index`, `tmutil
  isexcluded`, the N×cores test-worker explosion, parked worktrees. Baselines in
  `evals/baseline/` demonstrate the miss.
- **Species + dials:** procedural · `user-invocable: true` · `disable-model-invocation: false`
  (the model routes symptom phrasings to it).
- **Freedom:** LOW for measurement — one bundled read-only probe script, exact, exit-coded,
  selftested (`scripts/host_probe.mjs`); HIGH for the judgment layer turning probe JSON into the
  ranked report.
- **Type:** capability uplift (the probe set + remedy catalog are non-obvious; proven by the
  incident and the baselines).
- **Fences:** NOT for judging whether a specific red TEST RUN is trustworthy (the host repo's
  own flaky-gates skill, where present — this skill diagnoses the HOST, not the verdict); NOT
  for token/cost spend (spend-audit); NOT for repo layout hygiene (repo-audit). Report-only:
  the skill NEVER executes a remedy — every action is the user's, each carrying a warning tier.
- **Done-when:** a report exists in which every finding carries the measured number, the
  mechanism, THE fix command, a severity, and a warning tier (safe / needs-sudo /
  changes-system-behavior) — and zero system mutations were performed by the audit itself.
- **Platform ruling (Kim):** macOS-first; non-macOS branches named as unverified gaps, never
  guessed. Name ruling: `host-audit`. Report ruling: checklist + evidence + warnings.

## Gates
- P0 PASS 2026-08-20 — primitive = skill (on-demand procedure; mechanical slice = bundled
  script, not a hook — no tool-event to gate; no tool walls — not an agent).
- P1 PASS 2026-08-20 — slots above; Kim confirmed name/platform/probe-tier/report-depth in one
  batched round.
- P2 PASS 2026-08-20 — evals.json (12 trigger + 8 fenced no-trigger), 5 assertions, 2 baselines saved with the contamination caveat recorded honestly (fresh agents inherited project memory; still missed the probe/report contract).
- P3 PASS 2026-08-20 — SKILL.md (98 lines, dials explicit) + scripts/host_probe.mjs (selftested, negative control) + references/remedies.md (F1–F9, incident-grounded).
- P4 PASS 2026-08-20 — potency lint within budget (prohibitions 6→4 via affirmative reframes), description trimmed 835→~640 (W8), instantiation pass: contract head, good/bad pair, numeric anchors, one NEVER gate.
- P5 PASS 2026-08-20 — skill_lint clean; skill-checker verdict SHIP (4 minors applied: dead Bash grant dropped, drift pair de-enumerated, selftest paths quoted; disallowed-tools deliberately NOT added per the checker's own layering argument); behavior check ran live on the incident host (caught + fixed the Chrome-Helper miscount); fences reciprocated in spend-audit + repo-audit evals (flaky-gates lives in another estate — description names it conditionally, no reciprocal possible here, noted).

- P6 PASS 2026-08-20 — shipped: authorkit 0.25.0; tree = SKILL.md · intent.md · scripts/host_probe.mjs (selftested) · references/remedies.md (F1–F9) · evals/{evals.json, assertions.md, behavior-check.md, audit-report.md, baseline/×3}. Reminders honored: /doctor after install (listing budget); no snapshot mirrors exist for authorkit.
- ENRICH 2026-08-20 (authorkit 0.26.0) — F5/F10 wave from gen-ui-kit's same-day performance
  report (P4/P5/P6, relayed cross-session): probe worktree census gains per-home `pkgManagers`
  (npm/pnpm mix) + `nodeModulesDiskMB` (null = du over budget); remedies catalog gains the pnpm
  shared-virtual-store structural remedy on F5 (two verification prerequisites stated,
  designed-not-built) and new **F10 — gate-lane oversubscription** (cause-side twin of F3,
  computed from existing probe fields, portable, fenced against flaky-gates). The tree is now
  F1–F10 (supersedes the F1–F9 counts in the P3/P6 lines above, which stay as dated history).
  Fresh-context skill-checker PASS (this entry is its one minor, applied).
