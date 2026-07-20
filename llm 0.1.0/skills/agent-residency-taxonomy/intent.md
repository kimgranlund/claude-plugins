# intent — agent-residency-taxonomy
status: shipped          # forging | parked | shipped
species: knowledge
dials: { disable-model-invocation: false, user-invocable: false }
freedom: medium
type: capability-uplift

## trigger
should:      ["what's the difference between a CLI agent and a hosted chatbot",
              "is this a Resident Agent or an Ephemeral Agent",
              "does this guidance apply to a hosted chat agent or a CLI harness like Claude Code",
              "am I building for a CLI tool or a customer-facing chatbot",
              "which agent tier does this pattern belong to"]
should_not:  ["help me write a system prompt for my chatbot"]

## delta
WRONG (this session, real, 2026-07-20): CLI-harness dispatch findings (SendMessage
resume semantics, git worktree isolation, `gh` CLI merge/close mechanics) were
written into `llm:chat-harness-instructions-and-guardrails` as if they were
hosted chat-agent facts — caught and reverted by the user mid-task, twice
(once on the initial candidate list, once again after a correction was itself
misread backwards).
DESIRED: before writing agent-authoring/orchestration knowledge into any
knowledge-pack, check which tier (Resident vs Ephemeral) the target skill is
scoped to, and either confirm the fact's mechanism genuinely exists in that
tier's architecture, or reframe it as a same-tier-native illustration rather
than citing the other tier's tools as if they were native facts.

## fences
- NOT for authoring the actual Ephemeral/chat-agent guardrail content itself (llm:chat-harness-instructions-and-guardrails and its siblings own that)
- NOT for Resident-agent/CLI-harness authoring standards or orchestration patterns themselves (forge:agent-authoring-standards, orchestration:concurrency-design, orchestration:orchestration-design own that)
- NOT a general tutorial on building either kind of agent from scratch — narrowly the boundary classification + the axes that distinguish them + a routing map of which existing skill/plugin owns which tier's actual guidance

## assertions
1. The skill's description contains both "Resident Agent" and "Ephemeral Agent" as named terms.
2. The skill body states all 5 mechanistic axes (host/persistence, context assembly, tool use, orchestration/concurrency, trust boundary), naming which value belongs to which tier.
3. The skill body names, for at least 2 Resident-scoped and 2 Ephemeral-scoped existing skills/plugins in this workspace, which tier they belong to (a routing table).
4. `chat-harness-instructions-and-guardrails`'s own SKILL.md carries a reciprocal named-mention pointer to this new skill.

## gates
P0 route:      PASS — knowledge/procedure needed on demand; no mechanical pass/fail check, no always-true every-turn fact, no tool-wall/parallelism need. 2026-07-20.
P1 intent:     PASS — record confirmed by user as-drafted. 2026-07-20.
P2 evals:      PASS — evals.json (12 trigger / 8 no-trigger, lint clean), 4 behavioral assertions (from intent.md), 3 baseline prompts captured in evals/baseline/. 2026-07-20.
P3 draft:      PASS — SKILL.md authored from the Knowledge skeleton (5-axis table, routing table, residency-check handle, done/not-done predicate). 2026-07-20.
P4 language:   PASS — potency_lint.py clean (within budget); forge:linguistics-reviewer audit gate (L1/L3/L6) PASS with 4 findings, all 4 applied (compressed the meta-section into a named handle "the residency check"; added a per-axis fallback branch for hybrid agents; fixed the `NOT a <thing>` fence to `NOT for <thing> (<owner>)`; lowercased ad-hoc CAPS stress outside the one kept contrastive pair). Re-linted clean after rewrite. 2026-07-20.
P5 validate:   PASS — skill_lint.py + potency_lint.py both clean; skill-auditor FLOOR review PASS
               (no blocking findings, F1/R5/F2/F3/F4 all fixed); behavior check re-ran all 3
               baseline prompts fresh WITH the skill — all 4 intent assertions demonstrated (both
               tier names in description; all 5 axes stated with values; ≥2 Resident +
               ≥2 Ephemeral owners named and correctly routed to; reciprocal pointer landed) and
               the agent correctly declined the CLI-native worktree/SendMessage transfer in Q1,
               reframed the PR-merge/issue-close lesson as a same-tier refund/credit scenario in
               Q2 instead of quoting it verbatim, matching this skill's own harvest procedure; fence
               closure landed both directions (chat-harness-instructions-and-guardrails/SKILL.md's
               Boundaries section + its evals/evals.json n13). 2026-07-20.

## rulings
- Type note: baseline capture (evals/baseline/prompt-2-lesson-transfer.md) shows a fresh, directly-
  and-reflectively-asked agent already reasons through the CLI/chatbot boundary correctly — so the
  real gap this skill fixes is NOT "Claude lacks this reasoning in the abstract," it's "Claude
  doesn't reliably PAUSE to run this check mid-flow, under real multitasking dispatch load, without
  a named, discoverable checkpoint to invoke." Kept `type: capability-uplift` (the gap is real and
  demonstrated by this session's own incident, not a stylistic preference), but the skill body
  states this nuance honestly rather than overclaiming Claude has zero latent capacity here.
- skill-auditor FLOOR review (2026-07-20): PASS, no blocking findings. Fix-before-shipped F1
  (reciprocal pointer from chat-harness-instructions-and-guardrails missing) routed to this
  skill's own P5 fence-closure step. Accepted-with-note: R5 orchestration-row compression, F2
  session-deixis reword, F3 description re-budget, F4 empty references/ dir + this stray note —
  all four applied directly.
