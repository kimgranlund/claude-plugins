# Baseline (no skill) — Q3: does file-based context assembly apply to a hosted chatbot

**Prompt:** Does file-based CLAUDE.md-style layered context assembly (global/project/session
config files read from disk) apply to a hosted customer-support chatbot the same way it applies to
a CLI coding agent?

**Answer (fresh agent, no project context, no skill):**

The mechanism (reading layered config files off disk at session start) doesn't apply directly to a
hosted chatbot, since there's typically no per-session filesystem and no notion of "current
working directory" the way a CLI tool has — but the underlying pattern (layered context: global
policy → tenant/customer-specific config → conversation-specific state, each overriding/extending
the previous) absolutely applies, just implemented differently: a system prompt template pulling
from a config service or DB (org-level policy, then bot/workspace-level settings, then
session/user context), rather than literal files. So think of CLAUDE.md as one instantiation of
"layered context assembly," and ask what your hosted bot's equivalent tiers are (platform-wide
guardrails / customer account config / conversation memory) rather than trying to port the
file-reading mechanism itself.

**Assessment:** also solid — correctly separates the MECHANISM (files on disk) from the PATTERN
(layered precedence), matching this skill's own "Context assembly" axis almost exactly. Gap this
skill still fills: no named vocabulary, no pointer to this workspace's own `llm:chat-harness-*`
family as the concrete place that pattern already lives for the Ephemeral side.
