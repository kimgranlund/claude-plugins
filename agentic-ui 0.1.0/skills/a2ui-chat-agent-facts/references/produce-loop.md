# The produce() loop — bounded generate → heal → validate → self-correct

> Axis: the runtime driver that turns one `TurnInput` into a validated A2UI JSONL stream —
> retrieval conditioning, the catalog-derived prompt, the shared heal+validate gate, the
> feed-failures-back self-correct rounds, validate-then-stream, and halt-and-report. Grounded in
> `packages/agent-ui/a2ui/tools/agent/produce.ts`,
> `packages/agent-ui/a2ui/tools/agent/system-prompt.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R4/R5/R6/R7/N3). ADR-0070 = the runtime
> loop scope; ADR-0071 = the derived, drift-gated prompt. Verified against source as of 2026-07-07.

## The loop, in order (SPEC-R4 / ADR-0070)

`produce(input, deps, opts)` is an `async function*` yielding validated JSONL lines
(`produce.ts:109`). Per turn:

1. **Retrieve** top-k exemplars over the JUDGED shard — `deps.retrieve(queryOf(input, k))`,
   `k` defaulting to 3 (`produce.ts:110-111`, `59-61`; SPEC-R7). The query intent is the turn's
   user content (`userContent` — the intent text, or the framed client message).
2. **Build the catalog-derived prompt** — `buildSystemPrompt(deps.catalog, exemplars)`
   (`produce.ts:112`; SPEC-R6).
3. **Generate** — accumulate the injected provider's text fragments into `raw`
   (`produce.ts:119-127`). `deps.provider` is the model seam (a stub in tests, a real adapter in
   the proxy), so the loop mechanics are gate-covered with no live model.
4. **Assemble + heal** — `assembleFromRaw` strips a wrapping code fence, splits into lines, and
   runs the shared healer PER LINE (`produce.ts:94-107`, `stripOuterFence` at `83-87`,
   `heal(line, …)` at `102`). An unparseable line → `undefined` → a `PARSE` failure fed back
   (`produce.ts:130-132`).
5. **Validate** — `validateA2ui(output, deps.catalog)` (`produce.ts:134`).
6. **On valid → validate-then-stream**; **on invalid → feed failures back and loop** (below).

## The shared gate — no fork (SPEC-N3)

**Claim — `heal` and `validateA2ui` are the SAME surfaces the renderer and corpus admission use;
the loop never forks them** (`produce.ts:15-16`, `134`; SPEC-N3). Validator parity is itself a
standing test. **Why:** a payload that passes the runtime gate is admissible and renderable by the
identical verdict — one correctness surface, not three.

**Claim — the deterministic gate is the WHOLE runtime verifier; there is NO runtime
rubric-grading round** (ADR-0070). The `a2ui-payload` rubric + the `a2ui-reviewer` critic are
authoring/eval-time only — a web demo has no seat to dispatch a critic mid-turn. **Caveat:** this
means the runtime guarantees *validity*, not *quality* — a valid-but-mediocre surface still ships.

## Self-correct: feed the failures back (SPEC-R4)

On an invalid round, `failures = verdict.failures` and the loop repeats (`produce.ts:139`). The
next round's messages append the prior INVALID attempt plus a directive listing the failure codes:
`"That output was INVALID (<codes>). Re-emit the COMPLETE corrected A2UI JSONL — nothing else."`
(`messagesFor`, `produce.ts:68-79`). The model sees exactly what it emitted and what was wrong.

**Claim — the loop is bounded at `maxRounds` (the proxy passes 3) and ends in halt-and-report.**
If no round produces a valid payload, `produce` throws `ProduceHalt` carrying the last round's
failures (`produce.ts:117`, `141`, `46-53`). **Failure mode:** the page catches it and shows a
"could not compose a valid surface" system message — NOT a broken render (SPEC-R5;
`a2ui-live.ts:217-218`).

## Validate-then-stream (SPEC-R5 / SPEC-N4)

**Claim — a turn's payload is FULLY validated before ANY line reaches the browser.** Only after
`verdict.valid` does the loop yield: `for (const msg of output) yield JSON.stringify(msg)`, then
`return` (`produce.ts:135-137`). Nothing invalid is ever painted. It then streams line-by-line so
the surface still assembles progressively (root-early first paint), over the browser transport
that is identical for recorded and live paths (SPEC-N4; see agent-transport-seam).

## The model precedence rule — the trust boundary's teeth (SPEC-R12)

**Claim — `opts.model` wins over a client-supplied `input.model`:**
`opts.model ?? input.model ?? DEFAULT_MODEL` (`produce.ts:113`, `DEFAULT_MODEL = 'claude-sonnet-5'`
at `:23`). The proxy passes the allowlist-VALIDATED model as `opts.model`, so a crafted
`input.model` in a request body can never escape the PAIR check and reach the API
(`produce.ts:36-39`; see provider-model-seam-and-trust-boundary).

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

## What this file does NOT cover

The transport that carries the yielded stream (agent-transport-seam) · what feeds `input`
(turn-session-and-input-intent) · the provider adapter `deps.provider` resolves to + where the key
lives (provider-model-seam-and-trust-boundary) · the retrieval internals of `retrieve()` and the
judged shard — this loop is a CALLER of retrieve(), not its owner ([[a2ui-training-facts]]) · the
`validateA2ui` failure codes + catalog conformance rules ([[a2ui-protocol-facts]], [[a2ui-catalog-facts]]).
