# Sources — provenance in trust order

Corpus researched 2026-07-09 (four parallel research waves; ledgers archived in the session
scratchpad; citations inline in each reference). Re-run a wave when its canon moves (an HIG
revision, a Material Symbols re-spec, a WCAG dot-release).

## Trust order

1. **Normative standards** — w3.org/WAI: WCAG 2.1/2.2 Understanding pages (1.4.11 non-text
   contrast, 2.5.8/2.5.5 target size, 4.1.2 name-role-value).
2. **Platform owners** — m3.material.io (applying-icons, bidirectionality, states) +
   m2/m1.material.io archives (system-icons grid, keylines — still the canonical construction
   spec) + fonts.google.com glossaries (the four Material Symbols axes);
   developer.apple.com (HIG sf-symbols, right-to-left, icons; custom-symbol template docs).
3. **Browser/platform reference** — MDN (aria-hidden, forced-colors, forced-color-adjust).
4. **Design systems with published icon specs** — carbondesignsystem.com (sizes, filled-at-16,
   pixel-grid rule, 44 px targets), atlassian.design (1.5 px stroke, corner conventions),
   fluent2.microsoft.design (size tiers, 4 px base grid).
5. **Domain authorities** — nngroup.com (classifying-icons, icon-usability — the labels
   doctrine); CSS-Tricks + practitioner guides for the icon/text alignment math and half-pixel
   stroke technique (corroborated practice, not spec).

## Verified absences (worth as much as the facts)

- No system publishes an **emoji-as-icon** policy — the corpus's content-not-chrome default is
  its own recommendation, marked as such.
- No exhaustive **per-icon RTL mirroring list** was retrievable this wave (fetch-limited — NOT
  a verified absence); the taxonomy is principle-level; verify individual glyphs in the icon
  library metadata.
- **Correction 2026-07-09** (audit-caught inversion, fixed pre-ship): forced-colors mode DOES
  force SVG fill/stroke to system colors — accessibility-and-rtl.md carries the corrected claim.
- **Fluent 2 stroke token values**, Carbon corner radii, Atlassian keyline dimensions, Material
  overshoot dimensions — unpublished; don't invent them.
- Why Material dropped filled/two-tone in the M2→M3 transition — undocumented.
