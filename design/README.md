# design — color, typography, and design-system exports

One plugin for the visual-design layer: color science and OKLCH palettes, the 11-voice
typography system, Material Design's token grammar, and the export bundles a generative design
agent consumes (Claude Design/DESIGN.md, Figma Make, Google Stitch). Formed 2026-07-21 by
merging the `design-kits`, `color`, and `typography` plugins (ADR-0008) — the trio carried 48
cross-plugin mentions, the workspace's highest-coupling seam after the ui merge precedent.
Legacy per-plugin ledgers: `legacy/README-{design-kits,color,typography}.md`.

## Map

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/make-palette` | Procedural | both | OKLCH ramps + semantic role mapping from brand anchors; every ramp verified by `check-colors` |
| `skills/check-colors` | Procedural | both | Palette/pair verification — contrast, hue stability, evenness, CVD-safety → ColorProof |
| `skills/color-contrast-facts` | Knowledge | model-only | APCA vs WCAG, luminance, CVD simulation and safe pairs |
| `skills/color-perception-facts` | Knowledge | model-only | Vision/appearance science — chroma vs saturation, opponent process, CIECAM02 |
| `skills/color-space-facts` | Knowledge | model-only | Space conversions, gamut mapping, gradients, CSS color, libraries (project files: `color-science-project-files/`) |
| `skills/color-theory-facts` | Knowledge | model-only | Harmony, meaning, history — schemes, 60-30-10, palette mood |
| `skills/physical-color-facts` | Knowledge | model-only | Pigment/print physical color — Kubelka-Munk, ICC, iridescence, color naming (was `color-material-facts`) |
| `skills/pick-fonts` | Procedural | both | Design an 11-voice typography system from a brand brief; craft verification |
| `skills/font-token-rules` | Knowledge | model-only | The `--type-*` token grammar — voice × step, leading, concrete font per slot |
| `skills/lettering-facts` | Knowledge | model-only | The cited type corpus — anatomy, classification, scripts, OpenType, text a11y |
| `skills/make-design-system` | Procedural | both | The export hub: full design-system bundle across platforms (was `make-design-kit`) |
| `skills/make-dscard-kit` | Procedural | both | Claude Design / Claude Code bundle (DESIGN.md + tokens.json + @dsCard previews) |
| `skills/make-figma-make-kit` | Procedural | both | Figma Make guidelines/ folder export |
| `skills/make-stitch-kit` | Procedural | both | Google Stitch DESIGN.md export |
| `skills/design-md-rules` | Knowledge | model-only | The DESIGN.md format contract (term-of-art name, ADR-0008) |
| `skills/icon-rules` | Knowledge | model-only | Icon sizing/mirroring/set discipline (Phosphor house default) |
| `skills/figma-plugin-facts` | Knowledge | model-only | Figma plugin API facts |
| `skills/material-color-facts` | Knowledge | model-only | Material `--md-sys-color-*` consumption guide |
| `skills/material-type-facts` | Knowledge | model-only | Material typescale consumption guide (15 voices) |
| `skills/material-shape-facts` | Knowledge | model-only | Material geometry — control ramp, radius, space ladder |
| `skills/material-motion-facts` | Knowledge | model-only | Material `--md-sys-motion-*` tokens |
| `skills/material-token-facts` | Knowledge | model-only | The `--md-sys-*` token glossary across the three domains |
| `skills/artifact-styling-rules` | Knowledge | model-only | Styling/authoring doctrine for Claude Artifacts — platform facts, token role-alias architecture, type/layout, mermaid, shells/genres (#650) |
| `agents/token-builder.md` | Agent | dispatched | Realizes palettes/dimensions as project token layers |
| `agents/font-choice-checker.md` | Agent | dispatched | Grades ONE typography system against pick-fonts' rubric |
| `agents/design-system-checker.md` | Agent | dispatched | Grades ONE export bundle against the owning sibling's rubric (was `design-kit-checker`) |

## ADR-0008 transition table (merged 2026-07-21)

Three plugins merged into `design`; three members renamed. Old handles remain greppable only in
ledgers, CHANGELOGs, ADRs, and the legacy READMEs.

| Old | New |
|---|---|
| `design-kits` / `color` / `typography` (plugins) | `design` |
| `make-design-kit` | `make-design-system` |
| `color-material-facts` | `physical-color-facts` |
| `design-kit-checker` (agent) | `design-system-checker` |

v1.1.1 · 2026-08-18 · #660: artifact_check.py false-positive fixes — literal-outside-root scans only CSS (`<style>`/`style=""`; whole text for a bare stylesheet), all `:root` excluded, so prose `#NNN` issue refs no longer report; missing-ground accepts `var(--c-paper)` (css_build.py's emission). Selftest: negative controls for both + a real-literal-in-style positive. Pure script fix.
v1.1.0 · 2026-08-18 · #650: new skill `artifact-styling-rules` — 5-axis pack for Claude Artifact visual doctrine, migrated from docs' `artifact-rules` (now procedure-only) per Kim's ruling. 4-source research wave, dated 2026-08-18. New `artifact_check.py` (6 grep-gates, selftest green) + `rubric.md` (R1-R8). Reciprocal fences: make-design-system, break-down-layout. Gate clean. Full resolutions: lld-0020.
v1.0.9 · 2026-08-17 · reciprocal fence (docs' issue #619): `make-design-system`'s description gains "NOT for consuming an already-authored system into a rendered artifact/report page (docs' make-artifact)" — docs' new `make-artifact`/`artifact-rules` pair CONSUMES this hub's exported design systems; this hub still owns authoring/grading them only. One reciprocal no-trigger eval case added (n13). Trimmed the now-redundant "Owns core+profiles architecture and doctrines" clause to hold the W8 700-char budget. skill_lint.py clean.
v1.0.8 · 2026-08-16 · checker-agent diet tail (#367): font-choice-checker's description already had no removable boilerplate (collide.py scores unchanged, e.g. ↔doc-checker 75.5). Body opener reworded for consistency with #364's siblings. Critic clean. No evals owed.
v1.0.7 · 2026-08-16 · checker-agent description diet (#357): design-system-checker's description drops the shared fresh-isolated-context / never-grades-own-work / gap-map boilerplate (collide.py's top cross-plugin *-checker baseline, 6 agents, 103.9-158.4); doctrine moved to body. Re-run: ↔doc-checker 158.4→78.3, ↔flow-checker 115.4→101.1, ↔code-checker 109.9→91.3, ↔wiring-checker below threshold. Batched critic pass (6 files) clean; no evals.json owed. Siblings in docs/screens/teamwork trimmed same PR.
v1.0.6 · 2026-08-16 · #348 footer sweep: 8 packs' stamped "Extending this pack" paragraph replaced with the one-line `Extension: governed by [[make-pack]]` citation per pack-writing-rules (harness 3.8.9) — mechanical, bodies otherwise untouched
v1.0.5 · 2026-08-16 · checker retier (Kim's ruling): 2 *-checker agents move effort high→medium, model fable unchanged — review quality held at medium across the 2026-08-15/16 rounds while inherited-xhigh runs added cost, not findings
v1.0.4 · assembled 2026-08-15 · 1.0.4: issue #263 — the #79-style description diet wave scoped to `design`. Baseline (2026-08-15): 22 skills, 17,248 chars, ~784 avg — the estate's fattest per-skill, 8 of them over the W8 700-char budget (material-token-facts, make-stitch-kit, material-type-facts, color-perception-facts, physical-color-facts, make-dscard-kit, icon-rules, figma-plugin-facts — all 1,028–1,102 chars). Trimmed all 8 to the budget; the three kit skills (make-stitch-kit/make-dscard-kit/make-figma-make-kit) stayed model-invocable per a same-day scope ruling — make-design-system dispatches them by name and `disable-model-invocation: true` would block that Skill-tool path (#134/#135 class) — trim only, never unlisted. Blind re-judge via `/check-routing design` across all 22 suites (524 cases, fresh shuffle each dispatch): 3 real regressions surfaced from the trim itself — figma-plugin-facts lost its "unit-test plugin code" trigger (dead miss on t11), material-token-facts lost "-dim vs -low" and "scrim strengths" (dead + stolen), material-type-facts lost "menu item" from its covered-element list (stolen by font-token-rules), color-perception-facts lost "warm/cool as a perceptual axis" (stolen by color-theory-facts) — each healed by restoring the cut phrase and trimming elsewhere to hold the budget, then reverified via a scoped re-judge; all four now route correctly. Remaining failures across the full sweep (color-contrast-facts, pick-fonts, make-design-system, icon-rules t13, color-space-facts skips) are pre-existing single-judge noise in untouched siblings, several already recorded as known-ambiguous in their own suite notes — not attributable to this wave. Plugin total: 17,310 (measured) → 14,331 chars, avg 787 → 651. `evals/evals.json` dated-note updated on all 8 touched suites. skill_lint W8/W2 clean on every touched description · v1.0.3 · assembled 2026-07-26 · 1.0.3: issue #106 — material-color-facts' post-diet dead-routing repaired. #94's blind re-measure found FIVE bare-phrasing triggers routing to none (18/23): the dieted description's leading clause — 'whose color tokens use the Material --md-sys-color-* naming' — read as a PRECONDITION, so a prompt naming a color job but not the grammar failed it, even though two of the dead prompts were quoted VERBATIM in the description. Fix is shape, not phrasings: the description now leads with the JOB unconditionally and demotes the grammar to the covers sentence ('the estate's default color grammar'); suite note dated. Blind re-judge over the six seam suites (127 cases, fresh shuffle, judges given the new menu): material-color-facts 23/23, make-palette 23/23, material-type-facts 20/20, material-token-facts 15/16 (one judge-marginal glossary flip), check-colors and material-shape-facts unchanged at their pre-existing #94 fails — no new leak introduced anywhere. W8 budget held · v1.0.2 · assembled 2026-07-25 · 1.0.2: description diet (PR #92) — 14 SKILL.md descriptions + 3 agent descriptions trimmed to the resident-context budget (issues #79/#80 completion) · v1.0.1 · assembled 2026-07-25 · 1.0.1: retired the stale ADR-0006 transition-table section in `legacy/README-design-kits.md` — dead since ADR-0007 (2026-07-21) renamed every plugin dir to its plugin name and retired the workspace CLAUDE.md alias table it pointed to; replaced with the one true line, directories align with plugin names (ADR-0007); the live `## ADR-0008 transition table` in this file's own footer is unrelated and untouched · v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0008 — design-kits 1.0.6 + color 1.0.6 + typography 1.0.6 merge into `design` (coupling evidence: 48 intra-trio mentions; plan-plugin-split merge tests PASS). Three renames ride along (table above): the hub returns to the real term of art make-design-system (member-level term-of-art stutter exception, ADR-0008, extending ADR-0006 Decision 7), physical-color-facts frees "material" to mean only Material Design inside the plugin, design-system-checker follows its hub. Source ledgers preserved under legacy/. Baseline floors carried from the ADR-0006 measured runs (508/515 union); post-merge re-measure on the 22-skill union menu: 3 blind-judge rounds (515→488 raw, 524→507, 524→515 = 98.3% vs 98.6% baseline), ADR-0008 Decision 5 seams fenced — 22 ordered context splits, 8 thief-side description fences, 9 reciprocal no-trigger cases; material-token n07 recorded known-ambiguous (3/3 rounds); parity evidence on PR #73 ·
