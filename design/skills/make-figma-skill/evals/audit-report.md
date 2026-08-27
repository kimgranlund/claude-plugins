# Audit report — design:make-figma-skill (FLOOR depth)

Skill: `/Users/kimba/Projects/nonoun/plugins/design/skills/make-figma-skill/SKILL.md`
Standards: harness `skill-writing-rules` (+ `check-skill` procedure, `checking-rules`)
Lint: `python3 harness/scripts/skill_lint.py design/skills/make-figma-skill/SKILL.md` → **clean** (`skill-postwrite-invocation-lint`)
Bundled checker (`scripts/figma_skill_check.py selftest`): **14/14 PASS** — good fixture, bad fixture (F1/F2/F3/F4 WARN), resolution-miss pair (F6 heading + anchor bite), reverse control (F6/F5 pass), F8 vocab WARN, F7 TOC gate. Not laundered by eye — run for real.
`eval_check.py design/skills/make-figma-skill/evals/evals.json` → **clean** (22 cases: 12 `t*` / 10 `n*`, matches `intent.md`'s claimed count).

## Verdict: GO

No blocking findings. The skill is well-factored (dial-explicit, output contract + failure
branches + stopping predicate in the head, ≤3 hard gates, references one level deep, no
hardcoded paths, house convention for its own bundled script path followed). Two MAJOR /
MINOR gaps below concern the gap between what the skill's prose *claims* the mechanical
gate proves and what the gate *actually* checks — worth a same-tier fix, not a re-ship
blocker.

## Findings

| # | Severity | ID | Evidence (file:line) | Finding | Fix |
|---|---|---|---|---|---|
| 1 | **MAJOR** | R4/R7 (contract honesty) | `SKILL.md:19-22` claims "a checker run plus receipt prove it" for "every rule, threshold, and failure branch… survives… or is Dropped [with a reason]"; the closed Dropped-reason set is stated at `SKILL.md:58-60`, `references/conversion-rules.md:49-52`, `references/checklist.md:40`; but `scripts/figma_skill_check.py:216-234` (the F6 check) never validates that a Dropped entry's stated reason is one of the 5 closed-set strings — it only checks whether the omitted heading's normalized text appears *anywhere* in the `## Dropped` section's text (`dropped = norm_heading(dropped_section(body))`, then `h not in dropped`). A `## Dropped` bullet with zero reason, or a made-up reason, still passes F6 as long as the heading name string is present. | Either (a) extend F6 to require, per Dropped bullet, a trailing `— <one of the 5 closed-set tokens>` matched by regex (cheap, mirrors the existing `NUMERIC_ANCHOR_RE`/`ACTIVE_TRIGGER_RE` pattern style already in the file), or (b) soften the claim at `SKILL.md:22` to "a checker run proves nothing is silently dropped; the receipt's R1 judgment score is what proves the *reason* is honest" — don't leave the stronger claim standing over a check that doesn't back it. |
| 2 | MINOR | R5/R7 (contract honesty) | `references/checklist.md:41` tags the full Provenance line — `source:`, `date:`, `hash:` (sha256×12), `inventory:` counts — with `[F5]`, and that file's own header (`checklist.md:3`) says "Bracketed gate labels name the checker dimension that mechanizes the line." But `figma_skill_check.py:196-197` (`has_prov = bool(prov and re.search(r"\bsource:", …) and re.search(r"\bdate:", …))`) only requires `source:` and `date:` — `hash:` and `inventory:` are never checked. An export can pass F5 with no hash or inventory counts, contradicting the checklist's own labeling promise. Lower severity than #1 because this only weakens R5 (Regenerability judgment), not the resolution-loss invariant (headings/anchors, which F6 does enforce independent of Provenance). | Either extend F5's regex to also require `\bhash:` and `\binventory:` when `--source` is given (matches the checklist's claim), or retag `checklist.md:41` as `[F5: source/date only — hash/inventory scored under R5]` so the bracket promise matches the code. |
| 3 | MINOR | R5 (no restatement) | `SKILL.md:58-60` fully re-enumerates the 5-item closed Dropped-reason set that is already the canonical list at `references/conversion-rules.md:49-52` (the Reconcile pass). `references/checklist.md:40` does this correctly — it references "the closed set" without repeating it. The two full copies (SKILL.md + conversion-rules.md) currently agree, but nothing cross-checks them; an edit to one during a future revision drifts silently. | Replace `SKILL.md:58-60`'s inline list with a pointer: "a reason from the closed set (`references/conversion-rules.md`'s Reconcile pass)" — one line, references the canonical copy instead of restating it. |
| 4 | NIT | R2 (trigger fidelity, reciprocal fence) | `SKILL.md:9-11` fences OUT `make-figma-make-kit` and `figma-plugin-facts` by name, but neither sibling fences back: `make-figma-make-kit/SKILL.md:3-11` and `figma-plugin-facts/SKILL.md:3-11` (both pre-existing files, not edited by this change) carry no NOT-for clause naming `make-figma-skill`. Checked collision risk directly against `evals/evals.json`'s own `t*`/`n*` set: no shared content word between make-figma-skill's `t*` prompts (e.g. "export our Factory skills as Figma skills", "convert this skill into a Figma custom skill") and make-figma-make-kit's own trigger vocabulary ("Guidelines.md", "guidelines folder") — low practical risk, so this is a NIT not a MINOR. | When either sibling's description is next touched, add one clause each: make-figma-make-kit → "; NOT a single-file Figma custom skill (make-figma-skill)"; figma-plugin-facts → "; NOT authoring a Figma custom-skill .md (make-figma-skill)". Per this workspace's `plugin-authoring.md`, don't force an edit to those two files just to close this loop today — no blocking risk found. |

## What was checked and cleared (no finding)

- **F6 core invariant** (the audit's own probe question): the mechanical gate DOES prove the
  primary claim — every source heading and every numeric anchor (source SKILL.md + every
  cited `references/*.md`) must appear in the output or literally inside `## Dropped`, or F6
  FAILs. Confirmed via `figma_skill_check.py selftest`'s dedicated resolution-miss fixture
  (bites on both a dropped heading and a dropped numeric anchor) and its reverse control
  (passes once both are carried) — this is a real, provable gate, not merely described. Only
  the *reason-string* half of the claim (finding #1) is unmechanized.
  - `Dropped` reason set: identical closed 5-item list in `SKILL.md:58-60` and
  `conversion-rules.md:49-52` (restatement flagged as #3, but currently consistent).
  - `Provenance` fields: `SKILL.md:61-62`, `checklist.md:41`, and `rubric.md:34-41`'s receipt
  template all name `source:`/`date:`/`hash:`/`inventory:` — consistent in *prose*, only the
  checker's coverage of `hash:`/`inventory:` diverges (finding #2).
- Body 137 lines (well under 500); references one level deep, 4 files, none >100 lines
  (no TOC-in-reference required); no hardcoded machine paths anywhere in SKILL.md,
  references, or the checker script (`grep` swept for `/Users/`, `/home/`); own bundled
  script referenced as relative `scripts/figma_skill_check.py`, matching house convention
  used by 5+ sibling skills in this plugin (`make-dscard-kit`, `make-figma-make-kit`,
  `make-palette`, `make-stitch-kit`, `artifact-styling-rules`).
  - Both invocation dials declared explicitly (`disable-model-invocation: false`,
  `user-invocable: true`, `SKILL.md:12-13`) — matches procedural species.
  - ≤3 hard gates: exactly 3 `NEVER` instances (`SKILL.md:28,36,105`), no `MUST NOT`; none
  spent loosely.
  - Output contract (`SKILL.md:83-93`), named failure branches (`SKILL.md:95-107`), and a
  checkable stopping predicate ("Done when…", `SKILL.md:109-110`) all present and in the
  first ~2,300 words (well inside the 5,000-token compaction-survival window).
  - `## References & composition` table names `design-system-checker` and `doc-checker`
  (`SKILL.md:79-81`) as the fresh-context reviewers for the "generator ≠ critic" step —
  both confirmed to exist (`design/agents/design-system-checker.md`,
  `docs/agents/doc-checker.md`); not a dangling pointer.
  - Delegation-mechanics gate: N/A. Frontmatter carries no `context: fork` / `agent:` /
  `model:`; the "dispatch a fresh-context reviewer" language at `SKILL.md:79-81` is a
  procedural handoff to a *separate* skill invocation, not a subagent fork this skill
  configures — DM-R4/R5/R6 do not apply.

## Top 3

1. **(MAJOR)** F6 never validates that a `## Dropped` entry's stated reason is drawn from
   the closed 5-item set — only that the omitted heading's text appears somewhere in the
   `## Dropped` section (`figma_skill_check.py:216-234`). Extend the regex check or soften
   the "checker run… prove it" claim at `SKILL.md:19-22`.
2. **(MINOR)** `checklist.md:41` tags `hash:`/`inventory:` `[F5]`, but F5's code
   (`figma_skill_check.py:196-197`) only checks `source:`/`date:`. Extend F5 or retag the
   checklist line.
3. **(MINOR)** `SKILL.md:58-60` restates the closed Dropped-reason set already canonical at
   `conversion-rules.md:49-52` — a drift pair with no cross-check; point instead of repeat.
