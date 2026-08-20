# Platform baseline — the no-framework, no-native-control surface (June 2026)

The Realize axis (B2–B5) rests on platform primitives that all crossed into **Baseline** in the last
~18 months, which is *why* a zero-dependency, signals-reactive, no-native-form-element library is
finally viable. This file is the catalog: what to use, what it gives you, what bites, and the
honest **native-parity budget** for replacing native controls.

Idiom note: the reference libraries (`fable-tests/reactive-components`, `adia/gen-ui-kit`) both use a
signals core (`signal` / `computed` / `effect`), a `UIElement` / `UIFormElement` base, **light DOM by
default**, `@scope` CSS + custom-property token ramps, and `ElementInternals` for semantics. Match it.

## B2 · The element

- **Autonomous custom elements only.** Never customized built-ins (`extends`+`is=""`) — WebKit
  formally opposes them and will not ship them; they are not Baseline and won't be. Recover the
  semantics a native element would have given through `ElementInternals`, not the parser.
- **Constructor is restricted**: `super()` first; don't touch light-DOM attributes/children; defer
  that to `connectedCallback`. A throwing constructor silently downgrades to `HTMLUnknownElement`.
- **`attributeChangedCallback` only fires for `static observedAttributes`** — the #1 "my handler
  never runs" bug. In the signals idiom, reflected props *are* signals; reading one in a `computed`
  / `effect` tracks it, and the effect dies with the connection scope (no leaks on disconnect).
- **Light DOM is the default** in both reference libraries: page CSS, native ARIA association, and
  forms "just work," and SSR is trivial. Reach for an **open** shadow root only when you need style /
  DOM encapsulation; never *closed* (no security benefit, breaks tooling and a11y).

## B3 · Semantics & form participation (FACE)

This is the core of "no native form elements." A custom control earns form behavior through
**Form-Associated Custom Elements** + `ElementInternals` (Baseline since March 2023):

- `static formAssociated = true`; `this.internals = this.attachInternals()` once, in the constructor.
- **`internals.setFormValue(value, state?)`** — submitted under the element's `name` (no `name` →
  nothing submits, ever). Call it on **first render *and* every change**; pass `null` (not `""`) for
  empty. `state` is the user-facing value restored to `formStateRestoreCallback` on bfcache/autofill.
- **`internals.setValidity(flags, message?, anchor?)`** — flags are booleans (`valueMissing`,
  `customError`, …); there is no `valid` flag (valid = no flags); a `message` is mandatory when any
  flag is true; `anchor` must be a shadow-including descendant. **Render your own error UI** — Chrome
  doesn't show the native validation bubble for FACE.
- **ARIA via `internals`** (`internals.role`, `internals.ariaChecked`, `internals.ariaExpanded`, …)
  sets the element's *default* semantics — attribute-free, SSR-safe, author-overridable. Custom
  states: `internals.states.add('open')` → CSS `:state(open)`.
- Form lifecycle: `formDisabledCallback` (fires for an ancestor `<fieldset disabled>`, **not** the
  element's own `disabled`), `formResetCallback`, `formStateRestoreCallback`.
- **Element-reference ARIA** (`internals.ariaActiveDescendantElement`, `ariaLabelledByElements`) is
  the fix for cross-root associations but is **not fully Baseline** (Firefox lags) — feature-detect,
  or keep related ARIA inside one root.

## B4 · Interaction — APG contract + the native-parity budget

Keyboard + focus per the **WAI-ARIA Authoring Practices Guide**, per role. The cheap 20% is the
keyboard map; the expensive 80% is everything native gave you for free. **Budget for it explicitly —
this is a B4 review item, and `component-contract-check.py` gates the two that silently kill
controls (a missing role/keyboard and missing forced-colors).**

What you must rebuild when you drop the native control:
- **Focus**: a bare custom element still needs `tabindex`; choose **roving tabindex** (radios, tabs,
  menus, simple listboxes — gives free `:focus`, auto-scroll, reliable mobile SR) vs
  **`aria-activedescendant`** (comboboxes/command palettes where focus must stay in a text input — but
  then `:focus` won't match the active option, `scrollIntoView` is manual, mobile SR support is weak).
- **Forced colors / Windows High Contrast** — the most-cited custom-control failure. ARIA roles get
  *no* system colors, so a `div[role=button]` loses its boundary. Ship `@media (forced-colors:
  active)` with system color keywords (`ButtonText`/`ButtonFace`, `Canvas`/`CanvasText`,
  `Highlight`/`HighlightText`, `GrayText`, `AccentColor`) for **every** control. *(Gate.)*
- **The free stuff you forfeit and must replace or accept losing**: `<label>` click-to-focus + hit
  area, autofill / password managers (custom controls generally can't be autofilled — a real loss),
  the native mobile picker (custom selects on mobile often hijack the back gesture), IME /
  dictation / voice control, native validation UI, `inputmode` virtual keyboards, print styles, the
  OS focus ring.
- **WCAG 2.2 floors**: visible focus not obscured (2.4.11), target size ≥ 24×24 CSS px (2.5.8 — the
  44px figure is AAA/HIG, not the AA floor), non-text contrast ≥ 3:1 (1.4.11), honor
  `prefers-reduced-motion`.

Per-role minimums (the gate's table): button → Enter+Space (`preventDefault` Space on keydown);
checkbox → Space (not Enter); radiogroup → arrows move+check, roving; listbox → arrows+Home/End,
type-ahead ≥ 7; combobox → Down opens, Esc closes, Enter commits, activedescendant; menu → arrows +
Esc; tablist → Left/Right; dialog → Esc + focus trap + return focus.

## B5 · Fidelity — SSR, theming, icons, the non-Baseline edge

**SSR.** Declarative Shadow DOM (`<template shadowrootmode="open">`, Baseline since Feb 2024) renders
a shadow tree with zero JS. Hydrate by **adopting, not recreating**:
```js
let root = this.internals?.shadowRoot ?? this.shadowRoot;   // DSD root if present
if (!root) root = this.attachShadow({ mode: "open" });      // CSR fallback
```
(`attachShadow` on an existing declarative root silently empties it — guard with the check.) Inline
`<style>` for first paint, swap to a shared `adoptedStyleSheets` on upgrade; add `:not(:defined){
visibility:hidden }` against FOUC. **Light-DOM SSR** (the Enhance model, and both reference libs'
default) sidesteps the unsolved "shared stylesheet per declarative shadow root" payload-bloat problem
— prefer it unless you need encapsulation.

**Theming surface.** CSS custom properties (the primary API) + `::part` / `exportparts` + custom
`:state()`. You can't select *descendants* of a part, so give every styleable element its own `part`.
Wrap **all** library CSS in `@layer` so consumers override with plain unlayered CSS — no specificity
wars. Avoid `:host-context()` (Chromium-only, deprecated). `adoptedStyleSheets` is Baseline.

**Icons.** Default to **inline SVG rendered into the component's own tree** with `width/height: 1em`
+ `currentColor` — `<use href>` sprites **cannot reliably cross a shadow boundary** (a known
show-stopper), so never use them inside shadow-DOM components. `mask-image` is fine for *monochrome
chrome only*. Icons are **decorative by default** (`aria-hidden="true"`, `focusable="false"`); put
the accessible name on the host control, not the SVG.

**Modern layout primitives** (use freely; all Baseline): `@layer` (2022), container size queries
(2023, the self-responsive pattern: `:host{container-type:inline-size}` + `@container`), `:has()`
(2023), subgrid (widely available 2026), `::part` + `:state()`. Container **style** queries reached
Baseline only May 2026 — verify your floor.

**The progressive-enhancement edge** (feature-detect with `@supports`; degrade, don't depend):

| Feature | Status (mid-2026) | Use for | Fallback |
|---|---|---|---|
| **Popover API** (`popover`, `command`/`commandfor`) | Baseline Jan 2025; invoker commands ~Dec 2025 | menus, dropdowns, dialogs, tooltips — top layer, light-dismiss, focus, no JS | `popovertarget` + OddBird popover/invoker polyfill |
| **Anchor positioning** (`anchor()`, `position-area`, `@position-try`) | Baseline Jan 2026 (advanced surface uneven) | tethering overlays to a trigger — replaces Floating UI | `@supports` + static placement + OddBird polyfill |
| **View Transitions** same-doc | Baseline Oct 2025 | state changes, list reorder | none needed; gate on `prefers-reduced-motion` (not auto-suppressed) |
| **View Transitions** cross-doc (`@view-transition`) | **not** Baseline (Firefox partial) | MPA/SSR page nav | normal navigation |
| **Element-reference ARIA** (`ariaActiveDescendantElement`…) | **not** fully Baseline (Firefox lags) | cross-root ARIA | keep ARIA in one root; feature-detect |
| `popover=hint`, scroll-state queries | Chromium-only | tooltips, stuck-state | enhancement only |

**Animating popovers/dialogs in:** a plain `transition` won't animate top-layer entry — use
`@starting-style` + `transition-behavior: allow-discrete`.

## The 10-point platform policy checklist

1. Autonomous elements only; recover semantics via `ElementInternals`, never customized built-ins.
2. Every control is form-associated; `setFormValue` on first render + every change; a `name`; `null`
   for empty.
3. Default ARIA via `internals` (SSR-safe, overridable); treat element-reference ARIA as non-Baseline.
4. Full APG keyboard + focus per role; pick roving tabindex unless focus must stay in a text input.
5. Ship `@media (forced-colors: active)` for every control — or it disappears in High Contrast.
6. `setValidity` + your own error UI (Chrome won't show the native bubble for FACE).
7. Light DOM by default; open shadow only when you need encapsulation; never closed.
8. Theming = custom properties + `::part`/`:state()`, all wrapped in `@layer`.
9. Inline SVG in-tree for icons (never `<use>` across shadow); decorative by default; name the host.
10. Feature-detect the edge (anchor positioning, cross-doc VT, element-ref ARIA); degrade gracefully.
