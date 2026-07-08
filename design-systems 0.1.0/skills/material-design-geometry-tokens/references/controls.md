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
| caret | `--md-sys-size-{step}-caret` | the affordance mark (dropdown ▾) | 14px |
| font | `--md-sys-size-{step}-font` | the control's text size (composed from the UI type voice) | 14px |
| gap | `--md-sys-size-{step}-gap` | icon↔label gap INSIDE the control | 7px |
| pad | `--md-sys-size-{step}-pad` | inline edge padding for a control WITH a leading slot/icon | 5px |
| pad-edge | `--md-sys-size-{step}-pad-edge` | inline edge padding for a SLOTLESS (bare text) control | 14px |
| min | `--md-sys-size-{step}-min` | the 1:1 floor — an icon-only control is at least square | 28px |
| radius | `--md-sys-size-{step}-radius` | the control's own corner (its height-linked pill radius) | 14px |

**The law:** edge padding = (height − glyph)/2, so a glyph sits optically centered in the height² cell.
Note `--md-sys-size-md-radius` = 14 = height/2 — every control is already a full pill. If you set a
control's padding independently of its height you break centering — always use the paired
`--md-sys-size-{step}-pad` / `-pad-edge`.

## Recipes

**Button (text + optional icon)** — box: `.md-sys-control-md`, OR by hand:
```css
.btn {
  box-sizing: border-box;
  block-size: var(--md-sys-size-md-height);
  min-inline-size: var(--md-sys-size-md-min);
  padding-inline: var(--md-sys-size-md-pad-edge);   /* slotless: bare text */
  padding-block: 0;
  gap: var(--md-sys-size-md-gap);
  border-radius: var(--md-sys-size-md-radius);       /* = height/2, a pill */
  font-size: var(--md-sys-size-md-font);
}
```
Text: the box above already set `font-size` from `--md-sys-size-md-font` — which **is** the UI voice's
size at this step (`--md-sys-size-{step}-font` ≡ `--md-sys-typescale-ui-{step}-size`, so the box and its
text share one number). Add only the label's character from the UI voice VARS —
`font-family: var(--font-ui)`, `font-weight: var(--md-sys-typescale-ui-md-weight)`,
`letter-spacing: var(--md-sys-typescale-ui-md-tracking)` — **never** its `-size` or the whole
`.md-sys-typescale-ui-md` class (that re-sets `font-size` and a multi-line `-line` against the control box).

- **With a leading icon:** icon `--md-sys-size-md-icon` (18px), and swap the padding to
  `--md-sys-size-md-pad` (the slot edge, 5px) instead of `-pad-edge`.
- **Icon-only:** `inline-size: var(--md-sys-size-md-min)` (square, 28px), padding `--md-sys-size-md-pad`.
- **Dropdown / select:** append a caret at `--md-sys-size-md-caret` (14px).

**Input / select field** — `block-size: var(--md-sys-size-md-height)`, `padding-inline:
var(--md-sys-size-md-pad-edge)`, border `--md-sys-border-thin` (color from the color skill), radius
`--md-sys-size-md-radius`. The value text is `--md-sys-size-md-font`.

**Toggle / checkbox / radio** — the box tracks a small step (`--md-sys-size-sm-*` or `-xs-*`); the
control's `min` keeps it square.

## Don't

- Don't hardcode a control height (`height: 40px`) — pick a step.
- Don't set padding that isn't `--md-sys-size-{step}-pad` / `-pad-edge` — you'll un-center the glyph.
- Don't put `--md-sys-radius-md` on a control that should scale — use `--md-sys-size-{step}-radius` (it's
  already a pill), or `--md-sys-radius-full` for an explicitly round non-control.
- Don't mix steps within one control — height, icon, font, and pad must all be the same `{step}`.
