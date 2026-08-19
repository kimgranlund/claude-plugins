# Layout / shell intake schema

Fields lifted verbatim from `screens:break-down-layout`'s own OUTSIDE-IN (frame → regions →
groups → atoms) × INSIDE-OUT (verbs → bindings → feedback → coherence) axes
(`break-down-layout/SKILL.md`, `references/decomposition-method.md`) — reframed as intake
QUESTIONS, never a second copy of the axis doctrine.

## Outside-in (space) — frame → regions → groups → atoms

| Field | Question | Owning level |
|---|---|---|
| Archetype | Which of the four shells fits — productivity-shell, saas-dashboard, or a sibling archetype (`ui-pattern-facts`)? | A1 Frame |
| Region ownership | What are the named regions (header/left/canvas/right/footer) and what does each own? | A2 Regions |
| Region-internal order | Within each region, what's the internal grammar (title/desc/actions/tabs, sidebar-nav shape)? | A3 |
| Grouping | How do cards/panels group inside a region? | A4 |

## Inside-out (behavior) — verbs → bindings → feedback → coherence

| Field | Question | Owning level |
|---|---|---|
| Verbs | What actions does a user perform here (switch · select · inspect · create · edit · navigate)? | B1 Action inventory |
| Bindings | Does each verb have exactly one obvious surface co-located with its object? | B2 Action→surface binding |
| Feedback | What's the state + feedback for each verb once performed? | B3 |
| Surface fit | Does each surface (panel/pane) fit the verbs it hosts, with no orphaned or overloaded pane? | B4 Surface→pane fit |
| Cross-surface coherence | Does one selection update every OTHER surface that should reflect it? | B5 |

Keyboard/tab focus order is a separate CROSS-CUTTING concern, not part of `break-down-layout`'s
own axis vocabulary — it routes to `references/cross-cutting-ux.md`'s Focus section
(`check-focus`), never answered inline here.

## Scope frontmatter this shape stamps

```
scope: layout
build-owner: break-down-layout (DESIGN mode)
dod-checker: layout-checker
```

## Both-planes note

Outside-in-filled/Inside-out-empty is `break-down-layout`'s own "pretty but dead" quadrant; the
reverse is "functional but unreadable" (see the pack's own both-planes rule for the general
statement; not restated per file below).
