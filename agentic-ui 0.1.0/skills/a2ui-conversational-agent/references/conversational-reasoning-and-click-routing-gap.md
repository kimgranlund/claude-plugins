# The conversational-reasoning & click-routing gap — the CURRENT gap + the PROPOSED design

> Axis: why the live-agent demo cannot yet explain "why X not Y", why every click forces a turn,
> and the PROPOSED (unbuilt) design that would close both. Grounded in the shipped source
> (`site/pages/a2ui-live.ts`, `packages/agent-ui/a2ui/tools/agent/{agent-transport,produce}.ts`,
> `packages/agent-ui/a2ui/src/renderer/{action,dispatch,renderer}.ts`,
> `packages/agent-ui/a2ui/src/examples/canvas-button.ts`) and in the design record
> **ADR-0088** (`.claude/docs/adr/0088-a2ui-live-conversational-channel.md`).

> ⚠ **STATUS — ADR-0088 is `proposed` (2026-07-07), NOT built and NOT ratified.** Parts 1–3 below
> are a design record, not shipped behavior. The proposed→accepted flip is Kim's alone (a hook
> enforces it — the author cannot self-ratify). When answering from this axis, say plainly which
> claims are SHIPPED (the two gaps) and which are PROPOSED (the three-part design). Do not
> attribute authority to something that does not exist yet. Authoring/revising this ADR routes to
> [[system-planner]] (via [[adr-author]]), never to this pack.

## Gap 1 (SHIPPED reality) — there is no natural-language channel

**Claim — `Turn.content` is A2UI-JSONL-only; no field, on the wire or in the session, carries
prose.** For an `assistant` turn `content` is defined as "the A2UI JSONL the agent emitted"
(`agent-transport.ts:30-31`). `produce()` yields ONLY validated A2UI —
`for (const msg of output) yield JSON.stringify(msg)` (`produce.ts:136`). The chat's "Agent: …"
line is **synthesized client-side** by `summarize()`, which lists message KINDS
("Emitted 3 A2UI message(s): createSurface, …"), never a sentence the model produced
(`a2ui-live.ts:187-193`). **Failure mode:** ask "why did you choose a Card over a Table" today and
there is nowhere for the answer to live — and nothing recorded to ground it in (see the trace,
below).

## Gap 2 (SHIPPED reality) — clicks route indiscriminately, though `wantResponse` is wired

**Claim — `handleClientMessage` turns EVERY client message into a full visible turn, with no
condition** (`a2ui-live.ts:224-229`). Meanwhile **`wantResponse` is wired end-to-end but unused
for routing:** the agent authors it on a `Button.action` (ADR-0011), the renderer reads it
(`renderer.ts:348`) and stamps it onto the emitted `A2uiAction` (`action.ts:87-96`,
`protocol.ts:174`). Its only live use is renderer RPC-correlation (register an `actionResponse`
slot when `wantResponse` is set — `action.ts:100-106`); the "should this click talk back" signal
is unread by the page. **Blocking discovery:** the committed backbone seed sets **no**
`wantResponse` — `action: { action: 'submit' }` (`canvas-button.ts:27`), as do most corpus action
buttons. So any rule of "absent ⇒ silent" would kill the shipped demo's turn-2 and regress every
existing action button — which is why the proposed default is opt-out, below.

## The PROPOSED design (ADR-0088, three coupled parts on ONE new wire mechanism)

Bundled deliberately (part 2 rides part 1's channel; part 3 is the routing half of the same "which
interactions are conversational" question). Ratify all three knowingly.

**1. The `note` channel — a reserved leading meta-line on the SAME `AsyncIterable<string>`
stream.** Each turn's output splits into a short natural-language `note` + optional A2UI JSONL
(only when the UI changes). The note rides as a meta-line emitted FIRST — a JSON object with a
reserved wrapper key and **no `version` field**, e.g.
`{"a2uiMeta":{"note":"I used a Card because you asked for a summary with one action."}}`.
- **Claim (PROPOSED, ADR-0088 pt 1) — the meta-line would be provably NOT an `A2uiServerMessage`.**
  Every server message carries `version` + one fixed envelope key (`dispatch.ts:36-43`); a
  versionless line routes to `VERSION_UNSUPPORTED`, *returned not thrown* (`dispatch.ts:76-78`) — so
  even a leaked meta-line would be fault-isolated.
- **Claim (PROPOSED, ADR-0088 pt 1) — `AgentTransport.turn`'s signature would stay byte-identical**
  (`agent-transport.ts:67-69`);
  the meta-line is a demo-transport framing convention, NOT part of the A2UI protocol. This is the
  wire-purity constraint (SPEC-N3 / ADR-0070 clause 3): prose must ride *beside* the validated A2UI
  stream, never inside it (smuggling it into a server message would fail the shared validator or
  pollute the judged corpus). `produce()` would peel the meta-line BEFORE heal/validate and yield
  it first; the page filters it before `host.ingest`, then
  `addMessage('agent', note ?? summarize(...))` — so `summarize()` demotes to a fallback and the
  recorded backbone (which emits no note) renders exactly as today.

**2. The decision-trace — a light, browser-held, per-turn record that grounds "why".** A compact
`TurnTrace` per turn — `{ turnIndex, query{intent,k}, exemplarIds[], rounds, healed,
failureCodes[], model }` — carried back on the same meta-line.
- **Claim (PROPOSED, ADR-0088 pt 2) — it would live browser-side, PARALLEL to `session.turns`, not
  inside it.** `session.turns` is
  the Messages-API payload the model consumes; polluting it changes what the model sees (see
  turn-session-and-input-intent). It is also not on the A2UI wire. The proxy is stateless
  (ADR-0072 clause 4), so the browser holds it as it holds the session.
- **Claim (PROPOSED, ADR-0088 pt 2) — an explain-turn would be a normal `intent` turn, no new
  `TurnInput` kind.** The page would
  inject a digest of recent `TurnTrace`s (plus retained prior `note`s — the model's own
  at-the-time rationale) as extra context, so the answer cites REAL retrieved exemplars and real
  correction history. **Why the trace at all:** the retrieve/heal/validate material that drove the
  choice is consumed inside `produce()` and discarded; without recording it, an explain-turn would
  confabulate a retroactive justification (the exact gap this closes). The material to ground a
  "why" is retrieval over the judged shard — this pack is a CALLER of that; retrieval internals are
  [[a2ui-training-corpus]].

**3. `wantResponse`-routed click→turn — the agent's per-action talk-back choice, back-compat by
default.** `handleClientMessage` would route on the `action` arm's `wantResponse`:
- `action.wantResponse === false` → **silent apply** (no chat entry, no `runTurn`, no LLM round-trip).
- `wantResponse === true` OR **absent** → today's full visible turn.
- `functionResponse` and `error` arms **always** run a turn (inherently agent-directed).
- **Claim (PROPOSED, ADR-0088 pt 3) — the default would be deliberately opt-out, not opt-in:**
  absent `wantResponse` keeps current
  behavior, so the committed seed (`canvas-button.ts:27`) and every existing corpus action button
  still trigger turns and the shipped backbone is untouched. Which clicks talk back becomes the
  AGENT's authoring decision (it already sets `wantResponse` per action, ADR-0011) — no hardcoded
  client rule. **Caveat — `wantResponse` would carry two layer-local meanings** (renderer:
  RPC-correlation slot; page: routing hint) — documented and non-colliding today because no
  `actionResponse` RPC is wired for actions in this demo.

## The ONE open fork (Kim's call) vs the two build-time re-verify points

- **Fork — the routing default (part 3).** Ship the back-compat **opt-out** (recommended: absent
  keeps today's behavior; no re-seed) vs the RPC-aligned **opt-in** (cleaner semantics but breaks
  the demo's turn-2 and forces re-seeding transcript + corpus + prompt). A values trade-off with no
  empirical answer — hence Kim's, not the builder's.
- **NOT forks — decided-with-caveat, settled empirically at build:** (a) is the light objective
  `TurnTrace` enough for a grounded "why", or must the prompt teach the model to CITE it
  (answered by running a real explain-turn); (b) *when* to upgrade the meta-line to a typed
  transport frame (a future "if meta kinds proliferate" trigger, not a choice now).

## Alternatives ADR-0088 considered and rejected (each citable)

- **A typed transport frame** (`turn(): AsyncIterable<{kind; …}>`) — cleaner (no in-band sniffing)
  but changes the SPEC-R1 typed contract + every transport signature; rejected as the v1 shape,
  recorded as the natural upgrade if meta kinds proliferate.
- **Smuggle the note into an `A2uiServerMessage`** — rejected: fails the shared validator or
  pollutes the judged corpus (wire purity).
- **Rely on the model to justify retroactively (no trace)** — rejected: confabulation, since the
  driving context is gone by explain-time.
- **Record the trace proxy-side** — rejected: the proxy is stateless (ADR-0072 clause 4); the
  browser holds it.

## What this file does NOT cover

The shipped transport the meta-line would ride (agent-transport-seam) · the shipped turn/session
model an explain-turn reuses (turn-session-and-input-intent) · the shipped loop that would peel +
emit the meta-line (produce-loop) · the wire shape of `wantResponse` / `action` / the error
taxonomy ([[a2ui-protocol]]) · building the note channel / routing in SOURCE (the
[[a2ui-builder]] agent) · composing a payload that sets `wantResponse` (the [[a2ui-composer]]
agent) · authoring or ratifying ADR-0088 ([[system-planner]] / [[adr-author]]).
