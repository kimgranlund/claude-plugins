---
name: ui-genre-facts
description: >-
  Answers which patterns, modules, and conventions a product CATEGORY expects — the genre world
  model behind "is this the right pattern for THIS kind of product". Use when identifying or
  judging genre fit: "what genre is this app", "what do users expect in a dashboard / collab tool /
  habit tracker / AI chat app", "which patterns does this category demand", "genre conventions for
  X", "is this convention-violation acceptable here", "does a marketplace / this kind of product
  need a [surface]". Covers the genres: dashboards/analytics,
  collaboration, productivity, single-purpose utilities, content consumption, social
  media, AI-native apps, games, tracking/quantified-self, health,
  finance/fintech, marketplaces, and
  travel/booking. ANSWERS and names genre expectations; it does not apply or build them — NOT for which modules a
  page or screen needs (ui-pattern-facts); naming
  the underlying pattern is ui-pattern-facts, applying it to a concrete layout is break-down-layout,
  sweeping a whole product for conformance is check-whole-ui.
user-invocable: false
disable-model-invocation: false
---

# ui-genre-facts — the genre world model

Names what a product *category* expects — the pattern set, module inventory, signature
conventions, and the failure modes each genre invites — so conformance review can ask "is this the
right pattern for THIS kind of product" instead of "is this a canonical table". One axis of genre
files under `references/genres/`, indexed in `references/INDEX.md` — the canon for the genre count,
and carrier of the harvest provenance. Each file: conventions → signature UX patterns → pitfalls →
a good-vs-bad genre-fit contrast.

| Ask | Load |
|---|---|
| Monitoring/BI — KPI tiles, drill-down, alert fatigue | `genres/dashboards-analytics.md` |
| Multiplayer work tools — presence, RBAC, notifications, admin plane | `genres/workplace-collaboration.md` |
| Personal leverage tools — capture/retrieve, ⌘K, keyboard-first | `genres/productivity.md` |
| One-job utilities — the open→done loop, zero onboarding | `genres/single-purpose-task.md` |
| Feeds, media, streaming — scroll mechanics, resume, stopping cues | `genres/content-consumption.md` |
| Networks/communities — creation ladder, safety controls, moderation | `genres/social-media.md` |
| Model-centered apps — reviewable output, streaming, fallbacks | `genres/ai-native-apps.md` |
| Games — core/meta/onboarding loops, reward schedules, F2P surfaces | `genres/games.md` |
| Habit/health/budget logging — streaks, guilt-free lapses, reflection | `genres/tracking-quantified-self.md` |
| Health/behavior change — regulatory split, consent, safety escalation | `genres/health.md` |
| Money products — staged KYC, trust cues, step-up auth, disclosures | `genres/finance-fintech.md` |
| Two-sided buy/sell — trust machinery, listing cards, both sides' homes | `genres/marketplaces.md` |
| High-consideration booking — journey persistence, honest comparison | `genres/travel.md` |
| Which file / where a claim comes from | `references/INDEX.md` |

## Consult procedure

1. Classify the ask into a genre — from the product named or the surface described. Products
   blend genres (a fintech app has a dashboard home; a social app has a settings utility):
   classify per *surface*, not per product, and load every genre a surface belongs to. Grep the
   file for the convention or module term, Read that section — catalogs, not linear reads.
2. Answer with the genre's **expected pattern set AND the convention-violation to flag** — a
   genre answer that lists expectations without naming the failure they prevent is half an
   answer. Worked shape:
   > *"This habit tracker resets your streak to zero after one missed day — fine?"* → tracking
   > genre → expected set: streaks **with** freezes/repair, one-tap or passive logging,
   > guilt-free re-entry, reflection surfaces; the violation to flag: the **streak-shame
   > off-ramp** — a hard reset converts the genre's signature mechanic into a quit trigger
   > (`genres/tracking-quantified-self.md`).
3. Route output work at the boundary: name or explain the underlying pattern itself →
   [[ui-pattern-facts]] (this pack says the category *needs* a comparison table; that one says what a
   canonical table *is*); apply the expectation to a concrete screen → [[break-down-layout]];
   check a whole product's genre conformance (the sweep) → [[check-whole-ui]], which uses these files
   as the per-genre expectation baseline; verify an interaction invariant a convention implies →
   the verifier family via ui-pattern-facts' routing.

## Boundaries

- **This skill answers; it does not generate.** No wireframes, no feature lists, no product
  strategy — name the expectation, hand the making to the builder skills above.
- A genre convention is a *default with a rationale*, not a rule: when a product deviates, judge
  the deviation against the failure mode the convention exists to prevent — deviation with a
  reason is positioning, deviation without one is genre drift.
- Product strategy (metrics, growth loops, monetization economics) was deliberately dropped at
  harvest — this pack answers what the category's UI owes its users, not how the business scores
  itself.

## Extending this pack

A missing genre, a stale convention, or "add X to this pack" is authoring work — route to
[[pack-forge]] (axis decomposition, grounded research waves, index discipline); never bolt
an uncited file onto the corpus inline. Re-run the harness gates after any edit.
