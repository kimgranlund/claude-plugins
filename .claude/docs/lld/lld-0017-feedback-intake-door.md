---
doc-type: lld
id: lld-0017-feedback-intake-door
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
ticket: nonoun-plugins#622
spec: none — gh#622's own Acceptance section carries the checkable criteria, and idr-0008
  (LOCKED) already carries the ruled claim plus the named lean (feedback-intake door over an
  adoption probe, gh#622's own follow-up comment); a standalone SPEC would restate what the
  ticket and the locked IDR already state (same routing test lld-0008/lld-0009/lld-0013/lld-0015
  applied).
---
# LLD — the feedback-intake door: tag, gate, and count foreign-origin records (#622)

**Verdict, head-first:** no new door. The three GitHub issue templates
(`.github/ISSUE_TEMPLATE/{bug,feature,task}.yml`) already ARE the door — a real external filer
can already reach the spine today. What's missing, and what this build ships, is the other three
things idr-0008's Claim actually requires: **recognize** a foreign-origin record (an operational
proxy for clause (a), resolved below), **tag** it (`user-signal` label, applied wherever the
git-native backend mints or resumes a record), and **count** it VISIBLY (`check-state`'s
`ticket_state.py` collector gains an all-state `user-signal` tally, surfaced in its Counts
section). T3 routing (ADR-0021: foreign authors pass the friendlies gate before anything else) is
already `watch-tickets`' existing hold-first-filing behavior — nothing new to build there, only
to name and tag. Two plugins, one PR: docs (owns the capture skills + the shared provenance
convention) and harness (owns `watch-tickets`/`issue-sorter`, the actual GitHub-authorship-aware
surface, and `check-state`'s collector).

## Resolution 1 — Clause (a) measurability: an operator-login proxy, not install telemetry

**Resolved:** "foreign-origin" is operationalized as **the git-native record's filing author's
GitHub login differs from the estate operator's own login**, recorded once at
`.claude/ops/friendlies.json`'s existing `policy.confirmed_by` field (`"kimgranlund"` today — no
new field minted, the value already exists and is already the single human this estate's
`friendlies.json` bootstrap evidenced as its own operator/maintainer). This is deliberately
narrower than idr-0008's full Claim (which also reads "a party other than this estate's own
seats" as covering a future SECOND trusted human collaborator) — chosen because it is the one
thing `gh issue view --json author` can answer with zero ambiguity today, on a single-operator
estate, with no new state to bootstrap. The check re-derives correctly the day a second operator
is added to `policy.confirmed_by` (a list, not just a scalar) — out of scope here, named as Risk
R-2 below, not built.

**Rejected — install/clone/star adoption signal (idr-0008's clause (a) sibling reading).**
Named explicitly in idr-0008's own Open questions as possibly reducing the definition to
clauses (b)/(c) at lock time "without publishing infrastructure the estate doesn't yet have" —
that infrastructure (a package registry, a download counter) does not exist in this estate, and
the ticket's own dispatch instructions rule the same lean: "don't promise install telemetry that
doesn't exist." The feedback-intake door instrument therefore counts (b) and (c) only — a
foreign-authored record, and a foreign-authored comment (Resolution 4) — never adoption counts.

**Rejected — treating every non-operator `friendlies.json` entry as "estate."** Would silently
undercount: a future second trusted collaborator who is not the operator is still, per idr-0008's
literal Claim, not "this estate's own seats." The operator-login check stays correct in that
future case without modification — trust (friendlies membership, which only gates hold-vs-mint)
and estate-membership (who counts as "us" for user-signal purposes) are kept as two independent
axes, never conflated into one.

## Resolution 2 — Where the tag is applied: one convention, stated once, restated at each surface

**Resolved:** the tagging rule is authored once, canonically, in
`docs/skills/doc-writing-rules/references/backend-resolver.md` (the existing seven-operation
adapter-interface table's home) as a new "Provenance tagging" section — Option B (git-native)
only; Option A (file backend) has no filing-author concept to compare, Option C is deferred (its
adapter's own `read`/`create` operations don't yet surface a foreign-author field, named as a gap
rather than built around). `harness:watch-tickets` cannot preload a docs-plugin file (the
plugin-boundary rule this skill's own existing text already states for the payload-contract
restatement above it: "docs' skills are a different plugin — not preloadable across that
boundary — so the minted-record shape they own is stated here directly rather than restated from
a preload") — so `watch-tickets` gets its OWN short restatement of the identical rule, citing
`idr-0008`/`adr-0021` by id, not the docs file by path. This is the same restated-not-preloaded
shape the skill already uses for the record's payload contract one paragraph above where the new
text lands — not a new pattern.

**Applied at four mint/resume points**, listed once here, not repeated per file below:

1. `harness/skills/watch-tickets/SKILL.md` step 4 (trusted-author direct mint).
2. The approval-mint flow described in `harness/agents/issue-sorter.md`'s own
   approve-a-held-item `<example>` (a held item, by construction, was foreign at filing time —
   the approval mint always tags, no login comparison needed there since the hold itself already
   proved foreign origin).
3. `docs/skills/file-bug/SKILL.md` Phase 4 / `file-feature/SKILL.md` Phase 5 /
   `file-task/SKILL.md` Phase 4 — Option B record creation (a citation-only paragraph: these
   skills' own `gh issue create` calls almost always mint AS the operator's own authenticated
   identity, so the check is close to a no-op on FRESH creates from these three skills today; it
   is included for uniformity and because a resumed id — case 4 below — is the real payoff).
4. The same three docs skills' Phase 1 (resume-by-id): a record resumed on the git-native backend
   is read back (`gh issue view`) regardless; if its `author.login` differs from
   `policy.confirmed_by` and it lacks the label, apply it there too — the backfill safety net
   for a record minted before this feature shipped, or minted by any path that didn't yet tag it.

**Mechanics, restated once (both watch-tickets and the docs skills follow the same shape the
existing missing-label fallback already documents for kind/severity labels):** `gh issue edit
<id> --add-label user-signal`; if the label does not exist yet, `gh label create user-signal
--color 1D76DB --description "provenance: filed by a login other than the estate operator
(idr-0008, adr-0021)"` once, then retry the edit — never worked around or skipped, the same
fallback `file-task`'s SKILL.md already documents for its own kind label and `watch-tickets`'
Scope section states as this agent's own responsibility (docs' capture skills don't document a
missing-label path themselves, so, per that existing text, the skill applying the label owns the
create-once fallback).

## Resolution 3 — T3 routing: name it, don't rebuild it

**Resolved:** no new trust-gate mechanics. `watch-tickets` step 5 (an author not on
`friendlies.json` → hold, `needs-triage-approval` label, `held-items.md` entry, no record
minted) is already ADR-0021's T3 realized in full — "passes the friendlies gate before it is
even handled as T2; may trigger triage only, never dispatch" is exactly steps 5+6's existing
shape (triage classification, never execution). The only change earned here is naming it: one
sentence added to `watch-tickets`' step 3 (the trust-check itself — the actual gate-entry point,
a more precise home than the Scope section for a rule about what THIS step already does) citing
`adr-0021`'s T3 tier as what steps 5–6 already implement, so a future reader doesn't have to
re-derive the mapping. This is
deliberately the smallest possible edit at this surface — the anti-matrix rule idr-0008's own
Claim invokes ("reuse is the default and a new door owes job evidence") cuts the other way too:
an ALREADY-CORRECT mechanism owes no rebuild, only a citation.

## Resolution 4 — Counting: check-state's existing ticket collector, not a new trend file

**Resolved:** `check-state` over a standalone trend file. The ticket's own instruction offers
either; `check-state`'s `ticket_state.py` is already the live, run-on-demand instrument a human
or agent actually reads for "what's the state of things," and idr-0008's Proof condition is a
threshold event ("the first foreign-origin record… routing through the spine") a live collector
answers more directly than a file nobody has cause to open. `ticket_state.py` gains one new,
ALL-STATE (not just open) query: `gh issue list --label user-signal --state all --json
number,state,createdAt --limit 500`, tallied into `{"total": N, "open": [...], "closed": [...]}`
under a new `user_signal` key in its collected JSON — deliberately independent of the existing
`classify_issues()` open-only 200-row sweep (a closed, already-shipped foreign report must still
count; the existing open-issue collector would silently drop it the moment it's closed).
`check-state`'s SKILL.md Output-contract step 5 (Counts) gains one line: `user-signal records: N
total (M open)`. `state_diff.py` is untouched — it snapshots only the fixed `SLOT_KEYS` it
already declares (`issues`/`prs`` numbers), so the new `user_signal` key rides along in the raw
collector JSON without needing a diff-schema change; the Counts line reads the raw collector
output directly, same as every other Counts line already does.

**Explicit feedback comments (idr-0008 clause (b)'s comment half, per the ticket's own
measurability lean — "foreign-author records + explicit feedback comments").** Deferred, named
as Risk R-3 below rather than built: a foreign-authored COMMENT on an existing (not
foreign-filed) issue has no cheap `gh` query today (comments carry no queryable label; a sweep
would mean paging every open+recent-closed issue's comment list and diff-ing authors against
`friendlies.json` — real cost, real API-rate exposure, and no existing collector shape to extend
without inventing one). The minimal-first-instrument doctrine idr-0008 itself invokes ("the
smallest thing the ruling makes real, not a platform") argues for shipping the cheap half now
(foreign-authored records — mechanizable in one `gh` call) and naming the comment half as a named
follow-up rather than paying its cost inside this ticket.

## Components

1. `docs/skills/doc-writing-rules/references/backend-resolver.md` (edited, new section) —
   Resolution 2's canonical statement.
2. `docs/skills/file-bug/SKILL.md`, `file-feature/SKILL.md`, `file-task/SKILL.md` (edited,
   body-only) — Resolution 2, points 3–4.
3. `harness/skills/watch-tickets/SKILL.md` (edited, body-only) — Resolution 2 points 1–2,
   Resolution 3.
4. `harness/agents/issue-sorter.md` (edited, body-only) — Resolution 2 point 2's one-line
   cross-reference in the existing approve-a-held-item `<example>` commentary.
5. `harness/skills/check-state/SKILL.md` (edited, body-only) — Resolution 4's Counts line.
6. `harness/skills/check-state/scripts/ticket_state.py` (edited) — Resolution 4's collector
   query + selftest fixtures.
7. `docs/.claude-plugin/plugin.json` + `docs/README.md` — version bump + ledger line.
8. `harness/.claude-plugin/plugin.json` + `harness/README.md` — version bump + ledger line.
9. This LLD (`lld-0017-feedback-intake-door.md`) — doc_lint-clean.

No `object_vocab`/naming-manifest change: `user-signal` is a GitHub label, not a skill/agent/
plugin name under ADR-0011's grammar.

## Interfaces

- **`backend-resolver.md`'s Provenance-tagging section → `watch-tickets`/`file-bug`/`file-feature`
  /`file-task`:** the canonical statement; each citing surface restates only the mechanics it
  needs (a `gh` call shape), never the rationale — Resolution 2's plugin-boundary discipline.
- **`watch-tickets` step 3 → `adr-0021`'s T3 tier:** cited by id, never restated — Resolution 3.
- **`ticket_state.py`'s `user_signal` key → `check-state`'s Counts section:** a new top-level
  collector field, read directly by the report step; no `state_diff.py` schema change needed
  (Resolution 4).

## Data

One new GitHub label (`user-signal`, color `1D76DB`) plus label edits on existing/future issues —
no new file-based state. `ticket_state.py`'s collected JSON gains one new top-level key
(`user_signal: {total, open, closed}`) — additive, no migration, no existing key's shape changes.

## Risks

- **R-1 (the operator-login proxy undercounts a Kim-relayed report).** A report Kim hears
  out-of-band and files himself via `/file-bug` reads as operator-authored on GitHub regardless
  of who really reported it — Resolution 2 point 3 names this directly rather than silently
  presenting the count as complete. Detection: the Counts line's own description ("filed by a
  login other than the operator") is the honest scope, not "all user feedback". Fallback: none
  needed — this is a disclosed proxy limitation, not a defect; a future explicit "reported-by"
  field on the TICKET payload contract would close it, out of scope here.
- **R-2 (single-operator assumption).** `policy.confirmed_by` is read as a scalar login; a second
  trusted human operator would need the check to compare against a set, not one string. Detection:
  the LLD's own Resolution 1 names the exact field and shape assumed. Fallback: widen
  `confirmed_by` to a list and the comparison to `login not in confirmed_by` — a small, isolated
  change when that day comes, not designed around speculatively today.
- **R-3 (explicit feedback comments, unbuilt).** Named in Resolution 4 — a foreign-authored
  comment on an existing ticket earns no tag or count in this build. Detection: this LLD's own
  Resolution 4 states it as deferred, not silently absent. Fallback: a follow-up ticket, seeded
  in this PR's body, the same way idr-0008 itself named the door-vs-probe choice as a follow-up
  seed rather than building both at once.
- **R-4 (rate/latency of the new all-state `gh issue list` query).** A `--label user-signal
  --state all --limit 500` call is bounded (500-row cap, matching the pattern
  `ticket_state.py`'s existing `--limit 200`/`--limit 100`/`--limit 30` calls already use) and
  fires once per `check-state` run, not per-item — no new polling loop, no new hourly firing.
  Detection: `ticket_state.py selftest` exercises the classifier logic only (no live network);
  the real call is exercised by `check-state`'s own live run, same as every other collector query
  already is.

## Rejected alternatives

- **A new door** (a dedicated web form, a different issue template family) — rejected outright;
  idr-0008's own Claim rules reuse as the default and the three existing `.github/ISSUE_TEMPLATE/
  *.yml` files already realize the door. Job evidence for a new one does not exist.
- **An adoption/install probe** — rejected per Resolution 1; no publishing infrastructure exists
  to instrument, and the ticket's own dispatch instructions rule this lean explicitly.
- **A standalone trend CSV** (the `attention-trend.csv` shape) — rejected per Resolution 4;
  `check-state` is the live-read instrument this estate already uses for exactly this kind of
  question, and a second file nobody has cause to open recreates the "arriving ad hoc across
  scattered channels" failure `lld-0015`'s own Resolution 2 already named and rejected for a
  structurally identical choice (a new ops file vs. reusing an existing one).
- **Building the foreign-comment sweep now** — rejected per Resolution 4/R-3; named as a
  follow-up rather than paid for inside this ticket, per idr-0008's own minimal-first-instrument
  doctrine.
- **A hook applying the label automatically on `gh issue create`.** Rejected — this workspace's
  hooks are fully retired (#466); the tagging logic lives in the skills/agent that already
  perform the `gh` mint/resume call, mechanized inline, never a hook.

## Agent verification

**Mechanical layer:** `release_gate.py docs`, `release_gate.py harness` (both plugins touched);
`doc_lint.py` on this LLD; `ticket_state.py selftest` (new classifier fixtures, negative +
reverse controls per this repo's own script-writing-rules anatomy).
**Fresh-context checker:** one consolidated `harness:wording-checker` pass over every semantically
edited SKILL.md/agent body in this diff (`.claude/rules/plugin-authoring.md`'s semantic-edit
invariant — a body-only edit to a prompt-carrying artifact still rides a checker before merge).
**Payload/API layer (per gh#622's own Acceptance):** the `user-signal` label's existence and the
Counts line's presence are `gh`-verifiable directly (`gh label list`, a live `check-state` run).
**Human/final-ratification layer, stated exception:** whether the operator-login proxy (Resolution
1) is the RIGHT clause-(a) resolution, long-term, is a judgment call for Kim's own PR review —
named here as the open ratification this LLD's own draft status carries, not silently presented
as locked (idr-0008 itself stays LOCKED and unedited; this LLD is a build design under it, not a
supersession).
