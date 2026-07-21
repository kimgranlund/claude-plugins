---
name: make-stitch-kit
description: >
  Author, evaluate, or regenerate a Google Stitch DESIGN.md (single file: YAML
  frontmatter tokens + 8 canonical markdown sections) for any theme or brand.
  Use when asked to "create/author a Google Stitch DESIGN.md", "write a stitch
  design-md file", "lint my DESIGN.md", "port my design system / tokens to
  Stitch", "my DESIGN.md fails lint", or "why all these orphan warnings".
  Covers the alpha frontmatter schema and {path.to.token} refs, canonical
  section order + aliases, unknown-content tolerance, the prose philosophy (a
  specific reference beats adjectives), OKLCH values, dark schemes as -dark
  siblings + the primary compat alias, the --{prefix}-{family}-{slot} naming
  grammar, and the lint gate (npx @google/design.md lint — zero errors,
  expected-warning reading). NOT for Claude Design bundles
  (make-dscard-kit); NOT for Figma Make guidelines
  (make-figma-make-kit); NOT for cross-platform strategy
  (make-design-system); NOT for grading an export you didn't
  author (design-system-checker agent).
disable-model-invocation: false
user-invocable: true
---

# Google Stitch DESIGN.md — Author · Evaluate · Regenerate

A Stitch DESIGN.md has two readers: a **strict parser** (the `@google/design.md` linter — schema, section grammar, reference resolution, contrast) and a **model** (the agent that generates UI from it). Per the Stitch philosophy, *prose is where the design lives*; token values are context, not rendering instructions. Author for both readers at once — a file that lints clean but reads as adjectives generates generic UI; a vivid file that breaks the grammar forfeits the linter's checks.

Ground truth: `references/stitch-spec.md` — derived from github.com/google-labs-code/design.md (spec version **alpha**, fetched 2026-07-05); re-derive on any upstream version bump. Method + worked snippets: `references/authoring-method.md`. Gate mechanics: `references/lint-gate.md`. Standard: `references/rubric.md`.

## Facts that decide everything else (measured 2026-07-05)

- **OKLCH is accepted and contrast-checked.** The linter parses `oklch(L C H / A)` values and WCAG-checks them (internal sRGB conversion). Default to OKLCH; hex is upstream's *recommendation*, not a requirement.
- **`light-dark()` is REJECTED as an error** ("not a valid color"). The alpha schema has **no color-scheme axis** — dark values ride as `-dark` suffixed siblings (`primary-base` / `primary-base-dark`), legal under the accept-if-valid rule.
- **The inherent cost:** `-dark` siblings lint as `orphaned-tokens` *warnings* — components can only reference one end. Documented spec cost, not a defect; classify and record them in the receipt.
- **`primary` is quasi-required** (`missing-primary` warning: "agents will auto-generate one"). When the naming grammar puts the brand color at `primary-base`, ship a documented `primary` compat alias with the same value.
- **A duplicate `##` heading rejects the whole file.** Canonical order is enforced for the 8 known sections; unknown sections and unknown token names are tolerated — the load-bearing rule that lets extra sections, `-dark` siblings, and custom token groups ride.

## Create

1. **Theme → a specific reference.** Name a world ("a 1970s graduate lecture handout", "Studio 54's dancefloor"), never an adjective list — a reference describes a *point* in design space and imports its negative constraints for free.
2. **Roles before values.** 15–25 semantic color roles named by the grammar `{family}-{slot}` (slot registry in `references/authoring-method.md`); every fill ships a measured on-partner per scheme (never a constant); states (`-hover`, `-active`) ship as values. Every value is terminal — the consumer never derives, mixes, or darkens.
3. **Frontmatter** per the alpha schema: `colors` (with `-dark` siblings + the `primary` alias), `typography` (9–15 levels; size, line-height, weight set together — line-height as a unitless factor (`1.5`), letter-spacing as em/`%`, never px), `spacing`, `rounded`, `components` with variant keys (`button-primary-hover`) and `{path.to.token}` refs — reference roles, never repeat raw values.
4. **The 8 canonical sections in order** — Overview · Colors · Typography · Layout · Elevation & Depth · Shapes · Components · Do's and Don'ts — then any appended sections (Responsive Behavior, Agent Prompt Guide, Motion…) riding unknown-section tolerance. Prose–token accord runs both directions: every color the prose sells exists as a token; every role token appears in prose with its usage boundary.
5. **Verify** via the loop below; finalize only when the gate is clean and the receipt is written.

## Evaluate / Regenerate

Evaluate an existing DESIGN.md by running the gate loop, then scoring `references/rubric.md` — gates first, review dimensions with cited evidence after. Regenerate (porting an existing token system or brand into Stitch) is evaluate + close the gap, under one standing rule:

**Divergence rule.** An upstream system's made decisions — naming grammar, payload notation, role inventory, scale steps — are **called out, never silently overridden**. Where this skill's defaults differ (OKLCH payload, `{family}-{slot}` names), state the divergence and its reason in the deliverable; the follow-up is the author's call.

## Validation loop (the gate)

Draft → offline check → lint → classify → fix → re-run. Finalize only at zero errors with every warning classified.

```
python3 scripts/prelint.py check DESIGN.md            # offline: grammar, refs, parity, light-dark(), dupes
npx -y @google/design.md lint DESIGN.md > lint.json   # the platform gate; exit 1 on errors only
python3 scripts/prelint.py classify lint.json         # ACTION / EXPECTED / REVIEW / INFO / OK
```

- **Zero errors, always.** `broken-ref` is the only error-severity lint rule; duplicate headings and `light-dark()` values also hard-fail.
- **Warnings are read, not counted.** EXPECTED class (orphaned `-dark` siblings) rides; ACTION class (contrast < 4.5:1, missing-primary, section-order) gets fixed. Full interpretation table: `references/lint-gate.md`.
- **Deliver a receipt** with the file — lint result, warning classification, and the checks the linter does not run (all fill/on pairs in *both* schemes: dispatch [[check-colors]] for that proof; the linter only sees component pairs on the light end). Template in `references/lint-gate.md`.

## References & routing

| Path | Use when |
|---|---|
| `references/stitch-spec.md` | Any schema / section / CLI / lint-rule fact — the derived ground truth |
| `references/authoring-method.md` | Writing the file: prose doctrine, naming grammar + slot registry, scheme encoding, worked snippets |
| `references/lint-gate.md` | Running and reading the linter: JSON anatomy, expected-warnings table, pre-lint checklist, receipt template |
| `references/rubric.md` | Scoring a draft or an existing DESIGN.md |
| `scripts/prelint.py` | Deterministic offline structural check + lint-JSON classifier (first pass needs no npm) |
| [[check-colors]] | The all-pairs × both-schemes contrast proof the linter doesn't run |
| [[make-palette]] | Upstream: designing the ramp/roles this file reduces from — this skill consumes a palette, it does not design one |

**Done** = lint zero errors · every warning classified in the receipt · rubric gates pass · prose–token accord holds both directions. **Not done** = a green lint alone — the linter never reads the dark scheme, the prose, or the pairing law.
