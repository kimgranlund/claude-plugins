#!/usr/bin/env python3
"""bloat-audit measurer — deterministic signals for busy-work/over-specification.

Measures, per file: body size, a "Failure branches"-style section's size, a
"Done when" section's size, and a rough count of numbered phase/step
headings. Separately finds near-duplicate paragraphs across files (the
same lesson restated instead of cited once). Judgment (is a flag real
bloat or load-bearing content) belongs to the bloat-audit skill, not here.

Usage:
  measure.py --target PATH [--json]
  measure.py selftest              prove the counters bite

Exit codes: 0 no flags above threshold, 1 flags found, 2 no files discovered
or no args.
"""

import argparse
import json
import re
import sys
from pathlib import Path

LONG_BODY_CHARS = 6000
PHASE_HEAVY_COUNT = 5
MIN_PARAGRAPH_WORDS = 25
DUPLICATE_JACCARD = 0.5
SHINGLE_SIZE = 8
FAILURE_SECTION_CHARS = 800
DENSE_DESCRIPTION_CHARS = 700
# A "NOT for X (owner)" / "NOT the Y (owner)" routing-disambiguation clause, possibly
# chaining several "... (owner)" targets under one leading NOT ("NOT A (b) or C (d).") —
# load-bearing content a naming/routing convention packs into every description, not
# padding (issue #798: agent-ui estate calibration, 14/19 flagged files were entirely
# this shape). Only the parenthetical-owner shape is discounted; a NOT-clause with no
# paren-owner ("NOT marketing tactics ... — that is X's domain") is left counted, since
# it isn't the specific pattern the estate convention packs in and a broader strip risks
# discounting genuine prose.
NOT_FENCE_RE = re.compile(r"\bNOT\b(?:[^.;(]*\([^()]*\))+[.;]?", re.IGNORECASE)
RESTATEMENT_SHINGLE_SIZE = 1
RESTATEMENT_JACCARD = 0.15
RESTATEMENT_MAJORITY = 0.5
SKIP_DIRS = {".git", "node_modules", "dist", ".claude-plugin"}


def split_frontmatter(text):
    parts = text.split("---", 2)
    if len(parts) >= 3 and text.startswith("---"):
        return parts[1], parts[2]
    return "", text


def frontmatter_field(fm_text, field):
    m = re.search(rf"^{field}:\s*(.*)$", fm_text, re.MULTILINE)
    if not m:
        return ""
    val = m.group(1).strip()
    if val in (">", ">-", "|", "|-", ""):
        lines = []
        started = False
        for ln in fm_text.split("\n"):
            if ln.strip() == f"{field}:" or re.match(rf"^{field}:\s*[>|]", ln):
                started = True
                continue
            if started:
                if ln.startswith((" ", "\t")):
                    lines.append(ln.strip())
                else:
                    break
        return " ".join(lines)
    return val.strip("'\"")


def section_bounds(body, heading_pattern):
    """(start, end) line indices for the first section whose heading matches
    heading_pattern — start is the heading line itself, end is the next
    '## ' heading or EOF. Returns None if no heading matches."""
    lines = body.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if re.match(heading_pattern, ln):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s+\S", lines[j]):
            end = j
            break
    return start, end


def section_span(body, heading_pattern):
    """Char length of the first section whose heading matches
    heading_pattern, from that heading to the next '## ' heading or EOF."""
    bounds = section_bounds(body, heading_pattern)
    if bounds is None:
        return 0
    lines = body.split("\n")
    start, end = bounds
    return len("\n".join(lines[start:end]))


def list_entries(section_body):
    """Split a section's body (heading line already excluded) into
    top-level list entries — a bullet ('-'/'*') or numbered item plus its
    indented continuation lines. Returns [] when the section isn't
    list-shaped (no top-level bullet/numbered markers found) — the
    restatement exemption below only ever applies to genuinely enumerated
    sections, never free-form prose."""
    entries = []
    current = []
    for ln in section_body.split("\n"):
        if re.match(r"^(-|\*|\d+\.)\s+\S", ln):
            if current:
                entries.append("\n".join(current))
            current = [ln]
        elif current:
            current.append(ln)
    if current:
        entries.append("\n".join(current))
    return entries


def restates_procedure(entries, procedure_text):
    """True when a MAJORITY of a list-shaped section's entries substantially
    restate the procedure text stated above them in the same document —
    CALIBRATION.md's Keep test ("would cutting this lose a real instruction,
    or only its retelling?"), applied mechanically via shingle overlap
    against the procedure text (RESTATEMENT_SHINGLE_SIZE=1, i.e. shared
    vocabulary — a restated entry paraphrases the same words in a different
    order, so a wide shingle window like the cross-file duplicate-paragraph
    check's 8-word one misses it; a distinct edge case shares little
    vocabulary with the procedure at all). False when entries each name
    their own distinct, non-obvious edge case — the exact
    enumerated-failure-list shape CALIBRATION.md's Keep test protects
    (issue #775: 2/2 false positives on bare char count alone). None when
    the section isn't list-shaped, or the procedure text above it is too
    short to shingle — the caller falls back to char count alone in either
    case."""
    if len(entries) < 2:
        return None
    proc_shingles = shingles(normalize(procedure_text).split(), k=RESTATEMENT_SHINGLE_SIZE)
    if not proc_shingles:
        return None
    restated = sum(
        1 for entry in entries
        if jaccard(shingles(normalize(entry).split(), k=RESTATEMENT_SHINGLE_SIZE), proc_shingles)
        >= RESTATEMENT_JACCARD
    )
    return (restated / len(entries)) >= RESTATEMENT_MAJORITY


def phase_count(body):
    """Count real phase/step markers only — a heading ("## Phase 3") or a
    top-level numbered item whose own bold lead-in names a phase/step/stage
    ("1. **Phase 1: Discover**"). A plain numbered list of bolded terms
    (principles, glossary entries, findings) is not a phase list just
    because it's numbered and bold (issue #465)."""
    headings = len(re.findall(r"(?m)^##+\s*Phase\s+\d", body))
    numbered_top = len(re.findall(
        r"(?mi)^\d+\.\s+\*\*\s*(Phase|Step|Stage)\b", body))
    return max(headings, numbered_top)


def discover(target: Path):
    """Yield (kind, path) for skills/agents/commands dirs if present;
    otherwise fall back to every .md file under target (generic corpus)."""
    root = target / ".claude" if (target / ".claude").is_dir() else target
    found_any_species = False
    for kind, sub in (("command", "commands"), ("agent", "agents")):
        d = root / sub
        if d.is_dir():
            found_any_species = True
            for p in sorted(d.glob("*.md")):
                yield kind, p
    sd = root / "skills"
    if sd.is_dir():
        found_any_species = True
        for p in sorted(sd.iterdir()):
            if p.is_dir() and (p / "SKILL.md").is_file():
                yield "skill", p / "SKILL.md"
    if not found_any_species:
        for p in sorted(target.rglob("*.md")):
            if not any(part in SKIP_DIRS for part in p.parts):
                yield "doc", p


def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def shingles(words, k=SHINGLE_SIZE):
    if len(words) < k:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def collect_paragraphs(path, body):
    out = []
    for para in re.split(r"\n\s*\n", body):
        words = para.split()
        if len(words) >= MIN_PARAGRAPH_WORDS:
            norm = normalize(para)
            out.append({
                "path": str(path),
                "snippet": " ".join(para.split()[:15]) + " …",
                "words": norm.split(),
            })
    return out


def rel(path: Path, target: Path):
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def analyze(target: Path):
    """Core measurement logic over an already-resolved target. Returns the
    result dict, or None if the target doesn't exist or has no markdown to
    scan. Pure of argv/exit-code concerns so it is directly callable from
    both main() and selftest()."""
    if not target.exists():
        return None

    artifacts = list(discover(target))
    if not artifacts:
        return None

    measurements = []
    all_paragraphs = []

    for kind, path in artifacts:
        text = path.read_text(errors="replace")
        fm_text, body = split_frontmatter(text)
        desc = frontmatter_field(fm_text, "description")
        chars, lines = len(body), body.count("\n") + 1
        body_lines = body.split("\n")
        failure_bounds = section_bounds(body, r"^##+\s*Failure\s+(branches|catalog)")
        failure_chars = 0
        failure_restates = None
        if failure_bounds is not None:
            fstart, fend = failure_bounds
            failure_chars = len("\n".join(body_lines[fstart:fend]))
            if failure_chars > FAILURE_SECTION_CHARS:
                entries = list_entries("\n".join(body_lines[fstart + 1:fend]))
                procedure_text = "\n".join(body_lines[:fstart])
                failure_restates = restates_procedure(entries, procedure_text)
        done_chars = section_span(body, r"^##+\s*Done\b")
        if not done_chars:
            # Line-initial "Done when"/"Done when:" only — an incidental
            # mid-sentence mention ("...spec). Done when the lint is
            # clean...") must not anchor a match, and the match stops at
            # the next blank line so it can't run to EOF (issue #465).
            m = re.search(r"(?mi)^\*{0,2}done when\b.*?(?=\n\s*\n|\Z)",
                          body, re.DOTALL)
            done_chars = len(m.group(0)) if m else 0
        phases = phase_count(body)

        flags = []
        if chars > LONG_BODY_CHARS:
            flags.append(f"long-body ({chars} chars body, > {LONG_BODY_CHARS} threshold)")
        if phases >= PHASE_HEAVY_COUNT:
            flags.append(f"phase-heavy ({phases} phase/numbered-step headings)")
        if failure_chars > FAILURE_SECTION_CHARS and failure_restates is not False:
            flags.append(f"large-failure-section ({failure_chars} chars)")
        not_fence_chars = sum(len(m) for m in NOT_FENCE_RE.findall(desc))
        desc_content_chars = len(desc) - not_fence_chars
        if desc_content_chars > DENSE_DESCRIPTION_CHARS:
            flags.append(f"dense-description ({len(desc)} chars, {desc_content_chars} "
                         f"non-NOT-fence content chars)")

        measurements.append({
            "path": rel(path, target),
            "kind": kind,
            "lines": lines,
            "chars": chars,
            "description_chars": len(desc),
            "description_content_chars": desc_content_chars,
            "failure_section_chars": failure_chars,
            "done_section_chars": done_chars,
            "phase_count": phases,
            "flags": flags,
        })
        all_paragraphs.extend(collect_paragraphs(rel(path, target), body))

    for p in all_paragraphs:
        p["shingles"] = shingles(p["words"])

    duplicates = []
    seen_pairs = set()
    for i in range(len(all_paragraphs)):
        for j in range(i + 1, len(all_paragraphs)):
            a, b = all_paragraphs[i], all_paragraphs[j]
            if a["path"] == b["path"]:
                continue
            sim = jaccard(a["shingles"], b["shingles"])
            if sim >= DUPLICATE_JACCARD:
                key = tuple(sorted((a["path"] + a["snippet"], b["path"] + b["snippet"])))
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                duplicates.append({
                    "file_a": a["path"], "snippet_a": a["snippet"],
                    "file_b": b["path"], "snippet_b": b["snippet"],
                    "similarity": round(sim, 2),
                })

    flagged = [m for m in measurements if m["flags"]]
    recoverable = sum(
        m["failure_section_chars"] for m in flagged
        if any("large-failure-section" in f for f in m["flags"])
    )
    recoverable += sum(min(len(d["snippet_a"]), len(d["snippet_b"])) * 8 for d in duplicates)

    return {
        "target": str(target),
        "files_scanned": len(measurements),
        "measurements": measurements,
        "duplicates": duplicates,
        "totals": {
            "flagged_files": len(flagged),
            "duplicate_pairs": len(duplicates),
            "estimated_recoverable_chars": recoverable,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    result = analyze(target)
    if result is None:
        print(f"bloat-audit: target not found or no markdown discovered: {target}")
        sys.exit(2)

    flagged = result["totals"]["flagged_files"]
    duplicates = result["totals"]["duplicate_pairs"]

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"bloat-audit measure — {result['files_scanned']} files @ {target}")
        for m in result["measurements"]:
            if m["flags"]:
                print(f"  [FLAG] {m['path']}: {', '.join(m['flags'])}")
        for d in result["duplicates"]:
            print(f"  [DUPE {d['similarity']}] {d['file_a']} <-> {d['file_b']}: {d['snippet_a']}")
        print(f"  flagged={flagged} duplicate_pairs={duplicates} "
              f"est_recoverable_chars={result['totals']['estimated_recoverable_chars']}")

    sys.exit(1 if (flagged or duplicates) else 0)


def selftest():
    """Prove analyze()'s counters bite: a clean small file passes (reverse
    control); a phase-heavy file with an oversized Failure section is CAUGHT
    (inversion fixture); a plain numbered list of principles is NOT
    misread as phase-heavy, and an incidental mid-sentence "done when"
    doesn't capture to EOF (negative controls, issue #465); a genuine
    line-initial Done-when paragraph is still CAUGHT (inversion fixture); a
    genuine cross-file duplicate paragraph is CAUGHT; a dense-but-legitimate
    enumerated failure list — every entry naming its own distinct,
    non-obvious edge case, unrelated to the procedure text above it — is
    NOT flagged large-failure-section even past the char threshold (negative
    control, issue #775); a failure section that genuinely restates the
    procedure stated above it is still CAUGHT (inversion fixture, issue
    #775); a description over-length purely from "NOT for X (owner)"
    routing-disambiguation clauses is NOT flagged dense-description (negative
    control, issue #798), while a genuinely padded description with no such
    clauses still IS (inversion fixture, issue #798); a target with no
    markdown returns None (the usage-error case)."""
    import tempfile

    # Reverse control: a small, unflagged file must come back clean.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "clean-skill").mkdir(parents=True)
        (r / "skills" / "clean-skill" / "SKILL.md").write_text(
            "---\nname: clean-skill\ndescription: short\n---\n# clean-skill\n\nShort body.\n")
        result = analyze(r)
        assert result is not None
        assert result["totals"]["flagged_files"] == 0, "a short clean file must not be flagged"

    # Inversion fixture: phase-heavy + oversized Failure section must be CAUGHT.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "bloated-skill").mkdir(parents=True)
        phases = "\n".join(f"1. **Step {i}** — do the thing, at length, every single time.\n"
                           f"   More words padding this out to look load-bearing.\n" for i in range(6))
        failure = "x " * 500
        body = (f"---\nname: bloated-skill\ndescription: short\n---\n# bloated-skill\n\n"
                f"{phases}\n\n## Failure branches\n\n{failure}\n")
        (r / "skills" / "bloated-skill" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert any("phase-heavy" in f for f in flags), "phase-heavy file must be flagged"
        assert any("large-failure-section" in f for f in flags), "oversized Failure section must be flagged"

    # Negative control: a dense-but-legitimate enumerated failure list —
    # every entry names a distinct, non-obvious edge case with vocabulary
    # unrelated to the procedure text above it — must NOT be flagged
    # large-failure-section, even past the char threshold. Modeled on the
    # two live false positives (design/make-variants, screens/check-ui-
    # change) — issue #775.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "enumerated-edges").mkdir(parents=True)
        procedure = ("This skill resolves the target directory, runs the "
                     "deterministic measurer over every markdown file, and "
                     "renders a report citing the evidence for each finding.")
        failure_list = "\n".join([
            "- A user cancels mid-upload after the multipart request already "
            "flushed its first chunk to disk — sweep the orphaned partial "
            "blob on the next run, never leave it silently.",
            "- The template selector receives a locale code the catalog has "
            "never registered — fall back to the base locale instead of "
            "raising, and log the miss once per session.",
            "- A webhook redelivers an event after the original already "
            "committed — dedupe by the idempotency key stored on the "
            "transaction row, never by timestamp proximity alone.",
            "- The batch importer hits a row whose foreign key references a "
            "soft-deleted parent — skip that row into the rejection ledger, "
            "never cascade-delete the still-referenced parent.",
            "- A concurrent writer bumps the version counter between this "
            "process's read and its write — retry once with a fresh read, "
            "then surface a real conflict to the caller.",
            "- The exporter is asked for a format the current build doesn't "
            "register — return the capability list in the error body so the "
            "caller can negotiate a supported format down.",
        ])
        body = (f"---\nname: enumerated-edges\ndescription: short\n---\n"
                f"# enumerated-edges\n\n{procedure}\n\n"
                f"## Failure branches\n\n{failure_list}\n")
        assert len(failure_list) > FAILURE_SECTION_CHARS, "fixture must exceed the char threshold"
        (r / "skills" / "enumerated-edges" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert not any("large-failure-section" in f for f in flags), (
            "a dense-but-legitimate enumerated failure list must not be "
            "flagged on bare char count alone")

    # Inversion fixture: a failure section that genuinely restates the
    # procedure stated above it (padding, not new edge cases) must still be
    # CAUGHT — issue #775.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "restating-skill").mkdir(parents=True)
        procedure = ("Run the linter until every file is clean, verify each "
                     "finding is real bloat and not load-bearing content, "
                     "and render the report citing evidence for every "
                     "flagged file before handing it off.")
        failure_list = "\n".join([
            "- If the linter is not run until every file is clean, the "
            "audit is incomplete and must be redone from the start.",
            "- If a finding is not verified as real bloat and not "
            "load-bearing content, the classification recorded is wrong.",
            "- If the report does not cite evidence for every flagged file "
            "before handing it off, the finding is unusable to the reader.",
            "- If the linter is not run until every file is clean and every "
            "finding is not verified as real bloat, nothing here can be "
            "trusted, so redo the whole audit and render the report again.",
            "- Skipping the step where every finding is verified as real "
            "bloat and not load-bearing content means the report cannot be "
            "trusted, so run the linter until every file is clean first.",
            "- Handing off a report that does not cite evidence for every "
            "flagged file, after the linter has been run until every file "
            "is clean, still leaves the finding unusable to the reader.",
        ])
        body = (f"---\nname: restating-skill\ndescription: short\n---\n"
                f"# restating-skill\n\n{procedure}\n\n"
                f"## Failure branches\n\n{failure_list}\n")
        assert len(failure_list) > FAILURE_SECTION_CHARS, "fixture must exceed the char threshold"
        (r / "skills" / "restating-skill" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert any("large-failure-section" in f for f in flags), (
            "a failure section genuinely restating the procedure above it "
            "must still be flagged")

    # Negative control: a plain numbered list of bolded principles (no
    # phase/step/stage wording) must NOT be misread as phase-heavy — #465.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "principled-skill").mkdir(parents=True)
        principles = "\n".join(
            f"{i}. **Principle {i} is the name.** Explanatory prose follows here, "
            f"long enough to look like real content but not a build phase.\n"
            for i in range(1, 7))
        body = (f"---\nname: principled-skill\ndescription: short\n---\n"
                f"# principled-skill\n\n{principles}\n")
        (r / "skills" / "principled-skill" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert not any("phase-heavy" in f for f in flags), \
            "a plain numbered list of principles must not be flagged phase-heavy"

    # Negative control: an incidental mid-sentence "done when" phrase must
    # not fall back to a greedy to-EOF capture — #465.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "incidental-done").mkdir(parents=True)
        tail = "More unrelated content follows this paragraph, on and on. " * 200
        body = (f"---\nname: incidental-done\ndescription: short\n---\n"
                f"# incidental-done\n\nRun the linter until it is clean and every link "
                f"resolves. Done when the lint is clean and every link resolves.\n\n"
                f"## Unrelated section\n\n{tail}\n")
        (r / "skills" / "incidental-done" / "SKILL.md").write_text(body)
        result = analyze(r)
        done_chars = result["measurements"][0]["done_section_chars"]
        assert done_chars < 300, (
            f"an incidental mid-sentence 'done when' must not capture to EOF "
            f"(got {done_chars} chars)")

    # Inversion fixture: a genuine line-initial "Done when" paragraph must
    # still be caught (docs intake Failure-branches class — #373 deep pass).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "real-done").mkdir(parents=True)
        body = ("---\nname: real-done\ndescription: short\n---\n# real-done\n\n"
                "Some procedure body text describing the work to do.\n\n"
                "Done when the report exists with every finding named and every "
                "owner assigned, and nothing is left ambiguous.\n")
        (r / "skills" / "real-done" / "SKILL.md").write_text(body)
        result = analyze(r)
        done_chars = result["measurements"][0]["done_section_chars"]
        assert done_chars > 40, "a genuine line-initial Done-when paragraph must still be measured"

    # Inversion fixture: a near-identical paragraph repeated across two files must be CAUGHT.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "a").mkdir(parents=True)
        (r / "skills" / "b").mkdir(parents=True)
        para = ("This is a long restated paragraph that shows up nearly verbatim in two "
                "different files, which is exactly the kind of cross-file duplication this "
                "measurer exists to catch and report as a finding worth citing.")
        (r / "skills" / "a" / "SKILL.md").write_text(f"---\nname: a\ndescription: x\n---\n{para}\n")
        (r / "skills" / "b" / "SKILL.md").write_text(f"---\nname: b\ndescription: x\n---\n{para}\n")
        result = analyze(r)
        assert result["duplicates"], "a duplicated paragraph across files must be caught"

    # Negative control: a description over the raw 700-char threshold purely because
    # it packs several legitimate "NOT for X (owner)" routing-disambiguation clauses
    # must NOT be flagged dense-description once those clauses are discounted (issue
    # #798: agent-ui estate calibration, 14/19 flagged files were entirely this shape).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "fenced-skill").mkdir(parents=True)
        core = "Does the one real thing this skill owns, described plainly. " * 4
        not_fences = (
            "NOT for scoring or auditing brand work (brand-rubrics) or running the "
            "named-critic council (check-brand-council). NOT the guided 2x2 "
            "elicitation loop (make-brand-guidelines) or the one-page brand-stack "
            "summary (make-brand-stack). NOT corpus organizing or MCP wiring "
            "(brand-corpus). NOT strategy or positioning work (brand-methodology-"
            "rules) or naming and copy (the brand-writer agent). NOT packaging into "
            "a distributable plugin, skill, or MCP (file-brand) or exporting a "
            "navigable site (file-brand-corpus)."
        )
        desc = core + not_fences
        assert len(desc) > DENSE_DESCRIPTION_CHARS, "fixture must exceed the raw threshold"
        body = f"---\nname: fenced-skill\ndescription: {desc}\n---\n# fenced-skill\n\nShort body.\n"
        (r / "skills" / "fenced-skill" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert not any("dense-description" in f for f in flags), (
            "a description over-length purely from NOT-fence clauses must not be flagged")

    # Inversion fixture: a description over the threshold from genuine content (no
    # NOT-fence clauses at all) must still be CAUGHT.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "skills" / "padded-skill").mkdir(parents=True)
        desc = ("Does the one real thing this skill owns, at excessive length, "
                 "restating the same point in slightly different words every "
                 "sentence purely to fill space. " * 8)
        assert len(desc) > DENSE_DESCRIPTION_CHARS, "fixture must exceed the raw threshold"
        body = f"---\nname: padded-skill\ndescription: {desc}\n---\n# padded-skill\n\nShort body.\n"
        (r / "skills" / "padded-skill" / "SKILL.md").write_text(body)
        result = analyze(r)
        flags = result["measurements"][0]["flags"]
        assert any("dense-description" in f for f in flags), (
            "a genuinely padded description with no NOT-fence content must still be flagged")

    # Usage-error case: no markdown discovered -> None, never a silent pass.
    with tempfile.TemporaryDirectory() as td:
        assert analyze(Path(td)) is None, "an empty target must return None"

    print("bloat-audit measure selftest · PASS · flag/duplicate/empty-target counters bite")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
