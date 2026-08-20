# Built-but-unadopted vs. load-bearing — judge a layer by its real consumers

**The judgment call:** a sanctioned architectural layer is not "the answer" just because an ADR
ratified it. Before recommending a team migrate onto a layer, or flagging six bypasses of it as
drift, check which side of the adoption line it's actually on — a layer with zero real consumers
outside its own tests/docs needs a first real consumer or an explicit "deliberately shelved"
record, not more bypass-shaming; a layer with genuine multi-consumer adoption earns the bypass
inventory and the migration push.

## The worked case [verified]

agent-ui ratified two persistence-adjacent layers. Only one is real:

- **`@agent-ui/data` (ADR-0192): built-but-unadopted.** "Ratified 2026-08-16, shipped with full
  core/gateway/stream surfaces, size budgets, tests — but nothing outside its own package and the
  docs site calls `resource()`, `mutation()`, `paginated()`, `DataSource`, or the gateway client
  for real application logic." The one subpath with real cross-package use (`./stream`'s NDJSON
  hoist, six real consumers) is adoption of ONE hoisted function, not the CRUD grammar the ADR
  was actually about — don't count a narrow utility export as adoption of the layer it ships
  inside.
- **`StorageAdapter` (ADR-0193): load-bearing, real.** Four production modules genuinely persist
  through it (two localStorage, two IndexedDB tiers), and a 2026-08-17 amendment closed the one
  gap that used to bypass it. "It is the one part of the 'mixed implementations' picture that is
  NOT mixed" — but it still coexists with six site-level modules hand-rolling `localStorage` for
  page-level concerns, INCLUDING a full duplicate `SettingsStore` reimplementation
  (`agent-admin-presets.ts`) that duplicates what the sanctioned seam already does.

Source: `/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/data-persistence-layers.md`
(the "Sanctioned layers table" + "Adoption verdict" section); `FINDINGS.md` F4/F5/F8 name the same
split as, respectively, a SYSTEMIC finding (dead weight or unrealized plan) and two lower-severity
bypass findings.

## The corollary: fixed-once-never-swept is a load-bearing-layer failure mode too [incident]

Even a genuinely load-bearing convention decays the same way if nobody sweeps it. adia-v2's
audit named this as the single meta-pattern behind every one of its six axes: "a good fix or a
good convention gets built once, in one file, and never gets swept across its siblings." The
one CONFIRMED live bug in that corpus is exactly this shape: a comma-encoding helper
(`encodeMultiValue`/`parseMultiValue`) was written and tested for one URL-state bug, and two
sibling files with the IDENTICAL failure mode never adopted it — "picking a comma-bearing
`drug_class` value today sends the gateway two facets that don't exist and silently paints an
empty result with no error." The fix already existed in the same package; it just never got
back-ported.

Source: `/Users/kimba/Projects/adia/adia-v2/.claude/docs/reports/2026-08-20-reactivity-data-audit/00-index.md`
§1 ("The one confirmed live bug") and §2 ("The recurring meta-pattern: fixed once, not swept" —
also cites the stale-request-guard family, the two permission-check matrices, and the
practice-id-resolution family as further instances of the same shape).

## The diagnostic

1. **Count real consumers, not ADR intent.** Grep the actual import graph for the layer's public
   surface; a layer whose only importers are its own tests, its own docs page, or a displayed-
   but-never-executed code snippet is unadopted regardless of how thorough its ratification was.
2. **A narrow-subpath adoption is not grammar adoption.** If a layer ships several surfaces (a
   CRUD grammar plus a streaming hoist, say) and only one narrow surface has real callers, name
   that precisely — "adoption of one hoisted function" is a materially different verdict than
   "adoption of the layer."
3. **Give an unadopted layer a ruling, not a silent extension deadline.** The report's own
   recommendation: either it gets a first real consumer (often the exact feature whose ad hoc
   state motivated the audit) or it gets recorded as deliberately-shelved so its unadopted state
   stops reading as drift nobody noticed.
4. **A load-bearing layer's bypass inventory is still worth taking, even when the layer itself is
   healthy** — real adoption doesn't mean universal adoption; six site-level bypasses coexisted
   with a genuinely load-bearing `StorageAdapter`. List them, and separate "the app's most central
   state is on the wrong seam" (high stakes) from "a page-level nav-collapsed flag bypasses it"
   (low stakes, hygiene only).
5. **When a fix already exists somewhere in the tree, check for siblings with the identical
   failure mode before writing a new one.** The adia-v2 pattern generalizes past persistence:
   stale-request guards, permission matrices, and practice-id resolution all forked into 2–5
   independent reimplementations of the same already-solved idea, each individually reasonable,
   none reusing the first.
