# Sources — provenance in trust order

All research for this pack ran 2026-07-17 via six parallel `pack-researcher` dispatches, one per
axis (the seventh axis, `bug-task-feature-mapping-nuances.md`, is synthesis authored directly
against the other six plus this workspace's own ADR-0002/doc-authoring-standards — it cites no new
external sources of its own).

## Trust tier 1 — GitHub's own documentation (docs.github.com)

The primary source for nearly every `[verified]` claim in this pack. Authoritative for current
platform behavior; GitHub keeps this corpus current with GA/preview status, so a claim cited here
is the platform's own stated contract, not a third party's interpretation.

## Trust tier 2 — GitHub's Changelog and Engineering Blog (github.blog)

Used for release-timeline claims (beta/preview/GA dates), feature-motivation context, and any fact
docs.github.com states without a date attached. Dated by publish date, which doubles as the
feature's rollout date in most changelog entries.

## Trust tier 3 — third-party developer documentation (one GitHub Gist)

`projects-v2.md` cites one community-authored Gist (richkuz, "Notes about using the new GitHub
ProjectV2 API") for GraphQL object-shape details docs.github.com states less precisely. Treated as
supplementary, not primary — every claim it grounds is cross-checked against a tier-1 or tier-2
source in the same file before being marked `[verified]`.

## Grounding-marker legend (this pack's convention, adapted from `git-campaign-workflows`)

- **[verified]** — a platform contract, checked directly against a tier-1/2/3 source, with URL and
  access date.
- **[inferred]** — a claim built from verified facts but not itself directly stated by a source
  (e.g., "all three merge strategies trigger auto-close" — each piece is verified, the composite
  isn't directly confirmed anywhere).
- **[drift-prone]** — verified as of the access date below, but naming a feature young enough
  (days to months old at research time) or a numeric limit stated in a beta/private-preview
  announcement that GitHub is likely to have already changed or will change soon. Re-verify before
  treating as durably current.
- **[unconfirmed]** — searched for and not found in any tier-1/2/3 source; stated as an open gap,
  not a claim.

## Marker-inheritance convention

Within one `##` section of a reference file, a bare marker (`[verified]` with no restated source)
inherits the source named at that section's first fully-cited claim — a reference file is read
section-by-section, not line-by-line in isolation, so this doesn't re-cite the same URL four times
in a row. A marker that names a *different* source than its section's first claim always restates
it in full.

## Access date

Every citation in every reference file was accessed **2026-07-17**. A pack answering from this
citation set more than a few months past that date should re-run the affected axis's research wave
before being trusted on any `[drift-prone]`-marked claim — per `pack-authoring-standards`'
snapshots-and-freshness doctrine.
