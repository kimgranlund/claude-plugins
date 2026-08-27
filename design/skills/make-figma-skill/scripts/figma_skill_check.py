#!/usr/bin/env python3
"""figma_skill_check.py — mechanical gates for a single-file Figma custom skill.

Figma's agent / Figma Make accepts ONE markdown file per custom skill (Agent Skills
frontmatter, NO scripts/ references/ assets/) and validates nothing beyond parsing —
so this run is the gate of record. Judgment dimensions (R1 fidelity beyond the
mechanical slice, R2 tool mapping quality, R3 trigger quality) stay with
references/rubric.md.

Usage:
    python3 figma_skill_check.py <skill.md> [--source <source-skill-dir>] [--json]
    python3 figma_skill_check.py --hash <source-skill-dir>     # the provenance hash
    python3 figma_skill_check.py selftest

F3 scans the body MINUS the `## Dropped` / `## Provenance` sections and minus any
`(transposed from …)` parenthetical — those legitimately name sidecar paths.

Checks (labels match references/rubric.md):
  F1 frontmatter      — parses; `name` 1-64 chars [a-z0-9-], no leading/trailing/double
                        hyphen; `description` 1-1024 chars, non-empty.
  F2 portable keys    — no Claude-Code-only frontmatter keys (disable-model-invocation,
                        user-invocable, allowed-tools, disallowed-tools, context, agent,
                        model, effort, paths, hooks, shell, argument-hint, when_to_use).
  F3 no sidecars      — body carries no unresolved sidecar references: `references/`,
                        `scripts/`, `assets/`, `[[handle]]`, `${CLAUDE_PLUGIN_ROOT}`,
                        `python3 `/`node ` invocations, `AskUserQuestion`, `Bash(`.
  F4 active trigger   — description carries an active trigger clause ("Use when", "Use
                        for", "Trigger when", "Invoke when"); WARN on the soft forms
                        Figma documents as misread ("only when", "only if").
  F5 provenance       — a `## Provenance` section naming `source:` and `date:` (required
                        with --source; WARN without); with --source, WARN when `hash:` or
                        `inventory:` is absent.
  F6 resolution       — with --source: every `##`/`###` heading in the source SKILL.md
                        and every references/*.md it cites survives in the output
                        (normalized match), or is listed under `## Dropped` with a
                        reason; every numeric anchor (N:1, N%, Npx, N lines, N chars,
                        <= N, >= N, N-of-M) in the source survives verbatim. Every
                        `## Dropped` bullet carries a reason from the CLOSED set
                        (`uncited by source body`, `not performable in Figma`,
                        `Claude Code runtime only`, `superseded by inlined sibling
                        slice`, `user ruling:`) — any other reason FAILs.
                        Without --source: UNMEASURED (reported, never failed).
  F7 head-first       — a routing table or TOC (a `## Contents`/`## Routing` section or a
                        markdown table in the first 60 lines) when the body > 300 lines.
  F8 trigger vocab    — with --source and a source evals/evals.json: WARN naming every
                        `expect: trigger` prompt that shares no content word (>= 5 chars)
                        with the output description — the source's own trigger corpus is
                        the vocabulary the Figma description should carry.

Non-fatal notes: line/word count; heading count.

Exit 0 = all gates passed (WARN/UNMEASURED allowed). Exit 1 = at least one FAIL.
Exit 2 = usage error / unreadable input.
Selftest: runs the SAME check functions over embedded fixtures — one passing skill,
one failing skill (sidecar leak + Claude-only key + soft trigger), and one
resolution-miss pair (a source dir whose heading + threshold the output dropped) —
plus a reverse control proving F6 passes when the output DOES carry them.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

CLAUDE_ONLY_KEYS = {
    "disable-model-invocation", "user-invocable", "allowed-tools", "disallowed-tools",
    "context", "agent", "model", "effort", "paths", "hooks", "shell", "argument-hint",
    "when_to_use", "arguments",
}
SIDECAR_PATTERNS = [
    (r"\breferences/", "references/ path"),
    (r"\bscripts/", "scripts/ path"),
    (r"\bassets/", "assets/ path"),
    (r"\[\[[^\]]+\]\]", "[[handle]] wiki-link"),
    (r"\$\{CLAUDE_PLUGIN_ROOT\}", "${CLAUDE_PLUGIN_ROOT}"),
    (r"\bpython3\s+\S+\.py\b", "python3 invocation"),
    (r"\bnode\s+\S+\.(?:m?js|cjs)\b", "node invocation"),
    (r"\bAskUserQuestion\b", "AskUserQuestion tool"),
    (r"\bBash\(", "Bash( tool grant"),
]
ACTIVE_TRIGGER_RE = re.compile(r"\b(use when|use for|trigger when|invoke when|use this when|use it when)\b", re.I)
SOFT_TRIGGER_RE = re.compile(r"\b(only when|only if|use only)\b", re.I)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DROPPED_REASONS = (
    "uncited by source body",
    "not performable in figma",
    "claude code runtime only",
    "superseded by inlined sibling slice",
    "user ruling:",
)
NUMERIC_ANCHOR_RE = re.compile(
    r"(\b\d+(?:\.\d+)?\s*:\s*1\b"          # 4.5:1
    r"|\b\d+(?:\.\d+)?\s*%"                # 60%
    r"|\b\d+(?:\.\d+)?\s*(?:px|rem|em|dp|sp|ms|s)\b"  # 16px 0.5rem 200ms
    r"|\b\d+\s+(?:lines?|chars?|characters|words|tokens|steps?|files?|tries|attempts)\b"
    r"|(?:<=|>=|≤|≥|<|>)\s*\d+(?:\.\d+)?"
    r"|\b\d+-of-\d+\b)"
)


# ---------------------------------------------------------------- frontmatter
def split_frontmatter(text: str):
    """Return (meta: dict|None, body: str, error: str|None). Minimal YAML: key: value,
    folded `>-`/`>` scalars, quoted strings. Enough for Agent Skills frontmatter."""
    if not text.startswith("---"):
        return None, text, "no leading --- fence"
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None, text, "no closing --- fence"
    head = parts[0][3:].strip("\n")
    body = parts[1].lstrip("\n")
    meta: dict[str, str] = {}
    cur_key = None
    folded: list[str] = []
    for line in head.splitlines():
        if line.startswith((" ", "\t")) and cur_key is not None:
            folded.append(line.strip())
            continue
        if cur_key is not None and folded:
            meta[cur_key] = " ".join(folded).strip()
            folded = []
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            if line.strip():
                return None, body, f"unparseable frontmatter line: {line!r}"
            continue
        cur_key, val = m.group(1), m.group(2).strip()
        if val in (">", ">-", "|", "|-"):
            folded = []
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        meta[cur_key] = val
    if cur_key is not None and folded:
        meta[cur_key] = " ".join(folded).strip()
    return meta, body, None


# ---------------------------------------------------------------- helpers
def norm_heading(h: str) -> str:
    h = re.sub(r"[`*_#]", "", h).lower()
    h = re.sub(r"\(.*?\)", "", h)
    h = re.sub(r"[^a-z0-9 ]", " ", h)
    return " ".join(h.split())


def headings(text: str, levels=("##", "###")) -> list[str]:
    out = []
    for line in text.splitlines():
        for lv in levels:
            if line.startswith(lv + " "):
                out.append(norm_heading(line[len(lv) + 1:]))
                break
    return out


def cited_reference_files(source_dir: Path, source_body: str) -> list[Path]:
    refs = source_dir / "references"
    if not refs.is_dir():
        return []
    cited = set(re.findall(r"references/([A-Za-z0-9_./-]+\.md)", source_body))
    files = [refs / c for c in cited if (refs / c).is_file()]
    # A source citing `references/` as a folder (INDEX-style) contributes every file.
    if re.search(r"references/\s", source_body + " ") and not files:
        files = sorted(p for p in refs.rglob("*.md"))
    return files


HASH_EXCLUDE_DIRS = {"agents", "evals", "__pycache__", "dist"}
HASH_EXCLUDE_FILES = {"intent.md"}


def source_hash(source_dir: Path) -> str:
    """The provenance hash: sha256 over sorted `<relpath> <sha256(bytes)>` lines for every
    file under the source dir, excluding agents/ evals/ __pycache__/ dist/ and intent.md
    (harness overlays and forge state, not skill content). First 12 hex chars."""
    import hashlib
    lines = []
    for p in sorted(source_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(source_dir)
        if rel.parts[0] in HASH_EXCLUDE_DIRS or rel.name in HASH_EXCLUDE_FILES:
            continue
        lines.append(f"{rel.as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:12]


def dropped_section(body: str) -> str:
    m = re.search(r"^## Dropped\b.*?(?=^## |\Z)", body, re.M | re.S)
    return m.group(0) if m else ""


# ---------------------------------------------------------------- checks
def check(text: str, source_dir: Path | None) -> list[tuple[str, str, str]]:
    """Return findings as (level, gate, message). level ∈ FAIL/WARN/UNMEASURED/NOTE."""
    f: list[tuple[str, str, str]] = []
    meta, body, err = split_frontmatter(text)

    # F1
    if err or meta is None:
        f.append(("FAIL", "F1", f"frontmatter: {err}"))
        meta = {}
    name = meta.get("name", "")
    desc = meta.get("description", "")
    if not (1 <= len(name) <= 64 and NAME_RE.match(name)):
        f.append(("FAIL", "F1", f"name {name!r}: 1-64 chars, [a-z0-9-], no leading/trailing/double hyphen"))
    if not (1 <= len(desc) <= 1024):
        f.append(("FAIL", "F1", f"description length {len(desc)} outside 1-1024"))

    # F2
    bad = sorted(k for k in meta if k in CLAUDE_ONLY_KEYS)
    if bad:
        f.append(("FAIL", "F2", f"Claude-Code-only frontmatter keys: {bad} -> strip; Figma ignores or rejects them"))

    # F3 — scanned over the body MINUS the `## Dropped`/`## Provenance` sections (they
    # legitimately name what was left behind) and minus `(transposed from …)` parentheticals.
    scan = re.sub(r"^## (Dropped|Provenance)\b.*?(?=^## |\Z)", "", body, flags=re.M | re.S)
    scan = re.sub(r"\(transposed from [^)]*\)", "", scan)
    for pat, label in SIDECAR_PATTERNS:
        hits = re.findall(pat, scan)
        if hits:
            f.append(("FAIL", "F3", f"{len(hits)} sidecar reference(s): {label} (e.g. {hits[0]!r}) -> inline or transpose"))

    # F4
    if desc and not ACTIVE_TRIGGER_RE.search(desc):
        f.append(("FAIL", "F4", "description has no active trigger clause (Use when / Use for / Trigger when)"))
    if desc and SOFT_TRIGGER_RE.search(desc):
        f.append(("WARN", "F4", "soft trigger phrasing ('only when/if') — Figma reads it as 'don't use unless'; phrase as a requirement"))

    # F5
    prov = re.search(r"^## Provenance\b.*?(?=^## |\Z)", body, re.M | re.S)
    has_prov = bool(prov and re.search(r"\bsource:", prov.group(0)) and re.search(r"\bdate:", prov.group(0)))
    if source_dir is not None and not has_prov:
        f.append(("FAIL", "F5", "converted skill lacks `## Provenance` with `source:` and `date:`"))
    elif source_dir is not None:
        for key in ("hash:", "inventory:"):
            if not re.search(r"\b" + key, prov.group(0)):
                f.append(("WARN", "F5", f"`## Provenance` lacks `{key}` — regeneration can't diff without it"))
    elif source_dir is None and not has_prov:
        f.append(("WARN", "F5", "no `## Provenance` section (source:/date:) — fine for net-new, required for a conversion"))

    # F6
    if source_dir is None:
        f.append(("UNMEASURED", "F6", "resolution coverage not measured (no --source)"))
    else:
        src_skill = source_dir / "SKILL.md"
        if not src_skill.is_file():
            f.append(("FAIL", "F6", f"--source has no SKILL.md: {source_dir}"))
        else:
            src_text = src_skill.read_text(encoding="utf-8", errors="replace")
            _, src_body, _ = split_frontmatter(src_text)
            corpus = [("SKILL.md", src_body)]
            for rf in cited_reference_files(source_dir, src_body):
                corpus.append((f"references/{rf.relative_to(source_dir / 'references')}", rf.read_text(encoding="utf-8", errors="replace")))
            out_heads = set(headings(body))
            out_norm = norm_heading(body)
            dropped = norm_heading(dropped_section(body))
            missing_heads, missing_nums = [], []
            for label, txt in corpus:
                for h in headings(txt):
                    if h in ("references", "references tools", "references composition", "provenance", "dropped"):
                        continue
                    if h not in out_heads and h not in dropped and h not in out_norm:
                        missing_heads.append(f"{label}: {h}")
                for n in set(m.strip() for m in NUMERIC_ANCHOR_RE.findall(txt)):
                    if n not in body and n not in dropped_section(body):
                        missing_nums.append(f"{label}: {n}")
            bad_reasons = []
            bullets: list[str] = []
            for line in dropped_section(body).splitlines():
                if line.lstrip().startswith(("-", "*")):
                    bullets.append(line.strip())
                elif bullets and line.startswith((" ", "\t")):
                    bullets[-1] += " " + line.strip()      # wrapped continuation
            for b in bullets:
                if not any(r in b.lower() for r in DROPPED_REASONS):
                    bad_reasons.append(b[:70])
            if bad_reasons:
                f.append(("FAIL", "F6", f"{len(bad_reasons)} `## Dropped` entry(ies) without a closed-set reason: {bad_reasons[:4]}"))
            if missing_heads:
                f.append(("FAIL", "F6", f"{len(missing_heads)} source heading(s) neither carried nor listed under `## Dropped`: {missing_heads[:5]}"))
            if missing_nums:
                f.append(("FAIL", "F6", f"{len(missing_nums)} numeric anchor(s) lost: {missing_nums[:6]}"))
            if not missing_heads and not missing_nums and not bad_reasons:
                f.append(("NOTE", "F6", f"resolution held over {len(corpus)} source file(s)"))

    # F8
    if source_dir is not None:
        ev = source_dir / "evals" / "evals.json"
        if ev.is_file():
            try:
                cases = json.loads(ev.read_text(encoding="utf-8")).get("cases", [])
            except json.JSONDecodeError:
                cases = []
            dwords = set(re.findall(r"[a-z]{5,}", desc.lower()))
            misses = []
            for c in cases:
                if c.get("expect") != "trigger":
                    continue
                pw = set(re.findall(r"[a-z]{5,}", c.get("prompt", "").lower()))
                if pw and not (pw & dwords):
                    misses.append(c.get("id", "?"))
            if misses:
                f.append(("WARN", "F8", f"{len(misses)} source trigger prompt(s) share no content word with the description: {misses[:8]}"))
            else:
                f.append(("NOTE", "F8", "every source trigger prompt shares vocabulary with the description"))

    # F7
    lines = body.splitlines()
    if len(lines) > 300:
        head60 = "\n".join(lines[:60])
        if not (re.search(r"^## (Contents|Routing|Index)\b", head60, re.M) or re.search(r"^\|.*\|\s*$", head60, re.M)):
            f.append(("FAIL", "F7", f"body is {len(lines)} lines with no routing table/TOC in the first 60 lines"))

    f.append(("NOTE", "size", f"{len(lines)} lines · {len(body.split())} words · {len(headings(body))} headings"))
    return f


# ---------------------------------------------------------------- fixtures
GOOD = """---
name: ds-button-rules
description: >-
  Applies our design system's button rules when generating or editing buttons. Use when the
  user asks for a button, CTA, or action control, or when a screen being generated contains
  one. Covers variants, states, sizing, and the 4.5:1 contrast floor.
---
# ds-button-rules

## Variants
Primary, secondary, ghost. Contrast floor 4.5:1 on every fill/on pair.

## States
hover/active/disabled as literal values, never adjectives. Min touch target 44px.

## Provenance
source: frontend/skills/make-component (v1.2.0)
date: 2026-08-27
"""

BAD = """---
name: Button_Rules
description: Helps with buttons. Use only when a button is selected.
disable-model-invocation: false
allowed-tools: Bash(git add *)
---
# rules
See references/rubric.md and run python3 scripts/check.py. Also [[make-palette]].
"""

SRC_SKILL = """---
name: demo-source
description: demo. Use when demoing.
disable-model-invocation: false
user-invocable: true
---
# demo-source

## Variants
Three variants.

## Contrast gate
Every pair >= 4.5:1; body text 16px minimum. Details: references/gates.md.
"""
SRC_REF = """# gates
## Touch targets
Every control is at least 44px. Retry at most 3 tries.
"""
OUT_MISS = """---
name: demo-figma
description: demo. Use when demoing.
---
# demo-figma

## Variants
Three variants.

## Provenance
source: demo-source
date: 2026-08-27
"""
OUT_HIT = """---
name: demo-figma
description: demo. Use when demoing.
---
# demo-figma

## Variants
Three variants.

## Contrast gate
Every pair >= 4.5:1; body text 16px minimum.

## Touch targets
Every control is at least 44px. Retry at most 3 tries.

## Provenance
source: demo-source
date: 2026-08-27
"""


def selftest() -> int:
    ok = True

    def expect(cond, msg):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + msg)
        ok = ok and cond

    g = check(GOOD, None)
    expect(not any(lvl == "FAIL" for lvl, _, _ in g), "good fixture: zero FAIL")
    expect(any(gate == "F6" and lvl == "UNMEASURED" for lvl, gate, _ in g), "good fixture: F6 UNMEASURED without --source")

    b = check(BAD, None)
    gates = {gate for lvl, gate, _ in b if lvl == "FAIL"}
    expect("F1" in gates, "bad fixture: F1 bites on uppercase/underscore name")
    expect("F2" in gates, "bad fixture: F2 bites on Claude-only keys")
    expect("F3" in gates, "bad fixture: F3 bites on references/ scripts/ [[handle]] python3")
    expect(any(gate == "F4" and lvl == "WARN" for lvl, gate, _ in b), "bad fixture: F4 WARN on 'use only when'")

    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "demo-source"
        (src / "references").mkdir(parents=True)
        (src / "SKILL.md").write_text(SRC_SKILL, encoding="utf-8")
        (src / "references" / "gates.md").write_text(SRC_REF, encoding="utf-8")
        miss = check(OUT_MISS, src)
        f6 = [m for lvl, gate, m in miss if gate == "F6" and lvl == "FAIL"]
        expect(any("heading" in m for m in f6), "resolution-miss: F6 bites on dropped headings (contrast gate, touch targets)")
        expect(any("anchor" in m for m in f6), "resolution-miss: F6 bites on lost numeric anchors (4.5:1, 16px, 44px, 3 tries)")
        hit = check(OUT_HIT, src)
        expect(not any(gate == "F6" and lvl == "FAIL" for lvl, gate, _ in hit), "reverse control: F6 passes when headings + anchors carried")
        expect(not any(gate == "F5" and lvl == "FAIL" for lvl, gate, _ in hit), "reverse control: F5 passes with provenance")
        no_prov = check(OUT_HIT.replace("## Provenance", "## Origin"), src)
        expect(any(gate == "F5" and lvl == "FAIL" for lvl, gate, _ in no_prov), "conversion without Provenance: F5 bites")
        expect(any(gate == "F5" and lvl == "WARN" for lvl, gate, _ in hit), "F5 WARNs when hash:/inventory: absent on a conversion")
        dropped_ok = OUT_HIT.replace("## Touch targets\nEvery control is at least 44px. Retry at most 3 tries.\n",
                                     "## Dropped\n- Touch targets — not performable in Figma (44px, 3 tries)\n")
        expect(not any(gate == "F6" and lvl == "FAIL" for lvl, gate, _ in check(dropped_ok, src)), "Dropped with a closed-set reason: F6 passes")
        dropped_bad = dropped_ok.replace("not performable in Figma", "seemed unnecessary")
        expect(any(gate == "F6" and lvl == "FAIL" and "closed-set" in m for lvl, gate, m in check(dropped_bad, src)), "Dropped with an off-set reason: F6 bites")
        wrapped = dropped_ok.replace("- Touch targets — not performable in Figma (44px, 3 tries)",
                                     "- Touch targets — see references/gates.md; the byte diff is\n  not performable in Figma (44px, 3 tries)")
        w = check(wrapped, src)
        expect(not any(gate == "F6" and lvl == "FAIL" for lvl, gate, _ in w), "wrapped Dropped bullet: reason on line 2 still counts")
        expect(not any(gate == "F3" for lvl, gate, _ in w if lvl == "FAIL"), "references/ inside ## Dropped is exempt from F3")
        transposed = OUT_HIT.replace("## Touch targets", "## Touch targets (transposed from scripts/gates.py)")
        expect(not any(gate == "F3" for lvl, gate, _ in check(transposed, src) if lvl == "FAIL"), "(transposed from scripts/x) heading is exempt from F3")
        node_prose = check(GOOD.replace("Primary, secondary", "Read the selected node then Primary, secondary"), None)
        expect(not any(gate == "F3" for lvl, gate, _ in node_prose if lvl == "FAIL"), "'the selected node' prose does not trip the node-invocation pattern")
        expect(any(gate == "F3" for lvl, gate, _ in check(GOOD.replace("Primary", "run node build.mjs then Primary"), None) if lvl == "FAIL"), "'node build.mjs' still trips F3")
        h1, h2 = source_hash(src), source_hash(src)
        expect(h1 == h2 and len(h1) == 12, "source_hash is deterministic, 12 hex")
        (src / "SKILL.md").write_text(SRC_SKILL + "\nchanged\n", encoding="utf-8")
        expect(source_hash(src) != h1, "source_hash changes when a source file changes")
        (src / "evals").mkdir()
        (src / "evals" / "evals.json").write_text(json.dumps({"cases": [
            {"id": "t01", "prompt": "demoing the widget", "expect": "trigger"},
            {"id": "t02", "prompt": "align the carousel spacing", "expect": "trigger"},
            {"id": "n01", "prompt": "unrelated thing", "expect": "no-trigger"}]}), encoding="utf-8")
        f8 = [m for lvl, gate, m in check(OUT_HIT, src) if gate == "F8" and lvl == "WARN"]
        expect(f8 and "t02" in f8[0] and "t01" not in f8[0], "F8 warns on t02 (no shared word) and not t01 ('demoing')")

    long_body = GOOD + "\n" + "\n".join(f"## S{i}\ntext" for i in range(200))
    expect(any(gate == "F7" and lvl == "FAIL" for lvl, gate, _ in check(long_body, None)), "F7 bites on >300 lines with no TOC")
    long_toc = GOOD.replace("# ds-button-rules\n", "# ds-button-rules\n\n## Contents\n- Variants\n") + "\n" + "\n".join(f"## S{i}\ntext" for i in range(200))
    expect(not any(gate == "F7" for lvl, gate, _ in check(long_toc, None) if lvl == "FAIL"), "F7 passes with a Contents section")

    print("selftest:", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main(argv: list[str]) -> int:
    if argv[:1] == ["selftest"]:
        return selftest()
    if argv[:1] == ["--hash"]:
        if len(argv) != 2 or not Path(argv[1]).is_dir():
            print("usage: --hash <source-skill-dir>", file=sys.stderr)
            return 2
        print(source_hash(Path(argv[1])))
        return 0
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("skill_md")
    ap.add_argument("--source", help="source skill directory (enables F6 resolution gate)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    p = Path(a.skill_md)
    if not p.is_file():
        print(f"usage error: not a file: {p}", file=sys.stderr)
        return 2
    src = Path(a.source) if a.source else None
    if src is not None and not src.is_dir():
        print(f"usage error: --source is not a directory: {src}", file=sys.stderr)
        return 2
    findings = check(p.read_text(encoding="utf-8", errors="replace"), src)
    if a.json:
        print(json.dumps([{"level": lvl, "gate": g, "message": m} for lvl, g, m in findings], indent=1))
    else:
        for lvl, g, m in findings:
            print(f"{lvl:10s} {g:5s} {m}")
    fails = sum(1 for lvl, _, _ in findings if lvl == "FAIL")
    print(f"result: {'PASS' if not fails else 'FAIL'} ({fails} FAIL)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
