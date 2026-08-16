# Cold-start adoption — the north-star loop at turn zero

Source: this workspace's own ruling (Kim, 2026-08-16, issue #404) — not from the bible; kept as
its own file rather than folded into `knowledge-base-habits.md` so that file's bible-sourced
`[verified]` provenance stays uncontaminated by a non-bible addition.

## Why this is a first-class branch, not an edge case

Adopting the product seat onto a project with no existing intent layer (no product brief, no
IDRs, no roadmap) is the north-star loop running at turn zero — likely the MOST common entry
point (most projects a seat is bootstrapped onto are legacy: code and history exist, intent
records don't). Treating it as an error, or silently skipping straight to priority work, both
lose the loop-authority question this seat exists to answer.

## The four-step flow

1. **Harvest candidate intent** from what already exists — founding docs, README, existing ADRs
   (an orphan ADR often implies the IDR it should have cited but never got one — reverse-engineer
   it), commit and issue history, and a structured conversation with whoever is present. Three
   passes, in order: an intake interview to surface candidate claims, a stress-test pass to
   pressure-test each one before it's written down, then a captured artifact that records the
   result — a repo wires these to its own named tools (this workspace: `harness:find-intent` →
   `teamwork:grill-the-ask` → `docs:make-vision-memo`).
2. **Propose a DRAFT, not a decision.** A draft product brief plus draft IDRs, each passing the
   admission test (`references/alignment-record-types.md`), each explicitly provenance-marked:
   - `derived-from-evidence` — cite the source (a file, a commit, a conversation).
   - `inferred` — a plausible reading that needs human confirmation before it's load-bearing.
   - `gap` — a genuine open question, marked as one rather than silently guessed at.
3. **One batched human ratification round.** The seat proposes; it never adopts intent on its own
   authority. A single round, not a drip of individual confirmations — batch every draft item so
   the human DRI reviews the whole candidate intent layer once and owns the result.
4. **Close day 0 with homes, not content.** The maturation arc's own first stage
   (`knowledge-base-habits.md` — "born as homes") applies here literally: day 0 done means the
   doc SHELLS exist (a brief, a roadmap index, the ratified draft IDRs promoted to real ones) —
   not that every fact is filled in. Content accumulates by harvest afterward, same as any other
   knowledge base.

## Two guardrails

- **Thin-brief anti-big-bang.** The day-0 output is a THIN brief and a FEW IDRs — exactly the ones
  the harvest surfaced with real evidence or a real open question — never an attempt to
  pre-populate a complete intent layer from inference alone. A large draft on day 0 is the
  big-bang-knowledge-base anti-pattern wearing a different day.
- **Hypothesis phrasing for derived intent.** An `inferred` item is written as a hypothesis about
  the past — "the codebase behaves as if X; confirm or supersede" — with its evidence cited,
  never asserted as if it were an already-ratified decision. The ratification round in step 3 is
  what actually promotes it; the draft's own wording must not pre-empt that.
