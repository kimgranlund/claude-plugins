---
date: 2026-04-17
coverage: deep
peers:
  - ./css-text-properties.md
  - ./variable-fonts.md
  - ../techniques/small-caps.md
  - ../techniques/figures.md
  - ../scripts/arabic.md
  - ../scripts/cjk-han.md
  - ../scripts/japanese.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ae
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_fj
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_uz
  - https://www.w3.org/TR/css-fonts-3/
  - https://www.w3.org/TR/css-fonts-4/
  - https://drafts.csswg.org/css-fonts-5/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-alternates
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-position
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-east-asian
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-emoji
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@font-feature-values
  - https://caniuse.com/font-feature
  - https://caniuse.com/font-variant-numeric
  - https://caniuse.com/font-variant-east-asian
  - https://caniuse.com/font-variant-alternates
  - https://caniuse.com/mdn-css_at-rules_font-feature-values
  - https://caniuse.com/mdn-css_properties_font-variant-emoji
  - https://clagnut.com/blog/2380
  - https://wakamaifondue.com/
  - https://sparanoid.com/lab/opentype-features/
  - https://unicode.org/reports/tr53/
---

# OpenType Features

This file is the practitioner catalog for the ~150 OpenType Layout (OTL) feature tags you will actually meet in Latin and pan-script web type, with the CSS surface that exposes each one and the gotchas that break implementations. It is oriented to the Microsoft OpenType Feature Registry's May 2024 snapshot (the registry is revised in place; no date-stamped version), and to the W3C **CSS Fonts Module Level 4** (WD 2026-03-03) and the emerging **Level 5** (ED 2026). Coverage of every OTL feature tag in existence (the registry has more) is out of scope — this is the set that matters for production.

**Precedence rule, load-bearing.** In CSS there are two ways to enable an OpenType feature:

1. **`font-variant-*`** — a family of high-level properties (`font-variant-ligatures`, `font-variant-numeric`, `font-variant-caps`, `font-variant-alternates`, `font-variant-position`, `font-variant-east-asian`, `font-variant-emoji`), each of which compiles to a curated set of OT tags defined by the CSS spec.
2. **`font-feature-settings`** — a low-level property that sets any OT tag by name with an on/off value or index.

The CSS spec is unambiguous: **prefer `font-variant-*`**. `font-feature-settings` is a settings-style property that should be treated as an escape hatch. In practice this matters for two reasons: (a) `font-feature-settings` does not merge across the cascade — a later declaration *replaces* the earlier one in full, so `font-feature-settings: "tnum"` on a child wipes out `font-feature-settings: "kern", "liga"` on the parent; (b) the browser's default feature set (kerning, standard ligatures, required ligatures, standard contextual alternates, script-shaping features) is defined relative to `font-variant-*`, not to `font-feature-settings`. Use the high-level properties when they exist; reach for the low-level one only for tags no variant property covers (stylistic sets `ss01–ss20`, character variants `cv01–cv99`, and a handful of East Asian and positioning features).

**Out of scope.** Feature *tables* (GSUB/GPOS lookups, script/language systems, mark-attachment mechanics) live inside the font and are not a CSS concern. AAT (Apple Advanced Typography) feature IDs from the Graphite/AAT world are similarly out of scope — modern Apple fonts ship OpenType features alongside AAT and the CSS surface only speaks OpenType. See the Microsoft registry `featurelist` page for the full list of ~140+ registered OT tags beyond this catalog.

## CSS Surface — Which Property Wins

The following mapping is authoritative per CSS Fonts L4 §6. Use the **preferred** column by default; fall back to `font-feature-settings` only when no variant property covers the feature.

| What you want to control | Preferred CSS | OT tags emitted | Fallback if variant unsupported |
|---|---|---|---|
| Kerning | `font-kerning: auto \| normal \| none` | `kern` | `font-feature-settings: "kern"` |
| Standard ligatures (on/off) | `font-variant-ligatures: common-ligatures \| no-common-ligatures` | `liga`, `clig` | `"liga", "clig"` |
| Discretionary ligatures | `font-variant-ligatures: discretionary-ligatures` | `dlig` | `"dlig"` |
| Historical ligatures | `font-variant-ligatures: historical-ligatures` | `hlig` | `"hlig"` |
| Contextual alternates (on/off) | `font-variant-ligatures: contextual \| no-contextual` | `calt` | `"calt"` |
| Oldstyle vs lining figures | `font-variant-numeric: oldstyle-nums \| lining-nums` | `onum` / `lnum` | `"onum"` / `"lnum"` |
| Proportional vs tabular figures | `font-variant-numeric: proportional-nums \| tabular-nums` | `pnum` / `tnum` | `"pnum"` / `"tnum"` |
| Diagonal vs stacked fractions | `font-variant-numeric: diagonal-fractions \| stacked-fractions` | `frac` / `afrc` | `"frac"` / `"afrc"` |
| Slashed zero | `font-variant-numeric: slashed-zero` | `zero` | `"zero"` |
| Ordinal figures | `font-variant-numeric: ordinal` | `ordn` | `"ordn"` |
| Small caps (lowercase only) | `font-variant-caps: small-caps` | `smcp` | `"smcp"` |
| Small caps (all letters) | `font-variant-caps: all-small-caps` | `smcp` + `c2sc` | `"smcp", "c2sc"` |
| Petite caps | `font-variant-caps: petite-caps \| all-petite-caps` | `pcap` / `pcap`+`c2pc` | `"pcap"` / `"pcap", "c2pc"` |
| Unicase | `font-variant-caps: unicase` | `unic` | `"unic"` |
| Titling caps | `font-variant-caps: titling-caps` | `titl` | `"titl"` |
| Superscript / subscript | `font-variant-position: super \| sub` | `sups` / `subs` | `"sups"` / `"subs"` |
| Stylistic set N | `font-variant-alternates: styleset(<name>)` + `@font-feature-values` | `ss01`..`ss20` | `font-feature-settings: "ss01"` |
| Character variant N | `font-variant-alternates: character-variant(<name>)` + `@font-feature-values` | `cv01`..`cv99` | `font-feature-settings: "cv01"` |
| Swashes | `font-variant-alternates: swash(<name>)` | `swsh`, `cswh` | `"swsh", "cswh"` |
| Historical forms | `font-variant-alternates: historical-forms` | `hist` | `"hist"` |
| Ornaments | `font-variant-alternates: ornaments(<name>)` | `ornm` | `"ornm"` |
| Annotation | `font-variant-alternates: annotation(<name>)` | `nalt` | `"nalt"` |
| Stylistic (single-tag alternate) | `font-variant-alternates: stylistic(<name>)` | `salt` | `"salt"` |
| Full / half / third / quarter width | `font-variant-east-asian: full-width \| proportional-width` | `fwid` / `pwid` | `"fwid"` / `"pwid"` |
| Ruby | `font-variant-east-asian: ruby` | `ruby` | `"ruby"` |
| JIS / trad / simpl CJK forms | `font-variant-east-asian: jis78 \| jis83 \| jis90 \| jis04 \| simplified \| traditional` | `jp78` `jp83` `jp90` `jp04` `smpl` `trad` | corresponding tag |
| Emoji presentation | `font-variant-emoji: auto \| text \| emoji \| unicode` | *no OT tag — Unicode variation selector* | N/A (variant prop only) |

Three things are **not** reachable through `font-variant-*` as of CSS Fonts L4 (2026-03 WD): `ss01–ss20` and `cv01–cv99` are reachable *via `font-variant-alternates`* but only through `@font-feature-values` blocks that declare named handles — writing `font-feature-settings: "ss02"` is the shorter path and is how most production code ships. Also unreachable via variant props: `aalt`, `rand`, `size`, `case` (case-sensitive punctuation), `cpsp` (capital spacing), positioning/shaping features (`mark`, `mkmk`, `init`, `medi`, `fina`, etc.), and a grab bag of East Asian metric tags (`halt`, `palt`, `vert`, `vrt2`). For all of these you must use `font-feature-settings` — or, usually better, leave them alone (the browser and shaper handle them).

### The `font-variant` shorthand

`font-variant` is a shorthand for the seven `font-variant-*` longhand properties (ligatures, caps, alternates, numeric, position, east-asian, emoji). **Beware its reset behaviour**: setting `font-variant: small-caps` resets every other `font-variant-*` longhand to its initial value — so you lose any numeric, alternates, or east-asian settings you had applied above it in the cascade. For surgical control set the longhand you care about and leave shorthand alone. (The same warning applies to the `font` shorthand, which resets `font-variant` along with everything else.)

### Why `font-feature-settings` cascades badly

`font-feature-settings` is declared as a *single* property value that is a comma-separated list. In the cascade, later wins — but "later wins" means the whole declaration replaces the previous one. There is no merge. Consequence:

```css
body     { font-feature-settings: "kern", "liga", "calt"; }
.figures { font-feature-settings: "tnum"; }  /* kern/liga/calt are now OFF here */
```

To work around this people author bundles via CSS custom properties:

```css
:root {
  --ff-base: "kern", "liga", "calt";
  --ff-extra: ;
}
body     { font-feature-settings: var(--ff-base) var(--ff-extra); }
.figures { --ff-extra: , "tnum"; }  /* resolves to "kern", "liga", "calt", "tnum" */
```

This works but the *correct* fix is to use `font-variant-numeric: tabular-nums` on `.figures` — the variant longhands *do* merge, inherit, and compose across the cascade. Reserve the custom-property trick for genuine cases (stylistic sets, character variants).

## Feature Catalog

### Ligatures

| Tag | Name | When on by default | What it does | CSS exposure |
|---|---|---|---|---|
| `liga` | Standard Ligatures | **Yes** | fi, fl, ffi, ffl, ff — designer's "safe" set. | `font-variant-ligatures: common-ligatures` (or `no-common-ligatures` to disable). |
| `clig` | Contextual Ligatures | **Yes** | Ligatures that depend on surrounding glyphs (a form of `liga` triggered only in context). In CSS, `common-ligatures` controls both `liga` and `clig` together. | `font-variant-ligatures: common-ligatures`. |
| `dlig` | Discretionary Ligatures | **No** | Historical or ornamental ligatures — "ct", "st", "Th", "fh", "sp", etc. Designer's "fun" set. | `font-variant-ligatures: discretionary-ligatures`. |
| `hlig` | Historical Ligatures | **No** | Archaic forms — long-s variants, et-ligatures styled historically. Overlaps with `dlig` in practice. | `font-variant-ligatures: historical-ligatures`. |
| `rlig` | Required Ligatures | **Yes, always** | Ligatures the script *requires* to be legible — Arabic lam-alif is the canonical case. Never disable; doing so produces malformed script output. | Not independently toggleable in CSS. Always on. |

**When to use:** `liga` / `clig` are on by default and should stay that way for body text — their absence is visible (broken `fi` joins). Enable `dlig` for display headlines in editorial contexts only; never in UI body (a surprising `ct` ligature in a legal form is hostile). `hlig` is rarely useful outside deliberate historical pastiche. **Never disable `rlig`** — it is how Arabic, Devanagari, and many other scripts stay legible.

**Gotcha:** `no-common-ligatures` disables `liga` and `clig` together, but does **not** disable `rlig`. Some UI engineers disable `liga` to avoid the `fi` character in Material Icons name lookups (the old "use ligatures to name icons" trick); that also disables standard text ligatures globally. Fix: scope the disable to the icon element, not the document.

### Kerning

| Tag | Name | When on | What it does | CSS exposure |
|---|---|---|---|---|
| `kern` | Kerning | **Yes** (auto) | Pair-wise horizontal spacing adjustments between adjacent glyphs. | `font-kerning: auto \| normal \| none`. `auto` is UA default. `normal` explicitly enables. `none` disables. |
| `cpsp` | Capital Spacing | **No** | Adds 2–3% extra tracking between capitals — prevents all-caps from feeling cramped. Designer-specified, not automatic letter-spacing. | `font-feature-settings: "cpsp"`. No `font-variant-*` exposure. |

**When to use:** `kern` should always be on; leave it as `auto`. `cpsp` is useful for all-caps headlines or UI labels — enable it on elements with `text-transform: uppercase`. Do not confuse `cpsp` with `letter-spacing`: `cpsp` uses the designer's measured adjustments per capital pair; `letter-spacing` is a uniform addition that ignores kerning. If both are set, `letter-spacing` is *added* on top of `cpsp`-adjusted metrics.

**Gotcha:** As of April 2026 some Windows IME plus Chromium combinations disable `kern` at small pixel sizes (≤11px) as a legacy pixel-grid concession. Setting `font-kerning: normal` forces kerning back on in most of these cases; `font-feature-settings: "kern" 1` is belt-and-braces.

### Numerals

The numeral feature tags form a **2×2 design space**: *figure style* (oldstyle vs lining) × *width policy* (proportional vs tabular).

|                       | **Proportional width**                 | **Tabular (uniform) width**         |
|-----------------------|----------------------------------------|-------------------------------------|
| **Lining (cap-height)** | `lnum` + `pnum` — running prose with caps, most UI labels, anything sat next to uppercase type. | `lnum` + `tnum` — UI numbers in columns: currency totals, date/time clocks, stat dashboards, code. |
| **Oldstyle (x-height)** | `onum` + `pnum` — body text, running prose, anything next to lowercase letters. Less jarring in a paragraph. | `onum` + `tnum` — rare but legitimate for financial tables in editorial layouts that preserve oldstyle elsewhere. |

| Tag | Name | Effect |
|---|---|---|
| `onum` | Oldstyle Figures | x-height-ish digits with ascenders/descenders — 3/5/7/9 have descenders, 6/8 have ascenders. Blends with lowercase prose. |
| `lnum` | Lining Figures | Cap-height digits, all at the same baseline-to-top height. Matches uppercase typography. |
| `pnum` | Proportional Figures | Each digit uses its natural advance width (1 narrower than 8). Right for prose. |
| `tnum` | Tabular Figures | All digits share a uniform advance width. Numbers stack vertically in tables. |

**When each wins:**

- **UI body / prose with numbers mid-sentence:** `onum` + `pnum`. Phone numbers, street addresses, years: these are words, not data.
- **Data tables, stat cards, dashboard counters, timestamps, any vertical column of numbers:** `tnum` + `lnum`.
- **Editorial body type that prefers an oldstyle palette but has a side column of figures:** body is `onum` + `pnum`, side column is `onum` + `tnum`.
- **All-caps labels or titles with numbers ("PAGE 3 OF 12"):** `lnum` + `pnum`. Oldstyle next to caps is visually wrong.

**CSS exposure:**

```css
.prose { font-variant-numeric: oldstyle-nums proportional-nums; }
.table { font-variant-numeric: lining-nums tabular-nums; }
```

You can combine any figure-style + width-policy token. Two from the same axis is illegal (e.g., `oldstyle-nums lining-nums` — the last-wins ordering makes this a source of bugs; keep declarations to one of each axis).

**Default behaviour.** Most fonts default to `lnum + pnum`. Some text-oriented fonts (Georgia, Charter, Iowan Old Style) default to `onum + pnum` to match their body-text intent. You cannot rely on a specific default — always set the pair you want when numeric style matters.

**Browser support** (caniuse 2026-04): `font-variant-numeric` is at ~96.5% global — Chrome 52+, Firefox 34+, Safari 9.1+. Effectively universal on evergreen.

**Interaction gotcha:** `font-variant-numeric: lining-nums` on an element that inherits `font-variant-numeric: tabular-nums` from a parent gives you `lining-nums` + `tabular-nums` — the longhand merges. This is the key property of `font-variant-*` and why it is preferred over `font-feature-settings`. With `font-feature-settings: "lnum"` on the child, the parent's `"tnum"` is wiped out.

See also `../techniques/figures.md`.

### Fractions, Superiors, Inferiors

| Tag | Name | What it does | CSS exposure |
|---|---|---|---|
| `frac` | Diagonal Fractions | Converts a run like `1/2` into a nicely composed diagonal fraction (numerator — virgule — denominator with designer-tuned metrics). | `font-variant-numeric: diagonal-fractions`. |
| `afrc` | Alternative (Stacked) Fractions | Converts the run into a stacked fraction — numerator over horizontal bar over denominator. Rare; used in some cookbooks, chemistry, German typographic tradition. | `font-variant-numeric: stacked-fractions`. |
| `sups` | Superscript / Superior | Raises and shrinks a run of digits/letters into the superscript position — 2nd, H₂O's 2, footnote markers. | `font-variant-position: super`. |
| `subs` | Subscript / Inferior | Lowered, smaller version of the run — chemistry subscripts, ionic charges. | `font-variant-position: sub`. |
| `numr` | Numerators | The designer's numerator-only form (smaller digits sat at fraction-top). Used internally by `frac` but occasionally exposed for custom fraction composition. | `font-feature-settings: "numr"`. |
| `dnom` | Denominators | Mirror of `numr` for the bottom of a fraction. | `font-feature-settings: "dnom"`. |
| `ordn` | Ordinals | Converts letter sequences like `No`, `1o`, `2a` into ordinal forms with underlined small superscript letters — Spanish / Portuguese / French / Italian usage. | `font-variant-numeric: ordinal`. |
| `zero` | Slashed Zero | Replaces the default 0 with a slashed-zero variant — prevents confusion with O in monospace code / ID / serial-number contexts. | `font-variant-numeric: slashed-zero`. |

**When to use:**

- `frac` on prose that mentions amounts ("1/2 cup") and on measurement tables. Scope it narrow — applying `frac` globally mangles version numbers, aspect ratios, and dates that look like fractions.
- `sups`/`subs` for footnote markers and chemical formulas. Note that typographically-correct superscript and subscript are **not** the same as CSS `vertical-align: super/sub` — the latter just mechanically raises and shrinks via `font-size-adjust`; the former uses the designer's purpose-built glyph with tuned weight.
- `ordn` for editorial Romance-language prose. Leave off for UI chrome.
- `zero` in monospace code editors, password fields with masked-text, serial-number displays, anywhere O-vs-0 ambiguity matters. Not for body prose.

**Gotcha:** `frac` is usually implemented as a contextual substitution — it looks for `<digit>+ / <digit>+` sequences. Applied to a run like `1/2 cup and 3/4 of the jars`, most shapers handle it fine. Applied to `IP 192.168.1.1/24`, it will treat `1/24` as a fraction. **Always scope `frac` tightly**: apply it to a `.fraction` span, not to body text.

**`sups` vs CSS super:** the spec says browsers *must* fall back to synthesized super/sub if the font lacks real `sups`/`subs` glyphs. Safari and Chromium both do this; synthesized look is uniformly worse than real. Use fonts with genuine `sups`/`subs` tables (Source Sans 3, Inter, IBM Plex, Recursive all have them) when superscript is frequent.

### Stylistic Sets and Character Variants

This is where OpenType gets **designer-proprietary**. The registry allocates 20 slots for Stylistic Sets (`ss01`..`ss20`) and 99 slots for Character Variants (`cv01`..`cv99`). The registry does **not** prescribe what each slot does — the font designer chooses.

| Tag family | Slots | Semantics |
|---|---|---|
| `ss01`..`ss20` | 20 | **Stylistic Sets.** Contiguous substitutions — a set affects a defined set of characters simultaneously. `ss01` in Fira Sans might "use straight-sided letterforms", affecting a, g, j, l, y, etc. in one unified aesthetic move. |
| `cv01`..`cv99` | 99 | **Character Variants.** Per-character alternates — `cv01` might replace just `a`; `cv02` might replace just `g`. Designer-picked, and typically each `cv` affects one character or a small set of closely related characters (single/double-storey `a` alone; barred/unbarred `I` alone). |

**The key difference (from the registry docs, paraphrased):** `ss01–ss20` are meant for *grouped* stylistic changes — the user picks a "mode", letters change together. `cv01–cv99` are meant for *individual* character-level swaps — the user curates each substitution independently. A well-specified font might expose "straight g" as `cv03` so you can enable it without taking the rest of the `ss02` aesthetic, while exposing the full "straight sans geometry" as `ss02` for users who want the whole package.

**Why stylistic sets are named per font:** the OpenType registry lets the font specify a human-readable `nameID` for each slot via the `FeatureParamsStylisticSet` record. Specimens publish this — Grilli Type, Commercial Type, Klim, Dinamo, and Pangram Pangram all publish a one-line legend per slot ("GT America ss01: alternate g"). The CSS spec requires the author to declare the name in `@font-feature-values` before using it in `font-variant-alternates`. Example:

```css
@font-feature-values "GT America" {
  @styleset {
    alt-g: 1;       /* maps author's name "alt-g" to ss01 */
    geometric: 2;   /* maps "geometric" to ss02 */
  }
  @character-variant {
    double-storey-a: 5;   /* maps "double-storey-a" to cv05 */
  }
}

.display {
  font-family: "GT America";
  font-variant-alternates: styleset(alt-g) character-variant(double-storey-a);
}
```

This is the "correct" path. In practice, most production code uses `font-feature-settings: "ss01" 1, "cv05" 1` because the `@font-feature-values` ergonomics are clunky and browser support was uneven until ~2023. Browser support for `@font-feature-values` + `font-variant-alternates` with `styleset()`/`character-variant()` (caniuse 2026-04): Chrome 111+ (2023), Firefox 34+, Safari 9.1+ — effectively universal as of 2024.

**When to use `cv` over `ss`:**

- The user wants *just* one character changed (single-storey `a` in Inter without turning on the rest of Inter's "alternate geometry" set): use `cv`.
- The designer bundled several changes into a coherent aesthetic (a "geometric variant" that changes a, g, i, l, M, Q all at once): use `ss`.
- A single-character swap that the designer grouped into an `ss` slot can still be accessed *only* through that `ss` — the designer's packaging decision is final.

**Naming conventions in production:**

- **Inter** (Rasmus Andersson) exposes ~20 slots — famous ones: `cv01` single-storey `a`, `cv02` open digit 4, `cv11` alternate `l` with serif, `ss01` "open digits" bundle, `ss02` "disambiguation" (adds bars to I, l, 0).
- **IBM Plex Sans** uses `ss01` for "simplified" forms.
- **Fira Code** uses `cvXX` slots for individual ligature group disables and `ssXX` for alternate letterforms.
- **Recursive** uses `ss01`..`ss11` for casual vs linear alternates.
- **Iosevka** has a dense slot catalog — most production code ships a configuration file rather than CSS-side enabling.

**Gotcha with `font-feature-settings` syntax:** `"ss01" 1` turns on, `"ss01" 0` turns off, `"ss01"` alone defaults to 1 (per spec). All three are valid; the explicit-value form is clearer. Bare-string form trips up some tooling (PostCSS plugins occasionally normalize it). For `cvXX` the same applies; some fonts also respect an *index* value — `"cv05" 2` selects the second alternate in `cv05` if the font authored more than one. This is rare; always check the specimen.

### Case, Small Caps

| Tag | Name | What it does | CSS exposure |
|---|---|---|---|
| `smcp` | Small Capitals | Substitutes lowercase glyphs with small-cap forms sized around the x-height to cap-height range. | `font-variant-caps: small-caps`. |
| `c2sc` | Capitals to Small Capitals | Substitutes uppercase glyphs with small-cap forms. Used with `smcp` for *all-small-caps* runs. | `font-variant-caps: all-small-caps`. |
| `pcap` | Petite Capitals | Like `smcp` but smaller, x-height or below. Rare; found in some text-face supersets. | `font-variant-caps: petite-caps`. |
| `c2pc` | Capitals to Petite Caps | Counterpart of `c2sc` for petite caps. | `font-variant-caps: all-petite-caps`. |
| `unic` | Unicase | Mix of upper- and lowercase glyphs chosen to be visually uniform — all glyphs sit in a single height band. Rare feature. | `font-variant-caps: unicase`. |
| `case` | Case-Sensitive Forms | Adjusts **punctuation and symbols** for all-caps runs — raises parentheses, brackets, dashes, middle dots, guillemets to align with cap-height instead of x-height. Does *not* change letters. | No `font-variant-*` surface. `font-feature-settings: "case"`. |

**When to use:**

- `smcp` with a real small-cap font: for acronyms inline in prose (`ISO`, `HTTP`, `NASA` — though the "smcap acronym" convention is a regional style, more common in editorial British typesetting than in US tech writing).
- `c2sc` + `smcp` (i.e., `all-small-caps`): for section labels, standfirsts, figure captions — runs of text that should be typographically quieter than body but want the even color of caps.
- `case`: whenever you use `text-transform: uppercase` or `font-variant-caps: all-small-caps` with punctuation. Parentheses around a small-cap acronym look wrong unless `case` lifts them — `(NATO)` has parens sitting at lowercase height next to cap-height letters.
- `pcap` / `c2pc`: rarely needed. Some editorial contexts (academic-book-style page headers with petites) require them; most production code can skip.
- `unic`: typographically playful. Display contexts only.

**Synthesized small caps (the "fake" route):** when the font lacks `smcp`, CSS can synthesize small caps by scaling uppercase glyphs down. The result is *inferior* in weight balance (the shrunk glyph has a thinner stem than a real small-cap glyph, which is weight-compensated by the designer). See `../techniques/small-caps.md` for the quality comparison and when synthesized is acceptable.

**Gotcha:** `font-variant-caps: small-caps` vs `font-variant: small-caps` — the shorthand resets every other variant longhand. See the shorthand warning above.

### Contextual and Stylistic Alternates

| Tag | Name | What it does | CSS exposure |
|---|---|---|---|
| `calt` | Contextual Alternates | Substitutes glyphs based on surrounding glyphs — usually used for script and calligraphic fonts to make joins work, or for code fonts to trigger programming ligatures (`->`, `=>`). **On by default.** | `font-variant-ligatures: contextual \| no-contextual`. |
| `salt` | Stylistic Alternates | Generic "give me the designer's alternate for this glyph" substitution. Older, broader-brush than `ss`/`cv`. Still used. | `font-variant-alternates: stylistic(<name>)` (via `@font-feature-values`) or `"salt"`. |
| `titl` | Titling Alternates | Substitutes glyphs designed specifically for display/titling sizes — often refined, tighter, more delicate versions of body forms. | `font-feature-settings: "titl"`. |
| `nalt` | Alternate Annotation Forms | Annotation-style alternates — circled, parenthesized, boxed versions of characters (primarily East Asian usage). | `font-variant-alternates: annotation(<name>)`. |
| `swsh` | Swash | Adds swashes to glyphs designed for them — primarily italic and script fonts with extravagant initial/terminal forms. | `font-variant-alternates: swash(<name>)`. |
| `cswh` | Contextual Swash | Like `swsh` but only applied when context is right (e.g., only on a character that ends a word). | `font-variant-alternates: swash(<name>)` emits both `swsh` and `cswh`. |
| `hist` | Historical Forms | Substitutes characters with their historical counterparts (long-s, old-style ampersand, long-tailed Q). | `font-variant-alternates: historical-forms`. |
| `hlig` | Historical Ligatures | See Ligatures above. | `font-variant-ligatures: historical-ligatures`. |

**When to use:**

- `calt` should stay on. Disabling it in a code editor *is* sometimes deliberate — developers who dislike `->` becoming an arrow glyph set `font-variant-ligatures: no-contextual` to neutralize the font's programming-ligature substitutions. Everywhere else, leave it.
- `salt` is a catch-all. Many older fonts (pre-2010) expose alternates only through `salt`. Newer fonts tend toward `ss`/`cv`.
- `titl` on display headings when the font has a dedicated titling design cut inside it. This is rare in variable fonts — most families use the `opsz` axis instead (see `./variable-fonts.md`). A few families (Requiem, some Porchez designs) still ship `titl` as a substitution rather than an optical-size axis.
- `swsh` / `cswh` for initial or final swashes in italic or script display type. Use sparingly.
- `hist` for typographic pastiche (eighteenth-century reproductions, fine editions). Aggressively jarring in modern contexts.

**Gotcha:** `calt` being "on by default" is a CSS spec fact but not all browsers/shaper combinations respect it identically for all scripts. For Latin, treat it as on. For script and calligraphic fonts (e.g., Bickham Script), the font's core join system lives in `calt` and disabling it breaks the font.

### Localization

The `locl` feature tag is an inconspicuous but enormously important bucket. Its role: **swap glyphs based on the declared language of the surrounding text**, without changing the underlying characters. It is how a single font supports Dutch, Turkish, Catalan, Polish, Bulgarian, Serbian, and Romanian without treating them as five different fonts.

| Tag | Name | What it does |
|---|---|---|
| `locl` | Localized Forms | Substitutes glyphs based on `lang`-declared language. The OT shaper queries the font's language system for the current `lang` attribute and applies `locl` lookups tagged for that language. |

**Trigger in CSS/HTML:** set the `lang` attribute on the text or a parent element. The browser passes the language to the shaper; the shaper picks the locale-appropriate glyph.

```html
<p lang="tr">İstanbul ve izmir</p>  <!-- Turkish: i stays dotted, capital I gets a dot in Istanbul -->
<p lang="nl">IJsselmeer</p>         <!-- Dutch: IJ may be ligated or kerned as a single digraph -->
```

**Languages with well-known `locl` rules:**

- **Turkish (`tr`) / Azerbaijani (`az`) / Kazakh (`kk`).** Preserves the dotted-i / dotless-ı distinction in both cases. Capital İ (with dot) vs capital I (dotless) are separate Unicode characters; the `locl` feature doesn't change the character, but it adjusts the dot position for Turkish conventions. Critical for Turkish-language sites: no `lang` = Romanized rendering, meaning İ looks like I with a floating tittle that's too high.
- **Dutch (`nl`).** The IJ digraph. Some fonts treat IJ as two glyphs with special kerning; others provide a ligated IJ glyph triggered by `locl`. Proper Dutch requires `lang="nl"` for the digraph to hang together when title-casing ("IJsselmeer", not "Ijsselmeer").
- **Catalan (`ca`).** The middle dot in `ŀl` (el geminada, "double l"). Catalan spelling requires the interpunct between two l's: `cel·la`, `paraŀlel`. With `lang="ca"` the font may provide proper spacing and positioning for the middle dot relative to the l's.
- **Polish (`pl`).** The shape of the ogonek on ą and ę. Polish-specific ogoneks attach at the *right* side of the letter bowl; generic Latin ogoneks hang from the baseline under the center. `locl` swaps to the correct attachment.
- **Serbian / Macedonian (`sr` / `mk`).** Cyrillic `б`, `г`, `д`, `п`, `т` have different shapes in Serbian typography than in Russian. Italic Cyrillic especially diverges — the Russian italic `т` is roughly a latin `m`-shape, while Serbian italic `т` is more like a latin `w` with curved tops. Without `lang="sr"`, Cyrillic fonts default to Russian forms.
- **Bulgarian (`bg`).** Cyrillic forms that are noticeably closer to Latin shapes than the Russian defaults — `ж`, `к`, `Д` have distinct Bulgarian forms. The same font renders Russian `lang="ru"` vs Bulgarian `lang="bg"` quite differently when `locl` is implemented.
- **Romanian (`ro`) / Moldovan (`mo`).** Comma-below versus cedilla on `ș`, `ț`. Some fonts include both; `locl` swaps comma-below into place for Romanian.
- **Moroccan Arabic / Urdu / Persian variant Arabic.** For Arabic, `locl` controls differences in heh, kaf, yeh shapes across Arabic-speaking regions. See `../scripts/arabic.md` for the full regional variant story.
- **German (`de`).** Some fonts (Adobe Text, early Underware) use `locl` to switch the capital ẞ (sharp-s capital, U+1E9E) or provide German-specific long-s alternates.

**CSS exposure:** there is **no `font-variant-*` property** for `locl`. The trigger is **always** the `lang` HTML attribute (or CSS `:lang()` selector, but the actual shaping engagement happens via the attribute). Forcing `locl` via `font-feature-settings: "locl"` without a lang tag works in some browsers and not others; it is **not the idiomatic path**. Always set `lang`.

**Gotchas:**

- **Missing `lang` attribute.** If the root `<html lang="en">` is the only lang declaration, and you're serving Turkish content inside, the shaper will use English shaping — `locl` does not fire. Retrofit: `<html lang="en"><body><article lang="tr">` or set `lang` at whichever level the content changes.
- **BCP 47 region subtags matter sometimes.** `sr-Latn` vs `sr-Cyrl` (Serbian in Latin vs Cyrillic script) can change shaping. `pt-BR` vs `pt-PT` doesn't change `locl` for any commonly-used font but may affect hyphenation. `zh-Hans` vs `zh-Hant` is the big one — see East Asian below.
- **`locl` disabled by `font-feature-settings: normal`.** If a stylesheet sets `font-feature-settings: normal`, the browser's default feature emission (which includes `locl` for the shaper's own use) may or may not be preserved. Chromium preserves it; some older Safari versions did not. Don't set `font-feature-settings: normal` unless you want to lose script-critical defaults.

### East Asian

This section is a map; full-depth CJK typography lives in `../scripts/cjk-han.md` and `../scripts/japanese.md`.

| Tag | Name | Role |
|---|---|---|
| `fwid` | Full Widths | Substitutes narrow (half-width) glyphs with full-width (ideographic em-width) variants. E.g., Latin ASCII `A` → full-width `A` (U+FF21). |
| `hwid` | Half Widths | Mirror: converts full-width to half-width. |
| `qwid` | Quarter Widths | Rare; converts to quarter-em width. Used in some Japanese display typography. |
| `twid` | Third Widths | Rare; third-em width. |
| `halt` | Alternate Half Widths | **Metric-only** substitution — swaps glyphs whose *advance width* is half-em while keeping the glyph outline full-width. For optical mid-line spacing in CJK. |
| `palt` | Proportional Alternate Widths | Metric-only substitution to proportional (glyph's natural) advance width. Used in Japanese body type to tighten horizontal rhythm where full-width would look gappy. |
| `vert` | Vertical Alternates | Replaces glyphs with versions designed for vertical text — rotated punctuation, brackets, parentheses. Used in `writing-mode: vertical-rl/lr`. |
| `vrt2` | Vertical Alternates and Rotation | Superset of `vert` — also rotates non-CJK characters 90° counterclockwise to match vertical flow. Preferred over `vert` per the OT spec when available. |
| `vkna` | Vertical Kana Alternates | Vertical alternates specifically for hiragana and katakana. |
| `vrtr` | Vertical Alternates for Rotation | Subset providing only the rotated forms. |
| `ruby` | Ruby Notation Forms | Swaps to smaller kana/kanji designed for use as ruby (furigana) — proportioned for tiny sizes alongside a base character. |
| `jp78` | JIS78 Forms | Replaces kanji with their 1978 JIS standard (C 6226-1978) form. Archaic; used for historical reproduction. |
| `jp83` | JIS83 Forms | Replaces with 1983 JIS forms (C 6226-1983). Slightly revised from jp78. |
| `jp90` | JIS90 Forms | Replaces with 1990 JIS forms (X 0208-1990). |
| `jp04` | JIS2004 Forms | Replaces with 2004 JIS forms (X 0213-2004). Most modern Japanese body text wants jp04 in display, but often not in body. |
| `trad` | Traditional Forms | Substitutes simplified Han characters with traditional forms. Used by `zh-Hant`-targeting typography. |
| `smpl` | Simplified Forms | Mirror of `trad` — substitutes traditional with simplified. Used by `zh-Hans`. |
| `expt` | Expert Forms | Substitutes to "expert" glyph set — refined versions of kanji, kana, punctuation used in high-end Japanese book typography. |

**CSS exposure:**

```css
.jp-table { font-variant-east-asian: full-width; }
.jp-body  { font-variant-east-asian: jis04 proportional-width; }
.tw-body  { font-variant-east-asian: traditional; }  /* implies trad */
.cn-body  { font-variant-east-asian: simplified; }   /* implies smpl */
.ruby     { font-variant-east-asian: ruby; }
```

`font-variant-east-asian` is the canonical high-level property (Chrome 63+, Firefox 36+, Safari 9.1+; ~96.2% global, caniuse 2026-04). Not all East Asian tags are exposed through it — `halt`, `palt`, `vert`, `vrt2`, `vkna`, `vrtr` are not.

**Vertical text (tategaki):** set `writing-mode: vertical-rl` and the browser will automatically emit `vert`/`vrt2` during shaping — do not manually enable them. The shaper chooses `vrt2` over `vert` if both exist. Manually setting `font-feature-settings: "vert"` in horizontal text produces broken output (rotated punctuation floating in a horizontal baseline).

**Proportional vs full-width, the decision:** historical Japanese typesetting treats every character — kana, kanji, Latin — as full-width for the rhythm of the column. Modern web-first Japanese often switches to `palt` (proportional advance) for body text because full-width Latin inside Japanese paragraphs looks gappy at screen sizes. Noto Sans CJK, Source Han Sans, Hiragino Sans, Yu Gothic all ship both. See `../scripts/japanese.md`.

**Gotcha:** `lang="ja"` vs `lang="zh-Hans"` vs `lang="zh-Hant"` matters for **which glyphs the font picks** at all, not just for `locl`. Source Han Sans / Noto Sans CJK ship a single font with four language variants (JP, KR, SC, TC); CSS needs the right `lang` attribute **and** the right `font-family` branch (or a font that has proper language-system coverage). Without `lang`, the shaper picks a default language system — typically Japanese — and renders Chinese characters in their Japanese forms, which is wrong for Chinese.

### Script-shaping Features (Never Disable)

These features are how complex scripts *work*. They are applied automatically by the OpenType shaper (HarfBuzz in all major browsers as of 2026) based on script and language detected from `lang` and text content. **You should never disable these via `font-feature-settings` — doing so breaks shaping and produces garbage output.**

| Tag | Role | Applies to |
|---|---|---|
| `mark` | Mark positioning. Positions combining marks (accents, diacritics) relative to base glyphs via GPOS mark-to-base attachment. | All scripts with combining marks (Latin with accents, Arabic with tashkeel, Devanagari with matras, Hebrew with niqqud, etc.). |
| `mkmk` | Mark-to-mark positioning. Positions stacked marks relative to *other marks* (so an acute on top of a circumflex sits at the correct height). | Same scripts as `mark`. |
| `abvm` | Above-base marks. Indic-specific — positions vowel signs above the base consonant. | Indic scripts. |
| `blwm` | Below-base marks. Indic-specific — positions vowel signs below the base consonant. | Indic scripts. |
| `init` | Initial forms. Arabic/Syriac shaping — the word-initial contextual form of the letter. | Arabic, Syriac, N'Ko, Mongolian. |
| `medi` | Medial forms. Word-medial contextual form. | As `init`. |
| `fina` | Final forms. Word-final contextual form. | As `init`. |
| `isol` | Isolated forms. Isolated (unconnected) contextual form. | As `init`. |
| `cursive` | Cursive attachment. GPOS cursive connection — e.g., the tail of one Arabic letter attaching to the head of the next. | Cursive-joining scripts. |
| `pres` | Pre-base substitutions. Indic-specific — substitutes pre-base vowel/matra forms. | Indic scripts. |
| `psts` | Post-base substitutions. Mirror of `pres` for post-base. | Indic scripts. |
| `abvs` | Above-base substitutions. Substitutes glyphs with combined above-base-mark forms. | Indic scripts. |
| `blws` | Below-base substitutions. Mirror for below-base forms. | Indic scripts. |
| `akhn` | Akhand (indivisible) ligatures. Indic-specific — ksha, jnya, etc. | Indic scripts. |
| `half` | Half forms. Indic consonant half-forms used in conjuncts. | Indic scripts. |
| `cjct` | Conjunct forms. Explicit conjunct-form substitutions. | Indic scripts. |
| `rphf` | Reph forms. Indic — repositioned ra-above-base forms. | Indic scripts. |
| `blwf` | Below-base forms. Indic — consonant below-base forms. | Indic scripts. |
| `half` / `pstf` / `pref` | Various contextual Indic-script substitutions. | Indic scripts. |
| `ccmp` | Glyph composition / decomposition. General-purpose decomposition of composed Unicode characters to base+mark sequences for mark positioning to work. | All scripts. |

**The rule:** do not touch these through CSS. The only correct CSS action related to shaping features is setting `lang` correctly so the shaper picks the right script system.

**`font-feature-settings: normal` danger.** If you set `font-feature-settings: normal` on an element with Arabic content, you are asking the browser to go back to the *CSS-computed* defaults, which still include shaping features — so this is safe. What is **unsafe** is `font-feature-settings: "init" 0` or similar — explicitly disabling a shaping feature. Arabic will render every letter in its isolated form, producing gibberish.

### Access-all-alternates and Misc

| Tag | Name | Effect | CSS exposure |
|---|---|---|---|
| `aalt` | Access All Alternates | Exposes **all** alternate glyphs for a character as a menu. Not meant for layout engines — meant for the "Glyphs" palette in Illustrator/InDesign. In CSS, enabling it usually does nothing visible; some shapers pick the first alternate. | `font-feature-settings: "aalt"`. Rarely useful. |
| `rand` | Randomize | Chooses among multiple alternates pseudo-randomly — used for fake-handwriting or organic-feel fonts that ship multiple alternate forms per character. | `font-feature-settings: "rand"`. Browser support is partial — Chromium and Safari as of 2024 support `rand` in shaping; Firefox historically did not. |
| `size` | Optical Size | The **pre-variable-font** way to expose optical-size variants. A font with a `size` feature records design size ranges for each style (subfamily) in a font collection. Applications then select the right sub-font at render time. | Obsolete for CSS — `font-optical-sizing: auto` + `opsz` variable axis supersede it. Some applications (Adobe Illustrator) still honor `size`. |

**When to use:**

- `aalt`: don't. It's a design-app affordance.
- `rand`: on display playful contexts with a font designed for it (Beastly, Liza Pro, some handwriting-style fonts from OhNo or Maria Doreuli). Not a body-text tool.
- `size`: skip. Use variable fonts with `opsz`.

## Precedence and Cascade Gotchas

### The `font-feature-settings` replacement trap

**The problem (in one sentence):** `font-feature-settings` declarations don't merge across the cascade — any child declaration completely replaces the parent declaration. This is a spec-mandated behavior (CSS Fonts L3 §6.11), not a bug.

```css
:root           { font-feature-settings: "kern", "liga", "calt"; }
.tabular-block  { font-feature-settings: "tnum"; } /* kern, liga, calt all off here */
```

Inside `.tabular-block`, kerning is still on because `kern` is the browser default (and `font-kerning: auto` has not been overridden), and `liga` is on because `common-ligatures` is the default for `font-variant-ligatures`. But: `calt` is **not** automatically applied by the browser — it is implicit in `font-variant-ligatures: contextual` (which is the default), so it *would* still be on... unless you set `font-feature-settings: "tnum"` and the browser implementation interpreted this as turning off the author-controlled feature list. Chromium's behaviour is documented (CSS Fonts L4 §6): user-defined `font-feature-settings` are merged with browser-default shaping features; author-defined `font-feature-settings` replace author-default stacks.

The practical consequence is still confusion. Four defensive patterns:

**1. Use `font-variant-*` — the longhands merge.** This is the correct fix for everything the variants cover:

```css
:root          { font-variant-ligatures: common-ligatures contextual; }
.tabular-block { font-variant-numeric: tabular-nums lining-nums; }  /* ligatures still on */
```

**2. Re-declare the base set everywhere you need to extend it.**

```css
.tabular-block { font-feature-settings: "kern", "liga", "calt", "tnum"; }
```

Works, but couples every consumer to the full base list. Not scalable.

**3. Use CSS custom properties to compose.**

```css
:root {
  --ff-base: "kern", "liga", "calt";
  --ff-extra: ;
}
body            { font-feature-settings: var(--ff-base) var(--ff-extra); }
.tabular-block  { --ff-extra: , "tnum"; }
.slashed-zero   { --ff-extra: , "zero"; }
.stylistic-g    { --ff-extra: , "cv05", "ss02"; }
```

Custom properties merge through `--ff-extra` leading-comma. Gives you a composable base + extras model. The pattern is a common "fix" for libraries that must use `font-feature-settings` because stylistic sets / character variants aren't variant-addressable.

**4. Scope `font-feature-settings` only to the element that needs it, not to ancestors.** If only `.stat-counter` needs tabular numbers, put `font-feature-settings: "tnum"` on `.stat-counter` directly — don't put any `font-feature-settings` on `body`.

### Inheritance

Both properties inherit. A declaration on `<html>` or `<body>` reaches all descendants. With `font-feature-settings`, this inheritance is of a **single value** — the entire comma-separated list is inherited as one. With `font-variant-*`, each longhand inherits independently, and later declarations merge additively with the inherited set (as long as axes don't collide).

### Animation

`font-feature-settings` and `font-variant-*` both animate **discretely** — there is no half-ligated glyph. Setting a transition on them produces a step change at the 50% mark. This is distinct from `font-variation-settings` (see `./variable-fonts.md`) which *does* interpolate.

### Interaction with `font-kerning`

`font-kerning: none` will disable kerning regardless of `font-feature-settings: "kern"`. The high-level property wins for `kern` *specifically* because the spec gives `font-kerning` precedence over the underlying tag. This is the one case where high-level beats low-level without ambiguity.

### Variable fonts + features

OpenType features and variable axes compose independently. You can `font-variation-settings: "wght" 700` and `font-variant-numeric: tabular-nums` on the same element and both apply — the shaper picks `tnum`-targeted glyphs (often just metric adjustments, rarely full-glyph substitutions), and the variation engine produces the 700-weight outline. See `./variable-fonts.md` for the full interaction model.

## Anti-patterns

| Pattern | Why it's wrong | Fix |
|---|---|---|
| Disabling `rlig` | Produces malformed Arabic (no lam-alif), Devanagari, etc. | Do not touch `rlig`. Use `font-variant-ligatures: no-common-ligatures` at worst, which leaves `rlig` on. |
| Disabling `init`/`medi`/`fina`/`isol` to "simplify" Arabic rendering | Arabic relies on these for every letter's contextual form. Disabling produces isolated-form chains. | Leave all shaping features alone. Use `lang="ar"` and a real Arabic font. |
| `font-feature-settings: "tnum"` on a parent that also needs `kern` / `liga` | Replaces the parent's feature list entirely — `kern` and `liga` wink off (depending on UA merging semantics). | Use `font-variant-numeric: tabular-nums` on the child. Or use the custom-property compose pattern. |
| Enabling `dlig` by default on UI body | Discretionary ligatures produce "ct" and "st" joins that look odd in UI text; also affect serial numbers and codes unpredictably. | Leave `dlig` off for body/UI. Enable on editorial headlines by opt-in. |
| `font-feature-settings: "ss01"` without `@font-feature-values` | Works, but is font-family-specific — the same author code breaks when the font is swapped. Maintainability hazard. | `@font-feature-values` + `font-variant-alternates: styleset(named)` is more portable. `font-feature-settings` is fine for in-house use. |
| Synthesized small caps when the font has `smcp` | CSS synthesizes by scaling caps — thinner stems, off balance. Real `smcp` glyphs are weight-compensated. | Use `font-variant-caps: small-caps` so the shaper picks real glyphs if present. Fall back to synthesis only when necessary. |
| `font-variant: small-caps` in place of `font-variant-caps: small-caps` | The shorthand resets every other variant longhand — numeric, ligatures, etc. all revert. | Use the longhand. |
| Forgetting `lang` attributes | `locl` won't fire — Turkish renders Romanized, Serbian Cyrillic renders in Russian forms, Dutch IJ doesn't tighten, Chinese renders in Japanese Han forms. | Declare `lang` on `<html>` and override on inline content switches. Use BCP 47 subtags for script/region disambiguation (`zh-Hans`, `zh-Hant`). |
| `font-feature-settings: "vert"` in horizontal text | Emits rotated punctuation on a horizontal baseline — garbage. | Use `writing-mode: vertical-rl` for vertical text; the shaper handles `vert`/`vrt2` automatically. |
| Enabling `frac` globally | Mangles version numbers, aspect ratios, dates (`1/24` becomes a fraction). | Scope `frac` tightly to `.fraction` spans only. |
| `font-feature-settings: "wdth" 85` | `wdth` is a variable-font *axis* tag, not an OT feature tag. Goes in `font-variation-settings`, not `font-feature-settings`. | `font-variation-settings: "wdth" 85` or `font-stretch: 85%`. |
| `font-feature-settings: "liga" 0` to try to disable icon-font ligatures globally | Also kills standard text ligatures for all content. | Scope to the icon element: `.icon { font-feature-settings: "liga" 0; }`. |
| Mixing `font-feature-settings` and `font-variant-*` on the same element | `font-feature-settings` has higher precedence for its listed tags; the variant longhands apply only for tags not listed. Subtle wins/losses. | Pick one layer and stay in it. Prefer variant longhands. |
| Using `font-feature-settings: "kern"` instead of `font-kerning: normal` | `font-kerning` is the dedicated property — more cascadable and legible. | Use `font-kerning`. |
| Relying on `font-variant-emoji` for presentation in Chromium pre-125 | Chromium only shipped `font-variant-emoji` in version 125 (2024-06). Before that, no effect. | Check caniuse; supply Unicode variation selector fallback (`U+FE0E` for text, `U+FE0F` for emoji presentation) if you need pre-2024 support. |
| Dropping `ccmp` or `mark` via explicit feature-settings off | `ccmp` is load-bearing for decomposed-Unicode rendering; `mark` is load-bearing for diacritic positioning. | Never disable. If you didn't intend to, you shouldn't have turned `font-feature-settings` on. |

## Sources

- Microsoft Learn. "OpenType Feature Tags (Registered features)." https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist (retrieved 2026-04-17).
- Microsoft Learn. "OpenType Layout tag registry — Feature file: Features a-e, f-j, k-o, p-t, u-z." https://learn.microsoft.com/en-us/typography/opentype/spec/features_ae through `..._uz` (retrieved 2026-04-17).
- Microsoft Learn. "Stylistic Sets 1–20 feature records." Same source series.
- Microsoft Learn. "Character Variants 1–99 feature records." Same source series.
- W3C. "CSS Fonts Module Level 3." W3C Recommendation, 2018-09-20. https://www.w3.org/TR/css-fonts-3/.
- W3C. "CSS Fonts Module Level 4." W3C Working Draft, 2026-03-03. https://www.w3.org/TR/css-fonts-4/ (retrieved 2026-04-17).
- W3C CSS Working Group. "CSS Fonts Module Level 5 Editor's Draft." https://drafts.csswg.org/css-fonts-5/ (retrieved 2026-04-17).
- MDN Web Docs. "font-feature-settings." https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings (retrieved 2026-04-17).
- MDN Web Docs. "font-variant, font-variant-ligatures, font-variant-numeric, font-variant-caps, font-variant-alternates, font-variant-position, font-variant-east-asian, font-variant-emoji." Full property index at https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant (retrieved 2026-04-17).
- MDN Web Docs. "@font-feature-values." https://developer.mozilla.org/en-US/docs/Web/CSS/@font-feature-values (retrieved 2026-04-17).
- MDN Web Docs. "font-kerning." https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning (retrieved 2026-04-17).
- caniuse.com. "font-variant-numeric." https://caniuse.com/font-variant-numeric (2026-04 snapshot).
- caniuse.com. "font-variant-east-asian." https://caniuse.com/font-variant-east-asian (2026-04 snapshot).
- caniuse.com. "font-variant-alternates." https://caniuse.com/font-variant-alternates (2026-04 snapshot).
- caniuse.com. "font-feature-settings." https://caniuse.com/font-feature (2026-04 snapshot).
- caniuse.com. "@font-feature-values." https://caniuse.com/mdn-css_at-rules_font-feature-values (2026-04 snapshot).
- caniuse.com. "font-variant-emoji." https://caniuse.com/mdn-css_properties_font-variant-emoji (2026-04 snapshot).
- Richard Rutter. "OpenType features in web browsers — test results and practical guide." clagnut.com, 2020–ongoing. https://clagnut.com/blog/2380 (retrieved 2026-04-17).
- Roel Nieskens. "Wakamai Fondue — inspect any OpenType font's features in the browser." https://wakamaifondue.com/ (retrieved 2026-04-17).
- Sparanoid. "OpenType Features — exhaustive demonstration." https://sparanoid.com/lab/opentype-features/ (retrieved 2026-04-17).
- Unicode Consortium. "UTR #53: Unicode Arabic Mark Rendering." https://unicode.org/reports/tr53/.
- Rasmus Andersson. "Inter — feature catalog." rsms.me/inter (specimen + stylistic-set legend).
- Grilli Type (GT). "GT America — type specimen with stylistic-set legend." https://www.grillitype.com/typeface/gt-america (retrieved 2026-04-17).
- Commercial Type. "Graphik — type specimen." https://commercialtype.com/catalog/graphik (retrieved 2026-04-17).
- Klim Type Foundry. "Söhne — type specimen." https://klim.co.nz/retail-fonts/soehne/ (retrieved 2026-04-17).
- Nick Sherman. "Variable-Font catalog." https://v-fonts.com/ (cross-references for variable + feature coexistence).
- David Jonathan Ross. "Input — contextual alternates in monospace design." djr.com/input (retrieved 2026-04-17).
- Underware Type Design. "Liza Pro — contextual alternates and randomization in script type." https://underware.nl/fonts/liza/ (retrieved 2026-04-17).
- HarfBuzz documentation. "OpenType shaping models." https://harfbuzz.github.io/shaping-opentype.html (retrieved 2026-04-17).
