# The conversational channel & asks — SHIPPED

> Axis: how the live agent talks BESIDE the A2UI stream (the note channel), when it ASKS instead of
> guessing (clarify + catalog-boundary negotiation, feed-embedded asks), how a deployment scales the
> disposition (the mode axis), how idiom knowledge composes without context bloat (the mini-skill
> registry), and how `wantResponse` routes clicks. All SHIPPED and gated. Design records: ADR-0088 ·
> 0089 · 0090 · 0091 · 0097 (`.claude/docs/adr/`). Status cells: 0088/0089/0090/0097 = `accepted`;
> **ADR-0091's cell still reads `proposed`** (`0091:7`) even though its build is shipped and gated —
> cite the code for mini-skill claims. Paths below are relative to `packages/agent-ui/a2ui/` except
> `site/…` (repo root) and the `src/live-agent/*.test.ts` gates.

## 1. The note channel — prose rides BESIDE the A2UI stream, never inside it

**Claim — every turn opens with a reserved, versionless meta-line carrying the model's own prose.**
The GRAMMAR instructs "Note line (ALWAYS first)" — one JSON object
`{"a2uiMeta":{"note":"…"}}` before any A2UI JSONL, on EVERY turn (`tools/agent/system-prompt.ts:62-68`).
`readMetaLine` rejects any line carrying `version` (`tools/agent/meta-line.ts:85`) — the meta-line is
provably NOT an `A2uiServerMessage`, a demo-transport framing convention, not protocol
(`meta-line.ts:1-11`). The envelope is `{ note?, ask?, trace? }` (`meta-line.ts:62-68`).
- `produce()` peels the FIRST non-empty line before heal/validate (`tools/agent/produce.ts:180-187`,
  called at `:297`) — a blank-line-tolerant refinement over ADR-0088's literal "leading line" — and
  yields the re-composed meta-line FIRST, then the validated A2UI lines (`produce.ts:336-340`).
- *(Dated note 2026-08-19: the `{ note?, ask?, trace? }` shape above is the 2026-07-08 snapshot; the
  envelope has since grown to SIX reserved model-authored arms — see the UPDATE section below. The
  toolkit core also moved `tools/agent/` → `src/agent/` (ADR-0137 portable core), so this file's
  older `tools/agent/*` cites read as `packages/agent-ui/a2ui/src/agent/*` today — grep the symbol,
  not the old path.)*
- **A note-only turn is a clean success, not a halt** (empty ≠ invalid): zero remaining A2UI lines
  returns after yielding the meta-line alone (`produce.ts:303-311`; ADR-0088 Consequences).
- The page filters the meta-line before `host.ingest`/`allLines`/the JSON tab
  (`site/pages/a2ui-live.ts:294-304`) and shows the model's prose verbatim —
  `addMessage('agent', note ?? summarize(turnLines))` (`a2ui-live.ts:367`); `summarize()` is only the
  fallback for note-less turns (the recorded backbone).
- **The decision trace grounds "why".** `produce()` assembles a `TurnTrace` (`turnIndex`, retrieval
  query, `exemplarIds`, `rounds`, `healed`, `failureCodes`, `model` — `meta-line.ts:31-43`,
  `produce.ts:270-280`) onto the same meta-line; the browser holds `traces[]` parallel to the session,
  and `traceDigest()` prepends the last 5 (plus retained notes) to the NEXT intent turn's `text`
  (`a2ui-live.ts:387-402`, `:420`) — shipped as a text-prepend on the existing `TurnInput.text`, not a
  new context block; the chat still shows the user's bare text. Caveat: `turnIndex` is a
  Messages-array index advancing by 2, never a dense ordinal (`produce.ts:266-270`).

## 2. The ASK grammar — clarify, negotiate the catalog wall, and feed-embedded asks

**Clarify-before-acting** (ADR-0089 §1): an underdetermined turn ("make it better") gets a note-only
turn asking ONE qualifying question; a request actionable with a sensible default still builds
(`system-prompt.ts:82-88`). **Catalog-boundary negotiation** (ADR-0089 §2): at the wall the agent
names the limit, proposes an approximation from EXISTING catalog types, and waits for yes
(`system-prompt.ts:90-98`) — the SPEC-R9 allowlist is never widened; "improvise" =
approximate-within-catalog + disclose.

**Feed-embedded asks** (ADR-0097): for closed-set/typed answers the ask becomes clickable UI in the
chat feed.
- **The `ask` routing field** rides the same meta-line: `{"a2uiMeta":{"note":"…","ask":{"surfaceId":
  "ask-1"}}}` (`system-prompt.ts:70-80`, `meta-line.ts:50-52`); the ask's UI is ordinary validated
  A2UI on the same stream. A malformed `ask` drops only itself, never the envelope
  (`meta-line.ts:94-101`).
- **The 23-IN/13-OUT TOTAL partition** — `tools/agent/feed-catalog.ts`: `FEED_SURFACE_TYPES` (23,
  `:29-53`) and `FEED_EXCLUDED` with a recorded reason per entry (13, `:71-112`) — including the
  chart-family entries `Sparkline` (`:94-97`) and `BarChart` (`:98-102`), added per ADR-0107 /
  ADR-0097's 2026-07-08 Amendment ("report content, not an ask affordance").
  The gate (`src/live-agent/feed-catalog.test.ts:23,26-35`) asserts IN ∪ OUT = the catalog's
  component set exactly and disjointly — an undispositioned future type turns CI red.
- **Three enforcement points, one source** (`feed-catalog.ts:7-13`): (a) prompt-build — the GRAMMAR's
  feed-allowed list is composed from `FEED_SURFACE_TYPES` (`system-prompt.ts:80`); (b) producer — the
  `FEED_SCOPE` gate runs AFTER the shared validator, feeding a produce-layer-only `'FEED_SCOPE'`
  failure back as a self-correct round, never a stream (`produce.ts:246-256`, `:322-327`); (c) page —
  fail-closed: every type on the buffered ask lines must pass `isFeedSurfaceType` or the WHOLE ask
  drops to the note (`a2ui-live.ts:335-352`, `site/lib/ask-registry.ts:50-67`).
- **Ask integrity is a silent degrade, not a retry**: an `ask` no payload line creates, or colliding
  with a session-known surface, is dropped from the outgoing meta-line — the note stands
  (`produce.ts:231-235`, `:331`). A note-less ask never ships at all — the meta-line is only yielded
  when `note !== undefined` (`produce.ts:336-339`, post-ship review finding 4).
- **Lifecycle**: one fresh renderer host per ask in its own bubble; `pending → frozen(answered |
  bypassed)` via bubble `inert` + `data-state`, never disposed — history stays visible
  (`ask-registry.ts:84-94`, `:124-131`). **Freeze fires on turn COMPLETION, not dispatch** — the
  ADR's "freeze on dispatch" wording was corrected by its own Erratum; a halted turn leaves the ask
  pending (`a2ui-live.ts:326-329`). Line routing uses `has()` — ANY registry-known surface except
  this turn's own fresh ask is dropped (`a2ui-live.ts:305-313`, closing the one-turn `isFrozen` gap).
  Reset disposes all ask hosts (`a2ui-live.ts:445`, `ask-registry.ts:134-137`).

## 3. The mode axis — `specific` ↔ `blue-sky`; what scales and what never does

`GenUiMode = 'default' | 'specific' | 'blue-sky'` (`tools/agent/gen-ui-mode.ts:20-25`); Structural is
deliberately NOT a member — it is the shipped recorded transport, a different layer (Kim's resolved
fork, ADR-0090 §3). `grammarFor` composes the invariant spine + the mode's scaled block; absent or
`'default'` returns the literal `GRAMMAR` constant unchanged — byte-identity by construction
(`system-prompt.ts:258-270`; gated at `src/live-agent/system-prompt-grammar.test.ts:480`).
- **What scales**: clarify threshold and negotiation appetite — dialed DOWN in `specific`
  (decline-and-redirect, `system-prompt.ts:178-188`), dialed UP in `blue-sky` (multi-round clarify,
  narrated reasoning, the top-down/bottom-up/reconcile composition discipline + ★ calibration
  examples, `:190-221`) — plus the feed-ask disposition (`:231-250`).
- **What never scales**: the honesty floor — never invent a type/prop, never silently substitute —
  identical in every mode (`system-prompt.ts:170-173`; ADR-0090 §2); no mode widens SPEC-R9 or the
  feed set. The mode threads `ProduceOptions.mode → buildSystemPrompt` (`produce.ts:73-75`, `:263`) —
  the proven `model` path; nothing else in the loop branches on it.

## 4. The mini-skill registry — SIX modules, TF-IDF selection, cap 3, degrade-to-empty

`tools/agent/mini-skills.ts` hosts SIX `MiniSkill` modules (`{id, triggers, body}` — `:36-43`):
`card-game-sheet` · `settings-screen` · `dashboard-kpi-grid` · `login-form` · `master-detail-split`
(`:59-101`) plus `form-rhythm` (`:104-114`, the ADR-0103 cl.4 Lane-C module — FormProvider declares
zero layout, so `FormProvider › Column gap='md' › Field per control` is taught, not defaulted).
- **Selection**: `selectMiniSkills` ranks `triggers` against the turn's intent by TF-IDF cosine
  (`topKByCosine`, the same math `retrieve()` uses — `mini-skills.ts:127-129`), once per turn beside
  `retrieve()` (`produce.ts:262`); it degrades to `[]` on zero vocabulary overlap and — unlike
  `retrieve()` — never pads with zero-score entries (`floor: 0`, `mini-skills.ts:122-126`).
- **The anti-bloat budget**: `PER_MODULE_TOKEN_BUDGET = 200` (`:48`), `DEFAULT_MINI_SKILL_CAP = 3`
  (`:52`), both gated (`src/live-agent/mini-skills.test.ts:23-27`); `miniSkillsBlock` is a `fewShot`
  twin returning `''` on empty (`system-prompt.ts:303-307`) — the prompt grows by at most cap×budget
  regardless of registry size (ADR-0091 §3).
- **The ★-inline mechanism** (post-ship independent-review fix, not in ADR-0091's design):
  `NEGOTIATE_BLUE_SKY`'s three ★ calibration bullets are COMPOSED from `MINI_SKILLS[id].body` via
  `calibrationExampleBullet` (`system-prompt.ts:200-206`, rendered at `:220-221`) — the registry is
  the single source — and `miniSkillsFor` filters those three ids out of a `'blue-sky'` selection so
  the same paragraph is never injected twice (`system-prompt.ts:317-322`); `specific`/`default` carry
  no inline idioms, so selection injects all six normally there. A module-load marker guard hardens
  the GRAMMAR slicing (`assertMarkersHold`, `system-prompt.ts:149-164`).

## 5. `wantResponse` click routing — AS SHIPPED

**The routing predicate lives in the pure reducer layer, not the page** — a shipped refinement over
ADR-0088 §3's "handleClientMessage routes" sketch: `shouldRunTurn(message)` in
`tools/agent/session.ts:68-71` answers `action.wantResponse !== false` for the `action` arm and
`true` for `rendererFunctionResponse`/`error` (inherently agent-directed). The page calls it FIRST, so a
`TurnInput` can never be constructed for a message that should stay silent (`session.ts:9-13`):
`handleClientMessage` returns before any chat entry or `runTurn` on an explicit `false`
(`site/pages/a2ui-live.ts:404-413`). The default is the back-compat OPT-OUT Kim ratified (ADR-0088
Open fork, resolved 2026-07-07): absent or `true` ⇒ today's full visible turn — the committed seed
(`canvas-button.ts:27`, no `wantResponse`) keeps turning. The renderer's RPC-correlation reading of
the same flag is untouched — two documented, non-colliding layer-local meanings
(`session.ts:59-66`; ADR-0088 Consequences).

## UPDATE 2026-08-19 — the meta-line reserved vocabulary: SIX model-authored arms, four laws, one principle

**[verified]** against the ADR texts fetched from `kimgranlund/agent-ui` 2026-08-19 (ADR-0097 /
0174 / 0178 / 0198 incl. both ratified amendments / 0204 / 0206 — every one `accepted`) and the
shipped `src/agent/meta-line.ts` header comments, which restate each arm's law per-arm. §1's
`{ note?, ask?, trace? }` was the 2026-07-08 snapshot; the reserved MODEL-authored vocabulary is now
**`ask · plan · personaPatch · flowEnd · team · target`** (ADR-0206 Consequences names all six so
"the next envelope audit finds a cited decision"). `trace`/`progress`/`error` are the
RUNTIME-composed siblings — composed by `produce()`/the host, never declared by the model
(ADR-0174 Context draws this line explicitly).

| Arm | Shape | Decision | Consumer |
|---|---|---|---|
| `ask` | `{ surfaceId }` — this turn's A2UI carries a feed-embedded ask | ADR-0097 | the page's ask registry (§2) |
| `plan` | `{ steps: [{id, description}] }` — a declared step list | ADR-0174 | host-side plan runner, projected onto status-stream grouping |
| `personaPatch` | partial persona-store record | ADR-0178 | host-side apply gate (key-enumeration + per-key sanitizer), builder-scoped modality gate |
| `flowEnd` | literal `true` — this turn closes an ask-flow | ADR-0198 | page chrome appends the done/start-over row |
| `team` | `{ label, tagline?, members: [{name, role, routingDescription}] }` | ADR-0204 | `ui-agent-admin`'s `onTeamDeclared` seam ONLY; unregistered ⇒ silently dropped |
| `target` | `{ surfaceId }` — the existing surface this turn is about to mutate | ADR-0206 | `beginAgentTurn` sets `working` on THAT host at turn start |

**The four envelope laws every arm obeys** (each ADR restates them; cite the arm's own ADR when
asked "is this validated?"):

1. **Versionless, additive-only.** The envelope never carries `version`, so it is provably NOT an
   `A2uiServerMessage`; every widening is a new optional field. `AgentTransport.turn` stays a
   byte-identical contract through all six widenings, and no arm ever enters the validator or the
   corpus path (SPEC-N3 wire purity — "restated for the sixth time", ADR-0206 Non-goals).
2. **Whole-arm shallow validation.** Per-field independence: a malformed arm drops ONLY itself,
   never the envelope — every sibling field on the same line still parses. AND the arm validates as
   a WHOLE: `team` with any member missing a string field drops the ENTIRE arm (never a partial
   roster — "the one shape a host mint loop must never be handed", ADR-0204 cl.2); `target` with a
   missing/non-string `surfaceId` drops whole ("a malformed routing fact is worse than no routing
   fact" — a wrong-but-present target would breathe the WRONG card with full apparent authority,
   ADR-0206 cl.2); `flowEnd` accepts literal `true` only (ADR-0198 cl.1).
3. **Gate-blind producer pass-through.** `produce()` peels and re-emits each arm with NO integrity
   check, no re-validation, no verification that a stated target is later mutated or a declared
   team is sensible — structural validation (law 2) is the only guard this layer owns; whether an
   arm is CONSUMED is entirely the host's call (ADR-0204 cl.3, ADR-0206 cl.5).
4. **Degrade floor: absence is a neutral no-signal state.** A model that never emits an arm sees no
   regression (`target` absent ⇒ no early breathe, `working` set at the line burst — "late but
   never wrong", ADR-0206 cl.4); a consumer never infers a missing arm heuristically (ADR-0198
   Non-goals bans completion inference in chrome outright). An unknown/stale `target.surfaceId`
   simply never matches an open registry entry — no halt, no user-visible error (ADR-0206 Non-goals).

**The principle the sixth arm proves: a truthful model-stated early signal beats any host
heuristic.** Under validate-then-stream every content line lands in one late burst; the leading
meta-line is structurally the ONE line that arrives before it. GH #1134/PR #1138 tried the
heuristic route — "exactly one surface open ⇒ it's probably the target" — and GH #1259's live repro
showed the wrong-guess branch firing in the COMMON case (a one-card chat, an unrelated question).
Kim's ruling retired the heuristic for the stated `target` arm: "a heuristic, however narrower, is
still a GUESS about a fact the model already knows and could simply state; only (c) makes the
signal TRUTHFUL rather than merely less-often-wrong" (ADR-0206 Context). Same lesson as ADR-0187's
atFinalize: the missing fact lives only with the party that holds it — for a conversation flow,
the MODEL. Answer conduct: when a consumer needs an early routing fact, the fix is a new meta-line
arm the model states, never a smarter host guess.

## UPDATE 2026-08-19 — flow-completion conduct: the ADR-0198 laws (accepted record + both ratified amendments)

**[verified]** against ADR-0198's full text incl. the 2026-08-17 and 2026-08-18 amendments (both
ratified; fetched 2026-08-19). These are producer-grammar CONDUCT laws taught mode-invariantly in
`grammar.md` (never a mini-skill — completion must be unconditional default behavior, ADR-0198 cl.2):

- **`flowEnd: true` fires on ALL flow-terminal paths** (amendment A1): happy completion, escalation
  /early-stop (the escalation prose turn IS the closing turn — the observed urgent-triage gap), and
  model-visible abandonment ("never mind"). A silently closed tab is not a turn; chrome still never
  infers.
- **The user takes the final action** (A2): before any conclusive action the agent presents a final
  proposed-outcome artifact (the existing summary card — no new component) carrying an ORDINARY
  confirm ask; **ordering law: `flowEnd` comes AFTER the user's commit, never on the
  proposed-outcome turn**.
- **The answered-ask freeze begins at flow-final confirm, not before** (amendment B1): mid-flow
  Next/Back commits are SCENE TRANSITIONS on ONE still-open ask — the producer's `updateComponents`
  swaps the scene container's children on the SAME surface, the ask keeps its one `ask-<n>` id for
  the whole wizard, and draft state lives under a `/draft/*` prefix that survives every swap (Back
  is free because nothing is committed until the flow-final confirm). Only after that confirm does
  the fresh-id freeze law govern.
- **The closing turn emits NO A2UI — except exactly ONE settling `updateComponents`** (A3 + B2):
  the courtesy-close prose `note` + `flowEnd: true`, no new ask, and at most one update against the
  already-confirmed receipt's surface (strip Back/Confirm, add a settled Badge), never a fresh
  surface, never `deleteSurface` on a confirmed receipt. The five-part courtesy close (did / you
  made it happen / sent / thanks / offer) is prose guidance — the SIGNAL, not the prose, is
  load-bearing.

## What this file does NOT cover

The transport the meta-line rides (agent-transport-seam) · the turn/session model (turn-session-and-
input-intent) · the produce() loop mechanics beyond the peel/gates above (produce-loop) · the wire
shape of `wantResponse`/`action` ([[a2ui-protocol-facts]]) · building any of this in SOURCE
(`a2ui-builder`) · composing a payload that sets `wantResponse` (`a2ui-composer`) · authoring or
ratifying the ADRs (`planner` / docs' `make-doc`).

## History

This file was born (2026-07-07) as the OPEN-GAP record for this axis: it documented the two shipped
gaps — no natural-language channel anywhere in the turn model, and clicks routing indiscriminately
while `wantResponse` sat wired-but-unread — plus ADR-0088's then-`proposed` three-part design and its
one open fork (the routing default, Kim's call). The family was ratified and built 2026-07-08
(ADR-0088/0089/0090/0097 accepted; 0091 built with its Status cell still `proposed`), and this
rewrite replaced the pre-ship framing with the shipped-system documentation above.
