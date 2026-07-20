# Baseline (no skill) — Q2: should a CLI-harness lesson go into chatbot guardrail docs

**Prompt:** I found a great lesson from my Claude Code CLI session about how dispatched sub-agents
behave — specifically, that a sub-agent given "don't merge this PR" sometimes closes the related
issue anyway since nobody told it not to. Should I add this lesson to my hosted chatbot's guardrail
documentation?

**Answer (fresh agent, no project context, no skill):**

Not as-is — it's a fairly narrow, mechanism-specific lesson (a sub-agent given a narrow negative
instruction defaults to literal scope and doesn't infer adjacent implications) rather than a
hosted-chatbot-specific guardrail. The transferable version is the general principle: negative
instructions don't compose or generalize — "don't do A" doesn't imply "don't do B" even when B
achieves the same outcome as A, so guardrail docs should state the intent/outcome to prevent, not
just enumerate prohibited actions. If your hosted chatbot also does multi-step tool use or
delegates to sub-tasks, that generalized principle is worth capturing; the specific "PR merge vs.
issue close" anecdote itself probably isn't relevant unless your chatbot touches GitHub.

**Assessment:** this is the most important baseline result — a careful, DIRECTLY-asked model
already reasons through the CLI/chatbot boundary correctly here, extracting the transferable
principle and declining the literal mechanism. This is exactly the reasoning that failed to fire
this session's real incident. The gap isn't that Claude can't do this reasoning in the abstract —
demonstrated here, it can — it's that under real multitasking dispatch load (many rapid actions in
one session, not a single reflective question), Claude doesn't reliably PAUSE to run this check
before writing a knowledge-pack entry. This skill's actual value is a named, discoverable
checkpoint ("which tier is this?") cheap enough to invoke mid-flow, not a missing fact this
baseline shows Claude already lacks.
