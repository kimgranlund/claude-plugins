# color — color science, palette design, and verification

Explains color science, designs OKLCH palettes, and verifies them before they ship. Ported from
the personal skill corpus (`~/.claude/skills` + `~/.claude/agents/design/token-builder.md`) as one
of the plugins produced by a `plan-plugin-split` partition of that corpus. Designed by the
make-plugin method; shipped through the harness release gate.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/color-contrast-facts` | Declarative skill (knowledge) | model-only | APCA vs WCAG 2.2, contrast ratios and relative luminance, low-vision/readable color choices, CVD simulation (Brettel/Viénot/Machado) and CVD-safe pairs |
| `skills/color-material-facts` | Declarative skill (knowledge) | model-only | Pigment mixing (Kubelka-Munk, Spectral.js, Mixbox), print-vs-screen and ICC/rendering intents, iridescence, Pointer's gamut, and color-naming standards (ISCC-NBS, Munsell, Ridgway) |
| `skills/color-perception-facts` | Declarative skill (knowledge) | model-only | Vision and appearance science — chroma/saturation, lightness/brightness, opponent process, metamerism, CIECAM02/MacAdam ellipses; carries the full David Briggs huevaluechroma + colorandcontrast.com textbook layer |
| `skills/color-space-facts` | Declarative skill (knowledge) | model-only | The computational layer — space conversions (OKLCH, CIELAB, CAM16/HCT), gamut mapping, HDR/tone mapping, CSS color syntax, image-palette extraction/quantization, and the Culori/Color.js library catalog |
| `skills/color-theory-facts` | Declarative skill (knowledge) | model-only | Harmony, meaning, and history — color-wheel schemes, 60-30-10 proportion, palette mood/symbolism, and designers' colour programmes (Gerstner, Reilly) |
| `skills/make-palette` | Procedural skill | both (`/make-palette`) | Builds OKLCH ramps and semantic role mappings from brand anchors — ramp skeletons, lightness spacing, chroma arcs, hue stability, dark-scheme derivation; every ramp routes to `check-colors` before finalize |
| `skills/check-colors` | Procedural skill | both (`/check-colors`) | Verifies a candidate palette or semantic mapping — contrast (WCAG/APCA), hue stability, perceptual evenness, CVD-safety — card-gated, emits a ColorProof |
| `color-science-project-files` | Supporting library (not a skill — no SKILL.md, lives at plugin root, not under `skills/`) | n/a | The TypeScript color-math library + demo site that `color-space-facts`'s technique files pair with (`src/{spaces,gamut,adaptation,cvd,dithering,...}`); travels alongside its consumer, ported as-is |
| `agents/token-builder` | Agent | dispatched | The design-token seat — role-named token ladders, interaction-state roles, the focus-ring, density/motion constants; preloads `check-colors` (same plugin); soft cross-plugin mentions of `write-handoff` (owned by `harness`) and `check-focus` (owned by `screens`), each with an inline fallback when that plugin isn't installed |

`color-science-project-files` lives at the plugin root rather than under `skills/` — this
workspace's release gate (G2) requires every directory directly under `skills/` to carry a
SKILL.md, and this is deliberately not a skill (no frontmatter was added to force it into that
shape, per the port's own instruction). Several of `color-space-facts`'s technique files point
their "Implementation" section at its `src/` tree by relative path
(`../../../color-science-project-files/src/...`); every such relative reference across the ported
packs was shifted one level to match this plugin-root placement (the pre-migration
`~/.claude/skills/` layout had it as a `skills/`-level sibling instead). A handful of the knowledge
packs' `references/INDEX.md` files cite files owned by a sibling pack (e.g. `color-theory-facts` citing
`color-perception-facts`'s Albers chapter) or, in one case, a pack outside this plugin entirely
(`color-contrast-facts` citing `lettering-facts`'s low-vision reference) — these are
named in prose rather than linked by relative path, since this workspace's `corpus_check.py` only
reconciles a pack's own file tree.

`agents/token-builder`'s frontmatter preload list is `[check-colors]` only — `write-handoff` and
`check-focus` were dropped from the hard preload because they now live in different plugins
(`harness` and `screens`, respectively) and a `skills:` preload cannot cross a plugin boundary. Both are
still referenced in the agent's body prose as soft, degrade-gracefully mentions.

## ADR-0006 transition table (renamed 2026-07-21)

Old handles remain greppable only in ledgers, CHANGELOGs, ADRs, and attics.

| Old name | New name |
|---|---|
| `color-science-accessibility` | `color-contrast-facts` |
| `color-science-materials` | `color-material-facts` |
| `color-science-perception` | `color-perception-facts` |
| `color-science-spaces` | `color-space-facts` |
| `color-theory` | `color-theory-facts` |
| `color-verify` | `check-colors` |
| `palette-design` | `make-palette` |

v1.0.5 · assembled 2026-07-21 · 1.0.5: ADR-0007 dir alignment — the plugin's directory renamed to its plain plugin name (was the frozen `color 0.1.0`); version-suffixed, space-bearing paths retired estate-wide; pointer updates only · v1.0.4 · assembled 2026-07-21 · 1.0.4: ADR-0006 harness-rename sweep — live references rewritten (token-builder's write-handoff/check-focus pointers, harness plugin mentions); pointer updates only · v1.0.3 · assembled 2026-07-21 · 1.0.3: ADR-0006 screens-rename sweep — live references rewritten (token-builder's check-focus pointer, README seam notes, suites); pointer updates only · v1.0.2 · assembled 2026-07-21 · 1.0.2: ADR-0006 design-kits-rename sweep — live references rewritten; pointer updates only · v1.0.1 · assembled 2026-07-21 · 1.0.1: ADR-0006 typography-rename sweep — live references rewritten; pointer updates only · v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0006 rename PR 1/9 — the simple-paradigm member renames: color-science-{accessibility,materials,perception,spaces} → color-{contrast,material,perception,space}-facts · color-theory → color-theory-facts · color-verify → check-colors · palette-design → make-palette; the plugin name and token-builder keep theirs. MAJOR bump — names are APIs and this is breaking; the transition table above maps old → new. Workspace-wide reference sweep (112 files, ledger history excluded); baseline and post-rename blind eval-runs recorded in the campaign PR · v0.2.2 · assembled 2026-07-19 · 0.2.2: knowledge-pack factory-route convention repointed from scribe's retired `knowledge-forge` to forge's `pack-forge` (workspace-wide rename campaign) — every color-science-*/color-theory reference to its authoring factory updated; no functional/behavior change, a naming correction only · v0.2.1 · assembled 2026-07-16 · 0.2.1: color-verify wires the verify-family mechanics block (Issue #8; canon cross-plugin-soft: ui-audit's verify-mechanics) — color.cvd-collapse and sibling judgment slugs, symptom index, armed mode, waiver ladder starting at the per-rule rung (no per-pair card flag) with the AA floor never waivable · v0.2.0 · assembled 2026-07-16 · 0.2.0: palette-design gains the taste gate at anchor negotiation (Issue #13; canon: ui's taste-elicitation, degraded inline) — open direction or a multi-direction DecompositionGap renders candidate ramps as ONE labeled HTML artifact (each gamut-safe and evenness-passing; contrast stays step 7's gate) → one AskUserQuestion → the answer locks into ramp provenance + the BrandSchema/UISchema anchor (token realization stays downstream via token-builder); routing row + Update tripwire added; fresh-context audit's two majors applied · v0.1.7 · assembled 2026-07-15 · 0.1.7: subfolder conformance (ruled 2026-07-15: the sanctioned skill-subfolder set is evals/references/scripts/assets — release_gate G2 now warns on any other): color-verify's verification/ and palette-design's ramps/ moved under assets/; ramp_build.py's curve_path_for() repointed (the one code-level resolution in the campaign), both selftests green post-move · v0.1.6 · assembled 2026-07-14 · 0.1.6: displayName 'Color' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.1.5 · assembled 2026-07-12 · 0.1.5: token-builder effort high→xhigh (coding-row ceiling, forge 1.22.0 seat ladder) · v0.1.4 · assembled 2026-07-10 · 0.1.4: author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder) · assembled 2026-07-09 · 0.1.3: the color-verify↔accessibility seam resolved honestly after 4 blind runs — fence broadened to measurement asks, color-verify claims the failing verbatims, and the five flip-by-judge cases marked a KNOWN AMBIGUOUS SEAM (either owner answers correctly; never tune to chase); phantom fences repointed · assembled 2026-07-09 · 0.1.2: references to the renamed design-systems/typography skills swept (ADR-0001) · assembled 2026-07-09 · 0.1.1: token-builder fallback 'Tests run'→'Tests/checks run' (harness-audit finding, estate-wide sweep) · assembled 2026-07-07 · initial: ported from ~/.claude/skills + ~/.claude/agents/design/token-builder as part of a plugin-decompose partition
