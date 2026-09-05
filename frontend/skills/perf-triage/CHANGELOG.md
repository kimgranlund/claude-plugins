# Changelog

## 2026-09-05 · initial release (frontend 2.7.0)
- New skill: report to brief. `scripts/lh-brief.mjs <json...> [--out perf-brief.md] [--max-lines 400] [--items 5]` emits header, DO NOT BREAK list (passing audits + metric tolerances), failing audits ranked (score asc, wastedMs desc, wastedBytes desc) with a fixed cause-family taxonomy, a fix order by blast radius, and a line cap with a truncation note; `--slim` writes trimmed fixtures. `assets/fixtures/` carries the two 2026-09-05 ui-kit.exe.xyz prod reports (chat playground, admin dashboard), slimmed; the selftest locks every family tag the spec's finding list names. Exports the taxonomy and tolerances for lh-diff/lh-scoreboard. Provenance: 1rehfjf, 1tewaoi, 1taw297 (comment).
