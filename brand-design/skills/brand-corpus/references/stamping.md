# Stamping a corpus into a distributable

A finished (or partial) brand corpus is **stamped** into one of four forms, chosen by where it will be used. Each is produced by `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py"`. Three emit into their **own folder** under `-o <out>`, kept **pure and separate** — the plugin never carries the cloud skill or the standalone-MCP packaging; the fourth, `project`, stamps **in place**, turning the corpus repo itself into a Claude-ready seat. The _judgment_ (is it ready? which form? what name?) lives in `file-brand` and this skill.

## Readiness — don't stamp a snapshot of nothing

Stamp against the corpus maturity stages (see `corpus-architecture.md`). A corpus needs a decided **01-foundation** (stage ≥ 1) to be worth stamping; below that you're shipping scaffolding. Stamping is allowed at any stage, but the stamp should **name the stage**, so the recipient knows whether they hold a seed or a stewarded brand. Build down the stack before stamping ahead of it.

## The form is the user's choice — always ask

`file-brand` **always asks** which form; it never defaults. The four target different hosts and runtimes, so a wrong guess wastes the stamp.

|  | **plugin** | **skill** | **mcp** | **project** |
| --- | --- | --- | --- | --- |
| **For** | Claude Code / Cowork | Claude chat (cloud) | self-host / `claude mcp add` | the corpus repo, made its own consult seat |
| **Is** | installable plugin: corpus + the stdio `brand-corpus` MCP + a thin brand skill | a standard **Agent Skill folder** + the corpus bundled in `references/` | the stdio MCP server + corpus + a wiring `README.md` | the repo's own `.claude/` scaffold: a facts consult skill, `/ask-brand`, a `brand-liaison` agent, `.mcp.json` |
| **Local code?** | yes (bin/ MCP) | **no** — cloud can't run a local process | yes (stdio server) | yes (in-repo MCP) |
| **Retrieval** | the bundled MCP | the skill reads its own `references/` | the MCP, once wired | the in-repo MCP, or the facts skill reading the corpus directly |
| **Corpus** | folder-convention snapshot (or `--linked`) | bundled inside the skill (`references/<layer>/…`) | folder-convention snapshot (or `--linked`) | the repo's own live corpus (or `--snapshot` to bake a copy) |
| **Output** | `<out>/plugin/<brand>-brand/` | `<out>/skill/<brand>-brand/` | `<out>/mcp/<brand>-brand-mcp/` | in place: `<repo_root>/.claude/…` + `<repo_root>/.mcp.json` |

`plugin`/`mcp` use the folder convention + the MCP; `skill` bundles the corpus as the skill's own references (sub-folders are fine in a skill — the flat `NN-layer--name` convention is only needed when the corpus goes in as _separate_ claude.ai Project knowledge rather than bundled in the skill). `project` is the odd one out: it never copies the corpus into a separate output tree, because the corpus already lives in the repo being stamped.

## What each folder contains

```text
<out>/
├── plugin/<brand>-brand/          .claude-plugin/plugin.json · .mcp.json · bin/brand-corpus-mcp.py
│                                  corpus/<layer>/… (bundled) · skills/<brand>-brand/SKILL.md
├── skill/<brand>-brand/           SKILL.md · references/<layer>/… (the corpus, bundled in the skill)
└── mcp/<brand>-brand-mcp/         brand-corpus-mcp.py · corpus/<layer>/… (bundled) · README.md (claude mcp add recipe)

<repo_root>/                       (project form — stamped IN PLACE, no separate <out>)
├── .mcp.json                      wires brand-corpus at .claude/scripts/brand-corpus-mcp.py
└── .claude/
    ├── scripts/brand-corpus-mcp.py
    ├── skills/<brand>-facts/SKILL.md    consult skill, reads the in-repo corpus
    ├── skills/ask-brand/SKILL.md        /ask-brand command surface
    ├── agents/brand-liaison.md          cross-session perspective (modality 7, see below)
    └── corpus/<layer>/…                 only with --snapshot
```

## Bundled vs linked (`plugin` and `mcp`), and the `project` default

- **Bundled** (default for `plugin`/`mcp`): the corpus is copied in as a **snapshot** at stamp time — self-contained and distributable. Env `BRAND_CORPUS_DIR=${CLAUDE_PLUGIN_ROOT}/corpus` (plugin) or `$(pwd)/corpus` (mcp).
- **Linked** (`--linked` for `plugin`/`mcp`): no corpus is copied; the MCP points at a **live** corpus dir — `userConfig.corpus_dir` for the plugin, or a `BRAND_CORPUS_DIR` you set for the standalone MCP. What a brand's own team wants.
- **`project` inverts the default**: linking to the live in-repo corpus (no `--snapshot`) is the EFFECTIVE DEFAULT, because the corpus already lives in the same repo the scaffold points at — baking a snapshot of a repo into itself is the non-default case (`--snapshot` bakes a frozen copy under `.claude/corpus/` instead, for a repo that wants a pinned copy rather than always reading its own live working tree).

(The `skill` form has no bundled/linked switch — the corpus _must_ travel inside the skill, since cloud has no MCP.)

## `project` — the corpus repo as its own seat (modality 6)

`brand-stamp project <corpus_dir> --name <brand> [--repo-root R] [--snapshot]` stamps IN PLACE: no `-o`. The repo root is derived by walking up from `corpus_dir` to the nearest `.git` (override with `--repo-root` for an unusual layout). This closes modality 6 of the corpus's operating surface — a generated corpus that ships its own `.claude/skills|agents|commands`, able to answer questions about itself without anyone first packaging it as a plugin.

## Cross-session perspective — the modality-7 contract

Modality 7: another fleet agent, from a **separate** Claude Code session, wants this brand's perspective. The static `brand-corpus` MCP is **data-only** — it fetches documents and tokens, it never renders a judgment. Two ways in:

1. **Message the project's own session** (if one is live) and ask the question in natural language — it can read its own corpus and answer with the full context a live session carries.
2. **Dispatch this repo's `brand-liaison` agent** (`.claude/agents/brand-liaison.md`, emitted by the `project` form) — the judgment surface built for exactly this ask: it reads the in-repo corpus and answers with citations, without needing a live session.

Never treat the MCP's `search_brand`/`fetch_brand_section` output as if it were itself the brand's opinion — it is the evidence a judgment (from a live session or `brand-liaison`) would cite, not the judgment.

## Versioning — re-baking is a release

A bundled corpus is a **baked snapshot**, and shipping it is a _release action_: when the corpus changes, re-stamp from the source workspace and **bump the version** (`brand_stamp.py plugin … --version 0.2.0`). The editable **source-of-truth corpus lives in the consumer's version-controlled workspace** — never inside the plugin (the install cache is read-only). The plugin / skill / mcp artifacts are derived, versioned outputs; the workspace is the canon.

## Sizing the retrieval

Bundle _size_ decides how the brand is retrieved — it is not always "an MCP":

- **Small** — inline reference files + progressive disclosure; the `skill` form (corpus in `references/`, no MCP) is enough.
- **Medium** — the generated `INDEX.md` manifest + many on-demand files (skill), or the bundled grep MCP (plugin / mcp).
- **Large / queryable** — an **indexed** MCP (SQLite / embeddings) so context only ever holds the retrieved slice.

Every bundled corpus now ships an `INDEX.md` (per-layer manifest). The bundled reference MCP does **live grep** over the markdown — fine for small/medium; a genuinely large corpus wants an indexed server (a future `--index` that builds a SQLite/embedding index). The MCP is the retrieval _tier_, not a default for every bundle.

## Cloud limits — why `skill` carries no MCP

Claude chat can run **skills** (with bundled files/sub-folders) and use **remote (HTTP) MCP connectors**, but it **cannot run a local process** — no stdio MCP, no `bin/` scripts, no hooks. So the cloud form ships the corpus _inside the skill_. If you want live MCP retrieval in chat, host the `mcp` form's tools behind an HTTP transport and add it as a connector (the tool contract is identical — see `mcp-wiring.md`).

(Marketplace-distributed plugins' **skills** also surface in Claude chat, so a stamped _plugin's_ skill reaches chat too — only its bundled MCP / bin / hooks won't run there. The `skill` form is just the _self-contained_ chat artifact: it carries its own corpus, with no MCP dependency.)

## After stamping

**Verify first, every form.** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_stamp.py" verify <root> --form {plugin|skill|mcp}` asserts the stamped artifact has the structure its form requires before you ship it — plugin: a valid `plugin.json`/`.mcp.json` + the bundled server + the skill; skill: `SKILL.md` frontmatter + a non-empty `references/` corpus **and no leaked MCP/scripts** (the cloud form must stay pure); mcp: the server + the `claude mcp add` recipe — plus a drift check that the bundled `brand-corpus-mcp.py` matches the canonical one. (CI runs `verify` on all three forms; `brand_stamp.py selftest` proves the gate.) Then:

- **plugin**: `validate_plugin.py plugin <out>/plugin/<brand>-brand --strict` (it's authored to pass — the deep validation `verify` complements); then add it to a marketplace or install it. `/plugin-promote` for a hostile read first.
- **skill**: upload `<out>/skill/<brand>-brand/` to Claude chat as a skill — it carries its own corpus.
- **mcp**: run the bundled server's `… brand-corpus-mcp.py selftest`, then follow `<out>/mcp/<brand>-brand-mcp/README.md` to wire it (`claude mcp add`), or host it as a connector.

The factory feeding the factory: brand-design stamps all three; **plugins-factory** is the standard the plugin form is validated against, and `brand-corpus` is its worked MCP exemplar.
