---
name: a2ui-protocol-facts
description: >-
  The A2UI wire protocol + this repo's zero-dep renderer (@agent-ui/a2ui). Use for "why did this
  payload fail validation", "what does a binding/action/check look like on the wire", "how do
  dynamic lists render", "action vs function call", "which error code and why". Covers the
  message lifecycle, the Binding union, data-model updates, dynamic-list templates, DynamicString interpolation, the
  callFunction RPC, the error taxonomy, version pinning. ANSWERS from a cited corpus; does not
  build. NOT for catalog design (a2ui-catalog-facts); NOT for corpus records
  (a2ui-training-facts); NOT for the session/turn model or the live agent's validate-then-stream
  pipeline (a2ui-chat-agent-facts).
disable-model-invocation: false
user-invocable: false
---

# a2ui-protocol-facts — the wire model + renderer world model

Names and explains how an A2UI message stream becomes a live surface in `@agent-ui/a2ui`, so a
payload author, a debugger, or a reviewer can reason from the protocol instead of guessing. Six
retrieval axes, one per reference — each answering a distinct class of ask.

| Ask | Load |
|---|---|
| Message flow — "what happens on createSurface / updateComponents / deleteSurface?", "why isn't my tree rendering?", "how is the stream dispatched?" | `references/message-lifecycle.md` |
| Binding a value — "literal vs {path} vs {call}?", "how does updateDataModel propagate?", "why did only one widget update?", "is this pointer valid?" | `references/bindings-and-data-model.md` |
| List iteration — "how do dynamic lists render?", "why no per-item key?", "how does a relative binding resolve inside a list item?" | `references/dynamic-lists.md` |
| Interaction round-trip — "what does an action message contain?", "how does actionResponse correlate?", "how does two-way input work?", "wantResponse / sendDataModel?" | `references/actions-and-two-way-input.md` |
| Functions & validation — "action vs function call?", "how do checks / ${...} interpolation / @index work?", "client-side eval vs the callFunction RPC?", "callableFrom?" | `references/functions-and-checks.md` |
| Errors & versions — "which error code and why did I get it?", "why did this payload fail validation?", "VALIDATION_FAILED vs INVALID_FUNCTION_CALL?", "supported versions?" | `references/errors-and-versioning.md` |
| Provenance — where a claim comes from, spec-fact vs repo-choice | `references/sources.md` |

## Consult procedure

1. **Classify the ask** by axis (message flow · binding · list · interaction · function/validation ·
   error/version), then **Grep the term** in the matching reference and **Read that section** — the
   files are cited catalogs, not linear reads. Enter by search, not by reading top-to-bottom.
2. **Answer on the contract: claim + cited source (`file:line` or ADR clause) + the failure mode or
   caveat.** A protocol claim without its failure mode is half an answer. Worked example:
   > *"Why did my `callFunction` for `required` get rejected?"* → function/validation axis →
   > **claim:** the default catalog's `required` is `callableFrom: clientOnly`, and `clientOnly` is a
   > **hard floor** — most-restrictive-wins, order-independent (`call-function.ts:43-79`, ADR-0034
   > amendment). **Failure mode named:** a server `callFunction` for any `clientOnly` function emits
   > `INVALID_FUNCTION_CALL` + `functionCallId` (never invoked); it is NOT the render-time `FUNCTION`
   > error, and a permissive sibling catalog does not loosen it. **Caveat:** the default catalog ships
   > no server-invocable function — register a `remoteOnly`/`clientOrRemote` one in a project catalog.
3. **Verify before an action** (see `references/sources.md`): a `file:line` drifts as the renderer
   evolves — grep the symbol; an ADR clause may be superseded — confirm it still says what the
   reference claims. Recommending a stale citation is the pack's own failure mode.

## Deviation doctrine

Every default in the corpus carries its rationale, so a consumer knows when deviating is legal. The
protocol splits into two layers (`references/sources.md`): **wire facts** (v1.0-mandated — the
message envelopes, the two-code error contract, positional list matching, `@index` innermost-only,
`callableFrom` default) admit **no** deviation without breaking conformance (Constraint C1); **repo
mechanisms** (the 8-code internal taxonomy, per-path reactive waking, the bespoke positional
reconcile, `setPointer` structural sharing) are design choices whose rationale is recorded in an
ADR's Decision/Alternatives — a change there is an ADR-level decision, not a free edit. When a
payload or renderer question turns on "must it be this way," answer on which layer the fact lives in.

## Boundaries

- **This pack ANSWERS; it does not build, compose, or fix.** No renderer/catalog source edits, no
  payloads, no catalog rows. It explains what the protocol *is* and *why a payload behaves as it
  does*; it hands all making to the seats below.
- **Route all making:**
  - Compose / extend / debug an actual A2UI payload (message stream, node shapes) → the
    **`a2ui-composer`** agent (which runs the `a2ui-compose` skill's compose→validate→self-correct
    loop).
  - Build or fix renderer / validator / catalog / `protocol.ts` **source** → the **`a2ui-builder`**
    agent.
  - Grade a payload, a catalog row, or a corpus record → the **`a2ui-reviewer`** agent.
- **Sibling knowledge packs — route a question in their territory to them:**
  - Catalog authoring / coverage policy / type→widget resolution → the **`a2ui-catalog-facts`**
    pack (live).
  - The live demo's session / turn / provider / transport model → the **`a2ui-chat-agent-facts`**
    pack (live).
  - Corpus record format / admission / retrieval → the **`a2ui-training-facts`** pack (live).

## Corpus of record

This pack's deep-review routing corpus is checked in at `scripts/routing-corpus.json` (positive
asks that must land here + adversarial negatives drawn from the sibling packs' vocabulary). A
routing-eval or skill review reads it from there.

## Extending / re-syncing this pack

A missing axis, a stale reference, or "add X to this pack" is authoring work — route to
[[make-pack]] (this pack's factory: axis decomposition, grounded research waves, the typed
index). **Re-sync trigger:** when a cited SPEC/ADR is amended or a renderer symbol is renamed, re-run
the research wave for the affected axis, re-date `references/sources.md`, and re-verify the cited
`file:line`s and ADR clauses — a pack answering from a superseded edition is a false manifest with
citations. Never bolt an uncited file onto the corpus inline. Gate: where harness is installed, run
this workspace's skill lint (harness's `skill_lint.py SKILL.md`) to a clean pass, then the independent
`skill-checker` + `wording-checker` critics (generator ≠ critic); otherwise apply harness's
skill-authoring standard by hand as the checklist (frontmatter completeness, both invocation dials,
a cited corpus).
