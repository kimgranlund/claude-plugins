# Design-system consumption — tokens/DESIGN.md into artifact CSS

The question this file answers: **how do a DESIGN.md and/or tokens.json become the CSS an
Artifact/report page actually uses?** The contract below is the prose description of what
`make-artifact`'s bundled `css_build.py` mechanizes — the script IS the check
(script-writing-rules' mechanization test); this file explains the shape, it does not re-derive
the arithmetic.

## Two input representations, either legal

[verified against `~/Projects/adia/_shared/adia-design-system-files/design-system-for-claude-code/`,
2026-08-17 — the Adia system, this capability's first citizen]

A design system built by Ultimate Tokens ships two files that carry the SAME facts in two
different shapes:

- **`tokens.json`** — machine-consumption grammar. Colors split into two parallel top-level
  objects, `colors` (light) and `colorsDark` (dark), each keyed by role (`primary`,
  `neutral-surface`, …). Type roles live under `type.scale` (`size`/`lineHeight`/`weight`/
  optional `letterSpacing`, all bare numbers — px and unitless/em factor respectively). `spacing`
  is a flat, ordered array (`[0, 4, 8, 12, 16, 24, 32, 48, 64, 96]`). `radii` is an object
  (`none`/`xs`/`sm`/`md`/`lg`/`xl`/`full` → bare px numbers).
- **`DESIGN.md` frontmatter** — the prompt-reader grammar (Claude Design's own dialect). Colors
  are ONE flat map with `-dark`-suffixed sibling keys in the same object (`primary` /
  `primary-dark`). Typography is a nested `typography:` map keyed by role, each carrying
  `fontFamily`/`fontSize`/`fontWeight`/`lineHeight`/`letterSpacing` as CSS-flavored strings
  (`"72px"`, `"-0.02em"`). `spacing:` and `rounded:` are objects keyed by the same scale names
  tokens.json uses positionally (`none`/`xs`/`sm`/…/`5xl` and `none`/`xs`/…/`full`), values as
  px strings.

`css_build.py` accepts JSON in either shape and normalizes both into one internal role → value
model before emitting CSS — a role missing its dark counterpart in either shape is a build
failure (exit 1), never a silent light-only variable. **`tokens.json` is consumed directly** (it
is already JSON); a DESIGN.md-only invocation needs its YAML frontmatter extracted to JSON first
— a stated, mechanical, lossless step the invoking session performs (stdlib Python ships no YAML
parser, script-writing-rules' stdlib-only constraint) before handing the script its input.

## The `light-dark()` pattern — verbatim from the source's own Agent Prompt Guide

[verified: DESIGN.md's `## Agent Prompt Guide`, step 2, 2026-08-17]

```css
:root {
  color-scheme: light dark;
  --c-primary: light-dark(oklch(0.5837 0.1265 236.48), oklch(0.6716 0.1414 234.43));
  --c-primary-on-primary: light-dark(oklch(1 0 0), oklch(1 0 0));
  /* …every role, from its light + -dark pair… */
}
```

`color-scheme: light dark` on `:root` is required or the dark end of every `light-dark()` pair
never fires. A manual override is one rule per scheme, never a duplicated variable block:

```css
[data-theme="light"] { color-scheme: light; }
[data-theme="dark"]  { color-scheme: dark; }
```

**Browser support baseline** [verified, 2026-08-17]: the CSS `light-dark()` function ships in
Chrome/Edge 123+ (March 2024), Safari 17.5+, and Firefox 120+ — comfortably below the runtime
Claude Artifacts execute in, which is why this LLD rejected the `@media (prefers-color-scheme)`
double-block alternative (drift surface: every variable duplicated) in favor of the source
system's own pattern.

## Font fallback is mandatory

[incident-adjacent, 2026-08-18 finding folded into this pack]: CSP in Claude Artifacts blocks
external font files, so a bare `'GT America'` silently renders as the browser default with no
error. Every emitted font-family property therefore appends a system stack:

- Sans-serif family: `'<Family>', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Monospace family (name contains "Mono", case-insensitive): `'<Family> Mono', ui-monospace,
  'SF Mono', monospace`

`css_build.py`'s selftest asserts this holds for every emitted `--font-*` line — a fallback-less
custom font in the output is a build defect, not a style choice.

## Scale mapping

- **Type roles** → `--text-<role>-size` / `--text-<role>-weight` / `--text-<role>-lh` /
  `--text-<role>-ls` (the last only where the source states a value) — one set of four custom
  properties per scale entry, plus the deduplicated `--font-<slug>` family variables (slug =
  the family name, lowercased/hyphenated; deterministic derivation, no semantic-category
  guessing).
- **Spacing** → `--space-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`2xl`/`3xl`/`4xl`/`5xl`,
  values in px.
- **Radii** → `--r-<name>` for `none`/`xs`/`sm`/`md`/`lg`/`xl`/`full`, values in px.

## The naming grammar — `--c-{family}-{slot}`, adopted as-is

[verified: DESIGN.md's `### Token naming` section, 2026-08-17]. The family name alone is the
fill (`--c-primary`); text/icons ON a family fill are `--c-{family}-on-{family}`; states suffix
the fill (`-hover`/`-active`/`-disabled`); app surfaces live in the neutral family. This grammar
is prefix-adaptive (`--md-sys-*`, `--color-*` keep `{family}-{slot}` and swap only the prefix) —
`css_build.py` emits the `--c-` prefix by default; a consumer adopting a different host prefix
does a mechanical find/replace on the emitted custom-property names, never a re-derivation.

## The mermaid re-theme block

Every build emits a fixed CSS section overriding the rendered mermaid SVG's own inline styles
with `!important`, bound to the same `--c-*` roles as the rest of the page — see
`mermaid-style.md` for the doctrine; this file only notes that `css_build.py` is where the block
is emitted, one mechanism for both color schemes.

## The mechanized authority

The prose above describes the mapping; **`docs/skills/make-artifact/scripts/css_build.py`** IS
the check — its `selftest` mode proves every rule above against fixtures for both input
representations, with a negative control (a role missing its dark counterpart must fail) and a
reverse control (a complete fixture must emit every expected `--c-*`/`--space-*`/`--r-*` pair).
Consult that script, never hand-derive the CSS from this prose.
