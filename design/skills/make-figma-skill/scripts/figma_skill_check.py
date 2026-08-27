#!/usr/bin/env python3
"""figma_skill_check.py — mechanical gates for a single-file Figma custom skill.

Figma's agent / Figma Make accepts ONE markdown file per custom skill (Agent Skills
frontmatter, NO scripts/ references/ assets/) and validates nothing beyond parsing —
so this run is the gate of record. Judgment dimensions (R1 fidelity beyond the
mechanical slice, R2 tool mapping quality, R3 trigger quality) stay with
references/rubric.md.

Usage:
    python3 figma_skill_check.py <skill.md> [--source <skill-dir | agents/<name>.md>] [--json]
    python3 figma_skill_check.py --hash <source-skill-dir>     # the provenance hash
    python3 figma_skill_check.py selftest

--source accepts three shapes: a skill directory (kind `skill`, or `command` when its
frontmatter says disable-model-invocation: true), or a single agents/<name>.md file (kind
`agent` — its `skills:` preloads are resolved at <plugin-root>/skills/<name>/ and their
SKILL.md + cited references join the F6 corpus; an unresolvable preload is an F6 FAIL).

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
    "tools", "skills", "color", "background",        # agent-definition keys
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
    (r"\$ARGUMENTS\b", "$ARGUMENTS (command-skill placeholder)"),
    (r"\bSendMessage\b", "SendMessage (agent mailbox)"),
    (r"\b(?:Agent|Skill) tool\b", "Agent/Skill tool dispatch"),
]
ACTIVE_TRIGGER_RE = re.compile(r"\b(use when|use for|trigger when|invoke when|use this when|use it when|invoke with)\b", re.I)
SOFT_TRIGGER_RE = re.compile(r"\b(only when|only if|use only)\b", re.I)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DROPPED_REASONS = (
    "uncited by source body",
    "not performable in figma",
    "claude code runtime only",
    "superseded by inlined sibling slice",
    "sibling job, fenced",
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
    (harness overlays and forge state, not skill content). First 12 hex chars.
    An agent FILE hashes the file's own bytes plus each resolved `skills:` preload dir's
    hash (sorted), so an edit to the agent or to any preload changes it — a sibling agent's
    edit does not."""
    import hashlib
    if source_dir.is_file():
        meta, _, _ = split_frontmatter(source_dir.read_text(encoding="utf-8", errors="replace"))
        parts = [f"{source_dir.name} {hashlib.sha256(source_dir.read_bytes()).hexdigest()}"]
        for p in re.findall(r"[A-Za-z0-9_:-]+", (meta or {}).get("skills", "")):
            sd = resolve_preload(source_dir, p)
            parts.append(f"preload {p} {source_hash(sd) if sd else 'UNRESOLVED'}")
        return hashlib.sha256("\n".join(sorted(parts)).encode("utf-8")).hexdigest()[:12]
    lines = []
    for p in sorted(source_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(source_dir)
        if rel.parts[0] in HASH_EXCLUDE_DIRS or rel.name in HASH_EXCLUDE_FILES:
            continue
        lines.append(f"{rel.as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:12]


def _skill_corpus(skill_dir: Path, label_prefix: str) -> tuple[str, list[tuple[str, str]], list[str]]:
    """(kind, corpus, errors) for a skill directory: SKILL.md + every cited reference."""
    src_skill = skill_dir / "SKILL.md"
    if not src_skill.is_file():
        return "skill", [], [f"no SKILL.md under {skill_dir}"]
    meta, src_body, _ = split_frontmatter(src_skill.read_text(encoding="utf-8", errors="replace"))
    kind = "command" if (meta or {}).get("disable-model-invocation", "").lower() == "true" else "skill"
    corpus = [(f"{label_prefix}SKILL.md", src_body)]
    for rf in cited_reference_files(skill_dir, src_body):
        corpus.append((f"{label_prefix}references/{rf.relative_to(skill_dir / 'references')}",
                       rf.read_text(encoding="utf-8", errors="replace")))
    return kind, corpus, []


def resolve_preload(agent_file: Path, handle: str) -> Path | None:
    """`name` → <plugin-root>/skills/name; `plugin:name` → <plugin-root>/../plugin/skills/name
    (the workspace layout, one plugin dir per sibling). None when neither holds a SKILL.md."""
    plugin_root = agent_file.parent.parent
    if ":" in handle:
        plug, local = handle.split(":", 1)
        # A prefixed handle resolves ONLY in the named sibling plugin — a same-named local
        # skill would be the wrong content and a false F6 PASS.
        cands = [plugin_root.parent / plug / "skills" / local]
    else:
        cands = [plugin_root / "skills" / handle]
    for c in cands:
        if (c / "SKILL.md").is_file():
            return c
    return None


def load_source(source: Path) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Resolve a --source into (kind, corpus, errors).

    kind ∈ skill | command | agent.
      * a directory holding SKILL.md → skill (command when disable-model-invocation: true);
        corpus = SKILL.md + cited references/*.md
      * a single agents/<name>.md file → agent; corpus = the agent body + for every entry in
        its `skills:` preload list, that skill's SKILL.md and cited references, resolved at
        <plugin-root>/skills/<name>/ where plugin-root = the agents/ dir's parent. An
        unresolvable preload is an F6 error (its content would silently vanish otherwise).
    """
    if source.is_dir():
        return _skill_corpus(source, "")
    if source.is_file() and source.suffix == ".md":
        meta, agent_body, err = split_frontmatter(source.read_text(encoding="utf-8", errors="replace"))
        if err:
            return "agent", [], [f"agent frontmatter: {err}"]
        corpus = [(source.name, agent_body)]
        errors = []
        preloads = re.findall(r"[A-Za-z0-9_:-]+", (meta or {}).get("skills", ""))
        for p in preloads:
            sd = resolve_preload(source, p)
            if sd is None:
                errors.append(f"preload `{p}` not found (same plugin, or a sibling plugin dir `<workspace>/<plugin>/skills/<name>`) — inline from that plugin's checkout or Drop with `sibling job, fenced`")
                continue
            local = sd.name
            _, sub, sub_err = _skill_corpus(sd, f"preload {local}/")
            corpus.extend(sub)
            errors.extend(sub_err)
        return "agent", corpus, errors
    return "skill", [], [f"--source is neither a skill directory nor an agent .md file: {source}"]


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
        kind, corpus, load_errors = load_source(source_dir)
        for e in load_errors:
            f.append(("FAIL", "F6", e))
        if corpus:
            f.append(("NOTE", "F6", f"source kind: {kind}"))
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
        ev = source_dir / "evals" / "evals.json" if source_dir.is_dir() else None
        if ev is None:
            f.append(("NOTE", "F8", "agent source: no evals corpus — R3's trigger phrasings come from the agent description's own quoted phrases"))
        elif re.search(r"\binvoke with\b", desc, re.I):
            f.append(("NOTE", "F8", "command-derived description (Invoke with /name) — trigger-vocabulary check skipped by design"))
        elif ev.is_file():
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


AGENT_SRC = """---
name: demo-checker
description: Grades one demo. Use PROACTIVELY after a demo is built.
tools: Read, Grep
model: sonnet
skills: [demo-source]
---
The checker seat. Never edits.

## Priorities
1. Read the artifact. 2. Score it.

## Report shape
Verdict first; findings by severity, 3 tries max.
"""
AGENT_OUT = """---
name: demo-checker
description: Grades one demo. Use when a demo is built.
---
# demo-checker

## Hard rules
This skill reads and reports; it changes nothing on the canvas.

## Priorities
1. Read the artifact. 2. Score it.

## Report shape
Verdict first; findings by severity, 3 tries max.

## demo-source (preloaded)

## Variants
Three variants.

## Contrast gate
Every pair >= 4.5:1; body text 16px minimum.

## Provenance
source: agents/demo-checker.md
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
        # agent source: preload inlined vs. missing
        plugin = Path(td) / "plug"
        (plugin / "agents").mkdir(parents=True)
        (plugin / "skills" / "demo-source").mkdir(parents=True)
        (plugin / "skills" / "demo-source" / "SKILL.md").write_text(SRC_SKILL, encoding="utf-8")
        agent_md = plugin / "agents" / "demo-checker.md"
        agent_md.write_text(AGENT_SRC, encoding="utf-8")
        a_miss = check(OUT_HIT, agent_md)
        expect(any(gate == "F6" and lvl == "FAIL" and "priorities" in m.lower() for lvl, gate, m in a_miss), "agent source: F6 bites on the agent's own dropped heading (Priorities)")
        a_hit = check(AGENT_OUT, agent_md)
        expect(not any(gate == "F6" and lvl == "FAIL" for lvl, gate, _ in a_hit), "agent source: F6 passes when agent body + preloaded skill headings carried")
        expect(any(gate == "F6" and "agent" in m for lvl, gate, m in a_hit if lvl == "NOTE"), "agent source: kind reported as agent")
        ah1 = source_hash(agent_md)
        sib = Path(td) / "plug" / "agents" / "other.md"
        sib.write_text(AGENT_SRC.replace("demo-checker", "other"), encoding="utf-8")
        expect(source_hash(agent_md) == ah1 and len(ah1) == 12, "agent --hash: unaffected by a sibling agent file")
        (plugin / "skills" / "demo-source" / "SKILL.md").write_text(SRC_SKILL + "\nx\n", encoding="utf-8")
        expect(source_hash(agent_md) != ah1, "agent --hash: changes when a preload changes")
        (plugin / "skills" / "demo-source" / "SKILL.md").write_text(SRC_SKILL, encoding="utf-8")
        # cross-plugin preload resolved via the workspace sibling layout
        (Path(td) / "otherplug" / "skills" / "xskill").mkdir(parents=True)
        (Path(td) / "otherplug" / "skills" / "xskill" / "SKILL.md").write_text(SRC_SKILL.replace("demo-source", "xskill"), encoding="utf-8")
        agent_md.write_text(AGENT_SRC.replace("skills: [demo-source]", "skills: [demo-source, otherplug:xskill]"), encoding="utf-8")
        expect(not any(gate == "F6" and lvl == "FAIL" and "xskill" in m for lvl, gate, m in check(AGENT_OUT, agent_md)), "cross-plugin preload resolves via <workspace>/<plugin>/skills/<name>")
        (plugin / "skills" / "xskill").mkdir()
        (plugin / "skills" / "xskill" / "SKILL.md").write_text(SRC_SKILL, encoding="utf-8")
        agent_md.write_text(AGENT_SRC.replace("skills: [demo-source]", "skills: [demo-source, ghostplug:xskill]"), encoding="utf-8")
        expect(any(gate == "F6" and lvl == "FAIL" and "ghostplug:xskill" in m for lvl, gate, m in check(AGENT_OUT, agent_md)), "prefixed handle never falls back to a same-named LOCAL skill (false-PASS guard)")
        agent_md.write_text(AGENT_SRC.replace("skills: [demo-source]", "skills: [demo-source, ghost-skill]"), encoding="utf-8")
        expect(any(gate == "F6" and lvl == "FAIL" and "ghost-skill" in m for lvl, gate, m in check(AGENT_OUT, agent_md)), "agent source: unresolvable preload is an F6 FAIL")
        expect(any(gate == "F8" and "agent source" in m for lvl, gate, m in check(AGENT_OUT, agent_md) if lvl == "NOTE"), "agent source: F8 reports no-evals NOTE instead of silence")
        cmd_leak = check(AGENT_OUT.replace("## Priorities", "Seed: $ARGUMENTS\n\n## Priorities"), agent_md)
        expect(any(gate == "F3" and "ARGUMENTS" in m for lvl, gate, m in cmd_leak if lvl == "FAIL"), "$ARGUMENTS leaking into an export trips F3")
        expect(any(gate == "F2" for lvl, gate, _ in check(GOOD.replace("---\n# ds", "tools: Read, Grep\nskills: [x]\n---\n# ds"), None) if lvl == "FAIL"), "agent keys tools:/skills: trip F2")
        expect(not any(gate == "F4" for lvl, gate, _ in check(GOOD.replace("Use when the", "Invoke with `/ds-button-rules` when the"), None) if lvl == "FAIL"), "'Invoke with /name' counts as an active trigger (command-derived)")
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
        if len(argv) != 2 or not (Path(argv[1]).is_dir() or Path(argv[1]).is_file()):
            print("usage: --hash <source-skill-dir | agents/<name>.md>", file=sys.stderr)
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
    if src is not None and not (src.is_dir() or src.is_file()):
        print(f"usage error: --source does not exist: {src}", file=sys.stderr)
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
