---
doc-type: adr
id: adr-0027
status: proposed        # proposed | accepted | superseded
date: 2026-08-28
owner: kim.granlund
supersedes: null
intent-refs: idr-0002    # the git substrate as durable cold-start memory — an orphan ADR corpus is exactly the failure this claim measures against
scope: app
audience: planner, reviewer, builder
---
# ADR-0027 — A narrow T4 carve-out lets an accepted ADR receive its first `intent-refs:` citation

## Context

Ticket #978 asked for a sweep: link each of 22 orphan ADRs (`doc_lint.py` T6: no `intent-refs:`
citation) to a citing IDR, or mark it superseded. Running the sweep (branch
`978-sweep-22-orphan-adrs`) found all 22 are `status: accepted` and committed at HEAD — every one
is a locked ledger entry under T4 (`doc-writing-rules`' ledger-lock guard: "editing a file whose
COMMITTED HEAD version is a locked ledger entry... supersede, never edit"). Two candidate safe
paths were checked and both are unavailable structurally, not just in this instance:

- **A reverse citation on an unlocked IDR/RDD's own side.** The schema has no such field — an IDR
  never cites the ADRs that reference it, and RDD's `decision-refs:` points from RDD down to
  ADR/IDR, never the reverse. Even if it existed, all 11 IDRs and the 1 RDD in this corpus are
  themselves `locked`, so there is no unlocked ledger node anywhere to write to.
- **Marking the ADR superseded.** Legitimate only when a later ADR genuinely replaces the earlier
  decision. The corpus already carries several *partial* supersessions (adr-0009 → clause of
  adr-0006; adr-0013 → one bullet of adr-0012; adr-0015/0016/0017/0018/0024/0025 → single clauses
  of adr-0011; adr-0020 → part of adr-0015) — none of the 22 orphans has a full, wholesale
  supersession already evidenced anywhere in the corpus. Inventing one to force an orphan closed
  would fabricate decision history the ledger exists to keep honest.

13 of the 22 (adr-0001–0013) predate the `intent-refs:` field's own existence (added 2026-08-16,
#316, alongside the `idr` type) — they could never have carried it. `doc_lint.py`'s own T6 comment
already names this: "existing ADRs 0001-0013 predate `intent-refs:` and are EXPECTED to warn here
— the retrofit is its own deferred follow-up (PRD Implementation surface item 7)." The other 9
(adr-0014/0015/0016/0017/0018/0019/0020/0024/0025) postdate the field but were authored with
`intent-refs: null` and never revisited. Both groups hit the identical T4 wall.

T4 exists to protect the ledger's actual guarantee — a decision's Context/Decision/Consequences
cannot be silently rewritten after ratification. Backfilling a citation-only frontmatter field
from empty to non-empty touches none of that: it doesn't change what was decided, only records
which founding claim the decision served, closing exactly the gap idr-0002 measures ("a fresh
session can recover work-state, standing decisions, and next actions from the repo alone" — an
orphan ADR is a standing decision a cold session cannot trace back to why it mattered).

## Decision

We will add one narrow, mechanically-bounded exception to `doc_lint.py`'s T4 ledger-lock guard:
an already-committed, `status: accepted` ADR may receive exactly one class of edit — setting
`intent-refs:` from empty/`null` to a non-empty citation — verified structurally, not by trust.
The hook-mode guard diffs the committed HEAD version against the proposed write and ALLOWS it
only when every other line is byte-identical and the sole delta is the `intent-refs:` value
moving from empty/`null` to non-empty; any other delta on the same file (including a *second*
edit to an already-populated `intent-refs:`, or any change touching Context/Decision/
Consequences or any other field) still FAILs T4 exactly as today. This is a one-time,
one-directional, single-field carve-out — not a reopening of accepted ADRs generally.

**Alternatives considered:**

- **Require full supersession per orphan (mint a new ADR for each of the 22).** Rejected —
  disproportionate: creates 22 near-duplicate ledger entries whose only substantive delta is one
  frontmatter line, doubles the ADR corpus's size, and a `supersedes:` chain implies the decision
  itself changed, which it did not. Misleads exactly the cold-start reader idr-0002 is about.
- **Leave the 22 orphans permanently un-retrofitted; treat the T6 WARN as a standing, accepted
  cost.** Rejected — T6's own comment already frames the gap as a deferred *follow-up*, not a
  permanent waiver ("not required for this check to ship" implies the retrofit still ships
  later); PRD Implementation surface item 7 names it as owed work, not closed scope.
- **Widen T4's carve-out to any frontmatter field, not just `intent-refs:`.** Rejected — broader
  than the evidenced need, and reopens exactly the "trust me, it's just metadata" surface T4 was
  built to close off. Scoped to the one field this ticket's sweep actually needed.

## Consequences

Ratifying this unblocks the deferred PRD Implementation surface item 7 retrofit: a future
dispatch can populate `intent-refs:` on some or all of the 22 orphans (each citation still needs
its own honest judgment call — which IDR, if any, the ADR's decision actually served; not every
orphan necessarily has one, and a citation should never be invented just to clear the WARN).
It requires a `doc_lint.py` code change (the structural single-field diff check) before any
retrofit PR can land — not built by this ADR, named as follow-up. Until this ADR is accepted, the
22 orphans remain correctly blocked exactly as ticket #978's sweep found them, and the T6 WARN
stays an accurate signal rather than a stale one. If rejected, the alternative (full supersession
per orphan, or a permanent waiver) becomes the standing answer instead, and this file is
superseded by whichever is chosen.
