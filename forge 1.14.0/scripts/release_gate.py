#!/usr/bin/env python3
"""release_gate — the plugin release ritual as code.

Usage:
  release_gate.py <plugin-root> [--package]   run the gate; --package also writes
                                              dist/<name>-<version>.plugin on a clean gate
  release_gate.py selftest                    prove the checks on a temp fixture plugin

Gate order (plugin-authoring-standards §Release discipline):
  G1 manifest: .claude-plugin/plugin.json valid, kebab name, semver version
  G2 structure: only the manifest in .claude-plugin/; every skills/* dir has SKILL.md
  G3 full lint: every SKILL.md, agents/*.md, hooks.json, plugin.json via skill_lint (FAIL fails)
  G4 bundled selftests: every scripts/*.py|*.mjs|*.js exposing a selftest mode must exit 0
     (py via this interpreter, js via node; js with node absent -> WARN, unproven;
      exit 2 = SKIP, runtime dependency absent -> disclosed in the ok line, not failed)
  G5 phantom sweep: [[handle]] refs in live .md (CHANGELOG excluded) — WARN, counted
  G6 package (--package): dist/<name>-<version>.plugin, excluding dist/, .claude/, and the
     repo's root CLAUDE.md (dev harness != distribution); a same-version artifact FAILS
     (the version is the update cache key — same version means nobody receives the ship)
  G7 evals: every suite passes eval_check; model-invocable skills without a suite WARN
  G10 docs: README/MANUAL cover every skill, README ledger version matches the manifest,
      CLAUDE.md counts reconcile (composes docs_check.py; accuracy stays human)
  G9 packs: every skill with references/INDEX.md passes corpus_check (K1 FAILs fail the gate)
  G8 sibling names: kebab tokens in SKILL.md files that carry one of this plugin's own
     name-suffixes but match no installed skill -> WARN (rename drift, phantom prose siblings)

Exit 0 clean (warnings allowed), 1 on any FAIL.
"""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_lint  # the check tier composes; it is not restated
import eval_check
import corpus_check
import docs_check

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PHANTOM_RE = re.compile(r"\[\[[a-z0-9-]+\]\]")


def gate(root: Path, package: bool = False):
    fails, warns, lines = [], [], []
    ok = lambda m: lines.append(f"  ok    {m}")
    def fail(code, m):
        fails.append(code); lines.append(f"  FAIL  {code}  {m}")
    def warn(code, m):
        warns.append(code); lines.append(f"  warn  {code}  {m}")

    # G1 manifest
    mf = root / ".claude-plugin" / "plugin.json"
    name = version = None
    if not mf.is_file():
        fail("G1", f"missing {mf} -> the manifest is the plugin")
    else:
        try:
            m = json.loads(mf.read_text())
            name, version = m.get("name", ""), m.get("version", "")
            if not KEBAB_RE.match(name or ""):
                fail("G1", f"name `{name}` -> kebab-case required")
            if not SEMVER_RE.match(version or ""):
                fail("G1", f"version `{version}` -> semver required; the version is the update cache key")
            if not fails:
                ok(f"manifest {name} v{version}")
        except (json.JSONDecodeError, ValueError) as e:
            fail("G1", f"plugin.json invalid JSON ({e})")

    # G2 structure
    cp = root / ".claude-plugin"
    if cp.is_dir():
        strays = [p.name for p in cp.iterdir() if p.name not in ("plugin.json",)]
        if strays:
            fail("G2", f"components inside .claude-plugin/ ({strays[:3]}) -> only the manifest lives there")
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and not (d / "SKILL.md").is_file():
                fail("G2", f"skills/{d.name}/ has no SKILL.md")
    if "G2" not in fails:
        ok("structure: manifest isolated; every skill dir carries SKILL.md")

    # G3 full lint via skill_lint
    targets = (sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md"))
               + sorted(root.glob("hooks/hooks.json")) + ([mf] if mf.is_file() else []))
    lint_failed = []
    for t in targets:
        _, failed = skill_lint.lint_path(str(t))
        if failed:
            lint_failed.append(str(t.relative_to(root)))
    if lint_failed:
        fail("G3", f"skill_lint FAIL in: {', '.join(lint_failed)} -> run skill_lint.py on each for the repair list")
    else:
        ok(f"lint clean across {len(targets)} files")

    # G4 bundled selftests — py via the running interpreter, js/mjs via node (parity, 2026-07-14:
    # the original .py-only rglob left every .mjs selftest in the estate unrun at the gate)
    import shutil
    node = shutil.which("node")
    scripts = sorted(p for pat in ("scripts/*.py", "scripts/*.mjs", "scripts/*.js")
                     for p in root.rglob(pat) if "dist" not in p.parts)
    tested, js_skipped, dep_skipped = 0, 0, []
    for s in scripts:
        if "selftest" not in s.read_text(encoding="utf-8", errors="replace"):
            continue
        if s.resolve() == Path(__file__).resolve():
            continue  # the gate proves itself via its own selftest mode, not recursively
        if s.suffix == ".py":
            runner = [sys.executable]
        elif node:
            runner = [node]
        else:
            js_skipped += 1
            continue
        r = subprocess.run([*runner, str(s), "selftest"], capture_output=True, text=True, timeout=120)
        if r.returncode == 2:
            # ratified tri-state (2026-07-14, pioneered by ui-probe.mjs): exit 2 = SKIP,
            # the selftest cannot prove itself here (runtime dependency absent) — disclosed, not failed
            dep_skipped.append(s.name)
            continue
        tested += 1
        if r.returncode != 0:
            fail("G4", f"{s.relative_to(root)} selftest exit {r.returncode} -> a shipped script proves its counters or does not ship")
    if js_skipped:
        warn("G4", f"{js_skipped} js script(s) expose a selftest but node is not on PATH -> unproven, install node to run them")
    if "G4" not in fails:
        skipnote = f"; {len(dep_skipped)} skipped, dependency absent: {', '.join(dep_skipped)}" if dep_skipped else ""
        ok(f"bundled selftests green ({tested} scripts{skipnote})")

    # G5 phantom sweep — backticked/fenced [[handles]] are mentions, not routing.
    # Sibling-aware (2026-07-09, same rule as G8): a [[handle]] naming a real skill anywhere
    # in the workspace is the ported corpus's link STYLE, not rot — only handles resolving
    # to nothing warn. Style-only handles are reported as an ok-line count.
    g5_inventory = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    for sib in root.parent.glob("*/.claude-plugin/plugin.json"):
        g5_inventory |= {p.parent.name for p in sib.parent.parent.glob("skills/*/SKILL.md")}
    phantom_hits, style_refs = [], 0
    inline_code = re.compile(r"`[^`]*`")
    handle_re = re.compile(r"\[\[([a-z0-9-]+)\]\]")
    for md in root.rglob("*.md"):
        if "CHANGELOG" in md.name or "dist" in md.parts:
            continue
        fenced = False
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for h in handle_re.findall(inline_code.sub("", line)):
                if h in g5_inventory:
                    style_refs += 1
                else:
                    phantom_hits.append(f"{md.relative_to(root)}:{i} [[{h}]]")
    if phantom_hits:
        warn("G5", f"{len(phantom_hits)} dangling [[handle]] refs ({phantom_hits[:3]}...) -> they resolve to no skill anywhere in the workspace; repoint or cut")
    elif style_refs:
        ok(f"no dangling [[handles]] ({style_refs} style refs resolve to workspace skills)")
    else:
        ok("no phantom [[handles]] in live markdown")

    # G7 evals — schema FAILs, coverage gaps WARN
    suite_fail, suites = [], sorted(root.glob("skills/*/evals/evals.json"))
    for s in suites:
        fs = eval_check.check_suite_text(s.read_text(encoding="utf-8", errors="replace"), s.parent.parent.name)
        if any(f[0] == "FAIL" for f in fs):
            suite_fail.append(str(s.relative_to(root)))
    if suite_fail:
        fail("G7", f"eval_check FAIL in: {', '.join(suite_fail)} -> run eval_check.py on each")
    gaps = eval_check.check_coverage(root)
    if gaps:
        warn("G7", f"{len(gaps)} model-invocable skills without eval suites -> descriptions untuned: "
                   + ", ".join(g[2].split(':')[0] for g in gaps))
    if not suite_fail:
        ok(f"evals: {len(suites)} suites valid" + ("" if gaps else "; coverage complete"))

    # G9 corpus reconciliation for knowledge packs
    pack_fail, packs_seen = [], 0
    for sk in sorted(root.glob("skills/*")):
        fs = corpus_check.check_pack(sk) if sk.is_dir() else None
        if fs is None:
            continue
        packs_seen += 1
        if any(f[0] == "FAIL" for f in fs):
            pack_fail.append(sk.name)
    if pack_fail:
        fail("G9", f"corpus_check FAIL in: {', '.join(pack_fail)} -> run corpus_check.py on each")
    else:
        ok(f"packs reconciled ({packs_seen} with INDEX)")

    # G10 docs freshness
    dfs = docs_check.check(root)
    d_fail = [f for f in dfs if f[0] == "FAIL"]
    if d_fail:
        fail("G10", f"{len(d_fail)} docs finding(s): " + "; ".join(f[2] for f in d_fail[:3]) + " -> run docs_check.py")
    else:
        for f in dfs:
            warn("G10", f[2])
        if not dfs:
            ok("docs cover every artifact; ledger matches manifest")

    # G8 stale sibling names — deliberately does NOT strip code spans: a backticked
    # stale name is still rot on a routing-bearing surface (contrast G5's mention rule).
    # Sibling-aware (2026-07-09): cross-plugin soft mentions are doctrine-legal, so tokens
    # resolve against every workspace sibling's skills too before warning — only TRUE
    # phantoms (matching no skill anywhere in the workspace) remain findings.
    inventory = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    for sib in root.parent.glob("*/.claude-plugin/plugin.json"):
        inventory |= {p.parent.name for p in sib.parent.parent.glob("skills/*/SKILL.md")}
    suffixes = {n.rsplit("-", 1)[-1] for n in inventory}
    # verified prose-compound false positives (hyphenated phrases sharing a real suffix)
    allow = {"re-run", "dry-run", "no-split", "keep-separate", "cross-cite",
             "deep-review", "data-not-markup", "color-accessibility", "geometry-not-perception",
             "from-color-science-perception", "from-color-science-spaces", "neutral-by-design",
             "orphaned-tokens", "over-tokens", "prose-over-tokens", "ultimate-tokens",
             "change-verify", "composition-patterns", "macro-patterns", "micro-patterns",
             "state-patterns", "live-agent", "routing-corpus", "training-corpus",
             "catalog-design", "conversational-agent",
             # widened by sibling-aware suffixes (2026-07-09) — verified prose, not names:
             "agent-vs-agent", "fork-vs-agent", "per-agent", "sub-agent", "single-agent",
             "non-agent", "multi-agent", "whole-corpus", "thin-corpus", "source-corpus",
             "skill-corpus", "knowledge-corpus", "rubric-agent-corpus", "rubric-skill-corpus",
             "anti-patterns", "component-patterns", "contrast-standards", "audit-report",
             "lossy-by-design", "first-run", "material-design", "color-tokens",
             "figma-make", "google-stitch",
             # figma-plugin-api joining the estate added the -api suffix (2026-07-09):
             "attributes-as-api",
             # the mechanization pair (2026-07-14): "hand-run" is prose ("a hand-run check",
             # -run suffix from eval-run); "selftest-patterns" is a references file:
             "hand-run", "selftest-patterns",
             # the four UI/design knowledge skills (2026-07-15): "container-patterns" and
             # "scale-theory" are references files (ui-patterns, geometry-systems); "design-systems"
             # is the sibling PLUGIN's name, caught by geometry-systems' own "-systems" suffix;
             # "box-model-and-flow" is a references file (dom-block-flow); "mid-flow" is prose
             # ("mid-flow" in the hook skills), caught once dom-block-flow added the -flow suffix:
             "container-patterns", "scale-theory", "design-systems", "box-model-and-flow",
             # prose compounds newly caught by the same two suffixes (-flow, -systems):
             "mid-flow", "cross-flow", "self-orchestrated-looping-agentic-systems",
             # a2a-* skill names: the token regex skips the digit-bearing "a2a-" segment and
             # "sees" the tail of legitimate full names; plus that plugin's prose compounds
             # and a references file (2026-07-09):
             "agent-design", "isolation-verify", "agent-to-agent", "inter-agent",
             "clean-run", "halt-and-report", "report-format",
             # the `llm` plugin's chat-harness-* family (2026-07-13): "chat-agent" is the
             # family's own shared framing phrase ("a chat-agent harness"), tripping the
             # `-agent` suffix a2ui-conversational-agent already owns; "hardcoded-feature" is
             # ordinary prose in chat-harness-skills-and-routing's own axis description:
             "chat-agent", "hardcoded-feature"}
    token_re = re.compile(r"\b([a-z]{3,}(?:-[a-z]{2,})+)\b")
    stale = {}
    for sk in sorted(root.glob("skills/*/SKILL.md")):
        for tok in set(token_re.findall(sk.read_text(encoding="utf-8", errors="replace"))):
            if tok in inventory or tok in allow or tok.rsplit("-", 1)[-1] not in suffixes:
                continue
            stale.setdefault(tok, []).append(sk.parent.name)
    if stale:
        detail = "; ".join(f"`{t_}` in {', '.join(v[:3])}" for t_, v in sorted(stale.items()))
        warn("G8", f"{len(stale)} skill-like name(s) matching no installed skill -> {detail} "
                   "(rename drift or phantom prose sibling; fix or allowlist)")
    else:
        ok("no stale sibling names in any SKILL.md")

    # G6 package
    artifact = None
    if package and name and version and not fails:
        dist = root / "dist"; dist.mkdir(exist_ok=True)
        artifact = dist / f"{name}-{version}.plugin"
        if artifact.exists():
            fail("G6", f"{artifact.name} already exists -> bump the version (same version = update skipped as current)")
            artifact = None
        else:
            with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as z:
                for p in sorted(root.rglob("*")):
                    if p.is_dir() or "dist" in p.parts or p.name == ".DS_Store":
                        continue
                    rel = p.relative_to(root)
                    if rel.parts[0] == ".claude" or str(rel) == "CLAUDE.md":
                        continue  # repo dev harness, not a plugin component
                    z.write(p, p.relative_to(root))
            ok(f"packaged {artifact.relative_to(root)}")

    verdict = "FAIL" if fails else "CLEAN"
    head = f"release_gate · {root} · {verdict} · {len(fails)} fail / {len(warns)} warn"
    print("\n".join([head, *lines]))
    return (1 if fails else 0), artifact


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td) / "demo-plugin"
        (r / ".claude-plugin").mkdir(parents=True)
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "demo-plugin", "version": "0.1.0"}')
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_lint.GOOD_FIXTURE)
        (r / "README.md").write_text("demo-plugin map: demo-review\n\nv0.1.0 · initial\n")
        code, _ = gate(r)
        assert code == 0, "clean fixture plugin must pass"
        body = (r / "skills" / "demo-review" / "SKILL.md")
        body.write_text(body.read_text() + "\nsee ancient-review for history\n")
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            gate(r)
        assert "G8" in buf.getvalue() and "ancient-review" in buf.getvalue(), "stale sibling name must warn G8"
        body.write_text(body.read_text().replace("\nsee ancient-review for history\n", ""))
        (r / "skills" / "demo-review" / "evals").mkdir()
        (r / "skills" / "demo-review" / "evals" / "evals.json").write_text('{"skill": "wrong-owner", "cases": [{"id": "t0", "prompt": "x", "expect": "trigger"}]}')
        code, _ = gate(r)
        assert code == 1, "owner-mismatched suite must fail G7"
        (r / "skills" / "demo-review" / "evals" / "evals.json").write_text(json.dumps({"skill": "demo-review", "cases": (
            [{"id": f"t{i}", "prompt": f"p{i}", "expect": "trigger"} for i in range(5)]
          + [{"id": f"n{i}", "prompt": f"m{i}", "expect": "no-trigger"} for i in range(3)])}))
        code, _ = gate(r)
        assert code == 0, "valid suite must restore a clean gate"
        # G4 js leg: a failing .mjs selftest must bite; a passing one must not flag
        import shutil as _sh
        if _sh.which("node"):
            js = r / "skills" / "demo-review" / "scripts"
            js.mkdir()
            (js / "demo-check.mjs").write_text("if (process.argv[2] === 'selftest') process.exit(1)\n")
            code, _ = gate(r)
            assert code == 1, "failing .mjs selftest must fail G4"
            (js / "demo-check.mjs").write_text("if (process.argv[2] === 'selftest') { console.log('ok'); process.exit(0) }\n")
            code, _ = gate(r)
            assert code == 0, "passing .mjs selftest must keep the gate clean"
            (js / "demo-skip.mjs").write_text("if (process.argv[2] === 'selftest') process.exit(2)\n")
            import io as _io, contextlib as _ctx
            _buf = _io.StringIO()
            with _ctx.redirect_stdout(_buf):
                code, _ = gate(r)
            assert code == 0 and "demo-skip.mjs" in _buf.getvalue(), "exit-2 selftest must SKIP disclosed, not fail"
            (js / "demo-skip.mjs").unlink()
        code, art = gate(r, package=True)
        assert code == 0 and art and art.exists(), "clean plugin must package"
        code, _ = gate(r, package=True)
        assert code == 1, "same-version repackage must FAIL G6"
        (r / "README.md").write_text("demo-plugin map: demo-review, claude-helper\n\nv0.1.0 · initial\n")
        (r / "skills" / "claude-helper").mkdir()
        (r / "skills" / "claude-helper" / "SKILL.md").write_text(skill_lint.GOOD_FIXTURE)
        code, _ = gate(r)
        assert code == 1, "reserved-word skill dir must fail via G3/F8"
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "Demo Plugin", "version": "1"}')
        code, _ = gate(r)
        assert code == 1, "bad manifest must fail G1"
    print("release_gate selftest · PASS · clean passes, packages once, refuses same-version, catches F8 and bad manifest")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    code, _ = gate(Path(args[0]).resolve(), package="--package" in args[1:])
    sys.exit(code)
