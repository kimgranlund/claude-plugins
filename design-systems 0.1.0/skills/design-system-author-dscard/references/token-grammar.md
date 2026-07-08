# The Ultimate Tokens Naming Grammar

Naming standard for every color token in a Claude Design export bundle.
Source: derived from the design-system-files-for-llms spec §6.5 (adopted 2026-07-05)
and its reference implementation, NONOUN Ultimate Tokens ("Studio 54 · the dancefloor").
The snapshot embedded here is authoritative at runtime; re-derive from the upstream
spec on a version bump. This file owns the role budget (15–25); companions:
`dialect.md` (where the names appear), `gates.md` (what verifies them).

**Every color token is constructed, never invented:**

```
--{prefix}-{family}-{slot}
```

The family name alone denotes the base fill (`--c-danger`, `--c-primary-base`).

## Prefix — host-owned, adaptive

One prefix per corpus, stated once (reference implementation: `c`, so `--c-primary-base`).
In a host system carrying another prefix (`--md-sys-*`, `--color-*`), swap ONLY the
prefix and keep `{family}-{slot}` intact — the spine's "Token naming" section must
teach the design agent exactly this adaptivity. In non-CSS carriers (frontmatter
`colors:`, `tokens.json` maps) the keys drop the `--{prefix}-` and carry bare
`{family}[-slot]` (`primary-base-on-surface`); the CSS custom properties in previews
and emitted UI carry the full form.

## Families — an open set

Generic defaults: `neutral`, `primary`, `secondary`, `info`, `success`, `warning`,
`danger`. A theme may mint more; the reference theme carries nine:
`primary-base` (neutral-purple room), `primary-muted` (hot pink "spotlight"),
`secondary-base` (gold), `secondary-muted` (silver "mirror"), `accent-base`
(electric purple), `accent-muted` (cyan "beam"), `danger`, `success`, `warning`.
One family carries **neutral duty** (app surfaces + text); state that family in prose.

## Slots — a CLOSED registry

Construct from these categories only; a name outside the registry is a defect, not a
coinage. `×states` marks slots that may additionally suffix `-hover`/`-active`/`-disabled`.

| Category | Slots |
|---|---|
| Base fill | *(family name alone)* |
| Tone | `-dim` · `-bright` · `-low` · `-high` |
| States | `-hover` · `-active` · `-disabled` |
| On-colors | `-on-{family}` · `-on-{family}-{variant\|state}` · `-on-surface` · `-on-surface-variant` · `-on-surface-{state}` · `-on-surface-variant-{state}` |
| Text aids | `-placeholder` |
| Outlines | `-outline` · `-outline-variant` (each ×states) |
| Containers | `-container` · `-container-low` · `-container-high` (each ×states) |
| Inversion | `-inverse-surface` · `-inverse-on-surface` |
| Surfaces | `-background` · `-surface` · `-surface-{dim\|dimmest\|bright\|brightest}` · `-surface-{low\|lowest\|high\|highest}` |
| Scrims | `-scrim` · `-scrim-{weakest\|weak\|strong\|strongest}` |

## The consumption reduction is a slot SUBSET, not a new vocabulary

A reduced bundle selects roles from the registry above — every selected name exists
verbatim in the rich authoring layer, so consumption tokens and full CSS exports share
one vocabulary. The working selection:

- **Neutral-duty family (~10 slots):** `-background`, `-surface`, `-surface-high`,
  `-on-surface`, `-on-surface-variant`, `-outline-variant`, base fill, `-hover`,
  `-active`, `-on-{family}`.
- **Each accent / intent family (2 slots):** base fill + `-on-{family}`.

Role budget: **15–25 roles** (observed floor: 19). Below ~15, multi-signature brands
cannot express themselves; above ~25, role-selection reliability degrades and the
prompt budget pays for unused choices. Full tonal ramps never ship in a bundle.

## Pairing law

Text/icons ON a family fill use that family's `-on-{family}` token — which differs by
scheme (light fills typically pair with white; brighter dark-scheme fills pair with
near-black). Text on background/surface uses `-on-surface` / `-on-surface-variant`.
A crossed pair fails contrast in one scheme; the contrast gate derives its pairs from
exactly this law (see `gates.md`).

## Compat aliases — legal, documented

A plain `primary` alias of `primary-base` satisfies Stitch's required-`primary` lint
when the same DESIGN.md core is shared across platforms. Aliases are value-equal
duplicates, named in the receipt; `bundle_gates.py` detects them by value equality and
reports them as INFO, never as a missing on-partner.
