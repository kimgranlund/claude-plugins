# Stamping strategies + keyed reconcile: adopt-or-stamp, logicalChildren, the display:contents trap

A component has to put children on the DOM somehow, and the ratified doctrine names exactly three
strategies, picked by how the child tree changes over the component's lifetime — mixing per child
tree is sanctioned, mixing WITHIN one child tree is not [verified, `04-doctrine-vs-practice.md`
Part 1 rule 19].

## The three strategies

| Strategy | Fits when | Mechanism |
|---|---|---|
| `static parts` + `ensure(slot)` | Structure is fixed — the same named slots exist for every instance | `ensure()` returns an existing `[slot="X"]` child if present, else clones the class's `static parts` blueprint and appends it [verified, `core/element.js:381-394`] |
| `html\`\`` tagged template | Reactive scalar content, structure can vary by expression | `stamp()`/`mount()`/`update()` in `core/template.js` — see below |
| Imperative `createElement` | Dynamic-length lists, SVG, state-preserving diffs | Hand-written child management, no shared infrastructure |

`ensure()` carries its own invariant (FEEDBACK-31): call it from `render()`, never cache its result
once in `connected()` — a consumer that replaces the host's children (`el.innerHTML = …`) wipes
stamped parts, `render()` re-stamps them, but a reference captured once in `connected()` is left
pointing at detached DOM. Part identity does not survive a host child-list wipe [verified,
`core/element.js:369-380`].

## Adopt-or-stamp — slot content is the source of truth

Every slot-bearing primitive that exposes BOTH an attribute and a slot for the same logical
content (`text=` + `<span slot="text">`) follows one policy: `connected()` either adopts the
consumer-authored slotted child or stamps a new one, tagging it `data-{component}-stamped`;
`render()` may only mutate or remove elements carrying that stamp — an unstamped slotted child is
consumer-owned and stays untouched even when the matching attribute is empty [verified,
`lifecycle-patterns.md` §"Adopt-or-stamp", ADR-0010]. The failure this prevents is concrete and
measured: a 13-page audit found 73 slot uses where the slotted form was the only way to author the
intended content, with the destructive `render()` (overwriting `textContent` from the attribute,
or hiding the slot element when the attribute was empty) confirmed in 3 primitives before the
policy landed [incident, `lifecycle-patterns.md` §"Adopt-or-stamp", ADR-0010]. The same mechanism
governs every composition slot a stamp builds, not just the primary one — e.g. `slot="caret"`, the
one disclosure-indicator slot standardized across `tree-item-ui`/`pane-ui`/`accordion-item-ui`/
`nav-group-ui`/`select-ui`: honor a declarative `<… slot="caret">` child if present, else stamp
`<icon-ui slot="caret" name="caret-right">` [verified, `lifecycle-patterns.md` §"slot=\"caret\"",
ADR-0036].

## The `display:contents` trap — on CSS selectors AND on the JS side

The template engine wraps every `${expr ? html\`…\` : null}` conditional render in a
`<span style="display:contents" role="presentation">` housekeeping node
[verified, `core/template.js:430-445`] — layout-transparent (children take its place in the
parent's flex/grid), but still a real DOM node to any CSS selector or JS traversal that doesn't
know to look past it.

- **CSS side.** A direct-child-combinator slot selector (`:scope > [slot="description"]`) misses a
  conditionally-rendered slotted child, because the actual parent-of-the-slotted-element is now the
  wrapper span, not the host. Surfaced 2026-05-25 via `list-item-ui` slot misses; closed by a
  substrate-wide sweep converting 85 selectors across 12 components from direct-child to descendant
  combinator for slot selectors specifically (anatomy-marker selectors keep direct-child — a
  different rule, `attributes-as-api-grammar.md`) [incident, `component-implementation-patterns.md`
  §"the display:contents wrapper trap", v0.1.2, commit `464477598`].
- **JS side.** Reading projected children via `this.children` or the same
  `:scope > [slot=…]` shape has the identical blind spot in code, not just CSS — both miss
  template-conditional output behind the wrapper (gh#1301). The fix is `logicalSlotted(host,
  slotName)` / `logicalChildren(host)`, which pierce `display:contents` + `role="presentation"`
  wrapper spans and stop at a nested same-tag component boundary — already used by `tree-ui`,
  `select-ui`, `option-card-ui`, `input-ui`'s leading/trailing affordances, `agent-artifact-ui`,
  and `modal-ui`'s heading fallback [verified, `04-doctrine-vs-practice.md` Part 1 rule 25;
  `component-implementation-patterns.md` §"The same trap on the JS side"]. A read that's provably
  self-stamped-only (never consumer-slotted) doesn't need the pierce — mark it
  `// wrapper-trap-ok: <reason>` instead of converting it, per the repo's own
  `audit-wrapper-trap.mjs` convention [verified, `component-implementation-patterns.md`
  §"logicalSlotted/logicalChildren"].

## Keyed reconciliation — three parallel mechanisms for the same job

`UIElement.reconcile(parent, items, keyFn, stampFn)` keys a diff against a per-parent key map: skip
duplicate keys, reuse-and-restamp an existing keyed element or create one, remove keys no longer
present, then walk the new order back-to-front doing minimal `insertBefore` moves
[verified, `core/element.js:416-439`]. The template engine's `repeat()` directive does the
equivalent job for tagged-template components against its own `KEY_MAP`
[verified, `core/template.js:519-556`]. A field-report audit of the same codebase names this
directly as an inconsistency worth flagging: keyed `reconcile()`, template `repeat()`, and outright
hand-rolled loops are "the same job, three list mechanisms," with the package's single largest
list renderer using none of the shared infrastructure [verified, cited via
`reactivity-facts/references/below-element-reactivity.md`, itself sourced from
`01-primitives-reactivity.md` §"Inconsistencies worth flagging"].

## Practical guidance

- **Pick the stamping strategy by how the child tree changes, not by habit** — a fixed skeleton
  wants `static parts`, reactive scalar content wants a tagged template, a dynamic-length or
  state-preserving list wants imperative control. Mixing across different child trees in the same
  component is fine; mixing within one child tree is the anti-pattern the doctrine names.
- **Any selector or JS read touching a SLOT (not an internal anatomy marker) must assume a
  `display:contents` wrapper might sit between host and child** — descendant combinator in CSS,
  `logicalSlotted`/`logicalChildren` in JS, never the direct-child/`.children` shortcut.
- **A dual attribute+slot API needs the stamp-tag discipline from day one** — retrofitting it after
  real consumer content has already been silently destroyed is the expensive way to learn the rule.

## Boundary

This file covers how a component's own CHILD TREE gets created, updated, and torn down — the
strategies, the slot-vs-conditional-wrapper trap, and keyed diffing. The base element's OWN
lifecycle (construction, connect/disconnect, attribute sync) is `lifecycle-and-upgrade.md`. WHY a
per-part effect re-runs, or which reactive clock is driving the re-stamp, is reactivity MECHANISM —
`reactivity-facts`' law, not this pack's (see this pack's own SKILL.md Boundaries section).
