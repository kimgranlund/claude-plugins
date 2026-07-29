#!/usr/bin/env python3
"""state_diff.py — checkpoint + delta for the check-state skill.

Usage:
  state_diff.py <git.json|-> <ticket.json|-> <doc.json|-> --checkpoint <path>
  state_diff.py selftest

Builds the combined id snapshot from the three collector outputs and diffs it against the
existing checkpoint. A collector that was UNMEASURED this run (exit 2: no gh, non-GitHub
backend, not a repo) passes `-` in its slot: its layers are recorded as unmeasured, and
transitions into/out of measurability are reported as `remeasured`, never as add/remove
noise. Absent checkpoint -> first_run: true. A corrupt checkpoint resets to first-run and
says so (`checkpoint_reset`). The delta prints even when the checkpoint write fails
(`checkpoint_saved: false`) — the write is attempted before printing, but never traps.

The checkpoint write is the ONE file write a check-state run performs
(decision-watcher's committed-.claude/ops pattern).

Exit: 0 delta printed · 1 unreadable input · 2 usage.
Selftest: 0 proven · 1 a control failed.
"""
import json
import sys
from pathlib import Path

SLOT_KEYS = {"git": ("branches", "worktrees", "stashes"),
             "ticket": ("issues", "prs"), "doc": ("docs",)}


def snapshot(git, ticket, doc):
    """Any collector arg may be None (unmeasured): its keys land in 'unmeasured'."""
    snap, unmeasured = {}, []
    for slot, data in (("git", git), ("ticket", ticket), ("doc", doc)):
        if data is None:
            unmeasured.extend(SLOT_KEYS[slot])
            continue
        if slot == "git":
            snap["branches"] = sorted(data.get("branches", {}).get("all", []))
            snap["worktrees"] = sorted(w["path"] for w in data.get("worktrees", []))
            snap["stashes"] = sorted(s["message"] for s in data.get("stashes", {}).get("all", []))
        elif slot == "ticket":
            snap["issues"] = sorted(data.get("issues", {}).get("numbers", []))
            snap["prs"] = sorted(data.get("prs", {}).get("numbers", []))
        else:
            snap["docs"] = sorted(i.get("id") or i["path"] for i in data.get("items", []))
    return {"snapshot": snap, "unmeasured": sorted(unmeasured)}


def diff(old, new):
    """old/new: {'snapshot': {...}, 'unmeasured': [...]}. Keys unmeasured on either
    side are 'remeasured'/'unmeasured' transitions, never add/remove noise."""
    out = {}
    old_un, new_un = set(old.get("unmeasured", [])), set(new.get("unmeasured", []))
    old_s, new_s = old.get("snapshot", {}), new.get("snapshot", {})
    for key in set(new_s) | set(old_s) | new_un | old_un:
        if key in new_un:
            if key not in old_un:
                out[key] = {"transition": "became unmeasured"}
            continue
        if key in old_un or key not in old_s:
            if key in old_un:
                out[key] = {"transition": "remeasured — no comparable baseline"}
            continue
        added = sorted(set(new_s.get(key, [])) - set(old_s.get(key, [])))
        removed = sorted(set(old_s.get(key, [])) - set(new_s.get(key, [])))
        if added or removed:
            out[key] = {"added": added, "removed": removed}
    return out


def run(paths, cp_path):
    """paths: three collector-JSON paths or '-'. Returns (result, exit_code)."""
    loaded = []
    for p in paths:
        if p == "-":
            loaded.append(None)
            continue
        try:
            loaded.append(json.loads(Path(p).read_text()))
        except (OSError, json.JSONDecodeError) as e:
            return {"error": f"unreadable input: {e}"}, 1
    new = snapshot(*loaded)
    cp = Path(cp_path)
    first_run, reset = not cp.exists(), None
    old = {}
    if not first_run:
        try:
            old = json.loads(cp.read_text())
        except (OSError, json.JSONDecodeError) as e:
            first_run, reset = True, f"corrupt checkpoint, reset: {e}"
    if old and "snapshot" not in old:  # pre-unmeasured-era shape
        old = {"snapshot": old, "unmeasured": []}
    result = {"first_run": first_run,
              "delta": {} if first_run else diff(old, new),
              "unmeasured": new["unmeasured"]}
    if reset:
        result["checkpoint_reset"] = reset
    try:
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(new, indent=2) + "\n")
        result["checkpoint_saved"] = True
    except OSError as e:
        result["checkpoint_saved"] = False
        result["checkpoint_error"] = str(e)
    return result, 0


def selftest():
    import tempfile
    fails = []
    git = {"branches": {"all": ["main", "new-work"]},
           "worktrees": [{"path": "/r"}], "stashes": {"all": []}}
    doc = {"items": [{"id": "TKT-0001", "path": "a.md"}, {"id": None, "path": "plan.md"}]}
    new = snapshot(git, {"issues": {"numbers": [1, 2]}, "prs": {"numbers": [9]}}, doc)
    if new["snapshot"]["docs"] != ["TKT-0001", "plan.md"] or new["unmeasured"]:
        fails.append("snapshot doc-id fallback / unmeasured wrong")
    old = {"snapshot": {"branches": ["main", "shipped"], "issues": [1], "prs": [9],
                        "worktrees": ["/r"], "stashes": [], "docs": ["TKT-0001", "plan.md"]},
           "unmeasured": []}
    d = diff(old, new)
    if d.get("branches") != {"added": ["new-work"], "removed": ["shipped"]}:
        fails.append("negative control: branch add/remove not caught")
    if d.get("issues") != {"added": [2], "removed": []}:
        fails.append("negative control: new issue not caught")
    if "prs" in d or "docs" in d:
        fails.append("reverse control: unchanged section reported as delta")
    if diff(new, new):
        fails.append("reverse control: identical snapshots produced a delta")
    # B1 fixture (audit 2026-07-29): unmeasured ticket slot — no add/remove noise
    part = snapshot(git, None, doc)
    if sorted(part["unmeasured"]) != ["issues", "prs"]:
        fails.append("unmeasured slot not recorded")
    d2 = diff(old, part)
    if d2.get("issues") != {"transition": "became unmeasured"} or "added" in d2.get("prs", {}):
        fails.append("negative control: unmeasured transition leaked as add/remove")
    d3 = diff(part, new)
    if d3.get("issues") != {"transition": "remeasured — no comparable baseline"}:
        fails.append("negative control: remeasured transition not labeled")
    with tempfile.TemporaryDirectory() as td:
        gp, tp, dp = (Path(td) / n for n in ("g.json", "t.json", "d.json"))
        gp.write_text(json.dumps(git)); dp.write_text(json.dumps(doc))
        tp.write_text(json.dumps({"issues": {"numbers": [1]}, "prs": {"numbers": []}}))
        cp = Path(td) / "ops" / "cp.json"
        r1, c1 = run([str(gp), str(tp), str(dp)], str(cp))
        if c1 != 0 or not r1["first_run"] or not r1["checkpoint_saved"]:
            fails.append("first-run roundtrip wrong")
        r2, _ = run([str(gp), "-", str(dp)], str(cp))
        if r2["first_run"] or r2["delta"].get("issues") != {"transition": "became unmeasured"}:
            fails.append("second-run unmeasured-sentinel path wrong")
        # M4 fixtures (audit 2026-07-29): corrupt checkpoint resets, never tracebacks;
        # unwritable checkpoint still prints the delta
        cp.write_text("{not json")
        r3, c3 = run([str(gp), str(tp), str(dp)], str(cp))
        if c3 != 0 or not r3["first_run"] or "checkpoint_reset" not in r3:
            fails.append("negative control: corrupt checkpoint not reset cleanly")
        r4, c4 = run([str(gp), str(tp), str(dp)], "/dev/null/nope/cp.json")
        if c4 != 0 or r4.get("checkpoint_saved") is not False or "delta" not in r4:
            fails.append("negative control: unwritable checkpoint lost the delta")
    if fails:
        print(f"state_diff · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]; sys.exit(1)
    print("state_diff · selftest ok · 0 fail / 0 warn"); sys.exit(0)


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    if len(argv) != 6 or argv[4] != "--checkpoint":
        print(__doc__); sys.exit(2)
    result, code = run(argv[1:4], argv[5])
    if code == 0:
        print(json.dumps(result, indent=2))
    else:
        print(f"state_diff · FAIL · {result['error']}")
    sys.exit(code)


if __name__ == "__main__":
    main(sys.argv)
