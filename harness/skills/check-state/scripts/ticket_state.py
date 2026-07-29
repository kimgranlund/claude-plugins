#!/usr/bin/env python3
"""ticket_state.py — read-only ticket/PR collector for the check-state skill.

Usage:
  ticket_state.py [<repo-root>] [--stale-days N]   collect via `gh` and print the JSON snapshot
  ticket_state.py selftest                          prove the classifiers on inline fixtures

No args defaults the root to `.` — a deliberate, disclosed deviation from the
no-args-prints-usage anatomy: the default target is meaningful for a collector.

Backend resolution (issue-sorter's pattern): a github.com remote uses the `gh` CLI;
any other backend (Linear, Jira, non-GitHub git host) exits 2 UNMEASURED with the
reason — an adapter gap is disclosed, never silently skipped. Unauthenticated `gh`
is also environmental -> exit 2 with a curated line, not a raw stderr dump.

Collects (open issues + PRs, last 30 merged PRs, remote heads, viewer login):
  issues  stale (> --stale-days without update, default 30) · unassigned · blocked-labeled
  prs     awaiting review · changes requested · failing CI · conflicting · draft ·
          mine_failing_ci (the viewer's own PRs with red CI) ·
          awaiting_my_review (viewer named in reviewRequests)
  merged_branch_survivors  merged PRs whose remote head branch still exists —
          the silent-delete-failure class campaign_close.py exists to kill

Exit: 0 snapshot printed · 1 gh/git failure · 2 usage, gh absent/unauthenticated,
or non-GitHub backend.
Selftest: 0 proven · 1 a control failed.
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone


def _run(cmd, cwd=None, timeout=120):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def _when(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def parse_args(argv):
    """argv after the script name. Returns (root, stale_days) or None on usage error.
    2026-07-29 audit fixture M1: `--stale-days 45` with no root must not eat 45 as the root."""
    root, stale_days, i = None, 30, 0
    while i < len(argv):
        a = argv[i]
        if a == "--stale-days":
            if i + 1 >= len(argv):
                return None
            try:
                stale_days = int(argv[i + 1])
            except ValueError:
                return None
            i += 2
        elif a.startswith("-"):
            return None
        elif root is None:
            root = a; i += 1
        else:
            return None
    return (root or ".", stale_days)


def classify_issues(issues, now, stale_days):
    out = {"numbers": [], "stale": [], "unassigned": [], "blocked": []}
    cutoff = now - timedelta(days=stale_days)
    for i in issues:
        n = i["number"]
        out["numbers"].append(n)
        if _when(i["updatedAt"]) < cutoff:
            out["stale"].append(n)
        if not i.get("assignees"):
            out["unassigned"].append(n)
        if any("blocked" in lb["name"].lower() for lb in i.get("labels", [])):
            out["blocked"].append(n)
    return out


def classify_prs(prs, viewer=None):
    """viewer: the authenticated login — makes 'mine'/'my review' measurable (audit M2)."""
    out = {"numbers": [], "awaiting_review": [], "changes_requested": [],
           "failing_ci": [], "conflicting": [], "drafts": [],
           "mine_failing_ci": [], "awaiting_my_review": []}
    for p in prs:
        n = p["number"]
        out["numbers"].append(n)
        mine = viewer is not None and (p.get("author") or {}).get("login") == viewer
        if p.get("isDraft"):
            out["drafts"].append(n)
        elif p.get("reviewDecision") in ("", None, "REVIEW_REQUIRED"):
            out["awaiting_review"].append(n)
        elif p.get("reviewDecision") == "CHANGES_REQUESTED":
            out["changes_requested"].append(n)
        checks = p.get("statusCheckRollup") or []
        failing = any((c.get("conclusion") or "").upper() in ("FAILURE", "ERROR", "TIMED_OUT")
                      for c in checks)
        if failing:
            out["failing_ci"].append(n)
            if mine:
                out["mine_failing_ci"].append(n)
        if p.get("mergeable") == "CONFLICTING":
            out["conflicting"].append(n)
        if viewer is not None and any((r.get("login") or r.get("name")) == viewer
                                      for r in p.get("reviewRequests") or []):
            out["awaiting_my_review"].append(n)
    return out


def find_survivors(merged_prs, remote_heads):
    """Merged PRs whose head branch still exists on the remote."""
    return [{"pr": p["number"], "branch": p["headRefName"]}
            for p in merged_prs if p.get("headRefName") in remote_heads]


def collect(root, stale_days):
    if not shutil.which("gh"):
        print("ticket_state · SKIP · `gh` CLI not installed (brew install gh)"); sys.exit(2)
    try:
        remotes = _run(["git", "remote", "-v"], cwd=root)
    except (RuntimeError, FileNotFoundError, NotADirectoryError):
        print(f"ticket_state · SKIP · not a git repository: {root}"); sys.exit(2)
    if "github.com" not in remotes:
        print("ticket_state · SKIP · non-GitHub backend — no adapter implemented "
              "(GitHub only; Linear/Jira are a disclosed gap)"); sys.exit(2)
    auth = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=30)
    if auth.returncode != 0:
        print("ticket_state · SKIP · `gh` is not authenticated (run `gh auth login`)"); sys.exit(2)
    try:
        viewer = json.loads(_run(["gh", "api", "user"], cwd=root)).get("login")
    except (RuntimeError, json.JSONDecodeError):
        viewer = None  # ownership classes stay empty; the rest still measures
    now = datetime.now(timezone.utc)
    issues = json.loads(_run(["gh", "issue", "list", "--state", "open", "--limit", "200",
                              "--json", "number,title,labels,assignees,updatedAt"], cwd=root))
    prs = json.loads(_run(["gh", "pr", "list", "--state", "open", "--limit", "100",
                           "--json", "number,title,author,isDraft,reviewDecision,mergeable,"
                           "statusCheckRollup,reviewRequests,headRefName,updatedAt"], cwd=root))
    merged = json.loads(_run(["gh", "pr", "list", "--state", "merged", "--limit", "30",
                              "--json", "number,headRefName"], cwd=root))
    heads = {ln.split("refs/heads/", 1)[1].strip()
             for ln in _run(["git", "ls-remote", "--heads", "origin"], cwd=root).splitlines()
             if "refs/heads/" in ln}
    return {"backend": "github", "stale_days": stale_days, "viewer": viewer,
            "issues": classify_issues(issues, now, stale_days),
            "prs": classify_prs(prs, viewer),
            "merged_branch_survivors": find_survivors(merged, heads)}


def selftest():
    fails = []
    now = datetime(2026, 7, 29, tzinfo=timezone.utc)
    issues = [
        {"number": 1, "updatedAt": "2026-05-01T00:00:00Z", "assignees": [], "labels": []},
        {"number": 2, "updatedAt": "2026-07-28T00:00:00Z", "assignees": [{"login": "kim"}],
         "labels": [{"name": "blocked: upstream"}]},
    ]
    ic = classify_issues(issues, now, 30)
    if ic["stale"] != [1] or ic["unassigned"] != [1]:
        fails.append("negative control: stale/unassigned issue not caught")
    if 2 in ic["stale"]:
        fails.append("reverse control: fresh issue flagged stale")
    if ic["blocked"] != [2]:
        fails.append("blocked-label detection wrong")
    prs = [
        {"number": 10, "isDraft": False, "reviewDecision": "REVIEW_REQUIRED",
         "author": {"login": "kim"}, "mergeable": "MERGEABLE",
         "statusCheckRollup": [{"conclusion": "FAILURE"}], "reviewRequests": []},
        {"number": 11, "isDraft": True, "reviewDecision": "", "author": {"login": "someone"},
         "mergeable": "CONFLICTING", "statusCheckRollup": [{"conclusion": "SUCCESS"}],
         "reviewRequests": [{"login": "kim"}]},
    ]
    pc = classify_prs(prs, viewer="kim")
    if pc["awaiting_review"] != [10] or pc["failing_ci"] != [10]:
        fails.append("negative control: awaiting-review/failing-CI PR not caught")
    if 11 in pc["awaiting_review"] or 11 in pc["failing_ci"]:
        fails.append("reverse control: draft/green PR misflagged")
    if pc["drafts"] != [11] or pc["conflicting"] != [11]:
        fails.append("draft/conflicting classification wrong")
    # M2 fixtures (audit 2026-07-29): ownership is measured, not guessed
    if pc["mine_failing_ci"] != [10]:
        fails.append("negative control: viewer's own failing-CI PR not caught")
    if pc["awaiting_my_review"] != [11]:
        fails.append("negative control: review-requested-of-viewer PR not caught")
    if classify_prs(prs, viewer="stranger")["mine_failing_ci"]:
        fails.append("reverse control: another author's PR claimed as viewer's")
    # M1 fixtures (audit 2026-07-29): flag value must not be eaten as the root
    if parse_args(["--stale-days", "45"]) != (".", 45):
        fails.append("negative control: --stale-days with no root misparsed")
    if parse_args(["/repo", "--stale-days", "7"]) != ("/repo", 7):
        fails.append("root + flag parse wrong")
    if parse_args(["--stale-days"]) is not None or parse_args(["--bogus"]) is not None:
        fails.append("reverse control: bad flag forms accepted")
    surv = find_survivors([{"number": 20, "headRefName": "left-behind"},
                           {"number": 21, "headRefName": "cleanly-deleted"}],
                          {"main", "left-behind"})
    if surv != [{"pr": 20, "branch": "left-behind"}]:
        fails.append("negative/reverse control: survivor detection wrong")
    if fails:
        print(f"ticket_state · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]; sys.exit(1)
    print("ticket_state · selftest ok · 0 fail / 0 warn"); sys.exit(0)


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    parsed = parse_args(argv[1:])
    if parsed is None:
        print(__doc__); sys.exit(2)
    root, stale_days = parsed
    try:
        print(json.dumps(collect(root, stale_days), indent=2))
    except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired,
            FileNotFoundError, NotADirectoryError) as e:
        print(f"ticket_state · FAIL · {e}"); sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
