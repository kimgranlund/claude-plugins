# Baseline — usage question (WITHOUT attention-audit)

Conditions: fresh-context general-purpose agent, 2026-08-15, prompt = eval t04's territory:
"Which skills never actually get used? Cross-check against real usage." No method hints given.

## What the baseline did

Mined all 82 locally-retained session histories (back to ~May 2026) for Skill-tool calls,
slash invocations, and agent-dispatch counts. One-off, expensive, unreproducible sweep — but
methodologically excellent, and it surfaced TWO false-positive classes any naive telemetry
read WILL hit. These are now requirements on the telemetry script, not caveats:

1. **Rename lineage** — the estate ran 2+ rename campaigns (ADR-0006/0008/0011). A skill with
   zero hits under its current name may have real hits under its old plugin:name (e.g.
   harness:save-lessons = 58 combined as forge:knowledge-harvest + current; make-skill = 10 as
   forge:skill-forge). The script MUST consume a lineage map (old name → current) or it
   manufactures false retire candidates. fix-old-names / the rename-execute plan archive are
   the natural lineage sources.
2. **Preload-only consumption** — skills baked into an agent's system prompt never appear as
   Skill calls. Cross-check the owning agent's dispatch count (e.g. dispatch-ticket via
   build-lead 240x; check-skill/checking-rules via skill-checker 132x; ops-write-sandbox-rules
   via chore-lead 131x). The script MUST join skills→preloading-agents→dispatch counts.

## Verbatim findings (evidence for Phase C and the retire/merge pipeline)

- 73/140 skills (52%) zero evidence anywhere. By plugin: llm 9/9 (100%, no indirect path
  exists), agent-protocols 7/8, design 19/22, screens 12/14, docs 7/15, teamwork 4/13,
  harness 13/47, authorkit 1/8 (naming-conventions), project-docs 0 uses.
- Structural dead zone: teamwork's lead-build/lead-planning/lead-review self-adopt skills =
  ZERO everywhere while their agent twins are the estate's most-used artifacts (build-lead
  240, code-checker 197, planner 95). Outlier: lead-team 15 self-adopts vs 1 twin dispatch.
  Either dead weight or an unknown path — deliberate look needed.
- make-plugin and make-script: mandated by root CLAUDE.md ("never hand-scaffold") yet zero
  logged usage.
- Usage concentrates in a core ~15–20 skills; the long tail is mostly single-topic facts
  packs and niche one-shot makers.

## Delta the skill must demonstrate over this

Repeatable at near-zero cost (script over transcripts/skillUsage, not an 82-session LLM sweep),
lineage-aware and preload-aware BY CONSTRUCTION (the two false-positive classes above are
selftest fixtures), candidates cite ≥2 of 3 signals, and results append to the trend series
instead of evaporating with the session.
