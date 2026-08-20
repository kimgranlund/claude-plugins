# The postMessage bridge protocol, and the busy-flag reset rule

Source: `ultimate-tokens` `.claude/docs/reports/reactivity-2026-08-20/04-context-and-messaging.md`
(scope: `src/ui/app.js`, `overlays/{drawer,apply-gate,settings}.js`,
`scripts/gen-figma-ui.mjs`, `figma/plugin/code.js`). Verdict up front, quoted from the report: "one
designed protocol for the bridge itself (well-versioned, mostly symmetric), sitting inside an
accumulated, un-systematized context layer." [verified] unless marked [incident].

## The dispatcher shape

A sandboxed plugin bridge (UI iframe ⇄ a sandboxed execution context, here Figma's plugin sandbox)
routes through exactly ONE inbound dispatcher on each side — every message lands on one
`window.onmessage`/`figma.ui.postMessage` handler, unwraps its typed payload, and calls one
`app().<method>()` (or the sandbox-side equivalent). There is no second, parallel message channel
for the same concern — a UI-less, standalone command surface in the same codebase is confirmed
entirely out of this protocol's scope, not a hidden second bridge. — report §A [verified]

## Symmetric request/reply pairs

Each UI→sandbox request (`parent.postMessage({pluginMessage:{type}}, "*")`) names its own reply
type, and the report finds this DISCIPLINED, versioned by ticket as the codebase grew (e.g. one
ticket added a new read-type + reply pair, another added a rename's request/reply plumbing) — a
designed protocol, not organic accretion, "it reads like something someone sat down and
specified." — report §A, §E [verified]

**The one designed exception — a guaranteed-reply carve-out for the highest-stakes request.** The
sandbox side's outer error handler (`code.js`'s catch, lines 203-211) explicitly special-cases the
`apply` request type to post an `apply-error` reply even when the handler itself throws — every
OTHER request type's failure path (e.g. `sweep-scan`, `sweep-delete`) only surfaces a side-channel
`figma.notify(...)` toast, never a matching reply message. — report §A [verified]

## The rule this protocol's own gap teaches: every busy flag needs a guaranteed reset path

A request/reply pair that gates a busy flag (disables a control, blocks re-entry) is only safe if
EVERY exit path from the corresponding handler — success, a caught error, AND an uncaught throw —
posts the reply that clears the flag. The bridge's own inventory found this true for 4 of 5
in-flight flags, and false for the 5th:

- **Covered correctly (4 of 5):** `_applyBusy` is cleared on both `apply-done` and `apply-error` —
  the latter guaranteed by `code.js`'s special-cased catch above, not because the handler simply
  "shouldn't" throw. `_figmaProbed` and `_figmaFontsRequested` are correctly one-shot latches by
  design (never reset, because each operation is meant to fire exactly once per session) — not a
  wedge, since they were never meant to reset. `_loadRequested` resets on every exit path
  (success and both catch/no-raw branches). — report §B [verified]
- **NOT covered (1 of 5) — a real, confirmed incident:** `sweepBusy` is set before sending
  `sweep-scan`/`sweep-delete`, but `code.js`'s handler for BOTH has no equivalent special-cased
  catch — if `figma.getLocalTextStylesAsync()`/the sweep/delete logic throws inside the sandbox
  handler, the catch only fires `figma.notify(...)`, never posts `sweep-scanned`/`sweep-done`.
  Effect: `sweepBusy` is set and never cleared; the Cleanup panel's Scan/Delete buttons stay
  disabled **permanently for the rest of the session** (a fresh plugin open is the only reset,
  since the flag is a constructor default). This is not hypothetical — the report confirms it as a
  live, reproducible bug, distinct from the `_figmaProbed`-class documented one-shot latch. —
  report §B, §E [incident]

**The generalizable rule, stated by the report's own verdict:** the busy flags were "added
independently over several tickets with no shared 'every flag has a guaranteed reset path' rule
(four out of five happen to be fine ... because the rule was never written down to check
against)." Treat "does every exit path — success, caught failure, AND uncaught throw — post the
reply that clears this flag" as a checklist item at design time for any new request/reply pair that
gates a busy/disabled state, rather than discovering the gap after a control wedges in production.
— report §E [verified]

## What doesn't need this rule

A request/reply pair with no busy flag — just "overwrite state on reply, nothing gates on it" —
doesn't need a guaranteed-reset path at all: a lost reply there leaves stale or null data, never a
stuck disabled control. Reserve the guaranteed-reply-on-every-exit-path discipline for pairs that
actually gate a busy flag or disable a control; a plain read-and-overwrite pair is lower stakes by
construction. — report §B [verified]
