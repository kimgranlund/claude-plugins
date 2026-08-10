# lead-intake — forge intent record

Forged 2026-08-10 via /make-skill, immediately after the intake-lead agent forge (PR #162).
The interview's slots were ruled during this session's /lead-* family design; recorded here,
not re-asked.

## Gate P0 — Route (PASS)

Primitive = **skill, command species**. Not a hook (nothing mechanically checkable), not an
entry-file rule (on-demand, not every-turn), not an agent (the agent twin `agents/intake-lead.md`
already exists — this command is deliberately the OTHER half: the host adopts the same contract
itself, the `/lead-team` ↔ `team-lead` pattern).

## Gate P1 — Interview slots (PASS, pre-ruled)

- **Trigger:** human types `/lead-intake` when sitting down in (or converting a session into) a
  dedicated intake session — Kim's hand-rolled "BUGS"/"INTAKE" background sessions, formalized.
  Command species: the description is slash-menu documentation, no trigger contract.
- **Behavior delta:** today the priming is an ad hoc hand-written prompt — no standard contract,
  so walls, dedup, payload shape, and clarify discipline vary run to run (baseline evidence in
  `evals/baseline/`). With the skill: the session adopts `agents/intake-lead.md`'s exact
  contract plus the three host deltas below, identically every time.
- **Species + dials:** Command — `disable-model-invocation: true`, `user-invocable: true`.
- **Freedom:** medium — read-and-adopt the agent file (never restate its contract), plus the
  named host deltas; the intake procedures themselves stay owned by the four sibling skills.
- **Fences:** NOT the dispatched agent (`intake-lead` via the Agent tool — a sibling session,
  not this one); NOT a one-off filing (`/file-bug`/`/file-feature`/`/file-task` directly); NOT
  a coordination charter (`/lead-team`).
- **Done-when:** adoption acknowledged with the standing line; thereafter every raw seed in the
  session ends in a record (id/URL · kind · status · gaps) or a named blocker; intake-only held
  for the session's duration.

**Host deltas from the agent (the reason this command exists at all):**
1. **The clarifying round RUNS here.** The agent has no interactive channel; the host has
   `AskUserQuestion` — the siblings' one-batched-round discipline applies as written, replacing
   the agent's capture-with-gaps-always branch.
2. **The wall becomes stated discipline.** The agent's intake-only bar is structural
   (`disallowedTools`); the host keeps its tools — the adopted rule is the deliberate choice not
   to use Skill/Agent for builds or investigations (lead-team's exact
   discipline-instead-of-wall move).
3. **Delivery is direct.** No teammate mode, no SendMessage — the report contract (verdict line
   + per-record lines) lands as the session's own reply.

**Ruled fork — inline application, not Skill invocation (same ruling as the agent, new
rationale):** the host reads the four intake SKILL.mds at adoption and applies the owning
procedure inline per seed. For `file-bug`/`file-feature`/`file-task`, Skill-invoking forks
(`context: fork`), and the fork's clarifying round rests on the still-unverified
AskUserQuestion-from-fork assumption — the live question channel is this command's entire
point, so the procedure runs where the channel provably exists: the host's own turn.
`file-leftovers` carries no `context: fork` (its own design — a fork can't see the session it
sweeps); inline is where it runs anyway. One rule, two reasons (audit F1's scoping correction,
2026-08-10). (Fork-from-agent is verified broken for seats; fork-from-host remains
unverified — inline sidesteps both.)

## Gate P2 — Evals (PASS)

- **Trigger evals: skipped, recorded** — command species, `disable-model-invocation: true`; the
  description never reaches the router, there is nothing to trigger-test (house precedent:
  lead-team, build-feature, mobilize-chores all suite-less).
- **Behavioral assertions** (`evals/assertions.md`): 4 checkable statements.
- **Baseline** (`evals/baseline/`): fresh-context run of an ad-hoc-primed session against two
  seeds, captured before the skill existed — the "before" evidence.

## Gate P3 — Draft (PASS)

SKILL.md on disk; dials explicit; body ~70 lines; description ≤ 1,024 chars, menu-register.

## Gate P4 — Language pass (PASS)

prompt-wording-rules' instantiation core applied line-by-line: adoption steps are imperatives
with checkable objects (read X in full; state the line), the three deltas are declarative facts,
branches named, stopping predicate checkable, ≤ 3 hard gates (one: never dispatch builds).

## Gate P5 — Validate

- Lint: clean (first pass and after audit fixes).
- Fresh-context audit (`evals/audit-report.md`, 2026-08-10): verdict ship-after-one-major.
  F1 MAJOR (fork claim overgeneralized to file-leftovers, which carries no `context: fork`) —
  FIXED in SKILL.md + this record, independently verified against its frontmatter. F2 (baseline
  dir empty at audit time) — resolved by timing: `evals/baseline/baseline-report.md` landed
  minutes after the auditor's read; P2's PASS stands. F3 (sibling paths) and F4 (re-invocation
  branch) — FIXED. All other checks passed as reported.
- Behavior check (`evals/behavior-check.md`, 2026-08-10): all four assertions PASS with the
  baseline deltas demonstrated (acknowledgment none→full; procedure forks→inline; vague-seed
  questions buried→asked; delivery fragments→verdict contract; build ask declined with resume
  pointer). Remaining live item, disclosed: the AskUserQuestion round firing from a REAL
  /lead-intake session — the check proved content and timing, not the tool mechanism; first
  real use is the proof.

**Gate summary: P0 PASS · P1 PASS · P2 PASS · P3 PASS · P4 PASS · P5 PASS. Forge complete
2026-08-10.**
- Fence closure: fences name the agent (no eval suite exists for agents), three command-species
  or user-typed siblings, and /lead-team (teamwork — cross-plugin soft mention). No
  model-routing collision is possible from a dmi:true skill, so no reciprocal suite cases are
  owed (house precedent, teamwork 1.1.0 ledger); recorded here as the fence-closure disposition.

## Gate P6 — Ship

docs 1.3.1 → 1.4.0, README row, ledger entry, gate, branch + PR.
