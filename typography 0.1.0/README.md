# typography — choose, pair, and tokenize type

Sibling plugin to forge (which authors the harness) and color (which runs the analogous
decide-then-realize split for color): typography designs and realizes the type layer — an
11-voice system decided from a brand brief, tokenized as bound `--type-*`/`--font-*` custom
properties, and grounded in a cited lettering/type-anatomy corpus. Built from a
`plugin-decompose` partition of the legacy personal skill library.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/typography-system-design` | Procedural skill | both (`/typography-system-design`) | 11-voice per-voice font-and-rationale decision from a brand brief: territory interpretation -> per-voice rationale -> coherence pass -> craft check; `references/rubric.md` (S1-S6); `scripts/typeface-check.py` — metric-ratio and axis-apart pairing gates; routes to `typography-tokens` for realization |
| `skills/typography-lettering` | Declarative skill | model-only | Cited type/lettering corpus — anatomy (x-height, cap-height), Vox-ATypI classification, metric-compatible fallback stacks, font personality (neutral vs. distinctive), world scripts, OpenType features, variable-font axes, CSS text surface, measure, text accessibility; 63 files under `references/` (62 references across ten axes + `references/INDEX.md`) |
| `skills/typography-tokens` | Declarative skill | model-only | Eleven-voice `--type-*`/`--font-*` token grammar (voice x step, size derived); baked leading/paragraph rhythm; concrete font pick per family slot, distinctive vs. neutral by voice |
| `agents/typography-system-reviewer.md` | Subagent (adversarial critic) | dispatched (Task tool, model `fable`) | Grades ONE typography system decision against `typography-system-design`'s six-dimension rubric (S1-S6) and its `typeface-check.py` gate; preloads `typography-system-design` only |

Cross-plugin seam (soft, by design): the reviewer agent returns through forge's
`handoff-compose` block where forge is installed, and falls back inline
(Status/Summary/Files changed/Tests/checks run/Evidence/Risks/Open questions/Recommended next action)
when it is not — no hard preload crosses the plugin boundary.

v0.2.3 · assembled 2026-07-10 · 0.2.3: typography-tokens gains law 7 — the text-rendering baseline is ALWAYS on (the macOS smoothing pair · `optimizeLegibility` · `font-optical-sizing: auto` · `font-synthesis: none` · kerning + common ligatures · `code, pre, kbd` never ligate), included once in the project's global CSS as part of the token layer's contract; the font-synthesis doctrine travels with it (an unresolvable weight renders at the nearest REAL weight — fix the font, never fake it) (standing user rule 2026-07-10) · assembled 2026-07-10 · 0.2.2: author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder) · assembled 2026-07-09 · 0.2.1: hygiene pass — typography-system-design under the 1024 bar; lettering t01 and tokens t05/t08/t12 reassigned per unanimous multi-run blind verdicts (pairing-design and scale-design asks belong to typography-system-design); the judge-coin-flip duplicate case deleted · assembled 2026-07-09 · 0.2.0: BREAKING (ADR-0001) — typography-system-author→typography-system-design, matching sibling palette-design's verb pattern; typography-system-reviewer's preload updated in the same change · assembled 2026-07-09 · 0.1.2: eval-run tuning of the estate's worst routing boundary — typography-lettering dropped its generative 'choosing/pairing' claims and fences the pairing-design job to typography-system-design (which now front-loads 'pick or design a font pairing' verbatim); post-tuning blind re-run confirms all four steals resolved; the tokens↔system-author 'voice' vocabulary logged as a known context-dependent watch pair · assembled 2026-07-09 · 0.1.1: typography-system-reviewer fallback 'Tests run'→'Tests/checks run' (harness-audit finding, estate-wide sweep) · assembled 2026-07-07 · initial: ported from ~/.claude/skills + ~/.claude/agents/design/typography-system-reviewer as part of a plugin-decompose partition
