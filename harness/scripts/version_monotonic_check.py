#!/usr/bin/env python3
"""version_monotonic_check — a PR's plugin version must exceed origin/main's, ledger must match.

Usage:
  version_monotonic_check.py <plugin-root>
  version_monotonic_check.py selftest

Issue #445: the pre-merge, CI-visible tier of version discipline. `version_claim_check.py`
(#311/PR #329) is the coordinator-run, cross-PR-visible tier — it sees sibling OPEN PRs via
`gh`, which CI structurally cannot. This script is the complementary tier CI CAN see per PR: for
ONE plugin root, on the branch checked out, it FAILs when the branch's `.claude-plugin/
plugin.json` version is not strictly greater than the same plugin's version on `origin/main`, or
when the branch's README ledger's newest `vX.Y.Z` line does not name that branch version. It
reuses `version_claim_check.py`'s `parse_version`/`version_tuple` helpers rather than
reimplementing them.

Checks:
  M1 [SKIP] not applicable: `origin/main` is unreachable in this checkout (no fetch, or the ref
            is missing — never a false red), the plugin carries no diff against `origin/main`
            (untouched, including a `push` to `main` itself where HEAD IS origin/main), or the
            plugin's manifest doesn't exist on `origin/main` at all (a brand-new plugin, no
            baseline to compare)
  M2 [FAIL] the branch's version is <= origin/main's version — the #425/#430 negative control:
            two sibling PRs both bumped teamwork `2.16.2 -> 2.16.3`; whichever merged second
            would still carry a version already claimed by main once the first landed
  M3 [FAIL] the branch's README.md footer's newest `vX.Y.Z` ledger line doesn't name the
            branch's own plugin.json version

Exit 0 clean or SKIP (both non-blocking), 1 on any FAIL, 2 on a usage error.

"Touched" is git-diff-against-origin/main scoped to the plugin root, not just manifest/README —
any file under the plugin root counts (a plugin whose behavior changed but whose version wasn't
bumped is exactly the defect this check exists to catch).
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from version_claim_check import parse_version, version_tuple

LEDGER_RE = re.compile(r"^v(\d+\.\d+\.\d+)\b", re.M)


def parse_ledger_version(readme_text: str):
    """Pure: the newest (first) `vX.Y.Z` footer ledger line in a README's raw text. None if
    absent — mirrors docs_check.py's R3 pattern, restated here so this check is self-contained
    and its own selftest fixtures prove it directly."""
    m = LEDGER_RE.search(readme_text)
    return m.group(1) if m else None


def check_monotonic(branch_version: str, main_version: str):
    """Pure. Returns (ok, msg)."""
    if version_tuple(branch_version) <= version_tuple(main_version):
        return False, (f"branch version {branch_version} <= origin/main's {main_version} -> "
                        "bump strictly forward; reissuing or regressing a version is a collision")
    return True, f"{branch_version} > origin/main's {main_version}"


def check_ledger(branch_version: str, readme_text: str):
    """Pure. Returns (ok, msg)."""
    ledger_v = parse_ledger_version(readme_text)
    if ledger_v is None:
        return False, "README carries no `vX.Y.Z` footer ledger line"
    if ledger_v != branch_version:
        return False, (f"README's newest ledger line says v{ledger_v} but plugin.json says "
                        f"{branch_version} -> the ledger lies about the current release")
    return True, f"ledger's newest line matches v{branch_version}"


def _git(args, cwd):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)


def _origin_main_available(git_root: Path) -> bool:
    return _git(["rev-parse", "--verify", "-q", "origin/main"], git_root).returncode == 0


def _plugin_touched(git_root: Path, rel_root: str) -> bool:
    # --quiet: exit 0 = no diff, 1 = diff found, anything else = error (bad ref, etc).
    r = _git(["diff", "--quiet", "origin/main", "--", rel_root], git_root)
    return r.returncode == 1


def _file_at_main(git_root: Path, relpath: str):
    r = _git(["show", f"origin/main:{relpath}"], git_root)
    return r.stdout if r.returncode == 0 else None


def run(plugin_root: Path):
    plugin_root = plugin_root.resolve()
    top = _git(["rev-parse", "--show-toplevel"], plugin_root)
    if top.returncode != 0:
        _skip(f"{plugin_root} is not inside a git checkout -> not applicable")
        return 0
    git_root = Path(top.stdout.strip())
    rel = plugin_root.relative_to(git_root).as_posix()

    if not _origin_main_available(git_root):
        _skip("origin/main is not available in this checkout (no fetch, or the ref is missing) "
              "-> version-monotonicity check skipped, never a false red")
        return 0

    if not _plugin_touched(git_root, rel):
        _skip(f"{rel} carries no diff against origin/main -> untouched, not applicable")
        return 0

    manifest_rel = f"{rel}/.claude-plugin/plugin.json"
    main_manifest_text = _file_at_main(git_root, manifest_rel)
    if main_manifest_text is None:
        _skip(f"{manifest_rel} does not exist on origin/main -> new plugin, no baseline to compare")
        return 0
    main_version = parse_version(main_manifest_text)
    if main_version is None:
        _fail_report([("M0", False, f"origin/main's {manifest_rel} has no readable \"version\" field")])
        return 1

    local_manifest = plugin_root / ".claude-plugin" / "plugin.json"
    branch_version = parse_version(local_manifest.read_text()) if local_manifest.is_file() else None
    if branch_version is None:
        _fail_report([("M0", False, f"{local_manifest} has no readable \"version\" field")])
        return 1

    readme_path = plugin_root / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.is_file() else ""

    ok_mono, msg_mono = check_monotonic(branch_version, main_version)
    ok_ledger, msg_ledger = check_ledger(branch_version, readme_text)
    findings = [("M2", ok_mono, msg_mono), ("M3", ok_ledger, msg_ledger)]
    ok = ok_mono and ok_ledger
    print(f"version_monotonic_check · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg in findings:
        print(f"  {'ok  ' if item_ok else 'FAIL'} {code}  {msg}")
    return 0 if ok else 1


def _skip(msg):
    print("version_monotonic_check · SKIP")
    print(f"  skip  M1  {msg}")


def _fail_report(findings):
    print("version_monotonic_check · FAIL")
    for code, item_ok, msg in findings:
        print(f"  {'ok  ' if item_ok else 'FAIL'} {code}  {msg}")


def selftest():
    import tempfile

    # --- pure functions, fixture data only ---

    # check_monotonic — strictly-greater PASS
    ok, msg = check_monotonic("2.16.3", "2.16.2")
    assert ok, "a strictly forward bump must pass"

    # check_monotonic — equal-version FAIL (the #425/#430 2.16.2 -> 2.16.3 collision's shape:
    # once one PR merges and bumps main to 2.16.3, a sibling still claiming 2.16.3 is now equal,
    # not ahead)
    ok, msg = check_monotonic("2.16.3", "2.16.3")
    assert not ok, "a claim equal to origin/main's version must FAIL, not pass"
    assert "2.16.3" in msg

    # check_monotonic — lower-version FAIL
    ok, msg = check_monotonic("2.16.1", "2.16.3")
    assert not ok, "a claim behind origin/main's version must FAIL"

    # parse_ledger_version / check_ledger — matching ledger PASSes
    ok, msg = check_ledger("2.16.3", "map: x\n\nv2.16.3 · 2026-08-16 · did a thing\n")
    assert ok, "a ledger whose newest line names the branch version must pass"

    # check_ledger — mismatched ledger FAILs (stale ledger, forgot to add the new line)
    ok, msg = check_ledger("2.16.3", "map: x\n\nv2.16.2 · 2026-08-15 · did an earlier thing\n")
    assert not ok, "a ledger whose newest line is behind plugin.json must FAIL"

    # check_ledger — no ledger line at all FAILs, never silently skipped
    ok, msg = check_ledger("2.16.3", "no ledger here\n")
    assert not ok, "a README with no vX.Y.Z line must FAIL, not be silently ignored"

    # --- end-to-end via a real git fixture: origin/main-missing SKIP, touched/untouched,
    # and the full PASS/FAIL run() path, all on real git plumbing (not mocked) ---

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)

        plugin = root / "demo"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "demo", "version": "1.0.0"}')
        (plugin / "README.md").write_text("map: demo\n\nv1.0.0 · 2026-08-01 · initial\n")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        # No origin remote at all yet -> origin/main unavailable -> SKIP, not a false red.
        code = run(plugin)
        assert code == 0, "no origin/main at all must SKIP clean, never fail"

        # Fake an "origin/main" ref pointing at the initial commit (stand-in for a real fetch).
        main_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                   text=True, check=True).stdout.strip()
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", main_sha], cwd=root, check=True)

        # Branch identical to origin/main -> untouched -> SKIP (also the push-to-main shape:
        # HEAD == origin/main means nothing to compare).
        code = run(plugin)
        assert code == 0, "a plugin with no diff against origin/main must SKIP, not FAIL"

        # Bump forward correctly (version + matching ledger line) -> touched, PASS.
        (plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "demo", "version": "1.1.0"}')
        (plugin / "README.md").write_text("map: demo\n\nv1.1.0 · 2026-08-16 · a real bump\n")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump"], cwd=root, check=True)
        code = run(plugin)
        assert code == 0, "a strictly-forward bump with a matching ledger line must PASS"

        # Reissue the SAME version main already carries (the #425/#430 collision shape) -> FAIL.
        # Advance origin/main to the 1.1.0 commit, then re-claim 1.1.0 on the branch again.
        bumped_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                     text=True, check=True).stdout.strip()
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", bumped_sha], cwd=root, check=True)
        (plugin / "README.md").write_text("map: demo\n\nv1.1.0 · 2026-08-16 · touch readme only\n")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "touch readme only, same version"], cwd=root, check=True)
        code = run(plugin)
        assert code == 1, "reissuing origin/main's own current version must FAIL (the #425/#430 negative control)"

        # Ledger-mismatch FAIL: version bumped forward, ledger line left stale.
        (plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "demo", "version": "1.2.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump manifest, forget ledger"], cwd=root, check=True)
        code = run(plugin)
        assert code == 1, "a forward version bump with a stale ledger line must FAIL M3"

        # New plugin never on origin/main at all -> SKIP, no baseline to compare.
        new_plugin = root / "brandnew"
        (new_plugin / ".claude-plugin").mkdir(parents=True)
        (new_plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "brandnew", "version": "0.1.0"}')
        (new_plugin / "README.md").write_text("map: brandnew\n\nv0.1.0 · 2026-08-16 · new\n")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "new plugin"], cwd=root, check=True)
        code = run(new_plugin)
        assert code == 0, "a plugin absent from origin/main entirely must SKIP, not FAIL"

    print("version_monotonic_check selftest · PASS · strictly-greater PASS, equal-version FAIL "
          "(the #425/#430 2.16.3 negative control), lower-version FAIL, ledger-mismatch FAIL, "
          "and origin/main-missing/untouched/new-plugin all SKIP clean, on real git plumbing")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(argv[0])))
