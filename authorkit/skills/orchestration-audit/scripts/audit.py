#!/usr/bin/env python3
"""orchestration-audit driver — mechanizes the mechanizable slice of the eight per-archetype
orchestration rubrics (`teamwork:fleet-rules/references/orchestration-rubric-a{1-8}-*.md`,
issue #666). Same split as `doctrine-audit`'s `sweep.py`: every criterion is tagged
mechanizable or judgment in its owning rubric file; this script computes ONLY the
mechanizable ones and reports every judgment criterion as "queued, not built" to its named
owning checker — it never grades conduct, wiring quality, or anything a script cannot see
structurally.

Priority axes (2026-08-18 fold-in on #666):
  G1  A3-R2  durable-channel evidence reader — confirms `.claude/ops/fleet.json` and
             `.claude/ops/fleet-roster.md` exist and parse, cross-references roster rows
             against fleet.json's live_state (never reads agent-*.jsonl transcripts — that
             stays the flagged-incident deep-dive tier a human runs by hand, per the ruling)
  G2  A7-R4  workflows/*.js syntax lint tier — splits each file at the Workflow-tool
             loader's own `export const meta = {...}` boundary (issue #529: the loader runs
             the file as BOTH a module-level export AND the body of an async function it
             supplies, a combination no single eslint `sourceType` can parse), syntax-checks
             each half under the grammar it will actually run under (`node --check`)

Plus three narrower mechanizable checks named in the rubric files' own tables:
  X-R3   review-coverage existence — does a named owning-checker file exist on disk
  A6-R2  grant-literal presence — the doctrine text for the literal auto-merge grant strings
  A4-R1  roster row count — `fleet-roster.md` has parseable data rows
  A5-R3  resume-path presence — a fork's own skill body names a fold-in resume command

Usage:
  audit.py --root PATH --archetype {a1,a2,a3,a4,a5,a6,a7,a8,all} [--json]
  audit.py selftest

Exit codes: 0 clean (no mechanizable findings; judgment criteria may still be queued),
1 mechanizable findings present, 2 usage error (root missing, node unavailable for G2, or
an archetype naming a value outside a1..a8/all).
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import os
from pathlib import Path

ARCHETYPES = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8"]

# X-R3: the owning-checker file each archetype's rubric names, relative to the estate root.
# A missing entry (archetype maps to []) means the rubric itself records "no dedicated
# checker exists yet" — that is a named gap, not a script defect, and is reported as such.
OWNING_CHECKERS = {
    "a1": ["harness/scripts/release_gate.py", "harness/scripts/skill_lint.py"],
    "a2": ["teamwork/agents/wiring-checker.md", "teamwork/agents/code-checker.md"],
    "a3": [],
    "a4": ["teamwork/agents/wiring-checker.md"],
    "a5": ["harness/agents/skill-checker.md"],
    "a6": ["teamwork/skills/loop-rules"],
    "a7": ["authorkit/skills/orchestration-audit"],
    "a8": [],
}

# The two ADR-0012 grant literals check_grant_literal() proves independently — not a shared
# constant list, since a naive "both present" test over a substring pair is vacuous (see
# check_grant_literal's own docstring).


class UsageError(Exception):
    """A clean, expected usage failure — main() turns this into exit 2, never a traceback."""


# ---------------------------------------------------------------------------
# G2 / A7-R4 — workflows/*.js syntax lint tier
# ---------------------------------------------------------------------------

META_MARKER_RE = re.compile(r"export\s+const\s+meta\s*=\s*\{")


def split_workflow_file(text: str):
    """Pure: split a workflow script at the loader's own boundary — a top-level
    `export const meta = { ... }` object literal. The marker itself tolerates whitespace
    variation (`meta={`, a line-wrapped `=`) via `META_MARKER_RE`, never a literal
    single-spelling string match. The brace-balance scan that finds the matching close is
    both string-literal AND comment aware — a `{`/`}`/quote-lookalike inside a `//` or
    `/* */` comment, or inside a quoted string, never miscounts. Returns (meta_src,
    body_src), or None if no marker is found or the braces never balance (the file isn't
    this loader's shape, or is malformed — reported as a finding, never silently skipped)."""
    m = META_MARKER_RE.search(text)
    if m is None:
        return None
    idx = m.start()
    open_pos = m.end() - 1  # the '{' the regex itself matched
    depth = 0
    i = open_pos
    in_str = None
    escape = False
    in_line_comment = False
    in_block_comment = False
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
        elif in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 1
        elif in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_str:
                in_str = None
        else:
            if ch == "/" and nxt == "/":
                in_line_comment = True
                i += 1
            elif ch == "/" and nxt == "*":
                in_block_comment = True
                i += 1
            elif ch in ('"', "'", "`"):
                in_str = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
        i += 1
    else:
        return None  # unbalanced braces — malformed, reported as a finding
    close_pos = i
    end = close_pos + 1
    if end < len(text) and text[end] == ";":
        end += 1
    meta_src = text[idx:end]
    body_src = text[:idx] + text[end:]
    return meta_src, body_src


def node_check(src: str, ext: str, wrap_async: bool):
    """Shells to `node --check` against src written to a temp file — the ONE real syntax
    ground truth for what the Workflow tool's loader will actually try to run. `wrap_async`
    wraps src in an async function body first, realizing the loader's own "runs the rest as
    the body of an async function it supplies" contract so a legitimate top-level `return`/
    `await` in the body half is not a false positive. `ext` MUST be `.cjs` for the wrapped
    body check, never `.js` — Node's module-type auto-detection (>=22.7) inspects a `.js`
    file for ESM syntax anywhere in it and can silently re-parse the WHOLE file as a module
    even when the offending `export` sits illegally nested inside our async wrapper,
    producing a false PASS on exactly the #529 defect class this check exists to catch
    (measured 2026-08-18 code-checker review: a real `export default …` appended after the
    loader's own boundary passed under `.js`, failed correctly under `.cjs`). `.cjs`
    unambiguously forces CommonJS/script parsing regardless of that heuristic. Returns
    (ok, stderr)."""
    if wrap_async:
        src = "async function __workflow_body__() {\n" + src + "\n}\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=False) as f:
        f.write(src)
        path = f.name
    try:
        proc = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        return proc.returncode == 0, proc.stderr.strip()
    except FileNotFoundError as e:
        raise UsageError(f"node not found on PATH -> A7-R4's syntax check cannot run: {e}")
    finally:
        os.unlink(path)


def first_error_line(stderr: str) -> str:
    """Pure: pick the actual SyntaxError/Error line out of a node --check stderr blob, never
    the trailing 'Node.js vX.Y.Z' banner line those blobs also carry."""
    if not stderr:
        return "unknown"
    for line in stderr.splitlines():
        stripped = line.strip()
        if re.match(r"^\w*Error:", stripped):
            return stripped
    return stderr.splitlines()[-1].strip()


def check_workflow_syntax(path: Path):
    """Runs the full G2 check on one workflows/*.js file. Returns a finding dict."""
    text = path.read_text()
    split = split_workflow_file(text)
    if split is None:
        return {
            "criterion": "A7-R4",
            "file": str(path),
            "status": "fail",
            "detail": "no balanced `export const meta = {...}` found — not this loader's file shape, or malformed",
        }
    meta_src, body_src = split
    meta_ok, meta_err = node_check(meta_src, ".mjs", wrap_async=False)
    if not meta_ok:
        return {
            "criterion": "A7-R4",
            "file": str(path),
            "status": "fail",
            "detail": f"meta block syntax error: {first_error_line(meta_err)}",
        }
    # .cjs, never .js -- see node_check's own docstring for the #529 false-pass this avoids
    body_ok, body_err = node_check(body_src, ".cjs", wrap_async=True)
    if not body_ok:
        return {
            "criterion": "A7-R4",
            "file": str(path),
            "status": "fail",
            "detail": f"body syntax error: {first_error_line(body_err)}",
        }
    return {"criterion": "A7-R4", "file": str(path), "status": "pass", "detail": "meta + body both syntax-valid under the loader's own grammar"}


def run_g2(root: Path):
    files = sorted(root.glob("**/workflows/*.js"))
    files = [
        f for f in files
        if "node_modules" not in f.parts and "dist" not in f.parts and "worktrees" not in f.parts
    ]
    if not files:
        return [{"criterion": "A7-R4", "file": None, "status": "n/a", "detail": "no workflows/*.js files found under root"}]
    return [check_workflow_syntax(f) for f in files]


# ---------------------------------------------------------------------------
# G1 / A3-R2 — durable-channel evidence reader
# ---------------------------------------------------------------------------

def extract_role(entry):
    """Pure: a `live_state.joined` entry is a `{role, mode, date, agent_name}` object in the
    real fleet.json shape (`fleet-bootstrap` Phase 1's own realization) — extract its `role`.
    A bare string entry (the shape the ratified draft's own criterion text implies in the
    abstract) is accepted too, so this stays forward-compatible with either realization.
    Anything else is not a role and is filtered by the caller (`None`)."""
    if isinstance(entry, dict):
        return entry.get("role")
    if isinstance(entry, str):
        return entry
    return None


def check_durable_channel(fleet_json_text, roster_text):
    """Pure: given the raw text of fleet.json and fleet-roster.md (either may be None if
    the file is absent), returns the A3-R2 finding. Cross-references roster seat names
    against fleet.json's live_state.joined list — a roster row with no matching live_state
    entry AND vice versa are both named, never silently reconciled."""
    findings = []
    if fleet_json_text is None:
        findings.append({"criterion": "A3-R2", "status": "fail", "detail": "fleet.json not found — no durable-channel evidence source available"})
        fleet_data = None
    else:
        try:
            fleet_data = json.loads(fleet_json_text)
        except json.JSONDecodeError as e:
            findings.append({"criterion": "A3-R2", "status": "fail", "detail": f"fleet.json is not valid JSON: {e}"})
            fleet_data = None

    if roster_text is None:
        findings.append({"criterion": "A3-R2", "status": "fail", "detail": "fleet-roster.md not found — no durable-channel evidence source available"})
        roster_seats = []
    else:
        roster_seats = parse_roster_seats(roster_text)
        if not roster_seats:
            findings.append({"criterion": "A3-R2", "status": "warn", "detail": "fleet-roster.md found but no parseable data rows"})

    if fleet_data is not None and roster_seats:
        joined = set()
        live_state = fleet_data.get("live_state", {})
        if isinstance(live_state, dict):
            joined = {extract_role(entry) for entry in (live_state.get("joined", []) or [])}
            joined.discard(None)
        roster_set = set(roster_seats)
        only_in_roster = sorted(roster_set - joined)
        only_in_fleet = sorted(joined - roster_set)
        if only_in_roster:
            findings.append({"criterion": "A3-R2", "status": "warn", "detail": f"roster row(s) with no matching fleet.json live_state entry: {only_in_roster}"})
        if only_in_fleet:
            findings.append({"criterion": "A3-R2", "status": "warn", "detail": f"fleet.json live_state entry(ies) with no matching roster row: {only_in_fleet}"})
        if not only_in_roster and not only_in_fleet:
            findings.append({"criterion": "A3-R2", "status": "pass", "detail": f"fleet.json and fleet-roster.md both readable and reconciled ({len(roster_set)} seat(s))"})

    if not findings:
        findings.append({"criterion": "A3-R2", "status": "pass", "detail": "durable channels present and readable"})
    return findings


def parse_roster_seats(roster_text: str):
    """Pure: extract seat names from fleet-roster.md's own markdown table — first column of
    every data row (a row starting with `|`, not the header/separator rows)."""
    seats = []
    for line in roster_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        first = cells[0].strip("`* ")
        if first.lower() in ("seat", "name", "role") or set(first) <= {"-", ":"}:
            continue
        seats.append(first)
    return seats


# ---------------------------------------------------------------------------
# X-R3 — review-coverage existence
# ---------------------------------------------------------------------------

def check_review_coverage(root: Path, archetype: str):
    expected = OWNING_CHECKERS.get(archetype, [])
    if not expected:
        return [{"criterion": "X-R3", "status": "warn", "detail": f"{archetype}: no owning checker named yet — reported gap, not a script defect"}]
    findings = []
    for rel in expected:
        exists = (root / rel).exists()
        findings.append({
            "criterion": "X-R3",
            "status": "pass" if exists else "fail",
            "detail": f"{archetype}: {rel} {'found' if exists else 'MISSING'}",
        })
    return findings


# ---------------------------------------------------------------------------
# A6-R2 — grant-literal presence
# ---------------------------------------------------------------------------

def check_grant_literal(text: str):
    """Pure: confirms the ADR-0012 grant literals appear verbatim in the given doctrine
    text (fed the real dispatch-ticket/mobilize-chores skill bodies by the live runner).
    Presence of the doctrine text is what's mechanizable; whether a LIVE dispatch actually
    used it correctly stays judgment (A6-R2's own table entry). GRANT_LITERALS' two entries
    must be genuinely INDEPENDENT checks — `"auto"` as a bare substring is trivially present
    any time `"auto-merge: authorized"` is (it's literally a substring of it), which made the
    second conjunct vacuous (caught 2026-08-18 code-checker review); the bare-`auto` token
    is checked as its own standalone command usage instead (`/mobilize-chores auto`), never
    as a substring test."""
    missing = []
    if "auto-merge: authorized" not in text:
        missing.append("auto-merge: authorized")
    if "/mobilize-chores auto" not in text:
        missing.append("/mobilize-chores auto")
    if missing:
        return {"criterion": "A6-R2", "status": "fail", "detail": f"missing literal grant string(s): {missing}"}
    return {"criterion": "A6-R2", "status": "pass", "detail": "both grant literals present verbatim"}


# ---------------------------------------------------------------------------
# A5-R3 — resume-path presence
# ---------------------------------------------------------------------------

# Requires a real id-shaped suffix after the command -- a bare "/file-bug " with nothing
# after it used to match too (the trailing char class was zero-width-satisfiable), which is
# not a resume-command TEMPLATE, just a mention (caught 2026-08-18 code-checker review). The
# estate's own real convention is `<id>` (verified against file-bug/file-feature/file-task's
# own SKILL.md text, 2026-08-18) -- `#NN`/`#123` accepted too since file-task's own trigger
# phrasing uses that form, but `<id>` must not be REQUIRED to carry a leading `#`, an earlier
# draft of this regex wrongly did and produced a false FAIL on the real siblings.
RESUME_PATTERN = re.compile(r"/file-(bug|feature|task)\s+(#(\d+|NN)|<id>|<[^>]+>)")


def check_resume_path(text: str):
    """Pure: a fork's own skill body names a fold-in resume command template."""
    if RESUME_PATTERN.search(text):
        return {"criterion": "A5-R3", "status": "pass", "detail": "resume-command template found"}
    return {"criterion": "A5-R3", "status": "fail", "detail": "no resume-command template found"}


# ---------------------------------------------------------------------------
# A4-R1 — roster row count
# ---------------------------------------------------------------------------

def check_roster_rows(roster_text):
    if roster_text is None:
        return {"criterion": "A4-R1", "status": "fail", "detail": "fleet-roster.md not found"}
    seats = parse_roster_seats(roster_text)
    if not seats:
        return {"criterion": "A4-R1", "status": "warn", "detail": "fleet-roster.md found but no parseable data rows"}
    return {"criterion": "A4-R1", "status": "pass", "detail": f"{len(seats)} roster row(s) parsed"}


# ---------------------------------------------------------------------------
# Live filesystem runner
# ---------------------------------------------------------------------------

def read_optional(path: Path):
    return path.read_text() if path.exists() else None


def run_archetype(root: Path, archetype: str):
    findings = []
    findings.extend(check_review_coverage(root, archetype))

    if archetype == "a3":
        fleet_json = read_optional(root / ".claude" / "ops" / "fleet.json")
        roster = read_optional(root / ".claude" / "ops" / "fleet-roster.md")
        findings.extend(check_durable_channel(fleet_json, roster))

    if archetype == "a4":
        roster = read_optional(root / ".claude" / "ops" / "fleet-roster.md")
        findings.append(check_roster_rows(roster))

    if archetype == "a6":
        # The two grant literals live in different skills: "auto-merge: authorized" in
        # dispatch-ticket's own sealed-dispatch contract, "/mobilize-chores auto" in
        # mobilize-chores' own unattended-entry doctrine -- read both, never just one.
        dt_path = root / "teamwork" / "skills" / "dispatch-ticket" / "SKILL.md"
        mc_path = root / "teamwork" / "skills" / "mobilize-chores" / "SKILL.md"
        text = (read_optional(dt_path) or "") + "\n" + (read_optional(mc_path) or "")
        findings.append(check_grant_literal(text))

    if archetype == "a5":
        for skill_name in ("file-bug", "file-feature", "file-task"):
            p = root / "docs" / "skills" / skill_name / "SKILL.md"
            text = read_optional(p)
            if text is None:
                findings.append({"criterion": "A5-R3", "status": "n/a", "detail": f"{skill_name}/SKILL.md not found"})
                continue
            f = check_resume_path(text)
            f = dict(f)
            f["detail"] = f"{skill_name}: {f['detail']}"
            findings.append(f)

    if archetype == "a7":
        findings.extend(run_g2(root))

    return findings


def render_report(all_findings: dict) -> tuple:
    lines = []
    any_fail = False
    for archetype, findings in all_findings.items():
        fails = [f for f in findings if f["status"] == "fail"]
        warns = [f for f in findings if f["status"] == "warn"]
        if fails:
            any_fail = True
            verdict = "FAIL"
        elif warns:
            verdict = "ATTENTION"
        else:
            verdict = "CLEAN"
        lines.append(f"orchestration-audit {archetype.upper()} · {verdict} · {len(fails)} fail / {len(warns)} warn / {len(findings)} total")
        for f in findings:
            marker = {"pass": "ok  ", "fail": "FAIL", "warn": "warn", "n/a": "n/a "}.get(f["status"], "?   ")
            lines.append(f"  {marker} {f['criterion']:6s} {f['detail']}")
    return "\n".join(lines), any_fail


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(args):
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--root")
    p.add_argument("--archetype")
    p.add_argument("--json", action="store_true")
    ns, unknown = p.parse_known_args(args)
    if unknown:
        raise UsageError(f"unrecognized argument(s): {unknown}")
    if not ns.root:
        raise UsageError("--root is required")
    if not ns.archetype:
        raise UsageError("--archetype is required")
    if ns.archetype != "all" and ns.archetype not in ARCHETYPES:
        raise UsageError(f"--archetype must be one of {ARCHETYPES + ['all']}, got {ns.archetype!r}")
    return ns


def main(argv):
    if argv[:1] == ["selftest"]:
        return run_selftest()

    try:
        ns = parse_args(argv)
    except UsageError as e:
        print(f"orchestration-audit: {e}", file=sys.stderr)
        return 2

    root = Path(ns.root)
    if not root.exists():
        print(f"orchestration-audit: root not found: {root}", file=sys.stderr)
        return 2

    targets = ARCHETYPES if ns.archetype == "all" else [ns.archetype]
    try:
        all_findings = {a: run_archetype(root, a) for a in targets}
    except UsageError as e:
        # e.g. node missing from PATH -- node_check() raises this, never a bare
        # FileNotFoundError traceback (an environment gap is a usage error, not a false pass)
        print(f"orchestration-audit: {e}", file=sys.stderr)
        return 2

    if ns.json:
        print(json.dumps(all_findings, indent=2))
    else:
        report, _ = render_report(all_findings)
        print(report)

    any_fail = any(f["status"] == "fail" for findings in all_findings.values() for f in findings)
    return 1 if any_fail else 0


# ---------------------------------------------------------------------------
# selftest — proves the pure functions bite, real positive + negative controls, no network
# ---------------------------------------------------------------------------

def run_selftest():
    failures = []

    def check(name, cond):
        if not cond:
            failures.append(name)

    # split_workflow_file: real shape
    real = 'export const meta = {\n  name: "x",\n  nested: { a: 1 },\n};\n\nconst y = 1\nreturn { y }\n'
    split = split_workflow_file(real)
    check("split_workflow_file finds marker", split is not None)
    if split:
        meta_src, body_src = split
        check("split meta well-formed", meta_src.startswith("export const meta = {") and meta_src.rstrip().endswith("};"))
        check("split body has no export", "export const meta" not in body_src)
        check("split body keeps return", "return { y }" in body_src)

    check("split_workflow_file no marker -> None", split_workflow_file("const x = 1\n") is None)
    check("split_workflow_file unbalanced -> None", split_workflow_file("export const meta = {\n  a: 1\n") is None)

    # regression: the marker must tolerate whitespace variation (a line-wrapped `=`, no space
    # before `{`) -- a literal single-spelling string match missed these (caught 2026-08-18
    # code-checker review)
    whitespace_variant = 'export const meta ={\n  name: "x",\n};\nreturn 1\n'
    check("split_workflow_file tolerates whitespace-variant marker (regression)", split_workflow_file(whitespace_variant) is not None)

    # regression: a `{`/`'`/`"` inside a `//` or `/* */` comment must never desync the
    # brace-balance scan (caught 2026-08-18 code-checker review)
    commented = 'export const meta = {\n  // a comment with a { and a \' in it\n  name: "x", /* another { one */\n};\nreturn 1\n'
    csplit = split_workflow_file(commented)
    check("split_workflow_file is comment-aware (regression)", csplit is not None)
    if csplit:
        check("split_workflow_file comment-aware body keeps return", "return 1" in csplit[1])

    # node_check positive + negative controls (real subprocess — proves the mechanism, not a mock)
    ok, _ = node_check('export const meta = {a: 1};', ".mjs", wrap_async=False)
    check("node_check accepts valid module", ok is True)
    ok2, _ = node_check('export const meta = {a: ,};', ".mjs", wrap_async=False)
    check("node_check rejects invalid module (negative control)", ok2 is False)
    ok3, _ = node_check('return 1\nawait Promise.resolve()\n', ".cjs", wrap_async=True)
    check("node_check wrap_async accepts top-level return+await", ok3 is True)
    ok4, _ = node_check('return 1\nawait Promise.resolve()\n', ".cjs", wrap_async=False)
    check("node_check unwrapped rejects top-level return (negative control)", ok4 is False)

    # regression: the exact #529 defect class -- a LEGAL body plus a real top-level `export
    # default …` appended after the loader's own meta/body boundary. Under the OLD `.js`
    # extension this silently PASSED (Node's module-type auto-detection re-parses a `.js`
    # file containing `export` as an ES module even though the export sits illegally nested
    # inside our async wrapper) -- `.cjs` forces unambiguous CommonJS/script parsing and
    # correctly FAILS it (caught 2026-08-18 code-checker review, the review's own repro).
    real_529_shape = 'const seatResults = await parallel(1)\nreturn { ok: true }\nexport default await runSweep()\n'
    ok529, _ = node_check(real_529_shape, ".cjs", wrap_async=True)
    check("node_check .cjs catches the real #529 false-pass (regression)", ok529 is False)

    # check_durable_channel — real fleet.json shape: live_state.joined is a list of
    # {role, mode, date, agent_name} objects (fleet-bootstrap Phase 1's own realization,
    # confirmed against this estate's own .claude/ops/fleet.json 2026-08-18), not bare strings
    fleet_ok = json.dumps({"live_state": {"joined": [
        {"role": "seat-a", "mode": "manual", "date": "2026-08-18", "agent_name": None},
        {"role": "seat-b", "mode": "manual", "date": "2026-08-18", "agent_name": None},
    ]}})
    roster_ok = "| Seat | Role |\n|---|---|\n| seat-a | builder |\n| seat-b | checker |\n"
    findings = check_durable_channel(fleet_ok, roster_ok)
    check("durable_channel reconciled -> pass", any(f["status"] == "pass" for f in findings))

    fleet_partial = json.dumps({"live_state": {"joined": [{"role": "seat-a", "mode": "manual", "date": "2026-08-18", "agent_name": None}]}})
    roster_partial = "| Seat | Role |\n|---|---|\n| seat-a | builder |\n| seat-c | orphan |\n"
    findings2 = check_durable_channel(fleet_partial, roster_partial)
    check("durable_channel mismatch -> warn named", any(f["status"] == "warn" and "seat-c" in f["detail"] for f in findings2))

    # extract_role: dict shape (real), string shape (forward-compat), and a malformed entry
    check("extract_role dict shape", extract_role({"role": "x", "agent_name": None}) == "x")
    check("extract_role string shape", extract_role("x") == "x")
    check("extract_role malformed -> None (negative control)", extract_role(42) is None)

    findings3 = check_durable_channel(None, None)
    check("durable_channel both absent -> fail x2 (negative control)", sum(1 for f in findings3 if f["status"] == "fail") == 2)

    findings4 = check_durable_channel("not json", roster_ok)
    check("durable_channel malformed json -> fail (negative control)", any(f["status"] == "fail" and "not valid JSON" in f["detail"] for f in findings4))

    # parse_roster_seats
    seats = parse_roster_seats(roster_ok)
    check("parse_roster_seats extracts both rows", seats == ["seat-a", "seat-b"])
    check("parse_roster_seats empty on no rows", parse_roster_seats("no table here") == [])
    # regression: the real fleet-roster.md header is literally "| Role | Session name | ... |"
    # (not "Seat") — a naive header filter that only excludes "seat"/"name" leaks the header
    # row itself into the seat list (caught live against this estate's own roster, 2026-08-18)
    role_header_roster = "| Role | Session name | Date | Repo |\n|---|---|---|---|\n| reviewer | plugins-reviewer | 2026-08-16 | plugins |\n"
    check("parse_roster_seats excludes a 'Role' header (regression)", parse_roster_seats(role_header_roster) == ["reviewer"])

    # check_grant_literal — the two literals must be independently required, never one a
    # substring of the other (regression: "auto" alone used to pass trivially whenever
    # "auto-merge: authorized" did, since it's literally a substring of it)
    good_text = "the literal line `auto-merge: authorized` ... `/mobilize-chores auto` forwards ADR-0012's carve-out"
    check("grant_literal both present -> pass", check_grant_literal(good_text)["status"] == "pass")
    bad_text = "nothing about grants here"
    check("grant_literal missing -> fail (negative control)", check_grant_literal(bad_text)["status"] == "fail")
    only_first = "the literal line `auto-merge: authorized` ... never infer the grant"
    check("grant_literal only auto-merge present -> fail (regression, was vacuously pass)", check_grant_literal(only_first)["status"] == "fail")

    # check_resume_path — needs a real id-shaped suffix, not just a bare command mention
    check("resume_path finds template", check_resume_path("fold in via `/file-bug #NN <answers>`")["status"] == "pass")
    check("resume_path missing -> fail (negative control)", check_resume_path("no resume path here")["status"] == "fail")
    check("resume_path bare mention with no id -> fail (regression, was vacuously pass)", check_resume_path("see /file-bug for details")["status"] == "fail")

    # check_roster_rows
    check("roster_rows counts", check_roster_rows(roster_ok)["status"] == "pass")
    check("roster_rows absent -> fail (negative control)", check_roster_rows(None)["status"] == "fail")

    # check_review_coverage — pure w.r.t. a fake root
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "teamwork" / "agents").mkdir(parents=True)
        (tdp / "teamwork" / "agents" / "wiring-checker.md").write_text("x")
        cov = check_review_coverage(tdp, "a4")
        check("review_coverage finds existing file", any(f["status"] == "pass" for f in cov))
        cov2 = check_review_coverage(tdp, "a1")
        check("review_coverage flags missing file (negative control)", any(f["status"] == "fail" for f in cov2))
        cov3 = check_review_coverage(tdp, "a3")
        check("review_coverage names the no-owning-checker gap for a3", cov3[0]["status"] == "warn")

    # parse_args
    try:
        parse_args(["--archetype", "a1"])
        failures.append("parse_args should require --root")
    except UsageError:
        pass
    try:
        parse_args(["--root", ".", "--archetype", "bogus"])
        failures.append("parse_args should reject an unknown archetype")
    except UsageError:
        pass
    ns = parse_args(["--root", ".", "--archetype", "all", "--json"])
    check("parse_args accepts a clean call", ns.root == "." and ns.archetype == "all" and ns.json is True)

    if failures:
        print(f"orchestration-audit selftest · {len(failures)} FAIL")
        for name in failures:
            print(f"  FAIL {name}")
        return 1
    print("orchestration-audit selftest · all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
