---
name: naming-rules
description: >-
  Simple naming paradigm for plugins, skills, commands, agents. Use when naming something new
  ("what should we name this skill", "what should I call it"), simplifying a name ("too vague",
  "plain English", "five-year-old simple"), reviewing names, contrasting similar siblings, or a
  skill↔agent pair. NOT for legacy estate grammar (agent-writing-rules); NOT for executing
  renames (big-change-git-rules); NOT for plugin partitioning (plan-plugin-split); NOT for
  judging a name against the estate's ADR-0011 grammar or frontmatter/tool-grant schema
  (authorkit's naming-conventions).
disable-model-invocation: false
user-invocable: false
---

# naming-rules

A name under this paradigm is understood on first sight by a reader who has seen no manual: it
says what the thing does, in words a child knows, in a shape that announces its kind. The
paradigm governed ALL names in this estate through 2026-08-13 — ADR-0006's rename campaign
(executed 2026-07-21) brought every shipped plugin and member onto it — and every one of those
names stays exactly this shape (see the supersession note below: grandfathered, not renamed).
Shipped names remain APIs; changing one is still a deprecation campaign (ADR + branch + PR),
not an effect of this skill.

The no-lore test (below) is Dieter Rams' "as little design as possible" applied to naming: a
name earns every syllable it spends, nothing decorative, nothing added to sound important.

> **Supersession note (2026-08-14, ADR-0011 D9):** this skill's GRAMMAR — the five tests, the
> shapes-by-kind table, the verb registry below — is superseded as estate-wide canon by the
> harness artifact naming convention spec, ratified ADR-0011: `.claude/docs/spec/spec-naming-
> convention.md` (a plain document, not a routable skill — reach it through the validator's
> failures or the doc tree). Every name this estate shipped before 2026-08-14 is grandfathered
> verbatim into `naming.manifest.json`'s `exemptions` array (D8: grandfather + ratchet, no
> rename campaign) — nothing below is wrong about any name that already exists, and this file
> stays the accurate historical record of the grammar those names were built to. A genuinely
> NEW name conforms to the spec's grammar from day one, checked by authorkit's naming-audit
> validator (`--scope grammar`), not by the tests below. **What this file's discipline still
> governs, unchanged:** the symmetry hardline (frontmatter `name:` == directory/file stem,
> `skill_lint` F9/A6, mechanically enforced at write time and ship time) and the general
> practice of naming with intention — both survive the grammar swap intact.

## The five tests — historical (the grammar this estate's ~155 existing names were built to)

A name under this grammar passed all five or was reworked; the test that failed named the fix.
A new name is checked against the spec instead (see the supersession note above).

| # | Test | Rule (as world-state) | Contrast (bad side labeled) |
|---|---|---|---|
| 1 | says-the-job | An invocable name completes "I want to ___" read aloud | Bad: `skill-forge` (retired name, kept as the counterexample) → Good: `make-skill` |
| 2 | kind-audible | The shape alone identifies the kind (table below) | Bad: `feature` (verb-less runnable) → Good: `file-feature` |
| 3 | registry-verb | The verb comes from the registry — one verb per concept, kindergarten vocabulary | Bad: `docs-alignment` (retired) → Good: `tidy-docs` |
| 4 | no-lore | Zero metaphor, mythology, or seniority theater; a shelf noun says what the shelf holds | Bad: `forge`, `scribe` (retired) → Good: `harness`, `docs` |
| 5 | loud-contrast | Siblings differ by a whole word; a suffix or number as the only difference is a test-5 failure — and "sibling" means the whole installed estate, not one plugin: every name shares one flat menu, so a plugin boundary mutes nothing | Bad: `chores-lead` proposed while harness ships `chore-lead` — one letter apart across a plugin boundary, rejected live (ADR-0010, 2026-08-10) → Good: `build-lead` |

## Shapes by kind — historical

| Kind | Shape | Examples |
|---|---|---|
| Runnable (command or procedural skill) | verb-first: `verb-noun` | `make-skill`, `check-doc`, `ship-plugin` |
| Knowledge — binding | noun + activity + `-rules` | `doc-writing-rules`, `icon-rules` |
| Knowledge — factual | noun + `-facts` | `github-facts`, `material-color-facts` |
| Agent (a seat) | noun + person-word: `-checker`, `-builder`, `-sorter`, `-planner`, `-lead` | `skill-checker`, `issue-sorter`, `team-lead` |
| Plugin (a shelf) | plain noun naming what the shelf holds | `harness`, `docs`, `teamwork`, `screens`, `color` |

## The verb registry — historical

One concept, one verb, under this grammar. A retired synonym appearing in a name built to this
grammar was a test-3 failure. A genuinely new name is not checked against this registry — see
the supersession note above.

| Verb | Concept | Retired synonyms |
|---|---|---|
| `make` | create an artifact | forge, author, compose, scaffold, generate |
| `check` | judge an artifact against a bar | review, audit, verify, validate, judge |
| `plan` | decide before doing | decompose (decision sense), propose, assess |
| `split` / `merge` | execute a partition verdict | decompose (execution sense), synthesize, refactor |
| `break-down` | two-axis analysis of a whole | decompose (analysis sense) |
| `fix` | repair a defect | remediate, repair, resolve |
| `clean` / `tidy` | restore order, no behavior change | align, groom, organize |
| `ship` | release through the gate | release, publish |
| `file` | record an intake item | report, capture, log |
| `find` | surface what is hidden | extract, sweep, detect, discover |
| `save` | keep something durable | harvest, persist |
| `write` | produce prose | compose, draft |
| `sort` | triage into buckets | triage, classify |
| `pick` | choose among options | select, choose, decide |

## Refinements — mixed (grammar rows historical; the escape-hatch pointers below stay live)

The first four bullets are grammar detail for the historical shapes above (superseded for new
names, same as the sections before them). The last two — reserved-word and term-of-art — are
standing exceptions any grammar honors, spec included; skill-writing-rules and ADR-0008 own them
regardless of which naming grammar is canon.

- **`-rules` carries its activity** wherever the domain has more than one rule family:
  `doc-writing-rules`, never `doc-rules` — a bare `X-rules` reads as all rules about X.
- **`-facts` vs `-rules`**: facts state what is true (protocols, science, platform behavior);
  rules state what must be followed. A mixed catalog is named by its dominant half.
- **Twins**: a command and the agent it dispatches are verb↔noun of the same words —
  `/sort-issues` ↔ `issue-sorter`, `/bind-team` ↔ `fleet-marshal`. A twin sharing one literal name
  across artifact types is a test-2 failure (the kind is inaudible).
- **Deciders vs doers**: `plan-` names decide (`plan-skill-split`); bare-verb names execute
  (`reshape-skill`, `merge-skills`).
- **Reserved-word escape**: the name points at the artifact, never the platform —
  `entry-file-rules`, not `check-claude-md` (the install-rejection rule itself is
  skill-writing-rules' F8 row).
- **Term-of-art exception**: a term users type verbatim outranks the shape grammar — `llms-txt`,
  `a2a`, `ui` stay as-typed (rule owned by skill-writing-rules, 2026-07-15 amendment).
- **Term-of-art stutter exception** (ADR-0008, extending ADR-0006 Decision 7 to members): a
  member name may contain its plugin's word when that name IS the real-world term —
  `design:make-design-system` (the artifact is a design system), `design:design-md-rules`
  (DESIGN.md is the filename). Decorative repetition of the plugin word is still a
  test-2/no-stutter failure.

## The symmetry hardline — normative, mechanically enforced

A name exists in three places at once — frontmatter `name:`, the directory (or agent
filename), and every doc/fence/routing-table reference — and the frontmatter copy is the only
one the harness registers. Any drift ships an unreachable command that looks documented
(2026-07-21/23: six commands shipped this way — file-feature, file-task, sort-issues,
sweep-chores, plan-chores, build-feature — each found late, by a routing re-measure or in
passing, never by a gate).

- **Skill frontmatter `name:` equals its directory name; agent `name:` equals its file stem.**
  Not a convention — `skill_lint` F9/A6 FAIL on drift, at write time (the PostToolUse hook) and
  at ship time (the gate composes the lint). A rename is complete only when frontmatter, path,
  and references move in the SAME change — F9/A6 police the first two; references stay on the
  reviewer and the gate's G8 sweep.
- The incident mechanism to watch: three of the six drifted precisely because frontmatter still
  carried a retired same-name twin pairing. The Twins refinement above (command = verb, seat =
  role noun) is what a rename moves the frontmatter TO; F9/A6 catch the copy that lags behind.

## Worked contrast — illustrative

Naming the issue-triage pair (a scheduled triage seat plus its on-demand dispatcher):

```
Bad (counter-example — do not imitate):
  skill: issue-sorter        agent: issue-sorter
  — lore prefix, verb-less, twin shares one literal name; kind inaudible (tests 1, 2, 4, 5)

Good:
  command: /sort-issues    agent: issue-sorter
  — verb-first runnable, person-word seat, same words verb↔noun
```

## Worked example at estate scale — illustrative

`references/estate-rename-map.md` holds the full 2026-07-20 mapping of the nonoun estate
(9 plugins, ~130 members) from legacy grammar to this paradigm, including the findings that
motivated each rule. Ratified and EXECUTED as ADR-0006's rename campaign, 2026-07-21 — the map
is now the historical record of the transition, with per-plugin transition tables in each
README.
