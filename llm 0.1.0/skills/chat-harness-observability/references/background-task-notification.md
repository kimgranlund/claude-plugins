# Background-task notification — never poll for what the harness already tracks

> Axis: how a chat-agent harness tells a caller that background work is done, and the different
> mechanism for the genuinely separate case of waiting on external state the harness cannot track
> automatically. Grounded in this harness's own verified tool mechanics (a platform fact).

## The core rule — if the harness dispatched it, the harness will tell you; do not poll

**Platform fact (this harness, verified directly from this session's own tool instructions):** an
agent dispatched to run in the background does not require the caller to poll for completion —
when the background work finishes (success or failure), a notification is delivered automatically
to the caller's context, carrying status and a pointer to the output. The harness's own governing
instruction states this as an explicit anti-pattern to avoid: *"Do NOT sleep, poll, or proactively
check on its progress... you will be automatically notified when it completes."* **Failure mode
this prevents:** a caller that sleep-loops or repeatedly re-checks a background task it was
already going to be notified about wastes turns/tokens re-deriving information the harness is
already going to hand it for free, and risks racing its own polling against the real completion
event (checking right before the notification lands, then checking again right after, having
learned nothing new either time).

**Distinguish trigger from mechanism, not just outcome:** the notification is not something the
caller requests per-task — it is a property of *how the work was dispatched* (as a trackable
background unit), delivered automatically the moment that unit's state changes to "done," success
or failure alike. A caller's job is to keep working on something else and let the notification
interrupt it, not to design its own completion-detection loop for work the harness is already
watching.

## The genuinely different case — state the harness cannot track by itself

**Claim — this is NOT the same problem as watching a truly external system** (a CI run on a
remote server, a deploy pipeline, a log file being written by a separate process) that the harness
has no built-in hook into. For that case, this harness's own tooling documents a **different**,
explicitly poll-based mechanism, with cadence guidance baked into its own description — **verified
directly from this session's own Monitor tool documentation:**

- A **poll loop for genuinely external state** (the tool's own worked example is literally "poll
  GitHub for new PR comments") is expected to run on a cadence matched to how fast that state
  actually changes — the tool's own guidance states it explicitly: *"Poll intervals: 30s+ for
  remote APIs (rate limits), 0.5-1s for local checks."* This is the opposite instinct from the
  background-task case above: here, *some* polling is the correct and only available mechanism,
  because there is no automatic "it's done" signal the harness can hook into for a system outside
  its own dispatch tracking.
- A THIRD, distinct mechanism exists for pure time-based scheduling — a `schedule` capability this
  session's own menu describes as creating/running "scheduled cloud agents (routines) that execute
  on a cron schedule," explicitly covering "a one-time scheduled run ('run this once at 3pm',
  'remind me tomorrow')" — for asks shaped like "check on this again in an hour," which is a
  *scheduling* primitive keyed to wall-clock time, not a state-watching one. (A fourth,
  narrower mechanism — a wakeup scheduler for a `/loop`'s own self-pacing between iterations of one
  standing task — is a related but genuinely distinct case: it resumes THIS session's own recurring
  work, not an arbitrary future prompt; naming it here would overreach what this pack verified.)

**Why the contrast is the whole point:** the failure mode is picking the wrong one of these two —
either polling for something the harness was always going to announce on its own (wasted effort,
possible race), or assuming a truly external system will announce itself the way a harness-tracked
background task does (silent, indefinite wait, because nothing external is wired to notify
anyone). The question to ask before choosing: **did I dispatch this as trackable background work
myself, or is the state I'm waiting on owned by a system outside the harness's own tracking?** The
former never polls; the latter always does, at a deliberately chosen cadence.

## A note on portability — the exact tool names are this harness's, the shape generalizes

**Caveat, stated once so it need not be repeated per-claim:** the specific tool names cited above
belong to this session's own harness surface and can rename or reshape across harness versions —
verify against the current tool list if this pack has aged. The **shape** that should survive any
such rename is the two-mechanism split itself: one automatic-notification path for work the
harness dispatched and tracks natively, and one deliberately-paced polling path for state owned by
something outside the harness — collapsing these into a single "just poll for everything" habit is
the anti-pattern this file exists to name, regardless of what either mechanism happens to be
called in a given harness version.

## What this file does NOT cover

Deterministic per-event logging of a synchronous tool call, a different signal from an
async task's completion (logging-and-tracing) · measuring whether a skill's routing is accurate
over time (routing-accuracy-evals) · the provenance split between this harness's own verified
mechanics and anything else (sources).
