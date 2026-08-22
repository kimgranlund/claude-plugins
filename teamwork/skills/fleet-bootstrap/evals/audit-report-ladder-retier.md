# Audit — 2026-08-22 ladder retier + tier-reconcile amendment (FLOOR)

Skill: teamwork/skills/team-scaffolding + teamwork/skills/fleet-bootstrap (coordinated amendment,
incl. fleet-bootstrap/references/fleet-manifest-schema.md) · Standards: skill-writing-rules,
checking-rules · Lint: clean (both SKILL.md files, `skill_lint.py` run 2026-08-22)
Verdict: PASS — no blocking finding; 3 majors, 2 minors, 1 open question

Paths are relative to `/Users/kimba/Projects/nonoun/plugins/`.

## Dispatch questions, answered

1. **Tier-value consistency across the three edited files — CLEAN.** team-scaffolding
   SKILL.md:199-209, fleet-manifest-schema.md:19-22 (example JSON) and :74-76 (prose), and
   fleet-bootstrap SKILL.md:90-93 all state agent sonnet+high · reviewer sonnet+high · planner
   fable+medium · product sonnet+xhigh, each dated 2026-08-22 with the prior 2026-08-16 ladder
   named as superseded. The repo's own `.claude/ops/fleet.json` seats block matches
   (justification_date 2026-08-22 on all four). fleet-bootstrap Phase 1 point 4's comms-charter
   line (SKILL.md:90-93) agrees with team-scaffolding's agent row including the #313 fork-price
   rationale — no contradiction.
2. **Stale fable-heavy residue — FOUND, outside the three edited files** (finding F3): the old
   product row (`fable+high`) survives in `teamwork/agents/product-leader.md:30` (body) and
   `teamwork/skills/bind-product/SKILL.md:66-68`, while product-leader.md's frontmatter is
   already retiered to `model: sonnet` / `effort: xhigh` (:12-13). The retired fable+low marshal
   justification: no surviving occurrence anywhere in teamwork (grep for `fable+low` — zero hits).
3. **Reconcile three-outcome coherence — coherent in structure, two defects in the staleness
   test** (F1 boundary applies to the bind wiring, F2 to the test itself; see table). The
   ladder's ruling date IS decidable from data the file holds — "retiered 2026-08-22, Kim's
   ruling" at fleet-manifest-schema.md:74-77 — so this is not the feared hard gap, but the date
   is an unlabeled parenthetical inside the `seats.<role>.tier` field bullet, duplicated in
   team-scaffolding SKILL.md:197, and the reconcile section (:200-215) that consumes it never
   names it (F4).
4. **Wiring-by-citation consistency between the two bind paths — INCONSISTENT** (F1): the
   schema's §"Tier reconcile on every bind" (:204-206) claims "EVERY `fleet-bootstrap` Phase 0
   read of an existing manifest, and every `team-scaffolding` bind against one" runs the diff.
   fleet-bootstrap Phase 0 wires it (SKILL.md:38-41) and team-scaffolding's role-token branch
   wires it (SKILL.md:46-49), but team-scaffolding's BARE-invocation manifest-present branch
   (SKILL.md:69-81) binds via "proceed to Phase 2 as if it had been the `$ARGUMENTS` token"
   without ever running the reconcile — Phase 2 (:101-119) contains no reconcile step either.
5. **justification_date now spurious for planner?** No — dismissed with a cited check: the field
   bullet (:78-82) states a minimum ("required whenever tier deviates"), not a biconditional;
   both seed paths deliberately write it on every canonical-tier seat (fleet-bootstrap
   SKILL.md:32-33 "today's date as `justification_date` for every seat still at its canonical
   tier"; team-scaffolding SKILL.md:43-45), and the reconcile reads it only on mismatch rows
   (:207-215), so a match-row date is inert. A one-clause hardening is still worth it (F5).

## Findings

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| F1 | FAIL | major | fleet-manifest-schema.md:204-206 ("every `team-scaffolding` bind") vs team-scaffolding SKILL.md:69-81 — bare-invocation manifest-present branch reaches Phase 2 with no reconcile; the stranded-old-ladder class the amendment exists to close survives on the most common interactive path | In team-scaffolding Phase 1, hoist the reconcile to a branch-neutral clause — "manifest present (either branch), run the tier reconcile before any bind proceeds" — or add the same one-line citation to the bare branch's step 2/3 |
| F2 | FAIL | major | fleet-manifest-schema.md:209-215 — "justification_date NEWER than the current ladder's ruling date" is strict, but the stale-mismatch branch's own keep outcome records "today's `justification_date`" (:213-214); a keep executed ON the ruling day (today, 2026-08-22) yields date == ruling date, which the strict test re-classifies as stale on every subsequent bind — the reconcile's own output loops back as its own finding | Change "newer than" to "on or after" (>=) in the justified-mismatch bullet |
| F3 | FAIL | major | agents/product-leader.md:30 ("**Seat tier: fable+high**, the planning-tier ceiling") contradicting its own frontmatter :12-13 (`model: sonnet` / `effort: xhigh`); skills/bind-product/SKILL.md:66-68 instructs printing "fable+high ... (product-leader.md's own line)" verbatim in the adoption acknowledgment — a live product-seat bootstrap now announces the retired tier while fleet.json records sonnet+xhigh | Update both lines to sonnet+xhigh with the 2026-08-22 retier date; team-scaffolding SKILL.md:208-209's "matching `product-leader`'s own frontmatter" claim then holds against body and frontmatter alike |
| F4 | PASS (with gap) | minor | fleet-manifest-schema.md:200-215 — the reconcile's comparand (ladder ruling date) exists only as unlabeled parenthetical prose at :74-77, duplicated at team-scaffolding SKILL.md:197; decidable today, silently wrong on the next retier if either prose date is missed | Add one named line inside the reconcile section — "Current ladder ruling date: 2026-08-22 (update on every retier; this is the date the staleness test compares against)" — making it the single comparand |
| F5 | PASS | minor | fleet-manifest-schema.md:78-82 ("required whenever `tier` deviates") vs fleet-bootstrap SKILL.md:32-33 and team-scaffolding SKILL.md:43-45 (both seed it on canonical rows; example JSON :19-22 shows it on all four) | Append one clause to the field bullet: "also present, seed-dated, on canonical-tier rows — presence never implies deviation" |
| R1-R8 | PASS | — | Sampled load-bearing lines survive deletion (team-scaffolding:199-201 fork-price rationale; fleet-manifest-schema:76-77 "NOT silently correct"; fleet-bootstrap:38-41 never-silently-passed-over) — each changes reconcile/charter output if cut (R1). Both skills command species, `disable-model-invocation: true` + `user-invocable: true` explicit, descriptions are slash-menu docs — no routing-suite impact from these body-only edits (R2/R3). Reconcile stated as standing spec-present rules; canonical-home citation, not restatement, in both SKILL.md wirings (R4/R5). Three-outcome table + unattended branch = named failure handling; "match = quiet" is a checkable predicate (R7). Dated anchors throughout (R8) | — |
| DM-R4/5/6 | PASS / n-a | — | Neither skill carries `context: fork` or `model:` frontmatter (team-scaffolding:1-19, fleet-bootstrap:1-18); dispatch topology in fleet-bootstrap Phase 5 already lint-mechanized (lint clean) | — |

## Steelman record (checking-rules)

- F2 rebuttal considered — "newer" might be read loosely as "not older": rejected; the keep
  branch's own text (:213-214) manufactures the equal-date case on the ruling day itself, and
  this repo's fleet.json was rewritten that exact day. Finding survives.
- F1 rebuttal considered — "as if it had been the `$ARGUMENTS` token" might imply replaying the
  role-token branch including its reconcile: rejected; SKILL.md:80-81 routes to Phase 2, and the
  branch separately re-implements the collision guard (missing-seats-only offering, :72-74),
  showing the role-token branch's Phase-1 machinery is NOT replayed. Finding survives.
- F5 near-finding dismissed with the cited biconditional check (Dispatch answer 5 above).

## Open question (not a finding of this amendment)

`agents/review-leader.md:11-12` and `agents/planner.md` sit at `fable+medium`. planner matches
the new ladder's planner row. review-leader is the checker-family dispatcher; if the
"checker-family row" is now sonnet+high (team-scaffolding SKILL.md:203), the agent-frontmatter
sweep that retiered product-leader may owe review-leader a pass too — governed by
`agent-writing-rules` §Model tiering, out of this amendment's three-file scope. Flag to the maker
for a ruling, not fixed here.

Top 3: 1) F1 — wire the reconcile into team-scaffolding's bare-invocation bind path (the schema's
"every bind" claim is currently false for it). 2) F2 — ">=" not ">" on the justification-date
staleness test, or every same-day-kept deviation re-flags forever. 3) F3 — retire the two
surviving `fable+high` product-tier lines (product-leader.md body, bind-product Phase 2) that a
live bootstrap now prints verbatim against the new ladder.

Review: floor tier, fresh context, read-only — no audited file edited. Maker applies fixes.
