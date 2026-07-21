---
name: knowledge-harvest
description: >-
  Detects when a fact crosses the bar for durable project knowledge — a correction restated a
  third time, a ratified decision never captured as reusable knowledge, a high-impact convention
  worth keeping on first mention — turns it into a knowledge-pack (SKILL.md + references +
  routing-corpus + evals), via an AskUserQuestion confirming the plan before writing. Use for
  "third time I've explained X", "skill or reference?", "is this knowledge or noise", "scan our
  docs for uncaptured knowledge", "is our harvested knowledge still accurate", "did this citation
  go stale, the file moved", "is there already a reference covering this", or "propose a plan for
  capturing this decision before we write". NOT authoring content once confirmed (pack-forge);
  NOT a new skill's decomposition (system-decompose); NOT running gates directly (release_gate.py,
  /eval-run); NOT the decision record itself — an ADR IS a decision, this decides whether a fact
  FROM one earns a knowledge-pack entry (doc-writing-rules).
disable-model-invocation: false
user-invocable: true
---

# knowledge-harvest

knowledge-harvest turns a signal — a repeated correction, a ratified decision, a high-impact fact
— into a confirmed, gated addition to a project's knowledge-pack corpus, or explicitly declines to.
It never authors silently: every candidate reaches an AskUserQuestion gate carrying a concrete
plan before any file is written, and every landed citation is later re-checked rather than trusted
forever. This skill orchestrates existing machinery (`pack-forge` authors, `release_gate.py`
gates, `/eval-run` measures routing) — its own delta is the signal, the confirmation payload, the
placement/versioning judgment, and the staleness loop.

## Phase 1 — Detect a signal

A candidate exists when one of three detectors fires:

1. **Frequency** — the same correction, fact, or explanation has now been given a third time (the
   second occurrence is a signal to watch, not yet to act on; acting on the first or second telling
   over-harvests noise).
2. **Impact** — a decision was just ratified, ships as a fix to a defect class that will recur, or
   would silently misroute future work if lost — durable enough to capture on first occurrence.
3. **Managed-docs scan** (on explicit request, e.g. "scan our docs for knowledge we haven't
   captured yet" — never run silently in the background): read the project's docs folder
   (`references/managed-docs-scan.md` for the default location + document-type allowlist and how
   to override them) for a ratified ADR Decision, a closed ticket's Findings, a ratified SPEC/PRD
   clause, or an existing reference doc's claim that has no corresponding knowledge-pack entry yet.
   The same folder's existing high-quality entries also calibrate detectors 1 and 2 — "this is what
   good already looks like here" sharpens the bar rather than replacing it.

**Escape hatch:** a detector firing on something inherently ephemeral (in-progress task state, a
fact only true this session, something `git log`/`git blame` already answers) is not a candidate —
name why inline and stop. Apply the same judgment any persistence mechanism needs about what is
and isn't worth keeping past the moment it was true.

Assemble the candidate: the claim verbatim, its exact source (`file:line`, quote, or conversation
turn), which detector fired and why, and today's date.

## Phase 2 — Propose a plan (do not ask yet)

Before the user sees anything, work out a concrete plan:

- **Which project.** Usually the one you're already in; ask only if genuinely ambiguous (more than
  one project is live in the conversation).
- **Placement.** Grep that project's existing `skills/*/SKILL.md` descriptions and
  `references/*.md` for the same claim. Four outcomes, in order: already covered verbatim → reject
  as duplicate; covered but this sharpens/corrects it → extend the existing reference file;
  genuinely new but fits an existing skill's axis → new reference file within that skill; fits no
  existing skill → new skill (only when the fact is broad and durable enough to be its own axis —
  see `references/placement-heuristics.md`).
- **Versioning.** Never silently overwrite a previously-cited claim. An update to a fact already in
  the corpus appends a dated note or supersedes with a stated reason; it does not edit history in
  place.

## Phase 3 — Confirm with the user (the hard gate)

Ask via **AskUserQuestion**, carrying the concrete plan — never a bare "should I save this?":

- Header ≤ 4 words naming the axis (e.g. "Harvest this fact?").
- The recommended option IS the proposed plan, stated concretely: which file, new vs. extend vs.
  reject, and the versioning move — not a placeholder for the user to fill in.
- Always include a "skip — don't capture this" option.
- If the user picks a different placement than proposed, use that instead of the plan from Phase 2.

**No write happens without a pass through this gate.** A decline or skip ends the candidate here —
record nothing, and do not re-propose the same candidate again this session.

## Phase 4 — Author

**Precondition: do not start this phase without a passed Phase 3 gate.** If no AskUserQuestion
confirmation is on record for this candidate, stop and return to Phase 3 — Phase 4 has no
independent authority to write.

Route the confirmed plan to `pack-forge` (the corpus: `references/*.md`, `scripts/routing-corpus.json`,
`evals/evals.json`) and `skill-forge` (the `SKILL.md` entry surface) — or apply their conventions
inline where not installed — per this workspace's established knowledge-pack shape. Record the citation's
exact source (`file:line`, quote, commit/date) inline. Where the target project already has a
trust-class labeling convention for citations (e.g. the `llm` plugin's "Platform/vendor fact" /
"Worked instance" / "Observed harness behavior" split), follow it; where it doesn't, a bare
`file:line` citation is sufficient — do not import a labeling scheme the target project has no
other use for.

## Phase 5 — Validate before landing

In order, each with its own branch:

1. **Structural gate:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/release_gate.py" <plugin-root>` —
   fix and re-run until clean. This already
   includes the handle-convention and dangling-reference checks (G5/G8); do not build a second
   linter for it.
2. **Independent review:** dispatch `skill-auditor` (a new skill) or `plugin-reviewer` (an existing
   plugin's shape changed) on the landed content. Fix every blocking finding, or accept-with-note
   if the user arbitrates a disagreement.
3. **Routing gate:** if any description or routing-corpus changed, name `/eval-run <plugin-root>` as
   the next step for the user to run — it is a `disable-model-invocation` command, this skill
   cannot trigger it itself.

The same finding failing three times → stop and hand it to the user; do not suppress it.

## Phase 6 — Track staleness (a separate, later invocation)

Run only on an explicit ask ("check if our harvested knowledge is still accurate", "re-verify this
skill's citations") — never as a background process. For each landed entry's recorded citations:
re-open the cited `file:line`/quote and confirm it still matches current reality. Anything broken
or moved gets a proposed fix-or-retire plan, then returns to **Phase 3's same AskUserQuestion gate**
before any edit — staleness resolution is not exempt from the confirmation requirement.

## Output contract

```
Signal: <detector(s) fired> · <claim, verbatim> · <source: file:line/quote/turn + date>
Plan:   <project> · <new-skill | new-reference-file | extend-reference | reject-duplicate> · <versioning move>
Gate:   <user confirmed as-proposed | user overrode to: X | user skipped>
Landed: <files touched> · structural gate: <clean | fixed N> · review: <finding count, fixed/accepted> · routing gate: <named for user | not applicable>
```

## Failure branches

- Dedup finds the fact already captured verbatim → report the existing location, stop; do not
  propose a duplicate.
- User declines or skips at Phase 3 → stop, write nothing, do not re-ask this session.
- `release_gate.py` fails after authoring → fix and re-run; the same failure three times → stop,
  hand to the user.
- Independent reviewer finds a blocking issue → fix before treating the candidate as landed.
- A staleness check finds a broken citation but the user declines the fix-or-retire plan → leave it
  flagged in the entry (do not silently edit or silently leave it looking trustworthy) and report.

**Done when** a candidate has either landed (authored, structural-gate clean, review findings
resolved) or been explicitly declined/skipped by the user — never left as an unconfirmed draft.
**NOT done** when a candidate is authored before Phase 3's confirmation, when a citation is written
without its exact source, or when a fact already covered elsewhere gets a duplicate entry instead
of an extension.
