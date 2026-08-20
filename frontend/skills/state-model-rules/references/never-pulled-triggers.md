# Never-pulled re-evaluation triggers

**The judgment call:** a documented "if X happens, revisit this decision" clause is a promise
with an expiry condition, not a footnote. When the org's own ratified record NAMES the condition
under which a decision should be re-opened, and that condition later fires, the failure worth
reporting is not "the architecture drifted" in the abstract — it's "a named trigger was pulled
and nobody re-evaluated." That reframing changes the fix: it isn't a redesign from scratch, it's
running the re-evaluation the org already committed to running.

## The worked case [incident]

agent-ui's ADR-0050 built the framework's first context/provider primitive (a form-field
event-registry) and its own Alternatives section named the re-evaluation trigger explicitly: "if
a second context consumer appears, the community `context-request` protocol is the named
re-evaluation trigger... do not pre-abstract." Eight days later, ADR-0117 shipped a SECOND
provider-shaped control (theme, via pure CSS cascade) — a second context consumer, by the ADR's
own definition — "without ever mentioning ADR-0050's trigger... it built a third, incompatible
shape with no discussion of `context-request` adoption."

The framework audit's own verdict: "Kim's 'mix of implementations' traces to gap #1: there was
never a second sanctioned option to converge on" — not because nobody could have converged, but
because the org's own named checkpoint for deciding whether to converge was never run.

Source [verified]: `/Users/kimba/Projects/nonoun/agent-ui/.claude/docs/reports/data-model-review-2026-08-20/framework-state-idioms.md`
("Context-providing verdict" + "Gaps / tensions" #1); `FINDINGS.md` F3 names this as the
SYSTEMIC root-cause finding, distinct from the app-level symptom it produced.

## A second instance: a convergence question left permanently open [incident]

gen-ui-kit's review found the same shape at the level of an entire runtime, not one primitive:
two complete A2UI data-model implementations coexist — an in-repo 0.9-dialect runtime (brute-
force re-apply-all) and a vendored v1.0 runtime (`Cell`/`Derived`, RFC-6901, memoized reads,
demonstrably the better data model on that specific axis) — with no ADR ever deciding which one
the ecosystem converges on. "Until ruled, every new consumer picks a side and deepens [the
drift]." The report frames this explicitly as a program-level convergence QUESTION that has been
sitting unruled, not a design gap nobody noticed — the recommendation is "needs an ADR, not
code."

Source [verified]: `/Users/kimba/Projects/adia/gen-ui-kit/.claude/docs/reports/2026-08-20-reactivity-review/INDEX.md`
F3 + R3 ("Decide the two-runtime convergence direction explicitly").

## The diagnostic

1. **Grep ratified records for their own named re-evaluation conditions before writing a new
   design doc.** An ADR/decision record that states "revisit if Y" is leaving a structured,
   checkable trigger — treat "has Y happened yet" as a mechanical question to answer before
   assuming the decision needs re-litigating from first principles.
2. **When a second instance of the triggering condition ships, that shipment is itself the event
   to flag** — not months or years later when the divergence has compounded into "a mix of
   implementations." The gap between ADR-0050 and ADR-0117 was eight days; the audit surfacing it
   came much later.
3. **Distinguish "never pulled because nobody noticed" from "explicitly declined."** A trigger
   that fired and was deliberately NOT pulled, with a recorded reason, is a ratified status quo
   (see `doctrine-vs-practice.md`'s contradiction-tracking for how to record that kind of
   decision); a trigger that fired silently, with no record anyone even checked, is the defect
   this axis names.
4. **A live, unruled convergence question is itself a finding worth a name** — "R3: needs an ADR,
   not code" is a legitimate, complete recommendation on its own; don't feel obligated to pick a
   winner between two competing implementations just because the audit found them both.
