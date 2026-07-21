---
name: entry-file-rules
description: >-
  Standards for CLAUDE.md and .claude/rules/ — the harness's most expensive real estate. Use when
  the user asks what belongs in CLAUDE.md, how to write, trim, restructure, or optimize it, why
  Claude ignores an instruction that's "right there in CLAUDE.md", how big CLAUDE.md itself
  should be, when to use path-scoped rules, or how entry-file content routes to hooks and skills.
  The
  judgment criteria /check-entry-file applies. NOT for running that audit (the /check-entry-file
  command executes it; this skill only carries the standard it audits against).
disable-model-invocation: false
user-invocable: false
---

# Entry-File Standards

CLAUDE.md is reloaded into working memory every turn: every line is paid for constantly, for the whole session, whether or not this turn needs it. It is also *advisory* — the model can drift from all of it — and its force decays with distance from the action (position zero does not bind at turn forty). Those two facts decide everything: the entry file holds only what primacy serves and per-turn payment justifies; everything else routes down-stack. This is the standard `/check-entry-file` classifies against and `/check-everything` scores against; `skill_lint.py` (rules C1–C2) flags the mechanical smells.

## What earns residency

Short, always-true, identity-grade facts in declarative register: what the codebase is, directory topology, the invariant conventions, the build/test/lint commands, and **one-line pointers** to deeper homes ("component conventions: the `component-patterns` skill; load-bearing decisions: `docs/adr/` digest"). The residency test, per line: *is this true on every turn, and does the model need it before any task content frames it?* Two nos → it lives elsewhere.

## The routing table — where evicted content goes

| Content class | Signal | Destination |
|---|---|---|
| Mechanically checkable rule | You can write the pass/fail function ("no raw hex in `src/ui/**`") | **Hook** (`/make-hook`); prose deleted, pointer optional |
| Task procedure | Steps, workflows, "when doing X, first…" | **Skill** (`/make-skill`); loads only when used |
| Occasional reference | Correct but needed in a minority of turns | **Skill** (model-only knowledge) |
| Subtree-local knowledge | True inside `src/api/**`, noise outside | **`.claude/rules/`** path-scoped rule |
| Action-critical constraint | Must bind a specific action forty turns later | **Hook output or invoked skill** — the surfaces that fire near the action |
| Restated model knowledge | Deletion test fails: output identical without it | **Cut** |
| Stale fact | Refers to retired code, tools, decisions | **Cut** (false presupposition: the model absorbs it as ground truth) |

The last row is the deadliest: a stale entry-file line is not ignored, it is *believed* — read as world-state, built around, producing fluent wrongness that passes review.

## The physics

- **~150–200 instructions** is the adherence ceiling measured for frontier models; past it, following decays and every added imperative dilutes the ones before it. `skill_lint` C1 warns at 200 lines as the proxy.
- **Salience is a budget.** A wall of bolded MUSTs normalizes to noise; three plain sentences in a dedicated block outlast thirty scattered warnings. Structured emphasis over typographic shouting (`prompt-wording-rules` §8).
- **Declarative register.** "Every table has an RLS policy" shapes identity; "always remember to add RLS policies" competes with every other imperative for attention and loses on schedule.
- **Hierarchy [drift-prone]:** enterprise > personal > project on collisions; nested and `--add-dir` discovery has exceptions — verify against current docs when it matters.

## The growing dotfile — the one anti-pattern that is the whole game

Every incident adds a paragraph; nothing is ever removed; within months the file is a token tax the model skims. The entry file is a hot code path: additions need justification against the residency test, and the audit runs on a cadence, not after the rot is felt. One incident-driven line is a patch; the third repetition of the same correction is a skill or hook that should already exist (the three-strikes rule).

```
Bad  (procedure squatting per-turn):  ## Deploying
                                      1. run tests  2. build  3. push to staging  4. verify…
Good (residency + pointer):           Deploys are human-timed: /deploy (never run it unprompted).
```

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Growing dotfile | Monotonic additions, no eviction | `/check-entry-file` on a cadence; residency test per line |
| Checks in prose | ~70–90% compliance vs a hook's ~100% | Route to hooks; delete the prose |
| Procedures in the entry file | Paid every turn, needed rarely | Skills; loads on demand |
| Constraint dumping at position zero | Decays by the time the action arrives | Hooks / invoked skills near the action |
| Global noise for local truth | Subtree knowledge taxes every other subtree | Path-scoped rules |
| Stale lines | Absorbed as presupposed world-state | Audit for staleness first — it outranks length |
| Imperative walls | Salience inflation; adherence decay past ~150–200 | Declarative register; ≤ 3 hard gates; cut the rest |

## Shipped seed — the worked example

`assets/engineering-operating-contract.md` is a ready-to-install global `~/.claude/CLAUDE.md` that passes this standard (~20 lines: loop identity, four standing convictions in declarative register, a pointer block to the estate's doctrine skills). For a new setup, copy it in and adapt. The asset is the canonical seed — installed copies refresh *from* it, never the reverse (distilled 2026-07-12 from the standard's first full audit of a live 49-line contract). Its pointer block presupposes the harness/docs/teamwork plugins; trim any pointer whose owner isn't installed.

## Provenance

Adherence ceiling and compliance figures are ecosystem measurements (HumanLayer et al., 2025–26); hierarchy and loading mechanics verified against code.claude.com/docs 2026-07, [drift-prone]. Position/salience mechanisms: `prompt-wording-rules` (§8, §9). The routing destinations' own standards: `hook-writing-rules`, `skill-writing-rules`.
