# Baselines — 2026-08-20, fresh general-purpose agents WITHOUT the skill

CAVEAT recorded honestly: both baseline agents ran inside the agent-ui project session and
inherited its CLAUDE.md + accumulated memory (baseline-b literally cites "your memory notes the
ps aux vitest self-match trap") — so these are BEST-CASE baselines, far stronger than a cold
user's. Even so, both MISS relative to the skill's contract: neither produces a machine-readable
probe (each lists ad-hoc commands to maybe run), neither checks Time Machine inclusion
(`tmutil isexcluded`) or the `.metadata_never_index` mechanism (baseline-b names the Privacy
pane only), neither censuses parked worktrees against merged branches, and neither emits the
warned checklist contract (finding → measured number → mechanism → THE command → severity →
warning tier). A cold user (no project memory) gets the generic Activity-Monitor tier. The
skill's delta = the exact probe script + the report contract, uniformly, for anyone.
