# Selftest patterns — the shapes worth copying

> `script-writing-rules` reference. Every shape below exists in this workspace's shipped
> scripts; each entry names a live exemplar so the pattern can be read in the wild. · 2026-07-14

A selftest is the script's own release gate: it constructs a small world where the right answer
is known, runs the real code paths against it, and asserts the verdicts. The minimum bar is one
passing fixture **plus one control that bites** — a selftest that only proves a good input passes
is a green light wired to the wall.

## Inversion fixture — prove the wrong input is CAUGHT

Feed the check an input containing exactly the defect it exists to catch, assert the failure
verdict (exit 1, the FAIL line, the finding code). This is the control that distinguishes a
working check from a dead one.

```python
(js / "demo-check.mjs").write_text("...process.exit(1)...")   # a script whose selftest fails
code, _ = gate(r)
assert code == 1, "failing .mjs selftest must fail G4"
```

Live exemplar: `release_gate.py selftest` — bad manifest must fail G1, owner-mismatched eval
suite must fail G7, failing bundled selftest must fail G4.

## Reverse control — prove the right input is NOT flagged

The inversion's mirror: a valid input must come back clean. Guards against the over-eager
rewrite that starts catching everything. Every fix-then-assert-clean sequence in
`release_gate.py selftest` ("valid suite must restore a clean gate") is this shape.

## Fact × fact consistency gate

When the script publishes two facts that must agree — a declared design choice and a measured
value, a table and the formula that generated it — assert their agreement as a check, so a future
edit to one side cannot ship without the other. (The check-all-skills standard names this shape
RECIPE_MISMATCH.)

## Tri-state skip — dependency-honest selftests

A selftest needing a runtime the current machine may lack (browser, heavyweight package) probes
for it first and exits **2** with a one-line reason and the install hint. Exit 0 would make a
broken environment look green; exit 1 would fail ships on machines that never run that check.

Live exemplar: `ui-probe.mjs` (playwright probe → `SKIP` + install hint + exit 2); ratified into
G4's sweep 2026-07-14 — the gate discloses skips in its ok line instead of failing them.

## Fixture-plugin world — test the orchestrator, not mocks

An orchestrating script (a gate that composes checkers) selftests by building a real miniature
target in a tempdir — a whole fixture plugin with manifest, skill, README — then mutating it
defect by defect and asserting each gate code fires. No mocks: the real checkers run against a
real (tiny) world. Live exemplar: `release_gate.py selftest`'s `demo-plugin`.

## Self-reference exception

A gate that sweeps selftests must not recurse into its own: `release_gate.py` skips itself in G4
(`s.resolve() == Path(__file__).resolve()`) and proves itself via its own `selftest` entry point
instead. State the exception in a comment where the skip happens.

## Incident → fixture (the same-day rule applied here)

A false positive, a missed catch, or a skipped step observed in the field becomes a fixture in
the selftest before the fix ships — the selftest is where incidents are made unrepeatable. The
G4 js-parity hole is itself the worked example: discovered 2026-07-14 (`.mjs` selftests never
ran at the gate), closed the same day with the failing-mjs/passing-mjs/skip-mjs controls added
to `release_gate.py selftest`.
