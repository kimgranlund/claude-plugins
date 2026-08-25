# Which IDR governs — idr-0005 vs idr-0001 (ADR-0026)

Two locked IDRs both bear on toolchain/estate work and are easy to conflate. This is the routing
citation a future campaign checks before assuming either governs new work — cite it, don't
re-litigate the split.

| IDR | Claim | Governs |
|---|---|---|
| `idr-0005` (`.claude/docs/idr/idr-0005-portable-products-hypothesis.md`) | An external audience for these plugins will materialize eventually; the portability discipline already built is warranted at zero further investment until a real adoption signal lands | **Audience-facing surface only** (ADR-0026 narrowing): README/marketplace framing, LICENSE terms, plugin-boundary hygiene for third-party installers, `issue-sorter`'s friendlies allow-list |
| `idr-0001` (`.claude/docs/idr/idr-0001-self-governing-toolchain.md`) | A mechanized incident class stays gone once converted into a lint rule, gate check, or selftest fixture | **Cross-harness/agent-runtime interop work** — a second host tool reading this estate's plugins (gh#885's `harness_emit.py` and similar), scoped and invested in on its own merits, independent of idr-0005's adoption-signal gate |

**The split (ADR-0026, ratified 2026-08-23):** cross-harness/agent-runtime interop is a distinct
concern from external-audience portability. gh#885's packaging work is not gated on idr-0005's
adoption-signal proof/falsify condition — it is governed by idr-0001 instead. idr-0005 stays
locked and unedited; ADR-0026 is the citing record, not a change to the IDR itself. A future
campaign proposing new audience-facing surface (adoption tooling, expanded marketplace framing)
still checks idr-0005's proof/falsify condition first, unchanged.

Both IDRs are `locked` — cite, never edit. The narrowing decision itself lives in
`.claude/docs/adr/0026-idr-0005-scope-narrowed-to-audience-facing-surface.md`; this file is the
routing pointer, not a restatement of its Context/Decision/Consequences.
