---
name: palette-design
description: >-
  Design OKLCH color ramps and semantic role mappings from brand anchors. Use when the user wants to build a
  ramp from a brand anchor, extend a palette to a full scale, design the color system, map semantic roles,
  choose the intent hues (danger/warning/success/info), or derive the dark scheme — ramp skeletons (default
  13-step 0/50/100..900/950/1000), lightness spacing, chroma arcs, hue stability, gamut-safe C-only reduction,
  and role assignment, with every ramp verified by color-verify before finalize. NOT for verifying an existing
  palette or emitting a ColorProof (color-verify); NOT for color-space math or converting between color spaces
  (color-science-spaces); NOT for harmony, meaning, or art direction — vibe, mood (color-theory); NOT for
  realizing token layers in a repo (token-builder); NOT for the whole design-system export a platform consumes
  (design-system-author-claude-code / -google-stitch / -figma-make; cross-platform: the design-system-hub
  hub) — this skill designs only the ramp it consumes.
disable-model-invocation: false
user-invocable: true
---

# palette-design — OKLCH ramps & semantic mappings, verified before emit

Generator peer of [[color-verify]]: this skill designs the palette; the verifier proves it. It
owns the **how** of color in a product UI — from brand anchors and a role spec it derives the
numeric OKLCH steps, maps them to semantic roles, and derives the dark scheme. Perceptual
consistency under OKLCH is a **constrained-optimization problem, not a free choice**: given
anchors + constraints (contrast floor, chroma ceiling, hue stability) only a narrow corridor of
valid ramps exists — the job is to find that corridor, not to invent freely. The split's
contract: **design → verify** — nothing finalizes until [[color-verify]] returns a passing
ColorProof.

## Inputs (schemas + elicit fallback)

- **UISchema** — the project's token/role spec: color families, scale steps, semantic roles,
  contrast floor. Semantic roles are the project spec's; this skill NEVER invents new ones.
- **BrandSchema** — the brand's anchor colors + art-direction constraints (chroma ceiling, hue).
- **Neither exists?** Elicit: color families, scale step count, contrast floor, brand anchors.

Classify the ask: build a ramp from an anchor (needs anchor hue + step count) · extend an
existing palette (needs current palette + target coverage) · assign semantic roles (needs the UI
surface list) · derive the dark scheme (needs the light palette). "Verify this palette" is not
this skill — route to [[color-verify]].

## Procedure (anchor → ramp → roles → schemes → verify handoff)

1. **Skeleton.** Per family the UISchema declares (`neutral`, `accent`, `danger`, …): step count
   from `UISchema.primitive.color.scale` — the project token spec's scale list; absent → elicit
   (default 13: `0, 50, 100..900, 950, 1000`); the L grid from `assets/ramps/<family>-curve.json` (the
   canon); steps the curve doesn't anchor interpolate linearly in label space.
2. **Anchor.** A stated brand anchor (e.g. `accent-500 = oklch(0.62 0.18 270)`) overrides step
   500's ideal L; re-interpolate so per-label-unit evenness (numbers table) still holds. If the
   anchor cannot yield a full ramp while holding evenness, flag a `DecompositionGap` — ask for a
   different anchor. `scripts/ramp_build.py` owns the arithmetic of steps 1–4; anchor negotiation
   and role-mapping judgment stay with the model — the script reports gaps, it never renegotiates.
3. **Chroma arc.** `C(L) = C_max × exp(−k × (L − L_peak)²)` — `C_max` solved so the anchor step
   reproduces the anchor's C exactly; `L_peak`/`k` from the curve JSON (accent 0.60/28; ≈ 0.70+
   pastels · ≈ 0.50 jewel tones are anchor-negotiation moves); extreme caps per
   `accent-curve.json extremeFloors` (numbers table). Neutrals run the same bell at
   `C_max ≤ 0.02` — peaks mid-L, decays toward the ends (exactly 0 if `neutral: true-grey`).
4. **Hue + gamut.** Hue constant by default; allow ≤ ±8° drift only when gamut demands it, only
   toward the next-neighbor hue (blue at high L drifts toward cyan, never green) — a judgment
   trade the script never makes. Out-of-gamut steps take **C-only reduction** — chroma down in
   0.005 steps, never L or H, preserving ramp spacing — with the ΔC recorded in provenance
   (`gamut-reduced: ΔC = 0.015`); anchor-step ΔC > 0.05 means the anchor itself is out of gamut —
   flag it.
5. **Roles.** Map steps to the UISchema's semantic roles (defaults below; UISchema overrides).
   Intent hues (danger/warning/success/info) come from `assets/ramps/intent-hues.json`: distinct,
   culturally load-bearing hue regions.
6. **Dark scheme.** Neutrals mirror L (`L_dark = 1 − L_light`); accents flip L around 0.55, hold
   hue, cut chroma 10–15% (dark surfaces hide chroma less — reducing C avoids glow).
7. **Verify handoff.** Hand the candidate — every scheme — to [[color-verify]]: it gates the
   contrast arithmetic (`contrast-check.py`), sweeps (theme × scheme × contrast), and checks CVD
   safety. A violation returns as a `DecompositionGap` — re-enter at the step its remediation
   names. No ramp or mapping is emitted unverified; each emitted token carries OKLCH + sRGB +
   provenance + its checked contrast pairs.

## The numbers (derived from `assets/ramps/` — the canon)

| Parameter | Value |
|---|---|
| Scale | default 13 steps: `0, 50, 100..900, 950, 1000` (`scaleSteps` in `ramps/*-curve.json`; `UISchema.primitive.color.scale` overrides) |
| L grid | the full grids live in the curve JSONs; key anchors — neutral `0 → 0.995 · 500 → 0.600 · 950 → 0.150 · 1000 → 0.080`; accent `0 → 0.990 · 500 → 0.620 (the brand step — a stated anchor overrides) · 950 → 0.185 · 1000 → 0.100` |
| Evenness | per-label-unit ΔL (ΔL ÷ Δlabel): adjacent gap-to-gap ratio ≤ 1.5 — [[color-verify]]'s form, checked on every `ramp_build.py` run |
| Hue drift | ≤ ±8°, only toward the next-neighbor hue, only for gamut |
| Chroma extremes | C ≤ 0.04 below L 0.15 · C ≤ 0.03 above L 0.95 (`accent-curve.json extremeFloors`) |
| Neutral chroma | ≤ 0.02 on every step — a design margin, deliberately under [[color-verify]]'s 0.06 gate for declared-tinted neutrals; exactly 0 if `neutral: true-grey` |
| Gamut | C-only reduction in 0.005 steps, never L or H; anchor-step ΔC > 0.05 → the anchor is out of gamut, flag |
| Dark scheme | neutrals L-mirrored; accent L flipped about 0.55; chroma −10–15% |

Role defaults (light / dark): `--surface` neutral-50/950 · `--surface-raised` 0/900 ·
`--surface-sunken` 100/1000 · `--on-surface` 900/50 · `--on-surface-muted` 700/300 ·
`--border` 200/800 · `--border-strong` 400/600 · `--accent` accent-500 · `--on-accent` neutral-0
or neutral-1000 (whichever clears contrast) · `--focus-ring` accent-600 light / accent-400 dark.

## Mechanism — `scripts/ramp_build.py`

The ramp arithmetic is deterministic derivation, so it routes to code: `ramp_build.py <family>
[--curve assets/ramps/<file>.json] [--anchor "oklch(...)"] --json` runs skeleton → chroma bell → C-only
gamut walk from the curve JSON, reports monotonicity, evenness, gamut state, and any
`DecompositionGap` (exit 1 — a gap is never silently shipped). `ramp_build.py selftest` locks it:
the neutral canon build (monotone L, evenness ≤ 1.5, all steps in gamut) plus a negative control —
an out-of-gamut anchor must come back with reduced C and byte-identical L and H. The gate is
necessary, not sufficient: it proves the geometry, [[color-verify]] proves the palette.

## Detection catalog (generation anti-patterns)

Inventing a semantic role (`--primary-alt-subtle-hover`) — roles are the project spec's ·
gamut-mapping by lightness or hue instead of C-only reduction · a ramp or mapping emitted without
a [[color-verify]] run · HSL/HSV ramp generation (perceptually misleading) · shade-by-RGB-scalar
(destroys hue and contrast) · hex without OKLCH provenance · one hue serving several intents ·
a pair authored without a contrast number (the verifier catches it downstream, but authoring one
is already the defect).

## Material & routing

| Path / peer | Use |
|---|---|
| `assets/ramps/neutral-curve.json` | CANON — L-anchor grid + chroma bell/ceiling for neutral families |
| `assets/ramps/accent-curve.json` | CANON — L-anchor grid, chroma-bell parameters, extreme caps, gamut policy for accent/intent families |
| `assets/ramps/intent-hues.json` | CANON — hue ranges for danger/warning/success/info + tolerance + collision rule |
| `scripts/ramp_build.py` | the build arithmetic + selftest (skeleton · bell · gamut walk · invariant report) |
| `scripts/routing-corpus.json` | the checked-in M2 routing corpus |
| [[color-verify]] | the mandatory verify handoff — contrast gate, (theme × scheme × contrast) sweep, ColorProof |
| [[color-science-spaces]] | the perceptual theory these constraints assume (OKLCH, gamut math) |
| [[color-science-accessibility]] | the perceptual theory these constraints assume (APCA/WCAG, CVD) |
| [[color-theory]] | art direction upstream of the anchors — harmony, palette mood/vibe, what a color communicates |
| `token-builder` agent | realizes the verified palette as a token layer in a repo |

**Update:** when [[color-verify]]'s invariants or `ramps/*.json` move, re-derive the numbers
table and the procedure's constants from them — never patch the prose independently — then re-run
`ramp_build.py selftest` and the routing corpus.

**Done** = every scheme carries a passing ColorProof + provenance; **NOT done** = any emit
without one.
