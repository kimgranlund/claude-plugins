# Sources and provenance

This pack distills four independent, dated read-only field-report corpora and their cited source
files — not a live re-audit. Every corpus was authored 2026-08-20, on a different repo, by a
dedicated reader session; this pack's own synthesis (2026-08-20) reconciles the four against each
other.

## The four corpora

| Repo | Corpus | Files consulted for this pack |
|---|---|---|
| `adia/gen-ui-kit` | `.claude/docs/reports/2026-08-20-reactivity-review/` | `01-primitives-reactivity.md` (primary), `03-app-layer-stores.md`, `04-doctrine-vs-practice.md` |
| `nonoun/agent-ui` | `.claude/docs/reports/data-model-review-2026-08-20/` | `framework-state-idioms.md` (primary), plus direct source read of `packages/agent-ui/components/src/reactive/graph.ts` and `reactive/scheduler.ts` |
| `nonoun/ultimate-tokens` | `.claude/docs/reports/reactivity-2026-08-20/` | `00-synthesis.md` (primary), `01-core-reactivity.md` (primary) |
| `adia/adia-v2` | `.claude/docs/reports/2026-08-20-reactivity-data-audit/` | `00-index.md`, `03-page-data-workflow-patterns.md` (primary) |

## Grounding markers used in this pack

- **[verified]** — checked directly against the primary field-report file, or against the actual
  source file the report cites, on 2026-08-20 (this pack's authoring date). Every substantive claim
  in this pack's six axis files carries this marker unless noted otherwise.
- **[incident]** — a claim grounded in a NAMED, dated real-world failure the source material itself
  cites (e.g. gen-ui-kit's gh#961 parent↔child oscillation in `signal-kernels.md`). Distinguished
  from [verified] because the evidentiary weight is "this actually broke," not just "this is what
  the code currently does."

No claim in this pack is [inferred] or [drift-prone] as of authoring — every axis traces to a
specific file:line or a corpus's own explicit verdict sentence, quoted or closely paraphrased. If a
cited repo's code changes after 2026-08-20, the specific file:line citations in this pack become
[drift-prone] and should be re-verified at the next refresh boundary rather than assumed current.

## What this pack deliberately does NOT re-verify

This pack is a DISTILLATION of the four corpora, not an independent re-audit of the six cited repos.
Where a corpus itself states a finding as its own verdict (e.g. "one coherent model, not competing
paradigms" — ultimate-tokens `01-core-reactivity.md`), this pack cites that verdict rather than
re-deriving it from a fresh read of the full source tree. A reader who needs to confirm a specific
claim against CURRENT code should re-read the cited file:line, not treat this pack as a live source
of truth for a moving codebase.

Extension: governed by [[make-pack]]
