# One name, two owners — contract collisions worth flagging as live-bug-hazard

**The judgment call:** when one conceptual field, attribute, or record is written by TWO
independent code paths that don't know about each other, treat it as a live-bug-hazard class —
not "duplication, low priority" — the moment BOTH paths can fire in the same session. This is a
narrower, more urgent case than the general built-but-unadopted/never-swept pattern
(`adoption-verdict.md`): the tell is not "a fix exists and wasn't reused," it's "two write paths
to the same fact exist and neither yields to the other."

## The worked case — a live double-fetch [incident]

gen-ui-kit's #1-ranked cross-cutting finding: `[data-stream-src]` has two competing owners. A
core document-level observer auto-starts fetching for ANY element carrying that attribute, while
four billing composites independently hand-roll their own `fetch()` off the SAME attribute, each
with its own race guard and loading/error reflection. "A page importing both double-fetches every
billing composite. One attribute, two protocols." This is not a style inconsistency — it is a
live correctness bug the moment both the core observer and a billing composite are present on the
same page.

Source [verified]: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
F1 + R1 ("Fix F1 now (small, real bug class)").

## The scale this reaches when nobody counts it [verified]

The same corpus's app-layer survey put a number on how many independent "owners" of the identical
problem can accumulate before anyone notices: **seven** hand-rolled Set-of-listeners pub/sub
stores solving the one problem `signal()` already solves — `plan-store.js`'s `listeners =
new Set()`, `data-client.js`'s `_subscriptions = new Set()`, `patient-visit/record.js`'s
`subscribers = new Set()` (self-documented as a copy of the previous two), `persona/store.ts`'s
own `subscribers = new Set<() => void>()`, `task-service.js`'s `_subs = new Set()` plus a
BroadcastChannel cross-tab fanout, `a2ui/controllers/base.js`'s `BaseController` `#subs`, and
`a2ui/surface.js`'s path-keyed `#watchers Map<path, Set<fn>>` variant. Race control shows the
identical pattern one level down: three independent home-grown last-write-wins mechanisms
(`adia-embed-labs`'s `#summaryGen` counter, `site.js`'s route sequence number, the renderer
lifecycle's `generationId`) solving the exact staleness problem `sequence-tokens.md` (this pack's
sibling `reactivity-facts`) already names one canonical fix for. None of these seven owners
collide directly the way `data-stream-src` does — they're parallel reimplementations, not two
write paths to one shared attribute — but they are the same "one-name-two-owners" pathology
diffused across many names instead of concentrated on one: every one of the seven answers "how do
I get pub/sub" independently, with no shared owner anyone could point a new consumer at.

Source [verified]: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/03-app-layer-stores.md`
§4 ("Duplicated store/signal implementations") — the full store/race-control inventory behind
`INDEX.md`'s F2 finding.

## The worked case — a second live instance of an identical name collision [incident]

agent-ui's roster-name bug (see `two-facts-one-name.md` for the full trace) had a SECOND live
instance of the identical defect: the Team pane's `nameFor()` resolves GM/member display names
from the same stale `#pendingRoster` label snapshot the header picker reads from — "renaming via
the Settings Name field shows the OLD name in the Team pane's 'GM: …' line too." Same root cause
(two owners of "the agent's name," neither aware of the other), two independent visible symptoms.
Finding a second instance is the confirmation that the first was systemic, not a one-off.

Source [verified]: `/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/agent-admin-app-state-audit.md`
"Sync-point map" item 2; `FINDINGS.md` F2.

## The worked case — independently reinvented owners, not (yet) colliding [incident]

adia-v2's audit found several near-misses of the same shape, one clause short of an active bug:
`auth-store.ts` and `event-bus.ts` each independently invented the identical subscribe/notify-
singleton pattern in sibling files, with no shared helper between them; `canDo()` and `can()` are
two independently-maintained permission matrices for overlapping roles, "hand-synced by nothing";
the stale-request-guard idea was reimplemented under three different names
(`requestGeneration`/`isCurrent()`, `state.token`, `runsRequestSeq`) across five files that all
solve the identical staleness problem. None of these have YET produced the double-fetch class of
live bug, but each is one future edit away from it: the moment one owner changes behavior and the
sibling owner doesn't, the app has two disagreeing sources of truth for the same fact.

Source [verified]: `/Users/kimba/Projects/adia/adia-v2/.claude/docs/reports/2026-08-20-reactivity-data-audit/00-index.md`
§2 ("The recurring meta-pattern: fixed once, not swept").

## The diagnostic

1. **Search for a shared attribute/key/field name touched by more than one independent module,
   not just more than one line.** The `data-stream-src` case and the roster-name case both
   involve exactly one point of shared vocabulary (an attribute, a store key) with multiple
   INDEPENDENT write or read paths — that independence, not the duplication count, is what makes
   it dangerous.
2. **Rank by whether both owners can be live in the SAME session, on the SAME page, today.** The
   `data-stream-src` case ranks above the still-latent permission-matrix case precisely because
   the double-fetch fires whenever both modules are imported together — check adjacency/co-import
   before ranking severity, don't rank purely by "how many reimplementations exist."
3. **A "kept for backward compatibility" comment on one of the two owners is a signal to verify,
   not a reason to deprioritize.** `can()`'s own in-file comment says exactly this; the audit's
   own next step is "confirm nothing still depends on it diverging from `canDo()`, then either
   delete it or reconcile the two matrices into one" — the comment names the intended state, it
   doesn't prove the divergence is harmless today.
4. **The fix is unify-onto-one-owner, not a tagged union.** This is the axis's key distinction
   from `two-facts-one-name.md`: when investigation confirms the two owners really do mean the
   SAME fact (not two facts sharing a name), the right fix collapses them onto a single owner —
   reserve the tagged-union treatment for when they turn out to be legitimately distinct facts.
5. **When a fix for the collision already exists in one file, check the others before writing a
   new one** — see `adoption-verdict.md`'s "fixed once never swept" corollary for the
   sibling-sweep habit that closes this class permanently instead of one instance at a time.
