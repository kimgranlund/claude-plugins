---
name: pattern-sweeping
description: >-
  Runs a repo- or corpus-wide sweep for a code/DOM pattern or criterion safely:
  census → sanity-check → classify → report or transform → verify → ratchet.
  Use for "sweep the repo for X", "find every page/file that still does Y",
  "audit all drawers/pages/tables for Z", "codemod this pattern away", "how many places
  still use…", "migrate every remaining call site". Audit-first; mutation is a
  separately gated phase. NOT for the ops-queue sweep (sweep-chores); NOT for
  naming/bloat audits of instruction markdown (authorkit's naming-audit /
  bloat-audit); NOT for a single-site fix with no census scope (ordinary edit);
  NOT for rerunning trigger evals (check-routing).
disable-model-invocation: false
user-invocable: true
argument-hint: "[scope + pattern + criterion, e.g. 'src/pages — inline min-width on *-ui components — remove decorative ones']"
---

# pattern-sweeping

A sweep produces a **classified census and a verified outcome**, never a raw match list acted on
directly. The method exists because a sweep reports success from its own regex — which measures
the regex, not the codebase. Four production incidents fund every step below (adiav2 admin
campaigns, Jul 2026): markup greps missing TS-assembled style strings; a `[0-9]` class deleting
load-bearing `min-width: 0` flex-truncation idioms and collapsing a search input on ten pages; a
spec asserting element presence while the rendered property broke; a census regex undercounting a
registry 98→54 and shipping a confidently wrong filed finding.

## Pre-flight — grill the ask

Before parameter-binding, gate on how open the decision space still is. **Fires** when the sweep
is MUTATING (any transform phase is being authorized, now or later in the run) or the decision
space is large/open — deriving census scope + exclusions, the classification policy (which match
kinds are load-bearing vs. deletable — the `min-width: 0` incident class), transform design and
authorization, or verify criteria/ratchet target. **Skips** for a read-only, fully-specified
census at or below step 3's own threshold anchor (≤20 sites and ≤10 independent files) — a
settled decision space earns no grill (over-grilling is the mirror failure of skipping it).
Interactive: run `teamwork:grill-the-ask` (soft cross-plugin mention,
degrades gracefully where teamwork isn't installed — fall back to one `find-intent`-style batched
`AskUserQuestion` round). Unattended: an under-specified, mutating sweep reports **blocked**,
naming the missing fork(s), rather than guessing at scope/classification/authorization/
verify-criteria — matching `mobilize-chores`' own convention for an under-specified task; an unattended
sweep whose seed is already fully specified proceeds directly, same as the interactive skip.

## 0 — Bind the four parameters

A sweep is fully defined by four named values; the run states all four before any search:

1. **Scope** — repo, glob set, or an enumerated page/corpus list, plus HOW it was enumerated
   (that enumeration is itself a claim step 1 sanity-checks).
2. **Pattern tier** — text grep, AST/structural, or rendered-DOM query. The criterion's tier is
   named explicitly; a value assembled at runtime (a TS-built style string, a computed class)
   lives one tier above where it appears in source. When the tier is uncertain, run two tiers
   and diff the hit sets — a non-empty diff is a finding, not noise.
3. **Criterion** — the semantic rule, stated separately from the pattern. `min-width: 0` matches
   the pattern "inline min-width" and violates nothing; the criterion is what step 2 classifies
   against.
4. **Disposition** — report-only, mint records, or transform. Transform is never the opening
   disposition: the audit phases (1–2) complete and land in the report before any mutation.

Missing parameter → ask for it (interactive) or report the gap and stop (unattended). Skip
nothing by inference.

## 1 — Census, then prove the census

Run the extraction (`scripts/pattern_census.py` for grep-tier scopes — census + inline
sanity/negative controls + JSON output; AST/DOM tiers use the project's own tooling with the
same contract). Then, before ANY claim or record is built on the hit set:

- **Known-member check:** pick 1–2 members known to be in the set from independent evidence and
  confirm they appear (`--must-match`). A miss means the pattern undercounts — fix the pattern,
  not the expectation. In JS/TS object literals, match both `'name': ident` and bare `ident,`
  shorthand forms — the 98→54 incident is exactly this miss.
- **Known-nonmember check:** confirm one value the criterion protects does NOT match
  (`--must-not-match`) — e.g. `min-width: 0` against a `[1-9]`-guarded width pattern.

Census output: total hits, per-file counts, tier(s) used, both check results. This block leads
the report.

## 2 — Classify every hit before touching any

Each hit lands in exactly one bucket:

- **decorative** — removable/transformable with no behavioral consequence;
- **load-bearing** — the value does work (a flex-truncation `min-width: 0`, a search input's
  only width); transform means RELOCATING it to a sanctioned home, never deleting it;
- **idiom** — a deliberate, named convention; excluded and cited.

Only the decorative bucket is eligible for mechanical transform. A hit that cannot be classified
from reading its context is load-bearing until proven otherwise. The classification table
(bucket, count, evidence for the non-obvious calls) goes in the report verbatim.

## 3 — Act per disposition

- **Report-only:** emit the output contract below; done.
- **Mint records:** one record per coherent fix wave (not per hit), each carrying its bucket's
  hit list; done when the records exist and the report links them.
- **Transform:** script the change with assertions INSIDE the transform (refuse any block with
  unaccounted markup; verify preserved values survive verbatim). Transform decorative hits only;
  load-bearing relocations are their own reviewed change, never batched silently into the
  mechanical wave.

  **Solo vs. `/batch`.** Below a PROVISIONAL threshold — **>20 sites OR >10 independent files**
  (ratcheted on the first two real runs' evidence, not a priori debate) — transform solo, in-host,
  as above. Above it, the gated transform hands the CLASSIFIED census (step 2's table, decorative
  bucket only) to Claude Code's built-in `/batch` command as its decomposition input instead of
  transforming serially: `/batch <instruction>` researches, decomposes into 5–30 independent
  units, presents the plan for approval, then runs one subagent per unit in its own git worktree
  (acceptEdits mode with the inherited tool allowlist), each unit opening its own PR. Its
  concurrency cap is UNDOCUMENTED at the platform level — state that plainly rather than inventing
  a number.

  **Routing guidance:** `/batch` when the classified hits partition into independent units and N
  reviewable PRs are wanted; this skill's own solo transform (one verification pass, one verified
  result) below the threshold, or whenever the hits don't partition independently regardless of
  count.

  **Cautions:**
  - `/batch`'s acceptEdits mode plus its inherited allowlist is a pilot-scope rule, same as any
    other acceptEdits dispatch — scope the pilot before trusting the full sweep to it.
  - N parallel PRs against ONE plugin's version slot collide (one version-bumping build in flight
    per plugin at a time) — partition units by plugin, or serialize the version-bump commits
    across units that target the same plugin.
  - N PRs needing merge is real merge-on-green load — budget for it before choosing `/batch` over
    a single-PR solo transform.

  **Verify runs per-PR** (each `/batch` unit's own PR carries step 4's verification evidence for
  its slice) **plus the ratchet after merges** (step 5, run once against the merged whole, never
  once per unit).

  A structured match dataset (e.g. `authorkit:pattern-audit`'s id/file/line/col/match/context/kind
  output) is the natural `/batch` decomposition payload once classified — soft cross-plugin
  mention, degrading gracefully where authorkit isn't installed.

## 4 — Verify the claim, not a proxy

Assert the property that actually breaks — a rendered width, a computed style, a firing
ellipsis, an attribute value — never element presence/absence. Two standing checks:

- The verification environment is current: a dev server older than the last dependency install
  serves a stale module graph and passes stale code — check server age before believing a local
  result.
- "Zero matches remain" is a census claim and gets step 1's known-nonmember treatment: prove the
  pattern still FINDS a planted specimen before trusting its silence.

## 5 — Ratchet

A sweep that cannot hold its ground regresses. End by tightening a mechanical baseline the CI
already runs (a contract budget, a lint rule, a gate count) so residue and reintroduction fail
CI instead of waiting for the next human to notice. No ratchet mechanism exists → the report
says so explicitly and names the follow-up that would create one.

## Output contract

The report, in order: **verdict line** (criterion, scope, disposition, outcome) → census block
(step 1, checks included) → classification table (step 2) → actions taken or records minted
(step 3) → verification evidence naming the rendered/computed property (step 4) → ratchet named,
or its absence stated (step 5). Every count in the report traces to the census JSON, never to a
re-grep mid-run.

## Failure branches

- Census checks fail 2 times on the same pattern → the pattern tier is wrong; escalate one tier
  (grep → AST → rendered DOM) instead of iterating the regex a third time.
- A transform touches a load-bearing or unclassified hit → stop the wave, reclassify, restart
  from step 2 for the affected files.
- Verification cannot run (no browser, no test harness) → report the outcome as UNMEASURED with
  the exact check a follow-up must run; never substitute a presence assertion.
- An unattended, under-specified, mutating sweep hits the Pre-flight gate with no channel to
  answer it → report **blocked**, naming the missing fork(s) (scope, classification policy,
  transform authorization, or verify criteria); never guess and proceed.

Done when the output contract is emitted with all six sections and, for transform disposition,
verification passed on a current environment. Not done while any acted-on hit sits unclassified
or any count in the report lacks a census-JSON source.
