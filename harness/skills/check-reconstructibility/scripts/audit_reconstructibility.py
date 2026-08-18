#!/usr/bin/env python3
"""audit_reconstructibility — the ADR-0022 "repo is the backup" instrument.

Read-only sweep: what would a fresh machine plus a clone of `origin/main` NOT recover today?
Classifies every finding into ADR-0022's own trichotomy — committed / enrolled-with-mitigation /
defect — plus a fourth bucket, OPEN, for exception 4 (user-scoped `~/.claude`/`~/.config` state),
whose exact mitigation mechanism ADR-0022 itself leaves unruled at ratification (its own Open
questions section) — reporting that as OPEN is honest; folding it into "defect" would misstate an
already-acknowledged ADR gap as a build failure this ticket owes to fix.

Usage:
  audit_reconstructibility.py --repo-root PATH [--claude-home PATH] [--config-home PATH] [--json]
  audit_reconstructibility.py selftest

Checks (each cites the ADR-0022 line it realizes):
  1. Working-tree cleanliness — every git-ignored-and-present path under repo-root, classified
     against the repo's OWN `.gitignore` (declared-regenerable, e.g. `dist/`) vs a NAMED
     exception (e.g. `settings.local.json`, exception 4) vs UNCATEGORIZED (a defect candidate —
     load-bearing local state neither declared regenerable nor enrolled).
  2. `.claude/ops/` full-tracking — ADR-0022's own stated fact ("ALREADY fully committed") as a
     regression guard: any on-disk file under `.claude/ops/` NOT in `git ls-files` is a defect.
  3. Global git-ignore-file dependency — a pattern contributed by `core.excludesFile`, EXPLICIT
     (git config) or IMPLICIT (git's own fallback to `$XDG_CONFIG_HOME/git/ignore`, default
     `~/.config/git/ignore`, when no explicit config overrides it and that file exists) — either
     way, outside the repo entirely and invisible to a fresh clone; this is exception 4's own
     "entirely outside any repo" case, made concrete.
  4. Exception 1 (memory dir) — `<claude-home>/projects/<repo-slug>*/memory/*.md` existence +
     count; mitigation is a PROCESS (promote load-bearing entries into a committed record), so
     this is always reported enrolled-with-mitigation, never a defect, per the ADR's own text.
  5. Exception 2 (plugin cache) — `<claude-home>/plugins/cache/` existence; mitigation is the
     reinstall-path doc this same ticket owes — PRESENT at the expected path -> enrolled;
     MISSING -> defect (mitigation owed-at-lock, not yet shipped).
  6. Exception 3 (credentials) — `<config-home>/gh/hosts.yml` (or equivalent) existence, plus a
     repo sweep for any `.env`-class file (tracked or merely present) that should not exist under
     the standing deny rules; mitigation is the credential-runbook doc this ticket owes — same
     present/missing -> enrolled/defect split as exception 2.
  7. Exception 4 (user-scoped `~/.claude`/`~/.config` state) — existence of the global CLAUDE.md,
     `settings.json`, and the excludesFile dependency found in check 3; always OPEN (ADR's own
     ratification gap, never silently upgraded to enrolled or defect).

Exit codes: 0 = swept clean (no defects); 1 = at least one defect found; 2 = usage error (repo
root missing, not a git repo, or `.gitignore` unreadable).

Network: none. Live calls this makes: local `git` subprocess invocations against `repo-root`
only (status/ls-files/config — no `fetch`/`push`, and never touches `origin` over the network)
and local filesystem reads under `claude-home`/`config-home`. `selftest` touches neither — every
check function it proves (`classify_ignored_path`, `check_ops_tracked`,
`classify_excludesfile_patterns`, `build_report`) is pure, fed fixture data only.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

# Patterns this house's own repo already declares regenerable in its OWN .gitignore — mirrored
# here only as the CLASS test (a repo's own .gitignore entry is self-declared regenerable/
# expected), never hardcoded as the one true list: `classify_ignored_path` takes the repo's own
# parsed .gitignore lines as an argument, this constant is not consulted directly.
NAMED_EXCEPTION_MARKERS = {
    "settings.local.json": "exception-4-user-scope",
}


def parse_gitignore(text: str):
    """Pure: non-blank, non-comment lines, order-preserved, whitespace-trimmed."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out.append(stripped)
    return out


def classify_ignored_path(rel_path: str, gitignore_patterns: list):
    """Pure: bucket ONE git-ignored-and-present relative path.

    - Matches a pattern this repo's OWN `.gitignore` declares (substring match on the pattern's
      own text, trailing `/`/`*` stripped) -> "regenerable" (self-declared, in-repo, honest).
    - Matches a NAMED_EXCEPTION_MARKERS basename -> that exception's own tag.
    - Anything else -> "uncategorized" — a defect candidate: load-bearing local state neither
      declared regenerable nor enrolled in the ADR's own exception list.
    """
    base = rel_path.rsplit("/", 1)[-1]
    if base in NAMED_EXCEPTION_MARKERS:
        return NAMED_EXCEPTION_MARKERS[base]
    for pattern in gitignore_patterns:
        needle = pattern.strip("/").rstrip("*").strip()
        if not needle:
            continue
        if needle in rel_path:
            return "regenerable"
    return "uncategorized"


def check_ops_tracked(tracked: list, on_disk: list):
    """Pure: ADR-0022's own stated fact ("`.claude/ops/` is ALREADY fully committed") as a
    regression guard. Returns (ok, missing) — missing is every on-disk path absent from
    `tracked`, sorted for a stable report."""
    tracked_set = set(tracked)
    missing = sorted(p for p in on_disk if p not in tracked_set)
    return (len(missing) == 0, missing)


def classify_excludesfile_patterns(patterns: list):
    """Pure: every pattern a global `core.excludesFile` contributes is, by definition, invisible
    to a fresh clone (it lives entirely outside the repo) — exception 4's own "entirely outside
    any repo" case. Returns the patterns unchanged, labeled, for the report; an empty list means
    no global excludesFile dependency was found (the healthy default)."""
    return [{"pattern": p, "class": "exception-4-user-scope", "reason":
             "contributed by a global core.excludesFile, not this repo's own .gitignore — "
             "invisible to a fresh clone unless the same global config is also provisioned"}
            for p in patterns]


def build_report(*, ignored_findings, ops_check, excludesfile_findings, memory_dir_info,
                  plugin_cache_info, credentials_info, user_scope_info):
    """Pure: assemble the final trichotomy(+open) report from already-computed pieces. Never
    calls out to git/filesystem itself — every argument is pre-resolved data, so this function
    alone is what `selftest` proves without touching a live machine."""
    defects = []
    enrolled = []
    open_items = []

    for f in ignored_findings:
        if f["class"] == "uncategorized":
            defects.append({"item": f["path"], "why": "git-ignored and present, but neither "
                             "declared regenerable in this repo's own .gitignore nor enrolled "
                             "in ADR-0022's exception list"})
        elif f["class"] == "regenerable":
            pass  # committed-adjacent: declared, expected, not a finding
        else:
            enrolled.append({"item": f["path"], "class": f["class"]})

    if not ops_check["ok"]:
        for path in ops_check["missing"]:
            defects.append({"item": path, "why": ".claude/ops/ is ADR-0022's own stated "
                             "fully-committed fact — this path is on disk but untracked"})

    for f in excludesfile_findings:
        open_items.append({"item": f["pattern"], "class": f["class"], "reason": f["reason"]})

    # Exception 1 — memory dir: mitigation is a process (promotion of load-bearing entries),
    # never a defect by this audit's own design — always enrolled when the dir exists at all.
    if memory_dir_info["exists"]:
        enrolled.append({"item": memory_dir_info["path"], "class": "exception-1-memory",
                          "count": memory_dir_info["file_count"],
                          "mitigation": "process — promote load-bearing entries into a "
                          "committed record; residue accepted as lossy by design"})

    # Exceptions 2/3 — mitigation is a DOC this ticket itself owes; PRESENT -> enrolled,
    # MISSING -> defect (owed-at-lock and not yet shipped is a real gap, not a shrug).
    for info, tag in ((plugin_cache_info, "exception-2-plugin-cache"),
                       (credentials_info, "exception-3-credentials")):
        if not info["exists"]:
            continue  # nothing on this machine to account for
        if info["mitigation_doc_present"]:
            enrolled.append({"item": info["path"], "class": tag,
                              "mitigation_doc": info["mitigation_doc_path"]})
        else:
            defects.append({"item": info["path"], "why": f"{tag}'s owed-at-lock mitigation doc "
                             f"is missing at {info['mitigation_doc_path']}"})

    if credentials_info.get("stray_env_files"):
        for stray in credentials_info["stray_env_files"]:
            defects.append({"item": stray, "why": "an .env-class file is present in the repo "
                             "tree — never committed, but a stray copy here is itself the "
                             "load-bearing-and-unrecoverable risk exception 3 names"})

    # Exception 4 — user-scoped state: always OPEN, per ADR-0022's own ratification gap.
    for item in user_scope_info.get("items", []):
        open_items.append({"item": item["path"], "class": "exception-4-user-scope",
                            "status": "exists" if item["exists"] else "absent"})

    return {
        "defects": defects,
        "enrolled_with_mitigation": enrolled,
        "open": open_items,
        "totals": {
            "defects": len(defects),
            "enrolled_with_mitigation": len(enrolled),
            "open": len(open_items),
        },
    }


def _run_git(repo_root: str, args: list):
    r = subprocess.run(["git", "-C", repo_root, *args], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def _repo_slug(repo_root: str) -> str:
    return str(Path(repo_root).resolve()).replace("/", "-")


def run(repo_root: str, claude_home: str, config_home: str):
    repo = Path(repo_root)
    if not repo.is_dir():
        print(f"audit_reconstructibility: repo-root not found: {repo_root}", file=sys.stderr)
        return None, 2
    gitignore_path = repo / ".gitignore"
    if not gitignore_path.is_file():
        print(f"audit_reconstructibility: no .gitignore at {gitignore_path}", file=sys.stderr)
        return None, 2

    gitignore_patterns = parse_gitignore(gitignore_path.read_text())

    # Check 1 — ignored-and-present paths.
    status_out = _run_git(repo_root, ["status", "--ignored", "--porcelain"])
    ignored_paths = [line[3:] for line in status_out.splitlines() if line.startswith("!! ")]
    ignored_findings = [{"path": p, "class": classify_ignored_path(p, gitignore_patterns)}
                         for p in ignored_paths]

    # Check 2 — .claude/ops/ full-tracking.
    ops_dir = repo / ".claude" / "ops"
    if ops_dir.is_dir():
        tracked = [line for line in _run_git(repo_root, ["ls-files", ".claude/ops"]).splitlines()
                   if line]
        on_disk = [str(p.relative_to(repo)) for p in ops_dir.rglob("*") if p.is_file()]
        ops_ok, ops_missing = check_ops_tracked(tracked, on_disk)
    else:
        ops_ok, ops_missing = True, []
    ops_check = {"ok": ops_ok, "missing": ops_missing}

    # Check 3 — global excludesFile dependency. `core.excludesFile` may be set EXPLICITLY (git
    # config), or IMPLICITLY — git falls back to `$XDG_CONFIG_HOME/git/ignore`
    # (default `~/.config/git/ignore`) whenever that file exists and no explicit config overrides
    # it; a check that only reads the explicit config misses this default-path case entirely
    # (verified: this repo's own settings.local.json rule is invisible to `git config
    # --get core.excludesFile` — it resolves purely through the implicit default).
    explicit_excludes = _run_git(repo_root, ["config", "--get", "core.excludesFile"]).strip()
    if explicit_excludes:
        excludes_path = Path(explicit_excludes).expanduser()
    else:
        excludes_path = Path(config_home) / "git" / "ignore"
    excludes_patterns = []
    if excludes_path.is_file():
        excludes_patterns = parse_gitignore(excludes_path.read_text())
    excludesfile_findings = classify_excludesfile_patterns(excludes_patterns)

    # Check 4 — exception 1, memory dir.
    slug = _repo_slug(repo_root)
    projects_dir = Path(claude_home) / "projects"
    memory_dir_info = {"exists": False, "path": None, "file_count": 0}
    if projects_dir.is_dir():
        for candidate in sorted(projects_dir.glob(f"{slug}*")):
            mem = candidate / "memory"
            if mem.is_dir():
                files = [p for p in mem.glob("*.md") if p.is_file()]
                if not memory_dir_info["exists"] or len(files) > memory_dir_info["file_count"]:
                    memory_dir_info = {"exists": True, "path": str(mem), "file_count": len(files)}

    # Check 5 — exception 2, plugin cache.
    reinstall_doc = repo / ".claude" / "docs" / "runbook" / "plugin-reinstall-path.md"
    cache_dir = Path(claude_home) / "plugins" / "cache"
    plugin_cache_info = {
        "exists": cache_dir.is_dir(),
        "path": str(cache_dir),
        "mitigation_doc_present": reinstall_doc.is_file(),
        "mitigation_doc_path": str(reinstall_doc.relative_to(repo)),
    }

    # Check 6 — exception 3, credentials.
    runbook_doc = repo / ".claude" / "docs" / "runbook" / "credential-reissuance-runbook.md"
    gh_hosts = Path(config_home) / "gh" / "hosts.yml"
    stray_env = [str(p.relative_to(repo)) for p in repo.rglob(".env*")
                 if p.is_file() and ".git" not in p.parts]
    credentials_info = {
        "exists": gh_hosts.is_file(),
        "path": str(gh_hosts),
        "mitigation_doc_present": runbook_doc.is_file(),
        "mitigation_doc_path": str(runbook_doc.relative_to(repo)),
        "stray_env_files": stray_env,
    }

    # Check 7 — exception 4, user-scoped state.
    claude_md = Path(claude_home) / "CLAUDE.md"
    settings_json = Path(claude_home) / "settings.json"
    user_scope_info = {"items": [
        {"path": str(claude_md), "exists": claude_md.is_file()},
        {"path": str(settings_json), "exists": settings_json.is_file()},
    ]}

    report = build_report(
        ignored_findings=ignored_findings,
        ops_check=ops_check,
        excludesfile_findings=excludesfile_findings,
        memory_dir_info=memory_dir_info,
        plugin_cache_info=plugin_cache_info,
        credentials_info=credentials_info,
        user_scope_info=user_scope_info,
    )
    exit_code = 1 if report["totals"]["defects"] else 0
    return report, exit_code


def _print_report(report):
    print(f"audit_reconstructibility · defects={report['totals']['defects']} "
          f"enrolled={report['totals']['enrolled_with_mitigation']} "
          f"open={report['totals']['open']}")
    if report["defects"]:
        print("  DEFECTS:")
        for d in report["defects"]:
            print(f"    - {d['item']}: {d['why']}")
    if report["enrolled_with_mitigation"]:
        print("  ENROLLED-WITH-MITIGATION:")
        for e in report["enrolled_with_mitigation"]:
            print(f"    - {e['item']} ({e['class']})")
    if report["open"]:
        print("  OPEN (ADR-0022 ratification gap, exception 4):")
        for o in report["open"]:
            print(f"    - {o['item']} ({o['class']})")


def selftest():
    # parse_gitignore — comments/blanks stripped, order preserved
    assert parse_gitignore("# c\n\ndist/\n.claude/worktrees/\n") == ["dist/", ".claude/worktrees/"]

    # classify_ignored_path — repo-declared regenerable
    assert classify_ignored_path("dist/foo.plugin", ["dist/", ".claude/worktrees/"]) == "regenerable"
    assert classify_ignored_path(".claude/worktrees/scratch", ["dist/", ".claude/worktrees/"]) == "regenerable"
    # named exception (settings.local.json) recognized regardless of gitignore content
    assert classify_ignored_path(".claude/settings.local.json", []) == "exception-4-user-scope"
    # reverse control: an uncategorized ignored path must NOT silently pass as regenerable
    assert classify_ignored_path("some/random/local-state.db", ["dist/"]) == "uncategorized"

    # check_ops_tracked — clean case
    ok, missing = check_ops_tracked(
        tracked=[".claude/ops/fleet.json", ".claude/ops/plan.md"],
        on_disk=[".claude/ops/fleet.json", ".claude/ops/plan.md"])
    assert ok and missing == []
    # negative control: an on-disk file absent from git ls-files must be caught, never silent
    ok, missing = check_ops_tracked(
        tracked=[".claude/ops/fleet.json"],
        on_disk=[".claude/ops/fleet.json", ".claude/ops/rogue-local-state.json"])
    assert not ok and missing == [".claude/ops/rogue-local-state.json"]

    # classify_excludesfile_patterns — pure passthrough with the exception-4 tag
    tagged = classify_excludesfile_patterns(["**/.claude/settings.local.json"])
    assert len(tagged) == 1 and tagged[0]["class"] == "exception-4-user-scope"
    # reverse control: no excludesFile patterns -> empty, never fabricated
    assert classify_excludesfile_patterns([]) == []

    # build_report — full assembly, one of each bucket, defect wins the exit-code test upstream
    report = build_report(
        ignored_findings=[
            {"path": "dist/x.plugin", "class": "regenerable"},
            {"path": "some/rogue.db", "class": "uncategorized"},
            {"path": ".claude/settings.local.json", "class": "exception-4-user-scope"},
        ],
        ops_check={"ok": False, "missing": [".claude/ops/rogue.json"]},
        excludesfile_findings=[{"pattern": "**/.claude/settings.local.json",
                                 "class": "exception-4-user-scope", "reason": "r"}],
        memory_dir_info={"exists": True, "path": "/h/.claude/projects/x/memory", "file_count": 5},
        plugin_cache_info={"exists": True, "path": "/h/.claude/plugins/cache",
                            "mitigation_doc_present": True,
                            "mitigation_doc_path": ".claude/docs/runbook/plugin-reinstall-path.md"},
        credentials_info={"exists": True, "path": "/h/.config/gh/hosts.yml",
                           "mitigation_doc_present": False,
                           "mitigation_doc_path": ".claude/docs/runbook/credential-reissuance-runbook.md",
                           "stray_env_files": ["backend/.env"]},
        user_scope_info={"items": [{"path": "/h/.claude/CLAUDE.md", "exists": True}]},
    )
    # defects: rogue ignored path + ops-untracked file + missing credential runbook + stray .env
    assert report["totals"]["defects"] == 4, report
    # enrolled: exception-4 settings.local.json (from ignored_findings) + memory dir + plugin cache
    assert report["totals"]["enrolled_with_mitigation"] == 3, report
    # open: excludesfile finding + user-scope item
    assert report["totals"]["open"] == 2, report
    # reverse control: a fully clean input produces zero defects, zero open, zero enrolled
    clean = build_report(
        ignored_findings=[], ops_check={"ok": True, "missing": []},
        excludesfile_findings=[],
        memory_dir_info={"exists": False, "path": None, "file_count": 0},
        plugin_cache_info={"exists": False, "path": "x", "mitigation_doc_present": False,
                            "mitigation_doc_path": "x"},
        credentials_info={"exists": False, "path": "x", "mitigation_doc_present": False,
                           "mitigation_doc_path": "x", "stray_env_files": []},
        user_scope_info={"items": []},
    )
    assert clean["totals"] == {"defects": 0, "enrolled_with_mitigation": 0, "open": 0}, clean

    print("audit_reconstructibility selftest · PASS · classify_ignored_path (regenerable / "
          "named-exception / uncategorized-as-defect-candidate), check_ops_tracked "
          "(clean + untracked-file negative control), classify_excludesfile_patterns "
          "(passthrough + empty), and build_report's full trichotomy(+open) assembly "
          "(4 defects / 3 enrolled / 2 open) plus its all-clean reverse control all pass")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo-root")
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--config-home", default=str(Path.home() / ".config"))
    parser.add_argument("--json", action="store_true")
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selftest":
        return selftest()
    try:
        ns = parser.parse_args(argv)
    except SystemExit:
        return 2
    if not ns.repo_root:
        print("audit_reconstructibility: --repo-root is required", file=sys.stderr)
        return 2
    try:
        report, exit_code = run(ns.repo_root, ns.claude_home, ns.config_home)
    except RuntimeError as e:
        print(f"audit_reconstructibility: {e}", file=sys.stderr)
        return 2
    if report is None:
        return exit_code
    if ns.json:
        print(json.dumps(report, indent=2))
    else:
        _print_report(report)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
