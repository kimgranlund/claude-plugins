# Routing-accuracy evals — measure it, don't feel it

> Axis: how to know whether a skill's routing (does it fire when it should, stay silent when it
> shouldn't) is actually accurate, as a tracked number across repeated runs — not a felt sense
> from a handful of interactions. Grounded in a worked instance: this workspace's own,
> real, dated check-routing history and its blind-judge mechanism.

## The core discipline — routing accuracy is a number you track over runs, not a vibe

**Claim:** "this skill seems to trigger fine" is not a measurement — it is an impression formed
from whichever handful of prompts happened to come up. A routing-accuracy eval fixes this by
running a **held-out set** (prompts the description's own wording was not tuned against after the
fact) of both **positive** cases (should trigger) and **adversarial negative** cases (should NOT
trigger, drawn specifically from the near-neighbor skills most likely to steal or leak the case) —
through something that mimics the real router's decision — and recording a score, repeatably,
so a later run can be compared against an earlier one.

## The dual-schema corpus — a held-out set, not a description self-check

**Claim — every skill in this plugin (including the two this pack is templated on, and this pack
itself) carries the same paired artifact:** `scripts/routing-corpus.json` and
`evals/evals.json` — identical case content in two schemas, so both a legacy and a forge-native
eval tool can regress the same suite. Each case is a `{id, prompt, expect}` triple, `expect` ∈
`{trigger, no-trigger}`. **Mechanically enforced shape (this workspace's `eval_check.py`):** valid
JSON with a non-empty `cases` list (`E1`); every case has a unique `id`, non-empty `prompt`, and a
valid `expect` (`E2`); the suite's declared `skill` field must match its owning directory name so
a copied suite can't silently lie about which skill it belongs to (`E3`); duplicate prompts across
cases warn (`E4`); and a case-mix floor of at least 5 trigger / 3 no-trigger cases warns if unmet,
because a suite thinner than that "tunes nothing" (`E5`) — verified directly from
`eval_check.py`'s own rule comments. **Why negatives are drawn adversarially, not randomly:** a
random negative ("what's the weather") proves nothing about routing precision; a negative drawn
from the wording of a genuine sibling skill's description proves the two skills are actually
distinguishable at the boundary that matters.

## A worked, dated measurement history — judge noise vs a real fix vs a structural leak

**Worked instance — this workspace's own `agent-protocols` plugin,
`skills/a2ui-chat-agent-facts/evals/evals.json`, its `"note"` field, read in full and quoted
verbatim (not paraphrased, since the exact wording is the evidence):**

> "Blind run 2026-07-09: 33/36 — t14 (validate-then-stream) stolen by a2ui-protocol-facts: the term
> added verbatim to this description; t03/t04... chose none DESPITE the phrasing standing verbatim
> — judge noise, recorded as first strike... Estate-wide run 2026-07-09: 33/36 — t03/t04 came home
> (judge-noise cleared) and t14... proven; n12/n13/n14... leaked... structural: agents are absent
> from any skill menu."

This single note demonstrates all three distinct outcomes a routing-accuracy measurement must be
able to tell apart, and conflating any two of them wastes effort:

- **Judge noise** — a case flips between runs with *no* description change in between (t03/t04
  choosing `none` despite the matching phrasing standing verbatim). **Discipline:** record it as a
  "first strike," do not immediately chase a description rewrite for it — re-run before concluding
  a regression is real. The SAME note shows the resolution: on a later run, "judge-noise cleared,"
  no wording changed.
- **A real, fixable regression** — a case actually lost to a *specific, nameable* cause (t14 stolen
  because another skill's description added the exact term verbatim). **Discipline:** this one
  IS worth a wording fix, because the cause is concrete and nameable, not noise.
- **A structural leak** — a case that will lose **every time**, for an architectural reason no
  wording change can fix (n12/n13/n14 — asks for *making* something, which are owned by builder
  *agents*, leaked to a *skill* pack because "agents are absent from any skill menu" the judge
  ever sees). **Discipline:** the fix here is not a better description — the note records this as
  "by design," handled by the pack's own Boundaries section performing the two-hop handoff (a
  human or a routing layer reads the skill's boundary prose and redirects to the agent), not by
  trying to make a skill description win a router decision it structurally cannot win.

**A fourth outcome, added from a later measured run [2026-07-21, this workspace's ADR-0008 design
merge, PR #73]: the menu-scope collision.** When plugins merge, a case can fail with NO description
change and NO judge noise — the *menu itself* changed. A grammar-bare prompt ("what type token for
this heading") that routed correctly inside its source plugin's small menu collides in the merged
union menu, where a sibling legitimately claims the same phrasing and only ambient project context
(which a blind judge lacks) disambiguates. **Discipline:** heal the *prompt*, not the descriptions
— an ordered context split restores the marker the plugin-scoped menu used to carry ("what md-sys
type token for this heading"); both descriptions were already correct. The same run calibrated
single-judge noise at ~1.5% per ~520-case round and hardened the first-strike rule into "passes
2 of 3 rounds = noise, record and stop; fails 3 of 3 with a verbatim fence in place =
known-ambiguous, annotate and stop." Method detail: harness's
`plan-plugin-split/references/merge-seam-remeasure.md`, where installed.

## The blind judge — the measurer must see only what the real router sees

**Claim — the judge that scores a routing-accuracy suite must not see more than the router sees
at discovery time**, or its blindness is contaminated and the number it produces no longer
predicts real routing behavior. **Worked instance, verified directly from the agent definition
file** (`/Users/kimba/.claude/plugins/cache/nonoun-plugins/forge/1.21.0/agents/routing-judge.md`):
the `routing-judge` agent is declared with `tools: []` in its frontmatter — a genuinely empty tool
allowlist, not a documentation claim — and its own description states the reason explicitly: "a
judge that could read skill bodies, suites, or reports could contaminate its own blindness, so the
empty allowlist is the epistemic guarantee, not a limitation." Its dispatch prompt is described as
carrying, as its **entire world**, "the description menu and the shuffled, expectation-stripped
prompts" — no file access, no way to peek at a skill's full body or the suite's own expected
answers. **Why this is the right shape for the measurer, not an accident:** a routing decision in
real use is made from descriptions alone, before any skill's body is ever read — a judge that
could Read a skill's reference files would be answering a different, easier question ("does this
prompt relate to this skill's content") than the one that actually determines routing ("does this
prompt match this skill's description, sight-unseen").

## What this file does NOT cover

Deterministic hook-based logging of what a tool call actually did, a different (and non-statistical)
observability signal (logging-and-tracing) · notifying a human when background work completes
(background-task-notification) · the provenance split between a platform mechanism this pack cites
and this workspace's own measured, dated run history (sources).
