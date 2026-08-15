---
name: attention-audit
kind: skill
description: >
  Audit an estate's attention economy — the always-on menu rent skill and
  agent descriptions charge every turn, ranked description-collision
  detection across plugin boundaries, real-usage cross-reference, and a
  per-release trend series. Use for "which skills tax Claude's performance
  the most", "optimize for smart attention and efficient routing", "audit
  our menu cost", "which skills never actually get used", "will these
  descriptions collide in routing", "retire-or-merge candidates". Reports
  only, never rewrites. NOT for the LLM-judged routing simulation (harness
  check-routing); NOT for prose economy inside bodies (bloat-audit); NOT
  for one skill's content quality (harness check-skill).
author: kim
created: 2026-08-15
last_updated: 2026-08-15
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3 */scripts/rent.py *)
  - Bash(python3 */scripts/collide.py *)
  - Bash(python3 */scripts/usage.py *)
  - Bash(python3 */scripts/trend.py *)
---

# attention-audit

Deterministic measurement lives in `scripts/` — every number in the report
comes from a script run; a count derived in prose is a defect. This skill's
job is the judgment layer on top of the scripts' output: deciding which
costs buy routing value and which are pure rent.

The four series stay separate — always-on chars, dead, stolen, leaked —
never collapsed into one accuracy-per-token quotient. A single quotient
rewards deleting the fences that protect rare-but-expensive misroutes.

## Procedure

1. Resolve the target: an estate root (a plugin root, a workspace of
   plugins, or a bare `.claude/skills` tree). Multiple estates → one pass
   each, one report section each.
2. Rent: `python3 <this skill>/scripts/rent.py --target <root> --json` —
   per-plugin and estate totals for skill AND agent descriptions, as
   separate figures. Skills carrying `disable-model-invocation: true` are
   zero-rent (excluded from the routable figure, counted separately);
   agent descriptions bill in full unconditionally — weight findings
   accordingly: an agent char is the more expensive char.
3. Collisions: `python3 <this skill>/scripts/collide.py --target <root>
   --json` — IDF-ranked shared-vocabulary evidence over every routable
   description, skills and agents, ALWAYS across plugin boundaries (the
   estate's proven blind spot: same-plugin siblings fence reciprocally,
   cross-plugin pairs go unfenced, and per-plugin eval runs are blind to
   the boundary). The report is per-artifact nearest-neighbors (top-k
   matches per entry, recall by construction — a global top-N window lets
   boilerplate pairs crowd a real twin out, measured 2026-08-15). At estate
   scale render `--top 40` for classification and keep the full JSON as the
   report's attached artifact. At write time, pre-lint one edited artifact
   with `--against <name>`. Classify each rendered pair — the judgment the
   script deliberately does not make:
   - **routing twin** — unfenced, same ask territory → recommend the fence,
     its owner, and the reciprocal eval case;
   - **boilerplate tax** — shared template sentences across a role family
     (ops-seat wording, checker templates) → recommend moving the shared
     sentence into bodies; it pays rent in every resident description;
   - **coincidence** — dismiss with one clause.
   Two twin classes are the LLM tier's catch, not this script's — the
   report names them as check-routing's territory rather than over-claiming:
   common-words twins (shared evidence is only estate-generic vocabulary —
   canonical example: check-skill↔bloat-audit, "audit/review a skill") and
   crowded-territory twins (shared vocabulary claimed by 10+ descriptions,
   so no pair owns it — canonical example: naming-rules↔naming-conventions,
   where "naming" spans 23 descriptions and the split is canon knowledge).
4. Usage: `python3 <this skill>/scripts/usage.py --target <root>` — joins
   `~/.claude.json` skillUsage against the estate roster. Two false-positive
   classes are handled by construction — the script corrects both before
   anything is reported: rename lineage
   (zero hits under the current name, real hits under a pre-campaign name —
   pass `--lineage` when the estate has a rename history) and preload-only
   consumption (a skill in an agent's `skills:` list is used whenever that
   agent is dispatched, invisibly to skillUsage).
5. Judge. A retire/merge candidate needs at least 2 of the 3 signals —
   usage, eval verdict, description cost — cited with values. Zero usage
   alone is NOT a finding: knowledge packs are insurance and bill only
   their description until their topic arrives; the question for a
   zero-usage pack is whether its RENT is proportionate, not whether it
   fired. A collision pair is a finding only when both descriptions are
   routable and no NOT-fence names the other side.
6. Trend: `python3 <this skill>/scripts/trend.py --rent <rent.json>
   [--routing-report <path>] --out <root>/attention-trend.csv` — appends
   one dated row per plugin. Missing routing report → the dead/stolen/
   leaked columns record the literal `absent`.
7. Render per references/REPORT-TEMPLATE.md: verdict-first, the separate
   series, findings with evidence (file, chars, shared terms, usage
   values). Hand every fix to the owner — the owning plugin edits its
   descriptions, harness check-routing proves the boundary after; this
   report changes nothing itself.

Done when: the report exists with all five sections rendered from this
run's script outputs, every candidate carries its ≥2 signals, the trend
row is appended (or its columns read `absent` with the reason named), and
every finding names an owner.

## Degraded modes

- No eval/routing artifacts in the estate (external repos): steps 2–4 run
  in full; step 6 records the missing columns as `absent`; the report
  names the missing signal and the audit completes regardless.
- No `~/.claude.json` or empty skillUsage: step 4 reports "no telemetry on
  this host" and candidates fall back to cost + eval signals only.

## Composition

Inside authorkit, overhaul-execute runs this skill in its Phase 1 MEASURE
(alongside naming-audit and bloat-audit; the attention-audit-agent twin
takes the batch path at the same scale threshold) and re-runs trend.py in
its Phase 6 burn-down — the trend row is the baseline→now evidence.

## References

| File | Read when |
|---|---|
| REPORT-TEMPLATE.md | rendering the attention report |
