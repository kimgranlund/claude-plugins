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
            branch's own plugin.json version. Ticket #249 (adiahealth/adia-harness): a plugin
            README carrying no `vX.Y.Z` ledger line at all (rather than a stale/mismatched one)
            falls back to the newest GitHub Release or, when Releases are unreachable, the
            newest `git describe --tags` tag — the branch version AHEAD OF OR EQUAL TO that
            fallback (adiahealth/adia-harness#265: `version_tuple` compare, not string equality
            — the normal pre-merge-PR and post-ship-main states respectively) downgrades M3 to a
            [WARN] naming the fallback source used, never a silent PASS and never blocking; the
            branch version BEHIND the fallback, no fallback resolving at all, or a README that
            DOES carry a ledger line but it's wrong, all stay a [FAIL]. `release_gate.py`'s own
            G14 block composes this exact function (`check_ledger_with_fallback`) rather than
            calling bare `check_ledger` — adiahealth/adia-harness#265's root cause was G14
            bypassing the fallback entirely.

Exit 0 clean, SKIP, or WARN-only (all non-blocking), 1 on any FAIL, 2 on a usage error.

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


_TAG_VERSION_RE = re.compile(r"(?:^|[-_/])v?(\d+\.\d+\.\d+)$")


def _extract_version(tag):
    """Pure. Extracts an `X.Y.Z` version from a tag that may carry a plugin-name prefix (this
    repo's own real shape is `adia-sdlc-v0.6.76`, not a bare `v0.6.76`) — matches a trailing
    `-`/`_`/`/`-delimited (or bare, unprefixed) `vX.Y.Z`/`X.Y.Z` at the END of the string. Returns
    None on no match, never a raise or a garbage partial string."""
    m = _TAG_VERSION_RE.search(tag)
    return m.group(1) if m else None


def resolve_release_ledger_fallback(git_root, run_fn=None):
    """Ticket #249 (adiahealth/adia-harness). Test-injectable via `run_fn` (a callable taking
    `(*args)` and returning stdout, or raising on failure — mirrors this repo's own adapter
    transport seams elsewhere) so `selftest` never touches the real network or `gh`. Tries the
    newest GitHub Release first (`gh release list --limit 1 --json tagName`); on ANY failure
    (no `gh`, no auth, offline, not a GitHub remote) OR an unparseable tag name falls back to the
    newest local git tag (`git describe --tags --abbrev=0`). Both tag names are read through
    `_extract_version` — a plugin-prefixed tag (`adia-sdlc-v0.6.76`, this repo's own real shape,
    not a bare `v0.6.76`) resolves exactly like a bare one. Returns
    `(source: str|None, version: str|None)` — both None when neither resolves (a brand-new repo
    with no tags at all, or a tag whose shape doesn't carry a version at all), never a raise."""
    if run_fn is not None:
        try:
            out = run_fn("gh", "release", "list", "--limit", "1", "--json", "tagName")
            import json as _json
            data = _json.loads(out)
            if data:
                v = _extract_version(data[0]["tagName"])
                if v is not None:
                    return "GitHub Releases", v
        except Exception:  # noqa: BLE001 — any gh failure degrades to the git-tag fallback below
            pass
        try:
            out = run_fn("git", "describe", "--tags", "--abbrev=0")
            tag = out.strip()
            v = _extract_version(tag) if tag else None
            return ("newest git tag", v) if v is not None else (None, None)
        except Exception:  # noqa: BLE001
            return None, None

    gh = subprocess.run(
        ["gh", "release", "list", "--limit", "1", "--json", "tagName"],
        capture_output=True, text=True, cwd=git_root,
    )
    if gh.returncode == 0 and gh.stdout.strip():
        try:
            import json as _json
            data = _json.loads(gh.stdout)
            if data:
                v = _extract_version(data[0]["tagName"])
                if v is not None:
                    return "GitHub Releases", v
        except ValueError:
            pass
    tag = _git(["describe", "--tags", "--abbrev=0"], git_root)
    if tag.returncode == 0 and tag.stdout.strip():
        v = _extract_version(tag.stdout.strip())
        if v is not None:
            return "newest git tag", v
    return None, None


def check_ledger_with_fallback(branch_version: str, readme_text: str, git_root, run_fn=None):
    """Composes `check_ledger` with the ticket-#249 fallback (`resolve_release_ledger_fallback`)
    — the ONE place this composition lives; `run()` below and `release_gate.py`'s own G14 block
    both call this rather than each re-deriving the fallback-triggering condition or its
    comparison semantics. Returns `(ok: bool, severity: 'FAIL'|'WARN'|'ok', msg: str)`.

    A README carrying a ledger line at all (even a stale/wrong one) never triggers the fallback —
    that stays a straight FAIL, byte-identical to pre-#249 behavior. Only the "no ledger line at
    all" case falls back to the newest GitHub Release or git tag.

    Comparison semantics (this fix, adiahealth/adia-harness#265): the branch's `plugin.json`
    version is compared against the fallback version with `version_tuple`, not string equality —
    a branch STRICTLY AHEAD of the newest Release/tag (the normal pre-merge state of every open
    PR that bumped its version) is ok; EQUAL (the normal post-ship state of `main` itself, once
    the Release matching that version has been cut) is also ok; BEHIND is a real FAIL, never a
    transient one. Both ahead and equal WARN naming the fallback source — this is a fallback
    determination, never a silent PASS. No fallback resolving at all (no Release, no tag) stays a
    FAIL naming that gap."""
    ok_ledger, msg_ledger = check_ledger(branch_version, readme_text)
    if ok_ledger:
        return True, "ok", msg_ledger
    if parse_ledger_version(readme_text) is not None:
        return False, "FAIL", msg_ledger  # a ledger line exists but is wrong -> straight FAIL

    source, fallback_version = resolve_release_ledger_fallback(git_root, run_fn=run_fn)
    if fallback_version is None:
        return False, "FAIL", (msg_ledger + "; fallback also unresolvable (no GitHub Release and "
                                             "no local git tag)")
    if version_tuple(branch_version) >= version_tuple(fallback_version):
        relation = "matches" if fallback_version == branch_version else "is ahead of"
        return True, "WARN", (f"README carries no ledger line; verified via fallback ({source}): "
                               f"branch {branch_version} {relation} the newest {fallback_version}")
    return False, "FAIL", (f"README carries no ledger line; fallback ({source}) newest is "
                            f"{fallback_version}, plugin.json says {branch_version} -> plugin.json "
                            "is BEHIND the newest Release/tag")


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
    ok_ledger, ledger_sev, msg_ledger = check_ledger_with_fallback(branch_version, readme_text, git_root)

    ok = ok_mono and ok_ledger
    print(f"version_monotonic_check · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg, sev in [("M2", ok_mono, msg_mono, "FAIL"), ("M3", ok_ledger, msg_ledger, ledger_sev)]:
        label = "warn" if (item_ok and sev == "WARN") else ("ok  " if item_ok else "FAIL")
        print(f"  {label} {code}  {msg}")
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

    # ---- Ticket #249 (adiahealth/adia-harness): ledger-absent Release/tag fallback ----

    def _run_fn_gh_ok(*args):
        if args[:2] == ("gh", "release"):
            return '[{"tagName": "v2.5.0"}]'
        raise AssertionError(f"unexpected call in _run_fn_gh_ok: {args}")

    source, version = resolve_release_ledger_fallback(Path("."), run_fn=_run_fn_gh_ok)
    assert (source, version) == ("GitHub Releases", "2.5.0"), \
        f"positive control: a resolvable GitHub Release must be preferred: {(source, version)}"

    def _run_fn_gh_unreachable_git_ok(*args):
        if args[:2] == ("gh", "release"):
            raise RuntimeError("gh: authentication required")
        if args[:2] == ("git", "describe"):
            return "v2.4.0\n"
        raise AssertionError(f"unexpected call: {args}")

    source2, version2 = resolve_release_ledger_fallback(Path("."), run_fn=_run_fn_gh_unreachable_git_ok)
    assert (source2, version2) == ("newest git tag", "2.4.0"), \
        f"positive control: GitHub Releases unreachable must fall back to the newest git tag: {(source2, version2)}"

    def _run_fn_nothing(*args):
        raise RuntimeError("nothing resolves")

    source3, version3 = resolve_release_ledger_fallback(Path("."), run_fn=_run_fn_nothing)
    assert (source3, version3) == (None, None), \
        f"negative control: neither Releases nor a git tag resolving must degrade to (None, None), never raise: {(source3, version3)}"

    # Live fixture control (adiahealth/adia-harness#249 review): this repo's own real tag shape
    # is plugin-prefixed (`adia-sdlc-v0.6.76`), not a bare `v0.6.76` — a naive strip-leading-"v"
    # would have left "adia-sdlc-v0.6.76" un-parseable. Both the GitHub-Releases and git-tag tiers
    # must extract the version out of a prefixed tag exactly like a bare one.
    assert _extract_version("adia-sdlc-v0.6.76") == "0.6.76", \
        f"positive control: a plugin-prefixed tag must extract its trailing version: {_extract_version('adia-sdlc-v0.6.76')!r}"
    assert _extract_version("v0.6.76") == "0.6.76", "a bare v-prefixed tag must still extract"
    assert _extract_version("0.6.76") == "0.6.76", "a bare unprefixed tag must still extract"
    assert _extract_version("adia-sdlc-0.6.76") == "0.6.76", \
        "a name-prefixed tag with no 'v' at all must still extract (underscore/hyphen-delimited)"
    assert _extract_version("not-a-version") is None, \
        "a tag with no trailing X.Y.Z must extract to None, never a garbage partial match"

    def _run_fn_gh_prefixed_tag(*args):
        if args[:2] == ("gh", "release"):
            return '[{"tagName": "adia-sdlc-v0.6.76"}]'
        raise AssertionError(f"unexpected call: {args}")

    source4, version4 = resolve_release_ledger_fallback(Path("."), run_fn=_run_fn_gh_prefixed_tag)
    assert (source4, version4) == ("GitHub Releases", "0.6.76"), \
        f"positive control (live fixture shape): a plugin-prefixed GitHub Release tag must resolve to its bare version: {(source4, version4)}"

    # End-to-end via run(): a README with NO ledger line at all downgrades M3 to a WARN when the
    # (mocked) fallback names the SAME version as plugin.json — never a silent PASS, never a FAIL.
    with tempfile.TemporaryDirectory() as td2:
        root2 = Path(td2)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root2, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=root2, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root2, check=True)
        plugin2 = root2 / "demo2"
        (plugin2 / ".claude-plugin").mkdir(parents=True)
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.0.0"}')
        (plugin2 / "README.md").write_text("no ledger table here — this plugin's README carries no line at all\n")
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root2, check=True)
        main_sha2 = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root2, capture_output=True,
                                    text=True, check=True).stdout.strip()
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", main_sha2], cwd=root2, check=True)
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.1.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump, no ledger line ever added"], cwd=root2, check=True)
        # Plugin-prefixed shape (this repo's own real tag convention, e.g. `adia-sdlc-v0.6.76`),
        # not a bare `vX.Y.Z` — proves the real `git describe --tags` end-to-end path extracts it.
        subprocess.run(["git", "tag", "demo2-v3.1.0"], cwd=root2, check=True)

        code_warn = run(plugin2)
        assert code_warn == 0, "a ledger-absent README whose fallback (a real, plugin-prefixed git tag here) matches plugin.json must WARN, not FAIL — exit must stay 0"

        # adiahealth/adia-harness#265 positive control: plugin.json is STRICTLY AHEAD of the
        # fallback tag (the normal pre-merge-PR shape) -> still WARN/ok, exit stays 0. Before
        # this fix, this was a FAIL — the actual bug #265 reported (0.6.80 vs newest 0.6.79).
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.2.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump ahead of the fallback tag"], cwd=root2, check=True)
        code_ahead = run(plugin2)
        assert code_ahead == 0, "a ledger-absent README whose fallback tag is BEHIND plugin.json must WARN, not FAIL (adiahealth/adia-harness#265)"

        # Negative control: plugin.json is BEHIND the fallback tag -> real FAIL, never silently
        # passed just because Releases/tags exist at all.
        subprocess.run(["git", "tag", "demo2-v3.5.0"], cwd=root2, check=True)
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.3.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump, but a newer tag already exists"], cwd=root2, check=True)
        code_behind = run(plugin2)
        assert code_behind == 1, "a ledger-absent README whose fallback tag is AHEAD of plugin.json must FAIL"

    # check_ledger_with_fallback unit controls (adiahealth/adia-harness#265) — the composed
    # function release_gate.py's own G14 block now calls directly, on injected git_root/run_fn
    # so this never touches real git or the network.
    class _FakeRoot:
        """Stand-in for git_root — resolve_release_ledger_fallback only uses it as a subprocess
        cwd when run_fn is None; run_fn is always supplied below, so it's never dereferenced."""

    def _fallback_ahead(*args):
        if args[:2] == ("gh", "release"):
            return '[{"tagName": "v1.0.0"}]'
        raise AssertionError(f"unexpected call: {args}")

    ok_ahead, sev_ahead, msg_ahead = check_ledger_with_fallback("1.1.0", "no ledger here\n", _FakeRoot(), run_fn=_fallback_ahead)
    assert ok_ahead and sev_ahead == "WARN", f"branch strictly ahead of the fallback must be ok/WARN: {(ok_ahead, sev_ahead, msg_ahead)}"

    ok_equal, sev_equal, msg_equal = check_ledger_with_fallback("1.0.0", "no ledger here\n", _FakeRoot(), run_fn=_fallback_ahead)
    assert ok_equal and sev_equal == "WARN", f"branch equal to the fallback (post-ship main) must be ok/WARN: {(ok_equal, sev_equal, msg_equal)}"

    ok_behind, sev_behind, msg_behind = check_ledger_with_fallback("0.9.0", "no ledger here\n", _FakeRoot(), run_fn=_fallback_ahead)
    assert not ok_behind and sev_behind == "FAIL" and "BEHIND" in msg_behind, \
        f"branch behind the fallback must be a real FAIL, never transient: {(ok_behind, sev_behind, msg_behind)}"

    def _fallback_nothing(*args):
        raise RuntimeError("nothing resolves")

    ok_none, sev_none, msg_none = check_ledger_with_fallback("1.0.0", "no ledger here\n", _FakeRoot(), run_fn=_fallback_nothing)
    assert not ok_none and sev_none == "FAIL", f"no fallback resolving at all must FAIL, never silently pass: {(ok_none, sev_none, msg_none)}"

    ok_line, sev_line, msg_line = check_ledger_with_fallback(
        "1.1.0", "map: x\n\nv1.1.0 · 2026-08-16 · did a thing\n", _FakeRoot(), run_fn=_fallback_ahead)
    assert ok_line and sev_line == "ok", \
        f"a README that still carries a matching ledger line must skip the fallback entirely: {(ok_line, sev_line, msg_line)}"

    print("version_monotonic_check selftest (ticket #249, comparison semantics fixed by "
          "adiahealth/adia-harness#265) · PASS · GitHub-Releases-preferred fallback, git-tag "
          "fallback on Releases-unreachable, neither-resolves degrades to (None, None) never "
          "raises; run()'s end-to-end WARN for a ledger-absent README whose fallback is matched, "
          "AHEAD, or BEHIND plugin.json (only BEHIND FAILs — #265's own regression case); "
          "check_ledger_with_fallback's own ahead/equal/behind/unresolvable/still-has-a-line "
          "unit controls, on injected git_root/run_fn")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(argv[0])))
