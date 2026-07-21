# Task Prompts

Slice of `color-science-project-files/evals/task-prompts.md` (prompts 7 and 8 — this pack's per
§2 spec). Use these prompts for qualitative review of the skill. They are meant to test whether the
skill gives the right kind of answer, not whether it produces one rigid output.

## What to look for

- Does the answer pick the right conceptual frame quickly?
- Does it distinguish standards, heuristics, and implementation reality?
- Does it avoid shallow wheel-theory advice when a stronger explanation exists?
- Does it recommend tools and references that fit the actual task?
- Does it stay concise unless the task really needs deeper theory?

## Prompts

### 7. Perceptual terminology

"Please explain brightness, lightness, saturation, chroma, and colorfulness without sounding like a
textbook. I need to paste it into internal design docs."

Good answer:

- uses plain English without collapsing the terms into synonyms
- stays accurate enough to support later technical work
- does not drift into hand-wavy 'vibes' language

### 8. Image compression and vision

"Why does JPEG throw away so much color information before people notice? I want the answer in a
way frontend devs will actually remember."

Good answer:

- connects YCbCr and chroma subsampling to human vision clearly
- avoids explaining compression as if color simply matters less than brightness in every context
- keeps the explanation practical and memorable
