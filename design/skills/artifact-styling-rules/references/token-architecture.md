# Token architecture — the role-alias method

The question this file answers: **how does a consuming project's own design-system tokens become
the CSS custom properties an Artifact page actually uses?** The answer is a method, not a script —
`docs:artifact-rules`' `script-interface.md` owns the mechanical `css_build.py` contract this
doctrine describes the shape of.

## Role-alias, never a re-ramp

**[verified, reference impl `artifact-adiaui.tokens.json`, 2026-08-18]** An artifact's colors are
**aliases over the consuming project's own already-resolved semantic roles** — never a fresh ramp
built from raw scale stops. The reference implementation's own `_meta.description` states this
verbatim: *"Colors flow from the design system; geometry and type flow from the artifact
doctrine."* Concretely: the artifact never picks "primary-600" off a numeric ramp and decides for
itself what it means — it takes the project's own resolved `--md-sys-color-primary` (or
equivalent) value and aliases it to `--accent`. This is why `token-architecture.md`'s inventory
below is a table of ROLES, not a table of ramp stops.

## Build-time `light-dark()` + `color-scheme`, not a media-query double-block

**[verified, source DESIGN.md's own Agent Prompt Guide, cited via `docs/skills/artifact-rules`'
prior verification, 2026-08-17]**

```css
:root {
  color-scheme: light dark;
  --c-primary: light-dark(oklch(0.5837 0.1265 236.48), oklch(0.6716 0.1414 234.43));
}
[data-theme="light"] { color-scheme: light; }
[data-theme="dark"]  { color-scheme: dark; }
```

Every role emits ONE `light-dark(<light-value>, <dark-value>)` pair under `:root`, resolved
automatically by the tri-state described in `platform-facts.md`. This retires the
`@media (prefers-color-scheme)` triple-block pattern (one block for light, one for dark, one for
the override) — the double-block duplicates every variable and buys nothing `light-dark()` doesn't
already give for free. Browser support ([verified] Chrome/Edge 123+, Safari 17.5+, Firefox 120+,
March 2024) is comfortably below the Artifacts runtime.

## The artifact token inventory — 14 live roles + a tier-2 reserve

**[verified, reference impl `artifact-adiaui.tokens.json`'s `role-mapping` object, 2026-08-18]**
the live-bound roles, each a `{role, resolved}` pair (the `resolved` value already a complete
`light-dark(...)` CSS function):

| Custom property | Aliases | Purpose |
|---|---|---|
| `--paper` | `neutral-background` | page ground (the body-ground rule) |
| `--card` | `neutral-surface` | canvas-2 equivalent container |
| `--chip` | `neutral-surface-high` | canvas-3 equivalent, small enclosed elements |
| `--card-low` | `neutral-surface-low` | a dimmer container tier |
| `--ink` | `neutral-on-surface` | primary text |
| `--muted` | `neutral-on-surface-variant` | secondary text |
| `--fine` | `neutral-placeholder` | placeholder/tertiary text |
| `--line` / `--line-strong` | `neutral-outline-variant` / `-outline` | hairline / emphasis borders |
| `--accent` (+`-hover`/`-soft`) | `primary` family | the one-accent doctrine's single accent |
| `--on-accent` | `primary-on-primary` | text/icons on the accent fill |
| `--tertiary` | `tertiary` | diagram/data-distinction hue only |
| `--danger`/`--success`/`--warning`/`--info` (+`-soft` each) | intent families | status/callout roles |
| `--on-intent` | intent on-color | text on any intent fill |
| `--mono-bg` | alias of `--chip` | monospace/code block background |

**Tier-2, reserved not yet bound** (`_unbound`, [verified] same source): `secondary` (the
one-accent doctrine deliberately leaves it unmapped), `-active`/`-disabled`/outline-state ladders
(static pages need hover only), dialog-backdrop + scrims (reserved for future overlay work). A
styling choice needing one of these is a named gap, never an ad-hoc invented color — this is
Rubric R2's "tier-2 roles are never silently invented" gate.

## Colors-from-system, geometry/type-from-doctrine — the split, stated

**[verified, reference impl `_integration` block, 2026-08-18]** `"themes+type": "NOT integrated:
frozen projection, not live ramp binding; faces owned by the artifact type doctrine"` — colors
bind LIVE to whichever project's design system is consuming this doctrine; radius resolution and
type faces are the artifact's OWN fixed doctrine (`type-and-layout.md`), applied regardless of
what the source system's own fonts/radii happen to be, unless the source system explicitly states
an override. Two different sources of truth, on purpose: a project's brand colors should show
through; its font-of-the-week should not silently override the artifact's own reading-optimized
type stack.

## Comparison point: the jcmrs community token convention

**[verified, jcmrs/claude-visual-style-guide, accessed 2026-08-18]** A community-authored
alternative encodes the same role-alias IDEA differently: a flat JSON of semantic tokens
(`background`/`foreground`/`primary`/`muted`/`destructive`, etc.), each carrying separate `light`
and `dark` VALUES (not a single `light-dark()` pair), switched by toggling a `dark` CSS class on
the document root (`documentElement.classList.toggle('dark')`) rather than a `[data-theme]`
attribute + `color-scheme`. The naming grammar is compatible in spirit (purpose-driven role names
mapped to both a fill and an on-fill class, e.g. `primary` → `bg-primary`/`text-primary` — the
same shape this pack's `--c-{family}-on-{family}` grammar already uses) — this pack does NOT adopt
the class-toggle mechanism, since `light-dark()` + `color-scheme` already covers the tri-state
(`platform-facts.md`) with zero JS and one variable block, where a class-toggle needs a script to
flip it and still needs the tri-state's third (unstamped) state handled separately.

## The naming grammar — `--c-{family}-{slot}`

Family name alone is the fill (`--c-primary`); text/icons ON a family fill are
`--c-{family}-on-{family}`; states suffix the fill (`-hover`/`-active`/`-disabled`); app surfaces
live in the neutral family. Prefix-adaptive — a consumer using a different host prefix
(`--md-sys-*`, `--color-*`) does a mechanical find/replace on the emitted names, never a
re-derivation.

## The role-mapping file shape — the mechanized authority

The prose above describes the SHAPE; `docs:artifact-rules`' `script-interface.md` names the exact
`css_build.py` contract that mechanizes it, citing the same reference implementation
(`artifact-adiaui.tokens.json`) as its own input-shape fixture. Consult that file for the script's
CLI/exit contract; consult this file for why the mapping looks the way it does.

Extension: governed by [[make-pack]].
