# color-science-project-files

The color-math TypeScript library and interactive demo site behind the
`color-*-facts` family of agent skills. Built from resources I keep looking up,
returning to, and sharing with others.

## What this is

**This folder registers no skill.** It was `color-science` — a single combined
skill + reference corpus + library — until the 2026-07-06 extraction split it in
two: the reference corpus (159 markdown files) moved out into four focused,
independently-routed [agent skills](https://agentskills.io):

- **`color-space-facts`** (72 files) — computational color: spaces, conversions,
  gamut, gradients/ramps, ΔE, HDR/tone mapping, CSS color syntax, quantization,
  palette-generation methods, the library/tool catalog.
- **`color-perception-facts`** (49 files) — vision & appearance science: cones,
  opponent process, appearance models, MacAdam/JND, metamerism, warm-cool, plus the
  full David Briggs (huevaluechroma) and colorandcontrast scrapes.
- **`color-contrast-facts`** (8 files) — contrast standards & CVD: APCA vs
  WCAG 2.2, relative luminance, low vision, colorblindness simulation.
- **`color-material-facts`** (30 files) — physical color & naming: pigment
  mixing (Kubelka-Munk), paint data, print-vs-screen/ICC, iridescence, Pointer's
  gamut, naming standards (ISCC-NBS, Munsell, Ridgway, Jaffer).

What's **left here** is the non-skill remainder — the working TypeScript color-math
library and the demo site built on top of it:

1. **`src/`** — A working TypeScript implementation of the color math (~24 color
   spaces, gamut math, ΔE metrics, CVD simulation, tone mapping, dithering, K-M
   pigment mixing, spectral integration).
2. **`examples/`** — A static showcase site of 54 live interactive demos that
   dogfood every `src/` module, so an agent answering "show me a perceptual
   gradient" or "build me an OKLCh picker" (routed to `color-space-facts`, which
   points here) can hand the user a working example, not just a paragraph.
3. **`ARCHITECTURE.md` + `MATH-ROADMAP.md`** — the src/-reference co-versioning
   contract (markdown = explanation, TypeScript = implementation, same commit) and
   the prioritized list of math references still to write. Moved here from
   `references/` in the split — they document `src/`, not the corpus, and stay
   co-versioned with the code, not the packs.

There is also a lightweight **`evals/`** folder — realistic trigger and task
prompts, most of which have since been folded into the four packs' own `evals/`.

## How it was built

The collection process is simple: when I come across a color resource worth keeping — a YouTube video, a GitHub repo, a research-survey paper, an article — I paste the URL and the skill's workflow captures it:

- **Videos** get transcribed via [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), summarized, and key concepts extracted
- **PDFs and documents** get converted to markdown via [`markitdown`](https://github.com/microsoft/markitdown) by Microsoft
- **GitHub repos** get their README/docs fetched and documented
- **Articles** get their content extracted and saved
- **Books mentioned in videos** get searched on Archive.org; freely available PDFs get downloaded
- **Websites** (like huevaluechroma.com) get fully scraped chapter by chapter
- **Tools and links** mentioned in any resource get collected into the Online Tools table

That collection process built the reference corpus — now the four `color-*-facts`
packs' `references/`, not a folder here. This history is preserved for provenance;
new resources go straight into the owning pack, not into this folder.

## Structure

```text
CLAUDE.md                             # Claude Code repo instructions (no skill here)
ARCHITECTURE.md                       # src/-reference co-versioning contract (10 decisions)
MATH-ROADMAP.md                       # Prioritized list of math references, paired with src/
src/                                  # TypeScript implementation of the color math
  spaces/                             # 24 color spaces — every one exports toXYZ + fromXYZ
  gamut/                              # cusp, peak C/L, CSS Color 4 mapping
  metrics/                            # luminance, APCA, ΔE76/94/2000/ok/HyAB/CAM16
  cvd/                                # Machado 2009 colour-vision-deficiency matrices
  tonemap/                            # Reinhard simple/extended/luminance, ACES Narkowicz
  pigment/                            # Kubelka-Munk single-constant pigment mixing
  spectral/                           # CIE 1931 CMF, illuminant SPDs (D65/D50/A/F2/E), SPD→XYZ
  adaptation/                         # Bradford CAT (D50↔D65, etc.)
  interpolation/                      # linear, cubehelix, spline, lightness-curve ramps
  quantize/                           # k-means in OKLab
  dithering/                          # Floyd-Steinberg
examples/                             # Static showcase site — 54 live interactive demos
  index.html                          # Landing + categorized demo cards
  pages/*.html                        # One HTML per demo
  lib/js/components/*.js              # 28 custom-element components
  lib/dist/refcolor.bundle.js         # Classic-script IIFE bundle (~258 KB)
  build.sh                            # Optional tsc + always esbuild
  README.md                           # Quick-start for the examples site
evals/                                # Legacy eval slice; superseded by each pack's own evals/
MAINTENANCE.md                        # What belongs where, source quality bar, review rubric
CHANGELOG.md                          # Version history (full lineage, incl. pre-split)
```

The reference corpus (markdown reference files, `INDEX.md`, per-topic `SKILL.md`)
lives in the four packs, each a sibling of this folder:
`../color-space-facts/`, `../color-perception-facts/`,
`../color-contrast-facts/`, `../color-material-facts/`.

## Reviewing this folder

There's no skill-trigger review here (nothing in this folder registers a skill or
triggers on a query) — that review lives in each pack's own `evals/`. What's still
useful to check here:

1. `examples/build.sh` — confirms the TypeScript compiles and the demo bundle builds.
2. `MAINTENANCE.md` — what belongs in `src/`/`examples/` vs. a pack's `references/`.
3. `ARCHITECTURE.md` / `MATH-ROADMAP.md` — whether a new math module has both its TS
   implementation (here) and its markdown companion (in the owning pack).

## What's in it

The library: ~24 color spaces, gamut mapping, 5 ΔE variants, CVD simulation
(Machado 2009), HDR tone mapping (Reinhard/ACES), Kubelka-Munk pigment mixing,
spectral integration (CIE 1931 CMF + illuminant SPDs), Bradford chromatic
adaptation, k-means quantization, Floyd-Steinberg dithering, cubehelix/spline
interpolation — all branded-typed and round-trip test-vector-verified (see
`ARCHITECTURE.md`). The demo site: 54 live interactive pages built on top of it,
runnable directly over `file://`.

For the reference corpus content (video transcripts, article summaries, scraped
sites, standards, tool catalogs — 159 files total across the four packs), see each
pack's own `README.md`/`INDEX.md`. The opinions baked into that corpus (OKLCH over
HSL for perceptual work, APCA over WCAG 2.2 as the modern design standard, pigment
mixing ≠ RGB averaging, etc.) live in the owning pack's `SKILL.md`, not here.

## Installing the skills

This folder itself is not installed as a skill — there's nothing here for an agent
to trigger on. What gets installed (as [agent skills](https://agentskills.io)) are
the four sibling packs: `color-space-facts`, `color-perception-facts`,
`color-contrast-facts`, `color-material-facts`. Each is self-contained
(its own `SKILL.md`, `references/`, `evals/`) and can be copied, symlinked, or
installed independently; this folder is a shared dependency the `spaces` pack
points to for "show me a live demo" asks, not a skill in its own right.

## License

Original project materials in this repository — this README.md, CLAUDE.md,
ARCHITECTURE.md, MATH-ROADMAP.md, and the src/ implementation — are licensed under
CC BY 4.0. Third-party source materials and source-derived reference content
(now in the four packs) remain subject to their original authorship and licenses.
See LICENSE and THIRD_PARTY_NOTICES.md.

---

_The library and demo site were vibe-coded; the reference corpus that once lived
alongside them (now split into the four `color-*-facts` packs) came from a
collection of color resources curated over time. Original sources remain
attributed to their authors._

_Originally compiled by [@meodai](https://github.com/meodai) — one URL at a time._
