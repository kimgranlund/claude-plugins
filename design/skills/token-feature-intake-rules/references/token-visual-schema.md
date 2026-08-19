# Token / palette / typography seed intake schema

Fields lifted from `design:make-palette`'s ramp/role vocabulary, `design:pick-fonts`'s voice/step
grammar, and `design:check-colors`'s ColorProof surface — reframed as intake QUESTIONS a ticket
must answer before build, never a second copy of any of the three skills' own doctrine.

## Outside-in — which roles/ramps touched, both-theme reach, consumers

| Field | Question | Owning domain |
|---|---|---|
| Roles / ramps touched | Which semantic role (accent/danger/warning/success/info, or a typography voice) does this seed add or change? | `make-palette` role mapping / `pick-fonts` voice grammar |
| Both-theme reach | Does this seed need both a light AND a dark scheme derived, or is one theme explicitly out of scope? | `make-palette`'s dark-scheme derivation step |
| Which consumers | What UI surfaces consume this role/voice once shipped — which components, which screens? | downstream consuming surfaces |

## Inside-out — specific token values, contrast gates, interaction-state ladder

| Field | Question | Owning domain |
|---|---|---|
| Specific token values | What are the actual OKLCH anchor(s) — brand anchor hue, chroma ceiling? For typography: which VOICE (`pick-fonts`) and which numeric STEP on that voice's ramp (`font-token-rules`'s scale realization, a separate skill from the voice decision itself)? | `make-palette` inputs (BrandSchema) / `pick-fonts` voice pick / `font-token-rules` step |
| Contrast gates | What contrast floor must this role clear (WCAG AA/AAA or APCA), and against which backgrounds? | `check-colors`'s ColorProof surface |
| Interaction-state ladder | Does this role need hover/active/focus/disabled states, and are they distinct AND accessibility-safe across both schemes? | no dedicated owning skill — derive inline from `make-palette`'s own semantic-role assignment practice, each state's contrast re-verified by `check-colors` |

## Scope frontmatter this shape stamps

```
scope: visual
build-owner: make-palette | pick-fonts | token-builder
dod-checker: check-colors | design-system-checker
```

## Both-planes note

A named role with no stated contrast floor or interaction-state ladder is the visual-domain
equivalent of "looks clean but nothing does anything" — the role exists but nobody can verify it
before ship. The reverse — token values and contrast gates specified with no named consuming
surface — ships an orphan token nobody actually binds to. Both are named open forks, never
silently assumed.
