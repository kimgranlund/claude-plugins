# @layer cascade architecture vs. load-order discipline

Two live systems answer the same question — "who wins when two rules conflict?" — with opposite
mechanisms, and both are shipping in production today. Neither is a strawman for the other.

## The @layer system (gen-ui-kit, ADR-0038)

**[verified]** gen-ui-kit's `docs/ops/adr/adr-0038-cascade-layer-precedence.md` (accepted
2026-05-31, migration complete same day) replaced specificity-workaround precedence with one
declared layer order:

```css
@layer reset, tokens, elements, components, utilities, context, overrides;
```

A later layer beats an earlier layer **regardless of selector specificity**; within a layer,
normal specificity still applies. Before this ADR, the codebase carried the workaround tax the
ADR's own census measured: 2,285 `var(--public, var(--public-default))` consumer-override chains,
326 `:where()` zero-specificity wraps, 282 `@scope` blocks, and 31 `!important` escape hatches —
each one a hand-rolled substitute for a precedence rule that `@layer` now states declaratively
once. **[incident]** ADR-0037's `[inline]` convention had to ship as a *per-component*
`:scope[inline]` override (specificity 0,2,0) specifically because a bare global `[inline]`
(0,1,0) tied with the component's own `:scope{display}` rule and the tie was cascade-order-fragile
— there was no layer to break it. Under `@layer`, the same global rule in `utilities` beats the
component's rule in `components` by layer order alone, with no specificity arithmetic and no
per-component override needed.

**The `overrides` layer is a named consumer contract, not an accident.** ADR-0038's OD-02 makes it
explicit: naming the last layer `overrides` states the promise "consumer CSS always wins" as a
documented seam, and unlayered consumer CSS (which already wins over every `@layer`-declared rule
per the CSS spec) satisfies the same promise without even needing the name.

**@layer does not replace every mechanism it was hoped to retire.** ADR-0038's own "Thesis
correction" (recorded in its Status line) walks back part of the original goal: `@layer` governs
rule PRECEDENCE, and is *complementary to* — not a substitute for — the `var()`-chain indirection
(consumer-override surface, still useful for the indirection itself, just not as a
precedence-hack), `:where()` (still legitimate for genuine zero-specificity element defaults),
and `!important` (a11y/inline-beating escape hatches are a different problem than precedence).
"Retire N workarounds" was retired as a goal; "declare precedence once instead of per-rule" is
what shipped.

## The load-order system (agent-ui, its own ADR-0003)

**[verified]** agent-ui runs a different repo, a different numbering scheme, and — confirmed by
direct source read — no `@layer` at all in its shipped foundation stylesheet. Its own
`.claude/docs/adr/0003-single-file-component-css-barrels-host-page.md` (accepted 2026-06-26)
governs precedence through **declared import sequence**, not cascade layers: three barrels
(`foundation-styles`, `component-styles`, `components`) consumed by a host page that links them in
a fixed order, tokens first. The barrel file itself states the law inline:

```css
/* foundation-styles.css — the global foundation stylesheet barrel (ADR-0003). Aggregates the
 * cross-package foundation layer from `@agent-ui/shared`: the colour `tokens.css` FIRST, then the
 * dimensional ramp `dimensions.css` (authored to load AFTER tokens)... Order is load-bearing — do
 * not reorder. */
@import '@agent-ui/shared/tokens.css';
@import '@agent-ui/shared/dimensions.css';
```

Precedence here is a **file-ordering discipline enforced by convention and comment**, not a
browser-parsed declaration — a `@import` sequence is authorial, and nothing at parse time stops a
consumer from linking the barrels out of order. The system compensates with `@scope` (ADR-0003 in
gen-ui-kit's numbering; agent-ui uses the identical two-block contract, see
`scoping-strategies.md`) for component isolation and relies on source-order-within-a-scope for the
rest — the same "later declaration wins at equal specificity" rule `dimensions.css` itself invokes
for its viewport-responsive override block (see `frame-vs-rhythm-geometry.md`).

## The tradeoff — why neither system is strictly better

| | `@layer` (gen-ui-kit) | Load-order (agent-ui) |
|---|---|---|
| Precedence source | Declared once, parsed by the browser | Import sequence, enforced by convention |
| Fails how | A rule lands in the wrong layer (caught by lint/audit) | A barrel loads out of order (caught by nothing at parse time — a comment is the only guard) |
| Migration cost | A one-time, provably behavior-neutral wrap (ADR-0038's computed-style-probe discipline) | Zero migration — the discipline was there from barrel 1 |
| What it buys | Structural "consumer always wins" with no specificity arithmetic | Simplicity — no new at-rule to learn, fewer moving parts for a smaller stylesheet surface |
| What it costs | A census-and-migrate project once precedence has calcified around workarounds (2,285+326+31 in gen-ui-kit's case) | An unenforced invariant — "tokens load first" is a comment, not a browser-checked fact; a consumer who reorders the `<link>` tags gets silently wrong precedence |

**The actual decision isn't "which is correct" — it's "has precedence already calcified into
workarounds, or is the surface small enough that load order alone still holds."** ADR-0038 was
adopted specifically because the workaround census showed calcification (2,285 `var()`-chain
overrides is not a stylesheet that discipline alone can still hold); agent-ui's barrel system
predates that scale of surface and has not (yet) needed the same escape. Neither ADR treats the
other's approach as a strawman: ADR-0038's own "Alternatives considered" section (Alternative D in
gen-ui-kit's separate `@scope` ADR, not `@layer`'s own) explicitly notes that `@layer` and `@scope`
"compose... they are not substitutes" — the same non-competing relationship holds between `@layer`
and load-order: a codebase can adopt `@layer` for precedence while still deciding to link its
barrels in a specific, load-bearing order for readability, or it can rely on load order alone
until the workaround tax makes `@layer`'s migration cost worth paying.

## Sources

- gen-ui-kit `docs/ops/adr/adr-0038-cascade-layer-precedence.md` — the `@layer` decision, full
  workaround census, migration proof discipline, thesis correction.
- gen-ui-kit `docs/ops/adr/adr-0003-two-block-scope-css-contract.md`, Alternative D — states
  `@layer` and `@scope` compose rather than substitute.
- agent-ui `.claude/docs/adr/0003-single-file-component-css-barrels-host-page.md` — the barrel +
  load-order decision (agent-ui's own ADR-0003, a different document from gen-ui-kit's).
- agent-ui `packages/agent-ui/components/src/foundation-styles.css` — the load-bearing `@import`
  order (`@agent-ui/shared/tokens.css` then `dimensions.css`), read directly 2026-08-20.
