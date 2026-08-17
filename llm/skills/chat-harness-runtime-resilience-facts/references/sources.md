# Sources — provenance for the chat-runtime producer-loop claims

This pack teaches a PATTERN, distilled from **one real, inspectable worked instance** — the
`agent-ui` repo's live-agent producer loop (`@agent-ui/a2ui`'s `produce.ts`, `meta-line.ts`,
`validate.ts`) — plus general platform facts. Three trust classes appear, and they are not
interchangeable (the same convention [[chat-harness-guardrail-facts]]'s own `sources.md` uses):

1. **Verified `file:line`** — a real path this authoring session opened directly and quoted from.
2. **Observed harness behavior** — a real system's stated rule reported at task-dispatch time,
   rather than a versioned file this session opened itself.
3. **Platform/vendor fact** — a general, durable claim verifiable against external documentation,
   not tied to the worked example.

## The `agent-ui` repo's live-agent producer loop — the worked system

**Verified `file:line`, TKT-0081, 2026-07-17** (full citation and worked-instance narrative live in
this pack's own `multi-turn-validation-and-state-seeded-gates.md` "Provenance" section — not
restated here to avoid two copies of one citation drifting apart):

- `packages/agent-ui/a2ui/src/renderer/validate.ts:56,66,232-233` — the session-seeded validator
  (`SurfaceSeed`, `validateA2ui(…, sessionSeed?)`) and the two gates that deadlocked before it
  (`root-missing`, the cross-turn id-graph guard).
- `packages/agent-ui/a2ui/src/agent/produce.ts:278,328` — `sessionSurfaceSeeds`, threaded into
  every round's validate call.

**Verified `file:line`, agent-ui#1115 "Scope-conformant revision v2" knowledge-harvest, 2026-08-17**
(the same fold documented in [[chat-harness-guardrail-facts]]'s own `sources.md`; this pack's slice
of it, moved out here 2026-08-17 by `plan-skill-split`, issue #552):

- `produce.ts:139-207` (ADR-0146 F3, GH #240/ADR-0159) — the three independent, fail-closed
  disclosure knobs (progress detail's stage/full/source ladder).
- `meta-line.ts:143-157,306-316` (GH #144) — the reserved terminal `error` meta-line and the
  runtime-vs-model field-authorship partition.
- `produce.ts:306-314,381-397` (GH #404, `.claude/ops/mb-live-proof/box2-quizmaster-FAIL.json`) —
  the observed live retry-bound exhaustion incident (temp 0.9, `box2-quizmaster`).
- `produce.ts:294-314` (GH #307) — `ProduceHalt`'s model-authored-id-only error rendering.
- `produce.ts:99-189`; `prompt-equivalence.test.ts`, `prompt-drift.test.ts` (`src/live-agent/`) —
  the additive-opt-in-flags byte-identity gates.

## Platform / vendor facts — verify against current docs if stale-sensitive

- **"Never ship a silent empty success after a transport commits 200"** — a general streaming-API
  design pattern, not specific to any one vendor's SSE/streaming implementation.
- **Fail-closed, independent opt-in knobs (no accidental ladder)** — a general API-surface design
  pattern for any additive, backward-compatible knob set.

## Boundary — what this pack does not restate

The provider/secret trust-boundary pattern (registry validation, dev-proxy, adapter injection) is
a different, narrower concern — see [[llm-gateway-facts]]'s own `sources.md`. The instruction,
safety, and config-authoring layer this pack's producer-loop content sits downstream of —
instruction layering, injection defense, action risk tiers, hook-vs-prose, config precedence, and
config-schema/prompt-externalization — is [[chat-harness-guardrail-facts]]'s, not restated here.
The self-correct feedback loop's own prompt design (what the retry-bound halt in
`failure-surfacing-in-a-chat-runtime.md` is the backstop for) is
[[chat-harness-workflow-facts]]'s `self-correct-feedback-design.md`.

## Provenance — 2026-08-17 plan-skill-split (issue #552)

This pack was minted by splitting `chat-harness-guardrail-facts`, whose axis count had drifted to
8 reference files (one past the `pack-writing-rules` 3-7 target) after the agent-ui#1115 v2
knowledge-harvest fold (PR #547) added `disclosure-and-failure-surfacing-in-a-chat-runtime.md` as
a file that its own header admitted CONSOLIDATED five distinct v2-harvest lessons (29, 31-34) to
hold the parent pack's file count at 8 rather than let it run to 10-11 — a documented,
first-party admission of literature-shaped bundling that `pack-writing-rules` names directly as a
failure ("two genuinely different question types never share a file"). `plan-skill-split`'s four
tests (sizing, ask co-occurrence, vocabulary separability, cost ledger) were run against the full
8-axis corpus; verdict: split. This pack receives the two agent-ui-grounded, deployed-chat-runtime
producer-loop axes (`multi-turn-validation-and-state-seeded-gates.md`, moved whole, and
`disclosure-and-failure-surfacing-in-a-chat-runtime.md`, moved then un-bundled in the same change
into `disclosure-knobs-and-progress-detail.md` + `failure-surfacing-in-a-chat-runtime.md`) —
distinct in both grounding (agent-ui's A2UI runtime vs. Claude Code's own CLI harness) and
vocabulary (validator/disclosure-knob/terminal-error-line vs. layering/precedence/risk-tier) from
the six axes `chat-harness-guardrail-facts` retains. Full manifest and rejected alternatives:
this repo's issue #552.
