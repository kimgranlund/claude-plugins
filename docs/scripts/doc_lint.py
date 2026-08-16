#!/usr/bin/env python3
"""doc_lint — structural validation for functional documents (the docs plugin's check tier).

Usage:
  doc_lint.py <file.md> [...]      lint documents (files without `doc-type:` frontmatter are skipped)
  doc_lint.py --hook               hook mode: read {"tool_input":{"file_path":...}} from stdin;
                                   silent pass for non-documents; emits a block decision on findings
  doc_lint.py selftest             prove the counters bite

Rules ("no validator, no type" — Vol 3 §3.1):
  T1 [FAIL] frontmatter parses and carries doc-type, id, status
  T2 [FAIL] doc-type is one of the ten; status is in that type's enum
  T3 [FAIL] required sections for the type present as `## ` headings
  T4 [FAIL] ledger protection (hook mode): editing a file whose COMMITTED (HEAD) version is a
            locked ledger entry — an accepted ADR, a locked IDR, or a locked RDD — supersede,
            never edit. Refined 2026-07-15 (ADR): a new/untracked ADR, or one still `proposed` in
            HEAD, may be authored and ratified (the proposed->accepted flip is the ratification
            act, not a forgery); the append-only guarantee protects history. Generalized
            2026-08-16 (IDR, #316; RDD, #332) to a ledger-lock guard covering
            `doc-type: adr, status: accepted`, `doc-type: idr, status: locked`, and
            `doc-type: rdd, status: locked` — the same two-phase mechanic, reused verbatim per
            LEDGER_LOCK below. git absent / not a repo / any doubt -> conservative block, as before.
  T5 [WARN] plan steps without a done-when token; spec Requirements without REQ- IDs
  T6 [WARN] an ADR with no `intent-refs:` citation — an "orphan ADR" per the corpus's
            product-lifecycle-bible (Part 4): a HOW decision with no cited upstream IDR claim.
            Added 2026-08-16 (#316) alongside the `idr` type; existing ADRs 0001-0013 predate
            `intent-refs:` and are EXPECTED to warn here — the retrofit is its own deferred
            follow-up (PRD Implementation surface item 7), not required for this check to ship.
  T7 [FAIL] a `locked`-or-`superseded` RDD with an empty/missing `decision-refs:` OR an
            empty/missing `dri:` — a release commitment locked with no upward citation or no
            named accountable human. Added 2026-08-16 (#332, `prd-rdd-framework.md`) alongside
            the `rdd` type; `draft` RDDs are exempt on both fields (the harvest window — citations
            and DRI assignment may genuinely not be settled yet). Deliberately stricter than T6
            (FAIL, not WARN): RDD has zero existing instances, so there is no retrofit debt to
            excuse a soft landing. `decision-refs:` is a single-line comma/space-separated scalar
            (`parse_frontmatter` cannot read a YAML block list) — never a list.
  T8 [FAIL] an IDR with a missing/empty `provenance:` frontmatter key, or a value outside
            {derived-from-evidence, inferred, decided-by-human} — machine-readable provenance for
            every claim, one of the same three labels the `## Why` prose already states in prose
            for idr-0001..0006 (#431, ratification round). IDR-only for now (no retrofit debt on
            other types); FAIL, not WARN — IDR has a small, fully-authored instance set, so there
            is no soft-landing case to make.
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
    "brief":   {"status": {"active", "retired"},                  "sections": ["Thesis", "Confirmed", "Open Questions"]},
    "ticket":  {"status": {"open", "doing", "done", "wontfix"},   "sections": ["Summary", "Acceptance", "Links"]},
    "task":    {"status": {"todo", "doing", "done"},              "sections": ["Goal", "Done-when"]},
    "idr":     {"status": {"draft", "locked", "superseded"},      "sections": ["Claim", "Why", "Proof"]},
    "rdd":     {"status": {"draft", "locked", "superseded"},      "sections": ["Scope", "Acceptance", "Sequencing", "Completion"]},
}

# T4's ledger-lock scope, keyed by doc-type -> the status value that means "committed and locked".
# ADR's `accepted` and IDR's `locked` are the same mechanic (ADR-0013's proven two-phase
# proposed/draft -> ratified flip); adding a doc-type here is the whole extension, no new code path.
# RDD's `locked` reuses the identical mechanic verbatim (#332) — the primary Mutability design
# from `prd-rdd-framework.md`: `shipped-and-archived` tracks on the `roadmap`'s own living index,
# never a fourth status enum value here, so no new guard logic is owed.
LEDGER_LOCK = {
    "adr": "accepted",
    "idr": "locked",
    "rdd": "locked",
}

# T7's scope: RDD statuses at or beyond `locked` that must carry both a citation and a DRI.
RDD_CITED_STATUSES = {"locked", "superseded"}

# T8's scope: the vocabulary a `provenance:` key on an IDR must take.
PROVENANCE_VALUES = {"derived-from-evidence", "inferred", "decided-by-human"}


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
    if dtype == "adr":
        intent_refs = fm.get("intent-refs", "").strip().lower()
        if intent_refs in ("", "null", "none", "[]"):
            findings.append(("WARN", "T6", "no `intent-refs:` citation -> an ADR with no upstream "
                                            "IDR is an orphan (bible: 'an ADR with no IDR citation is an orphan')"))
    if dtype == "rdd" and status in RDD_CITED_STATUSES:
        decision_refs = fm.get("decision-refs", "").strip().lower()
        if decision_refs in ("", "null", "none", "[]"):
            findings.append(("FAIL", "T7", "no `decision-refs:` citation -> a locked-or-beyond RDD "
                                            "with no upward ADR/IDR citation is a release commitment "
                                            "with zero traceability"))
        dri = fm.get("dri", "").strip().lower()
        if dri in ("", "null", "none", "[]"):
            findings.append(("FAIL", "T7", "no `dri:` -> a locked-or-beyond RDD needs a named "
                                            "accountable human, mechanically, not just a Problem-statement claim"))
    if dtype == "idr":
        provenance = fm.get("provenance", "").strip()
        if provenance not in PROVENANCE_VALUES:
            findings.append(("FAIL", "T8", f"`provenance:` missing or not one of {sorted(PROVENANCE_VALUES)} "
                                            "-> every IDR claim needs a machine-readable source label, "
                                            "not just prose in `## Why`"))
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


def head_is_locked_ledger(p: Path) -> bool:
    """T4's scope test (refined 2026-07-15 for ADR; generalized 2026-08-16, #316, for IDR; #332,
    for RDD): the ledger protection guards COMMITTED history. True (block) when the file's HEAD
    version is a locked ledger entry per LEDGER_LOCK (an accepted ADR, a locked IDR, or a locked
    RDD); False (allow) when the file is new/untracked or still pre-lock (`proposed`/`draft`) in
    HEAD — authoring and the lock-flip ratification are legal acts on an uncommitted ledger entry.
    git absent, not a repo, or any failure -> True (conservative block, unchanged from the
    ADR-only version)."""
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
        if not head_fm:
            return False
        locked_status = LEDGER_LOCK.get(head_fm.get("doc-type"))
        return bool(locked_status and head_fm.get("status") == locked_status)
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
    dtype = fm.get("doc-type")
    locked_status = LEDGER_LOCK.get(dtype)
    if locked_status and fm.get("status") == locked_status and head_is_locked_ledger(p):
        findings.append(("FAIL", "T4", f"this {dtype.upper()} is {locked_status} in committed history — the ledger is append-only; "
                                       f"revert this edit and write a new {dtype.upper()} with `supersedes: " + fm.get("id", f"{dtype}-????") + "`"))
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
    # T6 orphan-ADR WARN (#316): no intent-refs -> warn; cited intent-refs -> silent
    orphan_adr = ("---\ndoc-type: adr\nid: adr-0099\nstatus: proposed\ndate: 2026-08-16\n"
                  "intent-refs: null\n---\n# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
    assert any(f[1] == "T6" for f in lint_text(orphan_adr)), "ADR with no intent-refs must WARN T6 (orphan)"
    cited_adr = orphan_adr.replace("intent-refs: null", "intent-refs: idr-0001")
    assert not any(f[1] == "T6" for f in lint_text(cited_adr)), "ADR citing an IDR must NOT warn T6"
    assert any(f[1] == "T5" for f in lint_text(bad.replace("status: shipped", "status: draft"))), "REQ-less spec must warn T5"
    # T7 RDD citation+DRI-presence FAIL (#332): locked-or-beyond with empty refs/dri FAILs;
    # draft is exempt on both; locked with both present is clean.
    rdd_base = ("---\ndoc-type: rdd\nid: rdd-0099\nstatus: {s}\ndate: 2026-08-16\nowner: k\n"
                "dri: {dri}\ndecision-refs: {refs}\nsupersedes: null\n---\n# R\n"
                "## Scope\ns\n## Acceptance\na\n## Sequencing\nq\n## Completion\nc\n")
    locked_empty_refs = rdd_base.format(s="locked", dri="kim", refs="")
    assert any(f[1] == "T7" for f in lint_text(locked_empty_refs)), "locked RDD with empty decision-refs must FAIL T7"
    locked_empty_dri = rdd_base.format(s="locked", dri="", refs="adr-0002")
    assert any(f[1] == "T7" for f in lint_text(locked_empty_dri)), "locked RDD with empty dri must FAIL T7"
    locked_clean = rdd_base.format(s="locked", dri="kim", refs="adr-0002, idr-0001")
    assert not any(f[1] == "T7" for f in lint_text(locked_clean)), "locked RDD with refs+dri must NOT FAIL T7"
    draft_empty = rdd_base.format(s="draft", dri="", refs="")
    assert not any(f[1] == "T7" for f in lint_text(draft_empty)), "draft RDD is exempt from T7 on both fields"
    # T8 IDR provenance FAIL (#431): missing/empty/bad-value provenance FAILs; a valid value is clean.
    idr_prov_base = ("---\ndoc-type: idr\nid: idr-0099\nstatus: draft\ndate: 2026-08-16\n"
                      "owner: k\nproof-ref: n/a\n{prov}supersedes: null\n---\n"
                      "# I\n## Claim\nc\n## Why\nw\n## Proof\np\n")
    missing_prov = idr_prov_base.format(prov="")
    assert any(f[1] == "T8" for f in lint_text(missing_prov)), "IDR with no provenance must FAIL T8"
    bad_prov = idr_prov_base.format(prov="provenance: made-up\n")
    assert any(f[1] == "T8" for f in lint_text(bad_prov)), "IDR with an out-of-vocab provenance must FAIL T8"
    good_prov = idr_prov_base.format(prov="provenance: decided-by-human\n")
    assert not any(f[1] == "T8" for f in lint_text(good_prov)), "IDR with a valid provenance must NOT FAIL T8"
    nofm = lint_text("---\ndoc-type: adr\n---\n# A\n## Context\n## Decision\n## Consequences\n")
    assert any(f[1] == "T1" for f in nofm), "missing id/status must fail T1"
    # T4 git-aware scope (2026-07-15, ADR; generalized 2026-08-16, #316, IDR): committed-locked
    # blocks; new/ratifying doesn't. Same temp repo, two independent ledger files -> proves the
    # generalized guard still handles ADR (regression) and now also handles IDR (new).
    import shutil
    if shutil.which("git"):
        import subprocess
        import tempfile
        adr = ("---\ndoc-type: adr\nid: adr-0001\nstatus: {s}\ndate: 2026-07-15\n---\n"
               "# A\n## Context\nc\n## Decision\nd\n## Consequences\nq\n")
        idr = ("---\ndoc-type: idr\nid: idr-0001\nstatus: {s}\ndate: 2026-08-16\nproof-ref: n/a\n"
               "provenance: decided-by-human\nsupersedes: null\n---\n# I\n## Claim\nc\n## Why\nw\n## Proof\np\n")
        rdd = ("---\ndoc-type: rdd\nid: rdd-0001\nstatus: {s}\ndate: 2026-08-16\nowner: k\n"
               "dri: k\ndecision-refs: adr-0002\nsupersedes: null\n---\n# R\n"
               "## Scope\ns\n## Acceptance\na\n## Sequencing\nq\n## Completion\nc\n")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            env_git = lambda *a: subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True,
                                                env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                                     "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                                                     "PATH": __import__("os").environ["PATH"], "HOME": td})
            env_git("init", "-q")
            # --- ADR regression: the pre-existing fixture pair, unaffected by the generalization ---
            f = repo / "0001-x.md"
            f.write_text(adr.format(s="accepted"))
            assert not head_is_locked_ledger(f), "untracked new accepted ADR must be ALLOWED (authoring, not forgery)"
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "adr proposed")
            assert head_is_locked_ledger(f), "committed-accepted ADR must BLOCK edits (the ledger) — regression"
            f.write_text(adr.format(s="proposed"))
            env_git("add", "0001-x.md"); env_git("commit", "-qm", "as proposed")
            assert not head_is_locked_ledger(f), "HEAD-proposed ADR must allow the ratification flip — regression"
            # --- IDR positive: committed-locked IDR blocks edit ---
            g = repo / "idr-0001-x.md"
            g.write_text(idr.format(s="locked"))
            env_git("add", "idr-0001-x.md"); env_git("commit", "-qm", "idr locked")
            assert head_is_locked_ledger(g), "committed-locked IDR must BLOCK edits (the ledger) — positive"
            # --- IDR negative: a draft IDR (even committed) stays freely editable ---
            g.write_text(idr.format(s="draft"))
            env_git("add", "idr-0001-x.md"); env_git("commit", "-qm", "idr amended to draft")
            assert not head_is_locked_ledger(g), "committed-draft IDR must be ALLOWED to edit — negative"
            # --- RDD positive: committed-locked RDD blocks edit ---
            h = repo / "rdd-0001-x.md"
            h.write_text(rdd.format(s="locked"))
            env_git("add", "rdd-0001-x.md"); env_git("commit", "-qm", "rdd locked")
            assert head_is_locked_ledger(h), "committed-locked RDD must BLOCK edits (the ledger) — positive"
            # --- RDD negative: a draft RDD (even committed) stays freely editable ---
            h.write_text(rdd.format(s="draft"))
            env_git("add", "rdd-0001-x.md"); env_git("commit", "-qm", "rdd amended to draft")
            assert not head_is_locked_ledger(h), "committed-draft RDD must be ALLOWED to edit — negative"
    print("doc_lint selftest · PASS · all 11 templates self-consistent; type/status/sections/spine counters bite; "
          "T4 ledger-lock guards committed ADR(accepted)/IDR(locked)/RDD(locked) history only; "
          "T6 orphan-ADR warn bites; T7 RDD citation+DRI-presence FAIL bites; T8 IDR provenance FAIL bites")
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
