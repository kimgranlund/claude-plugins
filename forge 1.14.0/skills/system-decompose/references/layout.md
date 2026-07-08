# Domain: Layout — manifest adapter

> `system-decompose` domain reference — **canon for this domain in this pack**: the two axis
> ladders (frame → regions → groups → atoms; feature-actions → bindings → surfaces), the justify
> values, and the manifest mapping below. The deeper archetype catalog and per-domain grading of
> the retired sibling pack are not carried here — grade against the generic `rubric.md`. Method
> depth in `method.md` (`scripts/coverage_check.py` runs the gate). · 2026-07-06

## Mapping to the manifest

- **nodes** (OUTSIDE-IN) — the macro→micro tree: frame, regions, groups, atoms
  become nodes; the smallest placed units are `leaf: true`.
- **actions** (INSIDE-OUT) — the feature-actions (what the user does here); the
  bindings and surfaces levels are how you *decide* a `hosts` row, not separate manifest entries.
- **hosts** — each feature-action → the region/atom that makes it reachable.
- **justify** values for an action-free leaf: `content`, `affordance`, `spacing`.

## Cross-check (defect quadrant)

- Every feature-action must host on a region or atom → else `UNHOSTED` (the screen can't do it).
- Every leaf atom must host an action **or** carry a `justify` → else `UNJUSTIFIED-LEAF` (decoration).

## Worked manifest (a sign-in screen)

Map: `recover password` finds no node → `UNHOSTED` → add a `recovery-link` atom under `main`.
Re-check → clean.

```json
{
  "domain": "layout",
  "nodes": [
    {"id":"main","label":"main"},
    {"id":"creds","label":"credentials-group"},
    {"id":"submit","label":"submit-button","leaf":true},
    {"id":"recover","label":"recovery-link","leaf":true}
  ],
  "actions": [
    {"id":"email","label":"enter email"},
    {"id":"pass","label":"enter password"},
    {"id":"go","label":"submit"},
    {"id":"recoverpw","label":"recover password"}
  ],
  "hosts": [
    {"action":"email","node":"creds"},{"action":"pass","node":"creds"},
    {"action":"go","node":"submit"},{"action":"recoverpw","node":"recover"}
  ]
}
```
