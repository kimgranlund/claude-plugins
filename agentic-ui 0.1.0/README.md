# agent-protocols — A2UI + A2A protocol, catalog, agent, and corpus knowledge

Two skill families over the agentic-UI estate, cited from the repo corpus. The **A2UI four** answer
how `@agent-ui/a2ui` (agent-to-UI) works; the **A2A four** cover the Agent2Agent layer
(`@agent-ui/a2a`, spec pin v0.3.0) — one knowledge pack, two verb-named procedures, one corpus
pack. The plugin was named `agent-protocols` rather than `a2ui` precisely to host both.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/a2ui-protocol-facts` | Knowledge pack | model-only | The wire protocol + zero-dependency renderer: message lifecycle, the Binding union, dynamic lists, two-way input, checks, the function-call vs `callFunction` RPC split, the two-code error taxonomy, version pinning |
| `skills/a2ui-catalog-facts` | Knowledge pack | model-only | How a catalog is designed and extended: the definition contract, the factory/resolution pattern, the naming law, two-tier extensibility, the security allowlist + conformance, and coverage policy |
| `skills/a2ui-chat-agent-facts` | Knowledge pack | model-only | The live-agent system: the AgentTransport isolation seam, the Turn/Session/TurnInput model, the produce() generate-heal-validate-self-correct loop, the multi-provider seam and trust boundary, the in-chat switcher, and the conversational channel + asks (the ADR-0088 family, shipped 2026-07-08) |
| `skills/a2ui-training-facts` | Knowledge pack | model-only | The curated training-corpus subsystem: record schema, the two-tier admission gate + healer, the judge/verdict adapter, canonicalization + dedup, retrieval, and the version-change repair loop |
| `skills/a2a-protocol-facts` | Knowledge pack | model-only | The A2A wire model (spec pin v0.3.0): AgentCard discovery, Message/Task/Artifact lifecycle + TaskState machine, Parts + media types, JSON-RPC/SSE transport, the extension mechanism (the A2UI-over-A2A bridge as the worked exemplar), and why version drift is wire-breaking (the full v0.3.0→v1.0.1 method rename table, fetched + carried in-file 2026-07-09) |
| `skills/make-a2a-agent` | Procedure | user + model | Design/build an A2A-conformant agent, both directions: card-first outside-in × state-machine inside-out, reconciled; pure RPC core behind a thin socket shell; conformance as a gate; the estate reference-implementation tour |
| `skills/check-a2a-isolation` | Procedure | user + model | The arena-minted no-cross-contamination proof kit: deterministic per-seat canaries, the wire-origin + context-provenance audits, closed schemas, byte-complete recording — each instrument proven to BITE via committed negative controls |
| `skills/a2a-training-facts` | Knowledge pack | model-only | The A2A concept/demo teaching corpus: record anatomy, HV-row citations, admission + quarantine, the derived concepts page + drift gates, line-order-as-teaching-order |

The knowledge packs are `user-invocable: false` — model-only, routed by description; the two A2A
procedures are user-invocable. The A2UI four each carry a `scripts/routing-corpus.json` (the
original routing corpus, kept as-is) alongside an `evals/evals.json` (this workspace's
`eval_check.py` schema, converted 1:1 from the same positives/negatives) so both the legacy and the
forge-native tooling can regress the same cases. **The A2A four were distilled 2026-07-08** from
the HV ledger (character-verified A2A v0.3.0 quotes) + the shipped `@agent-ui/a2a` sources, then
citation-verified by an independent pass (~70 citations opened, zero fabrications). Honest
residue: the four spec-fetch gap banners were RESOLVED 2026-07-09 by a direct fetch of the
pinned spec (verbatim quotes + VERIFIED SILENT verdicts carried in the resolved banners; one
narrow residual: v1.0.1's extension-activation mechanism). The A2A four
gained their `evals/evals.json` suites 2026-07-09 and the whole plugin passed a blind /eval-run
the same day (191/195; the four failures fence-tuned in the same change).

## Cross-plugin seam

`a2ui-protocol-facts`'s re-sync gate is soft, by design: where forge is installed, run its `skill_lint.py`
to a clean pass before the independent `skill-reviewer` + `linguistics-reviewer` critics; otherwise
apply forge's skill-authoring standard by hand. No hard edge crosses the plugin boundary.

## ADR-0006 transition table (renamed 2026-07-21)

The PLUGIN renamed: `agentic-ui` → `agent-protocols` (new install identity; the directory
`agentic-ui 0.1.0/` keeps its frozen path — see the workspace CLAUDE.md alias table). Old
handles remain greppable only in ledgers, CHANGELOGs, ADRs, and attics.

| Old name | New name |
|---|---|
| `a2a-agent-design` | `make-a2a-agent` |
| `a2a-isolation-verify` | `check-a2a-isolation` |
| `a2a-protocol` | `a2a-protocol-facts` |
| `a2a-training-corpus` | `a2a-training-facts` |
| `a2ui-protocol` | `a2ui-protocol-facts` |
| `a2ui-training-corpus` | `a2ui-training-facts` |
| `a2ui-catalog-design` | `a2ui-catalog-facts` |
| `a2ui-conversational-agent` | `a2ui-chat-agent-facts` |

v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0006 rename PR 4/9 — the PLUGIN renames agentic-ui → agent-protocols (first plugin-name rename of the campaign: new install identity, frozen dir path, workspace CLAUDE.md alias recorded per Decision 5) and all eight members take the simple paradigm (transition table above: make-a2a-agent, check-a2a-isolation, six -facts names). MAJOR bump — breaking. Workspace sweep (57 files, ledger history + forging evidence excluded); 197-case pre-rename baseline captured, post-rename re-measure in the campaign PR · v0.2.6 · assembled 2026-07-19 · 0.2.6: knowledge-pack factory-route convention repointed from scribe's retired `knowledge-forge` to forge's `pack-forge` (workspace-wide rename campaign) — every a2ui-* skill's reference to its authoring factory updated; no functional/behavior change, a naming correction only · v0.2.5 · assembled 2026-07-16 · 0.2.5: a2ui-conversational-agent description re-budgeted under the 1024 portability cap (was 1104) — and the suite's FIRST blind run exposed three pre-existing dead triggers on the conversational-channel axis (t07/t15/t19); the replying/explaining-in-prose phrasing added, re-judge 38/38 · v0.2.4 · assembled 2026-07-14 · 0.2.4: displayName 'Agentic UI' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.2.3 · assembled 2026-07-10 · 0.2.3: author attribution corrected to Kim G / NONOUN (was the Agentic Harness placeholder) · assembled 2026-07-09 · 0.2.2: a2a-protocol's four spec-fetch gap banners resolved — direct fetch of a2aproject/A2A at tags v0.3.0 + v1.0.1: the full 11-pair method rename table (tasks/resubscribe→SubscribeToTask is a rename, not casing), the push webhook contract (headers, StreamResponse payload, at-least-once + idempotency), resubscribe semantics (v0.3.0 VERIFIED SILENT on replay; v1.0.1 opens with current Task), the v0.3.0 AgentExtension truth (NO required field at the pin), card caching (one SHOULD; otherwise VERIFIED SILENT) + §5.6.3 transport selection; new [fetch — S §n] trust rung in sources.md, one rung below HV · assembled 2026-07-09 · 0.2.1: estate-wide blind run: a2ui-conversational-agent 33/36 — t03/t04 judge-noise cleared and validate-then-stream proven; n12-n14 (composer/builder AGENT-owned making asks) leaked structurally — agents are absent from any skill menu and the pack's Boundaries perform that handoff by design; annotated, no description change · assembled 2026-07-09 · 0.2.0: description-hygiene pass (the A2UI four trimmed from 1218-1536 chars to under the 1024 portability bar, triggers kept verbatim; a2a-protocol gains the Use-when formula; a2a-agent-design under the bar); the A2A four gain their eval suites (the pending pre-ship gate closed) and the plugin's first blind /eval-run lands 191/195 over 8 suites — a2ui-training-corpus's running-curation fence strengthened (n12 leak), validate-then-stream added to a2ui-conversational-agent (t14 stolen by a2ui-protocol), t03/t04 judge-noise first-strikes recorded · assembled 2026-07-07 · 0.1.0: initial: ported from ~/.claude/skills (a2ui-*) as part of a
plugin-decompose partition; scoped for future A2A content
