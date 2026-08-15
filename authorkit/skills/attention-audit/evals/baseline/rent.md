# Baseline — menu-cost question (WITHOUT attention-audit)

Conditions: fresh-context general-purpose agent, 2026-08-15, prompt = eval t03 verbatim.
Honest contamination note: the agent ran in the campaign worktree and noticed the in-progress
skill dir (read intent.md/evals AFTER measuring); the measurement method itself used no skill
content (none exists yet) — ad-hoc python over frontmatter, no repeatable script, no negative
control. Baseline validity holds; noted for the record.

## Measured numbers (better than the seeding session's own ad-hoc pass)

- 140 SKILL.md descriptions = 83,426 chars. 23 skills are `disable-model-invocation: true`
  and correctly EXCLUDED from the routing menu (12,214 chars that never bill) → routable
  ceiling 117 skills ≈ 71,200 chars ≈ 17.8–20.3k tokens.
- 30 agent descriptions = 20,188 chars ≈ 5.0–5.8k tokens.
- Estate ceiling ≈ 91,400 chars ≈ 22.9–26.1k tokens/turn.
- Per-plugin (chars/count/avg): harness 24,096/48/502 · design 17,248/22/784 ·
  screens 10,892/15/726 · teamwork 8,189/13/630 · docs 7,797/16/487 ·
  agent-protocols 5,268/8/658 · llm 4,984/9/554 · authorkit 4,268/8/534.
  7 of the top-10 longest descriptions are design skills (1,000–1,100 chars each).

## Two findings that become script requirements

1. **Respect the dials**: rent.py MUST exclude `disable-model-invocation: true` skills from
   the routable figure (report them as a separate zero-rent count) — the naive all-files sum
   overstates by ~12k chars.
2. **Skills and agents degrade differently**: observed this turn — all 30 agent descriptions
   rendered verbatim (zero elision, tax paid in full unconditionally), while whole plugins'
   skill descriptions were elided to bare names by the runtime (selection rule unknown,
   runtime-owned). Report skill-ceiling, agent-cost, and realized-vs-ceiling as SEPARATE
   figures; agents are proportionally the more expensive char.

Also flagged as same-category always-on costs, kept separate (never blended): MCP server
instruction blocks (Figma alone >2k chars) and the two CLAUDE.md files (~13KB combined).

## Delta the skill must demonstrate over this

Same numbers from one repeatable script run with selftest + negative control, dial-aware and
skill/agent-split by construction, trend-appended instead of evaporating — vs a one-off
session that cannot be re-run identically next release.
