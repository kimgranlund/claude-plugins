# Two facts, one name — and why a tagged union beats "just wire it up"

**The judgment call:** when two parts of an app both claim to hold "the X," check whether they
are actually the SAME fact with a missing wire, or two structurally DIFFERENT facts that happen
to share an English word. The fix is completely different depending on which one it is — and
treating the second case as the first (bolting on a subscribe call) produces a coupling nobody
asked for, while treating the first case as the second (declaring them "different by design")
leaves a real bug unfixed.

## The worked case [incident]

agent-ui's motivating symptom: the header agent-select menu stuck reading "New agent 48" while
the Settings panel's Name field said "Wrench." The investigation's bottom line: **never wired,
and it isn't a wiring bug** —

- The select-menu's label comes from `persona.label` (`Persona` roster/catalog identity) — set
  once at mint time, changed only through a dedicated rename affordance.
- The Settings Name field writes `store.get('name')` (a per-persona memory-store key, schema
  field `key: 'name'`) — read only by the per-turn `AgentConfigSnapshot` builder that feeds
  prompts and team-card mapping, never by the roster picker.

"`personaStore` exposes a `subscribe` seam, but its one wired subscriber only bumps a
`modifiedAt` localStorage marker. Nothing subscribes for `key === 'name'` to call
`pushRoster`/`renameImportedPersona`; `agent-admin-app.ts` has no `onFieldChange`-style hook at
all." The blur/Enter commit delay is real but doesn't explain the bug — the select-menu was
never a subscriber of that key AT ALL.

Characterization: **wired-but-disconnected-by-design.** Two legitimately different concepts share
the word "name" — roster identity (organizational identity in the picker/drawer/notifications,
edited only via a dedicated rename) and turn-time agent identity (what the agent calls itself
during generation, feeding prompts). The report frames this explicitly as an unruled FORK, not a
bug with one obvious fix: **unify** (subscribe the roster to the store's `name` key and drive the
same rename path the drawer uses) or **keep distinct** (reword the schema field's label so it
stops promising a roster rename it doesn't do).

Source: `/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/select-menu-name-bug.md`
(full trace + "Characterization and the fork" section); the same corpus's `FINDINGS.md` "The
forks needing a ruling" #1 states this explicitly as a product call blocking the fix.

## A second shape of the same defect [verified]

gen-ui-kit's framework survey found the identical shape one layer up, at the DOCTRINE level
rather than one app's bug: no single sanctioned context/shared-state mechanism exists — three
structurally unrelated point solutions (event-registry for forms, direct signal push for field
labelling, CSS cascade for theming) all answer "how do components share state," and nothing
unifies them under one name or one contract. See `never-pulled-triggers.md` for why that
divergence, specifically, was never resolved.

Source: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
F3 ("Two A2UI runtimes with incompatible data models" is the sibling instance at the runtime
layer — two systems solving the identical mount/data-binding problem under different names,
`Cell/Derived` vs plain-object re-apply-all).

## The diagnostic

1. **Before writing a fix, ask: do these two facts share ONE identity model, or two?** Trace
   each candidate "name" back to where it's WRITTEN and by what path. If the write paths never
   intersect and the values seed from different defaults at creation time (as `Persona.label`
   and `store.get('name')` do), they are two facts — not one fact with a missing wire.
2. **Model two genuinely different facts as a tagged union or two distinctly-named fields, not
   an implicit synonym.** The failure mode this axis names is exactly the opposite of premature
   unification: don't collapse two facts into "the name" just because English has one word for
   both; give each its own name in the schema/type once the investigation confirms they're
   separate.
3. **When they ARE the same fact wired twice (see `one-name-two-owners.md` for that sibling
   shape), unify onto the single owner instead of maintaining a tagged union — the union is the
   right tool only when the facts are legitimately distinct.**
4. **Escalate a same-name/different-fact finding as a product fork, not a silent engineering
   call.** Both real-world cases in this corpus (the agent-name bug, the context-mechanism gap)
   were left as open, explicitly product-owned decisions rather than auto-resolved — naming the
   fork IS the deliverable when the investigation reaches this point.
