---
name: make-figma-make-kit
description: >-
  Author, evaluate, or regenerate a Figma Make design-system guidelines/ folder for any
  theme or brand. Use whenever a Make kit needs the routed markdown tree (Guidelines.md
  entry + foundations/ + components/) it reads to generate on-brand UI, or when asked to
  "create/author Figma Make design system guidelines", "make kit guidelines folder",
  "write Guidelines.md for Figma Make", "add a component file to our Make guidelines",
  "Make output ignores our design system — fix the guidelines", or "check this guidelines
  folder before shipping". Covers the routed-folder shape, the imperative register, the
  React + Tailwind + shadcn/ui flavor, the --{prefix}-{family}-{slot} naming grammar, and
  the gates — Make validates nothing, so this is the gate. NOT for Claude Design
  (make-dscard-kit); NOT for Google Stitch
  (make-stitch-kit); NOT for cross-platform strategy
  (make-design-kit); NOT for grading (design-kit-checker); NOT for palette/tokens
  (make-palette / token-builder).
disable-model-invocation: false
user-invocable: true
---

# Design System Author — Figma Make guidelines/

A Figma Make design system is a **routed prompt**: a `guidelines/` folder of many short
markdown files that Make enters at `Guidelines.md` and follows on demand. **Structure is
the prompt** — the folder tree, file names, and routing tables do the work that sections
and schemas do on other platforms. Two platform facts govern everything (ground truth +
citations: `references/format.md`):

- **Progressive disclosure is the sizing rule.** Make reads `Guidelines.md` first, then
  only the leaves a task needs — "multiple short guidelines files are better than a few
  large files." Split before a file grows; never flatten into one file.
- **Make validates nothing.** No linter, no schema — every gate falls to this skill's
  run, which is the gate of record. Make can auto-generate baseline guidelines from a
  design package; hand-authored guidelines override that baseline and must out-specify it.

## The declared flavor: React + Tailwind + shadcn/ui

**Standing decision, not a per-project choice**: Figma Make's own ecosystem preference
is React + Tailwind + shadcn/ui — so this skill targets it by default, rather than the
platform docs' generic illustrative naming. The canonical `{prefix}-{family}-{slot}`
model stays the authoring source of truth; **`styles.css` is the compiled shadcn
projection of it** — the same core+profiles discipline every sibling already runs,
Figma Make was just missing its correct profile. Full mechanism, the exact variable
shape, and the four platform-specific doctrine overrides (dark mode is a `.dark` class
toggle, not `light-dark()`; states are Tailwind modifiers, not tokens; components are
shadcn's own variant API, not bespoke CSS; extension roles ride the same file):
**`references/shadcn-tailwind-flavor.md` — read this before authoring `color.md` or
any component leaf.**

## The shape (minimal conforming folder)

```
guidelines/
├─ Guidelines.md        # entry — character, routing table, hard rules, workflow
├─ setup.md             # import styles.css; no @source rules; no ThemeProvider needed
├─ styles.css           # real shadcn CSS-variable shape + @theme inline (the compiled core)
├─ foundations/
│  ├─ color.md          # roles narrated + mapped to shadcn/extension variable names
│  ├─ typography.md     # levels as set-together units (size + line-height + weight)
│  └─ spacing.md        # closed spacing scale, radius ladder, layout rules
└─ components/
   ├─ overview.md       # catalog + variant decision tree, routes to component leaves
   └─ button.md …       # one leaf per component: shadcn variant map, not raw CSS
```

`setup.md` + `styles.css` are now standard, not conditional — Figma Make's own docs
treat them as central, and the shadcn flavor always has a real stylesheet to wire.
(A kit with genuinely no code package at all falls back to the pre-shadcn raw-CSS
approach; that path is now the exception, not the default — see
`shadcn-tailwind-flavor.md`.) Grow one leaf per component as the kit grows. Per-file
templates: `references/templates.md`.

## Create — the method (each step with its failure mode)

1. **Ground the character as a specific reference.** One named world ("Studio 54's
   dancefloor: mirror-ball silver, gold lamé, hot-pink light on black") opens
   `Guidelines.md` — a specific reference describes a point in design space; adjectives
   ("modern, clean, premium") describe a region and force a rambling don't-list.
2. **Take terminal values from the verified upstream token model.** Never invent, derive,
   or eyeball a value — every OKLCH pair, type level, and spacing step arrives
   pre-verified from the palette/token source. **Divergence rule:** where the upstream
   system made a decision this skill would make differently, call it out to the author —
   never override it silently.
3. **Author `Guidelines.md`.** Character paragraph → routing table naming **every** leaf
   (a question column beats a file list — route by task) → hard rules as `Do NOT …`
   prohibitions under an `IMPORTANT` marker → a short tokens-first workflow. *Fails as:*
   an unrouted leaf Make never finds, or soft rules ("use sparingly") generation ignores.
4. **Compile `styles.css`, then author `foundations/`.** `styles.css`: the shadcn
   variable shape (`--background` … `--sidebar-ring`) plus every extension role this
   theme needs (signature families, `success`/`warning` — shadcn's base set has no
   slot for them), a `.dark` class block, and `@theme inline` mapping every role,
   base and extension alike. `color.md` then narrates roles by their shadcn/extension
   *names*, not the internal grammar — the naming-grammar model stays the authoring
   source (cite it), the prose points at what's actually importable. `typography.md`:
   each level a set-together unit. `spacing.md`: closed scales — "a 13px gap does not
   exist in this system."
5. **Author `components/`.** `overview.md` = catalog + variant decision tree routing to
   leaves. Each leaf: when-to-use, a **closed variant set mapped to shadcn's own
   variant prop** ("`variant=\"destructive\"` — nothing invented"), **states as Tailwind
   modifiers** (`hover:bg-primary/90`, not a separate token) with the literal per-scheme
   value they resolve to, one correct-vs-incorrect code pair, and its own `Do NOT`
   rules. *Fails as:* redeclaring padding/radius a shadcn component already bakes in —
   name the variant, not the CSS.
6. **Voice: imperative register, universal doctrine.** The platform's documented register
   ("Do not use small text for anything except captions" beats "use small text
   sparingly") carries *how* sentences are voiced; the universal prose doctrine — specific
   reference over adjectives, negative constraints first-class — governs *what* they say.
7. **Gate, score, receipt.** Run the checker (below), fix, re-run; self-score against
   `references/rubric.md`; write the profile receipt (README next to `guidelines/`)
   recording each gate's result — including UNMEASURED ones. Receipt template and gate
   definitions: `references/gates.md`.

## Evaluate / Regenerate

- **Evaluate** an existing folder: run the checker, then score the judgment dimensions
  (D7–D9) against `references/rubric.md` with cited evidence — a score with a fix, never
  a bare number.
- **Regenerate** after the token source or theme moved: re-derive tables and the runtime
  block from the *current* upstream model (never patch values in prose), then run the
  full loop. A receipt predating an upstream change is stale until re-run.

## Validation loop (finalize only when it clears)

draft → `python3 scripts/make_guidelines_check.py <guidelines_dir> [--compare sibling.json]`
→ fix the *folder*, not the check → re-run → self-score vs `references/rubric.md` →
receipt. The checker gates: routing integrity (every route resolves, no unrouted
leaves) · all fill/on pairs ≥ 4.5:1 in both schemes · scheme parity · runtime block +
the `color-scheme` trap · states as values · hard rules present · carrier equality when
`--compare` names a sibling export (UNMEASURED otherwise — recorded, never laundered
into a pass). `selftest` proves the checks fire. **Generator ≠ critic:** for a shipping
kit, dispatch the independent design-kit-checker seat (or doc-checker bound to
`references/rubric.md`) — don't bless a folder you just wrote in the same pass.

## References & composition

| Path / peer | Use when |
|---|---|
| `references/format.md` | Platform ground truth — layout, consumption model, endorsed shapes, conformance checklist; cited to source |
| `references/shadcn-tailwind-flavor.md` | The declared flavor — read before authoring `color.md`, `styles.css`, or any component leaf; the four doctrine overrides and why |
| `references/templates.md` | File-by-file templates + worked-example snippets (router, token tables, runtime block, component leaf) |
| `references/gates.md` | Gate definitions, receipt template, UNMEASURED discipline, divergence rule |
| `references/rubric.md` | The standard — score every create/evaluate/regenerate pass against it |
| `scripts/make_guidelines_check.py` | The mechanical gates (D1–D6, D10, D11); `selftest` fixture-locks them |
| [[make-palette]] / [[check-colors]] | Upstream: design the ramp / verify the pairs — this skill consumes their verified output |
| [[make-design-kit]] (hub) | Cross-platform strategy; sibling exports for other platforms route to make-dscard-kit / make-stitch-kit |

**Done** = folder authored to the shape, checker green, judgment dims ≥ 3 against the
rubric, receipt written with honest UNMEASURED entries. **NOT done** = a green checker
alone (D7–D9 unscored), a receipt claiming carrier equality that was never compared, or
values invented rather than taken from the verified upstream model.
