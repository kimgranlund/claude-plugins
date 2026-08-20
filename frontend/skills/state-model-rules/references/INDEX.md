# state-model-rules — reference index

Judgment calls for app-tier state architecture, distilled from three dated field-report corpora
(agent-ui, gen-ui-kit, adia-v2 — see `sources.md`). Eight files, above the flat-corpus threshold
(`harness:pack-writing-rules`' ≤~7 rule) — this INDEX is the retrieval map; the skill body's own
consult table mirrors it at a coarser grain.

## Axes (topical order — no natural severity ranking across these seven independent judgment calls)

| File | The question it answers |
|---|---|
| `four-generations.md` | Why does this app have N incompatible state patterns stacked on top of each other, and what's the diagnostic before recommending a rewrite? |
| `two-facts-one-name.md` | Two things share a name ("name", "active", "state") — are they the same fact with a missing wire, or two facts that need their own names? |
| `adoption-verdict.md` | Is this sanctioned layer/store actually used, or just built — and what does "load-bearing" mean when bypasses still exist? |
| `never-pulled-triggers.md` | We (or the doctrine) named a condition for revisiting this decision — did anyone ever check it fired? |
| `doctrine-vs-practice.md` | How far has practice drifted from doctrine, measured per layer instead of as one estate-wide verdict — and how does that differ from doctrine contradicting itself? |
| `one-name-two-owners.md` | Two places both write the same conceptual field, independently — when is that a live-bug-hazard rather than benign duplication? |
| `audit-technique.md` | How do I run this kind of audit on my own codebase — the four concrete techniques (sync-point mapping, bypass inventory, coherence mapping, doctrine-vs-practice diffing) the three source corpora actually used? |

## Provenance

`sources.md` — the three corpora, grounding markers, and what this pack deliberately does not
re-verify.

Extension: governed by [[make-pack]]
