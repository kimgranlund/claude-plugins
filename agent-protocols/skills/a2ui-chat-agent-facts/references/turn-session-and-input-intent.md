# Turn / Session / TurnInput — the multi-turn model and input-intent handling

> Axis: the turn-history data model the browser holds, how the two `TurnInput` kinds ("intent"
> text vs a "client" message reduced from a UI action/functionResponse/error) frame the next turn,
> and how "the agent continues." Grounded in
> `packages/agent-ui/a2ui/tools/agent/agent-transport.ts`,
> `packages/agent-ui/a2ui/tools/agent/session.ts`, `site/pages/a2ui-live.ts`,
> `.claude/docs/specs/specs/a2ui-live-agent.spec.md` (SPEC-R8). ADR-0072 = the multi-turn session
> model. Verified against source as of 2026-07-07.

## The shapes (SPEC-R8 / ADR-0072)

```ts
type Role = "user" | "assistant"
interface Turn { role: Role; content: string }   // assistant.content = the emitted A2UI JSONL
interface Session { turns: Turn[] }
type TurnInput =
  | ({ kind: "intent"; text: string; session: Session } & ProviderSelection)   // turn 1: free text
  | ({ kind: "client"; message: A2uiClientMessage; session: Session } & ProviderSelection) // later turns
```

(`agent-transport.ts:24-57`.) **Claim — this is the standard Messages-API turn array.** An
`assistant` turn's `content` is the A2UI JSONL the agent emitted; a `user` turn's is the framed
input (`agent-transport.ts:28-32`). `ProviderSelection` (`{provider?, model?}`) rides along on
both `TurnInput` arms and is threaded to the proxy by the live overlay only
(`agent-transport.ts:44-47`; see provider-model-seam-and-trust-boundary).

**Claim — the browser is the source of truth for the session; the proxy is stateless** (SPEC-R8,
ADR-0072 clause 4). The running `Session` is held page-side (`a2ui-live.ts:156`,
`let session: Session = { turns: [] }`) and passed IN on every `TurnInput`. A demo-level max-turns
cap guards runaway (SPEC-R8). **Failure mode / caveat:** `Turn.content` is a plain string that the
model consumes as its Messages-API history — anything written into `session.turns` becomes model
context. This is exactly why the PROPOSED decision-trace is held *parallel* to `session.turns`, not
inside it (see conversational-reasoning-and-click-routing-gap).

## Two turn kinds: intent vs client

- **Turn 1 is an `intent`** — raw user free text (`a2ui-live.ts:236`,
  `runTurn({ kind: 'intent', text, session })`). Its user content is just the text
  (`produce.ts:55-57`, `userContent`).
- **Every later turn is a `client` message** — a UI-originated `A2uiClientMessage` the rendered
  surface emitted, reduced into the next turn.

## The pure reducer + distinct framing (SPEC-R8)

`nextTurn(session, message)` is a **pure reducer** returning `{ kind: 'client', message, session }`
(`session.ts:43-45`). The raw message rides along; `produce()` frames it via `frameClientMessage`
when it assembles the model messages, so framing lives in ONE place
(`session.ts:38-45`, `produce.ts:55-57`).

**Claim — `frameClientMessage` frames each client-message arm DISTINCTLY** so the model knows what
happened and how to continue (`session.ts:20-36`, SPEC-R8 AC1):

- **`action`** → `"The user triggered the "<name>" action (from component <id>)."` plus the
  `context` and the surface `dataModel` when present (`session.ts:21-27`).
- **`functionResponse`** → the awaited value for the issued `callFunction`
  (`session.ts:29-31`).
- **`error`** → the rejected surface, fed back for **cross-turn recovery** — distinct from
  `produce()`'s intra-turn generate/validate self-correct loop; this is the agent getting a fresh
  turn to fix a rejected surface (`session.ts:33-35`).

**Caveat — `action` context resolution is a separate concern.** The reducer frames whatever
`context` the renderer collected; list-item relative-path context resolution is separately tracked
in the protocol layer (see [[a2ui-protocol-facts]]), not this pack.

## "The agent continues" — the round-trip is unconditional today

**Claim — any rendered control's action/functionResponse/error already round-trips to a full agent
turn, unconditionally.** `host.onClientMessage(handleClientMessage)` (`a2ui-live.ts:160`) →
`handleClientMessage` calls `runTurn(nextTurn(session, message))` for EVERY client message with no
condition (`a2ui-live.ts:224-229`). This is the whole answer to "how does a UI click become an
agent turn": the plumbing exists today. **Failure mode / caveat:** because it is unconditional,
every click — even a benign slider drag or tab switch — forces a visible LLM round-trip. Making
that selective is the PROPOSED `wantResponse` routing (see
conversational-reasoning-and-click-routing-gap); it is NOT shipped.

## An explain-turn needs no new kind

**Claim — a "why did you pick X over Y" question is a normal `intent` turn**, not a new
`TurnInput` kind. The session already carries full history via `appendUserTurn` /
`appendAssistantTurn` (`session.ts:47-55`, both pure — return a new `Session`), so the model can be
re-prompted over it. The real gap is *grounding* the answer, not routing it — covered in
conversational-reasoning-and-click-routing-gap.

## What this file does NOT cover

The transport the session flows through (agent-transport-seam) · the generate→validate loop that
turns a `TurnInput` into a JSONL stream (produce-loop) · what `ProviderSelection` binds to
(provider-model-seam-and-trust-boundary, switcher-and-live-overlay) · the shape of an
`A2uiClientMessage`'s `action`/`functionResponse`/`error` on the wire ([[a2ui-protocol-facts]]) · the
PROPOSED note channel + decision-trace + `wantResponse` routing
(conversational-reasoning-and-click-routing-gap).
