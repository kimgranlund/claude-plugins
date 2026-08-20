# URL-state synchronization

**Grounding note:** this axis draws on a single corpus surveying 20 URL-state modules in one
production codebase — a rare case where a shared contract genuinely held across the whole
surface, with the drift concentrated in a few precisely-named spots rather than spread everywhere.

## The shared contract, and where it has NOT drifted [verified]

Across the whole surveyed corpus: read via `URLSearchParams`, write via `history.replaceState`,
merge rather than replace the existing query string, omit params at their default value, and
validate incoming values against a known render-option array before trusting them. This part is
consistent everywhere it was checked — worth stating plainly, since a "drift" audit that only ever
reports gaps risks implying nothing is disciplined; here, most of it is.

## push vs. replace [verified]

Every file in the corpus uses `replaceState`, never `pushState`, for filter/sort/paging changes —
one browser-history entry survives per PAGE VISIT, not per filter tweak. This is the corpus's own
consistent convention: a filter or page-size change is treated as "the same view, refined," not "a
new navigable destination." A consumer wanting the opposite (a back-button step per filter change)
would be a deliberate divergence from this corpus's convention, not an extension of it, and should
be named as such rather than assumed to be the default.

## PHI exclusion from URLs — disciplined, but not enforced [verified]

Free-text search parameters are excluded from the URL on any list surface whose underlying data is
patient- or user-identifying, and included on surfaces whose data is not (catalog, ontology,
practice/org search). Every file that makes either choice carries its own paragraph re-deriving
the same reasoning independently — there is no shared flag or helper that enforces "this list's
search param may only be modeled in the URL if the underlying data is non-PHI." The risk this
guards is real: a free-text query param carrying patient-identifying text would ride into browser
history, referrer headers, and any URL-logging layer (server access logs, analytics) — exactly the
exposure the exclusion exists to prevent. Today's implementations are correct everywhere checked,
but the mechanism is a per-page judgment call repeated afresh each time, not a gate — a tenth list
page could omit the reasoning paragraph and ship a PHI-adjacent param with nothing stopping it.

**The checklist this axis hands a builder:** does this facet carry free text that could contain a
name, ID, or other identifying value tied to a real person? If the underlying resource is
patient/user-scoped, exclude the param from the URL (or actively strip it after load) and write
down why at that call site until a shared enforcement helper exists — don't rely on the previous
file's reasoning transferring by convention alone.

## The confirmed multi-value-comma bug [incident]

A shared helper exists specifically to fix comma-collision in multi-value URL facets (measured: 5
of 630 real `drug_class` values in production data contain a literal comma, which a naive
`.join(',')`/`.split(',')` corrupts). Two board pages that carry array-valued facets both
bypass that helper and hand-roll the exact naive join/split it was built to replace — a confirmed,
currently-live bug, not a latent risk, and the gap is already named in the shared helper's own
code comments and a tracked ticket. This is the URL-state-specific instance of the same
lesson the discipline-tiers axis draws for storage: a fix that exists in the codebase only
protects call sites that actually route through it.

**Checklist addition:** does this facet accept multiple values? If so, route through the corpus's
own multi-value encode/decode helper rather than hand-rolling `join`/`split` — that exact
shortcut is the corpus's own confirmed, still-open bug, not a safe simplification.

## Divergent write-API shape, and why it's deliberate [verified]

One page in the corpus uses a patch-based write (`buildWorkspaceUrl(patch, existingSearch)`)
instead of the otherwise-uniform full-state write (`build<X>Url(state, existingSearch)`) used
everywhere else. This is a documented, deliberate choice: two independent owners on the same page
(a page-shell tab selector and a list-zone's own filters/sort) need to write to the URL without
clobbering each other's params, which a full-state rebuild would risk. A future third owner
joining that specific page needs to know a patch-based write is in effect there before touching
its URL state — the divergence is legitimate, but not self-evident from the rest of the corpus's
own convention.

**Checklist addition:** does more than one independent piece of UI write to this same URL
concurrently? If so, a patch-based write is this corpus's own precedent for that specific
situation — not a full-state rebuild, which the rest of the corpus otherwise defaults to.

## Sources

`/Users/kimba/Projects/adia/adia-v2/.claude/docs/reports/2026-08-20-reactivity-data-audit/06-url-state-sync-patterns.md`
— comparison table (all 20 modules), "Divergence examples" #1/#2/#4, and "Flagged: latent
multi-value-comma bug candidates". Reviewed 2026-08-20.
