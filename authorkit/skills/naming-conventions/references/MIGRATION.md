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
