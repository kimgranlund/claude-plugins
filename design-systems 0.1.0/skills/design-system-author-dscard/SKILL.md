---
name: design-system-author-dscard
description: >
  Author, evaluate, or regenerate a Claude Design / Claude Code design-system export
  bundle — DESIGN.md + tokens.json + @dsCard previews — from a corpus (css, tokens,
  code, brand decks) or a brief. Use when asked to "create a Claude Design
  design-system bundle", "based on these css files create a design system for use in
  claude design and claude code", "make a DESIGN.md + tokens.json for Claude",
  "generate @dsCard previews", "export our design system for Claude Code", or "fix
  the dark scheme / on-colors in my Claude design bundle". Covers corpus census, Root
  Brand Architecture, the universal dialect and token grammar, OKLCH frontmatter,
  light-dark(), the reduction discipline, and gates with count-exact contrast
  disclosure. NOT for format Q&A alone (design-md-format); NOT for
  Stitch exports (design-system-author-google-stitch); NOT for Make guidelines
  (design-system-author-figma-make); NOT for cross-platform strategy
  (design-system-hub); NOT for grading an export you didn't author
  (design-system-reviewer).
disable-model-invocation: false
user-invocable: true
---

# Design System Author — Claude Design / Claude Code Bundle

A **Claude Design export bundle** is a consumption artifact for a generative design
agent: `DESIGN.md` (a prose spine the model reads *as its generation prompt* — a
SKILL for a brand, per `design-md-format`, this plugin's format ground truth),
`tokens.json` (flat role→value maps), `components/*.html` (`@dsCard` cards the app
indexes), and a `README.md` receipt. Claude Design validates nothing — the gate run
here is the gate of record. One loop drives three operations: **author · evaluate ·
regenerate** (evaluate is the primitive).

Derived from: Google Stitch DESIGN.md spec, version alpha
(github.com/google-labs-code/design.md) — the universal dialect adopts its section
grammar so one core file serves both platforms; reference implementation: NONOUN
Ultimate Tokens ("Studio 54 · the dancefloor"), whose structure the bundled snippets
quote. Everything needed at runtime is embedded in `references/` and `scripts/`;
first-party format anatomy, the six-slot brand architecture, and card syntax live in
`design-md-format`'s corpus (same plugin) — consult it rather than restating it.

Two standing fences, checked at every step: **framework-neutral** (zero framework
names as prescriptions — plain HTML/CSS only in examples) and **disclose, never
enforce** (ship the brand's values verbatim; measure contrast per fill/on-pair per
scheme; misses the brand accepts are disclosed count-exact in the receipt — an
undisclosed miss fails the gate, a disclosed one ships).

## The artifact

```
bundle/
├─ DESIGN.md          # universal-dialect spine: OKLCH frontmatter + 10 sections
│                     #   teaches the SYSTEM: grammar + the 15–25 consumption roles;
│                     #   the exhaustive token layer stays in the companion carrier —
│                     #   a full ramp dump in DESIGN.md is token bloat starving the prompt
├─ tokens.json        # colors/colorsDark hex maps + type/spacing/radii (the machine carrier)
├─ components/*.html  # self-contained @dsCard previews (light-dark runtime idiom)
└─ README.md          # profile receipt: gate results + measured divergences + disclosures, dated
```

## Method (author)

1. **Census the corpus and classify the run.** Inventory every input — token files,
   CSS, codebases, Figma exports, screenshots, brand decks, prose. **Extraction**
   (tokens/code exist): values lift verbatim — 5px stays 5px, never snapped to a
   4/8 grid; note each source against what it supplies. **Synthesis** (partial):
   mark which layers are evidence-backed and which are proposed. **Invention**
   (brief only): everything is a proposal until the user confirms. A
   mentioned-but-unreadable source (a repo you can't read, a dead link) stops the
   run — report and ask; never infer content you couldn't read.
2. **Capture the Root Brand Architecture** — the six slots from `design-md-format`'s
   brand-architecture reference: values, voice, visual territories, cultural
   references, refusals, signature details. Tokens make output *consistent*; this
   layer makes it *recognizable* — do not start token work until every slot holds
   committed lines that carry a design consequence ("restraint over decoration: one
   decisive action per view" passes; "clean and modern" fails). Extraction runs
   quote evidence (collect 5–10 verbatim product strings before the Voice slot);
   invention runs present each slot as a proposal and confirm in one round. A named
   world ("Studio 54's dancefloor: mirror-ball silver, gold lamé, hot-pink light on
   black") beats any adjective list and imports its negative space — the Don'ts —
   automatically. When the signature-details slot resists filling, ask: *"what would
   make you recognize a screen as yours with the logo removed?"*
3. **Build the role inventory: 15–25 roles, both schemes, every value terminal.**
   Measure the on-color per fill *per scheme* — constant-white foregrounds are the
   classic silent reduction failure (dark-scheme fills land ~3.1–3.7:1, below AA).
   Signature colors the prose sells survive as roles; states ship as slot tokens,
   never prose adjectives. Full discipline R1–R5: `references/gates.md`.
4. **Name every token by the grammar** `--{prefix}-{family}-{slot}` — prefix
   host-adaptive, families open, slots a closed registry:
   `references/token-grammar.md`.
5. **Write DESIGN.md in the universal dialect** (`references/dialect.md`):
   Stitch-canonical section names 1–8 plus Responsive Behavior and Agent Prompt
   Guide; OKLCH terminal values with `-dark` siblings in frontmatter; states as
   component-variant tokens; prose sells only what the tokens deliver. Weave the
   step-2 architecture in (values in Overview, voice as its own section, refusals in
   Do's and Don'ts, cultural references where they anchor) — the file opens
   addressing the consuming agent, and any open-ended section passes the anatomy
   test: a fresh agent would generate differently with it, or it's cut.
6. **Emit tokens.json and the previews.** `tokens.json` stays hex (parser-unverified
   carrier — a carrier moves to OKLCH only when acceptance is demonstrated), with
   `colors`/`colorsDark` parity. Each preview: `@dsCard` marker on line 1, one
   `:root` block with `color-scheme: light dark` + `light-dark(oklch, oklch)` custom
   properties — **without `color-scheme` on `:root` the dark end never fires**.
   Cards demonstrate states, the pairing law, and the scale; a resting-state-only
   card under-teaches the model that will imitate it. Badges/chips get ONE padding
   value below the scale's floor (e.g. `2px 8px`), used identically everywhere —
   the scale doesn't hold it as a token, but the bundle still owns it consistently.
7. **Gate.** Run `python3 scripts/bundle_gates.py <bundle-dir>`; fix the bundle (not
   the check) and re-run until exit 0. Then score the judgment dimensions against
   `references/rubric.md` — the script cannot see a vague theme or prose promising
   colors the tokens dropped. Close with the **round-trip check**: hand the
   DESIGN.md alone to a fresh context with "generate a settings screen for this
   brand" — the output must be *recognizable*, not merely compliant (compliance
   comes from tokens; recognition comes from the architecture). A miss names its
   failed layer — architecture vs tokens vs prose — and the fix lands in that step.
8. **Receipt.** Write `README.md`: per-gate measured results, the naming/encoding
   standards used, every DIVERGENCE/alias/known-cost line, and the count-exact
   contrast-disclosure line for any accepted sub-4.5:1 pairs, dated. Regenerated
   each build, never hand-synced.

## Evaluate · Regenerate

- **Evaluate**: run the gate script, then score `references/rubric.md` B1–B7 with
  cited evidence — a score with a fix, never a bare number.
- **Regenerate**: evaluate first, then rebuild from the role inventory outward —
  never patch values in place, and never over the shipped bundle: the hub's
  destructive-op ladder (shared-doctrines §7) governs — staged build, diff against
  the shipped export with hand-edits named individually, apply on approval where
  hand-edits exist. A reduction is re-verified, not trusted: upstream contrast
  proofs do not survive dropping, collapsing, or re-pairing (R4).

## The divergence rule

When the upstream or implicit token system already made a design decision — e.g.
on-colors deliberately constant across schemes — **call out the measured divergence
in the receipt; never override an authorial decision silently.** The gate script
prints these as DIVERGENCE/INFO lines and they never fail the run. Contrast follows
the same posture: a sub-4.5:1 pair the brand accepts ships **DISCLOSED** when the
receipt carries the count-exact disclosure (count drift IS a FAIL); a miss with no
disclosure fails. The gate enforces the honesty of the disclosure, not the brand's
values — follow-up is at the author's discretion.

## References & scripts

| Path | Use when |
|---|---|
| `scripts/bundle_gates.py <bundle-dir>` | The mechanical gates: contrast (both schemes), parity, carrier equality ±1/255, previews, references, sections, on-partner coverage, relative leading/tracking (never px, any carrier), pill/chip padding consistency (G9). `--selftest` locks the color math, gates the fixture green, and proves broken copies gate red |
| `references/mini-bundle/` | Cold-start template: the smallest well-shaped bundle end-to-end (8 roles × 2 schemes, all four artifacts, gates green) — copy the shape, then scale to the 15–25 band |
| `references/dialect.md` | Writing or judging the spine: section table, frontmatter conventions, prose doctrine, Agent Prompt Guide shape, tokens.json schema, @dsCard rules, receipt shape |
| `references/token-grammar.md` | Naming any token: prefix adaptivity, family rules, the closed slot registry, the consumption subset, pairing law, compat aliases |
| `references/gates.md` | Encoding rules, the reduction discipline R1–R5 with measured failures F1/F2, the gate table (mechanical vs judgment), divergence handling |
| `references/rubric.md` | Scoring a bundle: B1 [gate] + B2–B7 [review] with anchors and the ship gate |
| `design-md-format` (same plugin) | First-party format ground truth: DESIGN.md anatomy + openness doctrine, the six-slot Root Brand Architecture, @dsCard tag syntax — steps 1–2 and 5 lean on its corpus |

**Done** = `bundle_gates.py` exit 0 AND every rubric [review] dimension ≥ 3 AND the
round-trip output recognizable AND the receipt written from that run. **Not done** =
a green script alone (fidelity is judged, not computed), a receipt predating the last
edit to any carrier, or architecture slots skipped because the corpus "already had
tokens" — consistency without recognizability is the failure this skill exists to
prevent.
