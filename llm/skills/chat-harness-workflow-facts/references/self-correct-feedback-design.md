# Designing the self-correct loop's feedback — not just that it retries, but what it says

> Axis: given a bounded generate→validate→retry loop already exists (see
> `validate-then-stream-self-correct.md` in [[llm-streaming-facts]] for the loop's own shape),
> what the FEEDBACK fed into round N+1 must actually contain for the model to converge instead of
> repeating the same mistake. Grounded in a worked instance: `@agent-ui/a2ui`'s producer,
> `packages/agent-ui/a2ui/src/agent/produce.ts`.

## Name the expected value, never just the failure code

**Claim — a failure code alone teaches the model nothing; feedback must carry the code, the path,
and the expected type/enum value resolved from the catalog and the model's own prior output.** A
bare code like "CATALOG at lbl_in.emphasis" produced identical wrong guesses across whole retry
rounds in live repros; naming the expected type/enum broke the loop. · `produce.ts:515-544`
(`expectedTypeNote`, GH #288/#397) · 2026-08-17 · [verified][incident]

**Why this matters:** a self-correct loop that feeds back only "you were wrong" without saying
what "right" looks like is functionally the same as a blind retry — it burns retry-round budget
re-deriving information the loop already has and could have handed over on round one.

## Static repair hints per failure class, ordered safest-first

**Claim — a per-failure-class STATIC hint naming the concrete repair beats generic "re-emit
corrected output," and the safe repair must be ordered FIRST.** PARSE failures (pretty-printed
JSON across lines, trailing prose, a literal `</parameter>` tool-tag bleed-through at temp 0.9)
and IDGRAPH failures (duplicate root, missing root, dangling ref, cycle) each repeat identically
under generic feedback. A hint opening with "send only what changed" invited compliant rounds
shipping unparented orphans that validate but never render — ordering the safe repair first
closed that trap. · `produce.ts:392-479` (PARSE_HINT, IDGRAPH_HINTS incl. the review-F1 ordering
note; GH #307/#404) · 2026-08-17 · [verified][incident]

## Pin the user-visible reply's audience inside the correction loop

**Claim — every retry prompt must explicitly restate that the user-facing note addresses the
USER, in persona, never the correction machinery.** Without that explicit instruction, a
compliant model narrates its own compliance in the user-facing note ("Re-emitting the corrected,
validated JSONL…", observed live) — the correction succeeded but leaked its own internal process
into what the end user reads. · `produce.ts:349-355,497` (GH #174) · 2026-08-17 ·
[verified][incident]

## What this file does NOT cover

The bounded loop's own shape — accumulate, validate whole, retry, halt-and-report — and the
distinction between an empty/clean result and an invalid one: [[llm-streaming-facts]]'s
`validate-then-stream-self-correct.md` (a v2-harvest dedup: lessons 1 and 5 of the same source
export are already fully covered there and are not repeated in this pack). The chain-of-command
pattern for when a HUMAN-authored plan needs repair after a discovered constraint (a different
kind of "feedback loop," at the multi-agent level, not the single-producer retry level):
`multi-agent-decomposition-and-chain-of-command.md`.
