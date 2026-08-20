# @scope vs. CSS Modules scoping strategies

## The problem both solve

Light-DOM web components (the substrate both grounding repos build on — Shadow DOM is
deliberately rejected in gen-ui-kit's own architecture for form-participation reasons) have no
built-in style boundary: without SOME scoping mechanism, component CSS leaks into consumer
surfaces, and a consumer's CSS can accidentally restyle component internals.

## Browser-native `@scope` (the grounded system)

**[verified]** gen-ui-kit's `docs/ops/adr/adr-0003-two-block-scope-css-contract.md` (accepted
2026-04-24) adopts `@scope` (Chromium 118+, Safari 17.4+, Firefox 128+ — Baseline for the
project's own browser floor) as a **compiler-enforced boundary**: the browser itself refuses to
match a scoped selector outside its declared root, with no build step, bundler plugin, or naming
convention required. The contract is exactly two blocks per component:

```css
/* Block 1 — token declarations, all variants pre-declared, :where() keeps specificity at 0 */
@scope (component-name) {
  :where(:scope) {
    --component-color: var(--a-fg);
    --component-bg: var(--a-bg);
  }
  :where(:scope[variant="primary"]) {
    --component-bg: var(--a-primary);
  }
}

/* Block 2 — styling that CONSUMES the tokens, never re-declares them */
@scope (component-name) {
  :scope {
    background: var(--component-bg);
    color: var(--component-color);
  }
}
```

Two rules make this contract legible from the CSS text alone: block 1 is tokens-only (so every
themeable knob is visible at the top of the file), block 2 is styling-only and reads ONLY
component tokens — never primitives or semantics directly (see `token-taxonomy-and-themes.md`'s
hop-skipping rule) and never a raw color value (enforced by the `component-token-audit` skill in
that repo).

## CSS Modules (the alternative build-time strategy)

CSS Modules is a build-time scoping strategy: a bundler (webpack, Vite, etc.) rewrites each
class name in a `.module.css` file to a generated, collision-resistant identifier
(`.button` → `.button_a3f9x`), and the consuming JS imports a mapping object to reference the
rewritten name. Scoping is achieved by NAME UNIQUENESS at build time, not by a browser-parsed
containment rule — there is no runtime concept of "this selector cannot match outside this
subtree"; there is only "this class name is statistically unlikely to collide because a hash was
appended to it."

## The tradeoff — compiler-enforced vs. build-tool-enforced

| | `@scope` | CSS Modules |
|---|---|---|
| Enforcement point | Browser parse time — a `@scope`-declared selector structurally cannot match outside its root | Build time — a bundler step rewrites class names before the browser ever sees the CSS |
| Requires | Browser support (Baseline per ADR-0001's floor); no build step | A bundler/loader in the toolchain; breaks if CSS is hand-authored or served unprocessed |
| What "leak" means | A selector written to match outside `@scope`'s root is invalid by construction — there is nothing TO leak | A class name collision is still POSSIBLE if two files independently produce the same hash, or if a consumer references the raw (un-hashed) class name directly in markup the bundler didn't process |
| Consumer overrides | A consumer targets the component's exposed CUSTOM PROPERTIES (block 1's tokens), never its internal class names — the two-block contract makes the override surface the token layer, not CSS specificity | A consumer must import the SAME generated class-name mapping to target anything, or fall back to `:global()` escapes that reintroduce the leak class Modules exists to prevent |
| Where it lives | Pure CSS, works with a plain `<link>`, no JS runtime dependency | Coupled to the bundler's module graph — a CSS Module has no meaning outside a JS import that resolves its generated names |

**The relevant rejected alternative — gen-ui-kit's own ADR-0003 rejects a BEM-style class
contract (Option B) for the identical reason CSS Modules avoids full manual discipline but keeps
a variant of the same risk**: "BEM works when every contributor agrees on every class name; in a
library shipping to diverse consumers, selector leakage is a matter of time. `@scope` is a
compiler-enforced boundary." CSS Modules mechanizes what BEM asks a human to do by hand (never
collide a class name) but the mechanization still operates at the SAME layer BEM does — unique
class names — rather than at the layer `@scope` operates at (a browser-native containment rule
independent of naming). A CSS Modules setup that ships an escape hatch (`:global()`) reopens
exactly the leak class `@scope` closes structurally.

**Why gen-ui-kit chose `@scope` over either manual BEM or a build-time class-hashing tool**: the
project ships zero-dependency web components (see `web-component-facts`) consumed by diverse
downstream apps with their OWN build tooling — a CSS-Modules-authored library would force every
consumer's bundler to understand the generated-class-name contract, or ship a pre-resolved
(and now un-collision-guaranteed) static CSS bundle. A browser-native `@scope` boundary needs no
cooperation from the consumer's own build tool; a plain `<link>` gets the same guarantee a
bundler-processed import would.

## Not a strict either/or

`@scope` and CSS Modules solve overlapping but not identical problems — a project using CSS
Modules already inside a single-bundler app (no cross-consumer distribution concern) may have no
reason to adopt `@scope`; the choice tracks the distribution shape (a library shipped to diverse
consumers vs. an app's own internal component tree), not a universal "better" ruling.

## Sources

- gen-ui-kit `docs/ops/adr/adr-0003-two-block-scope-css-contract.md` — the `@scope` decision, the
  two-block contract, Alternative B's rejection of BEM-style manual discipline.
- CSS Modules' build-time class-hashing mechanism — general, widely-documented bundler behavior
  (webpack `css-loader`, Vite's built-in CSS Modules support); not independently re-verified
  against a specific grounding-repo source, since neither grounding repo in this pack's corpus
  uses CSS Modules — stated here as the comparison point ADR-0003's own BEM rejection generalizes
  to.
