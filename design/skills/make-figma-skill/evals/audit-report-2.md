# Audit report 2 — design:make-figma-skill (FLOOR depth, post source-shapes extension)

Skill: `/Users/kimba/Projects/nonoun/plugins/design/skills/make-figma-skill/SKILL.md`
Standards: harness `skill-writing-rules` (+ `check-skill` procedure, `checking-rules`)
Change under audit: `convert` now accepts a command-species skill dir or an `agents/<name>.md`
file in addition to a plain skill dir (`references/conversion-rules.md` §Source shapes,
`load_source()` in the checker, 8 new selftest fixtures, description re-dieted).

Lint: `python3 harness/scripts/skill_lint.py design/skills/make-figma-skill/SKILL.md` →
**clean** (`skill-postwrite-invocation-lint`).
Bundled checker (`scripts/figma_skill_check.py selftest`): **32/32 PASS** — confirmed by
direct run. The suite does NOT cover cross-plugin (`plugin:name`) preload resolution or
agent-source provenance hashing — see findings 1–2 below, both discovered only by running
`load_source()` and `--hash` directly against synthetic fixtures, not by reading prose.
`eval_check.py design/skills/make-figma-skill/evals/evals.json` → **clean** (27 cases: t01–t15
trigger, n01–n11 no-trigger; t13–t15/n11 confirmed present for the agent/command extension).
Description measured 691 chars (claimed ≤700) — confirmed true by direct count.

## Verdict: FAIL (2 blocking findings)

Both blocking findings are runtime-verified defects in the exact mechanism this extension
added (`load_source()`'s agent-preload resolution, and `--hash`'s source-shape coverage) —
not prose gaps. Neither is caught by the 8 new selftest fixtures, which exercise same-plugin
preloads and directory sources only.

## Findings

| # | Severity | ID | Evidence (file:line) | Finding | Fix |
|---|---|---|---|---|---|
| 1 | **BLOCKING** | R7 (contract honesty — runtime-verified) | `SKILL.md:19-22` ("preloads inlined whole", "without losing resolution"); `references/conversion-rules.md:52` ("A cross-plugin preload (`docs:x`) is inlined from that plugin's checkout…"); `references/checklist.md:9` (tagged `[F6]`, and `checklist.md:3` promises bracket tags "name the checker dimension that mechanizes the line"); `scripts/figma_skill_check.py:15-18` (docstring: preloads "resolved at `<plugin-root>/skills/<name>/`"); actual code at `figma_skill_check.py:235,237-238` — `plugin_root = source.parent.parent` (the agent's OWN plugin) and `local = p.split(":")[-1]` (the `plugin:` prefix is parsed then **thrown away**). Direct test: an agent in a synthetic `pluginA` with `skills: [docs:some-knowledge]`, and the real skill placed under a sibling `docs/skills/some-knowledge/SKILL.md`, produced `errors: ['preload `docs:some-knowledge` not found at .../pluginA/skills/some-knowledge — cross-plugin preloads must be inlined from their own plugin or Dropped']` — it never looked in `docs/`, only in the agent's own plugin. Worse: when `pluginA` was given a coincidentally same-named **local** `skills/some-knowledge/` (unrelated content, no `4.5:1` etc.), resolution succeeded with **zero errors**, silently substituting the wrong skill's headings/anchors into the F6 corpus — a false F6 PASS while the real cross-plugin content is never checked at all. Both cases reproduced live, not inferred. | Make `load_source()` prefix-aware: on a `prefix:local` preload, resolve first at `plugin_root.parent / prefix / "skills" / local` (the sibling plugin, matching the `plugin:skill` handle convention this same SKILL.md already uses, e.g. `harness:make-skill` at `SKILL.md:11`); fall back to same-plugin only when no prefix is given; when a prefix is given, never silently accept a same-named local skill instead. Add 2 selftest fixtures: a genuine cross-plugin resolution that succeeds, and the collision case proving the explicit prefix wins over a same-named local skill. |
| 2 | **BLOCKING** | R7 (contract honesty — runtime-verified) | `references/conversion-rules.md:108-118` (Provenance fields: `hash:` ← `` `python3 scripts/figma_skill_check.py --hash <source-dir>` ``, no carve-out for a file source); `SKILL.md:69-70`; `references/checklist.md:43`; `references/rubric.md:35` receipt template — all state the hash comes from `--hash <source-dir>` unconditionally, including for the new agent-file source shape. `figma_skill_check.py:596` (`if len(argv) != 2 or not Path(argv[1]).is_dir()`) rejects a file path outright. Direct run: `python3 scripts/figma_skill_check.py --hash design/agents/design-system-checker.md` → `usage: --hash <source-skill-dir>`, **exit 2** — there is no documented command that produces a hash for an agent-species conversion at all. The apparent workaround (pass the plugin root) is also broken: `HASH_EXCLUDE_DIRS = {"agents", "evals", "__pycache__", "dist"}` (`figma_skill_check.py:181`) excludes `agents/` from the walk, so `source_hash(Path("design"))` (verified: returns `3d388306f086`, exit 0) is structurally blind to changes in the very agent file being converted, while it pulls in every unrelated sibling skill under `design/skills/`. The regeneration-trigger contract at `SKILL.md:114` ("Source `hash:` differs from the export's `## Provenance` → regenerate the whole file") and F5's `hash:`/`inventory:` WARN (`figma_skill_check.py:297-299`) are non-operational for this extension's own new source shape. | Extend `--hash` to accept an `agents/<name>.md` path: hash the agent file's own bytes plus, per its `skills:` preloads, each resolved skill's tree — reuse `load_source()`'s own corpus-resolution walk so the two mechanisms are built from one code path and can't drift apart again. Add a selftest fixture proving the agent-source hash changes both when the agent file changes and when a preloaded skill's content changes. |
| 3 | MINOR | R8/R5 (quantities / no restatement) | `references/checklist.md:13` and `references/conversion-rules.md`'s "the source's own `evals/evals.json`… `t*` prompts are the trigger vocabulary" apply unconditionally to every source kind; `figma_skill_check.py:344-363` (F8) does the same — it WARNs on any `expect: trigger` source prompt sharing no content word with the output description, with no carve-out for a command-species source, whose converted description is deliberately built to say only "Invoke with `/name`… no auto-trigger phrasing" per `SKILL.md:53-55`/`conversion-rules.md:43`. A command source's `t*` prompts (still labeled `trigger` per `eval_check.py:16`'s universal `{trigger, no-trigger}` vocabulary, confirmed by reading the schema) will systematically WARN on F8 even when the export is correctly built per spec. Low severity: F8 is WARN-only (never blocks, confirmed `figma_skill_check.py:361` appends `WARN` not `FAIL`), and no false FAIL results. | Either skip F8 when `kind == "command"` (the deliberately-thin description makes the WARN structurally expected, not informative), or note in `conversion-rules.md`'s Trigger description rules section that an F8 WARN on a command-derived export is expected and not actionable. |

## What was checked and cleared (no finding)

- **Probe 2 (command-source vs. "Invoke with `/name`, no auto-trigger" rule):** no contradiction
  found. `SKILL.md:53-55`, `references/conversion-rules.md:43`, `references/checklist.md:20` all
  state the same rule consistently, and the checker's `ACTIVE_TRIGGER_RE`
  (`figma_skill_check.py:93`) explicitly includes `invoke with` as a satisfying F4 clause —
  confirmed by the selftest's own dedicated case, "'Invoke with /name' counts as an active
  trigger (command-derived)" (PASS, run directly). No place tells the author to add auto-trigger
  phrasing for a command source.
- **F2/F3/F4 pattern additions** (`tools`, `skills`, `color`, `background` in `CLAUDE_ONLY_KEYS`;
  `$ARGUMENTS`, `SendMessage`, `Agent/Skill tool` in `SIDECAR_PATTERNS`) all have a matching row
  in `references/conversion-rules.md`'s Source-shapes tables (Command §, Agent §) — no dangling
  pattern, no undocumented pattern. Confirmed by direct cross-read of both files.
- **evals.json**: t13–t15 (agent/command conversion prompts) and n11 (fencing
  `harness:make-agent` territory) are present and pass `eval_check.py` clean; the note field
  documents the 2026-08-27 extension. No stale/orphaned case IDs.
- **Description diet**: measured 691 chars against the claimed "≤700" — true, direct count.
- Delegation-mechanics gate: N/A — no `context: fork` / `agent:` / `model:` in this skill's own
  frontmatter (confirmed unchanged from the prior audit); the "dispatch a fresh-context
  reviewer" language is a handoff to a separate skill invocation, not a fork this skill
  configures.
- Both dials still explicit (`disable-model-invocation: false`, `user-invocable: true`,
  `SKILL.md:12-13`); ≤3 hard gates unchanged; output contract/failure branches/stopping
  predicate still in the head.

## Top 3

1. **(BLOCKING)** `load_source()`'s agent-preload resolution never actually looks in a
   cross-plugin `docs:x`-style preload's own plugin — it strips the prefix and always resolves
   under the agent's own plugin root (`figma_skill_check.py:235,237-238`), producing either a
   misleading "not found" error or, worse, a **silent** false F6 PASS built on a coincidentally
   same-named local skill's wrong content. Reproduced live both ways. Fix: make resolution
   prefix-aware; add 2 selftest fixtures.
2. **(BLOCKING)** The agent-source shape this extension adds has no working provenance-hash
   path: `--hash` rejects a file argument outright (usage error, exit 2, reproduced live), and
   the plugin-root workaround silently excludes the `agents/` directory from the hash walk
   (`HASH_EXCLUDE_DIRS`, `figma_skill_check.py:181`), so the documented regeneration-trigger
   contract (`SKILL.md:114`) cannot fire for an agent conversion. Fix: extend `--hash` to accept
   an agent file, reusing `load_source()`'s own corpus walk.
3. **(MINOR)** F8's trigger-vocab WARN applies uniformly to command-derived exports even though
   their descriptions are deliberately built to avoid the vocabulary F8 is checking for — no
   false FAIL results (WARN only), but the WARN is structurally expected noise for that source
   kind. Fix: skip F8, or document the expected WARN, for `kind == "command"`.
