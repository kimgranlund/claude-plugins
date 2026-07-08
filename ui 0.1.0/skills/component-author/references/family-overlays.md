# Family · Overlays — top-layer surfaces, built from the platform, not a JS library

Menus, modal cards, popovers, tooltips, drawers, and toasts are one family because they share a
realization: the **top layer** (Popover API / `<dialog>`), **anchor positioning** for placement, and
a **focus-behavior** spine that separates them. Build them from platform primitives (see
`platform-baseline.md`) — they replace Floating UI, focus-trap libraries, and z-index wars.

## The organizing axis — focus behavior

The whole family sorts by what happens to focus when the overlay opens. Get this right first; it
dictates role, keyboard, and dismissal:

| Focus behavior | Members | Realization |
|---|---|---|
| **Trap** (focus moves in, can't leave, returns on close) | modal card / dialog, modal drawer | `<dialog>.showModal()` — real focus trap + `::backdrop` that blocks the page |
| **Non-modal** (focus may move in, page stays live) | menu, popover, select listbox, non-modal drawer | `popover` attribute (top layer, light-dismiss) + anchor positioning |
| **Never focused** (purely supplementary) | tooltip, toast | `popover=hint` / `role=status`; **never** focusable, no interactive content |

## Modal card (header + body + actions) — the canonical pattern

The component you asked for: a dialog whose content is a header, a message/body, and an actions row.

- **Anatomy** `dialog` · `backdrop` · `header` (title + optional close button) · `body` · `actions`
  (a cluster of buttons; primary trailing). Title/body wire the accessible name/description.
- **States** open/closed · focus-trapped · returning-focus · (alert variant: assertive).
- **Role** `dialog` (or `alertdialog` for destructive confirms); `aria-modal`,
  `aria-labelledby`→header title, `aria-describedby`→body.
- **Keyboard** Tab wraps inside (trap) · Esc closes (`<dialog>.requestClose()` fires a cancelable
  `cancel` for unsaved-changes guards) · focus returns to the invoker.
- **Realization** `<dialog>` + `showModal()` for the true trap; the actions row is a `cluster`
  primitive with `gap` (no per-button margin); the close button and actions are **buttons** — same
  geometry, same family-controls contract. Animate in with `@starting-style` +
  `transition-behavior: allow-discrete`; consider a view transition (gate on `prefers-reduced-motion`).
- **Geometry** the card uses **composed padding**: the dialog's inner padding = the size's `inset`;
  the header/body/actions sections reuse the same `inset`, so their shared edges compose. Buttons in
  the actions row keep their own geometry.

```json
{ "component":"x-modal-card","layer":"pattern","role":"dialog",
  "parts":["dialog","backdrop","header","title","close","body","actions"],
  "props":["open","size","dismissible"],"boolean_props":["open","dismissible"],
  "states":["open"],"keyboard":["Escape","Tab"],"forced_colors":true,"owns_outer_margin":false }
```

## Menu

- **Anatomy** `trigger` (a button) · `content` · `item` / `item-checkbox` / `item-radio` ·
  `item-indicator` · `group` · `label` · `separator` · `submenu`.
- **Role** trigger `button` + `aria-haspopup="menu"` + `aria-expanded`; `menu` + `menuitem(...)`.
- **Keyboard** Enter/Space/Down opens · arrows navigate (**roving** real focus) · Esc closes ·
  type-ahead. (Contrast the select, which uses activedescendant.)
- **Realization** `popover` (non-modal, light-dismiss) + anchor positioning (`position-area`,
  `@position-try` flip on overflow) + `command`/`commandfor` for the declarative trigger.

## Popover (generic non-modal panel)

- **Anatomy** `trigger` · `anchor` (may differ from trigger) · `content` · `close` · `arrow`.
- **Role** non-modal `dialog`; focus *may* leave; Esc closes → focus returns to trigger.
- **Realization** the reference pattern for `popover` + anchor positioning; the `anchor` part lets
  you decouple placement from the trigger.

## Drawer / panel

- **Anatomy** dialog parts + `scrim` · `header` · `container` (side: start/end) · `divider`.
- **The modal/standard fork is load-bearing**: modal drawer = `<dialog>.showModal()` (trap + scrim);
  standard/inline drawer = no trap, no scrim, content stays in flow.

## Tooltip & toast (never-focused)

- **Tooltip** `role="tooltip"`, linked via `aria-describedby`; **never focusable, no interactive
  content**; Esc dismisses; `popover=hint` (Chromium) or a JS-light fallback. Don't put a button in
  a tooltip — that's a popover.
- **Toast** `role="status"` (polite) or `role="alert"` (assertive); `aria-live` + `aria-atomic`;
  must **not** steal focus; cap to one action; don't auto-dismiss an `alert`.

## Family policy

- Build on the **top layer** (`popover` / `<dialog>`), never a hand-rolled z-index stack.
- **Place** with anchor positioning + `@position-try` fallbacks; feature-detect (Baseline Jan 2026)
  and ship the OddBird polyfill or a static fallback.
- **Choose the focus behavior first** (trap / non-modal / never-focused) — it determines everything.
- Triggers, close buttons, and actions are **buttons** from `family-controls.md` — one geometry,
  reused; the overlay never sets outer margins on its children (use `cluster`/`stack` `gap`).
- Animate with `@starting-style` + `allow-discrete`; gate any view transition on
  `prefers-reduced-motion`.
