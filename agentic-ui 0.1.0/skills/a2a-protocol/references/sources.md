# Sources & provenance

Every claim in this pack is tagged `[spec — HV-n]` (upstream A2A v0.3.0 fact, host-verified) or
`[estate — file:line]` (a choice `@agent-ui/a2a` made). This file maps the tags to their ground
truth. Estate citations are relative to `agent-ui/packages/agent-ui/` unless a full path is given.
Distilled 2026-07-08 from the local corpus; residual gaps are bannered/noted in
`transport-and-streaming.md` · `versioning-and-conformance.md` · `extensions-and-bridging.md` ·
`discovery-and-agent-card.md` (each names exactly what needs a spec fetch).

| Source | What it grounds | Trust |
|---|---|---|
| **The HV ledger, HV-1..HV-12 — SPEC §2 of `agent-ui/.claude/docs/spec/a2a-foundations.spec.md`** | every `[spec]` claim: character-verified quotes from A2A `docs/specification.md@v0.3.0` [S] + `types/src/types.ts@v0.3.0` [T], version-cross-checked against `v1.0.1` [S1]; resolved 2026-07-07 | the estate's verification record — ALWAYS prefer over memory |
| `agent-ui/.claude/docs/lld/a2a-protocol-core.lld.md` | the transcription of the HV rows into the shipped design (transition-table policy §4, method tables §5, error/edge table §8) | accepted LLD — the owning record for the estate's POLICY (e.g. the TaskState edge set) |
| `a2a/src/protocol/{types,codec,task-state,validate}.ts` · `a2a/src/rpc/{frame,errors}.ts` · `a2a/src/channel/loopback.ts` | `[estate]` claims about the wire model, validator, lifecycle guard, framing, channels | the shipped code IS the fact |
| `a2a/tools/wellknown.ts` (card serving + discovery) · `a2a/tools/http/{core,server,channel}.ts` (dev HTTP transport) | `[estate]` claims about serving/discovery and the HTTP shell | shipped dev tools (Node-scoped, never in a consumer bundle) |
| `a2a/src/protocol/fixtures/*.json` | worked wire examples (cards, messages, tasks, rpc pairs) | committed in encode-canonical form; re-validated by a standing gate |
| `agent-ui/.claude/docs/{prd,spec,lld}/a2a-*.md` | design intent, forks, deferred scope (streaming/push deferrals, JSON-RPC-only posture) | ratified records |
| `a2ui/tools/pipeline/transports/a2a.ts` + `agent-ui/.claude/docs/lld/a2a-a2ui-bridge.lld.md` | the extension exemplar (HV-8): carriage, capabilities, unwrap tolerance | shipped + reviewed |
| `a2a/corpus/{concept,demo}/v0_3_0/a2a.jsonl` | the teaching corpus this pack's examples may quote | admission-gated records |

**Verification discipline (inherited from the build):** when this pack and the spec text disagree,
the spec wins and the pack gets repaired — but fetch and QUOTE the spec (the repo-absence ≠
spec-absence rule); never resolve a conflict from memory. New spec facts enter via a new/updated
HV row first, then the pack cites the row.
