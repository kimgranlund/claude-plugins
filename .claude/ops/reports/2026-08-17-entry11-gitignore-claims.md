# Plan entry 11 — gitignore re-measure + stale-claim survey (2026-08-17, drain session)

## gitignore_check
`gitignore_check · warn` — the same two standing G1 WARNs, no change from prior firings:
- `dist/` matches nothing (on-demand: `release_gate.py --package` output)
- `harness-audit-*/` matches nothing (on-demand: audit runs)
Both carry the recorded every-firing ruling: on-demand-generated, accepted, no edit. No G2 FAIL —
no uncovered generated dir exists on disk.

## Stale-claim survey
Zero assignee-based claims on any open issue (#490, #520–#526). Comment-based claims all live and
fresh (updated within the hour): #520–#524 held by plugins-dd's ADR-0020 wave chain (W2 building),
#525 execution rides wave 5 (recorded hold), #526 waits on the gen-ui-kit harvest (agent-ui#1115),
#490 waits on upstream (anthropics/claude-code#87349). **No stale claims found.**

Verdict: entry 11 CLEAN — nothing actionable, both WARNs pre-ruled.
