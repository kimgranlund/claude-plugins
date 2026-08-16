# Audit: teamwork/skills/leading-review — FLOOR review vs skill-writing-rules

Auditor: fresh-context checker, 2026-08-10. Inputs read on disk: `SKILL.md`, `intent.md`,
`evals/assertions.md`, `evals/baseline/baseline-report.md`; pattern baselines
`teamwork/skills/leading-teams/SKILL.md`, `teamwork/skills/leading-builds/SKILL.md`,
`docs/skills/lead-intake/SKILL.md`; all 11 routed checker agent files; shipped checker
descriptions. `skill_lint.py`: clean.

## Verdict

**PASS — ship-ready as is.** Two minor findings worth a small edit, three notes. Nothing
blocking. The deliberate asymmetry (no review-lead agent) is sound, defended in the right
places, and hard to "fix" wrongly by accident. The self-authored guard is instantiated —
checkable objects, not description. The routing table verifies: every named checker exists,
no stolen charters, no cross-plugin `${CLAUDE_PLUGIN_ROOT}` paths (the file contains none at
all).

## 1 — Routing table accuracy (SKILL.md:37–54): VERIFIED

Every row's checker exists as an agent file in the named plugin:

| Row | File | Charter match |
|---|---|---|
| code-checker (teamwork) | `teamwork/agents/code-checker.md` | ✓ "ONE bounded code change — a diff, branch, or built slice" |
| wiring-checker (teamwork) | `teamwork/agents/wiring-checker.md` | ✓ "how skills, subagents, and teams compose — and the frontmatter" |
| doc-checker (docs) | `docs/agents/doc-checker.md` | ✓ but row UNDERCLAIMS — see M1 |
| skill-checker (harness) | `harness/agents/skill-checker.md` | ✓ SKILL.md files (see N2 on depth) |
| agent-checker (harness) | `harness/agents/agent-checker.md` | ✓ agents/*.md |
| hook-checker (harness) | `harness/agents/hook-checker.md` | ✓ "registration entry plus the script" |
| plugin-checker (harness) | `harness/agents/plugin-checker.md` | ✓ — row deliberately drops the checker's word "wiring", correctly avoiding collision with the wiring-checker row |
| wording-checker (harness) | `harness/agents/wording-checker.md` | ✓ verbatim ("the LANGUAGE of a prompt-carrying artifact") |
| component/layout/flow-checker (screens) | all three in `screens/agents/` | ✓ component / screen-shell-page-wireframe / cross-screen flow |

No row claims territory its checker's shipped description disclaims. No checker is cited under
a charter belonging to a sibling.

## 2 — The no-agent-twin asymmetry: SOUND and adequately fenced

The rationale holds against doctrine. `team-or-solo-rules` is solo-first — a seat is minted
only for work an existing seat can't hold — and the estate's review capacity already exists as
eleven fresh-context checkers. A standing review agent would either (a) duplicate a checker or
(b) accumulate context across reviews, destroying exactly the fresh-context property that makes
the checkers worth dispatching to. The body states this as the OPENING move (SKILL.md:19–24:
"Unlike its siblings, this command adopts no single agent's contract — deliberately… one
standing 'review agent' would either duplicate them or launder their rubrics through a single
accumulating context"), and `intent.md:8–15` records it as Kim's explicit AskUserQuestion
ruling with the reasoning attached. A future maintainer reaching for "add the missing
review-lead agent to complete the family symmetry" hits the counter-argument in the first
paragraph of the body AND in the forge record. That is the right two places; no further
defense needed.

One structural elegance worth naming: because the desk never grades, its accumulating context
is HARMLESS — the generator ≠ critic property lives in the checkers' fresh contexts, not the
desk's. The body says exactly this (SKILL.md:23–25). The asymmetry is not a missing piece; it
is the design.

## 3 — Dispatch-only, degradation, self-authored guard: COHERENT, INSTANTIATED

- **Dispatch-only** (SKILL.md:58–63) is imperative with a named refusal ("just look at it
  yourself, it's quick" → declined) and one named exception. Consistent with leading-teams's
  precedent (leading-teams SKILL.md:57–59: doc-checker absent → hand-review against the owning
  rubric) — leading-review generalizes the same rule to all checkers and adds the disclosure
  requirement, which leading-teams's version lacked. An improvement, not a drift.
- **Self-authored guard** (SKILL.md:64–68) is instantiated, not described: the dispatch's
  permitted contents are enumerated ("the artifact pointer and the report destination"), the
  banned contents are enumerated ("zero rationale, zero framing, zero self-defense"), the
  disclosure locus is fixed ("next to the verdict"), and it covers subagent-authored work
  ("or its own dispatched subagents"), closing the laundering hole. It also appears in the
  done/NOT-done predicate (SKILL.md:98–102), so it is checkable at close. Matches Kim's
  ruling as recorded in `intent.md:37–41` exactly.
- **Verdict-first relay** (SKILL.md:69–72) correctly forbids the desk re-grading and routes
  disagreement to the human — the arbitration seat is named, not left implicit.

**M2 (minor):** the degradation branch says hand-review "against the owning rubric" — but when
the owning checker's plugin is absent, its bundled rubric is usually absent too (the checkers
preload rubrics shipped in their own plugins). The hand-review actually runs from the rubric's
remembered shape. This soft spot is inherited verbatim from leading-teams's precedent, and the
mandatory disclosure mitigates it, but one clause would make it honest: disclose when the
rubric itself was unavailable, not just the generator ≠ critic loss.

## 4 — Command-species conventions: CONFORMANT

`disable-model-invocation: true` + `user-invocable: true` ✓; `argument-hint` present ✓;
description carries the `/leading-review [optional repo root]` invocation and three NOT-fences
✓; eval-suite skip recorded for command species (`intent.md:49`, house precedent) ✓. Hard
gates: exactly three standing rules (SKILL.md:56–72) — at the ≤3 ceiling, none decorative.
Done/NOT-done predicate present and each clause independently checkable (SKILL.md:98–102).
Baseline evidence is real and honest — `evals/baseline/baseline-report.md` discloses that the
ad-hoc session's inline reviews were substantively decent and names why that's the trap
("decent-looking inline reviews are exactly how the anti-pattern survives"). The four
assertions map 1:1 onto the adoption ack + the three standing rules; no orphan assertions, no
unasserted rules.

## 5 — Cross-plugin hygiene: CLEAN

`SKILL.md` contains zero `${CLAUDE_PLUGIN_ROOT}` references (its siblings each use one,
intra-plugin, to read their agent contract — this skill has no contract file to read, so none
is correct, not an omission). All cross-plugin checker references are named soft mentions with
the owning plugin in parentheses, degrading through the named degradation rule when absent.
Legal under the workspace boundary invariant.

## 6 — Sibling comparison: nothing wrongly dropped, nothing needlessly copied

Kept from the family pattern, correctly adapted: bind-the-target Phase 1; adoption
acknowledgment before the first unit of work (adapted to name the table + guard instead of a
contract file, since there is no file); the "conversation about the seat is answered from
records, not re-run" rule (SKILL.md:77–78); re-invocation-rebinds branch; dispatch-failure
honesty branch; "When this rule ends" stand-down section; session-scoped duration.

Correctly dropped: the `${CLAUDE_PLUGIN_ROOT}` contract-read step (no agent to read); the
"NOT the dispatched sibling seat" fence (no sibling seat exists — and the body explains why,
so the missing fence reads as designed, not forgotten); lead-intake's inline-not-Skill-tool
rule (the desk's units of work ARE dispatches, the opposite constraint).

Correctly added beyond the siblings: the multi-row target rule (a PR shipping a skill → one
dispatch per owning row, SKILL.md:52–54) and the fresh-re-review rule (SKILL.md:86–88) —
both genuine desk-specific branches, not decoration.

## Findings ledger

- **M1 (minor).** The doc-checker row (SKILL.md:44) lists "PRD, SPEC, LLD, ADR, reference,
  vision memo" but doc-checker's shipped charter also owns CLAUDE.md, llms.txt, handoff
  blocks, decomposition manifests, and DESIGN.md. Under the table's own "matching no row →
  named gap" rule (SKILL.md:52), a CLAUDE.md or llms.txt sent to the desk gets a FALSE gap
  declaration instead of its real owner. Fix is one row edit: widen the row's class list or
  end it with "…and the rest of doc-checker's own description".
- **M2 (minor).** Degradation branch (SKILL.md:60–63): when the owning plugin is absent its
  rubric usually is too; the disclosure should cover rubric unavailability, not only the
  generator ≠ critic loss. Inherited from leading-teams's precedent; one clause fixes it.
- **N1 (note).** code-checker's own fence "NOT for a repo that carries its own review seat"
  is not reflected in the table — a repo with a native review seat (e.g. one carrying its own
  reviewer agent) would still be routed to code-checker. Acceptable for a generic desk;
  worth knowing.
- **N2 (note).** skill-checker and agent-checker carry FLOOR/DEEP depths; the desk's sealed
  dispatch doesn't address depth, so FLOOR-by-default applies. Fine — but a human asking the
  desk for a deep review should have that word survive into the dispatch. The "nothing else
  it doesn't need" clause (SKILL.md:38) arguably already permits this; it just isn't said.
- **W1 (wording nit).** "and nothing else it doesn't need" (SKILL.md:38) is a double negative;
  "and nothing it doesn't need" or "and only what it needs" reads cleaner.
