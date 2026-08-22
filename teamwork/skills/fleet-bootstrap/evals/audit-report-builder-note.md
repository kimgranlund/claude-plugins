# Floor-tier audit — fleet-manifest-schema.md "Why there is no `builder` seat here" section (2026-08-22)

Skill: teamwork/skills/fleet-bootstrap · Standards: skill-writing-rules, checking-rules · Lint: clean
(`skill_lint.py` on SKILL.md — the edited file is `references/fleet-manifest-schema.md`, out of lint scope; SKILL.md itself unchanged and clean)
Verdict: PASS

Scope: targeted semantic amendment — the new section at `references/fleet-manifest-schema.md:156-165`, inserted before "Doctrine-audit hook" (line 167). Floor-tier per dispatch.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| Accuracy vs. source of truth | PASS | — | mobilize-chores/SKILL.md:230-231 (`Agent(subagent_type: "teamwork:build-leader", name: "build-<ticket-id>")`), :241-243 (convention named, one-ticket-one-dispatch) confirm the schema note's claim that step 5 names every build-leader dispatch `build-<ticket-id>` | none |
| Concurrency claim | PASS | — | mobilize-chores/SKILL.md:252-253 ("parallel, independently-isolated builds") supports "several build-leader dispatches concurrently, one per in-flight ticket" | none |
| Resumability claim | PASS (confirmed via steelman) | — | Initially flagged "idle-and-resumable (SendMessage) after its first return" as mismatching step 5's write-gate-hold rationale; steelman check cleared it — mobilize-chores/SKILL.md:237 states an unnamed dispatch has "no seat left to address afterward", the direct contrapositive of the schema note's claim | none |
| R4 register | PASS | — | schema.md:165 "This is not a gap to fill later; it's the considered shape" — instantiates (commits), matching the doc's ruling register (cf. :51 "considered and declined") | none |
| R5 restatement / drift pair | PASS with nit | nit | schema.md:162-163 duplicates the literal `build-<ticket-id>` string owned by mobilize-chores/SKILL.md:241; owner is named, so acceptable reference — but a rename there now has two homes to update | acceptable as-is; if step 5's convention ever changes, this line is the drift partner |
| Analogy precision | — | nit | schema.md:164 "exactly like `planner`'s `"background"` mode above" — planner's mode (:68-69) is a standing long-lived seat WITH a fleet.json row; `build-<ticket-id>` is per-ticket and rowless. The sentence's own "without needing a fleet.json row" already draws the distinction, but "exactly like" overclaims | soften to "the same named-`Agent`-dispatch mechanism as `planner`'s `"background"` mode" |
| House citation style | — | nit | schema.md:156 carries only a date; every sibling rationale note cites its ruling issue (#410 :4, #586 :51, #853 :76) | if a governing issue/ticket exists for this ruling, add its number to the heading |
| Placement | PASS | — | Section sits after Fields, before Doctrine-audit hook (:156, :167) — the same design-rationale register and position class as the role-key-migration note (:51-59); not out of place | none |

Checks run (checking-rules compliance):
- Runtime over claim: mobilize-chores/SKILL.md:225-259 read directly; the schema note's three factual claims (naming convention, per-ticket concurrency, SendMessage addressability) each traced to a cited line.
- Steelman: the resumability finding was drafted, rebutted by :237's contrapositive, and dropped — recorded in the table above.
- Dismissals: the "out of place" question dismissed with the :51-59 sibling-note comparison cited.

Top 3: 1) nit — soften "exactly like" (:164) to name the shared mechanism, not identity. 2) nit — add the ruling's issue number to the heading (:156) to match sibling notes. 3) note — `build-<ticket-id>` now lives in two files; mobilize-chores/SKILL.md:241 is the owner if they ever diverge.
