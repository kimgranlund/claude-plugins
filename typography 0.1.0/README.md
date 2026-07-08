# typography — choose, pair, and tokenize type

Sibling plugin to forge (which authors the harness) and color (which runs the analogous
decide-then-realize split for color): typography designs and realizes the type layer — an
11-voice system decided from a brand brief, tokenized as bound `--type-*`/`--font-*` custom
properties, and grounded in a cited lettering/type-anatomy corpus. Built from a
`plugin-decompose` partition of the legacy personal skill library.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/typography-system-author` | Procedural skill | both (`/typography-system-author`) | 11-voice per-voice font-and-rationale decision from a brand brief: territory interpretation -> per-voice rationale -> coherence pass -> craft check; `references/rubric.md` (S1-S6); `scripts/typeface-check.py` — metric-ratio and axis-apart pairing gates; routes to `typography-tokens` for realization |
| `skills/typography-lettering` | Declarative skill | model-only | Cited type/lettering corpus — anatomy (x-height, cap-height), Vox-ATypI classification, metric-compatible fallback stacks, font personality (neutral vs. distinctive), world scripts, OpenType features, variable-font axes, CSS text surface, measure, text accessibility; 63 files under `references/` (62 references across ten axes + `references/INDEX.md`) |
| `skills/typography-tokens` | Declarative skill | model-only | Eleven-voice `--type-*`/`--font-*` token grammar (voice x step, size derived); baked leading/paragraph rhythm; concrete font pick per family slot, distinctive vs. neutral by voice |
| `agents/typography-system-reviewer.md` | Subagent (adversarial critic) | dispatched (Task tool, model `fable`) | Grades ONE typography system decision against `typography-system-author`'s six-dimension rubric (S1-S6) and its `typeface-check.py` gate; preloads `typography-system-author` only |

Cross-plugin seam (soft, by design): the reviewer agent returns through forge's
`handoff-compose` block where forge is installed, and falls back inline
(Status/Summary/Files changed/Tests run/Evidence/Risks/Open questions/Recommended next action)
when it is not — no hard preload crosses the plugin boundary.

v0.1.0 · assembled 2026-07-07 · initial: ported from ~/.claude/skills + ~/.claude/agents/design/typography-system-reviewer as part of a plugin-decompose partition
