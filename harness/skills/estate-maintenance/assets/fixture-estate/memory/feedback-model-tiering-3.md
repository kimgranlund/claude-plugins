---
name: review-tier-pin-reminder
description: "Review and critic agents should run at their own already-pinned tier — never pass a model override on a checker dispatch, only pin the model explicitly on ad-hoc general-purpose calls."
metadata:
  node_type: memory
  type: feedback
  originSessionId: fixture-session-0007
  modified: 2026-08-15T11:00:00.000Z
---

Third telling of the same underlying fact, worded again differently: review and critic agents
should run at their own already-pinned tier. Never pass a model override on a checker dispatch —
only pin the model explicitly on ad-hoc general-purpose calls that have no definition of their own.

**Regression note (gh#645):** this fixture trio is deliberately realistic (long, varied-length
descriptions, not near-identical toy strings) — it exists to prove D1's calibration catches a
genuine third-telling pattern that raw Jaccard misses. See `detect.py selftest`'s explicit
pairwise-metric assertion.
