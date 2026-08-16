#!/usr/bin/env python3
"""version_claim_check — detect a colliding cross-PR plugin-version claim, mechanically.

Usage:
  version_claim_check.py <plugin-root> [--repo <owner/repo>]
  version_claim_check.py selftest

Encodes the rule in `big-change-git-rules/references/who-ships-what.md`'s "Cross-PR
version-claim coordination" section: ONE version-bumping build in flight per plugin at a time.
`release_gate.py` and CI both run scoped to a single PR's own worktree/checkout and structurally
cannot see a sibling PR's claim; `campaign_close.py` runs post-merge, too late to prevent a
collision. This is the pre-merge, coordinator-run check that CAN see across PRs: it lists every
OPEN PR touching `<plugin-root>/.claude-plugin/plugin.json`, reads each one's claimed
`"version"`, and compares against the version already on `main`.

  V1 [FAIL] more than one OPEN PR claims a version bump for the same plugin at once — the "one
            build in flight per plugin" rule itself; the later claimant should stack its ledger
            entry onto the earlier PR's predecessor once it merges, not race it
  V2 [FAIL] an open PR's claimed version is <= the version already on `main` — a stale claim
            authored against an older `main`, needing a rebase-and-rebump (PR #284's
            `3.6.2 -> 3.6.2` collision with #289, merged mid-flight, 2026-08-16)

Exit 0 clean (0 or 1 open claim, and any single claim > main's version), 1 on V1/V2, 2 on a
usage error or an unreadable `main` manifest (never silently reads as clean).

Network: `run()` calls `gh api`/`gh pr list` live — by design, same as `campaign_close.py`'s own
`_gh_json`. `selftest` never touches the network; every check function it proves
(`parse_version`, `version_tuple`, `find_claiming_prs`, `check_collision`) is pure, fed fixture
data only.
"""
import base64
import json
import re
import subprocess
import sys


def parse_args(args):
    """Returns (plugin_root, repo). Raises ValueError on any unrecognized token or a flag
    missing its value — the #188-class silent-argument-swallowing defect this house style
    always rejects rather than risks."""
    if not args:
        raise ValueError("plugin-root is required")
    plugin_root = args[0]
    repo = None
    i = 1
    while i < len(args):
        flag = args[i]
        if flag != "--repo":
            raise ValueError(f"unrecognized argument: {flag!r}")
        if i + 1 >= len(args):
            raise ValueError("--repo requires a value")
        repo = args[i + 1]
        i += 2
    return plugin_root, repo


def parse_version(plugin_json_text: str):
    """Pure: extract the "version" field from a plugin.json's raw text. None if absent or
    unparsable — an unreadable manifest is a finding elsewhere, not this script's job."""
    try:
        value = json.loads(plugin_json_text).get("version")
        if value:
            return value
    except (json.JSONDecodeError, AttributeError):
        pass
    m = re.search(r'"version"\s*:\s*"([^"]+)"', plugin_json_text)
    return m.group(1) if m else None


def version_tuple(v: str):
    """Pure: '3.8.6' -> (3, 8, 6). A non-numeric segment maps to -1 so a malformed version
    never silently outranks a well-formed one in a comparison."""
    return tuple(int(seg) if seg.isdigit() else -1 for seg in v.split("."))


def find_claiming_prs(prs: list, plugin_root: str) -> list:
    """Pure: which open PRs (the `gh pr list --json number,url,headRefName,files` shape) touch
    this plugin's own manifest at all."""
    target = f"{plugin_root.rstrip('/')}/.claude-plugin/plugin.json"
    out = []
    for pr in prs:
        paths = {f.get("path") for f in pr.get("files", [])}
        if target in paths:
            out.append(pr)
    return out


def check_collision(main_version: str, claims: list):
    """claims: [{'number':.., 'url':.., 'version': '<claimed or None>'}, ...] — already
    resolved, no network here. Returns (ok, findings) where findings is [(code, ok, msg), ...]."""
    findings = []
    ok_all = True

    if len(claims) > 1:
        who = ", ".join(f"#{c['number']} ({c.get('version') or 'unreadable'})" for c in claims)
        findings.append(("V1", False,
                          f"{len(claims)} open PRs claim a version bump for this plugin at "
                          f"once: {who} -> only ONE version-bumping build may be in flight per "
                          "plugin; the later claimant should stack its ledger entry onto the "
                          "earlier PR's predecessor once it merges, not race it"))
        ok_all = False
    elif claims:
        findings.append(("V1", True, f"exactly one open claim (#{claims[0]['number']})"))
    else:
        findings.append(("V1", True, "no open PR claims a version bump for this plugin"))

    for c in claims:
        claimed = c.get("version")
        if claimed is None:
            findings.append(("V2", False, f"#{c['number']}'s claimed version is unreadable"))
            ok_all = False
            continue
        if version_tuple(claimed) <= version_tuple(main_version):
            findings.append(("V2", False,
                              f"#{c['number']} claims {claimed}, <= main's {main_version} -> "
                              "stale claim, rebase and rebump before merge"))
            ok_all = False
        else:
            findings.append(("V2", True,
                              f"#{c['number']} claims {claimed} > main's {main_version}"))

    return ok_all, findings


def _gh_json(args, repo=None):
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def _resolve_repo(repo):
    if repo:
        return repo
    r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh repo view failed: {r.stderr.strip()}")
    return r.stdout.strip()


def _file_at_ref(repo: str, path: str, ref: str) -> str:
    r = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}?ref={ref}", "--jq", ".content"],
                        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh api contents {path}@{ref} failed: {r.stderr.strip()}")
    return base64.b64decode(r.stdout.strip()).decode()


def run(plugin_root: str, repo=None):
    repo = _resolve_repo(repo)
    path = f"{plugin_root.rstrip('/')}/.claude-plugin/plugin.json"

    main_version = parse_version(_file_at_ref(repo, path, "main"))
    if main_version is None:
        _report(False, [("V0", False, f"{path} on main has no readable \"version\" field")])
        return 2

    prs = _gh_json(["pr", "list", "--state", "open", "--json", "number,url,headRefName,files"], repo)
    claiming = find_claiming_prs(prs, plugin_root)
    claims = [
        {"number": pr["number"], "url": pr["url"],
         "version": parse_version(_file_at_ref(repo, path, pr["headRefName"]))}
        for pr in claiming
    ]

    ok, findings = check_collision(main_version, claims)
    _report(ok, findings)
    return 0 if ok else 1


def _report(ok, findings):
    print(f"version_claim_check · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg in findings:
        print(f"  {'ok  ' if item_ok else 'FAIL'} {code}  {msg}")


def selftest():
    # parse_version — valid JSON, the regex fallback on malformed JSON, and total garbage
    assert parse_version('{"name": "x", "version": "1.2.3"}') == "1.2.3"
    assert parse_version('{"name": "x", "version": "1.2.3",}') == "1.2.3", \
        "a trailing comma (invalid JSON) must still resolve via the regex fallback"
    assert parse_version("not json at all") is None

    # version_tuple — a malformed segment must sort LAST, never silently win
    assert version_tuple("3.8.6") == (3, 8, 6)
    assert version_tuple("3.8.6") > version_tuple("3.8.x"), \
        "a malformed segment must never silently outrank a well-formed version"

    # find_claiming_prs — the filter must match on the exact manifest path, not just any file
    # under the plugin
    prs = [
        {"number": 1, "files": [{"path": "harness/.claude-plugin/plugin.json"}]},
        {"number": 2, "files": [{"path": "harness/README.md"}]},
        {"number": 3, "files": [{"path": "teamwork/.claude-plugin/plugin.json"}]},
    ]
    claiming = find_claiming_prs(prs, "harness")
    assert [p["number"] for p in claiming] == [1], \
        f"only the PR touching harness's own manifest must match: {claiming}"

    # check_collision V2 — the #284 negative control: a claim reissued at the SAME version
    # already on main (the exact 3.6.2 -> 3.6.2 collision with #289, 2026-08-16) must FAIL
    ok, findings = check_collision("3.6.2", [{"number": 284, "url": "u", "version": "3.6.2"}])
    assert not ok, "a claim equal to main's current version must FAIL, not pass"
    assert any(code == "V2" and not f_ok and "stale claim" in msg for code, f_ok, msg in findings)

    # check_collision V2 — reverse control: a genuine forward bump passes
    ok, findings = check_collision("3.6.2", [{"number": 284, "url": "u", "version": "3.6.3"}])
    assert ok, "a claim strictly ahead of main must pass"

    # check_collision V1 — two simultaneous open claims on the same plugin must FAIL, even
    # when both individually look like forward bumps (the actual failure mode: TWO builds in
    # flight, not a bad version number)
    ok, findings = check_collision(
        "3.6.2",
        [{"number": 284, "url": "u1", "version": "3.6.3"},
         {"number": 289, "url": "u2", "version": "3.6.3"}])
    assert not ok, "two concurrent open claims on one plugin must FAIL regardless of version math"
    assert any(code == "V1" and not f_ok for code, f_ok, _ in findings)

    # check_collision — reverse control: zero or exactly one open claim is the healthy default
    ok, findings = check_collision("3.6.2", [])
    assert ok, "no open claim at all must pass"
    ok, findings = check_collision("3.6.2", [{"number": 1, "url": "u", "version": "3.6.3"}])
    assert ok, "exactly one forward-bumping claim must pass"

    # check_collision — an unreadable claimed version must FAIL, never be skipped silently
    ok, findings = check_collision("3.6.2", [{"number": 1, "url": "u", "version": None}])
    assert not ok, "an unreadable claimed version must FAIL, not be silently ignored"

    # parse_args — the #188-class negative control: an unrecognized token, and a flag missing
    # its value, must both be rejected rather than silently swallowed
    root, repo = parse_args(["harness", "--repo", "o/r"])
    assert (root, repo) == ("harness", "o/r")
    root, repo = parse_args(["harness"])
    assert (root, repo) == ("harness", None), "a bare plugin-root with no flags must parse"
    try:
        parse_args(["harness", "--bogus", "x"])
        raise AssertionError("an unrecognized flag must be rejected, not silently swallowed")
    except ValueError as e:
        assert "--bogus" in str(e)
    try:
        parse_args(["harness", "--repo"])
        raise AssertionError("a flag missing its value must be a clean error, not an IndexError")
    except ValueError as e:
        assert "--repo" in str(e)
    try:
        parse_args([])
        raise AssertionError("no plugin-root at all must be a clean error")
    except ValueError:
        pass

    print("version_claim_check selftest · PASS · V1 (two concurrent claims) and V2 (a claim at "
          "or behind main's version, incl. the #284/#289 3.6.2->3.6.2 negative control) both "
          "bite; single/zero forward claims and parse_args' #188-class controls all pass clean")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    try:
        plugin_root, repo = parse_args(argv)
    except ValueError as e:
        print(f"version_claim_check: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(run(plugin_root, repo))
    except RuntimeError as e:
        print(f"version_claim_check: {e}", file=sys.stderr)
        sys.exit(2)
