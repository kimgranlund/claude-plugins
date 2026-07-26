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
            `git branch -r` sweep. GitHub deletes refs ASYNCHRONOUSLY, so the verification read
            polls up to 4 times over ~3.5s (0.5s/1s/2s backoff) before declaring FAIL — a ref
            still propagating resolves to ok; a ref present after the full window is the real
            silent-failure class (incident 2026-07-26, issue #102: one instant read false-FAILed
            a deletion that had already succeeded, teaching the reader to shrug at C2)
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
import time
from pathlib import Path

# C2's retry budget: 4 observations spanning ~3.5s. Wide enough for GitHub's async ref deletion
# to propagate (the 2026-07-26 race resolved within one manual re-run, seconds later); narrow
# enough that a genuinely stranded branch still fails the run in under 4 seconds.
C2_POLL_DELAYS = (0.5, 1.0, 2.0)


def poll_until_gone(exists_fn, delays=C2_POLL_DELAYS, sleep=time.sleep):
    """Call exists_fn until it reports the ref gone or the delay budget is spent.
    Returns (final_exists, observations). Pure given injected exists_fn/sleep — the selftest
    feeds a scripted sequence and a no-op sleep, never the network."""
    if not exists_fn():
        return False, 1
    for n, delay in enumerate(delays, start=2):
        sleep(delay)
        if not exists_fn():
            return False, n
    return True, len(delays) + 1


def verify_pr_merged(pr_info: dict):
    """pr_info: {'state': 'MERGED'|'OPEN'|'CLOSED', ...} from `gh pr view --json state`."""
    state = pr_info.get("state")
    if state != "MERGED":
        return False, f"PR state is {state}, not MERGED -> do not touch the branch"
    return True, "PR merged"


def verify_branch_deleted(existed_before: bool, exists_after: bool, branch: str,
                          observations: int = 1):
    if not existed_before:
        return True, f"{branch} already absent from remote before this run"
    if exists_after:
        return False, (f"{branch} STILL on remote after the delete attempt and a "
                        f"{observations}-observation retry window -> the silent-failure "
                        "class (2026-07-16/17: ten branches this way); delete manually "
                        f"(`gh api -X DELETE repos/.../git/refs/heads/{branch}`) and re-run")
    lag = "" if observations <= 1 else f" (async deletion propagated by observation {observations})"
    return True, f"{branch} deleted and reverified gone{lag}"


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
    if existed_before:
        exists_after, observations = poll_until_gone(lambda: _remote_branch_exists(branch, repo))
    else:
        exists_after, observations = False, 0
    ok, msg = verify_branch_deleted(existed_before, exists_after, branch, observations)
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
    ok, msg = verify_branch_deleted(existed_before=True, exists_after=True, branch="worktree-x",
                                    observations=4)
    assert not ok and "STILL on remote" in msg, "a branch surviving its own delete attempt must FAIL, not pass silently"
    assert "retry window" in msg, "the FAIL must say the retry window was already spent"
    ok, _ = verify_branch_deleted(existed_before=True, exists_after=False, branch="worktree-x")
    assert ok, "a branch confirmed gone after delete must pass"
    ok, _ = verify_branch_deleted(existed_before=False, exists_after=False, branch="worktree-x")
    assert ok, "a branch already absent needs no delete and must pass"

    # C2 poll — the #102 race fixture: present on the first read, gone on a later one, resolves
    # ok instead of the false FAIL observed live on 2026-07-26 (PR #101's branch was mid-
    # propagation; the instant read FAILed, the manual re-delete got 422 already-gone).
    seq = iter([True, True, False])
    exists, obs = poll_until_gone(lambda: next(seq), sleep=lambda _: None)
    assert not exists and obs == 3, f"present-then-absent must resolve ok within the window: {obs}"
    ok, msg = verify_branch_deleted(True, exists, "worktree-x", obs)
    assert ok and "observation 3" in msg, f"a propagation-lag pass must disclose the lag: {msg}"

    # ...and a branch present through the ENTIRE window still fails — the retry must not have
    # turned the check off.
    exists, obs = poll_until_gone(lambda: True, sleep=lambda _: None)
    assert exists and obs == len(C2_POLL_DELAYS) + 1, "a stranded branch must exhaust the window"
    ok, _ = verify_branch_deleted(True, exists, "worktree-x", obs)
    assert not ok, "a genuinely undeleted branch must still FAIL after the retry window"

    # gone on the very first read: no sleeping at all (sleep raising proves it was never called)
    def boom(_): raise AssertionError("must not sleep when the first read already says gone")
    exists, obs = poll_until_gone(lambda: False, sleep=boom)
    assert not exists and obs == 1

    # C3
    ok, msg = verify_gate_clean(1, "screens")
    assert not ok and "not release_gate-clean" in msg, "a red gate must be named, not swallowed"
    ok, _ = verify_gate_clean(0, "screens")
    assert ok, "a clean gate must pass"

    print("campaign_close selftest · PASS · merge/delete/gate checks bite, incl. the ten-branch "
          "silent-delete-failure negative control and the #102 async-propagation race (lag "
          "resolves ok and is disclosed; a stranded branch still fails after the window)")
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
