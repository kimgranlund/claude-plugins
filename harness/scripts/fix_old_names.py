#!/usr/bin/env python3
"""fix_old_names — rewrite retired plugin/skill/agent names in a CONSUMER repo, from a manifest.

A rename wave inside this workspace is invisible to every repo that merely INSTALLS these
plugins. Those repos keep the old handles in their own `.claude/**`, `CLAUDE.md`, and docs, and
every one of them fails SILENTLY: a retired agent name errors only at dispatch time, and a
description citing a retired skill mis-routes with no diagnostic at all.

Usage:
  fix_old_names.py <repo-root> [--manifest P] [--historical GLOB] [--include-memory] [--json]
                                     REPORT only. Exit 1 if any LIVE stale name remains, so a
                                     consumer repo can wire this straight in as a CI gate.
  fix_old_names.py <repo-root> --write [...]
                                     same scan, then rewrite the LIVE hits in place
  fix_old_names.py derive <plugins-repo-root> [--out P]
                                     regenerate the manifest from git rename detection
  fix_old_names.py selftest          prove the counters bite

Report-only is the DEFAULT, deliberately: the first real run against a consumer repo classified
542 hits, and which of them were records rather than pointers was not knowable from this side of
the repo boundary. A tool that rewrites hundreds of a stranger's files on a bare invocation is
the wrong shape; `--write` is one word, and a human reads the report first.

What it asserts:
  L1 [FAIL] a LIVE reference to a retired name -> rewrite (or, under --check, a finding)
  L2 [warn] an AMBIGUOUS retired name in free prose -> reported with both candidates, never
            rewritten; only a typed slot (a `skills:` item, a subagent_type, a /command) picks
  L3 [ ok ] a HISTORICAL reference (ADR body, changelog, ledger, dated record) -> left byte-identical
  L4 [warn] a retired name appearing as a FILENAME or path component -> reported, never rewritten;
            the consumer repo's own file was not renamed, so a rewrite points at nothing

The LIVE/HISTORICAL split is the whole safety story. A record of what WAS true must keep saying
what it said; only a pointer that must still RESOLVE gets rewritten. When the two are ambiguous
this script leaves the text alone and says so — a silent wrong rewrite of a decision record is
worse than a stale pointer a human can see in the report.

Exit 0 clean · 1 findings (check mode) or a write failure · 2 usage error.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".toml", ".txt"}

# Paths whose entire contents are a record of what WAS, never a pointer that must resolve.
# Whole directories whose contents are a dated log of what HAPPENED, not a pointer that must
# still resolve. Calibrated against a real consumer repo (agent-ui, 2026-07-26): of 542 first-pass
# hits, 322 sat in decomposition manifests, tickets and reports — records every one.
HISTORICAL_PATH_PARTS = ("adr", "adrs", "decisions", ".refactor-attic", "dist", ".git",
                         "archive", "archives", "attic", "legacy", "snapshots", "retros",
                         "decompositions", "tickets", "reports", "sessions")
HISTORICAL_NAME_RE = re.compile(r"^(changelog|history)", re.I)

# A heading that opens a block of historical content inside an otherwise-live file
# (README footer ledgers, a ticket's Findings log, a transition table).
HISTORICAL_HEADING_RE = re.compile(
    r"^(#{1,6})\s+.*\b(history|ledger|changelog|transition|findings|version history|"
    r"superseded|previously|migration log)\b", re.I)

# An explicit human freeze marker — the escape hatch when the heuristics disagree with intent.
FREEZE_RE = re.compile(r"<!--\s*fix-old-names:\s*keep\s*-->", re.I)

DEFAULT_SCAN = (".claude", "CLAUDE.md", "docs", "AGENTS.md", ".github")


# ---------------------------------------------------------------- manifest

def load_manifest(path: Path) -> dict:
    m = json.loads(path.read_text(encoding="utf-8"))
    if m.get("schema") != "renames/v1":
        raise ValueError(f"{path}: unknown manifest schema {m.get('schema')!r}")
    return m


class Index:
    """Compiled once per run. One combined alternation finds every candidate in a single pass
    per line — compiling 288 patterns per line instead made a real consumer repo time out."""

    def __init__(self, manifest: dict):
        self.by_old = {}
        for e in manifest["renames"]:
            self.by_old.setdefault(e["old"], []).append(e)
        for es in self.by_old.values():
            targets = {(e["new_plugin"], e["new"]) for e in es}
            kinds = {e["kind"] for e in es}
            for e in es:
                e["_ambiguous"] = len(targets) > 1 and len(kinds) > 1
        # longest first so `ops-issues` wins over a hypothetical `ops`
        names = sorted(self.by_old, key=len, reverse=True)
        self.combined = re.compile(
            r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(n) for n in names)
            + r")(?![A-Za-z0-9_-])") if names else None
        self.plugin_suffix = re.compile(r"(?<![A-Za-z0-9_-])([A-Za-z0-9_-]+):$")


# ---------------------------------------------------------------- classification

def is_historical_path(rel: Path, extra_globs=()) -> bool:
    parts = [p.lower() for p in rel.parts]
    if any(p in HISTORICAL_PATH_PARTS for p in parts):
        return True
    if any(rel.match(g) for g in extra_globs):
        return True
    return bool(HISTORICAL_NAME_RE.match(rel.name))


def historical_lines(text: str) -> set:
    """Line indices (0-based) inside a historical block or carrying a freeze marker."""
    out, open_level = set(), None
    for i, line in enumerate(text.splitlines()):
        if FREEZE_RE.search(line):
            out.add(i)
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            level = len(m.group(1))
            if HISTORICAL_HEADING_RE.match(line):
                open_level = level
                out.add(i)
                continue
            if open_level is not None and level <= open_level:
                open_level = None
        if open_level is not None:
            out.add(i)
    return out


SLOT_SKILL_RE = re.compile(r"^\s*-\s|^\s*skills\s*:|/(?P<cmd>[a-z][a-z0-9-]*)\b")
SLOT_AGENT_RE = re.compile(r"subagent_type|agent[s]?\s*:|Task\(|Agent\(", re.I)

# A retired skill name is ALSO, in some consumer repo, the name of a file. Rewriting it there
# breaks a working link and points at nothing — strictly worse than the stale prose it was
# fixing. Incident 2026-07-26 (agent-ui, live): `a2ui-training-corpus` is a retired skill AND
# `.claude/docs/spec/a2ui-training-corpus.spec.md` on disk; the first real sweep rewrote both
# markdown link targets to a file that does not exist. Two lexical shapes prove a path:
FILE_EXT_AFTER_RE = re.compile(r"^\.[A-Za-z0-9]{1,6}\b")   # name.md, name.spec.md, name.json
PATH_SEP_BEFORE_RE = re.compile(r"[/\\]$")                  # dir/name, ../spec/name


def looks_like_path(line: str, start: int, end: int) -> bool:
    """True when this match is a filename or path component rather than a handle."""
    return bool(FILE_EXT_AFTER_RE.match(line[end:]) or PATH_SEP_BEFORE_RE.search(line[:start]))


def slot_kind(line: str, in_skills_block: bool):
    """Which kind does this line's SHAPE prove? None when only prose context is available."""
    if SLOT_AGENT_RE.search(line):
        return "agent"
    if in_skills_block or re.search(r"^\s*skills\s*:", line) or re.search(r"(?<![\w])/[a-z]", line):
        return "skill"
    return None


def skills_block_mask(text: str) -> set:
    """Lines belonging to a frontmatter `skills:` list — a typed slot the shape alone proves."""
    out, active = set(), False
    for i, line in enumerate(text.splitlines()):
        if re.match(r"^\s*skills\s*:", line):
            active = True
            out.add(i)
            continue
        if active:
            if re.match(r"^\s*-\s", line):
                out.add(i)
                continue
            active = False
    return out


# ---------------------------------------------------------------- scan

class Hit:
    __slots__ = ("path", "line", "col", "old", "new", "status", "note", "span")

    def __init__(self, path, line, col, old, new, status, note, span):
        self.path, self.line, self.col = path, line, col
        self.old, self.new, self.status, self.note, self.span = old, new, status, note, span


def scan_text(rel: Path, text: str, idx: Index, hist_globs=()):
    """Return hits. status: 'live' (rewrite), 'ambiguous' (report), 'historical' (leave)."""
    hits = []
    if idx.combined is None or not idx.combined.search(text):
        return hits          # whole-file bail before the per-line masks — most files match nothing
    hist_path = is_historical_path(rel, hist_globs)
    hist_lines = set() if hist_path else historical_lines(text)
    skills_lines = skills_block_mask(text)

    for i, line in enumerate(text.splitlines()):
        if not idx.combined.search(line):
            continue
        historical = hist_path or i in hist_lines
        kind_hint = slot_kind(line, i in skills_lines)

        for m in idx.combined.finditer(line):
            old_name = m.group(1)
            entries = idx.by_old[old_name]
            start, end = m.start(1), m.end(1)

            if looks_like_path(line, start, end):
                hits.append(Hit(rel, i + 1, start, old_name, None,
                                "historical" if historical else "path",
                                "a filename or path component, not a handle — a rewrite here "
                                "would point at a file that does not exist", (start, end)))
                continue

            # A `oldplugin:` immediately before the name makes the reference QUALIFIED —
            # unambiguous, and the only way a plugin-PREFIX-only rename is visible at all
            # (the name never changed; only which plugin owns it did).
            pm = idx.plugin_suffix.search(line[:start])
            if pm:
                qual = [e for e in entries if e["old_plugin"] == pm.group(1)]
                if qual:
                    e = qual[0]
                    new_txt = f'{e["new_plugin"]}:{e["new"]}'
                    old_txt = line[pm.start(1):end]
                    if old_txt != new_txt:
                        note = (f'{e["kind"]} moved {e["old_plugin"]}->{e["new_plugin"]}'
                                if e["old"] == e["new"] else e["kind"])
                        hits.append(Hit(rel, i + 1, pm.start(1), old_txt, new_txt,
                                        "historical" if historical else "live", note,
                                        (pm.start(1), end)))
                    continue

            # Bare form — only entries the manifest marks token-safe may match unqualified.
            safe = [e for e in entries if e["match"] == "token"]
            if not safe:
                continue
            if any(e["_ambiguous"] for e in safe):
                typed = [e for e in safe if e["kind"] == kind_hint] if kind_hint else []
                if len(typed) != 1:
                    alts = " | ".join(f'{e["new_plugin"]}:{e["new"]} ({e["kind"]})' for e in safe)
                    hits.append(Hit(rel, i + 1, start, old_name, None,
                                    "historical" if historical else "ambiguous",
                                    f"kind not provable from context -> {alts}", (start, end)))
                    continue
                safe = typed
            e = safe[0]
            hits.append(Hit(rel, i + 1, start, old_name, e["new"],
                            "historical" if historical else "live", e["kind"], (start, end)))
    return hits


def rewrite(text: str, hits) -> str:
    """Apply only the LIVE hits, right-to-left per line so spans stay valid."""
    lines = text.splitlines(keepends=True)
    by_line = {}
    for h in hits:
        if h.status == "live" and h.new:
            by_line.setdefault(h.line, []).append(h)
    for ln, hs in by_line.items():
        raw = lines[ln - 1]
        for h in sorted(hs, key=lambda x: x.span[0], reverse=True):
            raw = raw[:h.span[0]] + h.new + raw[h.span[1]:]
        lines[ln - 1] = raw
    return "".join(lines)


def iter_targets(root: Path, extra=()):
    seen = []
    for name in list(DEFAULT_SCAN) + list(extra):
        p = root / name
        if p.is_file():
            seen.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES:
                    seen.append(f)
    return seen


def memory_dir(root: Path) -> Path:
    """Claude Code's per-project memory lives outside the repo, keyed by an escaped abs path."""
    slug = str(root.resolve()).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug / "memory"


# ---------------------------------------------------------------- run

def run(root: Path, manifest_path: Path, write: bool, include_memory: bool, as_json: bool,
        hist_globs=()):
    idx = Index(load_manifest(manifest_path))
    targets = iter_targets(root)
    extra_root = None
    if include_memory:
        md = memory_dir(root)
        if md.is_dir():
            extra_root = md
            targets += [f for f in sorted(md.rglob("*"))
                        if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES]

    all_hits, changed = [], []
    for f in targets:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        base = extra_root if (extra_root and extra_root in f.parents) else root
        rel = f.relative_to(base)
        hits = scan_text(rel, text, idx, hist_globs)
        if not hits:
            continue
        all_hits += hits
        if write and any(h.status == "live" for h in hits):
            new_text = rewrite(text, hits)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                changed.append(rel)

    live = [h for h in all_hits if h.status == "live"]
    amb = [h for h in all_hits if h.status == "ambiguous"]
    hist = [h for h in all_hits if h.status == "historical"]
    paths = [h for h in all_hits if h.status == "path"]

    if as_json:
        print(json.dumps({
            "live": [{"file": str(h.path), "line": h.line, "old": h.old, "new": h.new} for h in live],
            "ambiguous": [{"file": str(h.path), "line": h.line, "old": h.old, "note": h.note} for h in amb],
            "paths": [{"file": str(h.path), "line": h.line, "old": h.old} for h in paths],
            "historical_left": len(hist),
            "changed_files": [str(c) for c in changed],
        }, indent=2))
    else:
        verdict = ("rewritten" if write and live else
                   "FAIL" if live else ("warn" if (amb or paths) else "clean"))
        print(f"fix_old_names · {verdict} · {len(live)} fail / {len(amb) + len(paths)} warn")
        for h in live:
            arrow = f"{h.old} -> {h.new}"
            print(f"  {'FIXED' if write else 'FOUND'} L1  {h.path}:{h.line}  {arrow}  [{h.note}]")
        for h in amb:
            print(f"  WARN  L2  {h.path}:{h.line}  {h.old}  {h.note}")
        for h in paths:
            print(f"  WARN  L4  {h.path}:{h.line}  {h.old}  {h.note}")
        print(f"  ok    L3  {len(hist)} historical reference(s) left byte-identical "
              f"(ADR bodies, ledgers, changelogs, dated records)")
        if changed:
            print(f"  {len(changed)} file(s) rewritten")
        if amb:
            print("  -> ambiguous names need a human: the same retired name became a command "
                  "AND an agent; only you know which one each mention meant.")
        if live and not write:
            print("  -> report only. Re-run with --write to apply, after reading the list above.")

    return 1 if (live and not write) else 0


# ---------------------------------------------------------------- derive

def _parse_member_path(p: str):
    parts = p.split("/")
    if len(parts) < 3:
        return None
    plugin = re.sub(r"\s+[\d.]+$", "", parts[0]).strip()
    if parts[1] == "skills" and parts[-1] == "SKILL.md":
        return (plugin, "skill", parts[2])
    if parts[1] == "agents" and parts[-1].endswith(".md"):
        return (plugin, "agent", parts[-1][:-3])
    return None


def derive(repo: Path, out: Path):
    """Regenerate the manifest from git rename detection — the only record that cannot drift
    from what actually shipped (the per-plugin transition TABLES were retired as stale in
    2026-07-25's v1.0.5 sweep; prose was never a durable source)."""
    r = subprocess.run(
        ["git", "log", "--all", "-M", "-C", "--diff-filter=R", "--name-status",
         "--format=@@%h", "--", "*/SKILL.md", "*/agents/*.md"],
        cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"fix_old_names · FAIL · git log failed: {r.stderr.strip()[:200]}")
        return 1

    order = []
    for line in r.stdout.splitlines():
        if not line.startswith("R"):
            continue
        f = line.split("\t")
        if len(f) != 3:
            continue
        a, b = _parse_member_path(f[1]), _parse_member_path(f[2])
        if a and b and a != b:
            order.append((a, b))
    order.reverse()                      # git log is newest-first; chains resolve forward
    chain = dict(order)

    def resolve(t):
        seen = set()
        while t in chain and t not in seen:
            seen.add(t)
            t = chain[t]
        return t

    live = set()
    for pd in sorted(repo.iterdir()):
        if not (pd / ".claude-plugin" / "plugin.json").is_file():
            continue
        if (pd / "skills").is_dir():
            live |= {(pd.name, "skill", s.parent.name) for s in (pd / "skills").glob("*/SKILL.md")}
        if (pd / "agents").is_dir():
            live |= {(pd.name, "agent", a.stem) for a in (pd / "agents").glob("*.md")}

    live_names = {t[2] for t in live}
    renames = []
    for src in sorted(chain):
        dst = resolve(src)
        if src == dst or dst not in live:
            continue
        old_name, new_name = src[2], dst[2]
        # `token` only when the bare old name cannot be mistaken for something still current:
        # an unchanged name (a plugin-PREFIX-only move), a name still live elsewhere, or a
        # single bare word are all qualified-only. This is the rule that keeps a sweep from
        # rewriting the English word "build" or clobbering a correct current name.
        match = "qualified" if (old_name == new_name
                                or old_name in live_names
                                or "-" not in old_name) else "token"
        renames.append({
            "old": old_name, "new": new_name, "kind": src[1],
            "old_plugin": src[0], "new_plugin": dst[0], "match": match,
        })

    plugins = {}
    for e in renames:
        if e["old_plugin"] != e["new_plugin"]:
            plugins[e["old_plugin"]] = e["new_plugin"]

    manifest = {
        "schema": "renames/v1",
        "generated_by": "harness/scripts/fix_old_names.py derive",
        "source": "git rename detection over */SKILL.md and */agents/*.md, chained to final",
        "plugins": dict(sorted(plugins.items())),
        "renames": sorted(renames, key=lambda e: (e["old_plugin"], e["kind"], e["old"])),
    }
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tok = sum(1 for e in renames if e["match"] == "token")
    print("fix_old_names · derived · 0 fail / 0 warn")
    print(f"  {len(renames)} renames ({tok} token-safe, {len(renames) - tok} qualified-only), "
          f"{len(plugins)} plugin moves -> {out}")
    return 0


# ---------------------------------------------------------------- selftest

MANIFEST_FIXTURE = {
    "schema": "renames/v1",
    "plugins": {"forge": "harness", "color": "design"},
    "renames": [
        {"old": "intent-extract", "new": "find-the-ask", "kind": "skill",
         "old_plugin": "forge", "new_plugin": "harness", "match": "token"},
        {"old": "token-builder", "new": "token-builder", "kind": "agent",
         "old_plugin": "color", "new_plugin": "design", "match": "qualified"},
        {"old": "build", "new": "build-feature", "kind": "skill",
         "old_plugin": "orchestration", "new_plugin": "teamwork", "match": "qualified"},
        {"old": "ops-issues", "new": "sort-issues", "kind": "skill",
         "old_plugin": "forge", "new_plugin": "harness", "match": "token"},
        {"old": "ops-issues", "new": "issue-sorter", "kind": "agent",
         "old_plugin": "forge", "new_plugin": "harness", "match": "token"},
    ],
}


def selftest():
    import tempfile
    idx = Index(json.loads(json.dumps(MANIFEST_FIXTURE)))

    def scan(rel, text):
        return scan_text(Path(rel), text, idx)

    # L1 negative control — a live token rename must bite, and rewrite.
    t = "Ambiguous ask -> `intent-extract` before acting.\n"
    h = scan("CLAUDE.md", t)
    assert [x for x in h if x.status == "live" and x.new == "find-the-ask"], f"L1 must fire: {h}"
    assert "find-the-ask" in rewrite(t, h) and "intent-extract" not in rewrite(t, h)

    # L1 prefix-only control — the exact class the 2026-07-26 automated pass MISSED. The skill
    # name never changed; only its plugin did, so a name->name map has no entry at all.
    t2 = "preload: color:token-builder for ramps\n"
    h2 = scan("x.md", t2)
    assert [x for x in h2 if x.status == "live" and x.new == "design:token-builder"], \
        f"a plugin-prefix-only rename must be caught: {h2}"
    assert rewrite(t2, h2).strip().endswith("design:token-builder for ramps")

    # FALSE-POSITIVE control — a qualified-only entry must NEVER touch the bare English word.
    t3 = "We build the thing, then build it again. A build is a build.\n"
    h3 = scan("README.md", t3)
    assert not h3, f"a qualified-only entry must not match bare prose: {h3}"
    assert rewrite(t3, h3) == t3, "byte-identical or the safety story is a lie"

    # ...but the qualified form of that same entry must still be caught.
    h3b = scan("x.md", "see orchestration:build for the flow\n")
    assert [x for x in h3b if x.new == "teamwork:build-feature"], f"qualified form must fire: {h3b}"

    # L3 reverse control — a historical record must come back byte-identical, both ways it
    # can be historical: by PATH...
    t4 = "ADR-0006 renamed `intent-extract` to find-the-ask.\n"
    h4 = scan(".claude/docs/adr/0006-naming.md", t4)
    assert h4 and all(x.status == "historical" for x in h4), f"ADR path must be historical: {h4}"
    assert rewrite(t4, h4) == t4, "an ADR body must never be rewritten"

    # ...and by BLOCK inside an otherwise-live file.
    t5 = ("# Guide\n\nUse `intent-extract` today.\n\n"
          "## Version history\n\n- 1.0.0: renamed `intent-extract`\n")
    h5 = scan("README.md", t5)
    live5 = [x for x in h5 if x.status == "live"]
    hist5 = [x for x in h5 if x.status == "historical"]
    assert len(live5) == 1 and live5[0].line == 3, f"body hit must be live: {h5}"
    assert len(hist5) == 1 and hist5[0].line == 7, f"ledger hit must be historical: {h5}"
    out5 = rewrite(t5, h5)
    assert "Use `find-the-ask` today" in out5, "the live pointer must be fixed"
    assert "1.0.0: renamed `intent-extract`" in out5, "the ledger line must survive verbatim"

    # freeze marker
    t6 = "quoting `intent-extract` verbatim <!-- fix-old-names: keep -->\n"
    h6 = scan("x.md", t6)
    assert all(x.status == "historical" for x in h6), f"freeze marker must protect: {h6}"

    # L4 PATH guard — the live incident, 2026-07-26 (agent-ui). `intent-extract` stands in for
    # `a2ui-training-corpus`: a retired skill name that is ALSO a real file on disk in the
    # consumer repo. The first sweep rewrote both markdown link targets to a file that does not
    # exist — a broken link is strictly worse than the stale prose it replaced.
    incident = ("> Implements: [`../spec/intent-extract.spec.md`](../spec/intent-extract.spec.md)\n"
                "and `specs/intent-extract.spec.md` (R10-R12).\n")
    hi = scan("x.md", incident)
    assert hi and all(x.status == "path" for x in hi), \
        f"every hit inside a path/filename must be status=path, got {[(x.old, x.status) for x in hi]}"
    assert rewrite(incident, hi) == incident, \
        "the exact incident repro: a filename must come back byte-identical"

    # ...and the reverse control — a bare handle on the SAME name must still be rewritten, or the
    # guard has simply disabled the check.
    hr = scan("x.md", "Ambiguous ask -> `intent-extract` before acting.\n")
    assert [x for x in hr if x.status == "live"], f"a real handle must still be live: {hr}"

    # both path shapes independently
    assert all(x.status == "path" for x in scan("x.md", "see docs/intent-extract for more\n")), \
        "a path SEPARATOR before the name proves a path"
    assert all(x.status == "path" for x in scan("x.md", "the intent-extract.json config\n")), \
        "an EXTENSION after the name proves a filename"

    # L2 ambiguity — same retired name became a command AND an agent. Free prose: report only.
    t7 = "The ops-issues seat handles intake.\n"
    h7 = scan("x.md", t7)
    assert h7 and all(x.status == "ambiguous" for x in h7), f"must be ambiguous in prose: {h7}"
    assert rewrite(t7, h7) == t7, "an ambiguous name must never be silently rewritten"
    assert "sort-issues" in h7[0].note and "issue-sorter" in h7[0].note, \
        "the report must name BOTH candidates or a human cannot resolve it"

    # ...but a TYPED SLOT proves the kind, so it resolves.
    t8 = "skills:\n  - ops-issues\n"
    h8 = scan("agent.md", t8)
    assert [x for x in h8 if x.status == "live" and x.new == "sort-issues"], \
        f"a skills: slot must resolve to the skill: {h8}"
    t9 = 'Task(subagent_type="ops-issues")\n'
    h9 = scan("x.md", t9)
    assert [x for x in h9 if x.status == "live" and x.new == "issue-sorter"], \
        f"a subagent_type slot must resolve to the agent: {h9}"

    # end-to-end + idempotence: a second pass over the swept tree must find nothing left.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".claude" / "agents").mkdir(parents=True)
        (root / ".claude" / "docs" / "adr").mkdir(parents=True)
        (root / ".claude" / "agents" / "orchestrator.md").write_text(
            "---\nskills:\n  - intent-extract\n---\nUse color:token-builder.\n")
        adr = "ADR: we renamed intent-extract.\n"
        (root / ".claude" / "docs" / "adr" / "0006.md").write_text(adr)
        (root / "CLAUDE.md").write_text("Route via `intent-extract`.\n")
        mf = root / "m.json"
        mf.write_text(json.dumps(MANIFEST_FIXTURE))

        assert run(root, mf, False, False, False) == 1, "report mode must exit 1 on live stale refs"
        assert (root / "CLAUDE.md").read_text() == "Route via `intent-extract`.\n", \
            "report mode must not have written anything — that is the whole default-safety claim"
        assert run(root, mf, True, False, False) == 0, "--write sweep must succeed"
        assert run(root, mf, False, False, False) == 0, "re-check must reach ZERO live hits"
        assert (root / ".claude" / "docs" / "adr" / "0006.md").read_text() == adr, \
            "the ADR must be byte-identical after a full sweep"
        body = (root / ".claude" / "agents" / "orchestrator.md").read_text()
        assert "- find-the-ask" in body and "design:token-builder" in body, body

    print("fix_old_names selftest · PASS · live rewrite + prefix-only catch, qualified-only "
          "never touches bare prose, ADR/ledger/freeze left byte-identical, ambiguity reported "
          "not guessed, typed slots resolve, filenames/paths never rewritten (the 2026-07-26 "
          "broken-link incident), sweep idempotent to zero")
    return 0


# ---------------------------------------------------------------- cli

def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selftest":
        return selftest()

    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("target")
    ap.add_argument("--manifest")
    ap.add_argument("--out")
    ap.add_argument("--write", action="store_true",
                    help="apply the rewrites; without it this only reports")
    ap.add_argument("--include-memory", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--historical", action="append", default=[], metavar="GLOB",
                    help="treat matching paths as records, never rewrite (repeatable)")
    try:
        a = ap.parse_args(argv[1:] if argv[0] == "derive" else argv)
    except SystemExit:
        print(__doc__)
        return 2

    if argv[0] == "derive":
        repo = Path(a.target).resolve()
        out = Path(a.out).resolve() if a.out else repo / "harness" / "renames.json"
        return derive(repo, out)

    root = Path(a.target).resolve()
    if not root.is_dir():
        print(f"fix_old_names · usage · not a directory: {root}")
        return 2
    mf = Path(a.manifest).resolve() if a.manifest else Path(__file__).resolve().parent.parent / "renames.json"
    if not mf.is_file():
        print(f"fix_old_names · usage · manifest not found: {mf}")
        return 2
    return run(root, mf, a.write, a.include_memory, a.json, tuple(a.historical))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
