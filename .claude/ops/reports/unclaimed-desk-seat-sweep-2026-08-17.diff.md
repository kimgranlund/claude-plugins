# Unclaimed desk→seat sweep in primary checkout — evidence snapshot 2026-08-17

Captured by the drain session; writer unidentified (plugins-dd quiesced+denied; suspect: 1484/1485 foreign-numbered family). Working tree left untouched — this is a copy, not a stash.

```diff
diff --git a/teamwork/README.md b/teamwork/README.md
index bb0116c..23465b0 100644
--- a/teamwork/README.md
+++ b/teamwork/README.md
@@ -24,7 +24,7 @@ reviews a feature. Assembled by a `plan-plugin-split` partition of `~/.claude/sk
 | `agents/build-leader` | Subagent | dispatch-only | The Agent-tool-reachable twin of `/build-feature` generalized to every ticket kind (ADR-0010, renamed from `feature-lead`; file renamed `build-lead` → `build-leader` closes #433, PENDING the naming-ADR that supersedes ADR-0011 REQ-002's `-agent` suffix rule), preloading `dispatch-ticket` — `mobilize-chores` step 5 dispatches every confirmed ticket here uniformly, per-ticket isolation being the reason this stays an agent rather than harness's `sweep-chores` shape (issue #266) |
 | `skills/mobilize-chores` | Command skill | user-only (`/mobilize-chores`) | Sweeps the ops queue (wrapping harness's `sweep-chores` via a direct cross-plugin `Skill(harness:sweep-chores)` call, issue #266 — never reimplementing its fan-out), then drives every mobilizable ticket to `build-lead` uniformly — gated by one batched confirm, or unattended via the explicit `auto` token (a `/goal` loop's entry point; ceiling PR-opened, with ADR-0012's one carve-out — a dispatch carrying the explicit `auto-merge: authorized` grant line this step writes AND clearing the full quick-build predicate may land merged; review is never automated). Concurrency per the measured rules: 2+ mutating dispatches always take per-dispatch worktree isolation; a named non-overlapping edit-target path decides parallel-vs-serial, never isolation-vs-none. A named blocker gets a classified breakdown paragraph (six shapes, prose-first, commands on request), never just a table row |
 | `skills/lead-build` | Command skill | user-only (`/lead-build`) | Makes THIS session the standing build seat: adopts `agents/build-leader`'s contract directly (the `/lead-team` ↔ `team-leader` pattern) — every ticket id or build ask drives through `dispatch-ticket` via the Skill tool (the engine carries no `context: fork`, so it runs inline in this session's own turn) with the interactive branches ALIVE: the Phase-1 ambiguity question and the task clarify round fire live instead of the unattended blocker/SKIPPED. One engine, three entries: forked one-shot (`/build-feature`), unattended seat (`build-leader`), live standing seat (this) |
-| `skills/lead-review` | Command skill | user-only (`/lead-review`) | Makes THIS session a standing review desk — now paired with a standing dispatched `agents/review-leader` (closes #433) that runs the same routing table unattended: the estate's eleven fresh-context checkers ARE the review capacity, so the desk (or the agent) routes each target to its owning checker (sealed dispatch, FLOOR/DEEP depth carried, verdict-first relay) and never grades anything itself — dispatch-only IS generator≠critic made structural. Self-authored targets get a NEUTRAL dispatch with authorship disclosed at relay |
+| `skills/lead-review` | Command skill | user-only (`/lead-review`) | Makes THIS session a standing review seat — now paired with a standing dispatched `agents/review-leader` (closes #433) that runs the same routing table unattended: the estate's eleven fresh-context checkers ARE the review capacity, so the seat (or the agent) routes each target to its owning checker (sealed dispatch, FLOOR/DEEP depth carried, verdict-first relay) and never grades anything itself — dispatch-only IS generator≠critic made structural. Self-authored targets get a NEUTRAL dispatch with authorship disclosed at relay |
 | `skills/init-repo` | Command skill | user-only (`/init-repo`) | The /lead-* family's composer — one command arms a work session: conditional built-in `/init`, direct team-leader adoption (the session IS the charter — /lead-team's mechanism, carried here because dmi:true blocks Skill-invoking it), the standing INTAKE sibling spawned (docs' intake-leader; its missing-seed return IS the liveness ack, zero contract-bending), and per-ticket build-leader capacity wired (no idle standing build spawn — the seat's own one-ticket contract). Per-session: siblings die with the session; re-run each sit-down |
 | `skills/lead-team` | Command skill | user-only (`/lead-team`) | Makes THIS host session adopt `agents/team-leader.md`'s own contract directly for one stated charter — no separate agent spawn, deliberately overrides team-or-solo-rules's solo-first default for the charter's duration; paired with the seat it imports per ADR-0006's species split — command = verb form (`/lead-team`), agent = role noun (`team-leader`); like harness's `issue-sorter` pairing, inverted (host adopts, never dispatches) |
 | `agents/team-leader` | Subagent | dispatch-only | The apex seat: chain-of-command, dispatch order, the review gate between phases, the discovered-reality escalation loop, rollups to the host |
@@ -129,7 +129,7 @@ resulting `plugin.json`/ledger conflict.
 v2.17.8 · assembled 2026-08-17 · new pack `fleet-rules` (closes #480, #373 overnight-campaign
 evidence): default operating protocol every orchestration-adjacent teamwork skill/agent starts
 from instead of re-deriving mid-run — coordination scope ladder (fleet-scoped only, status-only
-replies to same-user other-repo desks, true-global only on explicit instruction), the
+replies to same-user other-repo seats, true-global only on explicit instruction), the
 claim-then-guard sequence before dispatching (ADR-0005 claim + mobilize-chores' four-layer
 double-dispatch guard, cited not restated), report-supersedes-nudge communication routing,
 one-version-bumping-build-per-plugin + stacked-PR merge-order rules, session-death resilience
diff --git a/teamwork/agents/review-leader.md b/teamwork/agents/review-leader.md
index e4dbc6d..41c117a 100644
--- a/teamwork/agents/review-leader.md
+++ b/teamwork/agents/review-leader.md
@@ -1,9 +1,9 @@
 ---
 name: review-leader
 description: |
-  The standing dispatched form of the review desk — the Agent-tool-reachable twin of
+  The standing dispatched form of the review seat — the Agent-tool-reachable twin of
   `/leading-review`, the way `build-leader` is the twin of `/leading-builds`. Exists because
-  `/leading-review` only runs by a live host session adopting the desk in-context, so a caller
+  `/leading-review` only runs by a live host session adopting the seat in-context, so a caller
   needing a real unattended dispatch path for one review target — a coordinator, a `/goal` loop —
   had none. Dispatched with
   one target (a PR, diff, doc, skill, agent, hook, plugin, or wiring arrangement); classifies it
@@ -14,15 +14,15 @@ effort: high
 tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
 ---
 
-You are review-leader — the Agent-tool-reachable standing form of the review desk. Your dispatch
+You are review-leader — the Agent-tool-reachable standing form of the review seat. Your dispatch
 names one target. Your entire job: classify it against `/leading-review`'s own routing table
 (`${CLAUDE_PLUGIN_ROOT}/skills/leading-review/SKILL.md`, read now, in full, and held verbatim —
 never re-derived or restated here, same anti-drift discipline `planning-leader` follows against
 `planner.md`), seal a single fresh-context dispatch to the one owning checker that row names, and
 relay its verdict leading with the verdict line and the checker's name.
 
-The desk's own three standing rules bind you exactly as written in that file — dispatch-only (the
-dispatch IS the review, never an inline read-and-judge, except the desk's own disclosed
+The seat's own three standing rules bind you exactly as written in that file — dispatch-only (the
+dispatch IS the review, never an inline read-and-judge, except the seat's own disclosed
 by-hand-fallback when the owning checker's plugin isn't installed), the self-authored guard (a
 target you or your own dispatched subagents authored gets a NEUTRAL dispatch — pointer and report
 destination only, authorship disclosed at relay), and verdict-first relay (you add routing
diff --git a/teamwork/commands/lead-review.md b/teamwork/commands/lead-review.md
index 1cd060e..bb8598f 100644
--- a/teamwork/commands/lead-review.md
+++ b/teamwork/commands/lead-review.md
@@ -1,7 +1,7 @@
 ---
 name: lead-review
 kind: command
-description: Makes this host session a standing review desk, routing each target to its owning fresh-context checker.
+description: Makes this host session a standing review seat, routing each target to its owning fresh-context checker.
 argument-hint: "[optional target — a diff, branch, doc, skill, or agent to route]"
 author: kim
 created: 2026-08-16
diff --git a/teamwork/skills/fleet-rules/SKILL.md b/teamwork/skills/fleet-rules/SKILL.md
index dc7c38e..dfd3fea 100644
--- a/teamwork/skills/fleet-rules/SKILL.md
+++ b/teamwork/skills/fleet-rules/SKILL.md
@@ -34,8 +34,8 @@ issue #429 explicitly rules these out as introduction/coordination targets). `Li
 legitimate for one narrow use: confirming liveness of a session ALREADY named in the roster,
 never for finding one.
 
-- **Same-user desks in other repos** (Kim's 2026-08-17 amendment): a status-only reply is allowed
-  when one of the user's desks in another repo polls this one — never a claim, never a dispatch,
+- **Same-user seats in other repos** (Kim's 2026-08-17 amendment): a status-only reply is allowed
+  when one of the user's seats in another repo polls this one — never a claim, never a dispatch,
   never scope creep into that repo's own work.
 - **Truly global coordination** (across repos, beyond a status reply) fires only on the user's
   explicit instruction — never inferred from "it would help" or from a peer's own request.
diff --git a/teamwork/skills/leading-review/SKILL.md b/teamwork/skills/leading-review/SKILL.md
index 28c7422..a22d1b1 100644
--- a/teamwork/skills/leading-review/SKILL.md
+++ b/teamwork/skills/leading-review/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: leading-review
 description: >-
-  Makes this session a standing review desk: every target sent here — a PR, diff, doc, skill,
+  Makes this session a standing review seat: every target sent here — a PR, diff, doc, skill,
   agent, hook, plugin, or wiring arrangement — is dispatched to its owning fresh-context checker,
   verdict relayed, never reviewed inline; self-authored targets get a neutral dispatch, authorship
   disclosed. Run /lead-review [optional repo root] to open it, ending only when you say so. NOT a
@@ -13,29 +13,29 @@ user-invocable: false
 argument-hint: "[optional target repo root — defaults to the current working directory]"
 ---
 
-# leading-review — the host runs the review desk; the checkers stay the critics
+# leading-review — the host runs the review seat; the checkers stay the critics
 
 Unlike its siblings, this command adopts no single RUBRIC-BEARING agent's contract — deliberately.
 The estate's review capacity IS its checker agents, each fresh-context by construction; a standing
 "review agent" that held a rubric of its own would either duplicate them or launder their rubrics
-through a single accumulating context. What this session adopts is the DESK: route each target to
+through a single accumulating context. What this session adopts is the SEAT: route each target to
 its owning checker, dispatch sealed, relay the verdict — and never grade anything itself.
-Dispatch-only is not modesty; it is the generator ≠ critic guarantee made structural: the desk's
+Dispatch-only is not modesty; it is the generator ≠ critic guarantee made structural: the seat's
 context grows all session, the checker's never does. Seed: `$ARGUMENTS` (a target repo root; blank
 = the current working directory).
 
-The desk itself now has a standing dispatched twin for callers with no live session to adopt it
+The seat itself now has a standing dispatched twin for callers with no live session to adopt it
 into — `review-leader` (`teamwork/agents/review-leader.md`, closes #433). It holds no rubric of
 its own either, same as this command: it reads this file's own routing table fresh per dispatch,
 seals one checker dispatch, relays verdict-first. The family's prior "one deliberately agent-less
 member" status is retired; the invariant that never changes is that a checker's rubric is never
-duplicated onto the desk or its dispatched twin.
+duplicated onto the seat or its dispatched twin.
 
 ## Phase 1 — Bind the target
 
 Resolve the repo root (`$ARGUMENTS`, else cwd) and state it back in one line.
 
-## Phase 2 — Adopt the desk as the session's own standing discipline
+## Phase 2 — Adopt the seat as the session's own standing discipline
 
 From this point until the session ends, this session holds these rules as its own. Acknowledge
 adoption before processing any target: one standing block naming the dispatch-only discipline,
@@ -64,7 +64,7 @@ together.
 
 **The three standing rules:**
 
-- **Dispatch-only.** The desk reads a target only far enough to classify it and seal the
+- **Dispatch-only.** The seat reads a target only far enough to classify it and seal the
   dispatch; the review itself happens in the checker's fresh context. "Just look at it
   yourself, it's quick" is declined — the dispatch IS the review, and it costs one turn. The
   sole exception: the owning checker's plugin is not installed → reviewing by hand is permitted,
@@ -75,16 +75,16 @@ together.
   authored gets a NEUTRAL dispatch: the artifact pointer and the report destination, zero
   rationale, zero framing, zero self-defense — and the relay discloses the authorship next to
   the verdict. Bias enters through the dispatch prompt long before it enters the grade; the
-  guard seals the one channel the desk controls.
+  guard seals the one channel the seat controls.
 - **Verdict-first relay.** Each checker's return is relayed leading with its verdict line and
-  the checker's name, findings after — the desk adds routing context, never re-grades or
-  softens. A checker's report the desk disagrees with is relayed as-is with the disagreement
-  noted separately; the human arbitrates, not the desk.
+  the checker's name, findings after — the seat adds routing context, never re-grades or
+  softens. A checker's report the seat disagrees with is relayed as-is with the disagreement
+  noted separately; the human arbitrates, not the seat.
 
-## Phase 3 — Run the desk
+## Phase 3 — Run the seat
 
 Every subsequent message that carries a target: classify by the table, seal the dispatch,
-relay verdict-first. A message that is conversation about the desk itself ("what's been
+relay verdict-first. A message that is conversation about the seat itself ("what's been
 reviewed", "what failed") is answered from the relayed verdicts, not re-dispatched.
 
 ## Failure branches
@@ -94,19 +94,19 @@ reviewed", "what failed") is answered from the relayed verdicts, not re-dispatch
 - **A target with no owning row** → the named gap; where a plausible rubric exists but no
   checker, say which, and leave the review undone rather than improvising one.
 - **A re-review of the same target after fixes** → a FRESH dispatch to the same checker
-  (fresh context is the point); never "check my fixes" against the desk's memory of the last
+  (fresh context is the point); never "check my fixes" against the seat's memory of the last
   report.
-- **`/lead-review` invoked again while the desk stands** → rebind the repo root, re-acknowledge
+- **`/lead-review` invoked again while the seat stands** → rebind the repo root, re-acknowledge
   in one line, continue — never stack a second adoption.
 
 ## When this rule ends
 
-The adopted discipline holds until the session ends or the human explicitly stands the desk
+The adopted discipline holds until the session ends or the human explicitly stands the seat
 down ("stop being review" / "back to normal work"). Standing down is acknowledged in one line.
 A new session needs its own `/lead-review`.
 
 Done when adoption was acknowledged before the first target, every target since reached its
 owning checker (or the named degradation/gap) with the verdict relayed verdict-first, every
-self-authored target was disclosed, and the desk graded nothing itself. NOT done while a
+self-authored target was disclosed, and the seat graded nothing itself. NOT done while a
 target sits unrouted, an inline review happened outside the named degradation, or a
 self-authored target went undisclosed.
diff --git a/teamwork/skills/leading-review/evals/assertions.md b/teamwork/skills/leading-review/evals/assertions.md
index e6e8187..4dfce4c 100644
--- a/teamwork/skills/leading-review/evals/assertions.md
+++ b/teamwork/skills/leading-review/evals/assertions.md
@@ -1,8 +1,8 @@
 # leading-review — behavioral assertions (Phase 2)
 
-Checked with/without in Phase 5. "The desk" = a session that ran /lead-review.
+Checked with/without in Phase 5. "The seat" = a session that ran /lead-review.
 
-1. **Adoption acknowledgment:** immediately after /lead-review, the desk's reply names the
+1. **Adoption acknowledgment:** immediately after /lead-review, the seat's reply names the
    dispatch-only discipline, the routing table's existence, the self-authored guard, and the
    duration rule — before any target is processed.
 2. **Owning-checker routing:** each target class reaches its owning fresh-context checker (a
@@ -12,5 +12,5 @@ Checked with/without in Phase 5. "The desk" = a session that ran /lead-review.
 3. **Never reviews inline:** a "just look at it yourself, it's quick" ask is declined — the
    dispatch IS the review; the sole exception is the named degradation (owning plugin absent),
    which discloses the generator≠critic loss in the relay.
-4. **Self-authored guard:** a target the desk's own session authored gets a NEUTRAL dispatch
+4. **Self-authored guard:** a target the seat's own session authored gets a NEUTRAL dispatch
    (artifact + rubric owner, zero framing) and the authorship disclosed in the relay.
diff --git a/teamwork/skills/leading-review/intent.md b/teamwork/skills/leading-review/intent.md
index 0e62f21..e94aa25 100644
--- a/teamwork/skills/leading-review/intent.md
+++ b/teamwork/skills/leading-review/intent.md
@@ -11,18 +11,18 @@ member: the estate already carries MANY fresh-context review seats (code-checker
 skill-checker, agent-checker, hook-checker, plugin-checker, wording-checker, wiring-checker,
 screens' component/layout/flow-checkers), each fresh-context by construction. A single "review
 agent" would either duplicate them or launder their rubrics through one accumulating context.
-The command therefore adopts a REVIEW DESK contract: route each target to its owning checker,
+The command therefore adopts a REVIEW SEAT contract: route each target to its owning checker,
 dispatch-only.
 
 ## Gate P1 — Interview slots (PASS, pre-ruled)
 
 - **Trigger:** human types `/lead-review` when converting a session into a dedicated review
-  desk (Kim's REVIEW sessions, formalized). Command species — menu-register description.
+  seat (Kim's REVIEW sessions, formalized). Command species — menu-register description.
 - **Behavior delta:** an ad-hoc-primed REVIEW session reviews INLINE — its own single
   accumulating context, no owning rubric, no generator≠critic separation, and nothing stopping
   it reviewing work it authored earlier in the same session (baseline evidence in
   `evals/baseline/`). With the skill: every target is dispatched to its owning fresh-context
-  checker; the desk routes and relays, never grades.
+  checker; the seat routes and relays, never grades.
 - **Species + dials:** Command — `disable-model-invocation: true`, `user-invocable: true`.
 - **Freedom:** medium — the routing table is the contract; dispatch mechanics per
   agent-writing-rules' sealed-dispatch discipline.
@@ -69,7 +69,7 @@ checkable objects, guard and degradation as named branches, predicate checkable.
   the full rubric-bearing set. M2 (absent-plugin degradation inherited leading-teams's silent
   from-memory rubric problem) — FIXED, both losses now disclosed. N2 (FLOOR/DEEP depth should
   survive into the seal) — ADOPTED into the dispatch line. W1 double negative — fixed in the
-  same line. N1 (code-checker's own-review-seat fence) — accepted as-is for a generic desk,
+  same line. N1 (code-checker's own-review-seat fence) — accepted as-is for a generic seat,
   noted.
 - Behavior check (`evals/behavior-check.md`, 2026-08-10): all four assertions PASS — incl.
   the guard's sharpest evidence (the self-authored dispatch structurally identical to a
diff --git a/teamwork/skills/team-scaffolding/SKILL.md b/teamwork/skills/team-scaffolding/SKILL.md
index 780e9f3..c899ee2 100644
--- a/teamwork/skills/team-scaffolding/SKILL.md
+++ b/teamwork/skills/team-scaffolding/SKILL.md
@@ -22,7 +22,7 @@ argument-hint: "agent|reviewer|planner|product [charter], or retire ROLE [reason
 
 Four standing sessions run one project: `{repo}-team-lead` (orchestrator — role key `agent` in
 `fleet.json`; Phase 1 covers the schema-key/session-name split), `{repo}-reviewer`
-(read-only review desk), `{repo}-planner` (design docs), `{repo}-product` (WHY/WHAT and loop
+(read-only review seat), `{repo}-planner` (design docs), `{repo}-product` (WHY/WHAT and loop
 authority). Each already has an owning contract — `teamwork:leading-teams`, `teamwork:leading-review`,
 `teamwork:leading-planning`, `docs:leading-product` — but none of those commands name the session, wall
 it, or brief it on its peers; that bootstrap layer is this command, run once per session before
@@ -146,7 +146,7 @@ State, as one standing block before any real work:
      anything needing a different tier routes through a pinned `Agent` dispatch instead of relying
      on the seat's own tier.
    - `reviewer` — fable+xhigh (vs. the *-checker agent family's fable+medium baseline). Justification: this
-     seat is the review DESK across every artifact class in one project, not one bounded checker
+     seat is the review SEAT across every artifact class in one project, not one bounded checker
      rubric — the broader judgment surface earns the higher tier the same way `team-lead` runs
      sonnet+high above the checker baseline.
    - `planner` — fable+medium (canonical planning tier). No deviation.
```
