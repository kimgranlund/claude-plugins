# Three-tier token taxonomy + generated theme packs with inheritance fallback

**This axis is the CSS ARCHITECTURE of a token layer — the tier boundaries, what lives where, and
how a generated theme variant relates back to the default. It is not a palette-design method (that
is the `design` plugin's `make-palette`/`token-builder`) — this pack takes a token layer's
existence as given and answers how its CSS is structured and extended.**

## The three tiers (gen-ui-kit, ADR-0002)

**[verified]** gen-ui-kit's `docs/ops/adr/adr-0002-three-tier-token-layering.md` (accepted
2026-04-24) names three tiers, each with a distinct question it answers:

1. **Primitives** — raw OKLCH ramps per color family (`colors/primitives-{family}.css`), plus raw
   spacing/radius/motion/chrome-height scales inline in `tokens.css`. Answers "what are the
   available values?"
2. **Semantics** — scheme-aware aliases (`colors/semantics.css`): `--a-fg`, `--a-bg`,
   `--a-primary`, `--a-accent-strong`. **Wrapped in `light-dark()` where applicable** (the bridge
   to `light-dark-theming.md`). Each semantic picks a primitive step; it never inlines the raw
   `oklch()` value. Answers "what's the role?"
3. **Component-scoped** — per-component tokens declared inside the component's own `@scope
   (component-name)` block as `--{component}-{prop}` (see `scoping-strategies.md`; ADR-0003's
   two-block contract). They map to semantics, never to primitives directly. Answers "what knob
   does this component expose?"

**The hop-skipping rule is enforced, not aspirational.** ADR-0002: "Component CSS **never**
references primitives directly. That hop is enforced by the `component-token-audit` skill." A
variant override targets the component tier, never the semantic or primitive tiers underneath it
— ADR-0002's own worked example repoints `--button-bg`/`--button-fg` (component tokens), never
`--a-primary` directly, inside a `[variant="primary"]` selector.

**Why not two tiers, or four?** ADR-0002's own rejected alternatives are load-bearing for this
question: two tiers (fold primitives into semantics) loses the ability to regenerate a color
family's ramp independently of its semantic assignment; four tiers (add a "transform" layer for
scrim alpha, tint/shade derivatives) is rejected because `light-dark()` already handles
scheme-aware transforms at the primitive level and scrim derivation has its own home
(`scrims.css`) — a fourth layer would add indirection with no new expressiveness.

## Generated theme packs with inheritance fallback (agent-ui)

**[verified]** agent-ui ships theme variants as **generated CSS files**, one per theme
(`packages/agent-ui/shared/src/tokens/themes/{orchid,fern,ruby,meadow,lagoon,ocean,amethyst,ember,
indigo,sky}.css`), each wrapping a full semantic re-declaration under an attribute selector:

```css
/* orchid.css — a THEME PACK (ADR-0141/TKT-0087): an Ultimate Tokens color export wrapped under
 * `[theme='orchid']`, re-declaring the --md-sys-color-* system-tier surface for any subtree an
 * ancestor `ui-theme-provider[theme='orchid']` themes. Generated — do not hand-edit; regenerate
 * via `wrap-pack.ts` from a fresh UT export. */
[theme='orchid'] {
  color-scheme: light dark;
  --md-sys-color-neutral-100: oklch(0.9571 0.0017 145.56);
  /* ...full primitive + semantic re-declaration... */
}
```

**The inheritance-fallback mechanic is the load-bearing fact of this axis.** A theme pack does
NOT re-declare every role the default `tokens.css` carries — only the ones an Ultimate Tokens
export actually supplies. `orchid.css`'s own header comment states the consequence directly:

> "Parity: the 16 hand-authored roles the default (tokens.css) carries beyond a stock UT export
> (focus-ring · neutral-tint-* · neutral-track{,-hover} · primary-selected · the raw 050/950 alpha
> triples — TKT-0087 Findings) are DELIBERATELY absent here; an element inside this themed subtree
> inherits those roles from `:root`'s default via ordinary CSS custom-property cascade — **no
> fallback mechanism needed.**"

This works because CSS custom properties are inherited by default: `[theme='orchid']` re-declares
a large subset of `--md-sys-color-*` on the themed subtree's root, but any property it does NOT
re-declare simply falls through the normal inheritance chain to whatever value `:root` (or a
closer themed ancestor) already set — no `var(--x, fallback)` chain, no explicit default
parameter, no build-time merge step. **The generation tool's own honesty about incompleteness is
what makes the fallback safe**: because `orchid.css` is generated fresh from each Ultimate Tokens
export rather than hand-maintained, a future export gaining a 17th non-standard role would surface
as a new gap in the SAME comment's parity list, not a silent drift — the generator, not a human,
is the source of truth for what a given theme pack does and doesn't carry.

**Why this differs from a "complete-clone" theme strategy.** An alternative design would have
every theme pack re-declare literally every role the default carries (copy the full `:root` block,
substitute values) — this is explicitly rejected by construction here: it would require every
theme regeneration to also re-derive the 16 hand-authored non-UT roles, coupling a
third-party-format export to house-specific extensions that export format doesn't know about.
Relying on cascade inheritance for the gap means the generator's job stays narrow (translate one
UT export to one CSS block) and the hand-authored extensions stay hand-authored in exactly one
place (`:root` in `tokens.css`).

## Sources

- gen-ui-kit `docs/ops/adr/adr-0002-three-tier-token-layering.md` — the three-tier decision, the
  hop-skipping enforcement, rejected two/four-tier alternatives.
- agent-ui `packages/agent-ui/shared/src/tokens/tokens.css` — the default `:root` tier, read
  directly 2026-08-20 (1,132 lines, full primitive + semantic + `light-dark()` role declarations).
- agent-ui `packages/agent-ui/shared/src/tokens/themes/orchid.css` — a generated theme pack, its
  own header comment stating the parity gap and the no-fallback-needed rationale, read directly
  2026-08-20.
