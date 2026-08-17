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
last_updated: 2026-08-16
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
   - **routing twin** — unfenced, same ask territory → recommend a fix from
     the structural-fix category set below (owner named), defaulting to the
     reciprocal fence unless a reduction criterion fires;
   - **boilerplate tax** — shared template sentences across a role family
     (ops-seat wording, checker templates) → recommend **centralize-boilerplate**
     (move the shared sentence into bodies or a shared reference); it pays
     rent in every resident description;
   - **coincidence** — dismiss with one clause.

   **Structural-fix category set (issue #297)** — a collision or rent
   finding names ONE fix: **reciprocal fence** (default — a NOT-clause on
   each side) · **demote-to-wiring** (narrow, or set
   `disable-model-invocation: true` on, a side reachable only by dispatch —
   agent-preloaded or Skill-tool-only, with no human-typed trigger) ·
   **merge** (the pair does near-duplicate work; fold one into the other) ·
   **centralize-boilerplate** (the shared text is template, not twin
   intent) · **retire** (one side already clears step 5's ≥2-signal retire
   floor). Reduction beats a fence when ANY of these hold — name which one,
   and pick the category from the pair's own evidence (a dispatch-only side
   → demote-to-wiring; near-duplicate work → merge; template text →
   centralize-boilerplate; otherwise → retire the weaker signal-holder):
   - **the fence would blow W8** — `collide.py`'s JSON carries each side's
     `headroom_a`/`headroom_b` (700 minus that side's current char count);
     `fence_tight: true` (either headroom under 23 — this estate's own
     shortest measured real NOT-clause, n=232, 2026-08-16) means no
     realistic fence fits without a diet first (precedent:
     naming-conventions v0.10.1 dieted its description just to afford its
     own fence — the treadmill this tier exists to stop).
   - **the pair was already fenced once** and rent is still climbing —
     evidenced by a prior report's Collisions block or `git log` on either
     description naming the fence (collide.py's own `fenced` check
     suppresses a currently-fenced pair from this run's collision output,
     so this criterion reaches the judge only via a rent/trend finding). A
     second fence on the same pair IS the treadmill, not a fix for it.
   - **one side is dispatch-only** — demote-to-wiring beats fencing a
     description no human ever routes to by typing.
   - **one side already clears step 5's retire/merge floor** — retire or
     merge it rather than fence an artifact that's already leaving.
   None fire → reciprocal fence, named with its owner, as today. A rent
   finding with no collision partner draws from the same set minus
   reciprocal fence (usually demote-to-wiring, centralize-boilerplate, or
   retire) and renders in the Retire/merge candidates section's "proposed
   action" slot — the Collisions block is pair-shaped and a partnerless
   finding has no pair to occupy it.
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
   routable and no NOT-fence names the other side; every such finding
   carries a structural-fix category per step 3.
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
run's script outputs, every candidate carries its ≥2 signals, every
collision/rent finding names a structural-fix category and an owner, and
the trend row is appended (or its columns read `absent` with the reason
named).

## Degraded modes

- No eval/routing artifacts in the estate (external repos): steps 2–4 run
  in full; step 6 records the missing columns as `absent`; the report
  names the missing signal and the audit completes regardless.
- No `~/.claude.json` or empty skillUsage: step 4 reports "no telemetry on
  this host" and candidates fall back to cost + eval signals only.

## Enforcement wiring (issue #294) — retired 2026-08-17 (#466)

Two of these steps used to also run unattended, as `authorkit/hooks/hooks.json` PostToolUse
siblings to the naming-grammar gate — neither replaced the manual procedure above,
both narrowed their own scope so the common write stayed cheap. Enforcement retired
2026-08-17 (#466, remove-all-hooks directive); the wrapper scripts are kept on disk retired,
not deleted, for history. Run the manual procedure above for both:

- **Step 3's write-time pre-lint** (`collide.py --against`) formerly fired via
  `scripts/collide_hook.py.retired` whenever a written `SKILL.md`'s `description:` field
  actually changed (a body-only edit no-op'd, measured ~0.04s; a real description
  change ran the full estate sweep, measured ~0.12s against this workspace's ~140
  skills — both well inside the hook's former 20s budget). Judgment-shaped, never a hard
  block: a flagged pair printed as an advisory finding to classify (routing twin /
  boilerplate tax / coincidence), the same three buckets step 3 already names.
- **Step 6's trend capture** formerly fired via `scripts/trend_hook.py.retired` whenever a
  plugin's own `.claude-plugin/plugin.json` `version` field changed (this workspace's own
  ship signal — every version bump happens right before/around `release_gate.py
  --package`) and appended that ONE plugin's row to `<estate-root>/attention-trend.csv`
  automatically, columns `absent` for dead/stolen/leaked (no routing report at hook
  time) — exactly like an unattended manual run without `--routing-report`.

Both hooks are fail-open by construction (#287's shape guards): a malformed event,
an unreadable file, no derivable git root, or any internal exception exits 0
silently rather than ever blocking a write.

## Composition

Inside authorkit, overhaul-execute runs this skill in its Phase 1 MEASURE
(alongside naming-audit and bloat-audit; `estate-audit-agent` dispatched
with `instrument: attention` takes the batch path at the same scale
threshold — the merged agent's batch twin since issue #293) and re-runs
trend.py in its Phase 6 burn-down — the trend row is the baseline→now
evidence.

## References

| File | Read when |
|---|---|
| REPORT-TEMPLATE.md | rendering the attention report |
