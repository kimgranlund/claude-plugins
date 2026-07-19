# orchestration — run a multi-agent feature-delivery team end to end

Sibling plugin to forge (which authors the harness) and scribe (which authors what flows through it).
This plugin owns the composition layer: deriving the decisions a greenfield needs, designing how
skills/subagents/teams discover and wire together, designing the continuation patterns that keep an
autonomous run bounded, and the five-seat delivery team that actually plans, builds, documents, and
reviews a feature. Assembled by a `plugin-decompose` partition of `~/.claude/skills` and
`~/.claude/agents/delivery`.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/intent-grill` | Declarative skill | both | Derives the load-bearing design decisions for a greenfield surface across two crossing axes (Structural / Mechanism) and cascading rounds; hands off a Ratified Design to `system-decompose` and the document author |
| `skills/orchestration-design` | Declarative skill | both | Design or review how skills, subagents, and teams compose, and the YAML frontmatter that wires them — unit choice (skill/subagent/team), sealed-dispatch discipline, the D2/D4 gate |
| `skills/loop-design` | Declarative skill | both | Design or review continuation patterns — `/goal`, `/loop`, Stop hooks, auto mode — that decide *when* the next turn fires; the self-orchestrated-looping canon for a delegating loop (budgets, locus escalation, durable state) |
| `skills/concurrency-design` | Declarative skill | both | Decide whether concurrent sessions/subagents touching one repo need git-tree isolation, and what to do when they collide anyway — the three-actor classification (spawned subagent / addressable peer session / opaque concurrent session) and the matching response for each |
| `skills/session-close` | Procedural skill | both | Wraps up a session's own worktree before it ends: checks mechanical git state, routes real findings through bug-report/feature/issue, triggers knowledge-harvest's detection pass, verifies every write via read-back, and states a mandatory two-shape verdict |
| `hooks/hooks.json` (`SessionEnd`) | Hook | automatic | Passive safety net for `session-close`: on actual session termination, logs a durable warning line if a git worktree was left dirty or unpushed — `SessionEnd` cannot block, so this never gates, only records |
| `skills/build` | Command skill | user-only (`/build`) | Record-first build: finds or mints the feature record (running scribe's `/feature` intake inline on a miss), sizes the dispatch by the solo-first floors (small → host inline / one sealed fork; big → the floored seats), drives it under a mandatory Findings write-back, closes the loop on the ticket |
| `agents/orchestration-coordinator` | Subagent | dispatch-only | The apex seat: chain-of-command, dispatch order, the review gate between phases, the discovered-reality escalation loop, rollups to the host |
| `agents/system-planner` | Subagent | dispatch-only | The design seat: decomposes a problem across both planes, authors/maintains PRD/SPEC/LLD/ADR |
| `agents/system-builder` | Subagent | dispatch-only | The build seat: implements an approved LLD's build sequence, runs mechanical checks, escalates design conflicts rather than editing the contract |
| `agents/docs-writer` | Subagent | dispatch-only | Owns a documentation site: derives pages from their canonical source, makes drift a failing gate, reports soft drift a static check can't see |
| `agents/code-reviewer` | Subagent | dispatch-only | Independent critic for one bounded code change, scored against the contract it was built to; generator ≠ critic for the delivery loop |
| `agents/orchestration-reviewer` | Subagent | dispatch-only | Independent critic for how skills/subagents/teams compose and the frontmatter that wires them, scored against `orchestration-design`'s rubric; a real gap closed post-migration (see below) |

## Construction note: hard cross-plugin preloads converted to soft mentions

Every one of the five ported agents carried a `skills:` frontmatter preload into skills that no
longer live in this plugin boundary. Fixing this was the bulk of the porting work:

- **`orchestration-coordinator`** preloaded `handoff-compose` (now in forge). Dropped from the
  preload list; the body now soft-mentions forge's `handoff-compose` block with an inline
  Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action
  fallback wherever it names a handback. `skills:` is now `[orchestration-design, loop-design]` —
  the two preloads that are still same-plugin, real preloads.
- **`system-planner`** preloaded `system-decompose` (now in forge) plus `prd-author`, `spec-author`,
  `lld-author`, `adr-author` — four names that no longer exist anywhere as skills: scribe
  consolidated all four into `doc-authoring-standards` plus a `doc-forge` drafting command. Every one
  of the six preloads was cross-plugin or stale, so the frontmatter now carries no `skills:` field at
  all; the body soft-mentions forge's `system-decompose` and scribe's `doc-forge`
  (`doc-authoring-standards`), each with its own inline fallback (the two-plane decomposition method;
  each document type's minimum contract — Problem/Users/Outcomes/Non-goals for a PRD,
  Requirements/Non-goals/Examples/Acceptance for a SPEC, Components/Interfaces/Data/Risks for an LLD,
  Context/Decision/Consequences for an ADR).
- **`system-builder`** preloaded `lld-author` (stale — same scribe consolidation), `system-decompose`
  and `handoff-compose` (both forge). Same fix: no `skills:` field; the body soft-mentions
  scribe's `doc-authoring-standards` for reading an LLD's shape, forge's `system-decompose` for
  implementation-level sub-breakdown, and forge's `handoff-compose` for the report-out, each with its
  inline fallback.
- **`docs-writer`** and **`code-reviewer`** each preloaded only `handoff-compose` (forge). Same fix:
  no `skills:` field; each body soft-mentions forge's `handoff-compose` block with the same inline
  fallback shape.

The pattern throughout: name the cross-plugin skill and use it where installed; otherwise apply its
minimum contract inline. No agent here silently degrades — every fallback is spelled out in the body,
not merely implied. `intent-grill`'s own SKILL.md carried the same stale
`prd-author`/`spec-author`/`lld-author` references in its NOT-for clause and output contract; those
were repaired the same way, pointing at scribe's `doc-forge`/`doc-authoring-standards`.

`loop-design/scripts/harness_checks.py` shipped in the source library as a symlink to a sibling
skill (`skill-author`) outside this plugin boundary — a second, quieter instance of the same
cross-boundary problem, this time at the file-path layer rather than the frontmatter layer. It has
been materialized as a real, self-contained copy so the skill's Review step
(`scripts/harness_checks.py goal "<goal text>"`) and its bundled selftest run standalone.

## Evals

Each model-invocable skill ships `evals/evals.json` in this workspace's `{skill, cases:[{id, prompt,
expect}]}` schema (`eval_check.py` E1–E5); the original three converted from the pre-migration
library's `scripts/routing-corpus.json` positives/negatives, `session-close`'s authored fresh at
mint.

v0.7.6 · assembled 2026-07-19 · 0.7.6: new `session-close` skill — wraps up a session's own git
worktree before it ends: checks mechanical git state, routes real findings through
bug-report/feature/issue, triggers knowledge-harvest's detection pass for a durable lesson, verifies
every write via read-back before counting it, and states a mandatory two-shape verdict (a
captured-items list or a single clean line — never silence, never a manufactured write to fill the
silence). Paired with a new, non-blocking `SessionEnd` hook (`hooks/hooks.json` +
`scripts/session_end_worktree_check.py`) that logs a durable warning if a worktree is left dirty or
unpushed at real session termination — a separate, secondary artifact, since `SessionEnd` carries no
decision control and cannot gate anything (verified against Claude Code's own hook docs before
building it, correcting an earlier plan that assumed otherwise). Fresh-context audit
(skill-auditor, FLOOR): 1 blocking finding fixed (a clean-tree fast path was skipping the
knowledge-harvest scan too, not just the git-side capture) and 2 majors fixed (an unanchored trigger
phrase collided with `open-questions-sweep`'s own eval case; this intent record had been advanced
past gates not yet actually run). A second, independently-dispatched skill-auditor (a separate
earlier-launched teammate whose report arrived after the fixes above already shipped)
cross-validated the same three findings against the pre-fix tree and surfaced two further MINORs,
fixed same-day: the git-absent failure branch collapsed from a third ad hoc verdict string into the
existing two-shape contract's own clean line, and the unattended-context failure branch now names
step 2's own capture skills (bug-report/feature run their own interactive intent-extract round) as
deferred alongside step 3's confirm gate, not step 3 alone. Reciprocal NOT-for fences added:
`concurrency-design` (this plugin) and forge's `open-questions-sweep`, each gaining a return
no-trigger case in its own `evals/evals.json` · v0.7.5 · assembled 2026-07-19 · 0.7.5: `concurrency-design` cross-references ADR-0005's ticket-claim
protocol — one boundary note added to its existing ticket-status pre-flight check (Decide step 3)
and one References & tools row: `claim` (scribe, where installed) prevents two independent agents
from starting the SAME ticket, one layer beneath this skill's own git-tree collision response,
which still has to catch two DIFFERENT tickets touching the same file. No description change, so
no eval-run obligation follows · v0.7.4 · assembled 2026-07-18 · 0.7.4: `/eval-run orchestration` tuning — a full blind-judge
routing pass (all 4 suites, against the estate's full 96-skill menu) found `orchestration-design`
leaking on two whole-corpus-audit phrasings ("audit the agent team for duplicates", "do my agents
leverage the right skills") despite an existing skills-audit/agents-audit fence that wasn't
landing on this exact wording — both added verbatim to the NOT-for clause and re-verified passing
via a second blind-judge pass · v0.7.3 · assembled 2026-07-18 · 0.7.3: concurrency-design gains async git-native coordination —
the opaque-session actor-type row and its escalation step now cover the case where the other
actor's work lives on a branch/PR/Issue with no live `SendMessage` channel: post a comment there
(durable, visible to whoever looks next) in addition to, not instead of, asking the human. Grounded
in a real incident: a repo-orchestrator session found three open PRs independently bumping the
same plugin's version from the same base, two still owned by live background sessions with no
teammate-message channel — resolved by posting the dependency on each PR rather than escalating
each one to the human. New tools-table row (`gh pr comment`/`gh issue comment`), Output contract's
Action enum extended, second worked example added · v0.7.2 · assembled 2026-07-17 · 0.7.2: concurrency-design — decide whether concurrent
sessions/subagents touching one repo need git-tree isolation, and what to do when they collide
anyway. Core uplift: baselines conflate three distinct actor types into "spawned vs. not"; this
skill's three-way classification (subagent spawned this session, full control · a peer session
addressable via `SendMessage` because it surfaces as a `teammate-message` sender · a truly opaque
concurrent session with no channel at all, the only case that structurally requires routing
through the human) and its matching response is the uplift baselines don't reach for on their own.
Fresh-context audit (skill-auditor): 1 MAJOR fixed — the first draft's isolation defaults
contradicted orchestration-design's own shipped guidance (worktrees only for overlapping targets,
not any multi-actor dispatch); reworded so isolation conditions on overlap, not actor count, with
the reciprocal disjoint-fan-out no-trigger case added. 3 MINORs fixed, incl. a commit-cadence eval
with no supporting description vocabulary. A real mishap during the behavior check (a dispatched
check agent added a live doctrine restatement to a consumer repo's CLAUDE.md despite a no-tools
instruction) is disclosed as-is in `evals/behavior-check.md` rather than scrubbed — it named a
real gap (the CLAUDE.md rule must be a one-line pointer, never a restatement), now fixed in the
skill body. Reciprocal no-trigger fences added in forge's agent-authoring-standards/
entry-file-standards/hook-authoring-standards and this plugin's own loop-design/
orchestration-design. G8 allow-set gains `self-report` (prose, not a skill name) · v0.7.1 · assembled 2026-07-14 · 0.7.1: displayName 'Orchestration' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.7.0 · assembled 2026-07-12 · 0.7.0: seat-ladder realignment — forge 1.22.0's ratified ceiling ladder replaces the operating-contract table as the owner's contract (the 0.5.0 realignment's successor): system-planner opus+xhigh→fable+high, system-builder sonnet+high→opus+xhigh, orchestration-coordinator opus→sonnet (deliberate reclassification: routing/gating is coordination, not judgment), code-reviewer and orchestration-reviewer opus→fable+high; best-practices' security-reviewer example retiered to the review row · v0.6.2 · assembled 2026-07-12 · 0.6.2: /build's inline-intake clause decides the index-bootstrap inheritance — the opt-in offer rides along where scribe is installed; no offer without scribe's template · v0.6.1 · assembled 2026-07-10 · 0.6.1: author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder) · assembled 2026-07-09 · 0.6.0: /build — record-first build command, /feature's momentum half: finds or mints the feature record (running scribe's intake inline on a miss), branches on record state (done/wontfix stops; kind: bug hands to bug-report), sizes the dispatch by the 0.5.0 solo-first floors (small → host inline / one sealed fork via the fork-vs-agent test; big → the floored seats), drives under a mandatory dated Findings write-back with a /goal try-cap, closes the loop on the ticket. loop-design's gates table gains the feature-ticket row. Independent FLOOR audit: PASS, all findings applied (TKT resume-state branch was the major) · assembled 2026-07-09 · 0.5.0: de-escalation tuning — consumer projects reported sluggishness from over-eager multi-agent ceremony. Materiality floors on every PROACTIVE trigger (system-planner no longer fires on 'any feature' — a feature must EARN a design doc; coordinator needs genuinely ≥2 seats — 'multi-step alone does not earn a team'; code-reviewer scoped to substantive slices; docs-writer to documented-surface changes; system-builder's adherence trigger to multi-context work; orchestration-reviewer to MATERIAL wiring changes); solo-first null-unit rule as orchestration-design Design step 1 + rubric D1 anchor + Done predicate + best-practices Do/Don't; model realignment to the owner's contract (system-planner fable→opus, docs-writer opus→sonnet). Explicit-ask routing untouched — every quoted-ask list kept verbatim. Independent orchestration-reviewer pass: gates PASS, both Majors (planner-body one-file-fix contradiction, rubric's missing null-unit anchor) fixed pre-ship. Known gap recorded: no agent-level routing eval mechanism exists estate-wide to pin the floors — candidate infrastructure for a future wave · assembled 2026-07-09 · 0.4.4: hygiene pass — orchestration-design's agent-author phantom fence repointed at forge's agent-forge/agent-authoring-standards · assembled 2026-07-09 · 0.4.3: references to the renamed skills swept (ADR-0001) · assembled 2026-07-09 · 0.4.2: orchestration-design's suite annotated for the accepted command-off-menu leak class; post-tuning blind re-run 61/61 · assembled 2026-07-09 · 0.4.1: all six agents' fallback blocks 'Tests run'→'Tests/checks run' (harness-audit finding, estate-wide sweep) · assembled 2026-07-07 · 0.4.0: fixed a real, user-reported pain inherited verbatim from the legacy corpus — system-planner's charter mandated authoring PRD+SPEC+LLD+ADR as a bundle on every planning dispatch, regardless of whether any one of them was warranted; "author all four" is now four independent routing decisions, ADR defaulting to NO unless a genuine fork with real rejected alternatives was resolved (contradicted adr-author's own philosophy — "if the Context could be deleted and the Decision still read fine, the Context is doing no work" — the mandate overrode the judgment call the philosophy demands) · 0.3.0: orchestration-reviewer agent ported — the last confirmed pre-migration gap; it fell through the cracks between forge's reviewer batch and this plugin's original member list (it reviews orchestration-design, which lives here, not in forge). Same soft-mention fix as its four siblings: `skills:` keeps only `orchestration-design` (same-plugin); `handoff-compose` and the hardcoded `~/.claude/skills/orchestration-design/SKILL.md` path both fixed · 0.2.0: loop-design gained a "this workspace's gates as goal conditions" recipe table (release_gate.py/skill_lint.py/doc_lint.py/eval_check.py/handoff_check.py and bug-report's Findings-entry predicate, each with a suggested try-cap) plus a worked proactive-intake example (`/schedule` + `/goal` + bug-report) · 0.1.0: initial: ported from ~/.claude/skills + ~/.claude/agents/delivery as part of a plugin-decompose partition
