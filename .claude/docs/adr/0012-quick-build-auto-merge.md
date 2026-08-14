---
doc-type: adr
id: adr-0012
status: proposed
date: 2026-08-14
owner: kim.granlund
---
# ADR-0012 — Quick-build auto-merge: a dispatched seat may merge its own PR on a pre-authorized, all-green predicate

## Context

Issue #244 reported the pain plainly: small, iterative changes have to run the full Issue → Build
→ PR → Merge stack, and that stack makes small work take forever. The seed asked for a "quick
build" mode that bypasses the ceremony, leaving open whether that meant skipping the Issue, the
PR, or both.

Measuring the actual stack against one night's session evidence (Kim, #244 comment, 2026-08-14)
found the bottleneck is not where the seed pointed. Every dispatch that session ran: worktree
isolate → build → `skill_lint` → fresh-context critic → `release_gate` → open PR → Kim's one-line
"merge" → `campaign_close`. The gate run and the critic pass cost the wall-clock, and both exist
because of specific incidents this repo has actually hit — #180's host-checkout bug caught by a
critic, #191's reuse-identity bug, PR #217's `dmi:true` catch that would otherwise have silently
broken agent preloading. A fast path that skips the PR saves seconds; a fast path that skips the
critic or the gate is the shape this repo's own incident history argues hardest against.

What genuinely costs time is a human typing "merge" for a change shape that was never going to be
rejected. Kim's comment named the narrower design and asked the build to "size the ADR-0002
amendment accordingly."

Two operational lines already ruled the opposite way and would have to be rewritten by any such
change: `dispatch-ticket` Phase 5 stage 3's "this seat never merges its own PR," and
`mobilize-chores`' 2026-08-11 unattended ceiling, "PR-opened, never merged" (restated in the
workspace CLAUDE.md routing table). Rewriting ruled lines with no decision record is exactly the
"silent SKILL.md edit" #244's own Scope section warned against.

Design: `.claude/docs/lld/lld-0002-quick-build-auto-merge.md` (v0.2.0, amended after an
independent `docs:doc-checker` review before any implementation).

## Decision

1. **Auto-merge on green, never "skip the PR."** Every dispatch still opens a PR; the
   fresh-context critic still runs; `release_gate.py` still runs; CI still gates. The only step
   removed is the human typing "merge." ADR-0002 Decision 1 (PRs are the merge gate for
   campaigns) stands unamended and is arguably strengthened — this path keeps the PR where the
   pre-existing "solo single-file fixes may still commit to main" precedent skips it entirely.

2. **A conjunctive, fail-closed predicate QB0–QB7 authorizes it**, evaluated by the dispatched
   seat immediately after the PR opens (LLD C1 is the normative table; summarized here): an
   explicit grant line (QB0), `size:small` (QB1), one plugin (QB2), one substantive file plus
   the version/ledger ride-alongs (QB3), the substantive file inside the QB4 allow-list, a green
   fresh-context critic (QB5), a green local gate AND green CI (QB6), no overlapping open PR
   (QB7). Any conjunct that fails, errors, times out, or is indeterminate → NOT eligible; the
   dispatch falls back to today's exact behavior (PR opened, human merges) and names the failed
   conjunct in its handoff. Never retried into eligibility.

3. **QB4 is an ALLOW-list, not a deny-list.** Exactly three file classes are eligible: a
   `SKILL.md` body-only edit (no hunk inside the frontmatter block), a `skills/*/references/*.md`,
   and a `scripts/*.{py,mjs,js}` (implementation and/or its selftest). Everything else is
   ineligible **because it is unlisted** — including artifact kinds nobody has thought of yet.
   A deny-list would be fail-open by construction; this is fail-closed by construction. The
   worst case of a mistake here is a legitimate small change waiting for a human, which is
   today's behavior.

4. **The grant is explicit, revocable, and never inferred.** The literal line
   `auto-merge: authorized` must appear in the sealed dispatch prompt, placed by the coordinator
   (`mobilize-chores` running with its `auto` token, a `/goal` wrapper Kim configured, or Kim
   directly) — the same doctrine as the `auto` token itself (2026-08-11: explicit, never
   inferred). Absent → the stage does not exist and nothing about today's behavior changes.
   Removing the grant line is the whole revocation mechanism.

5. **The audit trail grows; nothing is removed.** PR body, gate output, critic verdict, and the
   integration-notes line all stand as today. Auto-merge ADDS a dated Findings comment carrying
   the full QB0–QB7 snapshot, the merge SHA, and the `campaign_close.py` result.

6. **The merge sequence is verified, not trusted** (LLD I2): `timeout 900 gh pr checks --watch
   --fail-fast` (exit 124 is ineligible, never an implicit pass) → `gh pr merge --squash` →
   confirm `MERGED` plus a non-empty merge SHA by re-query → `campaign_close.py`. One attempt;
   a denial or an unverified state is a named blocker, never a retry or a force.

## Rejected alternatives

- **Skip the PR for `size:small` dispatches** (the seed's leading reading): removes ADR-0002's
  audit trail and CI enforcement to save the seconds between "gates green" and "merged" — the
  measured non-bottleneck. Rejected on Kim's #244 comment.
- **Skip the critic and/or the gate to go faster**: the only version that would save real
  wall-clock, and the one three recorded incidents (#180, #191, PR #217) argue against directly.
  QB5 deliberately goes the other way — auto-merge always pays for a critic, even for pure code
  that the baseline semantic-edit invariant would let ride its test gates alone.
- **Skip minting the Issue for trivial changes**: unaddressed by this decision and not required
  by the pain report; the record is what the Findings write-back and `Closes #<id>` hang off.
- **A dated addendum appended to ADR-0002 instead of a new ADR.** This was legal — T4 is
  "append-only, supersede never edit," and appending to an accepted ADR is exactly what
  append-only permits, so "ADR-0002 is accepted" was never a reason to avoid it. It was rejected
  on the fork itself: a different actor class (a dispatched agent merging under a pre-placed
  grant, not a solo human at a keyboard) and a different mechanism (this path KEEPS the PR where
  the cited precedent skips it) make this a new ruling rather than a citation of an old one — and
  it rewrites two previously-ruled operational lines. That clears the ADR-default-no bar on its
  own; the appended-addendum framing would have buried a real fork inside an unrelated decision.
- **Widening eligibility past one file / one plugin**: blast radius is the only thing standing
  between a predicate bug and an unreviewed merge. Deliberately narrow at first ship.

## Consequences

- `dispatch-ticket` Phase 5 gains stage 2b (evaluate, and only on all-green merge); stage 3's
  "this seat never merges its own PR" gains the carve-out; stage 4's typed handoff gains
  `merge-sha` / `campaign-close` / `qb-snapshot` when 2b fired. `build-lead` relays them verbatim.
- `mobilize-chores`' unattended ceiling and the workspace CLAUDE.md routing-table row are
  amended in the same change as the feature — no window where the capability is live while two
  house documents say it cannot be.
- `build-feature`'s human-facing body states plainly that an eligible, explicitly-granted small
  dispatch may return ALREADY MERGED, so no human is surprised by a closed PR they never clicked.
- **Deployment prerequisite, not a design gap:** the unattended permission classifier blocks
  `gh pr merge` today (recorded 2026-08). Until Kim adds a scoped allow-rule, every attempt
  degrades gracefully through the `auto-merge-denied` branch to today's behavior. The feature is
  fail-safe before that rule exists, and inert.
- Reverting a quick-build is an ordinary PR revert; the D1 Findings snapshot makes post-hoc
  auditing a grep (`qb-snapshot` comments against the actual diffs).
- The build that ships this decision is itself ineligible for the path it creates — `size:big`,
  multi-file, multi-plugin, contract-changing, touching an ADR and a CLAUDE.md. It fails QB1,
  QB2, QB3, and QB4 independently. Kim merging that PR is the ratification act that flips this
  ADR `proposed` → `accepted`; until then the carve-out is drafted, not ruled.
