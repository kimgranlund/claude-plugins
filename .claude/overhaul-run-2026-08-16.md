# Overhaul run — 2026-08-16

Driver: /overhaul-execute (session coordinator). Plan: `.claude/docs/lld/lld-0005-estate-overhaul-2026-08-16.md` (PR #346, merged 4ef595c; content Kim-confirmed pre-write).

## Scope table (Phase 0 — pending Gate 1)

| Root | Markers | Classification | Recommended | Why |
|---|---|---|---|---|
| /Users/kimba/Projects/nonoun/plugins | naming.manifest.json at root; 8× `*/.claude-plugin/plugin.json`; `*/skills/*/SKILL.md` trees; `.claude/` with skills | governed estate (single) | IN | the plan's own target; all 8 plugins governed by the one root manifest |

Noise auto-excluded: paths under `.claude/worktrees/` (this session's own), `dist/`, `.git/`.

## Phase 1 baselines (measured minutes before this run, reused not re-derived)

- naming-audit (grammar, 181 artifacts): 0 violations outside exemptions; exemptions 166, of which 10 stale.
- bloat-audit: 8/8 plugins covered (#258 sweep + core-4 sweep 2026-08-16); verified bloat = 2 systemic duplications + 28 stamped footers (pattern probe `STAMPED_FOOTER=Extending this pack`, 145 files, 28 hits).
- attention-audit rent baseline (rent.py, 2026-08-16): ESTATE-TOTAL routable_skills 122 / routable_chars 72,299 (~18,074 tok), zero-rent skills 22 / 11,647 chars, agents 28 / 18,466 chars (~4,616 tok). Per-plugin: harness 19,116 routable + 5,870 agent; design 14,269 + 2,205; screens 10,246 + 2,076; docs 8,806 + 2,487; authorkit 6,327 + 302; agent-protocols 5,268; llm 4,984; teamwork 3,283 routable + 5,526 agent (+4,906 zero-rent). collide.py: 505 cross-plugin pairs; top 6 all *-checker agents (158.4 worst: design-system-checker↔doc-checker) — shared generator≠critic template sentences, low misroute risk (domain fences intact). Raw JSON copied from job scratch: not durable — figures recorded here verbatim instead.

## Wave map (from lld-0005, pending Gate A)

| Wave | Seed | Action | Risk | Blocked-by |
|---|---|---|---|---|
| 0 | F | design:make-design-system → harness:plan-skill-split nomination (via /reshape-skill) | med | — |
| 1 | A | 28 stamped-footer sweep, 5 plugins (mechanical; serialize version bumps per plugin) | low | — |
| 1 | B | /exemption-retire the 10 stale manifest entries | low | — |
| 1 | C | authorkit structural hygiene (stray model field, frontmatter, .DS_Store ×4) | low | — |
| 2 | D | docs backend-seam paragraph → move-to-references (3 skills + evals) | med | — |
| 2 | E | teamwork lead-* adoption ritual → shared references/adopt-agent-contract.md (4 agents) | med | — |
| 3 | G | lexicon spec amendment: `-rules` class + ObjectVocab noun tail (contested) | high | — |

## Gate outcomes

- Gate 1 (scope): APPROVED (Kim, 2026-08-16, AskUserQuestion) — in scope as found, all 8 plugins.
- Gate A (findings + wave map): APPROVED all four waves (Kim, 2026-08-16, one batched round) — W0 approve, W1 all three, W2 both, W3 approve-as-design-ticket.
- Gate B (premise change): not fired

## Emergent queue

| # | Evidence | Problem | Blocker shape | Proposed solution | Route |
|---|---|---|---|---|---|
| E1 | collide.py top-6 pairs (score 103.9–158.4) all *-checker agents across design/docs/screens/teamwork; shared "scored in a fresh, isolated context / maker never grades own work / gap-map" template sentences | Checker-description boilerplate class pays rent in 6+ agent descriptions and inflates every pairwise collision score (systemic: 3+ estates → template problem) | template-tax (systemic) | Move the shared generator≠critic sentence from each checker's DESCRIPTION into its body; keep only the domain noun-phrase + NOT-fence routable. One ticket, 6+ agent defs, semantic → critic per def | docs:file-task at next gate |

## Per-wave status

- Minted (intake seat, 2026-08-16): #347 W0-F · #348 W1-A · #349 W1-B · #350 W1-C · #351 W2-D · #352 W2-E · #353 W3-G.
- Dispatched: #347 (analysis-only), #348, #349, #350 — four concurrent, disjoint targets. #351/#352 held for W1 close (plan order). #353 design ticket, execution deferred per Gate A.
- Ledger home note: working copy moved to this worktree (session isolation guard); commit to main as an ops record at campaign close.
- W0-F: analysis-only dispatch after mint; /reshape-skill execution (if split verdict) is human-run.
- W1 A/B/C: parallel after mint — disjoint targets (A: 5 pack plugins; B: manifest; C: authorkit). A serializes its own 5 version claims.
- W2 D/E: after W1 (docs/teamwork disjoint from W1 targets, but held to plan order).
- W3 G: design ticket only this campaign.
- Parallelism note: W0's analysis shares no member with W1–W3 (make-design-system is not among the 28 footers; plan doc records no cross-edges), so W0 analysis + W1 run concurrently under mobilize-chores' disjointness rule.
- W1-B #349: CLOSED — PR #354 merged (3c9e431), exemptions 166→156, all 10 re-verified before retire, gates clean, campaign_close clean. No plugin bump (root governance file).
| E2 | build-348 mid-task cwd redirected into build-350's worktree (no corruption — commit no-opd); coordinator hit the same class (session worktree identity migrating to newest-created worktree, write-guard follows) | Pinned-agent cwd sharing across parallel worktree sessions is a recurring hazard | infra-defect | Incident→infrastructure: file a bug with repro notes; candidate guard: worktree_prebash_guard or EnterWorktree pinning fix | docs:file-bug at next gate |
- W0-F #347: CLOSED — NO-SPLIT verdict (plan-skill-split tests 1–3 fail; healthy corpus). No manifest, no PR, zero design/ diffs. Wave 0 complete, no human /reshape-skill needed.
- W1-A #348: CLOSED — PR #356 merged (2d4ef51), 28 footers swept, 5 plugins bumped (design 1.0.6 / llm 1.0.10 / screens 1.0.12 / harness 3.8.11 / agent-protocols 1.0.8), all 5 gates clean.
- W1-C #350: CLOSED — PR #355 merged (e929477), authorkit 0.12.1; root-caused: validate.py schema gaps (model field + intent.md), pin kept; structural errors 11→9 (rest = fix-old-names fixture).
- Wave-1-close gate: Kim confirmed E1+E2 mints (AskUserQuestion, 2026-08-16). W2 dispatched: #351, #352.

## Wave 2 closes

- W2-D #351: CLOSED — PR #358 merged (bbfbb8e), docs 1.9.0; three intake skills now cite doc-writing-rules/references/backend-resolver.md (canonical text already existed); critic PASS, gate clean.
- W2-E #352: CLOSED — PR #360 merged (4dee5ef), teamwork 2.14.0; ritual centralized to lead-team/references/adopt-agent-contract.md, cited by lead-planning/lead-build; lead-review deliberately excluded (adopts no single contract); critic fix-then-ship (3 findings applied), gate clean.
- Emergent mints (Wave-1-close confirm): E1 → #357 (checker-description boilerplate, task) · E2 → #359 (worktree cwd-drift, bug).
- W3-G #353: design ticket, execution deferred per Gate A — stays open on the board by design.

## Phase 6 — prove + report (2026-08-16, main @ 4dee5ef)

1. Routing proof: no routable description changed in any executed wave (bodies/manifest/schema only) — boundary proofs stand from PR #344 (screens 22/22+24/24) and PR #345 (docs/harness 15/15). Named UNMEASURED-BY-DESIGN for this campaign rather than re-run.
2. Naming burn-down (validate.py --scope grammar, all 8 plugins at main): grammar errors 0 everywhere; structural errors authorkit 9 (all the deliberate fix-old-names fixture; was 11 at baseline, was 15 pre-campaign counting schema false-positives), all others 0. Exemptions 166 → 156.
3. Attention rent: 72,299 routable chars / ~18,074 tok — unchanged from baseline, as expected (no description edits executed; the rent-reduction work is minted as #357). Dated trend rows appended: attention-trend.csv (8 rows, routing columns `absent`).
4. Verdict roll-up: 🟢 estate — waves run 0/1/2 (5 rows executed + 1 no-split verdict), killed 0 at Gate B (never fired), W3 deferred by design; PRs all merged by coordinator post-CI (#354 #355 #356 #358 #360); emergent items minted #357 #359; skips: routing re-proof (reason above), trend routing columns absent (no routing report this run).

Campaign complete. Ledger committed to main as the ops record.
