---
name: color-verify
description: Verify a candidate OKLCH palette or semantic color mapping against contrast, hue stability, perceptual evenness, and CVD-safety, emitting a ColorProof. Use when asked "verify this palette", "does this palette pass", or to check contrast ratios, WCAG AA/AAA or APCA pass-fail, color-blind (CVD) safety, or alpha/translucent colors composited over a backdrop — every fg/bg pair across theme/scheme/contrast. NOT for building a ramp or dark scheme (palette-design); NOT for which contrast standard or CVD theory (color-science-accessibility); NOT for focus order, keyboard nav, or focus-ring contrast (focus-verify); NOT for RTL/bidi, locale Intl formatting, or text-expansion (i18n-verify); NOT for loading skeleton/spinner, CLS, or latency budgets (perf-verify); NOT for destructive-action undo/type-to-confirm or audit-trail UX (safety-verify); NOT for color-space math or converting between color spaces (color-science-spaces); NOT for harmony/meaning (color-theory); NOT for a color-picker component (component-author).
disable-model-invocation: false
user-invocable: true
---

# color-verify — palette & mapping invariants, card-gated

Pure verifier: it takes a candidate palette or semantic mapping and proves it behaves — it does
not design one. The verify contract: **declare the surface in a card → the checker gates the
arithmetic → judgment covers only what code cannot see** (CVD safety, perceptual evenness, the
full (theme × scheme × contrast) sweep). Output is a **ColorProof** — verdict + verified pairs +
violations, each violation citing what it evaluates with a scoped remediation. Building or
extending a ramp, assigning roles, deriving a dark scheme is generation and exits to
[[palette-design]]; its emits loop back here for proof before finalize.

## The card

A **color surface card** declares the foreground/background pairs that carry text or UI
indication. Name it to match the dir-glob patterns the checker walks — `*.surface.json` or
`*.contrast.json` (e.g. `default-light.surface.json`; a single file passed explicitly may have
any name):

```json
{ "meta": {"theme": "default", "scheme": "light", "contrast": "normal"},
  "pairs": [
  {"name": "body text",   "fg": "light-dark(#1a1a1a, #eeeeee)", "bg": "light-dark(#ffffff, #111111)",
   "fgToken": "--on-surface", "bgToken": "--surface"},
  {"name": "accent link", "fg": "oklch(0.558 0.135 255)", "bg": "#ffffff", "fgToken": "--accent-600"},
  {"name": "outline",     "fg": "#00000059", "bg": "#ffffff", "over": "#ffffff", "role": "ui"}
]}
```

Card `meta` (optional): `{theme, scheme: "light"|"dark", contrast}` — `scheme` picks the
`light-dark()` leg; all three pass through to the JSON report as provenance.

Per pair (only `fg` + `bg` required): `name` (report label) · `fg`/`bg` — `#rgb`, `#rrggbb`,
`#rrggbbaa`, `rgb()/rgba()`, `oklch(L C H [/ A])` (L as 0–1 or %, H in degrees; standard
OKLab→linear-sRGB matrices; an out-of-sRGB-gamut value clamps with an advisory warn), or
`light-dark(X, Y)` (resolved by `meta.scheme`; on a card with **no** scheme it is a per-pair
ERROR — never a silent first-leg pick) · `size` (`normal` default | `large`) · `role` (`text`
default | `ui`/non-text) · `over` — the backdrop an alpha fg is composited over (source-over in
gamma-encoded sRGB, as browsers composite CSS colors) before the ratio vs `bg`; an fg with
alpha < 1 and **no** `over` is a per-pair ERROR (silent-opaque substitution inverts to false-PASS
on exactly the riskiest pairs), and `bg`/`over` must be opaque · `fgToken`/`bgToken` — free-text
token provenance, passed through to the JSON report. A malformed color is a clear per-pair
error, never a crash.
`verification/contrast-pairs.json` is the authoritative list of semantic pairs a card must cover
(a repo may ship a role→pair manifest mapping those roles onto its concrete token names).

## Procedure

1. **Assemble the card** from the candidate palette + the semantic pairs in
   `verification/contrast-pairs.json` — one card per (theme × scheme × contrast) combination the
   system claims. A pair the palette cannot express is already a violation.
2. **Gate:** `python3 scripts/contrast-check.py <card.json | dir>` — a FAIL blocks the emit; fix
   the palette, not the card. `selftest` proves the checker itself.
3. **Judge what the checker can't:** sweep every (theme × scheme × contrast) combination — the
   palette passes only if every one passes; run the CVD safety check (simulate protanopia /
   deuteranopia — Brettel/Machado models via [[color-science-accessibility]] — and confirm intent colors stay
   distinguishable, no meaning carried by hue alone); apply the invariant table below to ramp
   geometry (evenness, hue drift, neutral chroma, C-only gamut provenance).
4. **Emit the ColorProof** — `{verdict, combinations, pairs: [{name, fg, bg, ratio, target,
   pass, fgToken?, bgToken?}], violations}` — the pairs table comes straight from the checker's
   `--json` output (every pair, pass AND fail); each violation cites the schema path or CSS rule
   it evaluates, with remediation scoped to the artifact that can fix it (a failing ramp routes
   to [[palette-design]] as a `DecompositionGap`, never patched here).

## Invariants (the numbers)

| Invariant | Value | Source |
|---|---|---|
| Text contrast (AA) | ≥ 4.5:1 normal · ≥ 3.0:1 large | `verification/contrast-pairs.json` — the authoritative pairs + targets |
| UI / non-text contrast | ≥ 3.0:1 (borders, focus rings, icons) | WCAG 1.4.11; same file |
| AAA tier (advisory) | ≥ 7.0:1 normal · ≥ 4.5:1 large — text only | same file |
| Neutral chroma | C ≤ 0.02 for declared `neutral: true-grey` · C ≤ 0.06 for declared `neutral: tinted` (slate) — the declaration is REQUIRED, never inferred | ramp invariant |
| Perceptual evenness | adjacent ΔL normalized per label-unit distance (ΔL ÷ Δlabel): gap-to-gap ratio ≤ 1.5 per unit — so 25/50-spaced stops are legal | ramp invariant |
| Hue stability | drift ≤ ±8°, only toward the next-neighbor hue — gated at C ≥ 0.02 (hue is meaningless achromatic) | ramp invariant |
| Gamut provenance | **C-only reduction** — a gamut-mapped step must show reduced C, never shifted L or H; ΔC > 0.05 means the anchor itself was out of gamut | the named gamut check |
| L monotonic | L strictly monotonic in the ramp's **declared** direction — lightness- and darkness-indexed ladders are both legal | ramp invariant |

The ramp-geometry rows ("ramp invariant", the named gamut check) restate a canon owned by
[[palette-design]] — its `ramps/` data and `ramp_build.py` gates; this table is the gate's view,
not a second canon.

Escalation for a failing pair (canon: `contrast-pairs.json`): the `DecompositionGap` carries the
prescription — step the FG one ramp step, then the BG, else redesign — and [[palette-design]]
executes it; a failing pair is never silently shipped.

## Detection catalog (what a review hunts)

A pair emitted without a contrast number · the near-miss (`#777` on white ≈ 4.48 — under the 4.5
floor an eyeball passes) · verified in the light scheme only · an alpha fg verified opaque
(compositing over the real backdrop inverts to FAIL on exactly the riskiest pairs) · an intent
color bound as text ink but verified at the 3.0 ui floor · intent colors sharing one hue
region (danger/success collapse under CVD) · meaning carried by hue alone · gamut overflow solved
by darkening (an L shift) instead of C-only reduction · a "verified" palette whose card omits
pairs from `verification/contrast-pairs.json` · hardcoded hex with no OKLCH provenance.

## Mechanism gate — `scripts/contrast-check.py`

WCAG contrast is **arithmetic**, not taste — the floor always routes to code. CVD safety and
perceptual evenness are perceptual judgments and stay a review (step 3). The checker sees PAIRS,
not ramps — the ramp-geometry gates run mechanically in [[palette-design]]'s `ramp_build.py` and
are re-judged here in step 3 against the invariant table. And it verifies only the pairs the card
shows: coverage against `verification/contrast-pairs.json` is never checked mechanically — an
omitted canonical pair is skipped-not-passed (step 1 assembles it; the detection catalog hunts
the omission). The checker (stdlib-only, selftest-locked) computes the WCAG 2.x ratio per pair
(sRGB → linearized relative luminance → `(L1+0.05)/(L2+0.05)`):

| Check | Severity | Fires when |
|---|---|---|
| `CONTRAST_FAIL_AA` | gate — exit 1 | any pair below its AA floor (4.5 text · 3.0 large/ui) |
| `CONTRAST_FAIL_AAA` | advisory WARN — exit 0 | a text pair clears AA but misses its AAA tier (graphics have no AAA tier) |
| `OKLCH_OUT_OF_GAMUT` | advisory WARN — exit 0 | an `oklch()` value outside sRGB gamut — clamped for the ratio; the upstream fix is C-only reduction |
| per-pair errors | gate — exit 1 | malformed color · bad `role`/`size` · `light-dark()` with no `meta.scheme` · alpha fg with no `over` · translucent `bg`/`over` — reported, never a crash |

`--json` emits the **full per-pair table** — every pair `{name, fg, bg, ratio, target, pass,
fgToken?, bgToken?, meta?, error?}`, passes included (the ColorProof requires it).
`python3 scripts/contrast-check.py selftest` exits 0, locked by good + bad fixtures (the `#777`
≈ 4.48 near-miss, a 3:1-as-normal-text fail, `#767676` ≈ 4.54 AA-pass, 3:1 passing as
`large`/`ui`, the oklch known values — sRGB-red roundtrip, the documented
`oklch(0.558 0.135 255)` ≈ 4.70-vs-white token, an out-of-gamut clamp — `light-dark()` leg
selection per scheme, the composited-outline inversion (α ≈ 0.35 black: 21:1 opaque,
≈ 2.43 composited), malformed colors, ratio symmetry, 21:1 black-on-white). The gate is
**necessary, not sufficient** — a clean run proves the arithmetic floor holds; step 3 proves the
palette safe.

## Material & routing

| Path / peer | Use |
|---|---|
| `verification/contrast-pairs.json` | authoritative semantic pairs, AA/AAA targets, the escalation rule |
| `scripts/contrast-check.py` | the contrast gate + selftest |
| [[palette-design]] | builds/extends ramps and mappings; every failing ramp routes back to it |
| [[color-science-accessibility]] | the perceptual theory under these constraints (APCA/WCAG math, CVD models) |
| [[color-science-spaces]] | gamut math under these constraints (peak chroma, C-only reduction) |
| [[focus-verify]] | **owns focus-ring contrast** — the `--focus-ring` pairs were removed from `contrast-pairs.json`; route every focus-ring pair there |
| `token-builder` agent | realizes verified palettes as token layers in a repo |
| [[ui-audit]] | the set-scoped sweep that composes this verifier |

**Done** = the contrast gate passes on every card + the full (theme × scheme × contrast) sweep
passes + CVD safety judged; **NOT done** = a green contrast-check alone, or a card omitting pairs
from `verification/contrast-pairs.json`.
