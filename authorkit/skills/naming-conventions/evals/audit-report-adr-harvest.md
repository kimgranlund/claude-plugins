# Audit — ADR-0024/0025 harvest into naming-conventions references

Skill: authorkit/skills/naming-conventions · Scope: references/LAYOUT.md + references/FRONTMATTER.md (dispatch-scoped doc-accuracy review) · Standards: check-skill + checking-rules · Lint (SKILL.md): 0 fail / 1 warn (pre-existing W2, out of scope)
Verdict: **PASS** — no blocking findings. Both edits are faithful, in-place extensions; three non-blocking accuracy findings below.

## Findings

| ID | Verdict | Severity | Evidence | Fix |
|----|---------|----------|----------|-----|
| F1 | FAIL | major | FRONTMATTER.md:3-5 — "Every field in the schema is validated… Fields nothing validates are prohibited, not optional." Contradicts ADR-0025 D1's "Common, not schema-enforced" tier (adr-0025:68-72): `model`/`tools`/`effort`/`skills`/`color`/`disallowedTools` are valid on agents yet nothing validates them estate-wide. A reader stopping at line 5 concludes those fields are prohibited on agents. | Scope the preamble: "…(commands and skills; agents follow the narrowed ADR-0025 convention below)." |
| F2 | FAIL | minor | FRONTMATTER.md:75-78 — "Measured 2026-08-21 … (40 files): … `autonomous_write`/`context` are carried by zero agents." Runtime check: `authorkit/agents/estate-audit-agent.md:10-11` carries both. ADR-0025:35 says 39/40, dogfood copy excluded. | Say "39/40; the one exception is authorkit's own dogfood copy" (which the paragraph's last sentence already names). |
| F3 | FAIL | minor | FRONTMATTER.md:82 — "These three fields remain valid ONLY as authorkit's…": nearest preceding list is the six common fields (line 80-84), not `performs`/`autonomous_write`/`context` from 60 words earlier. Misread hazard: implies `model`/`tools` etc. are authorkit-only. | Name them: "`performs`/`autonomous_write`/`context` remain valid ONLY as…". |
| F4 | FAIL | nit | FRONTMATTER.md:7 — Identity header still reads "(required, all kinds)" while its own D1 caveat (lines 16-19) exempts agents from `kind`; Provenance's header (line 86) got the parenthetical treatment, Identity's didn't. | Mirror line 86's header amendment. |
| F5 | FAIL | nit | FRONTMATTER.md:16, 98 cite "ADR-0025 D1"/"D3" without date; full "ADR-0025, 2026-08-21" appears only at line 72. | Add the date once per section, or rely on line 72 and cite "D1/D3 above". |

## Dispatch questions

1. **ADR fidelity** — PASS. LAYOUT.md:15-22 states six entries, cites ADR-0024 + date, reproduces D2's active-write/passive-test rationale accurately; no over-claim (the four-entry mention at line 16 is inside the supersession citation, correct usage). FRONTMATTER.md's three caveats correctly say "estate-wide" / "NOT part of the estate-wide agent schema" and preserve the authorkit `schema_scope: "full"` dogfood carve-out (lines 82-84, 98-103) — no fields implied banned everywhere. F1-F3 are precision defects, not scope inversions.
2. **Extension in place** — PASS. `git diff --stat`: +36/-4 across both files; all section headings and flow preserved; LAYOUT's code block extended, FRONTMATTER gained caveat paragraphs.
3. **Stale text** — one residue: F1 (the old "all validated" absolute at the file head). Grep for `five|four-entry|all validated|all kinds` found nothing else asserting the old five-entry set; "Rules (all validated):" at line 63 is adequately corrected by the caveat at line 72 immediately below — dismissed on that read.
4. **Citations** — PASS with F5 nit. Placement is correct (each caveat adjacent to the block it narrows).
5. **Reference quality** — good: declarative register, no imperatives, SKILL.md index rows for both files present (SKILL.md:46-47) with read-when triggers; LAYOUT's `evals/` gloss "model-invocable skills only" checked against ADR-0024:36-39 — the mandate is indeed scoped to model-invocable descriptions via plugin-authoring.md; dismissed as accurate.

Steelman on F1: "the schema" could be read as "the validated subset only" — but line 4's "Fields nothing validates are prohibited" then actively prohibits the convention tier; the finding survives.

Top 3: 1) F1 scope the preamble absolute. 2) F2 fix the zero-vs-39/40 count. 3) F3 name the three fields explicitly.
