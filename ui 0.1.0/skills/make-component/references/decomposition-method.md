# The two-axis method — COMPOSE × REALIZE

A component is **correct on two independent axes that walk the same hierarchy in opposite
directions** — the same outside-in / inside-out seam [[break-down-layout]] applies to space,
here applied to a building-block component.

- **Compose · whole → part** grades the **abstraction**: the layer it sits at → its anatomy (named
  parts) → its API surface → how it composes upward → its coherence with the rest of the library.
  *"Is it the right component, shaped to compose?"*
- **Realize · part → whole** grades the **embodiment**: its exact geometry → the custom element →
  its platform semantics (ARIA/FACE) → its interaction contract → its rendered fidelity.
  *"Does it render exact and actually work — no framework, no native form element?"*

They **cross at the component contract** — the contract is *both* the abstraction (a named part with
an API) *and* the embodiment (a real box with exact pixels, an `ElementInternals`-bearing element,
a keyboard map). That crossing is the whole technique. A component can be:

- **designed right, built wrong** — clean layer, clean anatomy, elegant API, but the geometry is off
  the ramp, it submits nothing in a form (no FACE), it traps no focus, or it vanishes in Windows
  High Contrast. *Good idea, bad build.*
- **built right, designed wrong** — pixel-exact, accessible, form-associated, renders perfectly —
  but a boolean-prop explosion, a baked-in outer margin, a wrong layer. Works in isolation, **rots
  the library**. *Good build, bad idea.*

Opposite defects, opposite fixes — so you **score and report the two axes separately, never
averaged**. An averaged "3/5" hides which of the two you have.

## The leveled walk

| Axis | Direction | Levels (in order) | Asks |
|---|---|---|---|
| **A · Compose** | whole → part | **A1** Layer `[gate]` → **A2** Anatomy `[gate]` → **A3** API surface → **A4** Composition *(tier ladder · seam — `[gate, code]` joints)* → **A5** Coherence | "Is it the *right component*, shaped to compose?" |
| **B · Realize** | part → whole | **B1** Geometry `[gate, code]` → **B2** Element `[gate]` → **B3** Semantics `[gate]` *(+ cross-component state)* → **B4** Interaction *(+ cross-component reflow)* → **B5** Fidelity | "Does it *render exact and work*, here, with no native control?" |

`A1 · A2` and `B1 · B2 · B3` are **`[gate]`s** — a failure cascades and BLOCKS the reviews below it
on that axis (you can't judge an API that's mis-layered, or fidelity for an element that never
attaches internals). `A3–A5 · B4–B5` are **`[review]`s** (1–5) — **with one exception: A4's
tier-consistency and seam joints are a mechanizable gate** (a mis-cut tier or a seamless component
blocks A4). A shippable component (or composition) is **≥4 on every review with zero gate failures**,
reported as two separate axis scores plus the quadrant.

Three gates route to code, never inference:
- **B1 Geometry** → `scripts/geometry-check.py` (the ramp + the `(height − glyph)/2` law). See
  `geometry-system.md`.
- **A1/A2/B2/B3/B4 contract** (single-component card) → `scripts/component-contract-check.py` (layer,
  parts, FACE, role, APG-keyboard minimum, forced-colors). See `api-policy.md`, `platform-baseline.md`.
- **A4/A5 composition** (multi-component card) → `scripts/composition-check.py` (tier-consistency, the
  seam gate, overflow-declared, the slot-presence → grid generator, no self-margin). See
  `composition-patterns.md`.

### A · Compose (whole → part)

- **A1 Layer `[gate]`** — is it placed at the right tier: **token** (a raw/aliased value), **primitive**
  (token-only API, no domain name — `box`, `stack`, `cluster`, `grid`), **component** (a named, skinned
  widget — `button`, `select`, `card`), or **pattern** (a reusable composition of components — a
  modal card, a form field)? A `Card` is not a primitive; a `Stack` is not a component. Mis-layering
  poisons every decision below. (Decision rule in `api-policy.md`.)
- **A2 Anatomy `[gate]`** — are the parts named, and is every styleable part exposed (a `::part`, a
  slot, or a `:state()`)? A button is `[ icon? · label? · caret? ]`; a select is `[ trigger · value ·
  listbox · option · indicator ]`. Anatomy you can't name you can't theme, compose, or test.
- **A3 API surface `[review]`** — props-vs-slots discipline (config the common + finite, slot the
  open-ended), orthogonal `variant` × `size` enums (not multiplied booleans), controlled/uncontrolled,
  event payload contracts. For a custom element the API *is* the **attributes-as-API** surface — typed
  attributes (+ reflection), declared-vs-manual properties, semantic events, the form-value channel
  (`attributes-as-api.md`). **A3 cannot score 5 while a `manual:true` property has no upgrade story**
  (the lazy-upgrade / `upgradeProperty` hazard — *designed-right, built-wrong* in API form).
- **A4 Composition `[review, with gated joints]`** — does it compose *up*? This rung carries the
  **tier ladder** (**primitive → component → module**) and **the seam**:
  - **Tier `[gate, code]`** — a *primitive* composes no other `x-*` (an atom — the leaf, graded as a
    single component below); a *component* composes ≥1 primitive **and adds a seam**; a *module*
    arranges ≥2 components into regions **with cross-component state**. A mis-tiered piece (a
    "component" that's really a module; a "module" that's one component in a frame; a primitive doing a
    component's job) poisons everything below. `composition-check.py` gates tier-consistency.
  - **Seam `[gate, code]`** — a component **wires** its primitives through a real seam: **named slots**,
    the **slot-presence grid** (the layout reshapes by which slots are filled — `:has()`-driven, no
    phantom column on an absent slot; the deterministic `slot-grid` joint), and, for a
    capacity-constrained axis, an **overflow mechanism** (priority-ordered collapse, the *same* items,
    one source of truth). A component with no seam (children hardcoded) is **boxed but inert** — it
    renders once and breaks when content varies. A `god-component` (one element swallowing many
    concerns) is the inverse defect.
  - **Nest `[review]`** — does its own anatomy nest (a button is also the trigger of a select, the item
    of a menu)? Does it compose without boolean-prop explosion or leaking compound-component state? The
    leaf primitives are **cited** (the single-component contract), never re-derived here.
- **A5 Coherence `[review]`** — naming, the semantic-token contract, size/density attributes, the
  versioning/deprecation surface — does it look like it belongs to the same library as its siblings?
  **No self-owned outer margin** (spacing *between* pieces is the parent composition's `gap` / region
  grid — the single most common composition-wide drift). And the **up-handoff**: the *module* is the
  largest thing this skill owns; the **app shell / page region grid** it sits inside hands UP to
  break-down-layout — A5 checks only *"does the module cohere as one workflow and fit the slot the
  shell hands it"*, not the shell's design.

### B · Realize (part → whole)

- **B1 Geometry `[gate, code]`** — does every dimension sit on the ramp and obey the `(height −
  glyph)/2` law: correct height/icon/caret/font/spacer for its size, derived edge paddings,
  icon-only/caret-only **square**, composed container insets? Routed to `scripts/geometry-check.py`.
- **B2 Element `[gate]`** — an **autonomous** custom element (never a customized built-in / `is=""` —
  Safari refuses them permanently), hyphenated tag, signals-reactive, lifecycle correct (light DOM by
  default; nothing leaked on disconnect).
- **B3 Semantics `[gate]`** — role/ARIA/`:state()` set via `ElementInternals`; any control is
  **form-associated** (`formAssociated`, `setFormValue` on first render *and* change, a `name`, a
  `setValidity` story). No native `<input>/<button>/<select>/<textarea>` anywhere. **Cross-component
  note:** in a composition, state flows *up* (a primitive's change event → component → module) and
  control flows *down*; cross-piece coordination (a modal's `open`, the settings nav↔content selection,
  the toolbar's overflowed set) lives at the **lowest common parent**, never duplicated. State authored
  twice (a modal that owns its own `open` *and* a parent that owns one) is the cross-component defect.
- **B4 Interaction `[review]`** — the APG keyboard + focus contract (roving tabindex vs
  `aria-activedescendant`), and the **native-parity budget**: every native affordance you gave up
  (focus ring, label association, autofill, mobile picker, forced-colors, IME) rebuilt and proven.
  `@media (forced-colors: active)` present. **Cross-component note:** a composition must *adapt* — the
  overflow actually collapses when width runs out (every overflowed action stays reachable), the
  slot-presence grid reshapes for present/absent slots, and empty/loading/error states are designed.
- **B5 Fidelity `[review]`** — SSR via declarative shadow DOM (adopt-don't-recreate) or light-DOM,
  theming surface (`::part` + custom properties), inline-SVG-in-shadow icons, and graceful
  degradation on the non-Baseline edge (anchor positioning, cross-doc view transitions).

## The opposite-defect quadrant

```
                 B · REALIZE passes        B · REALIZE fails
A · COMPOSE  ┌────────────────────────┬────────────────────────┐
   passes    │      SHIPPABLE         │  designed right,        │
             │  (≥4 every review,     │  built wrong — clean    │
             │   zero gate fails)     │  API, but off-ramp      │
             │                        │  pixels / no FACE /     │
             │                        │  dead in forced-colors  │
             ├────────────────────────┼────────────────────────┤
A · COMPOSE  │ built right, designed  │       REBUILD           │
   fails     │ wrong — accessible &   │                         │
             │ exact, but prop-       │                         │
             │ exploded / outer-      │                         │
             │ margined / mis-layered │                         │
             └────────────────────────┴────────────────────────┘
```

The quadrant **names the fix**: top-right needs platform/geometry work; bottom-left needs API
surgery. Report the cell, not an average. For a **composition**, the same two cells read in the
tier-ladder dialect: a beautifully-bounded composition whose seam is fake (a hardcoded "···" overflow,
static slots, state authored twice) is **boxed but inert** — Compose's A4 *seam* gate fails while the
boundaries look clean; a composition that works but whose tiers are mis-cut (a god-component, a
"component" that's really a module) is *built right, designed wrong* at A4.

## Modes

- **DESIGN** — new component **or composition**. Walk **A-down** (layer/tier → anatomy → API → the
  composition seam → coherence), then **B-up** (geometry → element → semantics+state → interaction →
  resilience), reconcile at the contract, run the relevant `scripts/` checks, hand the locked artifacts to
  the repo's component seat (in agent-ui, the `component-builder` agent) or the host/`system-builder`
  agent; the *app shell* hands up to break-down-layout.
  Output: a `*.contract.json` card and/or a `*.composition.json` card + a geometry spec + the two-axis
  grade.
- **DECOMPOSE** — read an existing component or composition (code, or a screenshot + measurements).
  Name its layer/tier and anatomy/boundary (A1–A2; A4 tier for a composition), walk its realization
  bottom-up (B1–B3), find the seam (A4) and cross-component state (B3), then score the reviews. Output:
  its contract/composition card + a platform/geometry gap list.
- **GRADE** — score both axes against the bound rubric: the leveled walk above IS the rubric
  (there is no separate rubric file). Gates first, in cascade order; stop an axis at its first failed gate;
  place the result in the quadrant; name one corrective per failure.

## Walk order (do not skip)

1. **A1 Layer** — name the tier. Wrong tier ⇒ stop, re-place.
2. **A2 Anatomy** — name the parts. Unnamed parts ⇒ name them before anything else.
3. **B1 Geometry** — run `geometry-check.py`. Off the ramp or non-square glyph-only ⇒ fix the
   numbers; they are not negotiable design taste, they are arithmetic.
4. **B2 Element / B3 Semantics** — autonomous element? form-associated control? role via internals?
   Run `component-contract-check.py`. Any gate fail ⇒ fix before reviewing.
5. **Reviews** — A3–A5 then B4–B5, 1–5 each. Below 4 ⇒ name the single corrective.
6. **Report** — two axis scores, the quadrant cell, gate failures first.
