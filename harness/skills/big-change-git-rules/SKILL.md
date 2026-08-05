---
name: big-change-git-rules
description: >-
  This workspace's git campaign safety rules. Use for "gh reports a post-merge checkout error",
  "did the remote branch actually get deleted", "pull without clobbering a parallel session's
  work", "a git command said it worked but nothing changed", "solo commit or a full campaign",
  "resolve a stash-pop conflict safely", "was requiring PRs on main ever considered here",
  "push or PR-create Blocked by classifier in a subagent", "execute this rename safely", "what
  must land in the same change as a rename". Covers discard safety, delete-failures, who
  ships, the rename contract. NOT authoring artifacts (*-writing-rules), NOT choosing the new
  name (naming-rules), NOT full campaigns (CLAUDE.md).
disable-model-invocation: false
user-invocable: false
---

# big-change-git-rules — the estate's own git operational lessons, citable

Every rule below traces to a dated, real incident this workspace hit — grounding markers per
`pack-writing-rules`, most carrying the `[incident]` class (a real failure the rule would
have prevented, added 2026-07-15 for exactly this kind of evidence). The unit is the question a
reader arrives with, not a chronological log.

## Consult table

| Ask | Load |
|---|---|
| Worktree placement, the post-merge checkout error, discard safety | `references/worktree-mechanics.md` |
| Squash safety, the ten-branch delete-failure class, CI as the gate, auth-path consistency | `references/merge-semantics.md` |
| "A command said it worked but nothing changed" — the general pattern + six dated instances | `references/silent-failure-catalog.md` |
| Pulling onto a checkout a parallel session is using; classification, quarantine, conflict resolution | `references/parallel-session-reconcile.md` |
| Solo-main-direct vs. campaign; the branch-protection rejection; the close sequence in order | `references/campaign-decision-tree.md` |
| A seat's push/PR-create "Blocked by classifier"; who pushes, who opens the PR, who merges; scoping a dispatch brief's ship leg | `references/who-ships-what.md` |
| Executing a rename campaign — PR order, the eight-part per-rename contract, the blind eval-run parity gate, the rename incident catalog | `references/rename-execution-playbook.md` |

Seven files, flat, no subdirectories — at the 3–7 axis band's ceiling, so this table IS the
retrieval map (no separate INDEX.md; the enumerability ruling, `pack-writing-rules`).

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

## The core invariant (why all seven files exist)

**A command's own report of success is a claim, not evidence — the state it claims to have
produced must be independently re-read before the session proceeds as if the claim were true.**
Three of the seven files instantiate this at a different layer (a shell pipe, a text-edit call,
a git subcommand's quiet-success case, a hand-rolled argv parser, `git status` itself
under skip-worktree, and a dispatch sandbox's write redirection); two (worktree placement, the decision tree) are the
operational context the doctrine gets applied inside; who-ships-what bounds who may attempt the
ship operations in the first place; and the rename playbook applies it at campaign scale — the
blind re-measure, not the executor's care, is what proves a rename landed.

## Boundaries — this pack ANSWERS the lessons; it never runs a campaign

- **Actually execute a worktree campaign** → the workspace's own CLAUDE.md routing table (branch
  + worktree + PR), not this pack.
- **Run the mechanical checks this pack documents** → `scripts/gitignore_check.py` /
  `campaign_close.py` / `sync_main.py` (same plugin, `harness`) — this pack cites their incidents
  and design, it does not invoke them.
- **Author or review a skill/agent/hook/plugin** → the sibling `*-writing-rules` family
  (`skill-writing-rules`, `agent-writing-rules`, `hook-writing-rules`,
  `script-writing-rules`, `plugin-writing-rules`) — a distinct concern from git
  operational mechanics.
- **A drifted repo needing a full alignment campaign** → `clean-repo` (same plugin) — that
  skill's own "`.gitignore` is a record" razor is one of this pack's grounding incidents
  (`worktree-mechanics.md`), but the campaigns themselves are a different job.

## Extending this pack

A new dated incident that generalizes past this one workspace, a stale citation (a cited script
path or commit that moved), or an eighth axis genuinely distinct from the seven above — route to
`make-pack` where installed; otherwise apply the discipline inline: one file
per question type, every claim dated and sourced, register a new axis in this table in the same
change that adds the file.
