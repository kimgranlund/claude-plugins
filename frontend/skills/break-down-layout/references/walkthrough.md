# Worked example — "functional but unreadable" on OUTSIDE-IN × INSIDE-OUT

A complete DECOMPOSE → fix → GRADE for one screen, showing the **A1 frame gate** failing while the
whole B axis passes — the signature *functional-but-unreadable* defect. **This decomposer has no
mechanized gate**: there is no bin, no red→green script. The **rubric is the gate**, and the two ASCII
wireframes below are the before/after — read the gates by eye, the way you would a real screenshot.

## The artifact

A team "Members" admin screen. Every control works — invite, search, filter, edit, paginate — but
the designer stacked it all in **one flat scrolling column**, no chrome, no regions:

```
  Acme Admin
  Members
  [⌘K search…]
  Overview · Members · Billing · Roles · Audit log        ← nav, inline, mid-page
  Manage who can access this workspace.
  [+ Invite]  [Export]
  [search____] [filter ▾] [sort ▾]   12 results
  ☐ Ada L.    Admin   2h ago   [⋯]
  ☐ Grace H.  Member  1d ago   [⋯]
  ‹ Prev  1 2 3 … 9  Next ›   rows: 25 ▾
  👤 Ada L.  ⚙ settings  ↪ sign out
```

## DECOMPOSE

**A · Outside-in** (macro → micro) — *is the space right?*
- **A1 Frame** `[gate]` — is there a fixed frame the eye can parse? **No.** Nav, header, content, and
  user menu all share one undifferentiated column; nothing is persistent chrome. ✗ **GATE FAILS.**
- **A2 Regions** `[gate]` — unmeasurable. With no frame there are no regions to name — sidebar-nav,
  page-header, page-content all collapse into the scroll. A failed A1 cascades: A2–A5 don't grade.

**B · Inside-out** (core → whole) — *is the behavior right?*
- **B1 Action inventory** `[gate]` — switch · search · invite · export · filter · sort · edit ·
  paginate · manage account. ✓
- **B2 Action→surface binding** `[gate]` — every verb has exactly one obvious control. ✓
- **B3–B5** `[review]` — feedback present (result count, pagination), surfaces sit near their objects,
  one nav selection would drive the content. **All pass.**

The B axis is **green**: as a list of controls, nothing is missing. That's the trap — *functional*.
But A1 is red, so the screen is *unreadable*: the eye has no frame to orient against, and a sympathetic
"it has everything" read hides it. Two axes, opposite verdicts — which is why they never average.

## Fix — frame it into regions per an archetype

Match the shell to an archetype (`references/archetype-saas-dashboard.md` — an app you *navigate*) and
pour the same controls into its **clamshell**: a persistent `sidebar-nav` (route switch + ⌘K + user),
a `page-header` (title · description · actions · tabs), and a `page-content` table.

```
┌─sidebar-nav─┬──────────────────── page ─────────────────────┐
│ ◆ Acme    ⟨ │ ┌─ page-header ───────────────────────────────┐│
│ [⌘K search] │ │ Members                  [Export] [+ Invite] ││
│ Overview    │ │ Manage who can access this workspace.        ││
│ Members  ◂  │ │ [ Active | Invited | Disabled ]   ← tabs     ││
│ Billing     │ ├─ page-content ──────────────────────────────┤│
│ Roles       │ │ [search__] [filter ▾] [sort ▾]    12 results ││
│ Audit log   │ │ ☐ Ada L.    Admin   2h ago            [⋯]    ││
│ ─────────── │ │ ☐ Grace H.  Member  1d ago            [⋯]    ││
│ 👤 Ada L. ▾ │ │ ‹ Prev 1 2 3 … 9 Next ›      rows: 25 ▾      ││
└─────────────┴─┴──────────────────────────────────────────────┘
```

The **control set is unchanged** — that's the point. The fix is structural, not functional: nav
becomes permanent chrome, the page identity separates from the records, and the eye now lands on a
frame → region → group → atom hierarchy. The same verbs, finally readable.

## GRADE — two scores, never averaged

- **Outside-in: A1 gate-fail → (after framing) 5/5** — frame present, regions named from the archetype
  (sidebar-nav · page-header · page-content), internal order and grouping clean.
- **Inside-out: 5/5 throughout** — unchanged; the controls were always complete.

**Quadrant:** the flat screen sat in **"functional but unreadable"** (Inside-out passed — every action
had a control — but Outside-in's frame gate failed) — *built right, laid out wrong*. The fix is a frame
and regions, not new controls. After it: **SHIPPABLE**.

The lesson: "does every action have a control?" is only half the question; "can the eye parse the
space?" is the other — and a layout that aces the first can still fail the second. Score them apart, or
the defect averages away.
