#!/usr/bin/env python3
"""transcript_locate — resolve session .jsonl transcript paths, print or copy them. No new data.

A LOCATOR, not an export: this touches nothing on disk beyond reading existing files' names and
mtimes, and its only "write" is an optional OS clipboard copy of the resolved path STRING (never
the transcript's own bytes). Fenced explicitly (issue #605, 2026-08-19 finding): NOT the maximal
custom bundle (2026-08-17 finding — heavier, out of scope here), NOT a Stop hook (#466 retired
every plugin hook estate-wide; this ships as an on-demand script only).

Usage:
  transcript_locate.py [--repo-root PATH] [--slug SLUG] [--session-id ID]
                        [--claude-home PATH] [--limit N] [--copy] [--json]
  transcript_locate.py selftest

No args resolves the CURRENT session, live, in the calling shell — the disclosed, deliberate
deviation from the no-args-prints-usage anatomy every other bundled script follows (same
disclosed shape as check-state's doc_state.py): a bare invocation is this script's entire reason
to exist ("one command, no per-session setup"), so a no-args run that only printed __doc__ would
defeat its own purpose. Passing any recognized flag (including a bare `--json` or `--copy`) still
runs the resolution; only a wholly empty argv is special-cased.

Resolution order, matching this machine's own verified `~/.claude/projects/` convention (audit
trail: harness/skills/check-reconstructibility's LLD, cross-checked live against this repo's own
worktree-scoped project dirs during this ticket's build):

  1. project-dir slug = the resolved absolute `--repo-root` (default: cwd) with every `/` and `.`
     character replaced by `-` (`slug()` below) — this is what turns a plain checkout
     (`/Users/x/proj`) into `-Users-x-proj` and a worktree-scoped one
     (`/Users/x/proj/.claude/worktrees/fix-1`) into `-Users-x-proj--claude-worktrees-fix-1` (the
     double dash is real: the `/` before `.claude` and the `.` itself each become their own `-`).
  2. session id = `--session-id` if given, else the `CLAUDE_CODE_SESSION_ID` environment variable
     (set by the live Claude Code process for the session calling this script — verified present
     and matching the on-disk transcript filename stem, 2026-08-19), else the most-recently-
     modified top-level `*.jsonl` file directly under the project dir (the past-session-by-slug
     path, when no live env var applies and no id was named) — always disclosed which branch fired
     and, on the fallback branch, how many candidate sessions existed.
  3. main transcript path = `<claude-home>/projects/<slug>/<session-id>.jsonl`.
  4. subagent transcripts = `<claude-home>/projects/<slug>/<session-id>/subagents/agent-*.jsonl`
     (the sibling `agent-*.meta.json` files are metadata, never counted or listed), sorted by
     mtime descending, capped at `--limit` (default 5).

Exit codes: 0 = main transcript resolved and exists on disk; 1 = it does not (wrong slug/session,
or a project/session that was never journaled — a findings/failure result, not a crash); 2 =
usage error. `selftest`'s own tri-state: this script has no runtime dependency beyond the
stdlib, so its selftest never skips.

Network: none. Filesystem: read-only except the optional `--copy` clipboard hand-off, which
shells out to the host's own clipboard tool (`pbcopy`/`xclip`/`wl-copy`, first found) and writes
nothing to any file — a clipboard write is not a file write, and the copied payload is the path
STRING, never transcript bytes.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SLUG_CHARS = re.compile(r"[/.]")


def slug(repo_root: str) -> str:
    """Pure: the exact `~/.claude/projects/<slug>` transform — every `/` and `.` -> `-`."""
    return SLUG_CHARS.sub("-", str(Path(repo_root).resolve()))


def pick_fallback_session(project_dir: Path):
    """Pure-ish (one readdir): the most-recently-modified top-level `*.jsonl` directly under
    `project_dir` (never one nested under a session-id subfolder, which holds THAT session's own
    subagents/workflows/tool-results, not sibling top-level sessions). Returns
    (session_id_or_None, candidate_count)."""
    if not project_dir.is_dir():
        return None, 0
    candidates = sorted(
        (p for p in project_dir.glob("*.jsonl") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None, 0
    return candidates[0].stem, len(candidates)


def resolve_session_id(explicit_id, env, project_dir: Path):
    """Pure given its inputs (env is a plain dict, never os.environ read directly here — the
    caller resolves that boundary): returns (session_id_or_None, source, candidate_count) where
    source in {"explicit", "env", "fallback", "none"}. Precedence: explicit --session-id > the
    live CLAUDE_CODE_SESSION_ID env var > the newest top-level transcript in project_dir."""
    if explicit_id:
        return explicit_id, "explicit", 1
    env_id = env.get("CLAUDE_CODE_SESSION_ID")
    if env_id:
        return env_id, "env", 1
    session_id, count = pick_fallback_session(project_dir)
    if session_id is None:
        return None, "none", 0
    return session_id, "fallback", count


def recent_subagent_transcripts(session_dir: Path, limit: int):
    """Pure-ish (one readdir): `agent-*.jsonl` under `session_dir/subagents`, newest first,
    capped at `limit`. Never includes a sibling `agent-*.meta.json` — glob's own suffix match
    already excludes it, asserted by the selftest's negative control rather than trusted blind."""
    subagents_dir = session_dir / "subagents"
    if not subagents_dir.is_dir():
        return []
    files = sorted(
        (p for p in subagents_dir.glob("agent-*.jsonl") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return [str(p) for p in files[:limit]]


def build_report(repo_root, claude_home, explicit_slug, explicit_session_id, limit, env):
    """Assembles the full resolution. Returns (report_dict, exit_code). report_dict is always
    returned (even on a 1/2-worthy gap) so a caller can still print what WAS resolved."""
    resolved_slug = explicit_slug or slug(repo_root)
    project_dir = Path(claude_home) / "projects" / resolved_slug
    session_id, source, candidate_count = resolve_session_id(explicit_session_id, env, project_dir)

    report = {
        "repo_root": str(Path(repo_root).resolve()),
        "claude_home": str(Path(claude_home)),
        "slug": resolved_slug,
        "project_dir": str(project_dir),
        "session_id": session_id,
        "session_id_source": source,
        "session_id_candidates_considered": candidate_count,
        "session_transcript": None,
        "session_transcript_exists": False,
        "subagent_transcripts": [],
    }

    if session_id is None:
        return report, 1

    transcript_path = project_dir / f"{session_id}.jsonl"
    report["session_transcript"] = str(transcript_path)
    report["session_transcript_exists"] = transcript_path.is_file()

    session_dir = project_dir / session_id
    report["subagent_transcripts"] = recent_subagent_transcripts(session_dir, limit)

    return report, (0 if report["session_transcript_exists"] else 1)


def copy_to_clipboard(text: str):
    """Best-effort OS clipboard copy of a path STRING — never a file write. Returns
    (ok, tool_name_or_None). No tool found is disclosed, never silently swallowed."""
    for tool, args in (("pbcopy", ["pbcopy"]), ("xclip", ["xclip", "-selection", "clipboard"]),
                       ("wl-copy", ["wl-copy"])):
        if shutil.which(tool):
            try:
                subprocess.run(args, input=text.encode(), check=True, timeout=5)
                return True, tool
            except Exception:
                continue
    return False, None


def _print_report(report, copied_with):
    print(f"transcript_locate · slug={report['slug']}")
    id_line = f"  session-id: {report['session_id']} (source: {report['session_id_source']}"
    if report["session_id_source"] == "fallback":
        id_line += f", candidates={report['session_id_candidates_considered']}"
    id_line += ")"
    print(id_line)
    exists = "exists" if report["session_transcript_exists"] else "MISSING"
    print(f"  session-transcript ({exists}): {report['session_transcript']}")
    subs = report["subagent_transcripts"]
    print(f"  subagent-transcripts (most recent {len(subs)}):")
    for p in subs:
        print(f"    {p}")
    if not subs:
        print("    (none found)")
    if copied_with:
        print(f"  copied session-transcript path to clipboard via {copied_with}")


def selftest():
    fails = 0

    # slug() — the real, verified transform: worktree-scoped path with a dot segment. This is a
    # regression fixture against this exact machine's own `~/.claude/projects/` directory naming
    # (proved live during this ticket's build, not assumed from prose alone).
    got = slug("/Users/kimba/Projects/nonoun/plugins/.claude/worktrees/fix-684")
    want = "-Users-kimba-Projects-nonoun-plugins--claude-worktrees-fix-684"
    if got != want:
        print(f"FAIL slug/worktree (got {got!r}, want {want!r})")
        fails += 1
    else:
        print("ok    slug/worktree (real machine fixture, double-dash at the .claude boundary)")

    # slug() — a plain checkout, no dot segment at all: the reverse control
    got = slug("/Users/kimba/Projects/nonoun/plugins")
    want = "-Users-kimba-Projects-nonoun-plugins"
    if got != want:
        print(f"FAIL slug/plain (got {got!r}, want {want!r})")
        fails += 1
    else:
        print("ok    slug/plain (no dot segment, single dash throughout)")

    # resolve_session_id — precedence: explicit wins over env and fallback
    sid, source, n = resolve_session_id("explicit-id", {"CLAUDE_CODE_SESSION_ID": "env-id"},
                                         Path("/nonexistent"))
    if (sid, source) != ("explicit-id", "explicit"):
        print("FAIL resolve_session_id/explicit-precedence")
        fails += 1
    else:
        print("ok    resolve_session_id/explicit-precedence")

    # resolve_session_id — env wins over fallback when no explicit id given
    sid, source, n = resolve_session_id(None, {"CLAUDE_CODE_SESSION_ID": "env-id"},
                                         Path("/nonexistent"))
    if (sid, source) != ("env-id", "env"):
        print("FAIL resolve_session_id/env-precedence")
        fails += 1
    else:
        print("ok    resolve_session_id/env-precedence")

    # resolve_session_id / pick_fallback_session / recent_subagent_transcripts / build_report —
    # exercised together against a REAL temp directory tree, mirroring the real on-disk layout
    import tempfile
    import time

    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp) / "projects" / "-Users-t-proj"
        project_dir.mkdir(parents=True)

        # two top-level sessions, "newer" must win the fallback pick
        older = project_dir / "older-session.jsonl"
        newer = project_dir / "newer-session.jsonl"
        older.write_text("{}\n")
        time.sleep(0.01)
        newer.write_text("{}\n")

        sid, count = pick_fallback_session(project_dir)
        if sid != "newer-session" or count != 2:
            print(f"FAIL pick_fallback_session (got {sid!r}/{count}, want 'newer-session'/2)")
            fails += 1
        else:
            print("ok    pick_fallback_session (newest top-level *.jsonl wins, count reported)")

        # reverse control: an empty/missing project dir yields no candidate, never a crash
        sid, count = pick_fallback_session(Path(tmp) / "projects" / "-nope")
        if sid is not None or count != 0:
            print("FAIL pick_fallback_session/empty (missing dir must yield None/0)")
            fails += 1
        else:
            print("ok    pick_fallback_session/empty (missing dir -> None/0, no crash)")

        # subagents: three real jsonl + one meta.json — the meta.json is the negative control
        session_dir = project_dir / "newer-session"
        subagents_dir = session_dir / "subagents"
        subagents_dir.mkdir(parents=True)
        names = ["agent-aaa.jsonl", "agent-bbb.jsonl", "agent-ccc.jsonl"]
        for n in names:
            (subagents_dir / n).write_text("{}\n")
            time.sleep(0.01)
        (subagents_dir / "agent-bbb.meta.json").write_text("{}\n")

        got = recent_subagent_transcripts(session_dir, limit=2)
        if len(got) != 2 or not got[0].endswith("agent-ccc.jsonl"):
            print(f"FAIL recent_subagent_transcripts/limit-and-order (got {got})")
            fails += 1
        elif any(p.endswith(".meta.json") for p in got):
            print("FAIL recent_subagent_transcripts/meta-json-leak (must never list a .meta.json)")
            fails += 1
        else:
            print("ok    recent_subagent_transcripts (newest-first, capped, meta.json excluded)")

        # build_report — full assembly, env-sourced session id, transcript present
        report, exit_code = build_report(
            repo_root=tmp, claude_home=tmp, explicit_slug="-Users-t-proj",
            explicit_session_id=None, limit=5,
            env={"CLAUDE_CODE_SESSION_ID": "newer-session"},
        )
        if exit_code != 0 or not report["session_transcript_exists"] or \
                len(report["subagent_transcripts"]) != 3:
            print(f"FAIL build_report/happy-path (exit={exit_code}, report={report})")
            fails += 1
        else:
            print("ok    build_report/happy-path (exit 0, transcript exists, 3 subagents found)")

        # build_report — reverse control: a session id with no on-disk transcript exits 1, but
        # the report is still returned (never None) so a caller can print what WAS found
        report, exit_code = build_report(
            repo_root=tmp, claude_home=tmp, explicit_slug="-Users-t-proj",
            explicit_session_id="ghost-session", limit=5, env={},
        )
        if exit_code != 1 or report["session_transcript_exists"] or report["session_id"] is None:
            print(f"FAIL build_report/missing-transcript (exit={exit_code}, report={report})")
            fails += 1
        else:
            print("ok    build_report/missing-transcript (exit 1, report still populated)")

        # build_report — no session id resolvable at all (empty project dir, no env, no
        # explicit id) -> exit 1, session_id None, never a crash
        empty_dir = Path(tmp) / "projects" / "-Users-empty-proj"
        empty_dir.mkdir(parents=True)
        report, exit_code = build_report(
            repo_root=str(empty_dir), claude_home=tmp, explicit_slug=None,
            explicit_session_id=None, limit=5, env={},
        )
        if exit_code != 1 or report["session_id"] is not None:
            print(f"FAIL build_report/no-session-anywhere (exit={exit_code}, report={report})")
            fails += 1
        else:
            print("ok    build_report/no-session-anywhere (exit 1, session_id None, no crash)")

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        return 1
    print("transcript_locate selftest · PASS · slug() proved against this machine's real "
          "worktree-scoped project-dir naming (dot-becomes-dash included) plus a plain-path "
          "reverse control, session-id precedence (explicit > env > fallback), the fallback "
          "picker's newest-wins + empty-dir reverse control, subagent listing's newest-first/"
          "cap/meta.json-exclusion negative control, and build_report's happy-path plus two "
          "missing-transcript/no-session reverse controls")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--copy", action="store_true")
    parser.add_argument("--json", action="store_true")

    if argv and argv[0] == "selftest":
        return selftest()

    try:
        ns = parser.parse_args(argv)
    except SystemExit:
        return 2

    report, exit_code = build_report(
        repo_root=ns.repo_root, claude_home=ns.claude_home, explicit_slug=ns.slug,
        explicit_session_id=ns.session_id, limit=ns.limit, env=dict(os.environ),
    )

    copied_with = None
    if ns.copy and report["session_transcript"]:
        ok, tool = copy_to_clipboard(report["session_transcript"])
        copied_with = tool if ok else None
        if not ok:
            print("transcript_locate: no clipboard tool found (tried pbcopy/xclip/wl-copy) — "
                  "path printed above only", file=sys.stderr)

    if ns.json:
        out = dict(report)
        out["clipboard_copied_with"] = copied_with
        print(json.dumps(out, indent=2))
    else:
        _print_report(report, copied_with)

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
