#!/usr/bin/env python3
"""session-end-worktree-check — passive SessionEnd log, never blocks.

SessionEnd fires once, when a session terminates, but carries NO decision control (verified
against Claude Code's own hook docs, code.claude.com/docs/en/hooks, 2026-07-19): exit code 2 on
SessionEnd only shows stderr to the user, it cannot block or prevent termination. This script
never attempts to. Its only job: if a git worktree is left with uncommitted changes or unpushed
commits when the session actually ends, append one durable, discoverable log line so the state
isn't silently lost — a future session or a human can find it — even when `close-session` (the
paired skill, teamwork/skills/close-session) was never invoked at all this session.

Modes:
  session_end_worktree_check.py --hook   SessionEnd hook: reads event JSON on stdin, checks git
                                          state in cwd, appends to the log if something was left
                                          behind. Always exits 0 (SessionEnd cannot block; see
                                          above) — the log write is the only effect.
  session_end_worktree_check.py selftest proves the detection logic on embedded fixtures
                                          (0 pass / 1 fail / 2 skip)

Log location: ${CLAUDE_PLUGIN_DATA}/session-close-warnings.log (plugin-scoped persistent storage,
never writes into the target repo itself — a hook side-effect that touched the repo's own working
tree would just create the next session's uncommitted-state finding).
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


def check_worktree_state(cwd):
    """Return (is_git, dirty, ahead_count, upstream_ok) for the repo at cwd, or None fields if not a git dir."""
    def run(args):
        try:
            r = subprocess.run(
                ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5
            )
            return r.returncode, r.stdout.strip(), r.stderr.strip()
        except (OSError, subprocess.SubprocessError):
            return 1, "", "exec-failed"

    code, _, _ = run(["rev-parse", "--is-inside-work-tree"])
    if code != 0:
        return {"is_git": False, "dirty": False, "ahead": 0, "has_upstream": False}

    code, out, _ = run(["status", "--porcelain"])
    dirty = code == 0 and bool(out)

    code, _, _ = run(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    has_upstream = code == 0

    ahead = 0
    if has_upstream:
        code, out, _ = run(["rev-list", "@{u}..", "--count"])
        if code == 0 and out.isdigit():
            ahead = int(out)

    return {"is_git": True, "dirty": dirty, "ahead": ahead, "has_upstream": has_upstream}


def format_log_line(cwd, state):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    flags = []
    if state["dirty"]:
        flags.append("uncommitted-changes")
    if state["ahead"] > 0:
        flags.append(f"unpushed-commits({state['ahead']})")
    if not state["has_upstream"]:
        flags.append("no-upstream")
    return f"{ts} · {cwd} · {', '.join(flags)}\n"


def should_log(state):
    if not state["is_git"]:
        return False
    return state["dirty"] or state["ahead"] > 0


def run_hook():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        event = {}
    cwd = event.get("cwd") or os.getcwd()

    state = check_worktree_state(cwd)
    if should_log(state):
        data_dir = os.environ.get("CLAUDE_PLUGIN_DATA", tempfile.gettempdir())
        os.makedirs(data_dir, exist_ok=True)
        log_path = os.path.join(data_dir, "session-close-warnings.log")
        with open(log_path, "a") as f:
            f.write(format_log_line(cwd, state))
    # SessionEnd carries no decision control — always exit 0.
    sys.exit(0)


def selftest():
    fails = 0

    with tempfile.TemporaryDirectory() as tmp:
        # Fixture 1: not a git repo at all
        non_git = os.path.join(tmp, "not-a-repo")
        os.makedirs(non_git)
        state = check_worktree_state(non_git)
        if state["is_git"] is not False or should_log(state) is not False:
            print("FAIL fixture1 (non-git dir should never log)")
            fails += 1
        else:
            print("ok    fixture1 (non-git dir -> no log)")

        # Fixture 2: clean git repo, no upstream
        clean_repo = os.path.join(tmp, "clean-repo")
        os.makedirs(clean_repo)
        subprocess.run(["git", "init", "-q"], cwd=clean_repo, check=True)
        subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=clean_repo, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=clean_repo, check=True)
        with open(os.path.join(clean_repo, "f.txt"), "w") as f:
            f.write("x")
        subprocess.run(["git", "add", "."], cwd=clean_repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=clean_repo, check=True)
        state = check_worktree_state(clean_repo)
        if should_log(state) is not False:
            print("FAIL fixture2 (clean committed repo, no upstream, should not log)")
            fails += 1
        else:
            print("ok    fixture2 (clean repo, no upstream -> no log)")

        # Fixture 3: dirty repo (uncommitted change) -- the negative control that must bite
        dirty_repo = os.path.join(tmp, "dirty-repo")
        os.makedirs(dirty_repo)
        subprocess.run(["git", "init", "-q"], cwd=dirty_repo, check=True)
        subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=dirty_repo, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=dirty_repo, check=True)
        with open(os.path.join(dirty_repo, "f.txt"), "w") as f:
            f.write("x")
        subprocess.run(["git", "add", "."], cwd=dirty_repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=dirty_repo, check=True)
        with open(os.path.join(dirty_repo, "f.txt"), "w") as f:
            f.write("changed, uncommitted")
        state = check_worktree_state(dirty_repo)
        if should_log(state) is not True:
            print("FAIL fixture3 (dirty repo should log -- negative control did not bite)")
            fails += 1
        else:
            print("ok    fixture3 (dirty repo -> logs)")

        # Fixture 4: log line format is parseable and contains the cwd + a flag
        line = format_log_line(dirty_repo, state)
        if dirty_repo not in line or "uncommitted-changes" not in line:
            print("FAIL fixture4 (log line missing cwd or flag)")
            fails += 1
        else:
            print("ok    fixture4 (log line format)")

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        sys.exit(1)
    print("-- all fixtures passed --")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "--hook":
        run_hook()
    else:
        print(__doc__)
        sys.exit(2)
