# Changelog — a2ui-catalog-design

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
