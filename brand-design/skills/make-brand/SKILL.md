---
name: make-brand
description: >-
  Runs a collaborative Build-mode brand engagement across research, strategy, identity, and voice
  — partner posture, not vendor. Locates the real pipeline stage, blocks expression work (color,
  type, logo, naming) before strategy is grounded, and names an aspiration before the work
  converges, then hands the method to brand-methodology-rules. Use when the user wants to build,
  develop, or work on a brand's strategy, positioning, identity, or voice — "let's build this
  brand", "work on the brand strategy", "develop the identity or voice". NOT the guided 2x2
  elicitation loop (make-brand-guidelines), the one-page brand-stack summary (make-brand-stack), or
  adversarial scoring (check-brand-rubric).
disable-model-invocation: false
user-invocable: true
argument-hint: "[what you're working on]"
---

# make-brand — Build mode

Build mode is the collaborative brand engagement — research, strategy, expression, or
stewardship — run as a partner, not a vendor: think alongside the user, ask the sharp question,
make real work. Not a grading pass — that's `check-brand-rubric`.

Working on: `$ARGUMENTS`

## Procedure

1. **Locate the stage.** Brand work runs `research → strategy → expression → stewardship`. From
   what the user says, classify the stage they're actually in — not where they think they are —
   and name it back in one line.
2. **Guard the order.** If the ask reaches for expression (color, type, logo, naming, visual
   identity) while strategy isn't grounded (no positioning, no cultural provenance, no point of
   view), stop and flag it: identity built on ungrounded strategy is decoration, and it will not
   survive `check-brand-rubric` or `check-brand-council`. Offer to ground the strategy first, or
   proceed with the caveat on the record — never silently comply.
3. **Name the pull before converging (soft gate).** State at least one sentence of direction the
   work reaches for; it will evolve. Resolve prior brand material via `brand-corpus`'s
   corpus-resolution ladder (cited, not restated) first and extend it rather than reinvent it. No
   aspiration stated, or the first idea
   is already hardening into "the" answer → set a provisional pull, or invoke `make-brand-muse`
   first. Clearing this gate means naming a direction, not stopping.
4. **Run the methodology.** Invoke the `brand-methodology-rules` skill and run the stage it names
   — it owns the method; this skill sets posture, routes, and keeps the work honest. For extended
   voice work (a full voice platform, a naming set, a long copy run), hand off to the
   `brand-writer` agent (an isolated maker context for sustained single-voice work) via the Agent
   tool; brief tactical copy (a headline, a tone check) stays in this session.
5. **Lint before presenting a draft.** Once written material exists (strategy doc, expression
   spec, voice sample), run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_lint.py" <file>...`
   before showing it to the user. Advisory only — a clean run says "no structural tells," never
   "this brand is good" — surface any findings (archetype language, the VMV template, personas,
   brand-DNA word-clouds, values with no trade-off) alongside the draft rather than silently.
6. **Point at the next seat.** When the work exists and a hostile read is wanted, point the user
   at `check-brand-rubric` or `check-brand-council`. Keep the seats distinct — the Muse
   (`make-brand-muse`) sets the pull, this skill makes, the council reviews — no seat judges its
   own work.

## Run modes

**Full** (Claude Code / Cowork) — the whole procedure: `brand_lint.py` in step 5, and an Agent-tool
handoff to the `brand-writer` agent for extended voice work in step 4. **Project single-context**
— no bundled scripts, no Agent tool: corpus state resolves via `brand-corpus`'s corpus-resolution
ladder (cited, not restated) at its Project-knowledge rung; step 5's lint is skipped and disclosed
as such (never silently); extended voice work that would hand off to `brand-writer` stays
in-session instead, named as the degraded single-context substitute, not a second implementation.

## Failure branches

- No rung of the corpus-resolution ladder reaches material → say so, proceed from what the user
  states directly.
- User insists on expression with no strategy after the flag → proceed, but the caveat goes into
  the record (a note in the response), never silently.

## Done / NOT done

Done when the stage is named, the order gate has been checked (cleared or flagged), a pull is at
least provisionally named, the methodology skill has been invoked for the classified stage, and
the response states the stage, the gate verdict, the pull, and (Full mode) whether lint findings
surfaced. NOT done if expression work started with an unflagged missing strategy, or the
methodology handoff was skipped in favor of freelancing the method here.
