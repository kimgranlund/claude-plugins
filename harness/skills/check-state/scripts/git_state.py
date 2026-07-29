#!/usr/bin/env python3
"""git_state.py — read-only git work-state collector for the check-state skill.

Usage:
  git_state.py [<repo-root>]     print the JSON snapshot (runs no mutating git command)
  git_state.py selftest          prove the classifiers on inline fixtures

No args defaults the root to `.` — a deliberate, disclosed deviation from the
no-args-prints-usage anatomy: the default target is meaningful for a collector.

Collects:
  branches   merged into the default branch but not deleted · upstream gone ·
             ahead/behind/diverged · no upstream
  worktrees  from `git worktree list --porcelain`: prunable, locked, dirty
  stashes    every stash; sync_main's "sync_main quarantine" entries flagged
             separately (they are blocked-on-you items)

Exit: 0 snapshot printed · 1 unexpected git failure · 2 usage / not a git repo.
Selftest: 0 proven · 1 a control failed.
"""
import json
import re
import subprocess
import sys

QUARANTINE_LABEL = "sync_main quarantine"


def _run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def classify_branches(rows, merged_names, default_branch, in_use=frozenset()):
    """rows: (name, upstream, track) from for-each-ref; track like '[ahead 2, behind 1]',
    '[gone]', or ''. merged_names: branches fully merged into the default branch.
    in_use: branches checked out in a worktree — never delete candidates."""
    out = {"all": [], "merged_undeleted": [], "gone_upstream": [],
           "ahead": [], "behind": [], "diverged": [], "no_upstream": []}
    for name, upstream, track in rows:
        out["all"].append(name)
        if name == default_branch:
            continue
        if name in merged_names and name not in in_use:
            out["merged_undeleted"].append(name)
        if not upstream:
            out["no_upstream"].append(name)
            continue
        if "[gone]" in track:
            out["gone_upstream"].append(name)
            continue
        a = re.search(r"ahead (\d+)", track)
        b = re.search(r"behind (\d+)", track)
        if a and b:
            out["diverged"].append({"name": name, "ahead": int(a.group(1)), "behind": int(b.group(1))})
        elif a:
            out["ahead"].append({"name": name, "ahead": int(a.group(1))})
        elif b:
            out["behind"].append({"name": name, "behind": int(b.group(1))})
    return out


def parse_worktrees(porcelain):
    """Parse `git worktree list --porcelain` into [{path, branch, prunable, locked, detached}]."""
    wts, cur = [], None
    for line in porcelain.splitlines():
        if line.startswith("worktree "):
            cur = {"path": line[9:], "branch": None, "prunable": False,
                   "locked": False, "detached": False}
            wts.append(cur)
        elif cur is None:
            continue
        elif line.startswith("branch "):
            cur["branch"] = line[7:].replace("refs/heads/", "")
        elif line.startswith("prunable"):
            cur["prunable"] = True
        elif line.startswith("locked"):
            cur["locked"] = True
        elif line == "detached":
            cur["detached"] = True
    return wts


def classify_stashes(rows):
    """rows: 'stash@{n}|message' lines. Quarantine stashes carry sync_main's label."""
    all_, quarantine = [], []
    for row in rows:
        if not row.strip():
            continue
        ref, _, msg = row.partition("|")
        entry = {"ref": ref, "message": msg}
        all_.append(entry)
        if QUARANTINE_LABEL in msg:
            quarantine.append(entry)
    return {"all": all_, "quarantine": quarantine}


def collect(root):
    try:
        _run(["git", "rev-parse", "--git-dir"], cwd=root)
    except RuntimeError:
        print(f"git_state · SKIP · not a git repository: {root}"); sys.exit(2)
    try:
        head = _run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], cwd=root).strip()
        default = head.split("/", 1)[1] if "/" in head else head
    except RuntimeError:
        default = "main"
    rows = []
    fmt = "%(refname:short)\t%(upstream:short)\t%(upstream:track)"
    for line in _run(["git", "for-each-ref", "refs/heads", f"--format={fmt}"], cwd=root).splitlines():
        parts = (line.split("\t") + ["", ""])[:3]
        rows.append(tuple(parts))
    try:
        merged = {ln.strip().lstrip("*+ ") for ln in
                  _run(["git", "branch", "--merged", default], cwd=root).splitlines() if ln.strip()}
    except RuntimeError:
        merged = set()
    wts = parse_worktrees(_run(["git", "worktree", "list", "--porcelain"], cwd=root))
    for wt in wts:
        try:
            wt["dirty"] = bool(_run(["git", "-C", wt["path"], "status", "--porcelain"]).strip())
        except RuntimeError:
            wt["dirty"] = None  # path gone -> prunable already says so
    in_use = frozenset(wt["branch"] for wt in wts if wt["branch"])
    stashes = classify_stashes(
        _run(["git", "stash", "list", "--format=%gd|%s"], cwd=root).splitlines())
    return {"default_branch": default,
            "branches": classify_branches(rows, merged, default, in_use),
            "worktrees": wts, "stashes": stashes}


def selftest():
    fails = []
    rows = [("main", "origin/main", ""),
            ("done-work", "origin/done-work", ""),          # merged, undeleted -> must bite
            ("old-pr", "origin/old-pr", "[gone]"),
            ("wip", "origin/wip", "[ahead 2, behind 1]"),
            ("local-only", "", "")]
    b = classify_branches(rows, {"main", "done-work"}, "main")
    if b["merged_undeleted"] != ["done-work"]:
        fails.append("negative control: merged-but-undeleted branch not caught")
    if "main" in b["merged_undeleted"]:
        fails.append("reverse control: default branch flagged as merged-undeleted")
    b2 = classify_branches(rows, {"main", "done-work"}, "main", in_use=frozenset({"done-work"}))
    if b2["merged_undeleted"]:
        fails.append("reverse control (2026-07-29 incident): branch checked out in a "
                     "worktree offered as a delete candidate")
    if b["gone_upstream"] != ["old-pr"] or b["no_upstream"] != ["local-only"]:
        fails.append("gone/no-upstream classification wrong")
    if b["diverged"] != [{"name": "wip", "ahead": 2, "behind": 1}]:
        fails.append("diverged parse wrong")
    porcelain = ("worktree /repo\nHEAD abc\nbranch refs/heads/main\n\n"
                 "worktree /repo/.claude/worktrees/dead\nHEAD def\n"
                 "branch refs/heads/dead\nprunable gitdir file points nowhere\n")
    wts = parse_worktrees(porcelain)
    if not (len(wts) == 2 and wts[1]["prunable"] and wts[1]["branch"] == "dead"):
        fails.append("negative control: prunable worktree not caught")
    if wts[0]["prunable"]:
        fails.append("reverse control: healthy worktree flagged prunable")
    st = classify_stashes(["stash@{0}|On main: sync_main quarantine",
                           "stash@{1}|WIP on feature: tinkering"])
    if len(st["quarantine"]) != 1 or st["quarantine"][0]["ref"] != "stash@{0}":
        fails.append("negative control: quarantine stash not caught")
    if len(st["all"]) != 2:
        fails.append("reverse control: plain stash miscounted")
    if fails:
        print(f"git_state · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]; sys.exit(1)
    print("git_state · selftest ok · 0 fail / 0 warn"); sys.exit(0)


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    root = argv[1] if len(argv) > 1 else "."
    if root.startswith("-"):
        print(__doc__); sys.exit(2)
    try:
        print(json.dumps(collect(root), indent=2))
    except (RuntimeError, subprocess.TimeoutExpired,
            FileNotFoundError, NotADirectoryError) as e:
        print(f"git_state · FAIL · {e}"); sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
