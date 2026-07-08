# Stitch DESIGN.md — Derived Platform Ground Truth

**Derived, not owned.** Source of record: `github.com/google-labs-code/design.md` — `docs/spec.md` (format), `README.md` (CLI + linting rules), `PHILOSOPHY.md` — spec version **alpha**, fetched 2026-07-05. On conflict, the upstream repo wins; re-derive this file whenever the version string moves past `alpha`. Measured probe results (marked *measured*) come from running `npx @google/design.md lint` on real files, 2026-07-05.

## 1. File anatomy

One self-contained file, two layers:

1. **YAML frontmatter** (optional) — machine-readable design tokens between `---` fences at the top of the file.
2. **Markdown body** — human-readable rationale in `##` sections.

"The tokens are the normative values; the prose provides context for how to apply them" (spec.md). Prose may use descriptive color names ("Midnight Forest Green") that correspond to systematic token names (`primary`). An `#` H1 is allowed for titling and is not parsed as a section.

## 2. Frontmatter schema (alpha)

```yaml
version: <string>          # optional, current version: "alpha"
name: <string>
description: <string>      # optional
colors:
  <token-name>: <Color>
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <token-name>: <string | token reference>
```

`<scale-level>` is any descriptive string key; `xs`/`sm`/`md`/`lg`/`xl`/`full` are common.

### Types

- **Color** — any valid CSS color string: hex (`#RGB[A]`, `#RRGGBB[AA]`), named, functional (`rgb()`, `hsl()`, `hwb()`), wide-gamut (`oklch()`, `oklab()`, `lch()`, `lab()`), `color-mix(in srgb, …)`. All values convert internally to sRGB for WCAG contrast checking; the original format is preserved for display/export. Upstream recommends hex as default; *measured*: `oklch(L C H / A)` values are parsed and contrast-checked, so OKLCH is a verified-safe payload. *Measured*: `light-dark(<L>, <D>)` is rejected as an **error** ("not a valid color") — never place it in a token value.
- **Dimension** — number + unit; valid units `px`, `em`, `rem` (negative values legal, e.g. `-0.02em`).
- **Typography** — object: `fontFamily` (string) · `fontSize` (Dimension) · `fontWeight` (number; bare or quoted) · `lineHeight` (Dimension *or* unitless multiplier of fontSize — the multiplier is the recommended CSS practice) · `letterSpacing` (Dimension) · `fontFeature` (string → `font-feature-settings`) · `fontVariation` (string → `font-variation-settings`).
- **Token reference** — `{path.to.token}` wrapped in curly braces, an object path into the YAML tree. Outside `components`, a reference must point at a *primitive* value (`colors.primary-60`), never a group. Inside `components`, composite references (`{typography.label-md}`) are permitted.

### Component tokens

`components` is `map<name, map<property, value|reference>>`. **Variants are related keys**, not nested state objects: `button-primary`, `button-primary-hover`, `button-primary-active` — "the agent will consider all variants and make the appropriate styling decisions" (spec.md). Valid component properties (the property-token registry):

`backgroundColor` · `textColor` · `typography` · `rounded` · `padding` · `size` · `height` · `width`

An unknown property (e.g. `borderColor`) is accepted **with a warning** — see §5. The components spec is flagged "actively evolving"; domain-specific component names are encouraged.

## 3. Body sections — canonical order and aliases

Sections use `##` headings. Any section may be omitted; those present must appear in this order:

| # | Section | Alias |
|---|---|---|
| 1 | Overview | Brand & Style |
| 2 | Colors | — |
| 3 | Typography | — |
| 4 | Layout | Layout & Spacing |
| 5 | Elevation & Depth | Elevation |
| 6 | Shapes | — |
| 7 | Components | — |
| 8 | Do's and Don'ts | — |

Spec norms per section worth holding: Colors — "at least the `primary` color palette must be defined"; conventional palette order `primary`, `secondary`, `tertiary`, `neutral`. Typography — "most design systems have 9–15 typography levels", semantic categories (`headline`, `display`, `body`, `label`, `caption`) × sizes. Recommended (non-normative) token names: colors `primary`/`secondary`/`tertiary`/`neutral`/`surface`/`on-surface`/`error`; typography `headline-display`…`label-sm`; rounded `none`/`sm`/`md`/`lg`/`xl`/`full`.

## 4. Unknown-content tolerance (the load-bearing table)

Consumer behavior when content is outside the spec (spec.md, verbatim semantics):

| Scenario | Behavior | Example |
|---|---|---|
| Unknown section heading | **Preserve; do not error** | `## Iconography` |
| Unknown color token name | **Accept if value is valid** | `surface-container-high: '#ede7dd'` |
| Unknown typography token name | Accept as valid typography | `telemetry-data` |
| Unknown spacing value | Accept; store as string if not a valid dimension | `grid-columns: '5'` |
| Unknown component property | Accept **with warning** | `borderColor` |
| Duplicate section heading | **Error; reject the file** | two `## Colors` headings |

This table is what makes the single-file superset strategy viable: `-dark` scheme siblings ride the accept-if-valid rule; appended sections (Responsive Behavior, Agent Prompt Guide, Motion) ride the unknown-section rule; custom top-level token groups (e.g. `motion:`) stay silent under `unknown-key` (typo-likeness only triggers the warning). The philosophy doc makes the stance explicit: "the format accepts any key, any section, any structure your design system needs" — the format grows through its users, not its spec.

## 5. The nine lint rules (README.md, fetched 2026-07-05)

`npx @google/design.md lint` runs nine rules; each emits findings at a fixed severity. Exit code `1` on **errors only**, `0` otherwise.

| Rule | Severity | What it checks |
|---|---|---|
| `broken-ref` | **error** | `{path.to.token}` references that resolve to no defined token |
| `missing-primary` | warning | Colors defined but no `primary` — "agents will auto-generate one" |
| `contrast-ratio` | warning | Component `backgroundColor`/`textColor` pairs below WCAG AA 4.5:1 |
| `orphaned-tokens` | warning | Color tokens defined but never referenced by any component |
| `missing-typography` | warning | Colors defined but no typography tokens — agents will use default fonts |
| `section-order` | warning | Sections out of the canonical order |
| `unknown-key` | warning | A top-level YAML key that looks like a typo of a schema key (`colours:` → `colors:`); genuine extension keys stay silent |
| `token-summary` | info | Count of tokens per section |
| `missing-sections` | info | Optional token groups (spacing, rounded) absent while other tokens exist |

Notes that matter in practice: `broken-ref` is the *only* error-severity rule, but a duplicate `##` heading rejects the file at parse (§4) and an invalid color value (`light-dark()`, *measured*) errors before rules run. `contrast-ratio` sees **only** component `backgroundColor`/`textColor` pairs, and only the values as written — with `-dark` siblings, that means the light end; the dark scheme is never contrast-checked by Stitch. `orphaned-tokens` counts only *component* references — a token referenced solely in prose still counts as orphaned.

## 6. CLI reference (the subset that matters here)

```bash
npx -y @google/design.md lint DESIGN.md            # JSON findings; exit 1 on errors only
npx -y @google/design.md diff BEFORE.md AFTER.md   # token-level changes; exit 1 on regression
npx -y @google/design.md export --format dtcg DESIGN.md          # → W3C DTCG tokens.json
npx -y @google/design.md export --format css-tailwind DESIGN.md  # → Tailwind v4 @theme block
npx -y @google/design.md spec --rules              # print the spec + active lint-rule table
```

- All commands accept a file path or `-` for stdin; output defaults to JSON.
- `export` exits 0 regardless of lint findings — run `lint` to gate; exit 1 = bad `--format`/emitter error, exit 2 = unreadable input.
- **Windows**: the `.md` suffix in the bin name collides with the Markdown file association; use the alias — `npx -p @google/design.md designmd lint DESIGN.md`. `ENOVERSIONS` on install means npm isn't hitting the public registry (`npm config get registry` should print `https://registry.npmjs.org/`).
- Programmatic: `import { lint } from '@google/design.md/linter'` → `{ findings, summary, designSystem }`.

## 7. Philosophy (PHILOSOPHY.md — binds the prose layer)

- "The prose is where the design lives. Everything else in the document exists to support it." "The quality of a generated design is determined less by the precision of its values than by how clearly the intent is described."
- **Tokens are context, not instruction**: "the token values serve as context and are not rendering instructions" — the spec deliberately refuses token *requirements*.
- **A specific reference beats adjectives**: "a 1970s graduate lecture handout in the tradition of an old and established university" evokes a complete world; "modern, clean, trustworthy, premium" describes a region and yields the generic center of it. Adjectives describe a region; a reference describes a point.
- **Negative constraints arrive free** with a specific reference ("naming the object names them, the same way naming a dog tells the model that dogs don't meow"). A long rambling don't-list signals the reference was too vague; "a strong reference and an intentional list of do's and don'ts working together is the sweet spot."
- **Growth by tolerance**: motion, iconography, elevation physics, casing — extra sections + free-form token groups, no spec change needed, because tokens are context rather than instruction.
