# Baseline (no concurrency-design skill) — "My subagent was mid-move when it noticed another, completely independent Claude Code session had uncommitted edits to the same files. What should it have done, and what should I do now?"

Captured 2026-07-17, fresh general-purpose agent, no tools, no repo context beyond ambient memory. This prompt is closest to the actual incident.

## Response

Short version: the subagent should have stopped and surfaced it, not tried to resolve it. [...] It should have then reported the collision upward rather than picking a resolution on its own [...] That's a judgment call above its pay grade [...] needs a human [...] not a subagent guessing.

What you should do now:
1. Check ground truth before assuming anything: `git status` and `git diff` [...]
2. Go coordinate with the other terminal directly — this is the part your subagent structurally cannot do. It's not a spawned agent you can reach with SendMessage; it's an independent human-driven session outside this one's reach. You need to either pause that session, have it commit or `git stash` its work [...]
3. Once the other session's state is safely committed or stashed, resume or replay the move cleanly [...]
4. Longer-term fix [...] git worktrees per session avoid this class of collision entirely [...]

## Gaps vs. the skill (annotated post-hoc)

- **Strongest baseline of the three** — stop/verify/escalate is already close to correct, which is good evidence the skill's job here is less "teach a totally new behavior" and more "make the full protocol reliable and complete by default," per skill-authoring-standards' capability-uplift-vs-encoded-preference axis: uplift on the parts below, preference (state the sequence, stop) on this part.
- Asserts flatly "it's not a spawned agent you can reach with SendMessage" — this is WRONG in this harness for one real subcase: a peer session that shows up as a `teammate-message` sender (a name-addressable channel this session used successfully, mid-incident, to resolve exactly this kind of question) is reachable via `SendMessage`. The baseline collapses "not spawned by me" and "unaddressable" into one case; they're actually three cases (spawned subagent — full control; named teammate session — addressable via SendMessage; opaque/unnamed session — must route through the human), and only the third is truly "structurally cannot."
- "have it commit or `git stash` its work" is offered as something the user just does, without naming that this requires knowing whether the other session is EVEN ADDRESSABLE at all — for the opaque case there may be no way to ask it to pause short of finding the human running it.
- No mention of independently verifying either side's self-reported state rather than trusting it (a discipline the actual incident leaned on twice — once re: the builder's own report, once re: the ADR-0138 session's "done" claim, both confirmed via direct `git diff`/timestamp inspection before acting).
