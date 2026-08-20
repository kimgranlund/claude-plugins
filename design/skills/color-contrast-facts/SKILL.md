---
name: color-contrast-facts
description: >-
  Use for color-accessibility QUESTIONS, never generates — APCA/WCAG 2.2, luminance, CVD —
  incl. an ad-hoc ratio/Lc NUMBER, not a verdict: "calculate the WCAG contrast ratio between
  these two colors", "what's the actual Lc value"; a CVD sim, no card: "simulate deuteranopia
  on this palette and tell me what changes"; or a CVD-safe pick: "give me a CVD-safe pair for
  error and success states". NOT a pass/fail VERDICT — "check the contrast ratio of this text
  on this background", "does it meet the accessibility contrast floor", "does this clear 3:1"
  are check-colors' asks; NOT a full VERIFICATION (check-colors); NOT space/gamut math
  (color-space-facts); NOT vision science (color-perception-facts).
disable-model-invocation: false
user-invocable: false
---

# color-contrast-facts — contrast standards & color-vision deficiency

Answers what makes color *usable*: the two contrast standards designers argue over, and what
color-vision deficiency (CVD) does to a palette. Extracted 2026-07-06 from the 159-file
`color-science` pack (now the non-skill `color-science-project-files` archive) alongside three
siblings — `color-space-facts` (space/gamut math), `color-perception-facts` (vision
science), `physical-color-facts` (pigment/naming). `references/INDEX.md` is the canonical
manifest and owns the file count (8 at this writing).

| Ask | Load |
|---|---|
| Contrast standards — APCA vs WCAG 2.2, contrast ratios, relative luminance, pair counts | `references/techniques/` + `references/contemporary/accessible-color-combinations-count.md` — INDEX §Contrast standards |
| CVD — simulation algorithms, canonical defaults, safe pairs, the opponent-process basis | `references/techniques/cvd-simulation-algorithms.md` + `references/contemporary/` — INDEX §CVD |
| Low-vision & readable color choices | a *lens* on the contrast-standards files, not a separate file — INDEX §Low-vision |
| WCAG 3 spec status | the one intentional cross-pack consult — INDEX §Cited-from-color-space-facts (never duplicated) |
| Provenance — where a claim comes from | `references/INDEX.md` (one row per file, with source links) |

## Consult procedure

1. Classify the ask: contrast standard (APCA/WCAG pick, ratio, luminance) · CVD (simulate, safe
   pairs, confusion) · low-vision readability. Open `references/INDEX.md`, Grep the axis section
   for the term, then Read only the matching file — the corpus is a catalog, not a linear read.
2. Answer with the **claim, its cited file, and the trap it guards against**. Worked shape:
   > *"Should our design system target WCAG AA or something stricter?"* → contrast-standard ask →
   > `references/techniques/wcag-2-2-current-legal-floor.md`: WCAG 2.2 is what regulations cite
   > (EAA, Section 508, AODA) — it is the **legal floor**, not a design-quality target, and its
   > polarity-blind ratio formula passes pairs that read poorly and rejects pairs that read fine;
   > `references/techniques/apca-lc-formula.md` is the **modern design standard** — polarity- and
   > size-aware, calibrated against real legibility research. The trap: never present either
   > standard as a drop-in replacement for the other — cite WCAG for compliance, APCA for quality,
   > and say which one the ask actually needs.
3. Check the source-tracing rule before answering: every claim traces to one of the reference
   files listed in the INDEX; an answer the corpus cannot back is general knowledge and must be
   flagged as such.
4. Route output work at the boundary (see Boundaries) — this pack answers standards and theory;
   it never emits a verdict on a candidate palette.

## Standing default (with rationale)

**APCA is the modern design standard; WCAG 2.2 is the legal compliance floor.** Use APCA for
design decisions (it is polarity-sensitive, spatial-frequency aware, and calibrated against real
legibility data); cite WCAG 2.2 where a regulation or audit specifically requires it (EAA, Section
508, AODA all cite WCAG, not APCA, as of 2026). Never present one as the other's replacement — a
WCAG-passing pair can still read poorly under APCA's polarity model, and an APCA-only palette
cannot substitute for a WCAG compliance citation.

**CVD default:** simulate deuteranopia first (the most common deficiency by a wide margin), at
Machado severity 0.6 rather than 1.0 — most real-world CVD is anomalous trichromacy, not full
dichromacy (`references/contemporary/cvd-simulation-canonical.md`). Always pair a color
distinction with a non-color cue (shape, icon, position, text); CVD-safe palettes alone are a
limited, often-ugly solution to what is really a disambiguation problem.

**WCAG 3 status:** still a Working Draft; do not cite it as settled. A "what's the current spec
status" ask routes to `color-space-facts`'s
[CSS Color 2026 Snapshot](../color-space-facts/references/techniques/css-color-2026-snapshot.md)
rather than a duplicate tracker here.

## Extending this pack

Extension: governed by [[make-pack]]

## Boundaries

- **This skill answers; it does not generate or verify.** It states what APCA/WCAG require and
  what CVD does to a palette — it never emits a pass/fail verdict.
- **Answers-vs-proves boundary with [[check-colors]]** (the seam this pack owns): theory,
  standards, and thresholds are answered here; a pass-fail verdict on an actual candidate
  palette — a ColorProof, an AA/AAA sweep across theme × scheme × contrast, CVD-safety proof on
  real hex values — is [[check-colors]]'s job. Route there, never improvise a verdict.
- **Focus-ring contrast belongs to `check-focus`** — it owns the 3:1 UI-component contrast
  invariant and hit-target sizing; this pack owns text/background contrast theory only.
- **Space-conversion and gamut math belong to `color-space-facts`** — sRGB/OKLCH/CIELAB
  conversion, gamut mapping, gradients. This pack cites its CSS Color snapshot but owns no
  conversion math itself.
- **Vision science beyond CVD belongs to `color-perception-facts`** — cone mechanics, appearance
  models, warm/cool, terminology. The opponent-process file stays here because its load-bearing
  claim is CVD-safe pairs, not the science of opponent processing.
- **Building a ramp, theme, or semantic mapping is `make-palette`'s job**, not this pack's —
  hand it the accessibility target (e.g. "APCA 60 minimum") and let it build.
- **Harmony, mood, and meaning are `color-theory-facts`'s domain**, not this pack's — a "which scheme is
  more legible" ask answers the legibility half here and routes the harmony half there.
