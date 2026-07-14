---
doc-type: adr
id: adr-0002
status: proposed
date: 2026-07-15
ratified: 2026-07-15 (maintainer, in-session AskUserQuestion — three rulings, one session)
owner: kim.granlund
---
# ADR-0002 — Git-native execution: Issues as the work-item canon, PRs as the merge gate, CI + style lint

## Context

An evaluation of the estate's linting and orchestration posture (2026-07-15) found: (1) the lint
tier is near-ceiling *in-session* (PostToolUse hook, composed G1–G10 gates, mandatory selftests)
but everything runs locally — a human editor or a parallel Claude session bypasses it entirely,
and nothing runs on push; (2) the estate's ~40 bundled `.py`/`.mjs` scripts have behavior proofs
(selftests) but no style/static linting; (3) execution is single-writer on `main` with no
branches or PRs, and **three concurrent-session collisions occurred in one week** — uncommitted
work from parallel sessions repeatedly shared one working tree, with safety resting on manual
disclosure at commit time. Worktree isolation exists in the harness (Workflow `isolation:
worktree`) but is not woven into the house workflow. The maintainer ratified three rulings via
AskUserQuestion; the third diverged from the session's recommendation (ruff-only) toward fuller
coverage.

## Decision

1. **Git-native max for work routing.** GitHub Issues become the work-item canon for this
   workspace (the TICKET/TASK tier); PRs become the merge gate for campaigns; a campaign runs on
   its own branch + git worktree (opt-in per campaign, default for multi-session or parallel
   work). `docs/tickets/` retires for NEW work items in this workspace. **Scope boundary:** only
   the work-item tier moves — ADR/PRD/SPEC/LLD and the README footer ledgers remain in-repo files
   (the ledger mutability classes are unchanged; an Issue is a work item, not a decision record).
   scribe's `/bug-report` and `/feature` remain file-ticket skills as shipped (portable product
   behavior); adapting them to a git-native backend where a workspace rules it is queued as this
   repo's first GitHub Issue rather than redesigned inline.
2. **Local + CI enforcement.** The in-session hook and local gates stay; a GitHub Actions
   workflow (`.github/workflows/gate.yml`) runs `release_gate.py` over all nine plugins plus the
   gate scripts' own selftests on every push to main and every PR — closing the
   human-editor/parallel-session bypass.
3. **Style lint for both script ecosystems.** ruff (`.py`) and eslint (`.mjs`/`.js`) join the
   lint tier as gate check **G11** — workspace-root configs (`ruff.toml`, `eslint.config.mjs`,
   both dependency-free), run-if-reachable/WARN-if-absent locally (the G4-node-leg posture),
   enforced in CI. Two ruff rules are configured out as deliberate house idiom (E702 semicolon
   one-liners, E731 lambda assignment); behavior remains G4/selftests' job.

## Consequences

- The concurrency hazard class (shared-tree collisions) is closed structurally for campaigns that
  opt into worktrees, and detectably for everything else (CI gates what local hooks miss).
- Two canons are avoided: work items live in Issues, decisions/contracts/ledgers stay files.
  The cost: work-item queries now need `gh` (or the GitHub UI) instead of Grep over
  `docs/tickets/`; agents working offline lose work-item visibility.
- The zero-dependency posture softens at the tooling boundary only: eslint arrives as a
  CI-installed/npx-run tool with an import-free flat config; no node_modules is committed.
- scribe's file-ticket path stays correct for consumers; this workspace's routing overrides it
  (workspace CLAUDE.md), and the backend adaptation is tracked as Issue #1 — until it lands,
  `/bug-report`/`/feature` in this workspace write Issues via `gh` per the routing table, not
  ticket files.
- 13 real defects surfaced the day ruff/eslint arrived (unused imports/variables, ambiguous
  names, an incomplete-rename NameError caught by a selftest during the fix wave) — the layer
  paid rent immediately.
