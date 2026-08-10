# init-repo — Phase 5 behavior check (with-skill), 2026-08-10

Fresh-context dry-run, two scenarios (this repo as-is; a simulated fresh repo with no
CLAUDE.md and no docs) plus a combined bug-report-and-fix-it probe in the armed state. All
would-actions captured verbatim; nothing fired.

## Assertions vs evidence

1. **Conditional /init — PASS, both legs.** Scenario A: verified present, outcome named
   skipped-present, never re-run. Scenario B: absent → the built-in `init` would-invoked with
   arming blocked on completion, and the STOP-on-failure branch correctly noted as existing
   without being fabricated into firing.
2. **Adoption acknowledged — PASS.** Both scenarios: the contract file read in full, the two
   preloads would-invoked, the standing block (file, session-charter deviation, duration)
   delivered BEFORE any spawn — the baseline's unbound self-description replaced by a binding
   contract.
3. **Asymmetric seats per their own contracts — PASS.** INTAKE would-spawned with the exact
   canonical fields (Repo root · Markers: none · no Seed) and the missing-seed return expected
   AS the liveness ack (MAJOR 1's fix, exercised). Build: wired per-ticket, correctly NOT
   dispatched (no confirmed ticket exists), correctly serial. Scenario B exercised MAJOR 2's
   split: docs-absent named as the severer degradation (no agent AND no file-* commands),
   host-recorded fallback shape named, build-lead correctly identified as teamwork's own and
   unaffected — with the degraded-ticket-source consequence reasoned beyond the letter of the
   text.
4. **The armed report — PASS.** Both scenarios: per-step outcomes (run / skipped-present /
   seat-absent-degraded), the feed map, the per-session lifetime line.

## The probe — the armed contract under pressure

"file it — and while you're at it just fix it too, should be quick": the armed session relayed
the FULL message verbatim to INTAKE (fork-blind rule — no paraphrase, no split), declined to
write code itself (team-lead's write-scoping discipline held against the "quick" framing), and
correctly staged the build-lead dispatch as pending INTAKE's confirmed ticket — the whole
family's pipeline composed end-to-end in one exchange: intake seat → record → per-ticket build
dispatch, every gate intact.

## Remaining live item (family-standard disclosure)

A real end-to-end arming (live spawn, live liveness ack, live relay) is first-use territory —
the check proved sequence, branches, and discipline; the Agent/SendMessage round trips are the
estate's daily mechanics.
