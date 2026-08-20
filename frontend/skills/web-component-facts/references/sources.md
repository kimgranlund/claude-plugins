# Sources and provenance

This pack distills two live source trees (gen-ui-kit's web-components core + traits, agent-ui's
own component/trait sources) plus one dated field-report corpus's Part 1 doctrine ledger and one
dated field-report's contrast finding — not a live re-audit of either repo's full source tree.
Live source files were read directly on 2026-08-20 (this pack's authoring date, ticket #809,
frontend wave 5); the doctrine report and the contrast finding were authored 2026-08-20 by
dedicated reader sessions in their own repos, per the frontend knowledge series' master outline
(the same 2026-08-20 corpus synthesis that seeded `reactivity-facts`, `state-model-rules`,
`persistence-facts`, and `data-wiring-facts`).

## The grounding files

| Axis | Repo | File(s) consulted |
|---|---|---|
| `lifecycle-and-upgrade.md` | `adia/gen-ui-kit` | `packages/web-components/core/element.js` (constructor, `connectedCallback`, `disconnectedCallback`) |
| `stamping-and-reconcile.md` | `adia/gen-ui-kit` | `packages/web-components/core/element.js` (`ensure`, `reconcile`) + `core/template.js` (`stamp`/`mount`/`update`/`repeat`, the `wrap()` `display:contents` span) + `.claude/docs/specs/component-implementation-patterns.md` + `packages/plugins/adia-ui-forge/skills/primitive-authoring/references/lifecycle-patterns.md` |
| `traits-primitive.md` | `adia/gen-ui-kit` + `nonoun/agent-ui` + `nonoun/ultimate-tokens` | `packages/web-components/traits/define.js` + `traits/index.js`; `packages/agent-ui/components/src/traits/press-activation.ts`; `src/ui/app.js:2537-2560` (`mixinInto`, live source, contrasted against `.claude/docs/reports/reactivity-2026-08-20/00-synthesis.md`'s H2 finding) |
| `form-and-a11y.md` | `adia/gen-ui-kit` | `packages/web-components/core/form.js` (`UIFormElement`) + `packages/web-components/components/check/check.class.js` |
| `attributes-as-api-grammar.md` | `adia/gen-ui-kit` + `nonoun/agent-ui` | `.claude/docs/reports/2026-08-20-reactivity-review/04-doctrine-vs-practice.md` Part 1 (27 rules) + Part 3 (contradiction #6); `.claude/docs/spec/app-surfaces-m2.spec.md` SPEC-R5 |
| `control-testing.md` | `nonoun/agent-ui` | `.claude/skills/component-testing/SKILL.md`; `packages/agent-ui/components/src/controls/checkbox/` (live directory listing) |

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary field-report file or a live source file
  cited above, on 2026-08-20 (this pack's authoring date). Every substantive claim in this pack's
  six axis files carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated, real (not hypothetical) failure the source
  material itself documents as having actually occurred, or as currently, confirmedly live in
  production code (e.g. the gh#284 SSR upgrade-replay gap, the gh#285 `NOOP_INTERNALS` crash site,
  the 73-slot-use/3-destructive-render adopt-or-stamp audit). Distinguished from [verified] because
  the evidentiary weight is "this actually broke or is still broken," not just "this is what the
  code currently does."
- **[incident→verified, re-checked]** — `traits-primitive.md`'s mixin-collision-guard claim is the
  one case in this pack where a dated report's OWN finding needed a same-session correction: the
  report (`00-synthesis.md`, dated 2026-08-20) states `mixinInto` has "no method-collision guard,"
  but this pack's own direct read of the LIVE `src/ui/app.js` (also 2026-08-20) shows a
  `throw new Error(...)` guard already present at the exact cited line range. Rather than
  presenting the report's claim as current, this pack states both: the report's original finding,
  and the live-source correction, dated at the same authoring session it was caught.

Most axes in this pack are grounded in DIRECT LIVE SOURCE reads (`core/element.js`, `core/
template.js`, `core/form.js`, `traits/define.js`, `check.class.js`, agent-ui's own trait/test
files) rather than a report distilling that source — a stronger grounding tier than a
report-only citation, since a file:line reference can be independently re-checked against the
exact code that produced the claim. `attributes-as-api-grammar.md` is the one axis grounded
primarily in a dated field-report DOCTRINE LEDGER (the 27 numbered rules) rather than direct source
reads of every cited spec/ADR file, since those specs live in a different repo tree than what this
pack's authoring session directly walked; its citations are report section references, not
independent file:line reads of every ADR named.

## What this pack deliberately does NOT re-verify

This pack reads gen-ui-kit's and agent-ui's own live source directly for five of six axes, and
distills the doctrine report's own numbered rules for the sixth — it does not independently
re-derive every cited ADR/spec document's full text, and it does not re-audit ultimate-tokens'
broader codebase beyond the one `mixinInto` function directly re-checked for the mixin contrast. A
reader confirming one specific claim against CURRENT code should re-read the cited file:line in the
named repo, not treat this pack as a live source of truth for a moving codebase — the doctrine
report's own H2 finding going stale within the same authoring day (see above) is the concrete
proof that even same-day field-report claims can drift out from under a pack the moment the
underlying source changes.

## Fence provenance

The web-component-facts-vs-make-component (build PROCEDURE, not platform facts) and
web-component-facts-vs-reactivity-facts (reactive stamping internals vs. the reactivity KERNEL)
fences in this pack's SKILL.md were negotiated against the two sibling packs directly implicated —
`make-component`'s own suite gains the reciprocal no-trigger case, and `reactivity-facts`' own
suite gains the reciprocal no-trigger case for a stamping-strategy-shaped ask that is NOT a kernel
question. See this pack's own Boundaries section and each sibling's own updated fence naming this
pack in return.

Extension: governed by [[make-pack]]
