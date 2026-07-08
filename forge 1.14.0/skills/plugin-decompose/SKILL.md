---
name: plugin-decompose
description: >-
  Analyze an existing harness surface — a folder of skills (plus agents, hooks, scripts), one
  oversized plugin, or several scattered ones — and decide how it should partition into 1–5
  manageable, portable, composable plugins. Use when: "which plugins should these skills become",
  "partition our .claude folder into plugins", "should this mega-plugin be several smaller ones",
  "can these skills and hooks be divided into portable domains", "group this grab-bag into
  installable units", "what is missing from this plugin corpus", "run a gap analysis on this
  plugin family". Direction-agnostic: fewer plugins than today is a merge verdict, more is a
  split, same tests either way. Frontmatter + structure is sufficient input (surface_map.py
  extracts the dependency graph). NOT for one knowledge corpus splitting into packs
  (skill-decompose); NOT greenfield family design (plugin-forge); NOT releasing or structuring a
  single plugin (plugin-release / plugin-authoring-standards).
disable-model-invocation: false
user-invocable: true
argument-hint: "[surface-root]"
---

# plugin-decompose — partition the surface, don't just group it

The distribution-layer sibling of `skill-decompose`: where packs partition by *question type*,
plugins partition by **job-to-be-done and lifecycle** — what one consumer installs, trusts,
versions, and updates as a unit. This skill decides and designs the partition; it never moves an
artifact. Execution: `/plugin-forge` Phases 3–6 scaffold and release each resulting plugin; member
moves follow the validated manifest. Surface: `$ARGUMENTS` (default `.`).

## Phase 1 — Survey: the graph is the evidence

`python3 "${CLAUDE_PLUGIN_ROOT}/skills/plugin-decompose/scripts/surface_map.py" map <root>` —
nodes (skills with dials, agents, hooks, scripts) and typed edges (`mention` from descriptions and
bodies, `preload` from agent `skills:`, `script` from hook/skill references). Frontmatter and
structure are sufficient by design; do not read bodies for content, read them for names. The graph
is deliverable even under a no-partition verdict.

## Phase 2 — The four tests, at the distribution layer

1. **Job-to-be-done clustering.** Group artifacts by the consumer who installs them and the job
   they install them *for* — the plugin-level analog of question types. A standards skill, the
   forge that applies it, the hook that enforces it, and the agent that reviews it are one job;
   two audiences who would never install each other's members are two plugins. Four lenses on one
   job are one plugin, whatever the file count.
2. **Dependency closure.** Read the graph: `preload` and `script` edges are **hard** — they cannot
   cross a plugin boundary (an agent cannot preload another plugin's skill; a hook's
   `${CLAUDE_PLUGIN_ROOT}` cannot reach a sibling plugin), so any candidate cut crossing one is
   dead on arrival (`surface_map.py check` kills it mechanically). `mention` edges are **soft** —
   handoffs and fences may cross, but a cut where cross-plugin mentions outnumber internal ones has
   made cross-plugin consult the common case: the co-occurrence kill, one level up.
3. **Namespace and vocabulary separability.** Each candidate plugin needs a distribution-scoped
   name disjoint from its members' domain prefixes (the stutter rule — checked mechanically), and
   sibling plugins must not compete for one trigger-token field: the 1% listing budget is shared
   across everything installed, so two plugins whose descriptions overlap steal from each other
   exactly as sibling skills do.
4. **Lifecycle ledger.** Each plugin costs a manifest, a version stream, a release ritual, and a
   recurring trust decision on every update. Artifacts that change together should version
   together; a stable standards core and a fast-moving experimental family on one version stream
   force consumers to re-trust churn they never use — that is a real split benefit, and it must be
   stated as one (installs avoided, updates decoupled), not as "cleaner". 1–5 plugins is the
   healthy output range; a 6+ partition is usually test 1 done by topic instead of job.

## Phase 2.5 — Escalate: partition as refactor opportunity (`reasoning-orders`)

The four tests answer "how should today's artifacts group" — a 1st/2nd-order question. Before
proposing, invoke `reasoning-orders` and climb, paying rent at each step:

- **3rd order** — for each candidate partition, model the reactions: which descriptions will the
  router confuse across the new plugin boundary (name the eval cases that will prove it); which
  consumer installs plugin A and immediately hits a wall that lives in plugin B?
- **4th order** — simulate the ecosystem: total listing-budget footprint before/after, trust
  re-decisions per year per consumer, version-stream coupling. A partition optimal per-plugin but
  corrosive in aggregate is rejected here.
- **5th order** — interrogate the inputs themselves: is the observed structure a fossil of its
  history rather than its jobs? Should some members be *dissolved, merged, or rewritten* rather
  than moved — thin skills a synthesis would strengthen, corpora a split would sharpen, prose rules
  a hook should replace? These findings do NOT expand this skill's scope: each becomes a routed
  line in the **refactor-opportunities ledger** (owner: skill-decompose, skill-synthesize,
  skill-review, hook-forge, or pack-forge), co-deliverable with the partition manifest.

The anti-tidying test, verbatim from the anti-pattern table: **if the proposed partition's graph is
isomorphic to the input's folder structure, no reasoning above 1st order occurred** — either climb
until something genuinely improves, or state honestly that today's structure already is the
optimum (a defended no-partition beats a relabeled one).

## Phase 2.6 — Negative space: what's missing (actual or hypothetical corpus)

`surface_map.py gaps <root>` produces the evidence: **dangling references** (prose names carrying a
family suffix but matching no artifact — an unowned handoff is the strongest gap signal there is;
every real gap this plugin's own history closed announced itself this way first) and the **family
matrix** (per name-prefix group: standards / command / check-script / evals present or absent).

Then the judgment, under the anti-matrix guard: **an absence is a gap only with job evidence** — a
dangling handoff, an ask no member's suite can answer, a charter line with no owner. Template
asymmetry alone is a question, never an answer; most matrix holes are *correct* absences (a
cross-cutting knowledge layer needs no command; a family whose checks live in a shared lint needs
no private script) and the verdict says so explicitly. For a hypothetical corpus — a charter with
no tree yet — this phase runs as a charter-vs-members diff and hands the result to
`/plugin-forge`'s rejected-members ledger, which owns the greenfield version of this question.
Confirmed gaps join the manifest as `gap_candidates`, each with its evidence and its build owner
(`/skill-forge`, `/pack-forge`, `/hook-forge`, `/agent-forge`).

## Phase 3 — Propose, with the rejected ledger

Candidate partition: per plugin — name (grammar- and reserved-checked), one-line charter, member
list, dials summary; plus the **cross-plugin seam list** (every surviving soft edge, named and
justified — an unexamined seam is a phantom reference waiting to happen) and the mandatory
**rejected-alternatives ledger** (every finer or coarser grouping considered and which test killed
it). The one-plugin answer is legitimate and must be argued against, not ignored.

## Phase 4 — Validate mechanically

Write the partition manifest and run
`surface_map.py check <partition.json> <root>` — every artifact assigned exactly once, names
clean, stutters warned, hard edges never crossing, every seam enumerated with counts. Fix and
re-run until clean; never hand off an unreconciled partition.

## Manifest schema

```jsonc
{
  "verdict": "partition",            // "partition" | "no-partition"
  "plugins": [
    { "name": "forge", "charter": "authoring the harness's artifacts",
      "members": ["skill-forge", "skill-authoring-standards", "skill-auditor", "skill_lint.py"] }
  ],
  "seams": [ { "from": "forge", "to": "data-plane", "kind": "mention", "count": 2, "justification": "handoff after verdict" } ],
  "gap_candidates": [ { "name": "x-refactor", "evidence": "3 dangling handoffs from x-decompose", "owner": "/skill-forge" } ],
  "refactor_opportunities": [ { "finding": "thin sibling pair with shared vocabulary", "owner": "skill-synthesize" } ],
  "rejected_alternatives": [ { "candidate": "split standards into their own plugin", "reason": "test 2: preload edges from every forge cross the cut" } ]
}
```

## Phase 5 — Verdict and handoff

`partition` (1–5 plugins, named) or `no-partition`, with the ledger either way. Handoff:
`/plugin-forge` scaffolds each new plugin and runs its member, fence-closure, and release phases;
each plugin's own release gate (G5/G8 sweeps, `/eval-run`) is the proof that no retired grouping
leaks. This skill's job ends at the validated manifest.

## Boundaries

- **Not skill-decompose.** One corpus → child packs is content partitioning; this is distribution
  partitioning of heterogeneous artifacts. A pack that is itself too big routes there first.
- **Not plugin-forge.** Greenfield family design runs on projections; this runs on an inventory.
  They meet at the handoff: this skill's manifest is that command's charter input.
- **Direction-agnostic, so no synthesize sibling exists at this layer.** Merging scattered plugins is a partition
  with fewer groups than today — same tests, same manifest, same skill.

## Done / NOT done

**Done** = graph extracted and cited, all four tests run in order with evidence from it, 1–5
plugins (or a defended no-partition), rejected ledger present, the escalation ladder climbed with rent paid (or 1st-order sufficiency stated honestly), refactor opportunities routed to owners, negative space examined with each confirmed gap carrying evidence and a build owner (and each matrix hole either confirmed or defended as correctly absent), every seam justified,
`surface_map.py check` clean, handoff names `/plugin-forge`. **NOT done** = a grouping proposed
from topic resemblance without the graph, a hard edge crossing a cut, an orphan artifact, a
missing rejected ledger, a partition isomorphic to the input folder structure presented as a refactor, or a benefit stated as an adjective.
