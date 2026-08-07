#!/usr/bin/env python3
"""adr_checkpoint — cheap, deterministic diff of an ADR corpus against its last-scanned state.

Usage:
  adr_checkpoint.py classify <adr-source> [--checkpoint <path>]  report the delta; never writes
  adr_checkpoint.py advance <adr-source> [--checkpoint <path>]   write the checkpoint to the
                                                                  current tree — run ONLY after
                                                                  classify's delta has been judged
  adr_checkpoint.py selftest                                     prove the classifier on fixtures

<adr-source> is either a DIRECTORY of one-ADR-per-file `*.md` or a single markdown FILE whose
ADRs are `##` sections — auto-detected via `Path.is_file()`.

A DIRECTORY's files are parsed in either of three dialects, tried per file in this order:

1. **YAML frontmatter** — `doc-type: adr` / `id:` / `status:` / `supersedes:`. Hash basis is the
   WHOLE file, unchanged since this script's first version, so existing checkpoints stay valid.
2. **H1 + blockquote status table** — an `# ADR-NNNN — Title` heading plus a leading blockquote
   table whose rows read `> | **Status** | accepted |` and
   `> | **Supersedes / Superseded by** | ... |` (agent-ui's dialect, which never adopted
   `doc-type:` frontmatter). Status is the first bare keyword in the cell, so a cell trailing
   prose after it still reads. Hash basis is the STATUS plus the `## Decision` / `## Amendment*` /
   `## Supersession*` sections only — NOT the whole file: this dialect's ADRs carry long
   Context/Consequences prose whose copy-edits are not decisions, and the status is folded in
   because a ratification or supersession flips only that one table cell and must still register
   as a change. A forward supersession is read ONLY from the active-voice `supersedes ADR-NNNN`;
   `Extends` / `Relates` / `Amended by` / `Superseded by` name relationships this script must
   never misread as a supersession — the row's own `**Supersedes / Superseded by**` label
   included.
3. **H1 + bold metadata block** — an `# ADR-NNN: Title` (or `— Title`) heading followed by plain
   `**Status:** <value>` / `**Supersedes:** <value>` lines (no blockquote table at all —
   adiav2's `docs/adr/` dialect). Status is the first bare keyword after the label, same
   extraction as dialect 2's table cell. Hash basis is the WHOLE file, same as frontmatter: this
   dialect's real corpus (a PoC findings report, an outbox design doc) uses ad hoc section names
   with no reliable `## Decision` heading to scope to, so — unlike dialect 2 — there is no safe
   narrower basis; any edit anywhere reads as amended, which is coarser but never silently misses
   a real change. `**Supersedes:**` values that don't resolve to a bare `adr-\d+` token (e.g. a
   pre-numbering external id like `ADR-Outbox-01`) correctly extract to nothing — this script
   only tracks numbered ADRs it can key a checkpoint entry on.

A file matching neither dialect is skipped, as before. But a source whose non-empty input yields
ZERO parsed ADRs now FAILS LOUDLY (exit 1, "unsupported shape") instead of reporting a clean empty
delta: a silent 0-ADR scan reads to its caller as "nothing changed" forever, which is the one
failure mode this script's whole purpose cannot survive.

A section's id comes from its heading
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

Exit codes: 0 clean · 1 unsupported shape (no ADR parsed from non-empty input) · 2 usage error.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
FIELD_RE = re.compile(r"^(id|status|supersedes)\s*:\s*(.+?)\s*$", re.MULTILINE)
ADR_ID_RE = re.compile(r"adr-\d+")

HEADING_RE = re.compile(r"^## .*$", re.MULTILINE)
ADR_HEADING_ID_RE = re.compile(r"^## (ADR-\d+)\b", re.IGNORECASE)
SUPERSEDES_ANNOTATION_RE = re.compile(r"(?i)\bsupersedes\s+([A-Za-z0-9,\s-]*ADR-\d+[A-Za-z0-9,\s-]*)")

H1_LINE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H1_ADR_ID_RE = re.compile(r"^(ADR-\d+)\b", re.IGNORECASE)
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
STATUS_KEYWORD_RE = re.compile(r"[A-Za-z]+")
# Active voice ONLY: `supersedes` never matches `superseded`/`superseding`, so "Superseded by
# ADR-0033" (this ADR is the victim, and its own Status cell already says so) and the row's own
# "Supersedes / Superseded by" label both fall through. After the keyword, only emphasis noise,
# commas, "and", and a markdown link TAIL may separate the ids — the first real prose word ends the
# run, so "Supersedes ADR-0017 cl.3 in part" yields adr-0017 and nothing else. The link tail is
# spelled `](no-spaces)` deliberately: it admits `[ADR-0002](./0002-x.md), [ADR-0003](...)` while
# still refusing a prose parenthetical, which always contains spaces — so "Supersedes ADR-0002 (the
# frozen-dir clause of ADR-0006 only)" can never over-capture ADR-0006. Over-capture is the worse
# failure here: it would brand a live, accepted decision as superseded.
TABLE_SUPERSEDES_RE = re.compile(
    r"(?i)\bsupersedes\b[:\s]*((?:(?:\]\([^)\s]*\)|[*`\[\]\s,]|\band\b)*ADR-\d+)+)"
)
# The sections whose content IS the decision — everything else in a table-dialect ADR is context.
HASH_SECTION_PREFIXES = ("decision", "amendment", "supersession")

# Dialect 3 — H1 + bold `**Field:**` metadata lines, no blockquote table (adiav2's docs/adr/).
# The trailing `:?` before AND after the closing `**` tolerates either colon placement
# (`**Status:**` or `**Status**:`) without needing two separate patterns.
BOLD_STATUS_RE = re.compile(r"^\*\*Status:?\*\*:?\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
BOLD_SUPERSEDES_RE = re.compile(r"^\*\*Supersedes:?\*\*:?\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)


class UnsupportedAdrShape(Exception):
    """Raised when non-empty input yields zero parsed ADRs — never a clean empty report."""


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


def table_row_cells(line):
    """Split one blockquote table row into its cells, honoring `\\|` escapes. Returns [] for any
    line that isn't a table row. Pure."""
    body = line.strip()
    if body.startswith(">"):
        body = body[1:].strip()
    if not body.startswith("|"):
        return []
    body = body[1:].rstrip()
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [cell.strip() for cell in CELL_SPLIT_RE.split(body)]


def table_field_name(cell):
    """Normalize a table row's label cell to a bare lowercase field name — `**Status**` -> status."""
    return cell.strip().strip("*`_ ").lower()


def table_superseded_ids(cell_value):
    """Extract the adr ids this ADR actively SUPERSEDES from its `Supersedes / Superseded by` cell.
    Pure. Returns a comma-joined string (the same shape frontmatter's `supersedes:` field carries,
    so `superseded_ids()` consumes it unchanged) or None."""
    if not cell_value:
        return None
    ids = []
    for m in TABLE_SUPERSEDES_RE.finditer(cell_value):
        for token in ADR_ID_RE.findall(m.group(1).lower()):
            if token not in ids:
                ids.append(token)
    return ", ".join(ids) if ids else None


def parse_status_table(text):
    """Extract id/status/supersedes from an H1 + blockquote-status-table ADR. Pure — no I/O.
    Returns None when the text isn't this dialect (no `# ADR-NNNN` title, or no Status row), so a
    README or a `# ADR-NNNN — <title>` TEMPLATE (literal NNNN, no digits) is skipped naturally."""
    title = H1_LINE_RE.search(text)
    if not title:
        return None
    id_match = H1_ADR_ID_RE.match(title.group(1).strip())
    if not id_match:
        return None

    status, supersedes = None, None
    for line in text.splitlines():
        cells = table_row_cells(line)
        if len(cells) < 2:
            continue
        field = table_field_name(cells[0])
        if field == "status" and status is None:
            # The bare leading keyword only: the template's cell trails a prose gloss after it.
            keyword = STATUS_KEYWORD_RE.search(cells[1].strip("*`_ "))
            if keyword:
                status = keyword.group(0).lower()
        elif "supersedes" in field and supersedes is None:
            supersedes = table_superseded_ids(cells[1])
    if status is None:
        return None
    return {"id": id_match.group(1).lower(), "status": status, "supersedes": supersedes}


def parse_bold_metadata(text):
    """Extract id/status/supersedes from an H1 + bold `**Field:**` metadata-block ADR (no
    blockquote table). Pure — no I/O. Returns None when the text isn't this dialect (no
    `# ADR-NNN` title, or no `**Status:**` line), so a file already claimed by the table dialect
    — or a non-ADR doc — is skipped naturally."""
    title = H1_LINE_RE.search(text)
    if not title:
        return None
    id_match = H1_ADR_ID_RE.match(title.group(1).strip())
    if not id_match:
        return None
    status_match = BOLD_STATUS_RE.search(text)
    if not status_match:
        return None
    keyword = STATUS_KEYWORD_RE.search(status_match.group(1).strip("*`_ "))
    if not keyword:
        return None
    supersedes = None
    sup_match = BOLD_SUPERSEDES_RE.search(text)
    if sup_match:
        ids = ADR_ID_RE.findall(sup_match.group(1).lower())
        supersedes = ", ".join(ids) if ids else None
    return {"id": id_match.group(1).lower(), "status": keyword.group(0).lower(), "supersedes": supersedes}


def decision_content(text):
    """The hash basis for a table-dialect ADR: its `## Decision` / `## Amendment*` /
    `## Supersession*` sections, concatenated, so Context/Consequences copy-edits never read as an
    amended decision. Falls back to the WHOLE text when no such section exists — never to an empty
    string, which would make every section-less ADR hash alike and hide real edits. Pure."""
    bounds = [m.start() for m in HEADING_RE.finditer(text)] + [len(text)]
    chunks = []
    for start, end in zip(bounds, bounds[1:]):
        section = text[start:end]
        heading = section.splitlines()[0][2:].strip().strip("*`# ").lower()
        if heading.startswith(HASH_SECTION_PREFIXES):
            chunks.append(section)
    return "".join(chunks) if chunks else text


def hash_adr(content):
    """sha256 of the full file content — pure, deterministic."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def parse_adr_file(text):
    """Parse one ADR file in whichever dialect it ships, frontmatter first. Returns a record
    {"id", "hash", "status", "supersedes"} or None when neither dialect matches. Pure."""
    fm = parse_frontmatter(text)
    if fm and fm["id"]:
        # Whole-file hash, unchanged — existing frontmatter checkpoints stay valid.
        return {
            "id": fm["id"],
            "hash": hash_adr(text),
            "status": fm["status"],
            "supersedes": fm["supersedes"],
        }
    table = parse_status_table(text)
    if table:
        # Status is folded into the basis: ratification and supersession flip ONLY that one cell,
        # and a status flip that left the hash untouched would never surface as a delta at all.
        return {
            "id": table["id"],
            "hash": hash_adr(table["status"] + "\n" + decision_content(text)),
            "status": table["status"],
            "supersedes": table["supersedes"],
        }
    bold = parse_bold_metadata(text)
    if bold:
        # Whole-file hash, same rationale as frontmatter — no reliable Decision-scoped section
        # to narrow to in this dialect's real corpus.
        return {
            "id": bold["id"],
            "hash": hash_adr(text),
            "status": bold["status"],
            "supersedes": bold["supersedes"],
        }
    return None


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


def unsupported_shape(source, skipped):
    """The loud failure: non-empty input, zero ADRs parsed. Names the dialects understood and
    samples the files that matched none, so an operator can tell an unsupported dialect apart from
    a corpus that genuinely holds no ADRs yet."""
    return UnsupportedAdrShape(
        "{} non-empty file(s) under {} but 0 parsed as an ADR — unsupported shape.\n"
        "  Dialects understood: (a) YAML frontmatter `doc-type: adr` + `id:` + `status:`; "
        "(b) an `# ADR-NNNN — Title` H1 plus a blockquote row `> | **Status** | accepted |`; "
        "(c) an `# ADR-NNN: Title` H1 plus a bare `**Status:** value` line, no table; "
        "(d) a single file of `## ADR-NNN — Title` sections.\n"
        "  Matched none: {}".format(
            len(skipped), source, ", ".join(skipped[:5]) + (" ..." if len(skipped) > 5 else "")
        )
    )


def scan_dir(adr_dir):
    """Read every *.md in adr_dir and parse it in either dialect (see parse_adr_file). Skips files
    matching neither — but raises UnsupportedAdrShape when EVERY non-empty file is skipped."""
    current = {}
    skipped = []
    for f in sorted(Path(adr_dir).glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        rec = parse_adr_file(text)
        if rec is None:
            if text.strip():
                skipped.append(f.name)
            continue
        current[rec["id"]] = {
            "hash": rec["hash"],
            "status": rec["status"],
            "supersedes": rec["supersedes"],
        }
    if not current and skipped:
        raise unsupported_shape(adr_dir, skipped)
    return current


def scan_single_file(adr_file):
    """Read one markdown file and hash its `## ADR-NNN` sections. Thin I/O wrapper around the
    pure `parse_single_file_sections` — mirrors scan_dir's split from parse_frontmatter, and shares
    its loud failure on non-empty input that yields nothing."""
    text = Path(adr_file).read_text(encoding="utf-8", errors="replace")
    sections = parse_single_file_sections(text)
    if not sections and text.strip():
        raise unsupported_shape(adr_file, [Path(adr_file).name])
    return sections


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

    # ---- the H1 + blockquote-status-table dialect (agent-ui's, 169 real files) ----------------
    table_adr = (
        "# ADR-0168 — Integrations become a manifest registry\n\n"
        "> Source: agent-ui ADR log. Log + lifecycle: [`README.md`](./README.md). · 2026-08-04\n"
        ">\n"
        "> | Field | Value |\n"
        "> |---|---|\n"
        "> | **Status** | accepted |\n"
        "> | **Date** | 2026-08-04 |\n"
        "> | **Ratified by** | kimgranlund (repo owner), 2026-08-04 |\n"
        "> | **Supersedes / Superseded by** | **Extends** [ADR-0137](./0137-a.md) (the shell law) "
        "· **Relates** [ADR-0091](./0091-b.md) · **Amended by ADR-0014** (the variant) "
        "· **Supersedes ADR-0017 cl.3 in part** (the dismissable clause only) "
        "· Font/glyph leg superseded by **ADR-0033** |\n\n"
        "## Context\n\nLong prose that is emphatically not a decision.\n\n"
        "## Decision\n\nEvery dispatch is validated against the declared schema.\n\n"
        "## Consequences\n\nMore prose nobody needs to re-judge.\n"
    )
    t = parse_status_table(table_adr)
    assert t == {"id": "adr-0168", "status": "accepted", "supersedes": "adr-0017"}, t

    # the direction/verb negative control that must bite: every OTHER relation verb in that same
    # cell names a relationship, never a supersession — and "Superseded by X" makes THIS ADR the
    # victim (its own Status cell says so), so X must never be reported as newly superseded
    assert table_superseded_ids(
        "**Extends** ADR-0137 · **Relates** ADR-0091 · **Amended by ADR-0014** "
        "· Font/glyph leg superseded by **ADR-0033** · **Extended by ADR-0032**"
    ) is None, "a non-supersedes relation verb was misread as a supersession"
    # ...including the row's OWN label, which contains the word "Supersedes" verbatim
    assert table_superseded_ids("Supersedes / Superseded by") is None
    assert table_field_name("**Supersedes / Superseded by**") == "supersedes / superseded by"
    # multiple ids after one keyword, emphasis/link noise and "and" between them
    assert table_superseded_ids("**Supersedes** [ADR-0002](./x.md), ADR-0003 and ADR-0004 in full") \
        == "adr-0002, adr-0003, adr-0004"
    # over-capture control: a prose parenthetical after the id must NOT drag in the ADR it cites —
    # branding a live accepted decision as superseded is the worse of the two failures
    assert table_superseded_ids(
        "**Supersedes** ADR-0002 (the frozen-dir clause of ADR-0006's install identity only)"
    ) == "adr-0002"

    # escaped pipes inside a cell must not split it — the real template's Status cell does this
    template_status_row = (
        "> | **Status** | proposed *(one bare keyword only: `proposed` \\| `accepted` \\| "
        "`superseded` — never trailing prose)* |"
    )
    cells = table_row_cells(template_status_row)
    assert len(cells) == 2, cells
    assert cells[1].startswith("proposed"), cells

    # the hash basis: Decision only (+ status), so a Context copy-edit is NOT an amended decision
    assert decision_content(table_adr).startswith("## Decision"), decision_content(table_adr)
    assert "Long prose" not in decision_content(table_adr)
    assert "More prose" not in decision_content(table_adr)
    rec = parse_adr_file(table_adr)
    assert rec["id"] == "adr-0168" and rec["status"] == "accepted", rec
    context_edited = table_adr.replace("emphatically not a decision", "certainly not a decision")
    assert parse_adr_file(context_edited)["hash"] == rec["hash"], \
        "a Context copy-edit must not read as an amended decision"
    # reverse control: a real Decision edit MUST move the hash
    decision_edited = table_adr.replace("validated against the declared schema", "dispatched raw")
    assert parse_adr_file(decision_edited)["hash"] != rec["hash"], \
        "a real Decision edit must move the hash"

    # a ratification/supersession flips ONLY the Status cell — folding status into the basis is
    # what makes that flip visible at all, and newly_superseded then fires off self-status
    flipped = table_adr.replace("| **Status** | accepted |", "| **Status** | superseded |")
    flipped_rec = parse_adr_file(flipped)
    assert flipped_rec["status"] == "superseded", flipped_rec
    assert flipped_rec["hash"] != rec["hash"], "a status-only flip must register as a change"
    d8 = classify_delta(
        {"adr-0168": {"hash": rec["hash"], "status": "accepted"}},
        {"adr-0168": {k: flipped_rec[k] for k in ("hash", "status", "supersedes")}},
    )
    assert d8["amended"] == ["adr-0168"], d8
    # adr-0168 fires off its own flipped status; adr-0017 off the forward declaration it still
    # carries — both are legitimately newly superseded on this round
    assert d8["newly_superseded"] == ["adr-0017", "adr-0168"], d8

    # an amendment section counts as decision content; a section-less ADR falls back to the WHOLE
    # text, so two different section-less ADRs never collide into one hash
    amended_adr = table_adr + "\n## Amendment 1 — 2026-08-05 — the key resolves server-side\n"
    assert parse_adr_file(amended_adr)["hash"] != rec["hash"], "an appended Amendment must be seen"
    bare_a = "# ADR-0900 — Bare\n\n> | **Status** | accepted |\n\nNo decision section here, A.\n"
    bare_b = "# ADR-0901 — Bare\n\n> | **Status** | accepted |\n\nNo decision section here, B.\n"
    assert decision_content(bare_a) == bare_a, "section-less fallback must be the whole text"
    assert parse_adr_file(bare_a)["hash"] != parse_adr_file(bare_b)["hash"], \
        "section-less ADRs must not hash alike"

    # non-ADR neighbours in a real ADR directory are skipped by shape alone, no name special-case:
    # the template's H1 is a literal `ADR-NNNN` (no digits) and the log README has no ADR H1
    assert parse_status_table("# ADR-NNNN — <short decision title>\n\n> | **Status** | proposed |\n") \
        is None, "the template must not be scanned as a real ADR"
    assert parse_status_table("# agent-ui — Architecture Decision Records (ADR log)\n\nprose\n") is None
    # an ADR H1 with no Status row at all is not this dialect
    assert parse_status_table("# ADR-0500 — No status row\n\n## Decision\n\nx\n") is None

    # ---- the H1 + bold metadata-block dialect (adiav2's docs/adr/, no blockquote table) --------
    bold_adr = (
        "# ADR-202: Transactional Outbox for Correctness-Critical Kafka Events\n\n"
        "**Date:** 2026-07-26\n"
        "**Status:** Proposed\n"
        "**Author:** Alex Meshkin\n"
        "**Linear:** ADIA2-6712\n"
        "**Supersedes:** ADR-Outbox-01 (Factory Retry-Coordinator \"transactional produce over "
        "outbox relay\")\n"
        "**Related:** ADR-200 (relational SoR + durable outbox projection)\n\n"
        "---\n\n## Context\n\nLong prose.\n"
    )
    b = parse_bold_metadata(bold_adr)
    # ADR-Outbox-01 carries no adr-\d+ token — a pre-numbering external id never resolves to a
    # checkpoint key, so it correctly extracts to no supersedes at all.
    assert b == {"id": "adr-202", "status": "proposed", "supersedes": None}, b

    # colon-outside-bold variant (`**Status**:` instead of `**Status:**`) must parse the same
    bold_adr_alt_colon = bold_adr.replace("**Status:** Proposed", "**Status**: Proposed")
    assert parse_bold_metadata(bold_adr_alt_colon)["status"] == "proposed"

    # a real numbered supersedes value must extract, same shape as the other two dialects
    bold_adr_numbered = bold_adr.replace(
        "**Supersedes:** ADR-Outbox-01 (Factory Retry-Coordinator \"transactional produce over "
        "outbox relay\")",
        "**Supersedes:** ADR-0006",
    )
    assert parse_bold_metadata(bold_adr_numbered)["supersedes"] == "adr-0006"

    # whole-file hash basis: a Context copy-edit as much as a Status flip must move the hash —
    # no Decision-scoped narrowing exists for this dialect
    bold_rec = parse_adr_file(bold_adr)
    assert bold_rec["id"] == "adr-202" and bold_rec["status"] == "proposed", bold_rec
    context_edited_bold = bold_adr.replace("Long prose.", "Different prose.")
    assert parse_adr_file(context_edited_bold)["hash"] != bold_rec["hash"], \
        "whole-file hash must see a Context edit too — this dialect has no narrower basis"

    # this dialect's H1 uses a colon, not the table dialect's em-dash — must never cross-match
    # dialect 2's table parser (no blockquote row present, so parse_status_table must decline)
    assert parse_status_table(bold_adr) is None, \
        "a bold-metadata ADR with no blockquote table must not be read as the table dialect"

    # a bare `# ADR-NNN: Title` H1 with no **Status:** line at all is not this dialect either
    assert parse_bold_metadata("# ADR-0500: No status line\n\nJust prose.\n") is None

    # ---- end-to-end: one directory, ALL THREE dialects, plus the loud 0-parsed failure ---------
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "0000-template.md").write_text(
            "# ADR-NNNN — <short decision title>\n\n> | **Status** | proposed |\n", encoding="utf-8"
        )
        (d / "README.md").write_text("# The ADR log\n\nindex prose\n", encoding="utf-8")
        (d / "0168-table.md").write_text(table_adr, encoding="utf-8")
        (d / "0003-frontmatter.md").write_text(
            "---\ndoc-type: adr\nid: adr-0003\nstatus: accepted\nsupersedes: null\n---\n# body\n",
            encoding="utf-8",
        )
        (d / "0202-bold.md").write_text(bold_adr, encoding="utf-8")
        scanned = scan_dir(d)
        assert set(scanned) == {"adr-0003", "adr-0168", "adr-202"}, scanned
        assert scanned["adr-0168"]["supersedes"] == "adr-0017", scanned["adr-0168"]
        assert scanned["adr-0003"]["status"] == "accepted", scanned["adr-0003"]
        assert scanned["adr-202"]["status"] == "proposed", scanned["adr-202"]
        # all three dialects feed one delta, keyed the same way
        mixed = classify_delta({}, scanned)
        assert mixed["new"] == ["adr-0003", "adr-0168", "adr-202"], mixed
        assert mixed["newly_superseded"] == ["adr-0017"], mixed

    # the negative control this fix exists for: a directory of files in NO understood dialect must
    # fail loudly, never report a clean empty delta (the silent false-quiet, gh nonoun-plugins#42)
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "README.md").write_text("# index\n\nprose\n", encoding="utf-8")
        (d / "0001-mystery.md").write_text("# Some Other Dialect\n\nStatus: accepted\n", encoding="utf-8")
        try:
            scan_dir(d)
            raise AssertionError("0 parsed ADRs from non-empty input must raise, not return {}")
        except UnsupportedAdrShape as exc:
            assert "unsupported shape" in str(exc), exc
            assert "0001-mystery.md" in str(exc), exc

    # ...but a genuinely EMPTY corpus is not a shape failure — nothing was skipped
    with tempfile.TemporaryDirectory() as tmp:
        assert scan_dir(Path(tmp)) == {}, "an empty directory must not raise"

    print("adr_checkpoint selftest · PASS · frontmatter parse, hashing, all four delta shapes, "
          "annotated-supersedes extraction (incl. already-recorded-supersession, corpus-size, "
          "no-adr-token, and post-advance forever-refire negative controls), single-file "
          "section parsing (self-status, forward-supersedes, complements-is-not-supersedes, "
          "no section bleed), the H1+status-table dialect (bare-keyword status, "
          "escaped-pipe cells, active-voice-only supersedes vs Extends/Relates/Amended-by/"
          "Superseded-by + its own row label, Decision-scoped hash with status folded in, "
          "section-less fallback, template/README skipped by shape), the H1+bold-metadata "
          "dialect (either colon placement, non-numeric supersedes ids resolving to nothing, "
          "whole-file hash basis, no cross-match with the table dialect), a three-dialect mixed "
          "directory, and the loud 0-parsed unsupported-shape failure vs an empty corpus)")
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
    try:
        if cmd == "classify":
            sys.exit(run_classify(adr_dir, checkpoint_path))
        sys.exit(run_advance(adr_dir, checkpoint_path))
    except UnsupportedAdrShape as exc:
        print("adr_checkpoint · FAIL · unsupported shape · 1 fail / 0 warn", file=sys.stderr)
        print("  {}".format(exc), file=sys.stderr)
        sys.exit(1)
