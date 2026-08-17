# Multi-turn validation and state-seeded gates

> How the VALIDATION GATES around a multi-turn structured-output producer must relate to each
> other and to the session's accumulated state — and the failure mode where two individually
> correct gates trap the model with no legal output shape. Grounded in one real, directly verified
> worked instance — the `agent-ui` repo's TKT-0081 (a measured live defect and its shipped fix) —
> not sole authority; the pattern generalizes to any loop that validates per-payload while a
> stateful consumer enforces cross-payload rules. Verified directly, 2026-07-17. Moved 2026-08-17
> from `chat-harness-guardrail-facts` into this pack (`plan-skill-split`, issue #552) — this
> pack's own producer-loop axis, alongside disclosure-knobs-and-progress-detail.md and
> failure-surfacing-in-a-chat-runtime.md, rather than the CLI-instruction-layer axes
> `chat-harness-guardrail-facts` retains (instruction layering, hook vs. prose, and the rest).

## A per-payload validator in a multi-turn loop must judge the state the consumer will hold

**Claim — when a producer loop validates each turn's output before shipping it, and the consumer
(a renderer, a database, an API) enforces rules that span turns, the producer's validator must be
seeded with the session's accumulated state — a session-blind per-payload judgment will
eventually contradict the consumer.** Each gate can be individually correct: the payload validator
correctly requires a complete self-contained structure; the consumer correctly rejects a
re-delivery of something already delivered. Together they leave the model no output that passes
both — the two-gates deadlock.

**Worked instance, verified directly:** `agent-ui`'s A2UI producer validates every model round
with a shared validator before streaming (`validate-then-stream`). Standalone, that validator
required every component-bearing payload to contain the `root` component and to have no dangling
references (`packages/agent-ui/a2ui/src/renderer/validate.ts:232` — `root-missing`) — correct for
single-turn generation. But the RENDERER accumulates the component graph across turns and rejects
any second delivery of `root` (`validate.ts:233` — the cross-turn id-graph guard). So on a
follow-up turn, an honest incremental update (only the changed components) failed the producer's
gate, while the full-tree-with-root shape that passed it failed the renderer — measured live as a
visible client-error round trip on every game move. The fix: an optional session seed on the ONE
shared validator (`SurfaceSeed`, `validate.ts:56`; `validateA2ui(…, sessionSeed?)`,
`validate.ts:66` — absent means byte-identical behavior, so single-turn callers are untouched),
built by replaying the session's prior turns
(`packages/agent-ui/a2ui/src/agent/produce.ts:278` — `sessionSurfaceSeeds`, threaded into every
round's validate at `produce.ts:328`). Seeded, the validator judges the MERGED graph the consumer
will actually hold: incremental updates validate, and a cross-turn re-delivery fails inside the
producer's own self-correct loop — pre-wire — instead of shipping and erroring client-side.

## Persistent model "misbehavior" is a harness question before it is a model question

**Claim — when a model persistently emits the same wrong shape despite teaching, check whether
the harness left it a legal move at all before adding more prompt prose or another enforcement
gate.**

**Worked instance (the same TKT-0081 defect, read from the other side):** the system prompt
already taught "never resend root" and
the model demonstrably understood it (its self-corrections applied the taught wrapper idiom) —
yet every live session resent full trees, because that was the only shape that passed the
producer's session-blind gate. The misbehavior was the model's only rational escape from a
structural trap. The diagnostic ordering that found it, cheapest-correct-first: (1) is the rule
taught at all; (2) do the enforcing gates contradict each other — READ both enforcers' actual
rules side by side; (3) only then sharpen the prose. A third gate or a sterner prompt would have
deepened the trap. (The intake for this very fix originally designed an additional producer-side
"don't resend root" policy gate; reading the standalone validator's rules exposed that gate as a
deadlock before it shipped — recorded in the ticket's own Findings.)

## Catch cross-payload violations producer-side: a self-correct round is cheaper than a shipped error

**Claim — a violation caught in the producer's validate loop costs one internal retry; the same
violation shipped costs a consumer-side rejection, an error message routed back as a new turn,
and a user-visible failure.**

**Worked instance (the same fix's measured before/after):** the pre-fix flow was: invalid payload
streams → renderer rejects → error client-message echoes into the conversation → the error frames
a whole NEW model turn to heal — one full round trip per move, visible in the chat log. Post-fix,
the same violation feeds back inside the producer's bounded self-correct loop (the consumer's own
failure verdict string, so the model sees the identical vocabulary either way) and the corrected
payload is the only thing that ever ships. The cost of the capability is exactly one seam: the
validator accepts optional accumulated state, additive and default-off.

## Provenance

Worked instance: the `agent-ui` repo (`/Users/kimba/Projects/nonoun/agent-ui`), TKT-0081
(`.claude/docs/tickets/tkt-0081-produce-root-resend-guard.md` — includes the measured live defect,
the discarded-deadlock design turn, and the verification transcript: a full multi-move game with
zero validation errors). File:line citations verified against that repo's `main` at commit
`c8aee65`, 2026-07-17.
