---
name: state-model-rules
description: >-
  Judges app-tier state ARCHITECTURE from a cited field-report corpus — stacked generations added
  without retrofit, a shared name masking two live facts, built-but-unadopted vs load-bearing
  layers, a named re-evaluation trigger nobody pulled, doctrine-vs-practice divergence per layer,
  one field with two live write-owners. Use for "why is our state a mix of implementations", "is
  this store actually used or just built", "did we ever revisit this decision", "two places both
  claim to own this field", "four generations of state pattern stacked in one app", "how do I
  audit our state architecture". ANSWERS the JUDGMENT call; NOT the reactivity MECHANISM
  (signal/effect internals) — reactivity-facts.
user-invocable: false
disable-model-invocation: false
---

# state-model-rules — app-tier state architecture judgment

Judges why an app's state ends up "a mix of implementations" and what to do about it — not by
citing a style guide, but from a corpus of dated, cited field reports across three independent
codebases (agent-ui, gen-ui-kit, adia-v2), each investigating the identical operator symptom.
The pattern that recurs across all three: individual solutions are well-reasoned; what's missing
is convergence — a fix built once and never swept, a trigger named and never pulled, two facts
that share a name and were never reconciled. This pack teaches the judgment calls, not the fix
mechanics.

| Ask | Load |
|---|---|
| "Why does this app have N incompatible state patterns stacked on top of each other" | `references/four-generations.md` |
| "Two things share a name (\"name\", \"active\", \"state\") but aren't the same fact" | `references/two-facts-one-name.md` |
| "Is this sanctioned layer/store actually used, or just built" | `references/adoption-verdict.md` |
| "We named a condition for revisiting this decision — did anyone ever check it" | `references/never-pulled-triggers.md` |
| "How far has practice drifted from what the doctrine says, layer by layer" | `references/doctrine-vs-practice.md` |
| "Two places both write the same conceptual field, independently" | `references/one-name-two-owners.md` |
| "How do I run this kind of audit on my own codebase" | `references/audit-technique.md` |
| Which file, at a glance, across all seven axes | `references/INDEX.md` |
| Provenance and grounding markers | `references/sources.md` |

## Consult procedure

1. Classify the ask against the seven axes above; load only the matching reference. Hunting one
   specific claim inside a file: Grep for the term first rather than reading the whole file.
2. Answer on the contract: **claim + cited file:line/report + the grounding marker
   ([verified]/[incident])**. Worked shape:
   > *"Our roster picker still shows the old name after a rename — is this a wiring bug?"* →
   name-collision ask → `two-facts-one-name.md` — check whether a debounce/subscribe call is
   missing (a real bug) or whether two structurally different identities share the English word
   "name" and were never wired to begin with (agent-ui's `select-menu-name-bug.md`: `Persona.label`
   vs `store.get('name')`, zero code path writes both, [incident]). The fix differs completely
   depending on which one it is.
3. State which axis the answer draws from and its grounding marker — never present a corpus
   citation as live-verified-today code if `sources.md`'s own disclosure says otherwise.
4. Route mechanism/build work at the boundary (below) — this pack judges architecture, it never
   explains a reactivity kernel or writes a store.

## Boundaries

- **This skill judges app-tier state ARCHITECTURE; it does not explain reactivity MECHANISM.**
  "Why did my effect refire twice", "computed vs signal vs effect", "guard a stale async
  response" are `reactivity-facts`' law — that pack explains the kernel a store runs on top of;
  this pack judges whether the store, the layer, or the convention around it is coherent. A
  question naming a specific stacked-generations app, an unswept fix, or a doctrine/practice gap
  is this pack's; a question naming a kernel primitive (signal/computed/effect/scope/sequence
  token) is `reactivity-facts`'.
- **Client-persistence facts belong to `persistence-facts`** — storage discipline tiers
  (schemaVersion/RENAME_MAPS vs ad-hoc JSON.parse vs cache-buster keys), whether a sync store next
  to an async storage seam is legitimate design or bypass drift, and URL-state sync. This pack's
  own `audit-technique.md` bypass-inventory technique (#2) is the general, cross-domain METHOD —
  `persistence-facts`' own audit-shape axis is the narrower storage-specific checklist built on top
  of it, not a competing method. A question naming a specific storage key, a rename risk, or a URL
  param is `persistence-facts`'; a question naming a whole app's mix-of-implementations symptom is
  this pack's.
- **Production component code, a reactivity kernel, or an app-tier store from scratch** →
  no owning builder skill in this plugin (same gap `reactivity-facts` names for its own
  territory) — derive the implementation inline against whichever axis file names the failure
  mode to avoid, rather than treating this pack as a builder.
- **UI pattern naming and the screen-state grammar** (loading/empty/error) stay
  `ui-pattern-facts`' law — a "these two stores disagree about who owns this field" ask and a
  "what should this empty state say" ask share no territory.

## Extending this pack

Extension: governed by [[make-pack]]
