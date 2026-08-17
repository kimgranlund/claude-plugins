#!/usr/bin/env python3
"""trend_hook.py — ship-time automatic trend capture (issue #294, part (b)).

Wires `trend.py`'s per-release trend series (v0.10.0, never invoked by
anything until now) into an actual ship-time signal, instead of depending on
a human remembering to run it by hand — scoped AUTHORKIT-SIDE ONLY. #294's
own scoping note: the harness version slot (`release_gate.py` /
`ship-plugin`) is issue #313's own concurrent dispatch right now; wiring this
into either of those harness files would collide with that in-flight work
AND force a harness version bump this dispatch has no standing to make.
Decision recorded here rather than silently taken: this hook is the
authorkit-side implementation; a harness-native rider (calling `trend.py`
straight out of `release_gate.py`'s own G6 package step, so it fires exactly
once per `--package` run rather than on every raw version-bump write) is a
reasonable FOLLOW-UP once #313 releases the harness slot — not built here.

The observable, harness-independent proxy for "a plugin just shipped": its
OWN `.claude-plugin/plugin.json` `version` field changed. Every plugin bump
in this workspace happens right before/around running `release_gate.py
--package` per the workspace CLAUDE.md's Invariants ("never re-ship a
version ... bump every change") — a version-bump write IS the ship-time
signal, independent of which command performed the bump.

Same derive-target-from-write plumbing as collide_hook.py (issue #276/#287's
shape): the WRITTEN file decides the checkout root and the plugin, never
`$CLAUDE_PROJECT_DIR` or a fixed list — worktree-correct by construction.

Captures ONE row for the ONE plugin that just shipped, not a full-estate
sweep — "per-release" means per release EVENT. `rent.py`'s own
`find_plugins()` already resolves a single-plugin target correctly (it walks
for a `.claude-plugin/plugin.json` marker, which a lone plugin dir satisfies
at its own root, so pointing it straight at the shipped plugin's directory
produces exactly one row). No routing-report is available at hook time (that
needs harness check-routing's LLM-judged run) — the dead/stolen/leaked
columns record the literal `absent`, exactly as a manual `trend.py` run
without `--routing-report` already does; never an invented number.

Fail-open discipline, identical to collide_hook.py and #287's precedent: a
malformed event, a non-dict shape, a missing file_path, no derivable git
root, an unreadable/malformed plugin.json, or ANY unexpected exception all
exit 0 silently. A flaky governance hook is worse than none.

Usage:
  trend_hook.py                    PostToolUse entry point, reads the hook
                                    event off stdin
  trend_hook.py selftest           prove the counters bite

Exit: always 0 — this hook only ever appends a CSV row or no-ops; it never
gates or blocks (trend capture is bookkeeping, not a judgment call, so it
carries none of collide_hook.py's advisory exit-2 tier).
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import rent  # noqa: E402  (sibling module, same scripts/ dir)
    import trend  # noqa: E402
except Exception:
    # hook-checker finding (2026-08-16): a broken sibling module must never surface as an
    # uncaught ImportError/traceback on every single write — fail open at import time too,
    # not just inside run_hook's own try/except (which never even gets a chance to run).
    rent = None
    trend = None


def find_repo_root(path: Path):
    """Same shape as collide_hook.py / naming-audit's validate.py (issue #276)."""
    cwd = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return Path(out.stdout.strip())


def find_durable_root(path: Path):
    """The PRIMARY checkout's own root — never the worktree's (hook-checker finding,
    2026-08-16). `find_repo_root`'s `--show-toplevel` correctly answers "which checkout did
    this write land in" for MEASUREMENT (worktree-correct, #276's whole point), but a trend
    row appended there dies the moment `campaign_close.py` deletes that worktree at the end
    of an ADR-0002 campaign — exactly the ship path this workspace uses. `--git-common-dir`
    answers a DIFFERENT question: every linked worktree of the same repo shares one common
    `.git` (verified 2026-08-16: from inside a `.claude/worktrees/<id>` checkout it resolves
    to the PRIMARY checkout's own `.git`, not a copy) — its parent is a durable home the
    worktree's own removal can never touch. Fail open (None) on any git failure, same as
    `find_repo_root`."""
    cwd = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--git-common-dir"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    common_dir = Path(out.stdout.strip())
    if not common_dir.is_absolute():
        # `--git-common-dir` prints RELATIVE TO THE `-C` DIRECTORY, never the calling
        # process's own os.getcwd() (measured 2026-08-16: a fresh non-worktree repo returns
        # `../../.git`) — resolving it against the process cwd instead of `cwd` here silently
        # produced a path outside the target repo entirely. `--show-toplevel` is documented
        # to always print absolute, so this guard is specific to this one subcommand.
        common_dir = cwd / common_dir
    return common_dir.resolve().parent


def prior_version(repo_root: Path, rel: Path):
    """The plugin.json's `version` field as of HEAD, or None when there's no HEAD
    blob at all (a brand-new plugin.json — always treated as a bump, its first)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "show", f"HEAD:{rel.as_posix()}"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    try:
        manifest = json.loads(out.stdout)
    except json.JSONDecodeError:
        return None
    return manifest.get("version") if isinstance(manifest, dict) else None


def run_hook(file_path: str) -> int:
    """Core logic, factored out of stdin parsing so selftest can drive it
    directly against fixture paths without faking a stdin event. Always
    returns 0 — every branch either appends a row or no-ops."""
    if rent is None or trend is None:
        return 0  # sibling modules failed to import — fail open, nothing else can run
    if not file_path.replace("\\", "/").endswith(".claude-plugin/plugin.json"):
        return 0
    p = Path(file_path)
    if not p.is_absolute() or not p.is_file():
        return 0
    try:
        new_manifest = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, json.JSONDecodeError):
        return 0
    if not isinstance(new_manifest, dict):
        return 0
    new_version = new_manifest.get("version")
    if not new_version:
        return 0  # no version field at all — nothing to detect a bump against
    repo_root = find_repo_root(p)
    if repo_root is None:
        return 0
    try:
        rel = p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return 0
    old_version = prior_version(repo_root, rel)
    if old_version == new_version:
        return 0  # not a version bump — a metadata-only plugin.json edit
    plugin_root = p.parent.parent  # <plugin>/.claude-plugin/plugin.json -> <plugin>
    durable_root = find_durable_root(p) or repo_root  # never lose the row for want of a
    # git-common-dir answer — the worktree root is still a legitimate (if less durable) home
    try:
        rent_data = rent.run(str(plugin_root))
        out_csv = durable_root / "attention-trend.csv"
        trend.append_rows(rent_data, None, str(out_csv), datetime.date.today().isoformat())
    except Exception:
        return 0  # fail open — an internal rent.py/trend.py bug never blocks the write loop
    return 0


def main_hook_stdin() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(event, dict):
        return 0
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    file_path = tool_input.get("file_path", "")
    if not isinstance(file_path, str) or not file_path:
        return 0
    try:
        return run_hook(file_path)
    except Exception:
        return 0  # belt-and-suspenders: nothing escapes this hook ungracefully


def selftest() -> int:
    import csv
    import tempfile

    def git(root, *args):
        subprocess.run(["git", "-C", str(root), *args], check=True,
                        capture_output=True, text=True)

    def write_manifest(root, plugin, version):
        d = Path(root) / plugin / ".claude-plugin"
        d.mkdir(parents=True, exist_ok=True)
        (d / "plugin.json").write_text(json.dumps({"name": plugin, "version": version}))
        return d / "plugin.json"

    def write_skill(root, plugin, skill, desc):
        d = Path(root) / plugin / "skills" / skill
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: {desc}\n---\n\n# {skill}\n")

    def fresh_repo():
        td = tempfile.mkdtemp()
        git(td, "init", "-q")
        git(td, "config", "user.email", "t@t.t")
        git(td, "config", "user.name", "t")
        return td

    # 1. non-plugin.json write -> no-op, no CSV created
    td = fresh_repo()
    manifest = write_manifest(td, "p1", "1.0.0")
    write_skill(td, "p1", "alpha", "ten char desc here")
    git(td, "add", "-A")
    git(td, "commit", "-q", "-m", "seed")
    other = Path(td) / "p1" / "README.md"
    other.write_text("hi")
    assert run_hook(str(other)) == 0
    assert not (Path(td) / "attention-trend.csv").exists(), \
        "a non-plugin.json write must never create the trend CSV"

    # 2. re-write with the SAME version -> exit 0, no row appended (not a bump)
    assert run_hook(str(manifest)) == 0
    assert not (Path(td) / "attention-trend.csv").exists(), \
        "an unchanged version must no-op, never append"

    # 3. brand-new plugin.json (no HEAD blob) -> treated as a bump, one row appended
    td = fresh_repo()
    new_manifest = write_manifest(td, "p2", "0.1.0")
    write_skill(td, "p2", "beta", "another routable description text")
    assert run_hook(str(new_manifest)) == 0
    csv_path = Path(td) / "attention-trend.csv"
    assert csv_path.is_file(), "a brand-new plugin.json must append its first trend row"
    rows = list(csv.reader(open(csv_path)))
    assert rows[0] == trend.HEADER, rows
    assert len(rows) == 2 and rows[1][1] == "p2", rows
    assert rows[1][8:] == ["absent", "absent", "absent"], \
        "no routing report at hook time — dead/stolen/leaked must record the literal absent"

    # 4. real version bump on an existing committed plugin.json -> exit 0, row appended
    td = fresh_repo()
    manifest = write_manifest(td, "p3", "1.0.0")
    write_skill(td, "p3", "gamma", "yet another description")
    git(td, "add", "-A")
    git(td, "commit", "-q", "-m", "seed")
    write_manifest(td, "p3", "1.1.0")
    assert run_hook(str(manifest)) == 0
    csv_path = Path(td) / "attention-trend.csv"
    assert csv_path.is_file()
    rows = list(csv.reader(open(csv_path)))
    assert len(rows) == 2 and rows[1][1] == "p3", rows

    # 5. only ONE plugin's row is appended, not a full-estate sweep — a sibling plugin in
    #    the SAME repo must never show up in the appended row set
    assert not any(r[1] == "p1" for r in rows), "must scope to the shipped plugin only"

    # 6. non-dict / malformed stdin event -> fail open, and a real event still appends
    old_stdin = sys.stdin

    def feed(text):
        import io
        sys.stdin = io.StringIO(text)

    try:
        feed("not json")
        assert main_hook_stdin() == 0
        feed(json.dumps([1, 2]))
        assert main_hook_stdin() == 0
        feed(json.dumps({"tool_input": "oops"}))
        assert main_hook_stdin() == 0
        feed(json.dumps({"tool_input": {"file_path": 12345}}))
        assert main_hook_stdin() == 0
        td2 = fresh_repo()
        m2 = write_manifest(td2, "p4", "0.0.1")
        write_skill(td2, "p4", "delta", "some description here")
        feed(json.dumps({"tool_input": {"file_path": str(m2)}}))
        assert main_hook_stdin() == 0
        assert (Path(td2) / "attention-trend.csv").is_file(), \
            "a real event through stdin must still append"
    finally:
        sys.stdin = old_stdin

    # 7. relative path / no git repo -> fail open, never crash
    assert run_hook("relative/.claude-plugin/plugin.json") == 0
    bare = tempfile.mkdtemp()
    lone = write_manifest(bare, "p5", "1.0.0")
    write_skill(bare, "p5", "epsilon", "lone plugin description")
    assert run_hook(str(lone)) == 0
    assert not (Path(bare) / "attention-trend.csv").exists(), \
        "outside any git checkout, no version-delta can be proven — must no-op, not guess"

    # 8. no "version" field at all -> no-op
    td3 = fresh_repo()
    empty = Path(td3) / "p6" / ".claude-plugin"
    empty.mkdir(parents=True)
    (empty / "plugin.json").write_text(json.dumps({"name": "p6"}))
    assert run_hook(str(empty / "plugin.json")) == 0
    assert not (Path(td3) / "attention-trend.csv").exists()

    # 9. WORKTREE DURABILITY (hook-checker major finding, 2026-08-16): a version bump written
    #    inside a LINKED worktree must append its row at the PRIMARY checkout's root, never the
    #    worktree's own — the worktree is exactly what `campaign_close.py` deletes at the end of
    #    an ADR-0002 campaign, so a row left there would die with it.
    primary = fresh_repo()
    write_manifest(primary, "p7", "1.0.0")
    write_skill(primary, "p7", "zeta", "a description for the worktree scenario")
    git(primary, "add", "-A")
    git(primary, "commit", "-q", "-m", "seed p7")
    wt_branch = "wt-scenario"
    wt_path = Path(primary).parent / "p7-worktree"
    git(primary, "worktree", "add", "-b", wt_branch, str(wt_path))
    wt_manifest = wt_path / "p7" / ".claude-plugin" / "plugin.json"
    wt_manifest.write_text(json.dumps({"name": "p7", "version": "1.1.0"}))
    assert run_hook(str(wt_manifest)) == 0
    assert (Path(primary) / "attention-trend.csv").is_file(), \
        "a worktree-written version bump must append at the PRIMARY checkout's root"
    assert not (wt_path / "attention-trend.csv").exists(), \
        "the row must NOT land inside the (deletable) worktree itself"

    print("trend_hook.py selftest: PASS")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        return selftest()
    return main_hook_stdin()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"trend_hook.py error: {e}", file=sys.stderr)
        sys.exit(0)  # even the top-level catch-all fails OPEN, never a nonzero exit on a crash
