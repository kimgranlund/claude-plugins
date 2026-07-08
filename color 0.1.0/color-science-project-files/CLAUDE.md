# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project Overview

**This folder registers no skill.** It is the color-math TypeScript library and
interactive demo site behind the `color-science-*` family of agent skills
(compatible with Claude Code, Codex, Cursor, Copilot, OpenCode, and others via
[agentskills.io](https://agentskills.io)). Until the 2026-07-06 extraction this
folder was `color-science` — a combined skill + reference corpus + library. The
reference corpus (159 files) split out into four independently-routed sibling
packs: `color-science-spaces`, `color-science-perception`,
`color-science-accessibility`, `color-science-materials` (each with its own
`SKILL.md`, `references/`, `evals/`). Aesthetics/meaning/history — harmony, the
color wheel, palette mood — live in the separate `color-theory` pack (split
2026-07-02, predates this extraction).

## Architecture

- `ARCHITECTURE.md` — The 10 architectural decisions for `src/` and its paired
  math references (source-of-truth hub, branded types, bidirectionality contract,
  where prose and code meet). The math references it describes now live in the
  four packs; this repo still owns and co-versions the TypeScript.
- `MATH-ROADMAP.md` — Prioritized roadmap of math-reference files, paired with
  `src/` modules; status columns point at the owning pack's file.
- `src/` — Working TypeScript implementation: 24 color spaces (every one exports
  `toXYZ` + `fromXYZ`), gamut math, ΔE metrics, CVD simulation (Machado 2009), tone
  mapping (Reinhard / ACES), Kubelka-Munk pigment mixing, spectral integration
  (CIE 1931 CMF + illuminant SPDs), Bradford CAT, k-means quantization,
  Floyd-Steinberg dithering, cubehelix / spline interpolation.
- `examples/` — Static showcase site dogfooding `src/`. 54 live demos as classic
  HTML pages; 28 custom-element components; single IIFE bundle
  (`examples/lib/dist/refcolor.bundle.js`) so everything works directly over
  `file://`. The `color-science-spaces` pack's SKILL.md points here for
  "show me a live demo / where's the implementation" asks.

## Build

`src/` and `examples/` are the only things here that build:

```bash
cd examples
./build.sh   # tsc (optional, if local) + esbuild → lib/dist/refcolor.bundle.js
```

`build.sh` falls back gracefully if no local `tsc` is present; it always runs `esbuild` to produce the IIFE bundle. CI is not required — the bundle is committed.

## Editing Guidelines

- This folder has no SKILL.md and cannot misroute — don't add one here (D2: the
  goal was project *files* vs "proper set of skills"; if that reading changes, a
  new SKILL.md scoped to demo/implementation asks would need those triggers
  removed from `color-science-spaces`'s description first, not duplicated).
- Every math module in `src/` is co-versioned with a markdown reference file in
  one of the four packs (`ARCHITECTURE.md` Decision 8): when the TS changes, the
  paired pack's markdown is updated in the same commit; when the math description
  is refined, the TS code blocks are re-quoted from the canonical source.
- Deep reference content (video transcripts, standards, tool catalogs) goes in the
  owning pack's `references/`, never here — this folder holds only working code
  and its demo site.
- No PDFs live on disk here; `.gitignore`'s `*.pdf` rule is vestigial but harmless.
  Archive.org source links are preserved in the reference files themselves (in the
  packs).
