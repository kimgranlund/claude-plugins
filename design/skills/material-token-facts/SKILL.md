---
name: material-token-facts
description: >-
  Answers what a `--md-sys-{color,typescale,size,radius,space,inset,gap,border,focus-
  ring}-*` token MEANS. Use when the user asks "what's surface-lowest vs surface-lower",
  "when do I use -dim vs -low", "what's the difference between the scrim strengths" —
  semantic glossary across the color/typography/geometry consumption guides. ANSWERS
  meaning only — not binding grammar, recipes, pairing laws, or bind-check: load the
  matching material-{color,type,shape}-facts skill. NOT for a raw hex/px value (the
  owning consumption skill); NOT for M3-vs-extension history — "is this token M3
  baseline" (each sibling's own extension table); NOT for a non-Material `--{prefix}-*`
  kit (decline).
disable-model-invocation: false
user-invocable: false
---

# material-token-facts — the token glossary

Names and explains what each `--md-sys-*` token MEANS, so a consumer picks the right token from its
MEANING instead of guessing from its name or a nearby example. One axis per domain, matching the three
sibling consumption skills:

| Ask | Load |
|---|---|
| A color role's meaning — an accent variant, a text-hierarchy role, a surface/scrim ladder step, container vs. surface | `references/color.md` |
| A typography voice's meaning — what it's FOR, prose vs. chrome, a sibling weight's meaning | `references/typography.md` |
| A geometry field's meaning — a control-ramp field, a radius level, an inset/gap group, borders/focus-ring | `references/geometry.md` |

## Consult procedure

1. **Classify the ask by domain** (color / typography / geometry) and load only the matching reference
   — Grep for the token or suffix first, Read that section; the files are glossaries, not linear reads.
2. **Answer on the contract: the token (or group), its meaning, and when to reach for it** — a name
   without a "when" is half an answer, since two tokens can look similar and mean opposite things (e.g.
   `-dim/-bright` vs `-low/-high` are BOTH "accent variants" but answer different questions).
   Illustrative worked shape:
   > *"What's the difference between `surface-low` and `surface-dim`?"* → color ask →
   > `surface-lowest→highest` is *relational* (low always reads recessed, in both schemes — pick it for
   > UI structure: wells, cards, modals); `surface-dimmest→brightest` is *literal* lightness
   > (mode-consistent — pick it for actual light/shading: a dimmed pane, a spotlight band). Don't mix
   > the two ladders for the same job — that's the failure mode.
3. **Route output work at the boundary**: the binding grammar, utility classes, pairing law, and full
   recipes live in the matching consumption skill — `material-color-facts` /
   `material-type-facts` / `material-shape-facts`; this pack never teaches
   those, only what the token means once you're there.

## Boundaries

- **This skill answers meaning; it does not teach binding, recipes, or run a bind-check.** No CSS
  snippets beyond what's needed to name a token, no lint/check script — those belong to the three
  sibling skills, which already own them.
- A token's stated meaning is the DEFAULT reading, not a rule that can never bend: a project may
  repurpose a role for a documented reason (e.g. using `-low/-high` for something other than a data-viz
  series) — judge a deviation against the CONFUSION it risks (two tokens meaning the same thing
  app-wide is the failure this pack exists to prevent), not against the letter of the one-liner.
- The M3-baseline-vs-nonoun-extension HISTORY (why 59 roles, why 15 voices, why two geometry tiers) is
  each sibling skill's own "Foundation vs. extension" table — this pack only answers "what does the
  token mean today," not "why does it exist."

## Provenance

Grounded directly in the three sibling consumption skills' own battle-tested prose (color's
containers/interactive/feedback/text/navigation references; typography's own voice table; geometry's
controls/containers/detail references) and the current nonoun engine source (`src/engine/semantic.js`,
`type.mjs`, `geometry.mjs`) — not an external literature search. Authored 2026-07-14 against the
engine's then-current shape (13 typography voices, the fixed-size table, 53+6 color roles, the
unchanged 6-step geometry ramp); re-synced 2026-07-16 for TKT-0008 (the `ui-control`/`ui-widget`
voices, 15 total, the BOX-voice reassignment, and the full-ramp control-text composition into
geometry); re-sync this pack's claims whenever a sibling skill's own token shape changes, the same
trigger that re-syncs the siblings themselves.

## Extending this pack

Extension: governed by [[make-pack]]
