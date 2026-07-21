# Sources & provenance

Every claim in this pack cites the agent-ui repo — this pack documents THIS repo's implementation of
the A2UI catalog layer, not a generic tutorial. Provenance in trust order. All source paths relative
to the repo root `/Users/kimba/Projects/nonoun/agent-ui/`. Dated 2026-07-07 (Wave D landed state).

## Tier 1 — the code (authoritative; verify claims here first)

The shipped source is the ground truth; specs/ADRs describe intent, code is what runs.

- `packages/agent-ui/a2ui/src/catalog/catalog.ts` — `Catalog`/`ComponentDef`/`PropDef`/`FunctionDef`
  schema model + `loadCatalog` (LLD-C1). Owner of `references/component-definition-contract.md`.
- `packages/agent-ui/a2ui/src/catalog/types.ts` — `WidgetFactory` / `CatalogEntry` /
  `CatalogRegistry` render contracts. Owner of `references/factory-and-widget-resolution.md`.
- `packages/agent-ui/a2ui/src/catalog/registry.ts` — the two-tier `Registry` (register / get /
  supportedCatalogIds / submitGateSelector). Owner of `references/two-tier-extensibility.md`.
- `packages/agent-ui/a2ui/src/catalog/naming.ts` — `validName` UAX-31 / reserved-`@` validator.
  Cited by `references/naming-law.md`.
- `packages/agent-ui/a2ui/src/catalog/conformance.ts` — `validateCatalogConformance` (the shared
  validator half). Owner of `references/security-allowlist-and-conformance.md`.
- `packages/agent-ui/a2ui/src/catalog/default/factories.ts` — the default factory table + the
  `accessorFactory`/bespoke split INVARIANT + the shipped per-type rationale. Heavily cited.
- `packages/agent-ui/a2ui/src/catalog/default/catalog.json` — the shipped catalog document (the rows).
- `packages/agent-ui/a2ui/src/catalog/default/index.test.ts` — the fleet-derived coverage gate,
  `EXCLUSION_ALLOWLIST`, `typesMissingCatalog`, negative controls. Owner of
  `references/coverage-policy-and-drift-gates.md`.
- `packages/agent-ui/a2ui/src/renderer/widget.ts` — `makeCreateWidget`, the resolution seam
  (`registry.get(catalogId)?.factories[type]`) + the CATALOG placeholder. Cited by
  `references/factory-and-widget-resolution.md` + `references/security-allowlist-and-conformance.md`.

## Tier 2 — the decision records (why the code is shaped as it is)

- `.claude/docs/adr/0087-a2ui-whole-fleet-catalog-scope-policy.md` — the whole-fleet policy flip, the
  CI-silent vs fleet-derived gate distinction, seed-and-drain, the four forks. Primary source for
  `references/coverage-policy-and-drift-gates.md`.
- `.claude/docs/adr/0053-a2ui-form-family-catalog-rows.md` — the bindable-naming law (fork F2), the
  form-family rows, the type↔tag bijection. Primary source for `references/naming-law.md`.
- `.claude/docs/adr/0016-a2ui-faithful-flex-layout-container-queries.md` — Row/Column/List/Grid; its
  List/Grid non-catalog exclusion was SUPERSEDED by ADR-0087 Fork A. Its Row/Column decision stands.
- Related, cited in passing: ADR-0019 (the one-`value`-mark two-way seam), ADR-0026/0034 (function
  args + `callableFrom`), ADR-0029 (component-level `checks`), ADR-0054 (the `submitGate` seam),
  ADR-0078 (the `Text.variant` fan-out).

## Tier 3 — the specs & LLD (the normative contract)

- `.claude/docs/specs/specs/a2ui-catalog.spec.md` — SPEC-R1…R9 + SPEC-N1/N2/N3 + §5.1 (typed
  contracts) + §5.2 (the normative row table) + §5.2.1 (the exclusion allowlist) + §5.3 (error
  codes). The owning doc for the per-row facts.
- `.claude/docs/specs/llds/a2ui-catalog.lld.md` — LLD-C1…C7 build-level design (load pipeline,
  registry, conformance, factories, resolution).

## Tier 4 — the external protocol (upstream authority)

- A2UI v1.0 (Google's Agent-to-Agent UI protocol, ~v0.9→v1.0). The catalog spec's Constraint C1 and
  SPEC-R8 derive from A2UI's own guidance: *a catalog is a JSON-Schema file declaring the components/
  functions/themes an agent may use, and clients SHOULD build catalogs that directly reflect their
  design system rather than adapting a generic (Basic) catalog.* This pack does not re-derive the
  wire protocol — for the message/node wire shape see the sibling `a2ui-protocol-facts` pack (when minted).

## Status note — ADR-0087 is code-landed, marker still `proposed`

ADR-0087 (whole-fleet coverage) carries `Status: proposed` (ADR-0087 header) — ratification lands at
the wave-gate close, not on the ADR itself. But the CODE has landed: all four forks resolved INCLUDE
(Kim, 2026-07-06), Waves A/B/C added the rows, and the `EXCLUSION_ALLOWLIST` is empty with gates
green (`default/index.ts:10-14`, `default/index.test.ts:142`). This pack answers from Tier-1 code
(the landed state), so it presents whole-fleet coverage as in-force; cite the `proposed` marker if a
user asks about formal ratification specifically.

## Verification note

A claim naming a `file:line` is a claim about the code AT WRITING (2026-07-07). Line numbers drift;
before recommending an action on a live claim, re-Grep the symbol rather than trusting the line.
