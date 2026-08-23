# wording-checker audit — file-bug SKILL.md, issue #880 fix

Artifact: `docs/skills/file-bug/SKILL.md` (Phase 1 status-line insertion + Phase 6 opening insertion)
Rubric: prompt-wording-rules potency rubric (instantiation-first)

## Lint (mechanical triage, whole file — pre-existing pattern, not new to this diff)

```
[  ok] hedges: 0 (budget 0)
[OVER] prohibitions: 33 (budget 5)
[OVER] NEVER (hard-gate cap): 28 (budget 3)
[  ok] vague quantifiers: 0 (budget 3)
[  ok] hard-emphasis markers: 0 (budget 3)
```

The prohibition/NEVER overage is a whole-file smell (this SKILL.md runs `never` densely across all
six phases as its house style) and is not attributable to either of the two new insertions — each
inserted passage contributes exactly one `never` clause (L53, L241). Treated as pointer, not
verdict, per the audit contract. `lint: over budget (pre-existing, not attributable to this diff)`.

## Q1 — Does the Phase 1 status-line requirement close off-ramps 1, 2, 4?

Cited text (SKILL.md:51-54):
> "Every branch above ends this invocation only after emitting a typed status line —
> `Resumed: <id> · route:<phase6|phase5|closed-stop> · status:<value read from the record's own
> state field, not inferred from comment text>` — never a bare id; reaching a phase number is not
> itself the report."

- **Off-ramp 2 (field-vs-comment-text ambiguity): CLOSED.** "status:<value read from the record's
  own state field, not inferred from comment text>" names the exact source and excludes the
  competing one. Instantiating.
- **Off-ramp 4 (bare id satisfying "report"): CLOSED.** "never a bare id; reaching a phase number
  is not itself the report" directly forecloses the minimal-compliance reading. Instantiating.
- **Off-ramp 1 (routing-arrow-as-no-op): NOT CLOSED — partial fix only.** The sentence commits the
  model to *emitting a report line*, not to *completing the routed phase's body*. "reaching a
  phase number is not itself the report" strengthens what counts as the REPORT, but says nothing
  about what counts as having DONE the routed phase's work. A model that reads Phase 1's branch
  "→ Phase 6" as label-only (the exact failure #880 exists to fix) can satisfy this new sentence
  in full by emitting `Resumed: <id> · route:phase6 · status:open` and then stopping — nothing in
  the added text ties emission of the line to prior completion of Phase 6's substantive steps
  (its read-back, its status advance, its report). Steelmanned: one could argue "→ Phase 6" already
  obligates continued execution on its own, so the new line is additive, not load-bearing for
  off-ramp 1 — but that argument assumes the very reliability the original finding (#880's own
  Findings) found false: routing arrows without commitment ARE read as labels, which is why the fix
  was scoped in the first place. The rebuttal does not survive; off-ramp 1 stays open.
- **New ambiguity introduced:** "ends this invocation only after emitting a typed status line"
  reads structurally like a stopping predicate (echoes "Done when X, not until"), but is placed
  mid-Phase-1, before the routed phase has run. A model pattern-matching on that cue could treat
  emission of the status line as the terminal action of the WHOLE invocation rather than a
  checkpoint en route to Phase 6/5's actual work — inviting exactly the premature-stop behavior the
  sentence exists to prevent, because "this invocation" is never pinned to "the entire multi-phase
  flow, after the routed phase has executed."

## Q2 — Does the Phase 6 opening sentence close off-ramp 3 (read-back presupposing a same-turn dispatch)?

Cited text (SKILL.md:239-241):
> "Read the record back — whether arriving here after this turn's own Phase 5 dispatch returned, or
> directly from Phase 1 on resume — before anything else in this phase; a resume that skips this
> read is incomplete regardless of what the record already shows"

**CLOSED.** Both entry paths are named explicitly (same-turn Phase 5 return; direct resume from
Phase 1), the read is placed "before anything else in this phase," and "regardless of what the
record already shows" forecloses the "I already know the status, no need to re-read" escape hatch.
This is a solid instantiating fix — presupposes both paths as valid, commits the action, forecloses
the shortcut. No blocking gap found here; the only soft point is "is incomplete" naming a judgment
rather than a hard branch (no explicit "then do X"), but the imperative framing plus "before
anything else" carries the intended force without a separate branch being required.

## Q3 — new ambiguity from wording itself

- Flagged under Q1 above: "ends this invocation only after emitting a typed status line" collides
  with the stopping-predicate pattern at the wrong phase, and is not pinned to "after the routed
  phase's body has run." This is the primary new-ambiguity finding.
- No other vague referents found: "the record's own state field" is used consistently with Phase
  6's own per-backend status vocabulary (frontmatter field / GitHub label+closed state / adapter
  status), so it resolves the same way across both new insertions and the pre-existing text — not
  a new escape hatch.

## Q4 — Is the Done-when predicate satisfiable without the new status line / read-back having run?

Cited text (SKILL.md:276-283):
> "Done when a `kind: bug` record exists — a `doc-type: ticket` file on disk, a labeled GitHub
> Issue, or an Option-C adapter's record (its native id reported) — carrying the report and
> classification, and either file-bug's own inline fix or the dispatched investigation has left at
> least one dated `## Findings` entry (file section or issue comment) — OR the seed was redirected
> ... no bug record is owed on a redirected seed, and no build is dispatched BY THIS SKILL either
> way"

**YES — residual gap, unclosed by either edit.** This predicate is pure artifact-state: record
exists + a dated Findings entry exists (or a redirect was reported). Neither new insertion touches
it. On the exact scenario #880 names — a pre-populated-Findings record on resume — this predicate
reads TRUE at entry, before Phase 1's new status line is ever emitted and before Phase 6's new
read-back ever runs. Neither insertion is referenced by, or feeds, Done-when. A model that
evaluates Done-when first (a common shortcut on resume) can see it already satisfied and terminate
without ever engaging Phase 1's branch logic or Phase 6's read-back — the identical silent-no-op
class #880 was filed to close. This is the single largest gap in the applied fix: the two
insertions add process language mid-phase, but the terminal checkable predicate that actually gates
"done" was never updated to require that process, so it remains satisfiable exactly as it was
before the fix.

## Verdict

**FAIL** — two blocking findings:

1. **SKILL.md:51-54** — off-ramp 1 (routing-arrow-as-no-op) not closed: the new sentence commits to
   emitting a report line, not to completing the routed phase's body first; "ends this invocation
   only after emitting a typed status line" reads as a stopping predicate untethered to Phase
   6/5's actual completion. Fix: pin the line's emission point explicitly — e.g. "emitted only
   after Phase 6/5's own work for this route has completed, never before it" — or fold Phase 6's
   completion into the same sentence as a precondition, not just its terminus.
2. **SKILL.md:276-283 (Done-when)** — untouched by the fix; still satisfiable purely on
   pre-existing artifact state (record + Findings entry already present), independent of whether
   the new Phase 1 status line or Phase 6 read-back ever ran. Fix: add a conjunct to Done-when
   tying it to the new process — e.g. "...and, on any resume, the record was re-read per Phase 6
   before this turn's status line was reported" — so the predicate can no longer be satisfied by
   artifact state alone on a resume path.

Non-blocking: Phase 6's opening sentence (SKILL.md:239-241) fully closes off-ramp 3 — no finding.
Off-ramps 2 and 4 (field-vs-text ambiguity, bare-id-as-report) are fully closed by SKILL.md:51-54 —
no finding on those two sub-points.

## Follow-up pass — both blocking findings amended, re-verified

Both fixes suggested above were applied:

1. Phase 1's sentence reworded to require the routed phase's own body to run to its own completion
   (Phase 6's close-out / Phase 5's dispatch / the closed-state report) BEFORE the status line —
   "as the last thing that phase does" — and "never emitted in place of running the routed phase's
   body" was added.
2. A new paragraph added after the Done-when predicate ("On a RESUME...") stating Done-when is
   never satisfied by pre-existing record state alone on a resume — it additionally requires
   Phase 1's own typed status line to have been emitted this invocation.

A second fresh-context wording-checker pass over the amended file confirmed:
- Off-ramp 1 (routing-arrow-as-no-op) now CLOSED — the status line is gated behind the routed
  phase's actual completion, not a substitute for it.
- The Done-when satisfiable-at-entry gap now CLOSED — the resume addendum directly forecloses it
  and correctly chains back to Phase 1's now-gated status line.
- No new escape hatch found; "Phase 5's dispatch" as its own completion point is intentional
  (Phase 5 is inherently async), not a loophole.

**Final verdict: PASS.**
