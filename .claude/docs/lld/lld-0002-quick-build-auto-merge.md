---
doc-type: lld
id: lld-0002-quick-build-auto-merge
status: draft
version: 0.2.0
date: 2026-08-14
owner: kim.granlund
ticket: nonoun-plugins#244
adr: adr-0012 (proposed by this design — see Components C5)
---
# LLD — Quick-build auto-merge: pre-authorized merge on green for small dispatches (#244)

*Amended 2026-08-14 (v0.2.0) per docs:doc-checker's fix-then-ship review, before any
implementation: QB4 rebuilt as an ALLOW-list (was a deny-list — fail-open by construction);
QB3's ledger-region check made mechanical; C5's T4 leg dropped as unsound (an appended addendum
to an accepted ADR is class-legal) leaving the actor/mechanism fork to carry the ruling alone;
I2 step 1's prose ceiling replaced with `timeout 900`. Risks 2 and 3 repaired to match.*

**Verdict, head-first: NOT "skip the PR" — auto-merge on green.** Per Kim's binding
design-narrowing comment on #244 (2026-08-14): every dispatch still opens a PR, the fresh-context
critic still runs, `release_gate.py` still runs, CI still gates — the ONLY thing removed is the
human typing "merge" for a change shape that was pre-authorized. The fast path is additive: any
eligibility miss falls back to today's exact behavior (PR opened, human merges). The safety
machinery is never skipped — the session evidence Kim cites (#180 host-checkout, #191
reuse-identity, PR #217 `dmi:true`) is precisely why critic+gate stay unconditional.

The five charter rulings, verdict-first:

1. **Eligibility** — a conjunctive, fail-closed predicate QB0–QB7 (Components C1); every
   conjunct is a checkable command, no judgment calls at merge time.
2. **Mechanics** — one new stage in dispatch-ticket Phase 5, between today's stage 2 (PR opened)
   and stage 3 (retirement): evaluate QB, and only on all-green run the merge sequence
   (Interfaces I2). Any QB miss → today's behavior unchanged.
3. **Audit trail** — the PR remains the record, nothing removed; auto-merge ADDS a dated
   Findings comment carrying the criteria snapshot + merge SHA (Data D1). Kim intervenes by
   declining at the batch confirm, revoking the QB0 grant, or reverting the merged PR.
4. **ADR** — a NEW narrow ADR-0012 (proposed), not an ADR-0002 amendment and not a supersession.
   Explicit ruling with reasoning in Components C5: the existing "solo single-file fixes may
   still commit to main" precedent does NOT cover a dispatched-agent auto-merge.
5. **Where it lives** — dispatch-ticket Phase 5 + build-lead's return contract + build-feature's
   human-facing note, PLUS two surfaces the charter's list didn't enumerate but analysis found
   load-bearing: mobilize-chores' auto-mode ceiling ("PR-opened, never merged", body line ~135)
   and the workspace CLAUDE.md routing-table row that states the same ceiling. Both currently
   contradict this feature and must be amended in the same change (stale context = defect).

## Components

### C1 — The eligibility predicate (QB0–QB7, all must hold, fail-closed)

Evaluated by the dispatch itself (the seat running dispatch-ticket Phase 5) immediately after
the PR opens. **Any conjunct that errors, times out, or is indeterminate → NOT eligible** —
report which QB failed in the retirement handoff and fall back to human merge. Never retried
into eligibility.

| # | Conjunct | Exact check (git-native backend) |
|---|---|---|
| QB0 | **Explicit grant** | The sealed dispatch prompt contains the literal line `auto-merge: authorized`, placed by the caller (mobilize-chores `auto` step 5, a `/goal` wrapper, or Kim's own dispatch). Never inferred from "unattended" — same doctrine as mobilize-chores' own `auto` token (2026-08-11: explicit, never inferred). Absent → today's behavior, no QB evaluation at all. |
| QB1 | **size:small** | The record carries the `size:small` label (`gh issue view <id> --json labels`); file backend: the ticket's Size field reads `small`. This is dispatch-ticket Phase 4's existing materiality floor, reused — no new size taxonomy. |
| QB2 | **Single plugin context** | Every path in `git diff --name-only origin/main...HEAD` sits under ONE top-level plugin directory. Any path at repo root, under `.claude/docs/`, `.github/`, or a second plugin → ineligible. |
| QB3 | **Single substantive file** | Let R = {`<plugin>/.claude-plugin/plugin.json`, `<plugin>/README.md`} (the mandatory version-bump + footer-ledger ride-alongs). `changed \ R` has exactly ONE member. The ride-alongs are themselves diff-checked, mechanically: the `plugin.json` diff's changed lines all match `"version"`; and **every changed hunk in `README.md` falls at or below the version-ledger heading** (`git diff -U0 origin/main...HEAD -- <plugin>/README.md`, compare each hunk's new-file start line against the ledger heading's line number). A hunk touching anything above that heading — or a README with no ledger heading found — is indeterminate → ineligible. |
| QB4 | **No contract change — ALLOW-list, fail-closed by construction** | The substantive file must MATCH one of exactly three eligible classes; anything that does not match is ineligible **because it is unlisted**, not because a deny-list names it. The three classes: (a) `<plugin>/skills/*/SKILL.md` where no changed hunk falls inside the frontmatter block (first line through the closing `---`) — a body-only edit; (b) `<plugin>/skills/*/references/*.md`; (c) `<plugin>/scripts/*.{py,mjs,js}` — implementation and/or its `selftest`. Nothing else is eligible, ever, including classes no one thought to enumerate. Named here only to orient a reader, never as the rule: `hooks/` (ANY file in it, not just `hooks.json`), `commands/*.md`, `agents/*.md`, any `evals.json`, anything under `.claude-plugin/`, any `CLAUDE.md`, anything under `.claude/docs/`, and **any file carrying a frontmatter block outside class (a)** — all fall outside the allow-list and are therefore out. A new artifact kind added to the estate tomorrow is ineligible on the day it appears, with no edit to this predicate. Cross-plugin edges are already excluded by QB2. |
| QB5 | **Critic green** | A fresh-context checker pass ran on this change within this dispatch and returned zero blocker/major findings — REQUIRED for auto-merge regardless of artifact class. Deliberately stricter than the baseline semantic-edit invariant (pure code normally rides its test gates alone): auto-merge always pays for a critic. Evidence: the checker verdict quoted in the Findings write-back. No recorded verdict → ineligible. |
| QB6 | **Gate green, twice** | `release_gate.py <plugin>` exit 0 locally, AND every CI check on the PR green (`gh pr checks <pr> --watch`, bounded — see I2 step 1). Local green alone is not enough; CI is ADR-0002's own enforcement layer. |
| QB7 | **No overlapping open PR** | No other OPEN PR's changed files touch the same plugin (`gh pr list --state open --json number,files`). Overlap → human merges (the integration-notes discipline already in Phase 5 stage 2 stays the arbiter). |

Worth stating: #244 itself is `size:big` with contract changes on every touched surface — the
build that ships this feature is NOT eligible for its own fast path. Kim merges it, and that
merge is also the ADR-0012 ratification act (C5).

### C2 — dispatch-ticket Phase 5: the mechanical change

Today's stage 2 ends with the PR open, `in-flight` removed, and stage 3 asserting "this seat
never merges its own PR, per ADR-0002's human-gated merge." The change:

- **New stage 2b — auto-merge eligibility.** After stage 2 completes: if QB0 absent, skip
  silently (zero new behavior). If QB0 present, evaluate QB1–QB7; all green → run the merge
  sequence (I2); any miss → state the failed conjunct in the retirement handoff and proceed to
  stage 3 exactly as today.
- **Stage 3's merge line is amended, not deleted:** "this seat never merges its own PR" gains
  the carve-out "— except under ADR-0012's quick-build predicate, stage 2b, when the sealed
  dispatch carried the explicit grant." The environment-clean line gains a fourth possible
  state for the branch axis: "auto-merged at <SHA>, remote branch verified deleted
  (campaign_close)."
- **Stage 4's typed handoff** gains the auto-merge fields (I3) when stage 2b fired.
- Phase 6 is unchanged in structure: `Closes #<id>` auto-closes the issue on merge; the
  read-back proceeds as written.
- dispatch-ticket's frontmatter `description` does NOT change (behavior-body change only) →
  no evals.json churn, no reciprocal-fence sweep owed. Verify with `/check-routing teamwork`
  at build anyway (cheap).

### C3 — build-lead return contract delta

`agents/build-lead.md`'s Phase-5-stage-4 gloss paragraph gains one sentence: a dispatch whose
stage 2b fired carries the merge SHA, the campaign_close result line, and the QB snapshot
reference through verbatim — a report missing them when auto-merge fired is dispatch-ticket's
contract gap to name. No tool, model, or description change.

### C4 — Human-facing docs (three surfaces, same change)

1. `build-feature/SKILL.md` body: one plain paragraph — an eligible, explicitly-granted small
   dispatch may return ALREADY MERGED (PR link + merge SHA), so a human is never surprised by a
   closed PR they didn't click.
2. `mobilize-chores/SKILL.md` body (~line 135): the ceiling amends from "PR-opened, never
   merged" to "PR-opened by default; a dispatch meeting ADR-0012's quick-build predicate, with
   the grant line this step placed, may land merged — everything else still waits for a human."
   The `auto` path's step 5 dispatch prompt is where the QB0 grant line gets placed.
3. Workspace `CLAUDE.md` routing-table row for mobilize-chores: same ceiling wording update
   ("ceiling PR-opened, never merge" → names the ADR-0012 carve-out). Stale-context repair in
   the same change, per house doctrine.

### C5 — The ADR ruling: new narrow ADR-0012, with explicit precedent analysis

**Does the existing precedent cover a dispatched-agent auto-merge? No — stated explicitly:**

- The precedent text "solo single-file fixes may still commit to main" lives in the workspace
  CLAUDE.md routing table, NOT in ADR-0002's ratified Decision text. ADR-0002's ratified text
  says "PRs become the merge gate for campaigns" — it nowhere states WHO clicks merge. The
  "human-gated merge" doctrine exists only as operational gloss: dispatch-ticket stage 3's
  line and mobilize-chores' 2026-08-11 auto-mode ceiling.
- The precedent's actor is a solo, human-supervised session; its mechanism is committing to
  main with NO PR at all. The new path's actor is an unattended dispatched agent; its
  mechanism KEEPS the PR and every gate. Different actor class + different mechanism = the
  precedent language does not cover it. Generalizing it is a new ruling, not a citation.

**Kim's #244 comment asks to "size the ADR-0002 amendment accordingly." Answered directly: the
right size is a NEW narrow ADR-0012, not an amendment to ADR-0002** — and it rests on one
argument, not two.

State plainly what is NOT being claimed: "ADR-0002 is accepted, so it cannot be touched" is not
a reason. T4 is *append-only, supersede never edit* — a dated APPENDED addendum to an accepted
ADR is class-legal, exactly what append-only permits. That leg is dropped; it never carried
weight.

The leg that stands alone is the fork itself, and it is enough. **Different actor class** — a
dispatched agent merging under a pre-placed grant, not a solo human at a keyboard. **Different
mechanism** — this path KEEPS the PR and every gate, where the cited precedent skips the PR
entirely. And the choice **rewrites two previously-RULED operational lines**: dispatch-ticket
stage 3's "this seat never merges its own PR" and mobilize-chores' 2026-08-11 "ceiling is
PR-opened, never merged." Genuine alternatives existed (skip the Issue / skip the PR /
auto-merge / status quo) and Kim's 2026-08-14 comment chose one. A resolved fork that rewrites
ruled lines is precisely what passes the ADR-default-no test — and rewriting ruled lines with no
decision record is exactly the "silent SKILL.md edit" #244's own Scope section warns against.

Not a supersession either: ADR-0002 Decision 1 stands, arguably strengthened, since the quick
path keeps the PR where the old precedent skipped it.

**ADR-0012 (proposed)** — Context: #244 + Kim's comment + this LLD. Decision: the QB0–QB7
predicate authorizes a dispatched seat to merge its own PR; PRs remain the merge gate for all
campaigns (ADR-0002 D1 cited, unamended); the grant is explicit and revocable. Consequences:
the two operational glosses and the CLAUDE.md row update; reverting a quick-build is a standard
PR revert. Ratification: Kim merging the build PR flips proposed→accepted (T4-consistent: the
flip is the ratification act). If Kim instead rules at review time that no ADR is warranted,
the fallback is the charter's addendum shape — the criteria stated in dispatch-ticket citing
ADR-0002's precedent — but this design recommends the ADR and says so plainly.

## Interfaces

### I1 — The grant line (caller → dispatch)

One literal line in the sealed dispatch prompt: `auto-merge: authorized`. Placed only by:
mobilize-chores running with the `auto` token, a `/goal` loop wrapper Kim configured, or Kim
directly. dispatch-ticket treats its absence as "this stage does not exist."

### I2 — The merge sequence (runs only on QB0–QB7 all green)

1. `timeout 900 gh pr checks <pr> --watch --fail-fast` — the ceiling is the `timeout` command
   itself, not a prose promise. Exit 0 is the ONLY pass. Exit 124 (timed out) and any non-zero
   check failure are both **ineligible** → report the exit code, fall through to human merge. A
   timeout is never read as an implicit pass, and the watch is never re-run to chase a green.
2. `gh pr merge <pr> --squash` — squash is the house shape for small single-file landings (the
   ledger-style one-liners with `(#NNN)` on main); campaign merge commits remain the big-change
   shape, unaffected.
3. Verify by SHA, never trust the command's print: `gh pr view <pr> --json state,mergeCommit`
   must show `MERGED` + a non-empty SHA.
4. `python3 harness/scripts/campaign_close.py <pr> --repo <owner/repo> --gate <plugin-root>` —
   re-verifies MERGED, deletes the remote branch, RE-verifies deletion (the ten-branch
   silent-delete-failure class), gates the touched plugin.
5. Findings write-back (D1), then Phase 6 read-back as today.

Failure at step 2 (e.g. the permission classifier denies `gh pr merge` — see Risks R1) or any
later step → named blocker `auto-merge-denied` / `auto-merge-unverified` in the handoff, PR
left standing for a human, claim NOT re-released (the PR is open and linked — today's normal
end state). One attempt; never force, never retry past the first denial.

### I3 — Return contract fields (stage 4, only when 2b fired)

Appended to the existing typed handoff (PR URL, Findings comment URL, environment-clean line):
`merge-sha: <sha>` · `campaign-close: <its summary line>` · `qb-snapshot: <the eight conjunct
results>`. build-lead relays verbatim (C3).

## Data

### D1 — The Findings audit comment (git-native: `gh issue comment`)

Dated entry, posted after I2 step 4: "Auto-merged under ADR-0012 quick-build predicate" + the
QB0–QB7 snapshot (each conjunct's observed value, e.g. the substantive file's path, the critic
verdict quote, both gate results) + merge SHA + campaign_close summary. This is the audit
trail's ADDITION; nothing existing is removed — PR body, gate output, critic verdict, and
integration-notes line all stand as today.

### D2 — Build-slice manifest (the plan the builder executes from)

| # | Slice | Files | Depends on |
|---|---|---|---|
| 1 | ADR-0012 authored (proposed) | `.claude/docs/adr/0012-quick-build-auto-merge.md` | this LLD approved |
| 2 | Phase 5 stage 2b + stage 3 amendment + stage 4 fields | `teamwork/skills/dispatch-ticket/SKILL.md` | 1 |
| 3 | Return-contract sentence | `teamwork/agents/build-lead.md` | 2 |
| 4 | Human-facing notes + ceiling amendments | `teamwork/skills/build-feature/SKILL.md`, `teamwork/skills/mobilize-chores/SKILL.md`, workspace `CLAUDE.md` | 2 |
| 5 | teamwork version bump + README ledger | `teamwork/.claude-plugin/plugin.json`, `teamwork/README.md` | 2–4 |
| 6 | Fresh-context critic pass over every prompt-carrying edit (slices 2–4), then `release_gate.py teamwork`, `/check-routing teamwork` | — | 2–5 |

One PR carries all six (the ADR rides with the edits it authorizes; Kim's merge ratifies it).
Acceptance predicates, checkable: doc_lint green on ADR-0012 and this LLD; `release_gate.py
teamwork` exit 0; grep proves the old ceiling wording ("never merged"/"never merge") survives
nowhere except ADR/history contexts; dispatch-ticket's description byte-identical to before
(no routing churn); critic verdict recorded with zero majors.

## Risks

1. **The permission classifier blocks `gh pr merge` in unattended goals** (recorded memory,
   2026-08). Detection: I2 step 2 denied at first live use. Mitigation: this is a deployment
   PREREQUISITE, not a design gap — the build PR's notes must name the required settings
   allow-rule (scoped to `gh pr merge`, ideally to the goal context Kim arms); until Kim adds
   it, the fast path degrades gracefully to today's behavior via the `auto-merge-denied`
   branch. Fail-safe by construction.
2. **Predicate misclassification lets a contract change slip.** Mitigation: QB4 is an
   ALLOW-list of three classes, so an unanticipated artifact kind is ineligible by construction
   rather than by someone remembering to deny it — the failure mode of a deny-list (a class
   nobody listed slips through) cannot occur here; the worst case is a legitimate small change
   falling back to human merge, which is today's behavior. Add fail-closed on any indeterminate
   diff; QB2/QB3 bound blast radius to one substantive
   file in one plugin; the critic (QB5) is unconditional. Detection: post-hoc — every
   auto-merge carries the D1 snapshot, so an audit greps `qb-snapshot` comments against the
   actual diffs.
3. **CI-watch flakiness or timeout stalls the dispatch.** Mitigation: the `timeout 900` wrapper
   on I2 step 1 bounds it mechanically (exit 124 = ineligible), with fall-through to human
   merge; the PR is already open, so nothing is lost — only the human wait returns.
4. **Concurrent open PRs on the same plugin conflict at merge.** Mitigation: QB7 excludes
   overlap outright; serial chains (mobilize-chores' own conflict-avoidance step) remain the
   primary defense.
5. **Skill edited without the ADR ratified** (ordering hazard). Mitigation: single PR carries
   ADR + edits; the ADR ships `proposed` and Kim's merge is the ratification flip — no window
   where the carve-out is live but unruled. If the PR is declined, nothing landed.
6. **Non-decision noted (no ADR here):** the squash-vs-merge-commit method choice (I2 step 2)
   is a house-shape observation, not a ratified fork — if Kim prefers merge commits for
   quick-builds, it's a one-flag edit with no doctrinal weight.
