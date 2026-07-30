# Baseline — un-skilled run, 2026-07-25

Captured verbatim from the authoring session, ~20 minutes before this skill existed. Not a
simulation: this is the real output the user received, and the reason they asked for the skill.

## Prompt

> summarize PR's merged today

## What the un-skilled run actually did

One improvised command:

```bash
gh pr list --repo adiahealth/adiav2 --state merged --limit 60 \
  --json number,title,author,mergedAt,additions,deletions,labels \
  --jq '[.[] | select(.mergedAt >= "2026-07-25T00:00:00Z")] | sort_by(.mergedAt) | .[] | ...'
```

Then read all 58 returned rows and sorted them into groups by reading titles.

## Output shape produced

Opened with **"18 real PRs merged today, plus 40 automated version bumps"**, then three
per-person sections (Alex Meshkin / Andrei Gaivoronskii / Kim), each with a bulleted PR list
and rough line counts.

## Gaps this baseline establishes

1. **Linear was never queried.** ADIA2-6449 and ADIA2-6584 both moved to Done that same day
   with no PR behind either. Neither appeared. A PR-only summary cannot surface them.
   → assertion A5
2. **GitHub issues were never queried.** Not consulted at all.
3. **Bot filtering was manual and fragile.** The 58→18 split came from eyeballing `v0.NNNN.0`
   titles. It happened to be correct; it breaks on any bot PR not matching that title shape.
   → assertion A3
4. **The counts were wrong.** Reported "58 PRs total, 40 automated version bumps". The true
   figures are **57 total / 39 bot / 18 human** — confirmed 2026-07-25 by running both the
   client-side (`gh pr list` + jq on `mergedAt`) and server-side (`gh search prs --merged-at`)
   methods, which agree exactly, so the error was hand-counting rather than a query boundary.
   Off-by-one on a 57-row list is precisely the error a script removes.
5. **`--limit 60` was a guess** that happened to exceed the day's 57 PRs. One busier day and
   the summary silently truncates with no indication.
6. **The window was never resolved or stated.** "Today" was interpreted as UTC midnight
   without saying so. → assertion A2

Gap 4 is the sharpest evidence: the un-skilled run was not merely less structured, it was
**numerically wrong**, and nothing in its output signalled that.
