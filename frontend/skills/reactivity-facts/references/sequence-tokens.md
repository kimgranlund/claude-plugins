# Monotonic sequence tokens — the strongest convergence tell in this corpus

Across two unrelated repos (adia-v2's admin frontend and gen-ui-kit), independent authors on
independent pages/modules reinvented the SAME idea — a monotonically-incrementing counter stamped
at request time and re-checked at response time to reject a stale async response — under six
distinct names (across eight file-level sites), with no shared helper extracted. This is the
single clearest "same mechanism, reinvented, unnamed" signal the whole corpus surfaces, which is
why it leads this pack's concept list.

## The mechanism, restated once

The shape is always: (1) increment a counter and capture the new value when a request/render cycle
begins; (2) when the async response arrives, compare the captured value against the counter's
CURRENT value; (3) if they differ, a newer request has since superseded this one — discard the
response rather than applying it. This defeats the "slow request that resolves after a faster,
later request already painted" race without needing to cancel the slow request at all.

## The instances

**adia-v2** (`frontend/apps/admin/src`, 2026-08-20 audit) — five pages independently reinvented
this counter under three different names [verified, source: `adia-v2/.claude/docs/reports/
2026-08-20-reactivity-data-audit/03-page-data-workflow-patterns.md`]:
1. `org-list-page.ts` — `state.requestGeneration` int + an `isCurrent()` closure
   (`generation = ++state.requestGeneration`).
2. `user-list-page.ts` — the identical `requestGeneration` + `isCurrent()` shape.
3. `approval-queue-list-page.ts` — the identical shape again, third file.
4. `conditions-board-page.ts` — reinvented as `state.token += 1`, no shared helper with #1–#3.
5. `ehr-imports-list-page.ts` — reinvented AGAIN as a bare module-level `runsRequestSeq` counter
   (`const token = ++runsRequestSeq`), a fourth name for the same idea.

The corpus's own index names this explicitly as the lead example of its meta-pattern: *"Same
mechanism, three names, no shared helper... despite this exact file family already having
`board-paging.ts`/`list-paging.ts` as proof the team knows how to extract a shared helper when it
wants to"* [verified, `00-index.md` §2]. Two more adia-v2 pages (`gti-list-page.ts`,
`order-set-list-page.ts`) layer a DIFFERENT guard (`AbortController` + a `pageOwner` UUID token) on
top for a second, independent race each page's own comments justify — a related but distinct
mechanism (cancellation-plus-remount-survival, not a pure stale-response counter), excluded from
every count below.

**gen-ui-kit** — the identical family of "last-write-wins via a monotonic counter" recurs here too,
independently of adia-v2 [verified, source: `gen-ui-kit/.claude/docs/reports/
2026-08-20-reactivity-review/03-app-layer-stores.md`]:
6. `adia-embed-labs`'s `#summaryGen` — a "supersede-token" counter, last-write-wins at the apply
   point (`03-app-layer-stores.md:24, 86`).
7. `site.js`'s route sequence-number pattern (`~line 470`) — a third independent home-grown
   last-write-wins mechanism in the SAME repo as #6.
8. The renderer lifecycle's `generationId` (REQ-008) — a fourth, "latest-generation-wins" scheme,
   formalized as part of the surface lifecycle machine (`adr-0061`, cited in
   `04-doctrine-vs-practice.md:60`) rather than an ad hoc page-local counter.

The gen-ui-kit report's own line names this directly: *"Race control duplicated ad hoc:
supersede-token counters in adia-embed-labs (`#summaryGen`) and site.js's route sequence-number
pattern..., vs `generationId` in the renderer lifecycle — three home-grown last-write-wins
mechanisms"* [verified, `03-app-layer-stores.md:86`].

**One counting rule, applied once**: count each distinctly-NAMED pure stale-response counter once,
regardless of how many files reuse that exact name/shape (the `pageOwner` UUID token is excluded
throughout, per the note above — a different mechanism). By that rule: adia-v2 contributes 3 names
(`requestGeneration`+`isCurrent()` — reused verbatim across 3 files — `state.token`,
`runsRequestSeq`); gen-ui-kit contributes 3 more (`#summaryGen`, the site.js sequence number,
`generationId`) — **6 independent reinventions across 2 repos**. Counting FILES instead of names
(every site that reinvents or reuses the idea, adia-v2's 5 pages plus gen-ui-kit's 3 sites) gives
8 — cited here as the fuller number, not a second, competing headline count.

## Why this is the strongest convergence tell, not just a frequent one

Every other axis in this pack (signal kernels, the tier split, verification strategy, ownership
scopes) shows two or three implementations agreeing on a SHAPE. This axis shows the same shape
recurring 6+ times, in two repos that don't share code, under enough different NAMES that no
grep for one name would find the others — which is exactly the signature `pack-writing-rules`
would call an unexplained-drift finding rather than a justified difference: nothing about
`conditions-board-page.ts` needing `state.token` instead of `requestGeneration` is ever explained
in either source report.

## The fix shape, if this pack is read while deciding one

Extract ONE function — the `requestGeneration`/`isCurrent()` shape is the best-tested of the named
variants per the adia-v2 corpus's own recommendation (`00-index.md` §5.2) — and route every stale-
response guard through it. A generation counter is cheap to implement correctly from scratch, which
is exactly why it keeps getting reinvented instead of shared; that cheapness is the trap, not a
defense of the drift.

## Boundary

This file is about REQUEST/RESPONSE staleness guards specifically. It is not about the reactive
KERNEL'S OWN internal versioning (agent-ui's `Producer.version`, `verification-vs-dirty-flag.md`) —
that's a same-process value-change counter inside a signals graph, a different mechanism solving a
different problem (recompute avoidance, not async race rejection), even though both are called
"version" or "generation" in their respective codebases.
