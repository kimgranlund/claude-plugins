# Task Prompts

Use these prompts for qualitative review of the skill. They are meant to test whether the skill
gives the right kind of answer, not whether it produces one rigid output.

Slice of the pre-split `task-prompts.md` (prompts 1 and 6 — the two whose "good answer" criteria
are owned by this pack). The source file lived at `color-science-project-files/evals/task-prompts.md`
until T6 removed it once every prompt had landed in a pack (2026-07-06, A2); the full 8-prompt set
with its original numbering is in git history: `git show af81c64:skills/color-science/evals/task-prompts.md`.

## What to look for

- Does the answer pick the right conceptual frame quickly?
- Does it distinguish standards, heuristics, and implementation reality?
- Does it avoid shallow wheel-theory advice when a stronger explanation exists?
- Does it recommend tools and references that fit the actual task?
- Does it stay concise unless the task really needs deeper theory?

## Prompts

### 1. UI ramps and accessibility

"I need a semantic color system for a data-heavy app. We want success, warning, danger, info, and
neutral scales with light and dark themes. Please recommend a practical color-space workflow, how
to keep the ramps perceptually even, and how to think about accessible foreground colors."

Good answer:

- pushes toward OKLCH or a similarly defensible working space
- distinguishes palette tokens from semantic tokens
- treats contrast as something to verify, not eyeball
- avoids pretending hue harmony alone solves readability

### 6. CSS color support question

"Can I rely on `contrast-color()` and `device-cmyk()` in production CSS today, or are those still
more spec than reality?"

Good answer:

- distinguishes specification from shipped browser support
- uses the CSS Color references without overclaiming implementation status
- stays grounded in practical deployment advice
