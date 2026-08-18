---
name: checker-model-pin-note
description: "Checker agents already pin fable at medium in their own frontmatter; a per-dispatch model override on a checker is redundant and can detach effort from the agent definition."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0005
  modified: 2026-07-20T10:00:00.000Z
---

First telling: a per-dispatch `model` override on a checker agent is redundant with the
frontmatter pin the checker already carries, and can silently detach the dispatch's effort from
the agent definition's own tuned value. Pass no override on checker/review dispatches.
