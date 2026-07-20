# Baseline (no skill) — Q1: CLI agent vs. hosted chatbot guardrail design

**Prompt:** What's the difference between a CLI coding agent (like Claude Code) and a hosted
chatbot agent, in terms of how you'd design safety guardrails for each?

**Answer (fresh agent, no project context, no skill):**

A CLI coding agent operates with direct filesystem/shell/git access on a developer's actual
machine and repos — the guardrails are mostly about blast radius and reversibility: permission
prompts before destructive ops (force-push, rm -rf, --no-verify), sandboxing/dry-run modes, scoped
tool allowlists, and audit trails since the "user" present to consent is usually the same person
who'll bear the consequences. A hosted chatbot agent usually acts on behalf of many different
end-users against shared backend systems (accounts, payments, data stores it doesn't own), so
guardrails skew toward identity/authorization boundaries, rate limiting, content policy,
preventing one user's session from affecting another's data, and stricter output filtering since
responses go to people who didn't write the prompt and may not trust the source. In short: CLI
agent guardrails are about "don't let one trusted operator's agent wreck their own stuff
irreversibly"; hosted chatbot guardrails are about "don't let this agent overstep its authority
across untrusted, multi-tenant interactions."

**Assessment:** genuinely solid — correctly distinguishes the two by trust model and blast
radius. Gap this skill still fills: no named vocabulary (Resident/Ephemeral), no explicit 5-axis
structure, no routing map to this workspace's OWN skills — this answer is correct in the abstract
but gives a reader nothing to check a SPECIFIC claim against, or route to.
