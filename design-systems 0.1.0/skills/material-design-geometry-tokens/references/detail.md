# Icons, hit targets, focus rings, density

## Icon sizes

An icon INSIDE a control uses that control's `--md-sys-size-{step}-icon` — never an independent size, or
it won't center. A standalone / decorative icon picks the `--md-sys-size-{step}-icon` of the step whose
scale it visually matches (an icon beside `md` text → `--md-sys-size-md-icon`). Per-step icon values live
in the [`controls.md`](controls.md) ramp table (the canonical numbers); icon color is the color skill
(icons inherit their text partner's role).

## Hit targets & minimum size

`--md-sys-size-{step}-min` is the 1:1 floor — an icon-only control is at least square (height × height);
the per-step floors ARE the heights (see the [`controls.md`](controls.md) ramp table). The platform touch
hit-target floor is ≈44px, but that's the HIT AREA, not the visible box: a compact control (e.g. `sm`=24px)
can still meet 44px by EXTENDING its target past its paint — inline padding, a `::before` overlay, or a
larger tap wrapper — while staying visually small. So EITHER size the visible control up (`xl`=48 / `2xl`=64
clear 44px on their own — the touch-first steps) OR keep it small and extend the hit area; never ship a bare
24px control whose target is also only 24px. The token gives you the square; the STEP choice — or the
extension — gives you the target.

## Focus rings (every focusable element)

One recipe app-wide:
```css
:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid <accent>;   /* width = 2px */
  outline-offset: var(--md-sys-focus-ring-offset);          /* offset = 2px */
}
```
The WIDTH and OFFSET are geometry tokens (both 2px in ADIA); the COLOR is the color skill's accent
(`--md-sys-color-primary`). The offset keeps the ring clear of the control edge so it survives any radius
(including the pill). Never remove a focus ring without replacing it, and never hardcode its width.

## Borders

`--md-sys-border-thin` (1px hairlines, field borders, dividers — the default) and `--md-sys-border-thick`
(2px emphasis). These are constants, NOT part of the space rhythm — a hairline is a hairline at every
density. Color comes from the color skill's outline roles.

## Density

`--md-sys-density` (a multiplier; ADIA = 1) is the treatment's rhythm knob — it already rides inside the
derived `--md-sys-size-{step}-*` values, so you don't apply it yourself. Read it only if you need to scale
a bespoke spacing to match the kit's feel; the standard tokens already carry it.

## The radius ladder vs the control pill

- `--md-sys-radius-{none|xs|sm|md|lg|xl}` (`0·4·8·12·16·28px`) — the flat Material-3 ladder for CONTAINER
  corners.
- `--md-sys-radius-full` (9999) — a pill / circle for round NON-control elements: avatars, standalone
  pills, dots.
- `--md-sys-size-{step}-radius` — a CONTROL's own height-linked corner (= height/2 pill radius by law, e.g.
  `md`=14px), so a control's roundness scales with its size. Use this on controls, the ladder on containers.

## Don't

- Don't size an in-control icon independently of `--md-sys-size-{step}-icon` (breaks centering).
- Don't shrink interactive controls below the hit-target floor on touch (stay at `xl`/`2xl`).
- Don't hardcode focus-ring width/offset or border width — they're `--md-sys-focus-ring-*` /
  `--md-sys-border-*`.
