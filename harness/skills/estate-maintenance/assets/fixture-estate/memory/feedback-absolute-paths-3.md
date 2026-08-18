---
name: bash-relative-path-warning
description: "Stop proposing relative paths in Bash calls — always use absolute paths, this has been said repeatedly."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0003
  modified: 2026-08-11T08:05:00.000Z
---

Repeatedly corrected: a Bash call in this project must use an absolute path, never a relative
one. Stop proposing relative paths for file reads or writes here.
