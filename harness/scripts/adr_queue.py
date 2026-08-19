#!/usr/bin/env python3
"""adr_queue — durable, batchable held-queue for ADR-review candidates.

Usage:
  adr_queue.py add <path> --adr <id> --kind harvest|stale-citation --evidence <text> [--plan <text>]
  adr_queue.py pending <path>                    list every unresolved candidate, one per line
  adr_queue.py clear <path> --ids <id[:kind],...>  drop resolved candidates after a batch confirm
                                                    (a bare id clears every kind queued for it;
                                                    "id:kind" clears only that one row)
  adr_queue.py selftest                          prove append/read/clear + idempotency

Exists so a scheduled firing never blocks on a live human: a candidate lands here instead of an
AskUserQuestion, and stays until the next session runs ONE batched confirm round over everything
pending — never one round per candidate, regardless of how many firings queued something.

Schema: {"candidates": [{"adr_id", "kind", "evidence", "plan", "queued_at"}]} — one row per
(adr_id, kind) pair; re-adding the same pair updates evidence/plan in place rather than growing
a duplicate, so a candidate re-detected on every firing until it's confirmed doesn't pile up.

Also carries `citation_on_ref` (issue #752): the stale-citation coverage check watch-adrs' step 3
prescribes must resolve a candidate ADR id against `origin/main`'s tree, never the invoking
checkout's working files — a worktree-isolated session branched before a covering reference
merged upstream would otherwise re-queue the same false positive every firing (the recurring
adr-0023 harvest false positive this issue names). `citation_on_ref selftest` proves the
ref-resolving decision against a real throwaway git fixture: a term covered on `main` but absent
from a stale branch's working tree must read as covered (not queue); a term covered nowhere must
still queue (negative control).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def citation_on_ref(term, ref, pathspec, cwd):
    """True if `term` appears under `pathspec` as committed at git ref `ref` — reads the ref's
    own tree via `git grep`, never the working directory, so a stale/worktree-isolated checkout
    can't miss a citation that already merged upstream. `ref` is expected to be a ref the caller
    has already made resolvable (e.g. `git fetch origin main` before passing `origin/main`) —
    this function performs no fetch itself, so the CALLER owns the fetch-failure branch
    (watch-adrs' Failure branches: an unresolvable ref is an UNVERIFIED check, never "no hit").
    Returns False on any git error (unresolvable ref, no matches, not a git repo), never raises;
    a caller that must distinguish "unresolvable" from "no match" checks the ref first
    (`git rev-parse --verify <ref>`)."""
    result = subprocess.run(
        ["git", "grep", "-l", "--no-color", "-e", term, ref, "--", pathspec],
        cwd=cwd, capture_output=True, text=True,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def load(path):
    p = Path(path)
    if not p.is_file():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("candidates", [])


def save(path, candidates):
    Path(path).write_text(
        json.dumps({"candidates": candidates}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def add_candidate(candidates, adr_id, kind, evidence, plan, queued_at):
    """Pure — append-or-update by (adr_id, kind), never a duplicate row. Selftest proves idempotency."""
    out = [c for c in candidates if not (c["adr_id"] == adr_id and c["kind"] == kind)]
    out.append({
        "adr_id": adr_id, "kind": kind, "evidence": evidence, "plan": plan, "queued_at": queued_at,
    })
    return out


def clear_ids(candidates, ids_to_clear):
    """Pure — drop candidates matching ids_to_clear. Each entry is either a bare adr_id (clears
    every kind queued for it) or "adr_id:kind" (clears only that one row) — an ADR carrying both a
    harvest and a stale-citation candidate, where a batch round resolves one and defers the other,
    must be able to clear precisely instead of losing the deferred row."""
    bare_ids, pairs = set(), set()
    for entry in ids_to_clear:
        if ":" in entry:
            pairs.add(tuple(entry.split(":", 1)))
        else:
            bare_ids.add(entry)
    return [
        c for c in candidates
        if c["adr_id"] not in bare_ids and (c["adr_id"], c["kind"]) not in pairs
    ]


def run(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]

    if cmd == "add":
        if not rest:
            print("add requires <path>"); return 2
        path = rest[0]
        opts = rest[1:]
        def opt(name, required=True, default=None):
            if f"--{name}" in opts:
                return opts[opts.index(f"--{name}") + 1]
            if required:
                raise SystemExit(f"add: missing --{name}")
            return default
        adr_id = opt("adr")
        kind = opt("kind")
        if kind not in ("harvest", "stale-citation"):
            raise SystemExit(f"add: --kind must be harvest|stale-citation, got {kind!r}")
        evidence = opt("evidence")
        plan = opt("plan", required=False, default="")
        import datetime
        queued_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        candidates = add_candidate(load(path), adr_id, kind, evidence, plan, queued_at)
        save(path, candidates)
        print(f"adr_queue · queued {adr_id} ({kind}) -> {path}  [{len(candidates)} pending total]")
        return 0

    if cmd == "pending":
        if not rest:
            print("pending requires <path>"); return 2
        candidates = load(rest[0])
        if not candidates:
            print("adr_queue · nothing pending")
            return 0
        print(f"adr_queue · {len(candidates)} pending candidate(s)")
        for c in candidates:
            print(f"  {c['adr_id']} · {c['kind']} · {c['evidence']}")
        return 0

    if cmd == "clear":
        if not rest:
            print("clear requires <path>"); return 2
        path = rest[0]
        opts = rest[1:]
        if "--ids" not in opts:
            raise SystemExit("clear: missing --ids")
        ids = opts[opts.index("--ids") + 1].split(",")
        before = load(path)
        after = clear_ids(before, ids)
        save(path, after)
        print(f"adr_queue · cleared {len(before) - len(after)} candidate(s) -> {len(after)} remain")
        return 0

    print(__doc__)
    return 2


def selftest():
    # add_candidate: fresh queue grows by one
    q = add_candidate([], "adr-0001", "harvest", "third time this convention was explained", "", "t0")
    assert len(q) == 1 and q[0]["adr_id"] == "adr-0001", q

    # add_candidate: idempotent re-add updates in place, never duplicates
    q2 = add_candidate(q, "adr-0001", "harvest", "fourth time, updated evidence", "", "t1")
    assert len(q2) == 1, f"re-adding the same (adr_id, kind) must not grow the queue: {q2}"
    assert q2[0]["evidence"] == "fourth time, updated evidence", q2

    # add_candidate: same adr_id, DIFFERENT kind is a distinct row
    q3 = add_candidate(q2, "adr-0001", "stale-citation", "cites a superseded decision", "", "t2")
    assert len(q3) == 2, f"same adr_id but a different kind must be its own row: {q3}"

    # a second, unrelated adr_id grows the queue normally
    q4 = add_candidate(q3, "adr-0002", "harvest", "high-impact convention", "", "t3")
    assert len(q4) == 3, q4

    # clear_ids: "id:kind" clears ONLY that one row — adr-0001 keeps its stale-citation row
    # when only its harvest row is resolved (the exact case a batch round resolving one kind
    # but deferring the other must not silently drop)
    q4b = clear_ids(q4, ["adr-0001:harvest"])
    assert len(q4b) == 2, f"an id:kind clear must drop only that one row: {q4b}"
    remaining_kinds = {c["kind"] for c in q4b if c["adr_id"] == "adr-0001"}
    assert remaining_kinds == {"stale-citation"}, \
        f"the deferred stale-citation row must survive a harvest-only clear: {q4b}"

    # clear_ids: a bare id drops every row for it, both kinds of adr-0001 at once
    q5 = clear_ids(q4, ["adr-0001"])
    assert len(q5) == 1 and q5[0]["adr_id"] == "adr-0002", \
        f"clearing a bare id must drop ALL its rows (both kinds), leaving unrelated ids untouched: {q5}"

    # negative control: clearing an id with nothing queued is a no-op, never an error
    q6 = clear_ids(q5, ["adr-9999"])
    assert q6 == q5, "clearing an absent id must be a no-op"

    # negative control: an id:kind pair that doesn't exist is also a safe no-op
    q7 = clear_ids(q5, ["adr-0002:stale-citation"])
    assert q7 == q5, "clearing a (id, kind) pair with no matching row must be a safe no-op"

    # citation_on_ref (issue #752): a real throwaway git fixture proves the ref-resolving
    # coverage check reads a candidate's ref tree, never the invoking checkout's working files —
    # the exact recurring adr-0023 false positive. Two commits: the first has no covering
    # reference at all; the second (advancing "main") adds one. A branch cut from the FIRST
    # commit — a stale worktree-isolated checkout, same shape as fix-684 branched before PR #707
    # merged — never receives that file in its own working tree.
    with tempfile.TemporaryDirectory() as repo:
        def git(*args, **kw):
            return subprocess.run(
                ["git", *args], cwd=repo, capture_output=True, text=True, check=True, **kw
            )

        git("init", "-q", "-b", "main")
        git("config", "user.email", "selftest@example.com")
        git("config", "user.name", "selftest")

        readme = Path(repo, "README.md")
        readme.write_text("seed\n", encoding="utf-8")
        git("add", "README.md")
        git("commit", "-q", "-m", "seed")
        git("branch", "stale-worktree")  # cut BEFORE the covering reference lands

        refs_dir = Path(repo, "skills", "fleet-rules", "references")
        refs_dir.mkdir(parents=True)
        (refs_dir / "substrate-choice.md").write_text(
            "covers adr-0023's substrate-choice decision\n", encoding="utf-8"
        )
        git("add", "skills")
        git("commit", "-q", "-m", "add covering reference (adr-0023)")

        git("checkout", "-q", "stale-worktree")  # simulate the stale, worktree-isolated checkout
        assert not (refs_dir / "substrate-choice.md").exists(), \
            "fixture setup bug: the stale branch must not carry the covering reference"

        pathspec = "skills/*/references/*.md"

        # positive case: covered on main, absent from the current (stale) working tree — must
        # read as covered, i.e. must NOT be queued as a stale-citation candidate
        assert citation_on_ref("adr-0023", "main", pathspec, cwd=repo) is True, (
            "a term covered on main must read as covered even when grepped from a stale branch "
            "whose own working tree lacks the file — this is the #752 regression itself"
        )

        # negative control: a term that exists nowhere, not even on main, must still read as
        # uncovered — the coverage check must still queue a genuine miss
        assert citation_on_ref("adr-9999-nowhere", "main", pathspec, cwd=repo) is False, (
            "a term covered nowhere must still read as uncovered (negative control) — proves "
            "the True case above isn't a check that always returns True"
        )

        # sanity: the ref itself resolving to nothing (a bad ref) is a no-op miss, never a crash
        assert citation_on_ref("adr-0023", "refs/heads/does-not-exist", pathspec, cwd=repo) is False, \
            "an unresolvable ref must degrade to a plain no-hit, never raise"

    print("adr_queue selftest · PASS · append/idempotent-update/multi-kind/precise-clear/bare-clear "
          "all correct, clearing an absent id or id:kind pair is a safe no-op; citation_on_ref "
          "resolves against the given git ref (not the working tree), proven against a real "
          "stale-branch fixture plus a nowhere-covered negative control and an unresolvable-ref "
          "no-crash case")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(argv))
