# T4 ledger-lock carve-outs — what's allowed on a locked entry, and what still FAILs

T4 is `doc_lint.py`'s ledger-protection guard (`head_is_locked_ledger()`): once an ADR reaches
`status: accepted`, an IDR reaches `locked`, or an RDD reaches `locked` **in committed history**
(HEAD, not the working tree), the file is append-only — any further edit to that committed version
FAILs T4 with "the ledger is append-only; revert this edit and write a new `<TYPE>` with
`supersedes: <id>`" (`doc_lint.py` `hook_mode()`). This file documents the one narrow exception
ratified against that guard so far. Absent a citation below, T4 has no other carve-out — the
default for every ledger type remains "supersede, never edit."

## The carve-out (ADR-0027): backfilling an ADR's `intent-refs:` citation

**What it is.** An already-committed, `status: accepted` ADR may receive exactly one class of
edit: its `intent-refs:` frontmatter field moving from empty, `null`, or absent to a non-empty
IDR citation. Nothing else about the file may change — not the Context/Decision/Consequences
body, not any other frontmatter field, and not a *second* edit to an `intent-refs:` that already
carries a value.

**Why this exists.** `intent-refs:` cites the upstream IDR an ADR's decision served — the field
`doc_lint.py`'s T6 checks to WARN an "orphan ADR" (no citation at all). At ADR-0027's own
ratification (2026-08-28), 22 ADRs were orphaned this way: ADRs 0001–0013 predate the field's
existence (added 2026-08-16, #316) and could never have carried it; ADRs 0014–0025 postdate it but
shipped with `intent-refs: null` and were never revisited. Both groups were locked under T4 the
moment they reached `accepted`, so neither group had any structurally safe way to receive the
citation later — full re-supersession was rejected as disproportionate (22 near-duplicate ADRs
whose only substantive delta is one frontmatter line; see ADR-0027's Alternatives). The gap this
closes is idr-0002's own claim — the repo's git history is durable cold-start memory, and a fresh
session should be able to recover *why a decision mattered* from the repo alone. An orphan ADR is a
standing decision a cold session cannot trace back to its founding claim; leaving the 22 orphans
permanently un-retrofitted would have made idr-0002's guarantee false for all of them at once.

**Full ruling:** `.claude/docs/adr/0027-narrow-t4-carve-out-for-intent-refs-backfill.md`
(status: accepted, ratified by Kim, 2026-08-28, `intent-refs: idr-0002`).

**Current state (as of this file's own writing, 2026-08-30):** PR #989 already used this carve-out
to retrofit 19 of the 22 — only `adr-0008`, `adr-0024`, and `adr-0025` still WARN T6 today (no
covering IDR was found for those three at retrofit time; see #989's own summary). The "22" figure
above describes the situation ADR-0027 was ratified to address, not the live count — re-run
`python3 docs/scripts/doc_lint.py .claude/docs/adr/*.md` for the current orphan set rather than
trusting either number as it ages.

## What still FAILs

Everything else. Concretely, T4 still blocks:

- A second edit to an `intent-refs:` field that already carries a value — this carve-out is
  strictly empty/`null`/absent → non-empty, one-directional and one-time per ADR.
- Any change to the ADR's body (Context, Decision, Consequences, or anything else after the
  frontmatter's closing `---`) — even alongside a legitimate `intent-refs:` backfill. The body
  must stay byte-identical to the committed HEAD version.
- Any change to a frontmatter field other than `intent-refs:` — reordering lines, editing
  `status`, `owner`, `date`, `supersedes`, or anything else, even a single-character fix, still
  FAILs. The carve-out's diff test requires the frontmatter block to differ from HEAD in exactly
  one line (the `intent-refs:` line) or exactly one inserted line (for ADRs 0001–0013, which
  never had the key at all).
- The identical class of edit on a locked IDR or a locked RDD. **This carve-out is ADR-only** —
  IDR and RDD ledger entries carry no `intent-refs:` field and get no equivalent exception; T4's
  default append-only rule applies to them unmodified.

## How it's verified — structurally, not by trust

The check never takes an editor's word for "this is just the one field." `doc_lint.py`'s
`is_intent_refs_backfill(p, new_text)` diffs the proposed write against the file's committed HEAD
version (via `git show HEAD:<path>`) and returns `True` — allowing the edit past T4 — only when
both hold:

1. **The body is byte-identical.** Everything after the frontmatter's closing `---` (Context,
   Decision, Consequences, and beyond) matches HEAD exactly, character for character.
2. **The frontmatter differs in exactly one of two shapes:**
   - an existing `intent-refs:` line's value moves from empty/`null` to non-empty, at the same
     position, with every other frontmatter line unchanged (the 0014–0025 bucket: the field
     existed, shipped null); or
   - a brand-new `intent-refs: <value>` line is inserted, with every other frontmatter line
     unchanged and in the same relative order (the 0001–0013 bucket: the field never existed —
     T6 already treats a missing key the same as an empty one via `fm.get("intent-refs", "")`, so
     a first-time insertion is the same backfill, not a new class of edit).

Any other delta on either axis returns `False`, and `hook_mode()`'s T4 FAIL fires exactly as it
did before this carve-out existed. `doc_lint.py`'s bundled `selftest` carries positive fixtures
(sole-delta backfill on both buckets) and negative fixtures (a second edit to an already-populated
`intent-refs:`, an edit that also touches another field) proving both directions hold.

**Implementation:** `docs/scripts/doc_lint.py` — `hook_mode()` (the T4 FAIL site, skips when the
carve-out holds) and `is_intent_refs_backfill()` (the structural diff check itself). Landed via
PR #989, docs 1.22.0 (README footer ledger, same version).

## Using this to retrofit an orphan ADR

Populating `intent-refs:` on a still-orphaned ADR (`adr-0008`, `adr-0024`, `adr-0025` as of this
writing — re-check with the `doc_lint.py` command above rather than trusting this list) is still a
judgment call, never a mechanical one — which IDR (if any) the ADR's decision actually served needs
an honest read of that ADR's own Decision text against the corpus's locked IDRs; not every orphan
necessarily has one, and a citation should never be invented just to clear T6's WARN — PR #989 left
these three uncited for exactly that reason, not as an oversight. The carve-out only removes the
structural block on writing the field once that judgment is made — it says nothing about which
value is correct.
