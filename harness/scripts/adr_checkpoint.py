#!/usr/bin/env python3
"""adr_checkpoint — cheap, deterministic diff of an ADR corpus against its last-scanned state.

Usage:
  adr_checkpoint.py classify <adr-source> [--checkpoint <path>]  report the delta; never writes
  adr_checkpoint.py advance <adr-source> [--checkpoint <path>]   write the checkpoint to the
                                                                  current tree — run ONLY after
                                                                  classify's delta has been judged
  adr_checkpoint.py validate <checkpoint-path>                   integrity check ONLY: every
                                                                  stored hash is a well-formed
                                                                  64-char sha256 digest AND every
                                                                  stored status is a known value
                                                                  (issue #1001), no ADR source
                                                                  needed — for a write-relay step
                                                                  to run right after landing a
                                                                  checkpoint on disk (issue #987)
  adr_checkpoint.py selftest                                     prove the classifier on fixtures

<adr-source> is either a DIRECTORY of one-ADR-per-file `*.md` or a single markdown FILE whose
ADRs are `##` sections — auto-detected via `Path.is_file()`.

A DIRECTORY's files are parsed in either of three dialects, tried per file in this order:

1. **YAML frontmatter** — `doc-type: adr` / `id:` / `status:` / `supersedes:`. Hash basis is the
   WHOLE file, unchanged since this script's first version, so existing checkpoints stay valid.
   **Second signal, body-clause supersession (issue #221):** when this field is `null` (unset, or
   left permanently null — an accepted ADR's frontmatter can never be edited post-ratification
   under this workspace's own T4 append-only hook) AND `status: accepted`, the ADR's own BODY
   prose is scanned for an explicit forward clause — `supersedes ADR-NNNN` (full), or `supersedes
   the *<scope>* halves? of ADR-NNNN[ and ADR-MMMM]` (partial, scope-carrying) — active voice
   only, same "never `superseded`/`superseding`" discipline as dialect 2's table cell. This is the
   ONLY place a ratified body-only supersession (ADR-0011's own case, over ADR-0001/ADR-0006's
   grammar halves) can ever be detected, since the frontmatter field is structurally frozen. A
   partial supersession's scope travels with its target id through to `newly_superseded_edges`
   (`adr-0011 -> adr-0006 [grammar]`) rather than collapsing to a bare id — a boolean "superseded
   or not" would lose exactly the information a partial supersession needs.
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
   included. **Amendment ratification marker (issue #929):** each `## Amendment` heading's own
   line — the one carrying its `**proposed** — Kim ratifies` -> `**ratified** — <owner>,
   [utterance](...), verified <date>` flip — is also hashed as its own dedicated signal
   (`amendment_ratification_markers`), independent of the Decision/Amendment section scan above.
   Ratifying an already-drafted amendment on an already-accepted ADR never flips the Status cell
   (accepted already) and, without this signal, would rely entirely on that section scan to catch
   the marker's own text moving — this makes it a structural guarantee instead.
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
`status:` field already says `superseded` — OR (issue #221) an accepted ADR whose own
`supersedes:` field is null names it via the body-clause signal above. `newly_superseded` fires
once, the run it's first detected — a caller that advances the checkpoint after acting on it
won't see the same ADR twice. `newly_superseded_edges` carries the same information scope-first,
one `"<announcer> -> <target>[ [<scope>]]"` string per edge — the frontmatter path's edges are
always scope-less (a boolean field), the body-clause path's may name a scope.

Checkpoint schema: {"formula_version": <int>, "adrs": {"<adr-id>": {"hash": "<sha256>",
"status": "<proposed|accepted|superseded>"}}}. A proposed (not-yet-ratified) ADR IS checkpointed
like any other — its own frontmatter's `status:` field is read verbatim, same as an accepted or
superseded one; nothing in `scan_dir`/`scan_single_file` special-cases it out. `formula_version`
names which HASH_ADR/decision_content
formula computed the stored hashes (issue #945) — a checkpoint written before this field existed
(pre-#929) reads as version 1. `classify` compares the stored version against
CHECKPOINT_FORMULA_VERSION before diffing: a mismatch on a non-empty checkpoint is reported as its
own named event, never silently diffed as a 100%-amended flood (every hash would differ from a
formula change alone, not a real edit) — the fix for the false-flood issue #929's own hash-basis
widening produced. Re-baseline (`advance` under the current script version) clears it forever.

issue #987: a stored "hash" that isn't a well-formed 64-char lowercase sha256 hex digest is
CORRUPTED — this script's own hash_adr/save_checkpoint can never produce one (hashlib's hexdigest
is unconditionally 64 chars; no code path here slices it). `classify` detects and loudly names any
such entry, treating it as unrecorded for that diff rather than silently comparing against
garbage; `advance` always overwrites every entry fresh regardless, so it self-heals once run.
`validate` is a standalone integrity check on an already-written checkpoint file for a write-relay
step to run right after landing one on disk.

issue #1001: `validate` also asserts every stored "status" is one of `{"proposed", "accepted",
"superseded"}` — the exact three-value enum the ADR template's own frontmatter comment states
(`status: proposed        # proposed | accepted | superseded`) and this repo's own ADR-0027 lived
through during its pre-ratification interval; a proposed ADR is checkpointed like any other (see
the checkpoint schema note above). A status outside that set is corrupted data, the same class of
defect #987 already catches for hashes — most concretely, the un-stripped #991-shaped template
comment (`accepted        # proposed | accepted | superseded`) landing IN the stored value because
the frontmatter capture that produced it truncated at a continuation line instead of raising
loudly. `validate` FAILs (exit 1) and names every offending id, rather than silently trusting a
stored status a later `classify` run would compare against as if it were real.

Exit codes: 0 clean · 1 unsupported shape (no ADR parsed from non-empty input) / validate found a
malformed hash or an unknown status · 2 usage error.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

# issue #945: bump this whenever a change to hash_adr/decision_content/amendment_ratification_
# markers changes what bytes a stored hash covers (#929's own widening should have bumped this
# and shipped a migration path — it did neither, which is the bug this constant + the
# formula_mismatch check below fix). A checkpoint with no "formula_version" key predates this
# field entirely and reads as version 1 (the pre-#929 `status + decision_content` formula).
CHECKPOINT_FORMULA_VERSION = 2

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
# issue #1001: a top-level YAML field line — no leading whitespace, `<name>:` then the first
# line's worth of value. Matched per physical line (never re.MULTILINE across the whole block),
# since the continuation rule below depends on testing EACH line's own leading whitespace.
FIELD_START_RE = re.compile(r"^(\S+):\s?(.*)$")
# The three fields this script ever reads out of frontmatter. Captured together by one helper
# (parse_frontmatter_fields) rather than three separate regexes, so `id`/`status` can never drift
# from `supersedes`'s own continuation-aware handling.
FRONTMATTER_FIELD_NAMES = ("id", "status", "supersedes")
# issue #991: a template placeholder inline-comment left on a frontmatter field
# (`status: accepted        # proposed | accepted | superseded`, the un-stripped ADR-authoring
# scaffold text) must never become part of the extracted value. Applied AFTER a field's
# continuation lines (issue #1001) are joined, so a comment trailing the LAST line of a
# multi-line value is stripped the same way a single-line value's comment always was.
TRAILING_COMMENT_RE = re.compile(r"\s+#.*$")
ADR_ID_RE = re.compile(r"adr-\d+")

# issue #987: hash_adr's own hashlib.sha256().hexdigest() is unconditionally 64 lowercase hex
# chars — no code path in this file can ever produce anything shorter. A stored "hash" that
# doesn't match this shape was corrupted OUTSIDE this script (e.g. a lossy transcription in an
# unattended agent's write-relay step, per ops-write-sandbox-rules) and must never be silently
# trusted as a valid prior value.
HASH_RE = re.compile(r"^[0-9a-f]{64}$")

# issue #1001: the exact three-value status enum the ADR template's own frontmatter comment
# states (`status: proposed        # proposed | accepted | superseded`,
# docs/skills/doc-writing-rules/references/templates/adr.md) — a proposed (not-yet-ratified) ADR
# IS checkpointed like any other (see the checkpoint schema note above; this repo's own ADR-0027
# carried "proposed" during its real pre-ratification interval). A stored status outside this set
# is corrupted data, the same class of defect #987 already catches for hashes.
KNOWN_STATUSES = {"proposed", "accepted", "superseded"}

# The second detection signal (issue #221): a forward supersession clause in an accepted ADR's
# own BODY prose, read only when the frontmatter `supersedes:` field is null. Active voice only —
# none of the three accepted verbs ever match their passive form ("superseded by"/"amended by"/
# "replaced by"), same discipline as the table dialect's TABLE_SUPERSEDES_RE below. issue #1715
# widened the verb set beyond literal "supersedes" — free prose that amends or replaces a prior
# ADR without the literal clause was previously invisible to this classifier. The three ratified
# phrasings — `supersedes`, `amends`, `replaces` — are extracted identically; the optional scope
# group (present or absent) is what actually distinguishes a partial edge from a full one, not the
# verb choice. The scope group captures an italicized noun phrase
# between "the" and "of" ("supersedes the *grammar* halves of ADR-0001 and ADR-0006") for a
# PARTIAL supersession; its absence ("supersedes ADR-0002") is a full one. One or more ids may
# follow, joined by "," or "and".
BODY_SUPERSEDES_RE = re.compile(
    r"(?i)\b(?:supersedes|amends|replaces)\b\s+"
    r"(?:the\s+\*(?P<scope>[^*]+)\*\s+\w+\s+of\s+)?"
    r"(?P<ids>ADR-\d+(?:\s*(?:,|and)\s*ADR-\d+)*)"
)

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

# issue #929: an amendment's own ratification-state marker — the ONE line its `## Amendment`
# heading carries the `**proposed** — Kim ratifies` -> `**ratified** — <owner>, [utterance](...),
# verified <date>` flip on (agent-ui's live convention; see ADR-0040/0160/0190's real amendments).
# Matched independently of decision_content's own heading-boundary scan below, so this specific
# signal is a structural, unit-tested guarantee rather than an incidental byproduct of that scan's
# scope — a future narrowing of decision_content (e.g. trimming an amendment down to a booked-
# repairs sub-list) must never silently stop seeing a ratify-only edit.
AMENDMENT_HEADING_LINE_RE = re.compile(r"^## Amendment\b.*$", re.MULTILINE | re.IGNORECASE)

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


def body_supersedes_ids(text):
    """The second detection signal (issue #221, verb set widened by issue #1715): extract forward
    supersession clause(s) from an ADR's own BODY prose — never the frontmatter block, which is
    handled separately by `superseded_ids()`. Recognizes `supersedes`, `amends`, and `replaces` as
    equally valid active-voice verbs. Returns a list of (target_adr_id, scope|None) tuples, one per
    id named in a matched clause: scope is the italicized noun phrase in a partial clause
    ("supersedes the *grammar* halves of ADR-0006" -> ("adr-0006", "grammar")), or None for a bare
    full supersession ("replaces ADR-0002" -> ("adr-0002", None)). Active voice only — "superseded
    by"/"amended by"/"replaced by"/"supersessions" never match. Pure — no I/O."""
    edges = []
    for m in BODY_SUPERSEDES_RE.finditer(text):
        scope = m.group("scope")
        scope = scope.strip() if scope else None
        for tok in ADR_ID_RE.findall(m.group("ids").lower()):
            edges.append((tok, scope))
    return edges


def parse_frontmatter_fields(block):
    """issue #1001: continuation-aware capture of id/status/supersedes out of a raw YAML
    frontmatter block (the text between the `---` fences). Pure — no I/O.

    A YAML plain-scalar value may continue onto following lines that are indented (this
    workspace's own ADR-0020 `supersedes:` field spans six lines this way) — the OLD single-line
    `FIELD_RE` (anchored `^...$` with a non-newline-crossing `(.+?)`) silently truncated at the
    first line break, so only the first target of a multi-target `supersedes:` was ever read.

    The rule mirrors YAML's own plain-scalar folding: a line with NO leading whitespace starts a
    fresh top-level field (whatever comes before its first `:` is the field name — tracked even
    for fields this script doesn't care about, like `ratified:` or `date:`, so an indented
    continuation line under THOSE fields is never mistaken for a value belonging to the
    previously-open id/status/supersedes field). Every following line that DOES start with
    whitespace is a continuation of whichever field is currently open, joined with a single space
    — this is also why a continuation line containing its own `:` (ADR-0020's `ratified:` field
    has one: "...same day: ratify stands...") is never misread as a new field: the leading-
    whitespace check runs before the field-line pattern is ever tried.

    Only once a field's lines are fully joined does the #991 trailing-comment strip run — so a
    comment trailing the LAST line of a multi-line value is stripped exactly like a single-line
    value's comment always was."""
    fields = {}
    current_name, current_parts = None, []

    def flush():
        if current_name in FRONTMATTER_FIELD_NAMES:
            value = " ".join(part for part in current_parts if part).strip()
            fields[current_name] = TRAILING_COMMENT_RE.sub("", value).strip()

    for line in block.splitlines():
        if line and not line[0].isspace():
            flush()
            m = FIELD_START_RE.match(line)
            if m:
                current_name, current_parts = m.group(1).strip().lower(), [m.group(2)]
            else:
                current_name, current_parts = None, []
        elif current_name is not None:
            current_parts.append(line.strip())
    flush()
    return fields


def parse_frontmatter(text):
    """Extract id/status/supersedes from an ADR's frontmatter block. Pure — no I/O."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields = parse_frontmatter_fields(m.group(1))
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


def amendment_ratification_markers(text):
    """issue #929: every `## Amendment` heading LINE in an ADR body, one per amendment section —
    the single line carrying that amendment's ratification-state marker. Pure — no I/O. Returns
    [] for a body with no Amendment section (never spuriously matches the word "amendment" inside
    ordinary prose, since only an actual `##`-level heading line qualifies)."""
    return [m.group(0) for m in AMENDMENT_HEADING_LINE_RE.finditer(text)]


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
    {"id", "hash", "status", "supersedes", "body_supersedes"} or None when neither dialect
    matches. Pure."""
    fm = parse_frontmatter(text)
    if fm and fm["id"]:
        # Whole-file hash, unchanged — existing frontmatter checkpoints stay valid.
        body_supersedes = []
        if fm["supersedes"] is None and fm["status"] == "accepted":
            # The frontmatter field carries no forward declaration — either never set, or (issue
            # #221's live case) permanently null post-acceptance under the T4 append-only hook.
            # The body prose is the only place a ratified clause can ever land, so scan it —
            # everything after the frontmatter block, never the block itself (its own literal
            # `supersedes: null` line must never be mistaken for a body clause).
            fm_match = FRONTMATTER_RE.match(text)
            body_text = text[fm_match.end():] if fm_match else text
            body_supersedes = body_supersedes_ids(body_text)
        return {
            "id": fm["id"],
            "hash": hash_adr(text),
            "status": fm["status"],
            "supersedes": fm["supersedes"],
            "body_supersedes": body_supersedes,
        }
    table = parse_status_table(text)
    if table:
        # Status is folded into the basis: ratification and supersession flip ONLY that one cell,
        # and a status flip that left the hash untouched would never surface as a delta at all.
        # An amendment's own ratification marker(s) are folded in explicitly too (issue #929) —
        # see amendment_ratification_markers's docstring for why this is a dedicated signal rather
        # than relying solely on decision_content's section inclusion.
        markers = "\n".join(amendment_ratification_markers(text))
        return {
            "id": table["id"],
            "hash": hash_adr(table["status"] + "\n" + markers + "\n" + decision_content(text)),
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
    current:        {adr_id: {"hash": str, "status": str, "supersedes": str|None,
                     "body_supersedes": [(str, str|None), ...]}}
    returns:        {"new": [...], "amended": [...], "newly_superseded": [...],
                     "newly_superseded_edges": ["<announcer> -> <target>[ [<scope>]]", ...],
                     "unchanged": [...]}
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
    # PARTIAL/annotated supersession (e.g. "adr-0006 (the frozen-dir clause ... only)", or issue
    # #221's body-clause signal) never flips the target's own status — it stays legitimately
    # "accepted" forever — so there is no persisted signal except "did the announcing ADR's
    # content change since last checkpoint". Deriving from every current record (changed or not)
    # is exactly the bug this guards: once advanced, the announcing ADR becomes unchanged next
    # run, and without this restriction its supersedes claim would be re-read and re-flagged as
    # newly_superseded forever.
    changed_ids = set(new) | set(amended)
    superseded_now = set()
    edges = []  # (announcer_id, target_id, scope|None) — the scope-carrying representation
    for adr_id in changed_ids:
        for target in superseded_ids(current[adr_id].get("supersedes")):
            superseded_now.add(target)
            edges.append((adr_id, target, None))
        for target, scope in current[adr_id].get("body_supersedes", []):
            superseded_now.add(target)
            edges.append((adr_id, target, scope))
    superseded_now |= {adr_id for adr_id in changed_ids if current[adr_id].get("status") == "superseded"}
    newly_superseded = sorted(
        adr_id for adr_id in superseded_now
        if old_checkpoint.get(adr_id, {}).get("status") != "superseded"
    )
    # newly_superseded_edges: one "<announcer> -> <target>[ [<scope>]]" string per (announcer,
    # target) edge whose target actually fired newly_superseded this round — a bare
    # self-status-flip target (no announcer, no edges entry) never appears here since it carries
    # no forward-declaration relationship to represent.
    newly_superseded_edges = sorted(
        "{} -> {}{}".format(announcer, target, " [{}]".format(scope) if scope else "")
        for (announcer, target, scope) in edges
        if target in newly_superseded
    )

    return {
        "new": sorted(new),
        "amended": sorted(amended),
        "newly_superseded_edges": newly_superseded_edges,
        "newly_superseded": newly_superseded,
        "unchanged": sorted(unchanged),
    }


def load_checkpoint(path):
    """Returns (adrs_dict, formula_version). No file yet -> ({}, CHECKPOINT_FORMULA_VERSION) —
    nothing to migrate, so it never reads as a mismatch against a first-ever checkpoint. A file
    with no "formula_version" key predates issue #945's own fix (pre-#929) and reads as version 1,
    never as the current version by silent default — that silent default is exactly the bug."""
    p = Path(path)
    if not p.is_file():
        return {}, CHECKPOINT_FORMULA_VERSION
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("adrs", {}), data.get("formula_version", 1)


def save_checkpoint(path, current):
    Path(path).write_text(
        json.dumps(
            {"formula_version": CHECKPOINT_FORMULA_VERSION, "adrs": current},
            indent=2, sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def formula_mismatch(old_checkpoint, old_formula_version):
    """issue #945: true when a NON-EMPTY existing checkpoint was written under a different hash
    formula version than this script now computes — the signal that stops a hash-basis change
    (like #929's) from reading as a silent 100%-amended flood. An empty checkpoint (first-ever
    run, or a genuinely empty corpus) never mismatches — there is nothing stored to compare
    against, so `new` is the correct and only verdict. Pure."""
    return bool(old_checkpoint) and old_formula_version != CHECKPOINT_FORMULA_VERSION


def malformed_hash_entries(checkpoint):
    """issue #987: adr ids whose stored "hash" isn't a well-formed 64-char lowercase sha256 hex
    digest — corrupted data (e.g. a truncated transcription) that must never be diffed against as
    if it were a real prior value. Pure."""
    return sorted(
        adr_id for adr_id, rec in checkpoint.items()
        if not HASH_RE.match(rec.get("hash", ""))
    )


def bad_status_entries(checkpoint):
    """issue #1001: adr ids whose stored "status" isn't one of KNOWN_STATUSES — corrupted data
    (e.g. the #991-shaped un-stripped template comment landing IN the value because a truncated
    frontmatter capture fed `superseded_ids` and friends only a partial line) that must never be
    trusted by a later `classify` as if it were a real prior status. Pure."""
    return sorted(
        adr_id for adr_id, rec in checkpoint.items()
        if rec.get("status") not in KNOWN_STATUSES
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
            "body_supersedes": rec.get("body_supersedes", []),
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
    silently reading as 'unchanged' forever.

    issue #945: a formula-version mismatch on a non-empty checkpoint short-circuits BEFORE the
    diff — every stored hash would differ from the current formula alone, so a normal delta here
    would be a 100%-amended flood with zero real signal in it, not a smaller report worth
    trusting partially. Reported as its own named event instead."""
    old, old_formula_version = load_checkpoint(checkpoint_path)
    current = scan_source(adr_source)

    print(f"adr_checkpoint classify · {adr_source}")
    malformed = malformed_hash_entries(old)
    if malformed:
        print(
            "  CORRUPTED CHECKPOINT DATA: {} stored hash(es) aren't well-formed 64-char sha256 "
            "digests -> {} (never introduced by this script's own write path — hash_adr's "
            "hexdigest is unconditionally 64 chars; the corruption entered elsewhere, e.g. a "
            "lossy transcription in an unattended write-relay step). Treated as unrecorded for "
            "this diff; `advance` overwrites them with a fresh correct hash regardless.".format(
                len(malformed), ", ".join(malformed)
            )
        )
    if formula_mismatch(old, old_formula_version):
        print(
            f"  FORMULA MISMATCH: checkpoint was written under hash formula v{old_formula_version}, "
            f"this script computes v{CHECKPOINT_FORMULA_VERSION} -> every hash in the checkpoint "
            "differs from the current formula alone, so a diff here would be a false 100%-amended "
            "flood, not a real event"
        )
        print(
            "  this is NOT a report of what changed — re-baseline instead: re-run classify with "
            "the OLD script version to isolate the true delta if one is owed, then `advance` "
            "under THIS version to re-baseline the checkpoint in one clean move"
        )
        print("  checkpoint NOT advanced -> re-baseline via `advance` once ready")
        return 0

    trustworthy_old = {
        adr_id: rec for adr_id, rec in old.items() if adr_id not in malformed
    }
    delta = classify_delta(trustworthy_old, current)

    print(f"  {len(current)} ADR(s) scanned against checkpoint ({len(old)} previously known)")
    for kind in ("new", "amended", "newly_superseded"):
        if delta[kind]:
            print(f"  {kind}: {', '.join(delta[kind])}")
    if delta["newly_superseded_edges"]:
        print(f"  newly_superseded_edges: {', '.join(delta['newly_superseded_edges'])}")
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


def run_validate(checkpoint_path):
    """issue #987 / #1001: a standalone integrity check on an ALREADY-WRITTEN checkpoint file —
    no ADR source needed, since it checks the stored shape only. Meant for a write-relay step
    (e.g. an unattended agent's fenced-payload apply, per ops-write-sandbox-rules) to run
    immediately after landing a checkpoint on disk, catching a corrupted transcription before
    it's trusted rather than after it's silently persisted for cycles. Two independent checks —
    a malformed hash and an unknown status are different corruption shapes, and both are named
    when both fire, not just the first one found."""
    old, _ = load_checkpoint(checkpoint_path)
    malformed = malformed_hash_entries(old)
    bad_status = bad_status_entries(old)
    if malformed or bad_status:
        print(f"adr_checkpoint validate · {checkpoint_path}")
        if malformed:
            print(
                "  FAIL: {} stored hash(es) aren't well-formed 64-char sha256 digests -> {}".format(
                    len(malformed), ", ".join(malformed)
                )
            )
        if bad_status:
            print(
                "  FAIL: {} stored status value(s) aren't one of {} -> {}".format(
                    len(bad_status), sorted(KNOWN_STATUSES), ", ".join(bad_status)
                )
            )
        return 1
    print(
        f"adr_checkpoint validate · {checkpoint_path} · {len(old)} ADR(s) · "
        "all hashes well-formed, all statuses known"
    )
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

    # issue #991: a template placeholder inline-comment left on the `status:` line (this
    # workspace's own adr-0027, un-stripped ADR-authoring scaffold text) must never leak into the
    # extracted value — positive control is the exact live corrupted shape.
    fm3 = parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0027\n"
        "status: accepted        # proposed | accepted | superseded\n"
        "supersedes: null\n---\n# body"
    )
    assert fm3["status"] == "accepted", fm3
    # a comment on `id:`/`supersedes:` is stripped the same way — one regex, three fields
    fm4 = parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0028   # numbering scratchpad\n"
        "status: accepted\nsupersedes: adr-0002   # the old one\n---\n# body"
    )
    assert fm4 == {"id": "adr-0028", "status": "accepted", "supersedes": "adr-0002"}, fm4
    # negative control: a field with no comment at all is unaffected (no over-trimming)
    assert parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0029\nstatus: proposed\nsupersedes: null\n---\n# body"
    )["status"] == "proposed"

    # negative control: a single-line value (no continuation) parses identically to before the
    # issue #1001 fix — proves continuation-awareness didn't touch the already-working common case
    assert parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0030\nstatus: accepted\nsupersedes: adr-0004\n---\n# body"
    ) == {"id": "adr-0030", "status": "accepted", "supersedes": "adr-0004"}

    # issue #1001: continuation-aware frontmatter field capture — ADR-0020's own REAL frontmatter
    # (`.claude/docs/adr/0020-fleet-vocabulary-and-binding-heads.md`) as the MANDATORY positive
    # control. Its `ratified:` field continues across four lines and its own continuation text
    # contains a colon ("...tie-break by Kim same day: ratify stands...") that must never be
    # misread as a new field start; its `supersedes:` field continues across six lines and names
    # FOUR superseded ids (adr-0015, adr-0016, adr-0017, adr-0011) — the OLD FIELD_RE truncated
    # this to just adr-0015, the exact bug this fix closes. `id`/`status` must come through
    # unaffected by the continuation lines above and below them.
    adr_0020_frontmatter_block = (
        "doc-type: adr\n"
        "id: adr-0020\n"
        "status: accepted\n"
        "ratified: rejected 2026-08-17T16:03Z (live, drain session) / ratified 16:04Z (live\n"
        "  AskUserQuestion) / tie-break by Kim same day: ratify stands — see #518. Drafted 2026-08-17\n"
        "  from Kim's live AskUserQuestion answers in a Cowork session; D5 ruled by Kim in a second\n"
        "  AskUserQuestion round the same day (merge).\n"
        "date: 2026-08-17\n"
        "owner: kim.granlund\n"
        "supersedes: adr-0015 (D1's role production insofar as RoleLex membership is closed to the\n"
        "  coordinative three — the {scope}-{role} production itself stands unamended); adr-0016\n"
        "  (D1 and D2 in full — the reserved `lead-` command head and its scope-resolution clause;\n"
        "  D4's fence stands); adr-0017 (the RoleLex sizing posture only — its 10 execution-seat\n"
        "  additions stand unamended); adr-0011 (D7's command production, already partially superseded\n"
        "  by adr-0016, now superseded again by the three-head scheme in D3)\n"
        "intent-refs: idr-0003    # same naming-grammar chain, the RoleLex/command-head reconciliation"
    )
    fm_0020 = parse_frontmatter("---\n" + adr_0020_frontmatter_block + "\n---\n# body")
    assert fm_0020["id"] == "adr-0020", fm_0020
    assert fm_0020["status"] == "accepted", fm_0020
    assert superseded_ids(fm_0020["supersedes"]) == \
        ["adr-0015", "adr-0016", "adr-0017", "adr-0011", "adr-0016"], fm_0020["supersedes"]
    assert set(superseded_ids(fm_0020["supersedes"])) == \
        {"adr-0015", "adr-0016", "adr-0017", "adr-0011"}, fm_0020["supersedes"]

    # a continuation line that ALSO ends in a `# comment` — both behaviors (issue #1001's
    # multi-line join and #991's trailing-comment strip) must compose, not just each work alone
    fm_continuation_and_comment = parse_frontmatter(
        "---\ndoc-type: adr\nid: adr-0031\nstatus: accepted\n"
        "supersedes: adr-0002 (first target continues here\n"
        "  onto a second line) and adr-0003   # trailing scratch note\n"
        "---\n# body"
    )
    assert fm_continuation_and_comment["supersedes"] == \
        "adr-0002 (first target continues here onto a second line) and adr-0003", \
        fm_continuation_and_comment
    assert superseded_ids(fm_continuation_and_comment["supersedes"]) == ["adr-0002", "adr-0003"]

    # body_supersedes_ids — the second detection signal (issue #221): ADR-0011's own REAL body
    # text (frontmatter `supersedes: null`, permanently frozen post-acceptance under the T4
    # append-only hook) as the MANDATORY positive control — a forward clause naming a partial
    # supersession over two targets, sharing one scope.
    adr_0011_text = (
        "---\n"
        "doc-type: adr\n"
        "id: adr-0011\n"
        "status: accepted\n"
        "ratified: by Kim, 2026-08-13 (in-session, session \"PLUGINS\")\n"
        "date: 2026-08-13\n"
        "owner: kim.granlund\n"
        "supersedes: null\n"
        "---\n"
        "# ADR-0011 — Adopt the harness naming-convention spec as estate-wide naming canon\n\n"
        "> ACCEPTED — ratified by Kim 2026-08-13. Originally a live conversation capture "
        "(session \"PLAN\", 2026-08-13). The headline\n"
        "> ruling (D7) was made in-session by Kim and REVERSES this session's own earlier\n"
        "> rulings (recorded in Context for the audit trail). All open rulings were closed\n"
        "> in-session 2026-08-13; nothing in this ADR awaits a decision — only acceptance.\n"
        "> On acceptance this ADR supersedes the *grammar* halves of ADR-0001 and ADR-0006;\n"
        "> their enforcement discipline (symmetry, lint gates) carries forward.\n"
    )
    adr_0011_rec = parse_adr_file(adr_0011_text)
    assert adr_0011_rec["id"] == "adr-0011", adr_0011_rec
    assert adr_0011_rec["supersedes"] is None, \
        "ADR-0011's frontmatter field is permanently null — the T4 hook's own live constraint"
    assert adr_0011_rec["body_supersedes"] == [("adr-0001", "grammar"), ("adr-0006", "grammar")], \
        adr_0011_rec["body_supersedes"]

    # end-to-end: ADR-0011 (new/amended this round) fires newly_superseded for BOTH targets, with
    # scope carried through as a dedicated edge string, never collapsed to a bare id
    old_pre_0011 = {
        "adr-0001": {"hash": "h1", "status": "accepted"},
        "adr-0006": {"hash": "h6", "status": "accepted"},
    }
    current_0011 = {
        "adr-0001": {"hash": "h1", "status": "accepted", "supersedes": None, "body_supersedes": []},
        "adr-0006": {"hash": "h6", "status": "accepted", "supersedes": None, "body_supersedes": []},
        "adr-0011": {
            "hash": adr_0011_rec["hash"], "status": "accepted",
            "supersedes": None, "body_supersedes": adr_0011_rec["body_supersedes"],
        },
    }
    d_0011 = classify_delta(old_pre_0011, current_0011)
    assert d_0011["new"] == ["adr-0011"], d_0011
    assert d_0011["newly_superseded"] == ["adr-0001", "adr-0006"], d_0011
    assert d_0011["newly_superseded_edges"] == [
        "adr-0011 -> adr-0001 [grammar]", "adr-0011 -> adr-0006 [grammar]",
    ], d_0011["newly_superseded_edges"]

    # MANDATORY negative control: an ACCEPTED ADR with frontmatter `supersedes: null` and NO
    # supersession clause anywhere in its body must never fire — proves the second signal doesn't
    # spuriously invent an edge out of ordinary prose that merely discusses other ADRs
    adr_no_clause_text = (
        "---\ndoc-type: adr\nid: adr-0012\nstatus: accepted\nsupersedes: null\n---\n"
        "# ADR-0012 — An unrelated ratified decision\n\n"
        "## Context\n\nThis ADR relates to ADR-0006 and extends ADR-0002, but never supersedes "
        "anything — it only cites them for background.\n\n"
        "## Decision\n\nAdopt the new convention going forward.\n"
    )
    adr_no_clause_rec = parse_adr_file(adr_no_clause_text)
    assert adr_no_clause_rec["supersedes"] is None, adr_no_clause_rec
    assert adr_no_clause_rec["body_supersedes"] == [], \
        f"an accepted ADR with no supersession clause must never fire: {adr_no_clause_rec}"

    # a PROPOSED (not yet accepted) ADR whose body drafts a future supersession must NOT fire —
    # only a ratified Decision is a real supersession; the gate is `status: accepted`, not merely
    # the presence of a matching clause in prose
    adr_proposed_text = (
        "---\ndoc-type: adr\nid: adr-0013\nstatus: proposed\nsupersedes: null\n---\n"
        "# ADR-0013 — A draft still under discussion\n\n"
        "This draft, once ratified, supersedes ADR-0007 in full.\n"
    )
    adr_proposed_rec = parse_adr_file(adr_proposed_text)
    assert adr_proposed_rec["body_supersedes"] == [], \
        f"a non-accepted ADR's body clause must never fire: {adr_proposed_rec}"

    # a bare full supersession (no italicized scope) must extract with scope=None
    assert body_supersedes_ids("This supersedes ADR-0002 outright.") == [("adr-0002", None)]

    # active-voice-only control, same discipline as the table dialect: "superseded by"/
    # "supersessions" must never match
    assert body_supersedes_ids("This was superseded by ADR-0009.") == []
    assert body_supersedes_ids("No supersessions occurred here.") == []

    # issue #1715 — widened verb set: "amends" and "replaces" extract identically to "supersedes"
    assert body_supersedes_ids("This amends ADR-0037 in part.") == [("adr-0037", None)]
    assert body_supersedes_ids("This replaces ADR-0002 outright.") == [("adr-0002", None)]
    assert body_supersedes_ids(
        "This amends the *sizing* axis of ADR-0037."
    ) == [("adr-0037", "sizing")]

    # active-voice-only control for the two new verbs — passive forms must never match
    assert body_supersedes_ids("This was amended by ADR-0040.") == []
    assert body_supersedes_ids("This was replaced by ADR-0009.") == []

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

    # ---- issue #929: amendment ratification-marker hashing --------------------------------------
    # amendment_ratification_markers — positive: each `## Amendment` heading line is extracted
    # verbatim, one per amendment, real agent-ui marker shape (`**proposed** — Kim ratifies`)
    draft_amendment_adr = table_adr + (
        "\n## Amendment (2026-08-20, **proposed** — Kim ratifies) — a second, unrelated amendment\n\n"
        "> Some amendment prose that never changes on ratification.\n"
    )
    markers_before = amendment_ratification_markers(draft_amendment_adr)
    assert markers_before == [
        "## Amendment (2026-08-20, **proposed** — Kim ratifies) — a second, unrelated amendment"
    ], markers_before

    # negative control: an ADR with no `## Amendment` heading at all extracts nothing
    assert amendment_ratification_markers(table_adr) == [], \
        "an ADR with no Amendment section must extract no ratification markers"

    # negative control: the word "amendment" inside ordinary body prose (never a `##` heading)
    # must never be mistaken for a marker line
    prose_only = table_adr.replace(
        "Every dispatch is validated against the declared schema.",
        "Every dispatch is validated against the declared schema; a future amendment may revisit "
        "this.",
    )
    assert amendment_ratification_markers(prose_only) == [], \
        "the word 'amendment' inside ordinary prose must never be read as a marker line"

    # end-to-end, the real-world case this issue exists for (agent-ui ADR-0040/ADR-0160/ADR-0190,
    # GH #1009/#1032/#1030): a ratify-only flip — the marker text changes, the amendment's own
    # prose and every other section stay byte-identical, and the ADR's Status cell stays
    # `accepted` throughout (it already was) — must still move the hash.
    ratified_amendment_adr = draft_amendment_adr.replace(
        "## Amendment (2026-08-20, **proposed** — Kim ratifies) — a second, unrelated amendment",
        "## Amendment (2026-08-20, **ratified** — kimgranlund, "
        "[utterance](https://github.com/kimgranlund/agent-ui/pull/1#issuecomment-1), "
        "verified 2026-08-21) — a second, unrelated amendment",
    )
    markers_after = amendment_ratification_markers(ratified_amendment_adr)
    assert markers_before != markers_after, "the marker line itself must change text on ratify"

    draft_rec = parse_adr_file(draft_amendment_adr)
    ratified_rec = parse_adr_file(ratified_amendment_adr)
    assert draft_rec["status"] == ratified_rec["status"] == "accepted", (draft_rec, ratified_rec)
    assert draft_rec["hash"] != ratified_rec["hash"], (
        "a ratify-only marker flip (issue #929) must move the hash even though the amendment's "
        "own prose, the Decision section, and the Status cell are all byte-identical"
    )
    # reverse control: strip the two heading lines from both texts before diffing — everything
    # ELSE (Context, Decision, Consequences, and the amendment's own prose below its heading) is
    # provably byte-identical, isolating the marker line as the only thing that moved the hash
    without_marker_line = lambda adr_text: "\n".join(
        line for line in adr_text.splitlines() if not line.startswith("## Amendment")
    )
    assert without_marker_line(draft_amendment_adr) == without_marker_line(ratified_amendment_adr), \
        "only the Amendment heading's own marker line may differ between the draft and ratified texts"

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

    # ---- issue #945: checkpoint formula-version detection, the false-flood fix ------------------
    # formula_mismatch, pure — the unit the end-to-end test below exercises through the CLI path
    assert formula_mismatch({}, 1) is False, "an empty checkpoint (first-ever run) never mismatches"
    assert formula_mismatch({"adr-0001": {"hash": "h", "status": "accepted"}}, 1) is True, \
        "a non-empty checkpoint at v1 must mismatch against the current v{}".format(
            CHECKPOINT_FORMULA_VERSION
        )
    assert formula_mismatch(
        {"adr-0001": {"hash": "h", "status": "accepted"}}, CHECKPOINT_FORMULA_VERSION
    ) is False, "a checkpoint already at the current formula version must never mismatch"

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        checkpoint_path = d / "adr-checkpoint.json"

        # no checkpoint file at all -> ({}, CURRENT), never a mismatch (nothing to migrate)
        assert load_checkpoint(checkpoint_path) == ({}, CHECKPOINT_FORMULA_VERSION)

        # a checkpoint written with NO "formula_version" key (the real pre-#945 shape every
        # checkpoint on disk today carries, since the field never existed before this fix) must
        # read back as version 1, never silently default to the current version — a silent
        # default to "current" is exactly the bug (every stored hash would then compare as if it
        # were computed under today's formula, when it was not).
        checkpoint_path.write_text(
            json.dumps({"adrs": {"adr-0001": {"hash": "legacy-hash", "status": "accepted"}}}),
            encoding="utf-8",
        )
        legacy_adrs, legacy_version = load_checkpoint(checkpoint_path)
        assert legacy_version == 1, legacy_version
        assert legacy_adrs == {"adr-0001": {"hash": "legacy-hash", "status": "accepted"}}

        # save_checkpoint always stamps the CURRENT formula version — round-trips clean, no
        # mismatch against itself
        save_checkpoint(checkpoint_path, {"adr-0001": {"hash": "h1", "status": "accepted"}})
        fresh_adrs, fresh_version = load_checkpoint(checkpoint_path)
        assert fresh_version == CHECKPOINT_FORMULA_VERSION, fresh_version
        assert formula_mismatch(fresh_adrs, fresh_version) is False

        # end-to-end, via the actual CLI entry point: a legacy (no formula_version key) checkpoint
        # against TRULY UNCHANGED content must report FORMULA MISMATCH, never a false 100%-amended
        # flood — this is the exact issue #945 repro (#929's hash-basis widening against an old
        # checkpoint), reproduced with a real table-dialect ADR so the widened hash basis
        # (status + markers + decision_content) is actually the mechanism under test, not a stand-in.
        adr_source_dir = d / "adrs"
        adr_source_dir.mkdir()
        unchanged_adr_text = (
            "# ADR-0100 — Unrelated ratified decision\n\n"
            "> | **Status** | accepted |\n\n"
            "## Decision\n\nSome decision text, never edited between the two checkpoint runs.\n"
        )
        (adr_source_dir / "0100-unchanged.md").write_text(unchanged_adr_text, encoding="utf-8")
        current_scan = scan_dir(adr_source_dir)
        # the OLD (pre-#929) formula for this dialect: status + decision_content, no markers —
        # deliberately NOT recomputed via today's hash_adr/decision_content composition, since the
        # whole point is a checkpoint whose hash basis predates the current script
        old_formula_hash = hash_adr(
            current_scan["adr-0100"]["status"] + "\n" + decision_content(unchanged_adr_text)
        )
        legacy_checkpoint_path = d / "legacy-checkpoint.json"
        legacy_checkpoint_path.write_text(
            json.dumps({"adrs": {"adr-0100": {"hash": old_formula_hash, "status": "accepted"}}}),
            encoding="utf-8",
        )
        import contextlib
        import io

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            rc = run_classify(str(adr_source_dir), str(legacy_checkpoint_path))
        out = captured.getvalue()
        assert rc == 0, rc
        assert "FORMULA MISMATCH" in out, out
        assert "amended:" not in out, \
            "a formula mismatch must never also print a (false) amended list: {}".format(out)
        # NOT advanced — the file on disk is untouched (still the legacy, no-formula-version shape)
        assert json.loads(legacy_checkpoint_path.read_text()).get("formula_version") is None

        # negative control: a checkpoint already at the CURRENT formula, same unchanged content,
        # must classify normally — no mismatch banner, no false amended entry either
        current_checkpoint_path = d / "current-checkpoint.json"
        save_checkpoint(current_checkpoint_path, {
            "adr-0100": {"hash": current_scan["adr-0100"]["hash"], "status": "accepted"}
        })
        captured2 = io.StringIO()
        with contextlib.redirect_stdout(captured2):
            rc2 = run_classify(str(adr_source_dir), str(current_checkpoint_path))
        out2 = captured2.getvalue()
        assert rc2 == 0, rc2
        assert "FORMULA MISMATCH" not in out2, out2
        assert "amended:" not in out2, \
            "unchanged content against a same-formula checkpoint must never read as amended: {}".format(out2)

        # issue #987: malformed_hash_entries unit-level — a truncated 57-char hash (the exact
        # repro shape) flags, a well-formed 64-char one never does
        assert malformed_hash_entries({
            "adr-0065": {"hash": "a" * 57, "status": "accepted"},
            "adr-0001": {"hash": "b" * 64, "status": "accepted"},
        }) == ["adr-0065"]
        assert malformed_hash_entries({}) == []

        # end-to-end via run_classify: a checkpoint carrying one corrupted (57-char) hash
        # alongside one genuinely well-formed entry must name the corrupted id loudly, never
        # silently diff it as a false "amended" — and must NOT block the real delta for the
        # sibling well-formed entry
        corrupt_checkpoint_path = d / "corrupt-checkpoint.json"
        save_checkpoint(corrupt_checkpoint_path, {
            "adr-0100": {"hash": "e" * 57, "status": "accepted"},
        })
        captured3 = io.StringIO()
        with contextlib.redirect_stdout(captured3):
            rc3 = run_classify(str(adr_source_dir), str(corrupt_checkpoint_path))
        out3 = captured3.getvalue()
        assert rc3 == 0, rc3
        assert "CORRUPTED CHECKPOINT DATA" in out3, out3
        assert "adr-0100" in out3, out3
        assert "FORMULA MISMATCH" not in out3, \
            "a malformed hash alone is not a formula mismatch: {}".format(out3)
        # treated as unrecorded, not a false "amended" against garbage
        assert "new: adr-0100" in out3, out3
        assert "amended: adr-0100" not in out3, out3
        # never advanced by classify — same untouched-on-classify contract as every other path
        assert json.loads(corrupt_checkpoint_path.read_text())["adrs"]["adr-0100"]["hash"] == "e" * 57

        # run_validate: FAIL + exit 1 on the same corrupted file, naming the bad id
        captured4 = io.StringIO()
        with contextlib.redirect_stdout(captured4):
            rc4 = run_validate(str(corrupt_checkpoint_path))
        out4 = captured4.getvalue()
        assert rc4 == 1, rc4
        assert "FAIL" in out4 and "adr-0100" in out4, out4

        # run_validate: clean PASS + exit 0 on a well-formed checkpoint
        clean_checkpoint_path = d / "clean-checkpoint.json"
        save_checkpoint(clean_checkpoint_path, {
            "adr-0100": {"hash": current_scan["adr-0100"]["hash"], "status": "accepted"}
        })
        captured5 = io.StringIO()
        with contextlib.redirect_stdout(captured5):
            rc5 = run_validate(str(clean_checkpoint_path))
        out5 = captured5.getvalue()
        assert rc5 == 0, rc5
        assert "FAIL" not in out5, out5

        # advance always self-heals a corrupted checkpoint — it recomputes every entry fresh
        # from source, never merges the old (possibly corrupted) stored value
        captured6 = io.StringIO()
        with contextlib.redirect_stdout(captured6):
            rc6 = run_advance(str(adr_source_dir), str(corrupt_checkpoint_path))
        assert rc6 == 0, captured6.getvalue()
        healed = json.loads(corrupt_checkpoint_path.read_text())["adrs"]["adr-0100"]["hash"]
        assert HASH_RE.match(healed), healed

        # issue #1001: bad_status_entries unit-level — the #991-shaped un-stripped template
        # comment landing IN the stored status (the exact corruption the old truncating FIELD_RE
        # could produce) flags; all three known values (including "proposed" — a not-yet-ratified
        # ADR is checkpointed like any other, per the ADR template's own three-value enum and
        # ADR-0027's real pre-ratification interval) never do
        assert bad_status_entries({
            "adr-0001": {"status": "accepted"},
            "adr-0002": {"status": "superseded"},
            "adr-0003": {"status": "proposed"},
            "adr-0004": {"status": "accepted        # proposed | accepted | superseded"},
            "adr-0005": {"status": "rejected"},
        }) == ["adr-0004", "adr-0005"]
        assert bad_status_entries({}) == []

        # end-to-end via run_validate: a checkpoint carrying one corrupted status must FAIL loudly
        # (exit 1), naming the offending id — never silently pass a value a later `classify` run
        # would then trust as a real prior status
        bad_status_checkpoint_path = d / "bad-status-checkpoint.json"
        bad_status_checkpoint_path.write_text(
            json.dumps({
                "formula_version": CHECKPOINT_FORMULA_VERSION,
                "adrs": {
                    "adr-0027": {
                        "hash": "a" * 64,
                        "status": "accepted        # proposed | accepted | superseded",
                    },
                },
            }),
            encoding="utf-8",
        )
        captured7 = io.StringIO()
        with contextlib.redirect_stdout(captured7):
            rc7 = run_validate(str(bad_status_checkpoint_path))
        out7 = captured7.getvalue()
        assert rc7 == 1, rc7
        assert "FAIL" in out7 and "adr-0027" in out7, out7

        # negative control: a checkpoint with only known statuses passes clean (exit 0, no FAIL) —
        # "proposed" included, since a not-yet-ratified ADR is a legitimately checkpointed status
        good_status_checkpoint_path = d / "good-status-checkpoint.json"
        save_checkpoint(good_status_checkpoint_path, {
            "adr-0001": {"hash": "b" * 64, "status": "accepted"},
            "adr-0002": {"hash": "c" * 64, "status": "superseded"},
            "adr-0003": {"hash": "d" * 64, "status": "proposed"},
        })
        captured8 = io.StringIO()
        with contextlib.redirect_stdout(captured8):
            rc8 = run_validate(str(good_status_checkpoint_path))
        out8 = captured8.getvalue()
        assert rc8 == 0, rc8
        assert "FAIL" not in out8, out8

    print("adr_checkpoint selftest · PASS · body-clause supersession signal (issue #221: ADR-0011's "
          "real body text as positive control, scope-carrying edges, accepted-with-no-clause and "
          "proposed-ADR negative controls, active-voice-only), frontmatter parse, hashing, all "
          "four delta shapes, "
          "annotated-supersedes extraction (incl. already-recorded-supersession, corpus-size, "
          "no-adr-token, and post-advance forever-refire negative controls), single-file "
          "section parsing (self-status, forward-supersedes, complements-is-not-supersedes, "
          "no section bleed), the H1+status-table dialect (bare-keyword status, "
          "escaped-pipe cells, active-voice-only supersedes vs Extends/Relates/Amended-by/"
          "Superseded-by + its own row label, Decision-scoped hash with status folded in, "
          "section-less fallback, template/README skipped by shape), the H1+bold-metadata "
          "dialect (either colon placement, non-numeric supersedes ids resolving to nothing, "
          "whole-file hash basis, no cross-match with the table dialect), a three-dialect mixed "
          "directory, the loud 0-parsed unsupported-shape failure vs an empty corpus, and the "
          "issue #929 amendment ratification-marker signal (heading-line extraction, no-Amendment "
          "and prose-mention negative controls, a ratify-only marker flip moving the hash with "
          "every other byte provably unchanged), and the issue #945 checkpoint formula-version "
          "signal (formula_mismatch's own empty/legacy/current-version cases, load_checkpoint's "
          "no-file and no-formula_version-key defaults, save_checkpoint's stamp round-trip, and "
          "end-to-end via run_classify: a legacy no-formula_version checkpoint against truly "
          "unchanged content prints FORMULA MISMATCH with no false amended list and leaves the "
          "checkpoint unadvanced, vs. a same-formula checkpoint classifying normally with neither)), "
          "and the issue #987 corrupted-hash signal (malformed_hash_entries' 57-char-vs-64-char "
          "unit cases, end-to-end via run_classify: a corrupted entry prints CORRUPTED CHECKPOINT "
          "DATA and is treated as unrecorded [new, never a false amended] without blocking a "
          "sibling well-formed entry's real delta, run_validate's FAIL/PASS cases on a corrupted "
          "vs. clean checkpoint file, and advance's unconditional self-heal of a corrupted entry)), "
          "and the issue #991 comment-unaware-FIELD_RE signal (a template placeholder inline-"
          "comment on status: stripped to the bare value — adr-0027's own live shape as positive "
          "control — the same strip on id:/supersedes:, and a no-comment field left untouched), "
          "and the issue #1001 signals (continuation-aware frontmatter capture: ADR-0020's own "
          "real multi-line ratified:/supersedes: shape extracting all four superseded ids with "
          "id:/status: unaffected, a mid-continuation colon never misread as a new field, a "
          "continuation line that also ends in a #991 trailing comment, and a single-line value "
          "unchanged; plus bad_status_entries' unit cases and run_validate's FAIL/PASS on a "
          "corrupted-vs-known status checkpoint)")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "selftest":
        sys.exit(selftest())
    if len(argv) == 2 and argv[0] == "validate":
        sys.exit(run_validate(argv[1]))
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
