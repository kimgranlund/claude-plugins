# Migration — grandfathering, exemptions, rename discipline

Posture: **enforce for new names; grandfather existing ones.** A grammar
without a migration mechanism is dead paper.

## The exemptions array

- Lives in the target estate's naming.manifest.json, one non-conforming name
  per entry, verbatim.
- Grammar checks skip exempt names (findings recorded as EXMPT for the
  burn-down). Frontmatter, layout, policy, and provenance checks still apply
  — legacy names get the governance layer without waiting for renames.
- **The array may shrink and may never grow.** CI diffs it; additions fail.
- Exemption count is a burn-down metric, reported by every audit run.

## Rename discipline

Renames are a known drift source: invocation strings live in prompts, hooks,
workflow configs, wrapper declarations, and requires edges. Therefore:

- Retire exemptions opportunistically — when an artifact is otherwise being
  touched — never as a big-bang campaign.
- Every rename goes through rename-planning first (blast-radius enumeration)
  and rename-execute second (atomic apply + post-verify via the validator).
- The post-execute verify is the same validator that audits — one oracle,
  two call sites, no drift between mint-time and audit-time rules.

## Seeding a new estate

An ungoverned estate (no manifest) is offered a seed on first audit contact:
copy MANIFEST-TEMPLATE.json, populate AuthorRegistry and lexicons via
manifest-authoring, enumerate the exemptions array from the first audit's
violation list. Governance is opt-in per estate, activated by the manifest's
existence — the hook no-ops without one, so installing authorkit never
bricks a legacy repo.

## schema_scope — the structural channel is opt-in per estate

`naming.manifest.json` may carry `"schema_scope": "grammar" | "full"` (2026-08-14,
issue #226, executing #224's ruling b). The four provenance fields
(`kind`/`author`/`created`/`last_updated`) are authorkit-internal convention, not
estate law — nothing outside authorkit reads them, so gating an estate that never
adopted that schema on hundreds of structural findings is unmade-adoption noise,
not a real defect.

- **`"full"`** (the default when the field is absent — back-compat, an existing
  manifest with no opinion behaves exactly as before): every finding gates —
  grammar and structural alike. Authorkit's own `naming.manifest.json` runs this
  way; it dogfoods the full schema on itself.
- **`"grammar"`**: only naming-grammar findings gate; structural findings for
  artifacts OUTSIDE authorkit's own tree are dropped entirely from the run (not
  merely non-gated) — the load-bearing half (name production, lexicon
  disjointness, the reserved `-agent` head — mandatory on skills/the primary
  agent production, optional on the orchestrator production per ADR-0015 D1)
  stays fully policed everywhere, regardless of this field. Artifacts INSIDE authorkit's own tree still get the
  full structural check even when the estate's own tier is `"grammar"` —
  authorkit keeps dogfooding `"full"` on itself.
- **One field, one manifest per estate** — never a hardcoded per-consumer plugin
  list (the stale-list defect class that recurred 3x this week: `gate.yml`,
  `marketplace.json`, the hook loop). Any caller that omits `--scope` inherits
  this field's choice; an explicit `--scope` flag on the CLI always overrides it
  (the PostToolUse hook and `release_gate.py`'s G12 both keep their own existing
  call patterns — G12 always passes `--scope grammar` explicitly, so this field
  never changes its behavior).
