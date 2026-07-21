#!/usr/bin/env python3
"""surface_map — the mechanical half of plugin partitioning.

Usage:
  surface_map.py map <root>                     emit the artifact graph as JSON (nodes + typed edges)
  surface_map.py check <partition.json> <root>  reconcile a partition manifest against the graph
  surface_map.py gaps <root>                    negative-space evidence: dangling kebab references
                                                (prose names matching no artifact) and the family
                                                matrix (per name-prefix group: standards / command /
                                                script / evals present or absent). Evidence for the
                                                skill's gap judgment — a listed absence is a
                                                question, never automatically a gap (anti-matrix)
  surface_map.py selftest                       prove the counters bite

`map` needs only frontmatter and structure: skills (name, dials, description), agents (name,
skills: preloads), hooks (commands), scripts. Edges: `mention` (a kebab token in one artifact's
text naming another artifact), `preload` (agent skills:), `script` (hook or skill referencing a
scripts/*.py). The graph is the evidence plan-plugin-split reasons over.

`check` validates a partition: every node assigned exactly once; plugin names kebab, reserved-word
free, and non-stuttering against member prefixes; every cross-plugin edge enumerated with counts
per plugin pair (the judgment about whether a seam is acceptable stays with the skill).

Exit: map always 0; check 0 clean/warn, 1 on any FAIL.
"""
import json
import re
import sys
from pathlib import Path

KEBAB_TOKEN = re.compile(r"\b([a-z]{3,}(?:-[a-z]{2,})+)\b")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("claude", "anthropic")


def build_map(root: Path):
    nodes, texts = [], {}
    for sk in sorted(root.glob("skills/*/SKILL.md")):
        t = sk.read_text(encoding="utf-8", errors="replace")
        fm = t.split("---")[1] if t.startswith("---") and t.count("---") >= 2 else ""
        dmi = (re.search(r"disable-model-invocation:\s*(\w+)", fm) or [None, "?"])[1]
        ui = (re.search(r"user-invocable:\s*(\w+)", fm) or [None, "?"])[1]
        nid = sk.parent.name
        nodes.append({"id": nid, "type": "skill", "dials": f"dmi={dmi},ui={ui}"})
        texts[nid] = t
    for ag in sorted(root.glob("agents/*.md")):
        t = ag.read_text(encoding="utf-8", errors="replace")
        nodes.append({"id": ag.stem, "type": "agent"})
        texts[ag.stem] = t
    for sc in sorted(root.glob("scripts/*.py")):
        nodes.append({"id": sc.name, "type": "script"})
    hooks = root / "hooks" / "hooks.json"
    if hooks.is_file():
        nodes.append({"id": "hooks.json", "type": "hooks"})
        texts["hooks.json"] = hooks.read_text(encoding="utf-8", errors="replace")

    skill_ids = {n["id"] for n in nodes if n["type"] == "skill"}
    script_ids = {n["id"] for n in nodes if n["type"] == "script"}
    edges = []
    for src, text in texts.items():
        for tok in set(KEBAB_TOKEN.findall(text)):
            if tok in skill_ids and tok != src:
                edges.append({"src": src, "dst": tok, "kind": "mention"})
        for sc in script_ids:
            if sc in text:
                edges.append({"src": src, "dst": sc, "kind": "script"})
        m = re.search(r"^skills:\s*\n((?:\s*-\s*.+\n)+)", text, re.M) or re.search(r"skills:\s*\[([^\]]+)\]", text)
        if m:
            for name in re.findall(r"[\w-]+", m.group(1)):
                if name in skill_ids:
                    edges.append({"src": src, "dst": name, "kind": "preload"})
    return {"root": str(root), "nodes": nodes, "edges": edges}


def check_partition(partition, graph):
    fails, warns = [], []
    inventory = {n["id"] for n in graph["nodes"]}
    assign = {}
    for plug in partition.get("plugins", []):
        name = plug.get("name", "")
        if not KEBAB_RE.match(name) or any(r in name for r in RESERVED):
            fails.append(f"plugin name `{name}` -> kebab-case, no reserved words")
        for member in plug.get("members", []):
            if member not in inventory:
                fails.append(f"plugin {name!r} claims unknown member {member!r}")
            elif member in assign:
                fails.append(f"member {member!r} assigned to both {assign[member]!r} and {name!r}")
            assign[member] = name
            first = member.split("-")[0].split(".")[0]
            if name == first:
                warns.append(f"stutter: plugin {name!r} + member {member!r} -> /{name}:{member}")
    orphans = inventory - set(assign)
    for o in sorted(orphans):
        fails.append(f"artifact {o!r} is assigned to no plugin -> every artifact needs a home")

    seams = {}
    for e in graph["edges"]:
        a, b = assign.get(e["src"]), assign.get(e["dst"])
        if a and b and a != b:
            seams.setdefault((a, b, e["kind"]), []).append(f"{e['src']}->{e['dst']}")
    seam_report = [{"from": k[0], "to": k[1], "kind": k[2], "count": len(v), "edges": v}
                   for k, v in sorted(seams.items())]
    hard = [s for s in seam_report if s["kind"] in ("preload", "script")]
    for s in hard:
        fails.append(f"{s['kind']} edge crosses plugins {s['from']} -> {s['to']} ({s['edges'][:2]}) -> "
                     "preloads and script paths cannot cross a plugin boundary; repartition or duplicate deliberately")
    return fails, warns, seam_report


def find_gaps(root: Path):
    graph = build_map(root)
    skill_ids = {n["id"] for n in graph["nodes"] if n["type"] == "skill"}
    all_ids = {n["id"] for n in graph["nodes"]}
    suffixes = {n.rsplit("-", 1)[-1] for n in skill_ids}
    dangling = {}
    for sk in sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md")):
        src = sk.parent.name if sk.name == "SKILL.md" else sk.stem
        for tok in set(KEBAB_TOKEN.findall(sk.read_text(encoding="utf-8", errors="replace"))):
            if tok not in all_ids and tok != src and tok.rsplit("-", 1)[-1] in suffixes:
                dangling.setdefault(tok, []).append(src)
    families = {}
    for s in skill_ids:
        families.setdefault(s.split("-")[0], set()).add(s)
    matrix = []
    for prefix, members in sorted(families.items()):
        if len(members) < 2 and not any((root / "skills" / m / "evals").is_dir() for m in members):
            continue
        row = {"family": prefix, "members": sorted(members),
               "has_standards": any(m.endswith("-standards") for m in members),
               "has_command": any("disable-model-invocation: true" in (root / "skills" / m / "SKILL.md").read_text(encoding="utf-8", errors="replace") for m in members),
               "has_script": any((root / "skills" / m / "scripts").is_dir() for m in members) or any(prefix in n["id"] for n in graph["nodes"] if n["type"] == "script"),
               "has_evals": any((root / "skills" / m / "evals" / "evals.json").is_file() for m in members)}
        matrix.append(row)
    return {"dangling_references": [{"name": k, "referenced_by": v} for k, v in sorted(dangling.items())],
            "family_matrix": matrix}


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        for name, body in [("alpha-forge", "uses `alpha-standards` and run_check.py"),
                           ("alpha-standards", "doctrine"),
                           ("beta-review", "NOT for forging (alpha-forge)")]:
            d = r / "skills" / name; d.mkdir(parents=True)
            (d / "SKILL.md").write_text(f"---\nname: {name}\ndisable-model-invocation: false\nuser-invocable: true\n---\n{body}")
        (r / "agents").mkdir(); (r / "agents" / "auditor.md").write_text("---\nname: auditor\nskills:\n  - alpha-standards\n---\nbody")
        (r / "scripts").mkdir(); (r / "scripts" / "run_check.py").write_text("x")
        g = build_map(r)
        kinds = {(e["src"], e["dst"], e["kind"]) for e in g["edges"]}
        assert ("alpha-forge", "alpha-standards", "mention") in kinds
        assert ("beta-review", "alpha-forge", "mention") in kinds
        assert ("auditor", "alpha-standards", "preload") in kinds
        assert ("alpha-forge", "run_check.py", "script") in kinds
        good = {"plugins": [{"name": "alpha", "members": ["alpha-forge", "alpha-standards", "auditor", "run_check.py"]},
                            {"name": "beta", "members": ["beta-review"]}]}
        fails, warns, seams = check_partition(good, g)
        assert not fails, f"good partition must pass, got {fails}"
        assert any(w.startswith("stutter") for w in warns), "alpha/alpha-forge stutter must warn"
        assert any(s["from"] == "beta" and s["to"] == "alpha" and s["kind"] == "mention" for s in seams)
        bad = {"plugins": [{"name": "alpha", "members": ["alpha-forge", "alpha-forge", "ghost"]},
                           {"name": "beta", "members": ["beta-review", "alpha-standards", "run_check.py"]}]}
        fails, _, _ = check_partition(bad, g)
        msgs = " | ".join(fails)
        assert "both" in msgs and "unknown member" in msgs and "assigned to no plugin" in msgs, msgs
        (r / "skills" / "alpha-forge" / "SKILL.md").write_text(
            (r / "skills" / "alpha-forge" / "SKILL.md").read_text() + "\nhandoff to alpha-review when decided\n")
        g2 = find_gaps(r)
        assert any(d["name"] == "alpha-review" for d in g2["dangling_references"]), "dangling handoff must surface"
        fams = {row["family"]: row for row in g2["family_matrix"]}
        assert "alpha" in fams and fams["alpha"]["has_standards"], "family matrix must see alpha-standards"
        cut = {"plugins": [{"name": "one", "members": ["alpha-forge", "beta-review", "run_check.py", "auditor"]},
                           {"name": "two", "members": ["alpha-standards"]}]}
        fails, _, _ = check_partition(cut, g)
        assert any("preload edge crosses" in f for f in fails), "cross-plugin preload must fail"
    print("surface_map selftest · PASS · graph extraction (mention/preload/script), reconciliation, "
          "stutter, hard-seam kills")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "map":
        print(json.dumps(build_map(Path(args[1]).resolve()), indent=2))
        sys.exit(0)
    if args[0] == "gaps":
        print(json.dumps(find_gaps(Path(args[1]).resolve()), indent=2))
        sys.exit(0)
    if args[0] == "check":
        graph = build_map(Path(args[2]).resolve())
        fails, warns, seams = check_partition(json.loads(Path(args[1]).read_text()), graph)
        print(f"surface_map check · {'FAIL' if fails else 'PASS'} · {len(fails)} fail / {len(warns)} warn / {len(seams)} cross-plugin seam(s)")
        for f in fails:
            print(f"  FAIL  {f}")
        for w in warns:
            print(f"  warn  {w}")
        for s in seams:
            print(f"  seam  {s['from']} -> {s['to']} ({s['kind']} ×{s['count']})")
        sys.exit(1 if fails else 0)
    print(__doc__); sys.exit(2)
