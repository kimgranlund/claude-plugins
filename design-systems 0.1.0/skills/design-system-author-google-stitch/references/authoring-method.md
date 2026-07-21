# Authoring Method — a Stitch DESIGN.md for Any Theme

How to write the file, section by section, with worked snippets. Assumes the platform facts in `stitch-spec.md`. Worked example quoted throughout: **Studio 54 · the dancefloor** (NONOUN Ultimate Tokens reference build, 2026-07-05 — lint receipt: 0 errors, 29 classified warnings). Naming grammar adopted from the Ultimate Tokens naming standard (universal design-system-files-for-LLMs spec v0.1, 2026-07-05).

## 1. Prose doctrine (write this layer first)

- **One specific reference, in the Overview.** Name a world and its physics — the worked example opens: *"A glittering 1970s nightclub at full tilt: mirror-ball silver, gold lamé, and hot pink-purple light playing over a deep black-purple dancefloor. The interface is the club — dark, calm, perceptually even surfaces carry the room, and the color arrives as light."* Everything downstream (surface ladder, signature roles, refusals) derives from that sentence.
- **Every role token appears in prose** with its role, usage boundary, and refusals — e.g. *"**Beam** `{colors.accent-muted}` — the cyan beam. Informational accents, data highlights, 'new' markers. Never a page background."* Component-level tokens may live in the Components section instead.
- **Prose promises must be token deliveries.** A brand story that sells hot pink, cyan, and silver while the tokens ship only a primary/secondary pair forces the model to hardcode or under-deliver (the classic reduction failure). If a family is cut, cut its prose in the same edit.
- **Negative constraints are first-class** and belong in Do's and Don'ts — deliberate, short, intentional: *"Disco is glamour, not kitsch — never muted '70s earth tones."* If the don't-list grows long and rambling, the Overview reference was too vague; sharpen the reference instead of extending the list.

## 2. Token naming — the Ultimate Tokens grammar

Every color token is **constructed, never invented**: `--{prefix}-{family}-{slot}`.

- **Prefix** is host-owned and adaptive (`--c-*`, `--md-sys-*`, `--color-*`); inside DESIGN.md frontmatter the prefix is dropped — keys are bare `{family}-{slot}` (`primary-base-hover`). State the project's prefix once in the Colors prose; keep `{family}-{slot}` intact under any prefix.
- **Families** are an open set. Generic defaults: `neutral`, `primary`, `secondary`, `info`, `success`, `warning`, `danger`. A theme may carry more — the worked example runs `primary-base`, `primary-muted`, `secondary-base`, `secondary-muted`, `accent-base`, `accent-muted`, `danger`, `success`, `warning`, each mapped to a brand meaning (spotlight pink, mirror silver, cyan beam…).
- **Slots** are a closed registry; the family name alone denotes the base fill. Categories: tone (`-dim`, `-bright`, `-low`, `-high`) · states (`-hover`, `-active`, `-disabled`) · on-colors (`-on-{family}`, `-on-{family}-{variant|state}`, `-on-surface`, `-on-surface-variant`, `-on-surface-{state}`) · text aids (`-placeholder`) · outlines (`-outline`, `-outline-variant`, × states) · containers (`-container`, `-container-{low|high}`, × states) · inversion (`-inverse-surface`, `-inverse-on-surface`) · surfaces (`-background`, `-surface`, `-surface-{dimmest…brightest}`, `-surface-{lowest…highest}`) · scrims (`-scrim`, `-scrim-{weakest…strongest}`).
- **Consumption files select a slot subset, never a new vocabulary**: ~10 slots on the neutral-duty family (`background`, `surface`, `surface-high`, `on-surface`, `on-surface-variant`, `outline-variant`, base, `hover`, `active`, `on-{family}`) plus 2 per accent/intent family (base, `on-{family}`). 15–25 roles total is the working band; below ~15 multi-signature brands can't express themselves, above ~25 role selection degrades and the prompt budget pays for unused choices. Full ramps never ship.
- **Teach the grammar in the file itself.** The Colors section carries a "Token naming" `###` block so the consuming agent constructs names by pattern — worked example: *"The family name alone is the fill: `--c-primary-base`, `--c-danger`. Text/icons ON a family fill: `--c-{family}-on-{family}` … Prefix-adaptive: in a host system using another prefix, keep the `{family}-{slot}` part intact and swap only the prefix."*

## 3. Scheme encoding — dark without a scheme axis

The alpha schema has one `colors` map and no dark counterpart. The pattern:

```yaml
colors:
  primary-base: "oklch(0.5585 0.0245 288.45)"
  primary-base-dark: "oklch(0.6492 0.0221 288.83)"
  primary-base-on-primary-base: "oklch(1 0 89.88)"
  primary-base-on-primary-base-dark: "oklch(0.1776 0 89.88)"
  # Stitch-compat alias of primary-base (its required `primary`); agents use primary-base
  primary: "oklch(0.5585 0.0245 288.45)"
  primary-dark: "oklch(0.6492 0.0221 288.83)"
```

- **`-dark` suffix siblings** ride the accept-if-valid rule. Invariant: **identical role inventories per scheme** — a role present in one scheme only is a build error. (A translucent token may carry the same value at both ends, like the worked example's `outline-variant` — both keys still exist.)
- **Never `light-dark()` in a value** — measured lint error. The two-ended value also has no single sRGB conversion for the contrast check.
- **The known cost**: components reference the light end, so every `-dark` sibling lints as an `orphaned-tokens` warning. Expected; classified in the receipt (`lint-gate.md`).
- **The `primary` compat alias** satisfies `missing-primary` so Stitch's agent never auto-generates key colors. Document it with a YAML comment as above; prose keeps pointing at the real role.
- **On-colors are explicit, measured, per fill, per scheme — never a constant.** The measured failure this prevents: every `-foreground` collapsed to `#FFFFFF`, and every dark-scheme fill landed at 3.1–3.7:1, below AA. Note the worked pattern: light fills pair with white; the *brighter* dark-scheme fills pair with near-black.
- **Runtime is a different layer.** The Agent Prompt Guide section may teach generated code to emit `:root { color-scheme: light dark; --c-primary-base: light-dark(<light>, <dark>); }` — that idiom lives in *prose/fenced code*, where the linter never parses it. Carrier data and runtime idiom must not be confused. Trap worth quoting: without `color-scheme: light dark` on `:root`, `light-dark()`'s second argument never fires.

## 4. Frontmatter beyond colors

- **Typography**: 9–15 levels (spec norm), voice-first names (`display-sm`, `heading-lg`, `body-md`, `ui-sm`, `caption-md`); each level binds `fontFamily` + `fontSize` + `fontWeight` + `lineHeight` together — a level is a set-together unit, never free-typed. **Leading & tracking are always relative (standing rule)**: `lineHeight` as a unitless factor (`1.5`), em, or `%`; `letterSpacing` as em or `%` — never absolute px in any carrier (`prelint.py check` errors on px; unitless lineHeight is also Stitch's own recommendation). Non-standard weights (550, 440) are legitimate with variable fonts; the prose names the fallback stack and what must survive fallback.
- **Spacing / rounded**: closed scales with named steps. Prose enforces closure — *"Compose every gap and padding from the spacing scale; a 7px or 13px gap does not exist."* Rounded gets per-tier assignments in Shapes prose: *"chips and tags `{rounded.xs}`, inputs `{rounded.sm}`, buttons `{rounded.md}`, cards and panels `{rounded.lg}`, modals `{rounded.xl}`, pills `{rounded.full}`."*
- **Components**: base entry carries the full anatomy via references; variants override only what changes:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary-base}"
    textColor: "{colors.primary-base-on-primary-base}"
    typography: "{typography.ui-md}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-base-hover}"
  button-primary-active:
    backgroundColor: "{colors.primary-base-active}"
```

  States ship as **values** (`-hover`/`-active` variant keys), never as prose arithmetic ("hover brightens slightly") — un-anchored state prose yields per-generation drift; every screen invents its own "slightly". Focus geometry (ring color, width, offset) is stated concretely in Components prose since no component property slot exists for it: *"**focus** shows a 2px `{colors.primary-base}` outline at 2px offset."*

## 5. Section-by-section content map

| §  | Section | Carries |
|---|---|---|
| 1 | Overview | the specific reference, audience, emotional register, restraint rules |
| 2 | Colors | Token-naming block · role-by-role prose with boundaries/refusals · the **pairing law** (*"Text on a family fill uses that family's `on-{family}` token — which differs by scheme… A crossed pair fails contrast in one scheme"*) · intent doctrine (status colors carry meaning only) |
| 3 | Typography | families by voice, weight-as-voice table, scale usage rules, fallbacks |
| 4 | Layout | spacing-scale closure, grid, reading measure, whitespace-over-borders |
| 5 | Elevation & Depth | surface ladder vs shadows (*"Elevation is a surface step, not a drop shadow"*) |
| 6 | Shapes | radius language + per-tier assignments; one radius language per view |
| 7 | Components | per-atom anatomy + explicit states — *"generic output betrays itself in hover/focus/disabled"* |
| 8 | Do's and Don'ts | the hard rules, ❌-style refusals first (never hardcode a color · never cross an on-pair · never stack competing primaries), then Prefer-rules |
| 9+ | Appended (tolerated) | Responsive Behavior (breakpoints, touch ≥ 44px, both schemes at every width) · Agent Prompt Guide (the work-order: tokens first → roles then scheme → scale then states → one focus per view → name by grammar) · Motion, Iconography… |

A useful opener above the sections (the H1 is unparsed): *"Read this file as your instructions — it is the prompt. Token values are normative; the prose explains how to apply them. Every color role ships a light value and a `-dark` sibling: pick the pair, not one end."*

## 6. Porting an existing system (Regenerate)

1. Inventory the upstream system: roles, values, scales, states, dark story, naming.
2. Map to the grammar; where upstream names diverge (`brand-500`, `text-muted`), **call the divergence out** in the deliverable and either alias or rename — never silently rewrite a system's made decisions. Same for payload (upstream hex stays hex if the owner prefers; note that OKLCH is verified-accepted).
3. Fill gaps by *measurement*, not invention: missing on-colors, missing dark ends, missing states are computed/verified upstream (dispatch [[make-palette]] / [[check-colors]]), then land here as terminal values.
4. Reduce prose and tokens together; run the gate loop; write the receipt.

Checklist before the gate: specific reference present · 15–25 roles, each in prose · every fill has its on-partner in both schemes · states as variant keys · `primary` alias · scales closed · canonical section order · appended sections after Do's and Don'ts.
