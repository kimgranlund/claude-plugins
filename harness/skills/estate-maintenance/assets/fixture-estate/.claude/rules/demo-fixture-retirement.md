# Demo fixture retirement (FIXTURE, synthetic)

**Path scope:** `**/fixtures/*.demo` (fictional — this rule is fixture-only).

A retired demo fixture is deleted via `/retire-fixture`, never left dangling. Second synthetic
rules file so D4's `rules_count`/`rules_total_lines` census has more than one entry to sum —
not consulted by anything outside `collect.py`'s selftest.
