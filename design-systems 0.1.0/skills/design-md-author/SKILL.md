---
name: design-md-author
description: >-
  Author a DESIGN.md design-system spec end-to-end — run when asked to "create a design system for
  use in claude design and claude code" based on a corpus of design files, css, tokens, descriptions,
  a codebase, or nothing but a brief. Five gated phases: corpus census → Root Brand Architecture
  capture → tactical token system → DESIGN.md draft → @dsCard preview cards + validation. Writes
  files. NOT for format Q&A without a writing run (design-md-format). NOT for consuming a finished
  design system to build UI. Emits framework-neutral output only; accessibility is measured and
  disclosed, never enforced.
disable-model-invocation: true
user-invocable: true
argument-hint: "[brand name or path to corpus]"
---

# design-md-author

Turn a corpus (or a brief) into a shipped DESIGN.md + preview cards through five gated phases. A failed gate stops the run; the fix lands in the failed phase.

Seed for Phase 1: `$ARGUMENTS`

Invoke `design-md-format` now — it is the ground truth for every phase and is not restated here. The one identity that governs everything: **you are writing a prompt, not documentation** — every line must change what a fresh agent generates.

Two standing fences, checked at every gate:
- **Framework-neutral**: zero framework names (React, Svelte, Vue, Tailwind, …) as prescriptions; examples in plain HTML/CSS only.
- **Disclose, never enforce**: ship the brand's values verbatim; measure contrast per fill/on-pair per scheme and list the misses; add no accessibility gates the brand didn't set.

## Phase 1 — Corpus census

Inventory every input: token files, CSS, codebases, Figma exports, screenshots, brand decks, prose descriptions. Classify the run:

- **Extraction** (tokens/code exist) — values will be lifted verbatim; note each source file against what it will supply.
- **Synthesis** (partial: e.g. colors but no type) — mark exactly which layers are evidence-backed and which will be proposed.
- **Invention** (brief only) — everything is a proposal until the user confirms.

Missing-but-expected inputs (a mentioned repo you can't read, a dead link) stop the run here — report what's unreadable and ask; never infer content you couldn't read.

**Gate 1:** input inventory written, run type declared, every unreadable source surfaced.

## Phase 2 — Root Brand Architecture

Fill the six slots from `design-md-format`'s brand-architecture reference: values, voice, visual territories, cultural references, refusals, signature details. This phase is where "decent but anonymous" is prevented — do not let token work start until it gates.

- Extraction runs: quote evidence; collect 5–10 verbatim product strings before writing the Voice slot.
- Invention runs: present each slot as a proposal ("Proposed value: …") and get confirmation in one round.
- The signature-details slot resists filling — when empty, ask the user: *"What would make you recognize a screen as yours with the logo removed?"*

**Gate 2:** every slot holds committed lines that carry a design consequence ("restraint over decoration: one decisive action per view" passes; "clean and modern" fails), and invention is confirmed or flagged.

## Phase 3 — Tactical system

Build the three token layers to the format's laws:

- **Colors** — declare prefix + families; construct the full slot inventory per family; every role gets a light value and a `-dark` sibling (identical key sets); high-resolution notation (OKLCH), alpha inline. Measure contrast for every fill/on-pair in both schemes; write the disclosure list.
- **Typography** — 8–15 levels, each indivisible (size + unitless lineHeight + weight, tracking in em); assign families to voices (display/body/mono); fractional weights are legal.
- **Geometry** — closed spacing ladder, closed radius scale with an element map, numeric focus ring; add the control-size ramp when the brand ships dense product UI.

Extraction runs copy exact numbers — 5px stays 5px, never snapped to a 4/8 grid.

**Gate 3:** scheme parity holds, no incomplete typography level, ladders closed, disclosure list written.

## Phase 4 — Draft DESIGN.md

Frontmatter first (it is the API), then the prose spine per the anatomy reference — Overview through Agent Prompt Guide — weaving the Phase-2 architecture into it (values in Overview, voice as its own section, refusals in Do's and Don'ts, cultural references where they anchor).

- Open the file addressing the consuming agent: it reads as instructions, first line onward.
- Add every open-ended section that passes the anatomy file's test (voice, iconography, motion, imagery, copy examples, …); cut any section a fresh agent wouldn't generate differently with.
- Exactly ~3 hard rules, stated as prohibitions; component prose names states numerically (hover fill, focus ring width/offset, disabled treatment).

**Gate 4:** frontmatter complete + spine complete + architecture woven in + both standing fences pass a grep (no framework names, no un-disclosed corrections).

## Phase 5 — Preview cards + validation

1. Write the `@dsCard` set per the preview-cards reference: self-contained, single `:root` with `color-scheme: light dark` + `light-dark()` pairs, one concept per card, component cards state-dense. 7–20 cards.
2. Run `design-md-format`'s validation order on your own draft: scheme parity → pairing law → levels → ladders → recipe states → hard-rules block → stranger test.
3. Round-trip check: hand the DESIGN.md alone to a fresh context with "generate a settings screen for this brand" — the output must be recognizable, not merely compliant. A miss names its layer (architecture vs tokens vs prose) and the fix lands in that phase.

**Gate 5:** cards render in both schemes, validation list clean, round-trip output recognizable.

## Ship

List the final tree (DESIGN.md + cards). Report the disclosure list and any proposals-accepted to the user — they own the tradeoffs. Done when all five gates pass and the files exist on disk.
