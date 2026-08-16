# Drain: waves F/G/H over the post-charter backlog — coordination record

Confirmed by Kim 2026-08-16 ("Full drain, waves F→G→H"). Same discipline as the closed
Batch-C/D/E charter (.claude/ops/charter-batch-cde.md): sealed dispatches, critics via
definition pins (fable·medium, PR #314 — NO per-dispatch model overrides), one
version-bumping build per plugin at a time, coordinator merges after CI, campaign_close per PR.

## Waves
- F: #310 DONE (PR #317 merged, teamwork 2.13.2 + harness 3.8.2) · #296 DONE (PR #315 merged,
  authorkit 0.11.1) · #300 BUILDING (screens 1.0.10)
- G (DISPATCHED): #313 (harness 3.8.3 slot) · #294 (authorkit 0.11.2 slot) · #309 queued
  (F5 experiment; its skill-writing-rules fact note takes the harness slot after #313)
- F CLOSED: #300 DONE (PR #319 merged, screens 1.0.10 — 53.9 collision cleared, 26/26 routing).
- Side work DONE: project-docs consult-table repair committed (9907852) — bible indexed,
  label-scheme + PRD/LLD rows corrected, critic pass applied.
- Lifecycle track (Kim 2026-08-16, post-H queue in arc order): #316 (IDR impl) → #318 (RDD,
  Blocked-by #316) → #320 (lifecycle knowledge pack from the bible) → #321 (stage awareness —
  reads the record types as signals; soft-depends #316/#318). #320/#321 are scoping-first,
  gaps named in their bodies.
- H (pending G): #308 (F4; harness slot) · #297 (authorkit after #294) · #286 (authorkit
  after #297) · #293 (authorkit LAST — the agent merge inherits all prior authorkit changes)
- HELD: #258 (Kim's standing defer) · #295 (own charter later, per Kim's confirm choice)

## Ratified
- Waves F/G/H: all 9 pre-#293 tickets merged (PRs #315, #317, #319, #322-#327). Two host-sleep
  crashes (#308, #297) salvaged: #308 coordinator-finished post-critic, #297 seat resumed in
  place. F4 measured (skill's model wins; R6 un-capped WARN→FAIL), F5 measured (fork blocks
  foreground under -p; R5 confirmed for that path).
- Lifecycle arc CONFIRMED by Kim (2026-08-16, batched confirm): full arc in order after #293 —
  #316 (IDR impl) → #318 (RDD scoping, Blocked-by #316) → #320 (bible pack) → #321 (stage
  awareness). Serialize where docs-plugin files overlap. Same gates/merge discipline.
