# Overhaul run — 2026-08-19

Driver: plugins-marshal session (live user: Kim). Read copy: fresh main clone at
`scratchpad/overhaul` (all mutations via scratch-clone branches + PRs; this worktree is the
ledger's home only).

## Scope (Phase 0 — pending gate 1)

| root | markers | classification | recommended | why |
|---|---|---|---|---|
| design | plugin.json · 25 skills · 3 agents · v1.2.4 | governed (root manifest ancestor) | IN | named in the argument; largest of the five |
| agent-protocols | plugin.json · 8 skills · 0 agents · v1.0.12 | governed | IN | named |
| screens | plugin.json · 16 skills · 3 agents · v1.1.2 | governed | IN | named |
| llm | plugin.json · 10 skills · 0 agents · v1.0.17 | governed | IN | named |
| teamwork | plugin.json · 19 skills · 10 agents · v2.28.14 | governed | IN | named; heaviest agent roster |

Governance: no plugin carries a bundled naming.manifest.json (root manifest governs; G12b parity
applies only where a bundled one exists — none here). Root doctrine.manifest.json present →
doctrine-audit fires estate-wide (its edges name teamwork + harness members).
Noise: 0 excluded paths.

Batch threshold: 5 estates > 3 → Phase 1 runs per-instrument via estate-audit-agent batches.

## Waves (Gate A: ALL APPROVED, 2026-08-19)

| wave | rows | risk | status |
|---|---|---|---|
| S0-A | +22 vocab nouns → root naming.manifest.json (retires 36/37 exemptions) | LOW | approved |
| S0-B | 7 descriptions cite feature-intake-rules/token-feature-intake-rules instead of restating | MEDIUM | approved |
| W1 | (empty — zero renames; grandfather ruling holds) | — | n/a |
| W2 | 17 diets/citation edits: design 11, screens 4, a-p 2; HIGH rows check-colors + material-type-facts serialized | MED/HIGH | approved (all 17) |

Execution-order note (driver): S0-B and W2 touch overlapping descriptions — executed per-estate
as ONE builder each (S0-B rows first, then that estate's W2 rows, one branch/bump/check-routing),
honoring the Blocked-by ordering inside the dispatch instead of across two merge cycles.
disable-model-invocation nominations: KILLED at planning (three-grep test failed grep 2 for all
three candidates — named Skill-path callers exist).

## Emergent queue

| item | shape | route | status |
|---|---|---|---|
| measure.py large-failure-section threshold (2/2 false positives) | instrument bug | file-bug | MINTED #775 |
| doctrine axis silent-by-omission for the 3 estates | manifest-authoring question | file-task | MINTED #776 |

## Phase 4 — EXECUTE

- **S0-A: DONE** — PR #777 merged. 29 vocab nouns added (2 rounds; catalog/motion skipped, shelf
  clashes); 31 exemptions retired (85→54); residual 7 all grandfathered (ADR-0011 D8); all 8
  plugins validate 0 grammar errors.
- **S0-B + W2: DONE** — #781 (agent-protocols 1.0.13), #783 (screens 1.1.3), #787 (design 1.2.5)
  all merged. The t19 safeguard caught 3 real diet regressions across the waves (screens
  archetype trigger; design t12 + t08), all healed in-change; design's builder self-caught a
  4th (dropped "low-vision"). One nested-judge stranding recovered by marshal nudge.

## Phase 6 — PROVE (2026-08-19, fresh main clone)

| axis | baseline | now |
|---|---|---|
| naming errors (3 estates) | 0 | 0 |
| exemption notes (3 estates) | 37 | **7** (all grandfathered: pick-fonts, break-down-×2, make-a2a-agent, make-figma-make-kit, material-motion-facts, a2ui-catalog-facts) |
| manifest exemptions array | 85 | **54** |
| over-700 descriptions | 13 (9+3+1) | **0** |
| routable chars: design | 18,887 (+2,130 agent) | 17,021 (+1,995) |
| routable chars: screens | 11,228 (+1,809) | 10,334 (+1,809) |
| routable chars: agent-protocols | 5,333 | 5,259 |
| doctrine | clean (by omission for the 3) | clean, no wave-introduced drift |
| attention trend row | — | appended for all 8 plugins, landed on main |

Routing proof: per-wave blind re-judges (design 258 cases, screens full touched-suite re-judge,
agent-protocols 45/45), regressions healed in-change. Cross-plugin recheck of design's
icon-rules n03 (scoped-menu artifact) DISCLOSED as not re-run estate-wide this pass — the #750
full-design run and per-wave proofs stand; a future estate /check-routing covers it.

- **S0-B + W2 (superseded status line): IN FLIGHT** — tickets #778 (design), #779 (screens), #780 (agent-protocols);
  3 build-leader dispatches in parallel, envelope-assisted (envelopes clean; the #773
  CLAUDE_SCRATCHPAD fix confirmed working — clones landed in the session scratchpad). Each
  builder: S0-B rows first, then W2 diets (design's HIGH rows serialized), t19 grep-before-cut,
  slice wording-checker overlapped with prep, post-edit blind re-judge, hold at write-gate.

## Gates

- Gate 1 (scope): ANSWERED 2026-08-19 — Kim picked "Only the design-family three": **design,
  screens, agent-protocols IN; llm and teamwork OUT** (teamwork mid-churn, llm deferred).
- Gate A: —
- Gate B: —

## Phase 1 — MEASURE (in flight)

3 estates ≤ threshold, but 9+ inline instrument runs would flood the driving session's context —
measuring via read-only estate-audit-agent batches (the agent's own stated purpose), one per
instrument, 4 in parallel:
- naming-audit (3 estates)
- bloat-audit (3 estates)
- attention-audit (3 estates, routing columns absent-if-no-report)
- doctrine-audit (root manifest, findings scoped to the three estates)
- pattern-audit: ABSENT — no pattern named in the invocation.
Read copy: fresh main clone at scratchpad/overhaul.

### Baselines (as they land)

- **doctrine** (returned): sweep CLEAN estate-wide (0 findings / 8 mechanizable, 3 judgment
  queued out-of-scope). For design/screens/agent-protocols: **clean BY OMISSION** — zero of the
  11 edges name any file in the three estates. Emergent-queue candidate: the doctrine axis is
  silent for these estates rather than verified-clean; whether they've earned edges is a
  manifest-authoring question, not drift.
- **naming** (returned): 0 errors / 0 warnings across all 55 artifacts — every finding is an
  exemption (design 20, screens 11, agent-protocols 6, total 37 of the manifest's 85). Systemic:
  36/37 are the SAME class — a domain noun missing from the manifest vocab (`material`×5, `ui`×2,
  `protocol`×2, `training`×2, `figma`×2, `design`×2, plus 15 singletons). Auditor recommends one
  batch vocab-add via manifest-authoring instead of piecemeal exemptions. True rename candidates
  (grammar, not vocab): `pick-fonts` (bare-verb head), `break-down-flow`/`break-down-layout`
  (mirrors the accepted break-down-problem precedent — ProcessLex add, not renames),
  `make-a2a-agent` (reserved `-agent` tail on a skill). No frontmatter drift, no orphaned
  relations.
- **bloat** (returned): **0 real findings across all 55 files** — every mechanical flag (30
  long-body, 2 large-failure-section) resolved to load-bearing content on CALIBRATION.md
  judgment; 0 duplicate pairs anywhere. Emergent-queue candidate: measure.py's
  large-failure-section threshold produced 2/2 false positives on enumerated failure lists —
  a script-calibration item for authorkit, not a content fix.
- **attention** (returned): rent — design 18,887 skill chars + 2,130 agent (9 over-700), screens
  11,228 + 1,809 (3 over), agent-protocols 5,333 (1 over). check-colors is design's structural
  blocker (1,280 chars, −580 headroom, blocks fences on 3 of the top-8 collision pairs).
  Systemic (3+ estates): the "feature-intake ticket" boilerplate sentence recurs in 10 of 19
  cross-plugin collision pairs across ALL THREE estates (+ its smaller sibling, the *-facts
  template). disable-model-invocation candidates (high rent + zero usage): design
  color-contrast-facts (1196), material-type-facts (814); screens ui-pattern-facts (1031) —
  three-grep test owed before any flip. trend.py deliberately not run (read-only clone).

### Grandfather check (driver's own, pre-planning)

The naming report's "rename candidates" (pick-fonts, break-down-flow/-layout, make-a2a-agent)
all shipped before 2026-08-13 → **grandfathered verbatim under ADR-0011 D8, no rename campaign**.
The vocab batch-add still retires their exemptions without touching any name.
