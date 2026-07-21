# House locks — the estate's ratified motion parameters

Ruled 2026-07-16 (Issue #9). The corpus's other files carry the cited ENVELOPE (ladders, curves,
floors — what the evidence permits); this file carries the estate's chosen POINT inside that
envelope: one sanctioned value per load-bearing knob, with its forbidden neighbors named, so a
generating session stops re-deriving taste per run. Every entry is a **house ruling** — provenance
class: ruled-in-workspace, informed by the 2026-07-15 external-skill review's type specimens
(jakubkrehel/make-interfaces-feel-better@366f0f86e, emilkowalski/skills@6bf24434f), each value
checked against this pack's own cited envelope — never presented as a platform citation.

## The precedence seam (who overrides whom)

Project ruling (a DESIGN.md/token lock, minted via a taste gate — layout-decompose's
`taste-elicitation.md`) **>** house lock (this file) **>** cited envelope (the sibling
references). A Material-token project's motion is governed by `material-motion-facts`
wholesale — these locks apply to unruled, non-Material contexts, which is exactly where taste
drift happens. Deviation from a lock inside one project IS a project ruling: record it, per the
ask-then-lock loop.

**The floor is not a knob:** `prefers-reduced-motion` handling (reduced-motion.md) sits OUTSIDE
this precedence chain — no house lock, project ruling, or user preference sampled at a taste gate
may trade it away.

## The locks

- **Press/tap feedback scale** — always `0.96`; never `0.95` or below (reads toy-like — the
  element visibly "collapses"), never `1.0` (no acknowledgment at all).
  *Exception: full-viewport surfaces don't scale on press — a pressed screen is disorienting,
  not tactile. (Press feedback is exempt from the frequency gate below: acknowledgment, not
  choreography.)*
- **Functional bounce** — always `0` overshoot on functional UI (dialogs, menus, drawers,
  list items); never `0.1`-class decorative bounce — a bounce cycle adds on the order of `200ms`
  of settling (house estimate, not a citation) the user must wait through before the surface is
  stable to read.
  *Exception: expressly playful contexts (celebration states, onboarding delight) may take
  slight underdamping — as a project ruling, never silently.*
- **Enter/exit asymmetry (user-initiated dismissals)** — when the USER dismisses a surface they
  opened (drawer, menu, sheet), the exit always runs faster than the entrance (house point: exit
  ≈ `0.8×` the entrance duration — the direction is corpus-backed via web.dev's
  asymmetric-animation-timing in durations.md; the `0.8×` constant is a house ruling, since
  durations.md's own gap note records that no system codifies a ratio); never symmetric (equal
  open/close reads as sluggish dismissal — the user is already done).
  *Exception: the initiator flip (durations.md's own cited case) — SYSTEM-presented surfaces the
  user must notice (errors, alerts) enter fast and depart gently, exit slower than entrance; the
  lock governs user-initiated dismissals only.*
- **List stagger** — always `20ms` per item on functional lists (the point Carbon and Material 2
  both codify — choreography.md; the lock adopts the cited value as the house point), capped at
  6 staggered items (the rest appear with the sixth); never `100ms`+ steps (a 10-item list takes
  a full second to settle), never staggering below 3 items (reads as jank, not choreography).
  *Exception: a ≤3-item hero sequence may take up to `80ms` steps where the entrance IS the
  content — a house ruling above the cited functional point, disclosed as such.*
- **Hover feedback onset** — always ≤ `150ms`; never slower (hover feedback past 150ms reads as
  the UI deciding whether to respond).
  *Exception: hover-triggered SURFACES (previews, cards) may add an intentional open delay —
  that's disclosure timing, a choreography.md question, not feedback latency.*

## The frequency gate (which tier of motion an interaction may take)

Adopted from the review's frequency-gated decision-table pattern (emilkowalski specimen); the
tiers are a house ruling:

| Interaction frequency | Motion budget |
|---|---|
| Habitual — many times per session (keystroke-adjacent: toggles, tabs, list selection) | **No choreography.** State changes read as instant; the only motion is sub-`100ms` FEEDBACK (the nngroup instant band durations.md cites — feedback is not choreography, and the press-scale lock stays live here). |
| Daily — several times per session (drawers, menus, dialogs) | Functional motion only: ≤ `300ms` entrance (the cited modal/Material standard band, durations.md), locked asymmetric exit, zero bounce. |
| Occasional — a few times per week (onboarding, empty states, confirmations of rare/heavy actions) | Full choreography legal — stagger, z-space, spring character; the reduced-motion floor still governs. |

The gate composes with the locks: a daily-tier drawer takes the asymmetry and bounce locks; a
habitual-tier toggle takes no CHOREOGRAPHY — but press feedback is exempt from the gate (it is
acknowledgment, not motion design), so the press-scale lock applies at every tier.
