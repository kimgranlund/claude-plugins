# teamwork — run a multi-agent feature-delivery team end to end

Sibling plugin to harness (the authoring toolchain) and docs (which authors what flows through it).
This plugin owns the composition layer: deriving the decisions a greenfield needs, designing how
skills/subagents/teams discover and wire together, designing the continuation patterns that keep an
autonomous run bounded, and the five-seat delivery team that actually plans, builds, documents, and
reviews a feature. Assembled by a `plan-plugin-split` partition of `~/.claude/skills` and
`~/.claude/agents/delivery`.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/grill-the-ask` | Declarative skill | both | Derives the load-bearing design decisions for a greenfield surface across two crossing axes (Structural / Mechanism) and cascading rounds; hands off a Ratified Design to `break-down-problem` and the document author |
| `skills/loop-rules` | Declarative skill | both | Design or review continuation patterns — `/goal`, `/loop`, Stop hooks, auto mode — that decide *when* the next turn fires; the self-orchestrated-looping canon for a delegating loop (budgets, locus escalation, durable state) |
| `skills/parallel-work-rules` | Declarative skill | both | Decide whether concurrent sessions/subagents touching one repo need git-tree isolation, and what to do when they collide anyway — the three-actor classification (spawned subagent / addressable peer session / opaque concurrent session) and the matching response for each |
| `skills/fleet-rules` | Declarative skill | both | The default operating protocol every orchestration-adjacent seat starts from instead of re-deriving it mid-run — the fleet-scoped coordination-scope ladder, the claim-then-guard sequence before dispatching, report-supersedes-nudge communication routing, one-version-bumping-build-per-plugin + merge-order rules, session-death resilience (orphaned-claim reset, resumable worktree/branch naming), and the `EnterWorktree` pin-race unblock playbook (#480) — AND (ADR-0020 D5, merged from `team-or-solo-rules`, closes #524) how skills/subagents/teams compose: unit choice (skill/subagent/team), sealed-dispatch discipline, the D2/D4 gate. Cites its canonical mechanics elsewhere (`dispatch-ticket`'s claim/version-collision checks, `mobilize-chores`' four-layer guard, `parallel-work-rules`' cwd-race detection, harness's `big-change-git-rules`' stacked-PR sequence) rather than restating them; preloaded by `fleet-marshal` and `build-leader` |
| `skills/close-session` | Procedural skill | both | Wraps up a session's own worktree before it ends: checks mechanical git state, routes real findings through file-bug/feature/issue, triggers save-lessons's detection pass, verifies every write via read-back, and states a mandatory two-shape verdict |
| `scripts/session_end_worktree_check.py.retired` | Retired script | none (hooks removed 2026-08-17, #466 — remove-all-hooks directive) | Formerly a `SessionEnd` hook: passive safety net for `close-session`, logging a durable warning line if a git worktree was left dirty or unpushed. `SessionEnd` never blocked; this was always a pure log, never a gate. Kept on disk retired, not deleted, for history |
| `scripts/worktree_prebash_guard.py.retired` | Retired script | none (hooks removed 2026-08-17, #466 — remove-all-hooks directive) | Formerly issue #139's repo-side `PreToolUse` mitigation, ASK-only: flagged (never blocked) a Bash command that `cd`'s or `-C`/`--prefix`'s out of a worktree cwd into the shared primary checkout or a sibling worktree and then ran a further command in the same call. Kept on disk retired, not deleted, for history — `parallel-work-rules` now carries this as a manual discipline instead |
| `scripts/pin_check.py` | Plugin script | `${CLAUDE_PLUGIN_ROOT}/scripts/pin_check.py <intended-branch> [--cwd <path>]` — called by `dispatch-ticket`'s Phase 3 mitigation-ladder bullet | Preflight, BEFORE-first-write check (#490/#609, ratified 2026-08-18): compares the session's actual bound git branch at `<cwd>` against the ticket's own decided branch name and fails loudly, naming the mitigation ladder's next rung, on a mismatch — catching pin drift before a write lands in the wrong tree rather than after. Also reports (informational only) whether `<cwd>` is the primary checkout or a linked worktree. `selftest` proves the drift/match logic plus the primary-vs-linked detection against a real `git worktree add` fixture — no network |
| `skills/build-feature` | Command skill | user-only (`/build-feature`) | The human-typed entry point only — delegates its full procedure to `dispatch-ticket` (issue #135: a `disable-model-invocation: true` skill can't be Skill-tool-invoked or preloaded by anything else, so the procedure had to move) |
| `skills/dispatch-ticket` | Procedural skill | model-only | The record-first procedure for one confirmed ticket of ANY kind (ADR-0010, renamed+generalized from `dispatch-feature`): finds or mints the record, then branches by kind — feature → size by the solo-first floors (small → host inline / one sealed fork; big → the floored seats) and build under a mandatory Findings write-back; task → one find-intent round, then a solo-first Agent dispatch under the same contract; bug → hand-off to docs' `file-bug` with the `[redirected-from:]` marker. Reached by name only, from `build-feature`'s own body or the `build-lead` agent's preload — never a direct user ask |
| `agents/build-leader` | Subagent | dispatch-only | The Agent-tool-reachable twin of `/build-feature` generalized to every ticket kind (ADR-0010, renamed from `feature-lead`; file renamed `build-lead` → `build-leader` closes #433, PENDING the naming-ADR that supersedes ADR-0011 REQ-002's `-agent` suffix rule), preloading `dispatch-ticket` — `mobilize-chores` step 5 dispatches every confirmed ticket here uniformly, per-ticket isolation being the reason this stays an agent rather than harness's `sweep-chores` shape (issue #266) |
| `skills/mobilize-chores` | Command skill | user-only (`/mobilize-chores`) | Sweeps the ops queue (wrapping harness's `sweep-chores` via a direct cross-plugin `Skill(harness:sweep-chores)` call, issue #266 — never reimplementing its fan-out), then drives every mobilizable ticket to `build-lead` uniformly — gated by one batched confirm, or unattended via the explicit `auto` token (a `/goal` loop's entry point; ceiling PR-opened, with ADR-0012's one carve-out — a dispatch carrying the explicit `auto-merge: authorized` grant line this step writes AND clearing the full quick-build predicate may land merged; review is never automated). Concurrency per the measured rules: 2+ mutating dispatches always take per-dispatch worktree isolation; a named non-overlapping edit-target path decides parallel-vs-serial, never isolation-vs-none. A named blocker gets a classified breakdown paragraph (six shapes, prose-first, commands on request), never just a table row |
| `skills/bind-build` | Skill-as-command | user-only (`/bind-build`) | Makes THIS session the standing build seat: adopts `agents/build-leader`'s contract directly (the `/bind-team` ↔ `fleet-marshal` pattern) — every ticket id or build ask drives through `dispatch-ticket` via the Skill tool (the engine carries no `context: fork`, so it runs inline in this session's own turn) with the interactive branches ALIVE: the Phase-1 ambiguity question and the task clarify round fire live instead of the unattended blocker/SKIPPED. One engine, three entries: forked one-shot (`/build-feature`), unattended seat (`build-leader`), live standing seat (this). ADR-0020/#525 (closes #523): renamed from `lead-build`, folded into skill-as-command shape — no separate wrapper command |
| `skills/bind-review` | Skill-as-command | user-only (`/bind-review`) | Makes THIS session a standing review seat — now paired with a standing dispatched `agents/review-leader` (closes #433) that runs the same routing table unattended: the estate's eleven fresh-context checkers ARE the review capacity, so the seat (or the agent) routes each target to its owning checker (sealed dispatch, FLOOR/DEEP depth carried, verdict-first relay) and never grades anything itself — dispatch-only IS generator≠critic made structural. Self-authored targets get a NEUTRAL dispatch with authorship disclosed at relay. ADR-0020/#525 (closes #523): renamed from `lead-review`, folded into skill-as-command shape |
| `skills/init-repo` | Command skill | user-only (`/init-repo`) | The `/bind-*` family's composer — one command arms a work session: conditional built-in `/init`, direct fleet-marshal adoption (the session IS the charter — `/bind-team`'s mechanism, carried here because dmi:true blocks Skill-invoking it), the standing INTAKE sibling spawned (docs' intake-leader; its missing-seed return IS the liveness ack, zero contract-bending), and per-ticket build-leader capacity wired (no idle standing build spawn — the seat's own one-ticket contract). Per-session: siblings die with the session; re-run each sit-down |
| `skills/bind-team` | Skill-as-command | user-only (`/bind-team`) | Makes THIS host session adopt `agents/fleet-marshal.md`'s own contract directly for one stated charter — no separate agent spawn, deliberately overrides fleet-rules's solo-first default for the charter's duration; paired with the seat it imports per ADR-0006's species split — command head = mechanic (`/bind-team`), agent = role noun (`fleet-marshal`); like harness's `issue-sorter` pairing, inverted (host adopts, never dispatches). ADR-0020/#525 (closes #523): renamed from `lead-team`, folded into skill-as-command shape |
| `agents/fleet-marshal` | Subagent | dispatch-only | The apex seat: chain-of-command, dispatch order, the review gate between phases, the discovered-reality escalation loop, rollups to the host |
| `agents/planner` | Subagent | dispatch-only | The design seat: decomposes a problem across both planes, authors/maintains PRD/SPEC/LLD/ADR |
| `skills/bind-planning` | Skill-as-command | user-only (`/bind-planning`) | Makes THIS session adopt `agents/planner.md`'s own contract directly for one named planning charter — fifth `/bind-*` member, paired per ADR-0006's species split (command head = mechanic `/bind-planning`, agent = role noun `planner`). Write discipline INVERTS relative to `/bind-team`: authoring the PRD/SPEC/LLD/ADR the charter earns is this seat's own deliverable, so the host writes them directly — but never grades one it wrote: every authored/revised doc rides to `docs:doc-checker` fresh-context, review-by-hand against `doc-writing-rules`' rubric where docs isn't installed. Roll-up audience is the invoking human; closes on a named `loop-rules` decision. Now also paired with a standing dispatched `agents/planning-leader` (closes #433) backing `planner`'s own procedure for unattended dispatch. ADR-0020/#525 (closes #523): renamed from `lead-planning`, folded into skill-as-command shape |
| `agents/builder` | Subagent | dispatch-only | The build seat: implements an approved LLD's build sequence, runs mechanical checks, escalates design conflicts rather than editing the contract |
| `agents/docs-writer` | Subagent | dispatch-only | Owns a documentation site: derives pages from their canonical source, makes drift a failing gate, reports soft drift a static check can't see |
| `agents/code-checker` | Subagent | dispatch-only | Independent critic for one bounded code change, scored against the contract it was built to; generator ≠ critic for the delivery loop |
| `agents/wiring-checker` | Subagent | dispatch-only | Independent critic for how skills/subagents/teams compose and the frontmatter that wires them, scored against `fleet-rules`'s rubric; a real gap closed post-migration (see below) |
| `agents/planning-leader` | Subagent | dispatch-only | NEW (closes #433): standing dispatched form of `planner`'s procedure, pairing with `/bind-planning` the way `build-leader` pairs with `/bind-build` — PENDING the naming-ADR that supersedes ADR-0011 REQ-002's `-agent` suffix rule |
| `agents/review-leader` | Subagent | dispatch-only | NEW (closes #433): standing dispatched form of `bind-review`'s dispatch-to-owning-checker routing table, pairing with `/bind-review` — the family's previously agent-less member now has a standing seat — PENDING the naming-ADR that supersedes ADR-0011 REQ-002's `-agent` suffix rule |
| `agents/product-leader` | Subagent | dispatch-only | NEW HOME (closes #433): moved from `docs/agents/product-leader-agent.md`, dropping the `-agent` suffix, to sit beside the `bind-product` skill it pairs with; docs-plugin preloads degraded to soft named mentions per the hard plugin-boundary rule — PENDING the naming-ADR that supersedes ADR-0011 REQ-002's `-agent` suffix rule |
| `skills/bind-product` | Skill-as-command | user-only (`/bind-product`) | Makes THIS session a dedicated product seat: adopts `agents/product-leader`'s own contract directly — loop authority, spec-lock, IDR/RDD authoring, Verify-stage bug-vs-gap calls, retro, citation-driven escalation. ADR-0020/#525 (closes #523): renamed from `lead-product`, folded into skill-as-command shape |
| `skills/team-scaffolding` | Command skill | user-only (`/team-scaffolding`) | Level 1 of the fleet bootstrap (#404, #410): names the session, walls the reviewer seat structurally, prints the dated seat-tier + comms charter, seeds/updates `.claude/ops/fleet.json` on first join, then adopts the matching `/bind-*`/`/bind-product` contract. Planner and reviewer each carry a standing-order self-check (#410 addendum 3): planner warns (never blocks) when no intent layer exists under `.claude/docs/`; reviewer notices (never blocks) style-review-only until a spec locks |
| `skills/fork-agent` | Skill-as-command | user-only (`/fork-agent {agent-name}`) | ADR-0020 D3/D4 (closes #523): the `fork-` mechanic named as a command — runs one named agent's contract as a `context: fork` off the caller's session, returning only the typed result. Parameterized only, no per-seat aliases |
| `skills/sub-agent` | Skill-as-command | user-only (`/sub-agent {agent-name}`) | ADR-0020 D3/D4 (closes #523): the `sub-` mechanic named as a command — dispatches one named agent unattended via the `Agent` tool. Parameterized only, no per-seat aliases |
| `skills/fleet-bootstrap` | Command skill | user-only (`/fleet-bootstrap`) | Level 2: one terminal cold-starts the whole fleet — adopts orchestrator, dispatches the product seat, HARD-GATES on human ratification of the intent layer (AskUserQuestion; no live user stops and names the pending gate), then spawns an explicit spawn-list of `reviewer`/`planner` as long-lived named background agents (default empty — those two are manually operated). Schema for the shared `.claude/ops/fleet.json` manifest lives in this skill's `references/fleet-manifest-schema.md` |

## Construction note: hard cross-plugin preloads converted to soft mentions

Every one of the five ported agents carried a `skills:` frontmatter preload into skills that no
longer live in this plugin boundary. Fixing this was the bulk of the porting work:

- **`team-lead`** preloaded `write-handoff` (now in harness). Dropped from the
  preload list; the body now soft-mentions harness's `write-handoff` block with an inline
  Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action
  fallback wherever it names a handback. `skills:` is now `[loop-rules, fleet-rules]` —
  the two preloads that are still same-plugin, real preloads.
- **`planner`** preloaded `break-down-problem` (now in harness) plus `prd-author`, `spec-author`,
  `lld-author`, `adr-author` — four names that no longer exist anywhere as skills: docs
  consolidated all four into `doc-writing-rules` plus a `make-doc` drafting command. Every one
  of the six preloads was cross-plugin or stale, so the frontmatter now carries no `skills:` field at
  all; the body soft-mentions harness's `break-down-problem` and docs' `make-doc`
  (`doc-writing-rules`), each with its own inline fallback (the two-plane decomposition method;
  each document type's minimum contract — Problem/Users/Outcomes/Non-goals for a PRD,
  Requirements/Non-goals/Examples/Acceptance for a SPEC, Components/Interfaces/Data/Risks for an LLD,
  Context/Decision/Consequences for an ADR).
- **`builder`** preloaded `lld-author` (stale — same docs consolidation), `break-down-problem`
  and `write-handoff` (both harness). Same fix: no `skills:` field; the body soft-mentions
  docs' `doc-writing-rules` for reading an LLD's shape, harness's `break-down-problem` for
  implementation-level sub-breakdown, and harness's `write-handoff` for the report-out, each with its
  inline fallback.
- **`docs-writer`** and **`code-checker`** each preloaded only `write-handoff` (harness). Same fix:
  no `skills:` field; each body soft-mentions harness's `write-handoff` block with the same inline
  fallback shape.

The pattern throughout: name the cross-plugin skill and use it where installed; otherwise apply its
minimum contract inline. No agent here silently degrades — every fallback is spelled out in the body,
not merely implied. `grill-the-ask`'s own SKILL.md carried the same stale
`prd-author`/`spec-author`/`lld-author` references in its NOT-for clause and output contract; those
were repaired the same way, pointing at docs' `make-doc`/`doc-writing-rules`.

**2026-08-16 (#382): the six hand-copied `write-handoff` fallback blocks became one referenced
copy.** Every agent above (plus `wiring-checker`, ported later) restated the same eight-field
Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next
action shape inline — six independent copies to keep in sync by hand. Since agents can't preload
a harness skill across the plugin boundary (the hard-preload rule above), the fix follows the
same `references/`-file pattern `bind-team`/`bind-planning`/`bind-build` already use for
`adopt-agent-contract.md`: the shape now lives once at
`teamwork/skills/fleet-rules/references/handoff-fallback.md`, and each of the six agent
bodies cites that path (`${CLAUDE_PLUGIN_ROOT}/skills/fleet-rules/references/handoff-fallback.md`)
instead of restating the fields. `write-handoff` itself also gained a precedence rule for which
channel carries the finished block: a sealed, record-first dispatch's dated `## Findings` entry
IS the handoff (no separate mailbox message), while a named teammate-mode seat still sends the
full block to its coordinator — stated once in `write-handoff`'s "Before you hand back" section
and pointed to from `fleet-rules`'s reference table, so no citing agent re-derives it.

`loop-rules/scripts/harness_checks.py` shipped in the source library as a symlink to a sibling
skill (`skill-author`) outside this plugin boundary — a second, quieter instance of the same
cross-boundary problem, this time at the file-path layer rather than the frontmatter layer. It has
been materialized as a real, self-contained copy so the skill's Review step
(`scripts/harness_checks.py goal "<goal text>"`) and its bundled selftest run standalone.

## Evals

Each model-invocable skill ships `evals/evals.json` in this workspace's `{skill, cases:[{id, prompt,
expect}]}` schema (`eval_check.py` E1–E5); the original three converted from the pre-migration
library's `scripts/routing-corpus.json` positives/negatives, `close-session`'s authored fresh at
mint.

Directories align with plugin names (ADR-0007).

## Version ledger

v2.27.0 · 2026-08-18 · closes #675 (Track B, platform resilience): the worktree pin-race mitigation ladder (#490/#609) is now first-class structure instead of hand-carried dispatch-prompt folklore. `dispatch-ticket`'s Phase 3 gains a "mitigation ladder" bullet (new `references/isolation-ladder.md`, F6 split) — for an `Agent`-tool-dispatched builder (`build-leader` and kin), the scratch-clone rung (clone into the session's own scratchpad by absolute path, branch off `origin/main`, push, PR via `gh`) is the DEFAULT isolation choice, not a fallback, since these seats carry no `EnterWorktree` grant at all (confirmed directly, 2026-08-18); the Git-Data-API landing is documented as the RECOVERY rung for work already stranded in a wedged worktree. Both rungs were tonight-proven: PRs #664/#665/#682/#685/#687/#688/#689/#690 via scratch clone, PR #663 via API landing. New minor capability: `scripts/pin_check.py` — a preflight check a builder runs before its first write, comparing the session's actual bound git branch against the ticket's own decided branch name and failing loudly with the ladder's next rung named, rather than letting a write land in the wrong tree; selftest proves the drift/match logic plus the primary-vs-linked-worktree detection against a REAL `git worktree add` fixture, no network. `fleet-rules` Section 6 (pin-race playbook) gains the no-`EnterWorktree`-reach caveat for dispatched seats and cites this ladder's tonight-proven ordering. Two fresh-context `skill-checker` passes (dispatch-ticket, fleet-rules).
v2.26.2 · 2026-08-18 · closes #671 (Track A, teamwork slice; harness slice same PR): `fleet-rules` Part B gains the "who holds the plan" organizing axis (plan holder · worker↔worker comms · file isolation · lifetime, tabled per this estate's eight orchestration archetypes) plus the 6-line topology decision tree, as a design-step aid consulted before Design step 1's job-evidence test — closing the gap `#666`'s rubric X-R4 criterion already cited ahead of this text landing. Harvested substance (never authority) from an external agent-classes doc; cost claims cite `#673`'s own measured gradient, never the source doc's reported folklore figures. Body-only edit, no description/evals change. Fresh-context `skill-checker` pass.
v2.26.1 · 2026-08-18 · closes #670 (teamwork slice, folded with docs/harness siblings in one PR, precedent #639): `dispatch-ticket`'s Phase 4 small-build checker bullet names the fresh-context checker dispatch UNNAMED and synchronous — a named dispatch strands the report (a fix fork's own checker dispatched `chk667` stranded its verdict at the root session, 2026-08-18 — the gh#154/#157 class, re-proven), citing harness's `agent-writing-rules` never-name rule as canon (soft mention, no restatement) — the same discipline the skill's own no-nested-wait preamble already names, now stated explicitly at the checker-dispatch site itself. Body-only edit, no description/evals change. Fresh-context `skill-checker` pass.
v2.26.0 · 2026-08-18 · closes #666 (orchestration-audit campaign, teamwork half; authorkit half same PR): `fleet-rules/references/` gains eight per-archetype orchestration rubrics (A1..A7 seeded verbatim from #666's ratified draft, plus the new A8 `/batch` taxonomy amendment, an A2×A7 hybrid lineage), each falsifiable, evidence-cited, and tagged mechanizable/judgment per criterion; A3 carries priority axis G1 (durable-channel conduct-evidence reader) and A7 carries G2 (the `workflows/*.js` syntax lint tier, realized in authorkit's new `orchestration-audit` instrument rather than a repo-root eslint edit — issue #529's loader meta/body split is incompatible with any single eslint `sourceType`). No new description/evals surface; `references/rubric.md`'s table row extended (not a new row, F6 cap) to point at the eight files. Four #671 canon-adoption citations folded in as new criteria (X-R4, A2-R6/A2-R7, A7-R6/A8-R5) — cited, not restated. Body-only, fresh-context `skill-checker` pass.
v2.25.4 · 2026-08-18 · closes #659 (#655 wave 2, decision 6): `bind-product`'s Phase 1 cold-start pointer names every artifact the flow seeds in a fresh repo, explicitly — a draft brief, the harvest-surfaced draft IDRs, and an empty ROADMAP index — placed per `docs:doc-writing-rules`' own docs-root ruling (issue #514's three-rung ladder) and carrying that skill's `scope:`/`audience:` frontmatter per its per-type grain table and enum, closing the cross-repo seam #652 came through. Body-only edit, no description/evals change; canon stays owned by `doc-writing-rules` (cited, never restated). Fresh-context `skill-checker` pass.
v2.25.3 · 2026-08-18 · closes #658 (#655 wave 2): `dispatch-ticket` cites the owed-chain sizing ladder (canon owned by `docs:doc-writing-rules`) in its sizing phase, plus a new Phase 3.6 spec-lock gate sibling to Phase 3.5 — a Links-cited upstream still pre-lock, or an owed rung with no citation, either yields a named blocker (Phase 1's existing class), never a build. New `references/spec-lock-gate.md` (algorithm + two worked fixtures); two existing Phase 3 bullets split to their own new reference files to hold the F6 body cap. Body-only edit, no description/evals change. Fresh-context `skill-checker`: PASS/ship, 1 major + 1 minor + 1 nit fixed same-change; 1 pre-existing stale cross-plugin citation in `docs:doc-writing-rules` named, deliberately left for a follow-up ticket (out of scope here).
v2.25.2 · 2026-08-18 · closes #667: `build-feature` doctrine drift fixed — its body still taught the pre-gh#541 claim that a `context: fork` skill reaches the live user via `AskUserQuestion` (both the fork preamble and the empty-`$ARGUMENTS` branch), the one forked-intake-archetype member left uncorrected after 2026-08-17's falsification (gh#541, measured two ways). Both passages replaced with the corrected doctrine — clarify pre-fork or fold via `/build-feature <id> <answers>` resume; empty seed → capture-with-gaps close-out naming the unasked question + resume command, `dispatch-ticket`'s own no-live-channel degrade — keeping the siblings' dated record-of-mistake convention. Body-only edit, no description/evals change. Fresh-context `skill-checker` pass.
v2.25.1 · 2026-08-18 · closes #624 (Wave 2; Wave 1 shipped `authorkit:spend-audit` via PR #642): `fleet-rules` Part A §4 and `loop-rules`' hierarchical-budgets bullet each gain a pricing bullet citing idr-0010 (LOCKED) — every recurring firing/loop budget is a spend-ledger row, plus the qualitative WORTH-FIRING test (citing #265's precedent). Body-only edits, no description/evals change; `fleet-rules`' Merge-on-green bullet tightened (deduped against `dispatch-ticket`'s own copy) to hold the F6 500-line body ceiling. Fresh-context `skill-checker` pass on each.
v2.25.0 · 2026-08-18 · closes #637: new command skill `chores-run` arms the recurring "drain the queue and ship PRs" `/goal` loop — writes+commits `.claude/ops/punch-list.md`, then prints (never auto-starts, #421/#423's defect class) an armed `/goal` block whose turn 1 reads `mobilize-chores`' own SKILL.md and carries out its procedure directly, never retypes a command-only command, until 0 punch-list rows read `queued`/`UNMEASURED`; `auto` forwards ADR-0012's carve-out. Named `chores-run`, not the ticket's `drain-queue` lean (unregistered ADR-0011 vocabulary, no live confirm channel — #612/#613 precedent). Two fresh-context `skill-checker` passes (first FAIL/blocking, fixed; second PASS/3 majors, fixed same-change). `scripts/verify_goal_and_punch_list.py` proves the live goal text + punch-list header. No evals (command-only, #601).
v2.24.4 · 2026-08-18 · closes #633 (teamwork slice, docs+harness siblings same PR; renumbered 2.24.3 -> 2.24.4: open PR #638 claims 2.24.3 for this plugin, version_claim_check.py's rebase-and-rebump rule applied — this is the later claimant): `dispatch-ticket`'s Phase 3 VALUE-race bullet gains a companion line — a dispatch minting a new adr/idr/lld/rdd record re-reads the spine's highest id for that family off `origin/main` immediately before numbering it, same discipline as the plugin-version re-read, named after the 2026-08-18 incident where two parallel builds both minted `lld-0011`. Canonical rule stays in `docs:doc-writing-rules`' ID-spine section; `doc_lint.py --spine` (T10) / `docs_check.py`'s R7 catch a miss mechanically, at gate time. No description change, no evals ride-along owed.
v2.24.3 · 2026-08-18 · closes #626 (idr-0011's deferred instrument wave — the first standing
schedule, deferred out of PR #628's docs-only ratification batch per #626's own dated Findings
deferral entry): `fleet-rules` Section 3 gains a bullet naming `.claude/ops/held-items.md`'s new
"Kim's ruling/merge queue" section as the default batching landing spot for a human-gate item,
never a live interrupt, citing `.claude/ops/calendar.md` as the tunable cadence canon rather than
restating cadence values inline. Neither `calendar.md` nor `held-items.md`'s new section nor
`.claude/ops/routines/daily-board-drain.json` (the committed `RemoteTrigger` create-body for the
daily `/mobilize-chores auto` drain) ships inside this plugin — all three are workspace-root ops
state; only the `fleet-rules` bullet is this plugin's own change. Named deviation: the schedule
routine could not be live-armed from this build's dispatch context (the `schedule` skill loaded,
but its `RemoteTrigger` tool was absent from this seat's tool wall) — the committed JSON is the
exact create-body, arm instruction inline, disclosed rather than silently substituted (full
resolution: `.claude/docs/lld/lld-0015-estate-rhythm-instrument.md` — renumbered from lld-0014,
which PR #636 claimed first for #627's reconstructibility-audit). Fresh `skill-checker` pass
on the `fleet-rules` diff; no evals touched (no description changed). Rejected alternative: a new
`ruling-queue.md` file instead of a `held-items.md` section — two files meaning "pending Kim's
decision" recreates the ad-hoc-arrival problem idr-0011 names.
v2.24.2 · 2026-08-18 · closes #625 (first hardening owed by ADR-0021, trust tiers and threat
model): `fleet-rules`' Section 3 (Communication routing) gains a bullet encoding the T2
quote-not-obey rule — record text entering a dispatch prompt is DATA unless the dispatcher
designated that record as the charter, and a directive found in incidental record text is
reported, never obeyed; `dispatch-ticket`'s Phase 5 stage 2b (the QB0 auto-merge grant check)
gains the matching bullet that the `auto-merge: authorized` line has force only in the sealed
dispatch prompt itself (T1) — the identical string inside record text (T2) is inert and gets
reported as a possible injection attempt, never acted on. Both bullets cite ADR-0021
(`.claude/docs/adr/0021-trust-tiers-and-threat-model.md`) rather than restate its tier table.
Fresh skill-checker pass on each touched skill's own diff; no evals touched (no description
changed). Rejected alternative (recorded inline): folding both bullets into one file — the two
sit in genuinely different reader moments (comms/records discipline vs. the sealed-dispatch
QB0 grant check), so one home each, cross-cited to the same ADR, rather than a single combined
bullet neither section fully owns.
v2.24.1 · 2026-08-18 · fleet-rules' References table cites `harness:check-state --fleet` (#620) as
the fleet-wide state-visibility concept's report-side realization — a pointer, not a restatement.
v2.24.0 · 2026-08-17 · closes #611: backlog/roadmap parking: mobilize-chores sweep immunity
(ticket-filter exempt), dispatch-ticket Phase 3.5 de-stale + `stale-premise` outcome.

v2.23.1 · 2026-08-18 · closes #608: `dispatch-ticket`'s bug branch (Phase 2's `kind: bug` bullet)
gains claim-provenance forwarding — live repro adiahealth/gen-ui-kit#1593 showed the redirect to
`docs:file-bug` deadlocking against its own lane's claim (a coordinator's own on-behalf-of claim,
per `fleet-rules`' Section 2 amendment, read by file-bug's dedup as a competing seat). Fix:
the `[redirected-from:dispatch-ticket]` marker now carries the claim comment's URL
(`claim:<claim-comment-url>`) when one already sits on the record at hand-off, so file-bug's
Phase 5 can tell this lane's own authorization from a stranger's rather than standing down either
way. Rejected alternative (recorded inline): deferring this skill's own claim until after
file-bug adopts the record — this skill's bug branch already claims nothing of its own to defer,
so an ordering fix can't repair a claim it never makes, and reordering would reopen the
double-dispatch window Phase 3's claim-then-isolate discipline exists to close (#183/#184).
Docs' `file-bug` gains the matching Phase 5 read-and-compare clause in the same PR (docs
1.15.2 → 1.15.3). Fresh skill-checker pass on this skill's own diff; no evals touched (no
description change).
v2.23.0 · assembled 2026-08-17 · closes #586: orchestrator seat naming converged on ADR-0020's
marshal vocabulary — the session-name convention moves `{repo}-team-lead` → `{repo}-marshal`
across every live canon surface: `fleet-bootstrap` SKILL.md (Phase 1, its 3 print/append sites),
`team-scaffolding` SKILL.md (description + 6 body sites: Phase 1's `Seat:`/tier-justification
lines, Phase 2's session-name print, Phase 4 point 7's introduction target, Phase 6's retire
report), `fleet-manifest-schema.md`'s schema-key/session-name split Field entry, and
`lld-0006-fleet-permission-profile.md`'s D1. `team-scaffolding`'s description changed, so its
`evals.json` n01 case moved from `team-lead` to `marshal` phrasing in the same change (no other
suite carried a reciprocal fence on this term). Repaired the stale rows named in the same
ticket: `.claude/ops/fleet-roster.md`'s two `agent | plugins-agent` rows corrected to
`plugins-marshal` in place (with an explanatory note — these predated even the `#434` convention
correctly, since the printed name was never the bare role token); `.claude/ops/fleet.json`'s
manual-mode `agent` live_state entry had a stray `agent_name: "plugins-agent"` where every sibling
manual entry carries `null` — corrected to `null` to match. `fleet-rules`'s own `team-lead`
mention (the `teammate_id="team-lead"` platform-default citation, `agent-writing-rules`' fact,
unrelated to this seat's own naming) and `handoff-fallback.md`'s historical "six ported agents"
citation are left untouched — neither is this convention. `init-repo`'s "team-lead contract"
phrasing checked and left alone too: it names the still-unrenamed `/bind-team` command, a
different axis ADR-0020 didn't touch. **Role-key migration declined this wave** (ticket's own
open question, builder's call): `fleet.json`'s schema key stays `agent` — not cheap, since it's a
live data field multiple sweepable-invariant greps and (potentially) other repos' own fleet.json
copies key on, with no cross-repo migration path this ticket's blast radius enumerated; the
split stays as designed, only the printed name's vocabulary moved. Fresh-context `skill-checker`
FLOOR pass on both edited skills: PASS.
v2.22.4 · assembled 2026-08-17 · closes #592: fleet-rules SKILL §4 (version-slot + merge-order
rules) gains the missing inverse rule — the shared primary checkout stays on `main`, always;
feature branches belong in worktrees. ADR-0002 states the forward half (a campaign gets its own
branch + worktree) but never the inverse, and the gap let a live incident bite: a session checked
out `fix/harness-ops-rulings` on the primary checkout while peers were live, stranding a
concurrent peer's ops commit (9e115cd) on that feature branch instead of `main`. Placed in §4
(shared-tree write discipline), not §1 (coordination scope/polling authority), per a
fresh-context skill-checker's major finding on the first draft. Optional repo-cleaner
inventory-flag piece deliberately not folded in here — left for its own ticket, out of this
small-sized ticket's scope. The #585 cross-reference in the seed didn't hold up on
verification: #585 is currently a decision-watcher no-op-firing ticket, unrelated to this
incident.
v2.22.3 · assembled 2026-08-17 · closes #588: fleet-rules SKILL §2 (work-claim protocol) gains
the claim-provenance wording rule — a coordinator's claim posted on behalf of a dispatch names
the dispatched builder, with a worked example line, closing the #542 abandoned-pre-claim
incident class (corrected wording already proven on #568, #577, #581).
v2.22.2 · assembled 2026-08-17 · #581: parallel-work-rules t10 ("design a protocol for running several Claude Code terminals against one repo") stopped losing to grill-the-ask — description gains the phrasing verbatim plus a named fence, grill-the-ask gains the reciprocal n09. fleet-rules gains NOT-fences for write-handoff and break-down-problem, closing n17/n18 as real tunes; n07/n16 confirmed as a genuine cross-plugin structural leak (true owner absent from a teamwork-scoped menu) and accepted with dated notes; t17/t18 re-judged as single-judge noise via the contested-vote round, not a regression.
v2.22.1 · assembled 2026-08-17 · fleet-rules SKILL §2 gains the guard-skipping-peer claim bullet; parallel-work-rules unattended-collision §2 gains the agent-ui #1150/PR #1161 checkout-time-self-detect instance.
v2.22.0 · assembled 2026-08-17 · closes #558: `mobilize-chores` now works the stuck set instead of
only reporting it. Root cause: step 2's `Blocked-by:` exclusion (#193) was a hard skip with no
executed follow-through — a per-shape proposed action in step 6 that was never acted on, even when
a blocker was itself a plainly mobilizable ticket. New reference file
`references/unstick-ordering.md` carries the fix as buildable prose (LLD `lld-0007`): a fail-closed
B0–B5 classification (CLOSED / UNRESOLVABLE / CYCLE-or-too-deep(depth cap 5) / IN-FLIGHT /
HUMAN-SHAPE / MOBILIZABLE) resolved depth-first per candidate with cycle detection and an in-run
memo cache, ordered dependency-first; only a B5 (fully mobilizable) blocker ever dispatches — every
other class stays report-only, by construction. Within-run chaining is bounded, never a wait: after
a wave's dispatches return, one read-only re-check of each sequenced dependent's blockers (never a
`gh pr checks --watch` or a sleep), all-CLOSED unlocking the next wave, max 3 waves — which on the
default PR-opened ceiling degrades to next-run-only unless an ADR-0012 quick-build merge closed a
blocker in-run. `blocked-by-convention.md` stays the one format canon (only its consumer-pointer
line changed); SKILL.md gained the unstick clause in its description, step 2's exclusion paragraph,
step 3's stop condition, one second listed section inside step 4's SAME single confirm round (a
chain confirms/declines as a whole — no second `AskUserQuestion` round, ever), step 5's wave
re-check paragraph (explicit: a chain member's dispatch carries no extra auto-merge authority —
`dispatch-ticket` stage 2b evaluates it exactly like any other ticket), step 6's three-way outcome
vocabulary (`unstuck-this-run` / `sequenced-for-next-run` / `still-stuck-and-why`), and matching
Failure-branch/Done-when extensions. The skill gains exactly ONE new verb (dispatch the mobilizable
blocker) — never a `Blocked-by:` line edit, a relabel, a claim-reclaim, or a ratify comment; those
stay human acts or `repo-cleaner`'s own territory (Rejected alternatives RA1–RA4 in the LLD). No
ADR: no cross-consumer contract changed (`blocked-by-convention.md`'s format/realization/non-goals
are untouched; `chore-planner`'s own ordering in harness's `blocked-by-rules` is unaffected).
`release_gate.py teamwork` exit 0; `/check-routing teamwork` shows no boundary regression from the
description-clause edit (mobilize-chores is `disable-model-invocation: true`, so no `evals.json` is
owed). Fresh-context `teamwork:code-checker` reviewed the semantic edits (SKILL.md body,
`unstick-ordering.md`, the convention file's pointer line) before merge, per the plugin-authoring
semantic-edit invariant (PASS, 0 blocker/major, 2 minor fixed in this same diff — verdict recorded on the PR and the issue Findings).

v2.21.7 · assembled 2026-08-17 · closes #577: fleet-marshal charter/role-name mismatch fixed.
Root cause: ADR-0020 Wave 3 (#521) renamed `team-leader`→`fleet-marshal` as a pure data-only edit
— the agent body still carried team-leader's single-team plan→build→review charter, and no
doctrine gave the orchestrator seat a route-anything-incoming protocol. Both surfaces landed in
one change: (a) `agents/fleet-marshal.md` rewritten into a fleet-command charter — STRICT ROUTER,
NEVER BUILDS enforcement (routes every incoming item — raw ask, bug/feature/task report, handback,
peer message — to its owning seat/skill/door within one turn, no small-fix latitude), chain-of-
command across parallel sessions, overdue-handback chasing, and fleet-scope budget/rollup
discipline — trimmed to a thin shell citing (b) `fleet-rules`' new Section 7
("Route-anything-incoming protocol": triage-within-one-turn, a 6-step routing precedence table,
escalation) rather than duplicating it, keeping the agent body under the thin-shell line cap. Part
B's three sections renumbered 7/8/9 → 8/9/10 to make room (Sections 1–6's own numbers, and every
external citation to "Section 3", stayed untouched — only Part B's outer numbers moved, `Design
step N`/`Part B` citations elsewhere are number-independent so nothing else broke). `fleet-bootstrap`
Phase 1 gained a one-line pointer to Section 7 (cite, don't restate). `/bind-team`'s Phase 2 gloss
of the agent's Priorities 1–8 updated to match, and both files now cross-cite `fleet-rules`' "Seat-
access doors" section explicitly — the agent file (door 3, dispatched) and `/bind-team` (door 1,
host-adopted) state they describe one discipline, not two. `fleet-rules`' description gained
"incoming-item triage" (kept ≤700 chars); `evals/evals.json` gained 3 positive cases (t23–t25) and
1 reciprocal negative fence against docs' `file-bug` (cross-plugin — filing the record is never
this skill's job). Fresh-context `harness:agent-checker` (fleet-marshal.md) found 3 majors — banned
persona opener (converted to third person), `/bind-team`'s Phase 2 contradicting Section 7's own
"binds both doors" claim (carved out explicitly), and a missing teammate-mode delivery clause /
`team-lead` identity caveat (added, plus a `SendMessage` tool grant) — all three fixed, plus 2
minors (tool-wall overstatement reworded to by-rule; `effort: xhigh`→`high` per the
orchestration-coordinator seat-ladder default). `harness:skill-checker` (fleet-rules) passed clean,
naming one owed proof: `/check-routing teamwork` on the description boundary change. That run
followed: fleet-rules' own 45-case suite and the two siblings carrying a reciprocal
`fleet-rules`/`NOT`-fence (loop-rules, parallel-work-rules) all dispatched to independent blind
`routing-judge`s, contested cases taken to a 3-judge majority vote — fleet-rules 45/45 pass
(t16/t20 needed the vote, 2-of-3 fleet-rules each; n07/n16/n17/n18 are the same pre-existing
cross-plugin structural leak n16 already carries as an accepted class — the true owner isn't in a
single-plugin menu, unrelated to this diff), loop-rules 25/25 clean, parallel-work-rules 22/23
(t10 "design a protocol for running several Claude Code terminals" loses 3-of-3 to grill-the-ask —
pre-existing, neither skill touched by this PR, filed as a follow-up rather than blocking here).
`release_gate.py teamwork` clean (1 pre-existing G8 warn, unrelated phantom-handle-shaped prose).

v2.21.6 · assembled 2026-08-17 · closes #574: `bind-team`, `bind-planning`, and `bind-product`
each defaulted a blank invocation instead of erroring — Phase 1 in all three now binds a default
charter on `$ARGUMENTS` blank ("adopt against cwd, hold for the first unit of work fed in"),
consistent with the sibling binds (`bind-build`/`bind-review`/docs' `bind-intake`, which already
default a blank seed to cwd). The corresponding "Invoked with no `$ARGUMENTS`" failure branch —
now the ordinary Phase 1 default path, not a failure — was removed from each. Descriptions and
argument-hints updated to state the default; `evals/evals.json` gained a blank-invocation trigger
case for `bind-team`/`bind-product` (`bind-planning` already carried one). ADR-0020 does not fix
the non-blank-charter requirement anywhere in its own text (checked in full: it rules the fleet
vocabulary and the `bind-`/`fork-`/`sub-` command heads, not per-seat blank-invocation behavior) —
no ADR amendment or dated note was needed; the requirement lived only in each skill's own prose,
edited directly. Fresh-context `wording-checker` pass rode the semantic edit (three SKILL.md
bodies): 1 major (bind-product's re-binding line pointed at "Phase 2" instead of "Phase 3" —
fixed) and 3 minor (redundant "instead of erroring" phrasing on a routing surface, and the
NEVER-prohibition-budget nudge from "never receives work" — both reworded across all three
files). Re-run after fixes: clean. `release_gate.py teamwork` clean.

v2.21.5 · assembled 2026-08-17 · (closes #554): `dispatch-ticket`'s no-nested-wait section
corrected — its prose claimed an unnamed `Agent`-tool critic dispatch's synchronous tool-result
was always the return value, "no separate signal will ever reach you." PR #547's fold observed a
real counter-case: a fresh-context critic dispatch ran ASYNC and its all-PASS verdict arrived as a
background task notification to the dispatching session instead. Added a dated correction
paragraph plus a caveat inline at the earlier absolute claim: an async, notification-routed
completion is a second valid path for an unnamed dispatch, not a stall and not grounds to
re-dispatch — a seat now accepts whichever of the two (synchronous return or task notification)
arrives first and reports it onward, escalating only when neither arrives within roughly 10
minutes or the dispatch's own stated budget. Rebased onto the ADR-0020 wave chain (through #551);
integrated cleanly against the renamed `/bind-build` surface with no further wording changes
needed. Prose-only; fresh-context skill-checker pass rode the edit. `release_gate.py teamwork`
clean.

v2.21.4 · assembled 2026-08-17 · closes #551: two follow-ups from the wave-5 rename campaign.
(1) `bind-product` (formerly `leading-product`, renamed under ADR-0020 W5) had two pre-existing
leaked no-trigger cases (n02 "gate this build dispatch" → was winning over its true owner
`bind-team`; n03 "what lifecycle stage" → was winning over `none`/`docs:check-stage`) — fixed by
narrowing the description's positive clause (dropped the bare words "gate" and "driving
docs:check-stage" that the leaks keyed on) and sharpening the NOT-fences; also repaired a stale
Phase 2 citation claiming product-leader.md records a dated seat-tier "deviation" for itself when
the agent file actually says the opposite (no deviation — it's the ladder's own default ceiling).
A 5th trigger case (t05) added to clear the E5 floor. Fresh blind routing re-proof: 10/10 clean,
n02/n03 now route to their true owners. Fresh-context skill-checker: PASS. (2) Merge-on-green
tooling defect, repeatedly bitten (#530, #546, #549 all raced it): `gh pr checks --watch
--fail-fast` was found to exit 0 on non-terminal/failed states, so a chained `&& gh pr merge`
could fire on a red or still-running PR. `dispatch-ticket`'s quick-build merge sequence gains
step 1b — a mandatory `gh api .../check-runs` sweep verifying every check's own `conclusion`
individually before merge, exit 0 from the watch demoted to advisory-only. `fleet-rules`' merge
choreography section gains the matching doctrine bullet, citing dispatch-ticket rather than
re-deriving it. `harness:merge_when_clean.py` was checked and found already immune (it polls
`gh pr view`'s `mergeStateStatus`, never `gh pr checks --watch`) — no script change needed there.
(3) Folded in per Kim's request before merge: W6's routing report (#565/#524) flagged one
marginal single-judge steal in the merged fleet-rules suite. Traced it to t03's own wording —
"what should I check on a ticket before I dispatch a build for it" reads as `dispatch-ticket`'s
domain, not fleet-rules' claim-then-guard protocol — confirmed 3-of-3 across a vote round, so a
real case defect, not noise. The eval case was wrong, not the description: reworded t03 to key
on fleet-rules' own claim-then-guard vocabulary instead. Fresh full 41-case re-proof: 41/41 clean.

v2.21.3 · assembled 2026-08-17 · closes #548: `dispatch-ticket`'s Phase 1 ambiguous-match failure
branch and the `[nested-intake]` marker rationale still carried the falsified 2026-08-09 canon
("forking relieves the caller's session, it does not remove the person, and `AskUserQuestion`
still reaches them directly") — measured false by gh#541 (a `context: fork` background dispatch
has no question channel at all). Rewritten to the capture-with-gaps + named-blocker shape docs'
`file-bug`/`file-feature` (PR #546) already landed: only `/bind-build`'s own standing seat (the
live host session, never forked) gets a real `AskUserQuestion`; `/build-feature`'s fork,
`build-leader`, and `mobilize-chores` all report the ambiguity as a named blocker naming both
candidate ids plus the resume path (re-invoke with the explicit id). The `[nested-intake]` marker
note corrected the same way — its rationale no longer claims a live round budget that never
existed past this point. Fresh-context skill-checker pass: PASS. `release_gate.py teamwork`
clean. No evals touched (description unchanged). Companion docs-half PR: #549.

v2.21.2 · assembled 2026-08-17 · closes #539: `fleet-rules` §3 (Communication routing) gains a
duty-report/work-order guarantee bullet, placed right after the "one decision, one channel"
bullet — every seat's duty report (or done/what's-next report) to the coordinator now must get
back one of three named shapes: an immediate assignment, an explicit QUEUED assignment naming
both the slice and its trigger condition, or an explicit empty-queue statement plus the next
check-in condition. A bare "hold idle"/"stand by" with no named slice or trigger is ruled out.
Minted from a 2026-08-17 incident: a fresh seat reported in, the queue was drained, and the seat
sat in an unstructured holding pattern for several message rounds before a queued-slice promise
finally emerged. Fresh-context skill-checker pass (FLOOR): PASS with one minor fixed pre-ship (the
bullet's original "always one of two shapes" self-contradicted its own third, empty-queue arm —
reworded to one three-arm enumeration) and one nit fixed ("marshal/coordinator" → "coordinator",
matching the file's established vocabulary). No evals change (description untouched).

v2.21.1 · assembled 2026-08-17 · closes #543: the gen-ui-kit CLI-tier fleet-ops harvest
(agent-ui#1115, comment 5317746661, 25 claim·evidence·date·confidence lessons) folds into its
actual owning doctrine, `fleet-rules` and `parallel-work-rules`, now that #524/D5 (above) has
settled the post-merge section layout this ticket was queued behind. `fleet-rules` gains: §1 a
two-host ratified-lane-split bullet (lesson 12); §2 a remote-absence-never-proves-stale
refinement (lesson 8); §3 a dead-mailbox-not-dead-agent bullet (lesson 9) and a
ruling-scoped-to-its-utterance bullet (lesson 15); §4 a hot-shared-file merge-then-rebase-next
nuance (lesson 6), a derived/generated-artifact merge-marshal-and-class-split cluster (lessons
1–3, 5, citing this workspace's own `dist/` as an existing Class-C instance), a
credentialed-steps-don't-run-in-seats bullet (lesson 19), and a worktree-installer-shapes-bytes
citation into `harness:big-change-git-rules` (lesson 18); §5 a peer-worktree-hygiene bullet, a
caffeinate/keep-awake bullet (lesson 22), and a fleet-ledger-anatomy elaboration (lesson 25);
Part B Design step 1 a worked release-authorization precedent for the solo-first default (lesson
14). `parallel-work-rules` gains one Decide-step-2 bullet: a pinned host poisons its plain-Bash
subagents, `isolation:"worktree"` is the fix (lesson 11). **Skipped by name as already covered,
no re-fold**: lesson 4 (regen-bot force-rebuild) and lesson 17 (isolation-worktree bootstrap) by
`dispatch-ticket`'s own VALUE-race/bootstrap-on-isolation mechanics (cited from fleet-rules §4);
lesson 7 by §4's own serialize-vs-parallelize + Part B Design step 5's disjoint-fan-out default;
lesson 10 by `dispatch-ticket` Phase 3's re-read-before-proceeding tie-break (cited from §2);
lesson 13 by this workspace's own ADR-0002/CLAUDE.md ticket-routing invariant; lesson 16 by
`.claude/rules/docs-mutability.md`'s accepted-ADR append-only rule; lesson 20 by
`harness:checks-that-bite`'s pre-PR-gate-with-auto-fix domain; lesson 21 by
`harness:flaky-gates`'s contention-vs-regression doctrine; lessons 23–24 by `dispatch-ticket`
Phase 5 stage 2b's verify-merge-by-state and mandatory Findings write-back (both already cited
from fleet-rules). The agent-ui#1115 "Scope-conformant revision v2" Excluded-list's own 7
whole-lesson + 3 split-dev-half items (relayed onto #543 as a second input source) are disposed
the same way: the worktree/branch peer-hygiene item folds alongside lesson 25 above; "seats never
merge, one host verifies serially" and "owner rulings park as affordances" skip as already
covered by ADR-0002/§3's one-decision-one-channel section respectively; "red gates under fleet
load aren't evidence," "hooks are a separate enforcement layer," and "generator≠critic as
residency law" skip as already covered by `harness:flaky-gates`, `harness:hook-writing-rules`,
and this estate's own generator-≠-critic invariant (`.claude/rules/plugin-authoring.md`) in turn;
the 3 split dev-side halves (a daily zero-SDK grep gate, a repo-internal dev-proxy trip-wire, a
prompt-drift/equivalence CI gate) are gen-ui-kit product-plumbing specific enough that they don't
generalize into this estate's CLI-harness doctrine — noted, not forced into a fold. Full
disposition table lives in #543's Findings. `harness/scripts/release_gate.py teamwork` green.
v2.21.0 · assembled 2026-08-17 · ADR-0020 wave 6 (closes #524, D5): `team-or-solo-rules` merges
into `fleet-rules` — the widest single-name blast radius in the estate (116 hits / 54 files).
`fleet-rules` keeps its name and both preload edges (`fleet-marshal`, `wiring-checker`); its
SKILL.md gains a Part A (unchanged fleet-ops protocol) / Part B (composition & wiring design,
folded verbatim from `team-or-solo-rules`) split, one merged description (~700 chars, down from
~1100 summed — net rent win per D5's recorded check), one merged `evals/evals.json` (22→41 cases,
self-fencing negatives dropped as now-internal). `references/{best-practices,foundations,
handoff-fallback,rubric}.md` moved from `team-or-solo-rules/references/` into `fleet-rules/
references/`; the retired skill directory relocated to `.refactor-attic/20260817T185430Z/
team-or-solo-rules/` (undo, not deletion — reshape-skill's own convention). Every live citer
repointed: `fleet-marshal`/`planning-leader`/`wiring-checker` `skills:` preloads (now
`[loop-rules, fleet-rules]` / `[fleet-rules]` / `[fleet-rules]`); the four agents citing the
`${CLAUDE_PLUGIN_ROOT}/skills/.../handoff-fallback.md` hard path (`builder`, `code-checker`,
`docs-writer`, `planner`); `dispatch-ticket`, `parallel-work-rules`, `loop-rules`, `bind-team`,
`init-repo`, `team-scaffolding` SKILL.md bodies and NOT-fences; six `evals/evals.json` sibling-fence
comments (`dispatch-ticket`, `team-scaffolding`, `fleet-bootstrap`, `bind-team`, `loop-rules`,
`parallel-work-rules`). `bind-team`'s Phase 2 step 2 got a real content fix, not just a rename:
`fleet-marshal` now preloads only two skills post-merge, so the old "two of the three, deliberately
not re-invoking fleet-rules" reasoning no longer parses — rewritten to name `fleet-rules`' Part B
as the operative half for a single-host charter, Part A as the one that doesn't bind. Historical
records left untouched per the append-only convention: `doctrine.manifest.json` D07 gets a dated
amendment (canon_file repointed) rather than a rewrite; dated ops reports, handoff docs, ADR-0014/
ADR-0020, `authorkit/renames.json`'s ADR-0006-era ledger, and prior ledger lines/`intent.md`/
`audit-report*.md` narratives are left verbatim.

v2.20.0 · assembled 2026-08-17 · ADR-0020 wave 5 (closes #523; teamwork slice of #525's
skill-as-command ruling): the five `commands/lead-*.md` wrapper commands (`lead-team`,
`lead-build`, `lead-planning`, `lead-product`, `lead-review`) are deleted outright — per #525's
ruling (skill-as-command is the successor shape, convert all, no grandfathering), each wrapped
skill folds the command into itself instead of gaining a renamed wrapper: `fleet-orchestration` →
`bind-team`, `leading-builds` → `bind-build`, `leading-planning` → `bind-planning`,
`leading-product` → `bind-product`, `leading-review` → `bind-review`, each now carrying
`disable-model-invocation: true` / `user-invocable: true` directly with no separate wrapper file.
Two new parameterized-only commands mint per ADR-0020 D3/D4: `skills/fork-agent`
(`context: fork`, one named agent's contract off-session) and `skills/sub-agent` (`Agent`-tool
dispatch of one named agent) — neither takes per-seat aliases. `evals/evals.json` updated in the
same change for all five renamed skills plus the two new ones; every live citer across
`build-feature`, `dispatch-ticket`, `fleet-bootstrap`, `init-repo`, `team-or-solo-rules`,
`team-scaffolding`, and the four dispatched-twin agents (`planning-leader`, `product-leader`,
`review-leader`, `build-leader`) repointed in the same change. docs' `lead-intake` is the sixth
`/lead-*` surface the ADR names but sits in a separate plugin — per #523's own scope note
("split it into its own sub-wave so each PR stays inside one plugin") it rides a companion PR,
not this one. `authorkit/skills/naming-audit/scripts/validate.py`'s `LEAD_HEAD_GRANDFATHER`
constant and its fixtures are retired in the same campaign (authorkit version bump, its own
ledger line) now that no live surface needs grandfathering.

v2.19.0 · assembled 2026-08-17 · ADR-0020 wave 4 (closes #522): `skills/leading-teams/` renamed
`skills/fleet-orchestration/` (frontmatter `name: fleet-orchestration`, title heading matched),
proving the `{object}-{process}` skill production for `orchestration` now that it's registered in
the root `naming.manifest.json`'s ProcessLex (wave 1, #519). Its two `references/` files
(`adopt-agent-contract.md`, `dispatched-agent-report-delivery.md`) and `evals/evals.json` moved
with the directory unchanged in content, save internal self-citations of the old skill name.
Every live invocation string repointed in the same change: `commands/lead-team.md`'s `wraps:`/
`requires:` (the command itself keeps its own name and `/lead-team` invocation — wave 5, #523,
converts that surface); the four `*-leader` twins' (`build-leader`, `planning-leader`,
`product-leader`, `review-leader`) citations of the shared `references/` files; `fleet-bootstrap`,
`team-scaffolding`, `leading-builds`, `leading-planning`, `leading-product`, `leading-review`'s
prose/path mentions and `evals/evals.json` no-trigger-owner comments; `doctrine.manifest.json`'s
D02 dependent path (appended a dated amendment note rather than rewritten — the accepted-ADR-
adjacent append-only convention); and harness's `estate-rename-map.md` paradigm-name table.
Historical ledger rows, dated audit reports, and ADR-0020/spec-naming-convention.md's own
wave-4 citations are left untouched by design — they record what was true at the time, not a
live pointer. `check-routing` on the renamed suite: clean, no new stolen/leaked/dead cases.
`naming-audit --scope grammar`: 0 errors (`fleet-orchestration` parses under `{object}-{process}`,
`fleet` in ObjectVocab, `orchestration` in ProcessLex per wave 1); full-scope structural findings
unchanged before/after (380, all pre-existing, none grammar). `release_gate.py teamwork` CLEAN.

v2.18.0 · assembled 2026-08-17 · ADR-0020 wave 3 (closes #521): `agents/team-leader.md` renamed
`agents/fleet-marshal.md` (frontmatter `name: fleet-marshal`), proving the `{scope}-{role}`
production end to end now that `marshal` is registered in the root `naming.manifest.json`'s
RoleLex (wave 1, #519) and `validate.py` carries the `bind-`/`fork-`/`sub-` heads with `lead-`
retired (wave 2, #520). Every live invocation string repointed in the same change: the
`agents/team-leader` construction-note/README rows, `doctrine.manifest.json`'s three
team-leader-citing edges (D04/D05/D08, each appended a dated amendment note rather than rewritten
— the accepted-ADR-adjacent append-only convention), `product-leader.md`'s four `team-leader`
mentions, the `leading-teams`/`leading-builds`/`leading-planning`/`leading-product` skills' shared
`` `/lead-team` ↔ `team-leader` `` pattern citation (now `fleet-marshal`), `init-repo`'s
`agents/team-leader.md` read-path, and `leading-teams`'s own description plus its two shared
`references/` files (`adopt-agent-contract.md`, `dispatched-agent-report-delivery.md`). Same-change
`evals/evals.json` update on `leading-teams` (t02/n05 reworded to the new agent name). The
`{repo}-team-lead` fleet SESSION-naming convention (`fleet-bootstrap`/`team-scaffolding`,
`fleet-roster.md`) is deliberately left untouched — lld-0006 D1 already decouples the
schema-stable `agent` role key and its printed `{repo}-team-lead` session name from the agent
DEFINITION file's own name, and ADR-0020's D1 only renames the latter. Historical ledger rows and
ADR/spec citations of `team-leader` as a past-tense fact are left as-is (append-only convention);
authorkit's `GRAMMAR.md`/`validate.py`/spec-naming-convention.md's own `team-leader` grammar
EXAMPLES are out of this wave's scope (grammar-layer work landed in wave 1/2, #519/#520) · v2.17.14
· assembled 2026-08-17 · `fleet-rules` gains a "One decision, one channel" rule in its
Communication routing section (closes #535): three clauses — one channel per user-decision; a
seat discovering the same decision pending elsewhere STOPS and routes to the first asker instead
of re-asking; a ruling is superseded only by an explicit later ruling naming the earlier one,
never by a parallel answer. Minted from the 2026-08-17 crossed-ruling evidence in #518 —
ADR-0020 rejected in one session at 16:03 and ratified in a parallel session one minute later at
16:04, requiring a consolidated tie-break round to repair. Prose-only addition to
`fleet-rules/SKILL.md`'s body (no description/frontmatter change, no evals churn — the routing
surface didn't move). Sequencing: lands before ADR-0020's own wave-3+ teamwork churn continues;
wave 6 (the `team-or-solo-rules` → `fleet-rules` merge) inherits this section verbatim · v2.17.13 · assembled 2026-08-17 · desk→seat terminology sweep (closes #517): `review desk`/`the
desk` reworded to `review seat`/`the seat` across README's own table row, `review-leader.md`,
`lead-review.md`, `fleet-rules/SKILL.md`, `leading-review/SKILL.md`, its `intent.md`, and
`evals/assertions.md` — landing wave 7's already-executed rewording (ADR-0020 REJECTED the
broader `marshal`/bind-/fork-/sub- rename campaign, gh#518; this sweep's own routing gates
were the only obligation the ADR carried forward, not the rename). Deliberately left untouched:
`leading-review/evals/evals.json`'s and `fleet-rules/evals/evals.json`'s "desk" test prompts
(synonym coverage — proving the skill still triggers on the pre-rename word a user might still
say) and `leading-review/evals/audit-report.md` / `behavior-check.md` (dated 2026-08-10 point-in-
time records quoting then-current line numbers; rewording them would falsify history, not fix
staleness) · v2.17.10 · assembled 2026-08-17 · `dispatch-ticket` Phase 3's isolate bullet names the

v2.17.12 · assembled 2026-08-17 · `team-or-solo-rules` gains a "Seat-access doors" section (closes
#531) documenting the three structurally different ways a caller reaches a standing seat's
contract — session adoption (`/lead-*` + `leading-*`), `context: fork` execution, and `Agent`-tool
dispatch via a `*-leader` agent — citing issue #134/#135 (a `disable-model-invocation: true`
command is unreachable via the `Skill` tool or an agent's `skills:` preload) as the mechanical
reason all three doors exist, and naming the `*-leader` twin rationale this forces. Prose only,
per the ticket's own non-goal: no rename, no bind-/fork-/sub- head coinage, no marshal vocabulary,
grammar untouched. Rejected ADR-0020 (gh#518) is this section's surviving insight, not a grammar
change. Body-only edit (no description/frontmatter change) to `team-or-solo-rules/SKILL.md`.
Version-slot note: this branch was cut when `main` was 2.17.10; PR #532 held an open claim on
2.17.11 (`worktree-land-desk-seat-sweep-517`, desk→seat terminology sweep) — bumped to 2.17.12 to
sequence behind it rather than race the same slot (`version_claim_check.py` V1/V2).
v2.17.10 · assembled 2026-08-17 · `dispatch-ticket` Phase 3's isolate bullet names the
bootstrap-on-isolation step at its own call site (closes #498, gen-ui-kit gh#1389 residual): the
moment a fresh worktree is created, feature-detect and run the host repo's
`scripts/dev/bootstrap-worktree.mjs` (or its declared equivalent) before trusting any gate/check
run inside it — full mechanics and rationale live in harness's `big-change-git-rules` (`worktree-mechanics.md`, harness 3.8.31), this is the pointer at the build path's own creation site.
v2.17.9 · assembled 2026-08-17 · `dispatch-ticket` gate-run time budget (gh#1485, adiahealth/
gen-ui-kit): Phase 5 stage 2's local gate-aggregate run (`npm run check` or the host repo's own
equivalent) now runs under the same feature-detected 900s wrapper as stage 2b's CI-watch
(`timeout`/`gtimeout`/perl-alarm fallback), defaulting to ~15 minutes and overridable by the
dispatch prompt. On exhaustion the seat records which gates already passed, names the aggregate
partially-run in Findings, and proceeds to PR-open — CI authoritative, a timeout read as a
`flaky-gates` contention verdict, never an implicit pass. Closes the gap that let build-leader
seats grind the aggregate indefinitely under host load (measured: a 4h no-progress seat, a
second killed by the stream watchdog at 600s). Version-slot note: this branch was cut when
`main` was 2.17.7 and PR #499 held an open claim on 2.17.8 — bumped to 2.17.9 to sequence behind
it rather than race the same slot (`version_claim_check.py` V1). #499 merged mid-build (`main`
is now 2.17.8); re-checked via a fresh `origin/main` re-read (the VALUE race, #445) — 2.17.9
still clears cleanly against 2.17.8, no rebump needed, rebased onto `main` to resolve the
resulting `plugin.json`/ledger conflict.

v2.17.8 · assembled 2026-08-17 · new pack `fleet-rules` (closes #480, #373 overnight-campaign
evidence): default operating protocol every orchestration-adjacent teamwork skill/agent starts
from instead of re-deriving mid-run — coordination scope ladder (fleet-scoped only, status-only
replies to same-user other-repo seats, true-global only on explicit instruction), the
claim-then-guard sequence before dispatching (ADR-0005 claim + mobilize-chores' four-layer
double-dispatch guard, cited not restated), report-supersedes-nudge communication routing,
one-version-bumping-build-per-plugin + stacked-PR merge-order rules, session-death resilience
(orphaned-claim reset, resumable worktree/branch naming), and the `EnterWorktree` pin-race unblock
playbook. Placement resolved on evidence rather than left open: a NEW pack, not a
`parallel-work-rules` extension — only one of the six areas (pin-race) nests inside that skill's
own git-tree-isolation/collision plane; the other five (scope ladder, claim/guard, comms routing,
version-slot, session-death) are cross-cutting orchestration default with no single existing
canonical home, scattered across `team-scaffolding`/`fleet-bootstrap`'s inline phases and this
workspace's own incident history instead — cramming them into `parallel-work-rules` would have
broken that skill's own stated plane separation (NOT dispatch shape, NOT next-turn timing) for a
net five-sixths mismatch. Reciprocal NOT-clause fences added to `team-or-solo-rules` and
`parallel-work-rules` (both this plugin, evals.json cases added on both sides); a body-only
cross-plugin citation added to harness's `agent-writing-rules` (its own authoring-mechanics scope
left untouched — no description/evals change there); `fleet-rules` preloaded into `team-leader`
and `build-leader`'s `skills:` lists with a body citation at each seat's own durable-state/claim
priority. Version-slot renumbered TWICE, both caught live (this pack's own §4 subject matter,
first-hand): dispatched to number from 2.17.7 on the expectation that open `PR #487` would land
2.17.6 first — it merged 2.17.6 to `main` mid-build (confirmed via a fresh
`version_claim_check.py` + an `origin/main` re-read; 2.17.7 still cleared cleanly, no rebump
needed at that point); a fleet coordinator then flagged a second collision in flight — sibling
`PR #495` (S8 lexicon) held a now-stale 2.17.6 claim (`version_claim_check.py` V2, verified
independently before acting on the coordinator's message) that would rebump to 2.17.7 and merge
first — so this build took the coordinator's explicit hand-assigned slot and renumbered to
2.17.8, the exact per-plugin version-slot discipline §4 documents, demonstrated on itself.
Fresh-context `skill-checker`/`agent-checker` passes before merge (no model override, per
plugin-authoring's semantic-edit invariant) — skill-checker's two MINOR findings (§2's guard
detail and §4's own merge-order sequence both drifted toward restating their cited owner files)
fixed by trimming to citation + one-line rule; `release_gate.py teamwork` result recorded in the
PR body ·

v2.17.7 · assembled 2026-08-17 · issue #477 sibling reference fix (docs' S8 lexicon amendment, ADR-0017/ADR-0018): `docs' intake-lead` renamed `docs' intake-leader` in `init-repo`'s SKILL.md dispatch step, README's live table row, and its own eval assertion — the docs-side agent rename's cross-plugin mention, updated in the same PR since preloads/dispatches are hard plugin boundaries, mentions are soft but still get fixed when the target renames. No behavior change; the dispatched Agent tool call already used the string literal

v2.17.6 · assembled 2026-08-17 · leading-product Phase 2 repointed at the same-plugin
`${CLAUDE_PLUGIN_ROOT}/agents/product-leader.md` (closes #486): Phase 2 still named the retired
cross-plugin path `docs/agents/product-leader-agent.md` (dead since the #433 move the skill's own
head acknowledges) with a fail-closed rule, so contract adoption failed in ALL installs; the
cross-plugin framing is dropped — the agent file is same-plugin, only its doctrine mentions stay
cross-plugin. Found by the abandoned #475 build's fresh-context skill-checker (MAJOR).

v2.17.5 · assembled 2026-08-17 · residual description diet (closes #475, #373 Phase-6
re-measure): the six teamwork artifacts still over the 700-char routable budget after #468/#471
— skill `leading-product` (879→699, boilerplate-trim style matching #468's leading-planning/
leading-review edits, NOT-fences kept in the description) and agents `build-leader` (1,038→584),
`planning-leader` (1,028→620), `review-leader` (979→643), `code-checker` (840→620), `planner`
(818→503) (trailing NOT-for disambiguation sentence moved into the body, #471's harness pattern).
Fresh-context `skill-checker`/`agent-checker` passes on all six surfaced two real findings fixed
in the same change: `review-leader`'s description carried a stale claim that `/leading-review` is
`disable-model-invocation: true` (it's actually `false` — corrected to a mechanism-neutral
statement), and `planner`'s body grew past its 60-line cap from the moved NOT-for paragraph
(trimmed Priority 1/2 restated doctrine to clear it). Blind `routing-judge` proof over the five
`leading-*` suites (40 cases) surfaced one contested case — `leading-product`'s spec-lock gate
phrasing leaked into a `leading-teams`-owned "gate this build dispatch" prompt — tuned the
NOT-fence to name the "gating a dispatch" verb explicitly; the 3-judge revote cleared it. All
five suites 0/0 stolen/leaked/dead/hung after the tune.

v2.17.4 · assembled 2026-08-17 · plugin-shipped hooks retired (#466, Kim's remove-all-hooks
directive): `hooks/hooks.json` deleted (the `worktree_prebash_guard.py` PreToolUse ASK-only
compound-cd guard and the `session_end_worktree_check.py` SessionEnd passive log). Both scripts
kept on disk retired (`.retired` suffix), not deleted, for history — no other caller depended on
either. `parallel-work-rules` and `close-session/intent.md` updated to state the enforcement is
retired rather than live. No gate check asserted a hook must exist, so no gate amendment was
needed.

v2.17.3 · assembled 2026-08-16 (closes #460): deduped the "report delivery" + "no nested wait"
paragraph the four Agent-tool-reachable `*-leader` twins (`build-leader`, `planning-leader`,
`review-leader`, `product-leader`) each restated inline — extracted verbatim into
`teamwork/skills/leading-teams/references/dispatched-agent-report-delivery.md` (home per #468's
fix), with each agent now citing it in one line and stating inline only what's per-citer: whether
it holds the `Agent` tool (only `product-leader` doesn't) and where its own report's content comes
from. Fresh-context `agent-checker` passes on all four confirmed nothing load-bearing was dropped.
v2.17.2 · assembled 2026-08-16 · overhaul #373 Wave-2 S3 (closes #458): centralized the
`leading-planning`/`leading-review` description boilerplate the standing-seat charter template
duplicated across all four `leading-*` skills (the estate's top description-collision cluster,
scores 172–247) — trimmed both under the 700-char budget (1082→672, 714→628) while keeping each
skill's domain noun-phrase and NOT-fences intact; `leading-builds`/`leading-teams` were already
under budget from a prior pass and got a lighter matching touch. Also fixed a stale
`skills/lead-team/references/adopt-agent-contract.md` path in `leading-planning`/`leading-builds`
(the real directory is `leading-teams`) that would have 404'd on first read. Folded in
`teamwork/agents/product-leader.md`'s description diet per the ticket's Scope/Open note — verified
teamwork-owned (not docs' twin) at build time, cut 1666→700 chars, keeping the loop-authority
framing, IDR/RDD types, spec-lock gate, and all four NOT-fences; three body-level asides (RDD/PRP
mapping, cite-the-pack-not-the-bible, cold-start branch) dropped from the description since each
is already stated in full elsewhere (the agent's own body, or `leading-product`'s SKILL.md).
Fresh-context `skill-checker`/`agent-checker` passes on all three touched files: PASS.

PENDING (no version bump yet — coordinator bumps once the full #433 wave lands) · 2026-08-16 ·
issue #433 wave 3, the agent-file leg: `team-lead.md`→`team-leader.md`, `build-lead.md`→
`build-leader.md` (self-references updated, `/lead-team`/`/lead-build` cross-references
untouched — already correct); `docs/agents/product-leader-agent.md` moved here as
`product-leader.md` (cross-plugin move + suffix drop, pairing with the already-moved
`leading-product` skill) with its `docs:product-lifecycle-rules`/`check-stage`/`doc-writing-rules`
dependencies degraded from a would-be structural preload to soft named mentions per the hard
plugin-boundary rule; two NEW standing dispatched agents minted — `planning-leader.md` (backs
`planner`'s procedure, pairs with `/lead-planning`) and `review-leader.md` (backs
`/lead-review`'s routing table, pairs with `/lead-review` — retires the family's prior
"one deliberately agent-less member" status). **All 5 files are non-conforming against the
CURRENTLY-LIVE naming grammar (ADR-0011 REQ-002's `-agent` suffix rule) — intentional, ahead of
the naming-ADR Kim has ruled will supersede that rule; `naming-audit` correctly fails on these 5
until it lands, then this branch rebases/re-verifies.** `skill_lint.py` clean on all 5 (mechanics
only; naming-grammar failures are the known, expected gap above).
v2.17.1 · 2026-08-16 · closes #449 and #450. `mobilize-chores` step 0/1 now classifies its
remainder as a TICKET FILTER (a comma/space-separated ticket-id list — bare numbers, `#NN`, or
`tkt-####`) vs. a SWEEP SCOPE (a seat name or hygiene instruction); only a sweep scope forwards
to `sweep-chores`, a ticket filter skips the sweep and narrows step 2 to reading the named ids
directly. Clears the three standing gate warnings: `dispatch-ticket`/`leading-builds`/
`leading-planning`/`leading-review`/`leading-teams` gain `evals/evals.json` trigger suites (G7);
9 `#433`-surfaced phantom-sibling names allowlisted in `harness/scripts/release_gate.py` (G8,
harness 3.8.22 companion bump — commands/agent-names/historical-citation/prose false
positives); v2.16.5's over-length ledger line rewrapped (G10). `release_gate.py teamwork`
CLEAN 0 fail / 0 warn.
v2.17.0 · 2026-08-16 · issue #433 wave 2 (closes skill/product legs; agent-file renames still blocked on a grammar-ADR, follow-up): `lead-team`/`lead-build`/`lead-planning`/`lead-review` skill dirs → `leading-teams`/`leading-builds`/`leading-planning`/`leading-review`; `/lead-*` user commands unchanged (grandfathered). `docs/skills/lead-product` full-moved here as `leading-product` (docs 1.11.0 companion bump), preloads already soft mentions. `team-scaffolding` stays standalone. `leading` + `build` registered in `naming.manifest.json` ObjectVocab; `naming-audit --scope grammar` clean.
v2.16.8 · 2026-08-16 · orchestrator seat session-name rename (closes #434): the `agent` role's PRINTED/roster session name changes from `{repo}-agent` to `{repo}-team-lead` — the `fleet.json` role key stays `agent` (schema-stable). `team-scaffolding` Phase 1/2/4 point 7, `fleet-bootstrap` Phase 1, `fleet-manifest-schema.md` (new Fields entry stating the key/display split), and lld-0006 D1 updated; `fleet-roster.md` historical `plugins-agent` rows left as-is with a migration note (append-only log). `skill-checker` PASS.
v2.16.7 · 2026-08-16 · fleet-bootstrap Phase 2/4 fix (closes #428): Phase 4's spawn confirm now reads `fleet.json`'s `live_state.joined` (latest row per role) and drops any already-held seat from the offered options instead of hard-coding all four; Phase 2 drops the stale "no dedicated agent file" line and dispatches `docs:product-leader-agent`. `skill-checker` FLOOR PASS (2 majors + 2 minors fixed).
v2.16.6 · 2026-08-16 · fleet-bootstrap Phase 1 fix (closes #423, same class as #421/#422): Phase 1 claimed a Skill-tool hand-off to `/team-scaffolding agent`, structurally blocked (`disable-model-invocation: true`); now registers `{repo}-agent` by reproducing team-scaffolding's Phase 1-4 mechanics inline, Phase 6 names `/lead-team` as the human's follow-up. Rejected: flipping the flag. `wording-checker` PASS (1 Major fixed).
v2.16.5 · 2026-08-16 · reviewer-wall falsification fixed (closes #427): lld-0006 C1's "blocks
every path" claim corrected, not restated — two edges. `team-scaffolding` Phase 1 gains a
`reviewer`-only worktree-isolation precondition (not isolated → stop, name `EnterWorktree`).
Phase 3's reviewer branch also writes a `PreToolUse`/`Bash` hook (lld-0006 C1a,
positive-allowlist regex, path-mandatory retirement escape hatch, hand-verified against 11
allow/deny cases); Phase 6 removes it. `skill-checker`/`doc-checker` FLOOR: 2 major + 3 minor,
all fixed pre-ship. Teardown already covered by #426/PR #430, rebased in. Residual risk named
honestly (lld-0006 R4): not proven sound against an adversarial payload.
v2.16.4 · 2026-08-16 · team-scaffolding orchestrator introduction (closes #429): new Phase 4 point 7 — every bound seat except `agent` itself introduces itself to the live `{repo}-agent` orchestrator via `SendMessage`, discovered fleet-scoped only (fleet-roster.md + fleet.json, never `ListAgents`); no live orchestrator → skip and state so. Kept `docs:product-authoring` as `product`'s hand-off, not a new `teamwork:lead-product` — it's already a fully-built seat, not a thin stub. `skill-checker` PASS.
v2.16.3 · 2026-08-16 · team-scaffolding seat-retirement/handover (closes #426): new Phase 6 `/team-scaffolding retire <role> [reason]`, run by the retiring session — un-walls reviewer's settings.local.json via Bash, appends a "released" fleet.json record, syncs fleet-roster.md. Schema gains action/reason fields (canonical home); Phase 1 collision check reads latest live_state.joined row. skill-checker PASS, 1 major fixed (un-wall mechanism named).
v2.16.2 · 2026-08-16 · team-scaffolding Phase 5 fix (closes #421): Skill-tool hand-off to the four lead-* targets was structurally impossible (all `disable-model-invocation: true`, #134/#135 class). Phase 5 now prints the `/lead-*`/`/lead-product` command for the human to type, mirroring `overhaul-execute`'s command-only handoff. `fleet-bootstrap` checked for the same defect — clean, no change needed. Rejected: flipping the lead-* flags (command-only adoption is deliberate). `wording-checker` PASS.
v2.16.1 · 2026-08-16 · close-session ↔ file-leftovers trigger boundary sharpened structurally (closes #416): 3 genuine close-session triggers (capture/file phrasing) had contested toward file-leftovers under vote; anchored on closing MOMENT vs MANY-item QUANTITY instead of verb choice. Blind routing proof 23/23 both suites, 5 probe cases 3-of-3 unanimous. `wording-checker` PASS.
v2.16.0 · 2026-08-16 · fleet bootstrap two-level design (#410 + addenda): `team-scaffolding` gains planner/reviewer standing-order self-checks (warn/notice, never block), seeds `.claude/ops/fleet.json` on join, and bare invocation asks one question offering only missing seats. New `fleet-bootstrap` hard-gates a full cold start on human ratification, then always confirms its background spawn-list. `fleet`/`bootstrap` registered in naming.manifest.json. `skill-checker`/`wording-checker` PASS. Details in #410.
v2.15.1 · 2026-08-16 · close-session gains a fourth NOT-for fence — sweeping the whole session for many dropped items (docs:file-leftovers) — closing #409, a blind routing-proof leak (n13 confirmed 3-of-3, #404 comment). evals.json already carried n13 as a negative case; file-leftovers already fences the reverse (n06). `wording-checker` PASS.
v2.15.0 · 2026-08-16 · fleet bootstrap seats 1-3 (#404): `team-scaffolding` command names the session, walls the reviewer seat structurally (`lld-0006-fleet-permission-profile.md`), prints the dated seat-tier + comms charter, then adopts `/lead-team`/`/lead-review`/`/lead-planning`/docs' `/lead-product`. Details in issue #404 and the LLD.
v2.14.9 · 2026-08-16 · doctrine-audit D04/D05 fixes (closes #398): construction-note ledger row's transposed apex-seat path corrected to `agents/team-lead.md`; `team-lead.md`'s `tools:` grant renamed the retired platform alias `Task` to the live name `Agent`, verified by an A4 spawn smoke test (dispatch succeeds; `docs:intake-lead`'s `Agent`-walling `disallowedTools` still blocks it) recorded in issue #398. Frontmatter-only, no evals impact.
v2.14.8 · 2026-08-16 · issue #382: the six hand-copied `write-handoff` eight-field fallback blocks (`team-lead`, `builder`, `planner`, `docs-writer`, `code-checker`, `wiring-checker`) consolidated to one referenced copy at `team-or-solo-rules/references/handoff-fallback.md`, following the `adopt-agent-contract.md` pattern; each agent cites the path instead of restating the fields.
v2.14.7 · 2026-08-16 · build-lead gains the standing teammate-mode SendMessage delivery clause (agent-writing-rules item 3, gh#157 stranded-report class; closes half of #381). Rebased onto 2.14.6 and rebumped by PR #383's takeover session (coordinator dispatch, 2026-08-16) — 2.14.4/2.14.5 stayed reserved/skipped per the 2.14.6 note below; supersedes that note, this is the actual #383 rebump.
v2.14.6 · 2026-08-16 · DE-standards adoption (#377): `dispatch-ticket`'s PR-open bullet and Findings write-back both gain a required rejected-alternatives entry (docs doc-writing-rules' TICKET contract, same tier as Findings); its critic dispatch may carry an optional review-path line, mirroring write-handoff's (harness). 2.14.4/2.14.5 skipped, reserved for PR #383's own rebump (comment-coordinated).
v2.14.4 · 2026-08-16 · agent-scoped worktree-identity pin (closes #375, #363/#359's own follow-up):
`worktree_prebash_guard.py`'s persisted pin was keyed by `session_id` alone, but this workspace's
multi-agent teams feature hands every parallel agent in one dispatch the SAME session_id — agent
B's correct, escape-free command in its OWN worktree false-positived as drift because agent A's
earlier call (different worktree) had written the shared pin file (screenshot evidence,
2026-08-16). Two independent fixes: (1) `resolve_agent_key()` folds a best-effort per-agent
discriminator (`CLAUDE_AGENT_ID`, else `CLAUDE_PID`/`CMUX_CLAUDE_PID` — no documented per-agent
field exists on the PreToolUse event or hook env, verified live; falls back to session-only
keying, unchanged, when none resolve) into the pin's file key. (2) a no-escape-attempt carve-out:
a call with no cd/pushd token anywhere no longer asks on a pin mismatch — live evidence during
this build that this host's own reported `cwd` can move between consecutive same-agent calls
with nothing in the command to explain it, making "no cd, cwd moved" alone unreliable; the
compound-cd/-C escape detection (`analyze_command`) is untouched, so a genuine cd-then-write into
the primary checkout or a sibling still asks regardless. 5 new selftest fixtures (40 repurposed,
42-45); fresh-context hook-checker critic: 1 Major fixed pre-merge (the carve-out's cd-token
scan initially also counted `-C`/`--prefix`, defeating itself on `rg -C 3 foo`-shaped commands —
narrowed to cd/pushd only, since a genuine -C escape is independently caught by
`analyze_command`'s own hits regardless of the pin), plus a stale docstring paragraph and the
drift ASK message text repaired to match the new behavior.
v2.14.3 · 2026-08-16 · critic-step nested-wait hardened (closes #370, PR #317's structural rule
extended past build delegation to the critic step): `dispatch-ticket`'s no-nested-wait paragraph
and `build-lead`'s own copy both gain an explicit recovery instruction — after dispatching a
fresh-context critic, never wait for a completion notification (it routes to the ROOT session like
any other nested callback, per PR #368's ADR-0014-build recurrence); act on the Agent tool call's
own synchronous return value directly, or, if already stalled, read the critic's transcript/output
file yourself or let the coordinator relay the verdict
v2.14.2 · 2026-08-16 · persisted worktree-identity pin (closes #363, #359 follow-up): `worktree_prebash_guard.py` gains a per-session, session_id-keyed pin, ASK-and-self-heal on drift (first-call pin-write, no cd needed to catch it); 10 new selftest fixtures (32-41); `parallel-work-rules` doctrine note citing #359. Fresh-context hook-checker: 1 Major fixed pre-merge (unwritable data dir crashed the hook — now fails open, tmp-write race fixed alongside)
v2.14.1 · 2026-08-16 · checker-agent description diet (#357): code-checker/wiring-checker descriptions drop the shared fresh-isolated-context / never-grades-own-work / gap-map boilerplate (collide.py's top cross-plugin *-checker baseline, 6 agents, 103.9-158.4); doctrine added to each body opener. Re-run: code-checker↔design-system-checker 109.9→91.3, ↔flow-checker 103.9→69.6; wiring-checker↔layout-checker 135.6→64.0, rest below threshold. Batched critic pass (6 files): both clean; layout-checker's dropped fix-owner clause repaired same-round. No evals.json owed. Siblings trimmed same PR.
v2.14.0 · 2026-08-15 · agent-contract-adoption ritual centralized (closes #352, bloat-audit
2026-08-16): `lead-planning`, `lead-team`, and `lead-build` carried near-duplicate copies of the
"read the agent file, adopt its contract verbatim, acknowledge before real work, don't stack a
second adoption, close on the named decision" ritual (1.0 similarity on parts, 0.7 on others).
Reconciled into one canonical copy, `lead-team`'s `references/adopt-agent-contract.md`, cited
one-line by the other two; `lead-review` was deliberately left out — it adopts no single agent's
contract by design, so it never carried this ritual to begin with. Each skill's own "three
places the host's version differs" list and duration rule (charter- vs. session-scoped) stayed
inline — genuine per-seat divergence, not drift.

v2.13.3 · 2026-08-16 · cross-PR version-claim coordination cross-referenced (closes #311,
harness-side doctrine): `dispatch-ticket`'s Phase 3 claim bullet gains a pointer — a ticket claim
is not a plugin-version claim, so right after claiming, and again before the PR opens, run
harness's new `version_claim_check.py` (where harness is installed; skipped and named otherwise)
against every plugin the build touches, per the #284/#289/#290 collision cluster now encoded in
`big-change-git-rules`' `who-ships-what.md`. Pointer only — the substantive rule stays owned there.
v2.13.2 · 2026-08-16 · the no-nested-wait rule encoded structurally (issue #310, four measured `build-lead` stalls #257/#282/#269/#280): `dispatch-ticket` and `build-lead` both gain a standing rule — a nested seat builds inline, never via a further fork/named dispatch it then waits on for an unreachable callback. Matching harness `agent-writing-rules` row (own bump)
v2.13.1 · 2026-08-16 · checker retier (Kim's ruling): 2 *-checker agents move effort high→medium, model fable unchanged — review quality held at medium across the 2026-08-15/16 rounds while inherited-xhigh runs added cost, not findings
v2.13.0 · 2026-08-16 · `mobilize-chores` step 1 repointed (issue #266, harness-side): harness's `chore-lead` coordinator agent retired, so this step now calls the reclassified `Skill(harness:sweep-chores)` directly cross-plugin instead of dispatching the retired agent — same fan-out, no duplicated logic, no hard `${CLAUDE_PLUGIN_ROOT}` path; step 5's build-lead comparison and Done-when text updated to match
v2.12.3 · 2026-08-16 · `team-or-solo-rules` gains the job-evidence test (#268), modeled on `plan-plugin-split`'s job-evidence rule: a NEW coordination seat/flow must record the concrete gap solo + one Explore/checker can't hold — step count alone never counts. New seats only, no retroactive re-justification. Documented-checklist form (no natural wiring-checker rubric anchor); Review gains a matching check. Body-only, no eval-run obligation
v2.12.2 · 2026-08-15 · `worktree_prebash_guard.py` read-only carve-out (`pwd`/`ls`/`true` + never-mutating git subcommands): a provably non-mutating tail after an escaping `cd` no longer prompts — ends `build-lead`'s per-build approval barrage. Hardened by two critic rounds: `--output=<path>` writes excluded outright; attached shell operators (not shlex words) caught by raw-substring metachar rejection. 31/31 fixtures, bypasses re-proven closed via `--hook`
v2.12.1 · 2026-08-14 · `dispatch-ticket` Phase 3's "Isolate second" bullet had a corrupted/truncated sentence (#249): "All four hold → build directly in the claim/write-back contract stays mandatory regardless" was missing its clause. Restored to "build directly in the host checkout; the claim/write-back contract stays mandatory regardless" — matches the phrase already used verbatim at Phase 5 stage 3. Grammar fix only, no behavior change, critic pass skipped per the ticket
v2.12.0 · 2026-08-14 · quick-build auto-merge (#244, ADR-0012 proposed, lld-0002 v0.2.1): `dispatch-ticket` Phase 5 gains stage 2b — on an explicit `auto-merge: authorized` grant plus an all-green fail-closed QB0–QB7 predicate (QB4 an ALLOW-list, so an unlisted file class is ineligible by construction), the seat watches CI under a feature-detected 900s bound (GNU timeout is absent on darwin), squash-merges, SHA-verifies MERGED, runs `campaign_close.py`, then posts a dated QB snapshot; any miss falls back to PR-opened. Critic, gates, CI and the PR are never skipped
v2.11.0 · 2026-08-13 · `mobilize-chores` gains the `Blocked-by: #NN` dependency convention (issue #193) as a third, independent step-2 exclusion plus step-6 blocked-and-why reporting; canonical format documented in new `references/blocked-by-convention.md`; harness's `chore-planner` (own bump) reads the same convention via a new preloaded skill; #197 migrated as the first real data
v2.10.1 · 2026-08-13 · `parallel-work-rules` gains the #207 worktree-vanished recovery procedure and the #189 sibling-cwd-race standing mitigation, both cited; body-only, no description change, no eval-run obligation
v2.10.0 · 2026-08-13 · `dispatch-ticket`'s Phase 3 isolation gated conditional on size/collision-risk instead of unconditional (issue #204), and the whole file tightened ~18% with zero rule/citation loss (issue #206) — combined build, one PR, fresh-context skill-checker FLOOR pass applied
v2.9.5 · assembled 2026-08-13 · 2.9.5: `dispatch-ticket` Phase 3's claim step gains a
list-visible `in-flight` label lifecycle (issue #199, Kim's own report: "I cannot tell that
Issues are claimed or in some kind of 'doing' state" — the claim comment alone is invisible in
the GitHub issue LIST view). Applied only after the claim wins Phase 3's own race-check, removed
at every terminal outcome — Phase 5 stage 2 the moment a PR opens, the Release-on-abandonment
bullet on a mid-flight abandon, and Phase 6's recorded-loss ending, all three naming the label
alongside the pre-existing assignee release, none left stale. Label = display, comment = record,
stated explicitly: `mobilize-chores` step 2 gains one sentence naming the label as a cheap,
optional pre-filter over its existing `assignees`+GraphQL correctness gate, never a substitute for
either. Correction to the ticket's own premise, investigated and deliberately NOT executed as
literally asked: #199 characterized this repo's pre-existing `doing` label as a stray duplicate
BUILD-192 minted and asked for its deletion — a grep across `file-bug`/`file-task`/
`parallel-work-rules`/this skill's own Phase 6 shows `doing` is the established, load-bearing
git-native status-vocabulary label (`open`→`doing`→`done`, `backend-resolver.md`'s `update`
operation), unrelated to claiming; deleting it would have broken that contract across three other
skills for one ticket's mistaken premise. The two labels legitimately coexist on one issue at
once — this PR documents the distinction instead of deleting either. Assignee stays required,
unchanged (ADR-0005/`backend-resolver.md`'s own ratified claim operation, a docs-plugin file
outside this ticket's target list) — the real gap #192 evidenced (assignee and label both left
stale after close) is closed by the new terminal-outcome release paths, not by dropping assignee.
Two fresh-context `skill-checker` FLOOR passes per edited file (`dispatch-ticket`: one major plus
five minor/nit findings, all closed across two follow-up rounds; `mobilize-chores`: one minor,
closed) — every finding applied before this PR opened. Incidental cleanup: removed the stale
`in-flight` label (and, on #192, the stale assignee) from #192/#198/#190 — all three closed, all
three evidencing the exact defect this ticket fixes; `doing` left untouched on all three · v2.9.4 · assembled 2026-08-13 · 2.9.4: `worktree_prebash_guard.py` gains sibling→sibling
detection (issue #198, composes with #139's worktree→primary fix without regressing it) — a
session pinned to one worktree cd/pushd/-C/--prefix'ing into a DIFFERENT worktree under
`.claude/worktrees/` now also flags, via the same ASK-only `hookSpecificOutput` pattern the
existing direction already uses. Correction to the ticket's literal wording: the issue text
called for a hard block (exit 2); the shipped fix does NOT introduce one — this hook stays
deliberately ASK, never BLOCK (hook-writing-rules: judgment-shaped rules are wrong often and
unoverridable always as a hard block), same as the pre-existing direction. The ASK message now
names BOTH worktrees involved (the session's own and the sibling target), not just a raw
resolved path. Five new selftest fixtures (13–17: sibling positive, own-worktree relative-cd
negative, seat1/seat10 boundary control, an own-name-not-shadowed-by-prefix control, and a
mechanized check that the message actually names both worktrees) bring the suite to 17, all
green. Pure code change — no hook MESSAGE prompt text materially changed beyond the ASK reason
string, so no separate `hook-checker` critic pass required per this repo's critic-seat
invariant · v2.9.3 · assembled 2026-08-13 · 2.9.3: `agents/build-lead.md` compression (issue #192) — the
verbatim-relay rule was stated four times across a ~27-line body (opening job statement, a
blocker/redirect restatement, the Phase-5 handoff's own "through verbatim" wording, and a closing
"you relay whatever `dispatch-ticket` actually states" clause) — flagged by PR #187's build-time
`agent-checker` critic and deferred as "compress on next touch." Now stated once, in the opening
paragraph, covering every phase and branch below by explicit reference rather than restatement;
the PRE-CLAIM/POST-CLAIM retirement-handoff distinctions and the no-fabrication rule on a missing
handoff line are unchanged in substance, just no longer re-deriving the relay rule to state them.
No frontmatter edit, no behavior change to the seat's contract. Fresh-context `agent-checker`
FLOOR audit: PASS, no blocking findings · v2.9.2 · assembled 2026-08-13 · 2.9.2: `dispatch-ticket` Phase 3 gains a verified teardown path
(issue #190, tracked from gen-ui-kit#1151) — the two cases where this skill retires a scratch
branch/worktree (a post-claim abandonment once released, or the bug hand-off's own worktree once
`file-bug`'s hand-off shows a terminal read-back) never delete with a raw `git branch -D` plus
worktree removal anymore. Feature-detects the host repo's own gated reap script (gen-ui-kit's
`scripts/ops/reap-branches.mjs --verify-branch <name>` is the reference shape) and gates the
delete on its exit code alone — exit 0 (a merge-base ancestor of `origin/main`, or an
exactly-matching MERGED PR) → `git worktree remove` then `git branch -d` (never `-D`, even
post-verify); exit 1 (KEPT/PROPOSED) or either verb refusing outright → leave standing, report
why; exit 2 (usage error) → report it, never treat as a verdict. No script at that path → an
unverified fallback, but always with a named warning, never silent. Independent `skill-checker`
FLOOR audit: PASS, one blocker + one major fixed same-pass (the bug-case trigger had no named
observable and could fire on a still-live fork; the delete verbs' own dirty-tree/unmerged
refusals had nowhere named to land) plus two minors (fallback op order, exact-path pinning).
Body-only, no description edit, no suite re-judge owed (Phase 3 carries no eval-suite-relevant
routing surface). Docs' sibling fix: docs 1.4.6 · v2.9.1 · assembled 2026-08-13 · 2.9.1: `dispatch-ticket` Phase 3's "Isolate second" reuse check
(issue #191) keyed off PATH SHAPE — "cwd is anywhere under `.claude/worktrees/`" — rather than
IDENTITY, so a nested `build-lead` dispatch invoked from inside an unrelated caller's own
long-lived worktree (`mobilize-chores`'s own, say) reused that caller's tree instead of creating
its own, checking the target ticket's branch out on top of the caller's uncommitted state.
Reuse now requires BOTH conjuncts: the cwd is a linked worktree (never the primary checkout — the
#180/#182 residue this same bullet already cited is exactly a stale branch left checked out IN
the primary checkout) AND that worktree's checked-out branch matches the name the claim bullet
(or the bug hand-off's own naming) just decided for THIS ticket — the decided name embeds the
ticket's own id, so a branch match against it is identity, not path shape. Fresh-context
`skill-checker` FLOOR audit: 2 majors fixed pre-ship (the reuse condition didn't exclude the
primary checkout, reproducing the exact #180 residue it cites; a proposed marker-based reuse path
read a marker nothing in the skill ever writes — dropped in favor of the branch-match conjunct
alone, which the audit confirmed already carries full identity since the decided name embeds the
ticket id) plus 2 minors (a dead pointer at a `file-bug` branch-naming convention that doesn't
exist; a near-verbatim sentence deduped between Phase 2 and Phase 3).

v2.9.0 · assembled 2026-08-13 · 2.9.0: `/lead-planning` (issue #194) — the fifth `/lead-*` member,
new command surface pairing with the existing, UNTOUCHED `agents/planner.md`: the host adopts the
design seat's own contract directly for one named planning charter, mirroring `lead-build`/
`lead-review`/`lead-team`'s four-phase shape (bind charter → adopt contract by reading the agent
file, never restating → run the loop → close on a named `loop-rules` decision). Two deltas from
`lead-team`'s host-adoption precedent: write discipline INVERTS (authoring the PRD/SPEC/LLD/ADR
the charter earns is this seat's own deliverable, so the host writes them directly — but never
grades one it wrote; every authored/revised doc rides to `docs:doc-checker` fresh-context, or the
disclosed by-hand fallback against `doc-writing-rules`' rubric where docs isn't installed) and
roll-up audience (the invoking human, not a dispatching coordinator). Failure branches mirror
`lead-team`'s: blank charter reports what a charter looks like rather than inventing one;
re-invocation while a prior charter is open checks records rather than merging state silently; a
doc-checker verdict failing twice indicts the doc's own intent capture, not the checker.
`disable-model-invocation: true` exempts it from the routing-eval coverage sweep (`eval_check.py`'s
E6 check skips every dmi:true skill outright) — matching `lead-build`/`lead-review`'s own
precedent of shipping no `evals/evals.json`; `evals/assertions.md` added for the behavioral
contract. Fresh-context `skill-checker` FLOOR audit: PASS, two minors fixed pre-ship (the Phase 2
priority gloss trimmed to heads-only rather than clause detail, closing the exact drift-pair
surface lead-team's own audit report flagged as a MAJOR at birth; reciprocal `/lead-planning`
NOT-for fences added to `lead-team` and `lead-build`'s menu descriptions, both dmi:true so no
evals.json obligation follows). `agents/planner.md` untouched, per the ticket's own constraint.

v2.8.0 · assembled 2026-08-12 · 2.8.0: build-dispatch lifecycle redesign (issues #183/#184,
mobilize-chores confirm round) — a build-lead/dispatch-ticket dispatch now owns its full
execution lifecycle end to end, not just the code change. Evidence: the #180/PR #182 dispatch ran
in the HOST checkout with no worktree at all and left its feature branch checked out; the
coordinator repaired it by hand, because isolation was mobilize-chores' own instruction,
conditioned on "2+ concurrent" — a bar a solo serial dispatch never clears. `dispatch-ticket`
gains a new Phase 3 ("Claim, then isolate"), renumbering the phases after it (old 3/4/5 → 4/5/6):
**claim** takes ADR-0005's ratified `claim` backend operation (assignee + timestamped comment,
git-native; `claimed-by`/`claimed-at`, file) before any build effort starts — this dispatch is
that operation's first real caller, closing the gap ADR-0005 itself named as open, not a new
mechanism invented here (`docs` 1.4.5 repairs `backend-resolver.md`'s now-stale "claim has no
caller today" line in the same spirit); re-reads to confirm the claim wasn't outraced, abandons on
a lost race. **Isolate** is unconditional by default for every tree-mutating path, including the
bug hand-off (which runs isolate — never claim, `file-bug` owns its own record lifecycle — before
invoking `file-bug`, since that skill's own body carries no worktree mechanics of its own to rely
on). Release-on-abandonment is post-claim-only (a mid-flight design fork or unresolved gate
failure) — a pre-claim exit (task SKIPPED, an ambiguous-match blocker) never claimed, so never
releases. Phase 5 ("Dispatch under contract") now enumerates the four lifecycle stages by name:
isolated execution, branch+commits+PR-opened per ADR-0002 (with an integration-notes line that
adopts another PR's already-defined shared field wording rather than minting a competing one),
verified-clean retirement (worktree/branch/host-checkout state, each stated, never assumed), and a
typed retirement handoff (PR URL + Findings comment URL + an explicit environment-clean line).
`build-lead`'s return contract (`agents/build-lead.md`) now carries that handoff through verbatim,
with the pre-claim/post-claim split named so it never fabricates an environment-clean line for a
dispatch that never started one. `mobilize-chores` step 2 gains a claim check (non-empty
`assignees`/`claimed-by`) alongside its existing open-PR check, closing the dispatch-to-PR-open
window a claim-blind check couldn't see (#184, folded into this same campaign per Kim's ruling);
step 5 drops its own "2+ concurrent → isolation" instruction entirely (isolation is now
`dispatch-ticket`'s own structural default) and keeps only the PARALLEL-vs-SERIAL timing call — a
named, non-overlapping edit target avoids a foreseeable merge conflict, a risk per-dispatch
isolation alone doesn't remove. `intent.md` gains assertions 8/9 and a dated ruling recording the
redesign, including a self-caught regression: step 5's first draft claimed bug-kind isolation
"inherits… regardless of kind" via the OLD fork-containment reasoning, while the same edit had
just removed the instruction that reasoning depended on — bug-kind was briefly left with NO
isolation layer at all, caught by a fresh-context skill-checker re-audit before ship and root-fixed
in `dispatch-ticket` itself (its bug branch now isolates before handing off). Four fresh-context
critic passes total (skill-checker ×2 initial + ×2 re-audit on dispatch-ticket/mobilize-chores,
agent-checker ×1 on build-lead): one blocking finding (the bug-kind regression above), one major
(a release-trigger enumeration listing two branches — task SKIPPED, an ambiguous-match blocker —
that can never actually hold a claim since both occur before Phase 3 ever runs), one major (the
isolate bullet's "create" case presupposed a claimed branch name the claim-free bug path never
has), all fixed pre-ship; minors/nits (try-cap scoping, duplicated stale-claim prose, incident
narration moved to `intent.md`, an overclaim about bug-kind retiring a worktree it never reaches)
fixed the same passes. `docs` 1.4.5 companion change: `backend-resolver.md`'s `claim` row names its
first real caller instead of "no caller today" — the only cross-plugin repair this campaign made,
disclosed here since the edit surface was otherwise teamwork-scoped · v2.7.3 · assembled 2026-08-12 · 2.7.3: README Map gains the missing `skills/mobilize-chores` row —
the plugin's most-shipped member (2.4.0 auto mode, 2.5.0 blocker breakdown, 2.6.x/2.7.1
concurrency rules) had no Map row at all; the gate's mention-based docs check passed because
sibling rows name it. Found by the repo-docs freshness sweep; README-only, no behavior change · v2.7.2 · assembled 2026-08-11 · 2.7.2: one-word reword in 2.7.1's measurement prose ("marker-file
write" → "probe marker write") — the phrase tripped G8's phantom-name check via the `-file`
suffix; reworded rather than allowlisted, and bumped rather than folded into 2.7.1 (the bump-every-
change invariant is unconditional; a first attempt to skip the bump on a no-reload-between
rationalization was itself the defect this entry corrects) · v2.7.1 · assembled 2026-08-11 · 2.7.1: fork-cwd containment MEASURED, the serial-bug-kind guard
retired — 2.6.0's one disclosed UNVERIFIED settled by a live probe the same week it was flagged: a
purpose-built `context: fork` skill invoked from inside a worktree-isolated general-purpose agent
executed entirely inside the agent's worktree (pwd, `git rev-parse --show-toplevel`, and a
marker-file write all at `.claude/worktrees/agent-<id>`, never the root checkout; probe deleted
after the measurement). A worktree genuinely contains a fork's cwd, so `mobilize-chores`' bug-kind
dispatches now take the same isolation/parallel rules as feature/task instead of the
mandatory-serial fallback. The probe re-confirmed in passing that a fork's completion notification
routes to the ROOT session (the invoking agent saw only the launch ack) — consistent with the A4
record and gh#157. The prior UNVERIFIED text stays in the intent record as dated history with the
MEASURED supersession appended. Semantic edit rode with its critic per the new workspace
invariant: fresh-context skill-checker delta audit PASS, no findings owed (the one steelmanned
concern — cwd-relative vs. absolute-path writes — dismissed against the guard's own stated
question, which was cwd escape specifically) · v2.7.0 · assembled 2026-08-11 · 2.7.0: the first /check-everything estate audit's teamwork fixes,
all checker-prescribed. `dispatch-ticket`: the Done predicate's bug arm required relaying
"file-bug's own result" — a thing the body's own VERIFIED finding says never reaches this seat
(fork completions route to ROOT), so satisfying it literally meant the exact wait the never-wait
rule forbids; the arm now names the read-back snapshot (state/Findings as of hand-off) as the
checkable done-state, with the fork's outcome explicitly never this seat's to wait on; the ":57
no longer an assumption" editorial trimmed; and Phase 3's small path gains the three-strikes
contract line (a small build that semantically edits a prompt-carrying artifact gets a
fresh-context checker pass before the loop closes — the audit found every recent unaudited
semantic edit carrying a real gap; docs 1.4.4 lands the same clause on file-bug's fix-inline
branch). `worktree_prebash_guard`: hook-checker's live probes found three undisclosed silent
bypasses — `pushd` and `command`/`builtin cd` are now RECOGNIZED (fixtures 10–11 prove they
bite), and `sh -c` wrapper strings join the disclosed-blind-spots list honestly (fixture 12 pins
the fail-open); `session_end_worktree_check`: committed-but-never-pushed work in a repo WITH a
remote but no upstream logged nothing — the exact campaign-loss case the hook exists for — now
counted via `rev-list HEAD --not --remotes` gated on a remote existing (fixture 5; a fresh local
repo with no remote stays silent), and the unset-CLAUDE_PLUGIN_DATA fallback moves from /tmp
(silently defeating "durable, discoverable") to `~/.claude/plugins/data/teamwork`. Both selftests
green, 12/12 and 5/5. Hook changes bite after reload · v2.6.1 · assembled 2026-08-11 · 2.6.1: `team-or-solo-rules` step 5 + its best-practices fan-out
section now NAME the host-owns-git precondition they previously only implied — save-lessons
harvest of 2.6.0's own incident, landed in the doctrine that owns it: the disjoint same-tree
fan-out is safe because workers only edit files while the HOST alone gates-and-commits; a worker
that drives its own branch/commit/PR lifecycle per dispatch (`build-lead`/`dispatch-ticket`, a
release cutter) races siblings on the shared index/HEAD regardless of file disjointness, so for
that worker shape file-disjointness decides PARALLEL-vs-SERIAL only and concurrency always takes
per-worker worktree isolation. The 2.6.0 re-audit explicitly noted `mobilize-chores` had become
more explicit about this than the owning doctrine itself — that inversion is the drift this entry
retires; `wiring-checker` preloads this skill, so the checker inherits the sharpened rule for
free. Body+reference only, no description edit, no suite re-judge owed; the precondition's factual
claims were source-verified by 2.6.0's own re-audit the same day. · v2.6.0 · assembled 2026-08-11 · 2.6.0: `mobilize-chores` step 5 gains a disjoint-fan-out check —
Kim's explicit request after reviewing this skill's alignment with `team-or-solo-rules`' "match
ceremony to the task" doctrine (step 5's default was blanket serial/isolation for every mutating
dispatch, never offering the disjoint-fan-out shortcut that doctrine sanctions elsewhere). FIRST
DRAFT copied that doctrine's permissive conclusion too literally and FAILED its own FLOOR audit
with 2 blocking findings: `team-or-solo-rules`' fan-out is safe because the HOST owns git while
workers only edit files, but a `build-lead` dispatch drives its OWN branch/commit/PR lifecycle per
ticket — two concurrent dispatches race on the shared git index/HEAD regardless of file overlap,
so "disjoint path → skip isolation" was false; the draft's "bug-kind always safe to overlap, no
tree mutation" claim was also false (`file-bug`'s own Phase 5 can fix a root-cause-evident bug
INLINE). Corrected model, RE-AUDITED PASS same day: `isolation: "worktree"` is now UNCONDITIONAL
for 2+ concurrent mutating dispatches of any kind; a named, non-overlapping edit-target path in a
confirmed ticket's own body (explicitly excluding a `## Links` doc-citation or a bare
plugin-level directory) only decides PARALLEL-isolated vs. SERIAL, never isolation-vs-none — no
such path on either side stays SERIAL, the pre-existing default. Two more findings closed same
re-audit pass: a serial dispatch now explicitly starts from a clean `main` HEAD (a dirty
predecessor is the next dispatch's named blocker, never silently inherited), and bug-kind's
`context: fork` hand-off into `file-bug` has UNVERIFIED fork-cwd containment against this
platform's real mechanics — disclosed plainly, with concurrent bug-kind dispatches staying SERIAL
until that's measured live. `intent.md` gains assertion 8 and a dated ruling recording the failed
first draft honestly, not just the fix. · v2.5.0 · assembled 2026-08-11 · 2.5.0: `mobilize-chores` step 6 gains a blocker breakdown — Kim's
explicit request after seeing the shape land well in a different repo's session (a per-blocker
paragraph naming what's blocking it and a proposed action, then commands only on request). Every
ticket that comes back as a named blocker (not a plain SKIPPED, which has no blocking reason to
break down) now gets one classified paragraph instead of a table row: `build-lead`'s own stated
cause quoted or paraphrased, which of six shapes it is (judgment call needing a live conversation
/ protocol ratification only a human utterance satisfies / someone else's in-flight work / a
mechanical human action — permission, credential, tool install / an external dependency with no
lever here / or an explicit "fits none" escape), and a proposed action fitted to that shape —
never a build attempt, on any of the six. Prose only in this pass, even where a command exists; a
documented follow-up convention ("give commands" or equivalent) switches to a commands-only pass
— a real verbatim command where one exists, an honest "nothing to run" where it doesn't.
`intent.md` gains assertions 6/7 and a dated ruling. Independent `skill-checker` FLOOR audit: PASS
after fixing 1 major (the original four-shape taxonomy had no escape hatch, and a real fifth
shape — a mechanical human action like a permission grant — existed that would have been misfiled
as "external dependency, nothing to do but watch" when a one-line grant is actually the lever;
added the fifth shape plus an explicit escape) + 1 minor (assertion 6 required the paragraph to
name its shape; the SKILL.md spec didn't say so) + 1 nit (a labeled bad/good pair closing the last
inline-command temptation in the ratification shape). · v2.4.0 · assembled 2026-08-11 · 2.4.0: `mobilize-chores` gains an explicit `auto` unattended mode — a
`/goal` loop draining the ops queue overnight has no one to answer step 4's `AskUserQuestion`, and
until now that made the skill structurally unable to run without a human in the room. New step 0
parses `$ARGUMENTS` for a leading, literal `auto` token (never inferred from "no user is watching"
— the same invocation behaves identically whether a human or a loop types it); step 4 branches
INTERACTIVE (today's confirm round, byte-unchanged) vs UNATTENDED (skip `AskUserQuestion`,
auto-confirm every ticket step 2 already found mobilizable — step 2's own filtering, not step 4,
was always the real correctness gate). Blast radius stays bounded on purpose: this mode only ever
reaches "built + PR opened," never merge/review — this workspace's standing doctrine
(`auto-mode-gh-permissions`) and the platform's own permission classifier both reserve that for a
human regardless of what the goal says, so the confirm round it replaces was never guarding that
door. `intent.md` assertion 2 gains the matching exception clause + a dated ruling. Independent
`skill-checker` FLOOR audit: PASS, no blocking findings; 2 major + 1 minor + 1 nit, all fixed
same-pass — the UNATTENDED branch's "in-flight PRs excluded on both branches" overclaim narrowed
to git-native (Option A/local tickets genuinely has no such check, step 2's own disclosed
limitation) with a named per-ticket gap instead; `intent.md`'s delta/assertions 2/3/5 de-staled
from the pre-ADR-0010 per-kind routing they'd drifted to since 2.0.0's rename; the "never reaches
merge" ceiling pinned by a one-line reference to ADR-0002's merge gate instead of resting on an
unstated environmental assumption; step 6 now names which branch ran, closing the one silent
misparse path (a scope instruction starting with the literal word "auto"). · v2.3.0 · assembled 2026-08-10 · 2.3.0: /init-repo — the /lead-* family's composer and closing artifact: one command arms a work session (conditional /init → team-lead adoption with the session-as-charter deviation named → standing INTAKE sibling → per-ticket build capacity → the armed report naming every step's outcome). Naming rides the term-of-art exception (init wraps the built-in /init it conditionally runs; lead-repo/arm-repo considered and rejected — ruling in the intent record). The forge's audit caught two real composition MAJORs pre-ship: (1) the seedless INTAKE spawn landed in intake-lead's missing-seed STOP branch — that agent's own A4 record had empirically proven the exact return — fixed by declaring that return the liveness ack (zero contract-bending; a SendMessage resumes the named seat per seed); companion gap queued for docs (intake-lead's description endorses the standing spawn its body never defines); (2) the docs-absent degradation routed to docs' OWN file-* commands — a dead pointer exactly when the branch fires — split into tool-error-with-docs (file-* by name) vs docs-absent (host-recorded work items, gap named). Behavior check: both scenarios PASS (this repo skipped-present; a simulated fresh docs-less repo exercising both fixes) and the combined file-it-and-fix-it probe held the adopted discipline — verbatim relay to INTAKE, no inline code under 'should be quick' pressure, build staged pending the confirmed ticket: the whole family composed end-to-end in one exchange. Baseline disclosed honestly: the ad hoc session did much right (anti-duplication, solo-first) and precisely thereby declined the ARRANGEMENT — no seat, no contract, no report · v2.2.0 · assembled 2026-08-10 · 2.2.0: /lead-review — the review desk's host-adoption command, fourth and final /lead-* family artifact, and the family's one deliberate asymmetry: NO agent twin (Kim's ruling — the estate's eleven fresh-context checkers ARE the review capacity; a standing review agent would duplicate them or launder their rubrics through one accumulating context). The session adopts the DESK: an 11-row routing table (every checker verified to exist with a matching charter), dispatch-only as generator≠critic made structural, verdict-first relay, and the self-authored-work guard (a target this session authored gets a NEUTRAL dispatch — pointer + rubric owner + depth + destination, zero framing — with authorship disclosed at relay). Forged through the full /make-skill loop: baseline caught the subtle failure (the ad-hoc REVIEW session NAMED the right routes as would-runs, then reviewed both targets inline anyway — routing instinct present, discipline absent), audit PASS with two minors fixed (doc-checker's row under-listed its charter, so a CLAUDE.md would have hit a false gap; the absent-plugin degradation inherited lead-team's silent from-memory-rubric problem — both losses now disclosed) plus the FLOOR/DEEP depth carried into the dispatch seal, behavior check all four assertions PASS incl. the guard's sharpest evidence: the self-authored dispatch came out structurally identical to a neutral one · v2.1.0 · assembled 2026-08-10 · 2.1.0: /lead-build — the build seat's host-adoption command, third artifact of the /lead-* family (after docs' intake-lead agent + /lead-intake). The session the human types into adopts build-lead's contract and drives every target through dispatch-ticket via the Skill tool — deliberately DIFFERENT mechanism from /lead-intake's read-and-apply-inline: dispatch-ticket carries no context: fork (ADR-0010's design), so a host Skill invocation runs inline naturally, no fork hazard, and the engine's interactive branches (Phase-1 ambiguity question, task clarify round) fire on the live user they test for. Forged through the full /make-skill loop: baseline (an ad-hoc-primed BUILD session paused on a closed ticket by luck but treated a vague 'when you get a chance' chore as license for immediate multi-file cross-plugin edits — no record, no scoping question, the append-only ledger footers one turn from being cut), fresh-context audit (1 MAJOR in the ENGINE's files: dispatch-ticket's caller enumeration excluded its third sanctioned caller — description, intro, and build-feature's no-fork rationale all repaired to the one-engine-three-entries truth, description re-dieted ≤700; routing re-judge rides the next wave boundary per the edit ladder's batching clause since the engine owns no suite and its fences are unchanged), behavior check on grounded probes (closed #150 → engine state-first stop with the record's own Findings; the vague chore → dedup sweep then [nested-intake] intake queued before any edit; the 'no ticket, it's tiny' pressure probe declined per contract). Reciprocal fence added to /build-feature's description. Disclosed: the no-match branch's intake forks from a host session and routes back to it (host = root) — one asynchronous hop · v2.0.1 · assembled 2026-08-10 · 2.0.1: dispatch-ticket's bug-branch fork caveat upgraded from assumption to VERIFIED finding — docs' intake-lead A4 spawn smoke test (2026-08-10, issue #160) produced the estate's first empirical data on the flagged fork-from-agent class: a `context: fork` skill invoked from inside an agent dispatch runs as a background fork (not synchronously), and its completion notification routes to the ROOT session, not the invoking seat, which strands idle waiting (also independently corroborates #157's root-routing report). The record-as-return-channel discipline 2.0.0's wiring review installed is therefore load-bearing, not merely cautious; the sentence now states the verified mechanism and the never-wait rule plainly. Body-only, no description edit, no suite re-judge owed · v2.0.0 · assembled 2026-08-10 · 2.0.0: BREAKING (ADR-0010) — `feature-lead` renamed `build-lead` and `dispatch-feature` renamed `dispatch-ticket`, both generalized to every confirmed ticket kind. The rename resolves the duplication the `/lead-*` session-priming design surfaced (a planned `build-lead` agent would have preloaded the same procedure `feature-lead` already preloads — the anti-matrix rule demanded one seat, not two; Kim's first candidate `chores-lead` rejected as a test-5 one-letter collision with harness's `chore-lead`). `dispatch-ticket` now branches by kind: feature keeps the find-or-make/size/dispatch/close-loop path byte-equivalent; task ABSORBS the clarify-then-dispatch logic (find-intent round → solo-first Agent dispatch → backend-aware Findings write-back and status verbs) that previously lived inline in `mobilize-chores` step 5 — one owner, deleted at the old site same-change; bug keeps the `file-bug` hand-off, marker now `[redirected-from:dispatch-ticket]`. `mobilize-chores` step 5 collapses to a uniform dispatch — every confirmed ticket → `Agent(teamwork:build-lead)` regardless of kind — and its `allowed-tools` sheds the verbs the absorbed task path used (`gh issue edit/close`, `Skill`); its NOT-done line now names re-growing per-kind routing in the sweep as the regression. `/build-feature` keeps its name and feature-flavored charter (ADR-0010 Decision 4 defers the command rename as a separate call); body repointed. G8's `already-shipped` phantom-name warn fixed in passing (reworded prose). Executed per the rename playbook (ADR-0007 Decision 2 / ADR-0009): `git mv` + frontmatter same-change (F9/A6), live references swept (docs' file-feature `[nested-intake]` pointer — docs 1.2.1; harness's agent-writing-rules three-piece worked example, dated in place — harness 3.1.12), ledger history untouched, `renames.json` re-derived. `dispatch-ticket` inherits `dispatch-feature`'s deliberate no-eval-suite disclosure (1.3.0: reached by name only, no genuine trigger prompts exist — fabricating them would be dishonest test data; the G7 warn stays accepted). Four fresh-context reviews (agent-checker, skill-checker ×2, wiring-checker) found and this change fixed pre-ship: a kindless-record default arm the rewrite had dropped (restored to the pre-ADR-0010 everything-else-builds behavior), the clarified brief missing from the task dispatch's seal, a phantom clarify round claimed on the unattended path in three surfaces (no round runs where there is no one to ask — the confirm round now flags under-specified tasks so the human declines them before paying a dispatch that will skip), the bug path's return channel moved from the fork's transcript to the RECORD read-back (fork-from-agent synchronous return is an unverified platform assumption, same flagged class as docs 1.2.0's), the depth-3 justification extended to the build-lead caller, and step 5's independence clause bounded (mutating dispatches serialize or take worktree isolation — independence is not a parallelism license). Issue #151's never-fired verification transfers to the renamed seat, noted on the issue · v1.4.1 · assembled 2026-08-09 · 1.4.1: closes issue #139 — the platform's `EnterWorktree` isolation guard binds git commands but not a compound Bash command that `cd`'s (or `-C`/`--prefix`'s) into the shared primary checkout and then runs an arbitrary mutating command in the same call (disclosed by a seat 2026-08-08 running `cd <primary> && node scripts/build/components.mjs`; harmless that instance, md5-verified idempotent). The prior investigation (2026-08-08 comment) called this "not repo-actionable" without checking whether a `PreToolUse` hook could mitigate it repo-side; re-investigated for real: `hook-writing-rules` confirms a `PreToolUse` hook CAN pattern-match a Bash command string before it runs, and EnterWorktree's own convention (worktrees always live in-repo at `<primary-root>/.claude/worktrees/<name>`, this workspace's CLAUDE.md) means the primary-root boundary is derivable purely from the event's own `cwd` string — no external config needed, which is what makes this different from the earlier dead-end. New `scripts/worktree_prebash_guard.py` (`PreToolUse`/`Bash`) resolves `cd`/`-C`/`--prefix` targets (literal, relative via `normpath`, `~`-expanded) against that boundary and emits `permissionDecision: ask` (never a hard block — hook-writing-rules' judgment-in-a-hook antipattern: a rule this shape is wrong often on adversarial input, so it flags for confirmation rather than enforcing). Proven on 9 selftest fixtures incl. the disclosed pattern, a negative control (in-worktree cd must not flag), a string-prefix boundary control (`/repo-backup` must not match `/repo`), a relative-path escape, and a numeric `-C` (ripgrep context flag) non-match. Explicitly disclosed, not silently absorbed: dynamic cd targets (`$(...)`, backticks, `$VAR`) can't be resolved without executing the shell and pass silently (fail-open by design, not fail-closed); a bare `cd <primary>` with no chained command is out of scope (git-only guard already binds plain git ops there); no nested-subshell paren tracking. README map gains the hook row · v1.4.0 · assembled 2026-08-09 · 1.4.0: `/build-feature` runs forked (`context: fork`) by default — the whole find-or-make/size/dispatch/close-loop chain executes off the caller's session/context, so kicking off a build no longer blocks or pollutes the main session. `dispatch-feature` (the engine both `/build-feature` and `feature-lead` invoke) deliberately stays un-forked itself: no double hop from `/build-feature`'s own fork, no needless third hop from `feature-lead`'s already-isolated agent context. `dispatch-feature`'s Phase 1 ambiguity branch now distinguishes a `/build-feature`-initiated call (interactive user present even though forked — forking relieves the caller's session, not the person, and `AskUserQuestion` still reaches them) from a `feature-lead`/`mobilize-chores` dispatch (the batch confirm already spent the user's one gate — nothing sanctioned to ask into, regardless of channel). Named the depth-3 justification on the big/coordinator path (the fork isolates the caller's session; the coordinator isolates the multi-seat delivery chain — two different things being kept separate, not accidental nesting past team-or-solo-rules' default depth ≤ 2). `build-feature` gained an empty-seed precondition guard (the fork carries no conversation history to fall back on for "build the thing we just discussed"). Companion change to docs 1.2.0 (`file-bug`/`file-feature`/`file-task`'s matching `context: fork` + seed-marker protocol) — `dispatch-feature` now emits the shared `[redirected-from:dispatch-feature]`/`[nested-intake]` markers when handing a bug-shaped ticket to `file-bug` or running `file-feature`'s intake, since a forked receiver can no longer infer the hand-over from conversation history. Independent fresh-context reviews (skill-checker × 2 on `build-feature`/`dispatch-feature`, wiring-checker on the cross-plugin composition) found and fixed: an overclaimed "reaches the user anywhere in the chain" phrasing narrowed to what's actually proven, the no-fork invariant's rationale added to `dispatch-feature` itself (previously lived only in `build-feature`'s body), and an unverified `AskUserQuestion`-from-agent mechanism claim softened to lean on the policy reason (the batch confirm already spent the gate) instead · v1.3.0 · assembled 2026-08-09 · 1.3.0: closes issue #135 — `mobilize-chores` step 5's feature branch could only name `/build-feature <id>` as a next command, never actually dispatch it, because `build-feature`'s `disable-model-invocation: true` blocks Skill-tool invocation AND agent preload alike (the same flag bites twice). Decomposed via `break-down-problem` (technical-architecture domain, plan mode, 4 nodes/9 actions, `coverage_check.py` clean) before building: split `build-feature` into (a) the unchanged human-typed command shell, now a thin delegator, and (b) `dispatch-feature`, a new `disable-model-invocation: false` skill carrying the actual find-record/size/dispatch/close-loop procedure verbatim — the two entry points share one procedure instead of duplicating it, so they can't drift apart. New agent `feature-lead` (mirrors `chore-lead`/`sweep-chores`) preloads `dispatch-feature` and is the Agent-tool-reachable twin `mobilize-chores` step 5 now actually dispatches for a confirmed `kind: feature` ticket, returning the same typed result a human running `/build-feature <id>` would see. One real behavioral addition beyond the pure split: `dispatch-feature`'s Phase-1 ambiguous-match branch now names an unattended-context fork (report as a blocker instead of asking) since `feature-lead` has no interactive user, unlike a human typing the command directly. `dispatch-feature` deliberately carries no eval suite — G7's E5 floor wants ≥5 genuine "trigger" prompts, but this skill has none by design (reached by name only, from `build-feature`'s body or `feature-lead`'s preload — its own description says so); fabricating positive cases to clear the warning would be dishonest test data, so the warning is accepted and disclosed here instead. README map gains rows for `dispatch-feature` and `feature-lead`; `build-feature`'s row corrected to describe the delegator it now is · v1.2.2 · assembled 2026-08-09 · 1.2.2: `close-session` step 2 now invokes `file-leftovers` (docs) instead of judging what's real from its own ad hoc read (issue #133, filed 2026-08-08 after a live session: real leftover work kept getting missed unless the user manually asked "anything not accounted for?" after every close-out). `file-leftovers`' own contract already covers what step 2 did by hand — evidence-quoted candidate table, one batched clarification round, mint-on-approval through the owning intake skill (`file-bug`/`file-feature`/`file-task`, dedup and payload contract included) — so the direct `file-bug`/`feature`/`issue` call step 2 used to make is now indirect, via `file-leftovers`' own Phase 4. Folded into step 2 rather than a new numbered step (the ticket's own Scope left this an implementation call; file-leftovers fully subsumes what step 2's judgment sub-task did, so a separate step would only duplicate it). The unattended/scheduled failure branch now names `file-leftovers` specifically (its own contract: no interactive channel → deliver the table, minting waits) instead of the old generic "file-bug/feature run find-intent's round" phrasing. References table gains a `file-leftovers` row; the `file-bug`/`feature`/`issue` row now notes it's reached indirectly. Body-only, no description edit, no suite re-judge owed (evals.json is pure trigger-routing, unaffected by an internal-behavior change) · v1.2.1 · assembled 2026-08-09 · 1.2.1: `mobilize-chores`' ticket-discovery step was hardcoded to `gh issue list` — found while reviewing this repo's own Git/ticketing practices against a community discussion on issue-tracker hygiene. `file-bug`, the skill it dispatches bug-kind tickets to, already resolves this workspace's backend via `doc-writing-rules`' three-way resolver (local `docs/tickets/`, git-native `gh issue`, or an Option-C adapter like Linear); `mobilize-chores`' own step 2 never called it, so a repo ruling Option A or C would silently see "0 tickets mobilizable" every run regardless of a real backlog. Step 2 now resolves the backend first and branches: git-native keeps the existing `gh issue list`/GraphQL logic unchanged; local scans `docs/tickets/*.md` frontmatter for `status: open` + a recognized `kind` (no in-flight-PR check exists for local tickets — no linking convention exists yet, disclosed as a named limitation rather than silently skipped); Option C has no listing primitive in the seven-operation adapter interface yet, so it reports UNMEASURED naming the adapter instead of returning a false zero. Step 5's task-kind write-back contract (`gh issue comment`/`gh issue close`) was the same git-native-only assumption — generalized to name the write-back verb per the resolved backend, mirroring `file-bug`'s own Phase 6 status verbs. Description trimmed to stay under the 1024-char portability ceiling after the edit. Not exercised against a live Option-A or Option-C repo (this workspace rules git-native, ADR-0002) — the git-native path is unchanged and already proven; the other two are new, untested against a real repo on those backends · v1.2.0 · assembled 2026-08-08 · 1.2.0: `mobilize-chores` gains `kind: task` mobilization (Kim's explicit request, after the first live sweep reported #138-140 as skipped and he asked why tasks were excluded). Tasks are deliberately heterogeneous (`file-task`'s own scope: chores, follow-ups, research items, debts) — no fixed dispatch verb like `build-feature`/`file-bug` fits them, so the shape is clarify-then-dispatch: a confirmed task ticket runs `find-intent` first (its own one-round cap, only fires when genuinely ambiguous), then dispatches via the `Agent` tool (`general-purpose` as the null-unit default, per `team-or-solo-rules`' own solo-first doctrine) under the same Findings-write-back contract `file-bug`'s own investigation dispatch uses — a Findings entry landed advances status (`doing`/`done`+close/`wontfix`+close), none landed gets one re-dispatch before recording the loss. A task still unclear after `find-intent`'s round is reported skipped, never dispatched blind. Considered and rejected two lighter shapes (blind dispatch per task, size:small-only gating) before Kim chose clarify-then-dispatch. Fresh-context `skill-checker` re-audit (semantic edit, same discipline as the original ship) found one major finding (the fork-vs-agent purge missed `intent.md`'s living-spec text after `SKILL.md` was already corrected to a concrete Agent-tool description) and three minor (missing `gh issue close` in `allowed-tools`, a null-unit-reasoning citation pointing at the wrong skill, a misquote of `file-task`'s scope) — all fixed same-pass · v1.1.2 · assembled 2026-08-08 · 1.1.2: fixes issue #137 (found via /mobilize-chores' first real live sweep) — `close-session` step 1 gains a fourth axis: a multi-seat session's own branch/worktree residue. The prior three axes (uncommitted diff, unpushed current branch, one open PR) never see a session's OTHER local branches, merged-but-undeleted remote branches, or extra worktrees — live evidence: a session verdicted "clean on all three" while 19 merge-verified-but-undeleted local branches and a stale remote branch from its own seats sat unaccounted for. The residue axis is now ALWAYS checked and ALWAYS named in the verdict (found, or explicitly none) — a gated reaper script where the host repo has one, else a plain `git worktree list`/`git branch --merged` fallback — and runs even unattended (read-only, no human gate needed). Output contract, Done-when, an unattended-context failure branch, and References all updated; "clean" now covers four axes, not three. Body-only, no description edit, no suite re-judge owed · v1.1.1 · assembled 2026-08-08 · 1.1.1: fixes issue #134 — `mobilize-chores` step 1's own live first run (2026-08-07) proved a real defect the shipping audit missed: `Run /sweep-chores` is unexecutable as written, since `sweep-chores` is `disable-model-invocation: true` and cannot be reached via the Skill tool from inside another skill's procedure — every run hit the error and silently recovered only because the model happened to reconstruct `sweep-chores`'s own wrapped `chore-lead` dispatch on its own, undocumented. Step 1 now names that dispatch explicitly (Agent tool, `subagent_type: "harness:chore-lead"`, same contract `sweep-chores`'s own body already documents) instead of the impossible Skill-tool call; `Agent` added to `allowed-tools`. Found the identical defect class lurking in step 5's feature branch while fixing this (`build-feature` is ALSO `disable-model-invocation: true`, but unlike `chore-lead` has no single wrapped agent to substitute) — filed separately as issue #135 rather than silently patched, since the right fix is a design call, not a mechanical one; step 5 now names this as an explicit known limitation (reports the confirmed ticket id + the exact next command) instead of failing silently or guessing an unverified invocation path. Description and Done-when corrected to stop overclaiming an automatic feature-ticket dispatch that doesn't exist yet · v1.1.0 · assembled 2026-08-07 · 1.1.0: new command `/mobilize-chores` — closes the gap between "queued" and "done": harness's `/sweep-chores` produces a prioritized ops queue and stops; nothing acted on it, a human had to manually read the queue and invoke the right build dispatch per item. `mobilize-chores` wraps `/sweep-chores` (calls it, never reimplements its fan-out — deliberately: `chore-lead`'s own charter is coordination-only, and folding execution into it would break the unattended-safety guarantee every existing caller relies on), finds open `feature`/`bug`-labeled tickets with no PR already in flight, gets ONE batched human confirm, then dispatches each by its own kind — feature to `/build-feature`, bug to `/file-bug` (which explicitly redirects bug-kind tickets away from `build-feature` — a real correction caught mid-draft, not assumed). Forged through the full `/make-skill` loop: intent interview (7 slots), a live baseline (a skill-less agent skipped the confirm gate on its own risk judgment and used an ad hoc "Owner field" heuristic — both now hard-blocked by design), fresh-context `skill-checker` audit caught ONE real blocking finding pre-ship (`gh issue view --json linkedBranches`/`gh pr list --search "linked:<id>"` are both fictional against real `gh`) — fixed, then RE-verified live and caught a SECOND real gotcha the fix itself introduced (`gh issue view --json closedByPullRequestsReferences` silently drops the `state` field entirely; only the `gh api graphql` form carries it), proven end-to-end against this repo's own live issue #131. `sweep-chores` and `build-feature` both gained a one-line discoverability mention (no suite re-judge owed — all three siblings are `disable-model-invocation: true`, command-only, zero model-routing collision possible) · v1.0.11 · assembled 2026-08-07 · 1.0.11: two skills gain the session-boundary/report-trust doctrine from a live incident (2026-08-05, chore-lead sweep) — a coordinating session dispatched chore-lead, which itself dispatched three seats; those seats' genuine reports also broadcast team-wide to the coordinating session (not chore-lead specifically), which relayed them (paraphrased, then verbatim) to chore-lead; chore-lead correctly refused both, holding for its own direct completion. team-or-solo-rules' best-practices gains "The return channel doesn't survive the session" — a background dispatch's notification reaches only the live dispatching session and dies with it, so a durable-effect dispatch (PR/branch/ticket) must be discoverable from that state alone, not solely from having witnessed the notification; the fix pattern is a standing ground-truth sweep (repo-cleaner/chore-lead), not tighter notification plumbing or a one-off session-scoped cron nobody re-arms. parallel-work-rules' "verify independently" rule extended with a third worked example: a relay — even accurate, even verbatim, even from your own dispatcher — is not your own direct completion for a worker you spawned. Body/reference-only both skills, no description edits, no suite re-judge owed · v1.0.10 · assembled 2026-08-05 · 1.0.10: parallel-work-rules' References table gains a pointer to harness's silent-failure-catalog's new sixth entry (the dispatch-sandbox-redirect incident, issue #125/PR #126) — a dispatched subagent's own success report doesn't prove its `Write` landed in the checkout the dispatching session will next read; this skill owns the isolation-DECISION doctrine, the catalog owns the failure-CLASS doctrine, now cross-referenced instead of siloed. save-lessons harvest, reference-table row only, no description edit, no suite re-judge owed · v1.0.9 · assembled 2026-07-30 · 1.0.9: docs' file-leftovers fence closure — close-session's suite gains the ticket-minting no-trigger (n13: 'Did we drop anything this session? Turn it into tickets.'); suite case only, no description change · v1.0.8 · assembled 2026-07-30 · 1.0.8: ADR-0009 find-intent-rename sweep — live references rewritten (grill-the-ask's fence + references, close-session pointer, suite owner comments; harness's find-the-ask → find-intent); grill-the-ask itself keeps its name per the ADR ("the ask" stays legal where it IS the thing being grilled); pointer updates only, ledger history untouched · v1.0.7 · assembled 2026-07-25 · 1.0.7: description diet (PR #92) — 6 agent descriptions: NOT-for prose trimmed to the routing contract (issue #80 completion) · v1.0.6 · assembled 2026-07-25 · 1.0.6: retired the stale ADR-0006 transition-table section — dead since ADR-0007 (2026-07-21) renamed every plugin dir to its plugin name and retired the workspace CLAUDE.md alias table it pointed to; replaced with the one true line, directories align with plugin names (ADR-0007); no other prose changed · v1.0.5 · assembled 2026-07-23 · 1.0.5: /build-feature reachable again — the dir and every reference said build-feature but frontmatter still carried the pre-rename name: build (the sixth instance of the #84 unreachable-command class, found during a naming-symmetry audit); the class is now extinct by construction — harness 2.0.10's F9/A6 lint FAILs on any name/dir drift at write time and at the gate · v1.0.4 · assembled 2026-07-22 · 1.0.4: the #79 description diet — six teamwork descriptions trimmed suite-aware (3,663 → ~2,100 chars incl. the two single-line-format skills the first sweep missed); team-or-solo-rules' whole-corpus-audit fence restored with its two verbatims after the trim's leak surfaced in the re-judge (n08/n09 healed to none). loop-rules t06 annotated as single-judge noise, at floor. Wave-boundary proof on the full 98-skill estate menu: teamwork suites clean apart from that annotated flip · v1.0.3 · assembled 2026-07-21 · 1.0.3: ADR-0007 dir alignment — the plugin's directory renamed to its plain plugin name (was the frozen `orchestration 0.1.0`); version-suffixed, space-bearing paths retired estate-wide; pointer updates only · v1.0.2 · assembled 2026-07-21 · 1.0.2: ADR-0006 harness-rename sweep — live references rewritten (write-handoff/break-down-problem/find-the-ask pointers across all seats); pointer updates only · v1.0.1 · assembled 2026-07-21 · 1.0.1: ADR-0006 docs-rename sweep — live references rewritten (build-feature/close-session/loop-rules pointers to file-bug/file-feature/file-task, docs plugin mentions); pointer updates only · v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0006 rename PR 7/9 — the PLUGIN renames orchestration → teamwork and seven skills + five agents take the simple paradigm (transition table above; docs-writer keeps). The 0.7.7 exact-name pairing splits by species on purpose: command = verb form (/lead-team), agent = role noun (team-lead). MAJOR bump — names are APIs and this is breaking. Workspace sweep (90 files + ordered context splits for the shared orchestration-coordinator token + a hand pass on the bare plugin token; ledger history and .claude/ops records excluded); baseline blind run 107/108 (concurrency n09 pre-existing); post-rename re-measure 108/108 — parallel-work-rules' n09 healed by the rename itself, and two single-judge flips (close-session n06, team-or-solo-rules n03) healed same-change by carrying the stolen verbatims into the existing fences, re-judged 44/44. Species alignment rode along: the three renamed -rules packs flipped user-invocable true→false (knowledge species is model-only — skill_lint W5, the Phase 0 standard) ·
v0.7.9 · assembled 2026-07-21 · 0.7.9: ADR-0006 screens-rename sweep — code-reviewer's UI-reviewer fences repointed (component-/layout-/flow-checker); pointer updates only · v0.7.8 · assembled 2026-07-20 · 0.7.8: `orchestration-coordinator` agent effort high→xhigh — with
0.7.7's same-named command making the HOST adopt this agent's contract directly, the effort field
now also sets the host's reasoning depth for a charter's routing/gating loop, not just a spawned
seat's. Model stays sonnet per the 0.7.0 seat-ladder reclassification (coordination, not judgment) ·

v0.7.7 · assembled 2026-07-20 · 0.7.7: new `orchestration-coordinator` command skill — makes the
HOST session itself adopt `agents/orchestration-coordinator.md`'s own eight priorities directly for
one stated charter (read from the agent file, never restated inline, so the two can't silently
drift), with no separate agent spawn for the coordinator role; a stated (not tool-walled) discipline
that the host never touches Write/Edit on charter deliverables, dispatching every unit of real work
instead. Deliberately overrides `orchestration-design`'s solo-first default for the charter's
duration — invoking the command IS the scoped choice to force team-shaped delegation regardless of
size, with no escape hatch back to solo mid-charter. Shares its exact name with the agent it adopts
the contract of, the same deliberate pairing ruled for forge's `ops-issues` — inverted here: the
skill there dispatches its same-named agent, this one never does. Independent FLOOR audit
(skill-auditor): 2 majors fixed pre-ship (Phase 2's restatement had silently dropped 7 of 8 priority
sub-clauses vs. the agent source — fixed by pointing at the agent file directly instead of
restating; the host was never told to load `orchestration-design`/`loop-design`, the same two skills
the agent itself preloads — fixed), plus 2 minors (no failure branch for re-invocation mid-open-
charter; bare relative citations to the agent file resolved to `${CLAUDE_PLUGIN_ROOT}` paths) ·

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
