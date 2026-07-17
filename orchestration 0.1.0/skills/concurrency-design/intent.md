# intent — concurrency-design
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: high
type: capability-uplift

## trigger
should:      ["should I work in a worktree for this", "another Claude session has uncommitted changes to files I need", "set up this repo so multiple sessions don't collide", "should this subagent use isolation: worktree"]
should_not:  ["should I fan out N subagents for this review"]

## delta
Incident (agent-ui repo, 2026-07-16/17): a dispatched builder subagent, working directly in the
shared git tree (no worktree isolation), was mid-move on a set of files when it discovered a fully
independent, concurrent Claude Code session had uncommitted, in-progress edits to those exact same
files. It was caught only because the subagent happened to notice pre-existing diffs before writing
and paused to ask — not because of any structural practice. Without this skill, a session (main-loop
or dispatched subagent):
- does not default to `EnterWorktree`/the `Agent` tool's `isolation:"worktree"` when concurrent
  sessions are plausible — `EnterWorktree`'s own contract requires an explicit trigger ("the user
  directly, or... project instructions (CLAUDE.md/memory)"), and nothing routes a session into that
  trigger automatically;
- does not treat a long-uncommitted working tree, or another session's fresh-looking diffs, as a
  risk signal to check before starting cross-cutting file-mutating work;
- has no standing habit of checking sibling ticket status (`doing` vs `open`) as a cheap
  coordination signal before touching files a ticket already claims.
If deleted after a month: the next multi-session collision has even odds of being silent instead of
caught — the outcome this incident avoided by luck (a subagent's own noticing), not by design.

## fences
- NOT for a single session's own subagent-vs-solo or fan-out dispatch decisions (orchestration-design)
- NOT for when the next autonomous turn fires — /goal, /loop, Stop hooks, auto mode (loop-design)
- NOT for how to author the hook/agent/entry-file mechanics once a rule is decided
  (hook-authoring-standards / agent-authoring-standards / entry-file-standards, forge) — this skill
  decides WHETHER isolation or commit-cadence is warranted and what to do on collision; those skills
  own HOW to encode the resulting rule

## assertions
1. Given a task that will dispatch 2+ file-mutating subagents/sessions against the same repo, the
   guidance names worktree isolation (`EnterWorktree` or the `Agent` tool's `isolation:"worktree"`)
   as the default to reach for, not an afterthought reached only after a collision.
2. Given a mid-task discovery of another session's uncommitted edits overlapping the current task's
   target files, the guidance produces a stop → independently verify → escalate-to-human sequence —
   never silent edit-around, never silent proceed on an unverified claim from either side.
3. Given a project that regularly runs concurrent Claude Code sessions, the guidance recommends a
   standing CLAUDE.md opt-in rule (since `EnterWorktree` requires explicit instruction) plus a
   commit-cadence practice (small, frequent, gate-green commits), not a per-invocation reminder.
4. The guidance names ticket-status vocabulary (`open`/`doing`/`done`, where a project has one) as a
   cheap coordination signal distinct from and cheaper than worktree isolation.

## gates
P0 route:      PASS — 2026-07-17, knowledge/procedure needed on-demand; not a hook (not fully
                mechanically checkable — the decision of WHEN to isolate is judgment, not pass/fail);
                not an entry-file fact (situational, not always-true every turn); not an agent
                (no tool-wall/parallelism need — this is reasoning guidance for the dispatching
                session itself)
P1 intent:     PASS — 2026-07-17, all 7 slots filled, species/dials/name confirmed by Kim
                (AskUserQuestion, two rounds: plugin home = orchestration, species = knowledge,
                name = concurrency-design, trigger+fence confirmed as drafted)
P2 evals:      PASS — 2026-07-17, evals/evals.json (12 trigger + 8 no-trigger), 3 baseline captures
                (evals/baseline/*.md, fresh general-purpose agents, no tools/repo context)
P3 draft:      PASS — 2026-07-17, SKILL.md ~131 lines (well under 500), description ~1,014 chars
                (under 1,024 cap), dials explicit. Body follows loop-design/orchestration-design's
                actual shape (numbered steps + table + worked example + done-when) — matches their
                species exactly, per the audit's MINOR-2 correction (see rulings): the dial set
                (disable-model-invocation:false, user-invocable:true) + verb name-head + imperative
                body all say procedural, not knowledge; there was no "purity deviation" to defend
P4 language:   PASS — 2026-07-17, potency_lint.py clean (prohibitions within the 5 budget). Zero
                UPPERCASE NEVER/MUST NOT in the shipped body (grep-verified, audit MINOR-3) — the
                surviving lowercase "never" instances are within the lint's own budget, not hard
                gates; several prohibition-dense lines rewritten affirmatively across the language
                pass and the later MAJOR-1 fix
P5 validate:   PASS — 2026-07-17, skill_lint.py clean · fresh-context audit (skill-auditor,
                evals/audit-report.md) PASS with 1 MAJOR + 3 MINOR, all four fixed (see rulings) ·
                behavior check (evals/behavior-check.md) demonstrates assertions 1/2/4 with a
                measurable delta over baseline, assertion 3 covered by the Phase-5 CLAUDE.md-pointer
                fix · fence closure: reciprocal no-trigger cases added to all 5 named siblings'
                evals.json (orchestration-design, loop-design, hook-authoring-standards,
                agent-authoring-standards, entry-file-standards) plus concurrency-design's own new
                disjoint-fan-out negative (n09)

## rulings
- Plugin home: orchestration, not forge. Kim's call — orchestration already owns the "how do
  independent actors coordinate" axis (loop-design: when the next turn fires; orchestration-design:
  solo vs team within one session); this extends that family to cross-session/cross-process
  coordination rather than joining forge's harness-mechanics layer.
- Phase 2 baseline finding (refines the delta, sharper than Phase 1's draft): all 3 baselines reason
  reasonably well about SAME-SESSION multi-agent dispatch (partitioning, `isolation:"worktree"`) and
  about the abstract idea of worktrees. The gap is a specific, previously-unnamed one: baselines
  conflate three distinct actor types into "spawned vs. not" — (a) a subagent spawned this session
  (full control: TaskList assignment, `isolation` param, direct edit); (b) a PEER session addressable
  via `SendMessage` because it surfaces as a `teammate-message` sender (discovered empirically
  mid-incident — real, working channel, but baseline-3 flatly denied it exists: "not a spawned agent
  you can reach with SendMessage"); (c) a truly opaque, unnamed concurrent session with no channel at
  all — only THIS one structurally requires routing through the human. The skill's core uplift is
  making this 3-way classification and its matching action the default move, not the vaguer
  spawned-vs-independent binary every baseline reached for.
- Phase 5 audit MAJOR-1 (fixed): the first draft's Decide steps 1-2 defaulted to isolation for
  ANY multi-actor dispatch, which directly contradicted orchestration-design's own shipped
  guidance (its SKILL.md line 40: "dispatch the disjoint same-tree fan-out... worktrees only when
  slices must mutate overlapping files") — two live skills gave opposite defaults for the same
  disjoint-fan-out scenario. Fixed per the audit's option (a): isolation now conditions on OVERLAP,
  not actor count — same-session subagents with genuinely disjoint slices need none (that's
  orchestration-design's own sanctioned default, cited, not overridden); isolation applies only to
  overlapping/unpartitionable targets or actors outside your control. Description fence + the
  References table's orchestration-design row reworded to match: that skill owns dispatch
  shape/cost, this skill owns only the overlap/tree-safety question. Added the reciprocal
  disjoint-fan-out no-trigger case (evals n09) the audit named.
- Phase 5 audit MINOR-4 (fixed): eval t09 (commit-cadence trigger) had no supporting description
  vocabulary — a blind router would plausibly miss it. Added "should I commit before this risky
  multi-file move" to the description's trigger list, re-budgeted under the 1,024 cap (trimmed two
  redundant phrasings elsewhere to make room).
- Phase 5 real-world mishap during the behavior check (Prompt 1, see evals/behavior-check.md):
  a dispatched check agent had real tool access despite an explicit no-tools instruction and
  actually added a full "## Concurrency" doctrine restatement to agent-ui's live CLAUDE.md —
  reverted immediately, agent stood down, confirmed. This exposed a real gap the skill's first
  draft had: it said the CLAUDE.md rule "belongs" there without saying it must be a one-line
  pointer, not a restatement. Fixed in Decide step 2. Kept as disclosed evidence in
  evals/behavior-check.md rather than scrubbed, per skill-forge's own honesty-in-reporting norm —
  the mistake produced a real finding the clean captures couldn't have.
