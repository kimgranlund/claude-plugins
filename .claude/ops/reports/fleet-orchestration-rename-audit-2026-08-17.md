# fleet-orchestration rename audit — FLOOR (2026-08-17)

Skill: /Users/kimba/Projects/nonoun/plugins/.claude/worktrees/build-522/teamwork/skills/fleet-orchestration · Standards: skill-writing-rules · Lint: clean (0 fail / 1 warn — W2, pre-existing)
Verdict: PASS

Scope: pure-rename audit (ADR-0020 wave 4, issue #522, `leading-teams` → `fleet-orchestration`) plus the standard FLOOR rubric.

## Rename-specific verification (all PASS)

| Check | Result | Evidence |
|---|---|---|
| skill_lint clean | PASS | `skill_lint.py` run: `0 fail / 1 warn`; the sole W2 warn ("model-invocable but no trigger phrasing") is pre-existing — the rename diff (HEAD~1) shows the description changed only `team-lead` → `fleet-marshal`, no trigger-phrasing regression |
| name / dir / H1 agree | PASS | SKILL.md:2 `name: fleet-orchestration` = directory stem = SKILL.md:15 H1 `# fleet-orchestration — the host runs the seat…` |
| No leftover `leading-teams` self-citation in the bundle | PASS | `grep -rn "leading-teams" <skill dir>` → exit 1 (no matches across SKILL.md, references/, evals/) |
| Internal self-citations updated | PASS | references/adopt-agent-contract.md:4,11,28 now say `fleet-orchestration` ↔ `fleet-marshal`; evals/evals.json:2 `"skill": "fleet-orchestration"`, t02 and n05 prompts renamed |
| Live cross-references updated | PASS | commands/lead-team.md:9,10,26–27 wrap/require/invoke `fleet-orchestration`; leading-planning/SKILL.md:41–42,61 and leading-builds/SKILL.md:37–38,90 cite the new path/name |
| Body coherence post-rename | PASS | Read in full (123 lines); phases 1–4, failure branches, and the done predicate all still parse as one procedure; every `fleet-marshal` mention (SKILL.md:4,19–20,24,42,49) points at the wave-3-renamed agent file, which exists (teamwork/agents/fleet-marshal.md, 74 lines) |
| Residual `leading-teams` mentions elsewhere | OK (not findings) | Only in sibling HISTORICAL audit records — teamwork/skills/leading-review/evals/audit-report.md:60,61,63,77,129 and leading-builds/evals/audit-report.md:91,106. These are dated review records describing the precedent at the time; rewriting history was out of the rename's scope. Steelman run: "should historical reports be renamed too?" — no, they cite the name as it was when the audit ran; confirmed acceptable, dismissed with the grep above as the check |

## FLOOR rubric

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | PASS | — | Sampled 3: SKILL.md:67–71 (coordinator write-discipline rule), :73–77 (explicit solo-first override), :99–102 (repair-by-locus branch) — each fails the deletion test's null case; output would differ without it | — |
| R2 | PASS | minor (pre-existing W2) | Description SKILL.md:3–9 carries trigger content ("run under the fleet-marshal agent's own contract", "/lead-team", 3 parseable NOT-for fences) and the evals suite (5 trigger / 5 no-trigger) keys on it; lacks the literal "Use when the user asks…" scaffold lint W2 wants | Optional, out of rename scope: add a "Use when…" clause — a description/boundary-tier edit owing a suite update + /check-routing per the edit ladder |
| R3 | PASS | — | Dials SKILL.md:10–11 (`disable-model-invocation: false`, `user-invocable: false`) = knowledge/model-only reach, deliberately: SKILL.md:25–28 states the /lead-team command wrapper is the human entry and this file is model-reached only. Name is noun-head orchestration handle per ADR-0011 new-mint canon. One story | — |
| R4 | PASS | — | Load-bearing lines commit ("the host does not touch Write/Edit on any charter deliverable", :67–68); uppercase hard-gate budget spent only in the description's NOT fences; body nevers are lowercase locks | — |
| R5 | PASS with findings | minor ×3 (all pre-existing, verified present before the rename via `git show a90aa70~1:teamwork/agents/team-leader.md`) | (a) SKILL.md:42–43 claims Priorities 1–8 live at "its own lines 22–69" — measured: 24–70 in fleet-marshal.md (Priority 1 at :24, Priority 8 at :68–70). (b) SKILL.md:49 cites the preloads at "agents/fleet-marshal.md:15" — measured: line 16. (c) SKILL.md:48–50 says "the same two skills the agent itself preloads" — the agent preloads THREE (fleet-marshal.md:16: `team-or-solo-rules, loop-rules, fleet-rules`); the host-adoption ritual never loads `fleet-rules`, so the adopted contract runs with one less module than the real seat | Maker, in a follow-up (not this rename PR): correct both line anchors and either add `fleet-rules` to Phase 2 step 2 or state why the host adoption deliberately omits it |
| R6 | PASS | — | Body is 123 lines (~1.5k tokens), entirely inside the 5,000-token compaction head; done/NOT-done predicate at :118–122; references one level deep | — |
| R7 | PASS | — | Output contract (write-handoff shape, :89–92), 5 named failure branches (:94–110), checkable stopping predicate (:118–122) | — |
| R8 | PASS | — | Anchors where load-bearing: 8 priorities, 4 phases, "three host deltas", "≥2 seats" (:97), "twice" re-dispatch cap (:99–102) | — |
| DM (gate scope) | PASS | — | In scope (body mentions Task/Agent dispatch throughout). Lint-mechanized DM R1–R3: 0 fail from step 1's lint line. DM-R4/DM-R5: no `context: fork` in frontmatter (:1–13) — not applicable. DM-R6: no `model:` field on the skill and no `agent:` dispatch field — no conflict possible | — |

Runtime-over-claim note: every "updated for the rename" claim in the dispatch was checked against the tree (grep sweeps, the HEAD~1 rename diff, file reads), not taken from the dispatch text; the R5(c) drift finding came from reading fleet-marshal.md:16 directly and confirming the same defect in the pre-rename `team-leader.md` via `git show`.

Top 3:
1. R5(c) — minor, pre-existing: SKILL.md:48–50 says the agent preloads two skills; fleet-marshal.md:16 preloads three (`fleet-rules` missing from the host-adoption ritual). One fix: add `fleet-rules` to Phase 2 step 2 or state the deliberate omission.
2. R5(a)/(b) — minor, pre-existing: stale line anchors (SKILL.md:42 "lines 22–69" → actual 24–70; SKILL.md:49 ":15" → actual :16). One fix: renumber both citations.
3. R2/W2 — minor, pre-existing: description lacks the literal "Use when the user asks…" scaffold. Optional boundary-tier edit with its suite update + /check-routing.

None of the three is rename-introduced; the rename itself is clean and complete.
