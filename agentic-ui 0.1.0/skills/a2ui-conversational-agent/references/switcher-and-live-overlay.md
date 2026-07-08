# The in-chat switcher & the dev-only live overlay

> Axis: the in-chat provider→model picker, how it renders from the same registry the proxy
> enforces, and how the whole live overlay (transport + switcher) is reached only through a
> DEV-guarded dynamic import so `vite build` tree-shakes it out. Grounded in
> `site/lib/provider-switcher.ts`, `site/lib/live-proxy-transport.ts`, `site/pages/a2ui-live.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R9/R12/N2). ADR-0069 = the layered
> demo shape; ADR-0073 = the registry as single source of truth. Verified against source as of 2026-07-07.

## The switcher renders FROM `providers.json` (SPEC-R12)

`mountSwitcher(slot)` builds a provider dropdown + a model dropdown and returns a `SelectionRef`
whose `.get()` yields the current `{provider, model}` (`provider-switcher.ts:67`, `141`).
**Claim — it renders from `providers.json`, the SINGLE source of truth — no hand-listed second
menu** (`provider-switcher.ts:17`, `36`, `94-97`). **Claim — `implemented: false` providers render
disabled/greyed ("coming soon"), never selectable** (`provider-switcher.ts:50`, `96`; SPEC-R12).
**Why:** the switcher's menu is a subset of the proxy's allowlist by construction (same registry),
so it can never offer a pair the proxy would reject with a 400 (see
provider-model-seam-and-trust-boundary). The selection persists to `localStorage`
(`LS_KEY = 'a2ui-live-provider-selection'`), restored only if still a valid, `implemented` pair
(`provider-switcher.ts:37`, `71-81`). **Caveat:** corrupt or unavailable storage falls back to the
registry defaults silently (`provider-switcher.ts:79-89`).

## It dogfoods `ui-select`, not native `<select>`

**Claim — the switcher uses the fleet's own `ui-select`** (Kim's directive: no native `<select>`
where a `ui-*` control exists), so options are `[role=option]` light-DOM children appended BEFORE
connect, selection is read/written via the `value` property, and commit fires the **`select`**
event (NOT `change`) (`provider-switcher.ts:15`, `43-52`, `92-98`, `117-120`). The `label`
attribute is the accessible-name seam (ADR-0085), naming the control without a wrapping `ui-field`.
**Caveat — the model dropdown is rebuilt fresh on a provider change**, not mutated in place:
`ui-select` moves its `[role=option]` children into its internal listbox ONCE at first connect and
does not observe post-connect child mutations, so a `replaceChildren()` on the live host would
clobber its parts. The switcher builds a new `ui-select` and swaps it in
(`provider-switcher.ts:100-134`).

## The live transport reads the selection per turn (SPEC-R12)

`createLiveProxyTransport(selection)` takes the `SelectionRef` and, on each `turn`, reads the
CURRENT selection and POSTs `{ input, provider, model }` to the dev proxy at `/__a2ui/agent`, then
reads the streamed ndjson and re-yields it **line by line so the browser transport is identical to
the recorded backbone** (`live-proxy-transport.ts:37-70`, esp. `40-45`, `49-50`). **Claim — the
selection is sent with EVERY turn** (SPEC-R12), via a ref indirection so the page can swap the
selection without reconstructing the transport (`live-proxy-transport.ts:30-36`). **Failure mode:**
a non-OK response or a null body throws (`live-proxy-transport.ts:46-48`); the page catches it and
shows a system message rather than a broken render.

## The overlay is reached only DEV-guarded → tree-shaken from the build (SPEC-N2)

**Claim — the entire live overlay (proxy transport + switcher) is dev-only.** `wireLiveOverlay()`
returns early unless `import.meta.env.DEV`, then dynamically `import()`s
`../lib/live-proxy-transport.ts` and, only if `probeLive()` reports available, `../lib/provider-switcher.ts`
(`a2ui-live.ts:279-300`). Because both are reached through a DEV-guarded dynamic import, `vite build`
tree-shakes them out entirely — SPEC-N2's belt-and-suspenders proof is a `dist/` grep for key/overlay
patterns returning zero hits (SPEC-R9 AC2 / R10 AC1). **Claim — the static built site ships the
backbone alone, with no switcher at all** (`a2ui-live.ts:280-282`; SPEC-R12).

`probeLive()` GETs `/__a2ui/agent/status` and returns `{ available, providers }`; **any error ⇒ not
available** (a production build has no proxy, so the fetch fails and the page runs the backbone —
`live-proxy-transport.ts:19-28`). On no key the proxy answers `available: false` and the page shows
"Recorded backbone (no live API key found)…" (`a2ui-live.ts:293-294`).

## The swap itself is one line

When the overlay is available, `wireLiveOverlay` mounts the switcher and reassigns the module-scoped
`transport = overlay.createLiveProxyTransport(selection)` (`a2ui-live.ts:288-292`) — the same
zero-edit seam swap covered in agent-transport-seam. `Reset` re-probes so a session can pick the
overlay up after start (`a2ui-live.ts:268`).

## What this file does NOT cover

The seam the transport swaps on (agent-transport-seam) · the proxy that answers `/status` + `/agent`,
`resolvePair`, and where the key lives (provider-model-seam-and-trust-boundary) · the loop that
produces the streamed lines (produce-loop) · `ui-select`'s own contract (the components fleet, not
this pack) · `ProviderSelection` on the turn model (turn-session-and-input-intent).
