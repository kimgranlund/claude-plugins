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
            newest git tag — the branch version AHEAD OF OR EQUAL TO that fallback
            (adiahealth/adia-harness#265: `version_tuple` compare, not string equality — the
            normal pre-merge-PR and post-ship-main states respectively) downgrades M3 to a
            [WARN] naming the fallback source used, never a silent PASS and never blocking; the
            branch version BEHIND the fallback stays a real [FAIL]; a README that DOES carry a
            ledger line but it's wrong also stays a straight [FAIL]. adiahealth/adia-harness#431:
            a marketplace repo tags each plugin independently (`sdlc-v0.7.159`,
            `research-v0.1.12`) — both the GitHub-Releases and git-tag tiers of the fallback
            filter to THIS plugin's own tag prefix (`_tag_belongs_to_plugin`) before comparing,
            never the newest tag/release repo-wide; no matching-prefix tag/release existing at
            all for this plugin (a plugin never yet released) downgrades M3 to an [INFO] naming
            the gap, never a FAIL and never blocking. `release_gate.py`'s own G14 block composes
            this exact function (`check_ledger_with_fallback`) rather than calling bare
            `check_ledger` — adiahealth/adia-harness#265's root cause was G14 bypassing the
            fallback entirely.

Exit 0 clean, SKIP, or WARN-only (all non-blocking), 1 on any FAIL, 2 on a usage error.

"Touched" is git-diff-against-origin/main scoped to the plugin root, not just manifest/README —
any file under the plugin root counts (a plugin whose behavior changed but whose version wasn't
bumped is exactly the defect this check exists to catch).
"""
import json
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


def parse_name(plugin_json_text: str):
    """Pure: extract the "name" field from a plugin.json's raw text, mirroring
    `version_claim_check.parse_version`'s own JSON-first/regex-fallback tolerance."""
    try:
        value = json.loads(plugin_json_text).get("name")
        if value:
            return value
    except (json.JSONDecodeError, AttributeError):
        pass
    m = re.search(r'"name"\s*:\s*"([^"]+)"', plugin_json_text)
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


def _tag_belongs_to_plugin(tag: str, plugin_name: str) -> bool:
    """Pure. adiahealth/adia-harness#431: a marketplace repo tags each plugin independently
    (`sdlc-v0.7.159`, `research-v0.1.12`, `rsi-v0.2.8`) — a tag only belongs to THIS plugin when
    its trailing version is delimited by exactly this plugin's own name (`-`/`_`/`/`-delimited).
    A bare, unprefixed `vX.Y.Z` tag and another plugin's own prefix both never match."""
    return re.match(rf"^{re.escape(plugin_name)}[-_/]v?\d+\.\d+\.\d+$", tag) is not None


def _newest_matching_version(tags, plugin_name):
    """Pure. The highest `X.Y.Z` among `tags` that belong to `plugin_name`
    (`_tag_belongs_to_plugin`), compared with `version_tuple` rather than string order. None when
    no tag among `tags` belongs to this plugin at all — never another plugin's tag leaking in as
    a false newest."""
    versions = [_extract_version(t) for t in tags if _tag_belongs_to_plugin(t, plugin_name)]
    versions = [v for v in versions if v is not None]
    return max(versions, key=version_tuple) if versions else None


def resolve_release_ledger_fallback(git_root, plugin_name, run_fn=None):
    """Ticket #249 (adiahealth/adia-harness), scoped per-plugin by adiahealth/adia-harness#431.
    Test-injectable via `run_fn` (a callable taking `(*args)` and returning stdout, or raising on
    failure — mirrors this repo's own adapter transport seams elsewhere) so `selftest` never
    touches the real network or `gh`. Tries GitHub Releases first (`gh release list --json
    tagName`, listing many rather than just the newest); on ANY failure (no `gh`, no auth,
    offline, not a GitHub remote) OR no release belonging to this plugin, falls back to local git
    tags (`git tag --list`, listing every tag rather than just the one nearest HEAD). Both tiers
    filter to tags/releases belonging to `plugin_name` (`_tag_belongs_to_plugin`) and take the
    HIGHEST matching version (`_newest_matching_version`) — a marketplace repo's other plugins'
    tags never leak into this plugin's own fallback. Returns
    `(source: str|None, version: str|None)` — both None when NO release or tag belonging to this
    plugin exists at all (a plugin never yet released, or neither Releases nor git tags are
    reachable), never a raise."""
    if run_fn is not None:
        try:
            out = run_fn("gh", "release", "list", "--limit", "200", "--json", "tagName")
            data = json.loads(out)
            v = _newest_matching_version([d["tagName"] for d in data], plugin_name)
            if v is not None:
                return "GitHub Releases", v
        except Exception:  # noqa: BLE001 — any gh failure degrades to the git-tag fallback below
            pass
        try:
            out = run_fn("git", "tag", "--list")
            v = _newest_matching_version(out.splitlines(), plugin_name)
            return ("newest git tag", v) if v is not None else (None, None)
        except Exception:  # noqa: BLE001
            return None, None

    gh = subprocess.run(
        ["gh", "release", "list", "--limit", "200", "--json", "tagName"],
        capture_output=True, text=True, cwd=git_root,
    )
    if gh.returncode == 0 and gh.stdout.strip():
        try:
            data = json.loads(gh.stdout)
            v = _newest_matching_version([d["tagName"] for d in data], plugin_name)
            if v is not None:
                return "GitHub Releases", v
        except ValueError:
            pass
    tagl = _git(["tag", "--list"], git_root)
    if tagl.returncode == 0 and tagl.stdout.strip():
        v = _newest_matching_version(tagl.stdout.splitlines(), plugin_name)
        if v is not None:
            return "newest git tag", v
    return None, None


def check_ledger_with_fallback(branch_version: str, readme_text: str, git_root, plugin_name: str,
                                run_fn=None):
    """Composes `check_ledger` with the ticket-#249 fallback (`resolve_release_ledger_fallback`,
    scoped per-plugin by adiahealth/adia-harness#431) — the ONE place this composition lives;
    `run()` below and `release_gate.py`'s own G14 block both call this rather than each
    re-deriving the fallback-triggering condition or its comparison semantics. Returns
    `(ok: bool, severity: 'FAIL'|'WARN'|'INFO'|'ok', msg: str)`.

    A README carrying a ledger line at all (even a stale/wrong one) never triggers the fallback —
    that stays a straight FAIL, byte-identical to pre-#249 behavior. Only the "no ledger line at
    all" case falls back to `plugin_name`'s own newest GitHub Release or git tag.

    Comparison semantics (adiahealth/adia-harness#265): the branch's `plugin.json` version is
    compared against the fallback version with `version_tuple`, not string equality — a branch
    STRICTLY AHEAD of the newest Release/tag (the normal pre-merge state of every open PR that
    bumped its version) is ok; EQUAL (the normal post-ship state of `main` itself, once the
    Release matching that version has been cut) is also ok; BEHIND is a real FAIL, never a
    transient one. Both ahead and equal WARN naming the fallback source — this is a fallback
    determination, never a silent PASS. No release or tag belonging to this plugin resolving at
    all (adiahealth/adia-harness#431: a plugin that has simply never been released yet, not a
    repo-wide absence of tags) downgrades to an INFO naming the gap — never a FAIL, never
    blocking."""
    ok_ledger, msg_ledger = check_ledger(branch_version, readme_text)
    if ok_ledger:
        return True, "ok", msg_ledger
    if parse_ledger_version(readme_text) is not None:
        return False, "FAIL", msg_ledger  # a ledger line exists but is wrong -> straight FAIL

    source, fallback_version = resolve_release_ledger_fallback(git_root, plugin_name, run_fn=run_fn)
    if fallback_version is None:
        return True, "INFO", (msg_ledger + f"; no release found for {plugin_name} yet -> "
                                            "skipping the Release/tag fallback comparison")
    if version_tuple(branch_version) >= version_tuple(fallback_version):
        relation = "matches" if fallback_version == branch_version else "is ahead of"
        return True, "WARN", (f"README carries no ledger line; verified via fallback ({source}): "
                               f"branch {branch_version} {relation} {plugin_name}'s own newest "
                               f"{fallback_version}")
    return False, "FAIL", (f"README carries no ledger line; fallback ({source}) {plugin_name}'s "
                            f"own newest is {fallback_version}, plugin.json says {branch_version} "
                            "-> plugin.json is BEHIND the newest Release/tag")


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
    local_manifest_text = local_manifest.read_text() if local_manifest.is_file() else None
    branch_version = parse_version(local_manifest_text) if local_manifest_text else None
    if branch_version is None:
        _fail_report([("M0", False, f"{local_manifest} has no readable \"version\" field")])
        return 1
    plugin_name = parse_name(local_manifest_text) or plugin_root.name

    readme_path = plugin_root / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.is_file() else ""

    ok_mono, msg_mono = check_monotonic(branch_version, main_version)
    ok_ledger, ledger_sev, msg_ledger = check_ledger_with_fallback(
        branch_version, readme_text, git_root, plugin_name)

    ok = ok_mono and ok_ledger
    print(f"version_monotonic_check · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg, sev in [("M2", ok_mono, msg_mono, "FAIL"), ("M3", ok_ledger, msg_ledger, ledger_sev)]:
        if item_ok and sev == "WARN":
            label = "warn"
        elif item_ok and sev == "INFO":
            label = "info"
        elif item_ok:
            label = "ok  "
        else:
            label = "FAIL"
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
            return '[{"tagName": "demo-v2.5.0"}]'
        raise AssertionError(f"unexpected call in _run_fn_gh_ok: {args}")

    source, version = resolve_release_ledger_fallback(Path("."), "demo", run_fn=_run_fn_gh_ok)
    assert (source, version) == ("GitHub Releases", "2.5.0"), \
        f"positive control: a resolvable GitHub Release must be preferred: {(source, version)}"

    def _run_fn_gh_unreachable_git_ok(*args):
        if args[:2] == ("gh", "release"):
            raise RuntimeError("gh: authentication required")
        if args[:2] == ("git", "tag"):
            return "demo-v2.4.0\n"
        raise AssertionError(f"unexpected call: {args}")

    source2, version2 = resolve_release_ledger_fallback(Path("."), "demo", run_fn=_run_fn_gh_unreachable_git_ok)
    assert (source2, version2) == ("newest git tag", "2.4.0"), \
        f"positive control: GitHub Releases unreachable must fall back to the newest git tag: {(source2, version2)}"

    def _run_fn_nothing(*args):
        raise RuntimeError("nothing resolves")

    source3, version3 = resolve_release_ledger_fallback(Path("."), "demo", run_fn=_run_fn_nothing)
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

    source4, version4 = resolve_release_ledger_fallback(Path("."), "adia-sdlc", run_fn=_run_fn_gh_prefixed_tag)
    assert (source4, version4) == ("GitHub Releases", "0.6.76"), \
        f"positive control (live fixture shape): a plugin-prefixed GitHub Release tag must resolve to its bare version: {(source4, version4)}"

    # ---- adiahealth/adia-harness#431: multi-plugin scoping — a marketplace repo's OTHER
    # plugins' tags must never leak into this plugin's own fallback, not via GitHub Releases
    # and not via git tags. ----

    def _run_fn_gh_multi_plugin(*args):
        if args[:2] == ("gh", "release"):
            # sdlc's own newest tag is 0.7.10; research's is 0.1.5; a THIRD, unrelated plugin's
            # tag (9.9.9) is numerically much larger than either — the pre-#431 bug took
            # whichever tag `gh release list --limit 1` happened to return newest overall, with
            # no plugin filter at all, so this unrelated tag would corrupt both plugins' checks.
            return '[{"tagName": "unrelated-v9.9.9"}, {"tagName": "sdlc-v0.7.10"}, ' \
                   '{"tagName": "sdlc-v0.7.5"}, {"tagName": "research-v0.1.5"}]'
        raise AssertionError(f"unexpected call: {args}")

    source_sdlc, version_sdlc = resolve_release_ledger_fallback(Path("."), "sdlc", run_fn=_run_fn_gh_multi_plugin)
    assert (source_sdlc, version_sdlc) == ("GitHub Releases", "0.7.10"), \
        (f"positive control (#431): sdlc's own fallback must resolve to sdlc's own newest tag "
         f"(0.7.10), never the unrelated plugin's 9.9.9: {(source_sdlc, version_sdlc)}")

    source_research, version_research = resolve_release_ledger_fallback(
        Path("."), "research", run_fn=_run_fn_gh_multi_plugin)
    assert (source_research, version_research) == ("GitHub Releases", "0.1.5"), \
        (f"positive control (#431): research's own fallback must resolve to research's own "
         f"newest tag (0.1.5), never sdlc's: {(source_research, version_research)}")

    # A plugin with NO matching-prefix tag/release anywhere in the same list -> unresolved
    # (None, None), never another plugin's tag borrowed as a stand-in.
    source_rsi, version_rsi = resolve_release_ledger_fallback(Path("."), "rsi", run_fn=_run_fn_gh_multi_plugin)
    assert (source_rsi, version_rsi) == (None, None), \
        (f"negative control (#431): a plugin with no release of its own must resolve to "
         f"(None, None), never borrow a sibling plugin's tag: {(source_rsi, version_rsi)}")

    # ---- adiahealth/adia-harness#431 sabotage-and-confirm: this is the exact false-mismatch
    # class the ticket reports. sdlc's declared 0.7.10 is ahead of sdlc's OWN newest tag
    # (0.7.5), so the correct, per-plugin-scoped fallback WARNs clean — but the pre-#431
    # repo-wide "just take the newest tag in the list" bug would instead compare against the
    # unrelated plugin's 9.9.9 (numerically bigger, nothing to do with sdlc) and report sdlc's
    # 0.7.10 as BEHIND it — a false FAIL for a plugin that is actually fine. Confirmed by hand:
    # reverting `resolve_release_ledger_fallback`'s GitHub-Releases tier to the pre-fix
    # `_extract_version(data[0]["tagName"])` (bare "take tag zero, unfiltered", no
    # `_newest_matching_version` scoping) turns this assertion red with exactly that
    # false-BEHIND message; restoring the real filtered call turns it green again.
    ok_sdlc, sev_sdlc, msg_sdlc = check_ledger_with_fallback(
        "0.7.10", "no ledger here\n", Path("."), "sdlc", run_fn=_run_fn_gh_multi_plugin)
    assert ok_sdlc and sev_sdlc == "WARN" and "BEHIND" not in msg_sdlc, \
        (f"negative control (#431, the ticket's own false-mismatch class): sdlc's declared "
         f"0.7.10 is ahead of sdlc's OWN newest tag (0.7.5) and must WARN clean, never FAIL "
         f"against another plugin's unrelated, numerically-larger tag: {(ok_sdlc, sev_sdlc, msg_sdlc)}")

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
        # not a bare `vX.Y.Z` — proves the real `git tag --list` end-to-end path extracts it.
        # A SECOND plugin's own, much-higher-numbered tag sits in the SAME repo (adiahealth/
        # adia-harness#431's own real-plumbing proof: demo2's check must never read it).
        subprocess.run(["git", "tag", "demo2-v3.1.0"], cwd=root2, check=True)
        subprocess.run(["git", "tag", "otherplugin-v9.9.9"], cwd=root2, check=True)

        code_warn = run(plugin2)
        assert code_warn == 0, "a ledger-absent README whose fallback (a real, plugin-prefixed git tag here) matches plugin.json must WARN, not FAIL — exit must stay 0"

        # adiahealth/adia-harness#265 positive control: plugin.json is STRICTLY AHEAD of
        # demo2's OWN fallback tag (the normal pre-merge-PR shape) -> still WARN/ok, exit stays
        # 0 — even though `otherplugin`'s 9.9.9 sits in the same repo and is numerically larger
        # (adiahealth/adia-harness#431: that tag must never be read for demo2's own check).
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.2.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump ahead of the fallback tag"], cwd=root2, check=True)
        code_ahead = run(plugin2)
        assert code_ahead == 0, "a ledger-absent README whose fallback tag is BEHIND plugin.json must WARN, not FAIL (adiahealth/adia-harness#265), and otherplugin's unrelated higher tag must never leak in (#431)"

        # Negative control: plugin.json is BEHIND demo2's OWN newer fallback tag -> real FAIL,
        # never silently passed just because Releases/tags exist at all.
        subprocess.run(["git", "tag", "demo2-v3.5.0"], cwd=root2, check=True)
        (plugin2 / ".claude-plugin" / "plugin.json").write_text('{"name": "demo2", "version": "3.3.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump, but a newer tag already exists"], cwd=root2, check=True)
        code_behind = run(plugin2)
        assert code_behind == 1, "a ledger-absent README whose fallback tag is AHEAD of plugin.json must FAIL"

        # adiahealth/adia-harness#431: a plugin with NO tag of its own at all (only
        # `otherplugin`'s tags exist in the repo) must INFO, never FAIL, never borrow
        # otherplugin's tag as a stand-in.
        plugin3 = root2 / "neverreleased"
        (plugin3 / ".claude-plugin").mkdir(parents=True)
        (plugin3 / ".claude-plugin" / "plugin.json").write_text('{"name": "neverreleased", "version": "0.1.0"}')
        (plugin3 / "README.md").write_text("no ledger table here either\n")
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "brand-new plugin, never released, no ledger"], cwd=root2, check=True)
        main_sha3 = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root2, capture_output=True,
                                    text=True, check=True).stdout.strip()
        # Fake origin/main to an EARLIER commit that already has this plugin (its manifest must
        # exist on origin/main to reach the ledger-fallback path at all, not the new-plugin SKIP).
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", main_sha3], cwd=root2, check=True)
        (plugin3 / ".claude-plugin" / "plugin.json").write_text('{"name": "neverreleased", "version": "0.2.0"}')
        subprocess.run(["git", "add", "-A"], cwd=root2, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "bump, still never released"], cwd=root2, check=True)
        code_never = run(plugin3)
        assert code_never == 0, \
            "a plugin with no release/tag of its own at all must INFO and stay exit 0, never FAIL, never borrow another plugin's tag (#431)"

    # check_ledger_with_fallback unit controls (adiahealth/adia-harness#265, re-scoped by #431) —
    # the composed function release_gate.py's own G14 block now calls directly, on injected
    # git_root/run_fn so this never touches real git or the network.
    class _FakeRoot:
        """Stand-in for git_root — resolve_release_ledger_fallback only uses it as a subprocess
        cwd when run_fn is None; run_fn is always supplied below, so it's never dereferenced."""

    def _fallback_ahead(*args):
        if args[:2] == ("gh", "release"):
            return '[{"tagName": "demo-v1.0.0"}]'
        raise AssertionError(f"unexpected call: {args}")

    ok_ahead, sev_ahead, msg_ahead = check_ledger_with_fallback(
        "1.1.0", "no ledger here\n", _FakeRoot(), "demo", run_fn=_fallback_ahead)
    assert ok_ahead and sev_ahead == "WARN", f"branch strictly ahead of the fallback must be ok/WARN: {(ok_ahead, sev_ahead, msg_ahead)}"

    ok_equal, sev_equal, msg_equal = check_ledger_with_fallback(
        "1.0.0", "no ledger here\n", _FakeRoot(), "demo", run_fn=_fallback_ahead)
    assert ok_equal and sev_equal == "WARN", f"branch equal to the fallback (post-ship main) must be ok/WARN: {(ok_equal, sev_equal, msg_equal)}"

    ok_behind, sev_behind, msg_behind = check_ledger_with_fallback(
        "0.9.0", "no ledger here\n", _FakeRoot(), "demo", run_fn=_fallback_ahead)
    assert not ok_behind and sev_behind == "FAIL" and "BEHIND" in msg_behind, \
        f"branch behind the fallback must be a real FAIL, never transient: {(ok_behind, sev_behind, msg_behind)}"

    def _fallback_nothing(*args):
        raise RuntimeError("nothing resolves")

    ok_none, sev_none, msg_none = check_ledger_with_fallback(
        "1.0.0", "no ledger here\n", _FakeRoot(), "demo", run_fn=_fallback_nothing)
    assert ok_none and sev_none == "INFO", \
        (f"adiahealth/adia-harness#431: no release found for this plugin at all must INFO and "
         f"stay non-blocking, never FAIL: {(ok_none, sev_none, msg_none)}")

    ok_line, sev_line, msg_line = check_ledger_with_fallback(
        "1.1.0", "map: x\n\nv1.1.0 · 2026-08-16 · did a thing\n", _FakeRoot(), "demo", run_fn=_fallback_ahead)
    assert ok_line and sev_line == "ok", \
        f"a README that still carries a matching ledger line must skip the fallback entirely: {(ok_line, sev_line, msg_line)}"

    print("version_monotonic_check selftest (ticket #249/#265, re-scoped per-plugin by "
          "adiahealth/adia-harness#431) · PASS · GitHub-Releases-preferred fallback, git-tag "
          "fallback on Releases-unreachable, both filtered to this plugin's own tag prefix; a "
          "multi-plugin tag/release list resolves each plugin to its OWN newest match, never a "
          "sibling's (positive controls for sdlc/research, negative control for an unreleased "
          "rsi); the ticket's own false-mismatch class (a numerically-larger sibling tag) no "
          "longer FAILs; no release/tag belonging to this plugin at all degrades to INFO, never "
          "FAIL, never blocking; run()'s end-to-end WARN/FAIL/INFO on real, multi-plugin git "
          "tag plumbing; check_ledger_with_fallback's own ahead/equal/behind/none/still-has-a-"
          "line unit controls, on injected git_root/run_fn")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(argv[0])))
