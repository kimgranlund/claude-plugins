# check-skill audit — pattern-sweeping (FLOOR)

Skill: /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/issue-576-sweep-skill/harness/skills/pattern-sweeping/SKILL.md · Standards: skill-writing-rules · Lint: clean
Verdict: PASS (no blocking findings; 2 major ledger/boundary findings must land before merge)

Audited 2026-08-17 per issue #576 dispatch. Delegation-mechanics gate: **not in scope** — no
`context: fork`, no subagent/dispatch/parallelism mention in body or frontmatter (checked
SKILL.md:1–123).

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | Sampled 3 load-bearing lines, each fails-if-deleted: SKILL.md:55–56 (object-literal quoted+shorthand dual-form rule — without it the 98→54 undercount recurs), SKILL.md:88–89 (assert the breaking property, never presence — model default is the presence assertion), SKILL.md:114–115 (2-failure tier-escalation rule with numeric anchor — without it the model iterates the regex) | — |
| R2 | PASS | — | Description phrasings (SKILL.md:6–8) verbatim-match evals t01/t05/t06/t07 (evals.json:5,9–11); fences in parseable `NOT for X (owner)` form (SKILL.md:9–12) repel t13–t20 (evals.json:17–24). Judged textually at floor; measured routing is a DEEP-tier item | — |
| R3 | PASS* | major (F1, filed below) | Species=procedural, `disable-model-invocation: false` + `user-invocable: true` (SKILL.md:13–14) agree with content (workflow + output contract). *Name grammar claim unverified — see F1 | — |
| R4 | PASS | — | Body is spec-present standing instructions throughout ("the run states all four", SKILL.md:30; "Each hit lands in exactly one bucket", SKILL.md:65). Hard-gate budget respected: zero uppercase NEVER/MUST NOT; locks are lowercase always/never with named neighbors (SKILL.md:70–71, 88–89) | — |
| R5 | PASS | — | Content is incident-funded (four named production failures, SKILL.md:22–26), not model knowledge or another skill's substrate. Grep of harness/authorkit skills found no drift-pair owner for census/classify/ratchet method | — |
| R6 | PASS | — | Whole body 123 lines (~1.4K tokens), fully inside the 5,000-token compaction head; output contract SKILL.md:104–110, failure branches 112–119; no references dir needed at this size | — |
| R7 | PASS | — | Output contract with 6 ordered sections (SKILL.md:106–110); 3 named failure branches (SKILL.md:114–119) incl. UNMEASURED path; checkable stopping predicate + NOT-done clause (SKILL.md:121–123) | — |
| R8 | PASS | — | Numeric anchors on load-bearing dims: "1–2 members" (SKILL.md:53), "fail 2 times" (SKILL.md:114), "exactly one bucket" (SKILL.md:65), tier ladder enumerated (SKILL.md:114–115) | — |

## Judgment findings (one home each)

**F1 · major · intent.md:15 — claimed ProcessLex registration does not exist in the tree.**
intent.md states "new ProcessLex token `sweeping` registered in `naming.manifest.json`". Runtime
check (structured walk of /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/issue-576-sweep-skill/naming.manifest.json):
`process_lex` contains no `sweeping`; only `verb_lex[21]='sweep'` and `exemptions[77]='sweep-chores'`
exist. Either the name `pattern-sweeping` fails authorkit's naming-audit grammar at the ship gate,
or the intent record is false. Fix: register `sweeping` in `process_lex` in the same change (keep
the exemptions array flat, as the intent line itself requires), and only then keep the ledger line.

**F2 · major · intent.md:24 — reciprocal-fence claim is false; boundary is one-directional.**
intent.md P5 states "fences reciprocated in sweep-chores + authorkit naming-audit/bloat-audit
suites". Runtime check: `grep -r "pattern-sweeping"` over all three skill directories returns
zero hits; sweep-chores' own fences (its SKILL.md:8–10) name only single-item triage and
teamwork's build path — nothing repelling a code/pattern sweep. Steelman ("a generic fence already
covers it") checked and failed: no such fence exists. "Sweep the repo for X" prompts are ambiguous
between the two skills until the reciprocal near-misses land. Fix: add no-trigger cases naming
`pattern-sweeping` as owner to sweep-chores', naming-audit's, and bloat-audit's `evals/evals.json`
in this same change (the description/boundary edit tier owes the suite update in the SAME change),
then one `/check-routing` run at the wave boundary.

**F3 · minor · intent.md:24 vs intent.md:32–34 — P5 pre-records this audit's outcome.**
The ledger claims "skill-checker audit: no blocking findings, 2 accepted-with-note (below)" while
the Accepted-with-note section still reads "(filled after audit)" — the claim predates its
evidence. Fix: rewrite the P5 line from this report's actual verdict and fill the section.

**F4 · nit · SKILL.md:49 — bundled script referenced by relative path.**
`scripts/pattern_census.py` resolves via the base-directory line injected at invocation (steelman
survives for the invoke path), but skill-writing-rules' stated convention for plugin-shipped
scripts is the `${CLAUDE_PLUGIN_ROOT}` form, which also survives copy-paste out of context.
Optional hardening; never blocks.

## Runtime checks performed (checking-rules compliance)

- Lint: `skill_lint.py` run for real → `clean` (verdict line above), not re-derived.
- Script: `python3 scripts/pattern_census.py selftest` → exit 0, "SELFTEST OK: 5 checks (2 member
  proofs, 1 nonmember proof, 2 negative controls)". The script's --must-match/--must-not-match
  flags cited in SKILL.md:54,58 exist and bite (negative controls prove non-inertness).
- Baselines: evals/baseline/ contains 2 real capture files (read baseline-1 head — genuine
  skill-absent transcript, not a stub). The P5 claim "all 3 assertions hold with skill, absent
  without" is **UNVERIFIED** at floor (captures exist; comparison not re-run here).
- Dismissals: F4's downgrade cites the base-directory injection check; F2's steelman cites the
  sweep-chores SKILL.md fence grep that failed to support it.

Top 3: 1) F1 — register `sweeping` in process_lex or the ship gate contradicts the ledger.
2) F2 — land the reciprocal near-miss evals in sweep-chores/naming-audit/bloat-audit in this
change. 3) F3 — rewrite intent.md P5 from this report and fill Accepted-with-note.
