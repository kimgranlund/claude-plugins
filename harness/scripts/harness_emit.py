#!/usr/bin/env python3
"""harness_emit — derive per-harness plugin overlays (Codex/Hermes/Pi) from each
plugin's Claude Code source of truth.

WHY THIS EXISTS (LLD-0025, gh#885/#886/#890)

Each plugin here is authored once, for Claude Code. Other agent harnesses (OpenAI Codex,
Hermes, Pi) read a DIFFERENT manifest shape. Rather than hand-author and hand-sync a second
manifest tree per harness, this script derives one **overlay** per target harness from the
SAME sources of truth `release_gate.py` already validates: `.claude-plugin/plugin.json`,
`skills/*/SKILL.md` frontmatter, the presence of `agents/`, `hooks/hooks.json`, `.mcp.json`,
and the root `.claude-plugin/marketplace.json`. The overlay is committed in-tree (never
`dist/` — `.claude/rules/dist-output.md`) and a freshness check (release_gate.py's G15) fails
the gate the moment a hand-edit or a stale overlay diverges from the recomputation.

This wave (W3, T-6, gh#891) adds the Pi backend, activating all three harnesses by default.
W4 (T-2, gh#887/#895) adds the Pi MCP passthrough note: Pi core has no MCP field, but the
third-party `pi-mcp-adapter` reads a project-local `.mcp.json` in the same shape Claude Code
uses, so a plugin's own `.mcp.json` already works with that adapter as-is once installed —
no glue is generated, only documented.

WHAT IT DERIVES (Codex)
  <plugin>/.codex-plugin/plugin.json
    name/version/description/author/license/homepage/keywords <- .claude-plugin/plugin.json
    skills      <- always "./skills/"
    mcpServers  <- "./.mcp.json" IFF the plugin ships one (values containing
                   ${CLAUDE_PLUGIN_ROOT} or ${user_config.*} are copied verbatim and flagged
                   [needs-substitution] in the plugin's HARNESS-NOTES.md)
    interface   <- <plugin>/codex.interface.json when present (hand-maintained, optional);
                   otherwise derived minimally (displayName from plugin.json's own
                   displayName or title-cased name; shortDescription = first sentence of
                   description)
  <plugin>/skills/<name>/agents/openai.yaml   (one per skill directory)
    interface.display_name      <- title-cased skill `name` frontmatter
    interface.short_description <- skill `description`, first sentence only
    interface.default_prompt    <- optional skill frontmatter key codex_default_prompt
    policy.allow_implicit_invocation <- false IFF the skill's own `disable-model-invocation:
                                   true` (issue #1008, author-cross-harness-plugins'
                                   surface-matrix.md invocation-policy mapping); omitted
                                   entirely for an ordinary skill, never emitted as `true`

WHAT IT DERIVES (Hermes)
  <plugin>/plugin.yaml
    name/version/description <- .claude-plugin/plugin.json; manifest_version: 1
  <plugin>/__init__.py
    register(ctx) — fixed template; one ctx.register_skill(<name>, <SKILL.md path>) line per
    skill directory, nothing else registered this wave (no hooks, no commands — R-5's Hermes
    verdict on #888 is terminal: ctx.register_command carries no invocation-source metadata,
    so a command-only skill degrades to a plain register_skill() line, same as Codex)
  <plugin>/hermes-mcp.yaml   (IFF the plugin ships .mcp.json)
    a config.yaml mcp_servers: fragment, mcpServers.<n> -> mcp_servers.<n>, command/args/env
    or url/headers copied 1:1; ${CLAUDE_PLUGIN_ROOT}/${user_config.*} values flagged
    [needs-substitution] (the user merges this fragment into ~/.hermes/config.yaml by hand —
    Hermes has no marketplace file, so install + config merge are both documented in
    HARNESS-NOTES.md rather than automated)

WHAT IT DERIVES (Pi)
  <plugin>/package.json
    name <- "@nonoun/<plugin>" (Resolution 4a scope); version verbatim; description;
    keywords <- ["pi-package", ...plugin.json keywords] ("pi-package" IS Pi's registry
    contract — the pi.dev gallery scrapes it, no separate marketplace file); pi.skills <-
    ["./skills"]; pi.prompts <- ["./prompts"] IFF the plugin has a command-only skill.
    A pre-existing package.json is merge-only: only the pi key + keywords entry are
    touched, every other key is left alone (Resolution 4, R-3).
  <plugin>/prompts/<skill-name>.md   (one per command-only skill; flat, non-recursive)
    frontmatter: description <- the skill's own description (or the body's first
    non-empty line); argument-hint <- the skill's own argument-hint frontmatter, if any.
    No `name` key — Pi derives the command name from the FILENAME. Body <- the SKILL.md
    body verbatim, $ARGUMENTS kept as-is (R-5 amendment, #888: this is how the human-only
    guard survives natively on Pi — a prompt template expands only from a human keystroke).
  MCP — passthrough, not derived (W4, T-2, #887/#895): `.mcp.json` (IFF the plugin ships one)
    is left exactly where it already is; nothing is written or copied for Pi. The plugin's
    HARNESS-NOTES.md documents the third-party `pi-mcp-adapter` caveat (install separately,
    not part of Pi core) and flags any `${CLAUDE_PLUGIN_ROOT}`/`${user_config.*}` value
    `[needs-substitution]`, same as the Codex/Hermes rows.

  <plugin>/HARNESS-NOTES.md   (one per plugin; every harness's degradation ledger)
  <workspace>/.agents/plugins/marketplace.json   (Codex only, estate-level; derived from the
    root .claude-plugin/marketplace.json 1:1)

NOT DERIVED this wave: a plugin's own agents/*.md and hooks/hooks.json have no manifest key
on any backend, and (on Hermes only, as of #1008 — Codex's own invocation-policy mapping is
now realized above) the disable-model-invocation flag, plus (on Codex/Hermes both) a skill's
`context` flag, have no further manifest key — they are dropped with a note (Resolution 3, the
degradation table) rather than guessed at. Pi's MCP cell is PASSTHROUGH, not generate-glue
(T-2, #887 amendment, W4/#895): the third-party pi-mcp-adapter reads a project-local
`.mcp.json` in the same `mcpServers` shape Claude Code uses, and that file already sits at the
plugin root where a Pi install places it — nothing for this backend to write or copy. The Pi
HARNESS-NOTES.md section documents the adapter's shape, the third-party-install caveat, and
flags any `${...}` substitution token exactly as Codex/Hermes already do; verified once against
the third-party adapter's own documented config contract (same filename, same `mcpServers`
key, same `${VAR}` interpolation) — no adapter source lives in this repo to check further than
that.

CROSS-HARNESS BODY-TOKEN INVENTORY (issue #1008, author-cross-harness-plugins'
surface-matrix.md rule 5 — degradation is recorded, not guessed at). A skill's SKILL.md BODY
(never its frontmatter — that's a harness's own manifest surface already handled above) can
carry a Claude-only substitution token — `${CLAUDE_PLUGIN_ROOT}` or `$ARGUMENTS` — that a
non-Claude harness reads verbatim as prose instead of expanding. `scan_claude_only_tokens()`
finds every occurrence, per skill, and both HARNESS-NOTES.md's own degradation-inventory
section and `release_gate.py`'s G15b WARN read off this SAME function — never two parallel
implementations. One exception: `$ARGUMENTS` inside a COMMAND-ONLY skill's body is not a
degradation on Pi specifically — Pi emits that skill as a native `prompts/<name>.md` prompt
template where `$ARGUMENTS` is the real, working substitution mechanism (R-5 amendment, #888),
not Claude-only prose. Every other combination (an ordinary skill's `$ARGUMENTS`, any skill's
`${CLAUDE_PLUGIN_ROOT}`, or `$ARGUMENTS` on Codex/Hermes regardless of command status) degrades
on every harness actually built this run.

WRITE / VERIFY / PROBE / SCAN
  harness_emit.py <plugin-root> [--harness codex,hermes,pi]              # write
  harness_emit.py <plugin-root> --verify [--harness codex,hermes,pi]     # gate: exit 1 on drift
  harness_emit.py <plugin-root> --probe [--harness codex,hermes,pi]      # tri-state harness load
  harness_emit.py <plugin-root> --scan-tokens [--harness codex,hermes,pi]  # info only, exit 0
                                                                           # always: list skills
                                                                           # whose bodies carry a
                                                                           # Claude-only token
                                                                           # (release_gate.py's
                                                                           # G15b sources its WARN
                                                                           # from this, never a
                                                                           # second scan)
  harness_emit.py selftest                                               # prove the gate bites

PROBE, established per CLI (Resolution 6 tier 2): Codex has no verified validator
subcommand -> SKIP always, tier-3-only. Hermes: `hermes plugins doctor` is NOT a real
subcommand on this CLI (checked via --help) -> the fallback is a temp-HOME copy into
~/.hermes/plugins/<name>/ (hermes_cli/plugins.py's own documented user-plugin path) plus
`hermes plugins list --json`; this proves plugin.yaml parses and the plugin is discoverable,
but does NOT execute register(ctx) — a partial tier-2 close, not a full load assert. Pi: no
`pi doctor`/`pi check` subcommand either (checked via `pi --help`) -> the fallback is `pi
install <plugin-root> -l` (project-local, cwd'd into a throwaway scratch dir — never the
plugin root itself) then `pi list`; verified LIVE that a local install is listed by its
resolved install PATH under a `Project packages:` heading, not by the package.json `name`
field (a local install carries no registry identity) -> the check matches the path.

No args (or a bare path with neither --verify/--probe and no write intent unclear) -> this
docstring, exit 2.

Verdict line first: `harness_emit · <root> · CLEAN|STALE|ERROR · n target(s)`, then one line
per finding.

Exit: 0 clean/written · 1 drift found (--verify) · 2 setup error (unreadable manifest, or an
unimplemented harness named explicitly via --harness). --scan-tokens is informational only —
0 (findings printed, if any) or 2 (setup error) — it never exits 1; it is not a freshness gate.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_lint  # parse_frontmatter — the only frontmatter reader this script trusts (R-2)

DEFAULT_HARNESSES = ["codex", "hermes", "pi"]  # W1 codex, W2 +hermes, W3 (T-6, #891) +pi
ALL_HARNESSES = ["codex", "hermes", "pi"]


# ---------------------------------------------------------------------------
# Source read (Resolution 2)
# ---------------------------------------------------------------------------

class SourceError(Exception):
    pass


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise SourceError(f"{p}: {e}")


def read_plugin(root: Path):
    """Reads a plugin directory into the internal Source shape (Interfaces). Refuses to
    invent a missing name/version/description (exit 1 upstream in the caller)."""
    mf = root / ".claude-plugin" / "plugin.json"
    if not mf.is_file():
        raise SourceError(f"missing {mf} -> the manifest is the plugin, nothing to derive from")
    pj = _read_json(mf)
    name, version, description = pj.get("name"), pj.get("version"), pj.get("description")
    if not name or not version or not description:
        raise SourceError(
            f"{mf}: missing name/version/description -> the emitter never invents one "
            "(release_gate.py's G1 already requires them)"
        )

    skills = []
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if not d.is_dir():
                continue
            sm = d / "SKILL.md"
            if not sm.is_file():
                continue
            lines = sm.read_text(encoding="utf-8").splitlines()
            fields, fm_span = skill_lint.parse_frontmatter(lines)
            if "name" not in fields or "description" not in fields:
                raise SourceError(f"{sm}: missing name/description in frontmatter")
            s_name = fields["name"][0]
            s_desc = fields["description"][0]
            # Cross-harness adapter-tree convention (author-cross-harness-plugins, gh adia-
            # harness#35, #1008's own sibling gap): Claude-only invocation fields
            # (disable-model-invocation, context: fork, argument-hint) may live on
            # adapters/claude/skills/<name>/SKILL.md instead of this shared root file — the
            # architecture doc requires the shared root to carry only the portable core.
            # name/description/body stay root-sourced (the portable, shared content); read
            # the invocation-control fields from the adapter when one exists, falling back to
            # the root's own frontmatter for a skill with no adapter (unchanged behavior).
            invocation_fields = fields
            adapter_sm = root / "adapters" / "claude" / "skills" / d.name / "SKILL.md"
            if adapter_sm.is_file():
                adapter_lines = adapter_sm.read_text(encoding="utf-8").splitlines()
                adapter_fields, _ = skill_lint.parse_frontmatter(adapter_lines)
                invocation_fields = adapter_fields
            command = invocation_fields.get("disable-model-invocation", ("false", 0))[0].strip().lower() == "true"
            fork = invocation_fields.get("context", ("", 0))[0].strip().lower() == "fork"
            codex_default_prompt = fields.get("codex_default_prompt", (None, 0))[0]
            argument_hint = invocation_fields.get("argument-hint", (None, 0))[0]
            # fm_span is guaranteed here — the fields check above already raised SourceError
            # for any SKILL.md whose frontmatter didn't parse (fm_span is None only then).
            body = "\n".join(lines[fm_span[1] + 1:]).strip("\n")
            skills.append({
                "name": s_name,
                "description": s_desc,
                "command": command,
                "fork": fork,
                "dir": d,
                "codex_default_prompt": codex_default_prompt,
                "argument_hint": argument_hint,
                "body": body,
            })

    agents = []
    agents_dir = root / "agents"
    if agents_dir.is_dir():
        for f in sorted(agents_dir.glob("*.md")):
            agents.append(f.stem)

    hooks = []
    hooks_file = root / "hooks" / "hooks.json"
    if hooks_file.is_file():
        try:
            hj = _read_json(hooks_file)
            hooks = sorted(hj.keys()) if isinstance(hj, dict) else []
        except SourceError:
            hooks = ["<unparseable hooks.json>"]

    mcp = None
    mcp_file = root / ".mcp.json"
    if mcp_file.is_file():
        mj = _read_json(mcp_file)
        mcp = mj.get("mcpServers", {}) if isinstance(mj, dict) else {}

    codex_interface = None
    iface_file = root / "codex.interface.json"
    if iface_file.is_file():
        codex_interface = _read_json(iface_file)

    # A pre-existing package.json (Pi backend, Resolution 4: merge-only — the emitter never
    # clobbers a hand-authored key beyond its own "pi" + "keywords"). Read here, not by the
    # backend, so every backend stays filesystem-free per the Interfaces contract ("none
    # touches the filesystem directly"). Unparseable -> SourceError, same discipline as every
    # other source read in this file; the emitter never silently discards a file it can't read.
    existing_package_json = None
    pkg_file = root / "package.json"
    if pkg_file.is_file():
        existing_package_json = _read_json(pkg_file)
        if not isinstance(existing_package_json, dict):
            raise SourceError(f"{pkg_file}: not a JSON object -> the emitter never clobbers a package.json it can't merge into")

    return {
        "name": name,
        "version": version,
        "description": description,
        "author": pj.get("author"),
        "license": pj.get("license"),
        "homepage": pj.get("homepage"),
        "keywords": pj.get("keywords", []),
        "display_name": pj.get("displayName"),
        "user_config": "userConfig" in pj,
        "skills": skills,
        "agents": agents,
        "hooks": hooks,
        "existing_package_json": existing_package_json,
        "mcp": mcp,
        "codex_interface": codex_interface,
    }


# ---------------------------------------------------------------------------
# Shared render helpers
# ---------------------------------------------------------------------------

NEEDS_SUBSTITUTION_RE = re.compile(r"\$\{(CLAUDE_PLUGIN_ROOT|user_config\.[^}]*)\}")


def first_sentence(description: str) -> str:
    m = re.match(r"^(.*?[.!?])(\s|$)", description.strip())
    return (m.group(1) if m else description.strip()).strip()


def title_case(kebab_name: str) -> str:
    return " ".join(w.capitalize() for w in kebab_name.split("-"))


def yaml_scalar(v) -> str:
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def py_str_literal(v) -> str:
    """A safely-quoted Python string literal for names embedded in generated .py source
    (the Hermes __init__.py) — repr() handles quoting/escaping generically rather than
    trusting names to stay free of quotes/backslashes (harness_emit.py's only generated-code
    surface; every other emitted artifact is JSON/YAML, already escaped via json.dumps/
    yaml_scalar)."""
    return repr(str(v))


def mcp_needs_substitution(mcp: dict):
    """[(server_name, field_path), ...] for any MCP value carrying a Claude-runtime
    substitution token neither Codex nor Hermes knows how to resolve."""
    flagged = []
    if not mcp:
        return flagged
    for server_name, cfg in mcp.items():
        if not isinstance(cfg, dict):
            continue
        for field in ("command", "url"):
            v = cfg.get(field)
            if isinstance(v, str) and NEEDS_SUBSTITUTION_RE.search(v):
                flagged.append((server_name, field))
        for i, a in enumerate(cfg.get("args", []) or []):
            if isinstance(a, str) and NEEDS_SUBSTITUTION_RE.search(a):
                flagged.append((server_name, f"args[{i}]"))
        for k, v in (cfg.get("env", {}) or {}).items():
            if isinstance(v, str) and NEEDS_SUBSTITUTION_RE.search(v):
                flagged.append((server_name, f"env.{k}"))
        for k, v in (cfg.get("headers", {}) or {}).items():
            if isinstance(v, str) and NEEDS_SUBSTITUTION_RE.search(v):
                flagged.append((server_name, f"headers.{k}"))
    return flagged


CLAUDE_ONLY_BODY_TOKEN_RE = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}|\$ARGUMENTS\b")


def scan_claude_only_tokens(source, harnesses=DEFAULT_HARNESSES):
    """[(skill_name, [(token, [affected_harness, ...]), ...]), ...] for every skill whose
    SKILL.md BODY (never frontmatter — a frontmatter field is a harness's own manifest
    surface, already handled by each backend above) carries a Claude-only substitution
    token. Sorted by skill name, then token, so both HARNESS-NOTES.md's rendering and
    release_gate.py's G15b get a deterministic order across reruns (G15's own freshness
    diff depends on it).

    One exception to "every built harness is affected": `$ARGUMENTS` inside a COMMAND-ONLY
    skill's body is NOT a degradation on Pi — Pi emits that skill as a native
    `prompts/<name>.md` prompt template where `$ARGUMENTS` is the real, working
    substitution mechanism (R-5 amendment, #888), not Claude-only prose read verbatim.
    Every other combination — `${CLAUDE_PLUGIN_ROOT}` on any skill, or `$ARGUMENTS` on an
    ordinary (non-command) skill, or `$ARGUMENTS` on Codex/Hermes regardless of command
    status — degrades on every harness this run actually builds; Codex/Hermes have no
    argument- or path-substitution channel of their own."""
    found = []
    for s in sorted(source["skills"], key=lambda sk: sk["name"]):
        tokens = sorted(set(CLAUDE_ONLY_BODY_TOKEN_RE.findall(s["body"])))
        if not tokens:
            continue
        per_token = []
        for tok in tokens:
            affected = [h for h in harnesses]
            if tok == "$ARGUMENTS" and s["command"] and "pi" in affected:
                affected = [h for h in affected if h != "pi"]
            per_token.append((tok, affected))
        found.append((s["name"], per_token))
    return found


# ---------------------------------------------------------------------------
# Ledger — the degradation record, rendered into HARNESS-NOTES.md
# ---------------------------------------------------------------------------

class Ledger:
    def __init__(self, source, built=("codex",)):
        self.source = source
        self.built = set(built)
        self.dropped_agents = list(source["agents"])
        self.dropped_hooks = list(source["hooks"])
        self.command_skills = [s["name"] for s in source["skills"] if s["command"]]
        self.fork_skills = [s["name"] for s in source["skills"] if s["fork"]]
        self.mcp_flags = mcp_needs_substitution(source["mcp"]) if source["mcp"] else []
        self.claude_only_tokens = scan_claude_only_tokens(source, harnesses=sorted(self.built))

    def render(self) -> str:
        s = self.source
        lines = [f"# {s['name']} {s['version']} — harness overlay notes "
                 "(generated by harness_emit.py; do not edit)", ""]

        def _list(items):
            return ", ".join(f"`{i}`" for i in items) if items else "none"

        lines += ["## Cross-harness token degradations"]
        if self.claude_only_tokens:
            for skill_name, per_token in self.claude_only_tokens:
                for tok, affected in per_token:
                    kind = "path" if tok == "${CLAUDE_PLUGIN_ROOT}" else "argument"
                    note = f"{kind} token is Claude-only; non-Claude harnesses read it verbatim."
                    if tok == "$ARGUMENTS" and "pi" not in affected:
                        note += (
                            " (Pi excluded: its own `prompts/" + skill_name + ".md` "
                            "substitutes this natively for this command-only skill.)"
                        )
                    affects = ", ".join(affected) if affected else "none this run"
                    lines.append(f"- `{skill_name}` body — `{tok}`: affects {affects} — {note}")
        else:
            lines.append("- none.")
        lines.append("")

        lines += [
            "## Codex",
            "- Loads via `.codex-plugin/plugin.json`; enable with the "
            "`[marketplaces.nonoun-plugins]` + "
            f'`[plugins."{s["name"]}@nonoun-plugins"]` entries in `~/.codex/config.toml`.',
        ]
        if self.mcp_flags:
            flags = ", ".join(f"`{n}.{f}`" for n, f in self.mcp_flags)
            lines.append(
                f"- MCP `[needs-substitution]`: {flags} use Claude-runtime tokens "
                "(`${CLAUDE_PLUGIN_ROOT}`, `${user_config.*}`) that Codex cannot resolve — "
                "replace each with a literal value in `.mcp.json` before enabling this plugin "
                "in Codex (the tokens are flagged here, not rewritten in `.mcp.json` itself)."
            )
        lines += [
            f"- Dropped — agents: {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
            "- Command-only skills — human-only timing preserved via each skill's own "
            f"`agents/openai.yaml` `policy.allow_implicit_invocation: false` (#1008): "
            f"{_list(self.command_skills)}.",
            f"- Fork skills (their `context` field drops; body runs inline): {_list(self.fork_skills)}.",
        ]
        if self.mcp_flags:
            lines.append(f"- MCP: `./.mcp.json` pointed at ({len(self.mcp_flags)} value(s) flagged above).")
        elif s["mcp"] is not None:
            lines.append("- MCP: `./.mcp.json` pointed at; no substitution tokens found.")
        else:
            lines.append("- MCP: none shipped.")
        lines.append("")

        if "hermes" in self.built:
            lines += [
                "## Hermes",
                "- Loads from a plugin directory carrying `plugin.yaml` + `__init__.py`. Two "
                f'verified paths (hermes_cli/plugins.py): local dev — copy this directory to '
                f'`~/.hermes/plugins/{s["name"]}/` (user plugin) or `./.hermes/plugins/'
                f'{s["name"]}/` with `HERMES_ENABLE_PROJECT_PLUGINS=1` (project plugin, opt-in) '
                f'— then `hermes plugins list` should show it; from a Git host — '
                f'`hermes plugins install owner/repo`, then `hermes plugins enable {s["name"]}` '
                '(or pass `--enable` to `install`) to activate it — install alone does not '
                "enable a plugin. Hermes has no marketplace file, so there is no registry "
                "listing step beyond the two paths above.",
                "- Plugin skills are NOT surfaced in `<available_skills>` (hermes_cli/"
                "plugins.py:3334-3337) — they resolve only as an explicit "
                f"`<plugin>:<skill>` load. Verify with a load, e.g. `load "
                f'{s["name"]}:{s["skills"][0]["name"] if s["skills"] else "<skill>"}`'
                ", never with \"list your skills\".",
            ]
            if self.mcp_flags:
                flags = ", ".join(f"`{n}.{f}`" for n, f in self.mcp_flags)
                lines.append(
                    f"- MCP `[needs-substitution]`: {flags} use Claude-runtime tokens that "
                    "Hermes cannot resolve — replace each with a literal value before merging "
                    "`hermes-mcp.yaml` into your config."
                )
            if s["mcp"] is not None:
                lines.append(
                    "- MCP: `hermes-mcp.yaml` generated from `.mcp.json` — first check whether "
                    "`~/.hermes/config.yaml` already has a top-level `mcp_servers:` key; if it "
                    "does NOT, `cat hermes-mcp.yaml >> ~/.hermes/config.yaml` is safe; if it "
                    "DOES, merge the two `mcp_servers:` blocks by hand instead — a blind append "
                    "onto an existing `mcp_servers:` key produces a duplicate top-level YAML "
                    "key, and most parsers silently keep only the last one, dropping your "
                    "existing servers with no error."
                )
            else:
                lines.append("- MCP: none shipped.")
            lines += [
                f"- Dropped — agents: {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
                f"- Command-only skills now model-routable: {_list(self.command_skills)} "
                "(R-5, #888: `ctx.register_command` carries no invocation-source metadata on "
                "Hermes — the plain-skill degradation is the CORRECT terminal fallback here, "
                "not a temporary gap).",
                f"- Fork skills (their `context` field drops; body runs inline): {_list(self.fork_skills)}.",
                "",
            ]
        else:
            lines += [
                "## Hermes",
                "- This backend isn't built yet (tracked as T-5; no install path exists for "
                "Hermes from this repo today) — no action needed here. What WOULD drop under "
                "this plugin's current Claude Code source, computed the same way Codex's row "
                "above is (kept for a preview, not yet verified against Hermes's own contract): "
                f"agents — {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
                "",
            ]

        if "pi" in self.built:
            lines += [
                "## Pi",
                f'- Loads via `package.json`\'s `"pi"` key (`"skills": ["./skills"]`); install '
                f'with `pi install <path-to-{s["name"]}> -l` from a checkout — confirm with '
                f'`pi list`, which shows the install path under `Project packages:`. The '
                f'`"pi-package"` keyword is added automatically (no extra step); once this '
                f'package is published, that keyword is what the pi.dev gallery scrapes to '
                f'list it — there is no separate marketplace file to maintain.',
                f"- Dropped — agents: {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
            ]
            if self.command_skills:
                lines.append(
                    f"- Command-only skills emitted as `prompts/{{name}}.md` templates "
                    f"(R-5 amendment, #888): {_list(self.command_skills)} — the human-only guard "
                    "is preserved natively (a prompt template expands only from a human keystroke; "
                    "the model has no channel to self-invoke it), unlike Codex/Hermes where these "
                    "become plain, model-routable skills."
                )
            else:
                lines.append("- Command-only skills: none.")
            lines.append(
                f"- Fork skills (their `context` field drops; body runs inline): {_list(self.fork_skills)}."
            )
            if self.source["mcp"] is not None:
                lines.append(
                    "- MCP: `./.mcp.json` passthrough (W4, T-2, #887/#895) — Pi core has no MCP "
                    "field; install the third-party `pi-mcp-adapter` separately (it is NOT part "
                    "of Pi core) and it reads this plugin's existing `.mcp.json` as-is, same "
                    "filename and `mcpServers` shape Claude Code uses. Nothing is generated for "
                    "Pi — the file already sits at the plugin root, where a `pi install` places "
                    "it."
                )
                if self.mcp_flags:
                    flags = ", ".join(f"`{n}.{f}`" for n, f in self.mcp_flags)
                    lines.append(
                        f"- MCP `[needs-substitution]`: {flags} use Claude-runtime tokens that "
                        "the pi-mcp-adapter cannot resolve — replace each with a literal value "
                        "in `.mcp.json` before installing this plugin's MCP server under Pi."
                    )
            else:
                lines.append("- MCP: none shipped.")
            lines.append("")
        else:
            lines += [
                "## Pi",
                "- Excluded from this run (`--harness` didn't include `pi`) — the Pi backend "
                "IS built (LLD-0025 W3, #891); rerun with `pi` in the `--harness` set, or omit "
                "`--harness` entirely (its default already includes `pi`), to render this "
                "section for real. What WOULD drop under this plugin's current Claude Code "
                "source, computed the same way Codex's row above is: "
                f"agents — {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
                "",
            ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Codex backend
# ---------------------------------------------------------------------------

class CodexBackend:
    name = "codex"

    def targets(self, source, root: Path):
        out = []
        pj = {
            "name": source["name"],
            "version": source["version"],
            "description": source["description"],
        }
        if source["author"] is not None:
            pj["author"] = source["author"]
        if source["license"] is not None:
            pj["license"] = source["license"]
        if source["homepage"] is not None:
            pj["homepage"] = source["homepage"]
        if source["keywords"]:
            pj["keywords"] = source["keywords"]
        pj["skills"] = "./skills/"
        if source["mcp"] is not None:
            pj["mcpServers"] = "./.mcp.json"

        if source["codex_interface"] is not None:
            pj["interface"] = source["codex_interface"]
        else:
            display_name = source["display_name"] or title_case(source["name"])
            pj["interface"] = {
                "displayName": display_name,
                "shortDescription": first_sentence(source["description"]),
            }

        content = json.dumps(pj, indent=2) + "\n"
        out.append((root / ".codex-plugin" / "plugin.json", content.encode("utf-8")))

        for s in source["skills"]:
            lines = [
                "interface:",
                f"  display_name: {yaml_scalar(title_case(s['name']))}",
                f"  short_description: {yaml_scalar(first_sentence(s['description']))}",
            ]
            if s["codex_default_prompt"]:
                lines.append(f"  default_prompt: {yaml_scalar(s['codex_default_prompt'])}")
            if s["command"]:
                # Invocation-policy mapping (issue #1008, author-cross-harness-plugins'
                # surface-matrix.md): Claude's disable-model-invocation: true has no direct
                # Codex manifest key of its own short of this — policy.allow_implicit_invocation:
                # false is the verified equivalent, so a command-only skill's human-only
                # timing survives on Codex instead of silently degrading to model-routable.
                lines += ["policy:", "  allow_implicit_invocation: false"]
            yaml_content = "\n".join(lines) + "\n"
            out.append((s["dir"] / "agents" / "openai.yaml", yaml_content.encode("utf-8")))

        return out

    def probe_hint(self):
        return "codex", ["--help"]


HERMES_INIT_HEADER = (
    '"""{name} — generated by harness_emit.py from .claude-plugin/plugin.json. '
    'Do not edit."""\n'
    "from pathlib import Path\n"
    "\n"
    "_HERE = Path(__file__).resolve().parent\n"
    "\n"
    "def register(ctx):\n"
)

HERMES_DESCRIPTION_MAX = 500  # sane truncation for progressive-disclosure metadata


class HermesBackend:
    name = "hermes"

    def targets(self, source, root: Path):
        out = []

        # plugin.yaml — manifest_version: 1; v2 fields (config_schema) are unverified,
        # never emitted (LLD-0025 Resolution 4).
        yaml_lines = [
            f"name: {yaml_scalar(source['name'])}",
            f"version: {yaml_scalar(source['version'])}",
            f"description: {yaml_scalar(source['description'])}",
            "manifest_version: 1",
        ]
        content = "\n".join(yaml_lines) + "\n"
        out.append((root / "plugin.yaml", content.encode("utf-8")))

        # __init__.py — fixed template; one ctx.register_skill() line per skill, nothing
        # else registered this wave (Resolution 3: no hooks, no commands — R-5's Hermes
        # verdict on #888 is terminal).
        body = HERMES_INIT_HEADER.format(name=source["name"])
        if source["skills"]:
            reg_lines = []
            for s in source["skills"]:
                skill_lit = py_str_literal(s["name"])
                skill_path = f'_HERE / "skills" / {skill_lit} / "SKILL.md"'
                desc = (s["description"] or "").strip()
                if len(desc) > HERMES_DESCRIPTION_MAX:
                    desc = desc[: HERMES_DESCRIPTION_MAX - 1].rstrip() + "…"
                desc_lit = py_str_literal(desc)
                reg_lines.append(
                    f'    ctx.register_skill({skill_lit}, {skill_path}, '
                    f'description={desc_lit})  # one per skill'
                )
            body += "\n".join(reg_lines) + "\n"
        else:
            body += "    pass  # no skills to register\n"
        out.append((root / "__init__.py", body.encode("utf-8")))

        # hermes-mcp.yaml — IFF the plugin ships .mcp.json. A config.yaml mcp_servers:
        # fragment; ${CLAUDE_PLUGIN_ROOT}/${user_config.*} values are copied verbatim and
        # flagged [needs-substitution] in HARNESS-NOTES.md, not rewritten here.
        if source["mcp"] is not None:
            frag_lines = ["mcp_servers:"]
            for server_name, cfg in sorted(source["mcp"].items()):
                if not isinstance(cfg, dict):
                    continue
                frag_lines.append(f"  {server_name}:")
                if "command" in cfg:
                    frag_lines.append(f"    command: {yaml_scalar(cfg['command'])}")
                if "args" in cfg and cfg["args"]:
                    frag_lines.append("    args:")
                    for a in cfg["args"]:
                        frag_lines.append(f"      - {yaml_scalar(a)}")
                if "url" in cfg:
                    frag_lines.append(f"    url: {yaml_scalar(cfg['url'])}")
                if "headers" in cfg and cfg["headers"]:
                    frag_lines.append("    headers:")
                    for k, v in cfg["headers"].items():
                        frag_lines.append(f"      {k}: {yaml_scalar(v)}")
                if "env" in cfg and cfg["env"]:
                    frag_lines.append("    env:")
                    for k, v in cfg["env"].items():
                        frag_lines.append(f"      {k}: {yaml_scalar(v)}")
            mcp_content = "\n".join(frag_lines) + "\n"
            out.append((root / "hermes-mcp.yaml", mcp_content.encode("utf-8")))

        return out

    def probe_hint(self):
        return "hermes", ["plugins", "doctor"]


PI_SCOPE = "@nonoun"  # Resolution 4a — reuses the marketplace's own nonoun-plugins identity


def _prompt_first_line(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return ""


class PiBackend:
    name = "pi"

    def targets(self, source, root: Path):
        out = []
        command_skills = [s for s in source["skills"] if s["command"]]

        # package.json — merge-only when one already exists (Resolution 4: no plugin here
        # has one today, R-3): on a pre-existing file, ONLY the "pi" key and the "keywords"
        # entry are touched — name/version/description/every other key are left exactly as
        # a human wrote them. A fresh file gets the full derived identity block. Reading the
        # existing file happens in read_plugin() (Source), never here — this backend stays
        # filesystem-free like every other one (Interfaces: "none touches the filesystem
        # directly").
        existing = source["existing_package_json"]
        keywords = list(dict.fromkeys(["pi-package", *source["keywords"]]))
        pi_section = {"skills": ["./skills"]}
        if command_skills:
            pi_section["prompts"] = ["./prompts"]
        if existing is not None:
            pkg = dict(existing)
            pkg["keywords"] = keywords
            pkg["pi"] = pi_section
        else:
            pkg = {
                "name": f"{PI_SCOPE}/{source['name']}",
                "version": source["version"],
                "description": source["description"],
                "private": True,
                "keywords": keywords,
                "pi": pi_section,
            }
        content = json.dumps(pkg, indent=2) + "\n"
        out.append((root / "package.json", content.encode("utf-8")))

        # prompts/<skill-name>.md — command-only skills, flat dir, non-recursive discovery
        # (R-5 amendment, #888: the human-only guard is preservable natively on Pi — a
        # prompts/ template loads only via a human keystroke, never model-invoked). No
        # `name:` frontmatter key emitted — Pi resolves the command name from the file's own
        # basename, not frontmatter (docs/prompt-templates.md).
        for s in command_skills:
            fm_lines = []
            description = s["description"] or _prompt_first_line(s["body"])
            if description:
                fm_lines.append(f"description: {yaml_scalar(description)}")
            if s["argument_hint"]:
                fm_lines.append(f"argument-hint: {yaml_scalar(s['argument_hint'])}")
            body_text = s["body"].rstrip("\n") + "\n"
            if fm_lines:
                content = "---\n" + "\n".join(fm_lines) + "\n---\n\n" + body_text
            else:
                content = body_text
            out.append((root / "prompts" / f"{s['name']}.md", content.encode("utf-8")))

        return out

    def probe_hint(self):
        return "pi", ["--help"]


BACKENDS = {"codex": CodexBackend, "hermes": HermesBackend, "pi": PiBackend}


# ---------------------------------------------------------------------------
# HARNESS-NOTES.md and estate marketplace are cross-backend, computed once
# ---------------------------------------------------------------------------

def notes_target(source, root: Path, harnesses=("codex",)):
    ledger = Ledger(source, built=harnesses)
    return root / "HARNESS-NOTES.md", ledger.render().encode("utf-8")


def estate_marketplace_target(workspace_root: Path):
    """Codex-only, estate-level. Derived from the root marketplace.json 1:1. Returns None
    when no root marketplace.json exists (not applicable, not an error)."""
    mf = workspace_root / ".claude-plugin" / "marketplace.json"
    if not mf.is_file():
        return None
    mj = _read_json(mf)
    out = {
        "name": mj.get("name", "marketplace"),
        "plugins": [
            {
                "name": p["name"],
                "source": {"source": "local", "path": f"./{p['name']}"},
                "description": p.get("description", ""),
            }
            for p in mj.get("plugins", [])
        ],
    }
    content = json.dumps(out, indent=2) + "\n"
    return workspace_root / ".agents" / "plugins" / "marketplace.json", content.encode("utf-8")


# ---------------------------------------------------------------------------
# run / verify / write
# ---------------------------------------------------------------------------

def compute_targets(root: Path, harnesses):
    """Returns (targets: [(Path, bytes)], errors: [str]). A NotImplementedError from a
    backend named explicitly via --harness is a setup error, not a silent skip."""
    source = read_plugin(root)
    targets = []
    for h in harnesses:
        backend = BACKENDS[h]()
        targets += backend.targets(source, root)
    targets.append(notes_target(source, root, harnesses=harnesses))
    return targets, source


def _find_orphans(root: Path, harnesses, live_targets):
    """unexpected: an overlay file whose source primitive no longer exists (a deleted
    skill's orphaned openai.yaml). Scoped to files this run's harness set would have
    produced a sibling for."""
    live_paths = {p for p, _ in live_targets}
    orphans = []
    if "codex" in harnesses:
        skills_dir = root / "skills"
        if skills_dir.is_dir():
            for f in skills_dir.glob("*/agents/openai.yaml"):
                if f not in live_paths:
                    orphans.append(f)
    if "hermes" in harnesses:
        mcp_yaml = root / "hermes-mcp.yaml"
        if mcp_yaml.is_file() and mcp_yaml not in live_paths:
            orphans.append(mcp_yaml)
    if "pi" in harnesses:
        prompts_dir = root / "prompts"
        if prompts_dir.is_dir():
            for f in prompts_dir.glob("*.md"):
                if f not in live_paths:
                    orphans.append(f)
    return orphans


def run(root: Path, harnesses=None, verify=False, workspace_root: Path = None):
    """Returns (code, findings: [str], targets: [(Path, bytes)])."""
    harnesses = harnesses or DEFAULT_HARNESSES
    unknown = [h for h in harnesses if h not in BACKENDS]
    if unknown:
        return 2, [f"unknown harness(es): {', '.join(unknown)} -> {', '.join(BACKENDS)}"], []

    try:
        targets, source = compute_targets(root, harnesses)
    except SourceError as e:
        return 2, [str(e)], []
    except NotImplementedError as e:
        return 2, [str(e)], []

    findings = []
    if verify:
        for path, content in targets:
            if not path.is_file() or path.read_bytes() != content:
                findings.append(f"stale: {path}")
        for orphan in _find_orphans(root, harnesses, targets):
            findings.append(f"unexpected: {orphan}")
    else:
        for path, content in targets:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        for orphan in _find_orphans(root, harnesses, targets):
            orphan.unlink()
            findings.append(f"removed unexpected: {orphan}")

    # workspace-root marketplace check — Codex only, once per run
    if "codex" in harnesses:
        ws = workspace_root or _infer_workspace_root(root)
        if ws is not None:
            mkt = estate_marketplace_target(ws)
            if mkt is not None:
                path, content = mkt
                if verify:
                    if not path.is_file() or path.read_bytes() != content:
                        findings.append(f"stale: {path}")
                    else:
                        claude_mf = ws / ".claude-plugin" / "marketplace.json"
                        cj = _read_json(claude_mf)
                        codex_j = _read_json(path)
                        claude_names = {p["name"] for p in cj.get("plugins", [])}
                        codex_names = {p["name"] for p in codex_j.get("plugins", [])}
                        if claude_names != codex_names:
                            findings.append(
                                f"marketplace-mismatch: {claude_names ^ codex_names}"
                            )
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)

    return (1 if findings else 0), findings, targets


def _infer_workspace_root(plugin_root: Path):
    """The plugin root's parent, when it carries the workspace-root marketplace.json —
    this workspace's own convention (one plugin dir per top-level directory)."""
    parent = plugin_root.resolve().parent
    if (parent / ".claude-plugin" / "marketplace.json").is_file():
        return parent
    return None


# ---------------------------------------------------------------------------
# --probe (Resolution 6, tier 2)
# ---------------------------------------------------------------------------

def _probe_hermes(exe: str, root: Path):
    """Copies root/plugin.yaml + root/__init__.py into a throwaway HOME's
    ~/.hermes/plugins/<name>/ and runs `hermes plugins list --json --no-bundled` against it.
    0 the plugin is discoverable and its manifest fields parse; 1 the CLI rejected it or the
    name is missing from the listing; 2 SKIP (setup problem, e.g. no plugin.yaml written yet).
    Partial tier-2 close only — this does not execute register(ctx), so it never proves the
    skill-registration calls themselves load; that needs a real session (tier 3)."""
    plugin_yaml = root / "plugin.yaml"
    init_py = root / "__init__.py"
    if not plugin_yaml.is_file() or not init_py.is_file():
        return 2, "SKIP — plugin.yaml/__init__.py not written yet; run the writer first"
    with tempfile.TemporaryDirectory() as td:
        fake_home = Path(td)
        try:
            name = re.search(r'^name:\s*"?([^"\n]+)"?', plugin_yaml.read_text()).group(1)
        except AttributeError:
            return 2, "SKIP — plugin.yaml has no parseable name: field"
        plugin_dir = fake_home / ".hermes" / "plugins" / name
        plugin_dir.mkdir(parents=True)
        shutil.copy2(plugin_yaml, plugin_dir / "plugin.yaml")
        shutil.copy2(init_py, plugin_dir / "__init__.py")
        try:
            r = subprocess.run(
                [exe, "plugins", "list", "--json", "--no-bundled"],
                capture_output=True, text=True, timeout=30,
                env={"HOME": str(fake_home), "PATH": os.environ.get("PATH", "")},
            )
        except (OSError, subprocess.SubprocessError) as e:
            return 2, f"SKIP — `hermes plugins list` failed to run: {e}"
        if r.returncode != 0:
            return 1, f"REJECTED — `hermes plugins list` exit {r.returncode}: {(r.stdout + r.stderr).strip()[-300:]}"
        try:
            listed = json.loads(r.stdout)
        except json.JSONDecodeError:
            return 1, f"REJECTED — `hermes plugins list --json` produced unparseable output: {r.stdout[-300:]}"
        names = [p.get("name") for p in listed] if isinstance(listed, list) else []
        if name not in names:
            return 1, f"REJECTED — plugin '{name}' not discovered by hermes (listed: {names})"
        return (0, f"loaded — hermes discovers '{name}' via ~/.hermes/plugins/ (list: {listed}); "
                   "partial tier-2 only, register(ctx) not executed (needs a real session, tier 3)")


def _probe_pi(exe: str, root: Path):
    """Established per `pi --help`/`pi install --help`/a live `pi list` run (Resolution 6 tier
    2, 2026-08-23): pi core has no dedicated manifest-validator subcommand (no `pi doctor`/`pi
    check`), so the fallback is `pi`'s own real discovery path — `pi install <path> -l`
    (project-local install, writes `.pi/settings.json` in a throwaway cwd, never the plugin
    root) then `pi list`. Verified live: `pi list` names a locally-installed "Project package"
    by its resolved install PATH under a `Project packages:` heading, NOT by the package.json
    `name` field (a local install carries no registry identity) — so the check matches the
    resolved root path, not the name, the same "found the real contract by running the CLI"
    class W2 hit with `hermes plugins doctor` not existing. 0 discovered; 1 the CLI rejected
    the package or the path is missing from the listing; 2 SKIP (setup problem, e.g. no
    package.json written yet)."""
    pkg_path = root / "package.json"
    if not pkg_path.is_file():
        return 2, "SKIP — package.json not written yet; run the writer first"
    resolved_root = str(root.resolve())
    with tempfile.TemporaryDirectory() as td:
        scratch = Path(td)
        try:
            r_install = subprocess.run(
                [exe, "install", resolved_root, "-l"],
                cwd=str(scratch), capture_output=True, text=True, timeout=60,
            )
        except (OSError, subprocess.SubprocessError) as e:
            return 2, f"SKIP — `pi install` failed to run: {e}"
        if r_install.returncode != 0:
            return 1, (f"REJECTED — `pi install {resolved_root} -l` exit {r_install.returncode}: "
                        f"{(r_install.stdout + r_install.stderr).strip()[-300:]}")
        try:
            r_list = subprocess.run(
                [exe, "list"], cwd=str(scratch), capture_output=True, text=True, timeout=30,
            )
        except (OSError, subprocess.SubprocessError) as e:
            return 2, f"SKIP — `pi list` failed to run: {e}"
        if r_list.returncode != 0:
            return 1, f"REJECTED — `pi list` exit {r_list.returncode}: {(r_list.stdout + r_list.stderr).strip()[-300:]}"
        listing = r_list.stdout
        if "Project packages:" not in listing or resolved_root not in listing:
            return 1, f"REJECTED — '{resolved_root}' not found under Project packages: in `pi list`: {listing[-300:]}"
        return 0, f"loaded — `pi install {resolved_root} -l` then `pi list` shows it under Project packages:"


def probe(root: Path, harnesses=None):
    """Tri-state per harness: 0 loaded/binary present and ran clean, 1 the harness rejected
    the overlay, 2 SKIP (binary absent). The exact validator subcommand is established from
    each CLI's own --help at build/probe time and recorded here; a harness with no dedicated
    load-validating subcommand falls back to its own install-and-list form."""
    harnesses = harnesses or DEFAULT_HARNESSES
    results = {}
    for h in harnesses:
        backend = BACKENDS[h]()
        binary, _ = backend.probe_hint()
        exe = shutil.which(binary)
        if exe is None:
            results[h] = (2, f"SKIP — `{binary}` not on PATH; install hint: see harness's own docs")
            continue
        if h == "codex":
            # No cited Codex validator subcommand in the research record (LLD-0025
            # Resolution 6). Fall back to a temp CODEX_HOME marketplace install-and-list —
            # scriptable in principle, declared human-only here since no primary-source
            # subcommand is verified; recorded as tier-3-only for Codex until one is found.
            results[h] = (2, "SKIP — no verified Codex validator subcommand "
                             "(Resolution 6 tier 2 unproven for codex; use tier 3, the "
                             "human load assert)")
        elif h == "hermes":
            # `hermes plugins doctor` does NOT exist on this host's hermes CLI (checked via
            # --help at build time, per Resolution 6 tier 2's own instruction) — no dedicated
            # load-validating subcommand exists. The established fallback: copy this plugin's
            # generated overlay into a temp HOME's ~/.hermes/plugins/<name>/ (hermes's own
            # documented user-plugin discovery path, hermes_cli/plugins.py) and run
            # `hermes plugins list --json` against that isolated HOME — proves plugin.yaml
            # parses and the plugin is discoverable. This does NOT execute register(ctx) (no
            # session bootstrap), so it is a partial tier-2 close, named as such rather than
            # silently upgraded to a full load assert.
            results[h] = _probe_hermes(exe, root)
        elif h == "pi":
            results[h] = _probe_pi(exe, root)
        else:
            results[h] = (2, f"SKIP — {h} backend not built this wave")
    return results


# ---------------------------------------------------------------------------
# selftest (Resolution 6, tier 1)
# ---------------------------------------------------------------------------

FIXTURE_SKILL_A = """---
name: foo-bar
description: >-
  Does the thing. Also does another thing.
disable-model-invocation: true
user-invocable: false
argument-hint: "[target] [--flag]"
---

# foo-bar
body
Uses ${CLAUDE_PLUGIN_ROOT}/scripts/x.mjs and $ARGUMENTS for its own invocation.
"""

FIXTURE_SKILL_B = """---
name: baz
description: Second skill, plain sentence.
disable-model-invocation: false
user-invocable: true
context: fork
---

# baz
body
"""


def _build_fixture(scratch: Path):
    plugin = scratch / "demo-plugin"
    (plugin / ".claude-plugin").mkdir(parents=True)
    (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": "demo-plugin",
        "version": "0.1.0",
        "description": "A fixture plugin for the selftest.",
        "author": {"name": "T"},
        "license": "MIT",
        "keywords": ["a", "b"],
    }))
    (plugin / "skills" / "foo-bar").mkdir(parents=True)
    (plugin / "skills" / "foo-bar" / "SKILL.md").write_text(FIXTURE_SKILL_A)
    (plugin / "skills" / "baz").mkdir(parents=True)
    (plugin / "skills" / "baz" / "SKILL.md").write_text(FIXTURE_SKILL_B)
    (plugin / "agents").mkdir()
    (plugin / "agents" / "helper.md").write_text("# helper\n")
    (plugin / ".mcp.json").write_text(json.dumps({
        "mcpServers": {
            "demo": {
                "command": "node",
                "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
                "env": {"TOKEN": "${user_config.token}"},
            }
        }
    }))
    (scratch / ".claude-plugin").mkdir()
    (scratch / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "name": "demo-marketplace",
        "plugins": [{"name": "demo-plugin", "source": "./demo-plugin", "description": "d"}],
    }))
    return plugin


def selftest():
    with tempfile.TemporaryDirectory() as td:
        scratch = Path(td)
        plugin = _build_fixture(scratch)

        # negative control: nothing written yet — verify must fail
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "unwritten fixture must fail verify"
        assert any("stale:" in f for f in findings), "unwritten fixture findings must name stale paths"

        # write, then verify passes
        code, findings, targets = run(plugin, workspace_root=scratch)
        assert code == 0, f"write should succeed, got findings: {findings}"
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 0, f"post-write verify should pass, got: {findings}"

        # content predicates (Acceptance 3-6)
        pj = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text())
        assert pj["version"] == "0.1.0", "version must mirror .claude-plugin/plugin.json"
        assert pj["skills"] == "./skills/", "skills field wrong"
        assert pj["mcpServers"] == "./.mcp.json", "mcpServers pointer wrong"
        assert pj["interface"]["displayName"] == "Demo Plugin", "derived displayName must title-case the name"

        yaml_a = (plugin / "skills" / "foo-bar" / "agents" / "openai.yaml").read_text()
        assert 'display_name: "Foo Bar"' in yaml_a, "display_name must be title-cased"
        assert 'short_description: "Does the thing."' in yaml_a, "short_description must be first sentence only"

        # #1008 invocation-policy mapping (Codex): a command-only skill (foo-bar,
        # disable-model-invocation: true) must emit the policy block; an ordinary skill
        # (baz, disable-model-invocation: false) must NOT (negative control).
        assert "policy:" in yaml_a and "allow_implicit_invocation: false" in yaml_a, \
            "a command-only skill must emit policy.allow_implicit_invocation: false on Codex"
        yaml_b = (plugin / "skills" / "baz" / "agents" / "openai.yaml").read_text()
        assert "policy:" not in yaml_b, \
            "an ordinary (non-command) skill must NOT emit a policy block (negative control)"

        # Hermes content predicates (W2, #890)
        plugin_yaml = (plugin / "plugin.yaml").read_text()
        assert 'name: "demo-plugin"' in plugin_yaml, "plugin.yaml name must mirror plugin.json"
        assert 'version: "0.1.0"' in plugin_yaml, "plugin.yaml version must mirror plugin.json, unreformatted"
        assert "manifest_version: 1" in plugin_yaml, "plugin.yaml must declare manifest_version: 1"

        init_py = (plugin / "__init__.py").read_text()
        assert "def register(ctx):" in init_py, "__init__.py must define register(ctx) per the fixed template"
        assert init_py.count("ctx.register_skill(") == 2, \
            "__init__.py must register exactly one line per skill directory (2 fixture skills)"
        assert "ctx.register_skill('foo-bar'," in init_py, \
            "a command-only skill still gets a plain register_skill line on Hermes (R-5 terminal)"
        assert "ctx.register_skill('baz'," in init_py, "fork skill also gets a plain register_skill line"
        assert "ctx.register_hook" not in init_py and "ctx.register_command" not in init_py, \
            "nothing but register_skill is registered this wave (Resolution 3)"

        # #899: the generated register() must survive a stub Hermes ctx whose
        # register_skill() calls path.exists() (hermes_cli/plugins.py:3355) AND requires a
        # non-empty description= — proves the Path emission + description passthrough, not
        # just that the string "ctx.register_skill(" appears in the source.
        import importlib.util as _ilu

        spec = _ilu.spec_from_file_location("_demo_plugin_hermes_init", plugin / "__init__.py")
        mod = _ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)

        registered = []

        class _StubCtx:
            def register_skill(self, name, path, description=None):
                assert hasattr(path, "exists"), \
                    f"skill {name}'s path must be a Path-like object, not a plain str"
                assert path.exists(), f"skill {name}'s registered path must actually exist"
                assert description, f"skill {name} must carry a non-empty description="
                registered.append(name)

        mod.register(_StubCtx())
        assert set(registered) == {"foo-bar", "baz"}, \
            "register() must call register_skill() for every skill in the fixture"

        # negative control: the OLD os.path.join(...) str emission must fail the same gate
        class _StrPathStubCtx:
            def register_skill(self, name, path, description=None):
                path.exists()  # AttributeError: 'str' object has no attribute 'exists'

        try:
            import os as _os

            def _old_register(ctx):
                ctx.register_skill("foo-bar", _os.path.join(str(plugin), "skills", "foo-bar", "SKILL.md"))

            _old_register(_StrPathStubCtx())
            raise AssertionError("old str-path emission should have raised AttributeError on .exists()")
        except AttributeError:
            pass

        hermes_mcp = (plugin / "hermes-mcp.yaml").read_text()
        assert "mcp_servers:" in hermes_mcp, "hermes-mcp.yaml must carry an mcp_servers: fragment"
        assert "demo:" in hermes_mcp and 'command: "node"' in hermes_mcp, \
            "hermes-mcp.yaml must carry the .mcp.json server 1:1"

        notes = (plugin / "HARNESS-NOTES.md").read_text()
        assert "`foo-bar`" in notes and "Command-only skills" in notes, \
            "command-only skill must be named in HARNESS-NOTES.md"
        assert "`baz`" in notes and "Fork skills" in notes, "fork skill must be named in HARNESS-NOTES.md"
        assert "`helper`" in notes, "dropped agent must be named in HARNESS-NOTES.md"
        assert "needs-substitution" in notes, "MCP substitution tokens must be flagged in the note"
        assert "## Hermes" in notes and "hermes-mcp.yaml" in notes, \
            "a built Hermes overlay must render a real Hermes section, not the not-built-yet stub"
        assert "## Pi" in notes and "package.json" in notes.split("## Pi")[1], \
            "a built Pi overlay must render a real Pi section, not the not-built-yet stub"

        # #1008 cross-harness body-token degradation inventory: foo-bar's body (see
        # FIXTURE_SKILL_A) carries both ${CLAUDE_PLUGIN_ROOT} and $ARGUMENTS; baz's body
        # carries neither (negative control, asserted below).
        assert "## Cross-harness token degradations" in notes, \
            "the degradation-inventory section must be rendered"
        token_section = notes.split("## Cross-harness token degradations")[1].split("## Codex")[0]
        assert "`foo-bar`" in token_section and "${CLAUDE_PLUGIN_ROOT}" in token_section, \
            "foo-bar's ${CLAUDE_PLUGIN_ROOT} body token must be inventoried"
        assert "$ARGUMENTS" in token_section, "foo-bar's $ARGUMENTS body token must be inventoried"
        ts_lines = [ln for ln in token_section.splitlines() if ln.startswith("- `")]
        args_line = next(ln for ln in ts_lines if "`$ARGUMENTS`" in ln)
        path_line = next(ln for ln in ts_lines if "${CLAUDE_PLUGIN_ROOT}" in ln)
        assert ", pi" not in args_line.split(":", 1)[1].split("—")[0], \
            "foo-bar is command-only -> $ARGUMENTS's affected set must exclude pi " \
            f"(Pi substitutes it natively via prompts/foo-bar.md); line was: {args_line!r}"
        assert "Pi excluded" in args_line, \
            "the pi-native-substitution fallback note must explain the exclusion, not just omit pi silently"
        assert ", pi" in path_line.split(":", 1)[1].split("—")[0], \
            f"${{CLAUDE_PLUGIN_ROOT}} has no Pi-native equivalent -> pi must stay in its affected set; line was: {path_line!r}"
        assert "`baz`" not in token_section, \
            "baz's body carries no Claude-only token -> it must not appear in the inventory"

        # W4 (T-2, #887/#895): Pi's MCP row must read PASSTHROUGH, never drop-with-note, and
        # must carry the third-party-adapter caveat plus its own needs-substitution flag —
        # the fixture's .mcp.json carries both a ${CLAUDE_PLUGIN_ROOT} and a ${user_config.*}
        # token (see _build_fixture above), so the Pi section must flag them independently
        # of Codex/Hermes's own flags earlier in the same file.
        pi_section = notes.split("## Pi")[1]
        assert "passthrough" in pi_section.lower(), \
            "Pi's MCP row must read passthrough (W4), not drop-with-note"
        assert "pi-mcp-adapter" in pi_section and "NOT part of Pi core" in pi_section, \
            "Pi's MCP row must name the third-party pi-mcp-adapter and the not-core caveat"
        assert "needs-substitution" in pi_section, \
            "Pi's MCP row must flag its own needs-substitution tokens, not just cross-reference Codex/Hermes"

        mkt = json.loads((scratch / ".agents" / "plugins" / "marketplace.json").read_text())
        assert mkt["plugins"][0]["name"] == "demo-plugin", "estate marketplace must mirror the root one"

        # negative control: hand-edit (Codex) -> verify must bite
        (plugin / ".codex-plugin" / "plugin.json").write_text('{"name": "drifted"}')
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "hand-edited overlay must fail verify"
        assert any("plugin.json" in f for f in findings), "hand-edit finding must name the drifted file"
        run(plugin, workspace_root=scratch)  # restore

        # negative control: hand-edit (Hermes __init__.py) -> verify must bite
        (plugin / "__init__.py").write_text("# hand-edited\n")
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a hand-edited __init__.py must fail verify"
        assert any("__init__.py" in f for f in findings), "hand-edit finding must name __init__.py"
        run(plugin, workspace_root=scratch)  # restore

        # restore, then negative control: a skill removed but its overlay left behind
        # (a partial delete — SKILL.md gone, agents/openai.yaml orphaned) -> unexpected
        (plugin / "skills" / "baz" / "SKILL.md").unlink()
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a deleted skill's orphaned overlay must fail verify"
        assert any("unexpected:" in f and "baz" in f for f in findings), \
            "deleted-skill finding must be tagged unexpected and name the orphaned file"

        # restore baz, then negative control: MCP dropped -> hermes-mcp.yaml orphaned -> unexpected
        (plugin / "skills" / "baz" / "SKILL.md").write_text(FIXTURE_SKILL_B)
        run(plugin, workspace_root=scratch)
        (plugin / ".mcp.json").unlink()
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a dropped .mcp.json must orphan hermes-mcp.yaml"
        assert any("unexpected:" in f and "hermes-mcp.yaml" in f for f in findings), \
            "the orphaned hermes-mcp.yaml finding must be tagged unexpected"
        (plugin / ".mcp.json").write_text(json.dumps({
            "mcpServers": {
                "demo": {
                    "command": "node",
                    "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
                    "env": {"TOKEN": "${user_config.token}"},
                }
            }
        }))
        run(plugin, workspace_root=scratch)

        # edge case: a plugin with zero skills -> __init__.py's fallback branch (Resolution 3:
        # nothing to register is still a valid register(ctx))
        no_skills = scratch / "no-skills-plugin"
        (no_skills / ".claude-plugin").mkdir(parents=True)
        (no_skills / ".claude-plugin" / "plugin.json").write_text(json.dumps({
            "name": "no-skills-plugin",
            "version": "0.1.0",
            "description": "A fixture plugin with zero skills.",
        }))
        code, findings, targets = run(no_skills, workspace_root=scratch)
        assert code == 0, f"a zero-skill plugin must still write cleanly, got: {findings}"
        init_no_skills = (no_skills / "__init__.py").read_text()
        assert "pass  # no skills to register" in init_no_skills, \
            "zero-skill __init__.py must fall back to a bare pass, not an empty register(ctx)"
        assert init_no_skills.count("ctx.register_skill(") == 0, \
            "zero-skill __init__.py must register nothing"
        code, findings, _ = run(no_skills, verify=True, workspace_root=scratch)
        assert code == 0, f"a written zero-skill overlay must verify clean, got: {findings}"

        # setup errors: missing manifest -> exit 2; unimplemented harness named explicitly -> exit 2
        empty = scratch / "no-manifest-plugin"
        empty.mkdir()
        code, findings, _ = run(empty, verify=True)
        assert code == 2, "a plugin with no manifest must be a setup error, not a drift finding"

        code, findings, _ = run(plugin, harnesses=["zzz-not-a-harness"], verify=True, workspace_root=scratch)
        assert code == 2, "an explicitly named unknown harness must be a setup error, not silently skipped"

        # Pi content predicates (W3, #891)
        pkg = json.loads((plugin / "package.json").read_text())
        assert pkg["name"] == "@nonoun/demo-plugin", "package.json name must be scoped @nonoun/<plugin>"
        assert pkg["version"] == "0.1.0", "package.json version must mirror plugin.json verbatim"
        assert "pi-package" in pkg["keywords"], "the pi-package keyword IS Pi's registry contract"
        assert pkg["pi"]["skills"] == ["./skills"], "pi.skills must declare the skills dir"
        assert pkg["pi"]["prompts"] == ["./prompts"], "pi.prompts must declare the prompts dir when a command skill exists"

        prompt = (plugin / "prompts" / "foo-bar.md").read_text()
        assert prompt.startswith("---\n"), "a command skill's prompt file must carry frontmatter"
        assert 'argument-hint: "[target] [--flag]"' in prompt, \
            "a command skill's own argument-hint must be emitted verbatim in the prompt frontmatter"
        assert "Does the thing." in prompt, "prompt description must come from the skill's own description"
        assert "# foo-bar\nbody" in prompt, "prompt body must be the SKILL.md body verbatim"
        assert not (plugin / "prompts" / "baz.md").is_file(), \
            "a non-command skill (baz) must not get a prompts/ file"

        notes = (plugin / "HARNESS-NOTES.md").read_text()
        pi_section = notes.split("## Pi")[1]
        assert "`foo-bar`" in pi_section and "prompts/{name}.md" in pi_section, \
            "a built Pi overlay must name the command skill's prompt file in the note"

        # negative control: hand-edit (Pi package.json) -> verify must bite
        (plugin / "package.json").write_text('{"name": "drifted"}')
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a hand-edited package.json must fail verify"
        assert any("package.json" in f for f in findings), "hand-edit finding must name package.json"
        run(plugin, workspace_root=scratch)  # restore

        # negative control: a command skill removed -> its prompts/<name>.md orphaned -> unexpected
        (plugin / "skills" / "foo-bar" / "SKILL.md").unlink()
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a deleted command skill's orphaned prompt file must fail verify"
        assert any("unexpected:" in f and "foo-bar.md" in f for f in findings), \
            "deleted-command-skill finding must be tagged unexpected and name the orphaned prompt file"
        (plugin / "skills" / "foo-bar" / "SKILL.md").write_text(FIXTURE_SKILL_A)
        run(plugin, workspace_root=scratch)

        # merge-only: an existing package.json keeps its other keys untouched
        merge_plugin = scratch / "merge-plugin"
        (merge_plugin / ".claude-plugin").mkdir(parents=True)
        (merge_plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({
            "name": "merge-plugin", "version": "0.1.0", "description": "Has its own package.json.",
        }))
        merge_plugin.joinpath("package.json").write_text(json.dumps({
            "name": "@nonoun/merge-plugin", "version": "0.0.1", "description": "old",
            "scripts": {"build": "tsc"},
        }))
        run(merge_plugin, harnesses=["pi"], workspace_root=scratch)
        merged = json.loads((merge_plugin / "package.json").read_text())
        assert merged["scripts"] == {"build": "tsc"}, \
            "the writer must merge only the pi key + keywords, leaving other package.json keys alone"
        assert merged["version"] == "0.0.1", \
            "merge-only means version too -> the ORIGINAL package.json version must survive untouched"
        assert merged["description"] == "old", \
            "merge-only means description too -> the ORIGINAL package.json description must survive untouched"
        assert merged["name"] == "@nonoun/merge-plugin", "merge-only leaves the original name untouched too"
        assert "pi-package" in merged["keywords"], "the writer still adds the pi-package keyword on merge"
        assert merged["pi"]["skills"] == ["./skills"], "the writer still adds its own pi key on merge"

        # negative control: an unparseable pre-existing package.json is a setup error, not a
        # silent clobber (the emitter never invents content for a file it can't read)
        bad_pkg_plugin = scratch / "bad-pkg-plugin"
        (bad_pkg_plugin / ".claude-plugin").mkdir(parents=True)
        (bad_pkg_plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps({
            "name": "bad-pkg-plugin", "version": "0.1.0", "description": "Has a broken package.json.",
        }))
        bad_pkg_plugin.joinpath("package.json").write_text("not json")
        code, findings, _ = run(bad_pkg_plugin, harnesses=["pi"], verify=True, workspace_root=scratch)
        assert code == 2, "an unparseable pre-existing package.json must be a setup error, not silently discarded"

        # #1008 --scan-tokens CLI leg: proves the actual subprocess path release_gate.py's
        # G15b invokes, not just the pure scan_claude_only_tokens() function underneath it.
        emit_script = Path(__file__).resolve()
        r = subprocess.run(
            [sys.executable, str(emit_script), str(plugin), "--scan-tokens", "--harness", "codex,hermes,pi"],
            capture_output=True, text=True,
        )
        assert r.returncode == 0, f"--scan-tokens must exit 0 (informational, never a gate): {r.stderr}"
        assert "token-degradation: foo-bar -> $ARGUMENTS, ${CLAUDE_PLUGIN_ROOT}" in r.stdout, \
            f"--scan-tokens must print a token-degradation line naming foo-bar and both tokens, got: {r.stdout}"
        assert "baz" not in r.stdout, "baz carries no Claude-only token -> must not appear in --scan-tokens output"

        # negative control: a plugin whose skill bodies carry no Claude-only token -> CLEAN, no findings
        r2 = subprocess.run(
            [sys.executable, str(emit_script), str(no_skills), "--scan-tokens"],
            capture_output=True, text=True,
        )
        assert r2.returncode == 0 and "CLEAN" in r2.stdout and "token-degradation:" not in r2.stdout, \
            f"a zero-skill plugin must scan CLEAN with no findings, got: {r2.stdout}"

        # negative control: an unreadable manifest is a setup error (exit 2), never a silent CLEAN
        r3 = subprocess.run(
            [sys.executable, str(emit_script), str(empty), "--scan-tokens"],
            capture_output=True, text=True,
        )
        assert r3.returncode == 2, "--scan-tokens against an unreadable manifest must be a setup error, not CLEAN"

    print("harness_emit selftest · PASS · write/verify roundtrip (codex+hermes+pi), hand-edit bite "
          "(all three backends), orphan detection (openai.yaml + hermes-mcp.yaml + prompts/*.md), "
          "MCP substitution flagging, __init__.py register_skill template, package.json merge-only, "
          "marketplace mirror, setup-error controls")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selftest":
        return selftest()

    root = Path(argv[0]).resolve()
    verify = "--verify" in argv[1:]
    do_probe = "--probe" in argv[1:]
    do_scan_tokens = "--scan-tokens" in argv[1:]
    harnesses = DEFAULT_HARNESSES
    for a in argv[1:]:
        if a.startswith("--harness"):
            _, _, val = a.partition("=")
            if not val and argv.index(a) + 1 < len(argv):
                val = argv[argv.index(a) + 1]
            if val:
                harnesses = [h.strip() for h in val.split(",") if h.strip()]

    if do_probe:
        results = probe(root, harnesses)
        lines = [f"harness_emit probe · {root}"]
        code = 0
        for h, (c, msg) in results.items():
            lines.append(f"  {h}: {msg}")
            if c == 1:
                code = 1
        print("\n".join(lines))
        return code

    if do_scan_tokens:
        # Informational only — never a freshness gate on its own; exit 0 unless the plugin
        # itself can't be read at all (a setup error, same discipline as every other mode).
        # release_gate.py's G15b subprocess-calls exactly this mode and parses its
        # `token-degradation:`-prefixed lines rather than re-implementing the scan.
        try:
            source = read_plugin(root)
        except SourceError as e:
            print(f"harness_emit scan-tokens · {root} · ERROR · {e}")
            return 2
        found = scan_claude_only_tokens(source, harnesses=harnesses)
        verdict = "CLEAN" if not found else "FOUND"
        print(f"harness_emit scan-tokens · {root} · {verdict} · {len(found)} skill(s)")
        for skill_name, per_token in found:
            toks = ", ".join(t for t, _ in per_token)
            print(f"  token-degradation: {skill_name} -> {toks}")
        return 0

    code, findings, targets = run(root, harnesses, verify=verify)
    verdict = {0: "CLEAN", 1: "STALE", 2: "ERROR"}[code]
    print(f"harness_emit · {root} · {verdict} · {len(targets)} target(s)")
    for f in findings:
        print(f"  {f}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
