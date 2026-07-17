# Controls — heights, the centering law, paddings, radius

A control is ONE size step; everything inside it derives from the height. Use the
`.md-sys-control-{step}` class for the box, or compose the `--md-sys-size-{step}-*` vars when you need
the parts.

## The size ramp — pick a step by density

ADIA ships six steps. Read the actual heights from the export; this kit's are:

| Step | Height | Typical use |
|---|---|---|
| `xs`  | 20px | dense toolbars, table-row controls, compact chips |
| `sm`  | 24px | secondary buttons, filter bars, inline controls |
| `md`  | 28px | the default button / input / select — the **baseHeight**, start here |
| `lg`  | 36px | primary CTAs, prominent form fields |
| `xl`  | 48px | hero actions, touch-first controls |
| `2xl` | 64px | oversized / marketing controls |

The step is a density choice; the same control is `md` in a dense admin and `lg` in a touch app.
Pick per context, then everything inside follows.

## What derives from the height (the centering law)

For a chosen `{step}` (values shown for `md` = the 28px baseHeight):

| Field | Var | What it is | `md` |
|---|---|---|---|
| height | `--md-sys-size-{step}-height` | the control's block-size | 28px |
| icon | `--md-sys-size-{step}-icon` | leading content-icon / slot glyph size | 18px |
| caret | `--md-sys-size-{step}-caret` | the affordance mark (dropdown ▾) — its own sublinear height law, gentler than the text's | 13px |
| font | `--md-sys-size-{step}-font` | the control's text size — composed from the `ui-control` type voice at EVERY step (`xs`..`2xl`; the voice rides the full 6-level ramp since 2026-07-16 — the old partial `label`-voice composition is retired) | 15px |
| gap | `--md-sys-size-{step}-gap` | icon↔label gap INSIDE the control — a hand-CALIBRATED unit per step (not a font fraction), scaled by baseHeight and the density knob | 4px |
| padding-narrow | `--md-sys-size-{step}-padding-narrow` | inline edge padding for a control WITH a leading slot/icon — the SLOT edge, keyed on the icon glyph | 5px |
| padding-wide | `--md-sys-size-{step}-padding-wide` | inline edge padding for a SLOTLESS (bare text) control — the bare/caret edge, keyed on the caret glyph | 7.5px |
| padding-narrow-compact | `--md-sys-size-{step}-padding-narrow-compact` | the slot edge with the control's own gap absorbed — for dense layouts | 3px |
| padding-wide-compact | `--md-sys-size-{step}-padding-wide-compact` | the bare/caret edge with the control's own gap absorbed — for dense layouts | 5.5px |
| min | `--md-sys-size-{step}-min` | the 1:1 floor — an icon-only control is at least square | 28px |
| radius | `--md-sys-size-{step}-radius` | the control's own corner (its height-linked pill radius) | 14px |

**The law:** edge padding = (height − glyph)/2, so a glyph sits optically centered in the height² cell —
`padding-narrow` keys this off the icon glyph, `padding-wide` off the caret glyph (the bare/caret edge —
formerly a flat height/2, now tighter: `md` 14px → 7.5px). The `-compact` twins subtract the control's own
gap first, for dense layouts. Half-pixel results (7.5px, 5.5px) are EXACT by design, never rounded.
Note `--md-sys-size-md-radius` = 14 = height/2 — every control is already a full pill. If you set a
control's padding independently of its height you break centering — always use the paired
`--md-sys-size-{step}-padding-narrow` / `-padding-wide` (or their `-compact` twins).

## Recipes

**Button (text + optional icon)** — box: `.md-sys-control-md`, OR by hand:
```css
.btn {
  box-sizing: border-box;
  block-size: var(--md-sys-size-md-height);
  min-inline-size: var(--md-sys-size-md-min);
  padding-inline: var(--md-sys-size-md-padding-wide);   /* slotless: bare/caret edge */
  padding-block: 0;
  gap: var(--md-sys-size-md-gap);
  border-radius: var(--md-sys-size-md-radius);       /* = height/2, a pill */
  font-size: var(--md-sys-size-md-font);
}
```
Text: the box above already set `font-size` from `--md-sys-size-md-font` — at `md` this **is** the
`ui-control` voice's own size (`--md-sys-size-md-font` ≡ `--md-sys-typescale-ui-control-md-size`, so
the box and its text share one number; since 2026-07-16 this equality holds at EVERY step, `xs`..`2xl` —
the `ui-control` voice rides the full 6-level ramp, and the old partial `label`-voice composition is
retired). Add only the text's character from the `ui-control` voice VARS —
`font-family: var(--font-ui)`, `font-weight: var(--md-sys-typescale-ui-control-md-weight)`,
`letter-spacing: var(--md-sys-typescale-ui-control-md-tracking)` — **never** its `-size` or the whole
`.md-sys-typescale-ui-control-md` class (that re-sets `font-size` and a multi-line `-line` against the
control box; the single-line fit is `--md-sys-typescale-ui-control-md-line-single`).

- **With a leading icon:** icon `--md-sys-size-md-icon` (18px), and swap the padding to
  `--md-sys-size-md-padding-narrow` (the slot edge, 5px) instead of `-padding-wide`.
- **Icon-only:** `inline-size: var(--md-sys-size-md-min)` (square, 28px), padding `--md-sys-size-md-padding-narrow`.
- **Dropdown / select:** append a caret at `--md-sys-size-md-caret` (13px).
- **Dense / compact layout:** swap either padding for its `-compact` twin (`--md-sys-size-md-padding-narrow-compact`
  = 3px, `--md-sys-size-md-padding-wide-compact` = 5.5px) — the same edge with the control's own gap
  already absorbed.

**Input / select field** — `block-size: var(--md-sys-size-md-height)`, `padding-inline:
var(--md-sys-size-md-padding-wide)`, border `--md-sys-border-thin` (color from the color skill), radius
`--md-sys-size-md-radius`. The value text is `--md-sys-size-md-font`.

**Toggle / checkbox / radio** — the box tracks a small step (`--md-sys-size-sm-*` or `-xs-*`); the
control's `min` keeps it square.

## Don't

- Don't hardcode a control height (`height: 40px`) — pick a step.
- Don't set padding that isn't `--md-sys-size-{step}-padding-narrow` / `-padding-wide` (or their
  `-compact` twins) — you'll un-center the glyph.
- Don't put `--md-sys-radius-md` on a control that should scale — use `--md-sys-size-{step}-radius` (it's
  already a pill), or `--md-sys-radius-full` for an explicitly round non-control.
- Don't mix steps within one control — height, icon, font, and pads must all be the same `{step}`.
