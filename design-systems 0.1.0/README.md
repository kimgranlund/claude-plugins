# design-systems — design-system export authoring + the Material Design token grammar

Sibling plugin to forge (which authors the harness) and scribe (which authors documents);
design-systems authors, regenerates, and grades the export bundles a generative design agent
consumes — Claude Design/Claude Code, Figma Make, Google Stitch — and carries the Material Design
token grammar those exports can extend. Two decomposition candidates (design-system-export and
material-design-tokens) merge here on explicit direction: the token skills exist chiefly to be
cited from the exports, so one plugin boundary serves both.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/design-system-author` | Procedural skill | both (model + user) | The cross-platform hub: core+profiles architecture, prose-over-tokens and terminal-value doctrines, `references/rubric.md` (H1–H7) and `references/shared-doctrines.md`; dispatches the three platform siblings and design-system-reviewer |
| `skills/design-system-author-dscard` | Procedural skill | both | Claude Design / Claude Code bundle authoring — DESIGN.md spine + tokens.json + `@dsCard` previews; the Ultimate Tokens grammar, OKLCH frontmatter, `scripts/bundle_gates.py` (B1–B7) |
| `skills/design-system-author-figma-make` | Procedural skill | both | Figma Make `guidelines/` folder authoring — Guidelines.md entry + routed `foundations/`/`components/` leaves; `scripts/make_guidelines_check.py` (D1–D11), the only gate since Make validates nothing natively |
| `skills/design-system-author-google-stitch` | Procedural skill | both | Google Stitch single-file DESIGN.md authoring — YAML frontmatter tokens + 8 canonical sections; `scripts/prelint.py` (G1–G7, R1–R5) ahead of `npx @google/design.md lint` |
| `skills/material-design-color-tokens` | Declarative skill | model-only | Consumption guide for the `--md-sys-color-*` 59-role semantic layer extending Material 3 — pairing laws, state families, tonal variants, surface/scrim ladders |
| `skills/material-design-geometry-tokens` | Declarative skill | model-only | Consumption guide for `--md-sys-size-*` / `--md-sys-radius-*` / `--md-sys-space-*` — control ramp, corner scale, spacing/inset/gap ladders, the centering law |
| `skills/material-design-typography-tokens` | Declarative skill | model-only | Consumption guide for the `--md-sys-typescale-*` eleven-voice type scale — voice x level selection, baked leading/tracking/paragraph rhythm |
| `agents/design-system-reviewer` | Agent | spawned | Independent critic for ONE export corpus (a bundle, a DESIGN.md, a guidelines folder, or a cross-platform set) — generator≠critic; preloads `design-system-author`; runs each owning sibling's checker plus the platform linter as the gate of record, then judges against the bound rubric |

Cross-plugin seams (soft, by design): `design-system-author`'s validation loop and
`design-system-reviewer`'s output contract mention `linguistic-techniques`, `linguistics-reviewer`,
and `handoff-compose` — artifacts that now live in the forge plugin — and each degrades to an
inline checklist or fallback report shape when forge isn't installed. No hard edges (preloads or
literal script paths) cross the plugin boundary; every same-plugin script/rubric reference among
the four `design-system-author*` skills and the agent resolves via `${CLAUDE_PLUGIN_ROOT}`.

v0.1.0 · assembled 2026-07-07 · initial: ported from ~/.claude/skills + ~/.claude/agents/design/design-system-reviewer as part of a plugin-decompose partition; merges the design-system-export and material-design-tokens candidate clusters on explicit direction
