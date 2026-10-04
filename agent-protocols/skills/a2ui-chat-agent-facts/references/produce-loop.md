# The produce() loop — bounded generate → heal → validate → self-correct

> Axis: the runtime driver that turns one `TurnInput` into a validated A2UI JSONL stream —
> retrieval conditioning, the catalog-derived prompt, the shared heal+validate gate, the
> feed-failures-back self-correct rounds, validate-then-stream, and halt-and-report. Grounded in
> `packages/agent-ui/a2ui/src/agent/produce.ts`,
> `packages/agent-ui/a2ui/src/agent/system-prompt.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R4/R5/R6/R7/N3). ADR-0070 = the runtime
> loop scope; ADR-0071 = the derived, drift-gated prompt. Verified against source as of 2026-07-07; round order and cites refreshed 2026-10-03 (see the UPDATE section).

## The loop, in order (SPEC-R4 / ADR-0070)

`produce(input, deps, opts)` is an `async function*` yielding validated JSONL lines
(`produce.ts`). Per turn:

1. **Retrieve** top-k exemplars over the JUDGED shard — `deps.retrieve(queryOf(input, k))`,
   `k` defaulting to 3 (`produce.ts`; SPEC-R7). The query intent is the turn's
   user content (`userContent` — the intent text, or the framed client message).
2. **Build the catalog-derived prompt** — `buildSystemPrompt(deps.catalog, exemplars)`
   (`produce.ts`; SPEC-R6).
3. **Generate** — accumulate the injected provider's text fragments into `raw`
   (`produce.ts`). `deps.provider` is the model seam (a stub in tests, a real adapter in
   the proxy), so the loop mechanics are gate-covered with no live model.
4. **Assemble + heal** — `assembleFromRaw` strips a wrapping code fence, splits into lines, and
   runs the shared healer PER LINE (`produce.ts`, `stripOuterFence`, `heal(line, …)`). An unparseable line → `undefined` → a `PARSE` failure fed back
   (`produce.ts`).
5. **Validate**, `validateA2ui(output, deps.catalog)` (`produce.ts`).
6. **On valid → validate-then-stream**; **on invalid → feed failures back and loop** (below).

## The shared gate — no fork (SPEC-N3)

**Claim — `heal` and `validateA2ui` are the SAME surfaces the renderer and corpus admission use;
the loop never forks them** (`produce.ts`; SPEC-N3). Validator parity is itself a
standing test. **Why:** a payload that passes the runtime gate is admissible and renderable by the
identical verdict — one correctness surface, not three.

**Claim — the deterministic gate is the WHOLE runtime verifier; there is NO runtime
rubric-grading round** (ADR-0070). The `a2ui-payload` rubric + the `a2ui-reviewer` critic are
authoring/eval-time only — a web demo has no seat to dispatch a critic mid-turn. **Caveat:** this
means the runtime guarantees *validity*, not *quality* — a valid-but-mediocre surface still ships.

## Self-correct: feed the failures back (SPEC-R4)

On an invalid round, `failures = verdict.failures` and the loop repeats (`produce.ts`). The
next round's messages append the prior INVALID attempt plus a directive listing the failure codes:
`"That output was INVALID (<codes>). Re-emit the COMPLETE corrected A2UI JSONL — nothing else."`
(`messagesFor` in `produce.ts`; the directive wording is a static hint plus `expectedTypeNote`). The model sees exactly what it emitted and what was wrong.

**Claim — the loop is bounded at `maxRounds` (the proxy passes 3) and ends in halt-and-report.**
If no round produces a valid payload, `produce` throws `ProduceHalt` carrying the last round's
failures (`produce.ts`). **Failure mode:** the page catches it and shows a
"could not compose a valid surface" system message — NOT a broken render (SPEC-R5;
`a2ui-live.ts:217-218`).

## Validate-then-stream (SPEC-R5 / SPEC-N4)

**Claim — a turn's payload is FULLY validated before ANY line reaches the browser.** Only after
`verdict.valid` does the loop yield: `for (const msg of output) yield JSON.stringify(msg)`, then
`return` (`produce.ts`). Nothing invalid is ever painted. It then streams line-by-line so
the surface still assembles progressively (root-early first paint), over the browser transport
that is identical for recorded and live paths (SPEC-N4; see agent-transport-seam).

## The model precedence rule — the trust boundary's teeth (SPEC-R12)

**Claim — `opts.model` wins over a client-supplied `input.model`:**
`opts.model ?? input.model ?? DEFAULT_MODEL` (`produce.ts`, `DEFAULT_MODEL = 'claude-sonnet-5'`). The proxy passes the allowlist-VALIDATED model as `opts.model`, so a crafted
`input.model` in a request body can never escape the PAIR check and reach the API
(`produce.ts`; see provider-model-seam-and-trust-boundary).

## The prompt is catalog-derived and drift-gated (SPEC-R6 / ADR-0071)

`buildSystemPrompt(catalog, exemplars)` = a fixed GRAMMAR + the component/function **inventory
derived from `catalog.json` at run time** + a `retrieve()`-sourced few-shot block
(`system-prompt.ts:68-77`, `catalogInventory` at `37-46`). **Claim — the model can never be told
about a component the catalog itself lacks:** a standing test (`prompt-drift.test.ts`) asserts the
derived inventory equals `Object.keys(catalog.components)` and each row's props; a planted catalog
row absent from the prompt FAILS it (SPEC-R6 AC1). **Caveat:** the GRAMMAR half is hand-authored
inline (a faithful copy of the `a2ui-compose` grammar); the drift gate covers only the
catalog-derived half — so a note-channel instruction (see
conversational-reasoning-and-click-routing-gap) would live in the grammar half without disturbing
the gate.

## Single-modality consumer prompt framing — the `exclusive` flag (issue #509)

**[incident]** — a real, dated live bug (`agent-ui gen-ui-live.html`, 2026-07-25), root-caused and
fixed; cited here from that report (memory `genui-exclusive-consumer-prompt-framing`; source
`genui-surface.spec.md` §10 v0.4 — re-verify against that spec text at the next refresh wave, not
independently re-checked from this pack's own repo). A shared system-prompt framing tuned for a
**COEXISTENCE** consumer — "A2UI stays your default; reach for genui only when the catalog cannot
express it" — silently misdirects a **GenUI-ONLY** consumer: the model still emits valid A2UI JSONL,
the transport still streams it, and a single-modality client drops every line by design. **Failure
mode:** zero errors anywhere in the pipeline — validate-then-stream still reports success (above) —
the only symptom is a blank surface, because the framing told the model a channel exists that this
particular caller never wired up.

**Fix pattern:** an explicit `exclusive` flag on the surface config composes an override paragraph
into the GRAMMAR naming the concrete fact — "this caller has no A2UI rendering path at all" — rather
than relying on the shared coexistence framing to degrade gracefully on its own. This is a GRAMMAR-half
change (see "The prompt is catalog-derived and drift-gated" above): it is hand-authored instruction
text, not something `prompt-drift.test.ts`'s catalog-inventory gate would ever catch, so it needs its
own explicit check rather than riding the drift gate's coverage.

**General law for this pack:** any prompt block that steers on an assumption about the CALLER's
rendering capabilities must be checked against every real consumer archetype the deployment actually
has, not just the one it was originally written for. A shared GRAMMAR string is a claim about every
caller that loads it, not just the first one.

## UPDATE 2026-10-03, the current round order and the produce-layer corrections

**[verified]** against `src/agent/produce.ts` and `corpus/heal.ts`, 2026-10-03. The numbered loop
above is the 2026-07 shape; the per-round order is now: **peel the meta-line, peel the genui
lines, heal per line, stamp the catalogId, validate (with session seeds and `atFinalize`), then
stream only validated lines.** Rounds are bounded (`maxRounds`, ADR-0070); self-correct hints are
static text plus an `expectedTypeNote`. The stamp step overwrites the model's `createSurface.catalogId`
with the server-selected one (`stampCreateSurfaceCatalogId`; see a2ui-catalog-facts
two-tier-extensibility). The validate call is `validateA2ui(output, catalog, sessionSeeds,
{atFinalize: true})`: seeds let a later-turn update reference earlier-turn ids, and `atFinalize`
is the turn-end-only judgment (see a2ui-protocol-facts message-lifecycle).

**Two produce-layer correction rounds, both degrade-never-halt (ADR-0187).**
- `NET_NOOP`: a turn whose `createSurface` is cancelled by a `deleteSurface` dodge is corrected
  once; if the model repeats it the dodge is stripped and the turn degrades to prose (tally
  `NET_NOOP_STRIPPED`).
- `FLOW_END_MISSING`: fires only when the turn is closing-shaped (a note with no ask, no plan, no
  genui line, zero A2UI lines, no `flowEnd`) AND the user's own message is an explicit close
  (`isExplicitClose`). One round, only if a round remains; otherwise the turn ships unchanged with a
  `FLOW_END_UNCORRECTED` tally.
These codes, together with `FEED_SCOPE`, `GENUI_ENVELOPE`, `GENUI_SIZE` and `GENUI_MULTIPLICITY`, are
produce-layer-only and never join the protocol `ErrorCode` union. A matcher miss degrades to no
round, never to a wrong rewrite (`NET_NOOP_HINT`, `FLOW_END_HINT`, the closing-shape branch).

**genui lines are dropped, not corrected, on the shipping round.** A structural failure of a genui line on the shipping
round is dropped from the wire; at most one genui line ships per turn, and extras are dropped and
counted (`multiplicity`), never fed back to the model. On a round that will retry, a genui failure
rides the same retry feedback as any other failure; only the shipping round drops it.

**Progress meta-lines are opt-in and byte-identical when absent.** The `progress` kind in
`meta-line.ts` is runtime-composed; `progressDetail` modes (`stages`, `full`, `source`) are
independent and capped, and `interleaveProgress` races progress against validated lines so the
status can paint while the model is still generating. **Failure mode:** a consumer that treats
progress as model-authored will wait for an arm the model never states.

## What this file does NOT cover

The transport that carries the yielded stream (agent-transport-seam) · what feeds `input`
(turn-session-and-input-intent) · the provider adapter `deps.provider` resolves to + where the key
lives (provider-model-seam-and-trust-boundary) · the retrieval internals of `retrieve()` and the
judged shard — this loop is a CALLER of retrieve(), not its owner ([[a2ui-training-facts]]) · the
`validateA2ui` failure codes + catalog conformance rules ([[a2ui-protocol-facts]], [[a2ui-catalog-facts]]).
