# Testing conventions: the per-control file quintet, jsdom-vs-browser split, architectural-boundary tests

Web components carry a specific test-bar shape because the platform surface itself is
layered (descriptor, DOM behavior, real-engine rendering, built output), and one test layer
routinely passes while another catches the actual regression.

## The per-control file quintet

A shipped control's own directory carries the same five-file shape every time: source
(`{name}.ts`), styles (`{name}.css`), a descriptor/usage doc (`{name}.md`), a jsdom behavior test
(`{name}.test.ts`), and a cross-engine browser test (`{name}.browser.test.ts`)
[verified, `packages/agent-ui/components/src/controls/checkbox/`, live directory listing
2026-08-20]. A control commonly grows beyond the bare quintet with named-scenario browser tests
(`answered-state.browser.test.ts`) and a visual-regression pass (`{name}.visual.browser.test.ts`
against `__baselines__`/`__screenshots__`) — additions, not replacements, for state or
regression coverage the plain quintet doesn't carry on its own [verified, same directory listing].

## The layered test bar, and what each layer actually proves

| Layer | Proves | Blind spot if skipped |
|---|---|---|
| Descriptor trip-wire | frontmatter ≡ `finalize(Class)` ≡ source (`customStates`/slots) | A yaml/source drift ships unnoticed — the exact failure mode `attributes-as-api-grammar.md`'s yaml-SoT rule exists to prevent |
| jsdom behavior + geometry/token trip-wires | props/events/form behavior; declared `--ui-{cmp}-*` custom properties all appear in `:where()`; no raw primitive refs | Fast, but jsdom does not lay out real boxes — geometry assertions here are structural, not pixel-real |
| Cross-engine browser test (Chromium + WebKit) | Rendered px actually responds to `[size]`/`[scale]`/`[density]`; survives `forced-colors`; the WHOLE rendered bounding box in a realistic container | Per-part px can all individually pass in jsdom while the control visually collapses to a dot — the "whole-shape law" this layer exists to catch |
| Built-output proof | The PRODUCTION build's shipped CSS/JS bytes behave, not just the dev-mode source | Dev-green ≠ built-green is a real, named failure class — a bundler downleveling a CSS feature broke a component only visible in a built-output test, never in a dev-mode jsdom or browser run |
| End-to-end (form controls) | Keyboard-only, behaves-like-a-user flows across the whole form lifecycle | Unit-level probes can each pass individually while the ASSEMBLED flow (tab order, submit, validation message surfacing) breaks |

[verified, `.claude/skills/component-testing/SKILL.md` "The bar, layer by layer" table]

## jsdom vs. real-browser: not a preference, a coverage split

The split is deliberate, not a speed shortcut: jsdom-green is explicitly NOT treated as "done" —
the control's `.browser.test.ts` must be green on BOTH engines before a control-wave commit is
considered gate-clean [verified, `.claude/skills/component-testing/SKILL.md` "The gates" item 2].
This matters specifically for web components because two of this pack's own axes are real-engine-
only concerns: the `display:contents` wrapper trap (`stamping-and-reconcile.md`) and the SSR
upgrade-replay gap (`lifecycle-and-upgrade.md`) both depend on actual layout/parsing behavior a
DOM-shim environment either doesn't reproduce or reproduces differently than a real browser.

## Architectural-boundary tests — a different unit than a per-control test

A per-control test asserts one control's own behavior. A SEPARATE test class asserts an
architectural CONTRACT across the whole component set: the descriptor drift-wire/source-wire pair
(`component-descriptor-{driftwire,sourcewire}.test.ts`) checks that frontmatter, the finalized
class, and the source file agree with EACH OTHER — not that any one control works, but that the
three-way contract the whole yaml-as-SoT grammar depends on hasn't silently drifted
[verified, `.claude/skills/component-testing/SKILL.md` descriptor trip-wire row]. Site-level gates
(`site-canon`, `site-toc`, `site-coverage`, the llms byte-gate) are the same class of test at a
different altitude — proving a cross-cutting invariant about the WHOLE catalog rather than any one
component's own behavior [verified, `.claude/skills/component-testing/SKILL.md` "The gates" item
5]. Treat "does this one control pass its own tests" and "does the architectural contract this
control participates in still hold" as two genuinely different questions — a green per-control
suite says nothing about whether the descriptor/source/yaml three-way agreement it depends on is
still intact.

## Practical guidance

- **A new control ships the quintet, not a subset** — source, styles, descriptor doc, jsdom test,
  browser test; a control missing the browser-test leg is untested for exactly the failure classes
  (display:contents layout, real cross-engine rendering) jsdom cannot see.
- **Never call jsdom-green "done"** for a web component specifically — the whole-shape law and the
  built-output-proof class both name real, measured incidents where a jsdom-only suite passed
  while the shipped behavior was broken.
- **An architectural-boundary test failing is a different kind of red than a per-control test
  failing** — it means the yaml/source/descriptor contract itself has drifted, not that one
  control's own behavior regressed; fix the contract violation at its source rather than patching
  the failing assertion.

## Boundary

This file covers WHAT gets tested and in which layer for a web component specifically. It is not a
general jsdom-vs-real-browser testing philosophy for arbitrary JS (out of scope for this pack
entirely) and not the component build PROCEDURE itself — authoring a new control's tests as part
of building it is `make-component`'s law, which this pack's own SKILL.md fences explicitly.
