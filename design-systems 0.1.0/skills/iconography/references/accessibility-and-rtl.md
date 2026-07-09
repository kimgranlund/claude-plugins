# Accessibility and RTL — the icon policy layer

Researched 2026-07-09 (w3.org/WAI, developer.mozilla.org, m3.material.io bidirectionality,
developer.apple.com HIG right-to-left, nngroup.com, carbondesignsystem.com).

## Contrast (WCAG 1.4.11 Non-text Contrast, AA)

Icons **required for understanding** need **3:1 minimum** against adjacent colors — computed
values unrounded (2.999:1 fails), no size exemption, measured from the markup/stylesheet colors
(anti-aliasing doesn't count for you). Exceptions: inactive controls, logos, essential sensory
presentations. Carbon goes stricter for its monochrome icons: the 4.5:1 text ratio.

## Decorative vs semantic in markup

- **Decorative** (label sits beside it): `aria-hidden="true"` on the icon span — and NEVER on a
  focusable element or an ancestor of one (inherited by children).
- **Semantic/interactive**: an accessible name is mandatory (WCAG 4.1.2 — non-empty name,
  programmatically determinable). Name precedence: `aria-labelledby` > `aria-label` > own
  attributes (title/alt) > label element > text content.
- **Tooltips are not names**: hover-dependent, undiscoverable to keyboard/touch/screen-reader
  users — a tooltip may supplement an `aria-label`, never replace it.
- Content parity: what sighted users see and what AT announces must match.

## Icon-only buttons

WCAG makes them nameable; NN/g makes them rare: unlabeled icons confuse users across decades of
research, and labels — visible ones — are the mitigation. Reserve icon-only for the universal
trio (home/print/search) and space-critical toolbars, always with the accessible name.

## RTL mirroring taxonomy

**Mirror** (direction follows reading order): back/forward, left/right arrows, text-alignment
and list icons, progress/timeline indicators depicting time's passage ("forward points to the
left" in RTL — Material bidirectionality), motion-toward-forward glyphs, sliders with direction.

**Never mirror**: clocks and circular refresh (**always clockwise** — Material's stated
exception) · **media playback controls and media progress** (they follow media direction, not
reading direction) · checkmarks · question marks · physical objects with no directional meaning
· logos/brand marks · glyphs containing embedded text (handle case-by-case).

Material's compact rule: "icons that do not communicate direction are not changed."
Apple's implementation note: SF Symbols mirror themselves automatically where needed; use
leading/trailing (not left/right) layout attributes and most of the UI mirrors for free. The
two systems agree on the principles; no exhaustive per-icon list was retrievable in this wave
(fetch-limited, NOT a verified absence — check the icon libraries' own metadata per glyph).

## Forced-colors / high-contrast mode

SVG `fill`/`stroke` ARE in forced-colors mode's forced-to-system-colors list (MDN
forced-colors — corrected 2026-07-09 after an audit caught the inverted claim; the research
ledger carries the dated amendment). Consequences: multi-color icons collapse to system colors
and lose color-borne distinctions — never encode meaning in fill color alone; draw glyphs in
`currentColor` so normal and forced modes share one code path; reach for
`forced-color-adjust: none` only where the literal color IS the meaning (e.g. a color swatch),
and test in forced-colors mode rather than assuming.
