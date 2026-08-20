# ElementInternals form association + a11y

No native form controls — the ratified rule is unconditional: the host custom element IS the
interactive surface, via `ElementInternals` for form participation/validation and explicit ARIA +
APG keyboard for accessibility; the single named exception is `<input-ui type="password">`
[verified, `04-doctrine-vs-practice.md` Part 1 rule 21, ADR-0025/ADR-0055]. This file covers what
that looks like concretely, and the constraint-validation lifecycle riding on top of it.

## `UIFormElement`: the shared form-participation base

`static formAssociated = true` plus a shared property set (`name`, `value`, `disabled`, `required`,
`readonly`, `error`, `hint`, `pattern`, `minlength`, `maxlength`, `throttle`) makes any subclass
form-associated with zero per-control boilerplate [verified, `core/form.js:46-72`]. The
`ElementInternals` accessors (`form`, `labels`, `validity`, `validationMessage`, `willValidate`,
`checkValidity()`, `reportValidity()`) are thin pass-throughs to `this.internals`
[verified, `core/form.js:83-90`] — the same `this.internals` the base `UIElement` constructor
already populated with either a real `attachInternals()` result or `NOOP_INTERNALS` under an
SSR shim (see `lifecycle-and-upgrade.md`). `UIFormElement` subclasses MUST call
`super.connected()`/`super.disconnected()` — a documented anti-pattern names the specific failure
mode (form participation silently fails) when a subclass forgets [verified,
`lifecycle-patterns.md` §"Anti-patterns to watch for"; `04-doctrine-vs-practice.md` Part 1 rule 21].

### The constraint engine

`syncValue(val)` calls `internals.setFormValue(val)` then runs `#runConstraints` — a plain
if-chain checking `required` (empty-after-trim), `pattern` (via `new RegExp`, wrapped in a
try/catch so a malformed pattern doesn't throw), `minlength`, `maxlength`, each calling
`internals.setValidity({...flag}, message, anchor)` on failure and `internals.setValidity({})` on
success [verified, `core/form.js:94-99, 207-253`]. `validate()` re-runs constraints and toggles
`aria-invalid` + the reflected `error` property to match [verified, `core/form.js:117-128`].
Auto-validation wires three listeners in `connected()`: `invalid` (browser-fired on submit,
`preventDefault` + set `aria-invalid`), `input` (re-validate only if currently invalid, so a user
mid-correction isn't nagged before they finish), `blur` (validate only if the field is dirty)
[verified, `core/form.js:255-279`] — each has a matching `removeEventListener` in `disconnected()`
[verified, `core/form.js:311-319`], the symmetric-lifecycle rule (`04-doctrine-vs-practice.md` Part
1 rule 17) applied specifically to the form auto-validation wiring.

Custom error messages read from `data-msg-{constraint}` attributes on the host
(`data-msg-required`, `data-msg-pattern`, `data-msg-minlength`, `data-msg-maxlength`, plus
subclass-specific siblings like `data-msg-min`/`data-msg-max`) — this whole family is deliberately
EXEMPT from the component's own yaml `states:`/`props:` declaration, since it's shared
component-side config read by one mixin across 7+ consuming components, not a per-component state
or prop [verified, `core/form.js:24-35`, ADR-0060 §Decision 3]. See `attributes-as-api-grammar.md`
for the yaml-as-SoT rule this is a named, ratified exemption from.

## The host-as-control pattern, concretely: `<check-ui>`

A checkbox with zero native `<input>` anywhere: `connected()` sets `role="checkbox"` and
`tabindex="0"` explicitly, wires `click` and `keydown` handlers itself
[verified, `components/check/check.class.js:38-44`]. `render()` derives `aria-checked` (three-way:
`"mixed"` for indeterminate, else the string-coerced boolean), `aria-disabled`, and `aria-label`
(from the `label` property — kept as the accessible name even when the visible text is suppressed
via `labelHidden`, so a composition that shows the name elsewhere doesn't lose it for
screen-reader users) [verified, `components/check/check.class.js:46-54`, gh#1010]. Keyboard
activation follows APG directly: Space and Enter both `preventDefault` then toggle
[verified, `components/check/check.class.js:65-67`] — the same Space/Enter-to-activate contract
`traits-primitive.md`'s `pressActivation` trait formalizes as a reusable unit in agent-ui rather
than hand-rolling it per control. `syncValue(this.checked ? (this.value || 'on') : '')` feeds the
checked state into the shared form-value/constraint machinery every `render()` pass
[verified, `components/check/check.class.js:55`].

## A11y primitives beyond the single-control case

- **Attribute honesty and reserved-name anti-patterns** apply to accessible-state naming too: no
  `title` (use `heading`), no `active` on parent components (use `value`/`step`), `error` is
  reserved for validation state, `disabled` only appears on form-participating components
  [verified, `04-doctrine-vs-practice.md` Part 1 rule 16] — this keeps a screen-reader-relevant
  attribute meaning one thing across the whole component set.
- **APG keyboard beyond Enter/Space** (arrow-key roving tabindex, typeahead, focus trap) is traits
  territory in both repos — `roving-tabindex`/`typeahead`/`focus-trap`/`arrow-grid-nav` in
  gen-ui-kit's trait barrel, `roving-focus.ts`/`tabbable.ts` in agent-ui's — see
  `traits-primitive.md` for the shared shape these compose through, rather than each form control
  reimplementing arrow-key handling inline.

## Practical guidance

- **A value-bearing custom element is form-associated via `ElementInternals`, never a wrapped
  native `<input>`** — the single sanctioned exception is a genuine password field, where the
  platform's own credential-manager integration only recognizes a real `<input type="password">`.
- **Constraint validation is a small, explicit if-chain against `internals.setValidity()`**, not a
  hidden native form's own validation — write custom messages via `data-msg-*` attributes read by
  the shared mixin, not a per-component prop.
- **ARIA state (`role`, `aria-checked`/`aria-disabled`/`aria-label`, `aria-invalid`) is set
  explicitly in `render()`/`connected()`**, derived the same way any other reflected state is —
  there's no shadow-DOM ARIA delegation to lean on since there's no shadow root at all.

## Boundary

This file covers form participation (`ElementInternals`, constraint validation) and the concrete
a11y wiring a form-associated or interactive host element carries. The base element's construction
and connect/disconnect lifecycle generally is `lifecycle-and-upgrade.md`; the closed event
vocabulary and attribute-naming rules a form control's own API surface follows is
`attributes-as-api-grammar.md`; reusable keyboard/interaction behavior units (roving tabindex,
focus trap, press activation) are `traits-primitive.md`.
