---
doc-type: rdd
id: rdd-0001
status: locked
date: 2026-08-23
owner: kim.granlund
dri: kim.granlund
decision-refs: idr-0001
supersedes: null
scope: app
audience: product-seat, human
---
# RDD-0001 — Every plugin ships Codex, Hermes, and Pi overlays alongside Claude Code

## Scope

This release commits the estate's nine plugins to shipping in-tree, committed overlay files for
three additional harnesses beyond Claude Code — Codex (`.codex-plugin/plugin.json` + per-skill
`agents/openai.yaml`), Hermes (`plugin.yaml` + `__init__.py` + `hermes-mcp.yaml` where an MCP
config exists), and Pi (`package.json` + `prompts/<name>.md` for command-only skills) — generated
by one stdlib-Python emitter (`harness/scripts/harness_emit.py`) and verified fresh by a new
release-gate check (G15). Two reasonable teams would ship different releases from this line: one
could have shipped Codex alone, deferred Hermes/Pi to a future release, or built per-harness
manual overlays instead of a shared generator — the actual commitment fixed all four waves (Codex,
Hermes, Pi, Pi-MCP passthrough) plus the generator/gate pairing as one release-grain unit.

## Acceptance

- Every one of the estate's nine plugins carries a Codex overlay (`.codex-plugin/plugin.json`,
  per-skill `agents/openai.yaml`) generated from its existing Claude manifests, with no hand-edited
  drift from the generator's own output — falsifiable by re-running `harness_emit.py --verify`
  against any plugin and finding a diff.
- Every plugin carries a Hermes overlay (`plugin.yaml`, a working `__init__.py` `register(ctx)`
  stub, `hermes-mcp.yaml` where the plugin ships an `.mcp.json`) that a fresh Hermes session can
  actually load and resolve skills through — falsifiable by the tier-3 human load assert (a fresh
  Hermes session invoking a plugin skill) failing, which it did once (gh#899, `__init__.py` passed
  `str` where Hermes's `register_skill` calls `.exists()`) before the fix (PR #900) made the claim
  hold.
- Every plugin carries a Pi overlay (`package.json`'s `pi` key, `prompts/<name>.md` for
  command-only skills) that `pi list` surfaces under Project packages — falsifiable by that command
  omitting a plugin its manifest claims to cover.
- `release_gate.py`'s G15 check FAILS when any harness overlay is stale relative to its source
  Claude manifests — falsifiable by hand-editing a generated overlay file and re-running the gate
  without regenerating.
- The Pi MCP surface is a passthrough of the existing `.mcp.json` (no separate generator), holding
  only while the third-party `pi-mcp-adapter` remains the sole MCP path on Pi core — falsifiable by
  Pi core shipping native MCP support that supersedes the adapter's `.mcp.json` compatibility
  contract.

## Sequencing

Four strictly serial waves, one emitter PR in flight at a time (LLD-0025, Ruling 3): **W1 Codex**
(gh#886, PR #892, merged) → **W2 Hermes** (gh#890, PR #893, merged) → **W3 Pi** (gh#891, PR #894,
merged) → **W4 Pi-MCP passthrough** (gh#895, PR #898, merged, gated on research seed T-2/gh#887).
Three research seeds ran ahead of and alongside the waves: T-1 (gh#885's own AC1 research record,
`.claude/docs/research/harness-packaging-pi-hermes-2026-08-23.md`), T-2/gh#887 (Pi MCP — resolved
to the passthrough design W4 built), T-3/gh#888 (command-only-skill native emission — split by
harness: Pi upgraded to generate-glue for W3, Hermes stays plain-skill degradation, Codex
unaffected), T-4/gh#889 (the 14-row hook-mapping table, non-blocking — the estate ships zero
hooks). One post-ship defect surfaced and closed serially: gh#899 (Hermes `__init__.py` type bug)
→ PR #900 (harness 3.18.4), after which the corrected Hermes tier-3 assert passed. Tracked at
kimgranlund/claude-plugins#885.

## Completion

Shipped-and-archived. All four waves merged to `main` (harness 3.18.4 as of the gh#900 follow-up);
all nine plugins carry Codex/Hermes/Pi overlays in-tree, gated by G15's freshness check; gh#885 is
CLOSED. Evidence: gh#885's own Findings thread (LLD-0025 ratification, the four wave PRs — #892,
#893, #894, #898 — plus the gh#899/PR #900 follow-up), and the three tier-3 human load asserts
Kim ran live and recorded there — Codex (all nine plugins listed, screenshot on gh#886), Pi (`pi
list` showing harness under Project packages), Hermes (a fresh session loading
`brand-design:make-brand`). This RDD stays `locked` at this evidence permanently, per the primary
Mutability design in `prd-rdd-framework.md` — the `roadmap`'s own Now→retired movement is where
this release's ongoing currency is tracked, not a further edit here.
