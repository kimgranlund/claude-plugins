# Baseline — collision question (WITHOUT attention-audit)

Conditions: fresh-context general-purpose agent, 2026-08-15, prompt verbatim = eval t06's
territory: "Are any of our skill descriptions so similar they'll collide in routing?" Repo:
/Users/kimba/Projects/nonoun/plugins (main tree). No method hints given.

## What the baseline did

Extracted all 140 SKILL.md description frontmatters across 8 plugins, then LLM-judged pairwise
overlap looking for shared trigger phrases with no disambiguating NOT-fence. One-off sweep:
no artifact, no determinism (a re-run could rank/word findings differently), full-context cost
paid in one session, no negative control, no trend.

## Verbatim findings (kept — these are real, feed the campaign's Phase C proving run)

Verdict: corpus unusually disciplined; same-plugin families fence reciprocally. Three real
gaps, ALL cross-plugin:

1. **harness:naming-rules vs authorkit:naming-conventions** — both answer "what should I name
   this / naming grammar"; neither description mentions the other. The old-canon/new-canon
   split (ADR-0006 grandfathered vs ADR-0011 new names) is documented in CLAUDE.md prose, not
   on the routing surface. A bare "what should I name this skill" can land on either.
2. **harness:check-skill vs authorkit:bloat-audit** (extends to check-all-skills /
   check-all-agents) — both trigger hard on "review/audit this skill"; bloat-audit's NOT-list
   has no harness cross-reference, and check-skill doesn't fence toward bloat-audit.
3. **harness:break-down-problem vs screens:break-down-layout** — break-down-problem names "UX
   architecture" in-scope; break-down-layout owns exactly that (app shells, frame→regions).
   Neither fences toward the other.

Baseline's own meta-observation: same-plugin authors cross-reference each other consistently;
the fencing discipline is not applied across plugin lines — and /check-routing runs per plugin,
so cross-plugin collisions are structurally invisible to today's tooling.

## Delta the skill must demonstrate over this

Deterministic (same input → same flags), artifact-producing, negative-control-proven,
cross-plugin BY DEFAULT (the baseline's finding: the blind spot is exactly the plugin
boundary), and cheap enough to run at write time — vs one expensive judged sweep with
unreproducible output.
