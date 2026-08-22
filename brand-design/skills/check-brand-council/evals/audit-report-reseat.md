# Audit — #849 SEATING reseat (george-l/nick-l → creative), v0.11.2

Skill: brand-design/skills/check-brand-council (+ council-rules ref, creative-convener agent) · Standards: skill-writing-rules, checking-rules · Lint: clean (check-brand-council SKILL.md, council-rules SKILL.md — both `skill-postwrite-invocation-lint · clean`)
Verdict: PASS — no blocking findings; 2 major, 2 minor. Depth: FLOOR. Reviewer: fresh-context skill-checker, 2026-08-22.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| A1 stale live claim missed | FAIL | major | brand-design/README.md:31 — the live "What's inside" component-map row still reads "`creative-convener` convenes the new `creative` sub-council, currently seeded empty (bench-seating ownership stays open)" | Update the row tail: "…now seats `george-l`/`nick-l` (#849, 2026-08-22); lead stays VACANT." Same-change repair per CLAUDE.md's stale-context rule |
| A2 revert correctness — parse ambiguity | PARTIAL | major | skills/check-brand-council/SKILL.md:45 (fixed enumeration `strategy · design · voice · full · advisory`) vs :58–59 ("a token matching neither a sub-council name nor a `## Groups` entry **in roster.md** → report the valid sub-councils and groups **actually present in the file** and stop") and :81–83 ("roster … is data … read it before resolving any sub-council or group token"); references/roster.md now declares `creative` rows | Reverting is CORRECT per #840's standing scoping (README.md:26 and evals.json:3 both record it; the external-seat reasoning holds — seating members doesn't change the seat surface). But #840's mechanical backstop was the empty bench; post-#849 the roster DATA declares `creative`, so a direct `/check-brand-council creative` token now matches "actually present in the file" and the model may fan out instead of erroring. Add one disambiguation line to the parse step (or the roster.md `creative` section): `creative` resolves only via `creative-convener`; a direct token takes the report-and-stop branch — or Kim rules to add it to the enumeration (that's a boundary edit owing its suite update) |
| A3 evals note not appended | FAIL | minor | skills/check-brand-council/evals/evals.json:3 — note chain ends at #840; no #849 entry recording that the enumeration was re-examined and deliberately kept post-seating | Append a dated #849 sentence to the note (no trigger cases change) |
| A4 roster schema / bijection | PASS | — | roster.md table: 14 data rows ↔ 14 files under references/critics/ (counted); only the `sub-councils` column + row order moved; `full` = union unchanged, so full-council runs still include both critics | none |
| A5 roster_check re-verified | PASS | — | `python3 scripts/roster_check.py skills/check-brand-council` → exit 0: `WARN: group 'leads' has a VACANT slot` + `INFO: 'advisory' … no seated critics` only — matches the maker's claim AND roster.md:50–51's own in-prose claims; `selftest` exit 0 | none |
| A6 ticket fidelity | PASS | — | Diff: only george-l (voice→creative) and nick-l (strategy→creative) moved; john-h row stays `strategy`, tim-d stays `voice`, rory-s stays `strategy`; non-seats recorded in prose (roster.md:46–49; role-pack-scaffolding.md:53–54) | none |
| A7 counts consistency | PASS | — | role-pack-scaffolding.md:48–49 claims 5/4/3/2; verified against roster.md table: strategy {luke-s, john-h, mark-p, brian-c, rory-s}=5, design=4, voice {david-a, tim-d, mary-n}=3, creative=2, total 14 | none |
| A8 version + ledger | PASS | — | plugin.json 0.11.1→0.11.2; README.md:84–89 ledger line dated 2026-08-22, cites #849, names both moves, the non-seats, and the still-VACANT lead. Patch bump consistent with v0.11.1 precedent (agent-body-only semantic edit, no description change) | none |
| A9 agent body accuracy | PASS | — | agents/creative-convener.md:22–26 — new claim verified against roster; the 2-of-3 caveat is correct (2 < 3); description:12's "An empty/VACANT bench reports 'no seats'" is a standing conditional branch, not a stale state claim | none |

## Dismissals (checks cited, per checking-rules)

- README.md:164, :180, :206 grep hits ("genuinely empty bench today", "only remaining VACANT seat (its bench itself stays open)", "strategy (6 … voice (4)") — DISMISSED: all three sit below the v0.11.2 entry inside the v0.9.0/v0.8.x ledger entries (v0.8.1 boundary read at README.md:184); ledger entries are dated historical records, append-only by house convention — rewriting them would be the defect.
- skills/make-critic/SKILL.md:54 ("advertising-creative") — DISMISSED: a role-family name in the minting interview, not a seating-state claim; read in context.
- Grep sweep (`creative` ±60 chars of empt/vacan/unseated/"no seats"/zero, all .md/.json under brand-design/) found no other live stale claim beyond A1.

## Steelman record

A2's dismissal steelman ("line 45's fixed list is authoritative; line 58's 'actually present in the file' only shapes the error message") was drafted and does NOT survive: SKILL.md:81–83 instructs reading roster.md before resolving ANY sub-council token, and roster-as-data (#838) made the file, not the prose list, the membership source of record — the ambiguity is real. Finding retained at major (latent, model-resolved, ruling owner is Kim), not blocking (no proven broken run).

## Verdict

PASS. The reseat itself is faithful, mechanically clean, and internally consistent. Two majors owed before the loop closes: repair README.md:31 (stale live claim) and disambiguate the post-seating `creative` token path (A2) — plus the minor evals-note append (A3).
