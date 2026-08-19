# Worked fixture — one capture-complete grid for the visual/token shape

Demonstration matter, not an enforced schema — a real ticket is graded by whether its own grid,
filled against `references/token-visual-schema.md`, has an answer or a named open fork in every
cell.

## Fixture — "Add a `caution` intent role (between `warning` and `danger`)"

```
scope: visual
build-owner: make-palette
dod-checker: check-colors

Outside-in:
  Roles / ramps touched — new intent role `caution`, sits between `warning` (amber) and `danger`
                          (red) on the hue wheel
  Both-theme reach       — both light AND dark schemes required at ship
  Which consumers         — badge component, inline banner, form-field validation state

Inside-out:
  Specific token values    — brand anchor hue ~55° (amber-orange), chroma ceiling matches the
                             existing `warning` ramp's ceiling, 9-step scale (same as sibling
                             intent roles)
  Contrast gates            — WCAG AA text-on-fill for the 500/600 steps; OPEN FORK: APCA sweep
                             deferred to check-colors' own card, not pre-decided here
  Interaction-state ladder   — hover/active/focus/disabled all distinct from base per the
                             existing intent-role ladder pattern (no new pattern invented)
```
