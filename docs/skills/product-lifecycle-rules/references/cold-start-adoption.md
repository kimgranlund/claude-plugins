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

## The flow: orient → harvest → draft → review → ratify

This is the ONLY cold-start flow — not a fallback for when some other plugin is absent. Every
step below runs with tools this workspace already owns; nothing here is conditioned on any other
plugin being installed (2026-08-16 supersession note on issue #404: an earlier revision of this
file soft-mentioned a separate marketplace plugin, `product-forge`, as an alternate path for
steps 1, 2, and 4 — Kim ruled that out entirely, not even as a soft mention, and this file was
rewritten to the single native flow below; issue #411).

1. **Orient.** Establish what's already known about the domain/market and this specific codebase
   before harvesting — read founding docs, README, existing ADRs, and recent commit/issue history
   to form a working classification of what kind of project this is and what shape its intent
   layer should take, before the harvest pass below goes looking for specifics.
2. **Harvest candidate intent** from what already exists — founding docs, README, existing ADRs
   (an orphan ADR often implies the IDR it should have cited but never got one — reverse-engineer
   it), commit and issue history, and a structured conversation with whoever is present. Three
   passes, in order: an intake interview to surface candidate claims (`harness:find-intent`), a
   stress-test pass to pressure-test each one before it's written down
   (`teamwork:grill-the-ask`), then a captured artifact that records the result
   (`docs:make-vision-memo`).
3. **Draft, not a decision.** A draft product brief plus draft IDRs, each passing the
   admission test (`references/alignment-record-types.md`), each explicitly provenance-marked:
   - `derived-from-evidence` — cite the source (a file, a commit, a conversation).
   - `inferred` — a plausible reading that needs human confirmation before it's load-bearing.
   - `gap` — a genuine open question, marked as one rather than silently guessed at.
4. **Review — generator≠critic on the draft, before it ever reaches the human.** Dispatch
   `docs:doc-checker`, fresh-context, against the draft brief and each draft IDR — at minimum one
   pass per document, run in parallel isolated dispatches so no pass anchors on another's
   read. Each pass grades its document against `doc-writing-rules`' own type contract (the
   admission test, unfalsifiable claims, missing non-goals, a broken ID spine) and returns
   severity-classified findings. Synthesize across the returned passes before ratification:
   - **Convergence** — a gap or defect more than one pass independently flagged (the strongest
     signal something is genuinely wrong, not one checker's idiosyncrasy).
   - **Highest severity** — the single biggest risk to the intent layer, named first.
   - **The blind spot** — provenance a `derived-from-evidence` item claims but no pass actually
     verified against the cited source; an `inferred` item whose hypothesis phrasing (guardrail
     below) slipped into asserted-fact language.
   A review that returns nothing on a thin, evidence-light draft has not actually looked — widen
   what's under review (more IDRs, the brief's open questions) rather than accepting a clean pass
   at face value.
5. **One batched human ratification round.** The seat proposes; it never adopts intent on its own
   authority. A single round, not a drip of individual confirmations — batch every draft item,
   with the review synthesis attached, so the human DRI reviews the whole candidate intent layer
   plus its critique once and owns the result. Close day 0 with homes, not content: the
   maturation arc's own first stage (`knowledge-base-habits.md` — "born as homes") applies
   literally — the doc SHELLS exist (a brief, a roadmap index, the ratified draft IDRs promoted
   to real ones), not every fact filled in; content accumulates by harvest afterward.

## Two guardrails

- **Thin-brief anti-big-bang.** The day-0 output is a THIN brief and a FEW IDRs — exactly the ones
  the harvest surfaced with real evidence or a real open question — never an attempt to
  pre-populate a complete intent layer from inference alone. A large draft on day 0 is the
  big-bang-knowledge-base anti-pattern wearing a different day.
- **Hypothesis phrasing for derived intent.** An `inferred` item is written as a hypothesis about
  the past — "the codebase behaves as if X; confirm or supersede" — with its evidence cited,
  never asserted as if it were an already-ratified decision. The ratification round in step 5 is
  what actually promotes it; the draft's own wording must not pre-empt that.

## Prior art (study pass, 2026-08-16, issue #411)

Step 4's convergence/highest-severity/blind-spot synthesis shape is adapted, with provenance and
a native rewrite, from a pattern observed in `product-forge` (a separate, unrelated marketplace
plugin, `kimgranlund/nonoun-plugins` — read as a study source only, never a runtime dependency):
its `product-council` agent fans out multiple isolated critic
passes over one artifact and synthesizes them across four axes (convergence, highest severity, a
named tension, a blind spot) rather than concatenating raw findings. This file's step 4 keeps the
fan-out-then-synthesize shape but drops the tension axis (this workspace's review runs one
instrument — `docs:doc-checker` — not several distinct critic lenses, so there is no second lens
to genuinely disagree with) and re-scopes "blind spot" to this review's own failure mode
(unverified provenance, drifted hypothesis phrasing) rather than a cross-lens gap. No other part
of `product-forge` cleared the bar for a note here — its orientation-classify shape
(`/product-orient`) and method-card schema (`timebox · participants · produces`) are both
plausible prior art in the abstract, but neither maps cleanly onto this file's five-step flow
without inventing an artifact class (a method-card catalog) this workspace's product doctrine
doesn't have yet — noted honestly as not adopted here, not silently dropped.
