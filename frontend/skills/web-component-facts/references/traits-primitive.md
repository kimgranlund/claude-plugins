# Traits: the convergent host-agnostic behavior primitive — and the mixin-flattened-this contrast

Two independent codebases converge on the same shape for reusable cross-cutting behavior — a
factory that takes a host element (plus config) and returns a cleanup — and a third, unrelated
codebase's `this`-flattening mixin approach shows why the convergence is load-bearing rather than
incidental.

## gen-ui-kit's version: `defineTrait()`, a registered factory with an ownership gate

A trait is a reusable behavior package (event listeners, attribute management, cleanup) defined
once via `defineTrait({ name, category, description, attributes, events, config, setup({host}) })`
and attachable to ANY DOM element, not just a `UIElement` subclass — `setup()` returns the cleanup
function the factory's `disconnect()` calls [verified, `traits/define.js:1-54, 124-170`]. Calling
the exported factory produces an INSTANCE closure holding its own `cleanup` reference; `connect`/
`disconnect` operate on that closure, never on a shared prototype `this` — two different elements
each get their own independent trait instance even though both came from the same factory
[verified, `traits/define.js:146-165`]. `UIElement` applies traits via `static traits = […]`,
`addTrait()`, or the declarative `traits="pressable scale-press"` attribute, each producing its own
`instance.connect(this, {host: this, signal, computed, effect})` call [verified,
`core/element.js:278-314`]. Registration enforces a `data-*` namespace-ownership gate: a trait owns
`data-{name}` (exact) and `data-{name}-*` (family) by default, any other prefix must be declared via
`prefixes: [...]`, and two checks run at registration time — every declared attribute/config name
must fall under an owned root, and a registered prefix can never overlap another trait's owned
namespace [verified, `traits/define.js:35-53, 70-110`, ADR-0060]. Behavior lives in traits, not in
generated layout — a designed-UI generator describes layout only, cross-cutting behavior always
routes through `defineTrait()` [verified, `04-doctrine-vs-practice.md` Part 1 rule 22].

## agent-ui's version: a plain function taking the host + config, no registry

agent-ui's own convergent shape drops the registry/schema machinery entirely but keeps the same
core contract — a function `(host, opts) => releaseFn` that wires listeners directly onto the
host's own connection lifecycle. `pressActivation(host, opts)` wires Space/Enter → `host.click()`
via `host.listen(host, 'keydown'/'keyup', handler)` — `host.listen` rides the host's own connection
`AbortSignal`, so listeners auto-remove on disconnect; the returned `release()` is only an
early-teardown escape hatch [verified, `packages/agent-ui/components/src/traits/
press-activation.ts:41-63`]. No factory registry, no schema, no ownership namespace — the
convergence with gen-ui-kit is at the SHAPE level (host-agnostic function/factory, explicit
teardown, no inheritance chain), not the implementation.

## What's actually convergent, and why it matters

Both repos independently reach: **a trait is a callable that takes a host reference (and config)
and returns/registers its own teardown — never a mixin merged onto a shared prototype, and never
baked into a base-class inheritance chain.** This is what "host-agnostic" means concretely: the
SAME trait can attach to unrelated host types (gen-ui-kit: any DOM element; agent-ui: any object
satisfying the host's own `listen`/`click` surface) because the trait never assumes anything about
`this` beyond what it's explicitly handed.

## The contrast: mixin-flattened `this` (a third, unrelated codebase)

A third codebase in the same field-report corpus (ultimate-tokens) composes cross-cutting behavior
by a different mechanism entirely: `mixinInto(Target, ...Sources)` copies every own
prototype method/getter/setter from each mixin "class" onto `Target`'s prototype — the mixin
classes exist only as a syntax carrier for their methods and are never instantiated
[verified, `src/ui/app.js:2537-2560`, live source read 2026-08-20]. Every mixin method, once
composed, runs with `this` bound to the ONE flattened host instance — there is no per-mixin
closure, no independent instance, and no ownership-namespace check; a name collision between two
mixins is a real risk the composer itself must guard against explicitly
[verified, `src/ui/app.js:2542-2559`]. The project's own field-report corpus names this as an
explicit, DOCUMENTED trade-off rather than a defect to fix — "the mixin-flattened `this` (file
organization, not encapsulation)" — while separately flagging that the collision guard is real
insurance, not decoration: an earlier snapshot of the same file had zero collisions today but
NOTHING catching the first one, until a same-day fix added exactly the
`owner.has(name) → throw` guard now present in the live source [incident→verified,
`ultimate-tokens/.claude/docs/reports/reactivity-2026-08-20/00-synthesis.md` H2 finding,
re-verified directly against `src/ui/app.js:2551-2555` current source, which now throws on a
duplicate own-property name across composed mixins — the report's "no guard" claim is
correction-worthy as of this pack's own authoring date, not a live gap].

The contrast is the point: gen-ui-kit's and agent-ui's traits are file-organization AND
encapsulation (each instance owns its own closure/cleanup, namespace-checked in gen-ui-kit's
case); the mixin approach is file-organization ONLY (`this` is genuinely shared, so a name
collision is a live class of bug the composer must guard against by hand, exactly as the
retrofitted throw now does).

## Practical guidance

- **Prefer a host-agnostic factory/function over a mixin when composing cross-cutting behavior
  onto a web component** — it keeps per-attachment state isolated (no shared `this` to collide on)
  and makes teardown an explicit, individually-callable contract.
- **If a mixin-onto-one-prototype approach is chosen anyway** (e.g. for genuine file-organization
  reasons on a large single-class app), a same-name collision across mixins needs a mechanized
  guard from day one — it is cheap insurance against a defect class that produces no symptom until
  the first collision actually happens.
- **"Host-agnostic" is a real, checkable property, not a description** — ask whether the SAME
  trait/behavior unit can attach to two structurally different host types without modification; if
  yes, the design achieved it (both gen-ui-kit's and agent-ui's traits pass); if the unit only
  works because it assumes a specific base class or a specific flattened prototype's `this`, it
  hasn't.

## Boundary

This file covers the trait/behavior-composition PRIMITIVE itself — what shape it takes, how
instances stay isolated, and the mixin contrast. It is not a catalog of individual traits (see the
live `traits/index.js` barrel for that) and not the reactivity kernel a trait's own `setup()` might
use internally (`signal`/`effect` mechanics are `reactivity-facts`' law).
