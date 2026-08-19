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
`CATALOG_FACTORY_MISSING`; see `references/factory-and-widget-resolution.md`).

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

---

## UPDATE 2026-07-08 — the residue guard (the seed-and-drain hardening, chart wave M1-d)

Seed-and-drain gained its missing negative half: the exclusion allowlist now carries a standing
**residue assertion** — every allowlisted type must be ABSENT from the catalog keys — driven
through an extracted predicate (`allowlistResidue`) that a synthetic negative control proves BITES.
Without it, a drained-but-not-removed seed stays silently green forever (the type is
catalog-covered, so the coverage checks pass; the stale entry sits inert). Lesson: a stopgap set
needs BOTH directions gated — "nothing missing" AND "no residue" — and the standing gate must call
the same predicate the negative control proves, never a parallel assertion form (two forms drift).

---

## UPDATE 2026-08-19 — three admission-design tests: mint-vs-compose (both directions), the smallest-floor, and chrome ownership

**[verified]** 2026-08-19 against the ADR texts fetched verbatim from `kimgranlund/agent-ui`
(ADR-0201, ADR-0107, ADR-0205 — all `accepted`) and GH #1332's ruled Findings (commit `46d0d4e7`,
landed via PR #1404). Coverage says every shipped control is catalogued; these three tests decide
what gets to EXIST as vocabulary in the first place.

**Mint-vs-compose runs in BOTH directions.** The standing test (ADR-0175's reference, applied in
ADR-0201's Context) asks whether a recurring payload shape earns a minted component or stays a
composed grammar pattern. The forward direction is familiar; the REVERSE direction is the one
answerers miss: **a composed grammar pattern is RETIRED by a mint when one of its laws becomes
enforceable by construction.** Worked instance — ADR-0201's `ui-description-list`: the receipt
lived as a taught composition (Column of label/value Rows, GH #1174, "written to be superseded")
with three structural weaknesses — the empty-value omission law was PROMPT-enforced only, the
gap/align rhythm was re-derived per payload (drift the validator cannot see), and a 6-field receipt
cost ~19 nodes. The mint moved the omission law into `cleanDescriptionRows` (a valueless row is
now UNREPRESENTABLE — dropped before it exists as property state), made the rhythm CSS, cut the
payload to 1 node + 6 bindable data entries — and the grammar clause was repointed in ONE edit,
its surviving laws (producer-side humanization, sentence-case headers, never `justify: between`)
riding the new clause verbatim. Answer conduct: when a composition pattern's laws keep being
violated by producers, that is a MINT signal, not a teach-harder signal.

**The smallest-floor-that-earns-the-name scoping test — two worked instances.** When a family's
scope explodes at a known cliff, v1 admits the SMALLEST vocabulary that still earns the type's
name, and every escalation is fenced as a NEW intake. ADR-0107 drew the fence (charts: axis-free
`Sparkline` + `BarChart`; "any axis-bearing type is a new intake"); ADR-0205 is that named intake
arriving — and it ran the same test AGAIN one level down: the smallest axis vocabulary that
distinguishes `LineChart` from `Sparkline` is a baseline line + always-shown min/max labels,
single-series only — because multi-series drags a legend (multiple unlabeled one-color lines are
not an accessible encoding) and a legend is the NEXT escalation the fence exists to hold.
"Shipping multi-series without a legend would be a silent accessibility regression; shipping it
WITH a legend re-opens exactly the scope explosion" (ADR-0205 cl.2). The floor is honest, not
minimal-for-its-own-sake: min/max labels are mandatory precisely because an axis-bearing chart
with no visible axis values would not earn the name.

**NESTED_ONLY vs browsable: the discriminator is CHROME OWNERSHIP, not family membership.** The
composite-exemption above says sub-parts are parent-declared; the site-tier question "does this
type get its own browsable card?" has its own ruled test (GH #1332 Findings, 2026-08-19): a type
whose visual identity is owned by its HOST's token chain has no standalone identity BY RULED
ARCHITECTURE and folds into its owner's card. `Segment` folded — `segment.css` deliberately owns
zero chrome (every sized value is the host segmented-control's own token chain, ADR-0095 cl.3), so
a standalone Segment card rendered bare text and `checked` painted nothing, in BOTH render modes.
`Radio` is the deliberate contrast that STAYS browsable: `radio.css` owns its own ring + dot, so a
lone Radio is standalone-legible — same family shape, opposite verdict. The catalog row is
untouched either way (Segment stays a parent-declared wire type like `Option`/`Tab`); NESTED_ONLY
is a SITE/browse disposition, not a wire one.
