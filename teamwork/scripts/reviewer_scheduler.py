#!/usr/bin/env python3
"""reviewer_scheduler — the recurring per-task `claude -p` spawn scheduler for the fleet's
`reviewer` seat (issue #856, follows up #853's one-shot bind-plus-I2-confirm round trip).

Usage:
  reviewer_scheduler.py run --worktree <path> --tasks-file <path>
                             [--log-dir <path>] [--index <path>]
                             [--timeout <secs>] [--max-retries <n>] [--keep-logs <n>]
  reviewer_scheduler.py selftest

#853 shipped the one-shot bind-plus-I2-confirm round trip (`fleet-bootstrap` Phase 5's
`reviewer` branch): the orchestrator writes+verifies a `deny-edit-write` wall in a worktree,
then spawns exactly ONE `claude -p` child to confirm it enforces. #853 deliberately did not
build the ONGOING scheduling layer that turns that one-shot confirm into a recurring cadence of
per-review-task spawns — this script is that layer. It does NOT write or verify the wall itself
(that stays `team-scaffolding` Phase 3 / `fleet-bootstrap` Phase 5 step 2's job, run once before
this script's first invocation against a given worktree) — it refuses to spawn at all against an
unwalled worktree (`verify_wall_present`), fail-closed, rather than silently repeating #852's
false-positive class at this layer.

**Cadence**: this script performs ONE scheduling pass over an explicit task list per invocation
— it is not its own daemon. Drive a recurring cadence with the harness's own interval primitives
instead of reimplementing one here: `/loop <interval> "run python3
${CLAUDE_PLUGIN_ROOT}/scripts/reviewer_scheduler.py run --worktree <wt> --tasks-file <path>"` for
a live session, or `/schedule` for an unattended cloud routine. Task SOURCING (which PRs/targets need
review right now) is the caller's decision, named explicitly in `--tasks-file` — this script
owns only the spawn/monitor/log/report mechanics once a task list is already decided.

**Crash recovery**: each task gets up to `1 + --max-retries` attempts (default 1 retry, so 2
attempts total). A `claude -p` child that exits non-zero or is killed on `--timeout` (default
600s) is retried into a fresh log file; if every attempt fails, the task is reported explicitly
(`outcome: "crashed"` or `"timeout"` in the index row, plus a stderr line) — never silently
dropped.

**Log rotation/retention**: every attempt's captured stdout+stderr lands in its own timestamped
`*.log` file under `--log-dir` (default `<worktree>-reviewer-logs`, a sibling of the worktree so
the walled child's own denied `Write` never has to touch it — this script's own file writes are
the orchestrator's, same non-tool-call redirect #853 already verified is invisible to the
child's wall). After each pass, `rotate_logs` deletes everything past the newest `--keep-logs`
(default 20) — #853's own build wrote one ad-hoc log per spawn with no retention policy; this is
the missing piece.

**Report collection**: the reviewer child's own review verdict is posted where #855's ruling
already put it — a `gh issue comment` / `gh pr comment` on the review target itself, never a
`fleet.json` write (a walled child cannot append JSON there anyway, per #855's charset finding).
This script's own durable artifact is narrower and local: one JSONL row per completed spawn
(`--index`, default `<log-dir>/index.jsonl`) naming which task, how many attempts, the final
outcome, the log path, and — when the child's own stdout carries the `POSTED: <url>` marker its
dispatch prompt requires — the comment URL. "Which spawn covered which review task, with what
outcome" (issue #856's own scope wording) is exactly this index, not a second copy of the
review's content.

Exit 0 every task in the pass succeeded, 1 at least one task crashed/timed out (the pass still
completed; failures are named in the index and on stderr), 2 usage error or the target worktree
carries no wall markers on disk (content-checked only, not I2-probe confirmed — refuses to spawn
at all rather than guess).

`selftest` touches no network and spawns no real `claude -p` process — it proves every pure
helper (arg parsing, task-file loading, prompt building, outcome classification, log rotation,
index row shape, wall verification) against local fixtures only; `_spawn_one`/`run_pass`'s own
real subprocess plumbing is exercised by the invariants those helpers compose, not re-tested
here (spawning a real `claude -p` child in a selftest would be slow, network-touching, and
non-deterministic — exactly what this house style keeps out of a selftest).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def parse_args(args):
    """Returns a dict of resolved `run` options, or raises ValueError on any unrecognized
    subcommand/flag or a flag missing its value (the #188-class silent-argument-swallowing
    defect this house style always rejects)."""
    if not args:
        raise ValueError("no subcommand given (expected 'run' or 'selftest')")
    if args[0] != "run":
        raise ValueError(f"unrecognized subcommand: {args[0]!r}")

    opts = {
        "worktree": None,
        "tasks_file": None,
        "log_dir": None,
        "index": None,
        "timeout": 600,
        "max_retries": 1,
        "keep_logs": 20,
    }
    flag_map = {
        "--worktree": ("worktree", str),
        "--tasks-file": ("tasks_file", str),
        "--log-dir": ("log_dir", str),
        "--index": ("index", str),
        "--timeout": ("timeout", int),
        "--max-retries": ("max_retries", int),
        "--keep-logs": ("keep_logs", int),
    }
    i = 1
    while i < len(args):
        flag = args[i]
        if flag not in flag_map:
            raise ValueError(f"unrecognized argument: {flag!r}")
        key, caster = flag_map[flag]
        if i + 1 >= len(args):
            raise ValueError(f"{flag} requires a value")
        raw = args[i + 1]
        try:
            opts[key] = caster(raw)
        except ValueError:
            raise ValueError(f"{flag} value must be a valid {caster.__name__}: {raw!r}")
        i += 2

    if not opts["worktree"]:
        raise ValueError("--worktree is required")
    if not opts["tasks_file"]:
        raise ValueError("--tasks-file is required")
    return opts


def load_tasks(tasks_file: str) -> list:
    """Reads a JSON array of non-blank task strings from tasks_file. Raises ValueError on
    malformed content (not a list, empty list, a non-string/blank entry) — fail closed, never
    spawn anything off a garbled task list."""
    data = json.loads(Path(tasks_file).read_text())
    if not isinstance(data, list) or not data:
        raise ValueError(f"{tasks_file} must contain a non-empty JSON array of task strings")
    tasks = []
    for t in data:
        if not isinstance(t, str) or not t.strip():
            raise ValueError(f"{tasks_file} contains a non-string/blank task entry: {t!r}")
        tasks.append(t.strip())
    return tasks


def slugify(task: str) -> str:
    """Pure: a filesystem/log-filename-safe slug for a task string — non-alnum runs collapse
    to one '-', truncated to 40 chars, never empty (falls back to 'task')."""
    out = []
    prev_dash = False
    for ch in task.lower():
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    slug = "".join(out).strip("-")
    return (slug or "task")[:40]


def build_child_prompt(task: str) -> str:
    """Pure: the sealed dispatch prompt for one `claude -p` reviewer child covering one review
    task. Quotes `bind-review`'s own routing table inline rather than a Skill-tool hand-off —
    `bind-review` is `disable-model-invocation: true`, same reasoning `fleet-bootstrap` Phase 5
    step 3 already uses for the reviewer's one-shot charter."""
    return (
        "Seat: reviewer (background-subprocess, one-task spawn — issue #856).\n"
        "You are running inside a worktree whose permission wall (deny Edit/Write, a "
        "PreToolUse Bash allowlist) was already written and verified by the orchestrator "
        "before this process started (issue #853). Do not attempt to write or edit files; "
        "report only via `gh issue comment` / `gh pr comment` on the target below.\n\n"
        f"Review task: {task}\n\n"
        "Classify the target per `teamwork:bind-review`'s own routing table (a code change -> "
        "code-checker; wiring/frontmatter/an arrangement -> wiring-checker; a rubric-bearing "
        "doc -> doc-checker; a SKILL.md -> skill-checker; an agent definition -> agent-checker; "
        "a hook -> hook-checker; a plugin's packaging -> plugin-checker; the language of a "
        "prompt-carrying artifact -> wording-checker), dispatch the owning checker, then post "
        "the verdict (leading with the verdict line and the checker's name) as a `gh issue "
        "comment` or `gh pr comment` on the target. Print the exact line `POSTED: <comment-url>` "
        "to stdout once the comment lands, and nothing else on that line — the scheduler's own "
        "log parser reads this literal key."
    )


def classify_outcome(returncode, timed_out: bool) -> str:
    """Pure: one attempt's outcome. `timed_out` wins over `returncode` — a killed-on-timeout
    process's exit code is never a trustworthy success/failure signal, even if it happens to
    read as 0."""
    if timed_out:
        return "timeout"
    if returncode == 0:
        return "succeeded"
    return "crashed"


def extract_posted_url(log_text: str):
    """Pure: pulls the child's own `POSTED: <url>` line out of its captured stdout. None when
    absent (crashed before posting, or never posted) or blank — never guessed at."""
    for line in log_text.splitlines():
        line = line.strip()
        if line.startswith("POSTED:"):
            url = line[len("POSTED:"):].strip()
            return url or None
    return None


def rotate_logs(log_dir: Path, keep: int) -> list:
    """Deletes the oldest `*.log` files in log_dir beyond `keep` (newest-mtime-first
    retention). Returns the deleted paths (as strings). `keep <= 0` is a no-op — never delete
    everything on a misconfigured zero/negative value; fail safe, not silently destructive."""
    if keep <= 0:
        return []
    if not log_dir.exists():
        return []
    logs = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    deleted = []
    for p in logs[keep:]:
        p.unlink()
        deleted.append(str(p))
    return deleted


def build_index_row(task, slug, attempts, outcome, log_path, comment_url, started_at,
                     finished_at):
    """Pure: the one durable JSONL row shape — 'which spawn covered which review task, with
    what outcome' (issue #856 scope item 4)."""
    return {
        "task": task,
        "slug": slug,
        "attempts": attempts,
        "outcome": outcome,
        "log_path": log_path,
        "comment_url": comment_url,
        "started_at": started_at,
        "finished_at": finished_at,
    }


def append_index(index_path: Path, row: dict) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("a") as f:
        f.write(json.dumps(row) + "\n")


def verify_wall_present(worktree: str) -> bool:
    """Reads `<worktree>/.claude/settings.local.json` for the reviewer wall's own two markers
    — `permissions.deny` containing both `Edit` and `Write`, plus a `PreToolUse` `Bash` hook —
    the same shape `team-scaffolding` C1-C1a writes and C3 verifies. Returns False on anything
    short of both markers present; never assumes a wall exists from the worktree's mere
    existence, or from a settings file that only partially matches."""
    settings_path = Path(worktree) / ".claude" / "settings.local.json"
    if not settings_path.exists():
        return False
    try:
        data = json.loads(settings_path.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    deny = data.get("permissions", {}).get("deny", [])
    has_deny = "Edit" in deny and "Write" in deny
    hooks = data.get("hooks", {}).get("PreToolUse", [])
    has_bash_hook = isinstance(hooks, list) and any(
        "Bash" in str(h.get("matcher", "")) for h in hooks
    )
    return has_deny and has_bash_hook


def _spawn_one(worktree, prompt, log_path, timeout):
    """Runs one `claude -p <prompt>` child, cwd=worktree, stdout+stderr redirected to
    log_path by THIS process's own file write — never a tool call the child makes, so the
    child's wall never touches it (the exact mechanism issue #853's own live round trip
    verified). Returns (returncode, timed_out)."""
    with open(log_path, "w") as logf:
        try:
            proc = subprocess.run(
                ["claude", "-p", prompt],
                cwd=worktree,
                stdout=logf,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            return proc.returncode, False
        except subprocess.TimeoutExpired:
            return None, True


def run_pass(opts) -> int:
    """Runs one scheduling pass over every task in opts['tasks_file']. Returns the process
    exit code (0 all succeeded, 1 at least one task never succeeded)."""
    worktree = opts["worktree"]
    tasks = load_tasks(opts["tasks_file"])
    log_dir = Path(opts["log_dir"] or f"{worktree.rstrip('/')}-reviewer-logs")
    index_path = Path(opts["index"] or (log_dir / "index.jsonl"))
    log_dir.mkdir(parents=True, exist_ok=True)

    any_failed = False
    max_attempts = opts["max_retries"] + 1
    for task in tasks:
        slug = slugify(task)
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        prompt = build_child_prompt(task)

        attempts = 0
        outcome = "crashed"
        log_path = log_dir / f"{ts}-{slug}-attempt1.log"
        while attempts < max_attempts:
            attempts += 1
            log_path = log_dir / f"{ts}-{slug}-attempt{attempts}.log"
            returncode, timed_out = _spawn_one(worktree, prompt, log_path, opts["timeout"])
            outcome = classify_outcome(returncode, timed_out)
            if outcome == "succeeded":
                break

        finished_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        log_text = log_path.read_text() if log_path.exists() else ""
        comment_url = extract_posted_url(log_text) if outcome == "succeeded" else None

        row = build_index_row(task, slug, attempts, outcome, str(log_path), comment_url,
                               started_at, finished_at)
        append_index(index_path, row)

        if outcome != "succeeded":
            any_failed = True
            print(f"reviewer_scheduler: task {task!r} {outcome} after {attempts} attempt(s) "
                  f"— see {log_path}", file=sys.stderr)
        else:
            print(f"reviewer_scheduler: task {task!r} succeeded — "
                  f"{comment_url or 'no POSTED url found in log'}")

    rotate_logs(log_dir, opts["keep_logs"])
    return 1 if any_failed else 0


def selftest():
    import tempfile

    # parse_args — happy path + #188-class negative controls
    opts = parse_args(["run", "--worktree", "/tmp/wt", "--tasks-file", "/tmp/tasks.json"])
    assert opts["worktree"] == "/tmp/wt"
    assert opts["timeout"] == 600 and opts["max_retries"] == 1 and opts["keep_logs"] == 20

    try:
        parse_args([])
        raise AssertionError("empty args must be rejected")
    except ValueError:
        pass
    try:
        parse_args(["bogus"])
        raise AssertionError("an unrecognized subcommand must be rejected")
    except ValueError as e:
        assert "bogus" in str(e)
    try:
        parse_args(["run", "--worktree", "/tmp/wt"])
        raise AssertionError("missing --tasks-file must be rejected")
    except ValueError as e:
        assert "tasks-file" in str(e)
    try:
        parse_args(["run", "--bogus", "x"])
        raise AssertionError("an unrecognized flag must be rejected, not silently swallowed")
    except ValueError as e:
        assert "--bogus" in str(e)
    try:
        parse_args(["run", "--worktree"])
        raise AssertionError("a flag missing its value must be a clean error, not an IndexError")
    except ValueError as e:
        assert "--worktree" in str(e)
    try:
        parse_args(["run", "--worktree", "/tmp/wt", "--tasks-file", "/tmp/t.json",
                     "--timeout", "notanint"])
        raise AssertionError("a non-int --timeout must be rejected")
    except ValueError as e:
        assert "timeout" in str(e)

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        # load_tasks — reverse control (valid, whitespace-trimmed) + negative controls
        tasks_file = td / "tasks.json"
        tasks_file.write_text(json.dumps(["PR #870", " skill:teamwork/skills/foo "]))
        tasks = load_tasks(str(tasks_file))
        assert tasks == ["PR #870", "skill:teamwork/skills/foo"], tasks

        empty_file = td / "empty.json"
        empty_file.write_text("[]")
        try:
            load_tasks(str(empty_file))
            raise AssertionError("an empty task list must be rejected")
        except ValueError:
            pass

        not_list_file = td / "notlist.json"
        not_list_file.write_text('{"a": 1}')
        try:
            load_tasks(str(not_list_file))
            raise AssertionError("a non-list tasks file must be rejected")
        except ValueError:
            pass

        blank_entry_file = td / "blank.json"
        blank_entry_file.write_text(json.dumps(["ok", "  "]))
        try:
            load_tasks(str(blank_entry_file))
            raise AssertionError("a blank task entry must be rejected")
        except ValueError:
            pass

        # slugify — deterministic, filesystem-safe, never empty
        assert slugify("PR #870: fix the thing!") == "pr-870-fix-the-thing"
        assert slugify("") == "task"

        # build_child_prompt — carries the task and the POSTED: contract key verbatim
        prompt = build_child_prompt("PR #870")
        assert "PR #870" in prompt
        assert "POSTED:" in prompt

        # classify_outcome — all three branches, timeout wins over a coincidentally-clean exit
        assert classify_outcome(0, False) == "succeeded"
        assert classify_outcome(1, False) == "crashed"
        assert classify_outcome(None, True) == "timeout"
        assert classify_outcome(0, True) == "timeout", \
            "a timed-out process must classify timeout even if its returncode looks clean"

        # extract_posted_url — found / not found / blank
        assert extract_posted_url("some log\nPOSTED: https://x/y\nmore") == "https://x/y"
        assert extract_posted_url("no marker here") is None
        assert extract_posted_url("POSTED:   \n") is None, \
            "a blank POSTED: line must read as no url, not an empty string treated as truthy"

        # rotate_logs — keeps the newest `keep`, deletes the rest; keep<=0 is a no-op
        log_dir = td / "logs"
        log_dir.mkdir()
        for i in range(5):
            p = log_dir / f"log{i}.log"
            p.write_text("x")
            os.utime(p, (i, i))  # force distinct, ascending mtimes
        deleted = rotate_logs(log_dir, keep=2)
        remaining = sorted(p.name for p in log_dir.glob("*.log"))
        assert remaining == ["log3.log", "log4.log"], remaining
        assert len(deleted) == 3

        log_dir2 = td / "logs2"
        log_dir2.mkdir()
        (log_dir2 / "a.log").write_text("x")
        assert rotate_logs(log_dir2, keep=0) == [], \
            "keep<=0 must be a no-op, never delete everything"
        assert (log_dir2 / "a.log").exists()

        # build_index_row / append_index — round trip, exact shape
        row = build_index_row("PR #870", "pr-870", 1, "succeeded", "/x/log", "https://x/y",
                               "2026-08-21T00:00:00Z", "2026-08-21T00:05:00Z")
        assert row["task"] == "PR #870" and row["outcome"] == "succeeded" and row["attempts"] == 1
        index_path = td / "index.jsonl"
        append_index(index_path, row)
        append_index(index_path, row)
        lines = index_path.read_text().strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0]) == row

        # verify_wall_present — reverse control (valid wall) + negative controls
        wt = td / "wt"
        (wt / ".claude").mkdir(parents=True)
        (wt / ".claude" / "settings.local.json").write_text(json.dumps({
            "permissions": {"deny": ["Edit", "Write"]},
            "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": []}]},
        }))
        assert verify_wall_present(str(wt)) is True

        missing_wt = td / "missing-wt"
        missing_wt.mkdir()
        assert verify_wall_present(str(missing_wt)) is False

        no_hook_wt = td / "no-hook-wt"
        (no_hook_wt / ".claude").mkdir(parents=True)
        (no_hook_wt / ".claude" / "settings.local.json").write_text(json.dumps({
            "permissions": {"deny": ["Edit", "Write"]},
        }))
        assert verify_wall_present(str(no_hook_wt)) is False, \
            "a deny list with no PreToolUse Bash hook must not read as a verified wall"

    print("reviewer_scheduler selftest · PASS · parse_args (#188-class controls), load_tasks "
          "(malformed/empty/blank-entry negative controls), slugify, build_child_prompt's "
          "POSTED: contract, classify_outcome (incl. the timeout-wins-over-clean-exit control), "
          "extract_posted_url, rotate_logs (retention count + keep<=0 no-op control), "
          "build_index_row/append_index round trip, and verify_wall_present (reverse control + "
          "missing-file/missing-hook negative controls) all pass clean")
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selftest":
        return selftest()
    try:
        opts = parse_args(argv)
    except ValueError as e:
        print(f"reviewer_scheduler: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2

    if not verify_wall_present(opts["worktree"]):
        print(f"reviewer_scheduler: no wall markers found on disk at {opts['worktree']} "
              "(.claude/settings.local.json missing the deny-edit-write + PreToolUse Bash "
              "markers) — refusing to spawn an unwalled child. Run the wall-write step first "
              "(team-scaffolding Phase 3 / fleet-bootstrap Phase 5 step 2).", file=sys.stderr)
        return 2

    try:
        return run_pass(opts)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"reviewer_scheduler: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
