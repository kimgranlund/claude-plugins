# Family · Controls — the form-associated, native-replacing components

Every control here **replaces a native form element** with an autonomous, form-associated custom
element. They share one geometry (the button box model in `geometry-system.md`) and one platform
contract (FACE + APG, in `platform-baseline.md`). For each: anatomy → states → role → keyboard →
the embodiment notes that bite. The button is the root — input, select, and menu-item are buttons
with extra parts.

## Button (the root unit)

- **Anatomy** `[ icon? · label? · caret? ]` — the eight permutations and their justification are in
  `geometry-system.md`. Icon-only → square. A button is also the **trigger** of select/menu/popover
  and the **action** in a modal card; design it so its anatomy nests.
- **States** default · hover · focus(-visible) · active/pressed · disabled · loading · (toggle:
  pressed). `:state(pressed)` / `:state(loading)` via `internals.states`.
- **Role** `button` (toggle: add `aria-pressed`). **Not** form-associated for value (it submits
  nothing — `formValue()` returns `null`) but it *is* form-aware: `type="submit"` →
  `internals.form?.requestSubmit()`, `type="reset"` → `form.reset()`.
- **Keyboard** Enter (keydown) **and** Space (keyup; `preventDefault` Space on keydown to stop page
  scroll).
- **Bites** focus isn't free (`tabindex`); ship forced-colors (`ButtonText`/`ButtonFace`); icon-only
  needs the accessible name on the host, not the SVG.

```json
{ "component":"x-button","layer":"component","role":"button","replaces_native":true,
  "parts":["icon","label","caret"],"props":["size","variant","disabled","loading","pressed"],
  "boolean_props":["disabled","loading","pressed"],"states":["pressed","loading","disabled"],
  "keyboard":["Enter","Space"],"forced_colors":true,"owns_outer_margin":false }
```

## Select / combobox (a button trigger + a listbox popover)

- **Anatomy** `trigger` (a button: icon? · value · caret) · `value` · `listbox` · `option` ·
  `option-indicator`. The trigger reuses the button geometry exactly; the listbox is an overlay
  (see `family-overlays.md`) tethered with anchor positioning, sized with `anchor-size(width)`.
- **States** collapsed/expanded · selected · highlighted(active option) · disabled · invalid ·
  placeholder · loading(async).
- **Role** `combobox` on the trigger, `aria-expanded` + `aria-controls`; popup `listbox`; items
  `option` with `aria-selected`. Highlight via **`aria-activedescendant`** (focus stays on the
  trigger), not roving.
- **Keyboard** Down / Alt+Down opens · arrows move the active option · Home/End · type-ahead (≥ 7
  options) · Enter commits · Esc closes → focus returns to trigger. `scrollIntoView` the active
  option manually.
- **FACE** form-associated; `setFormValue(selectedOption.value)`; `setValidity({valueMissing})` for
  `required`; `state` carries the user-visible label for restore.
- **Bites** the big native-parity loss is the **mobile picker** — custom selects on mobile often
  hijack the back gesture; weigh keeping a hidden native `<select>` for touch, or accept the cost
  knowingly. `required` validity doesn't cross shadow roots — compute group state via `getRootNode()`.

```json
{ "component":"x-select","layer":"component","role":"combobox","replaces_native":true,
  "form_associated":true,"validity":true,"parts":["trigger","value","listbox","option","indicator"],
  "props":["size","variant","disabled","invalid","open","required"],
  "boolean_props":["disabled","invalid","open","required"],"states":["open","disabled","invalid"],
  "keyboard":["ArrowDown","ArrowUp","Enter","Escape","Home","End"],"forced_colors":true }
```

## Checkbox & switch

- **Anatomy** `control` (the box/track) · `indicator` (check/thumb) · label is a sibling/slot.
- **States** unchecked · checked · indeterminate (checkbox only, `aria-checked="mixed"`) · disabled ·
  invalid · focus.
- **Role** `checkbox` / `switch`; `aria-checked` via `internals`.
- **Keyboard** **Space toggles** (Enter does **not**).
- **FACE** `setFormValue(checked ? value : null)` — `null` when unchecked so it leaves FormData,
  matching native.
- **Geometry** checkbox/switch (and radio, kbd, slider, tag, badge, chip) are **compact/dense**
  controls — sized on the *separate* two-band compact box ramp (`geometry-system.md` → "The compact /
  dense realm"; `geometry-check.py compact-ramp`), **not** the button height ramp, and they keep the
  compact pad (never the comfortable `h/2`). The indicator still centers in its square cell by the same
  `(box − glyph)/2` law; the toggle's control box is square.

## Radio group

- **Anatomy** `radiogroup` (container) · `radio` (control · indicator) per option.
- **States** selected/unselected · disabled · invalid · focus; exactly one selected.
- **Role** `radiogroup` + `radio`; `aria-checked`.
- **Keyboard** **roving tabindex is mandatory** — one `tabindex=0`, rest `-1`; arrows **move +
  select in one action** and wrap at ends.
- **FACE** the *group* owns the form value; only the checked radio sets it. Cross-root `required`
  validity needs `getRootNode()`.

## Textarea-like / editable

- **Anatomy** `field` (a `contenteditable` surface) · placeholder · count/affordances.
- **Role** `textbox` + `aria-multiline="true"`; `validityAnchor()` points at the editable surface,
  not the host.
- **Bites** you now own caret, undo, paste **sanitization** (Trusted Types if you parse HTML), IME
  composition, and value extraction. This is the most expensive native replacement — justify it.

## Family policy

- One geometry: every control's box is a button box; the indicator/caret is a glyph in a square cell.
- One value protocol: `setFormValue` on first render + change; `null` for empty; `name` required.
- One semantics path: role + ARIA + states via `ElementInternals`; never native elements.
- One a11y floor: APG keyboard for the role, roving-vs-activedescendant chosen deliberately,
  forced-colors shipped, target ≥ 24px.
- Defer the *code* to the repo's component seat (in agent-ui, the `component-builder` agent) or the
  host/`system-builder` agent; this family file locks the **contract**.
