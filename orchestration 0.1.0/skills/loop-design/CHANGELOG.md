# Changelog — loop-design

## 2026-07-03 — excellence-campaign batch 2 fixes
Deep-review fixes against `skills-audit/references/standard-of-excellence.md` v2 (ledger: `skills-audit/campaign/batch-2/loop-design.findings.jsonl`):
- **M2** the rubric's own vocabulary added to the triggers ("write a verifiable end-state condition", "add a turn cap / bound an autonomous run", "it keeps retrying the same failure", "the agent spins / thrashes and burns turns"); "setting up" → "writing or auditing"; routing corpus of record checked in (`scripts/routing-corpus.json`, 12 pos / 11 neg). Pass 1 exposed a fenceless grab into orchestration-design territory — fixed by adding the fence, never weakening positives. Final F1 0.917, every miss/grab dispositioned.
- **S2** the delegation edge is now real both ways: References table gains the [[orchestration-design]] row (the loop delegates work → dispatch/composition design), and the description fences it ("NOT for how the delegated work composes … this skill owns only when the next turn fires").
- **N3** "auto mode" in the description is now substantiated: best-practices gains an approval-plane section (auto mode decides who approves each call, never when turns fire; once the human gate is gone, cap + scope guard + escalation are the only brakes; △ build-variance marked).
- **S1** Improve and Update organs added (maker template): Improve = review + targeted redesign; Update fires when the build changes — the △ verify-against-your-build markers are the micro-mechanism it sweeps (they mitigate drift; the Update pass closes it).
- **S5** the generator ≠ critic pass names its critic: the shared **doc-reviewer** agent (goal conditions are in its charter).
- **A2** plane separation stated once (:12, handle defined) and invoked at :15 — the duplicate bullet collapsed.
- **L** SKILL.md closes on the done/NOT-done predicate.
