#!/usr/bin/env python3
"""skill-postwrite-invocation-lint — deterministic checks for SKILL.md files.

Check tier only: everything here is a pass/fail function. Judgment (behavior
delta, trigger fidelity, register) belongs to check-skill, not this script.

Modes:
  skill_lint.py <path> [<path>...]   CLI: repair-affordance report; exit 1 on any FAIL
  skill_lint.py --hook               PostToolUse hook: reads event JSON on stdin;
                                     silent exit 0 unless a SKILL.md write FAILs,
                                     then emits {"decision":"block","reason":...}
  skill_lint.py selftest             proves the counters on embedded fixtures

Rules (F = FAIL, blocks; W = WARN, reported, never blocks):
  F1 frontmatter block present (--- ... --- at top)
  F2 both invocation dials declared: disable-model-invocation AND user-invocable
  F3 no '<' inside frontmatter (XML injection surface)
  F4 description present
  F5 description + when_to_use combined <= 1536 chars (listing truncation cap)
  F6 body <= 500 lines
  F7 no persona opener in body ("You are a ...", "You're ...")
  F8 no reserved words in the skill's name field or directory ("claude", "anthropic")
     — the platform rejects the skill (and fails the plugin load) at install time
  W1 description <= 1024 chars (Agent Skills portability cap)
  W2 model-invocable description carries trigger phrasing ("use when ...")
  W3 name <= 64 chars, kebab-case
  W4 agentive head (-er/-or) on a skill name (cross-type ambiguity with agents)
  W5 knowledge-noun head with user-invocable left true
  W6 hedge describers in prose ("please", "try to", "be careful", "make sure") > 3
  W7 salience inflation: caps NEVER/CRITICAL/IMPORTANT > 5 outside code fences

Agent files (agents/*.md) get a focused rule set:
  A1 frontmatter block present
  A2 frontmatter is YAML-shaped: every column-0 line is a `key:` or a comment;
     bare <example> blocks and other multi-line description content must be
     indented under a block scalar (`description: |`)
  A3 name and description present
  A4 body <= 60 lines — <= 75 for -reviewer/-auditor seats, the dual-depth allowance
     (thin-shell law: knowledge belongs in skills: preloads)
  A5 tools declared (an agent without an allowlist runs with everything)

hooks.json files get:
  H1 valid JSON
  H2 outer "hooks" wrapper present (a bare settings-style snippet registers silently never)
  H3 known event names (unknown -> WARN; the event set is drift-prone)
  H4 entry shape: matcher groups carry a hooks array; command hooks carry a command
  H5 no hardcoded home paths (use ${CLAUDE_PLUGIN_ROOT} / ${CLAUDE_PLUGIN_DATA})

evals suites (skills/*/evals/evals.json):
  E-rules delegated to eval_check.py (schema, unique ids, owner identity, case-mix floors)
  — a suite broken at write time no longer waits for the release gate to be discovered

plugin.json (.claude-plugin/plugin.json):
  P1 valid JSON object
  P2 name present, kebab-case
  P3 version present, semver (the version is the update cache key)

CLAUDE.md files (CLI mode only — the write hook does not nag entry-file edits):
  C1 length > 200 lines -> WARN (adherence ceiling; run /check-entry-file)
  C2 > 10 imperative-check lines ("always run", "never commit", "must pass") -> WARN
     (checks in prose are hook candidates)
"""
import json
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
try:
    import eval_check as _eval_check
except ImportError:  # standalone copies of this lint degrade gracefully
    _eval_check = None
try:
    import corpus_check as _corpus_check
except ImportError:
    _corpus_check = None
import re
import sys
from pathlib import Path

HOOK_NAME = "skill-postwrite-invocation-lint"
CLOSING = ("If a finding seems wrong -> report it against "
           "skill-writing-rules; do not suppress it inline.")

# Genuine verbs whose spelling ends in -er/-or: legal skill heads, never agentive
# (ADR-0001, 2026-07-09: W4 false-positived on reshape-skill).
VERB_HEADS = {"refactor", "render", "filter", "author"} - {"author"}  # author retired per ADR-0001
KNOWLEDGE_NOUNS = {"patterns", "principles", "standards", "conventions",
                   "context", "architecture", "catalog", "reference", "tokens",
                   # ADR-0006 Phase 0 (2026-07-21): the simple paradigm's knowledge shapes —
                   # `X-facts` (what is true) and `X-rules` (what must be followed) — join the
                   # noun set so the ~40 renamed knowledge skills keep W5's model-only check.
                   "facts", "rules"}
TRIGGER_RE = re.compile(
    r"\buse\s+(when|whenever|this|it|for)\b|\bwhen\s+(the\s+user|you|asked|working|writing)\b",
    re.IGNORECASE)
HEDGE_RE = re.compile(r"\b(please|try to|be careful|make sure)\b", re.IGNORECASE)
SALIENCE_RE = re.compile(r"\b(NEVER|CRITICAL|IMPORTANT)\b")
PERSONA_RE = re.compile(r"^\s*(You are an?\b|You're\b)")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(lines):
    """Minimal YAML-subset parser: top-level scalars + folded/literal blocks.
    Returns (fields: {key: (value, line_no)}, fm_span: (start, end) or None)."""
    if not lines or lines[0].strip() != "---":
        return {}, None
    fields, end = {}, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, None
    i = 1
    while i < end:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if m:
            key, val, key_line = m.group(1), m.group(2).strip(), i + 1
            if val in (">", ">-", "|", "|-"):
                block, j = [], i + 1
                while j < end and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
                    block.append(lines[j].strip())
                    j += 1
                fields[key] = (" ".join(b for b in block if b), key_line)
                i = j
                continue
            fields[key] = (val.strip("'\""), key_line)
        i += 1
    return fields, (1, end)


INLINE_CODE_RE = re.compile(r"`[^`]*`")


def prose_lines(lines, body_start):
    """Body lines with fenced blocks blanked and inline code spans stripped
    (numbering preserved). Backticked text is quoted material — a `NEVER`
    discussed as vocabulary is a mention, not a hard gate."""
    out, fenced = [], False
    for idx in range(body_start, len(lines)):
        line = lines[idx]
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append((idx + 1, ""))
            continue
        out.append((idx + 1, "" if fenced else INLINE_CODE_RE.sub("", line)))
    return out


def lint_text(text, skill_dir_name):
    lines = text.splitlines()
    findings = []  # (severity, line, rule, message-with-fix)

    fields, span = parse_frontmatter(lines)
    if span is None:
        findings.append(("FAIL", 1, "F1",
                         "no frontmatter block -> open the file with `---`, fields, `---`; "
                         "malformed metadata kills auto-discovery silently"))
        return findings

    fm_start, fm_end = span
    for i in range(fm_start, fm_end):
        if "<" in lines[i]:
            findings.append(("FAIL", i + 1, "F3",
                             "'<' in frontmatter -> move XML/angle-bracket content into the body"))
            break

    for key in ("disable-model-invocation", "user-invocable"):
        if key not in fields:
            findings.append(("FAIL", fm_end + 1, "F2",
                             f"missing `{key}` -> declare it explicitly, even at its default "
                             "(house rule: both dials, always)"))

    desc, desc_line = fields.get("description", ("", fm_end))
    wtu, _ = fields.get("when_to_use", ("", 0))
    if not desc:
        findings.append(("FAIL", desc_line, "F4",
                         "missing `description` -> write the trigger contract: what it does + "
                         "when to use it, user's phrasings first"))
    else:
        combined = len(desc) + len(wtu)
        if combined > 1536:
            findings.append(("FAIL", desc_line, "F5",
                             f"description+when_to_use is {combined} chars -> cut to <=1536; "
                             "the listing truncates the tail first"))
        elif len(desc) > 1024:
            findings.append(("WARN", desc_line, "W1",
                             f"description is {len(desc)} chars -> <=1024 keeps it portable "
                             "across the Agent Skills standard"))
        dmi = fields.get("disable-model-invocation", ("false", 0))[0].lower()
        if dmi != "true" and not TRIGGER_RE.search(desc + " " + wtu):
            findings.append(("WARN", desc_line, "W2",
                             "model-invocable but no trigger phrasing -> add 'Use when the user "
                             "asks to <verbatim phrasings>'"))

    name, name_line = fields.get("name", (skill_dir_name or "", fm_start))
    if name:
        for token in ("claude", "anthropic"):
            if token in name.lower() or token in (skill_dir_name or "").lower():
                findings.append(("FAIL", name_line, "F8",
                                 f"reserved word '{token}' in the skill name/directory -> rename; "
                                 "the platform rejects it at install and the whole plugin fails "
                                 "to load"))
                break
        if len(name) > 64 or not KEBAB_RE.match(name):
            findings.append(("WARN", name_line, "W3",
                             "name -> kebab-case, <=64 chars"))
        head = name.split("-")[-1]
        ui = fields.get("user-invocable", ("true", 0))[0].lower()
        if len(head) >= 5 and (head.endswith("er") or head.endswith("or")) and head not in VERB_HEADS:
            findings.append(("WARN", name_line, "W4",
                             f"agentive head '{head}' on a skill -> agents take -er/-or; "
                             "a skill takes the verb or knowledge-noun form"))
        if head in KNOWLEDGE_NOUNS and ui != "false":
            findings.append(("WARN", name_line, "W5",
                             f"knowledge-noun head '{head}' with user-invocable left true -> "
                             "knowledge species is model-only (`user-invocable: false`)"))

    body_len = len(lines) - fm_end - 1
    if body_len > 500:
        findings.append(("FAIL", fm_end + 2, "F6",
                         f"body is {body_len} lines -> <=500; split detail to references/, "
                         "one level deep"))

    prose = prose_lines(lines, fm_end + 1)
    for ln, line in prose:
        if PERSONA_RE.match(line):
            findings.append(("FAIL", ln, "F7",
                             "persona opener -> skills state identity declaratively "
                             "('the review cites ...'), not as 'You are a ...'"))
            break

    hedges = [(ln, m.group(0)) for ln, line in prose for m in HEDGE_RE.finditer(line)]
    if len(hedges) > 3:
        ln = hedges[0][0]
        findings.append(("WARN", ln, "W6",
                         f"{len(hedges)} hedge describers ('{hedges[0][1]}', ...) -> state the "
                         "behavior as fact or cut the line"))

    salience = [ln for ln, line in prose for _ in SALIENCE_RE.finditer(line)]
    if len(salience) > 5:
        findings.append(("WARN", salience[0], "W7",
                         f"{len(salience)} hard-emphasis markers -> budget <=3 hard gates; "
                         "emphasis inflates"))

    return findings


def lint_agent_text(text):
    """Focused checks for agents/*.md — the failure class is frontmatter that a
    strict YAML parser rejects, which kills the whole plugin load."""
    lines = text.splitlines()
    findings = []
    fields, span = parse_frontmatter(lines)
    if span is None:
        findings.append(("FAIL", 1, "A1",
                         "no frontmatter block -> open the file with `---`, fields, `---`"))
        return findings
    fm_start, fm_end = span
    for i in range(fm_start, fm_end):
        line = lines[i]
        if not line.strip() or line.startswith("#"):
            continue
        if line[0] in (" ", "\t"):
            continue  # indented: block-scalar or list continuation
        if re.match(r"^[A-Za-z0-9_-]+:(\s|$)", line):
            continue
        snippet = line.strip()[:40]
        findings.append(("FAIL", i + 1, "A2",
                         f"column-0 `{snippet}` is not a YAML key -> fold multi-line "
                         "description content into a block scalar (`description: |`) and "
                         "indent it; strict YAML rejects bare <example> blocks"))
    for key in ("name", "description"):
        if key not in fields or not fields[key][0]:
            findings.append(("FAIL", fm_end + 1, "A3",
                             f"missing `{key}` -> required for agent discovery"))
    body_len = len(lines) - fm_end - 1
    # Reviewer-class seats (dual-depth dispatch contracts) carry a documented ~75-line
    # allowance (ruled 2026-07-16, check-everything): the earned residual of a FLOOR+DEEP
    # contract hovers near 60 even when clean, so the standing 60-line warn stays for
    # every other seat and reviewers warn only past 75.
    name_val = fields.get("name", ("", 0))[0]
    a4_cap = 75 if re.search(r"-(reviewer|auditor)$", name_val) else 60
    if body_len > a4_cap:
        findings.append(("WARN", fm_end + 2, "A4",
                         f"body is {body_len} lines -> thin shell (cap {a4_cap}); knowledge "
                         "belongs in `skills:` preloads, not the agent prompt"))
    if "tools" not in fields:
        findings.append(("WARN", fm_end + 1, "A5",
                         "no `tools` allowlist -> the agent runs with everything; declare "
                         "least privilege"))
    return findings


KNOWN_EVENTS = {  # drift-prone: re-verify the event set on a version bump
    "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "SessionStart",
    "SessionEnd", "UserPromptSubmit", "PreCompact", "Notification",
    "PermissionRequest", "StopFailure",
}
HOME_PATH_RE = re.compile(r"(/Users/|/home/)[A-Za-z0-9._-]+/")


def lint_hooks_text(text):
    """H-rules for hooks.json — the failure class is registration that silently
    never fires (missing wrapper) or config that works on one machine."""
    findings = []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError) as e:
        return [("FAIL", getattr(e, "lineno", 1), "H1",
                 f"invalid JSON ({e.msg if hasattr(e, 'msg') else e}) -> fix the syntax; "
                 "a malformed hooks.json registers nothing")]
    if not isinstance(data, dict):
        return [("FAIL", 1, "H1", "top level must be a JSON object")]
    if "hooks" not in data:
        eventish = [k for k in data if k in KNOWN_EVENTS]
        hint = f" (found top-level `{eventish[0]}` — settings-style)" if eventish else ""
        findings.append(("FAIL", 1, "H2",
                         f"missing outer `\"hooks\"` wrapper{hint} -> wrap it; a bare "
                         "snippet in a plugin registers silently never"))
        events = data if eventish else {}
    else:
        events = data["hooks"] if isinstance(data["hooks"], dict) else {}
        if not isinstance(data["hooks"], dict):
            findings.append(("FAIL", 1, "H4", "`hooks` must map event names to matcher arrays"))
    for event, groups in events.items():
        if event not in KNOWN_EVENTS:
            findings.append(("WARN", 1, "H3",
                             f"unknown event `{event}` -> verify against current docs "
                             "(the event set moves)"))
        if not isinstance(groups, list):
            findings.append(("FAIL", 1, "H4", f"`{event}` must be an array of matcher groups"))
            continue
        for g in groups:
            hooks = g.get("hooks") if isinstance(g, dict) else None
            if not isinstance(hooks, list) or not hooks:
                findings.append(("FAIL", 1, "H4",
                                 f"`{event}` group missing its `hooks` array -> each matcher "
                                 "group carries hooks: [{type, ...}]"))
                continue
            for h in hooks:
                if not isinstance(h, dict) or "type" not in h:
                    findings.append(("FAIL", 1, "H4", f"`{event}` hook missing `type`"))
                    continue
                cmd = h.get("command", "")
                if h["type"] == "command" and not cmd:
                    findings.append(("FAIL", 1, "H4",
                                     f"`{event}` command hook missing `command`"))
                if HOME_PATH_RE.search(cmd):
                    findings.append(("WARN", 1, "H5",
                                     f"hardcoded home path in `{event}` command -> "
                                     "${CLAUDE_PLUGIN_ROOT} for shipped files, "
                                     "${CLAUDE_PLUGIN_DATA} for state"))
    return findings


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def lint_plugin_json_text(text):
    """P-rules for the plugin manifest — a bad manifest is a plugin that never loads."""
    findings = []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError) as e:
        return [("FAIL", getattr(e, "lineno", 1), "P1", f"invalid JSON ({e}) -> fix the syntax")]
    if not isinstance(data, dict):
        return [("FAIL", 1, "P1", "top level must be a JSON object")]
    name = data.get("name", "")
    if not name or not KEBAB_RE.match(name):
        findings.append(("FAIL", 1, "P2", f"name `{name}` -> kebab-case, required"))
    version = data.get("version", "")
    if not version or not SEMVER_RE.match(str(version)):
        findings.append(("WARN", 1, "P3",
                         f"version `{version}` -> semver; the version is the update cache key — "
                         "unversioned plugins cannot ship updates reliably"))
    return findings


CHECK_PROSE_RE = re.compile(
    r"\b(always (run|use|add|check)|never (commit|push|use|write)|must (pass|run|have))\b",
    re.IGNORECASE)


def lint_claude_md_text(text):
    """C-rules for entry files — mechanical smells only; the judgment lives in
    entry-file-rules and runs through /check-entry-file."""
    findings = []
    lines = text.splitlines()
    if len(lines) > 200:
        findings.append(("WARN", 201, "C1",
                         f"{len(lines)} lines -> entry files are paid every turn and adherence "
                         "decays past ~150-200 instructions; run /check-entry-file"))
    hits = [i + 1 for i, ln in enumerate(lines)
            if not ln.lstrip().startswith("```") and CHECK_PROSE_RE.search(ln)]
    if len(hits) > 10:
        findings.append(("WARN", hits[0], "C2",
                         f"{len(hits)} imperative-check lines -> checks in prose are hook "
                         "candidates (~70-90% compliance vs a hook's ~100%); run /check-entry-file"))
    return findings


def classify(path):
    # Absolutize before keying on parent names: a bare relative filename has no
    # parent to match, so `cd agents && lint x.md` misclassified agent files as
    # skills (#83, 2026-07-21). absolute() not resolve() — following a symlink
    # would reclassify a linked member by its target's directory.
    p = Path(path).absolute()
    if p.name == "SKILL.md":
        return "skill"
    if p.suffix == ".md" and p.parent.name == "agents":
        return "agent"
    if p.name == "hooks.json":
        return "hooks"
    if p.name == "CLAUDE.md":
        return "claude_md"
    if p.name == "plugin.json" and p.parent.name == ".claude-plugin":
        return "plugin_json"
    if p.name == "evals.json" and p.parent.name == "evals" and _eval_check:
        return "evals"
    if p.name == "INDEX.md" and p.parent.name == "references" and _corpus_check:
        return "index"
    return None


def render(path, findings):
    fails = [f for f in findings if f[0] == "FAIL"]
    if not findings:
        return f"{HOOK_NAME} · clean · {path}", False
    head = f"{HOOK_NAME} · {len(fails)} fail / {len(findings) - len(fails)} warn · {path}"
    rows = [f"  L{ln:<4} {sev} {rule}  {msg}" for sev, ln, rule, msg in
            sorted(findings, key=lambda f: f[1])]
    return "\n".join([head, *rows, CLOSING]), bool(fails)


def lint_path(path):
    p = Path(path)
    if not p.is_file():
        return f"{HOOK_NAME} · missing file · {path}", True
    kind = classify(path) or "skill"
    text = p.read_text(encoding="utf-8", errors="replace")
    if kind == "agent":
        return render(path, lint_agent_text(text))
    if kind == "hooks":
        return render(path, lint_hooks_text(text))
    if kind == "claude_md":
        return render(path, lint_claude_md_text(text))
    if kind == "plugin_json":
        return render(path, lint_plugin_json_text(text))
    if kind == "index":
        fs = _corpus_check.check_pack(p.parent.parent)
        return render(path, [(sev, 1, code, msg) for sev, code, msg in (fs or [])])
    if kind == "evals":
        skill_dir = p.parent.parent.name
        fs = [(sev, 1, code, msg) for sev, code, msg in _eval_check.check_suite_text(text, skill_dir)]
        return render(path, fs)
    return render(path, lint_text(text, p.parent.name))


def main_cli(paths):
    any_fail = False
    for path in paths:
        report, failed = lint_path(path)
        print(report)
        any_fail = any_fail or failed
    return 1 if any_fail else 0


def main_hook():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed event: a flaky hook is worse than none — stay quiet
    file_path = (event.get("tool_input") or {}).get("file_path", "")
    kind = classify(file_path)
    if kind is None or kind == "claude_md":  # entry-file edits are audited, not nagged
        return 0
    report, failed = lint_path(file_path)
    if failed:
        print(json.dumps({"decision": "block", "reason": report}))
    return 0  # the JSON carries the decision; warnings stay silent


GOOD_FIXTURE = """---
name: demo-review
description: >-
  Reviews demo artifacts against the house standard. Use when the user asks to
  review, audit, or critique a demo. NOT for authoring demos (demo-forge).
disable-model-invocation: false
user-invocable: true
---
# demo-review
The review cites file:line for every finding.
Done when every criterion carries a verdict.
"""

BAD_FIXTURE = """---
name: Demo_Helper
description: <b>helper</b> for stuff
---
You are a helpful demo assistant.
Please try to be careful and make sure to please the user, and try to check twice.
"""

GOOD_AGENT_FIXTURE = """---
name: demo-auditor
description: |
  Fresh-context auditor. Dispatch with a target and a destination.

  <example>
  user: "validate the draft"
  assistant: "Dispatching demo-auditor."
  </example>
model: inherit
tools: ["Read"]
---
The demo-auditor writes one report file and nothing else.
"""

BAD_AGENT_FIXTURE = """---
name: demo-auditor
description: Fresh-context auditor.

<example>
Context: reproduces the 2026-07-06 plugin-load incident.
</example>
model: inherit
---
Body.
"""


def selftest():
    good = lint_text(GOOD_FIXTURE, "demo-review")
    assert not [f for f in good if f[0] == "FAIL"], f"good fixture failed: {good}"
    bad = {f[2] for f in lint_text(BAD_FIXTURE, "Demo_Helper")}
    for rule in ("F2", "F3", "F7", "W3", "W6"):
        assert rule in bad, f"expected {rule} in {bad}"
    good_agent = lint_agent_text(GOOD_AGENT_FIXTURE)
    assert not [f for f in good_agent if f[0] == "FAIL"], f"good agent failed: {good_agent}"
    bad_agent = {f[2] for f in lint_agent_text(BAD_AGENT_FIXTURE)}
    assert "A2" in bad_agent, f"expected A2 in {bad_agent}"
    body70 = "\n".join(f"line {i}" for i in range(70))
    import re as _re
    fm = GOOD_AGENT_FIXTURE.split("---")[1]
    fm_rev  = _re.sub(r"(?m)^name: .*$", "name: demo-reviewer", fm)
    fm_gen  = _re.sub(r"(?m)^name: .*$", "name: demo-helper", fm)
    assert not any(f[2] == "A4" for f in lint_agent_text("---" + fm_rev + "---\n" + body70)), \
        "70-line -reviewer body is inside the dual-depth allowance (ruled 2026-07-16)"
    assert any(f[2] == "A4" for f in lint_agent_text("---" + fm_gen + "---\n" + body70)), \
        "70-line non-reviewer body must still warn A4"
    mention = GOOD_FIXTURE + "\nThe catalog discusses `NEVER`, `NEVER`, `NEVER`, `IMPORTANT`, `IMPORTANT`, `CRITICAL` as vocabulary.\n"
    assert not any(f[2] == "W7" for f in lint_text(mention, "demo-review")), "backticked markers are mentions, not uses"
    bare = GOOD_FIXTURE + ("\nNEVER do X. NEVER do Y. NEVER do Z. IMPORTANT note. IMPORTANT note. CRITICAL step.\n")
    assert any(f[2] == "W7" for f in lint_text(bare, "demo-review")), "bare markers over budget must warn"
    locks = GOOD_FIXTURE + ("\nScale to `0.96`, never `0.95` or below. Bounce is always `0`, never `0.1`. "
                            "Duration `200ms`, never `300ms`. Opacity from `0.4`, never `0`. "
                            "Blur `8px`, never `4px`. Stagger `50ms`, never `100ms`.\n")
    assert not any(f[2] == "W7" for f in lint_text(locks, "demo-review")), \
        "lowercase parameter locks are uncapped (standards 2026-07-15); W7 counts only the uppercase tier"
    reserved = GOOD_FIXTURE.replace("name: demo-review", "name: claude-md-audit")
    assert any(f[2] == "F8" for f in lint_text(reserved, "claude-md-audit")), "reserved word must fail F8"
    assert any(f[2] == "F8" for f in lint_text(GOOD_FIXTURE, "anthropic-helper")), "reserved dir must fail F8"
    assert not any(f[2] == "F8" for f in lint_text(GOOD_FIXTURE, "demo-review")), "clean name must not trip F8"
    verb_head = GOOD_FIXTURE.replace("name: demo-review", "name: demo-refactor")
    assert not any(f[2] == "W4" for f in lint_text(verb_head, "demo-refactor")), "verb head 'refactor' must not trip W4 (ADR-0001 allowlist)"
    facts_ui = GOOD_FIXTURE.replace("name: demo-review", "name: demo-facts")
    assert any(f[2] == "W5" for f in lint_text(facts_ui, "demo-facts")), \
        "ADR-0006: '-facts' head with user-invocable true must warn W5"
    rules_mo = (GOOD_FIXTURE.replace("name: demo-review", "name: demo-writing-rules")
                            .replace("user-invocable: true", "user-invocable: false"))
    assert not any(f[2] == "W5" for f in lint_text(rules_mo, "demo-writing-rules")), \
        "ADR-0006: model-only '-rules' knowledge skill must pass W5 clean"
    agentive = GOOD_FIXTURE.replace("name: demo-review", "name: demo-author")
    assert any(f[2] == "W4" for f in lint_text(agentive, "demo-author")), "agentive head 'author' must still trip W4"
    good_hooks = ('{"hooks": {"PostToolUse": [{"matcher": "Write|Edit", "hooks": '
                  '[{"type": "command", "command": "python3 \\"${CLAUDE_PLUGIN_ROOT}/scripts/x.py\\" --hook"}]}]}}')
    assert not lint_hooks_text(good_hooks), "wrapped hooks.json must pass clean"
    bad_hooks = ('{"PostToolUse": [{"matcher": "Write", "hooks": '
                 '[{"type": "command", "command": "/Users/dev/.claude/hooks/x.sh"}]}]}')
    bad_rules = {f[2] for f in lint_hooks_text(bad_hooks)}
    for rule in ("H2", "H5"):
        assert rule in bad_rules, f"expected {rule} in {bad_rules}"
    assert any(f[2] == "H1" for f in lint_hooks_text("{not json")), "invalid JSON must fail H1"
    long_md = "\n".join(f"line {i}: always run the linter" for i in range(220))
    md_rules = {f[2] for f in lint_claude_md_text(long_md)}
    assert {"C1", "C2"} <= md_rules, f"expected C1+C2 in {md_rules}"
    assert classify("x/agents/demo.md") == "agent"
    assert not [f for f in lint_plugin_json_text('{"name": "demo-plugin", "version": "1.2.3"}') if f[0] == "FAIL"]
    p_bad = {f[2] for f in lint_plugin_json_text('{"name": "Demo Plugin"}')}
    assert {"P2", "P3"} <= p_bad, f"expected P2+P3 in {p_bad}"
    assert classify("x/.claude-plugin/plugin.json") == "plugin_json"
    if _eval_check:
        assert classify("skills/demo/evals/evals.json") == "evals"
    if _corpus_check:
        assert classify("skills/demo/references/INDEX.md") == "index"
    assert classify("x/hooks/hooks.json") == "hooks"
    assert classify("x/CLAUDE.md") == "claude_md"
    assert classify("x/skills/demo/SKILL.md") == "skill"
    assert classify("x/notes.md") is None
    # #83 regression — classification is invocation-invariant: a bare relative
    # filename linted from inside an agents/ dir classifies as agent, identical
    # to its absolute path
    import os as _os
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _adir = Path(_td) / "agents"
        _adir.mkdir()
        _af = _adir / "probe.md"
        _af.write_text("---\nname: probe\n---\n")
        _cwd = _os.getcwd()
        try:
            _os.chdir(_adir)
            assert classify("probe.md") == "agent", "bare relative agent path must classify as agent"
            assert classify(str(_af)) == "agent", "absolute agent path must classify as agent"
        finally:
            _os.chdir(_cwd)
    print(f"{HOOK_NAME} selftest · PASS · skills bad={sorted(bad)} · agents bad={sorted(bad_agent)}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "--hook":
        sys.exit(main_hook())
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(main_cli(args))
