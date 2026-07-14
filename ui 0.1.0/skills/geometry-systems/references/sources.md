# Sources — provenance in trust order

Corpus researched 2026-07-15 (one wave, two axes: scale theory + composable spacing). Re-run the
wave for an axis when its canon moves (Material re-specs its spacing scale, Tailwind changes its
default scale shape).

## Trust order

1. **Platform/design-system owners, primary docs** — m1.material.io/layout/metrics-keylines.html,
   m3.material.io/styles/spacing, tailwindcss.com/docs/customizing-spacing,
   carbondesignsystem.com (spacing tokens).
2. **This estate's own worked instances** — `component-forge`'s `references/geometry-system.md`
   (the mechanized button-family law and its "Composed padding" section, `geometry-check.py`
   selftest-proven), `material-design-geometry-tokens` (Material-consumption binding guide). These
   are cited as EXAMPLES this pack's principles already hold up against, not independent external
   sources.
3. **Domain commentary** — rejuvenate.digital, uxplanet.org, and similar 8pt-grid explainer
   articles, used only to corroborate the rationale already stated by trust-order-1 sources, never
   as the sole source for a claim.

## Known unverified edges (kept out of the corpus, listed so nobody re-invents them)

- **Apple's spacing scale as a single numeric ladder.** Unlike Material's explicitly published
  4dp/8dp two-tier grid, Apple's Human Interface Guidelines do not appear to publish one
  centralized numeric spacing scale the way Material does — spacing conventions across Apple's own
  apps are widely observed to cluster around 8pt-family steps, but this pack found no single HIG
  page stating a canonical ladder the way `m1.material.io/layout/metrics-keylines.html` does for
  Material. Treat any specific "Apple uses Npx here" claim as [inferred] from ecosystem convention,
  not as HIG's own stated rule, until a specific HIG page is found and cited.
- **A universal "correct" progression formula.** No source found publishes a formula for exactly
  where a scale should transition from dense-linear to sparse; every system's specific transition
  point is that system's own tuned choice, cited as example shape, not derived from a law the way
  `component-forge`'s glyph-centering law is.
- **IBM Carbon's exact base-unit rationale.** Carbon's spacing tokens (`spacing-01`…`spacing-13`)
  were confirmed to exist and follow the sparse-at-the-top shape, but this pack did not locate
  Carbon's own stated rationale for its specific base unit — cited for the shape, not the "why."
