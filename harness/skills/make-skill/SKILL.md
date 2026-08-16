---
name: make-skill
description: >-
  Forge a Claude Code skill end-to-end: intake interview, evals-first draft, and audit. Use when
  the user wants to build, make, author, write, or scaffold a new skill — a reusable capability,
  turning a workflow into a skill, or adding something the model can invoke on its own. NOT for
  auditing an EXISTING skill (check-skill); NOT a split/merge decision (plan-skill-split).
disable-model-invocation: false
user-invocable: true
argument-hint: "[skill-name or one-line intent]"
---

# make-skill

make-skill turns an intent into a shipped skill through six gated phases. Each phase ends at a checkable gate recorded in the intent record; a failed gate stops the forge — the fix lands in the failed phase, never by piling instructions onto a later one.

Seed for Phase 0/1: `$ARGUMENTS`

Invoke `skill-writing-rules` now — it governs every phase below and is not restated here.

Throughout the forge: one question per turn during interviews; every file lands under the target skill directory; the intent record at `<skill-dir>/intent.md` is the living state — phase gates, decisions, and accepted-with-note findings are written there as they happen, not recalled from conversation.

## Phase 0 — Route

A skill is one primitive among five. Walk the ladder against the stated intent:

1. Mechanically checkable rule (a program could return pass/fail) → **hook**, not a skill.
2. Always-true project fact, needed every turn → **entry file / rule**, not a skill.
3. Needs tool walls, parallelism, or multi-skill preload → **agent** (thin shell over skills).
4. Knowledge or procedure, needed on demand → **skill**. Continue.

If the ladder exits before step 4 → stop and report the primitive with the one-sentence reason. Do not forge a skill to be polite.

**Gate P0:** primitive = skill, reason recorded.

## Phase 1 — Intent interview

Interview per `references/interview.md` (question bank + record schema). The interview fills seven slots: Trigger, Behavior delta, Species + dials, Freedom, Type, Fences, Done-when. Capture trigger phrasings **verbatim** — they become the description and the eval queries.

The challenge rule: a skill with no demonstrable behavior delta restates model knowledge. If the user cannot show or describe a wrong current output ("what does Claude do today, without this skill, that this skill fixes?"), say so plainly and recommend stopping. Two failure branches:

- Answers stall on a slot → summarize the open slot, ask once more; still open → park the record with the gap named, stop.
- Species ambiguous after discussion → show the standards' species table; the user chooses; record the choice.

Write the completed record to `<skill-dir>/intent.md`.

**Gate P1:** every slot filled, species + both dials chosen, user has confirmed the record.

## Phase 2 — Evals before body

Evidence before prose:

1. **Trigger evals** (model-invocable skills only): ~20 queries in `<skill-dir>/evals/evals.json` — should-trigger phrasings from Phase 1 plus near-miss should-NOT-trigger queries that a lazy description would catch. User-only skills skip trigger evals.
   *Knowledge-species note:* this forge produces the skill's entry surface (SKILL.md, evals, structure) — it does **not** research or author a reference corpus. If Phase 1 revealed the skill needs `references/` content that doesn't exist yet, name that as an explicit deliverable gap in intent.md and route it to `/make-pack` (one research wave per axis); a knowledge skill shipped with an empty corpus is a description with nothing behind it.
2. **Behavioral assertions**: ≥ 3 checkable statements about the output ("the commit message names the ticket ID", "the report contains a verdict block").
3. **Baseline**: run 2–3 representative prompts in a fresh session *without* the skill; save outputs to `<skill-dir>/evals/baseline/`. These are the "before" evidence Phase 5 compares against.

**Gate P2:** evals.json (or the recorded skip for user-only) + assertions + baseline outputs exist.

## Phase 3 — Draft

Description first — it is the API:

1. Write 2–3 candidate descriptions; keep the one that front-loads the Phase-1 verbatim phrasings and carries the `NOT for <thing> (<owner>)` fences from the Fences slot. ≤ 1,024 chars.
2. Body from the matching skeleton in `references/templates.md`. Reference existing skills and docs for substrate; the draft carries only its delta.
3. Both invocation dials explicit; supporting material beyond ~500 lines splits to `references/` before the phase closes, one level deep.

**Gate P3:** SKILL.md + supporting files exist; dials explicit; body ≤ 500 lines.

## Phase 4 — Language pass

Invoke `prompt-wording-rules` (in this plugin) and run its **Audit** on the draft — potency lint + rubric, gated on L1/L3/L6 — then its **Rewrite** on every finding. The audit's instantiation core, applied to each load-bearing line:
1. Instantiation test: does the line commit, presuppose, or demonstrate the behavior — or only describe it? Rewrite the describers.
2. Affirmative framing; ≤ 3 hard gates in the whole body.
3. Numeric anchors on load-bearing dimensions.
4. Contracts and gates in the head; examples in the tail.
5. One labeled good/bad pair where a quality bar matters.

**Gate P4:** every load-bearing line instantiates; describers rewritten.

## Phase 5 — Validate

Three checks, in order; each has a branch:

1. **Lint (deterministic):** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/skill_lint.py" <skill-dir>/SKILL.md` — fix and re-run until clean. The same finding failing 3 times → stop and hand the finding to the user; do not suppress it. (This is a goal loop in miniature — `teamwork`'s `loop-rules` catalogs this exact gate-as-condition pattern, where installed.)
2. **Fresh-context audit (generator ≠ critic):** dispatch the `skill-checker` agent with the skill directory and a report destination `<skill-dir>/evals/audit-report.md`. Triage every finding: fix it, or accept it with a one-line note in intent.md. Blocking findings are fixed, always. Auditor and author disagree → the user arbitrates; record the ruling.
3. **Behavior check:** rerun the Phase-2 baseline prompts in a fresh session *with* the skill; compare against the assertions. A failed assertion names its failed layer — description (didn't trigger), body (triggered, wrong output), species/dials (wrong invocation path) — and the fix lands in that layer. For trigger-rate tuning at scale, the official `skill-creator` plugin's benchmark runs the evals.json automatically.

4. **Fence closure (family symmetry):** for every sibling named in this skill's NOT-clauses, add the reciprocal — a no-trigger case in *that sibling's* `evals/evals.json` carrying this skill's flagship phrasing, and (if the boundary is contested) a return NOT-clause in the sibling's description. A fence with one side is a leak waiting for `/check-routing` to find it; close it now, in the same change. Gate G8 catches stale sibling *names*; only this step closes the routing.

**Gate P5:** lint clean · zero blocking audit findings · every assertion demonstrated with/without · every NOT-clause reciprocated.

## Phase 6 — Ship

List the final tree. Confirm intent.md carries all six gates as PASS with dates — that checklist is the harness's stopping predicate: **done when P0–P5 read PASS and the deliverables exist on disk.** Close with the two operational reminders: descriptions share a 1%-of-context listing budget, so run `/doctor` after installing into a large library; and if the project mirrors skills as knowledge snapshots, refresh the snapshot from this source of record, never edit the copy.
