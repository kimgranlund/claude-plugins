#!/usr/bin/env python3
"""gitignore_check — .gitignore is a record and drifts like one (repo-alignment's razor).

Usage:
  gitignore_check.py <repo-root>     sweep .gitignore both directions
  gitignore_check.py selftest        prove the counters bite

Rules (mechanical slice; judgment on WHICH rule to add/retire stays with the author):
  G1 [WARN] a .gitignore rule matches nothing in the current tree -> stale, retire it
  G2 [FAIL] a known generated/tool-output dir exists on disk but `git check-ignore` does not
            cover it -> one `git add -A` from being committed (repo-alignment's razor; the
            worktrees-placement incident, 2026-07-16, is this rule's origin case)

G2's candidate list is deliberately small and conservative (real generated-output/tool-state
dirs seen in this estate) — it is not a general "everything unignored is wrong" scanner; a repo
legitimately tracking a dir with one of these names is a false positive to silence by naming, not
by disabling the rule (the estate's own suppression doctrine: narrowest control first).

Exit 0 clean/warnings, 1 on any FAIL.
"""
import fnmatch
import subprocess
import sys
from pathlib import Path

GENERATED_DIR_CANDIDATES = (
    ".claude/worktrees", "dist", "__pycache__", "node_modules",
    ".pytest_cache", "build", ".venv",
)


def load_tree(root: Path):
    """Every real path under root, .git pruned, dirs suffixed '/' — the pattern-match universe."""
    out = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if ".git" in rel.parts:
            continue
        out.append(rel.as_posix() + ("/" if p.is_dir() else ""))
    return out


def pattern_matches(pattern: str, files: list) -> bool:
    """Approximate gitignore semantics: anchored (`/x`) matches from root; bare `x` matches at
    any depth (segment or suffix); a leading `**/` (git's documented "anywhere, including root"
    idiom — the exact shape used for `**/node_modules`, `**/dist`, `**/__pycache__`) is unwrapped
    to the bare form rather than requiring a literal `/` before the tail, which is where a first
    cut of this function false-flagged the idiom as stale (caught live, 2026-07-17 fresh-context
    audit — reproduced with `**/node_modules` against a root-level `node_modules/`).
    fnmatch, not a full gitignore engine — `?` is looser here than git's (git's `?` excludes
    `/`; fnmatch's doesn't), a disclosed, false-CLEAN-only limitation, not a stale-flagging risk.
    Good enough for a WARN-tier staleness check, same pragmatism as this repo's other scripts."""
    if pattern.startswith("**/"):
        return pattern_matches(pattern[3:], files)
    anchored = pattern.startswith("/")
    pat = pattern.lstrip("/").rstrip("/")
    if not pat:
        return True  # a bare '/' or empty after stripping — don't flag, can't parse confidently
    for f in files:
        fc = f.rstrip("/")
        if anchored:
            if fnmatch.fnmatch(fc, pat) or fnmatch.fnmatch(fc, pat + "/*"):
                return True
        else:
            if fnmatch.fnmatch(fc, pat) or fnmatch.fnmatch(fc, "*/" + pat):
                return True
            if any(fnmatch.fnmatch(seg, pat) for seg in fc.split("/")):
                return True
    return False


def parse_rules(gitignore_text: str):
    """Non-comment, non-blank, non-negated lines — negation rules re-INCLUDE, a different
    check ('does the negation have anything to re-include') this pass doesn't attempt."""
    rules = []
    for raw in gitignore_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        rules.append(line)
    return rules


def stale_rules(gitignore_text: str, files: list) -> list:
    return [r for r in parse_rules(gitignore_text) if not pattern_matches(r, files)]


def unignored_generated_dirs(root: Path, candidates=GENERATED_DIR_CANDIDATES) -> list:
    """Real `git check-ignore` semantics for the direction fnmatch can't safely approximate —
    whether the actual tool considers a real path covered."""
    found = []
    for name in candidates:
        d = root / name
        if not d.is_dir():
            continue
        if any(d.iterdir()) is False:
            continue  # empty dir — nothing at risk of a stray `git add -A` yet
        r = subprocess.run(["git", "check-ignore", "-q", str(d)], cwd=root, capture_output=True)
        if r.returncode != 0:  # 0 = ignored, 1 = not ignored, >1 = error (surface as unignored)
            found.append(name)
    return found


def check(root: Path):
    findings = []
    gi = root / ".gitignore"
    if not gi.is_file():
        return findings  # no .gitignore is not this script's concern
    files = load_tree(root)
    text = gi.read_text(encoding="utf-8", errors="replace")

    for rule in stale_rules(text, files):
        findings.append(("WARN", "G1", f"`{rule}` matches nothing in the tree -> stale, retire it"))

    for name in unignored_generated_dirs(root):
        findings.append(("FAIL", "G2",
                          f"{name}/ exists and is NOT covered by .gitignore -> one `git add -A` "
                          "from being committed; add the rule or name the deliberate exception"))
    return findings


def run(root: Path):
    fs = check(root)
    verdict = "FAIL" if any(f[0] == "FAIL" for f in fs) else ("warn" if fs else "clean")
    print(f"gitignore_check · {verdict} · {root}")
    for sev, code, msg in fs:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if verdict == "FAIL" else 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        subprocess.run(["git", "init", "-q"], cwd=r, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=r, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=r, check=True)
        (r / "src").mkdir()
        (r / "src" / "app.py").write_text("x")
        (r / ".gitignore").write_text("*.pyc\n__pycache__/\n/dead-rule-nothing-matches-this\n")
        fs = check(r)
        codes = {f[1] for f in fs}
        assert "G1" in codes, f"a rule matching nothing must warn G1, got {fs}"
        msgs = " ".join(f[2] for f in fs)
        assert "dead-rule-nothing-matches-this" in msgs, "the STALE rule specifically must be named"
        assert any("*.pyc" in f[2] for f in fs if f[1] == "G1"), \
            "*.pyc has no match in this fixture (no .pyc file exists) — legitimately stale, must fire"
        assert any("__pycache__" in f[2] for f in fs if f[1] == "G1"), \
            "__pycache__/ has no dir in this fixture — legitimately stale, must fire"

        # G1 positive control: a rule that DOES match must not be flagged
        (r / "build").mkdir()
        (r / "build" / "out.txt").write_text("x")
        (r / ".gitignore").write_text("build/\n")
        fs2 = check(r)
        assert not any(f[1] == "G1" for f in fs2), f"a rule matching a real dir must not warn, got {fs2}"

        # G2
        (r / ".claude").mkdir()
        (r / ".claude" / "worktrees").mkdir()
        (r / ".claude" / "worktrees" / "scratch.txt").write_text("x")
        (r / ".gitignore").write_text("build/\n")  # worktrees NOT covered — the negative control
        fs3 = check(r)
        assert any(f[1] == "G2" and ".claude/worktrees" in f[2] for f in fs3), \
            f"an unignored generated dir must FAIL G2, got {fs3}"
        (r / ".gitignore").write_text("build/\n.claude/worktrees/\n")
        fs4 = check(r)
        assert not any(f[1] == "G2" for f in fs4), f"a covered generated dir must not fail, got {fs4}"
    # G1's **/ idiom (the fresh-context audit's live repro, 2026-07-17): a root-level dir
    # covered by the "anywhere including root" form must NOT be flagged stale.
    files_root_level = ["node_modules/", "src/", "src/app.py"]
    assert pattern_matches("**/node_modules", files_root_level),         "the **/ idiom must cover a root-level match — this is the exact false-stale repro"
    assert pattern_matches("**/dist", ["dist/", "dist/out.plugin"]), "**/ idiom, second shape"
    assert not pattern_matches("**/totally-absent-xyz", files_root_level),         "the **/ unwrap must not make every pattern match everything — still checks real absence"

    print("gitignore_check selftest · PASS · stale-rule detection both ways, unignored-dir gate "
          "real, the **/ root-level idiom no longer false-flags as stale")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(args[0]).resolve()))
