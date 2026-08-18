# Doc spine id VALUE race (F6 split)

Phase 3's VALUE-race bullet (plugin versions) has a doc-spine twin: a dispatch that mints a new
`adr`/`idr`/`lld`/`rdd` record races the exact same way a plugin version does — a branch-cut
number goes stale the moment a concurrent build mints its own record against the same
then-current spine.

**The incident that named this rule (2026-08-18, #633).** Two parallel builds (#618's PR #630 and
#620's PR #631) both minted `lld-0011` against their own stale branch-cut spine. Nothing mechanical
caught it: the collision was found only by a coordinator's manual pre-merge read, and fixed by
renumbering PR #631's record to `lld-0012` before merge. Had the coordinator not happened to read
both diffs side by side, the collision would have shipped.

**The rule.** A dispatch minting a new adr/idr/lld/rdd record re-reads the spine's highest id for
that family off `origin/main` immediately before numbering it — never from the branch-cut
snapshot, exactly the same discipline as the plugin-version VALUE-race re-read (Phase 3/Phase 5
stage 2 above). The canonical statement of this rule lives in `docs:doc-writing-rules`' ID-spine
section (item 3) — this file exists only to keep dispatch-ticket's own body under its line cap
while still carrying the full incident context a builder reading this skill might want.

**The mechanical backstop.** Even when the re-read is skipped or raced anyway, `docs:doc_lint.py
--spine` (its T10 check) and `harness:docs_check.py`'s R7 both sweep `.claude/docs/**` for two
adr/idr/lld/rdd documents claiming the same (family, number) — keyed on the number, not the full
`id:` string, since two colliding drafts plausibly differ only in their descriptive slug. R7 rides
release_gate.py's existing G10 wiring (no new G-check), so every plugin's gate inherits the same
protection. Both are a catch AFTER the fact, at gate time — the re-read above is what avoids
minting the collision in the first place.
