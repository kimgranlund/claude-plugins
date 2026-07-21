# The five instruments — as implemented in the arena

Estate root: the `agent-ui` repo; all paths below are under `packages/agent-ui/a2a/` unless noted.
Four of the five are transcript checks inside ONE pure gate, `checkIsolation(t): IsolationFailure[]`
— batch, total, never throws `[estate — src/arena/isolation.ts:192-194]`. The fifth (byte-complete
recording) runs UPSTREAM of the transcript, at the provider-adapter boundary, and is what makes the
other four sound (the transcript must be the whole truth before auditing it proves anything).

## 1. Per-seat canaries (check `'canary'`)

- **Derivation is deterministic, not secret-random:** FNV-1a over `` `${matchId}:${mark}` `` →
  `A2A-ISOLATION-CANARY-${mark}-${hex8}` `[estate — tools/arena/canary.ts:8-20]`. Determinism is
  load-bearing: the scripted CI backbone must re-run byte-identically `[estate — tools/arena/canary.ts:1-5]`.
  `deriveCanaryPair` asserts `X !== O` fail-fast at construction — a collision could only ever
  false-positive the gate, never hide a leak, so throwing beats retrying `[estate — tools/arena/canary.ts:37-44]`.
- **Planting:** one line in each seat's system prompt ("NEVER repeat this token")
  `[estate — tools/arena/seats/model.ts:35-42]`; scripted seats plant it too `[estate — tools/arena/seats/scripted.ts:15]`.
- **Scan:** regex `A2A-ISOLATION-CANARY-[XO]-[0-9a-fA-F]+` over (a) every context entry of the OTHER
  seat and (b) every wire message ADDRESSED to the other seat (JSON-stringified)
  `[estate — src/arena/isolation.ts:27,87-117]`. A fixture with no canaries at all is skipped, not passed vacuously `[estate — src/arena/isolation.ts:98]`.
- **Negative controls:** in-test context-leak and wire-leak transcripts `[estate — src/arena/isolation.test.ts:49-63]`;
  BOTH committed contaminated fixtures fire this check `[estate — src/arena/fixtures.test.ts:71-78 · src/arena-agent/model-seat.test.ts:189-196]`.

## 2. Wire-origin audit (check `'wire-origin'`)

- **What it actually walks:** every wire event; any message addressed to a seat must carry
  `from: 'referee'` — that is the whole check `[estate — src/arena/isolation.ts:121-131]`. It is
  sufficient because of the star topology: the runner owns both endpoints of each seat↔referee
  loopback pair and never forwards content between seats `[estate — tools/arena/match.ts:1-6,183-237]`.
- The "every fact an agent acts on traces to a message it received" arm is NOT here — that is
  check 4 (provenance), which matches context entries against actually-sent wire bodies.
- **Negative control:** an in-test seat→seat wire event
  `[estate — src/arena/isolation.test.ts:65-72]`.

## 3. Closed message schema (check `'closed-schema'`)

- **The closed shape:** `BoardMessage` = exactly `{board, yourMark, lastOpponentMove, legalMoves,
  status, feedback?}` `[estate — src/arena/referee.ts:31-38]`; the check pins that key set and fails
  any extra top-level key on a referee→seat body `[estate — src/arena/isolation.ts:42,136-153]`.
- **Nested hardening** (a top-level filter never looks INSIDE an allowed key): `feedback`'s own
  closed key set `{code, detail, retriesLeft}` `[estate — src/arena/isolation.ts:46,62-77]`, PLUS the
  one referee-authored deterministic string — the ILLEGAL `feedback.detail` template — pinned
  verbatim as a regex, including JS exponential number grammar (`cell 1e+21 is occupied…` must pass
  clean) `[estate — src/arena/isolation.ts:57,73-75 · src/arena/referee.ts:208 · src/arena/isolation.test.ts:108-114]`.
- **Deliberate scope limit:** free text the referee merely RELAYS (a MALFORMED `feedback.detail`
  carrying the seat's own raw reply, `assistant` context entries) is not content-validated — that
  surface rides on check 1 `[estate — src/arena/isolation.ts:6-14]`.
- **Negative controls:** the committed `contaminated-control` (seat X's `note` + canary injected into
  a referee→O body — one mutation, two firing checks) `[estate — tools/arena/generate-fixtures.ts:58-67 · src/arena/fixtures.test.ts:71-78]`;
  in-test nested-extra-key and non-pinned-detail leaks `[estate — src/arena/isolation.test.ts:85-102]`.

## 4. Context provenance (check `'provenance'`)

- **A transcript audit, not a per-message referee whitelist:** every `system` entry must sit at
  position 0 of its seat's context; every `user` entry must BYTE-IDENTICALLY equal
  `JSON.stringify` of a `BoardMessage` the transcript shows the referee actually sent to that seat
  `[estate — src/arena/isolation.ts:165-187]`. `assistant` entries have no referee-authored form to
  check against — deliberately unvalidated here; checks 1+3 own that surface
  `[estate — src/arena/isolation.ts:155-164]`.
- **Negative controls:** in-test fabricated `user` framing + a mid-history `system` preamble
  `[estate — src/arena/isolation.test.ts:117-131]`; the committed provider control fires
  provenance + canary `[estate — src/arena-agent/model-seat.test.ts:189-196]`.

## 5. Byte-complete boundary recording (the tap — upstream of the gate)

- **The tap:** `withRecordingTap` wraps `AgentProvider.stream` and captures the EXACT request
  (model, system, the FULL messages array — shallow-copied at capture time) plus the accumulated
  response the moment the stream completes `[estate — tools/arena/recording-tap.ts:23-38]`.
- **The seat records only what the tap saw** — never its own local `turns`/`raw` copies
  `[estate — tools/arena/seats/model.ts:88-110]` — and diffs `system` plus EVERY historical message
  against its own turn history (handed to the provider as a fresh per-message clone), recording any
  diverged value as an extra context entry, which checks 4/1 then fail
  `[estate — tools/arena/seats/model.ts:96,116-133]`.
- **Named precondition, not assumed:** the reused provider adapter's statelessness is discharged by
  this assertion + the control below, never by inspection `[estate — tools/arena/seats/model.ts:16-22]`.
- **Negative controls:** the committed `contaminated-provider-control` — a deliberately leaky SHARED
  provider mutating `req.system` below the seat seam, regenerated byte-identically in-process on
  every test run `[estate — src/arena-agent/model-seat.test.ts:151-168,204-226]`; the
  historical-message (non-last) mutation variant `[estate — src/arena-agent/model-seat.test.ts:118-142]`;
  positive control: recorded context ≡ the actual request bytes `[estate — src/arena-agent/model-seat.test.ts:86-116]`.

## Committed fixture ↔ instrument map

| Fixture (`matches/`) | Leak class | Proven to fire | Standing assertion |
|---|---|---|---|
| `contaminated-control.match.jsonl` | in-transcript | closed-schema + canary | `[estate — src/arena/fixtures.test.ts:71-78]` |
| `contaminated-provider-control.match.jsonl` | out-of-transcript | canary + provenance | `[estate — src/arena-agent/model-seat.test.ts:204-226]` |
| `scripted.match.jsonl` / `flagship.match.jsonl` | positive controls (must pass clean) | — | `[estate — src/arena/fixtures.test.ts:26-30,46-50]` |

Both contaminated fixtures are SCHEMA-valid — the leak is semantic; `validateTranscript` stays green
and only `checkIsolation` fires `[estate — src/arena/fixtures.test.ts:65-69]`. Per-check in-test
controls cover each of the four checks individually `[estate — src/arena/isolation.test.ts]`.
