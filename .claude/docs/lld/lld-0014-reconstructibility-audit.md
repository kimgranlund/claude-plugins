---
doc-type: lld
id: lld-0014-reconstructibility-audit
status: draft
version: 0.1.0
date: 2026-08-18
owner: kim.granlund
spec: none — ADR-0022 (accepted) is the upstream contract; gh#627 is the ticket
ticket: nonoun-plugins#627
---
# LLD — reconstructibility audit + the two owed-at-lock mitigation docs (ADR-0022's own instrument)

**Anti-matrix routing, ruled first (ADR-0022's own Open questions names this as owed):**
Home: **harness**, `skills/check-reconstructibility`. Candidates weighed: authorkit's audit
family (`naming-audit`/`bloat-audit`/`attention-audit`/`pattern-audit`/`doctrine-audit`) owns a
single, coherent axis — **estate GOVERNANCE**: does an artifact's name/prose/pattern/doctrine
conform to a written standard. Reconstructibility is a categorically different axis — **estate
RECOVERY**: what would a fresh machine lose. authorkit's own five siblings share one batch-sweep
mechanic and one report shape (`estate-audit-agent`'s parameterized `instrument`); folding in a
sixth that answers "what's missing from a clone" rather than "does this name/doc/pattern conform"
would blur that family's own single job, the same anti-matrix concern `repo-audit`'s own NOT-for
fence already states for `check-state` and `sweep-chores`. harness fits both on genuine adjacency
(`clean-git`/`repo-cleaner` already own THIS machine's git-surface hygiene — the sibling half of
"what's on disk vs. what git tracks", just scoped to the live checkout rather than a fresh-clone
hypothetical) and on charter (`CLAUDE.md`: "harness is the toolchain... governs work on every
plugin in this workspace" — a workspace-generic sweep, not one estate-governance instrument among
five). The seed comment on gh#627 already leans harness ("lean home: harness `scripts/`"); this
LLD confirms it rather than re-opening it, and records the rejected alternative (authorkit)
explicitly per the ADR-default-no discipline (no ADR needed — this is a routing call, not a fork
in project doctrine).

## Components

### `harness/skills/check-reconstructibility/SKILL.md`

Frontmatter mirrors sibling audit/report skills (`check-state`'s own shape): `kind: skill`,
`disable-model-invocation: false`, `user-invocable: true`, `argument-hint: "[repo-root]"`.
Description states the fences explicitly: NOT authorkit's estate-audit family (governance, not
recovery); NOT `clean-git`/`repo-cleaner` (THIS machine's git-surface hygiene, never a fresh-clone
question); NOT `check-state` (point-in-time work-state); NOT `check-everything` (plugin-packaging
health). Procedure: run the script, read the report verdict-first (defects/enrolled/open), route
every DEFECT to its owning next step (never fix inline — report-only per the ADR's own text),
state every OPEN item as an ADR-0022 ratification gap rather than a build failure.

### `harness/skills/check-reconstructibility/scripts/audit_reconstructibility.py`

Deterministic core, live-data shell — same split `pattern-audit`/`recurrence-audit` established:
pure functions (`classify_ignored_path`, `check_ops_tracked`, `classify_excludesfile_patterns`,
`build_report`) selftest-provable on fixture data with zero network/filesystem/git dependency;
`run()` wires them to real `git`/filesystem calls against a caller-supplied `--repo-root`
(default-free, required) and injectable `--claude-home`/`--config-home` (defaulting to
`~/.claude`/`~/.config`, overridable so a caller can point the sweep at a different machine's
mount, and so this doc's own worked selftest never touches the real machine).

```
audit_reconstructibility.py --repo-root PATH [--claude-home PATH] [--config-home PATH] [--json]
audit_reconstructibility.py selftest
```

Seven checks, each realizing one ADR-0022 line (full mapping: script's own module docstring):

1. Working-tree cleanliness — every git-ignored-and-present path, bucketed regenerable (declared
   in the repo's own `.gitignore`) / named-exception / uncategorized (a defect candidate).
2. `.claude/ops/` full-tracking — ADR-0022's own stated fact, as a regression guard.
3. Global `core.excludesFile` dependency — **both** the explicit git-config form and git's own
   IMPLICIT fallback to `$XDG_CONFIG_HOME/git/ignore` (default `~/.config/git/ignore`) when no
   explicit config overrides it. This second form is not a hypothetical: this repo's own
   `.claude/settings.local.json` ignore rule resolves entirely through the implicit path (`git
   config --get core.excludesFile` on this repo returns nothing; `git check-ignore -v` on the
   same path resolves the rule from `~/.config/git/ignore` regardless) — a check that only read
   the explicit config would silently miss this repo's own live case. Caught during this
   ticket's own day-one run (Data, below), not assumed from the ADR text alone.
4. Exception 1 (memory dir) — `<claude-home>/projects/<repo-slug>*/memory/*.md`; slug =
   `str(Path(repo_root).resolve()).replace("/", "-")`, the exact convention this machine's own
   `~/.claude/projects/` directory names already follow (verified against this repo's real
   memory dir during the day-one run). Mitigation is a PROCESS (promote load-bearing entries),
   never a doc — always reported enrolled when the dir exists, never a defect by this audit's own
   design (ADR-0022's own text: "the residue is accepted as lossy by design").
5. Exception 2 (plugin cache) — `<claude-home>/plugins/cache/`; mitigation is
   `.claude/docs/runbook/plugin-reinstall-path.md`, this same ticket's own deliverable —
   present → enrolled, missing → defect (an owed-at-lock mitigation not yet shipped is a real
   gap, never silently accepted).
6. Exception 3 (credentials) — `<config-home>/gh/hosts.yml` existence, plus a repo-tree sweep for
   any stray `.env*` file; mitigation is `.claude/docs/runbook/credential-reissuance-runbook.md`,
   same present/missing split as exception 2, PLUS a stray `.env*` file is always a defect
   regardless of the runbook's presence (a credential class documented is not the same claim as
   "no stray secret sits in the tree").
7. Exception 4 (user-scoped state) — global `CLAUDE.md`/`settings.json` existence, plus check 3's
   own excludesFile finding folded in here too (both are "entirely outside any repo," ADR-0022's
   own phrase). Always reported OPEN, never defect or enrolled — ADR-0022's own Open questions
   section leaves exception 4's exact mitigation mechanism unruled at ratification; folding an
   ADR-acknowledged gap into "defect" would misstate an already-known limitation as something
   this ticket owes to fix.

Exit codes: 0 = zero defects; 1 = ≥1 defect; 2 = usage error (repo-root missing, no `.gitignore`
at its root — a repo with no `.gitignore` at all is itself a signal this audit isn't equipped to
read, not silently treated as "nothing ignored").

Selftest fixtures (negative controls included, per `.claude/rules/scripts.md`): `classify_ignored_path`
— repo-declared regenerable (positive), the named `settings.local.json` exception (independent of
`.gitignore` content), and the reverse control — an uncategorized ignored path must NOT silently
read as regenerable. `check_ops_tracked` — the clean case, and the negative control: an on-disk
file absent from `git ls-files` must be caught. `classify_excludesfile_patterns` — passthrough
with the exception-4 tag, and the empty-list reverse control. `build_report` — one full assembly
exercising every bucket at once (4 defects / 3 enrolled / 2 open on a fixture with a mix of
findings) plus an all-clean reverse control (zero across all three buckets). All four are pure;
`selftest` touches no network, filesystem, or live git state.

### `harness/skills/check-reconstructibility/evals/evals.json`

≥6 trigger cases plus reciprocal no-trigger fences (owners named in comments): authorkit's
naming/bloat/attention/pattern/doctrine family (governance, not recovery), `clean-git`/
`repo-cleaner` (this machine's hygiene), `check-state` (point-in-time work-state),
`check-everything` (plugin-packaging health), `docs:make-doc` (ADR-0022 is already ratified —
this skill is the instrument, not the drafting seat).

### Reciprocal fences on siblings (steal-risk closure)

`harness/skills/clean-git/evals/evals.json` and `authorkit/skills/repo-audit/evals/evals.json`
each gain one new no-trigger case naming `check-reconstructibility` as the owner for a
fresh-clone-recoverability prompt that could otherwise plausibly route to either sibling —
mirrors `recurrence-audit`'s own LLD precedent (lld-0011, "reciprocal fences vs steal risks") and
the ticket's own explicit instruction.

### `.claude/docs/runbook/plugin-reinstall-path.md`

New doc-tree category (`runbook/` — none of doc-writing-rules' ten formal types fit an
operational how-to; `doc_lint.py` itself skips any file with no `doc-type:` frontmatter by
design, so a plain markdown runbook here is correctly outside its scope, not a gap). States the
reinstall path from a fresh clone: names that `.claude/settings.json`'s own
`extraKnownMarketplaces`/`enabledPlugins` declaration is ALREADY committed (verified: `git
ls-files` + `git check-ignore` both confirm it's tracked, not ignored) — narrowing exception 2 to
what's genuinely unrecoverable (the downloaded cache artifacts only, not the declaration of what
to install), cites `harness:plugin-install-facts` for the exact per-channel command forms rather
than forking a second copy of that corpus.

### `.claude/docs/runbook/credential-reissuance-runbook.md`

Same doc-tree category. Names four credential classes with re-obtain paths, no values: `gh` CLI
auth, the SSH keypair for `git@github.com`, the `CLAUDE_CODE_OAUTH_TOKEN` GitHub Actions repo
secret (`.github/workflows/claude.yml`/`claude-code-review.yml`), and the default per-run
`GITHUB_TOKEN` (named for completeness, nothing to re-obtain). Explicitly a skeleton per the
seed's own framing — class + purpose + re-obtain path + scope, not a full incident-response
runbook (Rejected alternatives).

### Ledger/manifest edits

`harness/README.md` member table row + footer ledger (v3.12.0) + `plugin.json` version bump
(3.11.0 → 3.12.0, re-read off `origin/main` immediately before bump per G14 — confirmed 3.11.0 on
`origin/main` at HEAD `686f1c2` before this branch cut). `authorkit/README.md` footer ledger
(v0.21.0) + `plugin.json` version bump (0.20.0 → 0.21.0, same re-read discipline) for its own
`repo-audit` evals-only reciprocal-fence edit. Repo-root `naming.manifest.json` gains
`{"canonical": "reconstructibility", "plural": null, "banned_aliases": []}` in `object_vocab` —
`check-reconstructibility` parses as `{verb: check}-{noun: reconstructibility}`, `check` already
registered in `verb_lex`; no authorkit-local manifest registration needed (the skill lives in
harness, which carries no per-plugin `naming.manifest.json` of its own — unlike `recurrence-audit`,
which lived in authorkit and needed both).

## Interfaces

### Skill ↔ script boundary

Same split `pattern-audit`/`recurrence-audit` established: the script is deterministic and
selftest-provable on fixture data; all live interpretation (reading the totals, routing a defect
to its owner, stating the open bucket as an ADR gap) lives in the skill body.

### Mitigation-doc existence as a live coupling, not a hardcoded assumption

The script checks for the mitigation docs at fixed relative paths
(`.claude/docs/runbook/plugin-reinstall-path.md`,
`.claude/docs/runbook/credential-reissuance-runbook.md`) — this is a real coupling (rename either
doc and the audit reports a false defect), accepted deliberately: the alternative (a
configurable path) adds a flag this ticket's own scope doesn't need, and the doc paths are this
same PR's own creation, not an external dependency likely to drift independently. A future rename
of either doc updates this one script constant in the same change (same discipline
`.claude/rules/gitignore-repair.md` already states for a retired path).

## Data

Day-one run against a fresh clone of `origin/main` (this ticket's own branch-cut clone, scratch,
per the pin-race mitigation) plus this machine's real `~/.claude`/`~/.config`:

```json
{
  "defects": [],
  "enrolled_with_mitigation": [
    {"item": "~/.claude/plugins/cache", "class": "exception-2-plugin-cache",
     "mitigation_doc": ".claude/docs/runbook/plugin-reinstall-path.md"},
    {"item": "~/.config/gh/hosts.yml", "class": "exception-3-credentials",
     "mitigation_doc": ".claude/docs/runbook/credential-reissuance-runbook.md"}
  ],
  "open": [
    {"item": "**/.claude/settings.local.json", "class": "exception-4-user-scope",
     "reason": "contributed by a global core.excludesFile, not this repo's own .gitignore"},
    {"item": "~/.claude/CLAUDE.md", "class": "exception-4-user-scope", "status": "exists"},
    {"item": "~/.claude/settings.json", "class": "exception-4-user-scope", "status": "exists"}
  ],
  "totals": {"defects": 0, "enrolled_with_mitigation": 2, "open": 3}
}
```

Zero defects on day one: `.claude/ops/` confirmed fully tracked (ADR-0022's own stated fact, not
just assumed), no uncategorized ignored-and-present paths, no stray `.env*` files, and both
owed-at-lock mitigation docs present in the same PR that ships the audit — a defect-free first
run because the mitigation docs shipped WITH the instrument, not because nothing was owed.
Exception 1 (memory dir) reported nothing for this specific run because the repo-root passed was
the scratch-clone path (a genuinely fresh checkout location has no accumulated memory yet, which
is the honest, correct answer for that literal path — not a script defect); a run against the
actual long-lived project checkout path would report this repo's real memory dir (30 files,
verified present during this build) as enrolled.

## Build manifest

| # | Path | Action |
|---|---|---|
| 1 | `harness/skills/check-reconstructibility/SKILL.md` | create |
| 2 | `harness/skills/check-reconstructibility/scripts/audit_reconstructibility.py` | create, selftest per Components |
| 3 | `harness/skills/check-reconstructibility/evals/evals.json` | create |
| 4 | `harness/skills/clean-git/evals/evals.json` | edit: reciprocal no-trigger fence |
| 5 | `authorkit/skills/repo-audit/evals/evals.json` | edit: reciprocal no-trigger fence |
| 6 | `.claude/docs/runbook/plugin-reinstall-path.md` | create |
| 7 | `.claude/docs/runbook/credential-reissuance-runbook.md` | create |
| 8 | `harness/README.md` + `harness/.claude-plugin/plugin.json` | edit: member row, ledger row, version bump (3.11.0 → 3.12.0) |
| 9 | `authorkit/README.md` + `authorkit/.claude-plugin/plugin.json` | edit: ledger row, version bump (0.20.0 → 0.21.0) |
| 10 | repo-root `naming.manifest.json` | edit: register `reconstructibility` in `object_vocab` |
| 11 | `.claude/docs/lld/lld-0014-reconstructibility-audit.md` | this document |

Explicitly NOT in this build: the ADR itself (already accepted, ADR-0022, this ticket only builds
its instrument + owed-at-lock docs); a retrofit of exception 4's exact mitigation mechanism
(ratification's own open question, unruled — Rejected alternatives); a fully narrated
incident-response credential-rotation runbook (the seed explicitly scopes this to a skeleton);
authorkit as the audit instrument's home (anti-matrix ruling above, harness wins).

## Acceptance (build gate — checkable predicates)

1. `python3 harness/skills/check-reconstructibility/scripts/audit_reconstructibility.py selftest` → exit 0.
2. `python3 harness/scripts/release_gate.py harness` → green (G4 selftest sweep, G7 eval-suite
   schema, G10 README/manifest version match, G12 naming grammar clean for the new skill name).
3. `python3 harness/scripts/release_gate.py authorkit` → green (evals-only edit, same gate suite).
4. `python3 authorkit/skills/naming-audit/scripts/validate.py --target harness --manifest
   naming.manifest.json --scope grammar --json` (repo root) → `grammar_errors` names no
   `check-reconstructibility` entry (confirmed clean during this build — zero mentions in the
   validator's own output at all, not even an exemption note).
5. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0014-reconstructibility-audit.md` → clean
   (no `doc-type` frontmatter issues; this LLD carries the standard ten-type frontmatter).
6. A real run (`--repo-root <this branch's own checkout> --json`) against the branch that ships
   both mitigation docs reports `defects: 0` for exceptions 2 and 3 specifically (mitigation-doc
   presence check) — proves the audit and its own owed docs land coherently in one PR, not a
   script that reports its own deliverable missing.
7. Fresh-context skill-checker pass on the new `SKILL.md` — verdict recorded in the build handback
   (semantic-edit invariant, `.claude/rules/plugin-authoring.md`).

## Risks

1. **The excludesFile implicit-default check is macOS/XDG-convention-specific** (assumes
   `~/.config/git/ignore` when `XDG_CONFIG_HOME` is unset, matching this repo's own verified
   case). Detection: a Linux box with `XDG_CONFIG_HOME` actually set to a non-default path would
   miss patterns living there. Fallback: `--config-home` is already a caller-supplied override for
   exactly this — a future run on a differently-configured machine passes the real
   `$XDG_CONFIG_HOME` explicitly; named here as a known scope edge, not silently assumed universal.
2. **Mitigation-doc-path coupling is a hardcoded constant** (Interfaces, above) — a rename of
   either runbook without updating the script produces a false defect. Detection: the audit's own
   next run. Fallback: this is accepted as a cheap, visible failure mode (a false defect is loud,
   never a false clean), not silently risked.
3. **Exception 1's memory-dir slug convention is inferred from one machine's observed layout, not
   documented anywhere authoritative.** Detection: a differently-configured Claude Code install
   using a different slug scheme would silently report `exists: false` for a memory dir that's
   actually there. Fallback: named as an assumption in the script's own docstring; a future
   platform-facts pack entry could ground this formally (Rejected alternatives — out of this
   ticket's scope to chase down a citation for a convention this build only needed to read, not
   author).
4. **Zero-defect first run could read as "nothing to find, why does this exist."** Detection: a
   reviewer skimming only the totals line. Fallback: the SKILL's own render step states the
   `enrolled`/`open` buckets by name every run, never just the defect count — a healthy sweep is
   evidence of a real check having run, not silence.

## Rejected alternatives

- **authorkit as the audit's home.** Rejected: different axis (estate governance vs. estate
  recovery), would blur the five-sibling family's single job; harness fits both by adjacency
  (`clean-git`/`repo-cleaner`) and by charter (workspace-generic toolchain). Ruling recorded in
  Components above, not a fork needing its own ADR.
- **Ruling exception 4's exact mitigation mechanism in this build.** Rejected: ADR-0022's own
  Open questions section leaves it explicitly unruled at ratification (open question 2); this
  ticket's own seed scopes the audit to REPORTING that gap, never resolving it. The audit's OPEN
  bucket is the honest artifact of that boundary.
- **A configurable mitigation-doc path (a `--reinstall-doc`/`--credential-doc` flag).** Rejected
  as unnecessary flexibility for a coupling this same PR both creates and controls (Interfaces,
  Risk 2) — added if a future rename campaign actually needs it, not speculatively now.
- **A fully narrated incident-response credential-rotation runbook** (rotation cadence,
  revocation-on-compromise steps, escalation contacts). Rejected: the seed explicitly names this
  a skeleton; a real re-issuance event would give a worked case to generalize from, which doesn't
  exist yet — inventing the narrative now risks getting the actual incident shape wrong.
- **Retrofitting `.claude/ops/`'s already-committed status as something this ticket needed to
  ACHIEVE rather than verify.** Rejected: ADR-0022's own text already states it as a checked
  fact ("verified on this branch"); this build's check 2 is a regression guard against that fact
  drifting, not new work to land it.
