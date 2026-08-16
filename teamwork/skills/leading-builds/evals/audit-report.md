# leading-builds — fresh-context FLOOR audit (2026-08-10)

Audited against harness `skill-writing-rules` (3.1.12) + the brief's six checkpoints.
Files read: `SKILL.md`, `intent.md`, `evals/assertions.md`, `agents/build-lead.md` (the twin),
`skills/dispatch-ticket/SKILL.md` (the engine, as shipped), `skills/build-feature/SKILL.md`,
`skills/leading-teams/SKILL.md` (pattern original), `docs/skills/lead-intake/SKILL.md` + its
audit report (sibling baseline). Lint: `skill_lint.py` clean. Description: 601 chars (cap
1,024); build-feature's: 673.

## Verdict

🟡 **One major reciprocal-closure gap owed — in the ENGINE's files, not this one — then
ship.** The skill itself is the cleanest of the three /lead-* artifacts: the host-delta claims
verify against the engine's actual text, the lead-intake fork hazard is correctly NOT imported
(and the why is stated), the re-invocation branch its sibling's audit had to ask for is
already here. But the change mints a third entry to an engine whose own files still declare
two, and the engine's description is a live routing surface.

## Findings, severity-ordered

### F1 — MAJOR: dispatch-ticket's caller enumeration is now stale (reciprocal closure owed)

`dispatch-ticket/SKILL.md` contains zero mentions of `leading-builds` (grep-verified). Two spots
declare the now-false caller set:

- Its description (lines 4–5): "Use when invoked by name from /build-feature's own body or the
  build-lead agent — never from a direct user ask." `dispatch-ticket` is
  `disable-model-invocation: false` — this description sits in the live listing budget. A
  standing /leading-builds session invokes the engine on every turn a target arrives, and from
  mid-session the target IS a direct user ask; the engine's self-declared caller contract now
  excludes its third sanctioned caller and actively repels the invocation path this command's
  Phase 3 orders.
- Its intro (lines 18–19): "factored out so it has two reachable entry points instead of one" —
  leading-builds's own body says "One engine, three entries, on purpose." One of these files is
  wrong, and it's the engine.

Same class, lower stakes: `build-feature/SKILL.md:41–43` rationalizes the engine's no-fork
design by enumerating two callers ("invoked from here … invoked from build-lead … no live user
either way"). The third caller has a live user and inline is still exactly right — the
rationale strengthens, the enumeration no longer covers it.

Per the tier ladder, the dispatch-ticket description edit is boundary-class: suite updated in
the same change, `/check-routing` at the wave boundary.

### F2 — ATTENTION: `evals/baseline/` is empty while intent.md claims two probes

`intent.md` Gate P2: "Baseline: `evals/baseline/` — ad-hoc-primed BUILD session vs a CLOSED
ticket id (state-check probe) and a raw vague ask (record-first probe)." The directory exists
and is empty (verified on disk 2026-08-10). Identical to lead-intake's F2; a
`leading-builds-baseline` seat is active this session — land its output before the P5 behavior
check, or the P2 PASS is unearned and assertions.md has no "without" leg.

### F3 — MINOR: one restated engine slogan (the body's only reference-discipline slip)

Phase 3's parenthetical "record-first is the entire loss-window fix and it does not move"
copies the engine's own line 47 ("ticket-first is the entire loss-window fix, and it does not
move") with a term swap — a drift pair in miniature, and the single place the body restates
rather than references. The decline rule already lives in the failure branch; cut the
parenthetical or cite the engine.

### F4 — MINOR: "This is the command's entire reason to exist" overclaims the interactive delta

Host delta 1 closes with that line, but the interactive branches are equally alive in
/build-feature's fork — the engine's own Phase 1 failure branch says a /build-feature-initiated
call counts as having an interactive user, and build-feature's body says "forking does not
remove the human." The claim is true only against the agent twin; the command's distinctive
value against BOTH siblings is the standing, session-long, unforked seat. Inside the
host-vs-agent deltas section it's defensible, but the superlative invites the wrong contrast —
"the delta the unattended twin structurally cannot offer" says what's meant.

## The brief's six checkpoints

1. **Engine-by-reference discipline — HOLDS.** No phase of dispatch-ticket is restated (F3's
   one slogan aside). The host-delta claims verify against the engine's shipped text: the
   Phase 1 ambiguous-match branch really does key on "an interactive user present" (ask one
   question) vs unattended (named blocker) — this session satisfies the test; the task-kind
   clarify round really is gated on "genuinely ambiguous AND an interactive user is present,"
   with the unattended path going roundless to SKIPPED — "runs instead of going straight to
   SKIPPED" is accurate. Closed-state stop and no-match→intake-first both match Phase 1 as
   written. The fork-hazard reasoning from lead-intake is correctly NOT imported: dispatch-
   ticket's frontmatter carries no `context: fork` (verified), so Skill-invoking it runs
   inline with the live channel intact — the read-and-apply-inline workaround would be cargo
   cult here, and the body instead orders the Skill invocation and states why. Exactly right.
2. **Three-entries framing — ACCURATE** against both siblings as shipped: /build-feature forks
   ONE target off the session (its own description says so), build-lead is the unattended
   programmatic seat (its body: "no clarify round runs here, there is no one to ask"), this is
   the live standing seat. Nit: "/build-feature <id>" is slightly narrow — that command also
   accepts a raw ask — but "ONE build" is the load-bearing half and it's right.
3. **Command-species conventions — CLEAN.** Both dials explicit, argument-hint present,
   description written as menu documentation, blank `$ARGUMENTS` is a designed default (cwd),
   not a missing precondition — no blank-args branch owed, unlike leading-teams's charter. Done /
   NOT-done predicate present; ≤3 uppercase hard gates; lint clean.
4. **Reciprocal fence — CONSISTENT both ways.** build-feature:9–11 carries "NOT for converting
   this session into the standing build seat (/leading-builds) — this command forks ONE
   already-known target"; leading-builds fences "/build-feature" back. Both descriptions well
   under budget (673 / 601 chars). Both dmi:true, so menu-clarity fences — matching intent.md
   P5's recorded disposition.
5. **`${CLAUDE_PLUGIN_ROOT}` paths — SAME-PLUGIN.** The only path is
   `${CLAUDE_PLUGIN_ROOT}/agents/build-lead.md`; both artifacts are teamwork's; the file
   exists as named.
6. **Sibling deltas — nothing wrongly dropped, nothing needlessly copied.** The re-invocation
   rebind branch (lead-intake audit F4's ask) is present from birth. Stand-down section and
   adoption-acknowledgment step mirror the family. lead-intake's record-first WALL is
   correctly inverted, not copied: this seat builds, so the analog is the "just do it, no
   ticket" decline — a live-session pressure the engine's unattended callers never face, so
   the branch earns its line rather than duplicating engine Phase 1. leading-teams's
   invoke-the-agent's-preloads step is correctly transformed into the per-target Skill
   invocation (the agent's `skills: [dispatch-ticket]` preload, host form). mobilize-chores'
   serialize rule cited in delta 3 exists as claimed (its SKILL.md line 98).

assertions.md spot-check: all four assertions map to verified engine text (closed→STOPPED,
interactive-branch question, no-match→intake with the disguised-shape redirect); the with/
without comparison is runnable once F2's baseline lands.

## Disposition

Fix F1 in the same change (dispatch-ticket description + intro line, build-feature's
two-caller rationale; suite + /check-routing per the boundary tier), land F2's baseline, take
or decline F3/F4 as taste. Nothing in this file itself blocks ship.
