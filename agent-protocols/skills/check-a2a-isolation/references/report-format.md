# The isolation proof artifact — report format

Derived from what the arena's checks actually assert (`agent-ui` repo, paths under
`packages/agent-ui/a2a/`). The proof is a PAIR of runs per instrument class — a clean run that
passes AND a poisoned run that fails — never the clean run alone. Six sections:

## 1. System identification (the header analog)

Declare WHO interacted and under what provenance — the arena's `TranscriptHeader` is the template:
`{matchId, protocolVersion, seats: {X: {provider, model}, O: {…}}, date, scripted}`
`[estate — src/arena/transcript.ts:14-20]`. A real (non-scripted) proof asserts real provenance
explicitly — the flagship gate checks `scripted === false` and the actual provider names
`[estate — src/arena/fixtures.test.ts:52-59]`. Pin the `date` when byte-identical regeneration is
part of the claim `[estate — tools/arena/match.ts:27-28,62-73]`.

## 2. The failure unit

One finding = `{check, detail}` with `check` naming the instrument
(`canary | wire-origin | closed-schema | provenance`) and `detail` naming the concrete leaked
value/key/origin — e.g. `X's canary "…" found in O's recorded context`
`[estate — src/arena/isolation.ts:20-25,103]`. The gate is batch + total: report EVERY failure
found, never the first, and never throw on malformed input `[estate — src/arena/isolation.ts:189-194]`.

## 3. Clean-run evidence

Per recorded exchange under test:
- **Schema-valid:** the recording validates against its own transcript schema (shape + version pin +
  event ordering — a move-apply must follow the wire move it names)
  `[estate — src/arena/transcript.ts:146-197 · src/arena/fixtures.test.ts:22-24]`.
- **Gate-silent:** `checkIsolation → []`, with the non-vacuity caveat stated: silence only counts
  because §4's controls prove the gate bites `[estate — src/arena/fixtures.test.ts:26-30]`.
- **Deterministic where claimed:** two-run byte-identity of the serialized recording
  `[estate — src/arena-agent/model-seat.test.ts:198-202]`.

## 4. Negative-control evidence (the half that makes it a proof)

- One COMMITTED poisoned fixture per leak class — in-transcript and out-of-transcript — each backed
  by a STANDING test asserting a non-zero gate result; a green run over a control is itself a suite
  failure `[estate — src/arena/fixtures.test.ts:62-79 · src/arena-agent/model-seat.test.ts:204-226]`.
- Per-instrument in-test controls covering each check individually
  `[estate — src/arena/isolation.test.ts:49-131]`.
- For each control, state: which checks fired, and that the fixture is schema-VALID (the leak is
  semantic, not a shape defect — a schema validator has nothing to say about it)
  `[estate — src/arena/fixtures.test.ts:65-69]`.
- Controls should be regenerable, not hand-authored: the in-transcript control is one scripted
  mutation over the clean fixture `[estate — tools/arena/generate-fixtures.ts:58-67]`; the
  out-of-transcript control regenerates byte-identically in-process
  `[estate — src/arena-agent/model-seat.test.ts:198-226]`.

## 5. Residual channels — named honestly

The arena's own completeness-scope statement is the template `[estate — src/arena/isolation.ts:6-14]`
(+ the arena LLD §2, `.claude/docs/lld/a2a-tic-tac-toe.lld.md:65-70`):

- Free-text fields the mediator merely relays are NOT content-validated — they ride on the canary
  check only.
- The agents' own free-form output (`assistant` entries) has no authored form to pin — same fallback.
- Reused adapter statelessness is a NAMED PRECONDITION discharged by the byte-complete recording
  assertion + its negative control, not proven of the imported module itself
  `[estate — tools/arena/seats/model.ts:16-22]`.
- Canaries catch ACCIDENTAL bleed (a shared session object, a copy-paste), not adversarial evasion —
  an agent that deliberately omits foreign-looking tokens defeats them; say so
  (the corpus's own `canary-mechanism` record states this `[estate — tools/corpus/seeds.ts:342-369]`).
- Timing side-channels: typically out of scope — state it rather than imply coverage.

## 6. Structural-isolation statement (input, not substitute)

State the structural separation as CONTEXT for the instrumented proof, never in its place: per-seat
channels with the runner owning and tearing down both endpoints of each pair, no seat→seat channel
existing, delivery proven by genuine transit through the boundary (send → drain → record the
delivered message) `[estate — tools/arena/match.ts:118-129,183-237]`; the closed reply surface
(`note` is spectator-only, never relayed to the opponent) `[estate — src/arena/referee.ts:40-44]`.

## UPDATE 2026-08-17 — verdicts are computed live, never precomputed (issue #511)

**[inferred]** from the arena's own standing practice, cited here from that report (source: `agent-ui`
`packages/agent-ui/a2a` arena + `matches/flagship.match.jsonl`; memory `a2a-section-state` —
re-Grep the cited files at the next refresh wave rather than trusting these line numbers cold).
**The proof's verdicts are computed LIVE at report/view time over the recording, never
precomputed or committed alongside it.** This is the same principle §4's clean-run evidence already
leans on ("gate-silent: `checkIsolation → []`") stated explicitly as its own rule: a report that
shows a STORED "passed" badge next to a transcript is trust theater — the only thing worth showing
is the gate's OWN output from re-running `checkIsolation`/`validateTranscript` against the actual
recorded bytes, right now. (The a2a-training-facts sibling pack documents the identical discipline
for its concepts-page artifact verdicts — `data-validated` is "computed, never a
precomputed/hardcoded badge" — the same rule, a different surface; see that pack's
`derivation.md`.) **Failure mode a report format must avoid:** caching or hand-transcribing a past
run's verdict into the report text — the moment the code changes, a cached verdict silently goes
stale while still reading as current.

**The standing evidence artifact is a REAL match between two DIFFERENT models**, not a scripted or
same-model fixture: `flagship.match.jsonl` is the positive control that must pass clean (§3 above;
`scripted === false` + real provider names, per the header check in §1) — its evidentiary weight as
a flagship specifically rests on it being a genuine cross-model interaction, not a same-model replay
that would leave a same-provider leak channel unexercised.
