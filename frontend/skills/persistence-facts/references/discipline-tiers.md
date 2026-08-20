# Client-persistence discipline tiers

**The judgment call:** not every persisted value needs the same rigor, but a codebase that never
names its OWN tiers can't tell a genuinely-safe-to-reset key from one silently losing user data on
the next rename. ultimate-tokens' store survey (grounding below) found three distinct tiers
already in use side by side in one app, undocumented as tiers until this audit named them.

## Tier 1 — spec-grade: fuzzed roundtrip + schemaVersion/RENAME_MAPS [verified]

One store (the doc/palette-set serializer) is built to an actual spec: a pure `serialize`/
`hydrate` pair with a sealed, fuzz-tested roundtrip-identity + per-field-clamp invariant, a
`schemaVersion` field, and a `RENAME_MAPS` forward-translation table that lets a field rename ship
without losing every user's existing override for the old name. A dedicated allowlist-parity test
keeps the store's hand-tracked field lists honest against the engine that defines them.

## Tier 2 — ad-hoc JSON.parse: shape-checked, not spec'd [verified]

Everything else in the same app — the doc-index/gallery list, a tier/license profile blob, a
project-slot key — persists via bare `JSON.parse`/`localStorage` try/catch, with validation
deferred to the moment each record is actually consumed (a lazy-clamp-at-read pattern) rather than
enforced at the storage boundary. This is a legitimate, consistently-applied design choice, not a
defect by itself — but one tier inside it is worse than the others: a profile/flag-style blob may
have a real allowlist clamp with idempotence tests, yet carry **no rename-map mechanism at all** —
a future key rename has no recovery path, which is a harder failure than tier 1's own worst case
(tier 1 at least ships a translate-forward table on a documented rename).

## Tier 3 — cache-buster: a version SUFFIX, not a migration [verified]

A third pattern uses a literal `-v1`-style suffix baked into the storage key itself (an app-prefs
blob, a one-shot consent flag). Here "version" means "cache-buster" — bump the suffix to force
every client to re-derive from defaults — not "migratable." This is deliberately excluded from
whatever forward-rename walker the app runs for its other keys, on the reasoning that this state
is always safe to silently reset (cosmetic prefs, a re-shown consent prompt). That reasoning is
sound in isolation, but it produces a real asymmetry: a future product rename correctly carries
tier-1/tier-2 keys forward while tier-3 keys silently reset — a low-severity but genuinely emergent
side effect of tiers 1–3 never having been designed together, not a decision made *at* the moment
of any single rename.

## The rename-without-migration data-loss class [incident]

This is not a hypothetical. The exact failure — a taxonomy rename shipped before the RENAME_MAPS
mechanism existed — silently dropped every user's per-item override for the renamed identifier on
their very next save/reload: no error, no toast, nothing. The parity test that exists today only
confirms that a store's hand-copied allowlist SETS match the engine's; it cannot tell whether a
given diff is an add/remove (safe) or a RENAME (needs a translate-forward entry) — that
distinction is a human judgment call each time, gated only by tests running green before merge. A
hotfix that adds a rename on the engine side without a matching translate-forward entry on the
storage side ships silently green and loses data on the next client read.

**The generalizable test for any new persisted key:** would a future rename of this key's own
field names, structurally, lose a user's data with no error surfaced anywhere? If yes, it needs
tier-1 discipline (schemaVersion + an explicit rename-map path checked at read-time), not tier-2's
shape-check-only clamp — and it is either tier-3-legitimate (truly safe-to-reset) or it is riding
on a lazy-clamp pattern that owes it more rigor than it currently has.

## Sources

`/Users/kimba/Projects/nonoun/ultimate-tokens/.claude/docs/reports/reactivity-2026-08-20/03-stores-and-persistence.md`
(sections A "Store inventory", B#3–4 "Inconsistencies", C "Drift / data-loss risk scenarios", D
"Verdict") — reviewed 2026-08-20 against commit `63e3dc3`.
