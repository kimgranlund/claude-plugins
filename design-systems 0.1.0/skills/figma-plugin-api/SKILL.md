---
name: figma-plugin-api
description: >
  Answers Figma Plugin-API questions from battle-tested practice — variables, styles, sandbox,
  interchange. Use for: variable collections/modes and raw→semantic ALIASING ("alias variables",
  "removing a mode threw", "find-or-create without duplicates"), styles bound to variables
  ("setBoundVariableForPaint", "text style ends up Inter Regular 12", "loadFontAsync can't find
  the face", "which text fields bind"), sandbox/VM failures ("parses in Node, fails in Figma",
  "catch without a param", "networkAccess none", "unit-test plugin code"), token JSON shapes
  ("UI3 import format", "com.figma.modeName", "aliasData", "moded plan"), and
  pluginData/clientStorage. ANSWERS, does not generate. NOT for the nonoun color-tokens plugin's
  own binder/apply procedure (its repo-local maintaining-figma-plugins); NOT the DESIGN.md format
  (design-md-format); NOT --md-sys-* semantics (material-design-*-tokens); NOT the Figma MCP
  tools; NOT the REST API, widgets, or scene-node/layer work (not covered).
user-invocable: true
disable-model-invocation: false
---

# Figma Plugin API — the earned knowledge

Answers-only domain pack, distilled from shipping a production Figma plugin (the nonoun
color/token generator: variable cascades, moded collections, bound style swatches — PRs #231–#238
and the incidents before them). Every claim carries a confidence marker (`[verified]` with source
+ date · `[inferred]` · `[drift-prone]`) — trust accordingly, and re-verify `[drift-prone]` rows
against developers.figma.com when the stakes are real.

## Consult table

| The ask looks like | Load |
|---|---|
| Parse/load failures in the sandbox, `catch {`, ES-version doubts, `networkAccess:"none"` consequences, testing sandbox code (mock figma, module.exports tail), the UI↔sandbox postMessage contract, async API surface | `references/sandbox-vm.md` |
| Variable collections/modes (defaultModeId, rename/add/prune), the raw→semantic ALIAS cascade, find-or-create + provenance registries (never touch user content), value types & literals-before-aliases, plugin-free native import | `references/variables.md` |
| Paint styles bound to color variables, text styles (face resolution from `listAvailableFontsAsync`, the Inter-Regular-12 abandonment bug, bindable text fields, the lineHeight/letterSpacing FLOAT-reads-px trap), style foldering/naming, style registries + safe prune | `references/styles.md` |
| Token JSON in/out of Figma: UI3 native-import files (`com.figma.modeName`, `aliasData`), the collection interchange envelope, value-complete moded apply plans, the styles plan schema, DTCG-proper vs Figma-flavor | `references/interchange-schemas.md` |
| `root.pluginData` vs `clientStorage`, the config-embed round-trip (lossless vs approximate), registry storage — **partial axis: no scene-graph coverage** | `references/document-plugindata.md` |

## The three cross-cutting disciplines (load-bearing everywhere)

1. **Pure planner + dumb executor** — compute a deterministic plan outside the sandbox, execute it
   verbatim inside; parity-gate any hardcoded mirror the no-modules VM forces.
2. **Provenance before mutation** — registries (`{name → id}` in `root.pluginData`) make pruning
   safe; nothing the user made is ever touched.
3. **Resolve from reality, mutate after success** — read Figma's actual state (fonts, collections,
   modes) before acting; never create-then-hope (the Inter-Regular-12 lesson).
