# Behavior check — with skill vs. baseline (Phase 5.3)

Same 3 prompts, fresh sessions, skill body supplied as standing context (the marketplace-install
step doesn't exist yet for an unshipped skill, so the check hands the fresh agent the SKILL.md body
directly rather than relying on auto-discovery — content parity with a real trigger, not the
trigger mechanism itself, which `evals/evals.json` covers separately).

## Prompt 1 — "set up this repo so multiple Claude sessions don't collide"

**Not cleanly captured.** The dispatched agent had real tool access despite an explicit "no tools"
instruction (general-purpose agents are not tool-walled by prompt instruction alone) and acted for
real against the live agent-ui repo — including adding a full doctrine restatement as a new
"## Concurrency" section in that repo's actual CLAUDE.md. Reverted immediately (`git diff`
confirmed clean afterward); the stray agent was messaged to stand down and confirmed.

This was a real mistake in the check's own setup, not a shrug — but it produced a genuine,
load-bearing finding: the skill body as first drafted said the CLAUDE.md rule "belongs" there
without specifying it must be a short pointer, not a restatement — exactly the gap the agent's
real action exposed. **Fixed in SKILL.md's Decide step 2** (now explicit: "a one-line pointer...
the skill's own doctrine staying here, in this one file... Copying these steps into CLAUDE.md
instead creates a second, drift-prone copy"). Re-verified: `potency_lint.py` and `skill_lint.py`
both clean after the fix.

Re-running this specific prompt safely (no real tool access, advisory framing) is deferred — the
other two prompts below already demonstrate the guidance is followed correctly when read; this one
additionally proved something about a specific gap in the guidance's own text, which is now closed.

## Prompt 2 — "I'm about to dispatch two builder subagents that will both touch files in the same area — should I do anything special?"

| | Baseline (no skill) | With skill |
|---|---|---|
| Names actor type before advising | No — reasons about "subagents" generically | Yes — explicitly "actor type one (subagents you spawned this session)... full control" |
| Isolation named as default | Yes, but as one option among several (partition / worktree / tell each other) | Yes, as the first, headline move: "set `isolation:\"worktree\"` on both dispatches" |
| Ticket-status check mentioned | No | Yes — explicitly checks `.claude/docs/tickets/` before handing out scope |
| Commit cadence tied to collision risk, not just merge hygiene | Mentioned, framed as merge hygiene | Mentioned, framed the same way the skill frames it: shrinks reconciliation blast radius |
| Considers non-spawned concurrent actors | **No — entirely scoped to the two subagents**, doesn't consider a third, unrelated session might also be active | Implicitly correct by construction (actor-type framing extends to it), though not tested directly by this prompt |

Assertion 1 (isolation named as default) and assertion 4 (ticket-status named) — **demonstrated**.

## Prompt 3 — "My subagent noticed another, completely independent Claude Code session had uncommitted edits to the same files. What should it have done, and what should I do now?"

This is the sharpest contrast of the three, and the one closest to the actual incident.

| | Baseline (no skill) | With skill |
|---|---|---|
| Stop-before-resolving | Yes | Yes |
| Classifies the actor before deciding what to do | No — reasons about "spawned vs. independent" as a flat binary | Yes — explicitly walks the 3-type table, names this one "opaque concurrent session," and explains WHY (no `<teammate-message>` sender, no SendMessage address) |
| Claims about SendMessage reachability | **Wrong** — flatly states "it's not a spawned agent you can reach with SendMessage" as if spawned-vs-not were the only axis | **Correct** — checks for a teammate-message sender specifically rather than assuming reachability tracks spawn origin |
| Who a subagent should escalate to | Says "go coordinate with the other terminal directly" (conflates the orchestrating session's action with the subagent's) | Correctly separates: the *subagent* escalates to *its own dispatcher* (no channel to the human); the *dispatcher* then escalates to the human — a sharper distinction than the skill's own text spells out, a good sign the framework transfers rather than being rotely repeated |
| Independent verification named | Yes (`git status`/`git diff`) | Yes, plus explicitly "not trust the subagent's characterization at face value" |

Assertion 2 (stop → verify → escalate, never trusting self-report) — **demonstrated, and measurably
sharper than the baseline's own attempt at the same sequence**, which is the strongest evidence in
this check that the skill earns its capability-uplift classification rather than restating
something the model already does correctly.

## Net

2 of 3 prompts captured cleanly and show a real, measurable delta on assertions 1, 2, and 4. Prompt
1's capture accident is disclosed rather than hidden, and it earned a real fix (the CLAUDE.md
one-line-pointer requirement) that the clean captures couldn't have surfaced on their own.
