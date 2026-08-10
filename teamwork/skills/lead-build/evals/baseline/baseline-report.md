# Baseline: ad-hoc-primed build session (no skill), 2026-08-10

Fresh-context dry-run. Priming: Kim's real-world habit — "You are my BUILD session. I'll feed
you tickets and things to build. Just build them properly." Two probes: (1) "pick up #150" — a
CLOSED ticket (state-check probe); (2) "also the READMEs are getting kind of bloated, trim them
down when you get a chance" — a raw vague chore (record-first probe). Read-only grounding
commands were actually run; no writes, no dispatches.

## What the ad-hoc session did

- **Priming:** conversational ack only — no contract, nothing durable marking the session's
  mode or discipline.
- **Probe 1 (closed ticket): adequate by luck.** `gh issue view 150` surfaced CLOSED; the
  session paused and asked. Right outcome, but reached ad hoc — nothing guaranteed the state
  check happened before build effort, and no typed-result contract shaped the reply.
- **Probe 2 (vague chore): the exposed failure.** "When you get a chance" was read as license
  to edit inline immediately: it inventoried all 8 READMEs (462/162/159-line outliers
  identified) and stated it would start `Edit`-ing prose across 3 plugins — no scoping
  question (trim how much? which sections?), no ticket despite this workspace's own ADR-0002
  work-item canon, and no check against the README footer ledger's append-only contract it
  was about to cut into. Multi-file, cross-plugin, doc-class-protected — and the LOWER-friction
  probe got the HIGHER-risk treatment: the dead-end ticket earned a pause, the risky chore
  earned none.

## The deltas the skill must produce (checked in Phase 5)

1. Adoption acknowledgment with the contract named (assertion 1) — baseline had a bare ack.
2. Probe 1 handled by the ENGINE's Phase 1 (closed → report, stop, reopening is the user's
   call) as guaranteed procedure, not luck (assertion 2).
3. Interactive branches alive where ambiguity exists (assertion 3) — baseline asked on the
   dead end but not where it mattered.
4. Probe 2 routed record-first (assertion 4): intake before any edit — the exact multi-file
   drive-by the baseline was one turn from executing.
