# Conversion / authoring checklist

Tick every line before the receipt is written. Bracketed gate labels name the checker
dimension that mechanizes the line; unlabeled lines are judgment (rubric R1–R5).

## Before writing

- [ ] Mode chosen: **new** (charter in hand) or **convert** (source resolved and readable: a skill dir, a command-species skill dir, or an `agents/<name>.md` file).
- [ ] Agent source: every `skills:` preload resolved to a real `skills/<name>/SKILL.md` (same plugin, or that plugin's checkout for `plugin:name`); none silently missing [F6].
- [ ] Command source: `$ARGUMENTS`, `context: fork`, `allowed-tools`, repo-state preconditions transposed or Dropped per conversion-rules §Source shapes [F2, F3].
- [ ] Destination path confirmed with the user in chat (this skill never assumes one).
- [ ] Convert: inventory written — headings (SKILL.md + every cited reference), scripts + their gates, handles/plugin mentions, numeric anchors, evals `t*`/`n*` cases.
- [ ] Convert: the source's own `evals/evals.json` opened — its `t*` prompts are the trigger vocabulary, its `n*` prompts the "Not for" list.

## Frontmatter

- [ ] `name`: specific, `<system>-<job>`, `[a-z0-9-]`, ≤ 64 [F1]
- [ ] `description`: job first → "Use when …" with ≥ 3 verbatim phrasings → "Not for: …"; ≤ 1024; no "only when/if" [F1, F4]
- [ ] No Claude-Code-only keys [F2]
- [ ] Command-only source (was `disable-model-invocation: true`): description says "Invoke with `/name`" and carries no auto-trigger phrasing

## Body — head

- [ ] Identity line (what this skill produces, to what standard)
- [ ] `## Contents` routing table when the body will exceed 300 lines [F7]
- [ ] `## Hard rules`: the source's NEVER/MUST NOT gates verbatim (≤ 3)
- [ ] `## Output contract` and failure branches verbatim

## Body — sections

- [ ] Every source `##`/`###` heading present in order, or under `## Dropped` [F6]
- [ ] Every cited reference inlined whole under its own heading [F3, F6]
- [ ] Every script transposed to a checklist with thresholds verbatim and an observable pass condition [F3]
- [ ] Every `[[handle]]` / plugin mention resolved to an inlined slice or a plain-prose fence [F3]
- [ ] Every tool verb mapped to a Figma action (tool map) — no "read the repo", "run", "dispatch" [F3]
- [ ] Every numeric anchor survives verbatim [F6]
- [ ] Good/bad pairs intact, bad side labeled

## Body — tail

- [ ] `## Examples` (worked examples from the source)
- [ ] `## Dropped`: one bullet per omission, `- <item> — <closed-set reason>` [F6]
- [ ] `## Provenance`: `source:` path @ version, `date:` [F5]; `hash:` (sha256 of the source tree, first 12), `inventory:` counts [F5 WARN]

## Gate

- [ ] `python3 scripts/figma_skill_check.py <out.md> --source <src>` exit 0 (F6 measured, never UNMEASURED on a conversion)
- [ ] Rubric R1–R5 scored with evidence; R1, R2 ≥ 3
- [ ] Generator ≠ critic: a fresh-context reviewer (design-system-checker bound to `references/rubric.md`, or doc-checker) scores the export — never the author alone
- [ ] In-Figma behavior check: 3 prompts (2 should-fire, 1 near-miss) run inside Figma with the skill loaded; recorded as fired/not + output vs assertions, or UNMEASURED with the reason
- [ ] Receipt written

## Regeneration trigger

- [ ] Source version or hash differs from `## Provenance` → re-run the whole loop; never patch the export by hand
