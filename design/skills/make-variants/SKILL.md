---
name: make-variants
description: >-
  Publish an Artifact of N variants along declared axes, each card voted thumbs-up/down with a
  free-text note, serializing a live variant-feedback/v1 JSON block pasted back to resume —
  anchors kept, rejected axes mutated, same URL. Use when asked to explore variants of a
  component, show variants of X, give N takes on a layout, iterate on a design, or run a variant
  exploration — or paste a blob whose first key is "schema": "variant-feedback/v1" (resume). NOT
  for one finished design or a hand-editable canvas (design canvas skill, artifact-design); NOT
  for grading an artifact/component (design-system-checker, screens:component-checker); NOT for
  building the winner (screens:make-component).
disable-model-invocation: false
user-invocable: true
---

# make-variants

Produces N design variants that differ along DECLARED axes, published as ONE artifact whose
cards each carry a vote (up/down/unvoted) + free-text note widget, and whose page serializes a
`variant-feedback/v1` JSON block the user copies back to drive the next round at the SAME URL.
This skill owns the exploration contract — declared axes, stable ids, the feedback schema, the
one-artifact rule, the resume loop; `artifact-design` owns the visual craft of each card, cited
below rather than restated here.

## Procedure

1. **Declare axes.** From the request (or by asking once if the brief names no axes), fix 2-4
   design axes that meaningfully vary the target (e.g. `density`, `corners`, `tone`) and 2-3
   values per axis. N variants are a curated subset of the axis product — the combinations that
   differ most, not an exhaustive grid.
2. **Derive stable ids.** Each variant's id joins its chosen axis values in the axes' declared
   order (`compact-sharp-quiet`) — `references/feedback-schema.md` is this id scheme's contract
   and the full serialization shape; read it before building the page.
3. **Build ONE artifact.** Every variant card renders in its own namespaced style scope (a
   per-card class or scoped selector prefix keyed to its id), so each card's CSS stays local to
   that card — cards differ by declared axis, by construction, not by cascade order. Each card
   carries: the axis labels, a thumbs-up/thumbs-down toggle with three states (up / down /
   unvoted), and a free-text note field. Both light and dark themes render correctly
   (`artifact-design`'s theme doctrine governs this).
4. **Serialize the feedback block.** The page keeps a live `variant-feedback/v1` JSON block
   (`references/feedback-schema.md`) in sync with every vote/note edit, and offers a copy
   affordance: `navigator.clipboard.writeText`, with a `document.execCommand('copy')` fallback
   after a `select()` on a hidden textarea for contexts where the Clipboard API is unavailable —
   an Artifact page cannot offer a real file download, so clipboard is the export path.
5. **Republish to the same path.** The artifact's file path is fixed at round 1; every later
   round republishes to that SAME path. NEVER mint a new path on a later round, resume included
   — this is the one mechanism that keeps "same URL, next round" true for the whole session.
6. **Resume mode.** A pasted blob whose first top-level key is literally
   `"schema": "variant-feedback/v1"` is round input, not a new request — apply
   `references/feedback-schema.md`'s resume-mode read (anchors held, rejects mutated, unvoted
   held-but-uncited) and republish round `round + 1` to the same path from step 5.
7. **Terminate.** A "pick" (a named winning id) or an all-up round is the stopping predicate —
   hand the winning axis combination as a spec to the build skill the request named, or
   `screens:make-component` by default, then stop; no further round follows convergence.

## Fences

NOT for producing one finished, hand-editable design — the design canvas skill and
`artifact-design` own single-artifact craft; this skill's own job is running N variants through
a vote loop. NOT for judging an existing artifact or component against a rubric
(`design-system-checker`, `screens:component-checker` — those grade one already-built thing;
this skill generates and collects votes on several unbuilt ones). NOT for building the chosen
winner (`screens:make-component`, or the host repo's own build skill) — this skill's own
contract ends at a winning spec; the shipped component is the build skill's job.

## Failure branches

- Pasted blob's first key isn't literally `"schema": "variant-feedback/v1"` → treat as a new
  exploration request. NEVER guess-parse a differently-shaped or unversioned blob into this
  contract.
- No axes stated and none inferable from the target → ask once, naming 2-4 candidate axes; still
  unclear → park with the gap named, naming a design rationale for whichever axes get picked.
- An unvoted (`null`) card in a resumed round → hold its axes exactly like an anchor. An unvoted
  card is NEVER read as a downvote (`references/feedback-schema.md`'s serialization invariant).

Done when the artifact renders N axis-labeled cards with working vote+note widgets in both
themes, the JSON block live-updates and copies, and a pasted `variant-feedback/v1` blob
regenerates round N+1 at the same URL with anchors preserved and unvoted distinct from downvoted
in the serialization.

## Material

| Path / peer | Use |
|---|---|
| `references/feedback-schema.md` | the `variant-feedback/v1` contract — shape, stable-id derivation, resume-mode read |
| `artifact-design` (soft, global) | visual craft of each card and the page shell — cited, not restated |
| `artifact-capabilities` (soft, global) | the republish-to-same-URL mechanism step 5 depends on |
| `screens:make-component` | the default build-skill handoff at termination |
