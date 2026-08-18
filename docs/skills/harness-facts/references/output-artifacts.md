# Output artifacts — the ready-to-install harness contract

`harness-facts`' Step 5 (see `extraction-procedure.md`) emits four artifact classes plus a run
manifest, never a single human-readable reference doc — the genuinely new substance this corpus
adds over the sibling (whose Step 5 is one `make-reference`-shaped write-up). Every artifact is
**staged**, not installed — this file states each artifact class's own conformance contract;
installing any artifact into a live project is always the invoking session's own act, never this
skill's.

## 1. CLAUDE.md-grade entry-file section

A drop-in section, sized and registered to slot into a project's own CLAUDE.md/entry file. Every
line in this artifact must pass the **residency test**, stated here inline as the floor this skill
applies whether or not `harness:entry-file-rules` is installed in the target project:

> *Is this true on every turn, and does the model need it before any task content frames it?* Two
> nos → the fact belongs in a different artifact class (a `.claude/rules/` file, a pack seed, or
> the dispatch-context block), never in this one.

(Cross-plugin soft mention per `plugin-authoring.md`: this skill cites `harness:entry-file-rules`
by name for the full standard — position/salience mechanics, the ~150–200 instruction adherence
ceiling, the seed-class ~20–40 line sizing target — and carries only the one-line test above as
the degraded-gracefully floor when that plugin isn't installed.)

Conformance for this artifact class:
- Identity-grade facts only (what the codebase is, directory topology, invariant conventions,
  build/test/lint/gate commands) in **declarative register** ("every plugin ships through the
  gate," never "remember to run the gate").
- Pointer-heavy: a fact with depth behind it gets a one-line pointer to that depth (a rule file, a
  skill, an ADR digest), never the depth itself inlined.
- Seed-class sized: the emitted section targets the same ~20–40 line ceiling
  `harness:entry-file-rules`' shipped seed models — if a project's discovered zones would blow that
  budget as entry-file-grade, the excess routes to artifact class 2 or 3 instead of inflating this
  one.
- A zone's Inside-Out score alone does not qualify it for this class — only zones whose finding is
  true EVERY turn, project-wide, qualify; a zone that's true only inside one subtree is artifact
  class 2's job.

## 2. `.claude/rules/` path-scoped rule files

One file per subtree-local zone finding — a zone whose truth holds inside a specific path but
would be noise project-wide (`harness:entry-file-rules`' own routing-table destination for
"subtree-local knowledge"). Conformance:
- Each emitted rule file **states its own path scope up top**, in the same form this workspace's
  own `.claude/rules/*.md` files use ("**Path scope:** `<glob>`, ...").
- One zone finding per file where the finding is genuinely path-bound; do not fold two unrelated
  subtree truths into one file just because both were discovered in the same run.
- A zone finding that's true project-wide is never routed here — that's a class-1 miss, not a
  class-2 candidate; the run manifest names the routing decision for every zone so a reviewer can
  check it.

## 3. Knowledge-pack seed candidates

Flagged entries, not authored pack files. This skill never hand-scaffolds a pack (the workspace
routing table's own rule: pack creation and growth is `/make-pack`'s job — `harness:make-pack`).
Each seed candidate states:
- The finding itself, with its source citation (R6).
- The **target pack** it belongs to (an existing pack skill's `references/` corpus, named by
  skill, or "no existing pack — new pack" if none fits).
- The exact **`/make-pack [skill-dir | "new pack: domain"]`** invocation a human would run next to
  actually land it.

A zone finding that doesn't clear the durable-knowledge bar (`harness:save-lessons`' own judgment
call, not this skill's) is still flagged as a candidate here — seeding is not the same act as
deciding a fact earns a durable entry; that decision stays downstream, at the human's `/make-pack`
run or a `save-lessons` pass.

## 4. Dispatch-context block

A single paste-ready digest sized for a `dispatch-ticket`/`build-leader` seat's own dispatch
prompt — the context a coordinator would paste ahead of a builder's task description, not a
document a human reads standalone. Conformance:
- Terse, Inside-Out-first: leads with the mechanism a builder needs before naming any task (which
  gate to run, where the LLD/ticket lives, which rule files bind the touched paths) — the same
  ordering this corpus's own weighting produces, made literal.
- No "what problem does this solve" framing (that's the sibling's Outside-In register) — every
  line answers "what does a builder need to already know to act correctly here."
- Bounded: this is a digest, not the run manifest — it points at the manifest and at specific rule
  files rather than inlining their full content.

## The run manifest — the corpus's gateable spine

One index document per harvest run, listing every artifact actually emitted (across classes 1–4)
plus every zone the run discovered — including a zone that was discovered but never surfaced in
any artifact (named "discovered, not surfaced," per `extraction-procedure.md` Step 5). For each
entry:

```
| Zone | Inside-Out | Outside-In | Weighted (0.6*IO+0.4*OI) | Artifact class(es) | Source |
```

The manifest is what `harvest-core.md`'s rubric self-score (R1–R7) is scored against, and what the
eval-harness's WITH-vs-WITHOUT run's traceability check (R6) points back to — it is the one thing
across a many-file run that stays a single gateable spine, per the LLD's own framing (Resolution
3).

## Staging, not installing

All four artifact classes plus the manifest land at a **staging path the invoking session
directs** — a scratch directory, a PR-review branch, wherever the invoker names. This skill never
writes into a target project's live `CLAUDE.md`, `.claude/rules/`, or a knowledge pack's committed
`references/` tree directly; installing a staged artifact into any of those live locations is the
invoking human or host's own act, made after its own review — mutating a project's entry file is
the highest-blast-radius write a harness has (`entry-file-rules`: a stale line is *believed*, not
ignored), and it stays behind that review on every run, not just the first.
