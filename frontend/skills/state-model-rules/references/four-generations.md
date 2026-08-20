# The four-generations pathology

**The judgment call:** when an app's state reads as "a mix of implementations," don't reach for
a single unifying rewrite before naming each stacked layer's own era and trigger. A codebase that
grew features over time without a retrofit pass doesn't drift randomly — it accretes GENERATIONS,
each internally coherent when it was written, each added because the previous generation wasn't
retrofitted for the new feature's needs.

## The worked case [incident]

agent-ui's `agent-admin-app.ts` (the app Kim's own charter named as symptomatic — "there seems to
be a mix of implementations now, and it is evident in how agent-admin-app is implemented") is at
least four stacked generations of state-management pattern, each added for a feature without
retrofitting the ones underneath:

- **Gen 1 (oldest):** the generic `SettingsStore` contract + signals `effect()` inside
  `agent-admin.ts`. Genuinely reactive, well-documented, internally consistent.
- **Gen 2:** the persona/preset roster — hand-rolled `Persona[]` + raw `localStorage` keys,
  predating any shared persistence seam. The reported bug (a stale name in the header
  select-menu) lives here; never reconciled with Gen 1's store despite both holding "what is
  this agent called."
- **Gen 3:** page-owned imperative DOM layered on Gen 2, plus a component-side push seam
  (`#pendingRoster`/`setAgentRoster`) — a third place "the roster" lives, synchronized with Gen 2
  only by call-site discipline.
- **Gen 4:** the proper async persistence tier (`StorageAdapter`, ADR-0193). Most disciplined,
  but arrived after Gen 2 and was never extended to the roster bookkeeping — the app's newest and
  oldest persistence idioms sit side by side on the same page.

Verdict, quoted: "The Settings Name field belongs to Gen 1 (store key, reactively read); the
select-menu label and Team-pane GM line belong to Gen 2/3 (hand-pushed snapshot). Nothing ever
treated these as 'the same fact' — there is no missing subscribe call to add; there are two
genuinely separate identity models that both happen to be called 'the agent's name.'"

Source [verified]: `/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/agent-admin-app-state-audit.md`
(Mechanism inventory table + "Verdict — four stacked generations" section), cross-referenced by
`FINDINGS.md` F1/F2/F5 in the same corpus.

## The diagnostic

1. **Name each generation, not just "the mess."** Walk the mechanism inventory (every place a
   fact is held) and tag each with an era/trigger — what feature shipped it, what pattern it
   used, and whether it was ever retrofitted when the NEXT generation landed. A mechanism table
   with a "Judgment" column per row (signal-clean / manual-sync / manual-sync-by-convention /
   write-only-no-read-path) is the mechanical form of this — see `audit-technique.md`'s sync-point
   mapping technique.
2. **A live bug inside a stacked-generations app is usually a cross-generation seam, not an
   in-generation defect.** The individual generations here were each internally
   "signal-clean" or "clean for its own record" — the defect lives at the BOUNDARY between two
   generations that both think they own the same fact (see `one-name-two-owners.md`), or in a
   fact that changed identity model between generations (see `two-facts-one-name.md`).
3. **Don't recommend "rewrite it all" as the default fix.** The corpus's own forks-needing-a-
   ruling section frames each generational seam as a PRODUCT call (unify vs. keep-distinct), not
   an automatic refactor — see `two-facts-one-name.md`'s unify-or-keep-distinct fork.
4. **A second live instance of the identical defect class is the tell that this is systemic, not
   an isolated bug.** agent-ui's Team-pane `nameFor()` read the same stale roster snapshot the
   header picker did — same root cause, different surface. Finding one instance of a
   cross-generation seam bug is a strong signal to grep for siblings before calling the fix done.

## What this axis does NOT claim

Four is not a magic number — it's how many generations this one worked case had. The judgment
transfers regardless of count: name the generations, find the cross-generation seams, treat the
fix as a product call where identity models genuinely differ.
