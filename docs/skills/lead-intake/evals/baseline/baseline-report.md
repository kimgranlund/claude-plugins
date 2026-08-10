# Baseline: ad-hoc-primed intake session (no skill), 2026-08-10

Fresh-context run. Priming: Kim's real-world habit verbatim — "You are my INTAKE session. Only
write bugs, tickets, features, etc. Don't do other work." Two seeds: (1) a concrete Safari
date-filter crash report; (2) "thinking we should maybe do something better with search, its
kind of weak". Dry-run constrained (no real records).

## What the ad-hoc session actually did

- **It did not run intake itself — it Skill-invoked `file-bug` and `file-feature`**, which
  forked into two background agents it then had to chase with follow-up messages to keep
  dry-run, ending idle waiting on forks whose results routed to the root session, not to it.
  The "session" the user primed never itself held the procedure.
- **Seed 2's clarifying questions were never asked.** The file-feature fork drafted three good
  questions (which search? weak how? example query?) and then — no interactive channel in a
  fork — filed them as Scope/Open gaps in a "scope TBD" ticket. A live user was one turn away
  the whole time.
- **The file-bug fork skipped the dedup sweep** (disclosed, but skipped) — procedure fidelity
  varied per fork.
- **Delivery scattered**: results arrived as two SendMessages plus two task notifications to
  the root, in fragments, with no verdict-line report contract anywhere.
- **Empirical side-finding:** the file-bug fork reported `AskUserQuestion` absent from its
  toolset — first direct evidence that an agent-spawned `context: fork` run structurally
  cannot ask (the flagged assumption's agent-spawned case; host-spawned remains open).

## The deltas the skill must produce (checked in Phase 5)

1. Standing adoption acknowledgment before any seed (assertion 1) — the baseline had none.
2. The session itself runs the procedure inline and reports the verdict-line contract
   (assertion 2) — the baseline delegated to uncontrolled forks with fragmented delivery.
3. Seed 2 gets its ONE batched AskUserQuestion round actually ASKED (assertion 3) — the
   baseline buried the questions in a TBD ticket.
4. Intake-only held by stated discipline (assertion 4) — untested in baseline (no build ask
   was included), asserted from the priming's own words being insufficient contract.

Raw fork payloads (both correct in content, wrong in channel): the file-feature dry-run's full
`gh issue create` payload and the file-bug fork's drafted command were delivered to the root
session and are preserved in the session transcript; content quality was NOT the baseline gap —
the missing standing contract (channel, clarify round, dedup fidelity, report shape) was.
