---
name: git-campaign-workflows
description: >-
  Answers how this workspace runs a git worktree campaign safely — placement, merge/branch-delete
  verification, pulling onto a parallel session's checkout, the solo-vs-campaign decision — from
  a dated incident corpus. Use for "gh reports a post-merge checkout error", "did
  the remote branch actually get deleted", "pull without clobbering a parallel session's work",
  "a git command said it worked but nothing changed", "solo commit or a full campaign", "resolve
  a stash-pop conflict safely", "was requiring PRs on main ever considered here". Covers discard safety, merge semantics (ten-branch delete-failure
  class, CI as gate), the silent-failure catalog (verify by re-reading), the reconcile protocol,
  the ADR-0002 decision tree. ANSWERS; never performs a git op on
  request — "delete this branch", "pull the latest", "merge and clean up" — sibling scripts or
  plain git/gh do that. NOT for authoring/reviewing skills/agents/hooks/plugins (the
  `*-authoring-standards` family); NOT running a campaign end-to-end (CLAUDE.md).
disable-model-invocation: false
user-invocable: false
---

# git-campaign-workflows — the estate's own git operational lessons, citable

Every rule below traces to a dated, real incident this workspace hit — grounding markers per
`pack-authoring-standards`, most carrying the `[incident]` class (a real failure the rule would
have prevented, added 2026-07-15 for exactly this kind of evidence). The unit is the question a
reader arrives with, not a chronological log.

## Consult table

| Ask | Load |
|---|---|
| Worktree placement, the post-merge checkout error, discard safety | `references/worktree-mechanics.md` |
| Squash safety, the ten-branch delete-failure class, CI as the gate, auth-path consistency | `references/merge-semantics.md` |
| "A command said it worked but nothing changed" — the general pattern + three dated instances | `references/silent-failure-catalog.md` |
| Pulling onto a checkout a parallel session is using; classification, quarantine, conflict resolution | `references/parallel-session-reconcile.md` |
| Solo-main-direct vs. campaign; the branch-protection rejection; the close sequence in order | `references/campaign-decision-tree.md` |

Five files, flat, no subdirectories — under the 3–7 axis band, so this table IS the retrieval
map (no separate INDEX.md; the enumerability ruling, `pack-authoring-standards`).

## Consult procedure

1. Classify the ask against the table; Grep the matching file for the term first, then Read that
   section — every file is a cited catalog, not a linear read.
2. Answer on the contract: **claim + its grounding marker's citation (the incident's date, the
   commit SHA where one landed, or the ADR/tool-contract source) + the failure mode it
   prevents.** A rule stated with no incident behind it is a guess wearing a citation.
3. Distinguish `[incident]` (a dated real failure, causal evidence the rule paid rent) from
   `[verified]` (a tool contract or ratified decision, checked directly) from `[ratified]` (a
   workspace decision, e.g. ADR-0002) — never present one as if it carried a stronger class's
   weight.
4. Route ANY ask to actually RUN a check to the mechanized scripts (same plugin,
   `scripts/gitignore_check.py` · `campaign_close.py` · `sync_main.py`) — this pack answers what
   the checks mean and why they exist; it does not execute them.

**Done when** the answer carries the claim + its grounding + the failure mode, and any
run-the-check ask is routed to the matching script. **NOT done** while a claim ships with no
incident or contract behind it, or a script's job is described instead of pointed at.

## The core invariant (why all five files exist)

**A command's own report of success is a claim, not evidence — the state it claims to have
produced must be independently re-read before the session proceeds as if the claim were true.**
Three of the five files instantiate this at a different layer (a shell pipe, a text-edit call, a
git subcommand's quiet-success case); the other two (worktree placement, the decision tree) are
the operational context the doctrine gets applied inside.

## Boundaries — this pack ANSWERS the lessons; it never runs a campaign

- **Actually execute a worktree campaign** → the workspace's own CLAUDE.md routing table (branch
  + worktree + PR), not this pack.
- **Run the mechanical checks this pack documents** → `scripts/gitignore_check.py` /
  `campaign_close.py` / `sync_main.py` (same plugin, `forge`) — this pack cites their incidents
  and design, it does not invoke them.
- **Author or review a skill/agent/hook/plugin** → the sibling `*-authoring-standards` family
  (`skill-authoring-standards`, `agent-authoring-standards`, `hook-authoring-standards`,
  `script-authoring-standards`, `plugin-authoring-standards`) — a distinct concern from git
  operational mechanics.
- **A drifted repo needing a full alignment campaign** → `repo-alignment` (same plugin) — that
  skill's own "`.gitignore` is a record" razor is one of this pack's grounding incidents
  (`worktree-mechanics.md`), but the campaigns themselves are a different job.

## Extending this pack

A new dated incident that generalizes past this one workspace, a stale citation (a cited script
path or commit that moved), or a sixth axis genuinely distinct from the five above — route to
`pack-forge` where installed; otherwise apply the discipline inline: one file
per question type, every claim dated and sourced, register a new axis in this table in the same
change that adds the file.
