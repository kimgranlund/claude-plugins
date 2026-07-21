# Species skeletons

Fill the matching skeleton; keep its ordering — the head survives compaction, the tail doesn't. Bad-side lines are labeled and are counter-examples: do not imitate them.

## Procedural

```markdown
---
name: <domain>-<verb>
description: >-
  <What it produces>. Use when the user asks to <verbatim phrasing>, <phrasing>,
  or <phrasing>. NOT for <adjacent thing> (<owner>).
disable-model-invocation: false
user-invocable: true
---

# <domain>-<verb>

<One identity line: what this procedure produces and to what standard.>

## Procedure
1. <Step, spec-present tense.> <Done-condition if non-obvious.>
2. ...
If <precondition absent> → skip to step <n>.

## Output contract
<The schema of what comes back — slots, not prose. Verdict/summary first.>

## Failure branches
- If <state> → <named action>; do not <improvised default>.
- If <state> → report the blocker; do not mark complete.

Done when <checkable world-state>.

## Example
<One good/bad pair, bad side labeled "counter-example — do not imitate".>
```

Line-level contrast:

```
Bad  (one-time step; dies after turn one):   First, read the failing test.
Good (standing instruction):                 Every fix starts from the failing test's output, quoted in the report.
```

## Knowledge

```markdown
---
name: <domain>-<knowledge-noun>        # -patterns, -conventions, -standards, -context
description: >-
  <What it covers>. Use when the user asks about <topic phrasings>, when writing
  <artifact>, or when <situation>. NOT for <adjacent> (<owner>).
disable-model-invocation: false
user-invocable: false
---

# <domain>-<knowledge-noun>

<One thesis line stating the catalog's claim as fact.>

## <Pattern group>
| Pattern | Rule (declarative) | Contrast |
|---|---|---|
| <handle> | <the rule as world-state> | Bad: `<labeled>` → Good: `<form>` |

<Examples marked normative or illustrative — unlabeled examples are read as contracts.>
```

Line-level contrast:

```
Bad  (imperative to nobody):   Always use design tokens for colors.
Good (declarative catalog):    Colors come from var(--token); raw hex does not appear in src/ui/**.
```

## Orchestrator

A command-species subtype: thin routing over modules and agents, `disable-model-invocation: true` always. Cross-domain orchestrators take workflow names and forfeit the domain prefix (`/design-to-code`, `/check-everything`); single-domain ones keep it.

```markdown
---
name: <workflow-name>            # or <domain>-<verb-phrase>
description: >-
  <Menu documentation: the pipeline it runs, what it dispatches, what lands where.
  Zero trigger keywords; this text never reaches the model.>
disable-model-invocation: true
user-invocable: true
argument-hint: "[<expected args>]"
---

# /<name>

<One identity line: what pipeline this runs and what it produces.> Seed: `$ARGUMENTS`

## Phase 1 — <inventory / frame>
<Build the manifest of what this run covers; everything below covers exactly it.>

## Phase 2..n — <the pipeline>
- Modules are referenced by canonical name, never copied inline — a stale internal copy is the
  highest-impact drift failure in orchestrator systems.
- Every dispatch declares its return contract (schema, severity taxonomy, file destination);
  workers return by file + verdict-first summary; reports are validated at the boundary before
  aggregation.
- Failure branches per dispatch: off-contract return → one re-dispatch with the contract quoted,
  then UNMEASURED with reason; never aggregate improvised prose.

## Close
<Head-first summary; the uncovered-rows check against Phase 1's manifest.>

Done when <checkable world-state over the manifest and the output files>.
```

Line-level contrast:

```
Bad  (internal copy):   ## The review criteria    (30 lines pasted from the module skill)
Good (canonical ref):   Workers preload `x-review`; its report contract governs every return.
```

## Command

```markdown
---
name: <domain>-<imperative-verb>[-<object>]
description: >-
  <Menu documentation for a human — what it does, what it touches, what it asks
  before doing. Zero trigger keywords; this text never reaches the model.>
disable-model-invocation: true
user-invocable: true
argument-hint: "[<expected args>]"
allowed-tools: <exactly the verbs the workflow needs, e.g. Bash(git add *) Bash(git commit *)>
---

# /<name>

<One identity line. The human chose the timing — proceed; do not re-ask why.>

## Preconditions
- <Validate $ARGUMENTS / tree state / credentials.> If <check fails> → <named action>; stop.

## Workflow
1. ...
2. <Side-effect confirmation point: show the diff / plan; proceed only on approval.>

## Report
<The format returned on completion — status, artifacts, what was NOT done.>

Done when <checkable world-state>.
```

Line-level contrast:

```
Bad  (grants nothing it means to):  allowed-tools: Read     # "restricted to Read" — it isn't; allowed-tools only pre-approves
Good (scoped grant):                allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
```
