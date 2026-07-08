---
name: handoff-compose
description: >
  Compose or review the standard handoff block a team agent returns when it hands work
  back to its coordinator or the host — Status · Summary · Files changed · Tests/checks run ·
  Evidence · Risks · Open questions · Recommended next action. Use whenever a subagent
  finishes a unit of work and must report, when a coordinator rolls several reports into
  one, or when judging whether a handoff is verifiable and routable: "how do I hand this
  back", "report my results", "write the handback", "is this handoff complete". NOT for
  designing how the seats compose (orchestration-design) — this owns only the return block.
disable-model-invocation: false
user-invocable: true
---

# Harness — Agent Handoff Contract

The single block every team agent emits when it hands work back (to the coordinator seat — `orchestration-coordinator` or a project equivalent — or to the host). One **verifiable, routable** shape, so the next step *checks* the work instead of re-reading it. Agents point at this contract rather than restating it; this skill is the authority on the fields and how to fill them. It is the return half of `[[orchestration-design]]`: that skill designs how capabilities compose, this one standardizes how a worker reports back. Its critic is the block's consumer: the recipient — the coordinator's eval gate, or the host — is fresh-context by construction (**consumer-as-critic**, a deliberate form the standard sanctions, not a missing reviewer seat).

## Before you hand back

**In a messaging team, drain your full inbox first.** Read every still-pending message before you compose — a handoff written one message behind is already wrong the moment it ships: it re-asks a question a later message already answered, re-edits an artifact a teammate already committed, or retracts a finding a newer commit already fixed. Compose only once nothing is left unread. A **sealed subagent has no inbox** — its world was enumerated at dispatch, and new information reaches it only by re-dispatch; for it, freshness means consistency with the inputs it was handed.

## The block — exactly these fields, in order

Keep each tight; omit nothing — write `(none)` when a field is empty. Inline what routes; anything bulky returns **by reference** (write it to a file, cite the path) — a handback is a routing surface, not a payload. A handoff is **write-once**: once shipped it is never edited in place — the recipient may already have routed on it; repair = re-dispatch + re-compose.

- **Status** — `done | partial | blocked(reason)`, first line, nothing else on it. `partial` names what remains; `blocked` names the missing input or decision. This is the enum the coordinator routes on — outcome state never lives only in Summary prose.
- **Summary** — what was done, in 1–3 sentences. The outcome, not the process.
- **Files changed** — each path touched (created / edited / deleted), one per line.
- **Tests/checks run** — the gates run and their result, *by command*: `npm run check && npm test`, `harness_checks.py <type>`, `coverage_check.py`, `trace_check.py`. Name the command + its verdict — `pass | fail | UNMEASURED — skipped-not-passed` (or the exit code) — never a bare "tests pass"; a gate you didn't run is UNMEASURED, stated, never silently omitted.
- **Evidence** — the proof a reviewer can verify *without re-doing the work*: gate exit codes, counts, `file:line` citations. Raw output longer than ~10 lines goes to a file, cited by path.
- **Risks** — what could be wrong or fragile, the assumptions made, the blast radius — max ~5, each with its suspected locus (`execution | spec | plan`) so the repair can be aimed. Honest, not reassuring.
- **Open questions** — unresolved decisions needing a human or another role; max 3, each decision-shaped.
- **Recommended next action** — the single best next step **and who owns it** (`system-planner` / `system-builder` / the maker whose work was reviewed — a reviewer's handback recommends "maker applies the fix" / host).

## Gate ≠ commit

A green gate is **not** a landed change. Read the gate output, *then* commit as a separate step — never chain a commit onto a test run with `&&`, or a regression rides in on a gate whose output was never read. (`orchestration-coordinator`/host commits; a maker hands back gated state, it does not self-land.)

## References & tools

| Path | Use when |
|---|---|
| `scripts/handoff_check.py` | Mechanical H1 gate — field presence, order, `(none)` markers, Status enum — run before any rubric judgment |
| `references/foundations.md` | Why the shape is verifiable-not-narrative; the up-loop + generator/critic split it feeds |
| `references/best-practices.md` | Per-field how-to + the per-seat notes (planning / execution / orchestration / steward / tokens) |
| `references/rubric.md` | Scoring a handoff block — completeness, verifiability, honesty, routing-readiness |

**Done** when all eight fields stand in order, Status routes on the enum, Evidence lets the consumer confirm the Summary without re-doing the work, every unrun gate is stated UNMEASURED, and the recommendation names one step with one owner. **NOT done** while a field is missing rather than `(none)`, a verdict hides in prose, a "tests pass" stands bare, Risks reassure — or a shipped block gets edited in place instead of re-dispatched and re-composed.
