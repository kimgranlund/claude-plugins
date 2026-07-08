# Encoding Rules, Reduction Discipline, and Verification Gates

What makes a bundle *conforming* — and the measured failures each rule prevents.
Source: derived from the design-system-files-for-llms spec §6–§8 (2026-07-05), its
BUNDLE-REVIEW case study, and an encoding probe of Stitch's linter (2026-07-05:
`oklch()` accepted and contrast-checked; `light-dark()` composites rejected as
errors). Companions: `dialect.md`, `token-grammar.md`; enforcement:
`../scripts/bundle_gates.py`. The snapshot embedded in this bundle is authoritative
at runtime; re-derive from the upstream spec on a version bump, never from memory.

**Constant ownership** (edit here first, then the derived copies): this file owns the
encoding constants — the AA 4.5:1 bar, the ±1/255 equality tolerance, the
`color-scheme` trap. `token-grammar.md` owns the role budget (15–25). SKILL.md and
`dialect.md` restate headlines for progressive disclosure; they are derived copies.

## Encoding rules

- **Terminal values only.** Every value is final — gamut-mapped, scheme-resolved,
  contrast-verified. The consumer never lightens, darkens, mixes, or derives;
  derivation happened upstream where the color math lives.
- **OKLCH is the payload wherever the parser provably accepts it** — the DESIGN.md
  frontmatter (probe-verified) and all CSS carriers. An OKLCH value here is still
  terminal; it buys self-documenting lightness/chroma and passes through to runtime
  unconverted.
- **Hex is the payload for parser-unverified carriers** — `tokens.json` (its consuming
  app documents no schema). A carrier moves to OKLCH only when acceptance is
  *demonstrated*, never assumed.
- **Carriers hold scheme pairs as data; runtime composes them.** `light-dark()` is
  NOT a carrier value (measured: Stitch rejects it; a two-ended value has no single
  sRGB conversion for lint-time contrast). The emitted runtime idiom is
  `color-scheme: light dark` + `light-dark(<light>, <dark>)` on `:root` custom
  properties — and **without `color-scheme` on `:root` the second argument never
  fires**; ship both lines together, always.
- **Alpha rides in the value** (`oklch(0.6 0.03 288 / 30%)`, `#807F904D`), never as a
  separate opacity token.
- **Notation is not identity.** Values in different notations are equal when they
  resolve to the same sRGB 8-bit triple within ±1/255 per channel (measured:
  4-decimal OKLCH rounding costs at most 1/255 on round-trip).

## The reduction discipline (R1–R5)

A bundle is produced by *reducing* a rich authoring model to the role budget
(owned by `token-grammar.md`); the reduction is where fidelity is won or lost:

| # | Rule | Measured failure it prevents |
|---|---|---|
| R1 | Every on-color is **selected by measurement, per fill, per scheme** | **F1**: all foregrounds collapsed to constant `#FFFFFF`; every dark-scheme fill landed 3.1–3.7:1 — below AA. The classic silent reduction bug |
| R2 | **Signature colors survive the cut** — roles are allocated to what the prose sells, not only the primary/secondary/accent triad | **F2**: the story promised hot pink, cyan, silver; the reduction dropped all three families while the spine forbade hardcoding — generated screens had nothing to bind |
| R3 | **States ship as values** (variant tokens), not prose adjectives | "hover brightens slightly" yields per-generation drift: every screen invents its own "slightly" |
| R4 | **The reduction is re-verified, never trusted** — upstream proofs do not survive dropping, collapsing, re-pairing | F1 again: the upstream model was contrast-correct; the reduction broke it *after* the last check that would have caught it |
| R5 | **Prose and tokens reduce together** — cut a family, cut its prose in the same change | the F2 story/token mismatch: a spine describing a palette the tokens can't deliver |

## The verification gates

Claude Design publishes no linter — **the author's gate run is the gate of record.**
Run: `python3 scripts/bundle_gates.py <bundle-dir>` (stdlib-only; exit 0 iff no FAIL;
`--selftest` locks the color math). What is mechanical vs judgment:

| Gate | Check | Enforced by |
|---|---|---|
| G1 Contrast | every derivable fill/on pair ≥ 4.5:1, BOTH schemes — normal-text bar on all pairs, the 3:1 large-text concession unused; pairs derived from the grammar's pairing law; `-disabled` and alpha<1 tokens excluded (reported SKIP) | script |
| G2 Scheme parity | identical role inventory: frontmatter light↔`-dark`, tokens.json `colors`↔`colorsDark` | script |
| G3 Carrier equality | frontmatter OKLCH ≡ tokens.json hex, notation-aware ±1/255 incl. alpha; inventories match | script |
| G4 Preview self-containment | `@dsCard` first line with group/title; no external fetches (`src=`/`href=`//`url(http`/`@import`); `color-scheme` present wherever `light-dark()` is used | script |
| G5 Reference resolution | every `{group.token}` in DESIGN.md resolves | script |
| G6 Section grammar | canonical names (aliases accepted), canonical order, no duplicates; Responsive Behavior + Agent Prompt Guide present | script |
| G7 Required roles | every family base fill has an on-partner (value-equal aliases pass as INFO); missing literal `primary` → WARN (ship the compat alias) | script |
| G8 Relative leading/tracking | leading/tracking are always relative — unitless factor, em, or % (standing rule); never px in any carrier: frontmatter `lineHeight`/`letterSpacing`, tokens.json `type.scale` (a string ending px, or a lineHeight number > 4 — a px length, not a factor), preview inline styles | script |
| G9 Pill/chip padding consistency | every `border-radius:9999px` element's padding, across every preview, is the same value | script |
| Orphans | color roles never referenced in prose/components/previews → WARN (never gates) | script |
| Prose–token accord (prose→token) | every color/face/effect the prose *names* exists as a token — a semantic read the script cannot do | judgment (`rubric.md` B3) |
| Theme specificity | one named world, not adjectives | judgment (`rubric.md` B2) |

Fix → re-run until exit 0; a FAIL is fixed in the *bundle*, never by loosening the
check. Judgment dimensions are scored against `rubric.md` after the script is green.

## Sanctioned exceptions — deliberate, named, never a blanket loosening

Distinct from a DIVERGENCE (an upstream system's already-made decision, called out
as-is): a **sanctioned exception** is a rule the *author* deliberately relaxes
because a schema constraint makes the stated rule structurally impossible to meet
in full — earned by evidence, scoped narrowly, and never used to excuse ordinary
carelessness.

**Known instance: badge/chip padding.** The spacing scale's floor is 4px; compact
pill-shaped badges/chips commonly need a compound value below it (e.g. `2px 8px`
for ~12–13px label text). This can never be expressed as a frontmatter `padding:`
token — Stitch's Dimension type holds one value, and a pill's padding is inherently
asymmetric (vertical ≠ horizontal). So the exception lives only in prose
(`dialect.md`) and in the previews' literal CSS.

**Evidence it's real, not an excuse:** two independent Claude Design generations
run against the same bundle, same prompt. Run 1 improvised **5 different** off-scale
values across every chip (`2,3,5,6,7,10,14,20`px, ~26 instances) — genuine drift.
Run 2 **converged to one dominant value** (`2px 8px`, ~10 instances) unprompted.
The convergence between independent runs — not the mere absence of the scale's
4px/8px/12px — is what makes this a real, structural gap rather than noise to
suppress.

**What "sanctioned" does NOT mean:** it does not loosen G1–G8, and it is not a
license to freehand a *different* off-scale value per element. G9 enforces the
one thing that actually matters: whatever value is chosen, it's chosen **once**
and used everywhere. Inconsistency — not off-scale-ness — is the violation.

**Criteria for blessing a new exception** (apply before adding one): (1) reproduces
across ≥2 independent generations or builds; (2) has a structural reason the
token schema can't express it as a single value; (3) is named explicitly in
DESIGN.md prose and demonstrated in a preview (`examples/mini-bundle/` shows the
badge/chip case); (4) gains a narrow, specific mechanical check — never a broad
loosening of an existing gate.

## Divergences — call out, never silently override

When the upstream or implicit token system has already made a design decision — e.g.
an on-color deliberately constant across schemes (mirror-silver keeping a near-black
label in both), or a compat alias — the gate run reports it as a `DIVERGENCE`/`INFO`
line and the receipt records it verbatim. **Never "fix" an authorial decision
silently**; contrast still gates it (a constant on-color that fails AA is F1, not a
divergence), but a passing divergence is the author's call to keep or revisit.
