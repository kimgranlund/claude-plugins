#!/usr/bin/env python3
"""adr_checkpoint — cheap, deterministic diff of an ADR corpus against its last-scanned state.

Usage:
  adr_checkpoint.py classify <adr-dir> [--checkpoint <path>]   report the delta; never writes
  adr_checkpoint.py advance <adr-dir> [--checkpoint <path>]    write the checkpoint to the
                                                                current tree — run ONLY after
                                                                classify's delta has been judged
  adr_checkpoint.py selftest                                   prove the classifier on fixtures

The economic contract this script exists to hold: judgment (a real model asking "does this
Decision cross the harvest bar") is expensive and must run ONLY on what changed. This script's
job ends at producing that delta — new / amended / newly-superseded / unchanged — as cheaply as
a content hash per file allows, so the cost of one firing stays proportional to what changed
since last time, never to how large the ADR corpus has grown.

`classify` and `advance` are deliberately two calls, never one: a caller that judges the delta
between them and dies before finishing leaves the checkpoint UNADVANCED, so the unjudged delta
reappears next firing instead of silently reading as "unchanged" forever (the same
create-then-edit safety split ADR-0004's dual-write already established for this workspace — a
combined classify-and-advance call that half-completes is worse than two calls that don't).

Supersession is read from frontmatter, not inferred: an ADR is superseded the moment ANY other
ADR's `supersedes:` field names it (ADR-0002/0003/0004/0005's own convention), or its own
`status:` field already says `superseded`. `newly_superseded` fires once, the run it's first
detected — a caller that advances the checkpoint after acting on it won't see the same ADR twice.

Checkpoint schema: {"adrs": {"<adr-id>": {"hash": "<sha256>", "status": "<accepted|superseded>"}}}
"""
import hashlib
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
FIELD_RE = re.compile(r"^(id|status|supersedes)\s*:\s*(.+?)\s*$", re.MULTILINE)


def parse_frontmatter(text):
    """Extract id/status/supersedes from an ADR's frontmatter block. Pure — no I/O."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields = dict(FIELD_RE.findall(m.group(1)))
    supersedes = fields.get("supersedes", "null").strip()
    return {
        "id": fields.get("id", "").strip(),
        "status": fields.get("status", "").strip(),
        "supersedes": None if supersedes in ("null", "") else supersedes,
    }


def hash_adr(content):
    """sha256 of the full file content — pure, deterministic."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def classify_delta(old_checkpoint, current):
    """The whole classifier, pure — the unit selftest proves every shape.

    old_checkpoint: {adr_id: {"hash": str, "status": str}}
    current:        {adr_id: {"hash": str, "status": str, "supersedes": str|None}}
    returns:        {"new": [...], "amended": [...], "newly_superseded": [...], "unchanged": [...]}
    """
    new, amended, unchanged = [], [], []
    for adr_id, rec in current.items():
        old = old_checkpoint.get(adr_id)
        if old is None:
            new.append(adr_id)
        elif old["hash"] != rec["hash"]:
            amended.append(adr_id)
        else:
            unchanged.append(adr_id)

    superseded_now = {rec["supersedes"] for rec in current.values() if rec.get("supersedes")}
    superseded_now |= {adr_id for adr_id, rec in current.items() if rec.get("status") == "superseded"}
    newly_superseded = sorted(
        adr_id for adr_id in superseded_now
        if old_checkpoint.get(adr_id, {}).get("status") != "superseded"
    )

    return {
        "new": sorted(new),
        "amended": sorted(amended),
        "newly_superseded": newly_superseded,
        "unchanged": sorted(unchanged),
    }


def load_checkpoint(path):
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8")).get("adrs", {})


def save_checkpoint(path, current):
    Path(path).write_text(
        json.dumps({"adrs": current}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def scan_dir(adr_dir):
    """Read every *.md in adr_dir, parse frontmatter + hash. Skips files with no adr frontmatter."""
    current = {}
    for f in sorted(Path(adr_dir).glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if not fm or not fm["id"]:
            continue
        current[fm["id"]] = {
            "hash": hash_adr(text),
            "status": fm["status"],
            "supersedes": fm["supersedes"],
        }
    return current


def run_classify(adr_dir, checkpoint_path):
    """Report the delta only — never writes the checkpoint. A caller that dies mid-judgment
    leaves the checkpoint untouched, so the unjudged delta reappears next firing instead of
    silently reading as 'unchanged' forever."""
    old = load_checkpoint(checkpoint_path)
    current = scan_dir(adr_dir)
    delta = classify_delta(old, current)

    print(f"adr_checkpoint classify · {adr_dir}")
    print(f"  {len(current)} ADR(s) scanned against checkpoint ({len(old)} previously known)")
    for kind in ("new", "amended", "newly_superseded"):
        if delta[kind]:
            print(f"  {kind}: {', '.join(delta[kind])}")
    if not any(delta[k] for k in ("new", "amended", "newly_superseded")):
        print("  nothing changed since the last checkpoint")
    print("  checkpoint NOT advanced -> run `advance` once this delta has been judged/queued")
    return 0


def run_advance(adr_dir, checkpoint_path):
    """Write the checkpoint to reflect the CURRENT tree — call only after the delta a prior
    `classify` reported has actually been judged and queued, never before."""
    current = scan_dir(adr_dir)
    save_checkpoint(checkpoint_path, {
        adr_id: {"hash": rec["hash"], "status": rec["status"]}
        for adr_id, rec in current.items()
    })
    print(f"adr_checkpoint advance · {len(current)} ADR(s) -> checkpoint written to {checkpoint_path}")
    return 0


def selftest():
    # parse_frontmatter — the real shape this workspace's ADRs ship
    fm = parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0003\nstatus: accepted\nsupersedes: null\n---\n# body"
    )
    assert fm == {"id": "adr-0003", "status": "accepted", "supersedes": None}, fm

    fm2 = parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0006\nstatus: accepted\nsupersedes: adr-0002\n---\n# body"
    )
    assert fm2["supersedes"] == "adr-0002", fm2

    assert parse_frontmatter("no frontmatter here") is None

    # hash_adr — deterministic, content-sensitive
    assert hash_adr("x") == hash_adr("x")
    assert hash_adr("x") != hash_adr("y")

    # classify_delta — every shape
    old = {"adr-0001": {"hash": "h1", "status": "accepted"}}
    current = {
        "adr-0001": {"hash": "h1", "status": "accepted", "supersedes": None},   # unchanged
        "adr-0002": {"hash": "h2", "status": "accepted", "supersedes": None},   # new
    }
    d = classify_delta(old, current)
    assert d["new"] == ["adr-0002"], d
    assert d["amended"] == [], d
    assert d["unchanged"] == ["adr-0001"], d
    assert d["newly_superseded"] == [], d

    # amended: same id, hash moved
    current_amended = {"adr-0001": {"hash": "h1-changed", "status": "accepted", "supersedes": None}}
    d2 = classify_delta(old, current_amended)
    assert d2["amended"] == ["adr-0001"], d2
    assert d2["new"] == [] and d2["unchanged"] == [], d2

    # newly_superseded: a fresh ADR's `supersedes:` names an old one
    old2 = {
        "adr-0001": {"hash": "h1", "status": "accepted"},
        "adr-0002": {"hash": "h2", "status": "accepted"},
    }
    current3 = {
        "adr-0001": {"hash": "h1", "status": "accepted", "supersedes": None},
        "adr-0002": {"hash": "h2", "status": "accepted", "supersedes": None},
        "adr-0003": {"hash": "h3", "status": "accepted", "supersedes": "adr-0001"},
    }
    d3 = classify_delta(old2, current3)
    assert d3["new"] == ["adr-0003"], d3
    assert d3["newly_superseded"] == ["adr-0001"], d3
    assert "adr-0002" not in d3["newly_superseded"], d3

    # the negative control this script exists to bite: a superseded ADR already recorded as
    # superseded in the OLD checkpoint must never re-fire newly_superseded on an unrelated re-run
    old3 = {
        "adr-0001": {"hash": "h1", "status": "superseded"},
        "adr-0003": {"hash": "h3", "status": "accepted"},
    }
    d4 = classify_delta(old3, current3)
    assert d4["newly_superseded"] == [], \
        f"an already-recorded supersession must not re-fire: {d4}"

    # cost-shape control: a large unchanged corpus + one new ADR only ever appears in 'new' —
    # the delta stays proportional to what changed, not to corpus size
    big_old = {f"adr-{i:04d}": {"hash": f"h{i}", "status": "accepted"} for i in range(500)}
    big_current = {
        f"adr-{i:04d}": {"hash": f"h{i}", "status": "accepted", "supersedes": None}
        for i in range(500)
    }
    big_current["adr-9999"] = {"hash": "hnew", "status": "accepted", "supersedes": None}
    d5 = classify_delta(big_old, big_current)
    assert d5["new"] == ["adr-9999"], d5
    assert len(d5["unchanged"]) == 500, d5
    assert d5["amended"] == [] and d5["newly_superseded"] == [], d5

    print("adr_checkpoint selftest · PASS · frontmatter parse, hashing, and all four delta "
          "shapes correct (incl. the already-recorded-supersession and corpus-size negative controls)")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "selftest":
        sys.exit(selftest())
    if len(argv) < 2 or argv[0] not in ("classify", "advance"):
        print(__doc__)
        sys.exit(2)
    cmd, adr_dir, rest = argv[0], argv[1], argv[2:]
    checkpoint_path = ".claude/ops/adr-checkpoint.json"
    if "--checkpoint" in rest:
        checkpoint_path = rest[rest.index("--checkpoint") + 1]
    if cmd == "classify":
        sys.exit(run_classify(adr_dir, checkpoint_path))
    sys.exit(run_advance(adr_dir, checkpoint_path))
