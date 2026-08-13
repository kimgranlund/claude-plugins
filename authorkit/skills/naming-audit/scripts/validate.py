#!/usr/bin/env python3
"""authorkit validator — enforces the harness artifact naming convention.

Deterministic checks only: name grammar, folder layout, frontmatter schema,
relation graph, policy/capability coherence, provenance. Judgment (severity
interpretation, report narrative) belongs to the naming-audit skill, not here.

Usage:
  validate.py --target PATH [--manifest PATH] [--json] [--hook]

Exit codes: 0 clean (warnings allowed), 1 errors found, 2 no manifest
(--hook mode exits 0 on missing manifest: governance is opt-in per estate).
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(text):
    """Minimal YAML-subset parser: scalars, inline lists, block lists,
    folded scalars. No external dependency by design."""
    if not text.startswith("---"):
        return {}, "missing frontmatter block"
    lines = text.split("\n")
    end = None
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip() == "---":
            end = i
            break
    if end is None:
        return {}, "unterminated frontmatter block"
    fm, key = {}, None
    i = 1
    while i < end:
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if raw.startswith((" ", "\t")):
            if key is None:
                return {}, f"indented line without key: {stripped!r}"
            if stripped.startswith("- "):
                if not isinstance(fm[key], list):
                    fm[key] = []
                fm[key].append(_scalar(stripped[2:]))
            else:  # folded/continued scalar
                fm[key] = (str(fm[key]) + " " + stripped).strip()
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
        if not m:
            return {}, f"unparseable frontmatter line: {stripped!r}"
        key, val = m.group(1), m.group(2).strip()
        if val in (">", ">-", "|", "|-"):
            fm[key] = ""
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            fm[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        elif val == "":
            fm[key] = []  # block list or empty; block items fill it
        else:
            fm[key] = _scalar(val)
        i += 1
    return fm, None


def _scalar(v):
    v = v.strip().strip("'\"").split("  #")[0].strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v

# -------------------------------------------------------------------- grammar

class Grammar:
    def __init__(self, manifest):
        self.verb_lex = set(manifest.get("verb_lex", []))
        self.process_lex = set(manifest.get("process_lex", []))
        self.role_lex = set(manifest.get("role_lex", []))
        self.exemptions = set(manifest.get("exemptions", []))
        self.authors = set(manifest.get("author_registry", []))
        self.brand_tokens = set(manifest.get("brand_tokens", []))
        self.mutation_allowlist = set(manifest.get("mutating_no_confirm_allowlist", []))
        self.objects = {}       # any acceptable surface form -> canonical
        self.banned = {}        # banned alias -> canonical
        for entry in manifest.get("object_vocab", []):
            canon = entry["canonical"]
            self.objects[canon] = canon
            if entry.get("plural"):
                self.objects[entry["plural"]] = canon
            for alias in entry.get("banned_aliases", []):
                self.banned[alias] = canon
        overlap = self.verb_lex & self.process_lex
        self.lexicon_errors = (
            [f"VerbLex/ProcessLex disjointness violated: {sorted(overlap)}"]
            if overlap else []
        )

    def resolve_objects(self, tokens):
        """Greedy left-anchored longest-match of hyphen tokens against
        ObjectVocab. Returns (ok, unresolved_token_or_None)."""
        i = 0
        while i < len(tokens):
            matched = False
            for j in range(len(tokens), i, -1):  # longest first
                cand = "-".join(tokens[i:j])
                if cand in self.banned:
                    return False, f"banned alias {cand!r} (use {self.banned[cand]!r})"
                if cand in self.objects:
                    i, matched = j, True
                    break
            if not matched:
                return False, f"token {tokens[i]!r} resolves in no lexicon or vocab"
        return True, None

    def check_brand(self, tokens):
        hits = [t for t in tokens if t in self.brand_tokens]
        return f"brand token(s) in local name: {hits}" if hits else None

    def parse(self, kind, name, skills, wraps_target=None):
        """Returns list of grammar errors for this name."""
        errs = []
        tokens = name.split("-")
        brand = self.check_brand(tokens)
        if brand:
            errs.append(brand)

        if kind == "agent":
            if not name.endswith("-agent"):
                return errs + ["agent name must end in -agent"]
            residue = name[: -len("-agent")]
            if residue in skills:
                return errs  # primary production: agent-of-skill
            rtoks = residue.split("-")
            if len(rtoks) >= 2 and rtoks[-1] in self.role_lex:
                ok, why = self.resolve_objects(rtoks[:-1])
                return errs if ok else errs + [f"orchestrator scope: {why}"]
            return errs + [
                f"strip -agent -> {residue!r} is no extant skill and no "
                f"scope-role production (RoleLex: {sorted(self.role_lex)})"
            ]

        if kind == "command":
            # wrapper production: command name identical to its wrapped skill
            if wraps_target and name == wraps_target and name in skills:
                return errs
            if len(tokens) < 2:
                return errs + ["command needs object-verb shape (>= 2 tokens)"]
            verb = tokens[-1]
            if verb not in self.verb_lex:
                return errs + [
                    f"command terminal {verb!r} not in VerbLex "
                    f"{sorted(self.verb_lex)} (and name is not a wrapper "
                    f"identical to its wrapped skill)"
                ]
            ok, why = self.resolve_objects(tokens[:-1])
            return errs if ok else errs + [f"command object: {why}"]

        if kind == "skill":
            if tokens[-1] == "agent":
                return errs + ["reserved head -agent on a skill"]
            if len(tokens) >= 2 and tokens[-1] in self.process_lex:
                ok, why = self.resolve_objects(tokens[:-1])
                return errs if ok else errs + [f"skill object: {why}"]
            ok, why = self.resolve_objects(tokens)  # nominal production
            if ok:
                return errs
            return errs + [
                f"neither object-process (terminal not in ProcessLex "
                f"{sorted(self.process_lex)}) nor nominal ({why})"
            ]
        return errs + [f"unknown kind {kind!r}"]

# ------------------------------------------------------------ schema & policy

COMMON_REQUIRED = ["name", "kind", "description", "author", "created", "last_updated"]
COMMON_OPTIONAL = ["review_after"]
FIELDS = {
    "skill":   {"required": COMMON_REQUIRED,
                "optional": COMMON_OPTIONAL + ["requires", "allowed-tools"]},
    "command": {"required": COMMON_REQUIRED,
                "optional": COMMON_OPTIONAL + ["requires", "wraps", "mutates",
                                                "confirm", "allowed-tools",
                                                "argument-hint"]},
    "agent":   {"required": COMMON_REQUIRED + ["performs", "autonomous_write",
                                                "context", "tools"],
                "optional": COMMON_OPTIONAL + ["requires"]},
}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}


def tool_list(fm):
    raw = fm.get("allowed-tools", fm.get("tools", []))
    if isinstance(raw, str):
        raw = [t.strip() for t in raw.split(",")]
    return [t for t in raw if t]


def policy_checks(kind, fm, name):
    errs, warns = [], []
    tools = tool_list(fm)
    unscoped_bash = any(t == "Bash" for t in tools)
    writey = bool(WRITE_TOOLS & set(tools)) or unscoped_bash
    for t in tools:
        if t == "Bash":
            errs.append("unscoped Bash grant — scope it: Bash(pattern)")
    if kind == "agent":
        aw = fm.get("autonomous_write", False)  # fail closed
        if not isinstance(aw, bool):
            errs.append("autonomous_write must be boolean")
            aw = False
        if not aw and writey:
            errs.append("autonomous_write: false but write-capable tools granted")
        if fm.get("context") not in ("isolated", "inherited"):
            errs.append("context must be isolated|inherited")
    if kind == "command":
        mutates = fm.get("mutates", False)
        confirm = fm.get("confirm", "none")
        if mutates and confirm != "required" and name not in _grammar.mutation_allowlist:
            errs.append("mutates: true requires confirm: required (or allowlist entry)")
        if mutates and not writey:
            errs.append("mutates: true but no write-capable tool granted")
        if not mutates and writey:
            errs.append("mutates: false but write-capable tools granted")
    return errs, warns


def provenance_checks(fm, grammar):
    errs, warns = [], []
    if fm.get("author") not in grammar.authors:
        errs.append(f"author {fm.get('author')!r} not in AuthorRegistry")
    d = {}
    for f in ("created", "last_updated"):
        try:
            d[f] = date.fromisoformat(str(fm.get(f, "")))
        except ValueError:
            errs.append(f"{f} is not an ISO date: {fm.get(f)!r}")
    if len(d) == 2 and d["last_updated"] < d["created"]:
        errs.append("last_updated predates created")
    if "last_updated" in d:
        window = int(str(fm.get("review_after", "180d")).rstrip("d") or 180)
        if (date.today() - d["last_updated"]).days > window:
            warns.append(f"stale: last_updated exceeds {window}d review window")
    return errs, warns

# ----------------------------------------------------------- layout & indexes

ALLOWED_SKILL_ENTRIES = {"SKILL.md", "references", "scripts", "assets"}


def layout_checks(skill_dir):
    errs = []
    entries = [p.name for p in skill_dir.iterdir()]
    if "SKILL.md" not in entries:
        errs.append("SKILL.md missing")
    for e in entries:
        if e not in ALLOWED_SKILL_ENTRIES:
            errs.append(f"top-level entry outside closed set: {e!r}")
    for sub in skill_dir.rglob("SKILL.md"):
        if sub.parent != skill_dir:
            errs.append(f"nested skill at {sub.relative_to(skill_dir)}")
    return errs


def index_checks(skill_dir, body):
    """Every references/ file appears in the SKILL.md reference index; every
    index row points at an extant file."""
    errs = []
    refdir = skill_dir / "references"
    files = {p.name for p in refdir.iterdir() if p.is_file()} if refdir.is_dir() else set()
    rows = set()
    in_refs = False
    for ln in body.split("\n"):
        if re.match(r"^##\s+References\b", ln):
            in_refs = True
            continue
        if in_refs and ln.startswith("## "):
            in_refs = False
        if in_refs:
            m = re.match(r"^\|\s*`?([^|`]+?)`?\s*\|", ln)
            if m and m.group(1).strip().lower() not in ("file", "---", ":---"):
                cell = m.group(1).strip()
                if not set(cell) <= {"-", ":", " "}:
                    rows.add(cell)
    if files and not rows:
        errs.append("references/ populated but SKILL.md has no '## References' index")
    for f in files - rows:
        errs.append(f"references/{f} missing from reference index")
    for r in rows - files:
        errs.append(f"index row {r!r} points at no file in references/")
    return errs

# --------------------------------------------------------------------- runner

_grammar = None


def discover(target: Path):
    """Yield (kind, name, path, is_dir_artifact). Supports a plugin root or a
    repo with .claude/."""
    root = target / ".claude" if (target / ".claude").is_dir() else target
    for kind, sub in (("command", "commands"), ("agent", "agents")):
        d = root / sub
        if d.is_dir():
            for p in sorted(d.glob("*.md")):
                yield kind, p.stem, p, False
    sd = root / "skills"
    if sd.is_dir():
        for p in sorted(sd.iterdir()):
            if p.is_dir():
                yield "skill", p.name, p, True


def main():
    global _grammar
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--manifest")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hook", action="store_true",
                    help="no-op cleanly when target has no manifest")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    mpath = Path(args.manifest) if args.manifest else None
    if mpath is None:
        for cand in (target / "naming.manifest.json",
                     target / ".claude" / "naming.manifest.json"):
            if cand.is_file():
                mpath = cand
                break
    if mpath is None or not mpath.is_file():
        msg = "no naming.manifest.json found — estate is ungoverned"
        if args.hook:
            print(f"authorkit: {msg}; skipping (governance is opt-in)")
            sys.exit(0)
        print(f"authorkit: {msg}. Seed one via manifest-authoring.")
        sys.exit(2)

    manifest = json.loads(mpath.read_text())
    _grammar = g = Grammar(manifest)

    artifacts = list(discover(target))
    skills = {n for k, n, _, _ in artifacts if k == "skill"}
    findings = []          # (name, level, message)
    fms = {}               # name -> (kind, fm)

    for msg in g.lexicon_errors:
        findings.append(("manifest", "error", msg))

    for kind, name, path, is_dir in artifacts:
        md = path / "SKILL.md" if is_dir else path
        text = md.read_text() if md.is_file() else ""
        fm, fmerr = parse_frontmatter(text)
        body = text.split("---", 2)[2] if text.count("---") >= 2 else ""
        fms[name] = (kind, fm)
        exempt = name in g.exemptions

        def E(m): findings.append((name, "error", m))
        def W(m): findings.append((name, "warn", m))
        def X(m): findings.append((name, "exempt-note", m))

        # 1–2: grammar (exemptions skip; recorded for burn-down)
        errs = g.parse(kind, name, skills, wraps_target=fm.get("wraps"))
        for e in errs:
            (X if exempt else E)(e)

        # 3: folder/file == name; layout; index
        declared = fm.get("name")
        if declared != name:
            E(f"frontmatter name {declared!r} != {'folder' if is_dir else 'file'} name")
        if is_dir:
            for e in layout_checks(path):
                E(e)
            for e in index_checks(path, body):
                E(e)

        # 4: frontmatter schema
        if fmerr:
            E(fmerr)
            continue
        spec = FIELDS[kind]
        for f in spec["required"]:
            if f not in fm:
                E(f"required field missing: {f}")
        allowed = set(spec["required"]) | set(spec["optional"])
        for f in fm:
            if f not in allowed:
                E(f"field outside schema for kind={kind}: {f}")
        if fm.get("kind") != kind:
            E(f"declared kind {fm.get('kind')!r} != decided kind {kind!r} (directory)")

        # 6: policy & grants
        pe, pw = policy_checks(kind, fm, name)
        for e in pe: E(e)
        for w in pw: W(w)

        # 7: provenance
        ve, vw = provenance_checks(fm, g)
        for e in ve: E(e)
        for w in vw: W(w)

    # 5: relation graph
    names = set(fms)
    for name, (kind, fm) in fms.items():
        def E(m): findings.append((name, "error", m))
        if kind == "agent":
            perf = fm.get("performs")
            if perf and name.endswith("-agent") and perf != name[:-6]:
                E(f"performs {perf!r} != name minus -agent")
            if perf and perf not in skills:
                E(f"performs target {perf!r} is no extant skill")
        if kind == "command":
            w = fm.get("wraps")
            if w and w not in skills:
                E(f"wraps target {w!r} is no extant skill")
        reqs = fm.get("requires", [])
        if isinstance(reqs, str):
            reqs = [reqs]
        for r in reqs:
            if r not in names:
                E(f"requires target {r!r} does not exist")
    # acyclicity over requires
    edges = {}
    for name, (_, fm) in fms.items():
        reqs = fm.get("requires", [])
        edges[name] = [reqs] if isinstance(reqs, str) else list(reqs)
    state = {}
    def dfs(n, trail):
        state[n] = 1
        for m in edges.get(n, []):
            if state.get(m) == 1:
                findings.append((n, "error", f"requires cycle: {' -> '.join(trail + [m])}"))
            elif state.get(m, 0) == 0 and m in edges:
                dfs(m, trail + [m])
        state[n] = 2
    for n in edges:
        if state.get(n, 0) == 0:
            dfs(n, [n])

    errors = [f for f in findings if f[1] == "error"]
    warns = [f for f in findings if f[1] == "warn"]
    exemption_notes = [f for f in findings if f[1] == "exempt-note"]

    if args.json:
        print(json.dumps({
            "target": str(target), "manifest": str(mpath),
            "artifacts": len(artifacts), "errors": errors, "warnings": warns,
            "exemption_burndown": {"count": len(g.exemptions),
                                    "notes": exemption_notes},
        }, indent=2))
    else:
        print(f"authorkit validate — {len(artifacts)} artifacts @ {target}")
        for name, lvl, msg in findings:
            tag = {"error": "ERROR", "warn": "WARN ", "exempt-note": "EXMPT"}[lvl]
            print(f"  [{tag}] {name}: {msg}")
        print(f"  errors={len(errors)} warnings={len(warns)} "
              f"exemptions={len(g.exemptions)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
