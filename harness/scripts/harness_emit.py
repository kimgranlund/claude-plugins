#!/usr/bin/env python3
"""harness_emit — derive per-harness plugin overlays (Codex/Hermes/Pi) from each
plugin's Claude Code source of truth.

WHY THIS EXISTS (LLD-0025, gh#885/#886)

Each plugin here is authored once, for Claude Code. Other agent harnesses (OpenAI Codex,
Hermes, Pi) read a DIFFERENT manifest shape. Rather than hand-author and hand-sync a second
manifest tree per harness, this script derives one **overlay** per target harness from the
SAME sources of truth `release_gate.py` already validates: `.claude-plugin/plugin.json`,
`skills/*/SKILL.md` frontmatter, the presence of `agents/`, `hooks/hooks.json`, `.mcp.json`,
and the root `.claude-plugin/marketplace.json`. The overlay is committed in-tree (never
`dist/` — `.claude/rules/dist-output.md`) and a freshness check (release_gate.py's G15) fails
the gate the moment a hand-edit or a stale overlay diverges from the recomputation.

This wave (W1, gh#886) ships ONLY the Codex backend. Hermes and Pi backends are stubbed to
raise NotImplementedError naming their own wave tickets (T-5, T-6) — selecting them via
--harness is a setup error (exit 2), not a silent no-op.

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
  <plugin>/HARNESS-NOTES.md   (one per plugin; every harness's degradation ledger)
  <workspace>/.agents/plugins/marketplace.json   (Codex only, estate-level; derived from the
    root .claude-plugin/marketplace.json 1:1)

NOT DERIVED this wave: a plugin's own agents/*.md, hooks/hooks.json, and the
disable-model-invocation/context flags on a skill have no Codex/Hermes/Pi manifest key —
they are dropped with a note (Resolution 3, the degradation table) rather than guessed at.

WRITE / VERIFY / PROBE
  harness_emit.py <plugin-root> [--harness codex,hermes,pi]              # write
  harness_emit.py <plugin-root> --verify [--harness codex,hermes,pi]     # gate: exit 1 on drift
  harness_emit.py <plugin-root> --probe [--harness codex,hermes,pi]      # tri-state harness load
  harness_emit.py selftest                                               # prove the gate bites

No args (or a bare path with neither --verify/--probe and no write intent unclear) -> this
docstring, exit 2.

Verdict line first: `harness_emit · <root> · CLEAN|STALE|ERROR · n target(s)`, then one line
per finding.

Exit: 0 clean/written · 1 drift found (--verify) · 2 setup error (unreadable manifest, or an
unimplemented harness named explicitly via --harness).
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_lint  # parse_frontmatter — the only frontmatter reader this script trusts (R-2)

DEFAULT_HARNESSES = ["codex"]  # widened per wave: W1 codex, W2 +hermes, W3 +pi
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
            fields, _ = skill_lint.parse_frontmatter(lines)
            if "name" not in fields or "description" not in fields:
                raise SourceError(f"{sm}: missing name/description in frontmatter")
            s_name = fields["name"][0]
            s_desc = fields["description"][0]
            command = fields.get("disable-model-invocation", ("false", 0))[0].strip().lower() == "true"
            fork = fields.get("context", ("", 0))[0].strip().lower() == "fork"
            codex_default_prompt = fields.get("codex_default_prompt", (None, 0))[0]
            skills.append({
                "name": s_name,
                "description": s_desc,
                "command": command,
                "fork": fork,
                "dir": d,
                "codex_default_prompt": codex_default_prompt,
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


# ---------------------------------------------------------------------------
# Ledger — the degradation record, rendered into HARNESS-NOTES.md
# ---------------------------------------------------------------------------

class Ledger:
    def __init__(self, source):
        self.source = source
        self.dropped_agents = list(source["agents"])
        self.dropped_hooks = list(source["hooks"])
        self.command_skills = [s["name"] for s in source["skills"] if s["command"]]
        self.fork_skills = [s["name"] for s in source["skills"] if s["fork"]]
        self.mcp_flags = mcp_needs_substitution(source["mcp"]) if source["mcp"] else []

    def render(self) -> str:
        s = self.source
        lines = [f"# {s['name']} {s['version']} — harness overlay notes "
                 "(generated by harness_emit.py; do not edit)", ""]

        def _list(items):
            return ", ".join(f"`{i}`" for i in items) if items else "none"

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
            f"- Command-only skills now model-routable: {_list(self.command_skills)}.",
            f"- Fork skills (their `context` field drops; body runs inline): {_list(self.fork_skills)}.",
        ]
        if self.mcp_flags:
            lines.append(f"- MCP: `./.mcp.json` pointed at ({len(self.mcp_flags)} value(s) flagged above).")
        elif s["mcp"] is not None:
            lines.append("- MCP: `./.mcp.json` pointed at; no substitution tokens found.")
        else:
            lines.append("- MCP: none shipped.")
        lines.append("")

        for harness_name, ticket in (("Hermes", "T-5"), ("Pi", "T-6")):
            lines += [
                f"## {harness_name}",
                f"- This backend isn't built yet (tracked as {ticket}; no install path exists for "
                f"{harness_name} from this repo today) — no action needed here. What WOULD drop "
                f"under this plugin's current Claude Code source, computed the same way Codex's "
                f"row above is (kept for a preview, not yet verified against {harness_name}'s own "
                f"contract): agents — {_list(self.dropped_agents)}; hooks: {_list(self.dropped_hooks)}.",
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
            yaml_content = "\n".join(lines) + "\n"
            out.append((s["dir"] / "agents" / "openai.yaml", yaml_content.encode("utf-8")))

        return out

    def probe_hint(self):
        return "codex", ["--help"]


class HermesBackend:
    name = "hermes"

    def targets(self, source, root: Path):
        raise NotImplementedError(
            "Hermes backend ships in W2 (ticket T-5, LLD-0025 Resolution 7) — not built this wave"
        )

    def probe_hint(self):
        return "hermes", ["--help"]


class PiBackend:
    name = "pi"

    def targets(self, source, root: Path):
        raise NotImplementedError(
            "Pi backend ships in W3 (ticket T-6, LLD-0025 Resolution 7) — not built this wave"
        )

    def probe_hint(self):
        return "pi", ["--help"]


BACKENDS = {"codex": CodexBackend, "hermes": HermesBackend, "pi": PiBackend}


# ---------------------------------------------------------------------------
# HARNESS-NOTES.md and estate marketplace are cross-backend, computed once
# ---------------------------------------------------------------------------

def notes_target(source, root: Path):
    ledger = Ledger(source)
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
    targets.append(notes_target(source, root))
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
---

# foo-bar
body
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

        notes = (plugin / "HARNESS-NOTES.md").read_text()
        assert "`foo-bar`" in notes and "Command-only skills" in notes, \
            "command-only skill must be named in HARNESS-NOTES.md"
        assert "`baz`" in notes and "Fork skills" in notes, "fork skill must be named in HARNESS-NOTES.md"
        assert "`helper`" in notes, "dropped agent must be named in HARNESS-NOTES.md"
        assert "needs-substitution" in notes, "MCP substitution tokens must be flagged in the note"

        mkt = json.loads((scratch / ".agents" / "plugins" / "marketplace.json").read_text())
        assert mkt["plugins"][0]["name"] == "demo-plugin", "estate marketplace must mirror the root one"

        # negative control: hand-edit -> verify must bite
        (plugin / ".codex-plugin" / "plugin.json").write_text('{"name": "drifted"}')
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "hand-edited overlay must fail verify"
        assert any("plugin.json" in f for f in findings), "hand-edit finding must name the drifted file"

        # restore, then negative control: a skill removed but its overlay left behind
        # (a partial delete — SKILL.md gone, agents/openai.yaml orphaned) -> unexpected
        run(plugin, workspace_root=scratch)
        (plugin / "skills" / "baz" / "SKILL.md").unlink()
        code, findings, _ = run(plugin, verify=True, workspace_root=scratch)
        assert code == 1, "a deleted skill's orphaned overlay must fail verify"
        assert any("unexpected:" in f and "baz" in f for f in findings), \
            "deleted-skill finding must be tagged unexpected and name the orphaned file"

        # setup errors: missing manifest -> exit 2; unimplemented harness named explicitly -> exit 2
        empty = scratch / "no-manifest-plugin"
        empty.mkdir()
        code, findings, _ = run(empty, verify=True)
        assert code == 2, "a plugin with no manifest must be a setup error, not a drift finding"

        code, findings, _ = run(plugin, harnesses=["hermes"], verify=True, workspace_root=scratch)
        assert code == 2, "an explicitly named unbuilt backend must be a setup error, not silently skipped"
        assert "T-5" in findings[0], "the setup-error finding must name the wave ticket"

    print("harness_emit selftest · PASS · write/verify roundtrip, hand-edit bite, "
          "orphan detection, MCP substitution flagging, marketplace mirror, setup-error controls")
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

    code, findings, targets = run(root, harnesses, verify=verify)
    verdict = {0: "CLEAN", 1: "STALE", 2: "ERROR"}[code]
    print(f"harness_emit · {root} · {verdict} · {len(targets)} target(s)")
    for f in findings:
        print(f"  {f}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
