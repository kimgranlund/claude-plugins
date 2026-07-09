---
name: perf-verify
description: >-
  Reason about and verify perceived latency. Use when auditing loading UX against a performance budget —
  the invariants an async surface must satisfy: latency feedback windows, skeleton vs spinner vs optimistic
  decisions, streaming UX, Core Web Vitals (CWV) and CLS budgets, layout shift / jank, image-dimension
  reservation, and cancellation of long-running operations — "the page feels slow even
  though the API is fast", "the layout jumps around while images load", when CLS is eroding trust, or
  streaming needs coherent presentation. NOT for contrast/palette/color-blind safety
  (color-verify); NOT for focus order, keyboard nav, or hit-targets (focus-verify); NOT for
  RTL/bidi/Intl/text-expansion (i18n-verify); NOT for undo/type-to-confirm or
  audit-trail UX (safety-verify); NOT for color-space math (color-science-spaces); NOT for
  wire latency or bundle-size; NOT for a spinner/skeleton-loader component (component-forge);
  NOT for animation duration/easing/choreography — sluggish by design, not by load
  (motion-design).
disable-model-invocation: false
user-invocable: true
---

# perf-verify — perceived-latency invariants, card-gated

Owns the perceived-latency layer of a product UI: wire latency is measured in ms, perceived
latency in trust. The verify contract: **declare measured metrics against budgets in a card → the
checker gates the arithmetic → judgment covers only what code cannot see** (whether a surface
*feels* fast, whether the loading affordance fits its operation).

## The card

A **performance budget card** (`*.budget.json`) pairs measured metrics with their budget:
`{"page": "/checkout", "metrics": {lcp_ms, cls, inp_ms, tbt_ms, bundle_kb, image_kb, requests},
"budget": {…}}` — lower is better for all. If no measurements exist, enumerate the async surfaces
from the codebase (fetches, route loaders, mutations, streams) and classify each in the card's
`operations: []` section: `{id, expectedLatencyP50Ms, expectedLatencyP95Ms, outcomeShape:
known|streamed|unknown, idempotent, cancelable, reversible, recipe?}` — an async surface with no
classification is the first finding. The checker now validates `operations[]` mechanically:
`OP_UNCLASSIFIED` (advisory) for an op missing its required fields, `RECIPE_MISMATCH` (gate) when
a declared `recipe` contradicts the feedback-window ladder, `CANCEL_MISSING` (gate) when a ≥ 3s
progress op exposes no cancel, `SHAPE_MISMATCH` (advisory) when a skeleton recipe declares
`outcomeShape: unknown`; whether the recipe *fits its layout-bearing surface* stays judgment in
step 3. A card carrying `operations[]` with no `metrics{}` reports `CWV: UNMEASURED` on the
summary line — unmeasured is never a pass.

## Procedure

1. **Enumerate** async operations and measured metrics; build the card.
2. **Gate:** `python3 scripts/budget-check.py <card.json | dir>` — a FAIL blocks the emit; fix the
   surface, not the card. `selftest` proves the checker itself.
3. **Judge what the checker can't:** match each operation's feedback recipe to the windows below;
   apply the affordance decision (`decisions/skeleton-vs-spinner.json`,
   `optimistic/eligibility.json`); check streaming posture (`streaming/posture.json`) and
   cancellation (`cancellation/contract.json`); verify every async insertion reserves its space.
4. **Emit** the verdict — every violation cites the operation/metric it evaluates and routes its
   fix to the artifact that can make it — plus per-operation recipes where asked, drawn from the
   checker's accepted set: `{id, recipe: none|instant|busy|spinner|skeleton|skeleton-or-spinner|
   skeleton+subtle-continuous|progress[+eta][+cancel][+explain]}` (the progress forms compose in
   that order).

## Invariants (the numbers)

| Invariant | Value | Source |
|---|---|---|
| Instant | < 100ms — no indicator; the state change itself is the feedback | `thresholds/perception.json` |
| Responsive | 100–300ms — inline busy micro-feedback; placeholder only past 300ms | `thresholds/perception.json` |
| Acknowledged | 300ms–1s — skeleton (layout-bearing) or spinner (unknown shape); never a blocking dialog | `thresholds/perception.json` |
| Progressing | 1–3s skeleton + continuous animation (show cached data) · 3–10s progress + ETA, cancel mandatory · > 10s add a proactive explanation ("usually takes ~15s") | `thresholds/perception.json` |
| Route loaders | hold ~200ms before showing loading UI — wire < 200ms with an 800ms skeleton is presentation scheduling, not server speed | — |
| CLS | ≤ 0.1 per interaction (checker poor line 0.25); every async insertion reserves space — skeleton, aspect-ratio box, or `min-block-size` | `cls/budget.json` |
| Image reservation | every image/media declares `width × height` or `aspect-ratio`; fonts use `font-display: swap` + matched metrics (or `optional`), never `block` | `cls/budget.json` |
| Cancellation | > 10s exposes cancel co-located with progress; cancel restores prior state; recall-window cancel is non-destructive | `cancellation/contract.json` |
| Streaming | render tokens as they arrive; no flash at stream-end (the streaming view *is* the final view); container grows monotonically; aria-live chunked to sentence/paragraph, never per-token; reduced-motion drops typing animation | `streaming/posture.json` |

**Affordance decision** (`decisions/skeleton-vs-spinner.json` · `optimistic/eligibility.json`;
windows: the invariants ladder above): **skeleton** when the data is layout-bearing with known
shape (lists, grids) — it reserves the space; **spinner** when the shape is unknown or a single
item replaces in place — honest about not knowing; **neither** below the ladder's placeholder
floor (the busy state suffices) or past its progress boundary (promote to progress + ETA);
**optimistic** only when almost-always-success, idempotent,
reversible with a declared rollback target, and low blast — otherwise pending-then-commit.
Stale-while-revalidate: render cached data immediately, mark it stale, update in place.

## Detection catalog (what a review hunts)

Spinner on every async call regardless of duration · skeleton flashing on a < 200ms operation ·
rendered content replaced by a spinner during revalidation · fake progress bar creeping to 90% on
a timer · per-token aria-live announcements · blocking "please wait" dialog under 3s · optimistic
update without rollback · "streaming" buffered server-side and rendered in one chunk ·
`font-display: block` (FOIT) · a long operation with no cancel — the user is trapped.

## Mechanism gate — `scripts/budget-check.py`

Measured-vs-budget is pure arithmetic — routed to code, never inference. The ladder's canon
speaks p50 (`thresholds/perception.json` picks the recipe by p50); the gate holds each recipe to
its **P95** window — the canon's own upgrade rule ("if p95 crosses a boundary, upgrade; never
downgrade") made mechanical. The checker (stdlib-only, selftest-locked) classifies each metric:

| Check | Severity | Fires when |
|---|---|---|
| `POOR` | gate | measured over the CWV poor line — `lcp_ms > 4000`, `cls > 0.25`, `inp_ms > 500` — poor is poor regardless of an indulgent local budget |
| `RECIPE_MISMATCH` | gate | an op's declared `recipe` contradicts the feedback-window ladder — P95 outside the recipe's window (each window is the ladder span — invariants table above — where the recipe is legal; the canon's composite tokens are accepted: `skeleton-or-spinner` takes the union of its legs, `skeleton+subtle-continuous` the skeleton window). A too-fast indicator flashes; a too-slow recipe under-indicates |
| `CANCEL_MISSING` | gate | a progress-family recipe without `+cancel` on an op that is not `cancelable: true` and whose P95 sits in the ladder's cancel-mandatory range — the user is trapped |
| `OVER_BUDGET` | advisory | over the effective budget but not poor — a regression to watch |
| `OP_UNCLASSIFIED` | advisory | an `operations[]` entry missing any of id / P50 / P95 / outcomeShape / idempotent / cancelable / reversible |
| `SHAPE_MISMATCH` | advisory | a recipe committing to a skeleton (`skeleton`, `skeleton+subtle-continuous`) on an op declaring `outcomeShape: unknown` — a skeleton reserves a known shape; `skeleton-or-spinner` defers the choice and is exempt |
| OK | — | within the effective budget |
| SKIPPED | skip | no measured value and no effective budget; `operations[]` with no `metrics{}` additionally reports `CWV: UNMEASURED` on the summary line |

Core Web Vitals carry canonical default budgets when the card omits them — `lcp_ms 2500`,
`cls 0.1`, `inp_ms 200`, `tbt_ms 300`; `bundle_kb`/`image_kb`/`requests` have no universal "good"
number, so they are checked only when the card budgets them. Absent metrics are **skipped and
reported**, never silently passed; a non-numeric value errors cleanly. The gate is **necessary,
not sufficient** — a clean budget run does not prove the surface *feels* fast; step 3's reviews
prove that.

## Material & routing

| Path / peer | Use |
|---|---|
| `thresholds/perception.json` | canonical latency → recipe table |
| `decisions/skeleton-vs-spinner.json` | loading-affordance decision tree |
| `optimistic/eligibility.json` | when optimistic UI applies |
| `streaming/posture.json` | streaming invariants + aria-live chunking rules |
| `cls/budget.json` | layout-stability budget + space-reservation patterns |
| `cancellation/contract.json` | cancel placement + state-restoration rules |
| [[component-forge]] | the maker seat — recipe/reservation/streaming defects route there (or the repo's component seat) for the fix |
| [[safety-verify]] | shares the recall/cancellation contract for long destructive operations |
| [[ui-audit]] | the set-scoped sweep that composes this verifier |

**Done** = the budget gate passes + every async surface classified with a ladder-consistent
recipe + step 3's judgments (affordance fit, streaming posture, cancellation, space reservation)
made; **NOT done** = a green budget-check alone, or an `UNMEASURED` card read as a pass.
