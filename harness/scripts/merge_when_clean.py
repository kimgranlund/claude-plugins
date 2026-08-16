#!/usr/bin/env python3
"""merge_when_clean — mechanize the coordinator's pre-merge CI wait, then merge, mechanically.

Usage:
  merge_when_clean.py <pr-number> [--repo <owner/repo>] [--gate <plugin-root>]...
                       [--timeout <seconds>] [--interval <seconds>]
  merge_when_clean.py selftest

Replaces the ad-hoc `gh pr checks <n> --watch && gh pr merge <n> --squash && campaign_close.py
...` ritual a coordinator ran by hand. The 2026-08-16 incident (issue #371): that hand-run wait
loop grepped for any SUCCESS check instead of requiring GitHub's own composite verdict, and
squash-merged PR #364 while `mergeStateStatus` was still UNSTABLE (one check pending). Main's
gate happened to re-run green, so no harm landed — but the wait predicate was never actually
"all required checks finished and passing," just "I saw a SUCCESS somewhere."

M1 [FAIL/blocking] the PR never reaches OPEN + MERGEABLE + mergeStateStatus == CLEAN within the
                    poll budget -> refuse to merge, report the last observed state
M2 [FAIL]          `gh pr merge` itself fails once M1 passes -> refuse, report gh's error

Once M1/M2 pass, this script runs `gh pr merge <n> --squash` itself, then COMPOSES
`campaign_close.py` (imported, not reimplemented) for the post-merge branch-delete-verify +
optional gate sweep. Exit 0 all clean, 1 on any FAIL (refused to merge, or merged but
campaign_close reported FAIL), 2 on a usage error.

Network: `run()` polls `gh pr view` live and shells out to `gh pr merge` and campaign_close.py's
own `run()` — by design, same as campaign_close.py's and version_claim_check.py's own network
calls. `selftest` never touches the network: `check_mergeable` and `poll_until_clean` are pure,
fed scripted fetch/sleep functions — the #371 incident (mergeStateStatus UNSTABLE waved through)
is the negative control.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_close  # noqa: E402 — composed, not reimplemented (see module docstring)

DEFAULT_TIMEOUT = 1800  # 30 min: wide enough for a normal CI run; a genuinely stuck PR should
                         # surface as a FAIL, not hang the coordinator forever.
DEFAULT_INTERVAL = 15


def check_mergeable(pr_info: dict):
    """pr_info: {'state':.., 'mergeable':.., 'mergeStateStatus':..} from
    `gh pr view --json state,mergeable,mergeStateStatus`. Pure — the #371 negative control:
    a PR with SUCCESS checks but mergeStateStatus UNSTABLE (one check still pending) must FAIL,
    not pass on "I saw a SUCCESS somewhere."""
    state = pr_info.get("state")
    if state != "OPEN":
        return False, f"PR state is {state}, not OPEN -> refuse to merge"
    mergeable = pr_info.get("mergeable")
    if mergeable != "MERGEABLE":
        return False, f"mergeable is {mergeable}, not MERGEABLE -> refuse to merge"
    status = pr_info.get("mergeStateStatus")
    if status != "CLEAN":
        return False, (f"mergeStateStatus is {status}, not CLEAN -> refuse to merge (this is "
                        "the #371 predicate: a SUCCESS check alone is not enough)")
    return True, "OPEN + MERGEABLE + mergeStateStatus CLEAN"


def poll_until_clean(fetch_fn, timeout=DEFAULT_TIMEOUT, interval=DEFAULT_INTERVAL,
                      sleep=time.sleep, clock=time.monotonic):
    """Poll fetch_fn() (returns a pr_info dict) until check_mergeable passes or the timeout
    budget is spent. Returns (ok, last_pr_info, elapsed_polls). Pure given injected fetch_fn/
    sleep/clock — selftest feeds a scripted sequence and no-op sleep/clock, never the network."""
    start = clock()
    polls = 0
    while True:
        info = fetch_fn()
        polls += 1
        ok, _ = check_mergeable(info)
        if ok:
            return True, info, polls
        if clock() - start >= timeout:
            return False, info, polls
        sleep(interval)


def parse_args(args):
    """Returns (pr_number, repo, gate_roots, timeout, interval). Raises ValueError on any
    unrecognized token or a flag missing its value — the #188-class silent-argument-swallowing
    defect this house style always rejects rather than risks."""
    if not args:
        raise ValueError("pr-number is required")
    pr_number = args[0]
    repo = None
    gate_roots = []
    timeout = DEFAULT_TIMEOUT
    interval = DEFAULT_INTERVAL
    i = 1
    while i < len(args):
        flag = args[i]
        if flag not in ("--repo", "--gate", "--timeout", "--interval"):
            raise ValueError(f"unrecognized argument: {flag!r} "
                             "(--gate takes one root and is repeatable: --gate a --gate b)")
        if i + 1 >= len(args):
            raise ValueError(f"{flag} requires a value")
        value = args[i + 1]
        if flag == "--repo":
            repo = value
        elif flag == "--gate":
            gate_roots.append(value)
        elif flag == "--timeout":
            timeout = int(value)
        else:
            interval = int(value)
        i += 2
    return pr_number, repo, gate_roots, timeout, interval


def _gh_pr_info(pr_number, repo=None):
    cmd = ["gh", "pr", "view", pr_number, "--json", "state,mergeable,mergeStateStatus"]
    if repo:
        cmd += ["--repo", repo]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh pr view failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def run(pr_number: str, repo=None, gate_roots=None, timeout=DEFAULT_TIMEOUT,
        interval=DEFAULT_INTERVAL):
    findings = []

    ok, info, polls = poll_until_clean(
        lambda: _gh_pr_info(pr_number, repo), timeout=timeout, interval=interval)
    _, msg = check_mergeable(info)
    findings.append(("M1", ok, f"{msg} (after {polls} poll(s))"))
    if not ok:
        _report(findings)
        return 1

    merge_cmd = ["gh", "pr", "merge", pr_number, "--squash"]
    if repo:
        merge_cmd += ["--repo", repo]
    m = subprocess.run(merge_cmd, capture_output=True, text=True)
    if m.returncode != 0:
        findings.append(("M2", False, f"gh pr merge failed: {m.stderr.strip()}"))
        _report(findings)
        return 1
    findings.append(("M2", True, f"PR #{pr_number} squash-merged"))
    _report(findings)

    print("merge_when_clean · handing off to campaign_close")
    return campaign_close.run(pr_number, repo, gate_roots)


def _report(findings):
    verdict = "FAIL" if any(not ok for _, ok, _ in findings) else "clean"
    print(f"merge_when_clean · {verdict}")
    for code, ok, msg in findings:
        print(f"  {'ok  ' if ok else 'FAIL'} {code}  {msg}")


def selftest():
    # check_mergeable — the #371 negative control: SUCCESS-looking but UNSTABLE must FAIL
    ok, msg = check_mergeable({"state": "OPEN", "mergeable": "MERGEABLE",
                                "mergeStateStatus": "UNSTABLE"})
    assert not ok and "not CLEAN" in msg, \
        "mergeStateStatus UNSTABLE must FAIL even if some check reported SUCCESS (#371)"

    ok, msg = check_mergeable({"state": "OPEN", "mergeable": "MERGEABLE",
                                "mergeStateStatus": "CLEAN"})
    assert ok, "OPEN + MERGEABLE + CLEAN must pass"

    ok, msg = check_mergeable({"state": "CLOSED", "mergeable": "MERGEABLE",
                                "mergeStateStatus": "CLEAN"})
    assert not ok and "not OPEN" in msg, "a non-open PR must never be treated as mergeable"

    ok, msg = check_mergeable({"state": "OPEN", "mergeable": "CONFLICTING",
                                "mergeStateStatus": "DIRTY"})
    assert not ok and "not MERGEABLE" in msg, "a conflicting PR must FAIL on mergeable, not status"

    # poll_until_clean — reverse control: clean on the first read, no sleeping at all
    def boom(_): raise AssertionError("must not sleep when the first read is already clean")
    ok, info, polls = poll_until_clean(
        lambda: {"state": "OPEN", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"},
        sleep=boom, clock=lambda: 0.0)
    assert ok and polls == 1, "an already-clean PR must resolve on the first poll, no waiting"

    # poll_until_clean — the #371 fixture as a time series: UNSTABLE for a while, then CLEAN,
    # resolving ok within the budget (this is the case the hand-run loop got wrong live)
    seq = iter([
        {"state": "OPEN", "mergeable": "MERGEABLE", "mergeStateStatus": "UNSTABLE"},
        {"state": "OPEN", "mergeable": "MERGEABLE", "mergeStateStatus": "UNSTABLE"},
        {"state": "OPEN", "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN"},
    ])
    clock_seq = iter([0.0, 1.0, 2.0, 3.0])
    ok, info, polls = poll_until_clean(
        lambda: next(seq), timeout=100, interval=0, sleep=lambda _: None,
        clock=lambda: next(clock_seq))
    assert ok and polls == 3 and info["mergeStateStatus"] == "CLEAN", \
        f"a PR that eventually goes clean must resolve ok, not FAIL early: polls={polls}"

    # poll_until_clean — a PR stuck UNSTABLE through the entire timeout budget must FAIL, not
    # hang forever or silently pass
    clock_seq2 = iter([0.0, 5.0, 11.0])  # 3rd read is past a 10s timeout
    ok, info, polls = poll_until_clean(
        lambda: {"state": "OPEN", "mergeable": "MERGEABLE", "mergeStateStatus": "UNSTABLE"},
        timeout=10, interval=0, sleep=lambda _: None, clock=lambda: next(clock_seq2))
    assert not ok and info["mergeStateStatus"] == "UNSTABLE", \
        "a PR stuck dirty past the timeout must FAIL, never silently pass or hang"

    # parse_args — the #188-class negative controls, mirrored from campaign_close/
    # version_claim_check: an unrecognized token and a dangling flag must both be rejected
    pr, repo, roots, timeout, interval = parse_args(
        ["187", "--repo", "o/r", "--gate", "teamwork", "--gate", "docs",
         "--timeout", "60", "--interval", "5"])
    assert (pr, repo, roots, timeout, interval) == ("187", "o/r", ["teamwork", "docs"], 60, 5), \
        "every flag, including repeated --gate, must parse"
    try:
        parse_args(["187", "--gate", "teamwork", "docs"])
        raise AssertionError("the #188-class arg vector must be rejected, not silently swallowed")
    except ValueError as e:
        assert "docs" in str(e)
    try:
        parse_args(["187", "--timeout"])
        raise AssertionError("a flag missing its value must be a clean error, not an IndexError")
    except ValueError as e:
        assert "--timeout" in str(e)
    try:
        parse_args([])
        raise AssertionError("no pr-number at all must be a clean error")
    except ValueError:
        pass
    pr, repo, roots, timeout, interval = parse_args(["42"])
    assert (pr, repo, roots, timeout, interval) == (
        "42", None, [], DEFAULT_TIMEOUT, DEFAULT_INTERVAL), \
        "a bare PR number must parse with the documented defaults"

    print("merge_when_clean selftest · PASS · check_mergeable rejects the #371 UNSTABLE-waved-"
          "through negative control (OPEN+MERGEABLE alone is not enough), poll_until_clean "
          "resolves on eventual CLEAN and FAILs on a timed-out stuck PR, and the #188-class "
          "parse_args controls (unknown token, dangling flag, bare PR number) all hold")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    try:
        pr_number, repo, gate_roots, timeout, interval = parse_args(argv)
    except ValueError as e:
        print(f"merge_when_clean: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(run(pr_number, repo, gate_roots, timeout, interval))
    except RuntimeError as e:
        print(f"merge_when_clean: {e}", file=sys.stderr)
        sys.exit(2)
