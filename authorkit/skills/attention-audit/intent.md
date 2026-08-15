# intent — attention-audit
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: low (mechanics — bundled scripts), medium (judgment layer over script output)
type: capability-uplift

## trigger
should:      ["which of these tax Claude's performance the most", "optimize for smart attention and efficient routing", "audit our menu cost", "which skills never actually get used", "how much context do our skill descriptions burn"]
should_not:  ["why does my skill never trigger", "rerun the routing evals", "audit this skill for bloat"]

## delta
Demonstrated live 2026-08-15 (the session that seeded this skill): without it, always-on
menu-rent measurement was an ad-hoc throwaway python one-liner (unrepeatable, no trend);
`~/.claude.json` skillUsage (327 entries, usageCount/lastUsedAt) was read by nothing in the
estate; description collisions surfaced only after expensive LLM-judged eval waves
(the "menu-scope collision" class, llm README ledger v1.0.6). Desired: one command —
repeatable per-plugin rent measurement, deterministic collision pre-detection at the cheap
tier, telemetry×eval×cost cross-reference producing cited retire/merge candidates, and a
dated trend series across release boundaries. Covers issues #259, #261, #264.

## fences
- NOT for the blind LLM-judged routing simulation (harness /check-routing — this skill is the deterministic cheap tier upstream of it)
- NOT for prose economy inside skill bodies (bloat-audit — this skill owns the always-on menu surface)
- NOT for judging one skill's content (harness check-skill / skill-checker)
- NOT for naming-grammar conformance (naming-audit)
- Reports only — never rewrites a description (the owning plugin edits; /check-routing proves)

## assertions
1. The report states per-plugin always-on totals (chars + est. tokens) covering BOTH skill and agent descriptions, plus an estate total.
2. Collision output is deterministic (same input → same output) and lists each flagged pair with its shared distinctive terms; a synthetic non-overlapping fixture yields zero flags (negative control).
3. Every retire/merge candidate cites at least 2 of the 3 signals (usage telemetry, eval verdict, description cost) with values.
4. The trend series appends one dated row per plugin per run with SEPARATE columns (always-on chars | dead | stolen | leaked) and no combined quotient anywhere in the output.
5. Every bundled script passes its own `selftest` mode (exit-code 0/1/2 contract per script-writing-rules).

## gates
P0 route:      PASS 2026-08-15 — primitive = skill: audit procedure + judgment over bundled deterministic scripts (sibling pattern: naming-audit/validate.py, bloat-audit/measure.py); hook/entry-file/agent rungs all declined (agent twin is a later thin shell over this skill).
P1 intent:     PASS 2026-08-15 — all seven slots filled from live session evidence; name (attention-audit) and record confirmed by Kim via AskUserQuestion.
P2 evals:      PASS 2026-08-15 — evals.json (10 trigger + 10 fence cases, t01–t02 verbatim user phrasings); 5 assertions in this record; 3 fresh-context baselines captured (rent.md, usage.md, collide.md) with per-baseline "delta the skill must demonstrate" sections. Baselines upgraded the spec: rent → dial-aware + skill/agent split; usage → lineage-aware + preload-aware (both as selftest fixtures); collide → cross-plugin by default, the 3 found real gaps become the proving fixture.
P3 draft:      PASS 2026-08-15 — SKILL.md (description ≤1024, both dials explicit, body ~120 lines), REPORT-TEMPLATE.md, four scripts (rent/collide/usage/trend) all selftest-PASS; live estate runs verified (rent reproduces the baseline's numbers independently). [Amended post-P5-audit, same day: the original "collide 3/3 recall" claim held only for the unbounded pair list, not the rendered report — skill-checker finding F1. Fixed via per-artifact neighbors reporting; the honest recall fixture is now 1 distinctive-vocab pair in-report + 2 measured LLM-tier exemplars, see rulings.]
P4 language:   PASS 2026-08-15 — potency lint within budget (3 nevers: one quoted trigger datum + the two real gates: never-rewrites, never-one-quotient); describers rewritten affirmative; skill_lint clean after the W8 description diet (973 → ~680 chars — flagged by the estate's own #79 budget, fitting). Instantiation test applied per line.
P5 validate:   PASS 2026-08-15 — skill-checker re-verdict PASS (all 3 findings independently re-verified, incl. a negative control: the recall harness exits 1 on an authorkit-only corpus where the fixture pair is absent). Original FAIL preserved in evals/audit-report.md. Detail: (1) skill_lint clean; (2) skill-checker FLOOR verdict FAIL → all 3 findings fixed same day (see rulings), re-verdict requested; (3) behavior check PASS: a fresh agent ran the full procedure against the live estate — all 5 assertions demonstrated (per-plugin skill/agent split + estate total; every collide pair classified into the four classes; both retire/merge candidates cite usage+cost with the missing eval signal named per degraded mode; trend rows appended with separate columns and literal `absent`; selftests green). Evidence: the agent's rendered report (relayed 2026-08-15) + evals/behavior-trend.csv on disk (dry-run destination). (4) fence closure: bloat-audit n05/n06, check-skill n07, check-routing n07 — all reciprocated.

## rulings
- P5 skill-checker triage (2026-08-15, verdict FAIL → all three findings fixed same day):
  F1 (blocking) global top-40 window buried the proving pairs (ranks 171/1000/1682 measured) →
  report is now per-artifact nearest-neighbors (collide.neighbors, k=5), recall by construction;
  fixture recalibrated honestly: break-down pair proves the cheap tier in-report (rank 166 of
  491, exit-0), while check-skill↔bloat-audit (all shared terms estate-common: skill df=52) and
  naming-rules↔naming-conventions (crowded commons: naming df=23, grammar df=12 across the
  rename family — twinhood is ADR-canon knowledge) are the two documented LLM-tier classes,
  measured via evals/debug_pair.py. F2 (major) check_known_pairs.py always exited 0 → now
  exits 1 on any fixture pair missing from the RENDERED report (bit immediately when k=2 was
  too tight — proof it discriminates). F3 (minor) usage.py takes --target (--estate alias
  kept); body gains a Done-when stopping predicate.
- Collision scorer *(superseded same day by the P5-triage ruling above — the "recall 3/3" and
  "--top 40" claims below describe the pre-neighbors design; kept as tuning history)*: (settled
  2026-08-15 after a measured tuning loop — count-threshold →
  fixed-DF cutoff → IDF cosine → salient-core → TOP-5 IDF sum): score = IDF sum of the pair's
  5 strongest shared items (unordered bigrams ×2), ranked output, name-family pairs bucketed
  last. Recall 3/3 on the baseline's known-real pairs; global ranking is imperfect BY DESIGN —
  the report is a bounded ranked evidence list (--top 40) the judgment layer classifies into
  routing-twin / boilerplate-tax / coincidence. Known limitation, documented in the body:
  semantic twins built purely from estate-common words rank low; that class belongs to
  check-routing (the LLM tier). Tuning harness preserved at evals/check_known_pairs.py.
- Name: attention-audit chosen over routing-audit (avoids permanent confusion with /check-routing) and menu-audit (narrower than charter). Kim, 2026-08-15.
- Separate-series rule is load-bearing: no accuracy-per-token quotient, ever (Goodhart risk ruled 2026-08-15 — a single quotient rewards deleting fences that protect rare-but-expensive misroutes).
- Portability constraint: no hard dependency on this workspace's layout; target estates include sibling plugins and external repos (adia). skillUsage key→plugin-qualified-name mapping is part of the telemetry script's work (caveat recorded in #259).
- Campaign scope addition (Kim, 2026-08-15): the driving use case is "open any project, run /overhaul-execute, ALL of authorkit unleashes." Therefore this campaign ALSO wires attention-audit into overhaul-execute — Phase 1 MEASURE (alongside naming-audit + bloat-audit, with an agent-twin batch path at the same >3-estates/>40-members threshold) and Phase 6 PROVE (the trend series row IS the burn-down's baseline→now evidence). Shipping the skill without this wiring would leave the driver's member list stale in the same release (stale-record invariant) — same-change repair, same PR.
- Degraded mode required: the eval-verdict input (dead/stolen/leaked) comes from harness check-routing artifacts, which external estates may lack — attention-audit runs on telemetry + cost signals alone and reports the missing signal, never blocks (matching overhaul-execute's existing harness-absent degraded modes).
