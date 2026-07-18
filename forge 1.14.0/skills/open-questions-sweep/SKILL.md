---
name: open-questions-sweep
description: >-
  Clears a session's backlog of unresolved items — an unanswered question, an unconfirmed
  assumption, a stray idea floated but left undecided — into one batched AskUserQuestion round
  instead of a prose dump nobody actually resolves. Use when the user asks "before we wrap up, is
  there anything still open", "anything still pending", "any decisions still open before we
  close this out", or "wrap up any loose ends"; also fires on its own at a natural closing point
  in a long session where items like this have piled up. NOT for resolving ambiguity before
  starting a task (intent-extract); NOT for a scheduled/interval reminder (loop-design / `/loop`);
  NOT for querying, tracking, or filing work items in an external tracker (ops-issues); NOT for
  producing a persisted decision record or ticket afterward (a separate, heavier ask).
disable-model-invocation: false
user-invocable: true
---

# open-questions-sweep

open-questions-sweep clears a session's backlog of unresolved items in one round, replacing the
prose list nobody actually resolves.

## Procedure
1. Scan the conversation for items that are still genuinely open: an unanswered question, an
   assumption stated but left unconfirmed, a stray idea floated in passing that stayed a maybe
   instead of a decision. Ground every item in something actually raised earlier in this session
   — a speculative "would this be useful" idea with no prior mention stays out of scope.
2. Nothing qualifies → report "nothing open" in one line and stop there. A clean session earns
   that line, not a manufactured question.
3. Turn every qualifying item into ONE AskUserQuestion call: 1-4 questions, 2-4 options each, the
   option matching the working assumption listed first and marked recommended. One call covers
   every item — a question-per-turn or a prose paragraph both fall short of the contract.
4. The reply after the user answers resolves each item by name — the decision, the insight, or
   the next step — earning more than a bare acknowledgment.

## Output contract
One AskUserQuestion call carrying every qualifying item, or (step 2) a single "nothing open"
line — the two outcomes are exclusive; a prose list satisfies neither.

## Failure branches
- More than 4 items qualify → batch the 4 most consequential (most likely to change what happens
  next); name the remainder in the batch's own framing text ("N more minor items — ask again to
  cover those"), keeping the surplus visible instead of dropped.
- An item already went stale — the code or decision moved past it — drops from the batch: asking
  about a settled decision spends the user's answer on nothing.
- The user skips or declines the round (picks "Other" with a dismissal, or answers "later") →
  stop there; the reply resolves nothing further and the same batch stays unasked for the rest of
  the session.

Done when every qualifying item has been asked about in that one call and answered, or the skill
reported "nothing open" and stopped there.

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
