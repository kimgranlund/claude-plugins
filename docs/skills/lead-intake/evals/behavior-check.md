# lead-intake — Phase 5 behavior check (with-skill), 2026-08-10

Fresh-context dry-run: the session executed SKILL.md's Phase 1–2 adoption as written (agent
file + all four preloads read from disk), then processed the two baseline seeds plus a
build-ask probe the baseline lacked. No records created, no Skill calls, no gh writes —
verified by the run's own constraint compliance and its verbatim would-run payloads.

## Assertions vs evidence

1. **Adoption acknowledgment — PASS.** Full standing block before any seed: contract file
   named, all three host deltas, duration rule.
2. **Record contract — PASS.** Seed 1 (clear bug report): complete payload (Summary/
   Acceptance/Repro/Expected-vs-actual/Classification/Severity/empty Findings), verdict line
   "1 record minted, 0 blocked", per-record line with named gaps and the `/file-bug <id>`
   resume pointer. Stop-at-record held — no investigation.
3. **Clarify discipline — PASS.** Seed 1: zero rounds (clear). Seed 2 (vague): exactly ONE
   batched round, four sharp questions (which surface / weak how / example / urgency) — the
   very questions the BASELINE buried as Scope/Open gaps in a "scope TBD" ticket. Correctly
   held capture until the round resolves (a live AskUserQuestion blocks until answered, so
   "round spent" always resolves in real use).
4. **Intake-only held — PASS.** The "just fix it real quick, probably one line" probe was
   declined verbatim-per-contract ("regardless of how small it looks"), with the resume
   pointer — and it correctly used the context-this-session-HAS branch (no re-ask of which
   bug), the exact failure-branch nuance the body added over the agent.

## Baseline → with-skill deltas (the behavior the skill buys)

| Dimension | Baseline (ad hoc priming) | With skill |
|---|---|---|
| Standing contract | none — one vague sentence | full acknowledgment block |
| Procedure locus | Skill-invoked forks it lost control of | inline, this session's own turns |
| Vague seed | questions buried in a TBD ticket | one batched round actually asked |
| Delivery | fragments across SendMessages + root notifications | verdict-line contract per seed |
| Build ask | untested | declined with resume pointer |

## Remaining live-verification item

The AskUserQuestion round firing from a REAL /lead-intake session (this check simulated the
round's content and timing, not the tool mechanism — the host session's own channel is the
one place it's known to exist). First real use is the proof; same disclosure class as the
estate's other named platform assumptions.
