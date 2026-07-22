---
name: github-facts
description: >-
  Answers what GitHub's Issue, PR, Discussion, and Projects v2 primitives actually ARE (verified
  2026-07). Use for issue vs. discussion, native issue types vs. labels, sub-issues vs. task-list
  checkboxes and nesting depth, closing keywords, squash-merge behavior, draft-PR/CODEOWNERS/
  merge-queue, or Projects v2 GraphQL fields. NOT our own git mechanics (`big-change-git-rules`);
  NOT the TICKET/ADR/SPEC contract (`doc-writing-rules`); NOT filing a work item
  (`file-bug`/`file-feature`/`file-task`).
disable-model-invocation: false
user-invocable: false
---

# github-facts — GitHub's platform facts, cited and dated

Every claim below traces to GitHub's own documentation or changelog, grounded 2026-07-17 —
grounding markers per `sources.md` (`[verified]` / `[inferred]` / `[drift-prone]` /
`[unconfirmed]`). This pack exists because this workspace's own ADR-0002 and doc-writing-rules
built a whole git-native ticketing convention on GitHub behavior that stayed unchecked against the
platform's real, current feature set — the same class of gap a 2026-07-17 fresh-context review
caught twice on a *different* platform (Linear, in the sibling `spec-linear-adapter`). The unit is
the question a reader arrives with, not the literature's own page structure.

## Consult table

| Ask | Load |
|---|---|
| What an Issue/PR/Discussion each fundamentally is; the REST data-model relationship; when to use which | `references/issue-vs-pr-vs-discussion.md` |
| GitHub's native Issue Types vs. labels vs. the newer Issue Fields; GA dates; query syntax | `references/issue-types-and-labels.md` |
| Sub-issues vs. task-list checkboxes; nesting depth; the retired tasklist-block feature | `references/sub-issues-and-task-lists.md` |
| `Closes`/`Fixes`/`Resolves #N` syntax, the default-branch gate, the unresolved merge-strategy gap | `references/linking-and-closing-keywords.md` |
| Draft PRs, review states, CODEOWNERS, required checks, merge queue, the three merge strategies | `references/pr-lifecycle-and-review.md` |
| GitHub Projects v2 — structure, fields, GraphQL-only API, multi-repo/org spanning | `references/projects-v2.md` |
| Mapping Bug/Task/Feature onto these primitives; where THIS workspace's own convention aligns or diverges | `references/bug-task-feature-mapping-nuances.md` |
| Citation trust tiers and the grounding-marker legend | `references/sources.md` |

Eight files, flat, no subdirectories — at the top of the 3–7 axis band (seven ask-answering axes
plus one provenance file), so this table IS the retrieval map, same convention as this plugin's
sibling `big-change-git-rules`.

## Consult procedure

1. Classify the ask against the table; Grep the matching file for the term first, then Read that
   section — every file is a cited catalog, not a linear read.
2. Answer on the contract: **claim + its grounding marker + source + access date +, where the
   source flags it, the caveat or unresolved gap.** Worked example: "Sub-issues nest up to 8 levels
   deep [verified, docs.github.com, 2026-07-17]" — not "sub-issues nest deeply" with no marker. A
   platform-behavior claim with no marker behind it is the failure mode this pack exists to
   prevent.
3. Distinguish `[verified]` (stated directly by a tier-1/2/3 source) from `[inferred]` (built from
   verified pieces, not itself directly confirmed) from `[drift-prone]` (true now, young enough to
   re-verify later) from `[unconfirmed]` (searched for, not found — a named gap, not a guess).
   Never present one as if it carried a stronger class's confidence.
4. Route ANY ask about THIS workspace's own git/worktree/campaign mechanics (not GitHub's platform
   data model) to `big-change-git-rules` (same plugin) instead — the two packs are deliberately
   disjoint (see Boundaries).

**Done when** the answer carries the claim + its grounding marker + citation, and any out-of-scope
ask is routed to the correct sibling. **NOT done** while a platform-behavior claim ships with no
citation, or this pack's own `bug-task-feature-mapping-nuances.md` findings get read as a ruling
rather than as grounding for one.

## The core finding (why this pack exists)

**GitHub's platform already offers native, GA mechanisms — Issue Types, sub-issues — that overlap
almost exactly with conventions this workspace built independently as labels and prose**
(`bug-task-feature-mapping-nuances.md` Findings 1–3). Neither this pack nor its findings decide
whether to migrate; they make the comparison possible for the first time, on cited facts instead
of assumption — the same discipline a 2026-07-17 review applied to a Linear-specific SPEC after two
assumed facts about that platform turned out wrong.

## Boundaries — this pack ANSWERS platform facts; it never decides or executes

- **This workspace's own git worktree/merge/campaign operational mechanics** → `big-change-git-rules`
  (same plugin, harness) — a disjoint pack; that one cites this workspace's own dated incidents, this
  one cites GitHub's platform docs. Neither restates the other's territory.
- **This workspace's TICKET/ADR/SPEC document contract** (frontmatter, mutability classes, required
  sections) → docs' `doc-writing-rules` — a different layer entirely (our document
  convention vs. GitHub's platform primitives).
- **Deciding whether to adopt Issue Types, sub-issues, or Issue Fields** → a future ADR, citing this
  pack's `bug-task-feature-mapping-nuances.md` findings — this pack states the platform fact, it
  does not ratify a change to ADR-0002 or doc-writing-rules.
- **Actually filing, triaging, resuming, or closing a work item** → docs'
  `file-bug`/`file-feature`/`file-task` skills, or the `issue-sorter` agent (same plugin) for
  unattended intake — this pack is consulted BY those, it does not perform their job.

## Extending this pack

A GitHub platform feature this pack doesn't yet cover, a citation gone stale (re-run that axis's
research wave, re-date it, note what changed rather than silently overwriting), or a genuinely new
eighth ask-class — route to `save-lessons`/`make-pack` where installed; otherwise apply
the discipline inline: one file per question type, every claim dated and sourced against a real
fetch, register the new axis in this table in the same change that adds the file.
