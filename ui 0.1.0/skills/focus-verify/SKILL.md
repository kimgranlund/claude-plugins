---
name: focus-verify
description: Verify focus-ring recipes, hit-target minimums, focus order, and keyboard affordances — and prescribe compliant values where missing. Use when checking focus order / tab sequence, keyboard navigation and traps, modal/dialog focus trap and restore, Escape and arrow keys per role, which keys a menu / tabs / listbox answers (APG), focus management on route change, focus-ring tokens that clear 3:1 under every surface, "the focus ring is invisible in dark mode", or hit-area expansions for small interactive elements. NOT for general text/background contrast, palette, or color-blind safety (color-verify) — owns only focus-ring contrast; NOT for RTL/bidi, dir/lang, locale Intl formatting, or text-expansion (i18n-verify); NOT for loading skeleton/spinner, CLS, or perceived-latency budgets (perf-verify); NOT for destructive-action undo/type-to-confirm or audit-trail UX (safety-verify); NOT for color-space theory or palette math (color-science-spaces); NOT for building a tab-list or menu component (component-forge).
disable-model-invocation: false
user-invocable: true
---

# focus-verify — keyboard & focus invariants, card-gated

Owns the WCAG 2.2 keyboard/focus invariants of a product UI. The verify contract: **declare the
surface in a card → the checker gates the mechanical facts → judgment covers only what code
cannot see** (whether the tab walk matches task flow, whether a recipe fits its surface).
Breadth under one stem, cited: hit-targets and keyboard affordances live under `focus` because one
interactive-surface card (`*.focus.json`) carries all three facts — ring, target, keys — for the
same elements, and splitting the stem would split the card; renaming was considered, keep-as-is
chosen (`skills-audit/references/standard-of-excellence.md` §N3).

## The card

A **focus order card** (`*.focus.json`) declares one view's keyboard structure — per element:
`tabindex` (0 natural · -1 programmatic · >0 the anti-pattern), `focusable`, `visible_focus`;
plus `dom_order`, `modals: [{id, open, trap, restore_focus}]` (one entry per overlay — sheet,
drawer, dialog; the trap/restore checks run per entry; the legacy single `modal{}` is still
accepted), `targets: [{id, w, h, inline_text?, spacing_ok?}]` (hit-target sizes with the SC 2.5.8
exception flags), and `ring: {width_px, contrast_light, contrast_dark}` (the focus-ring's
mechanical facts). The card can NEVER carry `:focus-visible` discipline or route-change focus
management — those are judgment-tier and live in step 3, not in any card key. If no inventory
exists to build it from, enumerate the interactive roles from the codebase (buttons, links,
inputs, triggers, composite widgets) — and flag anything that *looks* interactive but is declared
not: that is a UX bug upstream of focus. Declared narrowing: of SC 2.5.8's exceptions the card
models only `inline_text` and `spacing_ok` — the `essential` and UA-default-control exceptions are
NOT modeled; a target claiming either is argued in step 3, never encoded.

## Procedure

1. **Enumerate** interactive roles from the component inventory or codebase; build the card.
2. **Gate:** `python3 scripts/focus-check.py <card.json | dir>` — a FAIL blocks the emit; fix the
   surface, not the card. `selftest` proves the checker itself.
3. **Judge what the checker can't:** walk the passing tab order against reading order and task
   flow; match each ring to its recipe and each role's keys to APG (`assets/keyboard/affordances.json`);
   apply the invariant table below to sizes, contrast, and motion.
4. **Emit** the verdict — every violation cites the element/CSS rule it evaluates and routes its
   fix to the artifact that can make it. Where values are missing or non-compliant, the verdict
   carries its prescribed-values payload — per-role tokens
   `{role, hitAreaPx, focusRing: {recipe, widthPx, offsetPx, colorLight/Dark}, keyboard: {tabbable, activationKeys, escapeBehavior}}`
   — the compliant values the fix adopts, not a generation product.

## Invariants (the numbers)

| Invariant | Value | Source |
|---|---|---|
| Hit target | ≥ 24×24 CSS px — or inline-text exception, or ≥24px center-to-center spacing, documented | SC 2.5.8 |
| Platform floors | Apple 44pt · Material 48dp — the stricter wins on those platforms | `assets/targets/minimums.json` |
| Hit vs visual | hit area ≥ visual size; a 16×16 icon-button expands via padding/pseudo-element | SC 2.5.8 |
| Ring thickness | ≥ 2 CSS px | SC 2.4.13 |
| Ring contrast | ≥ 3:1 against **every** adjacent surface, in **both** schemes | SC 1.4.11/2.4.13 |
| prefers-contrast | ring → 3px, color → `CanvasText` | recipes.json |
| forced-colors | `outline: 2px solid CanvasText` — custom ring colors are ignored, plan for it | recipes.json |
| Ring motion | transition `outline-offset`/`outline-color` only — never `outline-width` (layout jitter); reduced-motion keeps color at ~80ms (it is feedback) | — |

`assets/targets/minimums.json` and `assets/focus-ring/recipes.json` are canonical for these numbers; this table
is the summary.

**Ring recipes** (`assets/focus-ring/recipes.json`): **outer** (default — 2px outline, offset per the
radius table) · **inner-outer** (2px + 2px, when both element and page surfaces could match a
single ring color) · **inset** (for elements that cannot paint outside their bounds). Offset grows
with radius (`assets/offsets/per-surface.json`): none/sm/md → 2px, lg → 3px, xl → 4px — a square-cornered
ring on a round element reads as broken.

## Detection catalog (what a review hunts)

`outline: none` without replacement · focus by background-change alone · positive `tabindex` ·
`:focus` instead of `:focus-visible` (ring-flash on click) · box-shadow rings clipped by
`overflow: hidden` · hover-only affordances · one ring treatment for both on-surface and on-accent
placements (one will fail 3:1).

## Mechanism gate — `scripts/focus-check.py`

Mechanical facts route to code, never inference. The checker (stdlib-only, selftest-locked):

| Check | Severity | Fires when |
|---|---|---|
| `POSITIVE_TABINDEX` | gate | any `tabindex > 0` — overrides DOM order |
| `NO_VISIBLE_FOCUS` | gate | `focusable:true` with `visible_focus:false` (SC 2.4.7) |
| `MODAL_NO_TRAP` | gate | an **open** modal with `trap:false` — per `modals[]` entry (or legacy `modal{}`) |
| `TARGET_TOO_SMALL` | gate | a target with `w` or `h` < 24 CSS px and neither `inline_text` nor `spacing_ok` (the SC 2.5.8 exceptions) |
| `RING_TOO_THIN` | gate | `ring.width_px < 2` CSS px (SC 2.4.13) |
| `RING_LOW_CONTRAST` | gate | `ring.contrast_light` **or** `ring.contrast_dark` < 3.0:1 (SC 1.4.11/2.4.13) |
| `ORDER_MISMATCH` | advisory | tab walk diverges from `dom_order` under positive tabindex |
| `MODAL_NO_RESTORE` | advisory | open modal with `restore_focus:false` — per entry |

Absent card sections are **skipped and reported**, never silently passed; a malformed card errors
cleanly. The gate is **necessary, not sufficient** — a clean run proves no mechanical defect; step
3's walk proves the order is the *right* order.

## Family mechanics (canon: [[ui-audit]]'s `references/verify-mechanics.md` — cited, not restated)

- **Findings format:** `file:line — [RULE_ID] finding → fix` — mechanical findings take the
  checker's own names (table above); step 3's judgment findings take the slugs
  `focus.order-vs-task-flow` · `focus.recipe-fit` · `focus.apg-keys` · `focus.invariant-fit`
  (the table's judgment rows: platform floors, hit-vs-visual, ring motion, forced-colors) ·
  `focus.route-change`.
- **Symptom index:** "the focus ring is invisible in dark mode" → `RING_LOW_CONTRAST` · "the
  ring flashes on mouse click" → `focus.recipe-fit` (`:focus` vs `:focus-visible`) · "I can't
  tab to it" → `NO_VISIBLE_FOCUS` · "tab jumps around the page" →
  `POSITIVE_TABINDEX` / `ORDER_MISMATCH` · "focus is lost when the dialog closes" →
  `MODAL_NO_RESTORE`.
- **Armed mode:** invoked with no card/artifact → these invariants become standing session
  constraints; subsequent UI edits are held to them at edit time. One-shot mode is unchanged.
- **Disputed finding** → the canon's waiver ladder; this card's `inline_text`/`spacing_ok`
  flags ARE rung 2 (per-instance, documented, checkable). An accepted `essential`-exception
  argument (step 3's territory, never encoded in the card) is recorded as an ELEMENT-scoped
  rung-3 line — `waived: TARGET_TOO_SMALL @ <element> — essential — <date>` — never a wholesale
  rule waiver. After any fix: re-run at the same scope — addressed findings gone, none new
  (canon §3).

## Material & routing

| Path / peer | Use |
|---|---|
| `assets/targets/minimums.json` | SC 2.5.8 rules, exceptions, platform floors |
| `assets/focus-ring/recipes.json` | the three recipes + color strategies + contrast/forced-colors handling |
| `assets/offsets/per-surface.json` | ring offset/radius per element radius |
| `assets/keyboard/affordances.json` | per-role tab order, keys, escape, arrows (APG) |
| [[color-verify]] | the ramps/contrast primitives ring colors draw on |
| `token-builder` agent | consumes emitted interactive-role tokens |
| [[component-forge]] / the repo's component seat | where keyboard-affordance defects route — the maker that fixes a role's missing APG keys |
| [[ui-audit]] | the set-scoped sweep that composes this verifier |

**Done** (one-shot mode) = the checker gates pass AND step 3's judgment walk confirms the order,
recipes, and keys fit their surface — the gate is **necessary, not sufficient**; **NOT done** = a
green `focus-check` run alone, or a verdict over skipped card sections left unargued. Armed mode
has no terminal Done — its steady state is the standing constraint.
