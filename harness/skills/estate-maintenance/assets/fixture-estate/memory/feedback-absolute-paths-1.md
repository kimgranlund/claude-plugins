---
name: always-absolute-paths
description: "Never use relative paths in Bash tool calls in this project; always use absolute paths for every file read or write."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0001
  modified: 2026-08-01T09:12:00.000Z
---

Correction given the first time: a relative-path Bash call in this project resolved against the
wrong working directory and silently touched a different file. Use absolute paths for every Bash
file operation from now on.
