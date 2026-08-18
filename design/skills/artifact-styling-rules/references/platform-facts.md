# Platform facts — what the Artifact runtime itself allows and forbids

The question this file answers: **before any styling choice, what does the runtime actually let a
Claude Artifact do?** These are hard constraints, not taste — every doctrine elsewhere in this
pack works around them, never against them.

## CSP forces single-file inlining

[incident, 2026-08-18] Claude Artifacts execute under a Content-Security-Policy that blocks
external stylesheets, external font files, and (for HTML artifacts) most external script sources.
The practical consequence: **all CSS lives in one `<style>` block, all fonts are system stacks
(never a `@font-face` remote URL), and any script dependency must come from the one allowlisted
CDN** (`cdnjs.cloudflare.com` for HTML artifacts — [verified, dev.to "Ultimate Claude Artifacts
Guide", accessed 2026-08-18]). A bare custom font name with no system fallback silently renders as
the browser default with no error — this is the origin of `token-architecture.md`'s mandatory
font-fallback rule.

- **[verified, Postman "Claude Artifacts Limitations", accessed 2026-08-18]** "Everything runs in
  a sandboxed browser environment. No server-side code, no Node.js, no external API calls" —
  frontend-only execution, no filesystem access, no auth mechanisms.
- **[verified, dev.to guide, accessed 2026-08-18]** React artifacts cannot use `<form>` tags;
  `onClick`/`onChange` handlers are required instead — a hard constraint, not a style preference.

## The 16MB practical size cap

**[verified, fast.io "Claude Artifacts Guide", accessed 2026-08-18]** Artifacts have a practical
size limit of ~16 MiB; large embedded images (base64-inlined, since external image URLs are
CSP-blocked the same way fonts are) are the usual cause of publish failures. `artifact_check.py`
does not itself measure page weight (that's a build-time concern for `make-artifact`, not a
styling-doctrine grep) — named here so a styling choice (an embedded raster background, a large
inlined SVG icon set) accounts for the ceiling before it's built against.

## Viewer theme is a TRI-STATE, not a binary

**[incident, 2026-08-18]** A rendered Artifact page can be viewed in exactly three theme states,
not two:

1. **`[data-theme="light"]`** — the host UI has explicitly stamped light mode.
2. **`[data-theme="dark"]`** — the host UI has explicitly stamped dark mode.
3. **No `[data-theme]` attribute at all** — the page is being viewed with no explicit stamp, and
   must fall back to the *system* `prefers-color-scheme` signal.

This is why `token-architecture.md`'s `light-dark()` + bare `color-scheme: light dark` pattern is
the correct default (state 3 resolves automatically, no query needed), with `[data-theme="light"]
{ color-scheme: light; }` / `[data-theme="dark"] { color-scheme: dark; }` as the ONLY override
rules needed for states 1/2 — never a `@media (prefers-color-scheme)` double-block, which would
duplicate every variable and still miss nothing for state 3 (it already handles it identically)
while adding a second maintenance surface for states 1/2.

## The body-ground rule

**[incident, 2026-08-18]** The page's `body` (or outermost content root) must bind its background
to the SAME token that the page's `:root`/surface system otherwise uses (typically the
`--paper`/`neutral-background`-family role) — never left as browser default white/transparent. A
missing body-ground binding is invisible in light mode (default white happens to look plausible)
and immediately wrong in dark mode (a flash of white behind otherwise-dark content). This is
`artifact_check.py`'s `missing-ground` check.

## Inert downloads, no persistent storage

**[verified, dev.to guide + fast.io guide, accessed 2026-08-18]** `localStorage`/`sessionStorage`
are blocked in the sandbox (storage keys, where a host-specific mechanism IS exposed, are capped
under 200 chars with no whitespace/slashes/quotes, values capped at 5MB per key — a build-time
concern, not styling). A download-triggering link/button inside an artifact cannot perform a real
file-system write; treat any "Download" affordance as inert unless the host page explicitly wires
a supported mechanism. State does not survive a session close — never style a page as though it
has durable client-side memory.

## Native mermaid support

**[verified, Claude Code official docs, accessed 2026-08-18]** The Artifact renderer ships mermaid
diagram rendering natively — no CDN import, no bundled mermaid.js needed in the page's own
`<script>` block. This is why `mermaid-reference.md`'s re-theme technique targets the RENDERED
SVG's own CSS classes rather than mermaid's JS-level `themeVariables` config: the invoking page
never touches mermaid's init call directly, so a runtime-injected `%%{init}%%` block is not even
where this pipeline's diagrams get their theme from.

Extension: governed by [[make-pack]].
