# Adversarial — find what breaks

Systematically attack the system with inputs and scenarios *designed to fail it*, classify each
outcome, and (optionally) harden the failures found. Answers: *"what breaks this? where are the
edges?"* — robustness as a measured survival rate, not a hunch.

## When to use
- A robustness check, stress test, security probe, or QA pass — before shipping or after a change.
- "Why is it broken" with **no** known-good prior state → probe for what's fragile (vs. **bisect**,
  which needs a good state).
- Not this method when: you want to raise a quality score → **autoresearch**; you want to know what's
  redundant → **ablation**.

## Input
The dispatch names what to probe — a component/module, a generation or transformation pipeline, a scorer
(can we fool it?), an API (error handling, edge cases), a config (invalid states) — and the pass/fail
bar. (Sealed dispatch: the caller enumerates the target; there is no "most recently changed" fallback.)

## Configuration
- `MAX_ROUNDS` 100 · `SEVERITY_THRESHOLD` medium (report at this level or higher) · `FIX_MODE` true
  (fix as found) or false (report only) — defaults; the dispatch may override any.

## Phase −1 · Research (mandatory)
Recon before the attack — real adversaries study the target first: (1) known bugs/CVEs and documented
failure modes for this kind of system; (2) established attack patterns for the class (OWASP for web,
fuzzing for parsers, boundary analysis for numeric code); (3) what QA practice recommends
(property-based, mutation, chaos). Build a prioritized **attack playbook** from known real-world
failures; test the highest-risk patterns first.

## Phase 0 · Threat model
Enumerate the attack surface; universal categories:
- **Boundary** — empty, null, max-length, negative, zero, off-by-one.
- **Type** — wrong/mixed types, coercion, format mismatch.
- **Volume** — too many items, deep nesting, huge inputs.
- **Timing** — rapid/concurrent calls, races, timeouts.
- **Mutation** — state changed mid-op, stale references.
- **Content** — malformed input, special chars, encoding, injection payloads.
- **Environment** — missing deps, permission/resource limits, config drift.
- **State** — invalid transitions, repeats, interruption mid-process.

Prioritize probes by likelihood × impact.

## Phase 1 · Loop
For each probe (1 → `MAX_ROUNDS`):
1. **Design the attack** — a specific input/scenario meant to break it.
2. **Execute** and observe.
3. **Classify** — `CRASH` (unhandled failure/hang) · `CORRUPT` (wrong output, data loss, silent
   failure) · `DEGRADE` (works but poorly) · `SURVIVE` (handled: error, fallback, boundary enforced).
4. **Fix (if `FIX_MODE`)** — at/above `SEVERITY_THRESHOLD`, fix, then **re-run the probe to verify**.

Per probe: `Probe n: <attack> · <category> · CRASH|CORRUPT|DEGRADE|SURVIVE · <severity> · fixed|reported`.

## Phase 2 · Hardening (if `FIX_MODE`)
Re-run every probe that initially failed and confirm all fixes hold.

## Phase 3 · Report
```
Adversarial · <target>  ·  probes <n>
Survived <s> (<pct>%) · Degraded <d> · Corrupted <c> · Crashed <x>
Bugs:  1. <desc> — <severity> — fixed|reported   2. …
Most fragile area: <category>   ·   Robustness: <survived>/<total>
Recommended hardening: <action> · <action>
```

## Rules
- Think like a QA engineer, a malicious user, and a tired developer at once. · Test the edges.
- Fix as you go (if `FIX_MODE`) and **verify each fix** by re-running the probe. · **Escalate the
  class** — one probe revealing a pattern ("all inputs >10k crash") means probe the whole class.
- Document critical bugs even when fixed, for the record.
- **Web-search on unfamiliar failures** — an unrecognized error, a crash in a dependency, or
  environment-specific behavior is often a documented bug/spec edge/platform quirk. Look up the error
  before guessing at a fix.

## Rubric — adversarial conducted well
Inherits **R1 · R3 · R7** from `references/rubric.md` (R1 here = the CRASH/CORRUPT/DEGRADE/SURVIVE
classification is the scorer; R3 = one attack per probe). Additive method checks:
- **Severity classification** — 1: pass/fail only · 5: every outcome typed and severity-rated, so the
  robustness rate is meaningful.
- **Verified fixes** — 1 (FIX_MODE): fixes claimed, not re-tested · 5: every fix re-run against its
  probe and confirmed to hold.
- **Class escalation** — 1: each bug treated in isolation · 5: a discovered pattern triggers a sweep of
  the whole class, not one instance.

**Gate:** R1 (outcomes classified) · R3 (one attack/probe) · R7 (probe budget or class-coverage
predicate, not an open-ended flail) ≥ 3, **and** in FIX_MODE every fix is verified by re-running its
probe (an unverified fix is a claim, not a result).
