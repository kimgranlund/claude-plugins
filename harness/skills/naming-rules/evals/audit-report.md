# Audit report — naming-rules (floor, post-write)

Skill: forge 1.14.0/skills/naming-rules · Standards: skill-authoring-standards · Lint: clean
Verdict: PASS

Audited 2026-07-20 · Depth: FLOOR (`skill-review` procedure) · Auditor: skill-auditor
Lint verdict line (run, not re-derived): `skill-postwrite-invocation-lint · clean · …/naming-rules/SKILL.md`

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| R1 | pass | — | SKILL.md:31 (registry-verb — deleting it restores synonym sprawl the delta section documents, intent.md:13-15); SKILL.md:69-70 (`-rules` carries its activity — deleting it re-licenses `doc-rules`); SKILL.md:33 (loud-contrast — deleting it re-licenses suffix-only sibling names). All three fail-if-deleted. | — |
| R2 | pass (1 minor) | minor | Triggers: "what should we name this skill" (SKILL.md:5), "is this name too vague" (SKILL.md:6), "name this so it reads like plain English" (SKILL.md:6-7) — all verbatim in the description; evals.json t01-t15 cover the three vocabularies. Fences in parseable `NOT for <x> (<owner>)` form (SKILL.md:8-11). **Minor:** the fence cites "skill-authoring-standards / agent-authoring-standards §Naming" — verified: agent-authoring-standards HAS `## Naming` (agent-authoring-standards/SKILL.md:96), but skill-authoring-standards has NO §Naming; it delegates the naming grammar to corpus Vol 2 (skill-authoring-standards/SKILL.md:18). The fence repels correctly; the owner citation is half-stale on arrival. | Reword the fence owner: "agent-authoring-standards §Naming / corpus Vol 2 + skill_lint (skill grammar)". Description edit ⇒ tier 2: suite check in same change. |
| R3 | pass | nit | Frontmatter: `disable-model-invocation: false` + `user-invocable: false` (SKILL.md:12-13) = knowledge (model-only), matching intent.md:3-4 and the species table; both dials explicit; preloadable state correct. **Nit:** the name `naming-rules` self-instantiates the NEW paradigm's knowledge shape inside a legacy-grammar estate (legacy head would be `naming-standards`). Intentional and already flagged in intent.md:43-44 for PR override; kind still reads as knowledge noun; lint clean. No action beyond the existing flag. | none (flag already recorded) |
| R4 | pass | — | Declarative register throughout — rules stated as world-state ("A proposed name passes all five or gets reworked", SKILL.md:25; "Shipped names are APIs", SKILL.md:20-21); zero imperatives mid-catalog; zero uppercase hard gates (lint W7 clean); lowercase locks with forbidden neighbors named (SKILL.md:70 "`doc-writing-rules`, never `doc-rules`"). Every section labeled normative/illustrative (SKILL.md:23,35,45,67,85,99) — the knowledge-species labeling rule met in full. | — |
| R5 | pass (1 minor) | minor | **Minor — two attributed restatements = drift pairs:** (a) reserved-word escape (SKILL.md:78-80) restates skill-authoring-standards' failure catalog F8 row; (b) term-of-art exception (SKILL.md:81-83) restates skill-authoring-standards/SKILL.md:47 nearly verbatim ("normalizing … destroys its exact-phrase match"). Both cite their source and date, so drift is traceable. Steelman (rebuttal considered pre-filing): the paradigm must carry both rules to be self-sufficient for new-name proposals — this survives for the RULE, not for the restated rationale. Finding kept at minor, scoped to the rationale prose. | Keep each rule as one line + owner pointer + the paradigm-local example (`entry-file-rules`); drop the restated rationale sentences. Drift pair partner: skill-authoring-standards (§Name-grammar exception; failure catalog F8 row). |
| R6 | pass | — | 104 lines total; normative content (tests, shapes, registry, refinements) occupies SKILL.md:23-83; illustrative examples in the tail (SKILL.md:85-104); references one level deep (references/estate-rename-map.md, 90 lines, labeled "illustrative, not ratified" at map:3 — matches the SKILL.md:104 claim). | — |
| R7 | n/a | — | Knowledge species — output contract / failure branches / stopping predicate not required. | — |
| R8 | pass | — | Load-bearing dimensions anchored: 5 tests (SKILL.md:23), one-verb-per-concept registry of 14 rows (SKILL.md:50-65), "siblings differ by a whole word" (SKILL.md:33). "Words a child knows" is operationalized by the registry itself rather than left as a vague quantifier. | — |

## Runtime verifications performed (claims vs tree)

- Lint run for real; verdict pasted above (not re-derived).
- intent.md:37 claims "15 trigger / 7 no-trigger" — counted in evals.json: t01-t15, n01-n07. Matches.
- intent.md:37 claims 3 fresh-context baselines — evals/baseline/ contains b1-b3. Present.
- Fence owners exist: `plugin-decompose`, `git-campaign-workflows`, `plugin-authoring-standards` (n05 comment) all present under forge 1.14.0/skills/. `§Naming` pointer: half-stale (see R2).
- estate-rename-map plugin-layer table: 9 rows, matching the "9 plugins" claim (map:22-32); "~130 members" hedged, not exactly counted — acceptable as-written.

## Findings summary

BLOCKING: 0 · MAJOR: 0 · MINOR: 2 · NIT: 1

Top 3:
1. (minor, R2) Fence cites a nonexistent "skill-authoring-standards §Naming" — repoint at agent-authoring-standards §Naming / corpus Vol 2; suite check owed in the same change (description-tier edit).
2. (minor, R5) F8 and term-of-art restatements are drift pairs with skill-authoring-standards — compress each to rule + owner pointer + paradigm-local example.
3. (nit, R3) Self-paradigm name in a legacy estate — already flagged in intent.md rulings for PR override; no further action.

Maker applies the fixes. intent.md P4 (language) and P5 (validate) remain PENDING; this floor audit does not clear them.
