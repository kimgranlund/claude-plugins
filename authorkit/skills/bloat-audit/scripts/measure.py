#!/usr/bin/env python3
"""bloat-audit measurer — deterministic signals for busy-work/over-specification.

Measures, per file: body size, a "Failure branches"-style section's size, a
"Done when" section's size, and a rough count of numbered phase/step
headings. Separately finds near-duplicate paragraphs across files (the
same lesson restated instead of cited once). Judgment (is a flag real
bloat or load-bearing content) belongs to the bloat-audit skill, not here.

Usage:
  measure.py --target PATH [--json]

Exit codes: 0 no flags above threshold, 1 flags found, 2 no files discovered.
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


def section_span(body, heading_pattern):
    """Char length of the first section whose heading matches
    heading_pattern, from that heading to the next '## ' heading or EOF."""
    lines = body.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if re.match(heading_pattern, ln):
            start = i
            break
    if start is None:
        return 0
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s+\S", lines[j]):
            end = j
            break
    return len("\n".join(lines[start:end]))


def phase_count(body):
    headings = len(re.findall(r"(?m)^##+\s*Phase\s+\d", body))
    numbered_top = len(re.findall(r"(?m)^\d+\.\s+\*\*", body))
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"bloat-audit: target not found: {target}")
        sys.exit(2)

    artifacts = list(discover(target))
    if not artifacts:
        print(f"bloat-audit: no markdown files discovered under {target}")
        sys.exit(2)

    measurements = []
    all_paragraphs = []

    for kind, path in artifacts:
        text = path.read_text(errors="replace")
        fm_text, body = split_frontmatter(text)
        desc = frontmatter_field(fm_text, "description")
        chars, lines = len(body), body.count("\n") + 1
        failure_chars = section_span(body, r"^##+\s*Failure\s+(branches|catalog)")
        done_chars = section_span(body, r"^##+\s*Done\b")
        if not done_chars:
            m = re.search(r"(?is)done when.*$", body)
            done_chars = len(m.group(0)) if m else 0
        phases = phase_count(body)

        flags = []
        if chars > LONG_BODY_CHARS:
            flags.append(f"long-body ({chars} chars body, > {LONG_BODY_CHARS} threshold)")
        if phases >= PHASE_HEAVY_COUNT:
            flags.append(f"phase-heavy ({phases} phase/numbered-step headings)")
        if failure_chars > 800:
            flags.append(f"large-failure-section ({failure_chars} chars)")
        if len(desc) > 700:
            flags.append(f"dense-description ({len(desc)} chars)")

        measurements.append({
            "path": rel(path, target),
            "kind": kind,
            "lines": lines,
            "chars": chars,
            "description_chars": len(desc),
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

    result = {
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

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"bloat-audit measure — {len(measurements)} files @ {target}")
        for m in measurements:
            if m["flags"]:
                print(f"  [FLAG] {m['path']}: {', '.join(m['flags'])}")
        for d in duplicates:
            print(f"  [DUPE {d['similarity']}] {d['file_a']} <-> {d['file_b']}: {d['snippet_a']}")
        print(f"  flagged={len(flagged)} duplicate_pairs={len(duplicates)} "
              f"est_recoverable_chars={recoverable}")

    sys.exit(1 if (flagged or duplicates) else 0)


if __name__ == "__main__":
    main()
