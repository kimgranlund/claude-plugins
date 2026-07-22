---
name: make-pack
description: >-
  Mint or grow a knowledge pack's reference corpus via question-led research waves: charter an
  axis, write the question set, gather dated sources, distill ask-shaped files, then register
  and validate. Run /make-pack [skill-dir or "new pack: domain"], one axis per wave. NOT the
  SKILL.md surface (make-skill); NOT a split/merge decision (plan-skill-split/plan-skill-merge);
  NOT the rules themselves (pack-writing-rules).
disable-model-invocation: true
user-invocable: true
argument-hint: "[skill-dir | new pack: domain]"
---

# make-pack

make-pack fills the gap every other make-* workflow fences: the corpus behind a knowledge skill. Target:
`$ARGUMENTS`. Invoke `pack-writing-rules` now — the wave method, grounding markers, and load
budgets below are its rules; this command only sequences and enforces them.

## Phase 0 — Route

SKILL.md surface wanted → `/make-skill` (a brand-new pack runs that first; this command fills what
it scaffolds). Corpus too big / too thin → `plan-skill-split` / `plan-skill-merge`. Corpus content
to create or grow → proceed.

## Phase 1 — Wave charter

Read the pack's SKILL.md and INDEX (or the fresh scaffold). One batched round with the user: which
axis this wave mints or grows, depth target (files, not pages), source constraints (allowed
domains, recency floor), and what "done" answers. **One axis per wave** — a request for the whole
pack becomes a numbered wave plan, executed one at a time with registration between waves.

## Phase 2 — Question set (the wave's evals)

Write the asks the new files must answer — 5–12 concrete questions in the user's likely phrasing —
*before any searching*. The user ratifies the set; it becomes the wave's acceptance criteria and,
verbatim, the trigger-phrasing candidates for the pack's eval suite in Phase 5. A question nobody
would ask is cut here, not researched.

## Phase 3 — Gather, dated

Per question cluster: dispatch a `fact-finder` agent (its allowlist enforces gather≠distill —
no Edit, no Bash; it preloads the standards so the grounding rules travel with it), each capturing
findings with source and access date into its own working ledger (`references/.wave-<n>-ledger.md`, atticked or
deleted after distillation). No prose yet — gathering and writing interleaved is how literature-
shaped files happen.

## Phase 4 — Distill ask-shaped

One file per question type, named for its ask, ≤1000 lines, every claim carrying [verified] /
[inferred] / [drift-prone] with source and date per the standards. Where a claim contradicts
something already in the corpus, amend the older claim in place with a dated note — never leave two
files answering the same question differently.

## Phase 5 — Register

In one change: INDEX lines under the axis heading, the SKILL.md consult-table row, and the eval
suite gains this wave's Phase-2 phrasings as trigger cases (plus reciprocal no-triggers in any
sibling whose vocabulary the new axis brushes — the fence-closure rule applies to axes, not just
skills). An unregistered file is unreachable; do not start the next wave with this one unregistered.

## Phase 6 — Validate and report

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/corpus_check.py" <skill-dir>` — INDEX↔tree reconciliation,
load budgets, grounding-marker coverage, axis count. Fix and re-run until clean. Report:

```
make-pack · <pack> · wave <n>: <axis>
Questions: <k> ratified · Files: <m> written (<lines> total) · Markers: <verified/inferred/drift-prone counts>
Registered: INDEX +<m>, consult table +1, evals +<k> triggers
corpus_check: clean · Next wave: <axis or none>
```

Done when corpus_check is clean and every Phase-2 question is answered by a registered, marked
file. NOT done if any file is unregistered, any claim is an orphan, or the wave silently grew past
its one axis — scope creep in a wave is how heroic dumps happen, and the wave plan exists to
prevent exactly that.
