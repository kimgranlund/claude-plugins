#!/usr/bin/env python3
"""fleet_state.py — read-only cross-repo state collector for check-state's --fleet scope.

Usage:
  fleet_state.py --repos <path1,path2,...> [--trackers <path-to-json>]
                                    print the JSON snapshot (issues zero mutating git/gh command)
  fleet_state.py selftest           prove the classifiers on inline fixtures (no live gh/network)

No implicit repo discovery — every repo in scope is named explicitly (lld-0011 ruling 2, #620):
never `ListAgents`-style discovery, never a filesystem walk. Degrades gracefully per repo: an
unreachable path never aborts the run, it reports UNMEASURED with a reason and the other repos'
rows still render (Acceptance: "degrade gracefully when a listed repo is unreachable (UNMEASURED
row, never silent)").

Collects, per `--repos` entry:
  open_work        open issues / PRs / `in-flight`-labeled claims (`gh issue list`)
  marketplace      per-plugin repo-version vs. locally cached version directories under
                    `~/.claude/plugins/cache/<marketplace>/<plugin>/` — the #582 stale-copy case
                    (lld-0011 ruling 3). "not-a-source-repo" (N/A, never UNMEASURED) for a repo
                    with no `.claude-plugin/marketplace.json` of its own.
  citation_edges    OPEN issue bodies matching a cross-repo reference — `owner/repo#NN` or the
                    bare-repo shorthand `repo#NN` (same owner implied, e.g. `gen-ui-kit#1593`) —
                    a plain in-repo `#NN` never matches; each resolved once via `gh issue view`

`--trackers <path>` (optional): a JSON list of {"local": "owner/repo#NN", "upstream":
"owner/repo#NN"} platform-defect pairs; each side resolved via one `gh issue view` call.
Absent → the section reports "no trackers file given" — a disclosed scope choice, not a failure.

Exit: 0 snapshot printed (even with per-repo UNMEASURED rows) · 1 unexpected internal failure ·
2 usage error (missing/empty --repos, unparseable --trackers path).
Selftest: 0 proven · 1 a control failed.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Matches both this workspace's two citation shapes (verified against #620's own Links section):
# a bare repo name implying the SAME owner ("gen-ui-kit#1593") and a full owner/repo form
# ("anthropics/claude-code#87349"). A repo-name segment must start with a letter, so a plain
# in-repo "#42" (no repo-name prefix at all) never matches — that is not a cross-repo citation.
CITATION_RE = re.compile(r"\b(?:[\w.-]+/)?[A-Za-z][\w.-]*#\d+\b")


def _run(cmd, cwd=None, timeout=60):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def parse_args(argv):
    """argv after the script name. Returns {"repos": [...], "trackers": path-or-None} or None."""
    repos, trackers, i = None, None, 0
    while i < len(argv):
        a = argv[i]
        if a == "--repos":
            if i + 1 >= len(argv):
                return None
            repos = [p for p in argv[i + 1].split(",") if p]
            i += 2
        elif a == "--trackers":
            if i + 1 >= len(argv):
                return None
            trackers = argv[i + 1]
            i += 2
        else:
            return None
    if not repos:
        return None
    return {"repos": repos, "trackers": trackers}


def semver_tuple(v):
    """('3', '10', '0') -> (3, 10, 0); non-numeric parts sort last (never crash on odd dirnames)."""
    parts = []
    for p in v.split("."):
        try:
            parts.append((0, int(p)))
        except ValueError:
            parts.append((1, p))
    return tuple(parts)


def classify_drift(repo_version, cache_versions):
    """Returns one of: in-sync, stale-cache, repo-behind-cache. cache_versions: list[str]."""
    if not cache_versions:
        return "stale-cache"
    highest = max(cache_versions, key=semver_tuple)
    if repo_version not in cache_versions:
        # repo shipped a version the cache has never seen at all
        if semver_tuple(repo_version) > semver_tuple(highest):
            return "stale-cache"
        return "repo-behind-cache"
    if semver_tuple(highest) > semver_tuple(repo_version):
        return "repo-behind-cache"
    return "in-sync"


def cache_root():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / "plugins" / "cache"


def owner_repo_from_remote(root):
    url = _run(["git", "remote", "get-url", "origin"], cwd=root).strip()
    m = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def collect_open_work(root):
    issues = json.loads(_run(["gh", "issue", "list", "--state", "open", "--limit", "200",
                              "--json", "number,title,body,labels"], cwd=root))
    prs = json.loads(_run(["gh", "pr", "list", "--state", "open", "--limit", "100",
                           "--json", "number"], cwd=root))
    in_flight = [{"number": i["number"], "title": i["title"]} for i in issues
                 if any(lb["name"] == "in-flight" for lb in i.get("labels", []))]
    return {"issues_open": len(issues), "prs_open": len(prs), "in_flight": in_flight}, issues


def collect_marketplace(root, owner_repo):
    mkt_path = Path(root) / ".claude-plugin" / "marketplace.json"
    if not mkt_path.exists():
        return "not-a-source-repo"
    mkt = json.loads(mkt_path.read_text())
    name = mkt.get("name", Path(root).name)
    plugins = []
    for p in mkt.get("plugins", []):
        pname = p.get("name")
        source = p.get("source", f"./{pname}")
        plugin_json = Path(root) / source.lstrip("./") / ".claude-plugin" / "plugin.json"
        try:
            repo_version = json.loads(plugin_json.read_text()).get("version")
        except (OSError, json.JSONDecodeError):
            repo_version = None
        cache_dir = cache_root() / name / pname
        cache_versions = sorted((d.name for d in cache_dir.iterdir() if d.is_dir())) \
            if cache_dir.is_dir() else []
        status = classify_drift(repo_version, cache_versions) if repo_version else "UNMEASURED"
        plugins.append({"name": pname, "repo_version": repo_version,
                         "cache_versions": cache_versions, "status": status})
    return {"name": name, "plugins": plugins}


def resolve_ref(owner_repo, number):
    try:
        data = json.loads(_run(["gh", "issue", "view", str(number), "--repo", owner_repo,
                                "--json", "state,title,url"]))
        return data.get("state", "UNMEASURED")
    except (RuntimeError, json.JSONDecodeError):
        return "UNMEASURED"


def collect_citation_edges(issues, cache, default_owner):
    edges = []
    for i in issues:
        for m in CITATION_RE.findall(i.get("body") or ""):
            ref, _, num = m.rpartition("#")
            owner_repo = ref if "/" in ref else f"{default_owner}/{ref}"
            key = m
            if key not in cache:
                cache[key] = resolve_ref(owner_repo, num)
            edges.append({"from_issue": i["number"], "to": m, "target_state": cache[key]})
    return edges


def collect_repo(path, ref_cache):
    row = {"path": path, "reachable": False, "reason": None, "owner_repo": None,
           "open_work": None, "marketplace": None, "citation_edges": []}
    if not Path(path).is_dir():
        row["reason"] = "path not found"
        return row
    try:
        _run(["git", "rev-parse", "--git-dir"], cwd=path)
    except (RuntimeError, FileNotFoundError):
        row["reason"] = "not a git repo"
        return row
    owner_repo = owner_repo_from_remote(path)
    if not owner_repo:
        row["reason"] = "non-GitHub backend"
        return row
    row["owner_repo"] = owner_repo
    row["marketplace"] = collect_marketplace(path, owner_repo)
    auth = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=30)
    if auth.returncode != 0:
        row["reason"] = "gh unauthenticated"
        return row
    try:
        open_work, issues = collect_open_work(path)
    except (RuntimeError, json.JSONDecodeError) as e:
        row["reason"] = f"gh call failed: {e}"
        return row
    row["open_work"] = open_work
    default_owner = owner_repo.split("/", 1)[0]
    row["citation_edges"] = collect_citation_edges(issues, ref_cache, default_owner)
    row["reachable"] = True
    return row


def collect_trackers(path):
    if not path:
        return "no trackers file given"
    try:
        pairs = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return f"trackers file unreadable: {path}"
    out = []
    for pair in pairs:
        local_owner, _, local_num = pair["local"].rpartition("#")
        up_owner, _, up_num = pair["upstream"].rpartition("#")
        out.append({"local": pair["local"], "local_state": resolve_ref(local_owner, local_num),
                    "upstream": pair["upstream"],
                    "upstream_state": resolve_ref(up_owner, up_num)})
    return out


def collect(repos, trackers_path):
    ref_cache = {}
    rows = [collect_repo(p, ref_cache) for p in repos]
    return {"repos": rows, "trackers": collect_trackers(trackers_path)}


def selftest():
    fails = []
    # semver_tuple / classify_drift
    if classify_drift("3.10.0", ["3.9.7", "3.10.0"]) != "in-sync":
        fails.append("negative control: matching highest version not classified in-sync")
    if classify_drift("3.10.0", ["3.9.7"]) != "stale-cache":
        fails.append("negative control: repo version absent from cache not classified stale-cache")
    if classify_drift("3.9.0", ["3.9.7", "3.10.0"]) != "repo-behind-cache":
        fails.append("negative control: repo behind the cache not classified repo-behind-cache")
    if classify_drift("1.0.0", []) != "stale-cache":
        fails.append("reverse control: empty cache should read stale-cache, not in-sync")
    if classify_drift("2.9.0", ["2.10.0"]) != "repo-behind-cache":
        fails.append("negative control: '2.10.0' > '2.9.0' numerically must not string-sort wrong")
    # citation edges
    cache = {}
    issues = [{"number": 620, "body": "See gen-ui-kit#1593 and anthropics/claude-code#87349 for context."}]
    edges = collect_citation_edges_offline(issues, cache)
    if sorted(e["to"] for e in edges) != ["anthropics/claude-code#87349", "gen-ui-kit#1593"]:
        fails.append("negative control: cross-repo citation refs not both extracted")
    plain = [{"number": 621, "body": "See #42 for the plain in-repo ref (no owner/repo prefix)."}]
    edges2 = collect_citation_edges_offline(plain, cache)
    if edges2:
        fails.append("reverse control: bare #NN (no owner/repo) must not be treated as cross-repo")
    # marketplace row shape without a live repo (no I/O — collect_marketplace requires a real
    # path only when marketplace.json exists; absence is a pure filesystem check)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        if collect_marketplace(td, "x/y") != "not-a-source-repo":
            fails.append("negative control: repo with no marketplace.json must read not-a-source-repo")
    # parse_args
    if parse_args(["--repos", "/a,/b"]) != {"repos": ["/a", "/b"], "trackers": None}:
        fails.append("repo list parse wrong")
    if parse_args(["--repos", "/a", "--trackers", "/t.json"]) != {"repos": ["/a"], "trackers": "/t.json"}:
        fails.append("trackers flag parse wrong")
    if parse_args([]) is not None or parse_args(["--repos", ""]) is not None:
        fails.append("reverse control: empty/missing --repos must be a usage error")
    # collect_repo: unreachable path
    row = collect_repo("/definitely/not/a/real/path/xyz", {})
    if row["reachable"] or row["reason"] != "path not found":
        fails.append("negative control: nonexistent path must report reachable=false, reason set")
    # collect_trackers: no file given
    if collect_trackers(None) != "no trackers file given":
        fails.append("reverse control: absent trackers path must report the disclosed-scope string")
    if fails:
        print(f"fleet_state · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]; sys.exit(1)
    print("fleet_state · selftest ok · 0 fail / 0 warn"); sys.exit(0)


def collect_citation_edges_offline(issues, cache):
    """selftest-only variant: resolve_ref is never called (fixtures never hit the network) —
    every match here is asserted as extracted, not resolved; state left UNMEASURED by design."""
    edges = []
    for i in issues:
        for m in CITATION_RE.findall(i.get("body") or ""):
            edges.append({"from_issue": i["number"], "to": m, "target_state": "UNMEASURED"})
    return edges


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    parsed = parse_args(argv[1:])
    if parsed is None:
        print(__doc__); sys.exit(2)
    try:
        print(json.dumps(collect(parsed["repos"], parsed["trackers"]), indent=2))
    except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired,
            FileNotFoundError, NotADirectoryError, OSError) as e:
        print(f"fleet_state · FAIL · {e}"); sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
