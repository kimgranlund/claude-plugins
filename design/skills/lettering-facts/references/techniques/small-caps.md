---
date: 2026-04-18
coverage: light
peers:
  - ../contemporary/opentype-features.md
  - ../contemporary/css-text-properties.md
  - ./figures.md
primary_sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt
  - https://www.w3.org/TR/css-fonts-4/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis-small-caps
  - https://caniuse.com/font-variant-alternates
  - https://practicaltypography.com/small-caps.html
  - https://webtypography.net/3.2.3
  - https://clagnut.com/blog/2380
  - https://rsms.me/inter/
  - https://wakamaifondue.com/
notes:
  - This file is the entry-level reference for small caps — the distinction between real and synthesized caps, the CSS surface that exposes the OpenType `smcp`/`c2sc`/`pcap`/`c2pc` features, and the editorial conventions for when small caps belong. Full OpenType tag catalog is in `../contemporary/opentype-features.md`; this file cross-refers rather than duplicates.
---

# Small caps — technique reference

**Coverage tier**: light
**Last verified**: 2026-04-18
**Sources**: OpenType spec (Microsoft registry, 2024-05 snapshot), W3C CSS Fonts L4 (WD 2026-03-03), MDN `font-variant-caps` and `font-synthesis-small-caps` (retrieved 2026-04-18), Butterick *Practical Typography* §small-caps, Rutter *Web Typography* §3.2.3, caniuse 2026-04.
**Peer files**: `../contemporary/opentype-features.md`, `../contemporary/css-text-properties.md`, `./figures.md`.

Covers real vs synthesized small caps, the CSS surface for capital-to-smallcap and lowercase-to-smallcap substitution, the OpenType feature tags involved, and the editorial rules for when small caps are the right answer. Out of scope: the broader OpenType tag taxonomy and `font-variant-*` vs `font-feature-settings` precedence (see `../contemporary/opentype-features.md`).

---

## What Small Caps Are

Small caps are caps-shaped glyphs sized to match the x-height (or slightly above) of the running text — letters that have the silhouette of uppercase but the visual mass of lowercase. They are drawn by the type designer alongside the regular uppercase and lowercase, with stroke weights adjusted so they sit evenly against the lowercase field they live in.

The use cases are narrow but traditional: acronyms and initialisms inside prose (`NASA`, `CSS`, `HTML`), centuries rendered with ordinal suffixes (`19TH century`), honorifics and abbreviations (`MR.`, `MRS.`, `ET AL.`, `IBID.`, `P.M.`, `A.D.`), stylistic emphasis in editorial typesetting, running heads in books, section-label and figure-caption text, and occasional brand-identity settings. Small caps are designed for *short runs* — a word, a few words, a label — and they fail as a full-sentence setting because the even visual color collapses into monotony past a line or two.

---

## Real Small Caps vs Fake Small Caps

This is the single most load-bearing distinction. A real small cap is a glyph the designer drew; a fake small cap is a browser scaling an uppercase glyph down to small-cap size.

### Real (true) small caps

The font contains dedicated glyphs for each small cap, cut by the type designer at the size they will display. The OpenType features `smcp` (substitute lowercase → small cap) and `c2sc` (substitute uppercase → small cap) activate the substitution. Because the glyphs are purpose-drawn, their stroke weight is adjusted to match the surrounding lowercase — they do not look thin, and the sidebearings are tuned to space evenly against lowercase letters.

### Fake (synthetic) small caps

The browser takes the uppercase glyph, shrinks it to roughly small-cap height, and presents that as the small cap. The result is predictably wrong: the stroke weight is proportional to the uppercase design, so when the glyph shrinks, the strokes shrink with it. What sat at body weight next to lowercase now reads as a hairline against the same lowercase — visibly thinner, visibly off-balance.

### Visual test

Set `MR. NATO` with real small caps from a font that carries `smcp`, and set the same string with synthetic small caps from a font that doesn't. Compare the stroke weight of any capital letter against the small-cap version of the same letter in the same word. If the stroke weights match, it's real. If the small cap is demonstrably thinner, it's synthetic.

### What CSS does when the font lacks `smcp`

Per CSS Fonts L4 §6, the browser *must* fall back to synthesis when `font-variant-caps: small-caps` is declared and the font has no `smcp` table. Chromium and WebKit both synthesize; Firefox synthesizes. The synthetic version is a compliance behavior, not an aesthetic choice — the browser is required to do *something*, and the something is the scaled-uppercase approach.

### Disabling synthesis

`font-synthesis-small-caps: none` (CSS Fonts L4, Baseline since 2022) disables the browser's fallback to synthetic small caps. With `font-synthesis-small-caps: none` on an element that requests small caps and a font that lacks `smcp`, the element renders in plain lowercase — no substitution at all. This is useful in publication workflows where you want to *catch* the failure rather than ship synthetic: either the font supports small caps and you get real ones, or it doesn't and you see the fallback immediately.

```css
* { font-synthesis-small-caps: none; }  /* refuse synthetic small caps project-wide */
```

---

## CSS

### `font-variant-caps` — the right property

```css
.acronym   { font-variant-caps: small-caps; }         /* lowercase → small cap */
.all-caps  { font-variant-caps: all-small-caps; }     /* upper + lower → small cap */
.petite    { font-variant-caps: petite-caps; }        /* lowercase → petite cap (smaller) */
.all-petite { font-variant-caps: all-petite-caps; }   /* upper + lower → petite cap */
.titling   { font-variant-caps: titling-caps; }       /* designer's titling-style caps */
.unicase   { font-variant-caps: unicase; }            /* mixed height single band */
```

The seven values:

- `small-caps` — emits `smcp`. Converts lowercase to small caps; leaves uppercase unchanged.
- `all-small-caps` — emits `smcp` + `c2sc`. Converts both lowercase and uppercase to small caps. The common editorial setting for all-caps runs ("section labels", "standfirsts", "figure captions") that should read quieter than body but retain caps' even color.
- `petite-caps` — emits `pcap`. Like `smcp` but smaller (around x-height, not slightly above). Rare.
- `all-petite-caps` — emits `pcap` + `c2pc`. Like `all-small-caps` but with petite caps. Rare.
- `titling-caps` — emits `titl`. Not small caps; substitutes the font's titling-style caps for uppercase. Useful for display-size all-caps that want the designer's refined titling cut rather than the body caps.
- `unicase` — emits `unic`. A mixed-height single-band alphabet. Display-only; very rare.
- `normal` — explicit default; disables any of the above.

### `font-feature-settings` — the low-level fallback

```css
.acronym  { font-feature-settings: "smcp"; }
.all-caps { font-feature-settings: "smcp", "c2sc"; }
```

Same OpenType tags, different cascade semantics. `font-feature-settings` declarations **replace** across ancestry, wiping out any inherited features (`kern`, `liga`, `calt`). Prefer `font-variant-caps` for everything it covers. See `../contemporary/opentype-features.md` §Precedence.

### Legacy `font-variant: small-caps`

The shorthand `font-variant: small-caps` still works in every browser, but it **resets every other `font-variant-*` longhand** to its initial value — `font-variant-numeric`, `font-variant-ligatures`, `font-variant-alternates`, `font-variant-position` all snap back to default. Any numeric or alternates setting you had applied above is lost. Always use `font-variant-caps: small-caps` instead. See `../contemporary/opentype-features.md` §The `font-variant` shorthand for the reset-behavior warning.

---

## OpenType Feature Tags

| Tag | Name | What it does |
|---|---|---|
| `smcp` | Small Capitals | Substitutes lowercase glyphs with small-cap forms sized near x-height to slightly above. |
| `c2sc` | Capitals to Small Capitals | Substitutes uppercase glyphs with small-cap forms. Paired with `smcp` for `all-small-caps`. |
| `pcap` | Petite Capitals | Like `smcp` but smaller — caps sized at or near x-height without the cap-compensating rise. |
| `c2pc` | Capitals to Petite Caps | Paired with `pcap` for `all-petite-caps`. |
| `titl` | Titling Capitals | Not small caps — substitutes uppercase with the designer's dedicated titling cut, usually refined for display sizes. |
| `unic` | Unicase | Mixed upper/lowercase chosen for uniform height in one band. Display-only. |
| `case` | Case-Sensitive Forms | Adjusts punctuation (parentheses, brackets, dashes) to align with cap height when text is all-caps or all-small-caps. Does not change letters. No `font-variant-*` surface; use `font-feature-settings: "case"`. |

Full catalog in `../contemporary/opentype-features.md` §Case, Small Caps.

**The `case` interaction.** When setting all-small-caps with adjacent punctuation, the punctuation glyphs are still sized for lowercase (parens sit at x-height), which looks wrong alongside cap-height glyphs. `font-feature-settings: "case"` raises the punctuation to match. Combined:

```css
.acronym-block {
  font-variant-caps: all-small-caps;
  font-feature-settings: "case";
}
```

---

## Browser Support

| Property | Ships on | Baseline | Notes |
|---|---|---|---|
| `font-variant-caps: small-caps \| all-small-caps` | Chrome 52+, Firefox 34+, Safari 9.1+, Edge 79+ | Baseline January 2020 | Every engine respects real `smcp`/`c2sc` if the font carries them; synthesizes otherwise. |
| `font-variant-caps: petite-caps \| all-petite-caps` | All above | Same | Few fonts carry `pcap`; mostly synthesizes. |
| `font-variant-caps: titling-caps` | All above | Same | Requires `titl` in the font. |
| `font-variant-caps: unicase` | All above | Same | Requires `unic` in the font. Rare. |
| `font-synthesis-small-caps` | Chrome 97+, Firefox 111+, Safari 16.4+, Edge 97+ | Baseline since 2022 | Disable synthesis explicitly. |
| `font-synthesis: none` | All above | Same | Disables weight, style, small-caps, position synthesis together. |
| Legacy `font-variant: small-caps` | Everywhere since IE 8 | — | Resets other `font-variant-*` — avoid. |

---

## Fonts with Real Small Caps

### Serifs (most reliable)

- **Adobe Pro and Premier families:** Garamond Premier Pro, Minion Pro, Adobe Jenson Pro, Adobe Caslon Pro, Adobe Text Pro, Warnock Pro. All carry `smcp` + `c2sc`, most also `pcap` + `c2pc` plus `case`.
- **Open-source serifs:** IBM Plex Serif, Source Serif 4, Fraunces (variable-font, carries `smcp` + `c2sc`), Literata, Cardo, PT Serif (partial — `smcp` yes, `c2sc` varies by weight), Merriweather (partial), EB Garamond (full set).
- **Classic book faces:** Bembo, Sabon, Perpetua, Janson, Centaur — all in their Pro-licensed forms.
- **Screen serifs:** Georgia — no small caps. Charter — yes in Pro version. Iowan Old Style — yes in premium licenses.

### Sans-serifs (less reliable)

- **Premium sans with small caps:** Gill Sans MT Pro, FF Meta, Futura OT Pro, FF DIN Pro, Akkurat Pro, Helvetica Now, Suisse Int'l (in paid licenses).
- **Open-source sans with small caps:** Inter (full `smcp` + `c2sc`), Source Sans 3 (full), IBM Plex Sans (full), Noto Sans (partial — `smcp` yes, `c2sc` varies).
- **Open-source sans without small caps:** Roboto — no `smcp`. DM Sans — no. Work Sans — no. Most of the single-weight Google Fonts families ship without small caps.

### System UI fonts

- **SF Pro / San Francisco** (Apple) — carries `smcp` + `c2sc` in `SF Pro Text`. `SF Pro Display` partial.
- **Segoe UI** (Windows) — no small caps.
- **Ubuntu** — no small caps.
- **Helvetica Neue** (legacy system) — no small caps in the system-bundled version.

**Verification:** drop the font into [Wakamai Fondue](https://wakamaifondue.com/) and check the feature list for `smcp` and `c2sc`. Or visually compare real caps against small caps in the same word — if the small cap is thinner, synthesis is happening.

---

## When Small Caps Are Right

- **Acronyms in prose.** `NATO`, `ISO`, `HTTP`, `CSS`, `NASA` — acronyms inside running text read better in small caps than in full caps. Full-caps acronyms shout through a paragraph; small caps sit evenly. The convention is more editorial-British than US-tech — most US tech publications leave acronyms in full caps — but it is the canonical typographic move. (See `../contemporary/opentype-features.md` §Case, Small Caps for the regional note.)
- **Centuries and eras.** `19TH century`, `18TH-century painting` — set the century abbreviation in small caps with the suffix as a small cap (or as a raised superior). Standard in academic and literary editorial.
- **Honorifics and abbreviations.** `MR.`, `MRS.`, `DR.`, `REV.`, `ET AL.`, `IBID.`, `OP. CIT.`, `P.M.`, `A.M.`, `A.D.`, `B.C.`, `C.E.`, `B.C.E.` — small caps are the traditional setting. `font-feature-settings: "case"` for the period punctuation.
- **Running heads and page headers.** Book design convention — chapter titles or section names rendered in small caps in the page header.
- **Drop caps + small caps.** The classical chapter-opening setting is a drop cap on the first letter, the next few words in small caps, then body lowercase. The small-caps run acts as a typographic lead-in. See `../contemporary/css-text-properties.md` §`initial-letter` for the drop-cap surface.
- **Section labels and figure captions.** All-small-caps for an even typographic color that reads quieter than full caps but denser than mixed case.
- **Stylistic emphasis.** In editorial typesetting, small caps replace italics for some emphasis contexts — quieter than italics, more typographic than bold.

### When small caps are wrong

- **Full sentences.** Small caps are designed for short runs. A paragraph in small caps reads as a single undifferentiated band; there is no silhouette contrast to anchor word-shape reading, and fatigue sets in within a few lines.
- **UI body text.** Outside editorial contexts, small-caps acronyms confuse users who read them as a visual style rather than as abbreviations. Full caps are the web default for a reason.
- **Inside code or data.** Small caps inside a tabular data cell or a monospaced code field looks broken.

---

## Tracking

Small caps typically need positive `letter-spacing` to breathe — the shorter vertical rise means the glyphs sit closer together than uppercase would, and default tracking can look cramped.

```css
.acronym {
  font-variant-caps: all-small-caps;
  letter-spacing: 0.05em;
}
```

Conventional values: **0.04–0.08em** positive tracking for all-small-caps runs. Some designers go to 0.1em for display contexts. Any higher and the letters start to float apart.

**Font-specific tuning:** some fonts pre-space their small-caps glyphs with additional sidebearings already applied. On those fonts, adding 0.05em produces visible gaps. Always check the specimen before applying project-wide tracking rules.

**Letter-spacing disables ligatures.** A well-known side effect in Blink and WebKit: setting any non-normal `letter-spacing` disables standard ligatures (`liga`, `clig`). With small caps this is usually fine — small caps rarely contain ligated pairs — but if the surrounding text inherits the tracking (an `.all-small-caps` class on a paragraph containing a `<span>` with lowercase), ligatures break. See `../contemporary/css-text-properties.md` §`letter-spacing` for the full caveat.

---

## Accessibility

Screen readers read small caps as the lowercase letter names (`nato` in small caps reads as "nato", not "N-A-T-O") because the underlying character stream is lowercase. There is no "shouting" effect for assistive technology — small caps are invisible to non-visual output.

This has two consequences:

- **No WCAG issue per se.** Small caps don't affect contrast, spacing, or text resize. WCAG 2.2 has no SC that targets small-caps rendering.
- **Semantic meaning must live in markup.** If small caps encode meaning (a `WARNING` set in small caps denoting an alert; a character-name `MR. HOLMES` in small caps denoting honorific), the meaning must also be in the DOM or in an `aria-label`. Visual typography and semantic markup are orthogonal.

```html
<span aria-label="Mister Holmes">
  <span style="font-variant-caps: all-small-caps;">Mr. Holmes</span>
</span>
```

---

## Common Traps

- **Using `text-transform: uppercase` + `font-size: 0.8em` to fake small caps.** Always looks thin and wrong. The stroke weight is reduced proportionally with the font-size, so the "small cap" is a hairline version of the uppercase. Fix: use `font-variant-caps: small-caps` on a font that carries `smcp`.
- **`font-variant: small-caps` instead of `font-variant-caps: small-caps`.** The shorthand resets all other `font-variant-*` longhands. Fix: always use the longhand.
- **Assuming `small-caps` produces real small caps.** Per spec, the browser must synthesize when the font lacks the feature. On Roboto, DM Sans, Segoe UI — all of which lack `smcp` — you get synthetic small caps. Fix: verify font support; use `font-synthesis-small-caps: none` to catch the failure if you want to refuse synthesis.
- **Small caps followed by a number in different style.** `NATO 1949` with all-small-caps and lining proportional digits: the number reads at cap-height, which is taller than the small-caps, creating visual inconsistency. Fix: set `font-variant-numeric: lining-nums` explicitly on the mixed run, or accept the inconsistency, or avoid the mix.
- **Punctuation at lowercase height inside all-small-caps runs.** `(NATO)` with `font-variant-caps: all-small-caps` leaves the parentheses at x-height while the letters are at small-cap height — the parens look sunken. Fix: `font-feature-settings: "case"` in addition to `font-variant-caps`.
- **Running small caps without tracking.** Cramped. Fix: add 0.04–0.08em of positive `letter-spacing` (and accept the ligature suppression side effect).
- **Disabling synthesis without a fallback plan.** `font-synthesis-small-caps: none` on an element with a font that lacks `smcp` renders plain lowercase. If you didn't expect that, it looks like a missing style. Fix: use the declaration deliberately, either to catch the failure or as part of a font-stack QA policy.

---

## Sources

- Microsoft Learn. "OpenType Feature tags: smcp, c2sc, pcap, c2pc, titl, unic, case." OpenType Feature Registry. [learn.microsoft.com/en-us/typography/opentype/spec/featurelist](https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist). Retrieved 2026-04-18.
- W3C CSS Working Group. "CSS Fonts Module Level 4." Working Draft, 2026-03-03. [w3.org/TR/css-fonts-4](https://www.w3.org/TR/css-fonts-4/).
- MDN Web Docs. "font-variant-caps." [developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps). Retrieved 2026-04-18.
- MDN Web Docs. "font-synthesis-small-caps." [developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis-small-caps](https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis-small-caps). Retrieved 2026-04-18.
- MDN Web Docs. "font-synthesis (shorthand)." [developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis](https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis). Retrieved 2026-04-18.
- caniuse.com. "font-variant-alternates and CSS variants." [caniuse.com/font-variant-alternates](https://caniuse.com/font-variant-alternates). 2026-04 snapshot.
- Butterick, M. *Practical Typography* — "Small caps." [practicaltypography.com/small-caps.html](https://practicaltypography.com/small-caps.html). Retrieved 2026-04-18.
- Richard Rutter. *Web Typography* §3.2.3 — "Small capitals." [webtypography.net/3.2.3](https://webtypography.net/3.2.3). Retrieved 2026-04-18.
- Richard Rutter. "OpenType features in web browsers — test results and practical guide." [clagnut.com/blog/2380](https://clagnut.com/blog/2380). Retrieved 2026-04-18.
- Bringhurst, R. *The Elements of Typographic Style*, 4th edition. Hartley & Marks, 2013. (Chapter 3 on small caps.)
- Rasmus Andersson. "Inter — feature catalog." [rsms.me/inter](https://rsms.me/inter/). Retrieved 2026-04-18.
- Roel Nieskens. "Wakamai Fondue." [wakamaifondue.com](https://wakamaifondue.com/). Retrieved 2026-04-18.
