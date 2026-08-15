#!/usr/bin/env python3
"""usage.py — join real usage telemetry against the estate roster.

Reads `skillUsage` from ~/.claude.json (or --skill-usage) and corrects the two false-positive
classes a naive name-match manufactures (both proven live 2026-08-15, both selftest fixtures):

  1. Rename lineage — a skill with zero hits under its current name may hold real hits under a
     pre-campaign name. Pass --lineage <json> ({"old-name": "current-name"}) to merge them.
  2. Preload-only consumption — a skill in an agent's `skills:` frontmatter list is consumed
     whenever that agent is dispatched and NEVER appears in skillUsage. Such skills are marked
     preloaded-by and excluded from the zero-evidence list.

Zero usage alone is never a retire verdict — the judgment layer (SKILL.md step 5) requires a
second signal. Missing/empty telemetry degrades to "no telemetry on this host", exit 0.

Usage:
  python3 usage.py --target <root> [--skill-usage <path>] [--lineage <path>] [--json]
  python3 usage.py selftest

Exit: 0 clean/degraded · 1 zero-evidence skills found · 2 error.
"""
import argparse
import json
import os
import re
import sys

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def frontmatter(path):
    m = FM_RE.match(open(path, encoding="utf-8", errors="ignore").read())
    return m.group(1) if m else ""


def roster(root):
    """{skill_name: {...}} plus agent preload edges, walked over plugin/estate layouts."""
    skills, preloads = {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "dist", ".refactor-attic", "worktrees")]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if fn == "SKILL.md":
                fm = frontmatter(path)
                nm = re.search(r"^name:\s*(\S+)", fm, re.M)
                name = (nm.group(1).strip("'\"") if nm else os.path.basename(dirpath))
                skills[name] = {"path": os.path.relpath(path, root)}
            elif fn.endswith(".md") and os.path.basename(dirpath) == "agents":
                fm = frontmatter(path)
                anm = re.search(r"^name:\s*(\S+)", fm, re.M)
                agent = anm.group(1).strip("'\"") if anm else fn[:-3]
                sm = re.search(r"^skills:\s*\n((?:\s+-\s+.*\n?)+)", fm, re.M)
                inline = re.search(r"^skills:\s*\[(.*?)\]", fm, re.M)
                names = []
                if sm:
                    names = [x.strip("- '\"\t ") for x in sm.group(1).strip().split("\n")]
                elif inline:
                    names = [x.strip(" '\"") for x in inline.group(1).split(",") if x.strip()]
                for s in names:
                    preloads.setdefault(s.split(":")[-1], []).append(agent)
    return skills, preloads


def join(skills, preloads, skill_usage, lineage):
    # fold usage through lineage: hits under an old name credit the current name
    usage = {}
    for key, rec in (skill_usage or {}).items():
        cur = lineage.get(key, key)
        cur_short = cur.split(":")[-1]
        u = usage.setdefault(cur_short, {"usageCount": 0, "lastUsedAt": 0, "as": []})
        u["usageCount"] += int(rec.get("usageCount", 0) or 0)
        u["lastUsedAt"] = max(u["lastUsedAt"], int(rec.get("lastUsedAt", 0) or 0))
        u["as"].append(key)
    rows, zero = [], []
    for name in sorted(skills):
        u = usage.get(name)
        vias = preloads.get(name, [])
        row = {"skill": name,
               "usageCount": (u or {}).get("usageCount", 0),
               "lastUsedAt": (u or {}).get("lastUsedAt", 0),
               "counted_as": (u or {}).get("as", []),
               "preloaded_by": vias}
        rows.append(row)
        if row["usageCount"] == 0 and not vias:
            zero.append(name)
    return rows, zero


def selftest():
    skills = {"save-lessons": {}, "dispatch-ticket": {}, "truly-dead": {}}
    preloads = {"dispatch-ticket": ["build-lead"]}
    skill_usage = {"knowledge-harvest": {"usageCount": 50, "lastUsedAt": 5},
                   "save-lessons": {"usageCount": 8, "lastUsedAt": 9}}
    lineage = {"knowledge-harvest": "save-lessons"}
    rows, zero = join(skills, preloads, skill_usage, lineage)
    by = {r["skill"]: r for r in rows}
    # fixture 1 (lineage): old-name hits merge — save-lessons is NOT zero-evidence
    assert by["save-lessons"]["usageCount"] == 58, by["save-lessons"]
    assert "save-lessons" not in zero
    # fixture 2 (preload): dispatch-ticket has no skillUsage but IS preloaded — not zero
    assert by["dispatch-ticket"]["usageCount"] == 0 and "dispatch-ticket" not in zero
    # positive control: the truly dead skill IS reported
    assert zero == ["truly-dead"], zero
    # negative control (naive method would fail this): WITHOUT lineage, save-lessons
    # undercounts — proves the lineage merge is load-bearing, not decorative
    _, zero_naive = join({"save-lessons2": {}}, {}, {"old-nm": {"usageCount": 9}}, {})
    assert zero_naive == ["save-lessons2"]
    # degraded: empty telemetry → every unpreloaded skill zero, no crash
    rows2, zero2 = join(skills, preloads, {}, {})
    assert set(zero2) == {"save-lessons", "truly-dead"} and len(rows2) == 3
    print("usage.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--target", "--estate", dest="estate",
                    help="estate root (--estate kept as an alias)")
    ap.add_argument("--skill-usage", default=os.path.expanduser("~/.claude.json"))
    ap.add_argument("--lineage")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.estate:
        print("usage.py: --target required (or `selftest`)", file=sys.stderr)
        return 2
    skills, preloads = roster(a.estate)
    su = {}
    if os.path.isfile(a.skill_usage):
        try:
            su = json.load(open(a.skill_usage)).get("skillUsage", {}) or {}
        except (json.JSONDecodeError, ValueError):
            su = {}
    lineage = json.load(open(a.lineage)) if a.lineage else {}
    rows, zero = join(skills, preloads, su, lineage)
    degraded = not su
    out = {"telemetry": "none on this host" if degraded else a.skill_usage,
           "lineage_map": a.lineage or "none supplied",
           "skills": rows, "zero_evidence": zero}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"telemetry: {out['telemetry']} · lineage: {out['lineage_map']}")
        for r in rows:
            via = f" preloaded-by {','.join(r['preloaded_by'])}" if r["preloaded_by"] else ""
            print(f"{r['skill']:32s} {r['usageCount']:5d} uses{via}")
        print(f"zero-evidence (post-correction): {len(zero)}")
    if degraded:
        return 0
    return 1 if zero else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"usage.py error: {e}", file=sys.stderr)
        sys.exit(2)
