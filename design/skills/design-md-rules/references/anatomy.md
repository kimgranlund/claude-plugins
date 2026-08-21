# DESIGN.md anatomy

## What the file is

A DESIGN.md is a **prompt, not documentation**. It is the single self-contained file that teaches a design agent (Claude Design, Claude Code, or any LLM) to generate on-brand UI. Its first law appears in its own opening: *"Read this file as your instructions — it is the prompt."* Every authoring decision follows from that identity:

- Documentation describes; a DESIGN.md **commits** ("Never hardcode a color", not "colors should generally use tokens").
- Documentation assumes a human who can ask questions; a DESIGN.md assumes a fresh-context agent that gets exactly one read.
- **Think of it as a SKILL for a brand**: a name + description, then knowledge (tokens), rules (laws), and procedures (a work order). The Agent Skills mental model transfers wholesale.

## The two layers

### Layer 1 — YAML frontmatter (normative, machine-readable)

The frontmatter carries the token payload. Values here are law; the prose explains application. Reference-dialect keys (Ultimate Tokens):

```yaml
---
version: alpha
name: <Brand>
description: The <Brand> design system.
colors:
  # every role ships a light value AND a `-dark` sibling — pick the pair, never one end
  primary: "oklch(0.6498 0.1222 224.12)"
  primary-dark: "oklch(0.6498 0.1222 224.12)"
  primary-hover: "oklch(0.496 0.0966 227.89)"
  primary-hover-dark: "oklch(0.7657 0.1409 221.45)"   # hover darkens in light scheme, brightens in dark
  primary-on-primary: "oklch(1 0 89.88)"
  # …neutral surfaces, outline, on-surface(-variant), every family × {fill, on, hover, disabled}; -active on interactive-fill families
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 440        # fractional weights are legal — variable-font axis positions
    lineHeight: 1.5        # ALWAYS a unitless factor, never px
  kicker-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.385
    letterSpacing: 0.14em  # tracking ALWAYS em, never px
spacing: { none: 0px, xs: 4px, sm: 8px, md: 12px, lg: 16px, xl: 24px, 2xl: 32px, 3xl: 48px, 4xl: 64px, 5xl: 96px }
rounded: { none: 0px, xs: 4px, sm: 8px, md: 12px, lg: 16px, xl: 28px, full: 9999px }
components:
  button-primary:
    backgroundColor: "{colors.primary}"     # recipes reference tokens by {path} interpolation —
    textColor: "{colors.primary-on-primary}" # a recipe NEVER carries a raw value
    typography: "{typography.ui-md}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
---
```

Hard properties of the layer:
- **Scheme parity**: the light inventory and the `-dark` sibling inventory are identical key sets.
- **High-resolution color**: OKLCH (or another wide-gamut notation), never bare rounded hex. Alpha rides inline: `oklch(L C H / 30%)`.
- **Typography levels are indivisible**: size + lineHeight + weight (+ tracking) set together; a level missing one is broken.
- **Component recipes are state-complete**: every interactive recipe ships `-hover` siblings; `-active` is required where the recipe's family serves as an interactive fill (see grammar.md's state rule, amended 2026-08-20).

### Layer 2 — Markdown prose (the spine)

The reference spine, in order — each section earns its place by changing agent behavior:

1. **Overview** — the philosophy in one line ("calm, even surfaces carry the layout and color arrives as accent") plus the brand's explicit refusals.
2. **Colors** — role reasoning ("reason over roles, never raw hexes"), the token naming grammar, surface ladder, the pairing law. See `grammar.md`.
3. **Typography** — the one-level rule ("set size and line-height and weight together from one level, never free-type"); weight as voice; and the **text-rendering baseline, always included** (a fenced CSS block the consumer pastes verbatim): `-webkit-font-smoothing: antialiased` + `-moz-osx-font-smoothing: grayscale` (the macOS pair — consistent weight in both schemes), `text-rendering: optimizeLegibility` (kerning + ligatures engaged), `font-optical-sizing: auto` (variable fonts use their optical axes), `font-synthesis: none` (no faux bold/italic — weights resolve from the actual font, never synthesized), `font-kerning: normal`, `font-variant-ligatures: common-ligatures`, plus `code, pre, kbd { font-variant-ligatures: none }` so code-like units and mono values never ligate.
4. **Layout** — the spacing composition law ("an off-scale gap does not exist"), reading measure (~60–75ch), whitespace-over-borders.
5. **Elevation & Depth** — "a surface step, not a drop shadow": background → surface → surface-high; shadow as garnish only.
6. **Shapes** — the radius-per-element map (chips xs · inputs sm · buttons md · cards lg · modals xl · pills full) and "one radius language per view".
7. **Components** — per-recipe prose **with explicit states**: "generic output betrays itself in hover/focus/disabled." Name the focus treatment numerically (e.g. 2px ring at 2px offset).
8. **Do's and Don'ts** — exactly ~3 hard rules stated as prohibitions, then softer preferences. The reference trio: never hardcode a color · never cross an on-pair · never stack competing primaries.
9. **Responsive Behavior** — stack point, size reductions, touch-target floor.
10. **Agent Prompt Guide** — the work order for the consuming agent: tokens first → roles then scheme → scale then states → one focus per view → name by grammar. Ends with the conflict rule ("when rules conflict, the three hard rules win").

## Open-endedness (the part most authors miss)

The spine above is a **floor, not a ceiling**. A DESIGN.md admits any section the brand needs an agent to know — this is the "it's a SKILL" property. Sections that routinely earn their place:

- **Voice & Tone** — person, casing, punctuation, emoji policy, with verbatim example phrasings.
- **Iconography** — the glyph system, stroke weight, sizing ramp, emoji/unicode policy. (A generator whose every kit ships an icon system may emit this always-on — the ultimate-tokens exporter does, inserting it with Motion between Shapes and Components; noted 2026-08-20.)
- **Imagery** — photographic treatment, color temperature, grain, when illustration vs photo.
- **Motion** — durations, easings, what never animates. (Like Iconography, legally always-on for a generator whose kits all carry motion tokens.)
- **Data visualization** — categorical palettes, axis treatment.
- **Cultural references** — the design lineage that anchors taste (see `brand-architecture.md`).
- **Copy examples** — real product strings an agent can pattern-match.

The test for any candidate section: *would a fresh agent generate differently with it than without it?* Yes → include. No → cut; padding dilutes the prompt.

## Consumption contract

- **Claude Design** reads DESIGN.md to seed a full design system project: token CSS, components, preview cards. The frontmatter becomes CSS custom properties; the prose becomes the readme's foundations and the agent's standing rules.
- **Claude Code** reads it as design guidance while writing production UI in whatever stack the repo uses.
- Therefore the file is **framework-neutral by construction**: it names roles, scales, and laws — never React, Svelte, Tailwind, or any component API. A DESIGN.md that says `className="btn-primary"` has leaked implementation.
- Companion files are optional, not required: a `tokens.json` (or `.css`) machine carrier and a README receipt may ride alongside (Ultimate Tokens ships both), but **the DESIGN.md alone must be sufficient as a generation prompt**. The division of labor: DESIGN.md *teaches the system* — the grammar, the laws, and the 15–25 consumption roles an agent reasons over; the **exhaustive token inventory** (full ramps, every step of every family) belongs in the companion carrier, never dumped into DESIGN.md — token bloat starves the prompt the prose exists to be.
