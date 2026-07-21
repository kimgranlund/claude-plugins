# State patterns — the screen-state grammar

Every data-bearing surface has five states; a screen designed only in its ideal state is 20%
designed. The five, and what each must do:

## The pentad

| State | Job | Contract |
|---|---|---|
| **ideal** | the designed case | what the mockup shows — but graded against realistic data volume, not lorem ipsum |
| **empty** | first-run or emptied | teach + seed: say what belongs here, give the one verb that fills it ("Create your first project"), never a bare "No data" |
| **loading** | latency window | reserve layout (no CLS), skeleton for structure / spinner for actions — the decision table and time budgets are `check-speed`'s |
| **partial** | some data, not enough | the forgotten state: 2 items in a table built for 200 — must not look broken; density and empty-column handling designed |
| **error** | the fetch/action failed | subject + diagnosis + remedy, inline where the failure happened; retry preserved input; error ≠ empty (never show "no data" for a failed fetch) |

**The two most common defects:** error rendered as empty (users conclude their data is gone), and
empty designed as an afterthought gray line when it is the *most-seen state of every new user's
first session*.

## Empty-state taxonomy
- **First-use** — onboarding surface: explain + primary verb + optional sample data.
- **Cleared** — user emptied it (inbox zero): celebrate/confirm, no onboarding copy.
- **No-results** — a filter/search excluded everything: say *what excluded*, offer to clear it.
Three different states; one "No items" string serving all three is the failure.

## Progressive disclosure
Show the 80% case; put the 20% behind "Advanced" / overflow / expand — but *one* level deep
(disclosure inside disclosure is a lost setting). The disclosure control names what it hides
("Advanced filters (3)"), never a bare chevron. Deviating default: when the audience is expert-only,
inverted disclosure (dense by default) is legitimate — that's a persona decision, not a pattern
violation.

## Optimistic UI + undo
Apply the change locally, sync in background, expose undo in a toast — the pattern that replaces
confirm dialogs for reversible actions. The blast-radius/reversibility calculus governing WHEN
optimistic+undo is allowed vs type-to-confirm is `check-safety`'s; the latency windows and
rollback behavior are `check-speed`'s. This file only places them: undo-toast for reversible,
confirm escalation for destructive, never both on one action.

## State × module composition
A module inherits the pentad per data region: a master-detail screen has *independent* state
machines for list and detail (empty list ≠ empty detail); a dashboard has one per widget — design
the mixed case (three widgets loaded, one erroring) or the first partial outage designs it for you.
Cross-SCREEN state machines — a journey's states, transitions, and exits — are `break-down-flow`'s
card, not this pentad; the pentad governs the data regions within one screen.
