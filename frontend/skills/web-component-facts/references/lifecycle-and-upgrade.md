# Light-DOM base element + lifecycle: upgrade races, SSR shim scars, NOOP_INTERNALS

A zero-dependency web component's own lifecycle is where most real bugs live, because the
Custom Elements spec's own "upgrade an element" algorithm and a non-browser SSR/test shim
disagree about what already ran by the time `connectedCallback` fires.

## The base shape: light DOM, signals, one render effect

`UIElement extends HTMLElement` — no shadow root, ever. Every declared `static properties` entry
is wrapped as a signal in the constructor (`installProps`); reading/writing the property reads/
writes the signal, optionally reflecting to the matching attribute [verified,
`core/element.js:31-65`, read 2026-08-20]. `connectedCallback` registers exactly one effect that
touches every prop signal, calls `ctor.template(this)` if declared, `stamp()`s the result, then
calls the instance's own `render()` [verified, `core/element.js:227-241`]. `disconnectedCallback`
tears the whole thing down symmetrically: disposes stamped parts, runs every effect's cleanup,
clears ad-hoc signals, disconnects traits and the controller [verified, `core/element.js:248-261`].
This is rule 1/2 of the ratified doctrine: light DOM is the load-bearing substrate (no
`attachShadow()` without a superseding ADR + major bump), and reactivity is fine-grained signals,
no virtual DOM [verified, `04-doctrine-vs-practice.md` Part 1 rules 1-2].

## The upgrade race: connectedCallback fires, attributeChangedCallback doesn't replay

The spec's "upgrade an element" algorithm (§4.13.5 step 6) requires replaying
`attributeChangedCallback` for every attribute already present on an element BEFORE
`connectedCallback` fires — several DOM shims used for SSR (linkedom) and this repo's own
`happy-dom` test environment skip that replay [incident, `core/element.js:161-169`, confirmed
directly by `element.test.js`'s "SSR attribute-upgrade replay (gh#284)" case]. Left unfixed, any
reflected property whose only value came from server-rendered or pre-parsed HTML is silently stuck
at its class default — `<nav-item-ui text="Profile">` renders an empty label. The fix re-syncs
every declared property from its live attribute inside `connectedCallback` itself (which fires
reliably everywhere), run entirely `untracked()` — `connectedCallback` commonly fires synchronously
inside a PARENT's render effect (a template engine appending children during `stamp()`), and a
tracked read there would subscribe the parent's effect to the child's signals, producing the
unbounded parent↔child oscillation the signals drain-loop guard traps (the admin-settings/
switch-ui/button-ui loop, gh#961) [verified, `core/element.js:170-215`]. A true-default reflected
Boolean gets a narrower, deliberately scoped stamp of its own for the same reason — reflecting
string/number defaults too would flip `[attr]` CSS gates framework-wide and cascade into the same
drain-loop guard [verified, `core/element.js:194-213`, gh#961].

## NOOP_INTERNALS — the single highest-leverage SSR crash site

An unconditional `this.attachInternals()` call in the constructor threw BEFORE any subclass code
ran under a DOM shim with no real ElementInternals implementation (linkedom and similar SSR
passes) — the single highest-leverage crash site in the whole framework under SSR, because it
fired before any per-consumer `.setValidity()`/`.setFormValue()` call could even be reached
[incident, `core/element.js:140-152`, gh#285]. The fix is a frozen no-op shim
(`NOOP_INTERNALS`) whose surface matches exactly what the framework's own consumers call
(`setFormValue`, `setValidity`, `checkValidity`, `reportValidity`, `form`, `labels`, `validity`,
`validationMessage`, `willValidate`) — feature-detected in the constructor
(`typeof this.attachInternals === 'function' ? this.attachInternals() : NOOP_INTERNALS`)
[verified, `core/element.js:67-85, 150-152`]. Form participation is meaningless server-side (no
live user interaction to validate), so every call site keeps working as an inert no-op instead of
throwing on a missing method — the same feature-detect-and-no-op pattern repeats for
`adoptedStyleSheets` (linkedom's `document` has none; styles matter for paint, which doesn't
happen server-side) [verified, `core/element.js:96-108`, gh#285].

## Practical guidance

- **A base element's constructor is not a safe place for an unconditional platform-API call** —
  feature-detect anything an SSR/test shim might not implement (`attachInternals`,
  `adoptedStyleSheets`) and substitute an inert no-op whose surface matches every real call site,
  rather than letting the crash migrate downstream to the first consumer.
- **Never trust `attributeChangedCallback` alone for initial state under a shim-based
  environment** — re-sync every declared property from its live attribute inside
  `connectedCallback`, wrapped in `untracked()`, since that hook fires reliably everywhere the spec
  replay does not.
- **A reflected default that must stamp its own attribute on first connect is a narrow, scoped
  exception (true-only Booleans)**, not a general "reflect every default" policy — the general
  policy cascades into the same render loop it's trying to avoid.

## Boundary

This file covers the base element's OWN lifecycle mechanics — construction, connect/disconnect,
attribute/property sync, and the SSR-shim scars that lifecycle carries. Stamping the CHILD tree
(which strategy, keyed reconcile) is `stamping-and-reconcile.md`; form-specific `ElementInternals`
usage (validity, form association) is `form-and-a11y.md`.
