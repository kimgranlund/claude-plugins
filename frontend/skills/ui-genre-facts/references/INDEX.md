# ui-genre-facts — reference index

One axis: `genres/` — one file per product genre, keyed by how users ask ("what does a
_dashboard / collab tool / AI app_ expect"). 13 genre files — this index is the canonical count
(the skill's frontmatter and the CHANGELOG cite it; update it here first when a genre is added or
dropped). Grep for the genre or module term first, Read the matching section — these are catalogs,
not linear reads.

**Provenance:** harvested from the product-forge `product-genres` genre corpus 2026-07-02, curated —
product-strategy content (metrics sections, growth loops, business-model debates, and a separate
metrics-index file) was dropped; the UI-convention content was kept with its
original citations. Each file's `curated:` frontmatter line states what was cut. Original research
date 2026-06-03.

## genres/ — which patterns, modules, and conventions a product category expects

| File | Genre (one line) |
|---|---|
| `genres/ai-native-apps.md` | Model-centered products — reviewable output, streaming/latency UX, deterministic fallbacks (observational; young category) |
| `genres/content-consumption.md` | Feeds, media libraries, streaming — infinite scroll vs load-more, continue/resume, stopping cues, the attention-ethics line |
| `genres/dashboards-analytics.md` | Monitoring + BI — glance-vs-explore split, preattentive encoding, KPI tiles, drill-down, alert fatigue |
| `genres/finance-fintech.md` | Money + identity — staged KYC, trust cues at the ask, unambiguous money state, step-up auth, designed disclosures |
| `genres/games.md` | Core/meta/onboarding loops, tutorialized first win, reward schedules, F2P surfaces, the dark-pattern line |
| `genres/health.md` | Behavior change + regulated data — the clinical-vs-consumer split, consent surfaces, relapse paths, safety escalation |
| `genres/marketplaces.md` | Two-sided products — trust machinery (reviews, verification, escrow, disputes), comparable listing cards, both sides' home surfaces |
| `genres/productivity.md` | Individual leverage — capture-process-retrieve, command palette, keyboard-first, progressive depth, speed as a feature |
| `genres/single-purpose-task.md` | Utilities — the open→done loop, primary action as home screen, near-zero onboarding, no manufactured retention |
| `genres/social-media.md` | Network products — empty-room onboarding, the engagement loop, the lurker→creator ladder, safety controls + accountable moderation |
| `genres/tracking-quantified-self.md` | prompt→log→reflect — streaks + freezes, one-tap/passive logging, guilt-free missed days, reflection payoff |
| `genres/travel.md` | High-consideration booking — multi-session journey persistence, honest comparison, all-in pricing, real (never fake) scarcity |
| `genres/workplace-collaboration.md` | Multiplayer tools — presence, RBAC + sharing defaults, comments/@mentions, notifications, the admin-vs-user split |
