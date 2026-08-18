#!/usr/bin/env python3
"""revalidation_checkpoint — sampled, round-robin re-test of accepted doctrine (idr-0009 / #623).

Usage:
  revalidation_checkpoint.py sample <adr-source> <idr-source> <rdd-source> [--checkpoint <path>] [--n N]
      report the next N claims due for re-test; never writes the checkpoint
  revalidation_checkpoint.py advance <adr-source> <idr-source> <rdd-source> [--checkpoint <path>] --n N
      persist the cursor bump — run ONLY after the N claims `sample` reported have been judged
  revalidation_checkpoint.py queue-add <path> --claim <id> --kind falsified|untestable
      --evidence <text> --owner <name>
      queue a re-validation finding (idempotent by claim+kind), against a scratch copy of the queue
  revalidation_checkpoint.py queue-pending <path>       list every unresolved candidate
  revalidation_checkpoint.py queue-clear <path> --ids <id[:kind],...>
      drop resolved candidates after a batch confirm (bare id clears every kind; "id:kind" precise)
  revalidation_checkpoint.py selftest                   prove sampling, extraction, and the queue

This is a MODE on the existing decision-watcher/watch-adrs machinery (idr-0007's job-evidence test:
no named gap justifies a sibling seat), not a new seat — see harness/skills/watch-adrs/SKILL.md's
"Revalidation mode" section for the full per-firing procedure this script is the substrate for, and
.claude/docs/lld/lld-0016-doctrine-revalidation-mode.md for the design resolutions. The economic
contract mirrors adr_checkpoint.py's classify/advance split (a crash between sample and advance
leaves the cursor untouched, so the same claims are re-sampled next firing rather than silently
skipped) and adr_queue.py's add/pending/clear pattern (a scheduled firing never blocks on a live
human; a candidate lands here until a batched confirm resolves it).

**Claim corpus, three kinds, sampled together (locked RDDs joined the rotation per #656/#655
decision 7 — the ADR+IDR sampling pool from here on always means ADR+IDR+RDD):**
- Every ADR whose live status is `accepted` — claim text is the WHOLE `## Decision` (+
  `## Amendment*` / `## Supersession*`) section, reusing `adr_checkpoint.decision_content()`
  verbatim (dialect-generic: frontmatter, H1+blockquote-table, H1+bold-metadata all work unchanged).
- Every IDR whose live status is `locked` — claim text is the WHOLE `## Proof` section, never a
  regex-anchored "Falsifies:" clause. This was tried first and falsified against the real corpus
  during authoring: idr-0009/idr-0011 read "Falsifies: ...", idr-0006 reads "Falsifies on the first
  review...", idr-0007/idr-0008 bury it mid-sentence, and idr-0001 never uses the word "Falsifies"
  at all ("falsified by a ledger entry...", passive voice). A keyword extractor would miss idr-0001
  outright; the whole Proof section costs nothing extra and hands judgment the Confirms condition
  for free (needed anyway to reason about the untestable branch).
- Every RDD whose live status is `locked` — claim text is the WHOLE `## Acceptance` section, RDD's
  own IDR-grammar criteria and the type's Proof-equivalent (`doc-writing-rules`' RDD template: "each
  phrased as a testable claim that could fail... mirrors IDR's own `## Claim` discipline"). Same
  whole-section extraction as the IDR resolution above, for the same reason — a criteria line's own
  phrasing varies claim to claim, so a narrower keyword anchor would be exactly as fragile here as
  the falsified "Falsifies:"-anchored extractor was for IDR. PRD/SPEC staleness is deliberately
  OUT OF SCOPE for this mode — it stays de-staling's job (#655 decision 7); this mode's own tri-state
  verdict machinery is otherwise unchanged by adding the third kind.

**Sampling: round-robin over a lexicographically sorted, combined id list**, one persisted integer
cursor. The ADR/IDR/RDD corpora are append-only under this workspace's own T4 discipline (an
accepted ADR's frontmatter never changes post-ratification; a locked IDR or locked RDD is
append-only), so the sorted list only grows at its tail (or narrows slightly when an ADR is
superseded) — round-robin handles a growing, mostly-stable corpus without needing to special-case
"new" vs. "old" claims the way the forward classifier does. `sample --n N` never duplicates a claim within one call, even when N
exceeds the corpus size (it caps at corpus size). Cadence (how often `sample` should be invoked) is
explicitly out of this script's scope — idr-0011 owns it, still open at gh#626.

**Verdict routing, realized as data, never executed by this script:** `confirmed` is reported and
dropped (no queue growth — keeping repeated-confirmed sweeps cheap is itself part of idr-0009's own
falsification test). `falsified`/`untestable` queue via `queue-add`, always carrying a named
`--owner` (idr-0009's own "who executes a falsified verdict" open question, closed structurally: the
field exists on every row). This script never files a GitHub Issue, never edits a locked IDR, a locked RDD, or an
accepted ADR, and never decides a verdict itself — verdicts are a judgment step's output, handed to
this script only to be queued.

Exit codes: 0 clean · 1 a named ADR/IDR/RDD source path doesn't exist or isn't a directory · 2 usage error.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adr_checkpoint import (  # noqa: E402  (sibling script, same harness/scripts/ directory)
    FRONTMATTER_RE,
    HEADING_RE,
    decision_content,
    parse_bold_metadata,
    parse_frontmatter,
    parse_status_table,
)

DOC_FIELD_RE = re.compile(r"^(doc-type|id|status)\s*:\s*(.+?)\s*$", re.MULTILINE)
# Reused by both parse_idr_frontmatter and parse_rdd_frontmatter below — the same three scalar
# fields, gated per-caller on the doc-type value each expects (never a shared parse of both kinds).


class SourceUnreadable(Exception):
    """A named ADR/IDR/RDD source path doesn't exist or isn't a directory — never a silent empty scan."""


def extract_section(text, prefix):
    """The generic heading-bounded-section extractor Resolution 3 is built on: return the first
    `## ...` section whose heading (lowercased, stripped of markup) starts with `prefix`, bounded to
    the next `##` heading of ANY kind or EOF — same bounding discipline as
    `adr_checkpoint.decision_content()`. Returns None when no matching heading exists (unlike
    `decision_content`'s whole-text fallback: a missing `## Proof` section on an IDR is itself a
    defect worth surfacing as empty text, not papered over with an unrelated fallback). Pure."""
    bounds = [m.start() for m in HEADING_RE.finditer(text)] + [len(text)]
    for start, end in zip(bounds, bounds[1:]):
        section = text[start:end]
        heading = section.splitlines()[0][2:].strip().strip("*`# ").lower()
        if heading.startswith(prefix):
            return section
    return None


def parse_idr_frontmatter(text):
    """Extract id/status from an IDR's frontmatter, gated on `doc-type: idr` — an ADR file (same
    frontmatter shape, `doc-type: adr`) must never be misread as an IDR. Pure."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields = dict(DOC_FIELD_RE.findall(m.group(1)))
    if fields.get("doc-type", "").strip() != "idr":
        return None
    return {"id": fields.get("id", "").strip(), "status": fields.get("status", "").strip()}


def parse_idr_file(text):
    """Parse one IDR file: id/status from frontmatter, claim text from the whole `## Proof` section
    (Resolution 3 — never a narrower keyword extraction). Returns None for a non-IDR file. Pure."""
    fm = parse_idr_frontmatter(text)
    if not fm or not fm["id"]:
        return None
    return {"id": fm["id"], "status": fm["status"], "proof_text": extract_section(text, "proof") or ""}


def parse_rdd_frontmatter(text):
    """Extract id/status from an RDD's frontmatter, gated on `doc-type: rdd` — an ADR/IDR file
    (same frontmatter shape) must never be misread as an RDD. Pure."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields = dict(DOC_FIELD_RE.findall(m.group(1)))
    if fields.get("doc-type", "").strip() != "rdd":
        return None
    return {"id": fields.get("id", "").strip(), "status": fields.get("status", "").strip()}


def parse_rdd_file(text):
    """Parse one RDD file: id/status from frontmatter, claim text from the whole `## Acceptance`
    section — RDD's own IDR-grammar criteria, the type's Proof-equivalent (same whole-section
    extraction discipline as parse_idr_file's Resolution 3, applied to Acceptance instead of Proof).
    Returns None for a non-RDD file. Pure."""
    fm = parse_rdd_frontmatter(text)
    if not fm or not fm["id"]:
        return None
    return {
        "id": fm["id"], "status": fm["status"],
        "acceptance_text": extract_section(text, "acceptance") or "",
    }


def scan_adr_claims(adr_dir):
    """Every ACCEPTED ADR in adr_dir -> {adr_id: {"kind": "adr-decision", "text", "source"}}. Tries
    all three dialects `adr_checkpoint` already supports, frontmatter first, same order as
    `parse_adr_file` — but unlike that function, this one needs the RAW file text too (to run
    `decision_content` over it), so it re-derives id/status per dialect directly rather than reusing
    `parse_adr_file`'s already-hashed record shape."""
    claims = {}
    for f in sorted(Path(adr_dir).glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if fm and fm["id"]:
            adr_id, status = fm["id"], fm["status"]
        else:
            table = parse_status_table(text)
            if table:
                adr_id, status = table["id"], table["status"]
            else:
                bold = parse_bold_metadata(text)
                if not bold:
                    continue
                adr_id, status = bold["id"], bold["status"]
        if status != "accepted":
            continue
        claims[adr_id] = {
            "kind": "adr-decision", "text": decision_content(text), "source": str(f),
        }
    return claims


def scan_idr_claims(idr_dir):
    """Every LOCKED IDR in idr_dir -> {idr_id: {"kind": "idr-proof", "text", "source"}}."""
    claims = {}
    for f in sorted(Path(idr_dir).glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        rec = parse_idr_file(text)
        if not rec or rec["status"] != "locked":
            continue
        claims[rec["id"]] = {
            "kind": "idr-proof", "text": rec["proof_text"], "source": str(f),
        }
    return claims


def scan_rdd_claims(rdd_dir):
    """Every LOCKED RDD in rdd_dir -> {rdd_id: {"kind": "rdd-acceptance", "text", "source"}}
    (#656 — locked RDDs join the idr-0009 sampling rotation alongside ADR Decisions and locked IDR
    falsification clauses; PRD/SPEC staleness stays out of scope, de-staling's own job)."""
    claims = {}
    for f in sorted(Path(rdd_dir).glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        rec = parse_rdd_file(text)
        if not rec or rec["status"] != "locked":
            continue
        claims[rec["id"]] = {
            "kind": "rdd-acceptance", "text": rec["acceptance_text"], "source": str(f),
        }
    return claims


def combined_claims(adr_dir, idr_dir, rdd_dir):
    """Union of all three corpora, keyed by claim id — `adr-NNNN`/`idr-NNNN`/`rdd-NNNN` ids never
    collide."""
    claims = {}
    claims.update(scan_adr_claims(adr_dir))
    claims.update(scan_idr_claims(idr_dir))
    claims.update(scan_rdd_claims(rdd_dir))
    return claims


def pick_sample(ids, cursor, n):
    """Pure. Up to `n` ids starting at `cursor mod len(ids)`, wrapping at most once, NEVER
    duplicating an id within one call even when n exceeds the corpus size — caps at len(ids)."""
    if not ids:
        return []
    length = len(ids)
    n = min(n, length)
    start = cursor % length
    return [ids[(start + i) % length] for i in range(n)]


def load_checkpoint(path):
    p = Path(path)
    if not p.is_file():
        return {"cursor": 0}
    return json.loads(p.read_text(encoding="utf-8"))


def save_checkpoint(path, cursor, sampled_at):
    Path(path).write_text(
        json.dumps({"cursor": cursor, "last_sampled_at": sampled_at}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_queue(path):
    p = Path(path)
    if not p.is_file():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("candidates", [])


def save_queue(path, candidates):
    Path(path).write_text(
        json.dumps({"candidates": candidates}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def add_candidate(candidates, claim_id, kind, evidence, owner, queued_at):
    """Pure — append-or-update by (claim_id, kind), never a duplicate row. Mirrors
    `adr_queue.add_candidate`'s idempotency, extended with a mandatory `owner` field (idr-0009's own
    open question — "who executes a falsified verdict" — closed structurally, not left to convention)."""
    out = [c for c in candidates if not (c["claim_id"] == claim_id and c["kind"] == kind)]
    out.append({
        "claim_id": claim_id, "kind": kind, "evidence": evidence, "owner": owner,
        "queued_at": queued_at,
    })
    return out


def clear_ids(candidates, ids_to_clear):
    """Pure — same bare-id-vs-id:kind precision as `adr_queue.clear_ids`."""
    bare_ids, pairs = set(), set()
    for entry in ids_to_clear:
        if ":" in entry:
            pairs.add(tuple(entry.split(":", 1)))
        else:
            bare_ids.add(entry)
    return [
        c for c in candidates
        if c["claim_id"] not in bare_ids and (c["claim_id"], c["kind"]) not in pairs
    ]


def _require_dirs(adr_source, idr_source, rdd_source):
    for label, src in (("ADR", adr_source), ("IDR", idr_source), ("RDD", rdd_source)):
        if not Path(src).is_dir():
            raise SourceUnreadable(f"{label} source not found or not a directory: {src}")


def run_sample(adr_source, idr_source, rdd_source, checkpoint_path, n):
    """Report the next N claims due for re-test — never writes the checkpoint (same crash-safety
    split as adr_checkpoint's classify/advance)."""
    _require_dirs(adr_source, idr_source, rdd_source)
    checkpoint = load_checkpoint(checkpoint_path)
    claims = combined_claims(adr_source, idr_source, rdd_source)
    ids = sorted(claims.keys())
    sampled = pick_sample(ids, checkpoint.get("cursor", 0), n)

    print(f"revalidation_checkpoint sample · {len(ids)} claim(s) in corpus "
          f"({len(scan_adr_claims(adr_source))} ADR, {len(scan_idr_claims(idr_source))} IDR, "
          f"{len(scan_rdd_claims(rdd_source))} RDD)")
    if not sampled:
        print("  nothing to sample — empty corpus")
        return 0
    print(f"  cursor {checkpoint.get('cursor', 0)} -> sampling {len(sampled)}: {', '.join(sampled)}")
    for claim_id in sampled:
        rec = claims[claim_id]
        text_preview = rec["text"] if rec["text"] else "(empty extraction — untestable-by-construction)"
        print(f"\n  --- {claim_id} · {rec['kind']} · {rec['source']} ---")
        print(f"  {text_preview}")
    print(f"\n  checkpoint NOT advanced -> run `advance --n {len(sampled)}` once these are judged")
    return 0


def run_advance(adr_source, idr_source, rdd_source, checkpoint_path, n, sampled_at):
    """Persist the cursor bump — call only after `sample`'s claims have actually been judged and any
    falsified/untestable verdicts queued."""
    _require_dirs(adr_source, idr_source, rdd_source)
    checkpoint = load_checkpoint(checkpoint_path)
    claims = combined_claims(adr_source, idr_source, rdd_source)
    ids = sorted(claims.keys())
    new_cursor = (checkpoint.get("cursor", 0) + n) % len(ids) if ids else 0
    save_checkpoint(checkpoint_path, new_cursor, sampled_at)
    print(f"revalidation_checkpoint advance · cursor {checkpoint.get('cursor', 0)} -> {new_cursor} "
          f"-> checkpoint written to {checkpoint_path}")
    return 0


def _opt(opts, name, required=True, default=None):
    if f"--{name}" in opts:
        return opts[opts.index(f"--{name}") + 1]
    if required:
        raise SystemExit(f"missing --{name}")
    return default


def run(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]

    if cmd in ("sample", "advance"):
        if len(rest) < 3:
            print(f"{cmd} requires <adr-source> <idr-source> <rdd-source>"); return 2
        adr_source, idr_source, rdd_source, opts = rest[0], rest[1], rest[2], rest[3:]
        checkpoint_path = _opt(opts, "checkpoint", required=False,
                                default=".claude/ops/revalidation-checkpoint.json")
        if cmd == "sample":
            n = int(_opt(opts, "n", required=False, default="5"))
            return run_sample(adr_source, idr_source, rdd_source, checkpoint_path, n)
        n = int(_opt(opts, "n"))
        import datetime
        sampled_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return run_advance(adr_source, idr_source, rdd_source, checkpoint_path, n, sampled_at)

    if cmd == "queue-add":
        if not rest:
            print("queue-add requires <path>"); return 2
        path, opts = rest[0], rest[1:]
        claim_id = _opt(opts, "claim")
        kind = _opt(opts, "kind")
        if kind not in ("falsified", "untestable"):
            raise SystemExit(f"queue-add: --kind must be falsified|untestable, got {kind!r}")
        evidence = _opt(opts, "evidence")
        owner = _opt(opts, "owner")
        import datetime
        queued_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        candidates = add_candidate(load_queue(path), claim_id, kind, evidence, owner, queued_at)
        save_queue(path, candidates)
        print(f"revalidation_checkpoint · queued {claim_id} ({kind}, owner={owner}) -> {path} "
              f"[{len(candidates)} pending total]")
        return 0

    if cmd == "queue-pending":
        if not rest:
            print("queue-pending requires <path>"); return 2
        candidates = load_queue(rest[0])
        if not candidates:
            print("revalidation_checkpoint · nothing pending")
            return 0
        print(f"revalidation_checkpoint · {len(candidates)} pending candidate(s)")
        for c in candidates:
            print(f"  {c['claim_id']} · {c['kind']} · owner={c['owner']} · {c['evidence']}")
        return 0

    if cmd == "queue-clear":
        if not rest:
            print("queue-clear requires <path>"); return 2
        path, opts = rest[0], rest[1:]
        ids = _opt(opts, "ids").split(",")
        before = load_queue(path)
        after = clear_ids(before, ids)
        save_queue(path, after)
        print(f"revalidation_checkpoint · cleared {len(before) - len(after)} candidate(s) "
              f"-> {len(after)} remain")
        return 0

    print(__doc__)
    return 2


def selftest():
    # ---- extract_section — the Resolution 3 primitive ---------------------------------------
    idr_text = (
        "## Claim\n\nSomething.\n\n"
        "## Proof\n\nConfirms X. Falsifies Y.\n\n"
        "## Open questions\n\nZ.\n"
    )
    assert extract_section(idr_text, "proof") == "## Proof\n\nConfirms X. Falsifies Y.\n\n", \
        extract_section(idr_text, "proof")
    assert extract_section(idr_text, "risks") is None, "a heading that doesn't exist must return None"

    # ---- parse_idr_frontmatter / parse_idr_file — gated on doc-type: idr, never an ADR --------
    adr_frontmatter_text = (
        "---\ndoc-type: adr\nid: adr-0002\nstatus: accepted\n---\n# ADR-0002 — X\n\n"
        "## Decision\n\nDo the thing.\n"
    )
    assert parse_idr_file(adr_frontmatter_text) is None, \
        "an ADR's frontmatter (doc-type: adr) must never be misread as an IDR"

    # ---- REAL corpus fixtures — the phrasing-variance evidence Resolution 3 is built on -------
    # idr-0009: "Falsifies: ..." colon-anchored, trailing "Supersede on falsification" boilerplate
    idr_0009_text = (
        "---\ndoc-type: idr\nid: idr-0009\nstatus: locked\ndate: 2026-08-18\nowner: kim.granlund\n"
        "supersedes: null\n---\n"
        "# IDR-0009 — Doctrine truth maintenance\n\n"
        "## Claim\n\nEvery accepted ADR Decision and locked IDR falsification clause must be "
        "periodically re-tested.\n\n"
        "## Why\n\nProvenance: derived-from-evidence.\n\n"
        "## Proof\n\n"
        "Confirms: a sweep run emitting per-claim tri-state verdicts as a machine-readable report; at\n"
        "least one falsification discovered by the sweep BEFORE an incident discovers it independently.\n"
        "Falsifies: repeated sweeps returning only \"confirmed\" while incidents keep independently\n"
        "falsifying doctrine in the same period (the sweep tests the wrong layer); or the sweep's\n"
        "measured cost exceeding its yield under idr-0010's worth-firing test across multiple cadences\n"
        "(truth maintenance that costs more than the drift it prevents). Supersede on falsification,\n"
        "never edit once locked.\n\n"
        "## Open questions\n\nInstrument shape: undecided at ratification.\n"
    )
    rec_0009 = parse_idr_file(idr_0009_text)
    assert rec_0009 == {
        "id": "idr-0009", "status": "locked",
        "proof_text": (
            "## Proof\n\n"
            "Confirms: a sweep run emitting per-claim tri-state verdicts as a machine-readable report; at\n"
            "least one falsification discovered by the sweep BEFORE an incident discovers it independently.\n"
            "Falsifies: repeated sweeps returning only \"confirmed\" while incidents keep independently\n"
            "falsifying doctrine in the same period (the sweep tests the wrong layer); or the sweep's\n"
            "measured cost exceeding its yield under idr-0010's worth-firing test across multiple cadences\n"
            "(truth maintenance that costs more than the drift it prevents). Supersede on falsification,\n"
            "never edit once locked.\n\n"
        ),
    }, rec_0009
    assert "Falsifies:" in rec_0009["proof_text"] and "Confirms:" in rec_0009["proof_text"]

    # idr-0006: "Falsifies on the first review..." — no colon, no trailing boilerplate, Proof is
    # the LAST section in the file (no next heading — must extract to EOF cleanly)
    idr_0006_text = (
        "---\ndoc-type: idr\nid: idr-0006\nstatus: locked\ndate: 2026-08-16\nowner: kim.granlund\n"
        "supersedes: null\n---\n"
        "# IDR-0006 — Incident-recurrence rate is the estate's primary success measure\n\n"
        "## Claim\n\nTracking incident-recurrence rate is sufficient.\n\n"
        "## Why\n\nKim's ratification answer closed the open question.\n\n"
        "## Proof\n\n"
        "At each monthly review, compare the DRI's independent read of estate health against what "
        "the two readouts show. Confirms if they keep agreeing. Falsifies on the first review where "
        "they disagree — DRI-judged health moving one way while both readouts hold flat or move the "
        "other; either failure mode means these two signals alone are not sufficient, and the "
        "measure set needs revisiting via a superseding IDR.\n"
    )
    rec_0006 = parse_idr_file(idr_0006_text)
    assert rec_0006["id"] == "idr-0006" and rec_0006["status"] == "locked", rec_0006
    assert "Falsifies on the first review" in rec_0006["proof_text"], rec_0006
    assert rec_0006["proof_text"].startswith("## Proof"), rec_0006
    assert "measure set needs revisiting" in rec_0006["proof_text"], \
        "a Proof section with no trailing heading must extract to EOF, not truncate early"

    # idr-0001: NEVER uses the word "Falsifies" at all — passive "falsified by" — the exact case a
    # keyword-anchored extractor would miss outright. Whole-section extraction must still succeed.
    idr_0001_text = (
        "---\ndoc-type: idr\nid: idr-0001\nstatus: locked\ndate: 2026-08-13\nowner: kim.granlund\n"
        "supersedes: null\n---\n"
        "# IDR-0001 — Self-governing toolchain\n\n"
        "## Claim\n\nThe estate's own toolchain enforces its own standards.\n\n"
        "## Why\n\nDerived from repeated manual-check incidents.\n\n"
        "## Proof\n\n"
        "`harness/scripts/release_gate.py` (the full gate set) plus the per-plugin README footer "
        "ledgers: falsified by a ledger entry re-fixing a previously-mechanized incident class, "
        "dated after that class's gate landed.\n"
    )
    rec_0001 = parse_idr_file(idr_0001_text)
    assert rec_0001["id"] == "idr-0001", rec_0001
    assert "Falsifies" not in rec_0001["proof_text"], \
        "idr-0001's real Proof text never contains the word 'Falsifies' — the whole point of the fixture"
    assert "falsified by a ledger entry" in rec_0001["proof_text"], \
        "a keyword-anchored extractor would have missed this clause entirely; whole-section must not"

    # negative control: a PROPOSED (not locked) IDR is excluded from the claim corpus
    idr_proposed_text = idr_0001_text.replace("status: locked", "status: proposed")
    assert parse_idr_file(idr_proposed_text)["status"] == "proposed"

    # negative control: an IDR with no ## Proof heading at all extracts empty text, never crashes,
    # and is never silently dropped from parse_idr_file's return (the caller decides untestable)
    idr_no_proof_text = (
        "---\ndoc-type: idr\nid: idr-0099\nstatus: locked\n---\n# IDR-0099 — Malformed\n\n"
        "## Claim\n\nSomething with no Proof section.\n"
    )
    rec_no_proof = parse_idr_file(idr_no_proof_text)
    assert rec_no_proof == {"id": "idr-0099", "status": "locked", "proof_text": ""}, rec_no_proof

    # ---- parse_rdd_frontmatter / parse_rdd_file — gated on doc-type: rdd, never an ADR/IDR (#656:
    # locked RDDs join the idr-0009 sampling rotation) -------------------------------------------
    assert parse_rdd_file(adr_frontmatter_text) is None, \
        "an ADR's frontmatter (doc-type: adr) must never be misread as an RDD"
    assert parse_rdd_file(idr_0009_text) is None, \
        "an IDR's frontmatter (doc-type: idr) must never be misread as an RDD"

    rdd_0001_text = (
        "---\ndoc-type: rdd\nid: rdd-0001\nstatus: locked\ndate: 2026-08-18\nowner: kim.granlund\n"
        "dri: kim.granlund\ndecision-refs: idr-0009\nsupersedes: null\n---\n"
        "# RDD-0001 — Locked RDDs join the idr-0009 revalidation rotation\n\n"
        "## Scope\n\nLocked RDDs are sampled alongside accepted ADR Decisions and locked IDR "
        "falsification clauses on the same round-robin rotation.\n\n"
        "## Acceptance\n\n"
        "Every locked RDD in the corpus is included in the combined sampling pool; a falsified or "
        "untestable verdict on a sampled RDD claim always queues with a named owner, same as an "
        "ADR/IDR claim. PRD/SPEC staleness stays de-staling's own job, explicitly out of scope.\n\n"
        "## Sequencing\n\nWave 1 of #655.\n\n"
        "## Completion\n\nShipped once this selftest proves RDD sampling end to end.\n"
    )
    rec_rdd_0001 = parse_rdd_file(rdd_0001_text)
    assert rec_rdd_0001 == {
        "id": "rdd-0001", "status": "locked",
        "acceptance_text": (
            "## Acceptance\n\n"
            "Every locked RDD in the corpus is included in the combined sampling pool; a falsified or "
            "untestable verdict on a sampled RDD claim always queues with a named owner, same as an "
            "ADR/IDR claim. PRD/SPEC staleness stays de-staling's own job, explicitly out of scope.\n\n"
        ),
    }, rec_rdd_0001
    assert parse_idr_file(rdd_0001_text) is None, \
        "an RDD's frontmatter (doc-type: rdd) must never be misread as an IDR"

    # negative control: a DRAFT (not locked) RDD is excluded from the claim corpus
    rdd_draft_text = rdd_0001_text.replace("status: locked", "status: draft")
    assert parse_rdd_file(rdd_draft_text)["status"] == "draft"

    # negative control: an RDD with no ## Acceptance heading at all extracts empty text, never
    # crashes, and is never silently dropped from parse_rdd_file's return (untestable is the
    # caller's call, same discipline as the missing-Proof-heading IDR control above)
    rdd_no_acceptance_text = (
        "---\ndoc-type: rdd\nid: rdd-0099\nstatus: locked\n---\n# RDD-0099 — Malformed\n\n"
        "## Scope\n\nSomething with no Acceptance section.\n"
    )
    rec_rdd_no_acceptance = parse_rdd_file(rdd_no_acceptance_text)
    assert rec_rdd_no_acceptance == {"id": "rdd-0099", "status": "locked", "acceptance_text": ""}, \
        rec_rdd_no_acceptance

    # ---- scan_adr_claims / scan_idr_claims / scan_rdd_claims — accepted/locked filters, real ----
    # ---- dialect reuse --------------------------------------------------------------------------
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        adr_dir, idr_dir, rdd_dir = Path(tmp) / "adr", Path(tmp) / "idr", Path(tmp) / "rdd"
        adr_dir.mkdir(); idr_dir.mkdir(); rdd_dir.mkdir()
        (adr_dir / "0002-x.md").write_text(adr_frontmatter_text, encoding="utf-8")
        (adr_dir / "0003-superseded.md").write_text(
            "---\ndoc-type: adr\nid: adr-0003\nstatus: superseded\n---\n# ADR-0003 — Y\n\n"
            "## Decision\n\nOld thing, now superseded.\n",
            encoding="utf-8",
        )
        (idr_dir / "0009-x.md").write_text(idr_0009_text, encoding="utf-8")
        (idr_dir / "0099-proposed.md").write_text(idr_proposed_text, encoding="utf-8")
        (rdd_dir / "0001-x.md").write_text(rdd_0001_text, encoding="utf-8")
        (rdd_dir / "0099-draft.md").write_text(rdd_draft_text, encoding="utf-8")

        adr_claims = scan_adr_claims(adr_dir)
        assert set(adr_claims) == {"adr-0002"}, \
            f"a superseded ADR must be excluded from the claim corpus: {adr_claims}"
        assert adr_claims["adr-0002"]["kind"] == "adr-decision"
        assert "Do the thing" in adr_claims["adr-0002"]["text"]

        idr_claims = scan_idr_claims(idr_dir)
        assert set(idr_claims) == {"idr-0009"}, \
            f"a proposed (not locked) IDR must be excluded from the claim corpus: {idr_claims}"
        assert idr_claims["idr-0009"]["kind"] == "idr-proof"

        rdd_claims = scan_rdd_claims(rdd_dir)
        assert set(rdd_claims) == {"rdd-0001"}, \
            f"a draft (not locked) RDD must be excluded from the claim corpus: {rdd_claims}"
        assert rdd_claims["rdd-0001"]["kind"] == "rdd-acceptance"

        combined = combined_claims(adr_dir, idr_dir, rdd_dir)
        assert set(combined) == {"adr-0002", "idr-0009", "rdd-0001"}, combined

    # ---- pick_sample — round-robin, no duplicates within one call, wraps correctly ------------
    ids = ["adr-0001", "adr-0002", "idr-0001", "idr-0002", "idr-0003"]
    assert pick_sample(ids, 0, 2) == ["adr-0001", "adr-0002"]
    assert pick_sample(ids, 3, 2) == ["idr-0002", "idr-0003"]
    # wrap: cursor near the end, n crosses the boundary back to the start
    assert pick_sample(ids, 4, 2) == ["idr-0003", "adr-0001"], \
        "sampling must wrap around the corpus, not stop short or error"
    # n exceeding corpus size caps at corpus size, never duplicates within one call
    sampled_all = pick_sample(ids, 2, 10)
    assert len(sampled_all) == len(ids) and len(set(sampled_all)) == len(ids), \
        f"n > corpus size must cap at corpus size with no duplicate: {sampled_all}"
    # empty corpus is a safe no-op, never an error
    assert pick_sample([], 0, 5) == []

    # ---- sample/advance end-to-end against a real temp corpus — cursor persists correctly -----
    with tempfile.TemporaryDirectory() as tmp:
        adr_dir, idr_dir, rdd_dir = Path(tmp) / "adr", Path(tmp) / "idr", Path(tmp) / "rdd"
        adr_dir.mkdir(); idr_dir.mkdir(); rdd_dir.mkdir()
        (adr_dir / "0001-a.md").write_text(
            "---\ndoc-type: adr\nid: adr-0001\nstatus: accepted\n---\n# ADR-0001 — A\n\n"
            "## Decision\n\nFirst.\n", encoding="utf-8",
        )
        (adr_dir / "0002-b.md").write_text(
            "---\ndoc-type: adr\nid: adr-0002\nstatus: accepted\n---\n# ADR-0002 — B\n\n"
            "## Decision\n\nSecond.\n", encoding="utf-8",
        )
        (idr_dir / "0001-c.md").write_text(idr_0001_text, encoding="utf-8")
        (rdd_dir / "0001-d.md").write_text(
            "---\ndoc-type: rdd\nid: rdd-0001\nstatus: locked\n---\n# RDD-0001 — D\n\n"
            "## Acceptance\n\nThird.\n", encoding="utf-8",
        )
        checkpoint_path = Path(tmp) / "checkpoint.json"

        assert not checkpoint_path.exists()
        assert run_sample(str(adr_dir), str(idr_dir), str(rdd_dir), str(checkpoint_path), 2) == 0
        assert not checkpoint_path.exists(), "sample must never write the checkpoint"
        assert run_advance(str(adr_dir), str(idr_dir), str(rdd_dir), str(checkpoint_path), 2,
                            "2026-08-18T00:00:00Z") == 0
        assert checkpoint_path.exists()
        cp = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        assert cp["cursor"] == 2, f"cursor must advance by exactly the judged count: {cp}"

        # a SECOND sample against the advanced checkpoint starts where the first left off — the
        # 4-claim corpus (adr-0001, adr-0002, idr-0001, rdd-0001) continues at cursor 2 with no
        # wrap needed this time (2 + 2 == 4, the corpus's own length)
        checkpoint2 = load_checkpoint(str(checkpoint_path))
        claims2 = combined_claims(str(adr_dir), str(idr_dir), str(rdd_dir))
        second_sample = pick_sample(sorted(claims2), checkpoint2["cursor"], 2)
        assert second_sample == ["idr-0001", "rdd-0001"], \
            f"round-robin must continue from the persisted cursor over the 4-claim corpus: {second_sample}"

    # ---- a genuinely missing source path fails loudly, never a silent empty scan --------------
    try:
        run_sample("/no/such/adr/dir", "/no/such/idr/dir", "/no/such/rdd/dir", "/tmp/x.json", 5)
        raise AssertionError("a missing source directory must raise SourceUnreadable")
    except SourceUnreadable as exc:
        assert "ADR source not found" in str(exc), exc

    # ---- queue-add / queue-pending / queue-clear — same idempotency discipline as adr_queue ---
    q = add_candidate([], "idr-0009", "falsified", "the sweep never fired in 3 cadences", "kim.granlund", "t0")
    assert len(q) == 1 and q[0]["owner"] == "kim.granlund", q

    # idempotent re-add updates in place, never duplicates
    q2 = add_candidate(q, "idr-0009", "falsified", "updated evidence", "kim.granlund", "t1")
    assert len(q2) == 1 and q2[0]["evidence"] == "updated evidence", q2

    # same claim, DIFFERENT kind is a distinct row
    q3 = add_candidate(q2, "idr-0009", "untestable", "unrelated ambiguity in the same IDR", "kim.granlund", "t2")
    assert len(q3) == 2, f"same claim but a different kind must be its own row: {q3}"

    # "id:kind" clears precisely, leaving the deferred row
    q3b = clear_ids(q3, ["idr-0009:falsified"])
    assert len(q3b) == 1 and q3b[0]["kind"] == "untestable", \
        f"an id:kind clear must drop only that one row: {q3b}"

    # a bare id clears every kind at once
    q4 = clear_ids(q3, ["idr-0009"])
    assert q4 == [], f"clearing a bare id must drop ALL its rows: {q4}"

    # negative controls: clearing an absent id or id:kind pair is a safe no-op
    assert clear_ids(q3, ["adr-9999"]) == q3
    assert clear_ids(q3, ["idr-0009:harvest"]) == q3

    # kind validation lives at the CLI layer (run()), proven via the actual entrypoint
    try:
        run(["queue-add", "/tmp/x.json", "--claim", "idr-0001", "--kind", "harvest",
             "--evidence", "e", "--owner", "o"])
        raise AssertionError("an invalid --kind must raise, harvest/stale-citation belong to adr_queue")
    except SystemExit as exc:
        assert "falsified|untestable" in str(exc), exc

    print("revalidation_checkpoint selftest · PASS · extract_section (found/absent), "
          "IDR-vs-ADR frontmatter gate, three real-corpus phrasing-variance fixtures "
          "(idr-0009 colon-anchored, idr-0006 mid-sentence no-boilerplate/EOF-bounded, idr-0001 "
          "passive-voice with no 'Falsifies' token at all), proposed-IDR and missing-Proof-heading "
          "negative controls, RDD-vs-ADR/IDR frontmatter gate (#656: locked RDDs join the "
          "revalidation rotation), a locked-RDD Acceptance-section fixture, draft-RDD and "
          "missing-Acceptance-heading negative controls, accepted/locked corpus filters (superseded "
          "ADR + proposed IDR + draft RDD excluded), round-robin sampling (no duplicates, wraps, "
          "caps at corpus size, empty-corpus no-op), sample/advance cursor persistence across two "
          "firings over the 4-claim ADR+IDR+RDD corpus, missing-source loud failure, and the "
          "queue's append/idempotent-update/precise-clear/bare-clear/kind-validation")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "selftest":
        sys.exit(selftest())
    try:
        sys.exit(run(argv))
    except SourceUnreadable as exc:
        print("revalidation_checkpoint · FAIL · source unreadable · 1 fail / 0 warn", file=sys.stderr)
        print(f"  {exc}", file=sys.stderr)
        sys.exit(1)
