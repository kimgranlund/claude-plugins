---
name: skill-writing-rules
description: >-
  Standards for writing Claude Code skills that change behavior instead of documenting it. Use
  when the user asks how to write, structure, review, or fix a SKILL.md; choosing invocation
  flags (disable-model-invocation, user-invocable) or skill species (procedural, knowledge,
  command); why a skill never triggers, misfires, or stops influencing behavior; body length; or
  what belongs in description vs body vs references/.
disable-model-invocation: false
user-invocable: false
---

# Skill Authoring Standards

A skill is a behavior delta, not documentation. Every line either changes what Claude does or spends context teaching Claude what it already knows. The **description is the API** — the only text that controls triggering; the **body is the payload** — standing instructions that persist for the session; the **numbers are the physics** — budgets that decide what survives. This document is the standard `/make-skill` authors against, `check-skill` audits against, and `skill-postwrite-invocation-lint` enforces the checkable slice of.

Scope: skill-specific standards only. Language techniques → the `prompt-wording-rules` skill (this plugin). Naming grammar → `naming-rules` (this plugin) for existing names, carrying an in-place supersession note as of ADR-0011 (2026-08-14) pointing at `.claude/docs/spec/spec-naming-convention.md` for new mints — the checkable slice moved from `skill_lint.py`'s retired W4/W5 to authorkit's naming-audit validator (`--scope grammar`), wired into this repo's ship gate and PostToolUse hook; `skill_lint`'s own F9/A6 symmetry checks (frontmatter `name:` == directory/file stem) are unaffected and still enforce here. Document contracts and primitive routing → the Agentic Harness corpus (Vols 3 and 1 §16 — external project knowledge, when present). Reference those; this file restates none of them.

## The physics — verified 2026-07, Claude Code 2.1.20x [drift-prone]

| Quantity | Value | Consequence |
|---|---|---|
| Description listing budget | 1% of context window, shared by all descriptions; least-invoked dropped first | Every model-invocable description is a claim on a shared budget; `/doctor` shows the damage; `skillListingBudgetFraction` raises it |
| Per-entry listing cap | 1,536 chars, `description` + `when_to_use` combined | Key use case in the first sentence — the tail truncates first |
| Open-standard caps | `name` ≤ 64 chars · `description` ≤ 1,024 chars | Exceeding 1,024 costs portability across the 30+ tools on the Agent Skills standard |
| Body size | ≤ 500 lines (~5,000 tokens) | Over the line → split to `references/`, one level deep, TOC if a reference exceeds 100 lines |
| Compaction survival | First 5,000 tokens per skill; 25,000 combined, most-recent-first | Contracts and constraints in the head; examples in the tail; older skills drop entirely |
| Body lifecycle | Enters context once on invoke; never re-read; identical re-invoke adds a note, not a copy | Standing instructions ("the review cites file:line"), never one-time steps ("first, read the file") |
| Stacking | `/a /b args` expands up to 6 skills, args to each | Pure sequencing is free; wrapper orchestrators are for composition with logic |
| Live bug | Budget computed against ~200K even on 1M-context models (#57168) | Extended-context users still see truncation; tighten descriptions regardless |

## The species

Content species, invocation dials, and name grammar are one decision made three ways — they must tell the same story:

| Species | Content | `disable-model-invocation` | `user-invocable` | Description's job | Name head | Preloadable into agents |
|---|---|---|---|---|---|---|
| **Procedural** | Workflow with a contract: review, audit, migrate | `false` | `true` | Trigger contract for auto-discovery | Zero-derivation verb (`x-review`) | Yes |
| **Knowledge** | Patterns, conventions, domain context | `false` | `false` | Trigger contract — the model is the only router | Knowledge noun (`x-patterns`, `x-standards`) | Yes |
| **Command** | Side effects, phase entries, human-timed workflows | `true` | `true` | Slash-menu documentation — it never enters model context | Imperative verb (`/x-deploy`, `/x-create`) | **No** |

Corrected rule, verified against live docs 2026-07: **`disable-model-invocation: true` blocks subagent preloading** (and scheduled-task firing, v2.1.196+). The preloadable module state is therefore **knowledge (model-only)**, not the both-flags state. Both flags set = invisible to the menu, to auto-discovery, *and* to `skills:` preloads — a skill nothing can reach except a raw file read. Treat it as a misconfiguration unless a future release documents a role for it. (This falsifies the earlier "library-only preload" claim; corpus Vol 1 §6.6 should be amended.)

Declare both dials on every skill, explicitly, including at their defaults. An omitted field couples the skill's behavior to whatever the current version defaults to; an explicit field pins what was meant. The lint fails omission.

Name-grammar exception (amended 2026-07-15; type specimen: raphaelsalaja/skill@dc9eef22f): when a knowledge catalog's subject IS a term of art users type verbatim (`12-principles-of-animation`, not `animation-principles`), the term outranks the noun-head grammar — the name is itself a trigger surface, and normalizing it destroys the exact-phrase match. The checkable slice (reserved words F8, length caps) still applies unconditionally. (The canonical naming grammar lives in corpus Vol 2, which should be amended with this exception — the same flag discipline as the §6.6 correction above.)

Two design axes cut across species (both primary-sourced from Anthropic):
- **Capability uplift** (Claude can't do it, or not consistently) vs **encoded preference** (Claude can do each piece; the skill sequences them your way). Uplift skills earn detail; preference skills earn brevity — state the sequence and stop.
- **Degrees of freedom**: many valid approaches → prose intent (high); one preferred pattern → pseudocode or a parameterized script (medium); fragile, consistency-critical operation → an exact script, no parameters (low). "Solve, don't punt": a bundled script beats instructions to improvise one, and it removes a hallucination surface.

## Frontmatter discipline

Runtime fields (Claude Code): `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`. Portable core (Agent Skills standard, runs everywhere): `name`, `description`, body, `scripts/` `references/` `assets/`. Everything else couples the skill to Claude Code by exactly that much — author the portable core first, add coupling deliberately. Those three dirs plus the house `evals/` are the ONLY sanctioned skill subfolders (ruled 2026-07-15; `release_gate` G2 warns on any other): topical data lives under `assets/<topic>/`, worked examples and consulted corpora under `references/` — never as ad-hoc top-level dirs, and never a `resources/` twin of `references/`.

- **`allowed-tools` grants; it does not restrict.** Listed tools skip the permission prompt while the skill is active; every other tool remains callable under normal permissions. To remove tools, use `disallowed-tools` (clears on the next user message). A skill claiming "restricted to Read" via `allowed-tools` has restricted nothing.
- **`paths`** scopes auto-activation to matching files — the path-scoped-rules mechanism applied to skills. Use it for monorepo package skills instead of description caveats.
- **`context: fork`**: the body *becomes the subagent's entire prompt* — no conversation history, no invoked skills. A guidelines-only body forked returns nothing useful; forked bodies carry explicit, self-sufficient task instructions. `agent: Explore` / `Plan` also skip CLAUDE.md.
- **Malformed YAML fails soft**: the body loads with empty metadata — `/name` still works, auto-discovery silently never does. A skill that "stopped triggering after an edit" has a parse error until proven otherwise (`claude --debug`).
- Bundled scripts are referenced via `${CLAUDE_SKILL_DIR}/scripts/...` (or `${CLAUDE_PLUGIN_ROOT}` inside a plugin) — a hardcoded path is a skill that works on one machine.

### Description engineering

The description is matched against *the user's words*, not the skill's content. Third person; [what it does] + [when to use it]; the verbatim phrasings a user actually types, front-loaded; slightly pushy — the documented bias is under-triggering, not over-triggering. Fence what it is NOT for using the parseable form `NOT for <thing> (<owner>)` — a repellent the router and measurement tooling can both key on. Three trigger vocabularies, mined in that order: **feature nouns** (what the user names), **symptom phrases** ("feels sluggish", "looks off", "why did the wrong one fire"), and **lifecycle moments** ("before committing…", "finishing a feature…", "ready to merge") — the third routes by WHEN the user is rather than what they can name, and fits verify/review skills whose users don't know the defect vocabulary yet (amended 2026-07-15; type specimen: millionco/react-doctor@5915a5823).

```
Bad  (label — never fires):
  description: Database migration helper

Good (trigger contract):
  description: >-
    Generates and applies schema migrations. Use when the user asks to add or
    change a column, create or alter a table, write a migration, or fix a failed
    migration. NOT for data backfills (backfill-runner).
```

For command skills the description never reaches the model — write it as documentation for the human scanning the `/` menu, and spend zero trigger keywords on it.

## Body style — universal

1. **Standing instructions, spec-present tense.** The body persists un-re-read for the whole session; "the report cites file:line for every finding" keeps binding at turn thirty in a way "first, cite your sources" does not.
2. **Contracts first, examples last.** Compaction keeps the head. The output contract, the hard gates, and the failure branches live in the first 5,000 tokens; worked examples fill the tail.
3. **The deletion test** — the calibration instrument for every line: *delete it; would Claude's output change?* No → the line restates model knowledge; cut it. Measured across public skills, >60% of body content fails this test. One scoring exception (amended 2026-07-15): a **coverage-forcing enumeration** — a checklist whose every line is individually model knowledge but whose value is forcing complete, priority-ordered coverage instead of open recall (type specimen: the 9-category a11y sweep in ibelick/ui-skills@ce91b8595) — is scored on the enumeration, not per line: it survives iff deleting the LIST would change which categories get checked or in what order.
4. One contrastive good/bad pair binds a quality bar better than a paragraph of criteria. Label the bad side — unlabeled counterexamples get imitated.
5. Numeric anchors on load-bearing dimensions ("3 sentences", "under 40 lines"); vague quantifiers ("briefly", "a few") inherit the model's prior, which is verbose.
6. ≤ 3 hard gates (`NEVER` / `MUST NOT`) per body, spent only on catastrophic invariants — a body with thirty has none. **Parameter locks are a different instrument, and uncapped** (amended 2026-07-15 — the external-skill review hit this misfire three times independently): a lock pins one aesthetic or config knob to a sanctioned value AND names its forbidden neighbors ("scale to `0.96`, never `0.95` or below" — the type specimen is jakubkrehel/make-interfaces-feel-better@366f0f86e). Locks are written lowercase (always/never + backticked values), keeping the uppercase salience budget — and lint W7's case-sensitive count — reserved for the catastrophic tier; a "lock" that names no forbidden neighbor is a preference, and earns no never at all.
7. **Escape hatch**: procedures state when to skip ("if no migration exists yet, skip to step 4") so the model doesn't march through irrelevant steps.
8. Reference, never restate: point at the canonical skill or doc. A restated convention is a drift pair with a countdown.

## Body style — per species

**Procedural.** Skeleton: one identity line (what this procedure produces) → numbered steps, each with its own done-condition where non-obvious → output contract (the schema of what comes back) → named failure branches ("if tests cannot run → report the blocker; do not mark complete") → stopping predicate ("done when <checkable world-state>", never "until done") → escape hatch. The most common defect: a beautiful procedure with no output contract — downstream consumers then parse improvised prose.

**Knowledge.** A pattern catalog in declarative register: each entry = the rule stated as fact + one contrastive pair; tables over prose lists; recurring bars bound to named handles, defined once. Zero imperatives — there is no actor mid-catalog to command. Mark every example **normative** or **illustrative**: the model treats unlabeled examples as contracts.

**Knowledge pack (the corpus sub-species — a cited retrieval corpus, not a plain catalog).** A knowledge pack is a corpus behind a boundary: `references/` organized by question type (axis decomposition, INDEX, load discipline, grounding markers, and research waves are `pack-writing-rules`' rules, not restated here — that standard explicitly excludes the SKILL.md surface itself, which is this entry's job). Five things belong on the entry surface that a plain knowledge catalog doesn't need:

- **The answers-only boundary, stated first.** The SKILL.md names, for every kind of "make/add/fix this" ask the pack could receive, which builder peer receives it — the pack itself never generates. An ask with no named peer is a phantom boundary; where no builder exists yet, say so explicitly ("not installed — derive inline"), never leave a silent gap.
- **The Grep-first consult discipline.** The body states, in the consult procedure itself, that the corpus is entered by search — Grep the matching file for the term first, then Read the section — never "read this whole folder." A pack whose entry surface doesn't say this gets read start-to-finish the first time it's loaded, defeating the boundary the axis decomposition exists to draw.
- **The deviation doctrine.** Every default the pack states carries its own rationale, so a consumer can tell a legal deviation from a violation — "we use X because Y" reads differently from a bare "use X," and only the first licenses "unless Y doesn't hold here, then don't."
- **The corpus-of-record rule.** A pack's trigger-phrasing test set is checked into the pack itself at `evals/evals.json` — the form `eval_check` validates, the release gate sweeps for coverage, and `/check-routing`'s blind judges consume (corrected 2026-07-26, issue #95: this rule previously named `scripts/routing-corpus.json`, which shipped practice had already superseded in every current suite). A `scripts/routing-corpus.json` positives/negatives file may ride along as `routing_eval.py`'s lexical-legibility aid — useful, optional, and by that script's own docstring "NOT THE PROOF." Either way, a review-time-only corpus that never lands in the tree evaporates, and isn't a test of record the next reviewer can rerun.
- **The answer contract.** State the shape every consult answers in — the base form is *claim + cited file + the failure mode or caveat*; a pattern-catalog pack (naming a reusable shape) extends it with *name / anatomy / when-it-fits*. One worked example on this contract belongs in the body; the rest is retrieval, not restatement.

**Command.** The human chose the timing — do not re-ask why. Preconditions gate first (validate `$ARGUMENTS`, working-tree state, credentials) and each failed precondition has a named branch. Side-effect confirmation points are explicit ("show the diff; proceed only on approval"). Ends with a report format. `allowed-tools` pre-approves exactly the verbs the workflow needs (`Bash(git add *)`), nothing broader.

## Calibration — too lean, too thick

| Too lean (no behavior delta) | Too thick (context tax + drift) |
|---|---|
| Describers: "be careful with edge cases", "handle errors properly" | > 500 lines inline; references not split out |
| Restates what the model already does correctly | Restates substrate owned by another skill or doc |
| No output contract; no failure branches | One-time-step phrasing that dies after turn one |
| Vague quantifiers on load-bearing dimensions | Instruction walls — adherence decays past ~150–200 instructions in context |
| Description is a noun-phrase label | Overfit to one repo: hardcoded paths, voodoo constants, brittle assumptions |

The symmetric resolution is the same move: run the deletion test line by line — coverage-forcing enumerations as a block, per rule 3; what survives is the skill.

## Stimulating the right reasoning

Match grammatical mood to the computation wanted. Imperatives request the *form* of an act; **questions force the computation itself** — "What would a security reviewer flag in this handler?" generates the flags to answer it. Match question polarity to epistemic state: leading ("what's wrong with X") for known-defective artifacts, neutral ("is anything wrong with X") for triage. Where output has a shape, give the skeleton — slots to fill beat open generation, and illegal outputs become grammatically hard to reach. Full mechanism catalog: `prompt-wording-rules` (§1–§12).

## Evaluate before shipping

The check is a **baseline comparison**: a few realistic prompts, each run in a fresh session with the skill available and again with it disabled (`skillOverrides: "off"`), comparing trigger reliability and output quality separately — a skill triggering proves Claude found it, not that it worked. A fresh session is mandatory; authoring-session context masks gaps in the written instructions. The official `skill-creator` plugin automates the loop (isolated runs, grading, benchmark, description tuning with should-trigger and near-miss should-not-trigger prompts). `/make-skill` builds this in as Phase 2 and Phase 5.

## What an edit owes — the tier ladder

Authoring earns the full loop; an edit owes only its tier (ruled 2026-07-12, codifying the
estate's proven practice — the forge-side twin of teamwork's solo-first floors):

| Edit class | Owes |
|---|---|
| **Mechanical** — trim, typo, formatting, a suite annotation, a ledger line | lint, nothing more |
| **Description/boundary** — trigger phrasing, a fence added or moved, dials | lint + the suite updated in the SAME change + `/check-routing` at the wave boundary (a batch of boundary edits shares one run; per-edit runs are ceremony) |
| **Semantic body change, or a new artifact** | the full loop — lint, fresh-context critic (generator ≠ critic), behavior check |

Two clauses the ladder carries: **a reciprocal fence costs description characters — re-budget
the description before adding one**, not after the 1,024 warn (the trim round-trip is the
predictable failure); and an edit that *changes tier mid-flight* (a "trim" that reworded a
trigger) owes the higher tier it became.

## Failure catalog

| Failure | Mechanism | Fix |
|---|---|---|
| Reserved word in the name | `claude`/`anthropic` in a skill name or directory is rejected at install — the whole plugin fails to load | Rename (lint F8 blocks it at write time); name the artifact, not the platform |
| Description-as-label | No trigger conditions → never fires | Trigger contract: what + when, user's verbatim phrasings first |
| Beautiful body, lazy description | Only the description controls triggering | Spend authoring effort proportional to what each part controls |
| One-time-step phrasing | Body persists but is never re-read | Standing instructions, spec-present tense |
| Contracts in the tail | Compaction keeps the first 5,000 tokens | Contracts and gates in the head, examples last |
| Restated model knowledge | Deletion test fails; pure context tax | Cut; keep only the delta |
| Restated substrate | Drift pair with the canonical home | Reference by name; never copy |
| Implicit invocation dials | Behavior acquired by omission, unpinned across versions | Both dials explicit on every skill; the lint enforces it |
| Preload expects a command skill | `disable-model-invocation: true` blocks `skills:` preloads | Preloaded modules are knowledge species (model-only) |
| `allowed-tools` as a wall | It grants; it never restricts | `disallowed-tools`, permission deny rules, or an agent tool allowlist |
| Guidelines-only fork | Fork receives no actionable task → empty return | Forked bodies carry explicit, self-sufficient instructions |
| Malformed frontmatter | Body loads with empty metadata; discovery silently dead | `claude --debug`; the lint catches it at write time |
| Skill "stops working" mid-session | Content present; model prefers other approaches | Strengthen description + instructions, or enforce with a hook; re-invoke after compaction |

## Provenance

Factual substrate: the project's *Verified Factual Foundation* (July 2026) plus live doc checks against code.claude.com/docs/en/skills at authoring time; the preload correction above supersedes both the foundation doc's §2 and corpus Vol 1 §6.6. All quantities [drift-prone]: on a Claude Code version bump, re-verify this table against `/doctor` and the changelog before relying on it.
