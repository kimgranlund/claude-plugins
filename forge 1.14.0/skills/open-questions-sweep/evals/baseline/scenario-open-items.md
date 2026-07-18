# Baseline — session with 4 unresolved items, no skill

Prompt (fresh session, skill unavailable): synthetic session log with 4 unanswered/unsurfaced
items (endpoint auth default, config-loader env-vs-file assumption, a rate-limiting aside, an
unanswered tests-scope question), closed with "Before we wrap up, is there anything still open?"

## Output

Yes, a few things I flagged along the way but never actually got closed out:

1. **Auth on the new endpoint** — I asked whether it should require auth or be public and never
   got a real answer, so I defaulted to requiring auth. Worth confirming that's actually correct
   before this ships.
2. **Config loader: env vars vs. config file** — I made a unilateral call to read from env vars
   for now. That was an assumption on my part, not a confirmed decision — worth double-checking
   it's what you want.
3. **Rate limiting** — I mentioned in passing that we might want it on the new endpoint at some
   point, but never turned that into an actual decision. Currently there's none. Fine to punt,
   just flagging it's not tracked anywhere.
4. **Test coverage for the new endpoint** — I asked whether you wanted full tests or just the
   happy-path, and never got an answer back. Right now I don't think I've added tests for it at
   all (only the happy path is implicitly covered by manual runs, if that). This is probably the
   one most worth deciding before we stop.

Want to knock these out now, or should I just leave notes (e.g. TODOs / a follow-up issue) so
they're not lost?

## Gap this skill closes

Correctly finds and enumerates all 4 items — the recall isn't the gap. The delta: it stops at a
prose dump plus one open-ended follow-up ("want to knock these out now?") instead of resolving
them — each item still needs a second round-trip, and nothing forces concrete, pickable options
per item. `open-questions-sweep` converts this into ONE AskUserQuestion call, each item as its
own question with 2-4 concrete options (recommended option marked), so the user answers once and
every item is actually closed instead of re-opened as a follow-up question.
