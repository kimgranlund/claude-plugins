---
name: orchestration-model-drift-report
description: "Kim observed several subagents riding the orchestrating session's higher-priced model tier during a busy stretch; the root cause traced back to per-dispatch model overrides plus inherit-class agents that carry no pin of their own."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0006
  modified: 2026-08-05T09:00:00.000Z
---

Second telling, different symptom: several subagents were observed riding the orchestrating
session's own (higher-priced) model tier during a busy stretch. Root cause traced to two things —
per-dispatch model overrides on agents that already carry a pin, and inherit-class agents that
carry no pin of their own at all.
