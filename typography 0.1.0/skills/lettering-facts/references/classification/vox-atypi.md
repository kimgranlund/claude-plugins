---
date: 2026-04-18
coverage: medium
peers:
  - ./bringhurst.md
  - ./din-16518.md
  - ./thibaudeau.md
  - ../historical/humanist-renaissance.md
  - ../historical/transitional.md
  - ../historical/modern.md
  - ../historical/sans-grotesque.md
  - ../historical/humanist-sans.md
  - ../historical/geometric-sans.md
  - ../historical/blackletter.md
primary_sources:
  - Vox, Maximilien. *Pour une nouvelle classification des caractères* (École Estienne, 1954)
  - ATypI — "Classification Vox-ATypI" official adoption (1962); minor revision 2010
  - BS 2961:1967 — British Standard — Typeface Nomenclature and Classification (British Standards Institution, 1967)
  - Jaspert, W. P., Berry, W. T., Johnson, A. F. *The Encyclopaedia of Type Faces* (Blandford, 4th ed. 1970)
  - Blackwell, Lewis. *Twentieth-Century Type* (Laurence King, rev. 2004)
  - McLean, Ruari. *The Thames & Hudson Manual of Typography* (1980)
  - Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012) — ch. 7 "Historical Interlude"
  - Kinross, Robin. *Modern Typography: An Essay in Critical History* (Hyphen Press, 2nd ed. 2004)
  - https://atypi.org — ATypI classification reference (accessed 2026-04-18)
  - https://en.wikipedia.org/wiki/Vox-ATypI_classification (historical content cross-checked against Jaspert/Blackwell)
  - Lawson, Alexander. *Anatomy of a Typeface* (David R. Godine, 1990)
  - Kupferschmid, Indra — writings on kupferschrift.de and type.today on classification critique
---

# Vox-ATypI Classification

The Vox-ATypI system is the classification most type specimens, foundry catalogs, type-design curricula, and ISO-style institutional references default to when they need a shared vocabulary for "what kind of typeface is this." It was created by **Maximilien Vox** in 1954, adopted almost verbatim by the **Association Typographique Internationale (ATypI)** in 1962, codified in Britain as **BS 2961:1967 — Typeface Nomenclature and Classification**, and lightly amended by ATypI in 2010. Its strengths and seams are both a product of its era: it was authored before digital type, before global (non-Latin) typography became a first-class concern in Western foundries, and before the sans-serif tradition had produced the density of distinctions we now take for granted.

This file is the medium reference for Vox-ATypI: what the categories are, where each came from, what goes in each bucket, where the system creaks, and what disagreements to expect in practice. For the parallel German industrial classification see `./din-16518.md`; for Bringhurst's essayistic alternative see `./bringhurst.md`; for the much older Thibaudeau silhouette taxonomy see `./thibaudeau.md`.

---

## History

### Vox, 1954

**Maximilien Vox** (1894–1974) was a French typographer, writer, and publisher who spent the 1930s–1950s critiquing the idiosyncratic, foundry-by-foundry naming of typefaces — each foundry called its own Garamond a "Garamond" and its own Clarendon a "Clarendon," with no agreement on what either word covered. Vox's 1954 essay *Pour une nouvelle classification des caractères* (published by the École Estienne, Paris) proposed a **nine-category grouping** organized chronologically by the dominant typographic sensibility of successive eras — from humanist manuscript roots through industrial-era slab serifs and sans — with a tenth bucket for broken-script (fraktur / blackletter) which stands outside the main chronological arc.

Vox's contribution was not the invention of the categories themselves — Thibaudeau (1921), Updike (1922), Francis Meynell (1923), and the Bauer Foundry had all published earlier taxonomies — but the **insistence on a culturally descriptive vocabulary** (Humanes, Garaldes, Réales, Didones, Mécanes, Linéales, Incises, Scriptes, Manuaires, Fractures) rather than serif-silhouette mechanics (Thibaudeau's antiques, égyptiennes, elzévirs, didots). The neologisms are made up of composites: *Garalde* = Garamond + Aldus; *Didone* = Didot + Bodoni; *Mécane* = mechanical / machine-age.

### ATypI adoption, 1962

At its **Stockholm congress in 1962**, ATypI adopted Vox's classification as the organization's official reference, giving the system the ATypI imprimatur and effectively making it the international-standard vocabulary. ATypI did not materially change the ten categories; it formalized them and propagated them through the international type community via specimens, foundry catalogs, and the eventual British Standard.

### BS 2961:1967

The **British Standards Institution** published **BS 2961:1967 — Typeface Nomenclature and Classification** in 1967. It is based substantially on Vox-ATypI but uses English names (Humanist, Garalde, Transitional, Didone, Slab-serif, Lineal, Glyphic, Script, Graphic, Black-letter) and adds minor subclassifications — most importantly, the four-way subdivision of **Lineal** into *Grotesque*, *Neo-Grotesque*, *Geometric*, and *Humanist* sans. This subdivision is the single most durable contribution of the BS version; the Lineal-quadrant vocabulary is now used almost universally, including by foundries that never cite BS 2961 as the source.

BS 2961 was **withdrawn** by BSI in the 2010s (the British Standard catalog no longer lists it as current). The vocabulary it defined remains in general use.

### ATypI 2010 revision

ATypI revisited the classification in **2010** under the broader "Classification Vox-ATypI" banner. The revision was light — the ten categories were retained — but added:

- An **eleventh bucket, *Étrangères* (Foreign / Non-Latin)**, as an explicit acknowledgment that Latin-rooted categories do not meaningfully classify Arabic, Devanagari, CJK, Hebrew, Thai, or other scripts. This is widely understood as a placeholder rather than a serious classification of non-Latin typography — which has its own script-specific conventions (see `../scripts/`) that the Vox framework was never designed to describe.
- **Explicit acknowledgment of overlap** — a typeface can legitimately sit in two categories (a humanist sans is both Linéale Humaniste and close to Incise; Optima, famously, has been classified as both Linéale Humaniste and Incise depending on whose system you use).
- **Recognition that digital-era faces** resist clean classification — the variable-font, screen-first, superfamily era (roughly 2000s onward) has produced faces that embody multiple traditions at once (Fraunces, Recursive, Roboto Flex).

The 2010 revision did **not** solve the underlying scope problems. It is better described as a patch acknowledging limits than a re-architecture.

### Relationship to DIN 16518

**DIN 16518** (Deutsches Institut für Normung) is a parallel German industrial classification, first published in 1964 (post-Vox, post-ATypI adoption). It uses different category names (*Venezianische Renaissance-Antiqua*, *Französische Renaissance-Antiqua*, *Barock-Antiqua*, *Klassizistische Antiqua*, *Serifenbetonte Linear-Antiqua*, *Serifenlose Linear-Antiqua*, *Antiqua-Varianten*, *Schreibschriften*, *Handschriftliche Antiqua*, *Gebrochene Schriften*, *Fremde Schriften*) and partitions the space slightly differently — most notably keeping **Antiqua-Varianten** (Glyphic / flared) and **Handschriftliche Antiqua** (casual hand) as separate categories rather than Vox's *Incises* and *Manuaires*, and maintaining **Gebrochene Schriften** with five sub-categories of blackletter (Gotisch, Rundgotisch, Schwabacher, Fraktur, Fraktur-Varianten). DIN retains formal authority in German-speaking type education; Vox-ATypI is more common internationally. See `./din-16518.md`.

---

## The nine (then ten, then eleven) categories

The original Vox proposal is usually given as **nine** categories; Fraktures / blackletter is counted as the tenth when presented in BS 2961 and most English sources; Étrangères is the eleventh added in 2010. The table below presents all eleven in the order they are conventionally taught, with their French, English (BS 2961), and German (for cross-reference) names.

| Vox (French) | BS 2961 (English) | DIN 16518 (German) | Era | Anchor examples |
|--------------|-------------------|---------------------|-----|-----------------|
| **Humanes** | Humanist | Venezianische Renaissance-Antiqua | 1460s–1500 | Centaur, Cloister, Adobe Jenson, Schneidler |
| **Garaldes** | Garalde | Französische Renaissance-Antiqua | 1500–1750 | Garamond, Bembo, Sabon, Minion, Granjon |
| **Réales** | Transitional | Barock-Antiqua | ~1700–1800 | Baskerville, Fournier, Bell, Caslon (late) |
| **Didones** | Didone | Klassizistische Antiqua | ~1780–1850 | Didot, Bodoni, Walbaum, Modern No. 20 |
| **Mécanes** | Slab-serif / Mechanistic | Serifenbetonte Linear-Antiqua | 1815– | Clarendon, Rockwell, Memphis, Courier, Archer |
| **Linéales** | Lineal / Sans-serif | Serifenlose Linear-Antiqua | 1816– | Akzidenz-Grotesk, Helvetica, Futura, Gill Sans |
| **Incises** | Glyphic | Antiqua-Varianten | — | Albertus, Copperplate Gothic, Trajan, Perpetua |
| **Scriptes** | Script | Schreibschriften | — | Zapfino, Bickham Script, Snell Roundhand |
| **Manuaires** | Graphic | Handschriftliche Antiqua | — | Klang, Papyrus, Lithos |
| **Fractures** | Black-letter | Gebrochene Schriften | 1450s– | Textura, Rotunda, Schwabacher, Fraktur |
| **Étrangères** (2010) | Non-Latin | Fremde Schriften | — | (everything not Latin-script) |

### Humanes (Humanist)

The earliest roman types, cut in the 1460s–1490s by printers working to imitate the **humanist minuscule** — a late-medieval Italian scribal hand that revived Carolingian minuscule as a reaction against Gothic textura. The first definitively humanist roman is **Nicolas Jenson's 1470 Venetian roman**, followed by the types of Aldus Manutius (pre-Griffo), Johannes de Spira, and others.

Humanes characteristics:

- Low stroke contrast (pen-like — the variation between thick and thin strokes is small).
- **Slanted axis** (the axis of the `o` and `O` tilts to the left, following the pen angle of a humanist docs).
- Small x-height; tall ascenders.
- Bracketed, slanted serifs on the lowercase; flat serifs on caps.
- A distinctive slanted crossbar on the lowercase `e` (the "humanist e") — this is the single most reliable single-glyph marker of the Humanes family.

Anchor digital revivals: Adobe Jenson (Robert Slimbach, 1996), Centaur (Bruce Rogers, 1914), Cloister Old Style (M. F. Benton, 1897), Schneidler Old Style (F. H. E. Schneidler, 1936), LTC Jenson, Centaur MT.

Traps:

- Many so-called "old-style" faces are Garaldes, not Humanes — Garamond is Garalde, not Humanist. The humanist sleeve is small: only the earliest Venetian revivals qualify.
- Adobe's own classification marks some faces as "humanist" that Vox would classify as Garalde.

### Garaldes (Garalde / Old-Style)

The dominant roman tradition of the **16th, 17th, and early 18th centuries** — the typefaces of **Francesco Griffo** (working for Aldus Manutius in Venice, from ~1495), **Claude Garamond** (Paris, 1530s–1560s), **Robert Granjon**, **Christoffel van Dijck**, and **Jean Jannon**. The name is a portmanteau: **Gar**amond + **Ald**us.

Characteristics vs Humanes:

- Higher stroke contrast (still moderate, but more pronounced thick-thin variation).
- Still-slanted axis, but less tilted than Humanes.
- More refined, more regular, better-fitted.
- Bracketed serifs; sometimes sharper than Humanes.
- The crossbar of `e` is horizontal, not slanted (Humanes had a slanted crossbar).

Anchor faces: Garamond (Claude Garamond, various digital revivals — Adobe Garamond by Slimbach 1989, Garamond Premier 2005, ITC Garamond is an anomaly), Bembo (Aldus/Griffo 1495, digital Monotype Bembo 1929), Sabon (Jan Tschichold 1967), Minion (Slimbach 1990), Granjon, Galliard, Centaur is Humanist not Garalde despite sometimes being shelved with them.

Traps:

- **ITC Garamond** (Tony Stan, 1977) is visually *not* a Garalde despite the name — it has a much higher x-height, tighter fit, and more modern fit than historical Garamond; it reads closer to a transitional or even a contemporary serif. Consider it nominally Garalde but practically its own category.
- **Sabon** is explicitly a Garamond-based Garalde (Tschichold's brief was a Garamond for Linotype machines that would cast identically on Linotype, Monotype, and foundry type).

### Réales (Transitional)

The **mid-18th century bridge** between Garalde and Didone. Named *Réales* by Vox after the work of **Pierre Simon Fournier** (Paris, 1730s–1760s) and **John Baskerville** (Birmingham, 1750s), with ancestry in the Romain du Roi (a rationalized roman commissioned by Louis XIV, 1692, cut by Philippe Grandjean beginning 1702).

Characteristics:

- **Increased stroke contrast** compared to Garalde — the thicks are heavier, the thins are finer.
- **Vertical axis** (the `o` is symmetric; no pen-tilt).
- **Finer, sharper serifs** — still bracketed but more crisp.
- Regularized proportions — the rationalist, Enlightenment sensibility visible in Baskerville's printing.

Anchor faces: Baskerville (Baskerville 1757, digital ITC New Baskerville, Berthold Baskerville Book), Fournier (Fournier 1742, Monotype Fournier), Bell (Richard Austin 1788), Bulmer (William Martin 1790s), Caslon (William Caslon I, 1720s — this is the contested case; see below).

Traps / the Caslon question:

- **William Caslon's** (1692–1766) types are sometimes classified as **Garalde** (on the basis of their English adaptation of Dutch / Flemish Garalde traditions) and sometimes as **Réale / Transitional** (on the basis of their date — 1720s — and their role bridging to later English work). Vox himself was inconsistent. Current practice: **early Caslon (pre-1740) = Garalde; later Caslon revivals (Caslon 540, Caslon 3, ITC Founder's Caslon) sit on the Garalde / Réale boundary and can be taught as either.** The digital "Adobe Caslon" (Carol Twombly, 1990) sits comfortably in Garalde.
- **Times New Roman** (Stanley Morison / Victor Lardent, 1932) is sometimes shelved as Réale, sometimes as a category of its own ("newspaper transitional"), sometimes as a 20th-c. Garalde. It was *designed as* a transitional-derivative for newspaper printing; practically, classify as Réale / Transitional.

### Didones (Modern / Didone)

Late-18th to mid-19th century. Named after **Firmin Didot** (Paris, 1784 onward) and **Giambattista Bodoni** (Parma, 1780s–1810s). The name *Didone* is a portmanteau: **Did**ot + **Bod**oni.

Characteristics — the most extreme typographic vocabulary Vox's system contains:

- **Extreme stroke contrast** — thin parts become hairlines, thick parts become broad vertical stems.
- **Fully vertical axis** (completely rationalized).
- **Hairline, unbracketed serifs** — flat, thin, often connected to the stem with a sharp right angle rather than a curved bracket.
- Rationalized, often mathematically regular construction.

Anchor faces: Didot (Didot 1784, digital HTF Didot 1992, Linotype Didot), Bodoni (Bodoni 1790s, digital ITC Bodoni 72 / Bodoni Poster, Berthold Bodoni, Bauer Bodoni — each revival has dramatically different metrics), Walbaum (Justus Erich Walbaum, 1800, digital Walbaum 2018 by Monotype), Modern No. 20, Scotch Roman (a related British tradition, sometimes classified separately).

Traps:

- Not every Didone revival is the same — **Bauer Bodoni** is the crispest, thinnest revival; **Bodoni Poster** is a fattened display cut; **ITC Bodoni 72** (Sumner Stone et al., 1994) has optical sizes that are dramatically different at 6pt, 12pt, 72pt — treat each as a different face.
- Modern sans-serifs are sometimes called "modern" in casual English — they are not Didone. The casual English "modern" (as in "modern sans") ≠ Vox *Didone*.

### Mécanes (Slab-serif / Egyptian)

**1815 onward** — a product of the Industrial Revolution and the rise of commercial display printing. First appeared in **Vincent Figgins**' specimen of 1815 (showing a "two-line English Antique" — a heavy slab-serif display face). Named *Égyptiennes* in French (no connection to Egypt — the name was fashionable in the 1810s post-Napoleon).

Characteristics:

- **Slab (square or rectangular) serifs** rather than bracketed or triangular.
- Minimal to moderate stroke contrast — often monoline.
- Design originally for posters, broadsides, display — later adapted to text.
- Two major sub-traditions: **unbracketed Egyptian** (Memphis, Rockwell — the slabs meet the stems at right angles) vs **bracketed Clarendon-style** (Clarendon, Farnham — the slabs are connected by a bracket curve, producing a less harsh junction).

Anchor faces: Clarendon (R. Besley & Co., 1845, digital Clarendon Text 2009, Farnham Display), Rockwell (Monotype 1934), Memphis (R. E. Weiss 1929), Courier (Howard Kettler 1955 — monospaced slab; originally for IBM typewriters), Archer (Hoefler&Frere-Jones 2001), Roboto Slab, Serifa (Adrian Frutiger 1967).

Traps:

- **Monospaced slabs** (Courier, Monaco, Andale Mono) are technically Mécanes *and* monospaced — Vox's framework doesn't cleanly account for monospace.
- **Clarendon** (bracketed slabs) is sometimes split out as its own category — in BS 2961 and some modern treatments, Clarendon is a subcategory of Slab-serif. The difference between unbracketed (Memphis, Rockwell) and bracketed (Clarendon, Farnham) is stylistically large enough that some practitioners treat them as separate.

### Linéales (Lineal / Sans-serif)

First sans-serif types date to **1816** (William Caslon IV's "Two Lines English Egyptian" — a caps-only monoline, technically the first printed sans) and **1819** (the Thorowgood sans — the first lowercase sans). The category explodes in the late 19th and early 20th centuries with Berthold's **Akzidenz-Grotesk** (1898), and again in the mid-20th century with **Helvetica**, **Univers**, and **Futura**.

Vox's original 1954 proposal did not subdivide Linéales. **BS 2961:1967** introduced the four-way subdivision that is now standard:

#### Grotesque (19th-century sans)

The first sans-serif tradition — **Berthold Akzidenz-Grotesk** (1898, drawn from late-19th-century German foundry sans), American Type Founders' **Franklin Gothic** (Morris Fuller Benton, 1902), **News Gothic** (Benton, 1908), **Trade Gothic** (Jackson Burke, 1948).

Characteristics:

- Irregular, quirky proportions (not yet standardized).
- Often a "g" with a two-story double-bowl construction.
- Visible stroke contrast (thicker where a pen would thicken).
- An organic, somewhat industrial, workmanlike voice.

Anchor faces: Akzidenz-Grotesk, Franklin Gothic, News Gothic, Trade Gothic, Monotype Grotesque.

#### Neo-Grotesque (mid-20th-century Swiss rationalization)

**Helvetica** (Max Miedinger / Eduard Hoffmann, Haas Type Foundry 1957, originally Neue Haas Grotesk), **Univers** (Adrian Frutiger, Deberny & Peignot 1957), **Arial** (Monotype 1982, a Helvetica-metric-compatible).

Characteristics vs Grotesque:

- Rationalized, regularized proportions — each letter drawn to harmonize with the others.
- Single-story `g` (in Helvetica, Univers) or regularized two-story (Akzidenz was irregular).
- Minimal stroke contrast (monoline ideal, though never truly monoline).
- Cool, neutral, International Typographic Style voice.

Anchor faces: Helvetica / Helvetica Neue / Helvetica Now, Univers (Univers 45 through 85, a matrix system), Neue Haas Grotesk, Arial, Folio, Aktiv Grotesk.

#### Geometric

**Futura** (Paul Renner, Bauer 1927) launched the geometric tradition — sans where the letters are constructed from geometric primitives (circles for `o`, triangles for `A`, straight lines for stems). Kabel (Rudolf Koch 1927), Erbar (Jakob Erbar 1922) preceded Futura but Futura dominated.

Characteristics:

- Circular `o`, `O`, `C`, `G`, `Q` — often geometrically exact.
- Triangular `A`, `V`, `W`.
- Minimal stroke contrast (truly monoline in ideal; optical correction always present).
- Long ascenders on `b`, `d`, `l` — classical rather than UI-tall proportions.
- Bauhaus / modernist aesthetic.

Anchor faces: Futura (all cuts), Avenir (Frutiger 1988 — geometric with humanist leanings), Avant Garde Gothic (Herb Lubalin / Tom Carnase 1970), Century Gothic, ITC Kabel, Gotham (Hoefler&Frere-Jones 2000 — an American geometric).

Traps:

- **Avenir** is sometimes shelved as Geometric, sometimes as Humanist-geometric hybrid. Frutiger himself described Avenir as a "humanist geometric" — it softens the pure-geometry construction of Futura with pen-sensibility adjustments (e.g., different widths for `O` vs `Q`).
- **Gotham** has proportions closer to American sign-painting geometric tradition than Bauhaus — a distinct substream.

#### Humanist sans

The most recent Linéale subdivision. **Gill Sans** (Eric Gill, Monotype 1928) anchors the English tradition. **Optima** (Hermann Zapf, 1958) — which is also claimed by *Incises*. **Frutiger** (Adrian Frutiger, Paris Charles de Gaulle airport signage 1976). **Myriad** (Robert Slimbach and Carol Twombly, Adobe 1992). **Meta** (Erik Spiekermann, 1991). **Segoe UI** (Steve Matteson, Microsoft 2004). **Lucida Sans** (Charles Bigelow and Kris Holmes, 1985).

Characteristics vs Geometric/Neo-Grotesque:

- Proportions of Humanist/Garalde serif lowercase, drawn without serifs — a true-italic tradition is common.
- Some stroke contrast (the `e` has a thick-thin variation).
- Double-story `a` and `g` drawn with the humanist-Garalde pen sensibility.
- Warmer, more readable voice for long-form text than Neo-Grotesque.

Anchor faces: Gill Sans, Frutiger, Myriad, FF Meta, Segoe UI, Lucida Sans, Stone Sans, Source Sans 3 (Adobe, Paul D. Hunt, 2012), Open Sans (Steve Matteson 2010), Fira Sans (Erik Spiekermann / Carrois 2014).

Traps:

- **Optima** (Zapf, 1958) — arguably the most-disputed classification in all of Vox. Zapf described it as "a serifless roman," the stems taper (thick-thin contrast without serifs), and the terminals flare outward. Vox-ATypI places it under **Linéale Humaniste**; Frutiger's own system (see `./thibaudeau.md` for context) places it in **Incise**; DIN 16518 places it in **Antiqua-Varianten** (glyphic). All three are defensible.
- **Inter** (Rasmus Andersson, 2016), **Roboto** (Christian Robertson, 2011), **SF Pro** (Apple 2015) — modern UI sans with deliberately-mixed DNA. Inter is a Grotesque / Humanist hybrid; Roboto is Neo-Grotesque / Humanist / Geometric hybrid; SF Pro is its own lineage. Classification is educational only — foundries don't treat it as definitional.

### Incises (Glyphic)

Typefaces inspired by **chiseled-stone inscription**, specifically Roman capital inscriptions like the Trajan column (113 CE). Characteristics:

- **Flared stroke endings** instead of bracketed or slab serifs — the stroke widens at the terminal, as if chiseled with a chisel's taper.
- Often no true serifs — the flared terminal replaces the serif.
- Usually caps-only or caps-dominant (inscriptional faces are often uppercase-only).
- Tight letterspacing suitable for display-only use.

Anchor faces: Albertus (Berthold Wolpe, Monotype 1932 — a classic glyphic, text-usable), Copperplate Gothic (Frederic Goudy 1901 — flared, caps-only, was considered Linéale in some classifications because of its lack of proper serifs), Trajan (Carol Twombly, 1989 — caps-only, directly modeled on the Trajan column), Perpetua (Eric Gill, 1929 — a glyphic-influenced roman with more text usability), Friz Quadrata (Ernst Friz 1965), Meridien (Frutiger 1957).

Traps:

- **Copperplate Gothic** is sometimes classified as *Linéale* (because it has no true serifs) and sometimes *Incise* (because of its flared terminals). Modern foundries more often shelve it as Incise.
- **Optima** as noted above.
- **Perpetua** is a hybrid — glyphic terminals, but with serifs proper; sometimes classified as a Garalde with glyphic tendencies, sometimes as Incise.

### Scriptes (Script)

Typefaces imitating **formal handwriting with connected letters**. The letters connect via drawn strokes that extend from one glyph's end to the next glyph's start — requiring careful fit and often OpenType `calt`, `liga`, and `ccmp` lookups to produce clean joins.

Anchor faces: Zapfino (Hermann Zapf / David Siegel, Adobe 1998 — the canonical OpenType script, with up to eight alternates per lowercase letter), Bickham Script (Richard Lipton, Adobe 1997 — formal Copperplate engraving style), Snell Roundhand (Matthew Carter 1966 — after an 18th-c. English writing master), Shelley Script, Edwardian Script, Künstler Script, Kuenstler Script.

Characteristics:

- Slanted (9–15° typical).
- Connected ligation.
- Ornate, formal (as opposed to casual script — which falls in Manuaires).
- Often with multiple stylistic alternates.

### Manuaires (Graphic / Manuary)

The **casual-handwriting** category — hand-lettered letters that do not connect, and do not imitate a formal writing style. The boundary with Scriptes is that Manuaires do not connect; the boundary with Linéale is that Manuaires have an explicitly hand-made feel.

Anchor faces: Klang (Will Carter 1955), Papyrus (Chris Costello, 1982 — the infamous one), Lithos (Carol Twombly, Adobe 1989 — a Greek-stone-carving inspired display), Mistral (Roger Excoffon 1953 — connects but barely; borderline Scripte / Manuaire), Comic Sans (Vincent Connare, Microsoft 1994 — a casual Manuaire), Choc (Excoffon), Banco (Excoffon).

Traps:

- **Mistral** connects its letters but in a casual-cursive way, not a formal-calligraphic way — classified as Scripte or Manuaire depending on authority.
- **Comic Sans** is unambiguously Manuaire in Vox terms.

### Fractures (Black-letter)

The **broken-script tradition** — the original European movable-type typography (Gutenberg 1455 set in *Textura* blackletter). Vox keeps this as a bucket on its own, acknowledging that it stands outside the humanist-roman chronological arc.

Five historical sub-classes (these are DIN's five Gebrochene subdivisions; BS 2961 does not split blackletter):

- **Textura / Textur** — the most angular, tall, narrow blackletter — Gutenberg's Bible, Wycliffe-era manuscripts. Sharp pointed feet, tight lateral compression.
- **Rotunda** — a rounder, Italian-influenced blackletter, still used in Italy and Iberia longer than in Germany.
- **Schwabacher** — a 15th-c. German broken script with curved strokes, less angular than Textura; dominant in early German printing 1500–1530s.
- **Fraktur proper** — the defining German blackletter 1513 onward (the Dürer-Schönsperger collaboration with Johann Neudörffer for Emperor Maximilian I). Angular but with curvy flourishes; the dominant German script until 1941.
- **Kurrent** / Sütterlin — handwritten blackletter (distinct from printed fraktur), a German-language school-taught handwriting script through 1941.

Historical note: **Nazi Germany banned blackletter in January 1941** (the *Normalschrifterlass* / Antiqua Decree of Martin Bormann, which declared Fraktur "Schwabacher Judenlettern" — Jewish-Schwabacher letters — on spurious-Jewish-origin grounds, and replaced it with Antiqua as the official script). This is the reason German typography became roman-dominant postwar; pre-1941 German books set in Fraktur, post-1945 German books set in Antiqua.

Anchor faces: Textur (Berthold Textur, Monotype Old English), Fette Fraktur (Berthold 1875), Walbaum Fraktur, Fette Schwabacher, San Marco, Wilhelm Klingspor Gotisch, Blackmoor, Cloister Black.

### Étrangères (Non-Latin) — 2010

Added in the 2010 revision as an acknowledgment that non-Latin scripts — Arabic, Hebrew, Greek, Cyrillic, Devanagari, CJK, Thai, Hangul, Ethiopic, etc. — don't fit the Latin-rooted categories. This is not a serious classification of non-Latin typography; each script has its own history and conventions, documented script-by-script in `../scripts/`.

**Practical note**: real global foundries (Adobe, Google Noto, Indian Type Foundry, 29Letters, ArabicType, Latinotype for non-Latin-Latin, Typotheque) do *not* use "Étrangères" to describe non-Latin work. They use script-specific classifications: naskh / nastaliq / kufi for Arabic; unicameral categories for Hebrew; monotonic / polytonic for Greek; etc.

---

## Strengths

The Vox-ATypI system, despite its age and limits, remains in wide use for good reasons.

- **Vocabulary is broadly understood in European type education.** Any typographer trained in France, Germany, the UK, the Netherlands, or Scandinavia will recognize Garalde, Didone, Mécane, Linéale — using them needs no glossing.
- **Maps reasonably onto chronological history.** Teaching typographic history as Humanes → Garalde → Réale → Didone is a faithful simplification of what happened in European printing between 1460 and 1850.
- **Lineale subclassification captures meaningful sans-serif distinctions.** Grotesque vs Neo-Grotesque vs Geometric vs Humanist is the most durable output of BS 2961 and is now universal.
- **Categories reflect design sensibility, not just mechanics.** Unlike Thibaudeau's silhouette-based classification (see `./thibaudeau.md`), Vox's names refer to cultural / historical voice (Didone = the Didot-Bodoni Enlightenment sensibility), not just serif shape.

## Weaknesses and seams

Known limits, roughly in order of severity:

- **Non-Latin is entirely subsumed in one bucket.** Étrangères is not a classification; it's a punt. Anyone working in global typography needs per-script conventions; Vox is not adequate.
- **Digital-era innovation doesn't map.** Variable fonts, superfamilies (a single family with both serif and sans — Fedra, Skolar, Fraunces), icon fonts, emoji fonts, color fonts, COLRv1, and the screen-first UI-sans tradition (Inter, SF Pro, Roboto) don't fit any single category.
- **Some fonts genuinely don't fit any category.** Reverse-contrast faces (Karloff, Stencil, Big Moore — where the horizontals are heavier than the verticals, inverting the Didone contrast); grunge / distressed faces (Trixie, Remingtoned); experimental / deconstructivist display (Emigre faces from the 1990s); the "neo-transitional" contemporary tradition (Tiempos — Kris Sowersby, Klim 2010; Questa — Jos Buivenga and Martin Majoor 2014).
- **Boundary between Garalde and Réale is fuzzy.** Caslon is the canonical example; Baskerville is arguably transitional-Garalde; Times New Roman sits on the boundary. Practitioners handle this case-by-case.
- **Manuaires and Scriptes overlap.** Mistral and Excoffon's work is the running example; the connection criterion (connected → Scripte, unconnected → Manuaire) doesn't hold up for every face.
- **Contemporary neo-transitional faces sit between categories.** Tiempos is explicitly designed as "a contemporary neo-transitional" — it's Garalde in its proportions and Didone in its contrast. Questa is a literal merger of Didone and Sans within one family. Neither fits Vox cleanly.
- **Optical-size variants don't have category mobility.** A single face like Source Serif 4 has an `opsz` axis from 8pt to 60pt — at 8pt it reads more like Réale/Transitional, at 60pt more like Didone. Vox has no vocabulary for size-conditional classification.
- **Linéale subclasses don't cover screen-first sans.** Inter, Roboto, SF Pro, Segoe UI — arguably a new subclass ("UI Neo-Grotesque" or "Screen-first sans") — are shelved as Humanist or Neo-Grotesque based on the classifier's preference, with neither being fully accurate.

---

## Modern practice

Where Vox-ATypI actually lives in 2026:

- **European type education** — still taught as the reference classification in European type programs (École Estienne, Atelier National de Recherche Typographique, KABK, Reading, and others).
- **Foundry specimens** — historically-leaning foundries (Storm, Rosetta, TypeTogether, Commercial Classics, HTF) use Vox vocabulary. Contemporary foundries (Klim, GT, Pangram Pangram, Sharp, Dinamo) often don't — they use looser genre categories ("sans," "serif," "slab," "display," "mono," "script").
- **ATypI website** — continues to reference the Vox-ATypI classification (visible on atypi.org as of 2026-04-18).
- **Wikipedia and type-education material** — Vox-ATypI is the default classification used by any English-language type-history reference, with BS 2961's English names.
- **Digital-foundry marketing** — largely superseded by informal genre buckets. Adobe Fonts, Google Fonts, MyFonts, FontShop, Future Fonts, and Type Network all use a looser taxonomy (Serif, Sans Serif, Display, Slab, Script, Handwritten, Monospaced, Blackletter) that doesn't map cleanly to Vox. When Vox vocabulary appears, it's in category descriptions or subcategory filters ("Old Style" ≈ Garalde; "Transitional" ≈ Réale; "Modern" ≈ Didone; "Humanist Sans" ≈ Linéale Humaniste).
- **Academic type history and criticism** — still uses Vox as its reference vocabulary.
- **International type-design competitions** (Type Directors Club, ATypI's own Letter.2) — accept work in Vox categories alongside looser groupings.

Practical rule: **Vox-ATypI is useful vocabulary for precise type discussion** (when you need to communicate that Minion is Garalde and Baskerville is Transitional), but **ineffective as a contemporary taxonomy** when applied to the full modern corpus.

---

## Examples of classification disagreements

A list of faces where practitioners legitimately disagree — these are the cases to teach when demonstrating the seams of the system.

| Face | Vox (typical) | Alternative | Why it's contested |
|------|---------------|-------------|---------------------|
| **Optima** (Zapf 1958) | Linéale Humaniste | Incise (Frutiger's system, DIN's Antiqua-Varianten) | Flared chisel-terminals + humanist proportions — both defensible |
| **Caslon** (1720s) | Garalde | Réale / Transitional | Dated to the Transitional era but designed in the Garalde tradition |
| **Copperplate Gothic** (1901) | Incise | Linéale (no true serifs) | No true serifs but flared terminals — structurally glyphic, visually sans |
| **Futura** (1927) | Linéale Géométrique | — (canonical) | Well-established; the Geometric anchor |
| **Perpetua** (1929) | Incise | Garalde with glyphic tendencies | Has serifs but with chiseled-inscription design influence |
| **Times New Roman** (1932) | Réale | Garalde, or "newspaper transitional" | Designed as a transitional-derivative; sits on the boundary |
| **Avenir** (1988) | Linéale Géométrique | Linéale Humaniste Géométrique | "Humanist geometric" per Frutiger himself |
| **Fraunces** (Undercase Type, 2020) | — (resists clean classification) | Variable Garalde / Didone superfamily | An opsz+wght+SOFT+WONK variable that spans multiple traditions |
| **Comic Sans** (1994) | Manuaire | — | Uncontroversially Manuaire |
| **Trade Gothic** (1948) | Linéale Grotesque | — | Canonical American grotesque |
| **Recursive** (Stephen Nixon, 2021) | — (resists) | Linéale Sans/Mono with `CASL` (casual) + `slnt` axes | Variable font spanning sans, mono, casual, oblique |
| **Tiempos** (Klim, 2010) | Réale / Didone hybrid | "Neo-transitional" | Explicitly designed between Garalde and Didone |
| **Inter** (Andersson, 2016) | Linéale Grotesque / Humaniste | "UI sans" (new category) | Modern UI-first sans with deliberate hybrid DNA |
| **Mistral** (Excoffon, 1953) | Scripte or Manuaire | — | Connects but casually — boundary case |
| **Avant Garde Gothic** (Lubalin/Carnase, 1970) | Linéale Géométrique | — | Uncontroversially geometric |

These cases are pedagogically useful precisely because they demonstrate where the system's seams are.

---

## Cross-references

- `./bringhurst.md` — Bringhurst's essayistic alternative to Vox, using historical-era names (Renaissance, Baroque, Neoclassical, Romantic, Realist, Geometric Modernist, Lyrical Modernist, Expressionist, Postmodern).
- `./din-16518.md` — German parallel classification with more granular blackletter subdivisions and separate categories for glyphic (Antiqua-Varianten) and hand-casual (Handschriftliche Antiqua).
- `./thibaudeau.md` — 1921 silhouette-based classification (Antiques / Égyptiennes / Elzévirs / Didots) — historical footnote; Vox superseded it.
- `../historical/humanist-renaissance.md` — deep narrative of Jenson → Aldus/Griffo → Garamond era (the Humanes + Garalde chronology).
- `../historical/transitional.md` — Baskerville, Fournier, Caslon era (Réales).
- `../historical/modern.md` — Didot and Bodoni era (Didones).
- `../historical/slab-egyptian.md` — 19th-c. slab-serif commercial printing (Mécanes).
- `../historical/sans-grotesque.md` — Akzidenz-Grotesk lineage (Linéale Grotesque).
- `../historical/humanist-sans.md` — Gill, Frutiger, Myriad (Linéale Humaniste).
- `../historical/geometric-sans.md` — Futura, Avenir, Kabel (Linéale Géométrique).
- `../historical/neo-grotesque.md` — Helvetica, Univers, Arial (Linéale Neo-Grotesque).
- `../historical/blackletter.md` — Textura, Rotunda, Schwabacher, Fraktur (Fractures).
- `../scripts/` — per-script conventions; the Étrangères bucket is a placeholder, not a classification.

---

## Sources

- Vox, Maximilien. *Pour une nouvelle classification des caractères* (École Estienne, Paris, 1954). The founding document.
- ATypI — "Classification Vox-ATypI", adopted Stockholm 1962, lightly revised 2010. atypi.org referenced 2026-04-18.
- BSI. *BS 2961:1967 — Typeface Nomenclature and Classification*. British Standards Institution, 1967. (Withdrawn from active status but still referenced.)
- Jaspert, W. Pincus, Berry, W. Turner, Johnson, A. F. *The Encyclopaedia of Type Faces* (Blandford, 4th ed. 1970). The English-language practitioner reference for classification through the 1970s.
- Lawson, Alexander. *Anatomy of a Typeface* (David R. Godine, 1990). English-language type history with Vox-ATypI vocabulary throughout.
- Blackwell, Lewis. *Twentieth-Century Type* (Laurence King, rev. 2004). Covers the expansion of Linéale through the 20th century.
- McLean, Ruari. *The Thames & Hudson Manual of Typography* (1980). BS 2961 vocabulary.
- Bringhurst, Robert. *The Elements of Typographic Style* (4th ed., Hartley & Marks, 2012) — ch. 7 "Historical Interlude" critiques Vox and proposes the alternative covered in `./bringhurst.md`.
- Kinross, Robin. *Modern Typography: An Essay in Critical History* (Hyphen Press, 2nd ed. 2004). Critical history of typographic categories.
- Kupferschmid, Indra — writings on kupferschrift.de and type.today on classification critique and contemporary type.
- Wikipedia, "Vox-ATypI classification" (en.wikipedia.org, content cross-checked against Jaspert and Blackwell; accessed 2026-04-18).
- I Love Typography — historical articles on Vox, Thibaudeau, and Bringhurst classification (ilovetypography.com, accessed 2026-04-18).
