# The Figma plugin sandbox & VM — what actually runs, and what silently doesn't

Provenance: earned in the ultimate-tokens generator (repo `nonoun/ultimate-tokens`:
`figma/plugin/code.js`, `figma/binder/figma-semantic-binder/code.js`, verifiers `test/figma/*.mjs`),
2026-06 → 2026-07. Confidence markers per claim.

## Why does my plugin fail to parse in Figma when Node runs it fine?

Figma's plugin VM is **jsvm-cpp, not V8**. Its parser rejects some post-ES2018 syntax that every
Node/`node --check` run accepts — so a green Node load proves nothing about Figma.

- **Optional catch binding (`catch {` with no param, ES2019) PARSE-fails the whole file.**
  [verified — real incident 2026-06-17: the entire plugin failed to load; Node and `new Function`
  both accepted the file]. Always write `catch (e) {`.
- Because the failure is at parse time, no runtime guard can catch it. The countermeasure is a
  **static gate**: grep the sandbox file for `catch {` (and other risky syntax) in CI
  ([verified — the `vmsyntax` gate in `test/figma/plugin.mjs`]).
- Posture for anything beyond ES2018 (`?.`, `??`, class fields): assume unsupported until proven
  in a real Figma run [inferred from the ES2019 failure; not exhaustively tested].

## Why can't my plugin import modules?

The sandbox is a **non-module VM** — no `import`, no `.mjs`, no dynamic `import()` [verified —
repo constraint #2]. Consequences:

- Shared logic must be **hardcoded as a mirror** in the sandbox file, with a **parity gate**
  diffing the mirror against the importable source both directions (the repo's `roleTable(n)`
  copy vs `bind-plan.mjs`; the 2026-06-18 scrim-grammar drift is the incident the gate exists for)
  [verified].
- The clean architecture this forces: **pure planner (importable, unit-tested) + dumb executor
  (sandbox, runs plans verbatim)**. The planner computes a deterministic plan object; the sandbox
  never re-derives anything. [battle-tested convention — three planners in the repo:
  `bind-plan.mjs`, `mode-apply-plan.mjs`, `style-plan.mjs`.]

## How do I unit-test sandbox code that can't be imported?

Two patterns, combined [verified — `test/figma/plugin.mjs`]:

1. **Conditional export tail** in the sandbox file:
   `if (typeof module !== "undefined") module.exports = { … }` — a no-op inside Figma, a handle
   for the verifier.
2. **Load via `new Function("figma", "__html__", "module", code + "\nreturn {…};")`** against a
   **mock figma** (in-memory collections/variables/styles with the same method names, including
   the async variants and `defaultModeId`). The mock can hide missing-API reality — pin the API
   names you use against the docs, and validate in a real Figma run before calling a feature done.

## What does `networkAccess: "none"` actually forbid?

Everything: `fetch`, `XMLHttpRequest`, `WebSocket`, remote `import()`, *and any CSS/resource URL in
the plugin UI* [verified — repo ADR-010/AC-P3]. Consequences that surprise:

- **Fonts must ship base64-embedded** in the UI html (`@font-face` data URIs) — there is no CDN.
- Runtime font loading features in the web build must be **gated off inside Figma** (an
  environment flag set by the bridge, e.g. `inFigma`).
- `figma.loadFontAsync` is NOT network access in this sense — it loads from Figma's own font
  service and works offline-declared plugins [verified in the styles feature, 2026-07-09].

## What error handling does Figma review require?

**Never surface a raw error to the user.** Figma policy rejects plugins that show
`e.message`/stacks in `figma.notify` [verified — repo constraint #4]. The pattern:

- Map each request type to a human action string (`ACTIONS = { apply: "apply the variables", … }`)
  and notify `Couldn't ${action}` on failure; log the real error to `console.error`.
- Enforce mechanically: a `compliance` gate greps for `figma.notify(...e.message/String(e)/.stack)`.
- Isolate independent applies in their **own try/catch** so a late failure never masks an earlier
  success (variables applied, styles failed → the user still gets the variables + an honest toast).

## How does the plugin UI talk to the sandbox?

The UI is an iframe (`__html__`); the contract is `postMessage` both ways [verified — the repo's
generated `ui.html` bridge]:

- UI → sandbox: `parent.postMessage({ pluginMessage: msg }, "*")`; sandbox receives via
  `figma.ui.onmessage`.
- Sandbox → UI: `figma.ui.postMessage(m)`.
- **Async completion signaling matters**: the sandbox's work is async; the UI's optimistic toast
  can't know when it finished. Post an explicit `…-done` message (and an `…-error` on failure) so
  the UI can settle its state [verified — the `apply-done`/`apply-error` contract].
- Messages are structured-cloned: plain JSON-able objects only.

## Which API surface is async, and which stale sync calls should I avoid?

Use the async variants throughout — they are required under dynamic-page access and safe
everywhere: `getLocalVariableCollectionsAsync`, `getLocalVariablesAsync`,
`getLocalPaintStylesAsync`, `getLocalTextStylesAsync`, `getStyleByIdAsync`,
`listAvailableFontsAsync`, `loadFontAsync`, `clientStorage.getAsync/setAsync`
[verified in shipped code, 2026-07; the sync twins are legacy]. [drift-prone — Figma migrates the
API surface; re-check against developers.figma.com at next major feature.]
