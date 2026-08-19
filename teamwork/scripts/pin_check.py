#!/usr/bin/env python3
"""pin_check — preflight worktree/branch pin verification, mechanically.

Usage:
  pin_check.py <intended-branch> [--cwd <path>]
  pin_check.py selftest

Ruled by ticket #675 (2026-08-18, the #490/#609 pin-race class, upstream
anthropics/claude-code#87349): a dispatched builder's cwd can be bound to the WRONG
worktree/branch before it ever writes a line — four wedge events on 2026-08-18 alone were each
caught only because a human or a later re-check happened to notice the mismatch mid-build, after
real writes had already landed somewhere unintended. This is the mechanized, BEFORE-first-write
check `dispatch-ticket`'s own Phase 3 now calls: read the session's ACTUAL bound git state at
`<cwd>` (default the process's own cwd) and compare its checked-out branch against the ticket's
OWN intended branch name (the one Phase 3's claim bullet already decided) — a mismatch fails
loudly, naming the mitigation ladder's next rung, rather than silently letting the first write
land in the wrong tree.

  P1 [FAIL] the bound branch at <cwd> does not match the intended target branch — pin drift,
            caught before any write rather than discovered after one
  P2 [info] whether <cwd> is the PRIMARY checkout or a linked worktree — informational only (a
            #204 host-checkout skip is a legitimate, separately-authorized branch; this check
            never fails on primary-checkout alone, only reports it so the caller can cross-check
            it against whether that skip was actually granted)

Exit 0 clean (bound branch matches the intended target), 1 on P1 (mismatch — the ladder's next
rung is named in the report), 2 on a usage error or an unreadable git state (`<cwd>` isn't inside
a git working tree at all, or HEAD is detached/unresolvable).

`selftest` builds real temporary git repos — a primary checkout AND a real `git worktree add`
linked worktree — and proves the primary-vs-linked detection against both, plus the pure
`evaluate()` match/mismatch logic on fixture branch names. No network: this check is 100% local
git state, same discipline as `version_claim_check.py`'s pure/impure split but with nothing to
call out to `gh` for at all.
"""
import os
import subprocess
import sys
import tempfile


LADDER_HINT = (
    "next rung: a live session holding EnterWorktree re-pins on its own claimed path "
    "(fleet-rules Section 6's pin-race playbook) -> an Agent-tool-dispatched builder has NO "
    "EnterWorktree reach at all, so its DEFAULT is the scratch-clone rung (clone the repo into "
    "the session's own scratchpad, cut the intended branch off origin/main there, work, push, "
    "open the PR via gh) -> Git-Data-API landing is the RECOVERY rung, for work already stranded "
    "in a wedged worktree that can no longer be committed from locally (dispatch-ticket Phase 3's "
    "mitigation ladder; teamwork/skills/dispatch-ticket/references/isolation-ladder.md for the "
    "full mechanics)."
)


def parse_args(args):
    """Returns (intended_branch, cwd). Raises ValueError on any unrecognized token or a flag
    missing its value — the #188-class silent-argument-swallowing defect this house style
    always rejects rather than risks."""
    if not args:
        raise ValueError("intended-branch is required")
    intended_branch = args[0]
    cwd = None
    i = 1
    while i < len(args):
        flag = args[i]
        if flag != "--cwd":
            raise ValueError(f"unrecognized argument: {flag!r}")
        if i + 1 >= len(args):
            raise ValueError("--cwd requires a value")
        cwd = args[i + 1]
        i += 2
    return intended_branch, cwd


def evaluate(actual_branch, intended_branch, is_primary):
    """Pure: (ok, findings) — findings is [(code, ok, msg), ...]. No I/O, fed resolved state
    only, so the drift-detection logic itself is provable without touching a real repo."""
    findings = []
    ok_all = True

    if actual_branch == intended_branch:
        findings.append(("P1", True,
                          f"bound branch '{actual_branch}' matches intended '{intended_branch}'"))
    else:
        findings.append(("P1", False,
                          f"bound branch is '{actual_branch}', expected '{intended_branch}' -> "
                          f"pin drift detected BEFORE first write. {LADDER_HINT}"))
        ok_all = False

    findings.append(("P2", True,
                      f"checkout kind: {'PRIMARY' if is_primary else 'linked worktree'} "
                      "(informational only — never fails this check alone)"))

    return ok_all, findings


def _run_git(args, cwd):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def get_git_state(cwd):
    """Returns (branch, is_primary). Raises RuntimeError on an unreadable/non-git cwd or a
    detached/unresolvable HEAD — never silently reads a bogus state as clean.

    Primary-vs-linked-worktree detection needs no external knowledge of "the primary checkout
    path": a linked worktree's own `--git-dir` always resolves under
    `<primary>/.git/worktrees/<name>`, while `--git-common-dir` always resolves back to the
    primary `.git` regardless of which worktree asks — so the two are equal only in the primary
    checkout itself. Both are resolved as absolute paths (git may print either form) before the
    comparison."""
    code, _, err = _run_git(["rev-parse", "--is-inside-work-tree"], cwd)
    if code != 0:
        raise RuntimeError(f"{cwd} is not inside a git working tree: {err}")

    code, branch, err = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    if code != 0 or not branch or branch == "HEAD":
        raise RuntimeError(
            f"{cwd} has no resolvable current branch (detached HEAD?): {err or branch}")

    code, git_dir, err = _run_git(["rev-parse", "--git-dir"], cwd)
    if code != 0:
        raise RuntimeError(f"{cwd}: git rev-parse --git-dir failed: {err}")
    code, common_dir, err = _run_git(["rev-parse", "--git-common-dir"], cwd)
    if code != 0:
        raise RuntimeError(f"{cwd}: git rev-parse --git-common-dir failed: {err}")

    git_dir_abs = os.path.realpath(os.path.join(cwd, git_dir))
    common_dir_abs = os.path.realpath(os.path.join(cwd, common_dir))
    is_primary = git_dir_abs == common_dir_abs

    return branch, is_primary


def run(intended_branch, cwd=None):
    cwd = cwd or os.getcwd()
    branch, is_primary = get_git_state(cwd)
    ok, findings = evaluate(branch, intended_branch, is_primary)
    _report(ok, findings)
    return 0 if ok else 1


def _report(ok, findings):
    print(f"pin_check · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg in findings:
        print(f"  {'ok  ' if item_ok else 'FAIL'} {code}  {msg}")


def _init_repo(path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=path, check=True)
    with open(os.path.join(path, "f.txt"), "w") as f:
        f.write("x")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=path, check=True)
    # Normalize the initial branch name across git version defaults (main vs master).
    subprocess.run(["git", "branch", "-M", "main"], cwd=path, check=True)


def selftest():
    fails = 0

    # evaluate() — pure logic, no git at all: the reverse control (match must pass)
    ok, findings = evaluate("675-pin-race-mitigation-ladder", "675-pin-race-mitigation-ladder",
                             False)
    if not ok:
        print("FAIL evaluate/match (identical branches must pass)")
        fails += 1
    else:
        print("ok    evaluate/match (identical branches pass)")

    # evaluate() — the negative control that must bite: drift is caught, and the report names
    # the ladder's next rung rather than a bare "mismatch"
    ok, findings = evaluate("670-unnamed-checker-dispatch", "675-pin-race-mitigation-ladder",
                             False)
    p1 = next((f for f in findings if f[0] == "P1"), None)
    if ok or p1 is None or p1[1] is not False or "next rung" not in p1[2]:
        print("FAIL evaluate/mismatch (drift must FAIL and name the ladder's next rung)")
        fails += 1
    else:
        print("ok    evaluate/mismatch (fails, names the ladder)")

    # evaluate() — P2 is informational only: a primary-checkout match must still pass overall
    ok, findings = evaluate("main", "main", True)
    p2 = next((f for f in findings if f[0] == "P2"), None)
    if not ok or p2 is None or "PRIMARY" not in p2[2]:
        print("FAIL evaluate/primary-informational (P2 must report PRIMARY without failing P1)")
        fails += 1
    else:
        print("ok    evaluate/primary-informational")

    # get_git_state() — real repos: a primary checkout AND a real linked worktree, proving the
    # --git-dir vs --git-common-dir detection against actual git behavior, not a mocked stand-in
    with tempfile.TemporaryDirectory() as tmp:
        primary = os.path.join(tmp, "primary")
        _init_repo(primary)

        branch, is_primary = get_git_state(primary)
        if branch != "main" or is_primary is not True:
            print(f"FAIL get_git_state/primary (expected main/True, got {branch}/{is_primary})")
            fails += 1
        else:
            print("ok    get_git_state/primary (real repo, detected as PRIMARY)")

        linked = os.path.join(tmp, "linked-worktree")
        r = subprocess.run(
            ["git", "worktree", "add", "-b", "a-feature-branch", linked, "main"],
            cwd=primary, capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"FAIL get_git_state/setup (git worktree add failed: {r.stderr.strip()})")
            fails += 1
        else:
            branch, is_primary = get_git_state(linked)
            if branch != "a-feature-branch" or is_primary is not False:
                print(f"FAIL get_git_state/linked (expected a-feature-branch/False, "
                      f"got {branch}/{is_primary})")
                fails += 1
            else:
                print("ok    get_git_state/linked (real worktree, detected as NOT primary)")

        # get_git_state() — a non-git directory must raise, never silently read as clean
        non_git = os.path.join(tmp, "not-a-repo")
        os.makedirs(non_git)
        try:
            get_git_state(non_git)
            print("FAIL get_git_state/non-git (must raise, not silently read as clean)")
            fails += 1
        except RuntimeError:
            print("ok    get_git_state/non-git (raises, as required)")

        # run() end-to-end — the primary repo IS on 'main': a matching run() must exit 0
        rc = run("main", cwd=primary)
        if rc != 0:
            print(f"FAIL run/match (expected exit 0, got {rc})")
            fails += 1
        else:
            print("ok    run/match (end-to-end exit 0)")

        # run() end-to-end — asking for a branch this repo isn't on must exit 1
        rc = run("some-other-branch", cwd=primary)
        if rc != 1:
            print(f"FAIL run/mismatch (expected exit 1, got {rc})")
            fails += 1
        else:
            print("ok    run/mismatch (end-to-end exit 1)")

    # parse_args — the #188-class negative control: an unrecognized token, and a flag missing
    # its value, must both be rejected rather than silently swallowed
    branch, cwd = parse_args(["675-pin-race-mitigation-ladder", "--cwd", "/some/path"])
    if (branch, cwd) != ("675-pin-race-mitigation-ladder", "/some/path"):
        print("FAIL parse_args/full")
        fails += 1
    else:
        print("ok    parse_args/full")
    branch, cwd = parse_args(["675-pin-race-mitigation-ladder"])
    if (branch, cwd) != ("675-pin-race-mitigation-ladder", None):
        print("FAIL parse_args/bare (a bare intended-branch with no flags must parse)")
        fails += 1
    else:
        print("ok    parse_args/bare")
    try:
        parse_args(["675-pin-race-mitigation-ladder", "--bogus", "x"])
        print("FAIL parse_args/bogus (an unrecognized flag must be rejected, not swallowed)")
        fails += 1
    except ValueError as e:
        if "--bogus" not in str(e):
            print("FAIL parse_args/bogus (error must name the bad flag)")
            fails += 1
        else:
            print("ok    parse_args/bogus (rejected, names the flag)")
    try:
        parse_args(["675-pin-race-mitigation-ladder", "--cwd"])
        print("FAIL parse_args/missing-value (a flag missing its value must be a clean error)")
        fails += 1
    except ValueError as e:
        if "--cwd" not in str(e):
            print("FAIL parse_args/missing-value (error must name the flag)")
            fails += 1
        else:
            print("ok    parse_args/missing-value")
    try:
        parse_args([])
        print("FAIL parse_args/empty (no intended-branch at all must be a clean error)")
        fails += 1
    except ValueError:
        print("ok    parse_args/empty")

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        return 1
    print("pin_check selftest · PASS · P1 drift detection (real mismatch + real match), P2's "
          "primary/linked distinction proved against a REAL git worktree, and parse_args' "
          "#188-class controls all pass clean")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    try:
        intended_branch, cwd = parse_args(argv)
    except ValueError as e:
        print(f"pin_check: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(run(intended_branch, cwd))
    except RuntimeError as e:
        print(f"pin_check: {e}", file=sys.stderr)
        sys.exit(2)
