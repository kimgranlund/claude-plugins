# Changelog — flow-decompose

Format: [Keep a Changelog](https://keepachangelog.com/). Versioning: [SemVer](https://semver.org/).

## [0.1.1] — 2026-07-03

Excellence-campaign batch-3 fix wave. Ledger: `skills-audit/campaign/batch-3/flow-decompose.findings.jsonl`.

### Changed
- **Description (M2)** — added the stranded symptom ("the user is stranded / has no way back") and
  the "trace what happens from X to Y" verb phrasing; corpus of record installed at
  `scripts/routing-corpus.json` (13 pos / 14 neg). routing_eval: F1 0.917, precision 1.000, both
  recall misses dispositioned (paraphrase-class proxy artifacts).
- **GRADE mode + Material table (S5)** — the fresh-context critic now has a name: the
  `flow-reviewer` agent (was "a fresh-context critic"). Reciprocal citation added to [[ui-audit]]'s
  flow pass (step 3): a flow you designed goes to the flow-reviewer agent.
- **Assert-walk scope unified (A3)** — Quick Start step 4 now matches the Verify Target: "every
  success exit's asserts (and any declared abandon/error asserts)".
- **Close + vocabulary (L/S3)** — Material & routing moved above Verify Target so the done/NOT-done
  predicate closes the file; the "skipped and reported, never silently passed" paraphrase replaced
  with the house token **skipped-not-passed**.

## [0.1.0] — 2026-07-02

Initial cut. The cross-screen FLOW altitude of the owned design stack: [[layout-decompose]] owns
within-screen space + behavior; this owns the journey between screens, declared as a state machine.

### Added
- **SKILL.md** — the two-axis method at flow altitude: OUTSIDE-IN (task → journey: A1 entry
  discoverable `[gate]` · A2 stage coverage `[gate]` · A3 ordering · A4 effort shape · A5 sibling
  coherence) × INSIDE-OUT (transitions → whole: B1 transition inventory `[gate]` · B2 exit truth
  `[gate]` · B3 recovery · B4 persistence/resume · B5 cross-flow coherence), the defect quadrant
  (shippable · right-journey-wrong-machine · wrong-journey-right-machine · broken), DESIGN /
  DECOMPOSE / GRADE modes (generator ≠ critic), and the card+checker discipline mirrored from
  focus-verify (skipped-not-passed; necessary-not-sufficient).
- **`scripts/flow-check.py`** (stdlib-only, selftest-locked) — the mechanism gate over `*.flow.json`
  cards: UNREACHABLE_STATE / DEAD_END / ORPHAN_EXIT / NO_EXIT_TRUTH / NO_RECOVERY gates,
  UNGUARDED_BACK / INPUT_LOSS advisories, and `--inventory inventory.json` (ui-audit's spine) for
  the UNKNOWN_SCREEN advisory. Absent sections skip-and-report; malformed cards error cleanly;
  exit 1 on gates. Selftest fixtures: clean flow, dead end, truthless success exit, fallible
  without recovery, unreachable island + orphan exits, unguarded back + input loss, sparse skips,
  inventory cross-check, seven malformed shapes.
- **`examples/one-time-pay.flow.json`** — real card from adia-pay's one-time-pay flow (statement →
  pay wizard → receipt): success exit asserting "youOweNowCents reflects the payment" + "receipt
  shows applied amounts", decline recovery preserving input, timeout-resume persistence
  (session timeout / re-auth, wizard step + amount restored — Tier-2 #9 in adia-pay's roadmap).
  Proven both ways: passes clean; stripping the success asserts fires NO_EXIT_TRUTH.

### Wired (same change)
- [[ui-audit]]: new step-3 **Flow pass** (cards from the inventory's declared flows → flow-check
  gates → walk success asserts against rendered truth), flow row in the output contract,
  flow-decompose added to the description's composed-instruments list.
- [[layout-decompose]]: description NOT-clause + §SelfAudit scope bullet — the cross-screen
  journey hands across to flow-decompose; layout owns within-screen.
- [[ui-patterns]] `references/state-patterns.md`: pointer in "State × module composition" —
  cross-screen state machines are flow-decompose's card; the pentad governs within one screen.
