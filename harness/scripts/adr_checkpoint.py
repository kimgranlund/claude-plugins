#!/usr/bin/env python3
"""adr_checkpoint — cheap, deterministic diff of an ADR corpus against its last-scanned state.

Usage:
  adr_checkpoint.py classify <adr-source> [--checkpoint <path>]  report the delta; never writes
  adr_checkpoint.py advance <adr-source> [--checkpoint <path>]   write the checkpoint to the
                                                                  current tree — run ONLY after
                                                                  classify's delta has been judged
  adr_checkpoint.py selftest                                     prove the classifier on fixtures

<adr-source> is either a DIRECTORY of one-ADR-per-file `*.md` (each carrying `doc-type: adr` /
`id:` / `status:` / `supersedes:` frontmatter) or a single markdown FILE whose ADRs are `##`
sections — auto-detected via `Path.is_file()`. A section's id comes from its heading
(`## ADR-NNN — Title`, case-insensitive `ADR-`); a heading annotation containing the word
"superseded" (e.g. `(SUPERSEDED — see ADR-011)`) sets that ADR's own status to `superseded`
directly — the single-file corpus this mode was built for records supersession on the
superseded ADR's own heading, not always as a forward `supersedes:` declaration on the
announcer, so self-status is the primary signal and a `(supersedes ADR-XXX[, ADR-YYY])`
annotation (never `complements`/other verbs) is read as the secondary, forward-declaring one —
same shape as frontmatter's `supersedes:` field, and reuses the same `superseded_ids()`
extraction. Each section is bounded by the next `##` heading of ANY kind (not just ADR
headings), so trailing non-ADR content (an appendix, a "quick map") never bleeds into the last
ADR's hash.

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
ADR_ID_RE = re.compile(r"adr-\d+")

HEADING_RE = re.compile(r"^## .*$", re.MULTILINE)
ADR_HEADING_ID_RE = re.compile(r"^## (ADR-\d+)\b", re.IGNORECASE)
SUPERSEDES_ANNOTATION_RE = re.compile(r"(?i)\bsupersedes\s+([A-Za-z0-9,\s-]*ADR-\d+[A-Za-z0-9,\s-]*)")


def superseded_ids(supersedes_value):
    """Extract adr-NNNN token(s) out of a `supersedes:` field value, ignoring any trailing
    annotation. A field can be a bare id ('adr-0006'), an annotated partial-supersession
    ('adr-0006 (the frozen-dir clause of its install-identity decision only)'), or list more
    than one id — the annotation text itself never matches a checkpoint key, so it must never
    be compared as-is."""
    if not supersedes_value:
        return []
    return ADR_ID_RE.findall(supersedes_value)


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


def parse_single_file_sections(text):
    """Split one markdown file into `## ADR-NNN ...` sections and return the same shape
    scan_dir does — pure, no I/O, so selftest can exercise it directly on fixture strings.

    Each section runs from its heading to the next `## ` heading of ANY kind (or EOF), so a
    trailing non-ADR heading never bleeds into the last ADR's hash. A non-ADR `##` section
    (e.g. an appendix) is skipped entirely — it never becomes a checkpoint entry."""
    bounds = [m.start() for m in HEADING_RE.finditer(text)] + [len(text)]
    current = {}
    for start, end in zip(bounds, bounds[1:]):
        section_text = text[start:end]
        heading_line = section_text.splitlines()[0]
        id_match = ADR_HEADING_ID_RE.match(heading_line)
        if not id_match:
            continue
        adr_id = id_match.group(1).lower()
        status = "superseded" if "superseded" in heading_line.lower() else "accepted"
        sup_match = SUPERSEDES_ANNOTATION_RE.search(heading_line)
        supersedes = None
        if sup_match:
            ids = [tok.lower() for tok in ADR_ID_RE.findall(sup_match.group(1).lower())]
            supersedes = ", ".join(ids) if ids else None
        current[adr_id] = {
            "hash": hash_adr(section_text),
            "status": status,
            "supersedes": supersedes,
        }
    return current


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

    # newly_superseded is derived ONLY from records whose content changed this round (new or
    # amended) — never from unchanged ones. A full supersession flips the superseded ADR's own
    # `status:` to "superseded", which IS a hash change, so it always shows up here. But a
    # PARTIAL/annotated supersession (e.g. "adr-0006 (the frozen-dir clause ... only)") never
    # flips the target's own status — it stays legitimately "accepted" forever — so there is no
    # persisted signal except "did the announcing ADR's content change since last checkpoint".
    # Deriving from every current record (changed or not) is exactly the bug this guards: once
    # advanced, the announcing ADR becomes unchanged next run, and without this restriction its
    # supersedes claim would be re-read and re-flagged as newly_superseded forever.
    changed_ids = set(new) | set(amended)
    superseded_now = set()
    for adr_id in changed_ids:
        superseded_now |= set(superseded_ids(current[adr_id].get("supersedes")))
    superseded_now |= {adr_id for adr_id in changed_ids if current[adr_id].get("status") == "superseded"}
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


def scan_single_file(adr_file):
    """Read one markdown file and hash its `## ADR-NNN` sections. Thin I/O wrapper around the
    pure `parse_single_file_sections` — mirrors scan_dir's split from parse_frontmatter."""
    text = Path(adr_file).read_text(encoding="utf-8", errors="replace")
    return parse_single_file_sections(text)


def scan_source(adr_source):
    """Auto-detect: a directory scans as one-ADR-per-file frontmatter, a file scans as
    `## ADR-NNN` sections. The caller never has to know which shape a repo's corpus uses."""
    return scan_single_file(adr_source) if Path(adr_source).is_file() else scan_dir(adr_source)


def run_classify(adr_source, checkpoint_path):
    """Report the delta only — never writes the checkpoint. A caller that dies mid-judgment
    leaves the checkpoint untouched, so the unjudged delta reappears next firing instead of
    silently reading as 'unchanged' forever."""
    old = load_checkpoint(checkpoint_path)
    current = scan_source(adr_source)
    delta = classify_delta(old, current)

    print(f"adr_checkpoint classify · {adr_source}")
    print(f"  {len(current)} ADR(s) scanned against checkpoint ({len(old)} previously known)")
    for kind in ("new", "amended", "newly_superseded"):
        if delta[kind]:
            print(f"  {kind}: {', '.join(delta[kind])}")
    if not any(delta[k] for k in ("new", "amended", "newly_superseded")):
        print("  nothing changed since the last checkpoint")
    print("  checkpoint NOT advanced -> run `advance` once this delta has been judged/queued")
    return 0


def run_advance(adr_source, checkpoint_path):
    """Write the checkpoint to reflect the CURRENT tree — call only after the delta a prior
    `classify` reported has actually been judged and queued, never before."""
    current = scan_source(adr_source)
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

    # superseded_ids — the annotated-value bug this script was fixed for: a `supersedes:` field
    # naming a partial supersession in prose must still extract the bare adr id
    assert superseded_ids("adr-0006") == ["adr-0006"]
    assert superseded_ids(
        "adr-0006 (the frozen-dir clause of its install-identity decision only)"
    ) == ["adr-0006"]
    assert superseded_ids(None) == []

    # negative control: a supersedes value with no adr-\d+ token must match nothing at all —
    # proves the extraction doesn't fall back to treating the raw string as an id
    assert superseded_ids("the old informal design, no ADR filed") == []

    # end-to-end: an annotated partial-supersession value must classify adr-0006 as
    # newly_superseded exactly once, driven off the extracted id, not the raw string. adr-0007
    # (the announcer) is absent from the old checkpoint — i.e. genuinely new this round — since
    # that's the real-world trigger: the announcing ADR's own content is new/amended.
    old6 = {"adr-0006": {"hash": "h6", "status": "accepted"}}
    current6 = {
        "adr-0006": {"hash": "h6", "status": "accepted", "supersedes": None},
        "adr-0007": {
            "hash": "h7",
            "status": "accepted",
            "supersedes": "adr-0006 (the frozen-dir clause of its install-identity decision only)",
        },
    }
    d6 = classify_delta(old6, current6)
    assert d6["newly_superseded"] == ["adr-0006"], d6
    assert d6["newly_superseded"].count("adr-0006") == 1, d6

    # negative control on the same shape: a supersedes value with no adr token must not
    # spuriously mark anything superseded
    current6b = {
        "adr-0006": {"hash": "h6", "status": "accepted", "supersedes": None},
        "adr-0007": {
            "hash": "h7", "status": "accepted", "supersedes": "an earlier informal draft",
        },
    }
    d6b = classify_delta(old6, current6b)
    assert d6b["newly_superseded"] == [], d6b

    # the "forever" bug this script was fixed for: after advance persists adr-0007's own status
    # ("accepted" — a partial supersession never flips it) verbatim, a SECOND classify against the
    # advanced checkpoint must NOT re-report adr-0006, even though adr-0006's own checkpoint
    # status is still (correctly) "accepted", not "superseded" — because adr-0007 is now
    # unchanged and carries no new information.
    old7_after_advance = {
        adr_id: {"hash": rec["hash"], "status": rec["status"]} for adr_id, rec in current6.items()
    }
    assert old7_after_advance["adr-0006"]["status"] == "accepted", old7_after_advance
    d7 = classify_delta(old7_after_advance, current6)
    assert d7["newly_superseded"] == [], \
        f"a partial supersession must not re-fire every run after advance: {d7}"

    # parse_single_file_sections — the real shape a monolithic decision-records.md ships:
    # heading-only ids, self-status from a "superseded" annotation, forward supersedes from a
    # "(supersedes ADR-NNN)" annotation, non-ADR headings skipped, no section bleed.
    single_file_text = (
        "# Decision records\n\n"
        "## ADR-001 — First decision\n"
        "- **Status.** DECIDED.\n\n"
        "## ADR-002 — Second decision  **(SUPERSEDED — see ADR-003)**\n"
        "- **Status.** DECIDED.\n\n"
        "## ADR-003 — Third decision  (supersedes ADR-002)\n"
        "- **Status.** DECIDED.\n\n"
        "## ADR-004 — Fourth decision  (complements ADR-003)\n"
        "- **Status.** DECIDED.\n\n"
        "## Quick map: things not to touch\n"
        "This trailer must never bleed into ADR-004's hash.\n"
    )
    sections = parse_single_file_sections(single_file_text)
    assert set(sections) == {"adr-001", "adr-002", "adr-003", "adr-004"}, sections
    assert sections["adr-001"]["status"] == "accepted", sections["adr-001"]
    assert sections["adr-002"]["status"] == "superseded", sections["adr-002"]
    assert sections["adr-003"]["status"] == "accepted", sections["adr-003"]
    assert sections["adr-003"]["supersedes"] == "adr-002", sections["adr-003"]
    # "complements" is not "supersedes" — must never be read as a supersession
    assert sections["adr-004"]["supersedes"] is None, sections["adr-004"]
    adr004_hash = hash_adr(
        single_file_text[
            single_file_text.index("## ADR-004"):single_file_text.index("## Quick map")
        ]
    )
    assert sections["adr-004"]["hash"] == adr004_hash, "trailing non-ADR heading bled into the hash"

    # case-insensitive heading id + a real single-file classify_delta round-trip: ADR-002's own
    # status flip to superseded fires newly_superseded on first sight (self-status), same as the
    # frontmatter-mode self-superseding path already proves above
    single_file_delta = classify_delta({}, sections)
    assert "adr-002" in single_file_delta["newly_superseded"], single_file_delta

    print("adr_checkpoint selftest · PASS · frontmatter parse, hashing, all four delta shapes, "
          "annotated-supersedes extraction (incl. already-recorded-supersession, corpus-size, "
          "no-adr-token, and post-advance forever-refire negative controls), and single-file "
          "section parsing (self-status, forward-supersedes, complements-is-not-supersedes, "
          "no section bleed)")
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
