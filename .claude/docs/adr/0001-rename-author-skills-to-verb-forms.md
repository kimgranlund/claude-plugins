---
doc-type: adr
id: adr-0001
status: accepted
date: 2026-07-09
ratified: 2026-07-09 (maintainer, in-session)
owner: kim.granlund
---
# ADR-0001 — Rename the `-author` skills to verb forms

## Context

The first harness-audit (2026-07-09) flagged nine skills whose name head is `author`/`refactor`
(lint W4: agents take agentive `-er`/`-or` heads; skills take verb or knowledge-noun forms). The
legacy corpus's naming convention deliberately used `-author` for maker skills, so this is a rules
conflict, not drift: either the lint's grammar yields (allowlist `-author`) or the names yield
(mass-rename). The names are public routing surfaces in a published marketplace — renaming is a
breaking change for anyone typing them, and touches ~200 live references plus 3 agent preload
edges. The maintainer chose the rename, against the session's allowlist recommendation, to keep
one naming grammar across the estate: agents are actors (`-er`/`-or`), skills are actions or
knowledge.

## Decision

We will rename eight of the nine flagged skills to verb-form names and exempt the ninth as a lint
false positive, per this manifest:

| Current | New | Rationale |
|---|---|---|
| `scribe:rubric-author` | `rubric-forge` | `-forge` is the house maker verb (doc-forge, skill-forge, pack-forge) |
| `scribe:reference-author` | `reference-forge` | same |
| `scribe:knowledge-author` | `knowledge-forge` | same; existing fence vs forge's `pack-forge` (corpus waves vs minting the pack) carries over unchanged |
| `scribe:llms-txt-author` | `llms-txt-forge` | same |
| `scribe:vision-memo-author` | `vision-memo-forge` | same |
| `ui:component-author` | `component-forge` | same; `component-reviewer`'s preload updates in the same change |
| `typography:typography-system-author` | `typography-system-design` | matches its sibling pattern `palette-design` (color plugin) — the skill designs a point in design space, it does not draft a document |
| `design-systems:design-system-author` | `design-system-hub` | its own first line is "the cross-platform hub"; a router/doctrine seat, not a maker — the name should say what it is |
| `forge:skill-refactor` | *(keep)* | `refactor` is a genuine verb; W4's `-or` suffix check false-positives on it. Fix the lint (verb allowlist + selftest fixture), not the name |

The three `design-system-author-*` platform siblings (`-dscard`, `-figma-make`, `-google-stitch`)
keep their names this pass: their heads are not flagged, their churn is the largest of all, and
the `-author-` infix can retire in a later natural rename. The asymmetry (hub renamed, siblings
not) is accepted and recorded here.

Execution follows forge's `skill-refactor` discipline: manifest ratified before any move; every
live reference rewritten in the same change (~200 across descriptions, fences, suites, agents,
READMEs); retired handles noted in each affected suite; sweep proof (zero live references to old
handles outside CHANGELOGs/this ADR); full blind eval-run re-measure after; version bumps + gates
for every touched plugin.

## Consequences

- One grammar estate-wide: `-er`/`-or` reads as agent, verb reads as skill — the routing surface
  and the naming standard stop contradicting each other, and W4 becomes enforceable at zero
  standing noise.
- **Breaking**: anyone invoking `/rubric-author` (etc.) or referencing the old handles in external
  projects must migrate; the marketplace ships this as a minor-version bump per plugin with the
  rename in each ledger. Old names are not aliased — the platform has no skill-alias mechanism, so
  stale references fail visibly rather than silently.
- ~200-reference rewrite plus a full re-eval-run is real work paid once; the alternative
  (allowlist) was cheaper but would have carried the convention conflict forever.
- The accepted sibling asymmetry in design-systems remains until a future pass.

## Alternatives considered

- **Allowlist `-author` as a sanctioned maker head** (the session's recommendation): zero churn,
  keeps the legacy convention documented. Rejected by the maintainer: it makes W4 permanently
  advisory for the largest name family in the estate and preserves two competing grammars.
- **Rename only the scribe five, leave ui/typography/design-systems**: partial consistency;
  rejected as producing a third state (some makers `-forge`, some `-author`).

## Acceptance

- `grep -rn` for each old handle across the workspace returns only CHANGELOG/ADR/attic hits.
- `skill_lint.py` estate sweep: zero W4 warnings (including `skill-refactor` via the verb
  allowlist, proven by a selftest fixture).
- Post-rename blind eval-run: renamed skills' suites route at parity or better with their
  pre-rename scores.
- All touched plugins gate CLEAN and package at bumped versions.
