# Attention report — template

Verdict-first, separate series, evidence per finding. Never a combined quotient.

```markdown
# Attention audit — <estate> — <date>

🟢/🟡/🔴 <one-sentence verdict: the single most expensive finding, or "rent proportionate">

## Rent (always-on, per turn)
| Plugin | Routable skills | Skill chars | Zero-rent (command-only) | Agents | Agent chars |
|---|---|---|---|---|---|
...one row per plugin, then the estate total row. Est. tokens = chars/4, stated once.
Note: agent chars bill unconditionally; skill chars are the ceiling (runtime may elide).

## Collisions (cross-plugin included)
One block per flagged pair: the two qualified names, shared distinctive terms, whether either
side fences the other, and the recommended fix — ONE category from SKILL.md's structural-fix
set (reciprocal fence · demote-to-wiring · merge · centralize-boilerplate · retire), its owner,
and — when it isn't the default fence — the one criterion that fired (e.g. "fence-tight:
headroom 12 < 23" or "already fenced once"). A rent finding with no collision partner draws
from the same set minus reciprocal fence, but renders in Retire/merge candidates' "proposed
action" slot below, not here — this block is pair-shaped.

## Usage cross-reference
Zero-evidence list AFTER lineage + preload correction (state both corrections ran; name the
lineage map used or "none supplied"). Telemetry host + date range.

## Retire / merge candidates
Each candidate: name · signal 1 (value) · signal 2 (value) [· signal 3] · proposed action ·
owner. Two-signal minimum is a hard floor — a candidate with one signal is not listed.

## Trend
The appended row(s) verbatim, and the delta vs the previous row per plugin. Columns missing a
source (no routing report) print `absent`.

## Handoffs
Every fix named with its owner (the owning plugin edits; harness check-routing proves after).
This report changes nothing itself.
```
