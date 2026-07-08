# The declared flavor — React + Tailwind + shadcn/ui

**This is the standing decision for every Figma Make bundle this skill authors.**
Figma Make's own ecosystem preference is React + Tailwind + shadcn/ui — not the
generic `--{category}-{role}` + hand-rolled Tailwind classes shown as illustrative
examples in the platform's docs (`format.md` §2.1 named this gap). Declaring the
real target stack resolves it: **we don't compete with shadcn's vocabulary, we compile
into it.** Ground truth for the mechanism: NONOUN Ultimate Tokens already emits a
correct, working shadcn stylesheet (`shadcn/*.css` in the token export) — this
document generalizes that into the skill's standing method.

## The upstream-integration answer

The question this resolves: *how do we integrate so we're upstream of React/Tailwind/
shadcn, seamlessly?* Answer — **by generating the exact file that stack already
expects, so the model never translates anything:**

```
canonical model (Ultimate Tokens grammar, OKLCH, this skill's usual reduction)
        │
        │  compile — deterministic, same discipline as every other platform target
        ▼
styles.css  (real shadcn CSS-variable shape + a Tailwind v4 `@theme inline` block)
        │
        │  import — one line, zero translation
        ▼
Figma Make's generated React/Tailwind/shadcn code
```

The canonical `{prefix}-{family}-{slot}` model stays the authoring source of truth —
richer, more expressive, shared with the Claude/Stitch siblings. shadcn's own ~20-role
vocabulary is the **compiled projection**, not a competing grammar to author in
directly. This is the same core+profiles principle the whole estate already runs on;
Figma Make was simply missing its correct profile.

## The exact shadcn shape (verified against NONOUN's own working export)

```css
:root {
  --radius: 0.75rem;
  --background: oklch(…); --foreground: oklch(…);
  --card: oklch(…); --card-foreground: oklch(…);
  --popover: oklch(…); --popover-foreground: oklch(…);
  --primary: oklch(…); --primary-foreground: oklch(…);
  --secondary: oklch(…); --secondary-foreground: oklch(…);
  --muted: oklch(…); --muted-foreground: oklch(…);
  --accent: oklch(…); --accent-foreground: oklch(…);
  --destructive: oklch(…); --destructive-foreground: oklch(…);
  --border: oklch(…); --input: oklch(…); --ring: oklch(…);
  --chart-1: oklch(…); /* … through --chart-5 */
  --sidebar: oklch(…); --sidebar-foreground: oklch(…);
  --sidebar-primary: oklch(…); --sidebar-primary-foreground: oklch(…);
  --sidebar-accent: oklch(…); --sidebar-accent-foreground: oklch(…);
  --sidebar-border: oklch(…); --sidebar-ring: oklch(…);
  /* extension roles — the brand's signature/intent families shadcn's base set has
     no slot for; same mechanism, same @theme inline mapping, just more of it */
  --spotlight: oklch(…); --spotlight-foreground: oklch(…);
  --beam: oklch(…); --beam-foreground: oklch(…);
  --mirror: oklch(…); --mirror-foreground: oklch(…);
  --success: oklch(…); --success-foreground: oklch(…);
  --warning: oklch(…); --warning-foreground: oklch(…);
}

.dark {
  /* same variable names, dark-scheme values — shadcn's mechanism is a CLASS
     TOGGLE, not light-dark(). This is a deliberate, named departure from this
     skill family's usual runtime idiom (see "What changes" below). */
}

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --font-sans: /* body voice, first-choice family + fallback stack */;
  --color-background: var(--background); /* …one line per role, base AND extension… */
}
```

**Wiring (`setup.md`):** *"Import `styles.css` directly into the app's global CSS
entry. Do NOT add `@source` rules for this package in the consumer's Tailwind
config — the tokens arrive pre-mapped through `@theme inline`."* No ThemeProvider is
required; dark mode is the `.dark` class on `<html>`/`<body>`, toggled by whatever
mechanism the generated app already uses (`next-themes` or equivalent) — this bundle
supplies the values, not the toggle.

## What changes from this skill family's usual doctrine, and why

Four deliberate, named departures — each is a platform-specific override, not a
correction to the universal spec (Stitch and Claude Design keep their own mechanisms
unchanged):

1. **Dark mode is `.dark` class-toggle, not `color-scheme` + `light-dark()`.** The
   `light-dark()` runtime idiom taught elsewhere in this estate has no foothold in
   the shadcn/Tailwind ecosystem — its own tooling (theme toggles, `next-themes`,
   every real shadcn theme in the wild) is built around class-scoped variable
   overrides. Fighting that convention costs real integration friction for zero
   benefit; adopt it instead.
2. **States are Tailwind modifiers, not separate tokens.** No `--primary-hover` /
   `--primary-active` custom properties — the generated code expresses them as
   `hover:bg-primary/90`, `active:bg-primary/80` (opacity/brightness modifiers on the
   base token). The *fact* of a hover/active state is still mandatory (R3 still
   applies: states ship as values, never adjectives) — only the *carrier* changes,
   because that's the idiom this ecosystem's own components already use.
3. **Components are shadcn's own component API, not bespoke CSS.** Button anatomy
   guidance stops being "padding 12px, radius `md`" (shadcn's `<Button>` already
   bakes that in from `--radius`) and becomes a **variant map**: `variant="default"`
   ↔ primary, `variant="destructive"` ↔ danger, `variant="secondary"` ↔ secondary,
   `variant="outline"`/`"ghost"`/`"link"` for neutral/quiet actions. Describing raw
   padding for a component whose padding is already baked into an installed
   component is redundant guidance the model has to reconcile against what it
   actually imports — remove the redundancy, name the variant instead.
4. **Extension roles ride the same mechanism, not a parallel one.** Signature/brand
   families and status intents shadcn's base ~20 roles don't cover (this system's
   equivalent of "spotlight/beam/mirror" plus `success`/`warning` — shadcn ships only
   `destructive`) are added as **more top-level pairs in the same file**, mapped
   through the same `@theme inline` block — never a second token system, never a
   different naming convention for "the roles shadcn forgot."

## What stays exactly as this skill family always requires

- **Terminal values, measured on-colors per fill per scheme** (R1) — unchanged; the
  five verification lines above are exactly this rule applied to the extension roles.
- **15–25 role budget, signature colors survive the cut** (R2/token-grammar) —
  unchanged; a `.dark` block is still a *scheme pair*, not a transform.
- **Prose–token accord** (R5) — the Overview/Colors prose in `Guidelines.md` still
  narrates every role, boundary, and refusal; it just points at shadcn's names now.
- **All-pairs contrast ≥ 4.5:1, both schemes** — unchanged, still the gate of record
  since Figma Make validates nothing.

## Checklist addition (until the checker script is updated — see gates.md TODO)

- `styles.css` present, real shadcn variable names, `.dark` class block, `@theme
  inline` mapping — base ~20 roles plus every extension role this theme needs.
- `setup.md` present with the import + no-`@source` instruction verbatim.
- Every component file names shadcn variant props, not raw padding/radius CSS.
- Extension roles: contrast-verified both schemes, named in prose with a boundary
  and a refusal, mapped in `@theme inline` exactly like the base set.
