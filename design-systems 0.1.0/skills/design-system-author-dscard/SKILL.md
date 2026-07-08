---
name: design-system-author-dscard
description: >
  Author, evaluate, or regenerate a Claude Design / Claude Code design-system export
  bundle — DESIGN.md spine + tokens.json + @dsCard component previews — for any theme
  or brand. Use when asked to "create/author a Claude Design design-system bundle",
  "make a DESIGN.md + tokens.json for Claude", "generate @dsCard previews", "export
  our design system for Claude Code", or "fix contrast / dark scheme / on-colors in
  my Claude design bundle". Covers the universal DESIGN.md dialect (Stitch-canonical
  sections + Responsive Behavior + Agent Prompt Guide), the Ultimate Tokens grammar
  --{prefix}-{family}-{slot}, OKLCH frontmatter with hex tokens.json, the
  color-scheme + light-dark() runtime idiom, the reduction discipline, and runnable
  WCAG/parity/carrier-equality gates. NOT for Google Stitch single-file exports
  (design-system-author-google-stitch); NOT for Figma Make guidelines folders
  (design-system-author-figma-make); NOT for cross-platform strategy or picking a
  platform (design-system-author, the hub); NOT for grading an export you didn't
  author (design-system-reviewer agent).
disable-model-invocation: false
user-invocable: true
---

# Design System Author — Claude Design / Claude Code Bundle

A **Claude Design export bundle** is a consumption artifact for a generative design
agent: `DESIGN.md` (a prose spine the model reads *as its generation prompt*),
`tokens.json` (flat role→value maps), `components/*.html` (`@dsCard` cards the app
indexes), and a `README.md` receipt. Claude Design validates nothing — the gate run
here is the gate of record. One loop drives three operations: **author · evaluate ·
regenerate** (evaluate is the primitive).

Derived from: Google Stitch DESIGN.md spec, version alpha
(github.com/google-labs-code/design.md) — the universal dialect adopts its section
grammar so one core file serves both platforms; reference implementation: NONOUN
Ultimate Tokens ("Studio 54 · the dancefloor"), whose structure the bundled snippets
quote. Everything needed at runtime is embedded in `references/` and `scripts/`.

## The artifact

```
bundle/
├─ DESIGN.md          # universal-dialect spine: OKLCH frontmatter + 10 sections
├─ tokens.json        # colors/colorsDark hex maps + type/spacing/radii
├─ components/*.html  # self-contained @dsCard previews (light-dark runtime idiom)
└─ README.md          # profile receipt: gate results + measured divergences, dated
```

## Method (author)

1. **Fix the theme as one named world.** A specific reference ("Studio 54's
   dancefloor: mirror-ball silver, gold lamé, hot-pink light on black") beats any
   adjective list and imports its negative space — the Don'ts — automatically.
2. **Build the role inventory: 15–25 roles, both schemes, every value terminal.**
   Measure the on-color per fill *per scheme* — constant-white foregrounds are the
   classic silent reduction failure (dark-scheme fills land ~3.1–3.7:1, below AA).
   Signature colors the prose sells survive as roles; states ship as slot tokens,
   never prose adjectives. Full discipline R1–R5: `references/gates.md`.
3. **Name every token by the grammar** `--{prefix}-{family}-{slot}` — prefix
   host-adaptive, families open, slots a closed registry:
   `references/token-grammar.md`.
4. **Write DESIGN.md in the universal dialect** (`references/dialect.md`):
   Stitch-canonical section names 1–8 plus Responsive Behavior and Agent Prompt
   Guide; OKLCH terminal values with `-dark` siblings in frontmatter; states as
   component-variant tokens; prose sells only what the tokens deliver.
5. **Emit tokens.json and the previews.** `tokens.json` stays hex (parser-unverified
   carrier — a carrier moves to OKLCH only when acceptance is demonstrated), with
   `colors`/`colorsDark` parity. Each preview: `@dsCard` marker on line 1, one
   `:root` block with `color-scheme: light dark` + `light-dark(oklch, oklch)` custom
   properties — **without `color-scheme` on `:root` the dark end never fires**.
   Cards demonstrate states, the pairing law, and the scale; a resting-state-only
   card under-teaches the model that will imitate it. Badges/chips get ONE padding
   value below the scale's floor (e.g. `2px 8px`), used identically everywhere —
   the scale doesn't hold it as a token, but the bundle still owns it consistently.
6. **Gate.** Run `python3 scripts/bundle_gates.py <bundle-dir>`; fix the bundle (not
   the check) and re-run until exit 0. Then score the judgment dimensions against
   `references/rubric.md` — the script cannot see a vague theme or prose promising
   colors the tokens dropped.
7. **Receipt.** Write `README.md`: per-gate measured results, the naming/encoding
   standards used, every DIVERGENCE/alias/known-cost line, dated. Regenerated each
   build, never hand-synced.

## Evaluate · Regenerate

- **Evaluate**: run the gate script, then score `references/rubric.md` B1–B7 with
  cited evidence — a score with a fix, never a bare number.
- **Regenerate**: evaluate first, then rebuild from the role inventory outward —
  never patch values in place. A reduction is re-verified, not trusted: upstream
  contrast proofs do not survive dropping, collapsing, or re-pairing (R4).

## The divergence rule

When the upstream or implicit token system already made a design decision — e.g.
on-colors deliberately constant across schemes — **call out the measured divergence
in the receipt; never override an authorial decision silently.** The gate script
prints these as DIVERGENCE/INFO lines; they never fail the run (contrast still
gates), and follow-up is at the author's discretion.

## References & scripts

| Path | Use when |
|---|---|
| `scripts/bundle_gates.py <bundle-dir>` | The mechanical gates: contrast (both schemes), parity, carrier equality ±1/255, previews, references, sections, on-partner coverage, relative leading/tracking (never px, any carrier), pill/chip padding consistency (G9). `--selftest` locks the color math, gates the fixture green, and proves broken copies gate red |
| `examples/mini-bundle/` | Cold-start template: the smallest well-shaped bundle end-to-end (8 roles × 2 schemes, all four artifacts, gates green) — copy the shape, then scale to the 15–25 band |
| `references/dialect.md` | Writing or judging the spine: section table, frontmatter conventions, prose doctrine, Agent Prompt Guide shape, tokens.json schema, @dsCard rules, receipt shape |
| `references/token-grammar.md` | Naming any token: prefix adaptivity, family rules, the closed slot registry, the consumption subset, pairing law, compat aliases |
| `references/gates.md` | Encoding rules, the reduction discipline R1–R5 with measured failures F1/F2, the gate table (mechanical vs judgment), divergence handling |
| `references/rubric.md` | Scoring a bundle: B1 [gate] + B2–B7 [review] with anchors and the ship gate |

**Done** = `bundle_gates.py` exit 0 AND every rubric [review] dimension ≥ 3 AND the
receipt written from that run. **Not done** = a green script alone (fidelity is
judged, not computed), or a receipt predating the last edit to any carrier.
