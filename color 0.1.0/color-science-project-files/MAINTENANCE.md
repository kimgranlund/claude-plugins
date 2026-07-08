# Maintenance Guide

Use this file when extending or reviewing the skill.

## What Belongs in Each Layer

### `SKILL.md`

Put only the highest-leverage guidance here:

- concepts the agent should reach for repeatedly
- corrections to common misconceptions
- short recommendation tables
- compact tool recommendations
- distinctions that change the answer materially

Keep it concise. If a section starts reading like notes for a lecture, it probably belongs in `references/`.

### `references/`

Put deeper material here:

- source summaries
- transcripts
- detailed implementation notes
- historical context
- library and spec documentation

Each reference should justify its presence by being either authoritative, unusually clarifying, or practically useful.

### `evals/`

Put realistic prompts here for checking two things:

- whether the skill should trigger
- whether it gives the right level and shape of answer

These files are for human review, not rigid benchmarking.

### `src/`

Put working TypeScript color math here. Every module is small, single-purpose, and exports a uniform interface where possible:

- **Color spaces** (`src/spaces/*.ts`) export `toXYZ(c)` and `fromXYZ(c)`. Composition goes through the XYZ_D65 hub — never write direct A→B converters unless there's a real reason. The test suite enforces this invariant.
- **Branded types** (`src/types.ts`) keep different spaces from being silently interchanged. Compile-time only; runtime is plain `[number, number, number]`.
- **Test vectors** in each module document the canonical reference values for the algorithm. New modules must add at least one round-trip test (`toXYZ(fromXYZ(c)) ≈ c`).

### `examples/`

Put **dogfooding demos** here, one per concept. The site is the proof that `src/` actually composes — when a new module lands in `src/`, it earns its keep by appearing in at least one demo here.

- Pages are self-contained HTML files in `examples/pages/`. They load the bundled JS and use `window.RefColor.*`.
- Reusable interactive elements are vanilla custom elements in `examples/lib/js/components/`.
- Add new components to `examples/bundle-entry.js`, add nav entries to `examples/lib/js/shell.js`'s `DEMO_GROUPS`, add a card to `examples/index.html`, and bump the skill version in `skill.json` + add a `CHANGELOG.md` entry.

## Source Quality Bar

Prefer sources in this order when possible:

1. primary papers, standards, official specs, original books
2. authoritative secondary explainers with strong citations
3. high-signal practical resources that correct common mistakes or expose real workflows

Avoid adding a source just because it is popular. Keep it if it adds one of these:

- a concept the skill otherwise lacks
- a better explanation than existing sources
- a practical tool or workflow the skill can recommend
- an important corrective to a widespread misconception

## Keep `SKILL.md` Opinionated, But Defensible

The skill should make choices. It should not flatten everything into "it depends." But recommendations need a reason behind them.

Good:

- recommend OKLCH for perceptual ramps because lightness and chroma behave more predictably than HSL
- recommend CAM16 or CIECAM02 when viewing conditions are part of the problem

Weak:

- list many spaces without telling the agent when each one is the right tool
- repeat folk design advice without a perceptual or workflow reason

## Review Rubric

Use this checklist when reviewing edits:

### 1. Trigger clarity

- Would the frontmatter description catch adjacent real-world color tasks?
- Does it avoid triggering on generic coding or design work that merely mentions color?

### 2. Factual accuracy

- Are the core claims technically defensible?
- Are key distinctions preserved instead of collapsed into simplified but wrong advice?

### 3. Source quality

- Are links stable and reasonably canonical?
- Is the source worth keeping, or is it duplicating weaker material already present?

### 4. Practical usefulness

- Would the guidance help someone make a better decision, not just learn trivia?
- Does it recommend tools, spaces, or references that fit the actual task?

### 5. Scope discipline

- Does the content belong in `SKILL.md`, `references/`, or nowhere?
- Is the top-level skill still a strongest-hits document rather than a dump of everything known?

## Signs of Drift

Watch for these failure modes:

- too much generic design advice and not enough color-specific reasoning
- too much wheel-theory language without perceptual grounding
- recommendations that confuse standards with shipping support
- stale counts or claims that will rot quickly
- duplicate references that add no new angle

## Preferred Update Loop

When making non-trivial edits:

1. update the skill or references
2. scan `evals/trigger-evals.json` and ask whether the new description still triggers in the right places
3. try at least one prompt from `evals/task-prompts.md`
4. fix anything that became misleading, overbroad, or too abstract
