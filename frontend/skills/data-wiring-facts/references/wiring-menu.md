# The six-pattern need→pattern wiring menu, and the Wiring Record gates

Source: `gen-ui-kit` `.claude/docs/reports/2026-08-20-reactivity-review/04-doctrine-vs-practice.md`
Part 2 — reporting the ratified taxonomy at
`packages/plugins/adia-ui-factory/skills/data-wiring/SKILL.md` (menu: "signals · Service/Command ·
DataClient · property-API · data-*"), with code shapes at
`packages/plugins/adia-ui-factory/references/data-and-hydration.md`. All claims [verified] against
the doctrine report unless marked otherwise.

## Six patterns, need → pattern

| # | Need | Pattern | Doctrine detail |
|---|---|---|---|
| 1 | Reactive local UI state | **signals** — `signal()`/`effect()` | Fine-grained, no vDOM; effect auto-cleans on disconnect |
| 2 | CRUD with mutations + undo | **Service / Controller / Command** | Service is async from day one; Controller orchestrates signals + service; Commands record patches for undo |
| 3 | Typed reads from a backend/corpus | **DataClient + mappers** | UI reads typed projections only; the pure mapper is the fixtures⇄API swap seam; every mutate call REQUIRES attribution (an `action_source`-shaped field) — the client throws without it |
| 4 | Populate a catalog component (table/select/chart) | **property-API** | `el.columns = […]`, `el.data = rows`, `el.options = opts` — NOT post-connect appended children |
| 5 | Static/declarative flow state | **`data-*` + CSS** | State is CSS: a data attribute on a container plus a matching attribute selector toggling display |
| 6 | Live/shared data into a settable-`.data` element | **`data-stream-*` trait** | Signal-backed, refcounted shared transports; fully declarative; SSR-inert (this pack's own `streaming-stack.md` is the full axis on pattern 6) |

Picking the wrong pattern for a need is itself a defect this menu exists to prevent — e.g.
populating a catalog component by appending `<option>` children post-connect instead of assigning
`el.options` (pattern 4's own named anti-pattern), or reaching for a full Service/Controller/Command
stack for state that's really just reactive local UI (pattern 1's territory, over-engineered into
pattern 2's). [verified]

## Hydration per rendering mode

| Context | Path |
|---|---|
| SPA static host | Surface self-boots — fetch in `connected()`, a `#booted` guard against double-fetch |
| SSR framework | Server fetch → initial props → client refresh; registration is client-only; cross-cutting state lives in cookies/session, never component-lifetime signals |
| Hybrid (SPA island in an SSR page) | Server-seeded props → client-boot island; the island owns its own state + in-island routing |

[verified] — doctrine report, citing the ratified skill's own hydration section.

## The Wiring Record gates — what "done" means for one state piece

Source: doctrine report Part 2, "Ownership rules (the Wiring Record gates, SKILL.md L61–103)".
A Wiring Record is the ratified deliverable per state piece: one row per piece of state, complete
only when every gate below holds AND the round-trip has been OBSERVED, never merely assumed.
[verified]

- **Single owner per piece of state.** A shadow copy is a defect. The owner must be a *named*
  file/component/route — never "shared" as the stated owner.
- **Exactly one route owner per scope.** Never a framework router AND a component-level router
  both owning navigation on the same scope.
- **Projections-only.** A direct backend call, or a per-view reshape of an existing projection,
  bypassing pattern 3's mapper seam, is a defect.
- **Data down, events up.** Sub-components receive state via properties and emit CustomEvents;
  reaching into a parent's internals from a child is a defect.
- **One reactive path.** Running a parallel CustomEvent-only state channel beside signals for the
  same piece of state is a defect — updates flow through one mechanism, not two competing ones.
- **Sibling-safe user state.** A user-set control is never auto-reset by an unrelated sibling's
  own change.
- **Shared detail drawer.** One drawer instance per collection, hydrated per-row via a `hydrate`
  event — N drawer instances for N rows is a defect (a specific instance of the single-owner rule,
  named separately because it recurs often enough to earn its own line).
- **Four states per data region.** Default / loading / empty / error, all wired — a region missing
  any of the four is unfinished, not merely imperfect.
- **The deliverable itself.** One Wiring Record row per state piece; "done" means every row is
  complete AND the round-trip has been observed running, never assumed from reading the code.

## Applying the menu

Classify the need first (which of the six rows it matches), then check the resulting wiring
against every applicable gate above — a correctly-chosen pattern can still fail the Wiring Record
gates (e.g. pattern 3's DataClient reads chosen correctly, but two different views both reshape
the same projection independently, violating projections-only). The pattern choice and the gate
check are two separate steps, not one.
