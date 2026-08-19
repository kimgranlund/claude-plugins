# Changelog — a2ui-catalog-design

## 2026-08-19 — field-doctrine harvest (agent-ui ADR wave)

Two reference UPDATE sections, ADRs fetched verbatim from `kimgranlund/agent-ui` (all cited records
`accepted`):

- `component-definition-contract.md`: the ADR-0211 wire-mark shape law (no `value` mark without a
  real readback accessor — the data-corruption class, probe-verified), ADR-0207 append-only enum
  widening (baselines byte-identical, drift pins pass unedited, zero validator code), and two
  validates-cleanly defect classes — schema-omission (conformance never descends into object keys)
  and mount-context probe artifacts (GH #1328/#1329 → PR #1404).
- `coverage-policy-and-drift-gates.md`: mint-vs-compose incl. the REVERSE direction (ADR-0201
  retiring the #1174 composed receipt when the omission law became enforceable by construction),
  the smallest-floor-that-earns-the-name test (ADR-0107 → ADR-0205, two worked instances), and the
  NESTED_ONLY-vs-browsable chrome-ownership discriminator (GH #1332, Segment vs Radio).
- `INDEX.md`: both rows' ask-classes widened to carry the new questions. No description/evals
  change (routing surface untouched).

## 2026-07-07 — minted

Knowledge pack minted (knowledge-author procedure), grounded in `@agent-ui/a2ui`'s shipped catalog
layer at Wave-D landed state (ADR-0087 whole-fleet coverage, `EXCLUSION_ALLOWLIST` empty).

- Six axes + provenance (7 `references/` files): component-definition-contract · factory-and-widget-
  resolution · two-tier-extensibility · naming-law · coverage-policy-and-drift-gates ·
  security-allowlist-and-conformance · sources.
- `references/INDEX.md` typed retrieval surface; `SKILL.md` entry surface (answers-only,
  `user-invocable: false`); `scripts/routing-corpus.json` corpus of record.
- Every claim cited to `packages/agent-ui/a2ui/src/catalog/**` `file:line` or an ADR/SPEC clause
  (0016 / 0053 / 0087 · SPEC-R1…R9 / N1…N3 / §5.1–5.2.1).
- Gates: skill-author harness 15/15; routing eval F1 0.788 (recall 0.929).
- Making routed out to the `a2ui-builder` / `a2ui-composer` / `a2ui-reviewer` agents; sibling packs
  `a2ui-protocol` (wire), `a2ui-training-corpus`, `a2ui-conversational-agent`.
