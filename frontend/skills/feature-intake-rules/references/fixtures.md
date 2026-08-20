# Worked fixtures — one capture-complete grid per shape

Each fixture is a minimal, grep-able worked example of a ticket that satisfies the both-planes
capture-completeness rule for its shape. These are demonstration matter, not enforced schemas —
`fixtures.md` itself carries no checker; a real ticket is graded by whether its own grid, filled
against the matching `references/*.md` file, has an answer or a named open fork in every cell.

## Fixture 1 — Component/module ("Add a `<tag-chip>` removable chip control")

```
scope: component
build-owner: make-component
dod-checker: component-checker

Compose (outside-in):
  Placement          — primitive tier, "display" family (nests inside a chip-group module)
  Parents / children  — hosts inside `<chip-group>`; no children of its own
  Composition & nesting — anatomy: leading icon slot (optional) + label + trailing remove button
  Consuming surfaces  — filter bars, multi-select form fields

Realize (inside-out):
  States              — `removable` attribute; `disabled` custom state
  API surface          — `label` attribute, `remove` event, `icon` slot
  Geometry             — SM/MD ramp only (no LG use case yet) — OPEN FORK: XL variant deferred, not answered
  Token bindings        — --c-chip / --c-chip-hover (existing tokens, no new token needed)
  Feedback              — Enter/Space activates remove; focus ring on the remove button per check-focus
```

## Fixture 2 — Layout/shell ("New `settings` page under the saas-dashboard shell")

```
scope: layout
build-owner: break-down-layout (DESIGN mode)
dod-checker: layout-checker

Outside-in (space):
  Archetype            — saas-dashboard
  Region ownership      — sidebar-nav unchanged; page-header carries title + save/discard actions
  Region-internal order — page-header → tabbed sections (Profile / Notifications / Billing)
  Grouping              — each tab is one card per settings group

Inside-out (behavior):
  Verbs                 — edit field, save, discard, switch tab
  Bindings               — save/discard co-located in page-header, always visible
  Feedback               — inline validation per field; toast on save
  Surface fit            — each tab pane hosts exactly one settings group's fields, no overflow
  Cross-surface coherence — OPEN FORK: does an unsaved-changes flag on one tab surface in the
                            page-header too? not yet decided
  (tab-switch keyboard focus: cross-cutting, not part of this grid — routes to
   references/cross-cutting-ux.md's Focus section, check-focus at DoD)
```

## Fixture 3 — UX flow ("Password-reset flow")

```
scope: flow
build-owner: break-down-flow
dod-checker: flow-checker

Outside-in (journey):
  Journey placement      — entered from the sign-in screen's "forgot password" link
  Entries                 — one entry: sign-in screen link (no deep-link entry in this iteration)
  Sequencing               — request → email-sent → reset-form → confirmed
  Effort shape              — linear wizard, 4 stages

Inside-out (machine):
  Per-transition mechanics  — request→email-sent (submit); email-sent→reset-form (link click,
                              external); reset-form→confirmed (submit); abandon at any stage returns
                              to sign-in
  Exit asserts               — confirmed: "user can sign in with the new password"
  Failure/interrupt states    — expired reset link → reset-form re-requests a new email, previous
                              input NOT preserved (single-use token)
  Resume/persistence           — not resumable across sessions (token is single-use, time-boxed)
```

## Fixture 4 — Cross-cutting UX ("New in-app notification toast")

```
scope: cross-cutting
build-owner: check-focus, motion-rules, check-translations
dod-checker: check-focus, check-translations (self-checking; motion-rules is answer-only, no gate)

Motion    — enter/exit on the standard "notification" duration ladder; reduced-motion: fades
            instead of slides
Focus     — toast never steals focus (assertive-but-non-blocking); Escape dismisses if focused
Hit target — dismiss (x) button meets the minimum hit-area even though the toast itself is compact
i18n      — message string routes through the translation layer; RTL: dismiss button mirrors to
            the leading edge
```
