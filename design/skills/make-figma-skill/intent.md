# intent — make-figma-skill
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium (one transposition table governs conversions; prose freedom inside sections)
type: capability-uplift (no-skill runs summarize and leave dead sidecar pointers — see evals/baseline.md)

Forged 2026-08-27 in the plugins-marshal session (plugins-62) from Kim's live ask: "How would
you create a secondary export of our Factory skills as optimized Figma Skills? They can be as
long as they need to be (prevent losing resolution). Create a plan + checklist + eval system
for the conversion, and save that as an authoring skill `design:make-figma-skill` (this
should be able to make a net-new skill or convert a reference skill)." Slots filled from the
ask and confirmed in one AskUserQuestion round (Confirm; export destination = always ask per run).

## trigger
should:      ["create a Figma skill from our button rules skill", "convert this skill into a Figma custom skill", "export our Factory skills as Figma skills", "make a custom skill for the Figma agent that enforces our token grammar", "write a Figma Make custom skill for our design system", "the Figma skill we exported lost the contrast thresholds, regenerate it from the source"]
should_not:  ["create Figma Make design system guidelines for our brand" (make-figma-make-kit), "setBoundVariableForPaint throws when I alias a variable" (figma-plugin-facts), "make a new skill for reviewing pull requests" (harness:make-skill), "install the figma-use skill so Claude Code can drive the Figma MCP" (not authoring)]

## delta
evals/baseline.md — without the skill: a summary with dead `references/` pointers, Claude-only
frontmatter keys, rounded thresholds, un-runnable script instructions, no provenance. With:
one file, F1–F7 green, F6 measured, receipt.

## rulings (Kim, 2026-08-27)
- Output length is unbounded; fidelity ("never lose resolution") is the deliverable.
- Destination path is asked per run, never defaulted.
- "Figma skill" = Figma's in-app custom skill (single .md, Agent Skills frontmatter, no
  sidecar dirs), NOT the `figma/mcp-server-guide` MCP skills family.

## fences
- NOT for a Figma Make guidelines/ FOLDER (make-figma-make-kit)
- NOT for the Figma Plugin API (figma-plugin-facts)
- NOT for authoring a Claude Code skill (harness:make-skill)
- NOT for installing/using the Figma MCP skills — figma-use etc. (a coding-agent job, not authoring)

## assertions
evals/assertions.md (6).

## gates
P0 route:      PASS 2026-08-27 — skill (on-demand authoring procedure with judgment; not hook/entry/agent).
P1 intent:     PASS 2026-08-27 — record confirmed by Kim (AskUserQuestion, this session).
P2 evals:      PASS 2026-08-27 — evals/evals.json 22 cases (12 trigger / 10 no-trigger), assertions.md (6), baseline.md (documented-delta).
P3 draft:      PASS 2026-08-27 — SKILL.md 139 lines; references/{figma-spec,conversion-rules,rubric,checklist}.md; scripts/figma_skill_check.py (F1–F8 + --hash, selftest 25/25); both dials explicit; description 698/700 (W8).
P4 language:   PASS 2026-08-27 — potency_lint: first pass 8 NEVERs (budget 3) + lint F3 (`<` in argument-hint) + W8 716; rewritten to exactly 3 hard gates (never summarize a source section / never default the destination / never hand-patch an export), argument-hint de-bracketed, description dieted. Re-run all within budget.
P5 validate:   PASS 2026-08-27 — skill_lint clean. UNNAMED synchronous skill-checker: GO, 0 blocking (1 major, 2 minor, 1 nit) — all fixed: F6 now rejects `## Dropped` bullets without a closed-set reason (bite + reverse-control fixtures), F5 WARNs on missing hash:/inventory:, SKILL.md cites the closed set instead of restating it, reciprocal negatives were already in make-figma-make-kit n14/n15 + figma-plugin-facts n08 (the nit predates its own read). Behavior check (fresh-context agent following SKILL.md, converting make-figma-make-kit): export 1004 lines/45 headings, checker exit 0 on round 3, F6 measured, R1–R5 = 4/4/4/4/5, in-Figma check UNMEASURED (no Figma seat) — scratchpad export kept out of the tree. The run's 10 friction findings fed back into the rules in this same change: F3 exemptions for `(transposed from …)` and the Dropped/Provenance sections; wrapped Dropped bullets joined; `node`/`python3` patterns narrowed to real invocations; in-reference path citations → `## <heading>` pointers + `rewrites:` count; head-once-plus-pointer rule for contract sections; first-citation order; n* FAMILIES not cases; hash method specified + `--hash` subcommand. Baseline: evals/baseline.md (documented-delta). Fence closure: n14/n15/n08 above.

## rulings (audit)
- Description-side reciprocal NOT-clause on make-figma-make-kit / figma-plugin-facts NOT added: both descriptions sit at the 700-char W8 ceiling and the auditor found no vocabulary collision in the corpus; the evals-side negatives carry the fence. Re-open if /check-routing shows a stolen case.
