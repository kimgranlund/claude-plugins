# Disclosure knobs and failure surfacing in a deployed chat runtime

> Axis: two adjacent concerns bundled deliberately into one file to hold this pack's axis count
> (already at 7 before this fold) — how much of the runtime's own internal state a disclosure
> knob may reveal, and how a runtime that has already committed to a response must still surface
> a failure loudly and safely rather than let it read as a silent, empty success. Grounded in a
> worked instance: `@agent-ui/a2ui`'s `produce.ts`/`meta-line.ts`. **Axis-budget note:** folding
> this v2-harvest content pushes `chat-harness-guardrail-facts` to 8 reference files, one past the
> pack-writing-rules 3-7 target — flagged as a split signal for a follow-up `plan-skill-split`
> pass, not resolved in this fold (see this ticket's PR body).

## Every disclosure knob is fail-closed and independent — no accidental ladder

**Claim — progress detail defaults to stage transitions only (no reasoning text); `'full'`
(bounded reasoning excerpts, capped ~200 chars) and `'source'` (raw payload lines behind
validate/retry stages, capped 16 KB with an EXPLICIT truncation marker, never a silent cut) are
separate opt-ins where one never implies the other.** A consumer needing both is a deliberate
future member, not a ladder accident. · `produce.ts:139-207` (ADR-0146 F3, GH #240/ADR-0159) ·
2026-08-17 · [verified]

## A stream that already committed 200 needs a reserved terminal error line

**Claim — once HTTP 200 is committed, a mid-stream halt yields a silently-empty "success"
client-side unless the transport itself composes a reserved terminal `error` meta-line (the last
line on the stream) — a line ONLY transports, never the model, may author.** Runtime-composed
fields (trace, error) and model-authored fields (note, ask, plan) are strictly partitioned by
author, so a consumer never has to guess which side wrote a given line. ·
`meta-line.ts:143-157,306-316` (GH #144) · 2026-08-17 · [verified]

## Halt loudly at the round bound — a loud halt is a feature

**Claim — a model repeating the identical mistake across every retry round (observed live at
temp 0.9) exhausts the self-correct budget and fails CLOSED with named failure codes, trading a
possible bad render for a diagnosable error.** Never widen the bound to chase a misbehaving
model; fix the feedback's teaching instead (see [[chat-harness-workflow-facts]]'s
`self-correct-feedback-design.md`). · `produce.ts:306-314,381-397` (GH #404, `.claude/ops/
mb-live-proof/box2-quizmaster-FAIL.json`) · 2026-08-17 · [verified][incident]

## Error text shown to end users may contain only model-emitted ids, never raw upstream text

**Claim — `ProduceHalt`'s `CODE at path` rendering is safe to surface directly to an end user
specifically because `path` is always a model-authored A2UI id, documented as a deliberate
invariant where the message is built.** A halt message that instead echoed raw upstream
provider text would risk leaking whatever that upstream text happened to contain. ·
`produce.ts:294-314` (GH #307) · 2026-08-17 · [verified]

## Additive opt-in flags must be byte-identical when absent

**Claim — every new knob added to the producer/provider seam (mode, effort, progress, tools,
genuiSurface, a2uiEnabled…) documents that its ABSENCE reproduces the prior request/stream
byte-for-byte.** This is what makes an evolving seam safe for existing consumers, and it is
TESTABLE, not just asserted — byte-pinned equivalence gates enforce it. ·
`produce.ts:99-189`; `prompt-equivalence.test.ts`, `prompt-drift.test.ts` (`src/live-agent/`) ·
2026-08-17 · [verified]

## What this file does NOT cover

The "browser cannot hold a secret" invariant — already covered by [[llm-gateway-facts]]'s
`dev-proxy-and-bundler-footguns.md` and `provider-adapter-seam.md` (a v2-harvest dedup: lesson 30
of the same source export is not restated here). Byte-pinning the PROMPT CONTENT itself (as
opposed to the seam's request/response shape) — already covered by this pack's own
`config-schema-and-prompt-externalization.md` (a v2-harvest dedup: the kept half of lesson 39 is
not restated here). The self-correct feedback loop's own design, which the round-bound halt above
is the backstop for: [[chat-harness-workflow-facts]]'s `self-correct-feedback-design.md`.
