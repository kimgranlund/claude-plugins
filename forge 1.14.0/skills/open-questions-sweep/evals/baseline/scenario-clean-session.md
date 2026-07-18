# Baseline — clean session, nothing open, no skill

Prompt (fresh session, skill unavailable): synthetic session log with two fully-resolved tasks
(a rename, a docstring), no unanswered questions, closed with "Before we wrap up, is there
anything still open?"

## Output

Nope — both done. The rename compiled clean and the docstring matches the existing style.
Nothing pending on my end.

## Gap this skill closes

None — this is the negative control. Restraint on a clean session already holds without the
skill; `open-questions-sweep` must not regress this (assertion 4: decline to fire rather than
manufacture filler questions).
