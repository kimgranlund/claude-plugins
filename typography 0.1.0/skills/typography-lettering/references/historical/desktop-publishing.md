---
date: 2026-04-18
coverage: light
peers:
  - ./phototype-era.md
  - ./variable-era.md
  - ./sans-grotesque.md
  - ./humanist-renaissance.md
  - ../techniques/fallback-stacks.md
  - ../contemporary/variable-fonts.md
  - ../metrics/metrics-glossary.md
primary_sources:
  - Meggs, Philip B. & Purvis, Alston W. *Meggs' History of Graphic Design* (6th ed., Wiley, 2016)
  - Kinross, Robin. *Modern Typography* (2nd ed., Hyphen Press, 2004)
  - Heller, Steven & Fili, Louise. *Typology — Type Design from the Victorian Era to the Digital Age* (Chronicle, 1999)
  - Shaw, Paul. *Revival Type — Digital Typefaces Inspired by the Past* (Yale, 2017)
  - https://en.wikipedia.org/wiki/Aldus_PageMaker
  - https://en.wikipedia.org/wiki/PostScript
  - https://en.wikipedia.org/wiki/TrueType
  - https://en.wikipedia.org/wiki/OpenType
  - https://en.wikipedia.org/wiki/Emigre_(magazine)
  - https://en.wikipedia.org/wiki/FontShop_International
  - https://en.wikipedia.org/wiki/Hoefler_%26_Co.
  - https://en.wikipedia.org/wiki/Georgia_(typeface)
  - https://en.wikipedia.org/wiki/Verdana
  - https://en.wikipedia.org/wiki/Erik_Spiekermann
  - https://www.emigre.com/Magazine
  - https://www.myfonts.com/pages/fontshop-30-years-of-fontshop/
  - https://www.moma.org/collection/works/101653
---

# Desktop Publishing Era (1984-2000) — historical reference

The desktop-publishing era is the period when typesetting and page layout moved from dedicated phototypesetting bureaus onto personal computers. It starts in 1984–1985 with three technologies arriving in a tight sequence: **PostScript** (Adobe, 1984), the **Macintosh** (Apple, January 1984), the **Apple LaserWriter** (March 1985), and **Aldus PageMaker** (July 1985). Together they let a designer typeset and lay out a page at their own desk, print a 300-dpi proof, and send a PostScript file to a service bureau for high-resolution imagesetter output. Within five years the phototypesetting industry (see `./phototype-era.md`) was in collapse and typesetting had become a software feature rather than a trade. By 2000 the ecosystem had stabilized around PostScript-compatible OpenType fonts, QuarkXPress and InDesign as the professional page-layout duopoly, Photoshop and Illustrator as the image-and-vector tools, and a rapidly expanding universe of independent digital type foundries.

This file is the light-coverage historical reference for that period. For the predecessor phototype era see `./phototype-era.md`; for the successor variable-font era see `./variable-era.md`; for specific font-technology details see `../contemporary/variable-fonts.md`.

---

## 1984–1985 — the convergence

Four technologies arrive within 18 months and the whole industry pivots.

### PostScript (Adobe, 1984)

John Warnock and Chuck Geschke, formerly of Xerox PARC, founded **Adobe Systems** in 1982. PostScript — a Turing-complete stack-based page description language, coupled to an outline-font format (**PostScript Type 1**, using cubic Bézier curves) — shipped publicly in 1984. Its design brief was device independence: the same PostScript file, sent to a 300-dpi laser printer or a 2540-dpi imagesetter, produced output at the device's native resolution.

PostScript achieved three things at once:
- **Vector font outlines.** Type 1 fonts were scalable to any size without the phototype-era loss of optical sizing (though optical-size-specific cuts were still produced as separate fonts at this stage — optical sizing as an *axis* returns only with variable fonts, see `./variable-era.md`).
- **Device-independent output.** The same file rendered at 300 dpi on a LaserWriter and at 2540 dpi on a Linotronic 300 imagesetter with automatically resolved hinting.
- **Licensable font format.** Fonts became discrete digital assets with documented file formats and licensing terms, rather than foundry-internal proprietary tooling.

Apple licensed PostScript for the Apple LaserWriter in 1985 — a huge, lucrative deal that funded Adobe's first several years. The LaserWriter cost about $7,000, contained an early 68000 CPU running PostScript, and shipped with **thirteen built-in Type 1 fonts** (Times, Helvetica, Courier, and Symbol in regular/bold/italic/bold-italic variants, plus a single cut of what would later be extended to ITC Bookman, Avant Garde, Palatino, Century Schoolbook, Zapf Chancery, Zapf Dingbats, Helvetica Narrow, and the New Century Schoolbook family in the later "LaserWriter Plus" model of 1986).

### Macintosh + PageMaker

The **Apple Macintosh** (January 1984) provided a graphical user interface with bitmap fonts and WYSIWYG layout. **Aldus PageMaker** (July 1985, by Paul Brainerd's Aldus Corporation) was the first widely-used WYSIWYG page-layout program — running on the Mac, outputting to the LaserWriter, and letting a user place text and graphics on a visible page that resembled the printed result. Brainerd coined the term "desktop publishing" to market PageMaker.

Within two or three years the combination Macintosh + PageMaker + LaserWriter + PostScript had displaced the phototype-composition-plus-paste-up workflow at thousands of small publishers, newsletter producers, in-house graphics departments, and ad agencies. Magazines and books at the mid-market level moved to desktop publishing across 1986–1990. Large newspapers and high-end book publishers followed more slowly, with QuarkXPress (first released 1987 for Mac) becoming the professional page-layout standard through the 1990s.

### QuarkXPress and the professional workflow

**QuarkXPress** (Quark Inc., Denver; first released 1987) was PageMaker's professional competitor. More precise typographic control, better multi-page document handling, better handling of long-document and color workflows. By about 1990 QuarkXPress had displaced PageMaker as the professional standard and held that position into the 2000s. Aldus was acquired by Adobe in 1994, PageMaker was eventually discontinued, and Adobe's own **InDesign** (first release 1999 as version 1.0; serious adoption from version 2.0, 2002) replaced QuarkXPress as the professional standard across the mid-2000s.

---

## Type technology — Type 1, TrueType, OpenType

### PostScript Type 1 (Adobe, 1984)

- Cubic Bézier outlines.
- Proprietary format; Adobe held the spec closed through the late 1980s. The **Type 1 Font Format specification** (the "black book") was published in 1990 under external pressure.
- **Hinting** via proprietary instructions interpreted by the Adobe Type Manager (ATM) or PostScript interpreter.
- Licensed per workstation; foundry-supplied fonts for professional use.

Type 1 was the professional standard through the 1990s. Adobe's PostScript-for-Windows (via ATM) and LaserWriter ecosystem held the high-end market.

### TrueType (Apple + Microsoft, 1991)

In the late 1980s, Apple chafed at Adobe's PostScript licensing fees. Apple developed **TrueType** as an alternative outline-font format: quadratic Bézier curves (Bézier splines with one control point; technically different from Type 1's cubics), integrated into the Mac OS at the operating-system level (not requiring a separate interpreter like ATM), and with a more extensible hinting bytecode than Type 1. Apple cross-licensed TrueType to Microsoft, and **System 7** (Mac OS, May 1991) and **Windows 3.1** (April 1992) both shipped with TrueType as the native font format.

The 1990s had a parallel font ecosystem:
- **PostScript Type 1** — professional use, service bureaus, professional designers, high-end publishing.
- **TrueType** — consumer use, office work, default Windows/Mac system fonts.

Serious designers in 1995 might have both on their workstation.

### OpenType (Microsoft + Adobe, 1996–2001)

**OpenType** emerged from a mid-1990s convergence. Adobe and Microsoft collaborated to unify the two font formats into a single container. The resulting specification:

- **Container-agnostic glyph outlines** — an OpenType file can contain TrueType outlines (quadratic, `glyf` table) *or* PostScript CFF outlines (cubic, `CFF` table).
- **Unicode codepoint-to-glyph mapping** (`cmap` table).
- **Advanced layout tables** (`GSUB` for glyph substitution including ligatures, small caps, stylistic alternates; `GPOS` for positioning including kerning, mark-to-base attachment, contextual positioning). These replace the font-internal kerning `kern` table and enable complex-script typography.
- **Cross-platform** — one `.otf` or `.ttf` file works on Mac, Windows, Linux.

OpenType was **announced in 1996**, the specification was stabilized across 1996–2000 (OpenType 1.0 in 1997 through 1.3), and **OpenType 1.4** was published in **February 2004** — the version that is the *de facto* professional baseline and that adds TrueType Collections and refined tables. Adobe finished converting its professional type library to OpenType (CFF flavor) across 2000–2002, which is the moment the professional ecosystem shifted decisively to OpenType. See the OpenType Wikipedia article for the full version history.

OpenType reached full enterprise adoption in the 2000s. It is the format every contemporary font (2026) ships — including variable fonts, which are a 2016 extension (OpenType 1.8, see `./variable-era.md`).

---

## Digital-first type designers

With Type 1 and TrueType, designers could draw fonts on a Mac in **Fontographer** (Altsys, 1986; later Macromedia; later acquired into FontLab, relaunched as FontLab Fontographer 5.0 in 2010) or **FontStudio** (Letraset, 1989). A designer did not need a foundry's drawing office and punchcutting or phototype production machinery. **The barrier to producing a distributable font collapsed from a foundry investment to a personal computer plus a drawing app.**

This enables a new kind of type designer — **digital-first**, working in outline tools from the start, releasing via small-scale distribution.

- **Matthew Carter** (b. 1937) — bridge figure. Trained in metal punchcutting at Enschedé, worked through phototype at Linotype, designed Bell Centennial (1978, for the AT&T Yellow Pages). In the desktop-publishing era he co-founded **Bitstream** (1981, with Mike Parker), a pioneering digital-first foundry. Later **Carter & Cone Type** (1992). His defining contributions: **Verdana** (1996, Microsoft), **Georgia** (released 1996, Microsoft, designed 1993), **Big Caslon** (1994), **Miller** (1997, a Scotch Modern revival), and dozens of commissioned faces.
- **Tobias Frere-Jones** (b. 1970) — digital-first. **Interstate** (1993, Font Bureau — based on the US Federal Highway Administration's Highway Gothic). **Retina** (1999, for *The Wall Street Journal*'s stock-quote pages, ink-trap compensated). **Gotham** (2000, Hoefler Frere-Jones for *GQ*). **Whitney** (2004, for the Whitney Museum). **Mallory** (2015, Frere-Jones Type). Consequential throughout the desktop-publishing era and the variable-font era.
- **Jonathan Hoefler** (b. 1970) — founded **Hoefler & Co.** (originally Hoefler Type Foundry, 1989) in New York. **HTF Didot** (1991, for *Harper's Bazaar*), **Hoefler Text** (1991, bundled with Mac System 7.5 as part of the system fonts), **Requiem** (1992), **Mercury** (1996), **Whitney** (with Frere-Jones, 2004), **Archer** (2008), **Sentinel** (2009). Partnered with Tobias Frere-Jones 1999–2014 as Hoefler & Frere-Jones; that partnership dissolved acrimoniously in 2014 (settled late 2014) and the firm reverted to Hoefler & Co.
- **Carol Twombly** (b. 1959) — Adobe. **Trajan** (1989, based on the Column of Trajan inscription capitals — all-caps, no lowercase, no italic). **Adobe Caslon Pro** (1990, careful Caslon revival from original Caslon specimen sheets). **Nueva** (1994), **Myriad** (1992, with Robert Slimbach), **Chaparral** (2000), **Lithos** (1989).
- **Robert Slimbach** (b. 1956) — Adobe. **Adobe Garamond** (1989, based on original 1540s Garamond and Granjon types). **Minion** (1990, Aldine-synthesis body face). **Myriad** (with Twombly, 1992). **Warnock** (2000, named for Adobe co-founder). **Adobe Jenson Pro** (1996). **Arno** (2007). **Garamond Premier Pro** (2005, the highest-fidelity Garamond Slimbach drew, based on original specimens at Plantin-Moretus). **Kepler** (2003). Variable-font-era work continues at Adobe.
- **Sumner Stone** (b. 1945) — Adobe's first director of typography (1984–1990). Supervised Adobe Type Manager and the initial Adobe Originals program. **Stone family** (1987, a sans+serif+informal system).
- **Zuzana Licko** (b. 1961) — **Emigre Fonts** (1984, co-founded with Rudy VanderLans). Designed the first Emigre bitmap fonts for the original 72-dpi Mac screen; later **Oakland**, **Filosofia** (Bodoni revival), **Mrs Eaves** (Baskerville revival), **Matrix**, **Modula**. Licko's is the definitive digital-first voice; her early work in 1984–1987 bitmap fonts is historically consequential because it was the first serious type design **conceived for the new pixel grid** rather than adapted to it.
- **Erik Spiekermann** (b. 1947) — founder of MetaDesign, FontShop, and later Edenspiekermann. **FF Meta** (1991, originally commissioned 1985 for the Deutsche Bundespost; see `./sans-grotesque.md` §humanist-sans for more). **FF Info** (2000). **FF Unit** (2003). Influential as practitioner, commentator, and foundry principal.
- **Lucas de Groot** (b. 1963) — **FF Thesis** (1994, a vast superfamily with TheSans, TheSerif, TheMix). Influential contribution to the desktop-publishing-era idea of a comprehensive typographic system released as one family.
- **Martin Majoor** (b. 1960) — **FF Scala** (1990, Aldine-humanist serif) and **FF Scala Sans** (1993, humanist sans paired with the serif). FF Scala is a canonical desktop-publishing-era release — designed specifically for digital, with PostScript-scalable outlines, and released via FontShop.

---

## Emigre — the 1980s–90s digital renaissance

**Emigre** (the magazine, the foundry, and the editorial voice) is the cultural center of the 1980s–90s digital type renaissance.

- **Founding**: 1984 by **Rudy VanderLans** (Dutch, b. 1955) with Marc Susan and Menno Meyjes as original collaborators; by issue 6 (1986) VanderLans was sole editor/art director. His wife **Zuzana Licko** (b. 1961) joined in late 1984 to design bitmap fonts for the magazine's Mac-based production.
- **Emigre magazine, 1984–2005** — 69 issues over 21 years, irregular schedule. A showcase for postmodern digital typography and graphic design. Each issue could be topical, monographic, or polemical; the magazine was influential on a generation of design students and practitioners. MoMA acquired the complete 1–69 run for its permanent design collection (catalog 101653).
- **Emigre Fonts** — the foundry branch. Licko's early fonts (Emperor, Oakland, Emigre, Modula, Matrix, all 1985–1990) were pioneered at the coarse Mac pixel grid before Adobe Type 1 or TrueType were common; later fonts (Filosofia 1996, Mrs Eaves 1996, Mrs Eaves XL 2009) moved to scalable formats and remain widely used.
- **Barry Deck, Jeffery Keedy, Elliott Peter Earls, P. Scott Makela** — designers published through Emigre Fonts and featured in Emigre magazine. Deck's **Template Gothic** (1990, Emigre, based on a distressed vernacular-Gothic sign he saw in a laundromat), Keedy's **Keedy Sans** (1991, Emigre), and Makela's various experimental designs defined the postmodern / grunge / "deconstructionist" typography of the early 1990s.

Emigre's significance — the magazine, the foundry, Licko as designer — is that it legitimized **digital-native type design**. Type no longer had to derive from metal or even from phototype models; it could be conceived on a Mac screen for Mac-screen readers, and its aesthetic could break explicitly with Swiss neutrality, metal-era Renaissance revivalism, and any sense of typographic "rules."

---

## FontShop and independent distribution

**FontShop** (1989, Berlin) was **Erik Spiekermann** and **Joan Spiekermann**'s distribution and publishing house. FontShop's model was manufacturer-independent retail: a designer or small foundry could submit fonts to FontShop, which published them under the **FontFont** label (founded 1990, with Neville Brody as co-founder) and distributed them globally through FontShop's growing international branches (Canada, UK, Sweden, Benelux, Italy, North America).

FontFont published canonical 1990s digital releases:
- **FF Meta** (Spiekermann, 1991)
- **FF Scala** + **FF Scala Sans** (Majoor, 1990, 1993)
- **FF Thesis** superfamily (Lucas de Groot, 1994)
- **FF DIN** (Albert-Jan Pool, 1995)
- **FF Dax** (Hans Reichel, 1995)
- **FF Dingbats** (Brody)
- **FF Trixie** (Erik van Blokland, 1991)
- **FF Beowolf** (van Blokland + van Rossum, 1990 — the "randomized" font)
- **FF Typestar** (Steffen Sauerteig, 1999)

FontFont and Emigre together are the two canonical **author-controlled** digital foundries of the 1990s — they published designers' work and paid royalties, bypassing the older foundry-employment model. FontShop Berlin was acquired by Monotype in 2014; the FontFont library is now distributed through Monotype's brand stack.

---

## Hoefler & Co. and premium foundry-as-commissioning-house

**The Hoefler Type Foundry** (later **Hoefler & Co.**; briefly **Hoefler & Frere-Jones** 1999–2014) was Jonathan Hoefler's New York foundry from 1989. Its model was different from FontShop's or Emigre's — not retail distribution of a broad catalog, but premium commissioning for corporate identity and editorial clients. The client list (*Rolling Stone*, *GQ*, *Esquire*, *Wall Street Journal*, Apple, American Apparel) is the marker.

Canonical releases (1991 through the 2010s):
- **HTF Didot** (1991) — high-contrast Modern for *Harper's Bazaar*
- **Hoefler Text** (1991) — bundled with Mac System 7.5 and subsequent macOS through about 2020 as a system font (a rare commercial face becoming a system font by OS-vendor licensing deal)
- **Champion Gothic** (1990)
- **Requiem** (1992)
- **Mercury** (1996) — newspaper workhorse
- **Gotham** (2000) — geometric sans, famous through the 2008 Obama campaign
- **Archer** (2008) — slab with calligraphic ball-terminal detail
- **Sentinel** (2009) — slab serif pair
- **Whitney** (2004) — humanist sans, originally for the Whitney Museum
- **Tungsten** (2009), **Gotham Narrow**, **Gotham Rounded**, etc. — the Gotham family extended through the 2010s

The **2014 split** — Frere-Jones's lawsuit against Hoefler, alleging an oral 1999 agreement that entitled him to half ownership; the subsequent confidential settlement (October 2014); the reversion of the firm to "Hoefler & Co.", and the launch of Frere-Jones Type as Frere-Jones's separate foundry — is the canonical 2010s type-foundry drama. Both firms remain active in the variable-font era.

---

## Microsoft Core Fonts for the Web (1996)

In November 1996 Microsoft released the **Core fonts for the Web** package — free TrueType fonts licensed for no-cost use, distributed with Internet Explorer 4.0 and available separately for Mac and Windows. The original package:

- **Arial** (Nicholas & Saunders, Monotype, 1982) + Arial Bold, Italic, Bold Italic, Arial Black
- **Verdana** (Matthew Carter, 1996) + three additional cuts — designed specifically for screen readability at low resolution. High x-height, wide letterfit, generous aperture, hinted by Tom Rickner for ClearType / pixel-grid fidelity.
- **Georgia** (Matthew Carter, 1996, designed 1993–1996) + three cuts — a serif companion to Verdana, designed to be legible as body text on 96-dpi CRT displays. Notable for its generous x-height, robust stroke contrast for screen, and four-style family.
- **Comic Sans** (Vincent Connare, 1994; released in Core fonts 1996) — designed as a UI font for Microsoft Bob (a home-computing project that shipped briefly in 1995). Now infamous for over-use in inappropriate contexts.
- **Trebuchet MS** (Vincent Connare, 1996) — humanist sans.
- **Impact** (Geoffrey Lee, 1965; included in Core fonts) — condensed display sans.
- **Andale Mono** (Steve Matteson, 1995) — monospace.
- **Courier New** (Monotype), **Times New Roman** (Monotype), **Webdings** — bundled.

Georgia and Verdana were particularly consequential. They became the **screen-first defaults** of the web from 1996 until roughly 2010, when variable-system-font stacks started replacing them. Georgia was the dominant serif on the web (NYTimes.com until 2014; thousands of blogs; editorial sites) and Verdana the dominant sans (defaults for hundreds of thousands of sites through the 2000s).

Matthew Carter's design brief for Georgia and Verdana was **screen-first** — not "print type shrunk to screen," but type conceived for the 96-dpi CRT pixel grid from scratch. This is the first time a first-class type designer worked directly with pixel constraints (parallel to Licko's bitmap Emigre work) and produced faces explicitly optimized for screen.

---

## Type pricing and access — commodification

Before desktop publishing, professional fonts cost thousands of dollars per workstation. A phototype foundry license for ITC Garamond in 1980 might be $500–$2,000 per machine; a full pro library on a Linotron could cost the equivalent of $20,000+ in 2026 dollars. Fonts were controlled, expensive, professional assets.

Desktop publishing commodified them:
- **1984**: the LaserWriter shipped with 13 fonts bundled.
- **1990**: an Adobe Type Basics pack of 60+ Type 1 fonts retailed for about $199.
- **1995**: FontShop retail for individual FontFont cuts at roughly $40 per weight.
- **2000s**: MyFonts (founded 1999) and other discount-aggregator sites offered individual cuts for $20–$40.
- **2005+**: **Google Fonts** (publicly launched 2010) offered hundreds of fonts for free under the SIL Open Font License.
- **2010+**: free-font ecosystem explodes — The League of Moveable Type, Font Squirrel, Google Fonts, hundreds of independent free foundries.
- **2015+**: open-source foundries (IBM Plex in 2017, Google Noto's continued expansion, Inter in 2016/17, Public Sans in 2020) offer professional-grade faces under permissive licenses.

The net effect: in 2026 a designer can equip a project with a professional variable-font system (Inter, IBM Plex Serif, Roboto Flex, Source Sans 3, Source Serif 4, Noto for all scripts) for zero license cost — a shift that would have been unimaginable in 1984.

---

## Early web typography (1993–2000)

The desktop-publishing era overlaps the early web's arrival. Mosaic (NCSA, 1993), Netscape Navigator (1994), Internet Explorer (1995) all shipped with minimal typography: default serif (usually Times New Roman), default sans (usually Helvetica/Arial), default monospace (Courier), and no mechanism for page-specified fonts beyond `<font face="...">` markup (Netscape 1995) and later CSS `font-family` (CSS1, December 1996).

Two technical constraints shaped 1990s web typography:

1. **No webfonts.** A browser could only render fonts the user already had installed. Specifying `font-family: "Futura"` on a page meant Futura rendered only on machines with Futura locally — otherwise the browser fell back to its platform default. The "web-safe" shortlist of fonts present on both Mac and Windows (Times New Roman, Arial, Helvetica, Georgia, Verdana, Courier New, Comic Sans) dominated web typography for over a decade.

2. **Low-resolution screens.** 72-dpi CRTs (Mac) and 96-dpi CRTs (Windows) rendered type at far lower fidelity than print. Many print-derived faces (Bembo, Garamond, Caslon) were unreadable at body size on these screens. The Core Fonts for the Web initiative (Verdana + Georgia, 1996) addressed this directly by designing new faces for the pixel grid.

**@font-face** (CSS2 Fonts, 1998 specification; abandoned in CSS 2.1 in 2002 and reintroduced in CSS3 Fonts) was technically specified in 1998 but not widely implemented. Microsoft's **EOT** (Embedded OpenType) format, shipped with IE4 (1997) and IE5, was an early attempt at webfont delivery; **TrueType Collection** / **OpenType** webfont formats were not widely supported until the 2009 rise of the WOFF format and then WOFF2 (2014).

The result: web typography was stuck at the Core Fonts shortlist from 1996 until roughly 2010, when WOFF webfonts became broadly viable and services like Typekit (Adobe, launched 2009), Fonts.com (Monotype), Webtype, and Google Fonts (launched as Google Web Fonts 2010) made professional fonts available on the web. This delay is why the 1995–2010 web is typographically less varied than 1990 print — the desktop-publishing-era explosion of digital type was artificially constrained at the browser for fifteen years.

---

## Consequences — anyone can typeset

Before 1985, typesetting was a trained profession. Union compositors and typesetters set text at local newspapers, trade presses, and service bureaus; roughly 15,000 typesetters worked in New York City alone at the peak of the phototype era in the 1970s. After 1990, typesetting is a software feature embedded in every word processor, page-layout app, and later every web browser. By 2005 the trade of typesetter is largely extinct outside of high-end book publishing.

This democratization produced three things simultaneously:
1. **Access** — designers, writers, small businesses, students could set type at their own desk.
2. **Volume** — the quantity of typeset output exploded. Most of it was typographically mediocre.
3. **Skill loss** — the trained knowledge of the professional typesetter (optical letterspacing, rag correction, widow/orphan control, hanging punctuation, H&J quality) was no longer embedded in the production pipeline. Authors produced their own pages with word-processor defaults, and those defaults were (and mostly still are) typographically poor.

Web typography, 1995–2010, was particularly weak — limited to a handful of web-safe fonts (Times, Georgia, Verdana, Arial, Courier), poor kerning, no hyphenation, bad measure control, no small caps, no old-style figures, no true italic distinction. The variable-font era (2016+) and CSS Fonts L4 are substantially the correction.

---

## Adobe Originals and the revival program

Parallel to independent digital-first designers, **Adobe Originals** (the Adobe in-house type program founded by Sumner Stone in 1984 and continued under Thomas Phinney, Robert Slimbach, and Carol Twombly) pursued a deliberate revival and commissioning program over 1988–2010 that produced many of the 2020s' most-used professional text faces.

Representative releases from the Adobe Originals program:

- **Adobe Garamond** (Slimbach, 1989) — based on 1540s Garamond; a breakthrough digital Garamond that displaced ITC Garamond in many professional contexts.
- **Adobe Caslon** (Twombly, 1990) — careful Caslon revival from original Caslon specimen sheets.
- **Minion** (Slimbach, 1990) — Aldine-derived body face; later Minion Pro (2000) and Minion 3 (2020, variable).
- **Myriad** (Slimbach + Twombly, 1992) — humanist sans that became Apple's corporate face 2002–2014.
- **Trajan** (Twombly, 1989) — Roman-inscription capitals; became ubiquitous in early-2000s movie-poster and book-cover typography ("every movie poster is Trajan" was the 2000s meme).
- **Adobe Jenson** (Slimbach, 1996) — Venetian humanist revival with Multiple-Master optical-size originally, later OpenType four-optical-sizes (Caption / Regular / Subhead / Display).
- **Warnock** (Slimbach, 2000) — named for Adobe co-founder John Warnock.
- **Chaparral** (Twombly, 2000) — slab-serif book face.
- **Arno** (Slimbach, 2007) — Italian-Renaissance-inspired literary face.
- **Garamond Premier Pro** (Slimbach, 2005) — the most scholarly Garamond revival Slimbach drew, based on original Garamond and Granjon specimens at the Plantin-Moretus museum in Antwerp.

The Adobe Originals program is the single largest contribution to the 1989–2010 digital revival canon. A contemporary editorial designer reaching for a "generic but excellent" serif workhorse often reaches for Minion or Warnock; a Garamond revivalist reaches for Garamond Premier Pro; a Caslon revivalist reaches for Adobe Caslon Pro. These are desktop-publishing-era commissions that continue to shape 2020s professional practice.

---

## Anti-patterns from the desktop-publishing era that persist

| Pattern | Era origin | Why persistent | What to do instead |
|---|---|---|---|
| Using Times, Helvetica, Arial, Courier as defaults without intention | 1985 LaserWriter bundled fonts | These shipped free with every printer and became the lazy defaults. "Times" evokes "default Microsoft Word document" rather than any editorial intention. | Choose the face intentionally. For editorial body text, a contemporary serif (Source Serif 4, Literata, Tiempos, Lyon). For UI, a modern sans (Inter, SF Pro, Segoe UI, Source Sans 3). |
| Using Comic Sans for informal-tone contexts | 1996 Core fonts | It shipped with Windows and Mac; it was the easy "friendly" choice. | Friendly but readable sans (Fira Sans, Nunito, Comfortaa, DM Sans) or a proper display face for emphasis. Comic Sans's limited weight range and unhinted rendering on modern devices are additional reasons to skip. |
| Unkerned text from word-processor defaults | 1990s word-processor implementations did not apply font kerning tables by default | Microsoft Word's default was (for a long time) `KERNING OFF`; designers used to Word output accept the look. | In CSS, use `font-kerning: normal` (default in most UAs) and ensure the font has real `GPOS` kerning. In Word, enable kerning explicitly. |
| Synthetic bold/italic as a substitute for true cut variants | 1990s Type 1 / TrueType defaults | Word processors and earlier browsers applied algorithmic bold/italic to single-cut fonts (mechanical slant for italic; morphological dilation for bold). Default behavior normalized this. | Use `font-synthesis-weight: none; font-synthesis-style: none` in CSS. Ship true italic and bold cuts. See `../contemporary/variable-fonts.md`. |
| "PDF-style" body text at fixed small size regardless of device / viewport | 1990s print-first habits carried into web | Designers trained on print produced web pages at print-body sizes (11–12 pt literally translated). Small screens and retina displays invalidate this. | Responsive type with fluid scale (`clamp()` in CSS), viewport-aware body size, variable-font `opsz`. See `../techniques/optical-size.md`. |
| Windows web-safe stack `Arial, Helvetica, sans-serif` | 1990s Microsoft ecosystem | Default fallback in thousands of Microsoft-tooling-generated CSS outputs. | Modern humanist-sans or system-stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, ...`). See `../techniques/fallback-stacks.md`. |
| Treating "Arial" as a neutral substitute for Helvetica | Arial was commissioned by IBM / Monotype 1982 as metric-compatible Helvetica replacement | It *is* metric-compatible — advance widths match. But the glyph shapes differ in detail. Brand-specified Helvetica rendered as Arial is a license violation masquerading as a rendering choice. | Self-host the specified face. Use Arial only when Arial is what's specified. |

---

## Notable institutional moments

A compact chronology of institutional events that reshaped the desktop-publishing era:

- **1982** — Adobe founded by Warnock and Geschke.
- **January 1984** — Apple Macintosh shipped.
- **1984** — PostScript published.
- **March 1985** — Apple LaserWriter released ($6,995 launch price; the first consumer-accessible PostScript laser printer).
- **July 1985** — Aldus PageMaker 1.0 released; Paul Brainerd coins "desktop publishing."
- **1986** — LaserWriter Plus released with 35 bundled Type 1 fonts (the "LaserWriter 35") that became the 1980s–90s default shared typographic baseline.
- **1987** — QuarkXPress 1.0 released.
- **1989** — Adobe Originals program formalized under Sumner Stone; Hoefler Type Foundry founded; FontShop founded in Berlin.
- **1990** — FontFont library launched by Spiekermann and Brody; Martin Majoor's FF Scala released.
- **1991** — Apple TrueType shipped with System 7; FF Meta released; HTF Didot released; Hoefler Text bundled with System 7.5.
- **1992** — Microsoft Windows 3.1 shipped with TrueType.
- **1994** — Aldus acquired by Adobe; Aldus PageMaker becomes Adobe PageMaker.
- **1996** — OpenType announced; Verdana and Georgia released as Core Fonts for the Web; Comic Sans distributed.
- **1999** — Adobe InDesign 1.0 released; Hoefler partners with Frere-Jones as Hoefler & Frere-Jones.
- **2000s** — OpenType reaches full professional adoption; QuarkXPress losing ground to InDesign across 2002–2006; Frere-Jones and Hoefler release Gotham (2000) used in 2008 Obama campaign.
- **2014** — Hoefler / Frere-Jones dissolve (January lawsuit, October settlement). FontShop and FontFont acquired by Monotype.

This arc — 1982 Adobe founding to 2014 Hoefler / FontShop consolidation — is the institutional backbone of the desktop-publishing era.

---

## Cross-references

- For the **phototype era** that desktop publishing displaced, see `./phototype-era.md`.
- For the **variable-font era** that continues the trajectory, see `./variable-era.md`.
- For **OpenType features** (ligatures, small caps, alternates, `GSUB`/`GPOS`) see `../contemporary/opentype-features.md`.
- For **contemporary font delivery** (WOFF2, subsetting, `unicode-range`) see `../contemporary/font-delivery.md`.
- For **screen-first humanist sans** that Verdana/Georgia inaugurated, see `./sans-grotesque.md` §screen-first-humanist-sans.
- For **digital Garamond / Caslon revivals** of the desktop-publishing era (Adobe Garamond 1989, Adobe Caslon 1990, Adobe Jenson 1996), see `./humanist-renaissance.md`.

## Sources

- **Philip Meggs & Alston Purvis**, *Meggs' History of Graphic Design* (6th ed., Wiley, 2016) — chapters on desktop publishing and digital-era type design.
- **Robin Kinross**, *Modern Typography* (2nd ed., Hyphen Press, 2004) — contextualizes desktop publishing within the broader modernist arc.
- **Steven Heller & Louise Fili**, *Typology — Type Design from the Victorian Era to the Digital Age* (Chronicle, 1999) — surveys desktop-publishing-era digital releases.
- **Paul Shaw**, *Revival Type* (Yale, 2017) — Slimbach's Garamond / Caslon / Jenson digital revivals treated at length.
- **Emigre Inc.** — https://www.emigre.com/ archive, with all 69 magazine issues documented. MoMA collection entry: https://www.moma.org/collection/works/101653.
- **FontShop 30 years retrospective**, MyFonts — https://www.myfonts.com/pages/fontshop-30-years-of-fontshop/. Also Wikipedia's *FontShop International* article.
- **Hoefler & Co.** — https://www.typography.com/ for contemporary catalog; Wikipedia's *Hoefler & Co.* for history of the 2014 split.
- **Matthew Carter / Verdana / Georgia** — MoMA collection, https://www.moma.org/collection/works/139312; Microsoft Learn Verdana/Georgia font pages; Wikipedia's *Verdana* and *Georgia_(typeface)* articles.
- **Aldus PageMaker / Apple LaserWriter / PostScript** — Computer History Museum's Desktop Publishing exhibit; Wikipedia's *Aldus_PageMaker*, *Apple_LaserWriter*, *PostScript*, *TrueType*, *OpenType* articles.
- **John D. Berry**, *Dot-Font: Talking About Design* (Mark Batty, 2006) — collected essays covering the desktop-publishing-era transitions.
