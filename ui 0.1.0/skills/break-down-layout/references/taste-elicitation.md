# Taste elicitation — sampling the user at genuine design forks

Ratified 2026-07-16 (Issue #13). Design work derives from constraints first — but after every
constraint is honored, **residual freedom** remains: layout archetype, density, motion character,
palette temperature, type personality. These are underdetermined by the brief, and people
recognize what they want far better than they can describe it. The instrument is
**AskUserQuestion**; this file is the discipline for using it. It is the canon for every design
skill that asks — consumers wire a *gate* (their fork, phase position, and lock destination) and
cite this file; they do not restate it.

## The five rules

1. **Ask at taste forks, never derivable forks.** A question whose answer is computable from the
   brief, the schema, or a constraint is laziness wearing a dialog. And taste operates strictly
   inside the verified envelope: no option may violate a floor — there is no "AA-failing but
   prettier" choice, ever. If every candidate fails a gate, that is a `DecompositionGap` to
   report, not a menu.

2. **Options are artifacts, not adjectives.** "Minimal or dense?" collects noise — everyone says
   minimal. "This one or this one?" collects taste. Use the `preview` field: ASCII wireframes of
   the user's actual screen (never the generic archetype specimen), code snippets for an API
   fork, state-machine sketches for a journey fork. Previews are single-select only — a fork
   needing multiSelect is usually two forks.

3. **The ask-then-lock loop.** A taste answer is expensive exactly once. Every fork answer lands
   somewhere durable in the SAME change: a parameter lock in the project's DESIGN.md or token
   file (lock grammar per forge's skill-authoring-standards, where installed: lowercase
   always/never + backticked values + named forbidden neighbors), or a session memory for
   cross-project preferences. Ratified taste is never re-asked — check the project's standing
   rulings and memories BEFORE building the question; an ask that re-opens a recorded ruling is
   a defect. (Illustrative precedent class: a cross-project easing or icon-library preference,
   sampled once as a session memory, applying silently ever after.)

4. **One batched round at a named phase gate.** Each consuming skill declares WHERE its gate sits
   — after inventory/constraints, before commitment — and batches every open fork into one round,
   ≤4 questions. Early gates ask wide (direction A/B/C, preview-backed); late gates ask narrow
   (the exact value entering a lock). Peppering asks across a run is the failure mode this rule
   exists to kill; a second round in one run needs the first round's answers to have genuinely
   created the fork.

5. **Every option is a committable plan.** The recommended option comes first, marked
   "(Recommended)", and states what picking it commits: "Warm neutral ramp anchored at your brand
   hue, dark scheme derived (Recommended)" — never "warm or cool?". Picking IS the decision; no
   follow-up question should be needed to act on an answer.

## Artifact escalation — when ASCII cannot carry the preview

Color and typography do not survive monospace. For those forks: render 2–3 candidate directions
as ONE private HTML artifact (palette strips, type specimens — side by side, labeled A/B/C), then
ask with options referencing the artifact's labels. One artifact per gate, not per option; the
artifact is the preview, the AskUserQuestion is still the decision instrument.

## The fence: measurement never asks

Verify-species skills (check-colors, check-focus, check-speed, check-translations, check-safety,
check-ui-change) run ask-free, always. A verifier that asks mid-measurement is laundering its
responsibility onto the user; findings are reported, and any resulting fork belongs to the
DESIGN-side skill that owns the fix. This fence is load-bearing: it is what separates taste
sampling from sycophancy machinery.

## The gate, worked (break-down-layout DESIGN mode) — normative shape

```
Context: brief = "internal claims-review tool"; constraints derive productivity-shell OR
saas-dashboard as legal; standing rulings checked — none covers this fork.

AskUserQuestion (one round):
  Q1 header "Shell"  ·  "Which shell fits how reviewers will work?"
    ○ Work-in cockpit (Recommended) — one claim framed by queue + detail panes
      [preview: ASCII wireframe of THEIR screens: app-pane-left=queue · canvas=claim ·
       pane-right=evidence]
    ○ Navigated dashboard — claims as records in pages
      [preview: sidebar-nav · table · detail-drawer wireframe of the same content]
  Q2 header "Density" · "Default density for the queue pane?" (only if genuinely open;
     a narrow late-gate ask — value-backed per rule 4, no preview owed)
    ○ Compact (Recommended) — 8px rhythm, more rows in view: `row-height: 32px`
    ○ Comfortable — 12px rhythm: `row-height: 40px`

Lock (same change): DESIGN.md gains "shell: productivity-shell (ruled <date>)" and
"queue density: always `32px` rows, never `40px`" — the next session never re-asks.
```

## Consumers (each declares: fork · phase position · lock destination)

| Skill | Fork | Gate sits | Lock lands |
|---|---|---|---|
| break-down-layout (screens) | archetype/variant, density | DESIGN mode: after intent + constraints, before wireframe emission | project DESIGN.md ruling |
| make-component (screens) | API shape / variant set when the charter leaves both legal | after the API-surface and composition drafts, before geometry is realized | the component's contract card (`rulings` entry) |
| break-down-flow (screens) | journey shape (linear wizard vs hub-and-spoke) when both machines pass | DESIGN mode: after the task inventory, before the card is written | the .flow.json card (+ a DESIGN.md line for area-wide rulings) |
| make-palette (color) | anchor negotiation / temperature direction | at anchor negotiation, artifact-escalated (palette strips) | ramp provenance + the BrandSchema/UISchema anchor |
| pick-fonts (typography) | territory point: the brief names two live references, or none it can name | at the named-reference push-back, artifact-escalated (type specimens) | the per-voice decision doc |

Cross-plugin consumers (color, typography) cite this file as "ui's break-down-layout
references/taste-elicitation.md, where installed" and carry their one gate block locally — the
discipline degrades to its five rules stated in one line, never to silence. The canonical
one-liner, copied verbatim so paraphrases don't fork: "ask only genuine taste forks inside the
verified envelope, options as artifacts not adjectives, one batched round, every option a
committable plan, the answer locked durably".
