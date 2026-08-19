# Gate-run time budget — Phase 5 stage 2's aggregate-gate bound (gh#1485)

Cited from `SKILL.md`'s Phase 5 stage 2 rather than restated inline (the same F6 split-to-
references pattern as this skill's other reference files) — moved here to keep the SKILL.md body
within its own `skill-writing-rules` line budget once Phase 5 stage 2a (the plan-approval
write-gate, ADR-0023 (c)) was added; this paragraph's own content and rule are unchanged from
before that addition.

**The local aggregate run ONCE, never ground.** The gate output named above (`npm run check` or
the host repo's own equivalent aggregate) is produced under the same feature-detected wrapper as
stage 2b's 900s CI-watch: `timeout 900 …` where GNU coreutils `timeout` is on PATH (`gtimeout 900
…` on a Homebrew macOS box), otherwise the portable `perl -e 'alarm 900; exec @ARGV' …` fallback
— ~15 minutes (900s) by default, overridable by an explicit budget the dispatch prompt names.

Run the aggregate ONCE under that bound; a hung single gate inside it is never chased with a
second run. On exhaustion (124/142/SIGALRM, or 127 when no wrapper was found at all — the bound
could not be enforced, so an unbounded run never substitutes for it), the seat records which of
the aggregate's own gates already reported green before the bound expired, names the aggregate
itself **partially-run** in the dated Findings write-back, and proceeds to open the PR anyway —
CI is authoritative from here (ADR-0002), and a timed-out local run is a contention verdict
(`flaky-gates`' contention-vs-regression discipline), never an implicit pass and never grounds to
grind the same aggregate again.

**The incidents this closes:** a seat that ran ~4h with no branch ever created, and a second the
stream watchdog killed after 600s of no progress — both under concurrent host load with no time
budget on this run at all (gh#1485).
