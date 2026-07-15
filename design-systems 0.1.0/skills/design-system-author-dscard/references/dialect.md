# The Universal DESIGN.md Dialect + the Claude Bundle Shape

The spine of a Claude Design bundle, written so ONE file also satisfies Google
Stitch's strict parser — canonical grammar for the strict consumer costs the prompt
reader nothing. Source: derived from the Google Stitch DESIGN.md spec, version alpha
(github.com/google-labs-code/design.md, fetched 2026-07-05) and the observed Claude
Design bundle format; structural snippets quote the NONOUN "Studio 54 · the
dancefloor" reference implementation. The snapshot embedded here is authoritative at
runtime; re-derive from the upstream specs on a version bump. Companions:
`token-grammar.md` (names), `gates.md` (encoding + verification); an end-to-end
micro-example ships at `mini-bundle/` (8 roles, all four artifacts,
gates green — copy the shape, not the size). Updated 2026-07-05 with findings
from live Claude Design generation testing (two independent runs against the
Studio 54 reference bundle) — the badge/chip padding and type-floor additions
below are evidence-derived, not spec-derived; re-test if a future generation
diverges from them.

Claude Design reads three artifacts: `DESIGN.md` **as the generation prompt** (not a
parsed grammar), `tokens.json` as the structured role source, `components/*.html` as
indexed preview cards. It validates nothing — the author's gate run is the gate of
record.

## Section inventory — ten `##` sections, this order

Stitch-canonical names 1–8 (parsed, order-enforced, duplicates rejected there), then
the two prompt-reader sections (Stitch preserves them as unknown content):

| # | Section | Carries |
|---|---|---|
| 1 | Overview | brand personality, audience, THE specific reference (one named world) |
| 2 | Colors | roles + usage boundaries + refusals, the Token naming subsection, pairing law, intent doctrine |
| 3 | Typography | families by voice, weight-per-role, scale usage rules, fallback intent |
| 4 | Layout | closed spacing scale, grid, reading measure |
| 5 | Elevation & Depth | surface ladder vs shadow doctrine |
| 6 | Shapes | radius language + per-tier assignments (chips xs · inputs sm · buttons md · cards lg · modals xl) |
| 7 | Components | per-component anatomy: fill role, on-color, radius, padding, and EXPLICIT states |
| 8 | Do's and Don'ts | the hard rules and deliberate refusals |
| 9 | Responsive Behavior | breakpoints, stacking, touch minimums (≥44px), both schemes at every width |
| 10 | Agent Prompt Guide | the work-order: tokens → roles/scheme → scale → states, + the runtime CSS idiom |

Canonical names are load-bearing: "Color Palette & Roles" or "Component Stylings"
reads fine to Claude but presents unknown sections to Stitch, forfeiting its lint.
Accepted aliases: "Brand & Style"→Overview, "Layout & Spacing"→Layout,
"Elevation"→Elevation & Depth.

## Frontmatter token block

YAML frontmatter per the Stitch alpha schema (`version`, `name`, `description`,
`colors`, `typography`, `spacing`, `rounded`, `components`), with these conventions:

- **Both schemes in one map** — dark values as `-dark` suffixed siblings:
  ```yaml
  colors:
    primary-base: "oklch(0.5585 0.0245 288.45)"
    primary-base-dark: "oklch(0.6492 0.0221 288.83)"
    primary-base-on-primary-base: "oklch(1 0 89.88)"
    primary-base-on-primary-base-dark: "oklch(0.1776 0 89.88)"
  ```
  Known measured cost: `-dark` siblings lint as `orphaned-tokens` *warnings* in
  Stitch — record in the receipt, not a defect.
- **On-colors are explicit tokens** — every fill ships its `-on-{family}` partner;
  never implied, never constant across schemes without measurement.
- **States as component variants** — `button-primary-hover`, `button-primary-active`:
  states ship as values, not prose adjectives.
- **References over repeats** — component values point at roles:
  `backgroundColor: "{colors.primary-base}"`, `typography: "{typography.ui-md}"`.
- **Typography**: 9–15 voice-first levels (`heading-lg`, `body-md`, `ui-sm`); each
  level binds size AND line-height AND weight — a set-together unit, never free-typed.
  Non-standard weights (550, 440) are legitimate with variable fonts; prose names the
  fallback stack and the intent that must survive it. **The smallest consumption
  level is the type floor — never dip below it, even for compact badge/chip text**
  (live-generation evidence: an 11px badge label appeared once against a bundle
  whose floor was 12px and did not reproduce on a second run — state the floor
  explicitly rather than rely on the model inferring it).
- **Badge/chip padding is the one sanctioned exception to the spacing scale** — a
  compound value below the scale's floor (e.g. `2px 8px` for ~12–13px badge text).
  It can never be a frontmatter `padding:` token (Stitch's Dimension type holds one
  value; a pill's asymmetric padding is inherently two), so it lives only in prose
  and in the previews' literal CSS — pick one value, hardcode it everywhere. Full
  reasoning and the mechanical consistency check: `gates.md` §"Sanctioned
  exceptions", `../scripts/bundle_gates.py` G9.

## Prose doctrine — prose carries the design; tokens anchor it

- **Open the body with the prompt framing** (quote from the reference spine):
  *"Read this file as your instructions — it is the prompt. Token values are
  normative; the prose explains how to apply them. Every color role ships a light
  value and a `-dark` sibling: pick the pair, not one end."*
- **A specific reference beats adjectives.** One named world imports its negative
  space automatically; a long rambling Don't-list signals the reference was too vague.
- Every role token appears in prose with its role, usage boundary, and refusals
  ("Beam — the cyan beam. Informational accents… Never a page background.").
- **Give every signature/brand family a concrete usage example**, not just a
  boundary — otherwise two expressive families can absorb all the "small read"
  duty and a third sits defined-but-unexercised (observed 2/2: a bundle's third
  brand accent was rendered only as decorative background wash across two
  independent generations, never as an actual badge/tag, because its prose
  boundary was vaguer than its siblings').
- **Prose promises must be token deliveries** — a story the tokens can't deliver
  forces hardcoding or under-delivery (failure F2, `gates.md`). Cut a family → cut
  its prose in the same change.
- Negative constraints are first-class; state the three hard rules in Do's and
  Don'ts (never hardcode a color · never cross an on-pair · never stack competing
  primaries) and repeat the tie-break in the Agent Prompt Guide: "When rules
  conflict, the three hard rules win."

## Agent Prompt Guide — the work-order

Numbered, imperative, ending with the runtime idiom the agent must emit:

```css
:root {
  color-scheme: light dark;
  --c-primary-base: light-dark(oklch(0.5585 0.0245 288.45), oklch(0.6492 0.0221 288.83));
  /* …every role, from its light + -dark pair… */
}
```

Order: (1) tokens first — never invent a value; (2) roles, then scheme — both ends
provided, never hand-roll a dark variant; (3) scale, then states — states are where
generic output shows; (4) one primary action per view; (5) name by grammar, adapt
the prefix only. The trap to state verbatim: **`color-scheme: light dark` on `:root`
is required or the dark end of `light-dark()` never fires.**

## tokens.json — the structured carrier

Flat maps, hex payload (parser unverified — see `gates.md`): `colors` / `colorsDark`
(identical key inventories), `type.fonts` (voice → family), `type.scale`
(level → `{size, lineHeight, weight}`: size a px number, lineHeight a unitless
factor — never px, gate G8, weight a number), `spacing` (number array), `radii`
(name → px). A `$note` string records the grammar, prefix, and verification date.
Both carriers are generated from one model in the same build — never hand-synced.

## Previews — `components/*.html` @dsCard cards

First line is the index marker; the file must render standalone:

```html
<!-- @dsCard group="Components" title="Content card" subtitle="surface · elevation · actions" -->
<style>:root{color-scheme:light dark;--c-primary-base:light-dark(oklch(…), oklch(…));…}</style>
<div class="cd">…markup binding ONLY var(--c-…) custom properties…</div>
```

Rules: one `:root` block with `color-scheme: light dark` + `light-dark(oklch, oklch)`
per role — no `prefers-color-scheme` media-query fork; no external fetches (fonts via
local stacks: `'Inter', system-ui, …`); cards demonstrate **states, the pairing law,
and the scale** — a resting-state-only card under-teaches the model that imitates it.
Typical set: buttons, inputs, card, feedback/badges, colors, typography, spacing.

## README.md — the profile receipt

Regenerated every build, never hand-edited into a second source of truth. Records:
contents line; naming standard (grammar, prefix, families); encoding standard (OKLCH
frontmatter, hex tokens.json, light-dark runtime); one line per gate with its measured
result ("all pairs ≥ 4.5:1 both schemes", "max dev 1/255", role count × 2 schemes);
every DIVERGENCE and alias, called out, dated.

**Leading & tracking are always relative (standing rule).** Express line-height as a unitless factor (`1.5`), em (`1.5em`), or `%`; letter-spacing as em or `%` — never absolute px in any carrier (frontmatter, tokens.json, tables, CSS). Stitch's own spec recommends the unitless multiplier. Gated mechanically: `bundle_gates.py` G8 — every platform sibling's checker now gates this (Stitch prelint, Make D11).
