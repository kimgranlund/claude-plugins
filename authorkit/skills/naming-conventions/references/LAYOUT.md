# Layout — skill folder contract and content organization

## Closed set

```
skills/{name}/
  SKILL.md          # required — routing stub + procedure
  references/       # passive matter: read into context, never executed
  scripts/          # executable matter: code the procedure invokes
  assets/           # inert payload: addressed by path, neither read nor run
  evals/            # evals.json — the trigger-eval suite, model-invocable skills only
  intent.md         # bare top-level file — a skill's own living build-state record
```

Six top-level entries, nothing else (ADR-0024, 2026-08-21 — supersedes ADR-0011
§6.1's four-entry set: `evals/` was already an enforced, cross-plugin invariant
the spec had fallen behind; `intent.md` joins as the second bare top-level file,
alongside `SKILL.md`, because it is actively *written to* during a skill's own
forge and fails `references/`'s passive-matter test on both axes). Partition
axis: how content participates at run time — context, computation, payload,
regression proof, or build-state ledger. Deterministic logic belongs in
scripts/, never re-derived in prose.

Boundary validation (and no deeper): SKILL.md exists; no stray top-level
entries; nothing in scripts/ referenced from outside the skill; **no nested
skills** — sub-capabilities wanting their own triggers decompose into sibling
artifacts with `requires` edges, never a hierarchy. Below the boundary the
validator is deliberately blind; validation pressure inside references/ is
the signal content wants to be an artifact, never a reason to grow the
validator.

## Corpora — two-hop discovery, on-demand loading

Discovery is always: description → SKILL.md → **reference index** → file.
The SKILL.md body must carry an index table — every references/ file with a
one-line *read-when* trigger:

```markdown
## References
| File | Read when |
|---|---|
| HIERARCHY.md | resolving V28 hierarchy conflicts between HCC codes |
```

The index is the corpus's contract with context: stub loads at trigger time,
individual files load only when their read-when fires. Agent sessions
inherit discovery through performs/requires via the same two hops. Validator:
index complete (every file listed) and dangling-free (every row extant) —
the one intra-folder check, justified because the index IS the boundary.

## Templates and schemas

Passive contracts → references/, UPPERCASE (`REPORT-TEMPLATE.md`,
`OUTPUT.schema.json`), indexed with read-when rows. No templates/ or
schemas/ folders — "template vs schema vs example vs fixture" is an
undecidable sort. A schema a script enforces stays single-copy in
references/; the script addresses it by relative path. Anything a second
skill needs follows the extraction rule below.

## Procedures and workflows

One skill, one procedure; SKILL.md is the procedure's single authority.
Long procedures split by phase into indexed references/ files
(`PHASE-2-RECONCILE.md`) loaded when the phase runs. A workflow spanning
multiple skills is composition, not a document: an orchestrating command
(behind its confirm gate) or orchestrator agent whose requires edges declare
the participants. Banned: a WORKFLOW.md in one skill's references/
describing steps other artifacts perform — an authority claim the relation
graph cannot see.

## Extraction rule

Knowledge lives in references/ of the skill that uses it. When a second
consumer materializes, extract to a skill of its own (nominal production),
consumers declare requires. Same judgment as extracting a shared function.
The tell: the urge to validate a resource means it has become a contract,
and contracts are artifacts.

Resource-level convention (validator ignores it): UPPERCASE for contracts
the skill's text points at; lowercase for supporting matter.
