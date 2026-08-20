# The no-DI four-substitute taxonomy — zero context APIs across four repos

None of the four field-report corpora ground a framework-level dependency-injection container or
a formal context-provide/consume protocol. Each repo independently reaches for one or more of the
same four substitutes. All claims [verified] against the cited report/file unless marked
[incident].

## Zero context APIs, confirmed independently in all four repos

- **agent-ui:** "No formal, general context protocol exists. No Lit-style provide/consume, no DI
  container, no `useContext`-shaped lookup." Three structurally unrelated point solutions exist
  instead (an event-registry for forms, ADR-0050; a direct imperative signal push for field
  labelling, ADR-0051; pure CSS cascade for theming, ADR-0117) — and ADR-0050's own named
  re-evaluation trigger ("if a second context consumer appears, adopt the community
  `context-request` protocol") was never pulled when the second provider-shaped control (theming)
  shipped ~8 days later. — `data-model-review-2026-08-20/framework-state-idioms.md` "Context-providing
  verdict", Gaps #1 [verified]
- **gen-ui-kit:** "There is no context-request protocol, no provider/inject DI, and no shared app
  store anywhere in web-modules — zero hits for `context-request`/`ContextProvider` in
  web-components or web-modules source." — `2026-08-20-reactivity-review/02-web-modules-state.md`
  §4 [verified]
- **adia-v2:** "No framework DI exists (expected — vanilla TS/Astro), and there's no single
  substitute pattern either. Each cross-cutting concern picked its own mechanism." —
  `2026-08-20-reactivity-data-audit/04-context-di-patterns.md` Verdict [verified]
- **ultimate-tokens:** a `mixinInto` helper flattens six mixin files' prototype methods onto one
  app prototype with "no interface, no explicit import of 'the methods I depend on' — every mixin
  file just calls `this.whatever()` and trusts it exists somewhere in the final flattened
  prototype." The module boundary (`sections/*`, `overlays/*`) is "a file-organization boundary,
  not an encapsulation boundary" — an explicit, acknowledged trade-off (TKT-0023), not an
  accident, but it means a reader of one overlay file alone cannot know which of its ~15 `this.*`
  dependencies are guaranteed to exist without reading every other mixin file too. —
  `reactivity-2026-08-20/04-context-and-messaging.md` §C [verified]

## The four substitutes actually used in place of DI

### 1. Typed handles

A small, typed object passed down that carries a capability (a method, a lifetime) but
deliberately zero application data — the caller gets exactly the seam it needs, nothing more.

- gen-ui-kit: "Dependency injection is property assignment by the host" — an admin shell's
  `renderer` and `runTurn` are host-injected properties on the consuming element; the consumer
  "never imports `@genui/renderer`... the HOST builds the renderer and hands it in." —
  `02-web-modules-state.md` §4 [verified]
- agent-ui: `RenderContext` (`{effect(fn)}`) is "a minimal seam so a per-hole directive installs
  effects under the HOST's scope — carries zero data, purely a lifetime handle." — ADR-0023, per
  `framework-state-idioms.md` sanctioned-idioms table [verified]

### 2. Re-derive helpers

Read fresh from the ambient source at each call site rather than resolving once and passing the
result down — trades a shared reference for "any caller can always get a correct current value
with no invalidation to manage."

- adia-v2: `getEnv(key, fallback)` is "a module-level pure function — no caching, no singleton;
  every call site re-reads `globalThis._env_`/`import.meta.env` fresh. This is 're-derive from
  source every time,' not 'read once and pass down.'" 30 files call it directly; it is "the ONE
  consistent mechanism in this audit... works because env values are static per build/runtime and
  never need to invalidate a subscriber." — `04-context-di-patterns.md` §1 [verified]
- The same repo shows the failure mode of re-deriving WITHOUT sharing the helper: three separate
  REST clients each hand-roll an identical local `getPracticeId()` re-reading
  `VITE_DEFAULT_PRACTICE_ID` with the same fallback literal, rather than importing one shared
  function — "known, temporary, and not yet centralized," by the client module's own comment. A
  re-derive helper is only a clean substitute when there's exactly ONE of it; three independently
  duplicated copies of the same re-derive logic is the drift this taxonomy exists to catch. —
  `04-context-di-patterns.md` §3 [verified]

### 3. Callback injection

Push the resolution decision to whoever mounts the consumer, as a plain function reference, rather
than having the consumer resolve its own dependency.

- adia-v2: two shared UI picker components take a `getPracticeId: () => string` callback at
  `mount()` time rather than resolving practice id themselves — "pushing the resolution decision to
  whatever page mounts the picker," which in turn calls one of that repo's several practice-id
  resolution strategies. — `04-context-di-patterns.md` §3, item 5 [verified]

### 4. Documented soft globals

A module-scope singleton, explicitly disclosed as such in its own documentation or ADR, rather
than a silent unstated global.

- agent-ui: `@agent-ui/data`'s default store and `ADR-0115`'s `defaultRouter` are named in the
  report as "module-level 'soft globals' for cross-package concerns... both documented as such." —
  `framework-state-idioms.md` "Context-providing verdict" [verified]
- gen-ui-kit: the `STREAMS` registry (`core/data-stream.js`) is exactly this shape — a
  module-scope `Map` shared across the whole document, with a deliberately exported read-only view
  (`streams.get/has/keys/size`) rather than a silent unexported global. — `02-web-modules-state.md`
  §4, `core/data-stream.js:77-85` [verified]

## Reading this taxonomy against a live codebase

None of the four is wrong in isolation — each repo's report treats its own point solutions as
reasonable choices given no framework DI exists. The recurring gap this taxonomy names is
CONVERGENCE, not the substitute itself: agent-ui's own re-evaluation trigger for a formal context
protocol was written down and never checked (`framework-state-idioms.md` Gaps #1); adia-v2's
practice-id re-derive helper is duplicated three times instead of shared once
(`04-context-di-patterns.md` §3). When auditing a codebase against this pack, the question is
never "which of the four substitutes is correct" — it's whether the SAME substitute, once picked
for a concern, is actually the one thing consumed everywhere that concern appears.
