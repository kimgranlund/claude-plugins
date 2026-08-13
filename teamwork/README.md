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
| `skills/team-or-solo-rules` | Declarative skill | both | Design or review how skills, subagents, and teams compose, and the YAML frontmatter that wires them — unit choice (skill/subagent/team), sealed-dispatch discipline, the D2/D4 gate |
| `skills/loop-rules` | Declarative skill | both | Design or review continuation patterns — `/goal`, `/loop`, Stop hooks, auto mode — that decide *when* the next turn fires; the self-orchestrated-looping canon for a delegating loop (budgets, locus escalation, durable state) |
| `skills/parallel-work-rules` | Declarative skill | both | Decide whether concurrent sessions/subagents touching one repo need git-tree isolation, and what to do when they collide anyway — the three-actor classification (spawned subagent / addressable peer session / opaque concurrent session) and the matching response for each |
| `skills/close-session` | Procedural skill | both | Wraps up a session's own worktree before it ends: checks mechanical git state, routes real findings through file-bug/feature/issue, triggers save-lessons's detection pass, verifies every write via read-back, and states a mandatory two-shape verdict |
| `hooks/hooks.json` (`SessionEnd`) | Hook | automatic | Passive safety net for `close-session`: on actual session termination, logs a durable warning line if a git worktree was left dirty or unpushed — `SessionEnd` cannot block, so this never gates, only records |
| `hooks/hooks.json` (`PreToolUse` · `scripts/worktree_prebash_guard.py`) | Hook | automatic | Issue #139's repo-side mitigation: flags (never blocks — `permissionDecision: ask`) a Bash command that `cd`'s or `-C`/`--prefix`'s out of a worktree cwd into the shared primary checkout and then runs a further command in the same call — the compound-command escape the platform's git-only worktree-isolation guard doesn't bind. Detects the primary-root boundary from the worktree cwd's own `.claude/worktrees/` path (no external config needed); dynamic (`$(...)`) targets are a disclosed blind spot, left silent rather than guessed |
| `skills/build-feature` | Command skill | user-only (`/build-feature`) | The human-typed entry point only — delegates its full procedure to `dispatch-ticket` (issue #135: a `disable-model-invocation: true` skill can't be Skill-tool-invoked or preloaded by anything else, so the procedure had to move) |
| `skills/dispatch-ticket` | Procedural skill | model-only | The record-first procedure for one confirmed ticket of ANY kind (ADR-0010, renamed+generalized from `dispatch-feature`): finds or mints the record, then branches by kind — feature → size by the solo-first floors (small → host inline / one sealed fork; big → the floored seats) and build under a mandatory Findings write-back; task → one find-intent round, then a solo-first Agent dispatch under the same contract; bug → hand-off to docs' `file-bug` with the `[redirected-from:]` marker. Reached by name only, from `build-feature`'s own body or the `build-lead` agent's preload — never a direct user ask |
| `agents/build-lead` | Subagent | dispatch-only | The Agent-tool-reachable twin of `/build-feature` generalized to every ticket kind (ADR-0010, renamed from `feature-lead`), preloading `dispatch-ticket` — `mobilize-chores` step 5 dispatches every confirmed ticket here uniformly, mirroring how `chore-lead` (harness) wraps `sweep-chores` |
| `skills/mobilize-chores` | Command skill | user-only (`/mobilize-chores`) | Sweeps the ops queue (wrapping harness's `/sweep-chores` via its `chore-lead` dispatch, never reimplementing it), then drives every mobilizable ticket to `build-lead` uniformly — gated by one batched confirm, or unattended via the explicit `auto` token (a `/goal` loop's entry point; ceiling PR-opened, never merge). Concurrency per the measured rules: 2+ mutating dispatches always take per-dispatch worktree isolation; a named non-overlapping edit-target path decides parallel-vs-serial, never isolation-vs-none. A named blocker gets a classified breakdown paragraph (six shapes, prose-first, commands on request), never just a table row |
| `skills/lead-build` | Command skill | user-only (`/lead-build`) | Makes THIS session the standing build seat: adopts `agents/build-lead`'s contract directly (the `/lead-team` ↔ `team-lead` pattern) — every ticket id or build ask drives through `dispatch-ticket` via the Skill tool (the engine carries no `context: fork`, so it runs inline in this session's own turn) with the interactive branches ALIVE: the Phase-1 ambiguity question and the task clarify round fire live instead of the unattended blocker/SKIPPED. One engine, three entries: forked one-shot (`/build-feature`), unattended seat (`build-lead`), live standing seat (this) |
| `skills/lead-review` | Command skill | user-only (`/lead-review`) | Makes THIS session a standing review desk — the family's one deliberately agent-less member: the estate's eleven fresh-context checkers ARE the review capacity, so the desk routes each target to its owning checker (sealed dispatch, FLOOR/DEEP depth carried, verdict-first relay) and never grades anything itself — dispatch-only IS generator≠critic made structural. Self-authored targets get a NEUTRAL dispatch with authorship disclosed at relay |
| `skills/init-repo` | Command skill | user-only (`/init-repo`) | The /lead-* family's composer — one command arms a work session: conditional built-in `/init`, direct team-lead adoption (the session IS the charter — /lead-team's mechanism, carried here because dmi:true blocks Skill-invoking it), the standing INTAKE sibling spawned (docs' intake-lead; its missing-seed return IS the liveness ack, zero contract-bending), and per-ticket build-lead capacity wired (no idle standing build spawn — the seat's own one-ticket contract). Per-session: siblings die with the session; re-run each sit-down |
| `skills/lead-team` | Command skill | user-only (`/lead-team`) | Makes THIS host session adopt `agents/team-lead.md`'s own contract directly for one stated charter — no separate agent spawn, deliberately overrides team-or-solo-rules's solo-first default for the charter's duration; paired with the seat it imports per ADR-0006's species split — command = verb form (`/lead-team`), agent = role noun (`team-lead`); like harness's `issue-sorter` pairing, inverted (host adopts, never dispatches) |
| `agents/lead-team` | Subagent | dispatch-only | The apex seat: chain-of-command, dispatch order, the review gate between phases, the discovered-reality escalation loop, rollups to the host |
| `agents/planner` | Subagent | dispatch-only | The design seat: decomposes a problem across both planes, authors/maintains PRD/SPEC/LLD/ADR |
| `skills/lead-planning` | Command skill | user-only (`/lead-planning`) | Makes THIS session adopt `agents/planner.md`'s own contract directly for one named planning charter — fifth `/lead-*` member, paired per ADR-0006's species split (command = verb form `lead-planning`, agent = role noun `planner`). Write discipline INVERTS relative to `/lead-team`: authoring the PRD/SPEC/LLD/ADR the charter earns is this seat's own deliverable, so the host writes them directly — but never grades one it wrote: every authored/revised doc rides to `docs:doc-checker` fresh-context, review-by-hand against `doc-writing-rules`' rubric where docs isn't installed. Roll-up audience is the invoking human; closes on a named `loop-rules` decision |
| `agents/builder` | Subagent | dispatch-only | The build seat: implements an approved LLD's build sequence, runs mechanical checks, escalates design conflicts rather than editing the contract |
| `agents/docs-writer` | Subagent | dispatch-only | Owns a documentation site: derives pages from their canonical source, makes drift a failing gate, reports soft drift a static check can't see |
| `agents/code-checker` | Subagent | dispatch-only | Independent critic for one bounded code change, scored against the contract it was built to; generator ≠ critic for the delivery loop |
| `agents/wiring-checker` | Subagent | dispatch-only | Independent critic for how skills/subagents/teams compose and the frontmatter that wires them, scored against `team-or-solo-rules`'s rubric; a real gap closed post-migration (see below) |

## Construction note: hard cross-plugin preloads converted to soft mentions

Every one of the five ported agents carried a `skills:` frontmatter preload into skills that no
longer live in this plugin boundary. Fixing this was the bulk of the porting work:

- **`team-lead`** preloaded `write-handoff` (now in harness). Dropped from the
  preload list; the body now soft-mentions harness's `write-handoff` block with an inline
  Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action
  fallback wherever it names a handback. `skills:` is now `[team-or-solo-rules, loop-rules]` —
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

v2.9.4 · assembled 2026-08-13 · 2.9.4: `worktree_prebash_guard.py` gains sibling→sibling
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
