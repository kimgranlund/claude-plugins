---
name: find-open-questions
description: >-
  Clears a session's backlog of unresolved items — an open question, unconfirmed assumption, or
  undecided idea — into one batched AskUserQuestion round. Use for "anything still open", "still
  pending", "close this out", "loose ends", or "left hanging"; fires at a natural close, never
  unattended. NOT pre-task ambiguity (find-intent); NOT sweeping the session's dropped work into
  tickets (docs' file-leftovers); NOT worktree state before session end (close-session).
disable-model-invocation: false
user-invocable: true
---

# find-open-questions

find-open-questions clears a session's backlog of unresolved items in one round, replacing the
prose list nobody actually resolves.

## Procedure
1. Scan the conversation for items that are still genuinely open: an unanswered question, an
   assumption stated but left unconfirmed, a stray idea floated in passing that stayed a maybe
   instead of a decision. Ground every item in something actually raised earlier in this session
   — a speculative "would this be useful" idea with no prior mention stays out of scope.
2. Nothing qualifies → report "nothing open" in one line and stop there. A clean session earns
   that line, not a manufactured question.
3. Turn every qualifying item into ONE AskUserQuestion call: 1-4 questions, 2-4 options each. An
   item with a working assumption behind it (the default it shipped with, the lean it was heading
   toward) lists that option first, marked recommended; a stray idea with no assumption ever
   stated lists its options unranked — inventing one to satisfy the marking misrepresents a real
   lean that was never there. One call covers every item — a question-per-turn or a prose
   paragraph both fall short of the contract.
4. The reply after the user answers resolves each item by name — the decision, the insight, or
   the next step — earning more than a bare acknowledgment.

## Output contract
One AskUserQuestion call carrying every qualifying item, or (step 2) a single "nothing open"
line — the two outcomes are exclusive; a prose list satisfies neither.

## Failure branches
- Dispatched in an unattended or scheduled context (a cloud-routine firing, a subagent with no
  interactive user on the other end) → skip auto-fire entirely, even with qualifying items on
  hand; an AskUserQuestion round nobody can answer just hangs the firing. User-invocation is
  unaffected — this only guards the on-its-own trigger.
- More than 4 items qualify → batch the 4 most consequential (most likely to change what happens
  next); name the remainder in the batch's own framing text ("N more minor items — ask again to
  cover those"), keeping the surplus visible instead of dropped.
- An item already went stale — the code or decision moved past it — drops from the batch: asking
  about a settled decision spends the user's answer on nothing.
- The user skips or declines the round (picks "Other" with a dismissal, or answers "later") →
  stop there; the reply resolves nothing further and the same batch stays unasked for the rest of
  the session.

Done when every qualifying item has been asked about in that one call and answered, the skill
reported "nothing open" and stopped there, or the user declined the round per the failure branch
above — each a valid terminal state; a decline is not re-asked later in the same session.

## Example
Good (one batched call, options that instantiate the real choices):
```
AskUserQuestion(questions: [
  { question: "Should the new endpoint require auth?",
    options: ["Require auth (recommended — matches what shipped)", "Leave it public", "Other"] },
  { question: "Add tests for the new endpoint now?",
    options: ["Full coverage (recommended)", "Happy-path only", "Skip for now", "Other"] }
])
```

Bad (counter-example — do not imitate): "Also, I was unsure about the config loader, and there's
the rate-limiting idea, and did you want tests too? Let me know what you think" — one open-ended
lump standing in for a batch of concrete choices.
