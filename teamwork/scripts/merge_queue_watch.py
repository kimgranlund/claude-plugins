#!/usr/bin/env python3
"""merge_queue_watch — one consolidated green/pending/failed line across every open PR head.

Usage:
  merge_queue_watch.py [--repo <owner/repo>]
  merge_queue_watch.py selftest

Replaces per-PR `waitpr`-style polling (two feed events per PR per wave — a "still waiting"
notice, then a merge notice) with ONE consolidated line per invocation, gh#713's marshal
feed-noise-reduction lever 2. Deliberately never `gh pr checks <pr> --watch` — that command's
exit code lies on non-terminal/failed states (`teamwork:fleet-rules` Section 4's "Merge-on-green"
bullet: #551 bit three live merges, #530/#546/#549). The real pass condition is a `check-runs`
REST query against each PR's own head SHA, same as `dispatch-ticket`'s own step 1b already
mechanizes — this script batches that query across every open PR in one wave instead of one PR
at a time.

Output — one line, PR numbers per bucket, `none` when a bucket is empty:
  green: #701 #705 / pending: #710 / failed: #698

Classification per PR (any check-run list, mixed states decided explicitly):
  FAILED  — any check-run's conclusion is a known-bad value (failure/cancelled/timed_out/
            action_required/stale) OR an unrecognized value never seen before (fail-closed on an
            unfamiliar future GitHub conclusion, never silently read as safe) — wins over pending,
            since a failure is already terminal and won't self-heal by waiting.
  PENDING — no failed check-run, and at least one check-run has status != "completed", or the
            check-run list is empty (no signal yet is not evidence of health).
  GREEN   — every check-run is "completed" with a conclusion in {success, neutral, skipped}.

Exit 0 no PR has failed (green/pending only, incl. zero open PRs — keep polling), 1 at least one
PR failed (actionable now), 2 usage error or an unreadable `gh`/API response (never silently
reads as clean).

Network: `run()` calls `gh pr list`/`gh api` live, same as `version_claim_check.py`'s own
`_gh_json`. `selftest` never touches the network; `classify_pr` and `build_report` are pure,
fed fixture check-run JSON only.
"""
import json
import subprocess
import sys

_BAD_CONCLUSIONS = {"failure", "cancelled", "timed_out", "action_required", "stale"}
_GOOD_CONCLUSIONS = {"success", "neutral", "skipped"}


def parse_args(args):
    """Returns repo (or None). Raises ValueError on any unrecognized token or a flag missing its
    value — the #188-class silent-argument-swallowing defect this house style always rejects."""
    repo = None
    i = 0
    while i < len(args):
        flag = args[i]
        if flag != "--repo":
            raise ValueError(f"unrecognized argument: {flag!r}")
        if i + 1 >= len(args):
            raise ValueError("--repo requires a value")
        repo = args[i + 1]
        i += 2
    return repo


def classify_pr(check_runs: list) -> str:
    """Pure: check_runs is a list of {'status':.., 'conclusion':..} dicts (the `gh api
    repos/<repo>/commits/<sha>/check-runs` shape's `check_runs` array). Returns
    'green' | 'pending' | 'failed'. FAILED wins over PENDING on a mixed PR — a failure is
    already terminal, never hidden behind a benign-looking wait."""
    if not check_runs:
        return "pending"

    any_incomplete = False
    for cr in check_runs:
        status = cr.get("status")
        conclusion = cr.get("conclusion")
        if status != "completed":
            any_incomplete = True
            continue
        if conclusion not in _GOOD_CONCLUSIONS:
            # covers every known-bad conclusion AND any unrecognized future value —
            # fail-closed, never silently treated as safe
            return "failed"

    return "pending" if any_incomplete else "green"


def build_report(prs_with_check_runs: list):
    """Pure: prs_with_check_runs is [{'number': int, 'check_runs': [...]}, ...]. Returns
    (line, exit_code, buckets) where buckets is {'green': [...], 'pending': [...],
    'failed': [...]} of PR numbers, each ascending."""
    buckets = {"green": [], "pending": [], "failed": []}
    for pr in prs_with_check_runs:
        buckets[classify_pr(pr["check_runs"])].append(pr["number"])
    for k in buckets:
        buckets[k].sort()

    def fmt(nums):
        return " ".join(f"#{n}" for n in nums) if nums else "none"

    line = (f"green: {fmt(buckets['green'])} / pending: {fmt(buckets['pending'])} / "
            f"failed: {fmt(buckets['failed'])}")
    exit_code = 1 if buckets["failed"] else 0
    return line, exit_code, buckets


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


def _check_runs_for_sha(repo: str, sha: str) -> list:
    r = subprocess.run(
        ["gh", "api", f"repos/{repo}/commits/{sha}/check-runs", "--jq", ".check_runs"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh api check-runs for {sha} failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def run(repo=None):
    repo = _resolve_repo(repo)
    prs = _gh_json(["pr", "list", "--state", "open", "--json", "number,headRefOid"], repo)

    prs_with_check_runs = [
        {"number": pr["number"], "check_runs": _check_runs_for_sha(repo, pr["headRefOid"])}
        for pr in prs
    ]

    line, exit_code, _ = build_report(prs_with_check_runs)
    print(f"merge_queue_watch · {line}")
    return exit_code


def selftest():
    # classify_pr — all-success is green (reverse control)
    assert classify_pr([{"status": "completed", "conclusion": "success"},
                         {"status": "completed", "conclusion": "success"}]) == "green"

    # classify_pr — neutral/skipped conclusions still count as green (not just "success")
    assert classify_pr([{"status": "completed", "conclusion": "neutral"},
                         {"status": "completed", "conclusion": "skipped"}]) == "green"

    # classify_pr — one in_progress among successes is pending
    assert classify_pr([{"status": "completed", "conclusion": "success"},
                         {"status": "in_progress", "conclusion": None}]) == "pending"

    # classify_pr — one failure among successes is failed
    assert classify_pr([{"status": "completed", "conclusion": "success"},
                         {"status": "completed", "conclusion": "failure"}]) == "failed"

    # classify_pr — the mixed negative control: a failure alongside a still-queued check-run
    # must classify FAILED, never PENDING (a failure is already terminal, not hidden by a wait)
    assert classify_pr([{"status": "completed", "conclusion": "failure"},
                         {"status": "queued", "conclusion": None}]) == "failed", \
        "a failed + pending mix must classify failed, not pending"

    # classify_pr — empty check-run list is pending, not green (no signal is not health)
    assert classify_pr([]) == "pending"

    # classify_pr — an unrecognized future conclusion value fails closed, never reads as safe
    assert classify_pr([{"status": "completed", "conclusion": "some_new_github_value"}]) == \
        "failed", "an unrecognized conclusion must fail closed, never silently pass as green"

    # build_report — a 3-PR mixed fixture: exact line, exit 1 (a failure present)
    line, code, buckets = build_report([
        {"number": 701, "check_runs": [{"status": "completed", "conclusion": "success"}]},
        {"number": 710, "check_runs": [{"status": "in_progress", "conclusion": None}]},
        {"number": 698, "check_runs": [{"status": "completed", "conclusion": "failure"}]},
    ])
    assert line == "green: #701 / pending: #710 / failed: #698", line
    assert code == 1
    assert buckets == {"green": [701], "pending": [710], "failed": [698]}

    # build_report — all-green multi-PR fixture: exit 0, failed bucket reads "none"
    line, code, buckets = build_report([
        {"number": 705, "check_runs": [{"status": "completed", "conclusion": "success"}]},
        {"number": 706, "check_runs": [{"status": "completed", "conclusion": "success"}]},
    ])
    assert line == "green: #705 #706 / pending: none / failed: none", line
    assert code == 0

    # build_report — zero open PRs is a clean pass, never a failure
    line, code, buckets = build_report([])
    assert line == "green: none / pending: none / failed: none", line
    assert code == 0

    # parse_args — the #188-class negative controls
    assert parse_args([]) is None
    assert parse_args(["--repo", "o/r"]) == "o/r"
    try:
        parse_args(["--bogus", "x"])
        raise AssertionError("an unrecognized flag must be rejected, not silently swallowed")
    except ValueError as e:
        assert "--bogus" in str(e)
    try:
        parse_args(["--repo"])
        raise AssertionError("a flag missing its value must be a clean error, not an IndexError")
    except ValueError as e:
        assert "--repo" in str(e)

    print("merge_queue_watch selftest · PASS · classify_pr (green/pending/failed incl. the "
          "mixed failed+pending negative control and the fail-closed unrecognized-conclusion "
          "control), build_report (3-bucket line format, exit tri-state, zero-PR clean pass), "
          "and parse_args' #188-class controls all pass clean")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "selftest":
        sys.exit(selftest())
    try:
        repo = parse_args(argv)
    except ValueError as e:
        print(f"merge_queue_watch: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(run(repo))
    except RuntimeError as e:
        print(f"merge_queue_watch: {e}", file=sys.stderr)
        sys.exit(2)
