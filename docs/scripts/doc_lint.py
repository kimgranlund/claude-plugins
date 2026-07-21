#!/usr/bin/env python3
"""doc_lint — structural validation for functional documents (the docs plugin's check tier).

Usage:
  doc_lint.py <file.md> [...]      lint documents (files without `doc-type:` frontmatter are skipped)
  doc_lint.py --hook               hook mode: read {"tool_input":{"file_path":...}} from stdin;
                                   silent pass for non-documents; emits a block decision on findings
  doc_lint.py selftest             prove the counters bite

Rules ("no validator, no type" — Vol 3 §3.1):
  T1 [FAIL] frontmatter parses and carries doc-type, id, status
  T2 [FAIL] doc-type is one of the eight; status is in that type's enum
  T3 [FAIL] required sections for the type present as `## ` headings
  T4 [FAIL] ledger protection (hook mode): editing a file whose COMMITTED (HEAD) version is an
            accepted ADR — supersede, never edit. Refined 2026-07-15: a new/untracked ADR, or one
            still `proposed` in HEAD, may be authored and ratified (the proposed->accepted flip is
            the ratification act, not a forgery); the append-only guarantee protects history.
            git absent / not a repo / any doubt -> conservative block, as before.
  T5 [WARN] plan steps without a done-when token; spec Requirements without REQ- IDs
"""
import json
import re
import sys
from pathlib import Path

TYPES = {
    "adr":     {"status": {"proposed", "accepted", "superseded"}, "sections": ["Context", "Decision", "Consequences"]},
    "prd":     {"status": {"draft", "approved", "superseded"},    "sections": ["Problem", "Users", "Outcomes", "Non-goals"]},
    "spec":    {"status": {"draft", "approved", "superseded"},    "sections": ["Requirements", "Non-goals", "Examples", "Acceptance"]},
    "lld":     {"status": {"draft", "approved", "superseded"},    "sections": ["Components", "Interfaces", "Data", "Risks"]},
    "plan":    {"status": {"active", "complete", "abandoned"},    "sections": ["Steps", "Validation", "Rollback"]},
    "roadmap": {"status": {"active", "retired"},                  "sections": ["Now", "Next", "Later"]},
    "ticket":  {"status": {"open", "doing", "done", "wontfix"},   "sections": ["Summary", "Acceptance", "Links"]},
    "task":    {"status": {"todo", "doing", "done"},              "sections": ["Goal", "Done-when"]},
}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = {}
    for line in parts[1].splitlines():
        m = re.match(r"^([\w-]+):\s*(.*?)(\s+#.*)?$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def lint_text(text):
    fm = parse_frontmatter(text)
    if fm is None or "doc-type" not in fm:
        return None  # not a functional document; not ours to judge
    findings = []
    dtype = fm.get("doc-type", "")
    spec = TYPES.get(dtype)
    if spec is None:
        return [("FAIL", "T2", f"doc-type `{dtype}` is not one of {sorted(TYPES)}")]
    for field in ("id", "status"):
        if not fm.get(field):
            findings.append(("FAIL", "T1", f"frontmatter missing `{field}` -> code cannot read this document's state"))
    status = fm.get("status", "")
    if status and status not in spec["status"]:
        findings.append(("FAIL", "T2", f"status `{status}` -> {dtype} takes {sorted(spec['status'])}"))
    heads = set(re.findall(r"^##\s+(.+?)\s*$", text, re.M))
    for sec in spec["sections"]:
        if sec not in heads:
            findings.append(("FAIL", "T3", f"required section `## {sec}` missing -> the template is the contract"))
    if dtype == "plan" and "Steps" in heads and "done-when" not in text.lower():
        findings.append(("WARN", "T5", "no `done-when` found in the plan -> steps without one are guesses"))
    if dtype == "spec" and "Requirements" in heads and not re.search(r"\bREQ-\d+", text):
        findings.append(("WARN", "T5", "no REQ- IDs in the spec -> the ID spine starts here"))
    return findings


def render(path, findings):
    if findings is None:
        print(f"doc_lint · not a functional document · {path}")
        return 0
    verdict = "FAIL" if any(f[0] == "FAIL" for f in findings) else ("warn" if findings else "clean")
    print(f"doc_lint · {verdict} · {path}")
    for sev, code, msg in findings:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if verdict == "FAIL" else 0


def head_is_accepted_adr(p: Path) -> bool:
    """T4's scope test (refined 2026-07-15): the ledger protection guards COMMITTED history.
    True (block) when the file's HEAD version is an accepted ADR; False (allow) when the file
    is new/untracked or still `proposed` in HEAD — authoring and the proposed->accepted
    ratification flip are legal acts on an uncommitted ledger entry. git absent, not a repo,
    or any failure -> True (conservative block, the pre-refinement behavior)."""
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, cwd=p.parent, timeout=10)
        if r.returncode != 0:
            return True
        top = Path(r.stdout.strip())
        rel = p.resolve().relative_to(top.resolve())
        r = subprocess.run(["git", "show", f"HEAD:{rel.as_posix()}"], capture_output=True,
                           text=True, cwd=top, timeout=10)
        if r.returncode != 0:
            return False  # not in HEAD: a new ledger entry, not history
        head_fm = parse_frontmatter(r.stdout)
        return bool(head_fm and head_fm.get("doc-type") == "adr"
                    and head_fm.get("status") == "accepted")
    except Exception:
        return True


def hook_mode():
    try:
        payload = json.load(sys.stdin)
        fpath = payload.get("tool_input", {}).get("file_path", "")
    except (ValueError, AttributeError):
        return 0
    p = Path(fpath)
    if p.suffix != ".md" or not p.is_file():
        return 0
    text = p.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    if fm is None or "doc-type" not in fm:
        return 0
    findings = lint_text(text) or []
    if fm.get("doc-type") == "adr" and fm.get("status") == "accepted" and head_is_accepted_adr(p):
        findings.append(("FAIL", "T4", "this ADR is accepted in committed history — the ledger is append-only; "
                                       "revert this edit and write a new ADR with `supersedes: " + fm.get("id", "adr-????") + "`"))
    fails = [f for f in findings if f[0] == "FAIL"]
    if fails:
        print(json.dumps({"decision": "block",
                          "reason": "doc_lint: " + " | ".join(f"{c} {m}" for _, c, m in fails)}))
    return 0


def selftest():
    tpl_dir = Path(__file__).resolve().parent.parent / "skills" / "doc-writing-rules" / "references" / "templates"
    for tpl in sorted(tpl_dir.glob("*.md")):
        text = tpl.read_text().replace("YYYY-MM-DD", "2026-07-07")
        fs = [f for f in (lint_text(text) or []) if f[0] == "FAIL"]
        assert not fs, f"template {tpl.name} must lint clean against its own contract, got {fs}"
    assert lint_text("# just a readme\nprose\n") is None, "non-documents are not ours to judge"
    bad = "---\ndoc-type: spec\nid: spec-x\nstatus: shipped\n---\n# S\n\n## Requirements\ntext\n"
    codes = {f[1] for f in lint_text(bad)}
    assert {"T2", "T3"} <= codes, f"bad status + missing sections must fail, got {codes}"
    assert any(f[1] == "T5" for f in lint_text(bad.replace("status: shipped", "status: draft"))), "REQ-less spec must warn T5"
    nofm = lint_text("---\ndoc-type: adr\n---\n# A\n## Context\n## Decision\n## Consequences\n")
    assert any(f[1] == "T1" for f in nofm), "missing id/status must fail T1"
    # T4 git-aware scope (2026-07-15): committed-accepted blocks; new/ratifying doesn't
    import shutil
    if shutil.which("git"):
        import subprocess
        import tempfile
        adr = ("---\ndoc-type: adr\nid: adr-0001\nstatus: {s}\ndate: 2026-07-15\n---\n"
               "# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            env_git = lambda *a: subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True,
                                                env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                                     "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                                                     "PATH": __import__("os").environ["PATH"], "HOME": td})
            env_git("init", "-q")
            f = repo / "0001-x.md"
            f.write_text(adr.format(s="accepted"))
            assert not head_is_accepted_adr(f), "untracked new accepted ADR must be ALLOWED (authoring, not forgery)"
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "adr proposed")
            # HEAD holds accepted now -> editing must block
            assert head_is_accepted_adr(f), "committed-accepted ADR must BLOCK edits (the ledger)"
            f.write_text(adr.format(s="proposed"))
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "as proposed")
            assert not head_is_accepted_adr(f), "HEAD-proposed ADR must allow the ratification flip"
    print("doc_lint selftest · PASS · all 8 templates self-consistent; type/status/sections/spine counters bite; T4 guards committed history only")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "--hook":
        sys.exit(hook_mode())
    sys.exit(max(render(a, lint_text(Path(a).read_text(encoding="utf-8", errors="replace"))) for a in args))
