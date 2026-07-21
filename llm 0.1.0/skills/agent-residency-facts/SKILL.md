---
name: agent-residency-facts
description: >-
  Classifies a conversational agent as a Resident Agent (a CLI harness like Claude Code — a
  persistent filesystem/git/shell host) or an Ephemeral Agent (a hosted chatbot — a per-conversation
  sandbox with a function-calling tool surface), and routes to which existing skill owns each
  tier's guidance. Use when the user asks "what's the difference between a CLI agent and a hosted
  chatbot", "is this a Resident Agent or an Ephemeral Agent", "does this guidance apply to a hosted
  chat agent or a CLI harness like Claude Code", "am I building for a CLI tool or a customer-facing
  chatbot", "which agent tier does this pattern belong to", or before writing agent-authoring
  knowledge into a knowledge-pack. NOT for Ephemeral guardrail content
  (llm:chat-harness-guardrail-facts); NOT for Resident authoring/orchestration patterns
  (forge:agent-authoring-standards, orchestration:concurrency-design); NOT for building either
  agent kind from scratch (route to the owning tier's authoring skill).
disable-model-invocation: false
user-invocable: false
---

# agent-residency-facts

A conversational agent is either a **Resident Agent** or an **Ephemeral Agent**, and the two are
different enough on five structural axes that a fact true of one is routinely false of the other —
guidance, citations, and worked examples do not transfer between them by default.

## The residency check

Before writing or citing any agent-authoring or orchestration finding: name the tier it was
observed in, then name the tier the target skill is scoped to. Fresh-context reasoning already
gets this boundary right unprompted (`evals/baseline/prompt-2-lesson-transfer.md`); under real
multitasking dispatch load it doesn't reliably fire on its own — this handle is what fires it.

**Observed harness behavior (the 2026-07-20 authoring session; not independently re-openable —
treat as a dated incident report, not a versioned citation):** CLI-harness dispatch findings (background agent-resume semantics, git worktree isolation, `gh` CLI
merge/close mechanics) were written into
`llm:chat-harness-guardrail-facts` — an Ephemeral-agent-scoped skill — as if they were
hosted chat-agent facts, and had to be caught and reverted by the user mid-task.

## The two tiers, on five axes

| Axis | Resident Agent (CLI harness, e.g. Claude Code) | Ephemeral Agent (hosted chatbot) |
|---|---|---|
| Host & persistence | A real, persistent filesystem + git + shell on one machine; state survives across sessions (CLAUDE.md, memory files, git history) | A per-conversation/per-session sandbox; no persistent filesystem in the same sense; session state typically lives in an external database, not files |
| Context assembly | Layered file-based discovery — global/project/session CLAUDE.md, on-demand skill preload via `skills:` frontmatter, subagent `.md` definitions | System prompt + injected context (RAG retrieval, conversation history) — no file-layer discovery of that kind |
| Tool use | OS-level tools with real side effects — shell, file read/write/edit, git, browser automation | Narrower, business-domain function-calling against a defined API surface (e.g. `issue_refund`, `close_ticket`) |
| Orchestration & concurrency | Can spawn sub-agents into isolated environments with no self-resume once a dispatched subagent's turn ends; other actors (peer sessions) may concurrently touch the same shared repo (`orchestration:concurrency-design` owns the operational detail) | Typically isolated per-conversation; a collision, if it exists, is usually about a shared backend resource (a customer record), not a shared file tree |
| Trust boundary | The operator is generally the trusted principal (though tool output is still untrusted data) | The end user is often an external, less-trusted party the agent transacts with (a customer, not the operator) |

An agent that splits across the columns (a hosted sandbox with a persistent filesystem, a
cloud-resident dev agent) classifies **per axis, not per agent**: each row stands alone; apply the
row that matches, and never carry the other rows over on the column label's authority.

**Neither column is generic "best practice" — each is grounded in a real system.** The Resident
column is Claude Code's own documented and observed behavior (`orchestration:concurrency-design`'s
actor-classification taxonomy, `forge:agent-authoring-standards`'s async-lifecycle note, and this
skill's own incident above, each exists because of these mechanics). The Ephemeral column is what
`llm:chat-harness-guardrail-facts` and its sibling packs already document in depth for
the hosted chat-agent shape.

## Routing — which existing skill owns which tier's actual guidance

| Question shape | Tier | Owner |
|---|---|---|
| "Should this subagent use `isolation:worktree`", "another session has uncommitted changes I need" | Resident | `orchestration:concurrency-design` |
| "Solo vs. team, how many subagents, is this fan-out worth it" | Resident | `orchestration:orchestration-design` |
| "How do I write a thin subagent file, what belongs in `skills:` preload" | Resident | `forge:agent-authoring-standards` |
| "Which instruction layer wins, how do I gate a risky action behind confirmation" | Ephemeral | `llm:chat-harness-guardrail-facts` |
| "How does my chatbot remember things across turns/sessions" | Ephemeral | `llm:chat-harness-memory-facts` |
| "How do my chat-agent's skills/tools get selected at runtime" | Ephemeral | `llm:chat-harness-routing-facts` |

A question that names both tiers, or asks "does X from one apply to the other," is this skill's own
territory — answer with the relevant axis row above, then route to the owning skill only for the
tier the question is actually about.

## Running the residency check at knowledge-harvest time

Same tier → cite directly. Different tier → either confirm the underlying mechanism genuinely
exists in the target tier's architecture (not just a superficially similar-sounding concept), or
extract the generalizable principle and illustrate it with a same-tier-native invented scenario,
citing the origin incident honestly as a different trust class (see
`llm:chat-harness-guardrail-facts`'s own `references/sources.md` for a worked example
of this exact citation discipline — trust-class 2, "Observed harness behavior," widened to cover
both a stated rule and a directly-witnessed incident).

**Done** when a claim about agent behavior states which tier it was observed in before it's applied
to the other, and a cross-tier citation either names the transferable principle explicitly or
declines the transfer with a stated reason. **NOT done** while a CLI-specific mechanism (a shell
tool, a git operation, a filesystem path) is quoted as if it were a fact about a hosted chatbot's
architecture, or vice versa.
