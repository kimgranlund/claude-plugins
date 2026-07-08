---
date: 2026-04-18
coverage: medium
peers:
  - ./wcag-type.md
  - ./dyslexia.md
  - ./cognitive.md
  - ../science/crowding.md
  - ../techniques/measure.md
  - ../../../color-science-accessibility/references/techniques/apca-lc-formula.md
primary_sources:
  - https://www.w3.org/TR/WCAG22/
  - https://www.who.int/publications/i/item/9789241516570  # WHO World Report on Vision, 2019
  - https://www.nei.nih.gov/learn-about-eye-health/outreach-resources/eye-health-data-and-statistics
  - https://www.aph.org/app/uploads/2017/10/APH-Large-Print-Guidelines.pdf
  - https://www.rnib.org.uk/professionals/accessibility/clear-print-guidelines/
  - https://apcacontrast.com/
  - https://readtech.org/ARC/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
---

# Low-vision typography — accessibility reference

**Peers:** [WCAG 2.2 type success criteria](./wcag-type.md) for the legal floor (SC 1.4.3 / 1.4.4 / 1.4.8 / 1.4.10 / 1.4.12) that grounds every recommendation here. [Dyslexia evidence](./dyslexia.md) and [cognitive accessibility](./cognitive.md) cover adjacent populations with partially overlapping but distinct needs. The crowding substrate — [`science/crowding.md`](../science/crowding.md) — explains *why* spacing interventions that help dyslexic readers also help macular-degeneration readers reading with peripheral retina.

Low vision is not blindness. Low-vision users read — typically with magnification, higher contrast, and assistive tech layered under or over the browser. Typography is one layer of the accessibility stack; the typographer's job is to produce text that **survives** zoom, override, and polarity inversion without breaking. This file catalogues what typography can do for low-vision readers, what it cannot, and the specific patterns that earn the most real-world benefit per unit of design effort.

---

## Part 1 — What "low vision" means

### Clinical definition

The WHO defines **low vision** as visual acuity in the better eye, with best possible correction, of worse than 6/18 (Snellen 20/60) but better than 3/60 (20/400), or a visual field of less than 20° — a functional deficit that **cannot be corrected by glasses, contact lenses, surgery, or medication** and that falls short of "blindness." The practical US framing commonly cited by the National Eye Institute is **visual acuity of 20/70 or worse, best-corrected**, paired with contrast-sensitivity loss, visual-field loss, or light sensitivity.

Three independent axes of functional loss matter for typography:

- **Acuity loss** — fine detail resolution. Below threshold, text cannot be resolved even when magnified.
- **Contrast-sensitivity loss** — ability to distinguish tones close in luminance. Often disproportionate to acuity loss; the most under-measured variable in accessibility.
- **Visual-field loss** — central (scotoma), peripheral (tunnel), hemifield, or scattered. Each imposes different reading strategies.

A fourth axis — **photophobia** (light sensitivity) — is orthogonal but drives strong preferences for dark-mode, reduced whites, and tinted backgrounds.

### Prevalence

- **~246 million** people globally had moderate-to-severe visual impairment in the WHO 2019 world report, with another ~36 million blind. The 2023 *Lancet Global Health* update revised these upward as population ageing has outpaced the rollout of cataract surgery and diabetic-retinopathy screening. Projected totals for 2030 cluster around **295–330 million** with low vision.
- **United States:** NEI estimates ~**7.3 million people** with uncorrectable vision loss as of 2022, of whom ~1 million are legally blind. The figure roughly doubles by 2050 on current demographic trends.
- **Ageing drives the curve.** Prevalence is <1% below age 40 and >25% above age 80 in most Western populations. Age-related macular degeneration (AMD) alone affects ~**11 million US adults** and is the leading cause of low vision in people over 60.

Practitioner consequence: low-vision accommodations are not edge-case work. Any consumer product with adult users has a low-vision cohort in the single-to-double-digit percent, rising sharply with audience age.

### Major conditions and their typographic consequences

- **Age-related macular degeneration (AMD).** Central-vision loss. Readers develop a **preferred retinal locus** (PRL) in the parafoveal or peripheral retina. Reading with the PRL is **crowding-limited, not acuity-limited** (see [`../science/crowding.md`](../science/crowding.md)): letters are resolvable but cannot be identified when closely flanked. Levers that *reduce crowding* (increased letter-spacing, larger x-height, shorter measure) disproportionately help AMD readers; sheer size alone helps much less than expected.
- **Glaucoma.** Peripheral-field loss; foveal acuity often preserved. Readers retain letter identification inside the surviving island but lose next-line preview and line-return tracking. At 400% zoom, only a couple of letters fit inside the surviving field. Short lines and generous paragraph spacing help.
- **Diabetic retinopathy.** Scattered scotomas; contrast sensitivity deteriorates before acuity. Readers see patchy letter blanks and may struggle with thin-stroke fonts. Higher weight, high contrast, generous spacing. Contrast requirements sit meaningfully above the WCAG AA floor.
- **Cataract.** Generalised blur plus contrast-sensitivity loss, often with glare sensitivity. The most common cause of reversible low vision globally. Typography: high contrast; avoid very thin weights; avoid high-luminance white backgrounds that amplify glare.
- **Retinitis pigmentosa.** Progressive rod-then-cone degeneration producing night blindness and tunnel vision. Similar consequences to glaucoma for advanced cases.
- **Albinism, achromatopsia, nystagmus.** Congenital low acuity and/or light sensitivity. Aggressive magnification from early school age. Stable layouts that survive 200%+ zoom without reflow jumps matter more than absolute contrast ratios.
- **Cortical / cerebral visual impairment.** Damage to visual-processing areas; the eye is intact but perception is impaired. Overlaps with [`./cognitive.md`](./cognitive.md).

Practitioner rule: **do not design for one condition and call it "low-vision accessible."** AMD and photophobic users have opposing preferences on background luminance; glaucoma and cataract users want different tracking defaults. Respect user preferences and let individuals select.

---

## Part 2 — What typography can and cannot do

### What typography can do

- **Increase readable size** — up to the user's preferred default. `rem`-based sizing that scales with the user's browser default is the structural lever; absolute `px` body text is the most common failure mode.
- **Survive magnification** — structural flexibility so that zoom (browser zoom, OS magnification, screen readers) does not clip, overlap, or reflow destructively. WCAG SC 1.4.4 (200%) and 1.4.10 (reflow at 320 CSS px) are the auditable floors.
- **Provide adequate contrast** — AA is the floor; AAA and APCA Lc ≥75 are the low-vision-friendly targets. Polarity-aware design (dark on light vs light on dark) matters more than the 2.x luminance ratio implies.
- **Respect spacing overrides** — SC 1.4.12 is an override-tolerance criterion, not a design target. Layouts must not break when the user applies the text-spacing bookmarklet.
- **Honour user media queries** — `prefers-contrast`, `prefers-color-scheme`, `prefers-reduced-motion`, `forced-colors`. Typography should *respond* to these, not fight them.
- **Offer differentiated letterforms** — fonts designed for low-vision (Atkinson Hyperlegible, Maxular Rx, Eido) improve character identification at small or peripheral sizes. Marginal benefit above a well-chosen general sans-serif, but real.

### What typography cannot do

- **Restore visual acuity below the acuity threshold.** At some combination of size and distance, no typography rescues a user who cannot resolve the letters at that angular size. Screen magnifiers (ZoomText, macOS Zoom, Windows Magnifier) and tactile/auditory assistive tech are the rest of the stack.
- **Compensate for dense central scotoma.** A user with bilateral foveal scotoma is reading with non-foveal retina. Typography can optimise for crowding reduction — the governing bottleneck there — but cannot reconstruct foveal reading rates.
- **Replace screen readers.** Readers with severe low vision often combine magnification with synthesised speech. Typography's job is not to substitute for the screen-reader layer; it's to not get in its way (live text not images, correct `lang`, proper semantic structure).
- **Override user operating-system settings.** On iOS, Android, macOS, and Windows, the user's preferred text size is an OS setting. Typography that uses `font-size: 14px !important` breaks this.
- **Solve glare or photophobia** via black-on-white alone. True photophobia is managed with dark-mode schemes and reduced whites — see §4.

### The stack

Typography sits inside a chain: OS scale/font-size preference → browser default and zoom → assistive tech (ZoomText, MAGic, JAWS, NVDA, VoiceOver, TalkBack, user stylesheet) → the page CSS → rendered glyphs under subpixel rendering and ambient lighting. Typography's contract is to be the *least brittle* layer. Absolute units, fixed heights, overflow-hidden containers, and `!important` rules all reduce robustness.

---

## Part 3 — Evidence-based recommendations for body text

### Size

- **Minimum 16 CSS px / 12pt** for body text. Below 14 CSS px is a legibility smell regardless of contrast ratio.
- **18 CSS px / 14pt preferred** for reading-heavy surfaces and audiences skewing older.
- **Low-vision users typically read at 200–400% zoom.** The *responsive behaviour* of the layout at high zoom matters more than the absolute design-time size.
- Use `rem` — never `px` — for body text. `rem` inherits from the user's root default; `px` does not.

Anti-pattern: `html { font-size: 10px }` to make `1rem` a convenient unit. This **breaks the user's preferred-size override**. Users who set their browser default to 24px expect body text at 24px; the 10px root makes the same "1.6rem" declaration render 16px instead of 38.4px. Use `rem` with a `100%` root.

### Contrast

- **WCAG 2.2 SC 1.4.3 (Minimum) — AA — 4.5:1** for body, **3:1** for large text. Legal floor; see [`./wcag-type.md §SC 1.4.3`](./wcag-type.md#sc-143-contrast-minimum--level-aa).
- **WCAG 2.2 SC 1.4.6 (Enhanced) — AAA — 7:1 / 4.5:1.** Better for reading-heavy surfaces and for mild low-vision readers. Cost of hitting AAA is usually a darker body colour (`#222` or `#1a1a1a` rather than `#333`) and a matching adjustment on links.
- **APCA ≥ Lc 75** for body (16 px / 400 weight), **Lc 60** for large text or bold body. Not a conformance target as of 2026-04 — but it is the polarity-aware check that catches the "light-on-dark at the WCAG floor" trap. See [`../../../color-science-accessibility/references/techniques/apca-lc-formula.md`](../../../color-science-accessibility/references/techniques/apca-lc-formula.md).

AMD and diabetic-retinopathy readers benefit from higher contrast than the AA floor provides. If your audience skews >60, design to AAA or APCA Lc 75 as the default body contrast, not as an accommodation mode.

Contrast is not the only thing: a 21:1 pair of `#000` on `#fff` with thin-weight 12px type is worse for AMD readers than a 7:1 pair at 18px/500-weight. Contrast, size, and weight trade off in a way the WCAG 2.x formula does not model (APCA does, partially; see [`./wcag-type.md §APCA`](./wcag-type.md#apca--accessible-perceptual-contrast-algorithm)).

### Line length (measure)

- **45–75 CPL** for standard low-vision-friendly body; **50–65 CPL** for reading-heavy surfaces with AMD or cognitively-loaded audiences.
- **80 CPL is the WCAG 1.4.8 ceiling.** Do not exceed it for prose.
- **At 200–400% zoom**, a design-time 65ch measure may become ~20–30 characters — too short, producing regressions. This is a trade-off: design for a reasonable measure at 100% and accept shorter measure at high zoom.

Low-vision readers benefit from shorter measures because line-return errors (losing the next line) compound peripheral-field deficits. A reader with glaucoma at 400% zoom cannot preview the line end; a long line becomes a navigational hazard. See [`../techniques/measure.md`](../techniques/measure.md) for CPL math.

### Line height

- **1.5–1.8** for body text at accessibility-sensitive surfaces. WCAG 1.4.8 AAA requires ≥1.5× within paragraphs; 1.4.12 AA requires content to survive user overrides to 1.5×.
- Use **unitless** `line-height` values (`line-height: 1.5`) so descendants scale correctly.
- For AMD readers specifically, slightly higher line-height (1.6–1.8) reduces line-tracking load and gives the PRL more vertical separation.

### Letter spacing

- **Default to the type designer's values** for body. Good fonts are spaced correctly for their intended size range.
- **Optional +0.02–0.05em** for low-vision-targeted surfaces. The evidence base comes from the dyslexia crowding literature (Zorzi et al. 2012, Perea et al. 2012; see [`../science/crowding.md`](../science/crowding.md)) but generalises to AMD readers and peripheral reading. **Do not exceed ~+0.1em** — beyond that, word grouping weakens and reading rate falls.
- WCAG 1.4.12 requires content to survive override to **+0.12em** without breakage. Design containers accordingly.

### Word spacing

- **0.16em minimum per WCAG 1.4.12** override tolerance. Not a design target.
- Overriding word spacing can damage CJK, Arabic, and mixed-script content. Test multilingual surfaces explicitly.

### Paragraph spacing

- **2× font-size minimum** per WCAG 1.4.12; WCAG 1.4.8 goes slightly further (≥1.5× line-spacing, so ≥2.25× font-size at 1.5 line-height).
- Generous paragraph breaks give low-vision readers navigation anchors that survive magnification.

### Font choice

- **Sans-serif generally preferred** for body text on screen for low-vision audiences. Cleaner stroke endings; fewer rendering artifacts at aggressive zoom; fewer small features that fall below contrast-sensitivity threshold.
- **High x-height** improves letter-feature visibility at small sizes. Good low-vision picks: **Atkinson Hyperlegible** (Braille Institute, 2020), **Verdana** (Matthew Carter, 1996), **Source Sans 3**, **Open Sans**, **Inter**. See [`./dyslexia.md §5`](./dyslexia.md#part-5--font-choices-that-are-well-defended) for the overlapping shortlist.
- **Avoid extreme-contrast serifs** (Didone, modern-revival display faces) for body — hairlines fall below contrast-sensitivity threshold for many low-vision readers. Didones at display sizes on high-DPI screens can be fine; the danger is body usage.
- **Avoid thin weights** (100–300) at small sizes. Regular (400) and Medium (500) for body; Semi-Bold (600) or Bold (700) for emphasis. Low-vision readers with contrast-sensitivity loss see thin strokes as broken or absent.
- **Avoid decorative fonts** for anything but brief display use. Script, brush, and hand-lettered fonts are unreadable for many low-vision readers.
- **Font-specific low-vision faces:** **Maxular Rx** (Christopher Slye / Adobe Originals, 2021, designed with the MN Low Vision Reading Lab) and **Eido** (Bonnie Shaver-Troup / Thomas Jockin, 2022, dyslexia/low-vision focus) are explicitly designed for AMD and similar central-vision conditions via enlarged sidebearings and open counters. Evidence base is thin but the design intent is sound. Consider for user-preference panels.

---

## Part 4 — Contrast, polarity, and colour

### Overlap with colour-vision deficiency

Roughly 8% of men and 0.5% of women of northern-European descent have some form of colour-vision deficiency (red-green most common). Many low-vision users have CVD or diminished colour discrimination from retinal disease. **Typography must not encode information in colour alone** (WCAG SC 1.4.1). Link underlines, error-state borders, icon pairing with colour-coded status — these are the typography-adjacent places where CVD intersects low vision.

For typography specifically:
- **Keep link underlines.** `text-decoration: underline` is the only colour-independent signal that a span of text is a link. `text-decoration-skip-ink: auto` handles the descender-clash without removing the line.
- **Use weight or italic for emphasis**, not colour alone.
- **Form error messages** should include text, an icon, and colour — not just a red border.

### Pure black on pure white

A contested default. Evidence is mixed:
- **Photophobia / scotopic-sensitivity users** (roughly includes many migraine, post-concussion, autism-spectrum, and dyslexic populations) report less discomfort reading on off-white backgrounds or dark schemes.
- **AMD readers** often find pure black on pure white the most legible because contrast-sensitivity loss is the binding constraint, and black-on-white maximises luminance contrast.

Practitioner compromise — not a universal rule:
- **Near-black on off-white** (`#1a1a1a` to `#222` on `#fafafa` to `#f5f5f5`) is a safe body default for general audiences. Mild reduction of the hardest whites; still comfortably above AA and usually above AAA.
- **Offer a true high-contrast mode** (`prefers-contrast: more`) that gives absolute black on absolute white for the AMD cohort that prefers it.
- **Offer dark mode** (`prefers-color-scheme: dark`) for photophobia, migraine, and general preference.

Do not impose near-black-on-off-white as a fixed default on AMD-heavy audiences (medical, senior-services, pension products); they may measurably prefer `#000` on `#fff`. Respect `prefers-contrast: more`.

### Dark mode and photophobia

**Photophobia** — light sensitivity — is common in migraine, post-concussion syndrome, multiple sclerosis, iritis, and some AMD subtypes. Dark-mode schemes measurably reduce discomfort for these users.

Rules for dark-mode typography:
- **Never use pure `#000` as the dark-mode background.** Pure black with light text produces halation — the light text appears to glow and smear. Use `#0a0a0a` to `#18181b` as the darkest background tier.
- **Never use pure `#fff` as dark-mode body text.** Use `#e5e5e5` to `#f0f0f0` on dark backgrounds to tame halation.
- **APCA shines in dark mode.** The WCAG 2.x formula treats dark-on-light and light-on-dark symmetrically; APCA does not. APCA Lc −75 (negative for light-on-dark) is the recommended body floor, and it often corresponds to a *higher* WCAG 2.x ratio than the AA minimum. See [`./wcag-type.md §APCA`](./wcag-type.md#apca--accessible-perceptual-contrast-algorithm).
- **Reduce body weight.** Light-on-dark body text at regular weight often looks over-emphatic. Dark-mode body at 400 may need to drop to ~380 via variable-font `wght`, or to a lighter weight if the font exposes it. Apple's San Francisco handles this automatically via its optical weight adjustment; open-source fonts rarely do.

### AMD and dark mode

AMD readers often find dark mode **harder**, not easier. Contrast-sensitivity loss compresses the effective dynamic range; light text on dark backgrounds has less perceived contrast than dark on light at equivalent luminance. Respect `prefers-color-scheme: light` explicitly — don't override user preference with a stylistic dark default.

### Forced colours / Windows High Contrast Mode

**`forced-colors: active`** indicates the user has turned on a system-level high-contrast override (Windows HC Mode, some Linux accessibility modes). The user's chosen system colours *override* the site's colours. Typography implications:

- **`color` and `background-color` are replaced** by system-defined values (`CanvasText`, `Canvas`, `LinkText`, `GrayText`, etc.).
- **`background-image` is stripped** unless the site explicitly sets `forced-color-adjust: none`.
- **Text shadows, drop shadows, and custom focus rings are ignored** unless the site opts out.
- **Custom fonts are preserved.** Font choice and size carry through; colour does not.

The right posture is to **let forced-colours mode do its job**. Use the `forced-colors` media query to verify focus rings, borders, and icons remain visible — but do not try to style around the user's chosen contrast.

```css
@media (forced-colors: active) {
  button {
    border: 2px solid ButtonBorder;
    color: ButtonText;
    background: ButtonFace;
  }
}
```

---

## Part 5 — Zoom and reflow

### Browser zoom vs text-only zoom

- **Browser zoom** scales the entire viewport; fixed-px text scales along with everything. Ctrl+`+`/`-` in every major browser.
- **Text-only zoom** scales text without scaling layout. Firefox supports it natively; Chromium browsers removed the UI but it remains invocable via user stylesheets. The stricter reading of SC 1.4.4 requires text-only zoom to work.

**`rem`-based typography** works under both. **`px`-based typography** fails text-only zoom because the user's browser font-size preference cannot increase `px` values.

### SC 1.4.10 Reflow — the 320 CSS px test

WCAG 2.2 SC 1.4.10 requires content without 2D scrolling at 320 CSS px × 256 CSS px (exceptions: tables, maps, toolbars, data visualisations). At 1280 CSS px × 400% zoom, the effective viewport is 320 CSS px — the single most revealing low-vision test any typography system can run.

Common typography-related failures: fixed-width containers without `max-width: 100%`; fixed-pixel table columns; horizontally-laid-out forms that don't collapse; nav bars with overflow-hidden clipping items; hero banners with `height: 100vh` and centred text pushed below the fold.

### Survival patterns

- `rem`/`em` for body text — never `px`.
- `max-width: 100%` on every fixed-width container.
- `min-height` over `height` on text-containing elements.
- Avoid `overflow: hidden` on prose containers.
- Never set `user-scalable=no`.
- Test at 200% browser zoom, 200% text-only zoom, and 400% browser zoom — three separate conditions.

### Dynamic type

OS-level text-size preferences feed through to the browser:

- **iOS Dynamic Type** — Settings → Accessibility → Display & Text Size. Safari propagates via `text-size-adjust` and root font-size.
- **Android font scale** — Settings → Display → Font Size. Chrome for Android respects this for `rem`/`em` and for `auto` `text-size-adjust`.
- **Windows** — System → Display → Scale plus Accessibility → Text Size. Firefox and Edge honour the text-size preference; Chrome is less consistent as of 2026.
- **macOS** — less uniform; browser-level preferences are the more reliable route.

The structural implication: **the browser's root `font-size` is a user-controlled value you do not own**. `html { font-size: 100% }` preserves the user's chosen default. Setting `html { font-size: 16px }` silently fights the user preference.

---

## Part 6 — Screen readers and live text

Low-vision users often supplement magnification with speech synthesis. Typography is mostly orthogonal to screen-reader UX — but a few typography decisions bleed into it:

- **Live text vs images of text.** Headlines or quotes rendered as SVG/PNG are invisible to screen readers unless you provide `alt` text, and they do not respond to zoom, selection, translation, or user stylesheets. WCAG SC 1.4.5 prohibits images of text except for logotypes and cases where the specific presentation is essential. **Ship headlines as live text.**
- **Decorative Unicode glyphs.** Mathematical Alphanumeric Symbols (𝐇𝐞𝐥𝐥𝐨, 𝘏𝘦𝘭𝘭𝘰, etc.), Old Italic (𐌇𐌔), and other Unicode codepoints used as "style" read aloud as their Unicode names: "MATHEMATICAL BOLD ITALIC CAPITAL H MATHEMATICAL BOLD ITALIC SMALL E…". Screen-reader output becomes gibberish. Use a styled font with proper weight/italic instead.
- **Emoji and pictographs.** Read aloud with their CLDR short names: 🎉 → "party popper". Fine for sparse use; disastrous for bullet substitution.
- **Icon fonts with private-use codepoints.** Read aloud as nothing, or as "private use area character", depending on the screen reader. Prefer SVG icons with explicit `aria-label`.
- **CSS-generated content (`::before`, `::after`).** Not all screen readers announce generated content; historically NVDA and VoiceOver have varied in behaviour. Never put meaningful text in `::before`.
- **Lang attributes.** `lang="en"` at the root and `lang="fr"` around French quotes switches the screen-reader voice and pronunciation correctly. Missing `lang` produces wrong pronunciation and fails WCAG 3.1.1 / 3.1.2.

---

## Part 7 — Condition-specific adjustments

### Central scotoma (AMD, Stargardt)

- **Peripheral reading is crowding-limited.** Increase letter-spacing by +0.03–0.05em on reading surfaces; offer a preference-toggle for +0.08em.
- **Higher line-height** (1.6–1.8) gives the PRL more vertical separation.
- **Shorter measure** (50–60 CPL) reduces line-return errors.
- **Sans-serif with open apertures.** Atkinson Hyperlegible, Maxular Rx, Verdana.
- **Contrast at AAA or APCA Lc 75.** Contrast-sensitivity loss is typical.
- **Do not assume dark mode helps.** AMD readers often prefer light mode.

### Peripheral-field loss (glaucoma, RP)

- **Short measure** — the visible field is narrow; long lines force re-fixations that lose context.
- **Clear paragraph boundaries** — navigation anchors survive zoom.
- **Avoid cramped UIs** — generous whitespace at low zoom is visible as "too much"; at high zoom it becomes just right.
- **Consider sans-serif** for cleaner letter identification; foveal acuity is usually preserved, so serif vs sans is less critical than for AMD.

### Photophobia (migraine, post-concussion, MS, some AMD)

- **Dark mode default**, with the anti-halation precautions above.
- **Reduce the highest whites.** `#fafafa` instead of `#fff`; `#f5f5f5` for cards and surfaces.
- **Offer a tint preference.** A warm off-white or pale amber background can help some users; don't impose it.
- **Respect `prefers-reduced-motion`.** Animated type and parallax are migraine triggers.

### Nystagmus, albinism

- **Larger body text** (18 CSS px minimum, 20–24 CSS px better).
- **Extra line-height** (1.7–1.8).
- **Short measure** (50–55 CPL).
- **High contrast**; respect `prefers-contrast: more`.
- **Stable layouts.** Jumpy zoom-reflow boundaries are disorienting; avoid UI that reconfigures at every breakpoint.

### Cataract and glare

- **High contrast**; AAA or APCA Lc 75.
- **Avoid pure `#fff` backgrounds on large areas.** Reduce to `#fafafa` or offer dark mode.
- **Avoid thin weights and narrow faces.** Stroke thickness matters for readers whose effective modulation transfer function is degraded.

---

## Part 8 — WCAG 2.2 Success Criteria most relevant to low-vision typography

For full SC mechanics see [`./wcag-type.md`](./wcag-type.md). The subset that applies most directly to low-vision readers:

- **SC 1.4.1 Use of Color — A.** Information not conveyed by colour alone.
- **SC 1.4.3 Contrast (Minimum) — AA.** 4.5:1 body, 3:1 large. Auditable floor.
- **SC 1.4.4 Resize Text — AA.** 200% zoom without loss of content or function.
- **SC 1.4.5 Images of Text — AA.** Avoid rendering text as images.
- **SC 1.4.6 Contrast (Enhanced) — AAA.** 7:1 body, 4.5:1 large. Low-vision target.
- **SC 1.4.8 Visual Presentation — AAA.** Comprehensive typographic targets: user-selectable colours, ≤80 CPL, no justified prose, ≥1.5 line-height, ≥1.5× paragraph spacing, 200% without horizontal scroll.
- **SC 1.4.9 Images of Text (No Exception) — AAA.** Stricter version of 1.4.5.
- **SC 1.4.10 Reflow — AA.** No 2D scrolling at 320 CSS px.
- **SC 1.4.11 Non-text Contrast — AA.** 3:1 for UI components and graphical objects.
- **SC 1.4.12 Text Spacing — AA.** Survival of content under user-applied line/letter/word/paragraph spacing overrides.
- **SC 1.4.13 Content on Hover or Focus — AA.** Tooltip and popover behaviour: dismissible, hoverable, persistent.
- **SC 2.4.11 Focus Not Obscured (Minimum) — AA.** New in 2.2.
- **SC 2.4.13 Focus Appearance — AAA.** New in 2.2.
- **SC 2.5.8 Target Size (Minimum) — AA.** 24×24 CSS px for interactive targets. New in 2.2.

SC 1.4.8, though AAA and therefore optional, is the most comprehensive typographic guidance in WCAG 2.x. Low-vision-friendly reading surfaces should treat 1.4.8 as a design target.

---

## Part 9 — User-preference media queries

Respect the following; do not override without explicit user action.

### `prefers-contrast`

```css
@media (prefers-contrast: more) {
  :root {
    --text: #000;
    --bg: #fff;
    --muted: #1a1a1a;  /* avoid soft grays */
  }
}

@media (prefers-contrast: less) {
  :root {
    --text: #222;
    --bg: #fafafa;
  }
}
```

Triggered on iOS by Increase Contrast, on macOS by Increase Contrast, on Windows by Contrast Themes (but `forced-colors: active` is the stricter signal).

### `prefers-color-scheme`

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #18181b;
    --text: #e5e5e5;
    --muted: #a1a1aa;
  }
}
```

Also: the CSS `light-dark()` function (Baseline 2024) avoids the media-query scaffolding for single-token pairs:

```css
:root {
  color-scheme: light dark;
  --text: light-dark(#1a1a1a, #e5e5e5);
  --bg: light-dark(#fafafa, #18181b);
}
```

### `prefers-reduced-motion`

Relevant to typography only for animated text — marquees, typewriter effects, kinetic type, text-reveal transitions. The default should be **static**; motion belongs behind a media query.

```css
@media (prefers-reduced-motion: no-preference) {
  .kinetic-headline {
    animation: reveal 600ms ease;
  }
}
```

### `forced-colors`

Respect the user's chosen system colour scheme (Windows High Contrast Mode).

```css
@media (forced-colors: active) {
  .card {
    border: 1px solid CanvasText;
    background: Canvas;
    color: CanvasText;
  }
  .link { color: LinkText; }
  .button { color: ButtonText; background: ButtonFace; border: 1px solid ButtonBorder; }
}
```

Do not use `forced-color-adjust: none` without very good reason — it opts the user's system preferences out, which is usually the opposite of what a low-vision user wants.

---

## Part 10 — APCA and low-vision: the honest picture

APCA (Accessible Perceptual Contrast Algorithm, Andrew Somers / Myndex Research) is the contrast model under consideration for WCAG 3.0 (still a Working Draft as of 2026-04). It is **not a WCAG conformance target**.

What APCA does that WCAG 2.x does not:
- **Polarity-aware.** Dark-on-light and light-on-dark are scored differently. Light text on dark needs more optical contrast than the 2.x formula implies.
- **Weight-aware.** Thin type at small sizes needs more contrast than heavy type at large sizes. The `APCA Readability Criterion` (ARC) gives per-weight thresholds rather than one flat ratio.
- **Perceptually weighted.** Uses a lightness-difference model closer to actual human contrast sensitivity than the 2.x luminance ratio.

For low-vision work specifically, APCA is the more predictive model. The WCAG 2.x dark-mode pass at 4.5:1 is frequently a dark-mode *fail* for AMD and diabetic-retinopathy readers; APCA Lc −75 catches this.

**Practitioner posture for 2026-04:**
- Conform to WCAG 2.2 AA for audits and legal defensibility.
- Use APCA as an internal secondary check, especially for dark-mode designs and thin-weight type.
- Flag APCA failures as design smells even when WCAG 2.x passes.
- Do **not** claim WCAG compliance via APCA — it is a supplement, not a replacement.

See [`../../../color-science-accessibility/references/techniques/apca-lc-formula.md`](../../../color-science-accessibility/references/techniques/apca-lc-formula.md) for the deep APCA primer.

### The `color-contrast()` CSS function

As of 2026-04, `color-contrast()` — which lets a site pick a foreground from a set based on contrast against a background — is shipped in Safari (16.4+, 2023), Firefox (134+, 2025), and is experimental in Chromium. The polarity-aware version uses APCA; the 2.x version uses luminance ratio. Useful for tokenised theming:

```css
p {
  color: color-contrast(var(--bg) vs #111, #f5f5f5 to AA);
}
```

The `to AA` / `to AAA` keyword uses WCAG 2.x; there is a proposal (2025) for `to APCA-75` but it is not yet normative. Track browser support before deploying in production.

---

## Part 11 — Print and physical accessibility

Low-vision needs don't end at the browser. Print conventions differ from screen:

- **APH (American Printing House for the Blind)** — 18-point minimum for large-print publications, up to 36-point. Sans-serif preferred. High-contrast ink on white or cream paper. Line spacing ≥1.25× leading.
- **RNIB Clear Print (UK)** — 12–14 point minimum, bold weight for readability at low contrast, matte-finish paper to reduce glare. Large print (14+) and giant print (18+) are separate tiers.
- **CNIB (Canada)** — 18-point minimum for large-print; heavy weight and matte paper.
- **DAISY Consortium** — digital accessible publishing standards; prioritises reflowable EPUB over fixed PDF.

For low-vision *print* specifically, sans-serif is usually recommended — magnification devices degrade serif rendering similarly to screens, and contrast-sensitivity loss makes thin-stroke differences harder to register. Leading runs 120–140% of font size (tighter than the screen ≥1.5 recommendation because print lacks the screen's rendering-noise floor). Matte paper, high-opacity stock, and dense K-only black ink round out the print stack.

---

## Anti-patterns

- **`font-size: 14px` on body.** Below the 16-px floor; breaks text-only zoom.
- **`html { font-size: 10px }`** to make `1rem = 10px`. Disables user font-size preference.
- **Pure `#000` on pure `#fff`** imposed as default for photophobic audiences. Offer reduced-whites alternative.
- **Pure `#fff` on pure `#000`** dark mode. Halation destroys legibility.
- **Fixed-height buttons** (`height: 40px; line-height: 40px`). Fail SC 1.4.12 under spacing override.
- **Image-of-text headlines.** Fail SC 1.4.5 and lose zoom/selection/translate/screen-reader.
- **Disabling zoom** via `<meta viewport user-scalable=no>`. Modern platforms ignore it; still a 1.4.4 smell.
- **Designing to WCAG 2.x AA as the ceiling.** For low-vision audiences, AA is the floor; design to AAA or APCA Lc 75.
- **Forcing dark mode** because it looks cool. AMD readers need light mode; respect `prefers-color-scheme`.
- **`forced-color-adjust: none`** on meaningful content. Overrides the user's system choice.
- **Fancy Unicode glyphs** for style (𝐁𝐨𝐥𝐝 𝐓𝐞𝐱𝐭). Screen readers read out "mathematical bold" for each letter.
- **Thin weights** (100–300) on body text. Contrast-sensitivity loss cannot resolve them.
- **Extreme-contrast serifs** (Didone) for body. Hairlines below contrast-sensitivity threshold.
- **`text-align: justify`** on prose without a hyphenation engine. Rivers and uneven spacing damage reading.
- **Missing link underlines.** Colour-only link signalling fails SC 1.4.1.
- **Ignoring `prefers-contrast: more`.** Users asking for high-contrast explicitly should get it.
- **Claiming APCA-only conformance.** Not valid for WCAG audits.

---

## Sources

### Clinical and prevalence

- **WHO.** *World Report on Vision* (2019). https://www.who.int/publications/i/item/9789241516570
- **GBD 2020 Vision Loss Expert Group.** "Causes of blindness and vision impairment in 2020 and trends over 30 years." *Lancet Global Health* (2021, updated 2023).
- **National Eye Institute (NEI).** "Vision Health Data and Statistics." https://www.nei.nih.gov/learn-about-eye-health/outreach-resources/eye-health-data-and-statistics
- **CDC.** "Vision and Eye Health Surveillance System (VEHSS)." https://www.cdc.gov/visionhealth/vehss/
- **ICD-11 (WHO).** Chapter 9 — Diseases of the visual system.

### Standards and contrast

- **W3C.** *WCAG 2.2* (2023). https://www.w3.org/TR/WCAG22/ — Understanding: https://www.w3.org/WAI/WCAG22/Understanding/
- **W3C.** *WCAG 3.0 Working Draft.* https://www.w3.org/TR/wcag-3.0/
- **ETSI EN 301 549** v3.2.1 — EU Accessibility Act harmonised standard.
- **Somers, A.** "APCA — Accessible Perceptual Contrast Algorithm." Myndex Research. https://apcacontrast.com/ and ARC: https://readtech.org/ARC/
- **W3C CSS Color 6.** `color-contrast()` function. https://www.w3.org/TR/css-color-6/

### Print standards

- **APH.** "Large-Print Guidelines." https://www.aph.org/app/uploads/2017/10/APH-Large-Print-Guidelines.pdf
- **RNIB.** "Clear Print Guidelines." https://www.rnib.org.uk/professionals/accessibility/clear-print-guidelines/
- **CNIB.** "Clear Print Accessibility Guidelines."
- **DAISY Consortium.** https://daisy.org/

### Fonts

- **Atkinson Hyperlegible** (Braille Institute, 2020). https://www.brailleinstitute.org/freefont
- **Maxular Rx** (Christopher Slye / Adobe Originals, 2021). Adobe Fonts.
- **Eido** (Bonnie Shaver-Troup / Thomas Jockin, 2022).
- **Lexend** (Thomas Jockin & Bonnie Shaver-Troup). https://lexend.com/
- **Verdana** (Matthew Carter, Microsoft, 1996). System font.

### Reading science

- **Legge, G. E.** (2007). *Psychophysics of Reading in Normal and Low Vision.* https://legge.psych.umn.edu/book
- **Chung, S. T. L.** (2002). "The effect of letter spacing on reading speed in central and peripheral vision." *IOVS* 43(4): 1270–1276.
- **Chung, S. T. L. & Mansfield, J. S.** (2009). "Contrast polarity differences reduce crowding but do not benefit reading performance in peripheral vision." *Vision Research* 49(23): 2782–2789.
- **Trauzettel-Klosinski, S. & Dietz, K.** (2012). "Standardized assessment of reading performance: the New International Reading Speed Texts (IReST)." *IOVS* 53(9): 5452–5461.
- See [`../science/crowding.md`](../science/crowding.md) for the full crowding bibliography.

### Assistive tech and practitioner resources

- **Freedom Scientific** (ZoomText, JAWS, MAGic), **Dolphin** (SuperNova), **Apple Accessibility** (iOS/macOS Zoom, VoiceOver), **Microsoft Accessibility** (Magnifier, Narrator).
- **Hassell, J.** *Inclusive Design for a Digital World.* Apress, 2nd ed., 2019.
- **WebAIM.** "Visual Disabilities." https://webaim.org/articles/visual/
- **Roselli, A.** Accessibility writing. https://adrianroselli.com/
- **GOV.UK Service Manual.** https://www.gov.uk/service-manual/helping-people-to-use-your-service

### Peer files

- [`./wcag-type.md`](./wcag-type.md) — WCAG 2.2 text SCs (the floor this file builds on).
- [`./dyslexia.md`](./dyslexia.md) — dyslexia typography (overlap on spacing and crowding).
- [`./cognitive.md`](./cognitive.md) — cognitive-accessibility typography.
- [`../science/crowding.md`](../science/crowding.md) — Bouma's law, peripheral reading, spacing.
- [`../techniques/measure.md`](../techniques/measure.md) — CPL math.
- [`../../../color-science-accessibility/references/techniques/apca-lc-formula.md`](../../../color-science-accessibility/references/techniques/apca-lc-formula.md) — APCA primer.
