# Coverage policy & drift gates

What the default catalog is obligated to cover, and how CI enforces it. Sourced from ADR-0087 (the
whole-fleet policy flip), the fleet-derived gate in `catalog/default/index.test.ts`, and catalog
SPEC-N2 / SPEC-R3 AC3 / §5.2.1. All paths relative to `packages/agent-ui/a2ui/src/`.

## The policy: whole-fleet or gate-encoded-allowlisted

Under ADR-0087 the default catalog covers the WHOLE shipped `ui-*` fleet: every shipped control
(`components/src/controls/*/*.md`) resolves to a catalog component type, OR sits on the exclusion
allowlist with a recorded reason + citation (SPEC-N2; ADR-0087 Decision). The allowlist is the ONLY
sanctioned form of "absent" — no silent dead types, no silent uncatalogued controls, no reliance on
a per-type `experimental` marker (SPEC-N2).

**Why it flipped** (ADR-0087 Context): coverage used to "track the family" (a subset), written when
only Button/TextField/the G9 containers had shipped. Three realities made the subset a defect for
robust App usage: (1) the fleet outran the catalog silently — `ui-icon`/`ui-menu`/`ui-popover`/
`ui-tooltip` shipped uncatalogued, a live SPEC-N2 violation; (2) the old gate couldn't catch it; (3)
the controls were built expecting inclusion (their descriptors already carried catalog comments).
Kim's directive: *"try to keep EVERYTHING in the catalog."*

## CI-silent vs fleet-derived gate

There are two ways to write a coverage gate, and only one actually catches drift:

- **CI-silent (the OLD gate, removed):** a hand-frozen name list —
  `expect(catalogKeys).toEqual([...19 names])`. It can NEVER fail when a shipped-but-uncatalogued
  control lands, because the expected set is hand-maintained. The drift it exists to prevent is
  exactly the drift it cannot see — icon/menu/popover/tooltip drifted in unnoticed (ADR-0087 Context
  + Alternatives; `default/index.test.ts:76-83`).
- **Fleet-derived (the NEW gate):** DERIVE the expected type-set from the shipped-descriptor glob
  itself — the same source of truth SPEC-N2 already trusts (`site-coverage.test.ts`'s walk).
  `fleetPrimaryTypes()` walks `controls/*/*.md`, reads each `tag:` frontmatter scalar, maps
  `ui-{kebab}` → PascalCase (`default/index.test.ts:119-134`), subtracts the allowlist, and asserts
  the remainder is present in BOTH `catalog.json` AND the factory table
  (`default/index.test.ts:166-171`). A shipped-but-uncatalogued, unallowlisted control FAILS CI.

**The rule of thumb:** a coverage gate whose expected set is HAND-MAINTAINED re-earns the blind spot
it was built to close. Derive the expected set from the same artifact the policy is about (ADR-0087
Alternatives — "the gate must derive from the fleet or it re-earns its blind spot").

## The `EXCLUSION_ALLOWLIST` and the `typesMissingCatalog` predicate

- `EXCLUSION_ALLOWLIST` (`default/index.test.ts:142`) is a `Map<type, reason>`. It landed EMPTY —
  all four ADR-0087 forks resolved INCLUDE (Kim, 2026-07-06) and every fork-deferred type drained
  across Waves A/B/C (`index.test.ts:136-142`). A future undispositioned control re-seeds it with a
  reason + citation.
- `typesMissingCatalog(expected, catalogKeys, allowlist)` (`default/index.test.ts:147-153`) is the
  pure predicate the gate runs — the types covered by NEITHER the catalog NOR the allowlist. Being
  pure, it is driven by SYNTHETIC negative controls that prove the gate BITES (not a vacuous pass):
  `['ZzFake']` with an empty catalog ⇒ `['ZzFake']`; a real catalogued `'Button'` ⇒ `[]`; a fake
  mixed into the real fleet run ⇒ caught (`default/index.test.ts:174-181`). Always ship the negative
  control — a coverage gate with no proof it can fail is a green light with the bulb removed.

## Seed-and-drain rollout

A fleet-derived gate goes RED the instant it lands if the rows don't yet exist. ADR-0087 took the
**seed-and-drain** path (the `site-coverage.test.ts` `KNOWN_UNDOCUMENTED` precedent): land the gate
FIRST with the allowlist seeded to every not-yet-catalogued type (green from day one), then each wave
DRAINS its types from the allowlist as it adds the rows — so drift is CI-visible throughout the
build, not only at the end (ADR-0087 Consequences). The rejected alternative — land the gate LAST —
leaves drift CI-silent for the whole build (ADR-0087 Alternatives).

## Forward-only, and the composite-exemption

The fleet-derived gate is FORWARD-ONLY: fleet primary types ⊆ catalog types (minus allowlist).
Composite sub-types (`Option`/`Tab`/`TabPanel`/`CardHeader`/`CardContent`/`CardFooter`, and
`MenuItem`/`Radio`) are **parent-declared and exempt** from the fleet derivation (SPEC-N2; ADR-0087
Consequences). The REVERSE direction — "no extra catalog type without a factory" — is guarded
separately by the catalog↔factory bijection (`factories.test.ts` + `registry.register`'s
`CATALOG_FACTORY_MISSING`; see [[factory-and-widget-resolution]]).

- **`Radio` is NOT exempt.** `ui-radio` ships its own descriptor (`radio.md`), so it enters the
  fleet-derived set directly and needs a real row — unlike `Option`/`MenuItem`, which never ship a
  descriptor (the Wave A reviewer correction, `factories.ts:337-348`; SPEC §5.2 RadioGroup row).

## `Image`/`Video` — documentary-only, NOT in the code set

`Image`/`Video` are the one §5.2.1 allowlist row, but they are documentary-only — NOT in the code
`EXCLUSION_ALLOWLIST` (`default/index.test.ts:138-141`). No `ui-image`/`ui-video` descriptor exists,
so they never enter the derived set; the doc row exists only so a reader isn't left wondering where
media types went (SPEC §5.2.1). Distinguish this from a fork-deferred allowlist entry: an
allowlist entry names a SHIPPED control deliberately left uncatalogued; `Image`/`Video` name a
control that doesn't exist yet.

## Answering "why is this control uncatalogued?"

Route the question by the gate: (1) does a `controls/{x}/*.md` descriptor exist? If no → it's not
shipped, so it's out of scope (like `Image`/`Video`). (2) If yes and it's uncatalogued → the gate
should be RED; either it's on `EXCLUSION_ALLOWLIST` with a reason, or it's a live SPEC-N2 violation
to fix by adding the row (a job for the `a2ui-builder` agent — see the SKILL boundary).
