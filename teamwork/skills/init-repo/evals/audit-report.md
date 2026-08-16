# init-repo — fresh-context FLOOR audit (2026-08-10)

Scope: `teamwork/skills/init-repo/` (SKILL.md, intent.md, evals/assertions.md) against
skill-writing-rules, with composition accuracy checked against the shipped parts on disk:
`teamwork/skills/leading-teams/SKILL.md`, `docs/agents/intake-lead.md` + `intake-lead.intent.md`,
`teamwork/agents/build-lead.md`, `teamwork/skills/mobilize-chores/SKILL.md`, sibling commands
`leading-builds`/`leading-review`, `harness/skills/naming-rules/SKILL.md`, issues #134/#135.
Mechanics: `skill_lint.py` clean.

## Verdict

**Needs revision before ship — 2 major, 3 minor.** The architecture is right (host adopts
team-lead, INTAKE standing, build per-ticket — each ruling traceable to the composed seats'
own contracts) and the body stays by-reference throughout. But the INTAKE spawn as written
lands in intake-lead's empirically-proven missing-seed stop branch, and the docs-not-installed
degradation routes to commands that are absent exactly when the branch fires.

## Major

### M1 — The seedless INTAKE spawn collides with intake-lead's missing-seed stop branch

SKILL.md step 4 spawns INTAKE "with its canonical seed shape: the repo root, no markers, its
own report contract" — i.e. no Seed. But the canonical dispatch prompt
(`docs/agents/intake-lead.intent.md`, "Canonical dispatch prompt" block) makes the Seed the
first mandatory field, and the agent's own branch is "Seed absent or empty → report the
missing field; stop." This is not hypothetical: the A4 smoke test (same intent record,
2026-08-10) ran exactly this dispatch shape — repo root + markers, no Seed — and the seat
stopped with "0 records minted, 1 blocked."

So the armed report's "INTAKE ready" would follow INTAKE's own first act being a blocker
report. The arrangement may still function as a mailbox (SendMessage continues a stopped
teammate), but the skill neither says that nor names the deviation. Calling a seedless prompt
"its canonical seed shape" is inaccurate — the seed IS the canonical shape's spine.

Fix options (either resolves it; name the choice):
- (a) Make the standing mode an explicit named deviation in the spawn prompt — parallel to the
  charter deviation in step 3: "standing mode: no initial seed; seeds arrive via SendMessage;
  acknowledge armed and idle" — and note it deviates from the agent's written one-shot
  contract. (intake-lead's own description and dispatch-example 1 already gesture at this
  long-lived mode; its body never defines it — a companion gap worth a line in the ship
  report, since the collision spans both files.)
- (b) Accept the missing-seed report as the liveness acknowledgment and say so: the armed
  report treats INTAKE's "0 minted, 1 blocked" return as proof-of-life, and relays begin from
  there.

### M2 — The docs-not-installed degradation points at docs' own commands

Step 4 and failure branch 2: "docs not installed → … intake asks route to the file-*
commands by name instead." The file-* commands (`file-bug`/`file-feature`/`file-task`) ARE
docs skills — when docs is not installed they are exactly as unreachable as intake-lead. The
fallback is a dead pointer in one of its two trigger cases:

- INTAKE spawn fails as a tool error with docs installed → file-* routing works. Valid.
- docs not installed → file-* commands don't exist either. Invalid.

Fix: split the two cases. Tool-error → file-* by name (docs is present). docs-absent → name
the missing plugin and degrade to what actually exists (e.g. raw `gh issue create` intake by
hand, disclosed as the un-proceduralized fallback), or simply report intake as an absent
capability.

## Minor

### m3 — "no markers" vs assertions.md's "marker protocol named"

SKILL.md step 4 says "no markers"; `evals/assertions.md` #3 asserts the spawn carries the
"marker protocol named". The canonical prompt's field is `Markers: <none | [unattended] |
[redirected-from:X]>` — a named field whose value may be none, not an omitted line. Align
both files to the canonical shape: the Markers field is named, its value at spawn is `none`.

### m4 — The adoption acknowledgment is tested for but never instructed

The done-when predicate ("the adoption acknowledged before any spawn") and assertion #2
("acknowledged … before any sibling spawns") both test for an explicit acknowledgment, but
step 3 never instructs one. Both siblings carry it as a numbered instruction (`leading-builds`
Phase 2.3, `leading-review` Phase 2 opening: "Acknowledge adoption before processing any
target: one standing block…"). Add the one line to step 3 so the predicate tests something
the body actually orders.

### m5 — The built-in `init` invocation's legality is assumed, not stated

Step 2 invokes the built-in `init` via the Skill tool; step 3 states why /leading-teams CANNOT be
Skill-invoked (dmi:true, the #134/#135 class) — but nowhere does the skill or intent record
state why `init` CAN be: it is model-invocable (present on the session's Skill surface),
i.e. the other side of the same #134 dichotomy. The estate's #134 defect arose precisely from
an unstated assumption that a Skill call in a procedure would execute. One clause in step 2
("model-invocable, so Skill-reachable — unlike the dmi:true /lead-* family below") closes it.
Containment note: the step-2 failure branch (report plainly, STOP the arming) already bounds
the blast radius if a host ever lacks the built-in — the branch discipline is right; only the
stated reasoning is missing.

## Checked and clean

- **Naming ruling (defensible, correctly stated).** `init` is confirmed absent from
  naming-rules' verb registry; the term-of-art row ("a term users type verbatim outranks the
  shape grammar", naming-rules Refinements) covers a command that wraps and conditionally RUNS
  the built-in `/init` users type verbatim. The body states it in one parenthetical pointing
  at the intent record — no over-arguing. One citation nuance for the record: the
  skill-writing-rules 2026-07-15 amendment's letter scopes to "a knowledge catalog's subject";
  the load-bearing basis here is naming-rules' broader term-of-art row plus the ADR-0006
  Decision 7 shelf precedent, both of which intent.md also cites. Defensible as ruled.
- **team-lead adoption fidelity.** Step 3 tracks /leading-teams Phase 2 by reference (read the
  agent file in full, adopt, invoke `team-or-solo-rules` + `loop-rules` — the agent's own
  preloads), names the ONE deviation (charter = the session) explicitly, and incorporates all
  three host deltas by name-and-reference ("roll-up audience, review-seat degradation, the
  write-scoping discipline — apply as written") — none restated, none dropped.
- **Per-ticket build ruling matches build-lead's contract.** `build-lead`'s description and
  body are one-ticket-per-dispatch ("Your dispatch names one ticket id"); a standing idle
  spawn would deadlock its report shape. Step 5's asymmetry ruling is the seats' own
  contracts, accurately. The serial citation is real: `mobilize-chores/SKILL.md:97-98`
  ("mutating dispatches share this one checkout, so run them SERIALLY, or give each
  `isolation: "worktree"`") — init-repo cites the serial half only, a conservative subset.
- **Cross-plugin hygiene.** The only `${CLAUDE_PLUGIN_ROOT}` path is
  `agents/team-lead.md` — same-plugin (file exists at `teamwork/agents/team-lead.md`).
  `docs:intake-lead` is an Agent dispatch — a legal soft mention with a degradation branch
  (the branch's content is M2, but its existence and shape are correct). All fence mentions
  (`/init`, `/leading-teams`, `/lead-intake`, `/leading-builds`, `/leading-review`,
  `/mobilize-chores`) resolve to shipped artifacts on disk.
- **Command-species conventions.** dmi:true + ui:true + argument-hint; `$ARGUMENTS` named in
  the intro and bound in step 1 (the siblings' shape); failure branches cover every step that
  can fail (init failure → STOP with rationale; spawn failure → degrade, never fabricate
  "INTAKE ready"; stale CLAUDE.md → observed, routed to `/check-entry-file`, not repaired;
  re-run → rebind, re-verify, never stack); stand-down stands INTAKE down via SendMessage
  rather than abandoning it; done/NOT-done predicate checkable. Trigger-eval skip recorded
  (command species, house precedent). Lint clean.
- **Nothing needlessly copied.** Every composed part is reached by reference; no sibling
  procedure is restated. Nothing the siblings carry is wrongly dropped except the
  acknowledgment instruction (m4).

## Assertion triage (Phase 5 input)

- A1 (conditional /init): body supports as written.
- A2 (adoption acknowledged before spawns): body under-specifies — blocked on m4.
- A3 (INTAKE canonical dispatch shape): as written the assertion and the body disagree with
  each other AND with the canonical prompt — blocked on M1 + m3.
- A4 (armed report): body supports as written; M2's degradation wording feeds the
  seat-absent-degraded outcome and should be fixed before the with-skill run.
