# Demo widget — shipping rule (FIXTURE, synthetic)

**Path scope:** `**/widgets/*.demo` (fictional — this rule is fixture-only).

A demo widget ships only through `/ship-widget`; never hand-copy a widget artifact. This file
exists purely to give `estate-maintenance`'s D4 census collector a real `.claude/rules/*.md`
entry to count — it is not consulted by anything outside `collect.py`'s selftest.
