# Figma interchange schemas — the JSON that moves tokens in and out

Provenance: the nonoun-color-tokens export/import surfaces (`exportDTCG`, `exportUI3`,
`typeTokensFigmaModes/Primitives`, `modeApplyPlan`, `stylePlans`), 2026-06 → 2026-07.
These are the shapes that worked against real Figma; markers per claim.

## What shape does Figma's native variable import want? (UI3 JSON)

One file per MODE of a collection, a token tree whose leaves are DTCG-ish color tokens, with the
mode named in `$extensions` [verified — the repo's `palette.tokens.json` / `Light_tokens.json` /
`Dark_tokens.json` triple imports natively]:

```json
{
  "$extensions": { "com.figma.modeName": "Light" },
  "primary": {
    "onPrimary": {
      "$type": "color",
      "$value": { "colorSpace": "srgb", "components": [0.1, 0.2, 0.3], "alpha": 1, "hex": "#1A334D" },
      "$extensions": { "com.figma.aliasData": {
        "targetVariableName": "primary/050",
        "targetVariableSetName": "Color Primitives"
      } }
    }
  }
}
```

- **`aliasData` resolves on native import ONLY when the target collection already exists in the
  file** — so import primitives first, semantic second (plugin-free cascade) [verified — OD-004
  spike, re-verified 2026-06-15].
- Tree paths become variable names: group nesting `primary → onPrimary` = variable
  `primary/onPrimary` [verified].

## What's the collection-level interchange (multi-mode, one file)?

The repo's UI3 collection schema (also what its plugin executors consume) [battle-tested;
not a Figma-published schema — a working convention]:

```json
{
  "$schema": "figma-ui3-variables.color.schema.v1",
  "collections": {
    "Color / Semantic": {
      "modes": ["Light", "Dark"],
      "variables": {
        "primary/onPrimary": { "type": "COLOR", "values": { "Light": "{raw/primary/050}", "Dark": "{raw/primary/950}" } }
      }
    }
  }
}
```

`{path}` string values are in-file alias references an importer resolves. Float/string variants use
the same envelope (`figma-ui3-variables.float.schema.v1`; `values` keyed by mode name; a
`{ type: "ALIAS", target: "<variable key>" }` entry instead of `values` for same-collection
aliases) [verified — `typeTokensFigmaModes` / `typeTokensFigmaPrimitives`].

## What does a VALUE-COMPLETE moded apply plan look like?

The deterministic plan an executor can run verbatim (the planner/executor split) [verified —
`modeApplyPlan`]:

```json
[{
  "collection": "Typography",
  "modes": ["Base", "Mobile"],
  "defaultMode": "Base",
  "addModes": ["Mobile"],
  "variables": [
    { "name": "Body/MD/size", "type": "FLOAT", "values": [
      { "mode": "Base", "value": 16 }, { "mode": "Mobile", "value": 13 } ] }
  ]
}]
```

Invariants: variables name-sorted (determinism), one value per mode per variable (validate BEFORE
planning — an unset mode is the half-bound-import bug), `defaultMode` = the first mode (the
executor renames Figma's un-removable default to it).

## What's the styles plan schema?

`nonoun-figma-styles.plan.v1` [verified — shipped in Download-All as `figma/styles.plan.json`]:

```json
{
  "$schema": "nonoun-figma-styles.plan.v1",
  "paints": [{ "name": "Primary/onPrimary", "varName": "primary/onPrimary" }],
  "texts": [{
    "name": "Display/xl", "voice": "Display", "step": "XL",
    "bind": { "fontSize": "Display/XL/size", "fontFamily": "font/Display", "fontWeight": "weight/Display/bold" },
    "literal": { "family": "Inter Tight", "weight": 700, "size": 61, "lineHeight": 49, "letterSpacing": -1.2, "textCase": "none" }
  }],
  "fontPrimitives": { "collection": "Font Primitives", "mode": "Value",
    "variables": [ { "name": "family/display", "type": "STRING", "value": "Inter Tight" },
                   { "name": "font/Display", "type": "ALIAS", "target": "family/display" } ] }
}
```

Design rules baked into the shape: every text style carries a **complete literal fallback** (so a
consumer degrades per-field when a bind target is missing); `fontPrimitives.variables` is ordered
**literals before aliases** with dangling aliases already dropped.

## DTCG proper (the W3C flavor) vs the Figma flavor — what differs?

- Pure DTCG carries `$type/$value` composite `typography` tokens, relative `lineHeight`
  (multiplier) and `em` tracking; Figma-bound exports flatten to per-property FLOAT variables and
  px, because Figma variables have no composite type [verified — the repo ships both,
  `type.tokens.json` (DTCG) vs `figma/type.tokens.json` (px) vs the moded collection].
- Keep the Figma-import files ALWAYS px regardless of the user's CSS unit preference — Figma is
  numeric [verified].
