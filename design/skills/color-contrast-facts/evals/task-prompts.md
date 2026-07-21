# Task Prompts

Slice of the original `color-science` (now `color-science-project-files`) eval set relevant to
`color-contrast-facts` — the boundary-routing prompt (task 5 of the original 8). See
`color-science-project-files/evals/task-prompts.md` for prior history / the full original set.

## What to look for

- Does the answer pick the right conceptual frame quickly?
- Does it distinguish standards, heuristics, and implementation reality?
- Does it recommend tools and references that fit the actual task?
- Does it stay concise unless the task really needs deeper theory?

## Prompts

### 5. Harmony advice under pressure (boundary-routing check)

"My teammate keeps insisting we should use a triadic palette because that's 'good color theory'. I
need a better argument for choosing a calmer, more legible palette for a dashboard."

Good answer (since the 2026-07-02 split, the harmony corpus lives in the `color-theory-facts` pack; this
is the accessibility half of a two-pack answer):

- answers the *legibility* half here — lightness separation, APCA/WCAG contrast targets
- routes the *harmony/aesthetics* half to `color-theory-facts` rather than improvising wheel talk
- gives a usable alternative rather than only criticizing triads
