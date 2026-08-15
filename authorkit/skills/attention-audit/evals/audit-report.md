# attention-audit — fresh-context FLOOR review (check-skill)

Skill: authorkit/skills/attention-audit · Standards: skill-writing-rules · Lint: clean
Verdict: **PASS** (re-verified 2026-08-15 after fixes — see "Re-verification" at the end; the original FAIL verdict and findings are preserved below as the record)

Original verdict (first pass, same day): **FAIL** (one blocking finding — the collision procedure's `--top 40` window misses its own proving fixture on the live estate)

Reviewer: audit-attention-skill (fresh context, 2026-08-15). All four bundled selftests run live: rent/collide/usage/trend all PASS. Live estate runs executed for rent.py, collide.py, and evals/check_known_pairs.py.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 behavior delta | PASS | — | SKILL.md:48-51 (agent chars bill unconditionally → weighting), SKILL.md:78-82 (zero usage alone NOT a finding), SKILL.md:37-39 (separate series, no quotient) — each fails the deletion test in the right direction | — |
| R2 trigger fidelity | PASS | — | Description phrasings (SKILL.md:8-12) match evals t01-t04 verbatim; fences (SKILL.md:12-14) repel n02/n03/n05/n07 by naming check-routing, bloat-audit, check-skill | — |
| R3 species/dials | PASS | — | Procedural species, both dials explicit (SKILL.md:18-19), name follows the naming-audit/bloat-audit sibling grammar; intent.md:3-4 agrees | — |
| R4 register | PASS | — | Instantiating lines throughout ("a count derived in prose is a defect", SKILL.md:33-34); hard gates = 3 (never rewrites, never one quotient, two-signal floor) | — |
| R5 no restatement | PASS | nit | Two-signal floor and the routing-twin/boilerplate/coincidence taxonomy each live in three homes: SKILL.md:59-66+77-79, REPORT-TEMPLATE.md:24-26, and collide.py:197-199's trailer text — a drift-triple to watch | Accept for now; if the taxonomy changes, all three must move in one change |
| R6 position | PASS | — | Whole body ≈1.2k tokens; gates and contract all in-head; references/ one level deep (SKILL.md:109-113) | — |
| R7 contracts | **FAIL** | **blocking** | See F1 below. Also minor: no explicit "Done when" stopping predicate — the procedure ends implicitly at step 7's render (SKILL.md:88-92); degraded modes are well named (SKILL.md:94-100) | F1 fix + one "Done when the report is rendered and every finding names an owner" line |
| R8 quantities | PASS | — | `--top 40` (SKILL.md:52-53), 2-of-3 signal floor (SKILL.md:77), chars/4 token estimate (REPORT-TEMPLATE.md:13) | — |

## F1 (blocking) — step 3's `--top 40` window cannot surface the skill's own proving fixture

intent.md:40 (P3) claims "collide 3/3 recall on the known-real pairs." Measured on the live estate (this worktree, default threshold 9.0): 3,346 pairs flag; the three known-real pairs from evals/baseline/collide.md rank **171 / 1000 / 1682** overall, and still **77 / 650 / 1186** after filtering to cross-plugin non-family pairs. The procedure as written (SKILL.md:52-53, `--top 40`) therefore produces a report in which *all three* pairs the skill was built to catch are absent — the recall claim is true only of the unbounded flag list nobody reads. The top-40 window is dominated by boilerplate-tax template pairs (watch-adrs↔watch-tickets, checker/lead wording), exactly the class the body says to dismiss. This is not the documented limitation (intent.md:50-52 covers semantic twins built from estate-common words; the naming pair shares the *distinctive* term "naming" and still ranks ~1186).

Note the `--against` write-time path (SKILL.md:57-58) is unaffected — scoped to one artifact, the known pairs do surface. The estate-sweep path, the skill's primary charter, is where recall dies.

Fix options (pick one, then amend intent.md P3's recall claim in the same change — falsified claims amend in place):
1. Bucketed reporting: collide.py already computes `cross_plugin` and `family` (collide.py:126-128) — report top-N *per class* (cross-plugin non-family first) instead of one global top-N, and/or discount shared boilerplate sentences (terms appearing in >K descriptions of the same role family).
2. Procedure-level: step 3 additionally runs `--against <name>` for every artifact edited since the last audit, making the sweep + pre-lint pair the recall mechanism, and the body stops implying the global top-40 catches the known class.

## F2 (major) — the recall harness cannot bite

evals/check_known_pairs.py prints `MISSED` on a lost pair but returns 0 unconditionally (check_known_pairs.py:27,31). A recall regression — or F1 itself, had the harness checked rank-within-window rather than presence-anywhere — exits green. Per the workspace's incident→infrastructure invariant this check must fail (exit 1) when a known pair is missed, and should assert the pair lands *inside the reported window*, not merely inside the unbounded list. (It sits under evals/, so G4's scripts/ selftest sweep doesn't cover it; it also has no selftest mode — fine for placement, but then its own exit code is the only teeth it has.)

## F3 (minor) — flag-name inconsistency across bundled siblings

rent.py and collide.py take `--target` (rent.py:145, collide.py:168); usage.py takes `--estate` (usage.py:119). The body documents each correctly so nothing breaks, but the inconsistency is friction for the operator and for the allowed-tools patterns' symmetry. Rename usage.py's flag to `--target` (keep `--estate` as an alias if the baseline scripts reference it).

## Verified clean (evidence)

- skill_lint: clean. Description 692 chars (under the 1024 cap, post-diet).
- All four selftests PASS with correct exit 0; collide.py's live run correctly exits 1 on findings (tri-state contract, collide.py:200).
- Script interfaces match every command line the body cites (rent `--target --json`; collide `--target --json --top --against`; usage `--estate --lineage`; trend `--rent --routing-report --out`).
- rent.py live run reproduces the skill/agent split and the zero-rent exclusion (authorkit: 9 routable/4,960ch, 3 agents/722ch, separate token figures).
- collide.py selftest proves the fence-defuses rule, the negative control, and determinism (collide.py:151-160).
- Evals: 10 trigger + 10 fence cases, t01-t02 verbatim user phrasings, every fence case names its owner.
- Composition claim (SKILL.md:102-107) is consistent with intent.md ruling on overhaul-execute wiring; the attention-audit-agent twin exists (it appears in the live collide output).

Top 3: 1) F1 — rework collide's reporting (bucketed top-N per class, or make `--against` the recall path) and amend P3's recall claim; 2) F2 — make check_known_pairs.py exit 1 on a miss and assert in-window rank; 3) add a one-line stopping predicate and unify usage.py's `--estate` → `--target`.

---

## Re-verification (same reviewer, fresh runs, 2026-08-15)

All three findings confirmed fixed by my own runs — verdict flips to **PASS**.

- **F1 confirmed fixed.** collide.py now selects per-artifact nearest neighbors (`neighbors()`, k=5 default, collide.py:132-150); `--top` only caps display *after* selection (collide.py:191-192, 211-212) and step 3 no longer prescribes it (SKILL.md:52-60). Live run via check_known_pairs.py: the distinctive-vocab fixture pair break-down-problem↔break-down-layout is **IN-REPORT at rank 166 of 491** rendered pairs, exit 0. The other two baseline pairs are honestly reclassified with measured evidence as the two LLM-tier classes — common-words twins (check-skill↔bloat-audit, skill df=52) and crowded-territory twins (naming-rules↔naming-conventions, naming df=23) — documented in SKILL.md:69-75 and check_known_pairs.py:13-20, and intent.md P3 (line 40) carries the dated amendment note replacing the falsified "3/3 recall" claim. The `--against` write-time path correctly bypasses neighbor selection (collide.py:206-209). The new OWN_MAX=10 ownership cap (collide.py:26-28) also cut noise: 3,346 → 1,650 unbounded pairs, 491 rendered.
- **F2 confirmed fixed and proven to bite.** check_known_pairs.py checks presence in the *rendered neighbors report*, not the unbounded list, and returns 1 on any miss (check_known_pairs.py:27-44). Bite proven live: run against a root lacking the fixture pair (authorkit alone) → `MISSED FROM REPORT`, **exit 1**; run against the full estate → in-report, exit 0.
- **F3 confirmed fixed.** usage.py takes `--target` with `--estate` kept as an alias (usage.py:119-120), docstring and SKILL.md step 4 (SKILL.md:76) updated; the body now ends with a checkable Done-when predicate (SKILL.md:101-104).
- All four script selftests re-run: PASS. skill_lint re-run on the edited SKILL.md: clean.

Residual nits (non-blocking, no action required):
- Step 3 says "classify every reported pair" and the full-estate neighbors report is ~491 pairs — a real but bounded judgment workload; the three-class triage makes it tractable, and `--top` exists if an operator wants a cap.
- `neighbors()` has no case in collide.py's own selftest; its proof lives in evals/check_known_pairs.py, which G4's scripts/ sweep does not run. Acceptable while check_known_pairs stays in the eval loop; worth a selftest case if neighbors() ever grows logic.
