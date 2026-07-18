# Floor audit — open-questions-sweep (first-draft review, 2026-07-18)

Skill: forge 1.14.0/skills/open-questions-sweep/SKILL.md · Standards: skill-authoring-standards · Lint: clean
Verdict: PASS

Depth: FLOOR (skill-review procedure). Reviewed against its own intent.md (trigger set, delta,
4 fences, 4 assertions) and evals/ (12 trigger / 10 no-trigger + 2 baseline scenarios).

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | SKILL.md:29-31 (ONE batched call, 1-4 q × 2-4 opts — baseline scenario-open-items.md:28-35 proves the no-skill output is a prose dump, so deletion changes output); SKILL.md:27-28 ("nothing open" one-liner); SKILL.md:40-42 (>4-items batching rule) | none |
| R2 | PASS | minor | Description phrasings SKILL.md:6-8 match evals t01/t03/t04 verbatim and intent.md:9-14; fences SKILL.md:9-12 mirror intent.md:35-38 and repel n03/n04/n05. Minor: n01 ("What's still open in the GitHub issue backlog?") shares the strong "still open" trigger phrase, but the ops-issues fence keys on "tracking or filing" — a backlog *query* is neither verb | Broaden the fence: "NOT for querying, tracking, or filing work items in an external tracker/backlog (ops-issues)" — re-budget first (description is 816/1,024 chars; room exists) |
| R3 | PASS | — | Procedural + `disable-model-invocation: false` + `user-invocable: true` (SKILL.md:13-14), both dials explicit; name head `-sweep` is a zero-derivation verb; matches intent.md:3-4 incl. the recorded knowledge→procedural correction (intent.md:75-77) | none |
| R4 | PASS | — | Load-bearing lines commit/presuppose: SKILL.md:27-28 ("Nothing qualifies → report… and stop there"), :30-31 ("One call covers every item"), :43-44 ("drops from the batch"). Zero uppercase hard gates (≤3 budget untouched); bad-side example labeled "do not imitate" (SKILL.md:60) | none |
| R5 | PASS | — | No restated substrate: AskUserQuestion mechanics not re-taught; intent-extract/loop-design/ops-issues referenced by name (SKILL.md:9-12), never copied. Step 1's grounding rule (SKILL.md:25-26) is a delta, not model knowledge | none |
| R6 | PASS | — | 63-line body; output contract at :35-37, failure branches :39-44, done-predicate :46-47 — all in the head; the worked example is the tail (:49-62); no references dir needed | none |
| R7 | PASS | nit | Output contract (SKILL.md:35-37, exclusive two-outcome), 2 named failure branches (:40-44), checkable stopping predicate (:46-47). Nit: predicate requires items "answered", but no branch covers the user dismissing/skipping the AskUserQuestion round — "answered" is then unreachable | Add a branch: "user dismisses the round → report the items as still open in one line; do not re-ask" |
| R8 | PASS | nit | Numeric anchors on every load-bearing dimension: 1-4 questions, 2-4 options (SKILL.md:29-30), top-4 batching (:40), one-line report (:27), ONE call (:29). Nit: "a natural closing point in a long session" (SKILL.md:8) is vague, but it sits on the trigger surface where a numeric anchor would be false precision | leave, or accept as-is |

## Cross-cutting finding (outside the R-table, one home)

**MAJOR — reciprocal fences not closed in sibling suites.** The workspace invariant (plugins
CLAUDE.md, "Descriptions are the routing surface") requires a new model-invocable description to
close reciprocal fences in sibling suites in the same change. open-questions-sweep's suite fences
*toward* intent-extract (n03/n06), ops-issues (n01/n09), and loop-design (n04/n08), but no
sibling suite gained a no-trigger case *back*: grep across `skills/*/evals/evals.json` for
"wrap"/"still open"/"loose end" matches only this skill's own suite. Nearest grab risks:
intent-extract ("resolve them with low-effort multiple-choice questions" vocabulary vs t02) and
handoff-compose (session-close vocabulary vs t12). Fix: add 1-2 no-trigger cases (e.g. "Before we
wrap up, is there anything still open?") to `intent-extract/evals/evals.json` and
`handoff-compose/evals/evals.json`, then one `/eval-run forge` at the wave boundary.

## Intent-contract check (dispatch ask: judge against its own stated contract)

- All 4 intent.md assertions land in the body: A1→step 3 (:29-31), A2→step 1 (:25-26),
  A3→step 4 (:32-33), A4→step 2 (:27-28).
- All 4 intent.md fences (:35-38) appear verbatim-equivalent in the description (:9-12).
- All 4 should-trigger phrasings (intent.md:9-14) appear in the description or as suite cases.
- Baseline correctly isolates the delta as the closure mechanism, not the noticing
  (scenario-open-items.md:28-35) — the body spends its lines on exactly that. Encoded-preference
  brevity ruling (intent.md:78-81) honored: 63 lines, sequence stated, stop.

Top 3:
1) (major) Close the reciprocal fences: add no-trigger cases for the wrap-up phrasings to
   intent-extract's and handoff-compose's suites, one `/eval-run` at the boundary.
2) (minor) Broaden the ops-issues fence to cover backlog *queries*, not just tracking/filing —
   n01 currently relies on the router inferring "backlog = tracker".
3) (nit) Add the user-dismisses-the-round failure branch so the "answered" stopping predicate
   has an exit.
