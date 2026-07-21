# The reference implementation — a guided tour of `@agent-ui/a2a`

Estate root: the `agent-ui` repo; paths under `packages/agent-ui/a2a/` unless noted. Read in this
order — it is the build order a new agent follows. The layering law: `src/` is zero-dep and
downward-only (`protocol/` ← `rpc/` ← `channel/` ← `arena/`); everything that touches Node, a
socket, or a model key lives under `tools/`, never reachable from the exports map
`[estate — .claude/docs/lld/a2a-protocol-core.lld.md:28,185-201]`.

## 1. Card-first construction

- **The shape:** `A2aAgentCard` `[estate — src/protocol/types.ts:105]` — note `protocolVersion`
  (the protocol pin) and `version` (the agent's own) are two DISTINCT required fields; never
  conflate them.
- **A committed example to copy:** the referee's card
  `[estate — src/protocol/fixtures/card.referee.json:1]` — identity, endpoint, `capabilities`
  (`streaming: false`, `pushNotifications: false` — claim only what you serve), JSON in/out modes,
  one `skills[]` entry. Seat cards `card.seat-{x,o}.json` sit beside it.
- **The fail-fast card gate:** `serveAgentCard(card)` validates through the shared `validateA2a` and
  THROWS rather than serve an invalid card — the one deliberate exception to the family's
  never-throw posture, startup-time only ("a lying card is worse than no card")
  `[estate — tools/wellknown.ts:16-25]`. The HTTP shell calls it at construction, so the server
  refuses to start on a bad card `[estate — tools/http/server.ts:15-17]`.
- **Discovery (the client side):** `wellKnownAgentCardPath = '/.well-known/agent-card.json'` — the
  v0.3.0-renamed path, NOT `agent.json` `[estate — tools/wellknown.ts:10]`; `discoverAgent`
  fetches + validates and never returns a failing card as usable; its injectable `get` seam keeps
  tests socket-free `[estate — tools/wellknown.ts:39-55]`.

## 2. The pure RPC seam

Framing knowledge is pure `src/` code; the request→response engine is a socket-free tools module.

- **Two method tables, one honesty rule:** `SUPPORTED_METHODS` (`message/send · tasks/get ·
  tasks/cancel`) vs `KNOWN_METHODS` (the full v0.3.0 surface), so `classifyMethod` distinguishes
  known-but-unsupported (`-32004`) from unknown (`-32601`)
  `[estate — src/rpc/frame.ts:10-43]`. `parseFrame` is total — parse failure and malformed envelope
  both become coded failures, never throws `[estate — src/rpc/frame.ts:119-130]`.
- **Correlation is deterministic:** monotonic integer ids from 1 + a pending map; an orphan response
  id is a coded failure, dropped-with-record `[estate — src/rpc/frame.ts:139-172]`.
- **One error table, both directions:** 5 standard JSON-RPC codes + the 7 A2A codes
  (`-32001..-32007`), `as const` `[estate — src/rpc/errors.ts:12-25]`; `toRpcError` is the 3-tier
  outbound mapping (parse→`-32700`, malformed envelope→`-32600`, schema-shaped→`-32602`)
  `[estate — src/rpc/errors.ts:40-44]`; inbound unknown codes fall back to `'unknown'` preserving
  the number `[estate — src/rpc/errors.ts:48-51]`.
- **The `handleRpc` seam:** `createRpcCore(handlers).handleRpc(body: string): Promise<string>` owns
  the whole path — parse → envelope validation → method dispatch → handler → framed response;
  handler throws are caught at this boundary → `-32603`. TOTAL and socket-free — this is what the
  standing tests exercise `[estate — tools/http/core.ts:31-73]`. Handlers are three typed methods
  `[estate — tools/http/core.ts:20-24]`.

## 3. The thin shell

- `serveA2a(core, card)` is ~40 lines of `node:http`: GET well-known → the pre-validated card body;
  POST `/a2a` → `handleRpc`; anything else 404. The ONLY file in the package touching a real socket
  `[estate — tools/http/server.ts:16-53,1-3]`.
- The client arm, `httpChannel`, implements the same `A2aChannel` contract as the in-proc loopback;
  sequential awaited POSTs preserve ordering, and its injectable `post` seam is the test hook
  `[estate — tools/http/channel.ts:24-31,44-71]`.

## 4. Task state machine + typed parts

- Upstream fact vs family policy, separated: the 9 states + 4 sealed terminals are upstream (HV-5);
  the full transition table is FAMILY POLICY owned by `TASK_TRANSITIONS`
  `[estate — src/protocol/task-state.ts:1-36]`. `guardTransition` judges — returns `A2A_STATE`
  failures, never throws `[estate — src/protocol/task-state.ts:44-53]`.
- Consumption pattern: the referee wraps the guard in `advance()` and THROWS on an illegal edge — a
  defect trip-wire, since every call site names a table-legal edge
  `[estate — src/arena/referee.ts:79-89]`.
- Content rides typed parts (`text | data | file`) `[estate — src/protocol/types.ts:41]`; the arena
  carries every game payload in ONE data part via `wireMessage`/`readWireData` — the single
  wrap/unwrap point `[estate — src/arena/transcript.ts:55-70]`.

## 5. The referee/seat construction (the two agent exemplars)

- **Server-side agent = a pure reducer:** `createRefereeState → beginMatch → reduce(state, input)`
  returning outbound messages as data — no I/O, no timers, no model
  `[estate — src/arena/referee.ts:91-121,199-211]`; bounded retry and forfeit arcs
  `[estate — src/arena/referee.ts:144-157]`. Timeouts are the RUNNER's concern, mapped to a
  malformed reply so the reducer stays pure `[estate — tools/arena/match.ts:131-139]`.
- **Client-side agent = the seat seam:** `respond(input) → SeatReply` + `pullContext()`
  `[estate — tools/arena/seat.ts:19-22]`. The model seat builds its prompt ONCE per match, makes ONE
  provider call per turn, parses strictly — deliberately NO nested self-correct loop; the referee
  owns the single retry bound `[estate — tools/arena/seats/model.ts:1-5,74-145]`. The scripted seat
  is the deterministic CI variant `[estate — tools/arena/seats/scripted.ts:13-41]`.
- The runner composes both over per-seat loopback pairs and owns teardown of every endpoint
  `[estate — tools/arena/match.ts:183-237]`.

## 6. Where the standing tests sit vs the manual smoke

- Standing tests never touch a socket: the transport-invariance test wires `httpChannel`'s `post`
  seam DIRECTLY to `core.handleRpc` — the full frame→dispatch→respond path with zero network
  `[estate — src/channel/transport-invariance.test.ts:53]`.
- The real socket is exercised ONLY by the manual dev smoke, run by hand
  (`node --experimental-strip-types packages/agent-ui/a2a/tools/http/smoke.ts`); it stays
  import-reachable (types-only) from the invariance test's module graph so `npm run check` covers it
  and it cannot rot silently `[estate — tools/http/smoke.ts:1-10]`.
- Conformance is fixture-backed: a committed canonical-form fixture per wire shape (messages, tasks,
  cards, per-method rpc pairs, an error envelope), re-validated by standing tests
  `[estate — src/protocol/fixtures.test.ts:1-22]`.

## 7. The build order a new agent follows

1. Write the AgentCard; wire the fail-fast validation at construction (§1). 2. Type (or import) the
wire model. 3. Implement handlers behind the pure `handleRpc` seam (§2). 4. Guard the task state
machine with a transition table (§4). 5. Add the thin socket shell LAST (§3). 6. Standing tests ride
the injectable seams; ONE manual smoke owns the real socket (§6).
