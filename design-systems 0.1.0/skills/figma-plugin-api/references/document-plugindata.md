# Document state: pluginData, clientStorage, and the config round-trip

> **PARTIAL AXIS — scope honesty.** The earned knowledge covers document-level state and the
> async API surface. **No scene-node manipulation knowledge was earned** (no frames, layers,
> selection, or node styling) — nothing here covers the scene graph, and this file must not be
> read as implying it. Fill via a cited research wave if a task needs it.

Provenance: nonoun-color-tokens (`figma/plugin/code.js` config/registry stores, the gallery's
saved-sets store), 2026-06 → 2026-07.

## Where do I persist state that must travel WITH the file?

`figma.root.setPluginData(key, string)` / `getPluginData(key)` — a synchronous string store on the
document root, scoped to your plugin, saved in the `.fig` and travelling with duplicates/handoffs
[verified]. The repo uses it for:

- **The config embed**: the full generator parameters serialized alongside the variables, so a
  later "load" round-trips **losslessly**. Without it, state can only be *approximated* back out
  of the live variables (the repo recovers hue/chroma from raw ramp values as a lossy fallback) —
  embed the source of truth, don't reverse-engineer it [verified].
- **Provenance registries** (`{name → id}` JSON for collections/styles the plugin created) — the
  basis of never-touch-user-content pruning; see `variables.md` / `styles.md`.

Practical limits: values are strings — `JSON.stringify` in, guarded `JSON.parse` out (a corrupt or
foreign value must degrade to a default, never throw) [verified — every reader in the repo wraps
in try/catch]. Keep payloads small (KBs, not MBs) [inferred — no hard limit hit; Figma documents
an entry size cap; re-check if embedding large blobs].

## Where do I persist state PER USER across files?

`figma.clientStorage.getAsync/setAsync` — async, per-user, per-plugin, machine-local (does NOT
travel with the file) [verified — the repo's gallery saved-sets]. Use for user-level libraries;
use `root.pluginData` for anything another person opening the file must see.

## The two stores side by side

| | `root.pluginData` | `clientStorage` |
|---|---|---|
| Travels with the .fig | ✅ | ❌ |
| Visible to other users of the file | ✅ | ❌ |
| Sync/async | sync | async |
| Value type | string | any structured-clonable |
| Repo use | config embed, provenance registries | the user's saved palette sets |

## Async API + documentAccess

The modern surface is async-first (`getLocalVariableCollectionsAsync`, `getStyleByIdAsync`,
`listAvailableFontsAsync`, …) and required under `documentAccess: "dynamic-page"`; prefer it
unconditionally [verified in shipped code; drift-prone — track Figma's deprecation notices].
