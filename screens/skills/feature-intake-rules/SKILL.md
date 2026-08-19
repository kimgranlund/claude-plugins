---
name: feature-intake-rules
description: >-
  Per-shape intake schemas for a UI feature ticket — component/module, layout/shell, UX flow,
  cross-cutting UX — fields lifted from the owning build skill's own two-plane axes, each naming
  its build owner and DoD checker. Use when capturing/reviewing what a UI-feature TICKET should
  state before build: "what fields does a button component ticket need", "what should a
  dashboard-shell ticket capture", "is this UI ticket capture-complete". NOT building/grading the
  component/layout/flow itself (make-component, break-down-layout, break-down-flow); NOT general
  feature intake (docs:file-feature, which consults this pack); NOT visual/token seeds
  (design:token-feature-intake-rules).
disable-model-invocation: false
user-invocable: false
---

# feature-intake-rules — per-shape UI ticket intake schemas

4 declared shapes (pack-writing-rules' 3-7 threshold), flat consult table below, no
`references/INDEX.md` — the table IS the retrieval map. Every schema field is LIFTED verbatim
from its owning build skill's own two-plane axes (cited by path, never restated) — this pack owns
WHAT A TICKET MUST CAPTURE, never how the build itself is executed.

## Both-planes capture-completeness rule

A UI feature ticket is capture-complete only when both plane columns carry an answer or a named
open fork. Single-plane capture ships the known failure quadrants: outside-in-only ("looks clean
but nothing does anything"), inside-out-only (orphan components).

## Consult table

| Shape | Load | Owning axes | Build owner | DoD checker |
|---|---|---|---|---|
| Component / module | `references/component-module.md` | `make-component`'s Compose × Realize | `make-component` | `component-checker` |
| Layout / shell | `references/layout-shell.md` | `break-down-layout`'s OUTSIDE-IN × INSIDE-OUT | `break-down-layout` (DESIGN mode) | `layout-checker` |
| UX flow | `references/ux-flow.md` | `break-down-flow`'s task → journey × transitions → whole | `break-down-flow` | `flow-checker` |
| Cross-cutting UX (motion/focus/i18n) | `references/cross-cutting-ux.md` | the named owner's own budget vocabulary | `motion-rules` / `check-focus` / `check-translations` (answers-only for motion, card-gated for the other two) | `check-focus` / `check-translations` (motion-rules is answer-only — no DoD gate) |
| Worked examples | `references/fixtures.md` | — | — | — |

## How to use it

1. **Classify the seed's shape** against the table above — a raw idea, a `file-feature` intake in
   progress, or an existing ticket being reviewed for completeness. One ticket may span more than
   one shape (a ticket introducing both a new component AND the shell that hosts it); capture each
   shape's own grid.
2. **Fill the grid**, both plane columns, per shape file — an unanswered cell is a named open
   fork, never a silent gap (the both-planes rule above).
3. **Stamp the ticket's own scope: frontmatter** with the shape's `build-owner` and `dod-checker`
   values from the table — so `dispatch-ticket` routes the build against the same owner this
   schema names, and the checker it dispatches at DoD is the same checker this schema names
   (invariant below).
4. **These same fields double as the pre-fork grill's fork menu** for big seeds (gh#654) — the
   grill's own step picks the highest-leverage unanswered cells (2 structural + 2 mechanism) from
   this same grid; one artifact, never two drifting lists.
5. **`docs:file-feature`'s classify step consults this pack** by soft named mention for any
   component/layout/flow/cross-cutting-shaped seed — this pack never invokes `file-feature`, only
   the reverse.

## Core invariants

- **(a) Both-planes capture-completeness** — stated above, verbatim, shared with
  `design:token-feature-intake-rules`.
- **(b) Fork-menu reuse** — these schema fields double as gh#654's pre-fork grill fork menu; one
  artifact, never two drifting lists.
- **(c) Scope/owner/checker geometry** — the ticket records `scope:`, the named build owner, and
  the pre-named DoD checker so capture → build → verify speak one geometry.
- **(d) No duplication** — no new agents (IDR-0007's bar — the checkers already exist), no
  procedure duplication (every schema field cites its owning skill's own axis, never restates it —
  doctrine-audit safe), no hooks (gh#466).

## Composition

- **`screens:make-component` / `break-down-layout` / `break-down-flow`** — the owning build skills
  this pack's schemas cite for their axis definitions; soft in-plugin citation, never a preload,
  never a restatement of the axis doctrine itself.
- **`screens:component-checker` / `layout-checker` / `flow-checker`** — the DoD checkers each
  schema names; reached at build-verify time, never invoked by this pack.
- **`screens:check-focus` / `check-translations` / `motion-rules`** — the cross-cutting concern
  owners `references/cross-cutting-ux.md` cites for its own budget vocabulary.
- **`docs:file-feature`** — the procedural intake this pack is consulted FROM (soft cross-plugin
  mention, degrades gracefully where `screens` isn't installed); this pack never restates
  `file-feature`'s own classify/dedup/size procedure.
- **`design:token-feature-intake-rules`** — the sibling pack for token/palette/typography seeds;
  disjoint domain, no citation between the two (each cites `file-feature` independently).

Extension: governed by [[make-pack]].
