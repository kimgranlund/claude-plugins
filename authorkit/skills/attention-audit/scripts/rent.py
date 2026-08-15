#!/usr/bin/env python3
"""rent.py — measure an estate's always-on menu rent: skill + agent description sizes.

Skills carrying `disable-model-invocation: true` are zero-rent (excluded from the routable
figure, counted separately). Agent descriptions bill unconditionally. Skills and agents are
reported as SEPARATE figures, never blended (see the owning SKILL.md's separate-series rule).

Usage:
  python3 rent.py --target <estate-root> [--json]
  python3 rent.py selftest

Exit: 0 measured OK · 2 error (measurement scripts don't have a findings state).
"""
import argparse
import json
import os
import re
import sys

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def parse_frontmatter(text):
    """Minimal YAML subset: scalar fields, `>`/`>-`/`|` folded description, booleans."""
    m = FM_RE.match(text)
    if not m:
        return {}
    fm, out = m.group(1), {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        if val in (">", ">-", "|", "|-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or lines[i] == ""):
                block.append(lines[i].strip())
                i += 1
            out[key] = " ".join(b for b in block if b)
            continue
        out[key] = val.strip("'\"")
        i += 1
    return out


def is_true(v):
    return str(v).strip().lower() == "true"


def find_plugins(root):
    """Plugin roots (.claude-plugin/plugin.json) under root; else root itself as one estate."""
    plugins = []
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "dist", ".refactor-attic", ".claude")]
        if os.path.isfile(os.path.join(dirpath, ".claude-plugin", "plugin.json")):
            plugins.append(dirpath)
            dirnames[:] = []
    if not plugins:
        # bare estate: a .claude/skills tree or a plain skills/ dir
        plugins = [root]
    return sorted(plugins)


def measure_plugin(proot):
    row = {"plugin": os.path.basename(os.path.abspath(proot)),
           "routable_skills": 0, "routable_chars": 0,
           "zero_rent_skills": 0, "zero_rent_chars": 0,
           "agents": 0, "agent_chars": 0}
    skill_globs = [os.path.join(proot, "skills"), os.path.join(proot, ".claude", "skills")]
    for sdir in skill_globs:
        if not os.path.isdir(sdir):
            continue
        for name in sorted(os.listdir(sdir)):
            f = os.path.join(sdir, name, "SKILL.md")
            if not os.path.isfile(f):
                continue
            fm = parse_frontmatter(open(f, encoding="utf-8", errors="ignore").read())
            desc = fm.get("description", "") or ""
            if is_true(fm.get("disable-model-invocation", "false")):
                row["zero_rent_skills"] += 1
                row["zero_rent_chars"] += len(desc)
            else:
                row["routable_skills"] += 1
                row["routable_chars"] += len(desc)
    adir = os.path.join(proot, "agents")
    if os.path.isdir(adir):
        for name in sorted(os.listdir(adir)):
            if not name.endswith(".md"):
                continue
            fm = parse_frontmatter(
                open(os.path.join(adir, name), encoding="utf-8", errors="ignore").read())
            row["agents"] += 1
            row["agent_chars"] += len(fm.get("description", "") or "")
    return row


def run(target):
    rows = [measure_plugin(p) for p in find_plugins(target)]
    total = {"plugin": "ESTATE-TOTAL"}
    for k in ("routable_skills", "routable_chars", "zero_rent_skills",
              "zero_rent_chars", "agents", "agent_chars"):
        total[k] = sum(r[k] for r in rows)
    return {"target": os.path.abspath(target), "plugins": rows, "total": total,
            "est_tokens_routable": total["routable_chars"] // 4,
            "est_tokens_agents": total["agent_chars"] // 4}


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        def mk(path, text):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").write(text)
        p = os.path.join(td, "plug")
        mk(os.path.join(p, ".claude-plugin", "plugin.json"), "{}")
        mk(os.path.join(p, "skills", "a", "SKILL.md"),
           "---\nname: a\ndescription: >\n  ten chars.\ndisable-model-invocation: false\n---\nbody")
        mk(os.path.join(p, "skills", "b", "SKILL.md"),
           "---\nname: b\ndescription: command only desc\ndisable-model-invocation: true\n---\nbody")
        mk(os.path.join(p, "agents", "x.md"),
           "---\nname: x\ndescription: agent words here\n---\nbody")
        # negative control: no frontmatter → measured as zero-length description, not a crash
        mk(os.path.join(p, "skills", "c", "SKILL.md"), "no frontmatter at all\n")
        r = run(td)
        t = r["total"]
        assert t["routable_skills"] == 2, t          # a + c (c routable, empty desc)
        assert t["routable_chars"] == len("ten chars."), t
        assert t["zero_rent_skills"] == 1 and t["zero_rent_chars"] == len("command only desc"), t
        assert t["agents"] == 1 and t["agent_chars"] == len("agent words here"), t
        # negative control: the zero-rent skill must NOT be in the routable figure
        assert t["routable_chars"] < t["routable_chars"] + t["zero_rent_chars"]
    print("rent.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--target")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.target:
        print("rent.py: --target required (or `selftest`)", file=sys.stderr)
        return 2
    r = run(a.target)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        for row in r["plugins"] + [r["total"]]:
            print(f"{row['plugin']:24s} routable {row['routable_skills']:3d}/"
                  f"{row['routable_chars']:6d}ch  zero-rent {row['zero_rent_skills']:3d}/"
                  f"{row['zero_rent_chars']:6d}ch  agents {row['agents']:2d}/"
                  f"{row['agent_chars']:6d}ch")
        print(f"est tokens — routable skills ~{r['est_tokens_routable']:,}, "
              f"agents ~{r['est_tokens_agents']:,} (separate figures, never blended)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"rent.py error: {e}", file=sys.stderr)
        sys.exit(2)
