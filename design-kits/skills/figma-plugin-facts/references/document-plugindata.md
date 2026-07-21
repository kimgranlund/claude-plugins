# Document state: pluginData, clientStorage, and the config round-trip

> **PARTIAL AXIS — scope honesty.** The earned knowledge covers document-level state and the
> async API surface. **No scene-node manipulation knowledge was earned** (no frames, layers,
> selection, or node styling) — nothing here covers the scene graph, and this file must not be
> read as implying it. Fill via a cited research wave if a task needs it.

Provenance: ultimate-tokens (`figma/plugin/code.js` config/registry stores, the gallery's
saved-sets store), 2026-06 → 2026-07.

## Where do I persist state that must travel WITH the file?

`figma.root.setPluginData(key, string)` / `getPluginData(key)` — a synchronous string store on the
document root, scoped **to your plugin's `id`** (not its name — see the rename trap below), saved in
the `.fig` and travelling with duplicates/handoffs [verified]. The repo uses it for:

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

## What happens to pluginData when the plugin's `id` changes?

**It is orphaned — permanently, and no migration can be written.** [verified — ultimate-tokens PR #247 /
ADR-014, 2026-07-09]

`setPluginData` keys are namespaced by the **calling plugin's `id`**. A plugin reads back only what *it*
wrote under *its own* id. So when a `manifest.json` `id` changes, the pre-rename keys are not
differently-named — they are **unreachable from any code path, in any plugin**. There is no cross-id read
API, and a "migration" would have to execute under the OLD id, which is the thing being replaced.

The consequences, in the order they bite:

- **A legacy-key fallback is dead code.** `getPluginData("old-key")` under the new id returns `""`, always
  — never the old value. A fallback that survived a *previous* rename only worked because that rename left
  the `id` untouched. Delete it; don't keep it as a comforting no-op.
- **Gate the degradation, not the migration.** The reachable behaviour is: with only pre-rename keys
  present, the loader must return a **clean empty state** — never throw, never adopt a stale key. That is
  the assertion worth writing.
- **Weigh the rename against the data.** Renaming a plugin's `id` is a data-loss event for every existing
  file. It can still be right (the repo did it), but price it: what did users store, and can they
  regenerate it? Here the config also travels in the exported bundle, so the cost was one re-run of
  *apply* on an old `.fig`.
- **A published sibling plugin should usually keep its `id`.** The repo renamed its flagship and
  deliberately left its companion binder plugin's `id` alone — renaming would have orphaned *that*
  plugin's data and its listing for no gain.

**The asymmetry to remember:** a web app's `localStorage` keys *are* migratable (same origin, no
namespacing), so a rename there is a chained copy — newest legacy wins, never clobber a present key. The
plugin store offers no such path. Same rename, two completely different compatibility stories; the
difference is the platform's, not a design choice [verified].

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
