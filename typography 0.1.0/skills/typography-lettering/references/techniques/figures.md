---
date: 2026-04-18
coverage: medium
peers:
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
  - ./small-caps.md
  - ./hanging-punctuation.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_fj
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_uz
  - https://www.w3.org/TR/css-fonts-4/
  - https://drafts.csswg.org/css-fonts-5/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
  - https://caniuse.com/font-variant-numeric
  - https://practicaltypography.com/numbers.html
  - https://practicaltypography.com/ordinals.html
  - https://practicaltypography.com/fractions.html
  - https://clagnut.com/blog/2380
  - https://rsms.me/inter/
  - https://wakamaifondue.com/
  - https://v-fonts.com/
  - https://www.chenhuijing.com/blog/font-variant-numeric/
  - https://fonts.google.com/
notes:
  - This file is the practitioner reference for figure styles — the 2×2 of figure shape × width policy, plus slashed zero, fractions, superiors/inferiors, and ordinals. Full OpenType-tag taxonomy and the `font-variant-*` vs `font-feature-settings` precedence rules live in `../contemporary/opentype-features.md`; this file cross-refers rather than duplicates.
---

# Figures — technique reference

**Coverage tier**: medium
**Last verified**: 2026-04-18
**Sources**: OpenType spec (Microsoft registry, 2024-05 snapshot), W3C CSS Fonts L4 (WD 2026-03-03), MDN `font-variant-numeric`/`font-variant-position` (retrieved 2026-04-18), Butterick *Practical Typography* §numbers/§fractions/§ordinals, caniuse 2026-04.
**Peer files**: `../contemporary/opentype-features.md`, `../contemporary/css-text-properties.md`, `./small-caps.md`, `./hanging-punctuation.md`.

Covers the practical surface of numeric typography on the web — figure style, width policy, slashed zero, fractions, superscript/subscript, ordinals — and the CSS-and-font decisions that make each one work. Out of scope: the full OpenType tag catalog (see `../contemporary/opentype-features.md`); CSS cascade mechanics for features (see same); variable-font axis wiring (see `../contemporary/variable-fonts.md`).

---

## The 2×2 Design Space

Latin figures sit on two independent axes: **figure shape** (lining vs oldstyle) and **width policy** (proportional vs tabular). Every Latin numeral in common use is one of these four combinations. Picking the right combination is the first and most-often-botched numeric decision in UI and editorial work.

|                         | **Proportional width**                      | **Tabular (uniform) width**              |
|-------------------------|---------------------------------------------|------------------------------------------|
| **Lining (cap-height)** | UI labels, all-caps headings with numbers, most display | Dashboards, data tables, code, clocks, SKUs |
| **Oldstyle (x-height)** | Running prose, book typography, long-form articles | Editorial-tradition financial tables (rare) |

### Lining figures

Cap-height digits, all at the same baseline-to-top height: every digit sits between the baseline and the cap line, with a uniform visual mass. Arabic numerals as rendered by most default system fonts are lining — `0123456789` reads as a row of boxes all occupying the same vertical band as an uppercase `A` or `H`. Lining figures match uppercase typography; they sit next to all-caps without visual disruption. They also shout: inside a lowercase paragraph, a run of lining figures rises above the x-height like a row of capitals, which is exactly the problem oldstyle figures solve.

OpenType tag: `lnum`. CSS: `font-variant-numeric: lining-nums`.

### Oldstyle figures (also called text figures, non-lining figures, lowercase figures)

Digits drawn with ascenders and descenders, so they range through the lowercase band rather than sitting at cap height. Traditional cut: `0`, `1`, `2` live at x-height; `6` and `8` rise to ascender height; `3`, `4`, `5`, `7`, `9` drop below the baseline with a descender. The exact set varies by designer — some cuts put `1` at x-height with a flag, some at cap-height, some draw `4` with a descender and some without — but the principle is consistent: oldstyle figures integrate with lowercase prose the way small caps integrate with lowercase prose. A page of running text with oldstyle figures reads as an even field; the same page with lining figures has rows of "shouting" numbers scattered through it.

OpenType tag: `onum`. CSS: `font-variant-numeric: oldstyle-nums`.

### Proportional figures

Each digit takes its natural advance width. `1` is narrow; `0`, `2`–`9` are wider and close to each other; `4` and `7` often sit in between. In running prose this is what you want — digits fit their own widths and the spacing looks rhythmic rather than forced.

OpenType tag: `pnum`. CSS: `font-variant-numeric: proportional-nums`.

### Tabular figures

Every digit has the same advance width regardless of its visual width. The narrow `1` is padded to match the `8`; the naturally wide `0` is drawn slightly narrower to match. The result is that a column of numbers stacks vertically — `10`, `20`, `1000`, `1234` all align digit-for-digit, right-justified by their own width. Tabular figures are what you want in any context where numbers stack in columns, change over time, or need to be compared position-by-position.

OpenType tag: `tnum`. CSS: `font-variant-numeric: tabular-nums`.

---

## The Four Combinations in Practice

**Lining + proportional** (`lnum` + `pnum`). The UI and display default for most fonts, including almost all sans-serif web fonts. Good for headlines, all-caps labels, hero numbers, and most marketing contexts where numbers appear next to other numbers rather than inside prose. This is the combination that comes out of a bare `font-family: Inter, sans-serif` with no `font-variant-numeric` set.

**Lining + tabular** (`lnum` + `tnum`). The UI-data default. Dashboards, analytics, stat cards, timestamps, clocks, data tables, spreadsheets, financial ledgers, any surface where numbers change and you want their columns to stay put. Code editors almost always deliver this through a monospace font, which is tabular by construction.

**Oldstyle + proportional** (`onum` + `pnum`). Book typography and long-form editorial. Running prose with numbers mid-sentence ("the 1820s", "the 47 cases studied", "page 152") — the numbers should integrate with the lowercase field, not punctuate it with capitals. This is the setting Bringhurst, Butterick, and most editorial designers endorse for body text when the font supports it.

**Oldstyle + tabular** (`onum` + `tnum`). Rare but legitimate. Editorial financial tables in publications that use oldstyle figures for body text and want the side-column numerics to continue the oldstyle voice without disrupting vertical alignment. Most literary magazines and classical editorial sites that commit to oldstyle body figures also ship oldstyle-tabular for the footnote callout, financial insert, or timeline column.

---

## CSS

### `font-variant-numeric` — the right property

```css
.prose   { font-variant-numeric: oldstyle-nums proportional-nums; }
.table   { font-variant-numeric: lining-nums tabular-nums; }
.stat    { font-variant-numeric: tabular-nums; }
.hero    { font-variant-numeric: lining-nums proportional-nums; }
.clock   { font-variant-numeric: tabular-nums slashed-zero; }
.recipe  { font-variant-numeric: oldstyle-nums proportional-nums diagonal-fractions; }
```

Tokens across four sub-axes can combine in one declaration:

- **Figure style:** `lining-nums` | `oldstyle-nums`
- **Width policy:** `proportional-nums` | `tabular-nums`
- **Fractions:** `diagonal-fractions` | `stacked-fractions`
- **Per-glyph switches:** `ordinal`, `slashed-zero` (both are additive)

Two tokens from the same sub-axis is a bug — `oldstyle-nums lining-nums` last-wins per the CSS grammar, and the result is engine-dependent. Keep to one token per axis.

### `font-feature-settings` — the low-level fallback

```css
.prose  { font-feature-settings: "onum", "pnum"; }
.table  { font-feature-settings: "tnum", "lnum"; }
.zero   { font-feature-settings: "zero"; }
.frac   { font-feature-settings: "frac"; }
```

Same OpenType tags, different cascade semantics. `font-feature-settings` declarations **replace** — they do not merge — across ancestry. A `font-feature-settings: "tnum"` on a child wipes out the parent's `"kern"`, `"liga"`, `"calt"` and any other tags set via the same property. This is the single most common cascade trap in OpenType CSS. See `../contemporary/opentype-features.md` §Precedence for the full treatment, including the custom-property workaround.

**Rule:** prefer `font-variant-numeric` for everything it covers. Reach for `font-feature-settings` only for tags outside the variant surface (`ss01`–`ss20`, `cv01`–`cv99`).

### Precedence when both are set

Per CSS Fonts L4 §6, when both are declared on the same element, `font-variant-*` wins for the tags it covers; `font-feature-settings` applies only for tags outside the variant surface. In practice, mixing layers on one element is a maintenance hazard — pick one.

---

## Browser Support

| Property | Ships on | Baseline | Notes |
|---|---|---|---|
| `font-variant-numeric` | Chrome 52+, Firefox 34+, Safari 9.1+, Edge 79+ | Baseline January 2020 | ~96.5% global usage (caniuse 2026-04). Effectively universal on evergreen. |
| `font-variant-numeric: ordinal` | All above | Same | `ordn` tag exposure. Font must carry the feature. |
| `font-variant-numeric: slashed-zero` | All above | Same | `zero` tag exposure. Font must carry the feature. |
| `font-variant-numeric: diagonal-fractions` | All above | Same | `frac` tag exposure. Font must carry the feature. |
| `font-variant-position: super \| sub` | Chrome 117+ (2023-09), Safari 17+ (2023-09), Firefox 34+, Edge 117+ | Baseline September 2023 | `sups`/`subs` tag exposure. Browser synthesizes if the font lacks the feature. |
| `font-feature-settings` | All evergreen | Baseline since 2017 | The low-level escape hatch. |

**The support table understates a real-world catch.** `font-variant-numeric` ships; the *feature the font exposes* may not. Setting `font-variant-numeric: oldstyle-nums` on a font with no `onum` feature is a silent no-op. Always verify with the specimen or with [Wakamai Fondue](https://wakamaifondue.com/) that the font you're using actually carries the features you're asking for.

---

## When to Use Each

### UI tables, dashboards, data views

**Lining + tabular.** `font-variant-numeric: tabular-nums lining-nums;` on the table or stat-card element. Every column of numbers aligns digit-for-digit; running ticks (stocks, sensors, clocks) don't jitter as the number changes. This is the single highest-leverage setting in data UI and the one most often omitted.

### Body prose with numbers

**Oldstyle + proportional** if the body font supports it. `font-variant-numeric: oldstyle-nums proportional-nums;` on `body` or the article container. Phone numbers, years, street addresses, ages, counts, measurements — these are words, not data, and deserve to read at lowercase color. If the body font ships only lining figures (true of most sans-serif UI fonts), accept lining + proportional for prose and save oldstyle for editorial surfaces that warrant a book-style serif.

### Headlines and display type

**Lining + proportional** in almost all cases. Display type sits away from lowercase running prose, so the "shouting" problem doesn't apply, and display cuts are often drawn with lining numerals by design. Editorial headlines set in a text-face family can use oldstyle for a book-cover feel — "Chapter 7" with an oldstyle `7` reads differently from "Chapter 7" with a lining `7` even at display size.

### Code

**Tabular, always.** Monospace fonts are tabular by construction — every glyph including digits shares one advance width. A "proportional monospace" is a contradiction. If you're setting code in a proportional font (which you shouldn't be), force `font-variant-numeric: tabular-nums` so at least the digits line up.

### Financial data

**Tabular, always.** Oldstyle tabular is acceptable in editorial contexts that preserve oldstyle elsewhere (a financial sidebar in a book-style layout). Everything else — bank statements, invoices, ledgers, crypto balances — is lining tabular. Digits must line up across rows and the column must not re-flow when a cell changes.

### Timestamps and clocks

**Tabular.** `00:00:00` with proportional figures means the seconds column shifts as the `1` narrows. Tabular figures freeze the column. Add `slashed-zero` if the timestamp format leads with `00` and the visual parity between `0` and `O` matters.

### Phone numbers, SKUs, IDs, serial numbers

**Tabular.** These are rendered in lists and tables, and list rendering with proportional figures produces width wobble between records. `+1 555 212 1111` aligned against `+1 555 313 9000` looks ragged in proportional, clean in tabular. Add `slashed-zero` if the field is alphanumeric and a leading `0` could be misread as `O`.

### Running scientific or technical prose

**Oldstyle + proportional** if the body font supports it and the numerical density is moderate. Switch to lining + proportional for math-heavy passages (readers expect lining when variables and equations are in play). Tabular is almost never right inside prose — it leaves visible gaps around narrow digits.

---

## Font Support

Which fonts actually carry which features is the deciding factor. Almost every Latin font has `lnum` + `pnum` (that's the normal state). Many have `tnum`. Fewer have `onum`. Fewer still have the full set plus `frac`, `sups`, `subs`, `ordn`, `zero`.

### Robust oldstyle + proportional + tabular

- **Adobe fonts:** Garamond Premier Pro, Minion Pro, Adobe Caslon Pro, Adobe Text Pro, Adobe Jenson Pro. All ship the full figure set by design.
- **Open-source serifs:** Source Serif 4 (full set), IBM Plex Serif (full set), PT Serif (oldstyle + lining + tabular variants), Fraunces (full set, variable-font), Merriweather (partial — oldstyle present, tabular limited), Literata (full set, variable-font), Cardo (oldstyle + lining; no tabular in recent builds).
- **Classic screen serifs:** Georgia (oldstyle default, lining + tabular available via `lnum`/`tnum`), Charter (oldstyle default), Iowan Old Style (oldstyle default).

### Robust tabular + proportional, lining-only

- **IBM Plex family** (Sans, Serif, Mono, Condensed) — tabular + proportional both; oldstyle only in Serif.
- **Inter** — tabular + proportional both; no true oldstyle, but ships a `cvXX` slot for alternate figure forms.
- **Source Sans 3** — tabular + proportional, lining-only.
- **Roboto** — tabular + proportional, lining-only.
- **Roboto Flex** — tabular + proportional + oldstyle (variable-font; one of the few open-source sans-serifs with genuine oldstyle).
- **DM Sans**, **Work Sans** — tabular + proportional, lining-only.
- **JetBrains Mono** — tabular (monospace) + slashed-zero variant + oldstyle available (rare for a monospace).

### System fonts

- **SF Pro / San Francisco** (Apple) — full set: oldstyle, lining, tabular, proportional, fractions, superscript, subscript. Exposes via `font-variant-numeric`. The most complete numeric surface in any shipped system font as of 2026-04.
- **Segoe UI** (Windows) — lining + tabular only. No oldstyle.
- **Helvetica Neue** (system) — lining + tabular only.
- **Ubuntu** (Linux default on some distributions) — full set.

### Google Fonts

Inconsistent. Many Google Fonts families ship only lining proportional figures; `font-variant-numeric: tabular-nums` silently does nothing on them. Always verify the feature list on the font's page or via Wakamai Fondue before committing. The Google Fonts family-detail page lists "OpenType features" explicitly.

**Verification tooling:**
- [Wakamai Fondue](https://wakamaifondue.com/) — drop in a font file, get the exhaustive feature list.
- [Axis-Praxis](https://www.axis-praxis.org/) — for variable fonts.
- Browser devtools → Computed → inspect `font-variant-numeric` and inspect whether the glyph changes.
- Eyeballing the specimen: set `1234567890` on and off with `font-variant-numeric: oldstyle-nums;` and see if the glyphs change.

---

## Slashed Zero

A `0` with a diagonal stroke through it, used to disambiguate from `O` (capital O). In monospace code contexts, in fixed-width ID/serial-number displays, in password fields where the character could be either, the slashed zero removes the ambiguity.

```css
.code    { font-variant-numeric: slashed-zero; }
.code-lo { font-feature-settings: "zero"; }  /* equivalent */
```

**Font support:**
- Monospace code fonts: JetBrains Mono, Cascadia Code, IBM Plex Mono, Fira Code, Source Code Pro, Hack, Inconsolata, SF Mono, Ubuntu Mono — all carry `zero`.
- Sans-serif UI fonts: Inter, Source Sans 3, IBM Plex Sans — yes. Roboto, DM Sans — varies by build. Segoe UI, SF Pro — yes.
- Serifs: less common. Iowan Old Style no; Literata yes; IBM Plex Serif yes.

**When to use:** any field where a leading-zero could be read as a capital O. Not for running prose — slashed zero breaks the rhythm of a paragraph.

**Gotcha:** some fonts ship the slashed zero as a *stylistic set* (`ss02` in Inter, for example) rather than as the dedicated `zero` feature. In that case `font-variant-numeric: slashed-zero` does nothing and you need `font-feature-settings: "ss02"` plus a careful read of the specimen to confirm.

---

## Fractions

`font-variant-numeric: diagonal-fractions` enables the font's `frac` feature, which substitutes a sequence like `1/2` for a composed fraction built from the designer's purpose-drawn numerator, virgule (the stroke between numerator and denominator), and denominator glyphs. The result looks like the Unicode ½ but is composed from the digits you typed, so any fraction works, not just the pre-composed ones.

`stacked-fractions` (the `afrc` tag) renders as a vertical stack with a horizontal bar — numerator above bar, denominator below. Rare; used in German typographic tradition, some mathematical and chemistry contexts, and a handful of cookbook designs.

```css
.recipe     { font-variant-numeric: diagonal-fractions; }
.fraction   { font-variant-numeric: diagonal-fractions; }
.math-stack { font-variant-numeric: stacked-fractions; }
```

**Implementation note:** the browser does not synthesize fractions. Only fonts that carry `frac` (or `afrc`) render the glyph substitution. Fonts without the feature leave `1/2` as three characters sitting on the baseline. Check the specimen.

**Scoping:** the `frac` feature is a contextual substitution that looks for `<digit>+ / <digit>+` sequences. Applied globally, it will mangle version numbers (`1.0/2.0`), IP addresses with CIDR notation (`10.0.0.1/24`), aspect ratios (`16/9`), dates (`12/31/2025`), and screen resolutions. **Always scope `font-variant-numeric: diagonal-fractions` to a `.fraction` span or an editorial element**, never to `body` or a large ancestor. See `../contemporary/opentype-features.md` §Fractions for the full trap.

**Pre-composed Unicode fractions.** Unicode encodes the common fractions as single codepoints: ½ ⅓ ¼ ⅕ ⅙ ⅛ ⅔ ¾ ⅖ ⅗ ⅘ ⅚ ⅞ ⅐ ⅑ ⅒. For the common fractions, inserting the Unicode codepoint is more portable than relying on `frac` — it works regardless of the font's feature support, and screen readers handle it as the full spoken fraction ("one half"). For uncommon fractions (`7/16`, `23/64`), `frac` on a supporting font is the only clean option.

---

## Superscript and Subscript

`font-variant-position: super` enables the `sups` OpenType feature; `font-variant-position: sub` enables `subs`. Both substitute the designer's purpose-drawn superscript or subscript glyphs — properly scaled, weight-compensated, and baseline-shifted — for the base digits or letters in the run.

```css
.footnote     { font-variant-position: super; }
.chemistry    { font-variant-position: sub; }
.ordinal-st   { font-variant-position: super; }
```

**Why this beats `<sup>` + `vertical-align`:** the markup-plus-CSS route (`<sup>` tag with `vertical-align: super` and `font-size: 0.6em`) mechanically shrinks and raises the glyph but does not compensate for stroke weight. The resulting superscript is thin — the digit was drawn for body-text weight and is now displayed at 60% size without the stroke adjustment a real superscript glyph would carry. A purpose-designed `sups` glyph has the stroke thickened to compensate, and the baseline shift is measured by the designer to sit at the correct optical position relative to the cap-height.

**Browser support (2026-04):** `font-variant-position: super | sub` is Baseline September 2023 — Chrome 117+, Firefox 34+, Safari 17+. Older Safari builds (9.1–16) shipped partial support. As of April 2026, evergreen engines cover it.

**Font support:** most serif book faces carry `sups`/`subs`. Source Sans 3, Inter, IBM Plex Sans, Recursive, Fira Sans, Public Sans all carry them. Many UI sans-serif fonts (older Roboto builds, DM Sans, Work Sans in some weights) ship only partial sets — `sups` may cover digits but not letters, so `2nd` renders the `2` as superscript but leaves the `nd` at base height. Verify.

**Synthesis fallback:** per CSS Fonts L4, when the font lacks `sups`/`subs`, the browser *must* fall back to synthesizing the position by shrinking and raising/lowering. Chromium and Safari both do this; Firefox does as well. The synthesized result is uniformly worse than a designed glyph — use fonts with genuine `sups`/`subs` in publications where footnotes and chemical notation are frequent.

**Accessibility:** screen readers read `<sup>` and `<sub>` as the literal characters with no special indication. `font-variant-position` does not alter the DOM text, so screen reader output is the same either way. For semantic footnote references use `<sup>` with `font-variant-position: super` on the element; the visual is typographic, the semantics stay markup-driven.

---

## Ordinals

`font-variant-numeric: ordinal` enables the font's `ordn` feature, which converts sequences like `1st`, `2nd`, `3rd`, `4th` into a composed form where the letter suffix is rendered as a raised small superior — the typographic convention for ordinals in English, French ordinals with `e` and `re`, Spanish and Portuguese ordinals with `a` and `o`, Italian ordinals similarly.

```css
.date { font-variant-numeric: ordinal; }   /* "March 3rd" → raised "rd" */
```

**Font support:** less common than figures-style features. IBM Plex family yes; Inter yes; Source Sans 3 yes; Source Serif 4 yes; Fraunces yes; Literata yes; Georgia no; Segoe UI no; SF Pro yes.

**Romance-language coverage:** `ordn` in Romance-language-capable fonts also handles `No.`, `1o`, `2a`, and some fonts include underlined small superior letters per the French and Portuguese conventions. Check the specimen if you're setting Romance-language ordinals.

**Alternative:** manual `<sup>st</sup>` markup plus `font-variant-position: super` approximates the result but lacks the designer's purpose-drawn small-superior forms. For English-only ordinal-heavy UI (dates, rankings), `font-variant-numeric: ordinal` on a font that supports it is the cleaner path.

---

## Inheritance and the Cascade

`font-variant-numeric` inherits, and each longhand sub-axis inherits and merges independently with descendant declarations. This is the load-bearing reason to prefer it over `font-feature-settings` for figure control:

```css
:root          { font-variant-numeric: oldstyle-nums proportional-nums; }
.data-block    { font-variant-numeric: tabular-nums; }
/* Inside .data-block, the computed value is oldstyle-nums tabular-nums
   — the width policy is overridden, the figure style is inherited. */
```

Contrast with `font-feature-settings`:

```css
:root          { font-feature-settings: "onum", "pnum", "kern", "liga"; }
.data-block    { font-feature-settings: "tnum"; }
/* Inside .data-block, onum / kern / liga are all replaced. The declaration
   does not merge; it wipes and sets the new comma-separated list. */
```

The merge-vs-replace distinction is the single most practically-important property of the variant longhands. For numerical control on component-scale elements (a stat card inside a prose body, a table inside an article), `font-variant-numeric` on the component and the inherited figure-style from the ancestor compose cleanly. `font-feature-settings` is always a single-value replacement.

**The `font-variant` shorthand resets.** Don't confuse the longhand `font-variant-numeric: oldstyle-nums` with the shorthand `font-variant: oldstyle-nums`. The shorthand is legal syntax but resets every other `font-variant-*` longhand (caps, ligatures, alternates, position, east-asian, emoji) to its initial value in the same declaration. The longhand is always the right tool for numeric settings.

---

## Interaction with Variable Fonts

Variable fonts and OpenType features compose independently. Setting `font-variation-settings: "wght" 600` and `font-variant-numeric: tabular-nums` on the same element gives you both: the 600-weight axis instance *and* the `tnum`-substituted glyphs. The shaper applies the `tnum` feature against the variable-axis-interpolated master, so tabular digits at weight 600 are rendered correctly.

**Where it can bite:** some variable fonts implement oldstyle figures as a `cvXX` or `ssXX` stylistic-set slot rather than via `onum`. On these fonts, `font-variant-numeric: oldstyle-nums` is a no-op, and you must reach for `font-feature-settings: "ssXX"` with the font-specific slot number. Inter is one such case — its oldstyle figures are accessed via `cv11` (or its `ss04` "open digit") rather than through `onum`. Always verify per font family before committing.

**Animating between styles** — for example, transitioning `font-variant-numeric: oldstyle-nums` → `lining-nums` on hover — animates *discretely*. The browser changes the glyph at the 50% mark of any transition timing. `font-feature-settings` and `font-variant-*` both behave this way. Variable-axis values via `font-variation-settings` *do* interpolate continuously (see `../contemporary/variable-fonts.md`). Don't expect smooth morphs between figure styles.

---

## Accessibility

Tabular vs proportional is invisible to screen readers — both render the same digit sequence and the assistive tech reads the values, not the glyphs. The visual jitter of proportional digits is a sighted-reader affordance, not an accessibility one.

**Exceptions and interactions:**

- **Pre-composed Unicode fractions** (½, ¾) read as the full spoken fraction in most screen readers. `frac`-composed fractions from three-character sequences (`1/2`) may read as "one slash two" or "one half" depending on engine and locale. Use Unicode codepoints when the fraction is common; use `frac` when it isn't.
- **`<time datetime="2026-04-18">Apr 18th</time>`** gives more semantic value than the visual alone. The ordinal rendering with `ordn` is purely visual.
- **Superscript and subscript** read as the literal character content. `H<sub>2</sub>O` reads as "H-2-O" in most engines. If the chemical or mathematical meaning is load-bearing, an `aria-label` on the container restores the intent ("water molecule", "hydrogen-2 oxide").
- **Slashed zero** is a font-glyph swap, not a character change. The underlying character is still `0`, so screen readers read it identically to a normal zero.
- **WCAG 2.2** has no specific SC for figure style. SC 1.4.4 (text resize to 200%) and SC 1.4.12 (text spacing) apply to any text regardless of figure features, but none of the numeric OpenType features affect compliance.

---

## Common Traps

- **Forgetting `font-variant-numeric: tabular-nums` on dashboard numbers.** Digits wiggle on every update, which is distracting and erodes trust in the data. Fix: set `tabular-nums` on the stat-value element at the earliest stage — on the design token, the component base, or the `:root` for a data-heavy product.
- **Using `font-feature-settings: "tnum"` alone.** The declaration replaces any earlier `font-feature-settings` (including inherited `"kern"`, `"liga"`, `"calt"`). Kerning and ligatures wink off where you least expect. Fix: use `font-variant-numeric: tabular-nums` — it merges across the cascade. See `../contemporary/opentype-features.md` §Precedence.
- **Assuming all fonts carry oldstyle figures.** Most sans-serif UI fonts ship only lining. Setting `font-variant-numeric: oldstyle-nums` on body with Roboto or DM Sans is a silent no-op. Fix: verify feature presence with Wakamai Fondue before committing, or choose a font family with documented oldstyle support (IBM Plex Sans + Serif, Source Sans + Serif, Roboto Flex).
- **Mixing tabular and proportional in the same table.** The stat label uses proportional, the stat value uses tabular, and the column widths drift as data changes. Fix: one width policy per table. Commit early.
- **Using `<sup>` + `vertical-align: super` + `font-size: 0.6em` instead of `font-variant-position: super`.** The results look crude — thin strokes, off-axis baseline shift. Fix: `font-variant-position: super` with a font that carries `sups`.
- **Applying `diagonal-fractions` globally.** `10.0.0.1/24`, `1920/1080`, and `03/15/2026` all render as fractions. Fix: scope `font-variant-numeric: diagonal-fractions` to a `.fraction` span.
- **Slashed zero via `font-variant-numeric: slashed-zero` when the font ships it as a stylistic set.** Inter's slashed zero is `ss02`; `font-variant-numeric: slashed-zero` silently does nothing. Fix: `font-feature-settings: "ss02"` (font-specific), or verify the font's `zero` tag presence.
- **Assuming `font-variant-numeric` shorthand-resets.** It doesn't — each declaration merges additively along orthogonal axes. But the `font-variant` *shorthand* (without the `-numeric` suffix) does reset every `font-variant-*` longhand. Don't write `font-variant: tabular-nums` thinking it's shorter — it's wrong. Always use the longhand.
- **Combining two figure-style tokens.** `font-variant-numeric: oldstyle-nums lining-nums` is last-wins, engine-dependent, and a latent bug. One token per sub-axis.

---

## Sources

- Microsoft Learn. "OpenType Feature tags: lnum, onum, pnum, tnum, frac, afrc, sups, subs, numr, dnom, ordn, zero." OpenType Feature Registry. [learn.microsoft.com/en-us/typography/opentype/spec/featurelist](https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist). Retrieved 2026-04-18.
- W3C CSS Working Group. "CSS Fonts Module Level 4." Working Draft, 2026-03-03. [w3.org/TR/css-fonts-4](https://www.w3.org/TR/css-fonts-4/).
- MDN Web Docs. "font-variant-numeric." [developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric). Retrieved 2026-04-18.
- MDN Web Docs. "font-variant-position." [developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position). Retrieved 2026-04-18.
- MDN Web Docs. "font-feature-settings." [developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings). Retrieved 2026-04-18.
- caniuse.com. "font-variant-numeric." [caniuse.com/font-variant-numeric](https://caniuse.com/font-variant-numeric). 2026-04 snapshot.
- Butterick, M. *Practical Typography* — chapters on numbers, ordinals, and fractions. [practicaltypography.com/numbers.html](https://practicaltypography.com/numbers.html), [.../ordinals.html](https://practicaltypography.com/ordinals.html), [.../fractions.html](https://practicaltypography.com/fractions.html). Retrieved 2026-04-18.
- Richard Rutter. "OpenType features in web browsers — test results and practical guide." [clagnut.com/blog/2380](https://clagnut.com/blog/2380). Retrieved 2026-04-18.
- Roel Nieskens. "Wakamai Fondue." [wakamaifondue.com](https://wakamaifondue.com/). Retrieved 2026-04-18.
- Rasmus Andersson. "Inter — feature catalog." [rsms.me/inter](https://rsms.me/inter/). Retrieved 2026-04-18.
- Chen Hui Jing. "font-variant-numeric." [chenhuijing.com/blog/font-variant-numeric](https://www.chenhuijing.com/blog/font-variant-numeric/). Retrieved 2026-04-18.
- Bringhurst, R. *The Elements of Typographic Style*, 4th edition. Hartley & Marks, 2013. (Chapter 3 on numerals.)
