---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; the metrics section dropped, UI conventions kept
coverage: foundational
primary_sources:
  - "MakeUseOf — 8 apps that do one thing perfectly (and nothing else) (practitioner survey; observational). https://www.makeuseof.com/apps-that-do-one-thing-perfectly-and-nothing-else/"
  - "Doug McIlroy, Unix philosophy — 'Make each program do one thing well' (Bell System Technical Journal, 1978; foundational design lineage, not an app metric)"
---

# Single-Purpose Task Apps as a Genre

A single-purpose task app exists to collapse one intention into one completed action with as little ceremony as possible: a timer, a unit converter, a scanner, a voice-memo recorder, a quick-capture note, a tip calculator. The genre's whole reason to exist is the **"open → done" loop** — the user opens the app already knowing what they want, and the app's job is to get out of the way between launch and completion. Everything that does not serve that loop is, by the genre's own standard, weight. The design lineage runs back to Doug McIlroy's Unix-philosophy line, "Make each program do one thing well" (Bell System Technical Journal, 1978) — a foundational design value, not a measurable app metric, but the cultural source of the genre's discipline.

> The genre's defining test: from the moment the app is on screen, how many taps, decisions, and seconds stand between the user and the thing they came to do? Good single-purpose apps drive that number toward its floor; bad ones quietly raise it in the name of features.

## Conventions: what the genre takes for granted

These are the field's working expectations. Most are observational — synthesized from practitioner surveys of well-regarded utilities (e.g. MakeUseOf's "apps that do one thing perfectly") rather than from a controlled study — so treat them as genre norms, not laws.

- **Near-zero onboarding.** The strong convention is no signup, no account, no setup wizard, no permission gauntlet before first use — the app is "ready to go as soon as the user downloads and opens it" (observational; practitioner consensus). A tutorial is a confession that the one thing is not self-evident.
- **The primary action is the home screen.** The single most common action _is_ the landing state. The canonical example is a one-tap voice recorder where launching the app and tapping once starts recording, with the transcript appearing on stop (observational, MakeUseOf). There is no menu to traverse to reach the point.
- **State persistence over re-entry.** A good utility remembers where you were (last conversion, last timer, last unit) so the next "open → done" is even shorter. Re-asking for input the app already has is friction.
- **Graceful exit / done-ness.** The loop has a clear terminal state — the conversion is shown, the recording is saved, the code is scanned. The app does not try to keep you after "done"; retention is a side effect of the tool being good, not of holding you.
- **Offline-first where the task allows.** A timer or calculator that needs a network round-trip has imported a dependency the task never required.

## Signature UX patterns

- **Single dominant control.** One primary affordance owns the screen (the big button, the single input field), with secondary controls demoted or hidden. Hick's law in practice: fewer visible choices, faster decision.
- **Immediate feedback.** The result appears as the input changes (live conversion, running timer) — no separate "calculate" or "submit" step where the task does not require one.
- **Sane defaults, minimal required input.** The most likely value is pre-filled; the user corrects rather than constructs. Optional refinement is available but never blocks the common path.
- **Reduced asset weight as a feature.** Minimalism is not only aesthetic: lighter interfaces load faster, and load time is part of the loop the genre is optimizing (observational; practitioner sources tie heavier UI to slower first paint).

## Common pitfalls

- **Feature creep / the kitchen-sink drift.** The most characteristic failure mode of the genre: a clean tool accretes adjacent features until the one thing is buried behind navigation. Each addition is locally reasonable and collectively fatal to the loop.
- **Onboarding gates on a task that needs none.** Inserting signup, an email-capture, or a permission wall before first value contradicts the genre's near-zero-onboarding convention and is felt as a bait-and-switch.
- **Manufactured retention.** Adding streaks, notifications, or a feed to a utility to inflate engagement borrows mechanics from the engagement genres (see `tracking-quantified-self.md` and `content-consumption.md`) onto a tool whose health is measured by how _little_ time it takes — a category mismatch that degrades the product on its own terms.
- **Hidden primary action.** Putting the core control behind a menu, a mode switch, or a non-default screen lengthens every single loop.
- **Latency in the loop.** Any network dependency, spinner, or ad interstitial between launch and completion is the most expensive defect, because it taxes the exact moment the genre promises to be fast.

## Good vs. bad (for a genre-fit dimension)

A review scoring genre-fit should reward the loop and penalize imported engagement mechanics.

| Dimension | Good (high genre-fit) | Bad (low genre-fit) |
| --- | --- | --- |
| First use | Usable in seconds, no account, no wizard | Signup / permissions / tutorial before any value |
| Primary action | The dominant, default, on-launch affordance | Buried behind a menu, mode, or secondary screen |
| Loop cost | Minimal taps and time to completion; live feedback | Extra confirm/submit steps; spinners; interstitials |
| Scope | Does one thing; resists adjacent features | Kitchen-sink accretion; the one thing is now a tab |
| Exit | Clear "done"; no attempt to retain post-task | Holds the user with feeds/notifications after completion |

The single most diagnostic question for genre-fit: **does a new addition shorten the open → done loop, or lengthen it?** Anything that lengthens it is, for this genre, a defect — even if it would be a feature in any other.
