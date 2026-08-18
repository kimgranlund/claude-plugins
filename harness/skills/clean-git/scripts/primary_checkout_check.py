#!/usr/bin/env python3
"""primary_checkout_check — is the shared PRIMARY checkout on `main`?

clean-git's own inventory step (fleet-rules' primary-checkout-stays-on-main rule, #592/PR#600)
states the rule; this script is the mechanical read-only check repo-cleaner's survey runs to
enforce it. Read-only, ALWAYS — this is a propose-only finding for repo-cleaner's report, never a
mutation (the drift class it exists to catch: a session leaving a feature branch checked out on
the shared primary, stranding a concurrent peer's commit — #592's incident, recovered as PR#591).

Usage:
  primary_checkout_check.py <primary-root> [<base-ref>]   check one checkout (base-ref default: origin/main)
  primary_checkout_check.py selftest                       prove the counters bite

Rule:
  P1 [FAIL] `git -C <primary-root> rev-parse --abbrev-ref HEAD` != main -> off-main, naming the
            branch and, where the base ref resolves, its ahead/behind count against it

P1 is the only rule; a resolvable HEAD reading anything other than `main` fires it regardless of
ahead/behind — the branch name alone is the finding, counts are supporting evidence only. An
unresolvable base ref (no such remote-tracking branch, e.g. a fixture with no remote configured)
degrades the count to "unknown" rather than failing the whole check — never blocks reporting the
branch-name finding itself.

Exit 0 on `main` (clean), 1 on FAIL (off-main, including a detached HEAD — `rev-parse
--abbrev-ref HEAD` succeeds there and prints the literal string `HEAD`, which is off-main like
any other non-`main` value), 2 on a usage error (no repo at the given path, an unborn HEAD — the
cases where `rev-parse` itself fails).
"""
import subprocess
import sys
from pathlib import Path


def current_branch(root: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git rev-parse failed: {r.stderr.strip()}")
    return r.stdout.strip()


def ahead_behind(root: Path, branch: str, base_ref: str):
    """(behind, ahead) of `branch` against `base_ref`, or None if base_ref doesn't resolve."""
    r = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--left-right", "--count", f"{base_ref}...{branch}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    parts = r.stdout.split()
    if len(parts) != 2:
        return None
    return int(parts[0]), int(parts[1])


def check(root: Path, base_ref: str = "origin/main"):
    branch = current_branch(root)
    if branch == "main":
        return []
    counts = ahead_behind(root, branch, base_ref)
    if counts is None:
        detail = f"branch `{branch}` (ahead/behind {base_ref}: unknown)"
    else:
        behind, ahead = counts
        detail = f"branch `{branch}` ({ahead} ahead / {behind} behind {base_ref})"
    return [("FAIL", "P1", f"primary checkout is not on `main` -> {detail}")]


def run(root: Path, base_ref: str):
    fs = check(root, base_ref)
    verdict = "FAIL" if fs else "clean"
    print(f"primary_checkout_check · {verdict} · {root}")
    for sev, code, msg in fs:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if fs else 0


def selftest():
    import tempfile

    def git(root, *args, check=True):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=check)

    with tempfile.TemporaryDirectory() as td:
        remote = Path(td) / "remote.git"
        primary = Path(td) / "primary"
        remote.mkdir()
        git(remote, "init", "-q", "--bare")

        git(Path(td), "clone", "-q", str(remote), str(primary), check=True)
        git(primary, "config", "user.email", "t@t")
        git(primary, "config", "user.name", "t")
        (primary / "f.txt").write_text("one")
        git(primary, "add", "f.txt")
        git(primary, "commit", "-q", "-m", "init")
        git(primary, "branch", "-M", "main")
        git(primary, "push", "-q", "-u", "origin", "main")

        # Positive control: on main, clean.
        fs_main = check(primary)
        assert fs_main == [], f"on main must read clean, got {fs_main}"
        assert run(primary, "origin/main") == 0, "run() must exit 0 on main"

        # Negative control (the off-main case this ticket exists for): a feature branch checked
        # out on the primary, ahead of main by one commit.
        git(primary, "checkout", "-q", "-b", "feature/off-main")
        (primary / "f.txt").write_text("two")
        git(primary, "commit", "-q", "-am", "feature work")
        fs_off = check(primary)
        assert len(fs_off) == 1 and fs_off[0][1] == "P1", f"off-main must fire P1, got {fs_off}"
        assert "feature/off-main" in fs_off[0][2], f"the branch name must be named, got {fs_off}"
        assert "1 ahead" in fs_off[0][2], f"ahead count must be reported, got {fs_off}"
        assert run(primary, "origin/main") == 1, "run() must exit 1 off-main"

        # An unresolvable base ref degrades to 'unknown' rather than erroring the whole check.
        fs_unknown = check(primary, base_ref="origin/does-not-exist")
        assert len(fs_unknown) == 1 and "unknown" in fs_unknown[0][2], \
            f"an unresolvable base ref must degrade to 'unknown', not error, got {fs_unknown}"

        # Back on main: clean again (branch state is read live, not cached).
        git(primary, "checkout", "-q", "main")
        fs_back = check(primary)
        assert fs_back == [], f"back on main must read clean again, got {fs_back}"

    print("primary_checkout_check selftest · PASS · main reads clean, an off-main branch fires "
          "P1 naming the branch and ahead/behind, an unresolvable base ref degrades to 'unknown' "
          "rather than erroring")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    base = args[1] if len(args) > 1 else "origin/main"
    try:
        sys.exit(run(Path(args[0]).resolve(), base))
    except RuntimeError as e:
        print(f"primary_checkout_check · ERROR · {e}")
        sys.exit(2)
