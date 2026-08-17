# decision-watcher sweep — 2026-08-17T18:31:58Z

Classify: 20 ADRs scanned, 1 amended (adr-0020: proposed -> accepted), 0 new, 1 newly_superseded
(adr-0015), edge adr-0020 -> adr-0015.

Judgment — adr-0020: impact-detector fires (ratified decision, gh#518 live tie-break). Placement
check found it already harvested — authorkit/skills/naming-conventions/references/GRAMMAR.md
(Productions/reserved-head/RoleLex sections cite ADR-0020 D3 directly), SKILL.md, and README's
ledger (v0.19.1 wave 1 #519, v0.19.2 wave 2 #520) already record it landed. No-candidate finding:
reject as duplicate.

Superseded ADRs — adr-0015 (partial, per adr-0020's own frontmatter): only D1's "RoleLex closed to
the coordinative three" framing is superseded; the {scope}-{role} production itself stands
unamended. Grepped skills/*/references/*.md + SKILL.md for adr-0015 citations: GRAMMAR.md (8),
MIGRATION.md:54, FRONTMATTER.md:20, SKILL.md:35 — all cite D1's production shape, D2, D3, or D4;
none cites the superseded closed-three clause, and GRAMMAR.md:110's RoleLex count already reads
14 (ADR-0015 D3, ADR-0017, ADR-0020). No-candidate finding: nothing downstream depends on the
superseded clause.

Candidates queued: 0 new. Pending total: 0.

Checkpoint: advanced to reflect adr-0020's new hash/status and adr-0015's hash (status unchanged,
still accepted per its own frontmatter — supersession represented only via adr-0020's
`supersedes:` field per the frontmatter dialect's contract). Queue: unchanged (still empty, no
block emitted).

Batched confirm: not applicable (0 pending).
