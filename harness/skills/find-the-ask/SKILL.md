---
name: find-the-ask
description: >-
  Extract the ROOT intent behind a task or brief before acting. Use when a request is vague
  or the wording and goal diverge — "what am I really asking for", "figure out what they
  actually want", "clarify this before we build it". Resolve gaps with multiple-choice
  questions. NOT for a new skill's interview (make-skill); NOT decomposing a system
  (break-down-problem); NOT a session's open questions (find-open-questions).
disable-model-invocation: false
user-invocable: true
---

# Intent extraction

Find the goal *under* the words and resolve only the gaps that genuinely change what you'd do — turning
a fuzzy or overloaded request into a precise, executable one.

## When to use / when not

- **Use** before acting on an ambiguous, underspecified, expensive, or hard-to-reverse request — or
  whenever you're asked to clarify intent or sharpen a prompt/brief/spec.
- **Skip** when the request is already unambiguous and low-stakes. Manufacturing questions for a clear
  ask is its own failure: over-clarifying spends the author's attention for nothing.

## Method

1. **Capture the literal ask.** Restate it near-verbatim — the surface form, before interpretation.
2. **Infer the root goal.** One sentence: the *why* — what outcome counts as success, who it's for, what
   they'll do with the result. This is the thing to optimize; the literal ask is just one candidate path
   to it.
3. **Scan for the delta** between ask and goal. Name each signal you find:
   - **Category mismatch** — the requested *form/unit* is wrong for the goal (e.g. "make a skill" for
     what is really reference knowledge; "build an agent" for a deterministic check).
   - **Ambiguity** — a term, scope, or referent readable two ways.
   - **Conflict** — two goals that can't both be maximized, or an instruction fighting a constraint.
   - **Unstated assumption** — a "should" with no owner; a dependency or default taken for granted.
   - **Missing acceptance** — no definition of done / no success signal.
   - **Hidden scope** — no non-goals; the unbounded "…and also".
4. **Sort the delta into Resolve vs. Ask.**
   - **Resolve silently** anything inferable from the artifact, surrounding context, or a conventional
     default — and *state the assumption* so it's correctable.
   - **Ask only** what genuinely changes what you'd do AND can't be defaulted. The bar is "their answer
     changes the output," not "I'm slightly unsure."
5. **Ask in one batched round** (discipline below) — never drip questions across turns.
6. **Synthesize** the Resolved Intent (output contract below).
7. **Validate, then finalize** (validation loop below) — do not deliver until it passes.

## Multiple-choice discipline — make it effortless for the author

Present clarifications as multiple-choice, not open prompts. Use the **AskUserQuestion** tool.

- **Batch everything** into one round of **1–4 questions**, **2–4 concrete options** each.
- **Lead with the option you'd recommend**, marked "(recommended)". An "Other" escape is always present,
  so never add one yourself.
- Give each question a **header chip (≤ 4 words)** and phrase options so the author **picks, not writes**.
- When an option is a concrete artifact (a layout, an approach, a structure), include a **preview (≤ 2
  lines or one fenced snippet)** so the author compares at a glance.
- **Pre-resolve everything defaultable and show the assumption** — only the load-bearing forks reach the
  author.

## Output contract — the "Resolved Intent"

```
ROOT GOAL   — one sentence: the why / what success looks like.
LITERAL ASK — what was said, near-verbatim.
DELTAS      — each ambiguity / conflict / category-mismatch / assumption found; for each you resolved
              by default, the assumption you made.
OPEN        — the multiple-choice questions, if any genuinely remain (else omit).
SHARPENED   — the 10x restatement: what to actually do, scoped (incl. non-goals), with the success
              criterion — ready to execute or hand to another agent.
```

## Validation loop (finalize only when clean)

Before delivering, check the draft against the source and fix what fails — re-check until all pass:

- **Goal test** — if SHARPENED were executed exactly, would it produce ROOT GOAL? If not, the goal is
  mis-stated or the restatement drifted → fix.
- **Coverage test** — is every DELTA either resolved (with a stated assumption) or in OPEN? A dropped
  ambiguity resurfaces downstream → fix.
- **Necessity test** — would each OPEN question's answer actually change the output? If not, default it
  and remove it → fix.
- **Grounding test** — is every inferred goal/assumption traceable to the text, the context, or a named
  convention — not invented? If not, downgrade it to an OPEN question → fix.

If no genuine ambiguity survives step 4, omit OPEN and deliver SHARPENED directly — extraction *without*
interrogation is the ideal outcome, not a skipped step.

The delivered read-back is the critic seat, filled by the consumer: presenting the Resolved Intent for
correction *is* the requester ratifying the extraction — generator ≠ critic, and the person whose intent
it is holds the verdict, never the extractor.

**Done** = all four validation tests pass and the requester has seen the read-back (ratified it, or every
default stands stated and correctable); **NOT done** = a delta that is neither resolved-with-assumption
nor in OPEN, an OPEN question whose answer wouldn't change the output, an inference that traces to
nothing, or a SHARPENED the extractor certified alone.

## Worked example

> **Ask:** "create a few skills or agents based on these three design docs."
>
> **ROOT GOAL** — operationalize the design standards in those docs into reusable, enforceable agent
> capabilities, so the rules get applied consistently as work is built.
> **DELTAS** — *Category mismatch:* the docs are referential knowledge, not procedures — "skill" is the
> wrong unit for most of it (→ references + a deterministic check + one skill). *Ambiguity:* "a few" and
> "skills **or** agents" — count and unit unspecified. *Assumption (resolved):* they want to feed the
> existing tooling, not invent parallel capabilities (stated, correctable).
> **OPEN** — one AskUserQuestion: *"Which unit for the enforceable parts?"* → (recommended) deterministic
> probe · a reviewing agent · fold into the author skill.
> **SHARPENED** — "Distill the docs into one reference; route the arithmetic rules to a probe; fold the
> application method into the existing author skill; defer the steward agent until there's something to
> steward" — scoped, with non-goals, ready to execute.

## References & tools

| Path | Use when |
|---|---|
| `AskUserQuestion` | The one batched round — closed multiple-choice forks |
| `references/foundations.md` | The models behind literal-vs-speaker meaning, the XY problem, the delta taxonomy |
| `references/best-practices.md` | The do/don't — resolve-vs-ask, closed-question design, techniques worth stealing |
| `references/rubric.md` | Score a Resolved Intent (the skill's output) |

A Resolved Intent is write-once: on a changed ask, **re-run the extraction** — never patch the old
contract, whose deltas and defaults were resolved against wording that no longer exists.
