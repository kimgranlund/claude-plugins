#!/usr/bin/env python3
"""sync_main — pull onto a possibly-dirty main checkout without clobbering a parallel session.

Usage:
  sync_main.py [--repo-root <path>]     classify, quarantine, pull, report
  sync_main.py selftest                 prove the classification logic bites

The incident this replaces (2026-07-17): a plain `git pull` on a dirty checkout with foreign
uncommitted work aborted silently under a `| tail -1` pipe, was misread as success, and the
follow-up diagnosis worked against stale pre-merge files for several steps before the failure
was traced. A second incident the same day: a `git stash pop` conflict was resolved by keeping
the WRONG side (the stale local copy) — nothing caught it until the next push failed.

S1 [classify] every locally-dirty file against the files origin/main's new commits touched —
    OVERLAP files are the danger zone (both sides changed the same file); FOREIGN-ONLY files are
    safe to quarantine untouched
S2 [quarantine] if anything is dirty, stash it under one NAMED, greppable message before
    touching HEAD — nothing of a parallel session's is ever staged into this run's own commit
S3 [pull] `--ff-only` — a non-fast-forward state FAILS loudly instead of silently creating a
    merge commit or (worse) silently doing nothing under a truncated pipe
S4 [reverify] local HEAD == origin/main by SHA after the pull, read fresh — never trust the
    pull command's own exit code alone (the doctrine this whole script exists to instantiate:
    verify by re-reading, never by a command's print)

Conflict RESOLUTION after a stash pop stays judgment — S1's report names which files are
foreign-only (safe to reapply blind) vs overlap (read both sides before choosing).
"""
import subprocess
import sys


def classify_overlap(dirty_files: set, incoming_files: set):
    """Pure classifier — no I/O, the unit selftest proves."""
    overlap = dirty_files & incoming_files
    foreign_only = dirty_files - incoming_files
    return {
        "overlap": sorted(overlap),
        "foreign_only": sorted(foreign_only),
        "nothing_dirty": not dirty_files,
    }


def verify_stash_created(before: list, after: list, label: str):
    """`git stash push` exits 0 even on "No local changes to save" — the caller must not trust
    the exit code. A real quarantine grew the list by exactly one, with OUR label on top; any
    other shape (list unchanged, or grown for an unrelated reason mid-race) means nothing of
    ours was actually stashed and `after[0]` would be a FOREIGN entry misattributed to this
    run — the wrong-side-pop incident class, reproduced via TOCTOU instead of a merge conflict."""
    if len(after) != len(before) + 1:
        return False, None, ("stash push reported success but the list did not grow by one -> "
                              "nothing was actually quarantined; do not trust any stash_ref")
    top = after[0]
    if label not in top:
        return False, None, (f"the list grew by one but the top entry (\"{top}\") does not carry "
                              f"our label \"{label}\" -> it is a FOREIGN stash from elsewhere; "
                              "do not report it as this run's quarantine")
    return True, top.split(":")[0], f"quarantined dirty tree as {top.split(':')[0]}"


def verify_head_matches_origin(local_sha: str, origin_sha: str):
    if local_sha != origin_sha:
        return False, (f"local HEAD {local_sha[:9]} != origin/main {origin_sha[:9]} after pull "
                        "-> the pull did not land as expected; do not assume it worked")
    return True, f"HEAD matches origin/main at {local_sha[:9]}"


def _run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def _dirty_files(root):
    out = _run(["git", "status", "--porcelain"], cwd=root)
    files = set()
    for line in out.splitlines():
        if not line.strip():
            continue
        files.add(line[3:].strip().strip('"'))
    return files


def _incoming_files(root):
    _run(["git", "fetch"], cwd=root)
    out = _run(["git", "diff", "--name-only", "HEAD..origin/main"], cwd=root, check=False)
    return {f for f in out.splitlines() if f.strip()}


def run(root="."):
    dirty = _dirty_files(root)
    incoming = _incoming_files(root)
    cls = classify_overlap(dirty, incoming)

    print(f"sync_main · {root}")
    print(f"  dirty: {len(dirty)} file(s)  ·  incoming: {len(incoming)} file(s)")
    if cls["overlap"]:
        print(f"  OVERLAP (read both sides before resolving): {', '.join(cls['overlap'])}")
    if cls["foreign_only"]:
        print(f"  foreign-only (safe to reapply blind after pop): {', '.join(cls['foreign_only'])}")

    stash_ref = None
    if not cls["nothing_dirty"]:
        label = "sync_main quarantine"
        before = _run(["git", "stash", "list"], cwd=root).splitlines()
        _run(["git", "stash", "push", "-u", "-m", label], cwd=root)
        after = _run(["git", "stash", "list"], cwd=root).splitlines()
        ok, stash_ref, msg = verify_stash_created(before, after, label)
        print(f"  {'ok  ' if ok else 'FAIL'}  {msg}")
        if not ok:
            return 1

    pull = subprocess.run(["git", "pull", "--ff-only"], cwd=root, capture_output=True, text=True)
    if pull.returncode != 0:
        print(f"  FAIL  pull --ff-only rejected: {pull.stderr.strip()}")
        if stash_ref:
            print(f"  your work is safe in {stash_ref} — resolve the divergence, then `git stash pop`")
        return 1

    local_sha = _run(["git", "rev-parse", "HEAD"], cwd=root)
    origin_sha = _run(["git", "rev-parse", "origin/main"], cwd=root)
    ok, msg = verify_head_matches_origin(local_sha, origin_sha)
    print(f"  {'ok  ' if ok else 'FAIL'}  {msg}")

    if stash_ref:
        print(f"  next: `git stash pop` — {stash_ref} still holds your quarantined work; "
              "resolve OVERLAP files by hand, reapply foreign-only files as-is")
    return 0 if ok else 1


def parse_cli(args):
    """Strict CLI parse for a git-mutating entry point: returns the repo root,
    or None on ANY unknown or malformed token — a typo'd flag must become a
    usage error, never a silent wrong-directory run (#74, 2026-07-21)."""
    root = "."
    i = 0
    while i < len(args):
        if args[i] == "--repo-root" and i + 1 < len(args):
            root = args[i + 1]
            i += 2
        else:
            return None
    return root


def selftest():
    # S1 — the pure classifier, every shape
    c = classify_overlap({"a.py", "b.py"}, {"b.py", "c.py"})
    assert c["overlap"] == ["b.py"], c
    assert c["foreign_only"] == ["a.py"], c
    assert not c["nothing_dirty"], c

    c2 = classify_overlap(set(), {"a.py"})
    assert c2["nothing_dirty"], "no local dirt must report nothing_dirty=True regardless of incoming"

    c3 = classify_overlap({"a.py"}, set())
    assert c3["foreign_only"] == ["a.py"] and not c3["overlap"], \
        "fully foreign dirt with no incoming overlap must never land in 'overlap'"

    # S4 — the negative control: the wrong-side-pop incident this doctrine exists to prevent
    ok, msg = verify_head_matches_origin("aaa111222", "bbb333444")
    assert not ok and "did not land as expected" in msg, \
        "a HEAD/origin mismatch after pull must FAIL explicitly, never be assumed correct"
    ok, _ = verify_head_matches_origin("aaa111222", "aaa111222")
    assert ok, "a real match must pass"

    # S2 — the negative control the fresh-context audit reproduced live (2026-07-17): `git
    # stash push` exits 0 with "No local changes to save"; the list is unchanged; a naive
    # `after[0]` grab would misattribute a FOREIGN pre-existing stash to this run
    foreign_only_list = ["stash@{0}: On main: someone else's unrelated stash"]
    ok, ref, msg = verify_stash_created(before=foreign_only_list, after=foreign_only_list,
                                         label="sync_main quarantine")
    assert not ok and ref is None and "did not grow by one" in msg, \
        "an unchanged stash list (the 'nothing to stash' case) must never report a stash_ref"
    # the list DID grow, but by someone else's push (a race between our list-read and theirs)
    ok, ref, msg = verify_stash_created(before=foreign_only_list,
                                         after=["stash@{0}: On main: a DIFFERENT run's stash",
                                                *foreign_only_list],
                                         label="sync_main quarantine")
    assert not ok and ref is None and "FOREIGN stash" in msg, \
        "a grown list whose top entry lacks OUR label must never be claimed as ours"
    ok, ref, msg = verify_stash_created(before=[],
                                         after=["stash@{0}: On main: sync_main quarantine"],
                                         label="sync_main quarantine")
    assert ok and ref == "stash@{0}", "a genuine one-entry grow carrying our label must pass"

    # S5 — #74 regression: the CLI contract rejects unknown tokens instead of
    # silently running the quarantine/pull sequence against cwd
    assert parse_cli([]) == "."
    assert parse_cli(["--repo-root", "/x"]) == "/x"
    assert parse_cli(["--repo-dir", "/x"]) is None, "the incident's typo'd flag must be rejected"
    assert parse_cli(["--repo-root"]) is None, "a flag missing its value must be rejected"

    print("sync_main selftest · PASS · overlap/foreign classification correct on all shapes, "
          "the HEAD-mismatch and foreign-stash negative controls both fire, "
          "unknown CLI tokens rejected before any git operation")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "selftest":
        sys.exit(selftest())
    root = parse_cli(args)
    if root is None:
        print("sync_main · usage error: unknown or malformed argument\n"
              "usage: sync_main.py [selftest | --repo-root <path>]", file=sys.stderr)
        sys.exit(1)
    sys.exit(run(root))
