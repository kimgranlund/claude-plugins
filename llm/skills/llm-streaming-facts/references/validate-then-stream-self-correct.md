# Validate-then-stream — never emit invalid structured output, bounded self-correct

> Axis: how to stream structured output (JSONL — one record per line — or any other structured
> format) from an LLM without ever handing a consumer a partial, malformed, or schema-invalid
> record, even when the model itself gets it wrong. Grounded in a worked instance:
> `packages/agent-ui/a2ui/tools/agent/produce.ts` in `@agent-ui/a2ui`.

## The core rule — validate the WHOLE output before streaming ANY of it

**Pattern — accumulate a full round's raw output, parse + validate it completely, and only THEN
stream the individual records out** — never stream a record as it's generated and validate it
after the fact. **Why this ordering, not the reverse:** a consumer of a "stream first, validate
later" design has already rendered/acted on a record by the time invalidity is discovered — there
is no clean way to un-render something a consumer already trusted. Validating the WHOLE
accumulated output before the first byte streams down means a consumer NEVER sees anything that
later turns out to be wrong; the cost is that nothing streams progressively WITHIN one round (an
acceptable trade for correctness — see the caveat below on where progressive rendering can still
happen safely).

**Worked instance:** `produce.ts:286-295` (accumulate the full raw text from the provider's
fragment stream before doing anything else with it — `raw += frag`), `:313,318` (`assembleFromRaw`
then `validateA2ui` run over the COMPLETE accumulated output — precisely `rest`, the raw text
minus a small A2UI-specific leading metadata line peeled off earlier in the round, `:297`; this
pack generalizes that as "the complete accumulated output," since the peel step itself is a
protocol-specific detail out of this pack's scope, not part of the portable pattern), `:319-341`
(only on a valid verdict does the loop `yield` anything at all — one line per structured record,
`:340`). **Caveat — this
does not forbid progressive UI rendering entirely:** a consumer CAN render each already-validated
line as it arrives (progressive paint), because by the time any line streams out, the WHOLE
round's output has already passed validation — "progressive" here means "the consumer paints
incrementally from a stream of already-guaranteed-valid records," never "the consumer paints
speculatively from not-yet-validated model output."

## The latency price, and the leading meta-line that pays it down

**Claim — validate-then-stream forfeits the early token BY DESIGN: the consumer sees nothing from
a round until the whole round has accumulated and validated, so the first visible output lands as
a late burst, not a trickle.** Budget for that honestly in the product; the perceived-latency
mitigation is a SMALL early validated unit, never a relaxation of validate-before-stream.

**The mitigation — reserve the round's FIRST emitted line as a protocol-known META-LINE** carrying
the model's one-line natural-language answer plus turn metadata, parsed as a typed envelope and
peeled before the structured payload behind it is validated. Because it is first in the emitted
sequence, a consumer renders the human-readable answer the instant it arrives, while the payload
burst is still ingesting and rendering — the one-line answer beats the burst, and the
no-early-token cost is felt as "a beat of silence, then an answer, then the UI," not "silence,
then a wall." This does not bypass the validation ordering: nothing emits until the round
validates; the meta-line only guarantees the first thing OUT of the pipe is the smallest, most
immediately useful unit. The note-only round (last section of this file) is its degenerate case —
a meta-line and zero records is a complete, clean answer. **Worked instance:** `produce.ts:297`
(the peel) + `src/agent/meta-line.ts` (`readMetaLine`, the `A2uiMetaEnvelope` typed envelope) in
`@agent-ui/a2ui`; the same repo treats the meta-line as a first-class wire citizen end to end —
its debug timeline routes `meta` lines as their own event kind (ADR-0200 clause 4), and a later
protocol addition (`flowEnd`) rode the meta-line envelope precisely because it was the established
additive-metadata home (agent-ui #1101, closed 2026-08-17) · 2026-08-19 · [verified]

## Structured parsing before validation — heal, then check the schema

**Pattern:** before schema validation, run a narrow, MECHANICAL healing pass over the model's raw
output — strip an unwanted markdown code fence the model added despite instructions, per-line
parse (when the format is one-record-per-line, parse and heal each line independently, since one
malformed line elsewhere in a batch shouldn't be allowed to invalidate lines that parsed fine),
and bail cleanly (a distinguishable PARSE failure, not a crash) if any line is fundamentally
unparseable. **Worked instance:** `produce.ts:130-136` (`stripOuterFence` — a single wrapping code
fence, if present), `:150-165` (`assembleFromRaw` — per-line heal + parse, returns `undefined` on
the first unparseable line, mapped by the caller to a PARSE failure). **Why heal at all, rather
than just validate the raw text as-is:** a model asked to emit strict structured output will
still, occasionally, wrap it in a code fence or leave a trailing comma — mechanical, narrow,
FORM-only repairs (never semantic ones) absorb that noise before it ever reaches schema
validation, so validation failures are reserved for genuine content problems, not markdown-fence
noise.

## The bounded self-correct loop — feed failures back, don't just retry blindly

**Pattern — on an invalid round, don't discard the failure and simply ask again identically; feed
the model back exactly what it emitted plus the STRUCTURED validation failures, and ask for a
corrected re-emission:**

Illustrative pseudocode, not the cited code verbatim (the worked instance below uses real
TypeScript with its own control flow):

```
for round in 0..maxRounds:
  raw = accumulate(provider.stream({ model, system, messages: withPriorFailures(failures, lastRaw) }))
  parsed = healAndParse(raw)
  if parsed is unparseable: failures = [PARSE]; continue
  verdict = validate(parsed)
  if verdict.valid: stream each record; return
  failures = verdict.failures   // fed back into the NEXT round's prompt
throw Halt(failures)             // maxRounds exhausted — a distinguishable, structured failure
```

**Worked instance:** `produce.ts:284` (the bounded `for` loop), `:343` (`failures =
verdict.failures`, fed back), the failure-feedback framing itself at `:110-128`
(`messagesFor` — appends the prior invalid raw output AS an assistant turn, then a user turn
naming exactly which structured failure codes were seen, asking for a complete corrected
re-emission). **Why feeding the ACTUAL prior output + the ACTUAL failures back, rather than just
re-asking the same question:** a model correcting blind (no memory of what it got wrong) tends to
repeat the same mistake or drift to a different one; showing it its own output plus the specific,
structured reason it was rejected gives it the information it needs to converge.

## Halt-and-report — a bounded loop must fail loudly and specifically, never silently

**Pattern — when the round bound is exhausted without ever producing valid output, raise a
distinguishable, typed failure carrying the LAST round's structured failures** — never an
unbounded retry, never a silent empty response, never a raw unhandled exception. **Worked
instance:** `produce.ts:91-99` (`ProduceHalt`, a named error class carrying `failures: 
RoundFailure[]`), `:345` (thrown only after the bound is genuinely exhausted). A caller catches
this ONE distinguishable type and shows a clear "could not produce a valid result" state — never a
broken partial render, never a generic crash.

## An empty-but-clean result is not the same as an invalid one

**Pattern worth generalizing:** if your protocol allows a round to legitimately produce a
prose-only or zero-record response (e.g. the model just wants to say something, with no
structured payload this turn), that is a SUCCESS with zero records streamed — not a failure, and
not something the self-correct loop should retry against. Conflating "nothing to stream" with
"invalid" wastes a retry round correcting something that was never wrong. **Worked instance:**
`produce.ts:303-311` — a note-only round (zero structured lines, a leading meta-line present) is
treated as a clean success and returns immediately, never entering the self-correct path.

## What this file does NOT cover

How the raw text this operates on was correctly assembled from a chunked stream in the first place
(sse-chunk-parsing-technique, anthropic-sse-worked-example) · the provider/session
plumbing this loop is called from ([[llm-gateway-facts]]).
