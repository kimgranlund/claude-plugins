#!/usr/bin/env python3
"""worktree-prebash-guard — flags a Bash command that cd's (or -C/--prefix's) out of a
worktree cwd into the PRIMARY checkout and then runs a further command in the same call.

Repo-side mitigation for issue #139: a dispatched worktree seat ran
`cd <primary-checkout> && node scripts/build/components.mjs` and the platform's git-only
worktree-isolation guard didn't bind it (it binds git commands, not arbitrary compound
commands that cd into the shared checkout). This hook is deliberately ASK, never BLOCK
(hook-writing-rules: judgment-shaped rules are wrong often and unoverridable always as a
hard block) — it flags for confirmation, it does not enforce isolation on its own.

Detection is possible without any external knowledge of "the primary checkout path" because
EnterWorktree worktrees always live IN-REPO at <primary-root>/.claude/worktrees/<name>
(this workspace's own convention, CLAUDE.md). The primary root is therefore always a
deterministic string-prefix of the worktree cwd handed to every hook event — no config, no
external lookup.

Known blind spots (disclosed, not silently papered over):
  - Dynamic cd targets ($(...), `...`, $VAR) cannot be resolved without executing the
    shell — such segments are treated as unknown and pass silently (fail open, not fail
    closed: a hard block on an unprovable case is the judgment-in-a-hook antipattern).
  - Only `cd`, `-C`, and `--prefix` path-target forms are recognized; other path-bearing
    flags (`-w`, `--cwd`, tool-specific flags) are not scanned.
  - A bare `cd <primary>` with no chained command in the same Bash call is out of scope —
    the disclosed gap is specifically the COMPOUND escape (git-only guard already binds
    plain git commands cd'd into primary).
  - No nested-subshell paren tracking; a `(cd /x && ...)` is scanned the same as a flat
    compound, which is usually right but not guaranteed for deeply nested forms.

Modes:
  worktree_prebash_guard.py --hook   PreToolUse(Bash) hook: reads event JSON on stdin;
                                      silent exit 0 unless a hit is found, then emits
                                      {"hookSpecificOutput": {"permissionDecision": "ask", ...}}
  worktree_prebash_guard.py selftest proves the detection logic on embedded fixtures
                                      (0 pass / 1 fail / 2 skip)
"""
import json
import os
import shlex
import sys

HOOK_NAME = "worktree-prebash-guard"

WORKTREE_MARKER = "/.claude/worktrees/"


def find_primary_root(cwd):
    """Return the primary checkout root if cwd is inside <root>/.claude/worktrees/..., else None."""
    if not cwd or WORKTREE_MARKER not in cwd:
        return None
    root = cwd.split(WORKTREE_MARKER, 1)[0]
    return root or None


def split_segments(command):
    """Split a shell command into segments on unquoted &&, ||, ; and newlines."""
    segments = []
    buf = []
    quote = None
    i = 0
    n = len(command)
    while i < n:
        ch = command[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch in ("\n", ";"):
            segments.append("".join(buf))
            buf = []
            i += 1
            continue
        if command[i : i + 2] in ("&&", "||"):
            segments.append("".join(buf))
            buf = []
            i += 2
            continue
        buf.append(ch)
        i += 1
    segments.append("".join(buf))
    return [s.strip().lstrip("(").strip() for s in segments if s.strip().strip("()")]


def parse_cd_target(segment):
    """Return the raw cd argument for a `cd ...` segment, '~' for bare `cd`, else None."""
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None
    if not tokens or tokens[0] != "cd":
        return None
    return tokens[1] if len(tokens) > 1 else "~"


def scan_path_flags(segment):
    """Return raw path arguments following -C or --prefix in this segment."""
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return []
    targets = []
    for i, tok in enumerate(tokens):
        if tok in ("-C", "--prefix") and i + 1 < len(tokens):
            targets.append(tokens[i + 1])
    return targets


def resolve_target(target, current_dir):
    """Resolve a cd/-C target to an absolute path, or None if it can't be resolved statically."""
    if target is None or current_dir is None:
        return None
    if "$" in target or "`" in target:
        return None  # dynamic — cannot resolve without executing the shell
    expanded = os.path.expanduser(target)
    if os.path.isabs(expanded):
        return os.path.normpath(expanded)
    return os.path.normpath(os.path.join(current_dir, expanded))


def is_within(path, root):
    if path is None or root is None:
        return False
    return path == root or path.startswith(root.rstrip("/") + "/")


def analyze_command(command, cwd):
    """Return a list of (kind, resolved_path, segment) hits, or [] if not applicable / no hit."""
    primary_root = find_primary_root(cwd)
    if primary_root is None:
        return []
    worktrees_root = os.path.join(primary_root, ".claude", "worktrees")

    segments = split_segments(command)
    hits = []
    current_dir = cwd
    for i, seg in enumerate(segments):
        cd_target = parse_cd_target(seg)
        if cd_target is not None:
            resolved = resolve_target(cd_target, current_dir)
            if resolved is None:
                current_dir = None  # unknown from here on — stay quiet, don't guess
                continue
            current_dir = resolved
            escapes_primary = is_within(resolved, primary_root) and not is_within(resolved, worktrees_root)
            has_follow_on = i < len(segments) - 1
            if escapes_primary and has_follow_on:
                hits.append(("cd", resolved, segments[i + 1]))
            continue
        for flag_target in scan_path_flags(seg):
            resolved = resolve_target(flag_target, current_dir or cwd)
            if is_within(resolved, primary_root) and not is_within(resolved, worktrees_root):
                hits.append(("flag", resolved, seg))
    return hits


def format_reason(primary_root, hits):
    lines = [
        f"{HOOK_NAME} · compound command reaches into the primary checkout from a worktree session",
        f"primary checkout: {primary_root}",
    ]
    for kind, resolved, seg in hits:
        via = "cd" if kind == "cd" else "-C/--prefix"
        lines.append(f"  via {via} -> {resolved} · then: {seg.strip()}")
    lines.append("If intentional, proceed. If not, cd back into the worktree checkout first.")
    return "\n".join(lines)


def run_hook():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed event: a flaky hook is worse than none — stay quiet
    if event.get("tool_name") != "Bash":
        return 0
    command = (event.get("tool_input") or {}).get("command", "")
    cwd = event.get("cwd") or ""
    if not command or not cwd:
        return 0

    primary_root = find_primary_root(cwd)
    hits = analyze_command(command, cwd)
    if not hits:
        return 0

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": format_reason(primary_root, hits),
                }
            }
        )
    )
    return 0


def selftest():
    fails = 0

    def check(name, command, cwd, expect_hit):
        hits = analyze_command(command, cwd)
        got_hit = bool(hits)
        if got_hit != expect_hit:
            print(f"FAIL {name} (expected hit={expect_hit}, got={got_hit}, hits={hits})")
            return False
        print(f"ok    {name} (hit={got_hit})")
        return True

    cases = [
        # positive: the disclosed #139 pattern — compound cd into primary + mutating command
        (
            "fixture1_disclosed_pattern",
            "cd /repo && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # negative control: cd within the SAME worktree must never flag
        (
            "fixture2_in_worktree_cd",
            "cd /repo/.claude/worktrees/seat1/sub && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # boundary control: a sibling dir that string-prefixes primary_root must not false-positive
        (
            "fixture3_prefix_boundary",
            "cd /repo-backup && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # relative-path escape must resolve via normpath, not just literal string match
        (
            "fixture4_relative_escape",
            "cd ../.. && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # dynamic/unresolvable target: documented blind spot, must stay quiet (fail open)
        (
            "fixture5_dynamic_target",
            "cd $(git rev-parse --show-toplevel) && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # not a worktree session at all: guard is not applicable
        (
            "fixture6_primary_cwd_not_applicable",
            "cd /repo && node scripts/build/components.mjs",
            "/repo",
            False,
        ),
        # bare cd with no chained command: out of scope (compound-only per issue #139)
        (
            "fixture7_bare_cd_no_followon",
            "cd /repo",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # flag-based escape: git -C / make -C / npm --prefix targeting primary in one shot
        (
            "fixture8_dash_C_flag",
            "make -C /repo build",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # numeric -C (ripgrep context flag) must not false-positive against a path compare
        (
            "fixture9_dash_C_numeric_not_path",
            "rg -C 3 foo",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
    ]
    for name, command, cwd, expect_hit in cases:
        if not check(name, command, cwd, expect_hit):
            fails += 1

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        sys.exit(1)
    print("-- all fixtures passed --")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "--hook":
        sys.exit(run_hook())
    else:
        print(__doc__)
        sys.exit(2)
