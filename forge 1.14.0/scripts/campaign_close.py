#!/usr/bin/env python3
"""campaign_close — verify a worktree campaign's PR actually closed clean, mechanically.

Usage:
  campaign_close.py <pr-number> [--repo <owner/repo>] [--gate <plugin-root> ...]
  campaign_close.py selftest

The ritual this replaces (run ~8 times by hand across 2026-07-16..17, with a real silent-failure
incident on every one of them — ten stale remote branches accumulated before anyone checked):

  C1 [FAIL] the PR is MERGED — never touch a branch behind an unmerged or closed-not-merged PR
  C2 [FAIL] the PR's remote head branch, if it still exists after the delete attempt, is the
            exact bug this script exists to catch: `gh pr merge --delete-branch` reported success
            while the branch stayed on the remote, ten times in a row, undetected until a manual
            `git branch -r` sweep
  C3 [WARN] any named gate root (--gate, repeatable) is not release_gate-clean at HEAD

The three checks are pure functions (`verify_*`) fed by real `gh`/`git` calls in `run()` —
selftest proves the checks bite on fixture inputs, never on live network state; the negative
control is exactly C2's "still present after delete" case, the incident this script encodes.

Exit 0 all clean, 1 on any FAIL (C3 warns, never fails — a red gate is the owner's call, not a
reason to leave a branch dangling).
"""
import json
import subprocess
import sys
from pathlib import Path


def verify_pr_merged(pr_info: dict):
    """pr_info: {'state': 'MERGED'|'OPEN'|'CLOSED', ...} from `gh pr view --json state`."""
    state = pr_info.get("state")
    if state != "MERGED":
        return False, f"PR state is {state}, not MERGED -> do not touch the branch"
    return True, "PR merged"


def verify_branch_deleted(existed_before: bool, exists_after: bool, branch: str):
    if not existed_before:
        return True, f"{branch} already absent from remote before this run"
    if exists_after:
        return False, (f"{branch} STILL on remote after the delete attempt -> the silent-failure "
                        "class (2026-07-16/17: ten branches this way); delete manually "
                        f"(`gh api -X DELETE repos/.../git/refs/heads/{branch}`) and re-run")
    return True, f"{branch} deleted and reverified gone"


def verify_gate_clean(gate_output_returncode: int, root: str):
    if gate_output_returncode != 0:
        return False, f"{root} is not release_gate-clean at HEAD -> fix before the next campaign"
    return True, f"{root} clean"


def _gh_json(args, repo=None):
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def _remote_branch_exists(branch: str, repo: str = None) -> bool:
    """Same auth path as the delete step, always — an anonymous check on a private repo
    fails closed (exit 128, empty stdout) and would misreport 'already absent', skipping the
    delete entirely (the ten-branch class, reincarnated through this exact auth seam)."""
    if repo:
        r = subprocess.run(["gh", "api", f"repos/{repo}/git/refs/heads/{branch}"],
                            capture_output=True, text=True)
        return r.returncode == 0
    r = subprocess.run(["git", "ls-remote", "--heads", "origin", branch],
                        capture_output=True, text=True)
    return bool(r.stdout.strip())


def run(pr_number: str, repo=None, gate_roots=None):
    findings = []
    ok_all = True

    pr = _gh_json(["pr", "view", pr_number, "--json", "state,headRefName,mergeCommit"], repo)
    ok, msg = verify_pr_merged(pr)
    findings.append(("C1", ok, msg))
    if not ok:
        ok_all = False
        _report(findings)
        return 1

    branch = pr["headRefName"]
    existed_before = _remote_branch_exists(branch, repo)
    if existed_before:
        del_cmd = ["gh", "api", "-X", "DELETE", f"repos/{repo}/git/refs/heads/{branch}"] if repo else \
                   ["git", "push", "origin", "--delete", branch]
        subprocess.run(del_cmd, capture_output=True, text=True)
    exists_after = _remote_branch_exists(branch, repo) if existed_before else False
    ok, msg = verify_branch_deleted(existed_before, exists_after, branch)
    findings.append(("C2", ok, msg))
    ok_all = ok_all and ok

    gate_script = Path(__file__).resolve().parent / "release_gate.py"
    for root in (gate_roots or []):
        gate = subprocess.run(
            ["python3", str(gate_script), root],
            capture_output=True, text=True)
        ok, msg = verify_gate_clean(gate.returncode, root)
        findings.append(("C3", ok, msg))  # C3 never flips ok_all — warn, not fail

    _report(findings)
    return 0 if ok_all else 1


def _report(findings):
    verdict = "FAIL" if any(not ok and code != "C3" for code, ok, _ in findings) else "clean"
    print(f"campaign_close · {verdict}")
    for code, ok, msg in findings:
        sev = "ok  " if ok else ("WARN" if code == "C3" else "FAIL")
        print(f"  {sev} {code}  {msg}")


def selftest():
    # C1
    ok, msg = verify_pr_merged({"state": "OPEN"})
    assert not ok and "not MERGED" in msg, "an open PR must never be treated as closeable"
    ok, _ = verify_pr_merged({"state": "MERGED"})
    assert ok, "a merged PR must pass C1"

    # C2 — the negative control: this exact case happened ten times, undetected, on 2026-07-16
    ok, msg = verify_branch_deleted(existed_before=True, exists_after=True, branch="worktree-x")
    assert not ok and "STILL on remote" in msg, "a branch surviving its own delete attempt must FAIL, not pass silently"
    ok, _ = verify_branch_deleted(existed_before=True, exists_after=False, branch="worktree-x")
    assert ok, "a branch confirmed gone after delete must pass"
    ok, _ = verify_branch_deleted(existed_before=False, exists_after=False, branch="worktree-x")
    assert ok, "a branch already absent needs no delete and must pass"

    # C3
    ok, msg = verify_gate_clean(1, "ui 0.1.0")
    assert not ok and "not release_gate-clean" in msg, "a red gate must be named, not swallowed"
    ok, _ = verify_gate_clean(0, "ui 0.1.0")
    assert ok, "a clean gate must pass"

    print("campaign_close selftest · PASS · merge/delete/gate checks bite, incl. the ten-branch "
          "silent-delete-failure negative control")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    pr_number = args[0]
    repo = None
    gate_roots = []
    i = 1
    while i < len(args):
        if args[i] == "--repo":
            repo = args[i + 1]; i += 2
        elif args[i] == "--gate":
            gate_roots.append(args[i + 1]); i += 2
        else:
            i += 1
    sys.exit(run(pr_number, repo, gate_roots))
