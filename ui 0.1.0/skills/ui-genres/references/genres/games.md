---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; the metrics and F2P-economics sections dropped, UI conventions kept
coverage: foundational
primary_sources:
  - "Nir Eyal (2014). Hooked: How to Build Habit-Forming Products. Portfolio/Penguin (variable reward; the Manipulation Matrix). https://www.nirandfar.com/how-to-manufacture-desire/"
  - "Solsten. The True Drivers of D1, D7, and D30 Retention in Gaming (practitioner analysis; observational — cited here for the FTUE→first-day tie). https://solsten.io/blog/d1-d7-d30-retention-in-gaming"
  - "Game-design lineage: the 'core loop' / 'meta loop' vocabulary is practitioner-standard (e.g. GDC talks, Deconstructor of Fun); definitions here follow common practitioner usage and are labeled observational."
---

# Games as a Genre

A game is an engagement product whose value is the experience of playing. The genre is structured as nested loops at three timescales: the **core loop** (the second-to-minute action you repeat — aim/shoot, match/clear, tap/collect), the **meta loop** (the session-to-week progression that gives the core loop a reason — leveling, base-building, collection, ranks), and the **onboarding loop** (the first-session experience, the FTUE, that decides whether a player ever reaches the other two).

> The loop vocabulary (core / meta / onboarding) is practitioner-standard rather than drawn from a single canonical text — it recurs across GDC talks and game-economy writing (e.g. Deconstructor of Fun). Treat the definitions here as the common practitioner usage, labeled observational.

## The three loops (the genre's architecture)

- **Core loop.** The tight, repeated action that _is_ the moment-to-moment game. It must be satisfying in isolation — good "game feel," fast feedback, low input latency — because the player does it hundreds of times per session. A weak core loop cannot be rescued by meta systems.
- **Meta loop.** The longer arc that gives the core loop stakes and forward motion: progression, unlocks, collections, social ladders, live events. The meta loop is what converts "this is fun for five minutes" into "I want to come back tomorrow."
- **Onboarding loop (FTUE).** The first-time user experience teaches the core loop, delivers an early win, and previews the meta payoff — all before the player decides to leave. Practitioner analysis ties FTUE quality directly to first-day survival, which then caps everything downstream (Solsten; observational).

## Signature UX patterns

- **Tutorialized first win.** Guided early play that produces a success within the first minute or two, establishing the core loop's payoff before introducing complexity.
- **Reward schedules and variable rewards.** Loot, drops, daily rewards, and randomized outcomes — Eyal's variable-reward mechanic (Hooked, 2014) in its purest form. The unpredictability of the next reward sustains the core loop.
- **Daily-return mechanics.** Daily login bonuses, refreshing energy/lives, and time-gated events that create a reason to open the app each day.
- **Progression and meta dashboards.** Level maps, collection grids, and rank ladders that make the meta loop visible and create open loops the player wants to close.
- **F2P monetization surfaces.** Soft/hard dual currencies, energy systems, gacha/loot boxes, battle passes, ad-reward placements, and limited-time offers — the module set through which a free-to-play game surfaces its economy. Expected as UI; the ethical constraints on them are below.

## The engagement-vs-dark-pattern line

The genre runs the same ethical seam as content consumption (see `content-consumption.md`), and a review should score it.

- **Variable reward is the shared mechanic.** The reward schedule that makes a core loop compelling is the same mechanism that, over-tuned, becomes compulsion. Eyal's own guardrail — the **Manipulation Matrix** — applies: build hooks that improve the player's life, and provide graceful exits.
- **The recognized dark patterns.** Predatory monetization (pay-to-win paywalls that gate core enjoyment), loot-box mechanics that obscure odds (now regulated in several jurisdictions and increasingly required to disclose drop rates), artificial energy/time-gates engineered to sell relief, and FOMO-driven limited offers aimed at impulse rather than value. These are the genre's named over-the-line patterns.
- **The test.** Engagement a player would endorse on reflection (this is fun, the progression feels earned) is the product working; engagement built on obscured odds, manufactured scarcity, or pay-gated core enjoyment is the product exploiting. The same loop produces both; the genre is judged by which it engineers.

## Common pitfalls

- **A weak core loop dressed in meta systems.** No amount of progression UI rescues a moment-to-moment action that is not fun.
- **Onboarding that loses the first session.** A long, un-fun, or unclear FTUE that delays the first win caps everything downstream — you cannot retain or delight a player who quit in session one.
- **Monetization that breaks the loop.** Paywalls or ad density that interrupt the core loop trade short-term revenue for the collapse of the thing being monetized.
- **Chasing daily opens with mechanics that do not deepen play.** Daily-login bonuses that inflate visit counts without strengthening the core or meta loop produce hollow engagement that decays.

## Good vs. bad (for a genre-fit dimension)

| Dimension | Good (high genre-fit) | Bad (low genre-fit) |
| --- | --- | --- |
| Core loop | Satisfying in isolation; fast feedback, good feel | Repetitive, sluggish, or unrewarding moment-to-moment |
| Meta loop | Gives the core loop stakes; a reason to return | Thin or absent; nothing to come back for |
| Onboarding | Early win in the first minute; core loop taught by play | Long/confusing FTUE before any payoff |
| Monetization | Funds the game without breaking the loop | Pay-to-win paywalls; ad density that interrupts play |
| Loot/odds | Disclosed drop rates; value-aligned offers | Obscured odds, manufactured scarcity, FOMO traps |
| Ethics posture | Engagement the player endorses on reflection | Compulsion via gates/odds; manipulation-matrix fail |

The single most diagnostic question for genre-fit: **does each loop earn the next — core loop fun enough to repeat, meta loop rich enough to return for, onboarding fast enough to reach both — and does monetization ride the loops without breaking them?**
