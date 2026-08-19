---
name: token-feature-intake-rules
description: >-
  Intake schema for a token/palette/typography feature ticket — which roles/ramps, both-theme
  reach, and consumers on one plane; specific token values, contrast gates, and the
  interaction-state ladder on the other. Use when capturing/reviewing what a visual-token TICKET
  should state before build: "what should a new-accent-color ticket capture", "what fields does a
  typography-seed ticket need", "is this token ticket capture-complete". NOT for building/grading
  the palette or type system itself (make-palette, pick-fonts, token-builder); NOT general
  feature intake (docs:file-feature, which consults this pack); NOT UI component/layout/flow
  seeds (screens:feature-intake-rules).
disable-model-invocation: false
user-invocable: false
---

# token-feature-intake-rules — visual/token feature ticket intake schema

1 declared axis, flat consult table below, no `references/INDEX.md`. Every schema field is
LIFTED from the owning skill/agent's own domain — this pack owns WHAT A TOKEN TICKET MUST
CAPTURE, never how the palette, typography, or export is actually built.

## Both-planes capture-completeness rule

A UI feature ticket is capture-complete only when both plane columns carry an answer or a named
open fork. Single-plane capture ships the known failure quadrants: outside-in-only ("looks clean
but nothing does anything"), inside-out-only (orphan components).

## Consult table

| Shape | Load | Build owner | DoD checker |
|---|---|---|---|
| Token / palette / typography seed | `references/token-visual-schema.md` | `make-palette` / `pick-fonts` / `token-builder` | `check-colors` / `design-system-checker` |
| Worked example | `references/fixtures.md` | — | — |

## How to use it

1. **Fill the grid**, both plane columns — an unanswered cell is a named open fork, never a
   silent gap (the both-planes rule above).
2. **Stamp the ticket's own scope: frontmatter** with `build-owner`/`dod-checker` from the table
   — so `dispatch-ticket` routes the build against the same owner this schema names, and the
   checker it dispatches at DoD is the same checker this schema names (invariant below).
3. **These same fields double as the pre-fork grill's fork menu** for big seeds (gh#654) — the
   grill's own step picks the highest-leverage unanswered cells (2 structural + 2 mechanism) from
   this same grid; one artifact, never two drifting lists.
4. **`docs:file-feature`'s classify step consults this pack** by soft named mention for any
   token/palette/typography-shaped seed — this pack never invokes `file-feature`, only the
   reverse.

## Core invariants

- **(a) Both-planes capture-completeness** — stated above, verbatim, shared with
  `screens:feature-intake-rules`.
- **(b) Fork-menu reuse** — these schema fields double as gh#654's pre-fork grill fork menu; one
  artifact, never two drifting lists.
- **(c) Scope/owner/checker geometry** — the ticket records `scope:`, the named build owner, and
  the pre-named DoD checker so capture → build → verify speak one geometry.
- **(d) No duplication** — no new agents (IDR-0007's bar — the checkers already exist), no
  procedure duplication (every schema field cites its owning skill's own axis, never restates it —
  doctrine-audit safe), no hooks (gh#466).

## Composition

- **`design:make-palette` / `pick-fonts`** — the owning build skills this pack's schema cites;
  soft in-plugin citation, never a preload, never a restatement of their own doctrine.
- **`design:token-builder`** — an AGENT, cited by name as a build owner (dispatched, not
  routed-to by description-match, so no reciprocal routing fence is owed to it).
- **`design:check-colors` / `design-system-checker`** — the DoD checkers this pack's schema
  names; reached at build-verify time, never invoked by this pack.
- **`docs:file-feature`** — the procedural intake this pack is consulted FROM (soft cross-plugin
  mention, degrades gracefully where `design` isn't installed); this pack never restates
  `file-feature`'s own classify/dedup/size procedure.
- **`screens:feature-intake-rules`** — the sibling pack for UI component/layout/flow seeds;
  disjoint domain, no citation between the two (each cites `file-feature` independently).

Extension: governed by [[make-pack]].
