# The stateless proxy + client-held session + pure turn reducer

> Axis: how a server-side LLM gateway avoids becoming a stateful service, while still supporting
> a genuine multi-turn conversation. Grounded in a worked instance:
> `packages/agent-ui/a2ui/tools/agent/{agent-transport.ts,session.ts}` in `@agent-ui/a2ui`.

## The split — who holds what

**Pattern — the CLIENT holds the conversation history; the SERVER computes one turn and forgets:**

```ts
type Role = 'user' | 'assistant'
interface Turn { role: Role; content: string }
interface Session { turns: Turn[] }
```

Every request to the gateway carries the FULL running session; the server never persists it
between requests. **Why this is the right split, not just a simpler one:** a stateful proxy that
tracks sessions server-side needs a session ID, a store, an eviction/expiry policy, and a
consistency story between the client's UI state and the server's copy — all to hold data the
client already has (it rendered the conversation; it knows what was said). Making the server
stateless deletes an entire class of drift bugs (client and server disagreeing about what
happened) at the cost of a slightly larger request body. **Worked instance:**
`agent-transport.ts:24-32` (`Role`/`Turn`) and `:35-37` (`Session`), the latter commented
explicitly: "the ordered turn history the BROWSER holds (the proxy is stateless)."

## Framing a CONTINUATION turn — one function, not scattered inline logic

**Claim — turning "the app is reacting to something the LLM's own prior output caused" into the
next turn's input is a SINGLE pure function**, not logic scattered across call sites. This is
specifically the CONTINUATION half of the turn model (see "First-turn vs continuation framing"
below for why the opening turn is a genuinely separate concern this function does not, and should
not, also handle):

```ts
function nextTurn(session: Session, event: SomeAppEvent): TurnInput {
  return { kind: 'continuation', event, session }
}
```

**Why centralizing this (continuation) half matters:** the alternative — each call site building
its own ad-hoc "next turn" shape — means the framing logic (how an event becomes readable model
input) drifts between call sites and is untestable in isolation. A single reducer function is a
pure, unit-testable seam: given a session and an event, it deterministically produces the next
turn's input, with zero I/O and zero side effects. **Worked instance:** `session.ts:49-51`
(`nextTurn`) — note this constructs ONLY the `kind: 'client'` (continuation) variant; the worked
example currently builds the OPENING `kind: 'intent'` variant as an inline object literal at each
call site rather than through a matching centralizing function (e.g.
`produce-loop.test.ts:55,81,319,339,402` in the same repo) — a real, named asymmetry, not a
misreading: the pattern below argues this opening path would benefit from the same centralizing
treatment, not that the worked example already does it. Note also the adjacent
`frameClientMessage` (`session.ts:26-42`), which is the SEPARATE concern of turning a
raw event into natural-language content the model reads; keeping "build the TurnInput shape" and
"frame this specific event as text" as two distinct pure functions (rather than one function doing
both) means either can change without touching the other.

## An explicit "should this even become a turn" gate — not everything needs the model's attention

**Pattern (a REAL, worth-generalizing refinement beyond the bare reducer above):** not every
client-side event should round-trip to the LLM as a conversational turn — some events are
already fully handled by the app's own reactive state and would only add noise (and cost) if
also sent to the model. **Recommendation:** make this an EXPLICIT, separately-named decision
function the caller runs BEFORE constructing a `TurnInput` — never folded silently into the
turn-builder itself, so a caller can never accidentally construct a turn for an event that should
have stayed silent. **Worked instance:** `session.ts:9-13` (the file-header rationale), `:68-71`
(`shouldRunTurn` itself) — deliberately
NOT folded into `nextTurn`; the caller checks `shouldRunTurn` first and only calls `nextTurn` when
it answers `true`.

## First-turn vs continuation framing — an intent isn't a reaction

**Recommendation:** distinguish the conversation's OPENING input (a raw user intent/prompt) from
every SUBSEQUENT turn (the app reacting to something that happened as a result of a prior model
turn) as two distinct variants of your turn-input type, rather than forcing both through one
generic "message" shape — the model-facing framing genuinely differs (an opening prompt needs no
framing; a reaction typically does, per the `frameClientMessage` pattern above), and a type-level
distinction catches a caller that tries to open a fresh conversation through the "continuation"
path (or vice versa) at compile time rather than at a confusing runtime message.

## What this file does NOT cover

The adapter interface `messages`/`Turn[]` are ultimately passed to
(provider-adapter-seam) · how the resolved provider/model selection threads alongside the
session on each request (registry-and-trust-boundary) · how the model's OWN streamed output
is parsed and validated before it becomes the next assistant turn's content
([[llm-streaming-facts]]).
