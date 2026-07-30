Permission allow rule (.claude/settings.json): Write(.claude/ops/watch-checkpoint.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/watch-checkpoint.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/friendlies.json) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/friendlies.json) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/held-items.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/held-items.md) instead (Edit rules cover all file-editing tools).
Permission allow rule (.claude/settings.json): Write(.claude/ops/reports/*.md) is not matched by file permission checks — only Edit(path) rules are. Use Edit(.claude/ops/reports/*.md) instead (Edit rules cover all file-editing tools).
All three leftovers are now tickets — nothing else was dropped.

**Minted (in `kimgranlund/claude-plugins`):**
1. [#117](https://github.com/kimgranlund/claude-plugins/issues/117) — bug: login bug; blocked-at-intake finding recorded, needs your symptom + repro
2. [#118](https://github.com/kimgranlund/claude-plugins/issues/118) — feature: CSV export, `size:small` provisional, scope open
3. [#119](https://github.com/kimgranlund/claude-plugins/issues/119) — task: decide the retry policy; the decision lands as a Findings comment there

**Discards:** none. **Not minted:** nothing else — this session's transcript starts at your message, so the sweep's only evidence was your recap; all three rows quote it.

Caveats (🟡):
- None of the three items name a product or surface, and they landed in this plugins-workspace repo because it's the resolved backend here. If they belong to a different project, tell me and I'll re-home them.
- Native GitHub issue types are undefined in this org, so the `bug`/`feature`/`task` labels carry the classification (noted per the skill's contract).
- Project-docs index skill not offered (non-interactive run) — a later `/file-feature` run can add it.

Next (~2 min): reply with the login bug's actual symptom (`/file-bug #117 <detail>`) so investigation can start.
