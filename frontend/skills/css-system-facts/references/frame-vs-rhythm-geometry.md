# The FRAME-vs-RHYTHM geometry split — the single most novel concept in this pack

**This axis is CSS-architecture naming/mechanics — which token FAMILY a given dimensional value
belongs to, and which of two global multipliers it must ride. It is not the general theory of WHY
a spacing scale looks the way it does (that is `size-and-shape-rules`, the `frontend` plugin's own
theory pack) — this axis is the narrower, CSS-specific fact of how one production system encodes
that theory as two independently-multipliable custom-property families.**

## The split

**[verified]** agent-ui's `dimensions.css` names two token families sharing the control-band
ramp, each answering to a DIFFERENT global multiplier:

> "The two families (geometry.md): FRAME ∝ height (height, inline-pad, min-inline-size, radius) and
> RHYTHM ∝ font (gap = font/2, caret = font). `[scale]` multiplies BOTH the frame and the font;
> `[density]` multiplies the RHYTHM ONLY (the gap) — never the frame, since scaling the frame
> un-centers the glyph and breaks the square."

Concretely: `--md-sys-height-*`, `--md-sys-font-*`, `--md-sys-icon-*` are FRAME — they scale
together under `[scale]` and hold constant under `[density]`. `--md-sys-gap-*` is RHYTHM — it
rides `[density]` (and inherits scale's effect on font, since `gap = font / 2`, but is never
independently multiplied by `--md-sys-scale`). The file states the invariant with a physical
reason, not just a naming convention: **scaling the frame independently of the glyph it centers
would break the square** — a control's height and its glyph size must move together or the
centring math (`padding-inline-start: calc(height / 2)`, the h/2 law) stops holding.

**The same split governs layout spacing, one level up.** `--md-sys-space-*` (the Row/Column/Card
gap-and-padding ladder, distinct from a control's own internal gap) rides `[density]` only, never
`[scale]` — the file's own comment: "`[scale]` does NOT touch it: the base px is a LITERAL..
because layout rhythm is not control-frame size — a `[scale]` theme resizes the controls, not the
gutters between them." Both instances of the split — inside a control, and between laid-out
elements — agree on the same law: FRAME is the thing being resized when the user asks for a bigger
control; RHYTHM is the thing being resized when the user asks for a denser or airier layout. They
are orthogonal by construction, and a token that answers to the wrong multiplier is a defect, not
a style choice.

## The rejected-multiplier history

**[incident]** The current explicit per-`[scale]`-tier lookup table did not start this way. The
file's own comments name what it superseded: **"ADR-0038, supersedes the MULTIPLIER: ADR-0007's
control leg + ADR-0032's 0.875…1.75 ladder."** (This is agent-ui's own internal ADR-0038, a
different document from gen-ui-kit's cascade-layer ADR-0038 discussed in
`cascade-and-load-order.md` — same number, different repo, unrelated decision.) The rejected
design multiplied a SINGLE literal height by a per-tier ratio (`0.875`, `1`, `1.125`, `1.375`,
`1.5`, `1.75`) to derive every other control-band value from it — `height × ratio → font`,
`height × ratio → icon`, and so on, all riding one `var(--md-sys-scale)` chain.

**Why the ratio-multiplier approach broke:** a pure multiplier forces every derived value onto the
SAME ratio, but the actual desired control-band values at each tier are not a clean ratio of each
other — rounding a multiplied height to the nearest sane pixel, then re-deriving font/icon from
THAT rounded height by the same ratio, drifts from the hand-tuned values a designer actually wants
at that tier. The file's own comment names the specific failure this produced: "each `[scale]`
tier re-tables `--md-sys-{height,font,icon}-{sm,md,lg}` to its chosen §1 row (height picks the row;
font/icon derive from it — ONE consistent row per cell, **the thing the multiplier broke**)."

**The fix was an explicit lookup table, not a better multiplier.** Rather than deriving font/icon
from height via any ratio, each `[scale]` tier now hand-states all three literals directly:

```css
[scale="ui-lg"] {
  --md-sys-scale: 1.125;
  --md-sys-height-sm: 28px;
  --md-sys-height-md: 36px;
  --md-sys-height-lg: 48px;
  --md-sys-font-sm: 14px;
  --md-sys-font-md: 16px;
  --md-sys-font-lg: 18px;
  --md-sys-icon-sm: 18px;
  --md-sys-icon-md: 20px;
  --md-sys-icon-lg: 24px;
  --md-sys-compact-sm: 16px;
  --md-sys-compact-md: 18px;
  --md-sys-compact-lg: 20px;
}
```

`--md-sys-scale` itself is RETAINED as a custom property, but its role narrowed: it no longer
derives the control-band ramp (which is now a pure per-tier literal table); it survives only as
the multiplier the free-standing document typescale (`--md-sys-typescale-*-size`) still reads,
because that ramp genuinely IS a clean multiply-and-round case with no competing rounded-literal
requirement. **This is the pack's single most novel concept**: a design system's "make it
consistent" instinct (one multiplier, applied everywhere) is not always right — sometimes
consistency is better served by a literal per-tier table where a shared multiplier would force
every derived value onto a ratio the actual hand-tuned design doesn't want, and the correct fix is
recognizing WHICH values genuinely derive cleanly (typescale) versus which don't (the control
band) rather than forcing one mechanism onto both.

## Why this must sit on `*`, not `:root` (the pre-substitution trap)

**[verified]** A related, easy-to-miss mechanic the same file documents: the DERIVED ramp
(`--md-sys-gap-*`, `--md-sys-typescale-*-size`, `--md-sys-space-*`) is declared on the universal
selector `*`, never on `:root`, and the file's comment states why: "A `var()` inside a custom-
property value is substituted where the property is DECLARED, not where it is read: declared on
`:root`, every ramp token would freeze the `:root` values of `--md-sys-scale`/`--md-sys-density`
(= 1) into a literal, so a SUBTREE `[scale]`/`[density]` (on a wrapper, not `<html>`) would
repoint the multiplier but the ramp would never re-multiply — subtree scale/density would be
dead." Declaring on `*` makes every element re-substitute the multiplier IT inherits, which is what
makes a wrapper-scoped `[scale="content-lg"]` actually affect only its own subtree rather than the
whole document. The control-band literals (height/font/icon), by contrast, correctly sit on
`:root` PLUS the `[scale="..."]` selectors — they are not `var()`-derived from the multiplier at
all anymore (that's exactly what the rejected-multiplier fix removed), so the pre-substitution
trap doesn't apply to them.

## Sources

- agent-ui `packages/agent-ui/shared/src/tokens/dimensions.css` — the full FRAME/RHYTHM split, the
  rejected-multiplier history (agent-ui's own ADR-0007/ADR-0032/ADR-0038 citations), the
  per-`[scale]`-tier literal table, and the `*`-vs-`:root` pre-substitution comment — read directly
  2026-08-20 (500 lines).
