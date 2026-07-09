# Figma Variables — collections, modes, aliasing, and safe mutation

Provenance: the nonoun-color-tokens variable system (Color Primitives → Color Modes cascade,
Typography/Geometry moded collections, Font Primitives), `figma/plugin/code.js` +
`figma/binder/*.mjs`, PRs through #238 (2026-07). Confidence markers per claim.

## How do I get a live raw→semantic cascade (edit one primitive, everything follows)?

**Aliasing is the only mechanism.** A semantic variable whose mode value is
`figma.variables.createVariableAlias(rawVariable)` re-resolves live when the raw variable changes;
a copied VALUE is dead on arrival [verified — the repo's whole Color Modes design; conceptual model
in its `knowledge-05-figma-plugin.md`]. Pattern per semantic role:

```js
const alias = figma.variables.createVariableAlias(rawVar);
semanticVar.setValueForMode(lightModeId, figma.variables.createVariableAlias(rawLight));
semanticVar.setValueForMode(darkModeId, figma.variables.createVariableAlias(rawDark));
```

Anything BOUND to the semantic variable (paints, styles, node properties) then tracks
Light/Dark automatically through the collection's mode.

## How do I handle a collection's modes without corrupting it?

- **Anchor on `collection.defaultModeId`, never `modes[0]`** — for a collection you created they
  coincide, but a *foreign same-named collection's* default may not be first, and removing it
  throws [verified — the repo's `applyFloatPlans` comment + fix].
- The default mode can't be removed: **rename it** to your first mode (`renameMode(defaultId,
  "Base")`), then `addMode(name)` the rest — reusing an existing mode **by name,
  case-insensitively** on re-apply.
- Prune stale modes only when they're not the default and not the last remaining mode.
- **Write a value for EVERY mode of every variable** ("value-complete" plans). A variable with an
  unset mode is the classic half-bound import that looks fine in one mode and broken in the other
  [verified — `validateModeInterchange` exists exactly for this].

## How do I create/update variables idempotently?

**Find-or-create by name, scoped to the collection; prune orphans the same way** [verified —
every apply in the repo]:

```js
const byName = {}; // name → Variable, from getLocalVariablesAsync filtered by variableCollectionId
const v = byName[name] || figma.variables.createVariable(name, collection, type);
v.setValueForMode(modeId, value);
// after the loop: every byName entry NOT in the current plan → v.remove()
```

Re-applying the same plan must be a no-op (no duplicate collections/variables/modes) — assert this
in tests; duplicates corrupt the user's Variables panel.

## How do I make sure I never touch the USER's collections/styles?

**Provenance registries in `figma.root` pluginData**: a JSON map of `{ name → id }` for everything
you created, written at each apply [verified — the repo's float + style registries]. Rules:

- Look up by **id from the registry first**, then by name — a user's manual RENAME survives
  (you track id, not name); a user-deleted entry just recreates.
- Never canonicalize or prune a same-named collection you didn't create — make your own instead.
- Prune = "registry entries absent from the current plan", never "things whose name looks like ours".

## What variable types exist and what are the value shapes?

`COLOR` (`{r,g,b}` or `{r,g,b,a}` floats 0..1 — **alpha rides IN the variable value**, not on the
consuming paint), `FLOAT` (number), `STRING`, `BOOLEAN`; plus the alias value
`{ type: "VARIABLE_ALIAS", id }` in any slot [verified]. Two ordering rules when applying a plan
that mixes literals and aliases:

1. **Literals before aliases** — an alias needs its target to exist; flatten plans so every alias
   follows its target, and drop dangling aliases planner-side so the executor can never throw
   [verified — `primitivesApplyPlan`].
2. `setBoundVariableForPaint`/`setBoundVariable` take the **Variable object, not an id string** —
   resolve via your byName/byId map first [verified — also documented in Figma's typings].

## How many variables is too many?

The repo ships ~424 semantic + ~500 raw color variables plus moded float collections in one file
without issues [verified 2026-07]. Figma's own per-file limits are generous (thousands)
[drift-prone — plan-level counts are fine; re-check Figma's published limits if you approach 5k].

## Can variables be imported without a plugin?

Yes — Figma's native variable import (UI3 JSON) resolves alias references **when the target
primitives collection already exists in the file** [verified — the repo's OD-004 spike, re-verified
2026-06-15]. That makes a two-file import order (primitives first, semantic second) a viable
plugin-free path; the moded float collections still need the plugin (native import doesn't create
modes).
