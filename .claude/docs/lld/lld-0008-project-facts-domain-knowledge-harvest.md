---
doc-type: lld
id: lld-0008-project-facts-domain-knowledge-harvest
status: approved
version: 1.0.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#612
spec: none — the record's own Acceptance section carries the checkable criteria; #612's
  Scope/Open section names the exact design questions this LLD resolves, so a standalone SPEC
  would restate what the ticket already states (doc-writing-rules' own routing test)
---
# LLD — `project-facts`: the domain-knowledge harvest skill and its shared core with #613

**Verdict, head-first:** one user-invocable docs skill (`project-facts`), one shared core file it
mints (`references/harvest-core.md`) that the sibling ticket (#613) will cite rather than
duplicate, topic zones discovered per project rather than fixed, and this workspace itself as the
eval's sample project. The one open item this LLD does NOT resolve on its own authority: the
skill's name deviates from ticket #612's stated lean (`harvest-domain-knowledge`) because that name
fails ADR-0011's naming-grammar gate without new vocabulary registration, and
`authorkit:manifest-authoring`'s own confirm gate cannot fire unattended (no live user in this
build). Resolutions below, each with its rejected alternative.

## Resolution 1 — Surface shape: one skill, not a command or dual-mode SKILL.md

**Resolved:** one user-invocable, model-invocable skill (`disable-model-invocation: false`,
`user-invocable: true`), matching the ticket's own lean and this plugin's dominant shape
(`make-reference`, `make-rubric`). Not a command (`disable-model-invocation: true` would make it
unreachable from `dispatch-ticket`'s own Skill-tool routing, and from the sibling's future
composition — see #612's own citation of the #134/#135 defect class in the shared `dispatch-ticket`
skill this build ran under). Not a single SKILL.md carrying both siblings as "modes" — the two
corpora differ in consumer and weighting but share nothing else that a mode-switch would clarify
over two skills each citing one shared reference file; forcing both into one file would also
force one skill's frontmatter description to carry two audiences' trigger vocabulary, working
against the routing-surface discipline `plugin-authoring.md` states.

**Rejected:** a `harvest-*` command pair (`/harvest-domain-knowledge`, `/harvest-project-context`)
wrapping two skills — adds a wrapper layer neither corpus's own workflow needs (no confirm-gated
mutation, no user-only mechanic); rejected per the same reverse-wrapper-amendment reasoning that
lets a `user-invocable: true` skill carry the same "two surfaces" fact on one file instead of two
(spec-naming-convention.md §14.9).

## Resolution 2 — Topic-zone taxonomy: discovered per project, never fixed

**Resolved:** topic zones are discovered from each project's own harvest sources (a zone earns its
place by recurring across ≥2 independent sources — `references/extraction-procedure.md` Step 2),
and the rubric scores zone COVERAGE against whatever set the harvest itself discovered
(`references/harvest-core.md` R1).

**Rejected:** a fixed taxonomy (e.g. a standing list like "Business rules / Architecture / Data
model / Integration points"). Rejected because a fixed list either overfits a project whose real
shape doesn't match those buckets (forcing zones into a wrong bucket) or leaves a project's actual
first-class concern unscored because it didn't map to any bucket name. The ticket's own Scope/Open
question left this genuinely undecided; discovery is the only shape that scores fairly across
projects of very different structure.

## Resolution 3 — Eval sample project: this workspace itself

**Resolved:** `kimgranlund/claude-plugins` (this repo) is the sample project for deliverable (c)'s
eval run (`references/eval-harness.md`) — its own brief, IDRs, ADRs, PRDs, and roadmap are already
a ratified, known-answer corpus, so the eval's known-answer key needs no separate authoring pass.

**Rejected:** a synthetic toy project — would need a hand-authored answer key with no independent
ratification behind it, materially weaker grounding than this repo's own accepted records.

## Resolution 4 — Shared-core home: lives in `project-facts`'s own `references/`, cited by #613

**Resolved:** `docs/skills/project-facts/references/harvest-core.md` is the ONE canonical file
carrying both corpora's shared definitions and the two-axis rubric (#612 mints it, per the
dispatch's own instruction — first in the serial chain). #613's future build cites it by relative
path (`../project-facts/references/harvest-core.md`) rather than duplicating its body; the
citation is an ordinary same-plugin mention, not a plugin-boundary violation
(`plugin-authoring.md`'s hard/soft split governs cross-PLUGIN preloads/`${CLAUDE_PLUGIN_ROOT}`
paths, not a same-plugin file reference).

**Rejected:** a third, neutral skill existing only to host the shared core (e.g.
`docs/skills/harvest-core/`) — adds a skill with no independent trigger of its own (nothing should
ever route to it directly), which is exactly the anti-pattern `spec-naming-convention.md` §"Templates
and schemas" warns against for a shared artifact needed by exactly two consumers: the §9
extraction rule's bar ("a template or schema needed by a SECOND skill becomes an ordinary skill")
is designed for genuinely reusable, addressable contracts, not a two-item citation the owning
skill can carry directly. Also rejected: a symlink (this plugin's own precedent,
`make-llms-txt`'s `best-practices.md` → `make-reference`) — a symlink states "this IS that file,"
appropriate when one skill's content is wholly subsumed by another's; here #613 cites the core but
adds its own distinct weighting and procedure around it, so a plain relative-path citation (not an
identity symlink) is the more honest relation.

## Resolution 5 — Naming: `project-facts`, not `harvest-domain-knowledge`

**Resolved:** the skill is named `project-facts` — `ObjectVocab` "project" + `ProcessLex` "facts",
both already registered in the repo-root `naming.manifest.json` (ADR-0011). Parses cleanly under
the object-process production with zero new vocabulary.

**Rejected:** `harvest-domain-knowledge` (the ticket's own stated lean) and its grammar-correct
verb-terminal cousin `domain-knowledge-harvest` (legal under spec-naming-convention.md §14.9's
reverse-wrapper amendment, since this skill IS `user-invocable: true`) — both require registering
NEW lexicon tokens (`ObjectVocab: domain-knowledge`, `VerbLex: harvest`) via
`authorkit:manifest-authoring`. That skill's own procedure is explicit and unconditional: "before
writing `naming.manifest.json`, present the proposed change and wait for explicit confirmation...
No live user to confirm with → stop and report the gate SKIPPED rather than writing unconfirmed."
This build has no live user (an unattended `build-leader` dispatch). Rather than either (a)
silently editing the shared, estate-wide manifest without the confirmation its own skill demands,
or (b) shipping a brand-new mint that fails `release_gate.py`'s G12 naming-grammar gate outright,
this LLD follows the identical precedent already recorded in this plugin's own README ledger for
`agent-harness-rules`: "G12's naming-grammar gate (ADR-0011) has no live-confirm path to register a
brand-new lexicon token unattended, so the name was chosen from already-registered vocabulary
instead." `project-facts` is that same trade: correct on the grammar, deliberately less precise
than the ideal name, with a `manifest-authoring` follow-up left open if Kim wants
`domain-knowledge-harvest` instead — a rename at that point is a `rename-planning`/`rename-execute`
job, not a re-author.

**Consequence for #613, named but not decided here:** #613's own build should NOT default to
"project-facts"'s own naming shortcut without checking for collision; the same reasoning suggests
`project-facts`'s natural sibling could resolve to something distinctly agent/harness-flavored
(e.g. a name built on the already-registered `-rules` reserved tail, matching this estate's own
`*-rules` convention for agent-facing directives) rather than reusing "project-" as a prefix and
risking two skills that read as near-duplicates by name alone. Left to #613's own build-leader.

## Components

- **`docs/skills/project-facts/SKILL.md`** — the routing surface + 6-step procedure pointer.
- **`docs/skills/project-facts/references/harvest-core.md`** — shared definitions (domain
  knowledge + project context) + the two-axis rubric (R1–R7); canonical, cited by #613.
- **`docs/skills/project-facts/references/extraction-procedure.md`** — this corpus's own
  step-by-step harvest procedure and Outside-In 60/Inside-Out 40 weighting arithmetic.
- **`docs/skills/project-facts/references/eval-harness.md`** — deliverable (c): payload-layer eval
  prompt set (E1–E6), sample project, scored-report shape.
- **`docs/skills/project-facts/evals/evals.json`** — routing eval suite (7 trigger, 8 no-trigger,
  including the not-yet-built #613 sibling as a forward-declared fence).
- **Reciprocal fences**: `docs/skills/make-reference/evals/evals.json` (n13),
  `docs/skills/make-rubric/evals/evals.json` (n13) — the neighbors whose trigger vocabulary this
  skill's description could steal from.

## Interfaces

- **Skill → shared core**: `project-facts`'s `SKILL.md` and `extraction-procedure.md` both read
  `harvest-core.md` by relative path; no code interface, a plain markdown reference contract.
- **#613 → shared core** (future, not built by this LLD): cites
  `../project-facts/references/harvest-core.md` by the same relative-path convention; #613's own
  build states its own weighting (Inside-Out 60/Outside-In 40) and its own procedure file, never
  copying `harvest-core.md`'s body.
- **Eval harness → rubric**: `eval-harness.md`'s scored-report cites `harvest-core.md`'s R1–R7
  dimension IDs directly — no separate schema, the rubric table IS the interface.

## Data

Static markdown artifacts only — no runtime data store, no migration. A harvest RUN's own output
(a produced domain-knowledge corpus doc) is user/project-owned, not part of this plugin's own
shipped tree; the skill produces it wherever the invoking session directs, per
`docs:make-reference`'s own authoring convention (canonical, one topic, dated).

## Risks

- **R-1 (naming).** `project-facts` is a deliberately-compromised name (Resolution 5). Detection:
  a future reader expecting `harvest-domain-knowledge` won't find it by that name. Fallback: the
  SKILL.md description states the full trigger vocabulary regardless of file name, so routing
  isn't harmed; a future `manifest-authoring` + `rename-planning`/`rename-execute` pass can rename
  it if Kim ratifies the new vocabulary live.
- **R-2 (zone-discovery subjectivity).** Discovered-not-fixed zones (Resolution 2) mean two harvest
  runs over the same project could name zones slightly differently. Detection: `harvest-core.md`'s
  R1 gate requires zones traceable to specific source passages — a run that can't cite its zone
  boundaries fails the gate before this becomes a silent inconsistency. Fallback: none needed
  beyond the gate; this is the accepted cost of discovery over a fixed taxonomy (Resolution 2's
  own rejected-alternative reasoning).
- **R-3 (eval scope).** The eval harness (`eval-harness.md`) ships with 6 fixed prompts (E1–E6);
  a materially different project shape might need additional probes. Detection: an eval run that
  scores clean on E1–E6 but a reader still can't answer a real question from the corpus. Fallback:
  the file's own header states "extend per project as new zones surface" — extension is expected,
  not a gap.

## Agent verification

Payload-layer, per `docs:agent-harness-rules` (cited in #612's own Acceptance section): deliverable
(c)'s `references/eval-harness.md` IS the new harness this design needed built — no existing
instrument in this estate already ran fixed prompts against an extracted domain-knowledge corpus
scored via a two-axis rubric, so this is a genuine new harness, not a re-use of one
(`agent-harness-rules`' own "estate mapping first" step was checked: `research-methods`' six
methods presuppose an already-scorable system, which is exactly what this eval harness makes true
for the first time here). The rubric self-score (Step 6, gate R1/R4/R5/R7 ≥ 3) is the mechanical
half; the eval run against the known-answer sample project (this workspace) is the payload-layer
half proving the corpus is valuable, not merely well-formed.
