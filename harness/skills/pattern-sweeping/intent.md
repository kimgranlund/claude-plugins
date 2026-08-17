# intent — pattern-sweeping

Record: https://github.com/kimgranlund/claude-plugins/issues/576

## Slots (Phase 1)

- **Trigger (verbatim phrasings):** "sweep the repo for X"; "find every page that still does Y"; "audit all drawers for Z"; "sweep a corpus of pages for a DOM pattern"; "codemod this pattern away"; "how many places still use …"; "migrate every remaining call site".
- **Behavior delta:** without the skill, a sweep reports success from its own regex — four documented production failures (adiav2 admin campaigns, Jul 2026): (1) markup greps miss values assembled in TS strings; (2) numeric-class regex deleted load-bearing `min-width: 0` idioms and a load-bearing search width (live regression on ten pages); (3) proxy assertions (element presence) passed while the real property broke; (4) an undercounting census (54 of 98 registry entries) produced a confidently wrong filed finding. The skill forces census sanity-check, classification before touching, rendered-property verification, and a ratchet.
- **Species + dials:** procedural; `disable-model-invocation: false`, `user-invocable: true`.
- **Freedom:** medium — prose pipeline (classification is judgment) + a bundled low-freedom census script (`scripts/pattern_census.py`) with known-member sanity check and selftest negative controls.
- **Type:** encoded preference backed by paid-for incident evidence; detail spent only where the incidents were.
- **Fences:** NOT the ops-queue sweep (harness:sweep-chores); NOT naming/bloat conformance audits over instruction markdown (authorkit:naming-audit / authorkit:bloat-audit); NOT routing evals (harness:check-routing).
- **Done-when:** a sweep run ends with the typed report (census + sanity proof, classification table, per-bucket disposition, verification evidence naming a rendered/computed property, ratchet named) — or, in audit-only disposition, the report plus minted follow-up records.

Confirmation: design summarized to Kim in-session 2026-08-17; approved verbatim ("ok great, use /make-skill to create this…"). Naming: `pattern-sweeping` — new ProcessLex token `sweeping` registered in `naming.manifest.json` (exemptions array must not grow; `sweep-chores` stays the only sweep-named exemption).

## Gates

- P0 route: PASS 2026-08-17 — primitive = skill (judgment-carrying on-demand procedure; census slice mechanized as a bundled script, not a hook — the sweep as a whole is not pass/fail checkable).
- P1 interview: PASS 2026-08-17 — slots above; confirmed in-session.
- P2 evals: PASS 2026-08-17 — evals/evals.json (20 cases), 3 behavioral assertions (below), baselines captured in evals/baseline/.
- P3 draft: PASS 2026-08-17 — SKILL.md 118 lines, dials explicit, description 892 chars.
- P4 language: PASS 2026-08-17 — potency pass applied on draft (describers rewritten to standing spec-present contracts; 2 hard gates; numeric anchors on census/verify steps).
- P5 validate: PASS 2026-08-17 — (1) skill_lint clean after one F3 fix (angle brackets out of frontmatter). (2) skill-checker audit verdict PASS, 3 findings: F1 manifest token missing → fixed (ProcessLex `sweeping` added to root + authorkit bundled manifests); F2 reciprocal fences absent → fixed (no-trigger cases added to sweep-chores t08, check-routing t13, authorkit naming-audit t08, bloat-audit t09); F3 intent pre-recorded results → this entry rewritten from the actual report. (3) Behavior check (plan-mode `claude -p` probes, skill copied into a scratch project): flagship phrasing produced method-conformant output — assertions 2 and 3 fully demonstrated (load-bearing `min-width: 0` classified and relocated not deleted; verification named rendered truncation + the ui:contract ratchet), both absent in the saved baselines; assertion 1 partially demonstrated (census + tier present, the known-member proof was not verbalized). (4) Fences reciprocated as in F2. Watch-item below.

## Behavioral assertions (Phase 2)

1. The output contains a census block that names the pattern tier(s) used and shows the known-member sanity check result before any classification.
2. Every hit is assigned one of exactly three buckets — decorative / load-bearing / idiom — and only decorative-bucket hits are eligible for mechanical transform.
3. The verification section names a rendered or computed property (never element presence/absence) and names the ratchet (baseline/gate tightened), or states explicitly why none exists.

## Accepted-with-note (Phase 5 audit)

- Watch-item (routing): the drawer-title phrasing ("find every page in our admin app that still renders a hand-rolled drawer title… and fix them") did not visibly invoke the skill in a headless plan-mode probe, while the flagship min-width phrasing produced method-conformant behavior. Suite case t02 covers the phrasing; judge on the next /check-routing run before spending description characters on it.
- Behavior-check assertion 1 (explicit known-member proof verbalized in the report) demonstrated only partially in probes; the body's step-1 contract carries it — re-check on first real-repo use.
