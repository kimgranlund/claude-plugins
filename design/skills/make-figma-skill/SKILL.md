---
name: make-figma-skill
description: >-
  Author, convert, check, or regenerate a single-file Figma custom skill — the one .md the
  Figma agent and Figma Make load. Use for "create a Figma skill from our X skill", "convert
  this skill / agent / command into a Figma custom skill", "export our Factory skills as
  Figma skills", "the Figma skill lost the contrast thresholds — regenerate it", "check this
  figma skill before I publish". Converts a skill, command, or agent without losing
  resolution: references and preloads inlined whole, scripts transposed, thresholds verbatim,
  checker gate. NOT a Figma Make guidelines/ folder (make-figma-make-kit); NOT the Plugin
  API (figma-plugin-facts); NOT a Claude Code skill (harness:make-skill).
disable-model-invocation: false
user-invocable: true
argument-hint: "[new charter | convert skill-dir-or-agent.md] [--check file.md]"
---

# make-figma-skill

Produces ONE markdown file that Figma's agent / Figma Make loads as a custom skill, to the
standard in `references/rubric.md`: every rule, threshold, and failure branch of the source
survives (a conversion) or of the charter is encoded (net-new), nothing points at a sidecar
the platform cannot open, and a checker run plus receipt prove it. Two platform facts
govern everything (ground truth + citations: `references/figma-spec.md`): **one file, no
`references/` `scripts/` `assets/`**; and **Figma validates nothing**, so
`scripts/figma_skill_check.py` is the gate of record.

**Resolution survives whole — length is not a cost.** Kim's ruling (2026-08-27): an export
is as long as it needs to be, and an export NEVER summarizes a source section — it carries
it or lists it under `## Dropped`. The substitute for progressive disclosure across files is
a `## Contents` routing table at the head of the one file.

## Procedure

1. **Resolve the mode and the destination.** `new <charter>` or `convert <source>` — a
   skill directory holding `SKILL.md` (procedural, knowledge, or command species), or one
   `agents/<name>.md` file; an installed plugin's cache path counts. The source's kind
   selects the extra transposition rows in `references/conversion-rules.md` §Source shapes
   (an agent's `skills:` preloads inline whole; a command's `$ARGUMENTS`, fork, and
   tree-state preconditions transpose or Drop). The destination
   path is the user's answer to a question asked in chat before anything is written — NEVER
   a default this skill picks. An unreadable source dir → report the path and stop.
2. **Inventory (convert) / frame (new).** Convert: list every `##`/`###` heading in the
   source body (SKILL.md, or the agent file plus each preloaded skill's SKILL.md) and in each
   `references/*.md` it cites, every bundled script with the
   gates its docstring names, every `[[handle]]`/`plugin:skill` mention, every numeric
   anchor, and the source `evals/evals.json` `t*`/`n*` prompts. New: the charter's rules,
   thresholds, output shape, and the phrasings the user would type. This list is the
   coverage manifest F6 enforces.
3. **Write the frontmatter.** `name`: specific, `<system>-<job>` (`nonoun-button-rules`),
   `[a-z0-9-]`, ≤ 64. `description` ≤ 1024: job first → "Use when …" carrying ≥ 3 verbatim
   `t*` phrasings → "Not for: …" naming the `n*` families (one clause per owner, not per
   case). Active voice; "only when/if"
   is excluded (Figma reads it as "don't use unless"). A command-only source (was
   `disable-model-invocation: true`) says "Invoke with `/name`" and carries no auto-trigger
   phrasing. Every Claude-Code-only key is stripped.
4. **Transpose the body, head-first, in source order** — the full table is
   `references/conversion-rules.md` (read it before a conversion): cited references inline
   whole under their own headings, in first-citation order, path citations inside them
   rewritten to `## <heading>` pointers; scripts become `## <check> (transposed from
   scripts/x)` numbered checklists with thresholds verbatim and an observable pass
   condition; handles
   become an inlined slice or a plain-prose fence; `Read`/`Grep`/`Bash`/`Agent`/
   `AskUserQuestion` verbs become canvas or chat actions per the tool map. Head =
   identity line, `## Contents`, `## Hard rules` (≤ 3, verbatim), `## Output contract`;
   tail = `## Examples`, `## Dropped`, `## Provenance`.
5. **Reconcile.** Everything not carried lands under `## Dropped` as one bullet per item,
   `- <heading> — <reason>`, the reason drawn from the closed set canonical in
   `references/conversion-rules.md` (the checker's F6 rejects any other). `## Provenance`
   carries `source:` path @ version (or `charter:`), `date:`, `hash:` (from
   `figma_skill_check.py --hash <source-dir>`), `inventory:` counts — field shapes in the
   same reference.
6. **Gate, score, receipt.** Run the checker (below); fix the *file*, not the check; re-run.
   Score R1–R5 against `references/rubric.md` with cited evidence. Run the in-Figma
   behavior check where a Figma seat is reachable (3 prompts: 2 should-fire, 1 near-miss),
   else record UNMEASURED with the reason. Write the receipt (rubric's template) next to the
   export or into the source's ledger.

If the user only wants a file checked (`--check <file.md>`) → skip to step 6.

## Validation loop (finalize only when it clears)

draft → `python3 scripts/figma_skill_check.py <out.md> --source <skill-dir>` (omit
`--source` for net-new; F6 then reports UNMEASURED — legal for new, a defect for a
conversion) → fix → re-run → self-score → receipt. Gates: F1 frontmatter · F2 no
Claude-only keys · F3 no sidecar references · F4 active trigger · F5 provenance · F6
resolution (every source heading carried or Dropped, every numeric anchor verbatim) · F7
routing table when > 300 lines · F8 trigger vocabulary (WARN). `selftest` proves the checks
fire. **Generator ≠ critic:** a shipping export gets a fresh-context reviewer
(design-system-checker bound to `references/rubric.md`, or docs' doc-checker); the
author's own score is evidence for the reviewer, not the verdict.

## Output contract

```
figma-skill: <name>  ·  mode: new | convert <source @ version>
file: <destination path>  (<n> lines, <n> headings)
checker: F1 ✓ F2 ✓ F3 ✓ F4 ✓ F5 ✓ F6 ✓|UNMEASURED F7 ✓ F8 ✓|WARN(<ids>)   exit <0|1>
judgment: R1 <n> R2 <n> R3 <n> R4 <n> R5 <n>  — one evidence line each
dropped: <n> (<reasons>)
in-figma check: fired <2/2>, near-miss held <1/1>, assertions <n/n> | UNMEASURED: <reason>
next: <regenerate when source hash ≠ provenance hash | publish to team | fix list>
```

## Failure branches

- Source dir has no `SKILL.md`, a cited reference file is missing, or an agent's `skills:`
  preload resolves to no skill directory → name the path; stop before writing — a
  conversion from a partial source is a silent resolution loss.
- F6 fails on a heading the export genuinely should not carry → it goes to `## Dropped`
  with a closed-set reason, as an entry — not a deletion from the manifest, not a summary.
- A script's check is not performable on the canvas (byte diff, HTTP) → `## Dropped` as
  `not performable in Figma; run <script> on the export instead`; the rest of the script's
  gates still transpose.
- Source `hash:` differs from the export's `## Provenance` → regenerate the whole file;
  NEVER hand-patch an export.
- No Figma seat reachable for the behavior check → `UNMEASURED` in the receipt, with the
  reason, and no claim of a run.

Done when the destination file exists, the checker exits 0 with F6 measured (conversions),
R1 and R2 ≥ 3 with evidence, and the receipt is written with honest UNMEASURED entries.

## References & composition

| Path / peer | Use when |
|---|---|
| `references/figma-spec.md` | Platform ground truth — single-file rule, frontmatter, slash-name, soft-trigger warning, the in-Figma runtime; cited to source |
| `references/conversion-rules.md` | The transposition table, tool map, three passes, head-first skeleton — read before any conversion |
| `references/checklist.md` | The tick-list a run walks; every line names the gate that mechanizes it |
| `references/rubric.md` | F1–F8 + R1–R5, the receipt template, done/not-done |
| `scripts/figma_skill_check.py` | The mechanical gates; `selftest` fixture-locks them |
| [[make-figma-make-kit]] | A Make `guidelines/` FOLDER for a design system — a different Figma surface |
| [[figma-plugin-facts]] | The Plugin API when a transposed check needs variable/style facts |
| harness `make-skill` / `skill-writing-rules` | Authoring a Claude Code skill — the source side of a conversion |

## Example

```
Bad  (counter-example — do not imitate; pointer survives, content lost):
  ## Gates
  Run scripts/make_guidelines_check.py; see references/gates.md for definitions.

Good (content inlined, check transposed, threshold verbatim):
  ## Gates (transposed from scripts/make_guidelines_check.py)
  1. Every fill/on token pair reads ≥ 4.5:1 in BOTH light and dark — open each pair's
     variable values in the Variables panel and compute the ratio.
  2. Every component section names `hover` with a literal value or a `-hover` token …
```
