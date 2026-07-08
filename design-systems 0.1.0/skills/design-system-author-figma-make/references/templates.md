# Templates — file by file, with worked-example snippets

Each template: the skeleton to fill, then a snippet quoted from the reference
implementation ("Studio 54 · the dancefloor", NONOUN Ultimate Tokens build,
2026-07-05 — the worked example that passes every gate). Substitute your theme's
character, prefix, families, and values; keep the shapes.

## 1. Guidelines.md — entry: character → routing → hard rules → workflow

```markdown
# {Theme name} — Guidelines

You are building UI for **{theme}**: {2–4 sentences of SPECIFIC reference — a named
world, its materials and light — ending with the design stance}.

## Reading order
| Question | Read |
|---|---|
| Which color/token do I use? | `foundations/color.md` |
| Which type level? | `foundations/typography.md` |
| Which gap, padding, radius? | `foundations/spacing.md` |
| Which component and variant? | `components/overview.md`, then the component file |

## Hard rules — IMPORTANT
- Do NOT hardcode a color. Every color is a `--{prefix}-*` role from `foundations/color.md`.
- Do NOT put text on a fill in anything other than that fill's own on-token.
- Do NOT invent dark-mode values. Every role ships a light and a dark value; use the pair.
- Do NOT free-type font sizes, gaps, or radii. Compose from the scales.
- {theme-specific prohibitions — usage boundaries for signature colors}

## Workflow
1. Tokens first — take every value from the foundations files.
2. Pick roles, not colors; both schemes come with the role.
3. Set type, spacing, and radius from the scales.
4. Add the interactive states from the component files.
```

Worked character paragraph (note: a named world, not adjectives):

> You are building UI for **Studio 54 · the dancefloor**: a glittering 1970s nightclub —
> mirror-ball silver, gold lamé, and hot pink-purple light playing over a deep
> black-purple dancefloor. The interface is the club: calm dark-capable surfaces carry
> the room; color arrives as *light* — pink wash, purple and cyan beams, silver
> reflection. Restraint over decoration. Disco is glamour, not kitsch.

Routing rule: the table must name **every** leaf that exists (the checker fails an
unrouted leaf), routed by *question*, not by filename list.

## 2. foundations/color.md — grammar → tables → tree → rules → runtime block

Section order matters: the naming grammar comes first (Make constructs names by
pattern), tables carry the facts, the decision tree routes, the runtime block ships.

### 2a. Naming grammar section (Ultimate Tokens)

Every color token is constructed, never invented: **`--{prefix}-{family}-{slot}`**.
State the prefix once; keep `{family}-{slot}` intact under any prefix. Worked snippet:

> Every token is `--{prefix}-{family}-{slot}`; this project's prefix is `c`. Families:
> `primary-base` (neutral-purple room), `primary-muted` (hot pink), `secondary-base`
> (gold), `secondary-muted` (silver), `accent-base` (electric purple), `accent-muted`
> (cyan), `danger`, `success`, `warning`. Construct names — do not invent them:
> - Family alone = the fill: `--c-primary-base`, `--c-danger`.
> - Text/icons ON a fill: `--c-{family}-on-{family}`.
> - States: `-hover`, `-active`, `-disabled` suffix the fill.
> - App surfaces live in the neutral family: `--c-primary-base-background`, `-surface`,
>   `-surface-high`; text on them `-on-surface` / `-on-surface-variant`; hairlines
>   `-outline-variant`.
> - Prefix-adaptive: under `--md-sys-*` or `--color-*`, keep `{family}-{slot}` intact
>   and swap only the prefix. Richer sheets add slots (`-container`, `-scrim-*`,
>   `-surface-lowest…-highest`, `-placeholder`) on the same pattern.

Slot budget (the consumption reduction is a slot *subset*, not a new vocabulary):
~10 slots on the neutral-duty family (`background`, `surface`, `surface-high`,
`on-surface`, `on-surface-variant`, `outline-variant`, base, `hover`, `active`,
`on-{family}`) + 2 per accent/intent family (base, `on-{family}`). 15–25 roles total.

### 2b. Token tables — three tables, fixed column shapes

The checker parses these shapes; keep them. Surfaces & text (2 color columns):

```markdown
| Token | Light | Dark | Use for |
|---|---|---|---|
| `--c-primary-base-background` | `oklch(0.9554 0.0013 286.37)` | `oklch(0.2354 0.0019 286.25)` | the app canvas — lowest surface |
| `--c-primary-base-on-surface` | `oklch(0.1776 0 89.88)` | `oklch(1 0 89.88)` | primary text and icons on surfaces |
```

Actions & brand, and Intents (4 color columns — fill L/D + Foreground L/D; the
foreground cell is `{light fg}` / `{dark fg}`):

```markdown
| Token | Light | Dark | Foreground (L/D) | Use for |
|---|---|---|---|---|
| `--c-primary-base` | `oklch(0.5585 0.0245 288.45)` | `oklch(0.6492 0.0221 288.83)` | `oklch(1 0 89.88)` / `oklch(0.1776 0 89.88)` | THE action per view: CTA, link, selection |
```

Every "Use for" cell is a usage *boundary*, not a synonym — signature colors carry
their refusals ("hot-pink wash — featured/live markers only").

### 2c. "Which token?" decision tree (ASCII, one per token file)

```
Is it a page/panel background?
├─ yes → background / surface / surface-high (elevation = one ladder step up)
└─ no → Is it text or an icon?
   ├─ on a plain surface → -on-surface (primary) or -on-surface-variant (secondary)
   └─ on a colored fill  → that fill's --c-{family}-on-{family}. Always.
      Is it the view's ONE decisive action? → primary
      Status (error/saved/caution)?         → danger / success / warning
      {…one line per remaining family, ending in its role}
```

### 2d. Rules — IMPORTANT (per-file prohibitions)

> - Do NOT cross an on-pair (e.g. white text on `--c-secondary-muted`). The pair is
>   the contract; crossing it fails contrast in one scheme.
> - Do NOT use intent colors decoratively. `danger` means destructive/error — never
>   an ordinary red button.

### 2e. Runtime block — paste-ready, the trap named in prose

```css
:root {
  color-scheme: light dark;
  --c-primary-base-background: light-dark(oklch(0.9554 0.0013 286.37), oklch(0.2354 0.0019 286.25));
  --c-primary-base: light-dark(oklch(0.5585 0.0245 288.45), oklch(0.6492 0.0221 288.83));
  --c-primary-base-on-primary-base: light-dark(oklch(1 0 89.88), oklch(0.1776 0 89.88));
  /* …one line per role, every role in the tables, nothing extra */
}
```

Precede it with the trap sentence, verbatim intent: "`color-scheme` on `:root` is
required — without it the dark end never fires." The block is the carrier-equality
surface: the checker compares these declarations against a sibling export.

## 3. foundations/typography.md — levels as set-together units

```markdown
| Level | Family | Size px / Leading × | Weight | Use for |
|---|---|---|---|---|
| `body-md` | Inter | 16 / 1.5 | 500 | primary reading text — the floor for content |
| `ui-md` | Inter | 14 / 1.429 | 550 | buttons, inputs, menus |
```

9–15 levels, voice-first names (`heading-lg`, `body-md`, `ui-sm`); each binds size AND
line-height AND weight — "Do NOT free-type a size or pair a level with a different
line-height." Name the fallback stack and the intent that must survive fallback.
Non-standard weights (550, 440) are legitimate with variable fonts.

**Leading & tracking are always relative (standing rule).** Express line-height as a
unitless factor (`1.5`), em (`1.5em`), or `%`; letter-spacing as em or `%` — never
absolute px in any carrier (frontmatter, tokens.json, tables, CSS). Make's own
composite type-class example writes leading unitless — `text-title` (24px, 600,
**1.4**) — see `format.md`.

## 4. foundations/spacing.md — closed scales

Spacing steps table (px + typical use; "a 7px or 13px gap does not exist in this
system"), radius ladder with per-tier assignments (chips `xs`, inputs `sm`, buttons
`md`, cards `lg`, modals `xl`), then 3–4 layout rules (measure, stacking breakpoint,
touch minimum, elevation = surface step not shadow).

## 5. components/overview.md — the second router

Catalog table (Component | Alt names | Purpose | Guidelines file) + a variant decision
tree. Components without a dedicated leaf yet get a one-line token recipe under
"Shared patterns (until a dedicated file exists)" — never a bare mention. Worked tree:

```
Is it THE action of the view?          → Button primary
Is it a supporting action?             → Button secondary
Is it destructive?                     → Button danger (confirm patterns apply)
Is it metadata?                        → Chip secondary-muted (mirror)
Is it a status?                        → Badge danger / success / warning
```

## 6. components/{component}.md — one leaf per component

Sections: When to use → Variants (closed set) → Anatomy → States → Correct vs
incorrect → Rules. The two load-bearing shapes:

**Closed variant set** — "Valid variants are `primary`, `secondary`, `danger` —
nothing else. Do NOT invent `ghost`, `outline`, or `link` variants."

**States as literal per-scheme values:**

```markdown
| Variant | State | Light fill | Dark fill | Label (L/D) |
|---|---|---|---|---|
| primary | rest | `oklch(0.5585 0.0245 288.45)` | `oklch(0.6492 0.0221 288.83)` | `oklch(1 0 89.88)` / `oklch(0.1776 0 89.88)` |
| primary | hover | `oklch(0.4689 0.0176 289.88)` | `oklch(0.7362 0.0171 289.81)` | unchanged |
```

Plus focus (ring token + width + offset) and disabled (mechanism, e.g. "45% opacity,
pointer removed. Do NOT recolor to gray."). Correct-vs-incorrect pair, worked:

```html
<!-- Correct: family fill + its own on-token -->
<button style="background:var(--c-primary-base);color:var(--c-primary-base-on-primary-base)">Book a table</button>

<!-- Incorrect: hardcoded color, crossed pair -->
<button style="background:#8E8D9C;color:#FFFFFF">Book a table</button>
```

## 7. setup.md — only when a code package ships

CSS import order, provider wiring, build prohibitions (e.g. "Do NOT extend the
Tailwind config with raw colors"). Omit the file entirely when the kit ships no code
package — record the omission in the receipt ("intentionally absent").
