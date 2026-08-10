# init-repo — forge intent record

Forged 2026-08-10 via /make-skill, the /lead-* family's composer and its closing artifact.
Slots ruled across the family design session; recorded, not re-asked.

## Gate P0 — Route (PASS)

Primitive = **skill, command species**. A composer over shipped parts (the built-in /init, the
team-lead adoption mechanism, the intake-lead standing sibling, per-ticket build-lead
dispatches) — nothing here is a hook, an always-true rule, or a new agent.

## Gate P1 — Interview slots (PASS, pre-ruled)

- **Trigger:** human types `/init-repo` when sitting down in a repo to start a work session.
- **Behavior delta:** the sit-down ritual today is a manual multi-step: maybe run /init, hand-
  prime the session, hand-open renamed background sessions with ad hoc prompts (every prior
  /lead-* baseline documents how those ad hoc prompts fail). With the skill: one command arms
  the session — conditional /init, team-lead adoption, INTAKE sibling spawned, build capacity
  wired — identically every time.
- **Species + dials:** Command — `disable-model-invocation: true`, `user-invocable: true`.
- **Freedom:** medium — a fixed arming sequence composing named parts by reference.
- **Fences:** NOT the parts themselves (/init, /lead-team, /lead-intake, /lead-build,
  /lead-review — each usable alone); NOT batch ticket mobilization (/mobilize-chores).
- **Done-when:** the armed report delivered — what was adopted, what was spawned, how to feed
  each seat — with every step's outcome named (run, skipped-present, or failed-plainly).

**Naming ruling (the registry question, settled):** `init` is not a registry verb; the name
rides the term-of-art exception (skill-writing-rules' 2026-07-15 amendment; ADR-0006 Decision
7's shelf precedent) because this command literally wraps and conditionally RUNS the built-in
`/init` users type verbatim — normalizing the name would break the association with the thing
it extends. `lead-repo` (family verb) and `arm-repo`/`start-repo` (new verbs, no registry
case) were considered and rejected. Kim named it `init-repo` in the originating ask.

**The composition rulings (settled across the session's design rounds):**
1. **Host adopts team-lead; no team-lead spawn** (Kim's AskUserQuestion answer). Mechanically:
   /lead-team is dmi:true — NOT Skill-invocable from inside this command (the #134/#135
   class) — so this body carries the adoption step itself: read agents/team-lead.md and adopt
   per /lead-team's Phase 2, with one deviation, the CHARTER: /lead-team binds one bounded
   charter; here the charter IS the work session ("this session's incoming work on <repo>"),
   closing at session end or stand-down. Named deviation, not silent drift.
2. **INTAKE spawns standing; BUILD is per-ticket — the asymmetry is the seats' own contracts.**
   intake-lead's shipped description names the long-lived-sibling shape ("typically spawned as
   a long-lived sibling named INTAKE"). build-lead's shipped contract is one-ticket-per-
   dispatch — spawning it idle as a standing mailbox would deviate from its own contract and
   deadlock its report shape. So: the INTAKE sibling is spawned at arming; build capacity is
   the armed host dispatching build-lead per confirmed ticket (its designed shape, serial per
   mobilize-chores' rule). Kim's original "intake and build sibling" vision realized honestly
   rather than literally; flagged in the ship report for his veto.
3. **Per-session arming, not durable infrastructure** (the wiring review's return-channel
   finding, 2026-08-10): Agent-tool siblings die with the session that spawned them. The
   command arms ONE work session and says so; re-run per session — the estate's session-scoped
   cron re-arm precedent (repo-cleaner/decision-watcher).
4. **Home: teamwork** — composes team-lead (this plugin), build-lead (this plugin), and the
   /lead-team mechanism; `docs:intake-lead` is a named cross-plugin Agent dispatch (soft,
   degrades gracefully when docs is absent — the arming reports the missing seat and
   continues).

## Gate P2 — Evals (PASS)

- Trigger evals: skipped, recorded — command species, house precedent.
- Behavioral assertions: `evals/assertions.md` (4).
- Baseline: `evals/baseline/` — an ad hoc "set this session up as my working session" ask.

## Gate P3 — Draft (PASS)

SKILL.md on disk; dials explicit; the arming sequence by reference to shipped parts.

## Gate P4 — Language pass (PASS)

Instantiation core applied: arming steps imperative with checkable outcomes, deviations
declared as named rulings, branches named, predicate checkable.

## Gate P5 — Validate

- Lint: clean, first pass and after fixes.
- Fresh-context audit (`evals/audit-report.md`, 2026-08-10): needs-revision verdict, all five
  findings fixed. MAJOR 1 (the seedless INTAKE spawn lands in intake-lead's missing-seed STOP
  branch — proven empirically by that agent's own A4 record) — fixed via the auditor's option
  (b): the missing-seed return IS the liveness ack, zero contract-bending, the seat resumes
  per seed via SendMessage. Companion gap noted for the ship report: intake-lead's description
  endorses the standing spawn its body never defines — a docs follow-up. MAJOR 2 (the
  docs-absent degradation routed to docs' own file-* commands — a dead pointer exactly when
  the branch fires) — split into the two real cases: tool-error-with-docs-present (file-*
  by name) vs docs-absent (host-recorded work items, gap named). m3 (markers wording) — the
  canonical field form. m4 (acknowledgment never instructed) — the standing-block line added
  to step 3. m5 (built-in init's Skill legality assumed) — the reachable-side clause added to
  step 2.
- Behavior check (`evals/behavior-check.md`, 2026-08-10): all four assertions PASS across
  both scenarios (this repo; a simulated fresh docs-less repo), MAJOR 1's liveness-ack fix and
  MAJOR 2's degradation split both exercised, and the combined file-it-and-fix-it probe held
  the adopted coordinator discipline — verbatim relay, no inline code, build staged pending
  the confirmed ticket.

- Fence closure: all fenced siblings command-species; no routing collision from dmi:true —
  recorded disposition.

**Gate summary: P0 PASS · P1 PASS · P2 PASS · P3 PASS · P4 PASS · P5 PASS. Forge complete
2026-08-10. The /lead-* family is complete.**

## Gate P6 — Ship

teamwork 2.2.0 → 2.3.0, README row, ledger, gate, branch + PR.
