# lead-intake — fresh-context FLOOR audit (2026-08-10)

Audited against harness `skill-writing-rules` (3.1.12) + the brief's six checkpoints.
Files read: `SKILL.md`, `intent.md`, `evals/assertions.md`, `agents/intake-lead.md` (the twin),
`teamwork/skills/lead-team/SKILL.md` (pattern baseline), and the four sibling procedures'
SKILL.mds. Lint: `skill_lint.py` clean. Description: 551 chars (cap 1,024).

## Verdict

🟡 **One major factual fix owed, then ship.** The skill is a faithful, correctly-scoped
instance of the /lead-team host-adoption pattern; the deltas match the agent as shipped; the
read-don't-restate discipline holds. But the inline-not-Skill rationale overclaims on exactly
the axis the pattern's credibility rests on: it asserts all four siblings fork, and one doesn't.

## Findings, severity-ordered

### F1 — MAJOR: the fork rationale is false for one of the four siblings

`SKILL.md` Phase 2 step 2: "never invoke them via the Skill tool from inside this seat — a
Skill invocation forks (`context: fork`)". Verified frontmatter: `file-bug`, `file-feature`,
`file-task` carry `context: fork`; **`file-leftovers` does not** — it deliberately runs
in-context (its own body, line 20: "the sweep runs in THIS context — a subagent or fork cannot
see the conversation"). A Skill invocation of file-leftovers would run in this session's own
turn with the live channel intact; the stated mechanism does not apply to it.

The *rule* (apply all four inline) can stand uniform — reading-and-applying a non-fork skill is
behaviorally equivalent to invoking it, and one discipline is simpler than a per-sibling split.
But the *claim* must match the facts: scope the fork clause to the three fork siblings and note
file-leftovers runs in-context by its own design, so inline is trivially where it already runs.
`intent.md`'s "Ruled fork" paragraph carries the same generalization — fix both in the same
change (drift pair otherwise).

The unverified-reachability wording itself is precise and correct: the body claims only that
fork-from-host AskUserQuestion reachability is *unverified* (never "broken"), matching the
verified record (fork-from-agent broken, A4 smoke 2026-08-10; fork-from-host untested). No
overclaim there.

### F2 — ATTENTION: `evals/baseline/` is empty while intent.md claims captured evidence

`intent.md` Gate P2: "Baseline (`evals/baseline/`): fresh-context run … captured before the
skill existed — the 'before' evidence." The directory exists and is empty (verified on disk
2026-08-10). If the baseline run is still in flight (a `lead-intake-baseline` seat is active),
land it before the P5 behavior check; if it never lands, the P2 PASS is unearned and the
with/without comparison in assertions.md has no "without" leg.

### F3 — MINOR: the four sibling reads have no explicit paths

Phase 2 step 2 orders "Read the four intake procedures … (this plugin, each skill's SKILL.md)"
but gives no path, while step 1 gives the agent file's full `${CLAUDE_PLUGIN_ROOT}` path. A
Read needs a resolvable path; "this plugin" makes the host derive it. Give
`${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` explicitly — same-plugin, so no boundary issue.

### F4 — MINOR: no branch for a repeat `/lead-intake` while the seat stands

`/lead-team` carries a re-invocation branch (charter still open → check records, ask
close/replace/parallel). The analogous case here — `/lead-intake /other/repo` typed while the
seat is armed — is unhandled: rebind the target? acknowledge already-armed? The seat is
long-lived by design (session-duration discipline), so a second invocation is likelier here
than in the charter-scoped sibling. One branch line suffices (e.g., re-invocation rebinds the
target repo root in one acknowledged line; the adopted contract does not re-adopt).

## Checkpoints from the brief — dispositions

1. **Command-species conventions** — 🟢 PASS. Description is menu-register with zero trigger
   spend, run-line and argument named, three parseable NOT-fences; both dials explicit;
   `argument-hint` documents the blank-default, so no blank-invocation failure branch is owed
   (unlike lead-team, whose charter is mandatory). Report contract per seed + checkable
   done/NOT-done predicate close the body. Side-effect confirm points are correctly left to the
   sibling procedures that own the mints.
2. **Read-don't-restate** — 🟢 PASS. Step 1 is a pointer inventory (rule *names*, not rule
   *bodies*) — the same shape as lead-team's eight-priority line, with the drift warning
   stated. The sibling procedures are read, not restated; the one place sibling text would
   conflict inline (their own Skill-tool redirect instruction on misclassification) is resolved
   by the adopted agent file's "one-hop redirect rule satisfied inline" clause, reached by
   reference — no drift pair created.
3. **The three host deltas vs the agent as shipped** — 🟢 PASS, all three accurate.
   Delta 1 correctly replaces the agent's no-channel branch (agent line: "No clarifying round
   runs in this seat") with the siblings' own discipline *as written*, and the
   `[unattended]`/`[redirected-from:X]` semantics match file-task Phase 2's canonical
   statement: capture-with-gaps only when the round is spent or a marked seed arrives.
   Delta 2 matches the agent's `disallowedTools: ["Skill", "Agent", "Task"]` wall becoming
   stated discipline — lead-team's exact move, correctly attributed. Delta 3 matches the
   agent's SendMessage-in-teammate-mode clause. Bonus: the first failure branch correctly
   *inverts* the agent's thin-seed guard (the host may HAVE the referenced context) — a real
   host delta the intent record didn't even list, rightly in the body.
4. **Inline-not-Skill ruling** — 🟡 instantiated clearly, rationale correct for three of four
   siblings; see F1.
5. **`${CLAUDE_PLUGIN_ROOT}` paths** — 🟢 PASS. One use, `agents/intake-lead.md`, same plugin
   (docs). The four siblings also live in docs, so F3's fix stays boundary-clean. The one
   cross-plugin mention (`/build-feature`, teamwork) is a named soft mention with a same-plugin
   fallback (`/file-bug <id>`) — degrades correctly.
6. **vs the /lead-team template** — 🟢 mostly clean. Correctly dropped: the blank-argument
   branch (blank is a documented default), the solo-first override paragraph (no doctrine
   conflict exists here), the preload-invoke step (these siblings must be READ — they are
   procedural/fork, not knowledge preloads). Correctly kept: bind → adopt → run → end-rule
   skeleton, the three-delta block, the drift warning, done/NOT-done. Wrongly dropped: the
   re-invocation branch (F4). Nothing needlessly copied — the ADR-0006 species sentence is
   tighter than lead-team's two-sentence version.

## Eval-suite skip

Recorded skip is sound: `disable-model-invocation: true` — the description never reaches the
router; house precedent (lead-team, build-feature, mobilize-chores) confirmed suite-less. The
four behavioral assertions are individually checkable and map 1:1 onto the body's contract
(acknowledgment, record contract, clarify discipline, intake-only wall). No fence-closure debt:
a dmi:true skill cannot collide in routing, per the teamwork 1.1.0 precedent intent.md cites.
