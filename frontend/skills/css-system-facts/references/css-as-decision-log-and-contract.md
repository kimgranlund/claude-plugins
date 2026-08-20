# CSS files as decision logs + CSS-as-tested-contract

Two related but distinct facts about how a mature CSS system stays legible and safe to change:
the FILE carries its own decision history inline, and the RULES it encodes are checked by
structural unit tests, not just visual review.

## CSS files as decision logs

**[verified]** Both grounding repos write CSS comments that cite ADRs, tickets, and GitHub issue
numbers directly beside the rule they justify — not a separate changelog, the CSS file itself.
agent-ui's `dimensions.css` is the clearest example: nearly every token block carries a comment
naming the ADR that ratified it, the alternative it superseded, and — critically — WHY, not just
WHAT:

```css
/* --md-sys-widget-inset (ADR-0041 cl.3) — the THUMB inset law for thumbed widgets (switch knob,
   slider handle): thumb = box − 2×inset, track = the widget box. A FLAT fleet CONSTANT (like a
   1px border / --md-sys-shape-corner-base), NOT box-scaled — 2px reads correctly from the 12-box
   to the 28-box. Geometric (frame family) → density-INVARIANT (density rides the gap, never the
   inset). On :root, not the `*` ramp. */
--md-sys-widget-inset: 2px;
```

This is qualitatively different from a typical "explain what this does" code comment — it encodes
a DECISION (why 2px, why a flat constant rather than scaled, why `:root` and not the derived
ramp) that a reader would otherwise have to reconstruct from an external ADR document, a git blame,
or a Slack thread. The `--md-sys-height-*`/`--md-sys-font-*` block goes further, naming the
specific ADRs it supersedes ("ADR-0038, supersedes the MULTIPLIER: ADR-0007's control leg +
ADR-0032's 0.875…1.75 ladder") — a reader hitting this token in isolation can trace exactly which
design was tried, rejected, and why, without leaving the file. gen-ui-kit's ADR-0038 (cascade
layers) shows the inverse direction of the same discipline: the ADR document itself names the
EXACT file paths and gate commands (`npm run check:cascade-layers`, `npm run
check:override-conformance`) that enforce it — the decision record and the enforced code stay
mutually citable.

**Why this matters architecturally, not just stylistically.** A CSS file with no inline decision
history invites the exact failure both these token files' comments explicitly guard against: a
future editor "simplifying" a constant back onto a derived ramp, or moving a token between
`:root` and `*` without understanding the pre-substitution trap (`frame-vs-rhythm-geometry.md`).
`dimensions.css`'s own comment states this defense explicitly: "Do NOT 'simplify' this back onto
`:root` — that re-breaks subtree scale/density." The comment is not documentation of a static fact;
it is an ANTI-REGRESSION note aimed at a plausible future edit.

## CSS-as-tested-contract

**[verified]** agent-ui's `disclosure-css.test.ts` demonstrates a distinct, complementary
discipline: a CSS file's STRUCTURE is asserted by a unit test that reads the raw CSS text and
regex-matches specific rules — not a rendered-browser snapshot test, and not a linter checking
generic syntax, but a test that encodes the SAME architectural invariants the file's own comments
state, as executable assertions:

```ts
it('the summary row: block-size off the ramp, padding-block: 0 (the centering law, geometry.md)', () => {
  const m = stylesBlock.match(/:scope \[data-part='summary'\]\s*\{([^}]*)\}/)
  expect(m, 'the summary rule is missing').not.toBeNull()
  const rule = (m as RegExpMatchArray)[1]
  expect(rule).toMatch(/block-size:\s*var\(--ui-disclosure-height\)/)
  expect(rule).toMatch(/padding-block:\s*0/) // NEVER block-padding as the sizing lever
  ...
})
```

**Four techniques recur across the suite, each worth naming as its own reusable pattern:**

1. **Comment-stripping before a grep-able-ABSENCE check.** A test asserting a pattern is ABSENT
   (`expect(code).not.toMatch(/transition\s*:/)`) must first strip comments (`stripCssComments`),
   or a prose comment explaining WHY a rule is absent ("no transition here — SPEC-R18") would
   itself contain the word `transition` and falsely trip the very probe meant to catch a real
   regression. This is a genuinely non-obvious testing gotcha specific to CSS-as-text assertions.
2. **Token-hygiene as a var()-reference audit.** `foreignScopeRefs()` extracts every `var(--...)`
   reference inside a scope block and flags any that is neither the component's own
   `--ui-{name}-*` chain nor an explicitly allow-listed shared seam (the focus-ring pair, the
   control line-height constant) — mechanically enforcing the "component CSS never references
   primitives directly" rule (`token-taxonomy-and-themes.md`) as a grep, not a manual review.
3. **The NEGATIVE control.** `disclosure-css.test.ts` includes a test that PLANTS a violation
   (`color: var(--md-sys-color-neutral-on-surface)` inside the scope block) and asserts the
   hygiene predicate CATCHES it — proving the detector actually detects, not just that the real
   file currently passes. Without this, a hygiene check that silently stopped matching anything
   (a broken regex, a typo'd selector) would read as a permanent green with zero signal.
4. **Structure/sectioning assertions distinct from computed-style assertions.** The suite's own
   header comment states the boundary explicitly: "jsdom can't compute rendered colours/px/
   rotation — that is `disclosure.browser.test.ts`'s cross-engine smoke; these pin the STRUCTURE
   + the CSS text." A CSS unit test in jsdom asserts what the TEXT says (selector shape, which
   properties a rule sets, token-reference hygiene); it does not and cannot assert what a real
   browser engine computes from that text (final pixel values, actual rotation angles) — that is a
   SEPARATE test tier (a real-browser smoke test), never faked by a jsdom string match pretending
   to be a rendered assertion.

**Why structural CSS unit tests earn their place alongside visual review.** A visual regression
test (screenshot diff) catches "does this look different," but is expensive to run, flaky under
font-rendering/anti-aliasing drift, and blind to WHY a rule changed. A structural CSS test like
`disclosure-css.test.ts` is fast, deterministic, and — because it asserts the SAME invariants the
file's own decision-log comments state (the h/2 centering law, the frame/rhythm token split, the
scope-hygiene rule) — it turns those architectural comments from prose that could silently drift
from the code into an executable contract that fails loudly the moment the code stops matching
what the comment (and the ADR behind it) actually claims.

## Sources

- agent-ui `packages/agent-ui/shared/src/tokens/dimensions.css` — the ADR-citing decision-log
  comment style, read directly 2026-08-20.
- gen-ui-kit `docs/ops/adr/adr-0038-cascade-layer-precedence.md` — the ADR-to-gate-command
  citation (`npm run check:cascade-layers`, `check:override-conformance`).
- agent-ui `packages/agent-ui/components/src/controls/disclosure/disclosure-css.test.ts` — the
  full structural CSS unit-test suite: sectioning, token-hygiene audit, the negative control, and
  the jsdom/browser-tier split, read directly 2026-08-20.
