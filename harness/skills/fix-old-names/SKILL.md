---
name: fix-old-names
description: >-
  Sweep a repo for references to RETIRED plugin, skill, agent, or command names from a rename
  wave and rewrite the live ones. Use for "my agent dispatch says no such agent", "these skill
  names look old", "did the rename break this repo", "migrate this repo to the new names", or
  "a CI check that fails when our config references a renamed agent" — that gate ships with it.
  Reads a derived manifest, never guesses. NOT for choosing a new name (naming-rules); NOT for
  executing a rename in the plugin repo itself (big-change-git-rules); NOT for mechanizing some
  other check as a script (make-script); NOT for general repo drift (clean-repo).
disable-model-invocation: false
user-invocable: true
argument-hint: "[repo-root, default .]"
---

# fix-old-names

A rename wave inside a plugin repo is invisible to every repo that merely **installs** those
plugins. Those repos keep the old handles, and each one fails silently: a retired agent name
errors only at dispatch, a description citing a retired skill mis-routes with no diagnostic at
all. This command finds them from a manifest and rewrites the ones that must still resolve.
Target root: `$ARGUMENTS` (default `.`).

The one rule everything else serves: **a pointer gets fixed, a record gets left alone.** An ADR
saying "we renamed X to Y" must keep saying exactly that. Rewriting it destroys the only
evidence of the rename — a worse outcome than the stale pointer you were fixing.

A `Bad:`-labeled counterexample is the same record, in miniature: the retired name it quotes is
quoted on purpose — text inside a labeled counterexample (a `Bad:` table cell, a "retired name
kept as the counterexample" annotation) is record, never a live reference, and a sweep rewrites
live references only. The ADR-0006 sweep rewrote naming-rules' own `Bad:` cells this way,
collapsing three rows to degenerate Bad==Good pairs — found 2026-08-12 by a fresh-context audit
and restored by hand the same day (issue #171 / harness 3.1.21). Freeze such a cell with
`<!-- fix-old-names: keep -->` if the classifier ever reads it as a pointer.

## Phase 1 — Report first, always

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fix_old_names.py" <root>
```

Report-only is the default and exits 1 when live stale names remain. Five buckets come back:

- **L1 live** — a reference that must resolve: a frontmatter `skills:` preload, a dispatch name,
  a seat map, a doctrine pointer. These are the silent failures.
- **L2 ambiguous** — a retired name that became *both* a command and an agent (`ops-issues` →
  `sort-issues` or `issue-sorter`). Reported with both candidates, never rewritten from prose;
  only a typed slot resolves it. **These need a human — bring them to the user as a choice.**
- **L3 historical** — ADR bodies, ledgers, changelogs, dated records. Counted, never touched.
- **L5 dated** — the retired name sits on a line carrying an ISO date. A date proves nothing
  either way: measured on real data, half such lines were records ("Codified 2026-07-12
  (repo-alignment Phase 3)") and half were live pointers that merely end with one ("the
  component-author skill, which points here. Distilled 2026-06-27"). Reported for a human,
  never guessed in either direction.
- **L4 path** — the retired name appearing as a *filename* or path component. The consumer repo's
  own file was never renamed, so rewriting the reference points it at nothing. Reported, never
  rewritten. Found the hard way on the first live sweep: `a2ui-training-corpus` is both a retired
  skill and a real `.spec.md` on disk, and the sweep broke two working markdown links.

## Phase 2 — Read the report before writing

Skim the L1 list for anything that is really a record the classifier read as a pointer. The
split is by record TYPE, not by directory: `docs/process.md` is live doctrine while
`docs/tickets/**` is a record, and a repo that files its records somewhere unusual needs
`--historical <glob>` (repeatable) to say so. A `<!-- fix-old-names: keep -->` marker freezes
one line where the heuristics and the intent disagree.

Surface the count and the L2 list to the user, then apply:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fix_old_names.py" <root> --write
```

Re-run without `--write` afterwards. **Zero live hits is the done condition** — a sweep that
does not re-verify has not finished. Report what changed AND what was deliberately left.

## Phase 3 — What the sweep cannot reach

- **Project memory** lives outside the repo (`~/.claude/projects/<slug>/memory/`). `--include-memory`
  covers it; it is off by default because writing outside the repo you were pointed at deserves
  a knowing yes. Ask before using it.
- **A retired name absent from the manifest** is never guessed at. If the user names a rename the
  manifest lacks, the fix is to regenerate the manifest in the plugin repo
  (`fix_old_names.py derive` at that repo's root), not to hand-edit `renames.json`.
- **Anything outside `.claude/`, `CLAUDE.md`, `docs/`, `AGENTS.md`, `.github/`** — source code
  referencing a plugin handle is out of scope by design.

## There is no runtime alias — the sweep is the whole mechanism

Do not propose a hook, a shim, or an alias layer to catch what this sweep misses. It was built,
shipped, and retired inside one day (2026-07-26); the finding is recorded here so the next reader
does not spend the day again.

**Proven, by running it:** both `Task` and `Skill` validate the requested name against their
registry *before* `PreToolUse` fires. A retired name never reaches a hook, so a hook cannot
translate it.

```
Agent type 'ops-planner' not found. Available agents: …
Unknown skill: intent-extract
```

Two consequences worth keeping straight:

- **A retired dispatch does not fail silently.** The platform already errors and lists the valid
  names. The premise that motivated an alias layer was wrong for the dispatch path — what it
  cannot tell you is what the old name *became*, and no hook can add that.
- **A stub skill or agent per retired name would work**, and is still rejected: 288 stub
  descriptions against a resident listing budget this estate has already breached four times.

What *does* still fail silently is the case this skill exists for — a **description** or doctrine
pointer citing a retired name, which mis-routes with no error at all. Files are the only surface
where the failure is invisible, which is why a file sweep is the only mechanism that pays.

## Wiring it as a gate

The default invocation already is one: exit 1 on live stale names, exit 0 clean. A consumer repo
adds it to CI, or to a PostToolUse hook, with no extra flags. `--json` emits the same three
buckets as data.

## The manifest

`${CLAUDE_PLUGIN_ROOT}/renames.json` — `{old, new, kind, old_plugin, new_plugin, match}` per
entry, derived by `fix_old_names.py derive` from git rename detection, which is the only record
of a rename that cannot drift from what shipped. It carries `old_plugin`/`new_plugin` separately
from the name because a **plugin-prefix-only** rename (`color:token-builder` →
`design:token-builder`, where the name never changed) is invisible to any name-to-name map — the
exact class that survived the first automated pass over a consumer repo in 2026-07.

`match` is the safety valve: `token` names may match bare, `qualified` names only ever match as
`plugin:name`. That is what keeps the sweep from rewriting the English word "build", or
clobbering `make-skill` — a name that is simultaneously current and formerly-old.
