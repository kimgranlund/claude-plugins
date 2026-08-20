# The attributes-as-API contract grammar

"Attributes-as-API" names a designed grammar, not an ad-hoc convention: bare attributes + a yaml
single source of truth + one global attribute vocabulary, with a completeness target and a gate
[verified, `04-doctrine-vs-practice.md` Part 1 rule 6]. Each rule below is numbered against that
doctrine report's own Part 1 (27 ratified rules total).

## yaml is the single source of truth

A component's public API is authored ONCE in yaml; the sidecar files, the catalog, and the
generated-UI grammar are all GENERATED from it, never hand-edited in parallel
[verified, rule 5, `component-yaml-contract.md` L6]. This is why `UIFormElement`'s shared
`data-msg-*` family (see `form-and-a11y.md`) is a NAMED, RATIFIED exemption rather than a silent
gap — it's shared mixin config read across 7+ components, not a per-component declared prop, and
the doctrine says so explicitly instead of leaving the yaml simply incomplete
[verified, rule 5 cross-ref, ADR-0060 §Decision 3].

## No-shadowing + the boolean flip rule

A component-local attribute name may never shadow a global attribute name (`size`, `gap`,
`density`, `padding`, `margin`, `weight`, `color`, …) — a collision either renames
(`qr-code`'s `margin` → `quiet-zone`) or converges (`table`'s own `density` folds into the global
one); the only pass-through is an ADR-cited exemption table [verified, rule 7, ADR-0053/ADR-0054].
Boolean props are always `default: false`, with the name inverted at the API boundary so the
default reads naturally — `permanent` (not a default-true `closable`), `no-*` for opt-outs; expand/
collapse naming splits by default-visibility (default-hidden overlays use `open`, default-visible
rails use `collapsed`) [verified, rule 8]. `no-*` is the one canonical negation prefix (`hide-*`
retired); interactivity is always opt-in via a positively-named boolean, default false
[verified, rule 9]. The absolutist "Boolean defaults are ALWAYS false" phrasing in the spec docs is
itself flagged as stricter than the ADR ledger's real position: a small, named set of ratified
`default: true` exceptions ships (`nav-group-ui collapsible`, `password-strength-ui show-label`),
carried by the same connect-time attribute-stamping mechanism `lifecycle-and-upgrade.md` documents
for true-default reflected Booleans [verified/disclosed-tension, rule 6 contradiction #6 in
`04-doctrine-vs-practice.md` Part 3, ADR-0075].

## Literal-false parity and null-over-sentinels

Literal string `"false"` parses to JS `false` on a Boolean prop — a deliberate deviation from
plain HTML presence semantics (where any attribute value, including the string `"false"`, is
normally truthy), chosen to match the generated-UI transpiler's own output
[verified, rule 10, ADR-0075]. A numeric prop's "no value" state is always `null`, never a
sentinel — `-1` on `progress-ui` is a named, grandfathered exception, not a pattern to repeat
[verified, rule 11, ADR-0013].

## Reflect rules and the data-* tiers

`reflect: true` is required for every state-bearing Boolean, so CSS can match `[attr]` — string
properties CSS needs to introspect prefer attribute bindings generally
[verified, rule 12]. API-conceptual state is always a declared, reflected yaml prop, never a
private `data-*` stamp — e.g. selection-item state is the parent group's own `value` (single
source of truth), with ARIA treated as derived wiring rather than API surface
[verified, rule 13, ADR-0056]. The `data-*` namespace itself has three ratified, ownership-decided
tiers: (a) a component's own class → internal anatomy markers only, never API state; (b) an
attachable trait → `data-{trait-name}-*`, prefixes globally exclusive (the exact mechanism
`traits-primitive.md`'s `defineTrait()` registration gate enforces); (c) the generated-UI runtime →
its own `data-a2ui-*` tier [verified, rule 14, ADR-0060/ADR-0061, `traits.md` rule 5]. Anatomy
markers use the DIRECT-CHILD combinator (`:scope > [data-row]`); slot selectors use the DESCENDANT
combinator (`:scope [slot="…"]`) because of the template engine's own `display:contents`
conditional wrapper — see `stamping-and-reconcile.md` for the trap this rule exists to route
around [verified, rule 15]. Attribute honesty rounds the grammar out: components silently accept
invented attributes with zero warnings, and a small reserved-name anti-pattern list keeps
meaning stable across the whole set (no `title`, no `active` on parents, `error` reserved for
validation, `disabled` only on form-participating components) [verified, rule 16].

## The closed event vocabulary — and its one ratified escape valve

Custom events bubble, use kebab-case names, and carry `detail`; the interaction lifecycle fires
`input` during interaction and `change` on commit [verified, rule 20]. agent-ui's own SPEC names
the vocabulary's actual closed set explicitly — `change · input · select · open · close · toggle`
— and treats adding a seventh member as an ADR-gated admission, not a casual addition
[verified, `app-surfaces-m2.spec.md` SPEC-R5, §4 cross-ref]. SPEC-R5 itself is the one deliberate,
disclosed divergence from that closure: a chat-submission affordance is not a form commit, a
selection, or a disclosure toggle, so `ui-conversation` exposes `onSubmit(cb)` as a
CALLBACK REGISTRATION instead of inventing a seventh event name — matching the same
non-standard-signal-as-callback precedent `RendererHost.onClientMessage` already set, rather than
requesting a new vocabulary member [verified, `app-surfaces-m2.spec.md` SPEC-R5, L89, L149].
The lesson generalizes: the event vocabulary stays closed and small BY DEFAULT, and a genuine
exception is named, cited, and precedent-matched rather than silently added.

## Practical guidance

- **Before naming a new attribute, check it against the global vocabulary first** — a
  component-local name that happens to collide with `size`/`gap`/`density`/etc. is a defect,
  not a coincidence to shrug off.
- **A Boolean's name is chosen so `default: false` reads naturally** — if the natural name would
  need `default: true` to make sense, invert the name instead of the default (the flip rule), and
  treat any surviving `default: true` case as needing its own ADR citation.
- **A `data-*` attribute is either an internal anatomy marker, a trait's namespaced family, or a
  runtime tier — never a substitute for a declared, reflected prop when the state is genuinely
  part of the component's public contract.**
- **A new custom-event name is a bigger decision than it looks** — the vocabulary is closed by
  design; reach for a callback-registration seam (SPEC-R5's pattern) before proposing a seventh
  event, and if an event genuinely is needed, cite the ADR that ratifies it.

## Boundary

This file covers the ATTRIBUTE/PROPERTY/EVENT naming grammar itself. The `ElementInternals`
mechanics a form-associated component's `value`/`validity` ride on are `form-and-a11y.md`; the
`data-*` trait-ownership REGISTRATION mechanism (as opposed to the naming tier this file states) is
`traits-primitive.md`; per-control test coverage for this contract (descriptor drift-wire tests)
is `control-testing.md`.
