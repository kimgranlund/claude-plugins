# The two-phase model — blind first, deliberation second

## The order is load-bearing, not a style choice

**Phase 1 — blind.** Every critic reads the artifact and context cold, independently, with no
visibility into any peer's take (`blind-fanout-mechanics.md`). **Phase 2 — deliberation.** Critics
receive the ANONYMIZED phase-1 finding set and cross-examine, defend, or ideate against it,
moderated by a Chair. The order never reverses, and phase 1's independence is never partially
compromised (a critic getting an early peek "just this once") because the entire value of phase 2
depends on phase 1 having actually been blind:

- **Anchoring resistance.** A critic who sees another's read before forming their own tends to
  drift toward it, consciously or not — the second critic's finding stops being an independent
  signal and starts being a weighted echo. Convergence (`synthesis-shapes.md`'s highest-confidence
  signal) is only meaningful if the critics who converged did so without having compared notes.
- **Groupthink resistance.** A panel that deliberates from the start tends to settle on the most
  socially confident voice's framing rather than surfacing the full spread of independent lenses.
  Blind-first guarantees the full spread exists BEFORE any social dynamic can narrow it — phase 2
  then interrogates that spread rather than starting from a pre-narrowed one.

A council that runs deliberation-shaped critique from the start (critics conferring as they go) is
not a two-phase council with the phases collapsed — it has given up the anchoring/groupthink
resistance the two-phase model exists to buy, and its convergence findings can no longer be read
as independent.

## Phase 2's own contract

Deliberation is not a second blind pass — the anonymized phase-1 finding set is shared context
every participating critic now sees, and a critic's phase-2 job (see the domain critic-shell's own
deliberation-round extension) is to respond to it: cross-examine a peer's finding, defend its own
against a peer's challenge, or propose a joint finding two lenses converge on once they can compare
notes. **Anonymized** means the finding set names the CLAIM, not the critic — deliberation is about
the substance of a finding, not a critic defending their reputation against a named peer.

## The Chair: orchestrates, never judges

Phase 2 is moderated by a **Chair** — a strict router/moderator seat, patterned on
`teamwork:fleet-marshal`'s own contract (a named mention in prose, never a cross-plugin preload or
`${CLAUDE_PLUGIN_ROOT}` path across plugins; the pattern is borrowed, the implementation is local
to whatever plugin hosts the council). The Chair:

- Routes the anonymized phase-1 finding set to each participating critic.
- Collects each critic's deliberation-round response.
- Rolls up the collected responses (revisions with stated cause, joint findings, unresolved
  cross-examinations) for the orchestrating procedure's own final synthesis.
- **Never** judges an artifact itself, never revises a critic's severity on its own authority, and
  never casts a vote in the 2-of-3 sense (`severity-and-voting.md`) — those stay the critics' own.

## The hard mechanics constraint — why the Chair's collection channel is load-bearing

**Named agent dispatches strand their reports at the root session.** A further-nested dispatch
made from inside an already-dispatched seat — the Chair dispatching each critic for its
deliberation-round response is exactly this shape — completes to the ROOT session when it is
NAMED (teammate/mailbox mode), never back to the Chair that dispatched it. The callback
structurally never arrives; the Chair stalls waiting on a report that is never coming back to it.
This is not a hypothetical: it is the same finding `teamwork:dispatch-ticket`'s own no-nested-wait
section documents for build dispatches, and it bit this exact council-generalization work as a live
incident before this pack was written.

**The fix, mechanically:** the Chair collects every deliberation contribution through dispatches
whose results return to the Chair itself — unnamed, synchronous `Agent`-tool calls (the same shape
`blind-fanout-mechanics.md` already uses for phase 1), or an explicit collection protocol the
orchestrating procedure states up front (e.g., each critic's response landing in a shared record
the Chair reads back, rather than being pushed to the Chair by name). **Never** rely on a named
teammate's own completion routing to deliver a deliberation-round response to the Chair — that
channel does not deliver to the Chair at all, it delivers to whatever session happens to be root.

## The Project single-context degraded mode

At the corpus-resolution ladder's Project rung — no `Agent` tool, no filesystem, a single
continuous context (the same run-mode convention every brand-design procedure declares per S2's
portability work) — neither phase can dispatch anything. Both phases run as **sequential persona
simulation**: the model embodies each persona in turn, in-context, producing that persona's blind
read before moving to the next (never letting an earlier persona's simulated read leak into a
later one's — the same independence requirement, honored by discipline instead of dispatch
isolation). The Chair, in this mode, is **an in-context role** rather than a dispatched agent: the
model narrates the routing/collection/roll-up steps itself, disclosed as the degraded substitute
for a real Chair dispatch, never presented as equivalent. A council instance's own procedure states
which rung it is running at explicitly (never inferred from a transient tool-call failure, which is
a failure branch, not a mode switch) — the same discipline `make-brand-guidelines`' own Run modes
section already established for this plugin's Project-mode declarations.
