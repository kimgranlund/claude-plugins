# llm — portable LLM-integration and chat-agent-harness knowledge

Ten knowledge packs teaching general, project-agnostic technique — never one repo's
implementation. Two families plus one cross-cutting taxonomy: **the LLM-integration two** answer
HOW to call a model safely and stream its output correctly, distilled FROM `@agent-ui/a2ui`'s
live-agent system (a real, shipped, tested instance); **the chat-harness seven** answer how to
construct a mini/portable chat-agent harness AROUND that call — instructions/guardrails,
skills/routing, orchestration/workflows, knowledge/memory, tools/resources/services,
observability, and a deployed runtime's own producer-loop resilience — distilled from Claude
Code's own live, current harness plus this very workspace's own conventions
(`chat-harness-guardrail-facts` and most of the family) or from `@agent-ui/a2ui`'s live-agent
producer loop (`chat-harness-runtime-resilience-facts`, split out of `chat-harness-guardrail-facts`
2026-08-17 once its axis count drifted past the `pack-writing-rules` budget — issue #552);
**`agent-residency-facts`** sits above both families, classifying which of the two the finding at
hand actually belongs to (a CLI-harness Resident Agent vs. a hosted-chatbot Ephemeral Agent)
before a claim from one gets written into the other's corpus. Every claim in all three groups is
grounded either in a platform/vendor/harness fact (verify against current docs if stale-sensitive)
or cited to a real worked instance as proof-of-concept, never as the only valid implementation.

| Artifact | Type | Invocation | What it carries |
|---|---|---|---|
| `skills/llm-gateway-facts` | Knowledge pack | model-only | The swappable multi-provider gateway pattern: one adapter interface per vendor (secrets injected via factory, never module-scope), a registry as the single source of truth for both a picker UI and a server-side allowlist, the `resolvePair` trust-boundary check, the dev-only proxy pattern (server-side key custody), the bundler env-inlining footgun (Vite's `VITE_*` and its analogues), the stateless-proxy + client-held-session + pure-turn-reducer conversation model, and live-gateway ops (the per-model curl matrix as first diagnostic, the upstream-503-storm posture, planning-vs-execution model tiering) |
| `skills/llm-streaming-facts` | Knowledge pack | model-only | Streaming structured output safely: the general SSE chunk-buffering technique (partial-frame handling across `fetch` reads, blank-line event framing per spec), Anthropic's Messages API SSE contract as a fully worked instance, an error-sentinel technique for async generators, validate-then-stream (never emit invalid output, bounded self-correct rounds feeding structured failures back to the model, halt-and-report on exhaustion, the leading meta-line paying down the no-early-token cost), and the ONE `turn(input) → AsyncIterable<string>` seam with its replay/live/peer backend shelf and pinned proxy body fields |
| `skills/chat-harness-guardrail-facts` | Knowledge pack | model-only | Layering instructions (global < project < session precedence, a safety-floor exception), the closed instruction-source boundary (tool/file/web output is DATA never a command — prompt-injection defense), action risk tiers + confirmation gates, deterministic rule enforcement (hooks/lint) vs. prompted guidance, config precedence, reproducible setup/install, config-schema/prompt-externalization, and the ingestion trust story for imported third-party prose (import-time snapshot, pinned provenance, review-before-enable, a strip-nothing directive scan, prose-never-executes) |
| `skills/chat-harness-runtime-resilience-facts` | Knowledge pack | model-only | A deployed chat runtime's producer loop staying honest across turns and failures: a per-turn validator seeded with the session's accumulated state (the two-gates deadlock), catching a cross-payload violation producer-side before it ships, fail-closed independent disclosure knobs (no accidental ladder), a reserved terminal error line for a stream that already committed 200, halting loudly at a retry bound, and byte-identical additive opt-in flags |
| `skills/chat-harness-routing-facts` | Knowledge pack | model-only | Authoring a capability as a describe-to-route, load-on-demand skill vs. a hardcoded feature; the model-invoked vs. user-invoked species dial; description-based routing measured against a held-out adversarial eval corpus, not a felt sense |
| `skills/chat-harness-workflow-facts` | Knowledge pack | model-only | Decomposing a large task across multiple specialized agents with a clear chain of command (coordinator/planner/builder/reviewer, generator≠critic); verifiable typed hand-off contracts; deterministic scripted pipelines (fan-out/fan-in) as a distinct alternative to ad hoc dispatch |
| `skills/chat-harness-memory-facts` | Knowledge pack | model-only | Authoring a knowledge base as a cited, retrieval-by-search corpus (never prose dumped wholesale into context); durable cross-session memory (typed, with a hard exclusion list and a verify-before-trusting caveat) distinct from ephemeral within-conversation task state |
| `skills/chat-harness-tool-facts` | Knowledge pack | model-only | The tool/skill/resource three-way distinction; typed tool schemas; deferring a large tool catalog's loading until needed (search-to-load); read-only resources; routing the external-service-integration axis to `llm-gateway-facts` rather than duplicating it |
| `skills/chat-harness-logging-facts` | Knowledge pack | model-only | Hook-based logging/tracing distinguishable from user input; measuring routing/skill accuracy against a held-out adversarial suite over repeated runs (judge-noise vs. a real regression vs. a structural leak); background-task notification vs. polling, the distinct case of polling genuinely external state, and the replay-CI/live-acceptance two-tier proof split (deterministic replay as the standing gate; one engineered, defect-baiting live turn as a change's acceptance) |
| `skills/agent-residency-facts` | Knowledge pack | model-only | Classifies a conversational agent as a Resident Agent (a CLI harness — persistent filesystem/git/shell host) or an Ephemeral Agent (a hosted chatbot — per-conversation sandbox, function-calling tool surface) across five axes (host/persistence, context assembly, tool use, orchestration/concurrency, trust boundary); routes to which existing pack owns each tier's actual guidance, and names the check to run before writing a cross-tier finding into either |

All ten packs are `user-invocable: false` — model-only, routed by description. Each carries a
`scripts/routing-corpus.json` (positives/negatives, adversarial near-neighbors named explicitly)
and an `evals/evals.json` (this workspace's `eval_check.py` schema, converted 1:1 from the same
cases) so both the legacy and forge-native eval tooling can regress the same suite.

## Two families, two decompositions

The LLM-integration two came from the user's own framing — "Anthropic LLM gateways and JSONL"
names two genuinely distinct concerns (who you're allowed to call and how the secret stays safe,
versus how you correctly consume what comes back) — confirmed by a `break-down-problem` pass
(technical-architecture domain, `coverage_check.py` clean: 7 leaf reference files, 11 actions,
zero unhosted, zero unjustified) before either was authored.

The chat-harness six came from a SECOND, larger `break-down-problem` pass over "everything learned
about mini/portable chat-agent harnesses" — 6 nodes, 21 actions, 21 hosts, zero unhosted, zero
unjustified. The six cluster along a genuine structural seam (what governs behavior, what the
agent can invoke, how multiple agents compose, what it remembers, what it can reach outside its
own context window, and how its behavior is measured) — not an arbitrary split of the user's own
named list. `chat-harness-tool-facts` deliberately routes its
external-service-integration axis to `llm-gateway-facts` rather than re-deriving it, so the two
families interlock instead of duplicating.

## Cross-plugin seam

Neither LLM-integration pack owns `@agent-ui/a2ui`'s OWN shipped system as a repo-specific answer —
that's the `agent-protocols` plugin's `a2ui-chat-agent-facts` pack (dated, `file:line`-cited against
a single snapshot). `agent-protocols`'s `a2ui-chat-agent-facts` also carries a THIRD reference,
`anthropic-sse-wire-contract.md`, documenting the same Anthropic contract as THAT repo's own dated
answer — the two packs describe the same underlying facts from two different postures (portable
pattern vs. this-repo's-current-state) and should stay consistent, not merge. The chat-harness six
similarly do not own Claude Code's own docs as a versioned reference — they teach the pattern,
citing this session's own observed, current mechanics and flagging where a tool name may drift
across harness versions (the portable claim is the two-mechanism SHAPE, not one exact tool name).

## ADR-0006 transition table (renamed 2026-07-21)

Old handles remain greppable only in ledgers, CHANGELOGs, ADRs, and attics.

| Old name | New name |
|---|---|
| `agent-residency-taxonomy` | `agent-residency-facts` |
| `chat-harness-instructions-and-guardrails` | `chat-harness-guardrail-facts` |
| `chat-harness-knowledge-and-memory` | `chat-harness-memory-facts` |
| `chat-harness-observability` | `chat-harness-logging-facts` |
| `chat-harness-orchestration-and-workflows` | `chat-harness-workflow-facts` |
| `chat-harness-skills-and-routing` | `chat-harness-routing-facts` |
| `chat-harness-tools-resources-and-services` | `chat-harness-tool-facts` |
| `llm-jsonl-streaming` | `llm-streaming-facts` |
| `llm-provider-gateway` | `llm-gateway-facts` |

v1.0.17 · assembled 2026-08-19 · #743 (PR #742's checker verdict 1/4 — routing debt): the 1.0.16
upsert wave landed `llm-gateway-facts`' 7th axis (`live-ops-diagnostics-and-model-tiering.md`)
with ZERO description edits by directive, leaving axes 5-7 (single-flight 401 refresh, retry
policy + streaming pass-through, live-gateway ops/model tiering) invisible to routing and the
corpus notes still reading "four axes" from the 08-17 fold. Description gains one clause
registering all three (683/700 chars, W8; the #730/#715 implement/build/write NOT-fence
untouched); the consult table was already complete (7 rows, no edit owed); `evals/evals.json` +
`scripts/routing-corpus.json` notes reworded to "all seven axes" and gain t17-t22 positive
triggers for the newly-described vocabulary (existing t01-t16/n01-n12 untouched). SKILL.md body
gains a one-sentence ceiling note directly under the consult table: at the 7-axis
`pack-writing-rules` ceiling; the next axis proposal triggers `plan-skill-split`/INDEX rather than
an eighth row. `/check-routing llm-gateway-facts` + its `[[llm-streaming-facts]]`/
`a2ui-chat-agent-facts`/`a2ui-protocol-facts` fence siblings re-judged clean.

v1.0.16 · assembled 2026-08-19 · agent-ui provider/harness doctrine fold (branch
`upsert-llm-provider-doctrine`): four packs extended from field-proven agent-ui doctrine, every
ADR claim read at source via the GitHub API (ADR-0073/0137/0200/0208), each target diff-read first
so upserts EXTEND, never restate. `llm-gateway-facts` +1 axis
(`live-ops-diagnostics-and-model-tiering.md`: per-model curl matrix as the first diagnostic, the
upstream-503-storm posture — plain REST + bounded retry + verify-writes-landed, planning-vs-
execution model tiering as a standing config decision; ADR-0073's dev-proxy trust-boundary shape
diff-checked and found already fully covered — no restatement). `llm-streaming-facts`: the
stream-abstraction file gains the ONE `turn(input) → AsyncIterable<string>` seam (ADR-0073/0137),
the three-backend shelf — deterministic replay as CI backbone / HTTP-only proxy / peer (ADR-0200
cl.3), pinned request-body fields (proxy drift = spec diff, not silent break), and the NDJSON
splitter's own chunk-boundary contract; validate-then-stream gains the latency-cost/leading-
meta-line section (the one-line answer that beats the burst; agent-ui #1101's `flowEnd`-on-the-
envelope as evidence). `chat-harness-guardrail-facts`: the injection-defense file gains the
ADR-0208 ingestion trust story (import-time snapshot over runtime fetch, pinned commit provenance
with dropped-and-counted honesty, declared-scope fidelity, review-before-enable + copy-on-opt-in,
directive scan as a strip-nothing review aid, prose-never-executes) — kept as a second lens on the
existing axis, not a seventh axis (the #552 split ruling respected). `chat-harness-logging-facts`
+1 axis (`live-turn-acceptance-and-replay-ci.md`: replay-CI vs one live acceptance turn, the
fresh-server/OS-allocated-port/proven-teardown run shape from agent-ui `e2e-devtools.mjs`, the
bait-the-defect acceptance ask from #1101's closing verification) — placement judged per the
brief's own escape hatch: this pack owns the proof/measurement axis, tool-facts owns extension
surfaces, so `chat-harness-tool-facts` is deliberately untouched. ZERO description edits (all
routing surfaces byte-unchanged, per the merge-desk directive — the #715/#706 fences stand);
consult tables + sources.md provenance notes updated in the same change.

v1.0.15 · assembled 2026-08-19 · #715 (the #676 sweep's implement/build/write-the-code leak): a
passive "ANSWERS; does not build" / "answers, no build" disclaimer is not an explicit NOT-fence
against implement/build/write verbs on a menu with no builder present — a blind routing judge
vote-confirmed 3-0 leaked 7 no-trigger cases (7 named implement/build/write-the-code asks) to the
nearest topic owner as fallback. Explicit `NOT an implementation ask (implement/build/write the
code — route to your own project's build seat)` fence added to `llm-gateway-facts`,
`llm-streaming-facts`, and `chat-harness-runtime-resilience-facts`; a config-authoring variant
(`implement/build/write/add the config or code yourself`) added to `chat-harness-guardrail-facts`
since its own leaking case was a settings.json edit, not pure code. `evals/evals.json` notes
updated for all four; post-fix full-suite blind re-judge clean (110/111 across the four touched
suites, one pre-existing hung vote unrelated to the fence wording — see #715). `wording-checker`
pass: see PR.

v1.0.14 · assembled 2026-08-19 · #706 (2026-08-19 estate sweep, #676's final matrix): the
`chat-harness-logging-facts` / `chat-harness-routing-facts` sibling fence made reciprocal in BOTH
descriptions, closing a 2-of-3 steal on logging-facts' own t07/t09 ("measure whether my
descriptions route correctly", "build a held-out adversarial test suite") — routing-facts now
explicitly owns AUTHORING a new eval corpus, logging-facts owns RE-RUNNING an existing one over
repeated runs to track regression vs. judge noise. Both evals.json gained reciprocal negatives
mirroring the other suite's near-duplicate positive phrasing (routing-facts n19/n20 mirror
logging-facts' t07/t09 verbatim; logging-facts n16/n17 mirror routing-facts' t13/t14 verbatim).
`/check-routing llm`: see PR.

v1.0.13 · assembled 2026-08-17 · ADR-0020 wave 6 companion (#524): `agent-residency-facts` and
`chat-harness-workflow-facts` repoint their `team-or-solo-rules` citations at `teamwork:fleet-rules`
(D5 merged the former into the latter) — also fixes a stale `orchestration:` plugin-boundary
prefix in `agent-residency-facts`' routing table (should have read `teamwork:` since the ADR-0006
rename). Pointer-only, no trigger/description change; both skills' evals untouched beyond the
same string fix in comments.

v1.0.12 · assembled 2026-08-17 · 1.0.12: `plan-skill-split` resolves the split signal PR #547
flagged (issue #552) — `chat-harness-guardrail-facts` had drifted to 8 reference files, one past
the `pack-writing-rules` 3-7 target, after its own fold consolidated 5 v2-harvest lessons into one
file specifically to hold that count rather than let it run to 10-11 (a documented
literature-shaped-bundling admission). Verdict: split. New pack `chat-harness-runtime-resilience-facts`
takes the two agent-ui-grounded, deployed-chat-runtime producer-loop axes —
`multi-turn-validation-and-state-seeded-gates.md` (moved whole) and
`disclosure-and-failure-surfacing-in-a-chat-runtime.md` (moved, then un-bundled in the same change
into `disclosure-knobs-and-progress-detail.md` + `failure-surfacing-in-a-chat-runtime.md`, landing
the new pack at 3 axes, not 2) — leaving `chat-harness-guardrail-facts` at 6 axes, its own
CLI-instruction-layer scope. Both packs' SKILL.md/evals/routing-corpus/sources.md updated;
referrer survey found no existing external mention specific enough to need repointing (every
referrer names the pack at the general instruction-layering/guardrail level, unaffected by the
split). Full manifest, rejected alternatives, and evidence: issue #552's Findings comment.
`release_gate.py`: clean · v1.0.11 · assembled 2026-08-17 · 1.0.11: llm-fold step of issue #526 (part of #526, not closing
it) — the agent-ui#1115 "Scope-conformant revision v2" knowledge-harvest export (53 of 60 v2
lessons IN, 8 packs) folded across 8 chat-harness/gateway/streaming packs as 19 new reference
files (workflow +3, routing +4, tool +2, memory +2, guardrail +1 consolidated, logging +2,
gateway +2, streaming +3); 8 lessons hard-deduped against pre-existing coverage and skipped by
name (workflow's validate-then-stream/empty-not-invalid → llm-streaming-facts; workflow's
client-held-session/shouldRunTurn → llm-gateway-facts; routing's server-validated-selection →
llm-gateway-facts; tool's one-provider-seam[split] and guardrail's browser-cannot-hold-secret
[split] → llm-gateway-facts; logging's byte-pinned-prompt[split] → chat-harness-guardrail-facts);
7 CLI-tier lessons + 3 split-dropped development halves confirmed already excluded by v2 itself,
relayed to #543. chat-harness-guardrail-facts flagged at 8 reference files (one past the
pack-writing-rules 3-7 target) — a named split signal for a follow-up `plan-skill-split` pass, not
resolved here. Every SKILL.md consult table gained rows for the new files; every touched pack's
`sources.md` gained a dated Provenance note citing the v2 comment. `release_gate.py llm`: clean.
· v1.0.10 · assembled 2026-08-16 · 1.0.10: #348 footer sweep: 8 packs' stamped "Extending this pack" paragraph replaced with the one-line `Extension: governed by [[make-pack]]` citation per pack-writing-rules (harness 3.8.9) — mechanical, bodies otherwise untouched · v1.0.9 · assembled 2026-08-15 · 1.0.9: the six chat-harness-{guardrail,logging,memory,routing,tool,workflow}-facts SKILL.md files each carried a templated "Done when/NOT done" paragraph after their Consult procedure, restating step 2's answer contract (claim + grounding + failure mode) in a different grammatical register — bloat-audit CALIBRATION's boilerplate-restatement flag (closes #339). Cut from all six; no description, routing, or eval change · v1.0.8 · assembled 2026-08-15 · 1.0.8: chat-harness-guardrail-facts' config-precedence-and-setup.md — two dated in-place amendments after the cited worked instance changed underneath it: the global `dotenv-guard.py` PreToolUse hook (user settings.json) was retired 2026-08-15 in favor of `permissions.deny` Read rules for `.env`/credential paths, so both citations of it (the layering worked-instance and the additive-merge concrete example) now carry amendment notes; the mechanism claims themselves stand unchanged. Prose amendment only — no description, routing, or eval change · v1.0.7 · assembled 2026-07-22 · 1.0.7: the #79 description diet — all 9 llm pack descriptions trimmed suite-aware (8,864 → ~4,500 chars), then re-healed where the trim cut distinctive frame vocabulary (memory-facts' axis/Grep-then-Read/answers-not-generates/admission-gate cluster — 5 cases healed to 36/36; routing-facts' dial/preload vocabulary — t06/t10 healed; workflow-facts' earns-a-team + hand-off-fields quotes — t05/t07 healed; guardrail-facts' per-turn-validator quote). Residual fails annotated at floor in their own suites: the full-menu-twin class (first-person my-skill asks legitimately owned by harness's tools on a full-estate menu — these suites were calibrated llm-only) plus single-judge noise. Wave-boundary proof: 1087/1098 estate-wide · v1.0.6 · assembled 2026-07-21 · 1.0.6: chat-harness-logging-facts' routing-accuracy measurement history gains a fourth dated outcome class — the menu-scope collision (a case fails with no description change and no judge noise because plugins merged and the union menu itself changed; heal the prompt via ordered context split, not the descriptions), from this workspace's ADR-0008 run (PR #73), with the hardened noise rules (2-of-3 = noise, 3-of-3 with verbatim fence = known-ambiguous) · v1.0.5 · assembled 2026-07-21 · 1.0.5: ADR-0007 dir alignment — the plugin's directory renamed to its plain plugin name (was the frozen `llm 0.1.0`); version-suffixed, space-bearing paths retired estate-wide; pointer updates only · v1.0.4 · assembled 2026-07-21 · 1.0.4: ADR-0006 harness-rename sweep — live references rewritten (chat-harness packs' routing-judge/skill-writing-rules citations; dated cache-path citations keep their versions); pointer updates only · v1.0.3 · assembled 2026-07-21 · 1.0.3: ADR-0006 docs-rename sweep — live references rewritten; pointer updates only · v1.0.2 · assembled 2026-07-21 · 1.0.2: ADR-0006 teamwork-rename sweep — live references rewritten (chat-harness-workflow-facts' team-lead citations, agent-residency-facts' teamwork:parallel-work-rules pointers); pointer updates only · v1.0.1 · assembled 2026-07-21 · 1.0.1: ADR-0006 agent-protocols-rename sweep — live references to agentic-ui's old plugin/member handles rewritten (streaming/gateway fences); pointer updates only · v1.0.0 · assembled 2026-07-21 · 1.0.0: ADR-0006 rename PR 3/9 — all nine members take the simple paradigm's -facts shape (transition table above); the plugin name keeps `llm` under ADR-0006 Decision 7's term-of-art shelf exception. MAJOR bump — breaking. Workspace sweep (52 files, ledger history excluded); 282-case pre-rename baseline captured, post-rename re-measure in the campaign PR · v0.5.0 · assembled 2026-07-20 · 0.5.0: `skills/agent-residency-taxonomy` added — a ninth, cross-cutting pack classifying a conversational agent as a Resident Agent (CLI harness) or an Ephemeral Agent (hosted chatbot) across five axes, routing to which existing pack owns each tier's guidance and naming the check to run before writing a cross-tier finding into either. Grounded in a real 2026-07-20 incident (CLI-harness dispatch findings written into chat-harness-instructions-and-guardrails as if they were hosted-chat-agent facts, caught and reverted mid-task) plus a baseline test showing the underlying reasoning already exists in the abstract — the pack's value is a named, cheap-to-invoke checkpoint under real dispatch load, stated honestly rather than as a missing-fact claim. Reciprocal fence landed both directions with chat-harness-instructions-and-guardrails (Boundaries section + evals n13). skill_lint.py + potency_lint.py clean; skill-auditor FLOOR review PASS. release_gate.py: clean · v0.4.1 · assembled 2026-07-19 · 0.4.1: knowledge-pack factory-route convention repointed from scribe's retired `knowledge-forge` to forge's `pack-forge` (workspace-wide rename campaign) — every chat-harness-* skill's reference to its authoring factory updated; no functional/behavior change, a naming correction only. · v0.4.0 · assembled 2026-07-17 · 0.4.0: chat-harness-instructions-and-guardrails gains a seventh axis — references/multi-turn-validation-and-state-seeded-gates.md (a per-payload validator in a multi-turn loop must judge the state the consumer will hold; the two-contradictory-gates deadlock; persistent model "misbehavior" is a harness question first; catch cross-payload violations producer-side as a self-correct round), grounded in agent-ui TKT-0081 as a directly verified worked instance (validateA2ui sessionSeed, file:line at commit c8aee65); description + consult table + invariants route it; corpus +3 positives (plus 3 config-schema positives the 0.3.0 axis never got), evals t22–t24; the ADR-0137 tools/agent→src/agent move re-verified across sources.md and config-schema-and-prompt-externalization.md (one missed line-number pair fixed after an independent skill-audit flagged it). release_gate.py: clean · v0.3.2 · assembled 2026-07-16 · 0.3.2: chat-harness-instructions-and-guardrails and chat-harness-observability descriptions re-budgeted under the 1024 cap (the 0.3.1 eval tunings had pushed both over) — triggers preserved; instructions' generic does-not-build fence replaced by a NAMED-artifact fence after the post-trim judge leaked three build asks (the #8 lesson: name the artifacts) — re-judge 33/33; observability 31/31 · v0.3.1 · assembled 2026-07-15 · 0.3.1: /eval-run tuning (254/258 → 258/258 on the re-judged suites): chat-harness-instructions-and-guardrails gains the registry-drift trigger phrase (t20 was dead — the registry-projection claim lived only in the reference body); chat-harness-observability's does-not-build fence strengthened after three build-ask leaks (n07/n08/n09), with "build a held-out adversarial suite" added verbatim when the stronger fence overcorrected t09 to dead — blind re-judges confirm both suites clean · v0.3.0 · assembled 2026-07-15 · 0.3.0: chat-harness-instructions-and-guardrails gains a sixth axis — references/config-schema-and-prompt-externalization.md (one typed shared config schema over scattered params; prompt prose in files, never string constants; option lists projected from the real registry; byte-identity on refactor), grounded in agent-ui ADR-0135 as a directly verified worked instance (sources.md extended to three instances); description + consult table route the new axis; evals t18–t21 cover it · v0.2.1 · assembled 2026-07-14 · 0.2.1: displayName 'LLM' added to the manifest — plugin naming hygiene ruled 2026-07-14: Title Case display names with UI/LLM acronyms uppercased (marketplace entries carry the same field; Claude Code ≥2.1.143, falls back to name) · v0.2.0 · assembled 2026-07-13 · the chat-harness six added: a second `system-decompose` pass (6
nodes/21 actions, `coverage_check.py` clean) built into 6 parallel-authored knowledge packs
covering the mini/portable chat-agent-harness construction layer, folded into this plugin rather
than a new one (a chat harness is built ON TOP OF the LLM-integration layer this plugin already
taught). Grounded in Claude Code's own live, current harness mechanics (the instruction-source
boundary, the three-tier action-risk model, hooks, `ToolSearch` deferred-tool loading,
background-task notification, the four-type auto-memory system) plus this workspace's own
conventions (routing-corpus/evals discipline, `handoff-compose`, the `orchestration` plugin's
agent roster, `knowledge-forge`, a real dated eval-run history). One authoring convention error
caught and fixed across the batch: `[[double-bracket]]` handles are for cross-SKILL links only —
a same-skill sibling reference file is named in plain, unbracketed prose. `release_gate.py`: clean.
· 0.1.0 · assembled 2026-07-13 · initial: distilled from `@agent-ui/a2ui`'s live-agent system
(`packages/agent-ui/a2ui/tools/agent/`) via a `system-decompose` pass (technical-architecture
domain, `coverage_check.py` clean) into two skills, generalized as portable technique rather than
ported as a repo-specific answer pack.
