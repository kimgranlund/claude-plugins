---
name: file-brand
description: >-
  Stamps a finished (or partial) brand corpus into a distributable — an installable plugin, a
  Claude-chat cloud skill, a standalone MCP, or the corpus repo itself made into its own
  Claude-ready seat — and runs the brand-lint structural check before ratifying. Always asks
  which form; never defaults. Use when the user wants to package, ship, stamp, or ratify a brand
  as a plugin/skill/MCP/project — "stamp this brand", "package the brand as a plugin", "ship this
  as a skill", "make this brand corpus deployable", "make this brand repo answer its own
  questions". NOT the corpus-as-site export (file-brand-corpus) and NOT the one-page summary
  (make-brand-stack).
disable-model-invocation: false
user-invocable: true
argument-hint: "[plugin|skill|mcp] [corpus path] [brand name]"
---

# file-brand

Packages a finished brand corpus into a shareable, host-appropriate artifact. This is the
mutability-class ratification point — the corpus is treated as an accepted record from here on,
following the same discipline `docs:doc-writing-rules` states for its Ledger mutability class
(ADR/IDR/RDD: append-only, supersede never edit) — once stamped, amend by superseding, never by
silently rewriting what shipped. This skill's output follows that existing contract; it does not
invent separate ratification semantics.

Request: `$ARGUMENTS`, parsed as `[form] [corpus] [name]` (form ∈ `plugin | skill | mcp |
project`). There is no default form.

## Procedure

1. **Ask which shape — always.** Form not named explicitly → stop and ask. `plugin`/`skill`/`mcp`
   each emit into their own folder under `-o <out>` (`<out>/plugin/`, `<out>/skill/`,
   `<out>/mcp/`) and stay pure — the plugin form never carries the cloud-skill or
   standalone-MCP packaging. `project` stamps in place instead, with no `-o`.
   - `plugin` → Claude Code / Cowork: an installable plugin (corpus + a read-only `brand-corpus`
     stdio MCP + a thin brand skill). Bundled snapshot by default; `--linked` points the MCP at a
     live `corpus_dir`.
   - `skill` → Claude chat (cloud): a standard Agent Skill folder (`SKILL.md` + the corpus bundled
     in `references/`, one folder per layer). No MCP, no scripts — cloud can't run local
     processes.
   - `mcp` → standalone deployable MCP: the stdio server + the corpus (bundled or `--linked`) plus
     a `README.md` with the `claude mcp add` recipe.
   - `project` → the corpus repo itself, made a Claude-ready seat: stamps IN PLACE into the
     repo's own `.claude/` — a `<brand>-facts` consult skill reading the live in-repo corpus, an
     `/ask-brand` command skill, `agents/brand-liaison.md` (the judgment surface for cross-session
     perspective asks — see `stamping.md`'s modality-7 contract), and `.mcp.json` wiring. Linking
     to the live corpus is the effective default here (the corpus already lives in this repo);
     `--snapshot` bakes a frozen copy under `.claude/corpus/` instead.
2. **Check readiness.** Invoke the `brand-corpus` skill to assess the corpus's maturity stage. A
   corpus stamps well only once `01-foundation` is decided (stage ≥ 1) — name the stage and what's
   missing. Stamping a stage-1 corpus is allowed, but say so plainly: that's shipping a seed, not
   a brand. Confirm the corpus path and brand name before writing anything.
3. **Lint before ratifying.** Run `brand_lint.py` against the corpus's foundation and expression
   docs — e.g. `find <corpus> -name '*.md' | xargs python3
   "${CLAUDE_PLUGIN_ROOT}/scripts/brand_lint.py"` (or the specific docs about to ship). It is
   advisory by design — a clean run says "no structural tells," never "this brand is good" — so
   surface any findings (archetype language, the vision/mission/values template, personas,
   brand-DNA word-clouds, values stated without trade-offs) to the user and get an explicit call
   (fix, or ship with the finding on the record) before step 4, rather than silently stamping over
   it.
4. **Stamp it.** `plugin`/`skill`/`mcp`: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py"
   {plugin|skill|mcp} <corpus> --name <brand> -o <out>` (add `--linked` for `plugin`/`mcp`;
   `plugin` also takes `--version`). `project`: `python3
   "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py" project <corpus> --name <brand>` — no `-o`; it
   derives the repo root from `<corpus>` (override with `--repo-root`), add `--snapshot` to bake a
   frozen copy instead of linking the live corpus.
5. **Verify the output.** `plugin`/`skill`/`mcp`: `python3
   "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py" verify <out>/<form>/<brand>-brand --form
   <plugin|skill|mcp>`. `project`: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py" verify
   <repo_root> --form project`. Either way this is the stamp script's own built-in check
   (self-contained; no external plugins-factory dependency). A failure is a finding to fix before
   handing it over, never something to ship past.

## Run modes

**Filesystem-only (Claude Code / Cowork), disclosed — no Project mode.** Every step is
script-load-bearing (`brand_stamp.py`, `brand_lint.py`) and the output IS files on disk (a plugin,
skill folder, or MCP package); a Claude Project single-context session has no filesystem to write
that output to and no way to run the scripts. State this plainly rather than attempting a
degraded chat-only stamp — there is no meaningful in-chat equivalent to "package a distributable."

## Failure branches

- Form not named → stop and ask; never guess (a wrong guess wastes the stamp — the four forms
  target different hosts and runtimes).
- `project` form and `<corpus>` isn't inside a git repo (no `.git` found walking up) → the derived
  repo root falls back to `<corpus>`'s parent; confirm that's the intended root, or pass
  `--repo-root` explicitly, before writing anything.
- `brand_lint.py` reports findings and the user wants to ship anyway → record the decision in the
  response; never suppress the finding to make the ratification look cleaner.
- `verify` fails → fix and re-stamp; a failing verify is never handed over as done.

## Done / NOT done

Done when the form was explicitly confirmed, readiness was named, `brand_lint.py` ran with its
findings (if any) acknowledged on the record, the artifact stamped, and `verify` passed clean. NOT
done if any of those five steps was skipped or its output silently discarded.
