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

## The flow: orient → harvest → draft → council → ratify

1. **Orient.** Establish what's already known about the domain/market and this specific codebase
   before harvesting — a repo with a `product-forge` plugin installed routes this to its
   `/product-orient` command; without it, this step folds into the harvest pass below.
2. **Harvest candidate intent** from what already exists — founding docs, README, existing ADRs
   (an orphan ADR often implies the IDR it should have cited but never got one — reverse-engineer
   it), commit and issue history, and a structured conversation with whoever is present. Three
   passes, in order: an intake interview to surface candidate claims, a stress-test pass to
   pressure-test each one before it's written down, then a captured artifact that records the
   result — a repo wires these to its own named tools (this workspace's inline fallback:
   `harness:find-intent` → `teamwork:grill-the-ask` → `docs:make-vision-memo`; with `product-forge`
   installed, `/product-discover` + `/product-strategy` supply the intent-content methods instead).
3. **Draft, not a decision.** A draft product brief plus draft IDRs, each passing the
   admission test (`references/alignment-record-types.md`), each explicitly provenance-marked:
   - `derived-from-evidence` — cite the source (a file, a commit, a conversation).
   - `inferred` — a plausible reading that needs human confirmation before it's load-bearing.
   - `gap` — a genuine open question, marked as one rather than silently guessed at.
4. **Council — generator≠critic on the draft, before it ever reaches the human.** With
   `product-forge` installed, `/product-score` + `/product-council` critique the draft the same
   way any other generated artifact gets an independent pass before it ships; without it, this
   step is skipped and the draft goes straight to ratification (a smaller safety margin, named
   explicitly rather than silently absent).
5. **One batched human ratification round.** The seat proposes; it never adopts intent on its own
   authority. A single round, not a drip of individual confirmations — batch every draft item so
   the human DRI reviews the whole candidate intent layer once and owns the result. Close day 0
   with homes, not content: the maturation arc's own first stage (`knowledge-base-habits.md` —
   "born as homes") applies literally — the doc SHELLS exist (a brief, a roadmap index, the
   ratified draft IDRs promoted to real ones), not every fact filled in; content accumulates by
   harvest afterward.

## product-forge integration — soft named mentions only

`product-forge` (a separate, possibly-absent marketplace plugin) supplies METHODS and CRITIQUE
for steps 1-4 above; this seat always keeps the RECORDS and the loop-authority/ratification
decision (step 5) regardless of whether `product-forge` is installed. Per plugin-authoring.md's
hard boundary rule: no preload, no `${CLAUDE_PLUGIN_ROOT}` cross-plugin path — every reference is
a soft named mention that degrades to the inline fallback (steps 2-3 above) when the plugin isn't
present.

## Two guardrails

- **Thin-brief anti-big-bang.** The day-0 output is a THIN brief and a FEW IDRs — exactly the ones
  the harvest surfaced with real evidence or a real open question — never an attempt to
  pre-populate a complete intent layer from inference alone. A large draft on day 0 is the
  big-bang-knowledge-base anti-pattern wearing a different day.
- **Hypothesis phrasing for derived intent.** An `inferred` item is written as a hypothesis about
  the past — "the codebase behaves as if X; confirm or supersede" — with its evidence cited,
  never asserted as if it were an already-ratified decision. The ratification round in step 3 is
  what actually promotes it; the draft's own wording must not pre-empt that.
