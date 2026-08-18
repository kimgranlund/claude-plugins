---
name: absolute-path-reminder
description: "Third time now: use absolute paths for Bash file operations, not relative paths, in this project."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0002
  modified: 2026-08-06T14:30:00.000Z
---

Third telling of the same correction — relative paths in a Bash call keep resolving against the
wrong cwd in this project. Always use absolute paths for Bash file operations.
