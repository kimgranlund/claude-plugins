# Migration provenance

Ported from `nonoun-plugins/brand-forge` at frozen SHA `1e0d2d9e554b547f59260f63e31b4af2575196b0` (v0.4.36,
2026-06-20), via the 2026-08-19 overhaul-execute migration campaign
(ledger: `.claude/overhaul-run-2026-08-19-brand-design.md` in kimgranlund/claude-plugins,
checklist: https://claude.ai/code/artifact/b4840743-ca07-4676-8475-ad8564f5b6f0).

Source repo left untouched (Gate A ruling). `source-README.md`, `source-CHANGELOG.md`,
`source-ROADMAP.md` in this directory are the pre-migration record, verbatim.

## What changed structurally (Gate A rulings)
- Council: 17 agents -> 3 (`muse-agent`, `brand-writer`, `brand-judge`); 14 named critics ported
  verbatim as `references/critics/*.md` personas; the orchestrator retired into
  `check-brand-council`'s own procedure (host-side unnamed dispatch, not nested Agent calls).
- 9 commands -> user-invocable skills, renamed to VerbLex-legal heads (see the naming table in
  the campaign ledger).
- `hooks/brand-lint` (#466 retired estate-wide) -> gate-time script calls.
- `bin/corpus-reader/` (a static web app, not a script) -> `references/corpus-reader/`; only its
  `build-sitemap.py` generator promoted to a real bundled script.
- `evals/council-calibration/` + `evals/guidelines-walkthrough/` (dated quality-history data,
  distinct from routing evals.json) ported verbatim, Phase 3 retrofits selftests.
- `agents/.name-map.md` (gitignored critic-attribution data in the source) deliberately NEVER
  copied into this repo — carried outside both repos, per Kim's ruling.
