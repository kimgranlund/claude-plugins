# Skill / agent / hook authoring — wiring and semantic-edit invariants

**Path scope:** `**/skills/*/SKILL.md`, `**/agents/*.md`, `**/hooks/*.json` (and the hook scripts
they point at), `**/evals/evals.json`, plus `**/scripts/*.py|mjs|js` for the plugin-boundary rule
below.

- **Descriptions are the routing surface.** Any model-invocable description edit updates its
  `evals/evals.json` in the same change, closes reciprocal fences in sibling suites, and gets an
  `/check-routing` after boundary changes.
- **A semantic edit rides with a critic.** A semantic edit to a prompt-carrying artifact (a
  SKILL.md body, an agent definition, a hook prompt) gets a fresh-context `*-checker` pass before
  its loop closes, whichever flow applied it — inline fix, unattended dispatch, or a host session.
  Lint and gates prove mechanics, not semantics (2026-08-11 audit: every recent unaudited semantic
  edit carried a real gap). The contract is encoded where those flows live — `file-bug`'s
  fix-inline branch, `dispatch-ticket`'s build path, `make-skill`'s P5. Pure code/config under the
  repo's own test gates is exempt. **The invariant's UNIT** — semantic (earns the dispatch, at any
  diff size) vs. mechanical (a ledger-line trim, a version renumber — floor-tier verification in
  the same loop suffices) — is calibrated in harness's `checking-rules` (2026-08-16, #272); don't
  re-derive the boundary here.
- **Plugin boundaries are hard for preloads and `${CLAUDE_PLUGIN_ROOT}` paths, soft for mentions.**
  Cross-plugin handoffs are named mentions that degrade gracefully when the other plugin isn't
  installed; an agent preload or script path crossing plugins is a defect (plan-plugin-split's
  `surface_map.py check` kills it).

Split from CLAUDE.md (issue #262, 2026-08-16).
