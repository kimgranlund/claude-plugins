# Sources and provenance

This pack distills two live source trees (agent-ui's shared token/dimension/theme CSS + a
structural CSS test file; gen-ui-kit's own cascade-layer, token-tier, and scoping ADRs) read
directly on 2026-08-20 (this pack's authoring date, ticket #810, frontend wave 6, the final wave
of the series) — a live re-read of the specific files below, not a distillation of a prior dated
field-report corpus the way several sibling waves were. Both repos ship production CSS
architecture; neither is a strawman for the other where the two disagree (`cascade-and-load-order.md`
is explicit about this).

## The grounding files

| Axis | Repo | File(s) consulted |
|---|---|---|
| `cascade-and-load-order.md` | `adia/gen-ui-kit` + `nonoun/agent-ui` | gen-ui-kit `docs/ops/adr/adr-0038-cascade-layer-precedence.md` (the `@layer` decision, including its own §Context citation of gen-ui-kit's ADR-0037 as the symptom that motivated ADR-0038 — ADR-0037 itself was not independently re-read as a primary source, only ADR-0038's account of it); gen-ui-kit `docs/ops/adr/adr-0003-two-block-scope-css-contract.md` (Alternative D, `@layer`/`@scope` composability); agent-ui `.claude/docs/adr/0003-single-file-component-css-barrels-host-page.md` (agent-ui's own, differently-numbered ADR-0003 — the barrel/load-order decision); agent-ui `packages/agent-ui/components/src/foundation-styles.css` (the load-bearing `@import` order) |
| `token-taxonomy-and-themes.md` | `adia/gen-ui-kit` + `nonoun/agent-ui` | gen-ui-kit `docs/ops/adr/adr-0002-three-tier-token-layering.md` (the three-tier decision + rejected two/four-tier alternatives); agent-ui `packages/agent-ui/shared/src/tokens/tokens.css` (the default `:root` tier); agent-ui `packages/agent-ui/shared/src/tokens/themes/orchid.css` (a generated theme pack, its own header comment naming the parity gap + no-fallback-needed rationale) |
| `light-dark-theming.md` | `nonoun/agent-ui` + `adia/gen-ui-kit` | agent-ui `tokens.css` (`color-scheme: light dark;` + the full `light-dark()` semantic-role block); gen-ui-kit `adr-0002` ("Wrapped in `light-dark()` where applicable") |
| `frame-vs-rhythm-geometry.md` | `nonoun/agent-ui` | `packages/agent-ui/shared/src/tokens/dimensions.css` in full (500 lines) — the FRAME/RHYTHM split comment, the rejected-multiplier history citing agent-ui's OWN ADR-0007/ADR-0032/ADR-0038 (`.claude/docs/adr/0007-universal-selector-ramp-tokens.md`, `0032-ui-content-scale-tier-system.md`, `0038-control-sizing-size-scale-row-lookup.md` — confirmed present on disk, distinct documents from gen-ui-kit's identically-numbered ADR-0038), the per-`[scale]`-tier literal table, the `*`-vs-`:root` pre-substitution comment |
| `scoping-strategies.md` | `adia/gen-ui-kit` | `docs/ops/adr/adr-0003-two-block-scope-css-contract.md` (the `@scope` two-block contract, Alternative B's rejection of BEM-style manual discipline) — CSS Modules itself is general, widely-documented bundler behavior, not independently re-verified against a grounding-repo source (neither repo uses it); stated as the comparison point ADR-0003's BEM rejection generalizes to |
| `css-as-decision-log-and-contract.md` | `nonoun/agent-ui` + `adia/gen-ui-kit` | agent-ui `dimensions.css` (the ADR-citing decision-log comment style); agent-ui `packages/agent-ui/components/src/controls/disclosure/disclosure-css.test.ts` (the full structural CSS unit-test suite); gen-ui-kit `adr-0038` (the ADR-to-gate-command citation) |

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary CSS/ADR file cited above, read on
  2026-08-20 (this pack's authoring date). Every substantive claim in this pack's six axis files
  carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated design failure or rejected approach the
  source material itself documents as having actually been tried and abandoned (ADR-0037's forced
  per-component `[inline]` override that `@layer` later resolved; agent-ui's own rejected
  multiplier-ladder history in `dimensions.css`, superseded by its own ADR-0038's explicit lookup
  table). Distinguished from [verified] because the evidentiary weight is "this was tried and
  didn't hold up," not just "this is what the code currently does."

## A same-number, different-repo trap this pack deliberately surfaces rather than silently resolves

Both agent-ui and gen-ui-kit number their own ADRs independently, and **both happen to have their
own ADR-0003 and their own ADR-0038 — about entirely different decisions.** gen-ui-kit's ADR-0003
is the `@scope` two-block contract; agent-ui's ADR-0003 is the CSS-barrel/load-order decision.
gen-ui-kit's ADR-0038 is the cascade-layer decision; agent-ui's ADR-0038 is the control-sizing
row-lookup table (the rejected-multiplier fix in `frame-vs-rhythm-geometry.md`). Every citation in
this pack's axis files states which repo's numbering it means at first use, precisely because the
numeric collision is real and a reader cross-referencing "ADR-0038" without the repo qualifier
would land on the wrong document in either direction.

## What this pack deliberately does NOT re-verify

This pack reads six specific CSS/ADR files directly rather than sampling either repo's full
stylesheet tree; it does not re-audit every component's CSS for conformance to the patterns it
documents (that is each repo's own `component-token-audit`/gate tooling), and it does not
independently re-verify CSS Modules' bundler-level mechanics against a live source (general,
widely-documented behavior, cited as such). A reader confirming a specific claim against CURRENT
code should re-read the cited file directly in the named repo — both grounding repos' own CSS is a
moving target, same caveat every sibling pack in this series carries.

## Fence provenance

The css-system-facts-vs-size-and-shape-rules (CSS-specific FRAME/RHYTHM token-family naming vs.
the general spacing/density THEORY) and css-system-facts-vs-web-component-facts (structural CSS
architecture/testing vs. per-control platform lifecycle/test-file facts) fences in this pack's
SKILL.md were negotiated against the two frontend siblings most directly implicated — each
sibling's own suite gains the reciprocal no-trigger case, and each sibling's own description gains
a one-line NOT-pointer naming this pack in return. The `design` plugin's palette/typography/
design-system suites (`make-palette`, `pick-fonts`, `font-token-rules`, `make-design-system`,
`token-builder`) were checked directly against this pack's trigger surface (`@layer`, cascade,
`@scope`, `light-dark()`, CSS Modules, decision-log/tested-contract) and carry NO colliding
trigger language in their own descriptions — the router selects on description text, not body
prose, and none of those five descriptions mentions any of this pack's trigger vocabulary. This PR
stays single-plugin on that basis (see PR body's judgment-call note) rather than also bumping
`design`.

Extension: governed by [[make-pack]]
