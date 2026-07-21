---
name: naming-rules
description: >-
  The simple naming paradigm for harness artifacts — plugins, skills, commands, agents. Use when
  naming something new ("what should we name this skill/plugin/agent", "what should I call it"),
  simplifying a name ("is this name too vague", "name this so it reads like plain English",
  "a name a five-year-old would understand"), reviewing names for simplicity, or naming a
  skill↔agent pair. NOT for the legacy estate grammar, or why the EXISTING estate's names are
  structured the way they are (agent-writing-rules §Naming; skill_lint's checkable slice);
  NOT for executing renames across an estate
  (big-change-git-rules — names are APIs); NOT for plugin partitioning (plan-plugin-split);
  NOT for code identifiers — variables, functions (general engineering).
disable-model-invocation: false
user-invocable: false
---

# naming-rules

A name under this paradigm is understood on first sight by a reader who has seen no manual: it
says what the thing does, in words a child knows, in a shape that announces its kind. The
paradigm governs ALL names in this estate — ADR-0006's rename campaign (executed 2026-07-21)
brought every shipped plugin and member onto it, so a new name conforms and an existing name
already does. Shipped names remain APIs; changing one is still a deprecation campaign (ADR +
branch + PR), not an effect of this skill.

## The five tests — normative

A proposed name passes all five or gets reworked; the test that fails names the fix.

| # | Test | Rule (as world-state) | Contrast (bad side labeled) |
|---|---|---|---|
| 1 | says-the-job | An invocable name completes "I want to ___" read aloud | Bad: `make-skill` → Good: `make-skill` |
| 2 | kind-audible | The shape alone identifies the kind (table below) | Bad: `feature` (verb-less runnable) → Good: `file-feature` |
| 3 | registry-verb | The verb comes from the registry — one verb per concept, kindergarten vocabulary | Bad: `tidy-docs` → Good: `tidy-docs` |
| 4 | no-lore | Zero metaphor, mythology, or seniority theater; a shelf noun says what the shelf holds | Bad: `harness`, `docs` → Good: `harness`, `docs` |
| 5 | loud-contrast | Siblings differ by a whole word; a suffix or number as the only difference is a test-5 failure | Bad: `check-skill` + `check-all-skills` coexisting → Good: `check-skill` + `check-all-skills` |

## Shapes by kind — normative

| Kind | Shape | Examples |
|---|---|---|
| Runnable (command or procedural skill) | verb-first: `verb-noun` | `make-skill`, `check-doc`, `ship-plugin` |
| Knowledge — binding | noun + activity + `-rules` | `doc-writing-rules`, `icon-rules` |
| Knowledge — factual | noun + `-facts` | `github-facts`, `material-color-facts` |
| Agent (a seat) | noun + person-word: `-checker`, `-builder`, `-sorter`, `-planner`, `-lead` | `skill-checker`, `issue-sorter`, `team-lead` |
| Plugin (a shelf) | plain noun naming what the shelf holds | `harness`, `docs`, `teamwork`, `screens`, `color` |

## The verb registry — normative

One concept, one verb. A retired synonym appearing in a new name is a test-3 failure; a new
concept earns a new verb only when no registry verb fits.

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

## Refinements — normative

- **`-rules` carries its activity** wherever the domain has more than one rule family:
  `doc-writing-rules`, never `doc-rules` — a bare `X-rules` reads as all rules about X.
- **`-facts` vs `-rules`**: facts state what is true (protocols, science, platform behavior);
  rules state what must be followed. A mixed catalog is named by its dominant half.
- **Twins**: a command and the agent it dispatches are verb↔noun of the same words —
  `/sort-issues` ↔ `issue-sorter`, `/lead-team` ↔ `team-lead`. A twin sharing one literal name
  across artifact types is a test-2 failure (the kind is inaudible).
- **Deciders vs doers**: `plan-` names decide (`plan-skill-split`); bare-verb names execute
  (`reshape-skill`, `merge-skills`).
- **Reserved-word escape**: the name points at the artifact, never the platform —
  `entry-file-rules`, not `check-claude-md` (the install-rejection rule itself is
  skill-writing-rules' F8 row).
- **Term-of-art exception**: a term users type verbatim outranks the shape grammar — `llms-txt`,
  `a2a`, `ui` stay as-typed (rule owned by skill-writing-rules, 2026-07-15 amendment).

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
