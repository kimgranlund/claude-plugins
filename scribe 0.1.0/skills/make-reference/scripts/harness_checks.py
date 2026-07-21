#!/usr/bin/env python3
"""harness_checks.py — mechanical [gate] checks for harness artifacts.

Routes the deterministic rubric dimensions to code instead of inference.
Judgment ([review]) dimensions are NOT checked here — score those against
the bundled rubric.md. This only verifies what is mechanically checkable.

Usage:
    python harness_checks.py <type> <file>
    python harness_checks.py goal "<goal string>"   # goal takes a string OR a file
    python harness_checks.py selftest               # fixture-locked proof of the gates

Types: skill agent claude-md llms-txt rubric reference prd spec lld goal

Exit 0 = all gate checks passed.  Exit 1 = at least one failed (fails loudly).

Selftest: runs the SAME check functions the CLI uses over embedded fixtures — one passing
skill, one failing fixture per skill gate (D1 no-trigger, D2 over-length, D5 no-loop, D7 bare
tool name, D9 dangling pointer, D9 dangling in-bundle markdown link, D10 name != dir, D11
contradictory invocation flags), one passing + one failing agent fixture, and negative controls
(a validation token inside an HTML comment must NOT satisfy D5; a bundle whose relative links
resolve — with scheme-URL, mailto:, pure-anchor, #fragment, and code-span/fence exclusions —
must PASS the D9 link gate).
Every OTHER mode is fixture-locked too: prd, spec, lld, rubric, claude-md, reference,
llms-txt, goal each carry one passing fixture + one that trips a representative gate
(rubric locks both new gates, D3 anchors and D5 evidence column; claude-md locks the
D1/D4 gate labels), plus a second negative control (a vague word embedded inside a longer
token — "cleanup" — must NOT trip the goal C1 vague-term check).
"""
import re
import sys
from pathlib import Path

VAGUE = ("clean", "elegant", "good", "nice", "properly", "robust", "well")


def read(arg: str) -> str:
    p = Path(arg)
    return p.read_text(encoding="utf-8") if p.exists() else arg


def frontmatter(text: str) -> str:
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    return m.group(1) if m else ""


class Result:
    def __init__(self):
        self.checks = []  # (ok, label, detail)

    def add(self, ok, label, detail=""):
        self.checks.append((bool(ok), label, detail))

    def report(self, title):
        print(f"== {title} ==")
        for ok, label, detail in self.checks:
            mark = "PASS" if ok else "FAIL"
            line = f"[{mark}] {label}"
            if detail and not ok:
                line += f" — {detail}"
            print(line)
        failed = [c for c in self.checks if not c[0]]
        print(f"-- {len(self.checks) - len(failed)}/{len(self.checks)} gate checks passed --")
        return 0 if not failed else 1


TOOL_VERB = r"(?:create|list|get|update|delete|send|search|fetch|add|remove|assign|archive|schedule|invite|move|merge)"
RESERVED_SKILLS = {
    "code-review", "debug", "run", "verify", "loop", "batch",
    "claude-api", "run-skill-generator",
}
# D9 placement — two INDEPENDENT registries (folder no longer needs to match role, or vice versa).
# AGENT_ROLES: the closed role enum an agent name's suffix must belong to (unchanged grammar).
AGENT_ROLES = {
    "coordinator", "explorer", "researcher", "reviewer", "planner",
    "builder", "tester", "writer", "author",
}
# AGENT_CONCEPT_FOLDERS: the concept-folder registry `agents/README.md` declares as canon.
# Extend THIS set, not AGENT_ROLES, when a new concept folder is ratified.
AGENT_CONCEPT_FOLDERS = {"design", "corpus", "delivery", "research"}
VALIDATION_RE = r"check|verif|re-?check|re-?run|validate|harness|exits?\s*clean|scripts/"
TRIG_RE = r"\b(use|when|whenever|invoke|apply|reach|if|after)\b"


def _description(fm):
    m = re.search(r"description:\s*(.*?)(?=\n[A-Za-z][\w-]*:\s|\Z)", fm, re.S)
    return " ".join(m.group(1).split()) if m else ""


# True markdown-link syntax only: [text](dest), optionally <dest> and a "title".
# Also matches the [alt](dest) inside an image ![alt](dest) — a dangling image is dangling too.
_MD_LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)<>\s]+)>?(?:\s+[\"'][^)]*)?\)")


def _md_link_targets(md_text):
    """RELATIVE markdown-link destinations in live prose, for the D9 in-bundle link gate.
    Code fences, inline code spans, and HTML comments are stripped first — backticked paths
    and prose mentions stay judgment-tier. Excluded: scheme URLs (https://…, mailto:),
    pure-anchor links (#…), and /-rooted paths (not bundle-relative); a #fragment is
    stripped before the target is resolved."""
    live = re.sub(r"<!--.*?-->", "", md_text, flags=re.S)
    live = re.sub(r"^[ \t]*```.*?^[ \t]*```", "", live, flags=re.S | re.M)
    live = re.sub(r"`[^`\n]+`", "", live)
    out = []
    for target in _MD_LINK.findall(live):
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):  # absolute URL: scheme:// or mailto:
            continue
        rel = target.split("#", 1)[0]                      # strip #fragment before resolving
        if not rel or rel.startswith("/"):                 # pure anchor / rooted path
            continue
        out.append(rel)
    return out


def check_skill(t, r, path=None):
    lines = t.count("\n") + 1
    r.add(lines <= 500, "D2 body <= 500 lines", f"{lines} lines")

    fm = frontmatter(t)
    desc = _description(fm)
    r.add(bool(desc), "D1 description present", "no description: field")
    r.add(bool(desc) and bool(re.search(TRIG_RE, desc, re.I)),
          "D1 description states a trigger",
          "states capability only -- add a when/use/if condition")
    r.add(len(desc) <= 1536, "D1 description within listing budget",
          f"{len(desc)} chars > ~1536 -- gets truncated in the menu")
    if desc and len(desc) > 200:
        r.add(bool(re.search(TRIG_RE, desc[:200], re.I)),
              "D1 trigger in first ~200 chars",
              "use-condition buried late -- lead with it")

    # body = everything after the frontmatter fence
    body = t
    if t.count("---") >= 2:
        body = t[t.index("---", t.index("---") + 3) + 3:]

    # D5 reads only LIVE prose: a validation token inside an HTML comment is not a loop the
    # model executes (selftest negative control pins this).
    body_live = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    r.add(bool(re.search(VALIDATION_RE, body_live, re.I)),
          "D5 validation loop present",
          "no check/verify/re-check/script step in the body")

    bare = sorted(set(re.findall(rf"`({TOOL_VERB}_[a-z0-9_]+)`", body)))
    r.add(not bare, "D7 tool refs qualified (Server:tool)",
          f"bare tool names -- qualify as Server:tool: {', '.join(bare)}")

    p = Path(path) if path else None
    if not (p and p.is_file()):
        return
    skill_dir = p.parent

    # D9 -- referenced depth resolves and is substantive (no dangling pointers, no stubs).
    #        Bundle is conditional: a skill that points at nothing ships nothing and passes.
    #        Match BUNDLE-relative `references/x.md` AND `resources/x.md` (foundation/knowledge
    #        docs live in either) -- the negative lookbehind excludes an external repo path
    #        (`.claude/docs/references/x.md`) the skill deliberately cites-not-copies, which D9 does not
    #        govern (that is the target repo's file, not the skill's bundle).
    referenced = sorted(set(re.findall(r"(?<![\w./-])((?:references|resources)/[A-Za-z0-9._-]+\.md)", body)))
    dangling, stubs = [], []
    for rel in referenced:
        fp = skill_dir / rel
        if not fp.is_file():
            dangling.append(rel)
            continue
        nonblank = [ln for ln in fp.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
        if len(nonblank) < 12 and fp.stat().st_size < 500:
            stubs.append(rel)
    r.add(not dangling, "D9 referenced files exist (no dangling pointers)",
          f"body points at missing: {', '.join(dangling)}")
    r.add(not stubs, "D9 referenced files are substantive (no stubs)",
          f"stub references: {', '.join(stubs)}")
    ref_scripts = sorted(set(re.findall(r"(?<![\w./-])scripts/([A-Za-z0-9._-]+\.(?:py|sh|js|ts))(?![\w])", body)))
    missing = [f for f in ref_scripts if not (skill_dir / "scripts" / f).is_file()]
    r.add(not missing, "D9 referenced scripts exist",
          f"body points at missing scripts: {', '.join(missing)}")

    # D9 -- in-bundle markdown links resolve: every RELATIVE [text](path) link in every bundle
    #        .md (SKILL.md + references/**/*.md + any other) must resolve on disk relative to
    #        its CONTAINING file. Exclusions live in _md_link_targets: absolute URLs, pure
    #        anchors, stripped #fragments; only true link syntax counts -- backticked paths and
    #        prose mentions stay judgment-tier.
    bad_links = []
    for md in sorted(skill_dir.rglob("*.md")):
        try:
            md_text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for rel in _md_link_targets(md_text):
            if not (md.parent / rel).exists():
                bad_links.append(f"{md.relative_to(skill_dir)} -> {rel}")
    r.add(not bad_links, "D9 in-bundle markdown links resolve",
          f"dangling relative links: {', '.join(bad_links)}")

    # D10 -- identity: the DIRECTORY name is the command (name: is display-only for skills)
    dirname = skill_dir.name
    r.add(bool(re.match(r"^[a-z0-9][a-z0-9-]*$", dirname)),
          "D10 directory is a valid command token",
          f"'{dirname}' -- skills invoke by directory name; use lowercase-kebab")
    nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    if nm:
        r.add(nm.group(1).strip() == dirname,
              "D10 name matches directory (or omit it)",
              f"name '{nm.group(1).strip()}' != directory '{dirname}' -- the directory is the command")
    r.add(dirname not in RESERVED_SKILLS,
          "D10 does not shadow a bundled skill",
          f"'/{dirname}' shadows a bundled skill -- higher precedence wins silently")

    # D11 -- invocation posture: the two frontmatter flags are mutually exclusive. Both true
    #        makes a skill unreachable by EITHER surface -- hidden from the / menu
    #        (user-invocable:false) AND hidden from Claude's context until invoked
    #        (disable-model-invocation:true) -- a silently dead capability nobody can fire.
    dmi = re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M)
    uninv_false = re.search(r"^user-invocable:\s*false\s*$", fm, re.M)
    r.add(not (dmi and uninv_false), "D11 invocation posture not contradictory",
          "both disable-model-invocation:true and user-invocable:false set -- "
          "unreachable by user (hidden from menu) AND by model (hidden from context)")


def check_agent(t, r):
    fm = frontmatter(t)
    r.add(re.search(r"^tools:", fm, re.M), "D2 tools scoped (not omitted)",
          "no tools: field — inherits full toolset incl. MCP")
    r.add(re.search(r"^model:", fm, re.M), "D5 model set")
    desc = re.search(r"description:\s*(.+)", fm, re.S)
    r.add(bool(desc) and re.search(r"\buse\b", desc.group(1), re.I),
          "D1 description states a trigger")
    r.add(not re.search(r"IMPORTANT:\s*never|never\s+(do|touch|write|call)", t, re.I),
          "D7 no enforcement-in-prose", "found 'never do X' style invariant — belongs in a hook")


def _name_of(text):
    m = re.search(r"^name:\s*(.+?)\s*$", frontmatter(text), re.M)
    return m.group(1).strip() if m else None


def _agents_root(path):
    """Nearest ancestor directory literally named 'agents' (the flat registry root)."""
    for parent in path.parents:
        if parent.name == "agents":
            return parent
    return None


def check_agent_placement(path, r):
    """D9 [gate] — collision-safety in the flat, global agent namespace.

    Identity is the `name` field only; the folder is cosmetic to resolution.
    A duplicate name is silently dropped, so this gate enforces the invariants
    that fail invisibly: the name's role suffix is registered, its folder is a
    registered concept, and the name is unique. Role and folder are checked
    INDEPENDENTLY — neither derives the other (folder is a concept the agent
    serves, recorded as a judgment call in agents/README.md; role is the
    closed <domain>-<role> morphological enum).
    """
    root = _agents_root(path)
    if root is None:
        r.add(True, "D9 placement/naming", "skipped: file is not under an agents/ tree")
        return
    name = _name_of(path.read_text(encoding="utf-8"))
    r.add(bool(name), "D9 frontmatter has name", "no name: field to resolve by")
    rel = path.relative_to(root)
    folder = rel.parts[0] if len(rel.parts) > 1 else None
    if name:
        role = name.split("-")[-1]
        r.add(role in AGENT_ROLES, "D9 name suffix is a registered role",
              f"name '{name}' suffix '{role}' is not in the registered role set: "
              f"{sorted(AGENT_ROLES)}")
    if folder:
        r.add(folder in AGENT_CONCEPT_FOLDERS, "D9 folder is a registered concept",
              f"folder '{folder}/' is not in agents/README.md's registered concept-folder "
              f"set: {sorted(AGENT_CONCEPT_FOLDERS)}")
    if name:
        dupes = []
        for md in root.rglob("*.md"):
            if md.name.upper() == "README.MD":
                continue
            try:
                other = _name_of(md.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                continue
            if other == name and md.resolve() != path.resolve():
                dupes.append(str(md.relative_to(root)))
        r.add(not dupes, "D9 name unique across the tree",
              f"'{name}' is also defined in: {', '.join(dupes)} — one silently wins")


def check_claude_md(t, r):
    # Gate IDs follow the entry-file-author rubric's D-labels (the rubric is the spine).
    lines = t.count("\n") + 1
    r.add(lines <= 200, "D1 \u2264 200 lines", f"{lines} lines")
    r.add(not re.search(r"IMPORTANT:\s*never|^\s*never\s", t, re.I | re.M),
          "D4 no 'IMPORTANT: never' as control", "enforcement belongs in a hook")


def check_llms_txt(t, r):
    r.add(re.search(r"^#\s+\S", t, re.M), "D1 has H1 project name")
    r.add(re.search(r"^>\s+\S", t, re.M), "D1 has blockquote summary")
    r.add(re.search(r"^##\s+\S", t, re.M), "D1 has \u2265 1 H2 section")
    r.add(re.search(r"\[[^\]]+\]\([^)]+\)", t), "D2 has \u2265 1 markdown link")


def check_rubric(t, r):
    # Dimension-id prefixes in use across the corpus: D/P/S/L/C/A/B plus R (research-methods),
    # V (vision-memo), H (handoff-compose). A row is a table line (>=3 pipes) carrying such an id.
    rows = [ln for ln in t.splitlines() if ln.count("|") >= 3
            and re.search(r"\b[DPSLCABRVH]\d", ln)]
    r.add(len(rows) >= 1, "structure: dimension table present", "no dimension rows found")
    if rows:
        typed = all(("[gate]" in ln or "[review]" in ln) for ln in rows)
        r.add(typed, "D1 every dimension typed [gate]/[review]")
        # D3 -- behavioral anchors: every dimension row carries 1/3/5 anchor text
        # ("1: ... 3: ... 5: ..."), not a bare scale.
        def dim_id(ln):
            m = re.search(r"\b([A-Z]\d+)\b", ln)
            return m.group(1) if m else ln.strip().strip("|").strip()[:24]
        unanchored = sorted({dim_id(ln) for ln in rows
                             if not all(re.search(rf"\b{lvl}\s*:", ln) for lvl in (1, 3, 5))})
        r.add(not unanchored, "D3 every dimension carries 1/3/5 anchors",
              f"bare scale (no 1:/3:/5: descriptors) on: {', '.join(unanchored)}")
    # D5 -- measurement plan: the table has a column stating HOW each dimension is checked.
    r.add(re.search(r"^\|[^\n]*\b(what it checks|evidence|how to (?:check|measure)|measurement)\b",
                    t, re.I | re.M),
          "D5 evidence column present",
          "no 'What it checks' / evidence column stating how each dimension is measured")
    # Accept any "Gate to <verb>" (promote / ship / accept …) — the verb suits the artifact (a memo
    # ships, an investigation is accepted, a doc is promoted); a bare "Gate:" line also counts.
    r.add(re.search(r"gate\s+to\s+\w+|^gate:", t, re.I | re.M),
          "D8 aggregation/gate rule present")


def check_reference(t, r):
    r.add(len(re.findall(r"^#{1,6}\s+\S", t, re.M)) >= 2, "D1 has headings (scannable)")
    r.add(re.search(r"\b20\d\d[-/]\d|updated|source:|version", t, re.I),
          "D5 freshness marker present", "no date/source/version on volatile content")


def _ids(text, pat):
    return set(re.findall(pat, text))


def check_prd(t, r):
    r.add(bool(_ids(t, r"PRD-G\d+")), "P7 goal IDs present (PRD-G#)")
    r.add(re.search(r"out[- ]?of[- ]?scope|^\s*out:", t, re.I | re.M), "P3 out-of-scope stated")
    r.add(re.search(r"\bmust\b|\bshould\b|\bcould\b|priority", t, re.I), "P5 prioritization present")


def check_spec(t, r):
    r.add(bool(_ids(t, r"SPEC-R\d+")), "S7 requirement IDs present (SPEC-R#)")
    r.add(bool(_ids(t, r"PRD-G\d+")), "S1 traces up to PRD goals (PRD-G#)")
    r.add(re.search(r"acceptance|given .*when .*then", t, re.I | re.S), "S2 acceptance criteria present")


def check_lld(t, r):
    r.add(bool(_ids(t, r"LLD-C\d+")), "L1 component IDs present (LLD-C#)")
    r.add(bool(_ids(t, r"SPEC-R\d+")), "L1 traces up to SPEC requirements (SPEC-R#)")
    r.add(re.search(r"error|edge|failure|fallback", t, re.I), "L5 error/edge handling section present")


def check_goal(t, r):
    r.add(re.search(r"stop after|\b\d+\s*(turn|minute|hour)", t, re.I), "C3 bounded (turn/time cap)")
    measurable = re.search(r"exits?\s*0|passes|== |\bzero\b|\btest", t, re.I) or re.search(r"\d", t)
    r.add(bool(measurable), "C1 measurable end-state token present")
    vague = [w for w in VAGUE if re.search(rf"\b{w}\b", t, re.I)]
    r.add(not vague, "C1 no vague success terms", f"vague: {', '.join(vague)}")


CHECKS = {
    "skill": check_skill, "agent": check_agent, "claude-md": check_claude_md,
    "llms-txt": check_llms_txt, "rubric": check_rubric, "reference": check_reference,
    "prd": check_prd, "spec": check_spec, "lld": check_lld, "goal": check_goal,
}


# --- selftest ------------------------------------------------------------------------------------
# Fixture-locked proof of the gate checks. Purely ADDITIVE: it drives the SAME check functions the
# CLI uses and asserts each gate fires (fail fixtures) or holds (pass fixtures). 9 sibling skills
# symlink this file — the selftest is the lock that lets the shared gates be edited safely.

_FIX_SKILL_PASS = """---
name: selftest-pass
description: Formats fixture skills for the harness selftest. Use when the selftest needs a fully passing skill fixture.
---
# Selftest passing fixture
1. Draft the artifact.
2. Check it against the reference; fix and re-check until it exits clean.
"""

# D1 — description present but names NO trigger condition (no use/when/if/... vocabulary).
_FIX_SKILL_D1 = """---
name: selftest-d1
description: Formats fixture text blocks for the harness selftest suite.
---
# Fixture
1. Draft the artifact.
2. Check it against the reference and re-check.
"""

# D5 — no validation loop anywhere in the body.
_FIX_SKILL_D5 = """---
name: selftest-d5
description: Demo fixture. Use when the selftest needs a loopless skill fixture.
---
# Fixture
1. Draft the artifact.
2. Save it and stop.
"""

# D5 negative control (comment-trap) — the ONLY validation token sits inside an HTML comment,
# which the model never executes; D5 must still FAIL.
_FIX_SKILL_D5_COMMENT = """---
name: selftest-d5c
description: Demo fixture. Use when the selftest needs the comment-trap fixture.
---
# Fixture
1. Draft the artifact.
2. Save it and stop.
<!-- verify: a gate token inside a comment must NOT satisfy D5 -->
"""

# D7 — a bare (unqualified) MCP tool name.
_FIX_SKILL_D7 = """---
name: selftest-d7
description: Demo fixture. Use when the selftest needs a bare-tool skill fixture.
---
# Fixture
1. Call `create_issue` on the tracker.
2. Check the result and re-check.
"""

# D9 — body points at a references/ file that does not exist in the bundle.
_FIX_SKILL_D9 = """---
name: selftest-d9
description: Demo fixture. Use when the selftest needs a dangling-pointer fixture.
---
# Fixture
1. Read references/ghost.md first.
2. Check the result and re-check.
"""

# D9 links — a bundle reference doc carries a dangling RELATIVE markdown link; the target must
# resolve against the CONTAINING file (references/), not the skill root, so the gate must bite.
_FIX_SKILL_D9LINK = """---
name: selftest-d9link
description: Demo fixture. Use when the selftest needs a dangling-link fixture.
---
# Fixture
1. Read references/guide.md first.
2. Check the result and re-check.
"""

_FIX_D9LINK_REF_BAD = "\n".join(
    ["# Guide", "", "See [the missing appendix](missing.md) for detail."]
    + ["Substantive line %d so the stub gate stays quiet." % i for i in range(12)]) + "\n"

# D9 links reverse control — resolving relative links (SKILL.md -> references/, references/ ->
# ../SKILL.md) plus every exclusion class: scheme URL, mailto:, pure #anchor, #fragment on a
# resolving target, and link-shaped text inside a code span / code fence. Must fully PASS.
_FIX_SKILL_D9LINK_OK = """---
name: selftest-d9link-ok
description: Demo fixture. Use when the selftest needs the resolving-links fixture.
---
# Fixture
1. Read [the guide](references/guide.md#usage) and the [docs](https://example.com/docs).
2. Mail [the owner](mailto:owner@example.com) or jump to [usage](#usage).
3. Check the result and re-check.

## Usage
The backticked `[not-a-link](ghost.md)` stays judgment-tier.
"""

_FIX_D9LINK_REF_OK = "\n".join(
    ["# Guide", "", "Back to [the skill](../SKILL.md).", "",
     "```", "[fenced example](ghost.md) inside a code fence stays exempt.", "```", ""]
    + ["Substantive line %d so the stub gate stays quiet." % i for i in range(12)]) + "\n"

# D10 — frontmatter name contradicts the directory (the directory is the command).
_FIX_SKILL_D10 = """---
name: selftest-mismatch
description: Demo fixture. Use when the selftest needs a name-mismatch fixture.
---
# Fixture
1. Check the result and re-check.
"""

# D11 — both invocation flags set: unreachable by the user (hidden from the / menu) AND by
# the model (hidden from context until invoked) at once.
_FIX_SKILL_D11 = """---
name: selftest-d11
description: Demo fixture. Use when the selftest needs a contradictory-invocation fixture.
disable-model-invocation: true
user-invocable: false
---
# Fixture
1. Check the result and re-check.
"""

_FIX_AGENT_PASS = """---
name: selftest-reviewer
description: Reviews selftest fixtures. Use PROACTIVELY after the harness changes.
tools: Read, Grep
model: haiku
---
Focus on the diff; return a one-paragraph summary.
"""

# Fails every agent gate: no tools (inherits everything), no model, no trigger word in the
# description, and an enforcement-in-prose invariant that belongs in a hook.
_FIX_AGENT_FAIL = """---
name: selftest-bad
description: A helpful agent for demos.
---
IMPORTANT: never touch production systems.
"""

# D9 placement fixtures — role and folder are now independent registries; a valid role suffix
# must pass in ANY registered concept folder, and an unregistered role must fail regardless.
_FIX_AGENT_PLACEMENT_OK = """---
name: foo-reviewer
description: Reviews foo. Use PROACTIVELY after foo changes.
tools: Read, Grep
model: haiku
---
Body.
"""

_FIX_AGENT_PLACEMENT_BAD_ROLE = """---
name: foo-frobnicator
description: Frobnicates foo. Use PROACTIVELY after foo changes.
tools: Read, Grep
model: haiku
---
Body.
"""

# --- fixtures for the non-skill, non-agent modes (one pass + one representative trip each) ------

_FIX_PRD_PASS = """# PRD — selftest fixture
Goals: PRD-G1 must reduce checker toil; PRD-G2 must cut review latency.
Out of scope: mobile clients.
Priority: must-have.
"""

# P3 — no out-of-scope statement anywhere.
_FIX_PRD_P3 = """# PRD — selftest fixture
Goals: PRD-G1 must reduce checker toil.
Priority: must-have.
"""

_FIX_SPEC_PASS = """# SPEC — selftest fixture
SPEC-R1 (serves PRD-G1): the checker exits 0 on a conforming artifact.
Acceptance: given a conforming artifact, when the checker runs, then it exits 0.
"""

# S1 — requirements present but no PRD goal referenced.
_FIX_SPEC_S1 = """# SPEC — selftest fixture
SPEC-R1: the checker exits 0 on a conforming artifact.
Acceptance: given a conforming artifact, when the checker runs, then it exits 0.
"""

_FIX_LLD_PASS = """# LLD — selftest fixture
LLD-C1 implements SPEC-R1: the parser module.
Error handling: malformed input returns exit code 2.
"""

# L5 — no error/edge/failure/fallback handling named.
_FIX_LLD_L5 = """# LLD — selftest fixture
LLD-C1 implements SPEC-R1: the parser module. Happy path described only.
"""

_FIX_RUBRIC_PASS = """| # | Dimension | Type | What it checks | 1 → 3 → 5 |
|---|---|---|---|---|
| D1 | Naming | [gate] | Name matches directory | 1: mismatch · 3: close · 5: exact |
Gate to promote: D1 >= 3.
"""

# D3 — a dimension row with a bare scale (no 1:/3:/5: anchor text).
_FIX_RUBRIC_D3 = """| # | Dimension | Type | What it checks | 1 → 3 → 5 |
|---|---|---|---|---|
| D1 | Naming | [gate] | Name matches directory | bad → good |
Gate to promote: D1 >= 3.
"""

# D5 — no evidence / "What it checks" column in the table header.
_FIX_RUBRIC_D5 = """| # | Dimension | Type | 1 → 3 → 5 |
|---|---|---|---|
| D1 | Naming | [gate] | 1: mismatch · 3: close · 5: exact |
Gate to promote: D1 >= 3.
"""

_FIX_CLAUDE_MD_PASS = """# Project notes
Build: make test
"""

# D4 — enforcement-in-prose ("IMPORTANT: never ...") used as a control.
_FIX_CLAUDE_MD_D4 = """# Project notes
IMPORTANT: never commit directly to main.
"""

_FIX_REFERENCE_PASS = """# Topic — selftest fixture
Updated: 2026-07-03
## Detail
The load-bearing facts live here.
"""

# D5 — volatile content with no freshness marker (no date/updated/source/version).
_FIX_REFERENCE_D5 = """# Topic — selftest fixture
## Detail
The load-bearing facts live here.
"""

_FIX_LLMS_TXT_PASS = """# Project
> One-line summary of the corpus.
## Docs
- [Guide](docs/guide.md)
"""

# D1 — no blockquote summary under the H1.
_FIX_LLMS_TXT_D1 = """# Project
## Docs
- [Guide](docs/guide.md)
"""

_FIX_GOAL_PASS = "Run pytest until it exits 0; stop after 10 turns."

# C3 — no turn/time bound anywhere.
_FIX_GOAL_C3 = "Run pytest until it exits 0."

# Negative control — "cleanup" embeds the vague word "clean" inside a longer token;
# the C1 vague-term check is word-bounded and must NOT fire.
_FIX_GOAL_CLEANUP = "Run the cleanup script, then rerun pytest until it exits 0; stop after 5 turns."


def _selftest_skill(tmp, dirname, content, extra=None):
    """Write the fixture as <tmp>/<dirname>/SKILL.md (plus any extra bundle files, keyed by
    bundle-relative path) and return {check label: ok}."""
    d = Path(tmp) / dirname
    d.mkdir()
    p = d / "SKILL.md"
    p.write_text(content, encoding="utf-8")
    for rel, body in (extra or {}).items():
        fp = d / rel
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(body, encoding="utf-8")
    r = Result()
    check_skill(content, r, str(p))
    return {label: ok for ok, label, _ in r.checks}


def _selftest_agent(content):
    r = Result()
    check_agent(content, r)
    return {label: ok for ok, label, _ in r.checks}


def _selftest_agent_placement(rel_path, content):
    """Write <throwaway tmp>/agents/<rel_path> and run check_agent_placement on it — a real
    filesystem path is required since the check walks the tree for name collisions."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "agents" / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        r = Result()
        check_agent_placement(p, r)
        return {label: ok for ok, label, _ in r.checks}


def _run_mode(kind, content):
    """Drive the SAME check function the CLI routes <kind> to; return {label: ok}."""
    r = Result()
    CHECKS[kind](content, r)
    return {label: ok for ok, label, _ in r.checks}


def _selftest_modes(errs):
    """Fixture-lock the non-skill, non-agent modes: pass fixture holds every gate,
    trip fixture fires exactly the representative gate named for it."""
    # (kind, pass fixture, trip fixture, label of the gate the trip fixture must fire)
    cases = [
        ("prd", _FIX_PRD_PASS, _FIX_PRD_P3, "P3 out-of-scope stated"),
        ("spec", _FIX_SPEC_PASS, _FIX_SPEC_S1, "S1 traces up to PRD goals (PRD-G#)"),
        ("lld", _FIX_LLD_PASS, _FIX_LLD_L5, "L5 error/edge handling section present"),
        ("rubric", _FIX_RUBRIC_PASS, _FIX_RUBRIC_D3, "D3 every dimension carries 1/3/5 anchors"),
        ("claude-md", _FIX_CLAUDE_MD_PASS, _FIX_CLAUDE_MD_D4, "D4 no 'IMPORTANT: never' as control"),
        ("reference", _FIX_REFERENCE_PASS, _FIX_REFERENCE_D5, "D5 freshness marker present"),
        ("llms-txt", _FIX_LLMS_TXT_PASS, _FIX_LLMS_TXT_D1, "D1 has blockquote summary"),
        ("goal", _FIX_GOAL_PASS, _FIX_GOAL_C3, "C3 bounded (turn/time cap)"),
    ]
    for kind, fix_pass, fix_trip, label in cases:
        c = _run_mode(kind, fix_pass)
        bad = [k for k, ok in c.items() if not ok]
        if bad:
            errs.append("%s: passing fixture failed gates: %s" % (kind, bad))
        c = _run_mode(kind, fix_trip)
        if label not in c:
            errs.append("%s: gate label '%s' missing — labels drifted" % (kind, label))
        elif c[label]:
            errs.append("%s: trip fixture did not fire '%s'" % (kind, label))

    # rubric D5 — a table with no evidence column must fire the new evidence-column gate
    c = _run_mode("rubric", _FIX_RUBRIC_D5)
    if c.get("D5 evidence column present", True):
        errs.append("rubric: evidence-less table did not fire 'D5 evidence column present'")

    # claude-md relabel lock — the emitted gate IDs follow the rubric's D-labels, not B-labels
    c = _run_mode("claude-md", _FIX_CLAUDE_MD_PASS)
    if "D1 ≤ 200 lines" not in c:
        errs.append("claude-md: length gate not labeled 'D1' (rubric labels drifted)")
    if any(label.startswith("B") for label in c):
        errs.append("claude-md: emits B-labels; the rubric's D-labels are the spine")

    # negative control (word-boundary trap) — "cleanup" embeds the vague word "clean";
    # the goal C1 vague-term check must NOT fire on it
    c = _run_mode("goal", _FIX_GOAL_CLEANUP)
    if not c.get("C1 no vague success terms", False):
        errs.append("goal cleanup-trap: 'clean' inside 'cleanup' wrongly tripped the vague-term check")


def selftest():
    import tempfile
    errs = []
    with tempfile.TemporaryDirectory() as tmp:
        # 1. passing skill fixture — every gate check holds
        c = _selftest_skill(tmp, "selftest-pass", _FIX_SKILL_PASS)
        bad = [k for k, ok in c.items() if not ok]
        if bad:
            errs.append("passing skill fixture failed gates: %s" % bad)

        # 2. D1 — no-trigger description must fail the trigger check (and nothing else about D1)
        c = _selftest_skill(tmp, "selftest-d1", _FIX_SKILL_D1)
        if c.get("D1 description states a trigger", True):
            errs.append("D1: trigger-less description not flagged")
        if not c.get("D1 description present", False):
            errs.append("D1: fixture's present description wrongly flagged missing")

        # 3. D2 — an over-length body must fail the line budget
        c = _selftest_skill(tmp, "selftest-d2", _FIX_SKILL_PASS + "filler line\n" * 520)
        if c.get("D2 body <= 500 lines", True):
            errs.append("D2: 500+-line body not flagged")

        # 4. D5 — a loopless body must fail
        c = _selftest_skill(tmp, "selftest-d5", _FIX_SKILL_D5)
        if c.get("D5 validation loop present", True):
            errs.append("D5: loopless body not flagged")

        # 5. D5 negative control (comment-trap) — a gate token inside an HTML comment must NOT
        #    satisfy D5; the check reads live prose only
        c = _selftest_skill(tmp, "selftest-d5c", _FIX_SKILL_D5_COMMENT)
        if c.get("D5 validation loop present", True):
            errs.append("D5 comment-trap: a validation token inside an HTML comment satisfied D5")

        # 6. D7 — a bare backticked tool verb must fail hygiene
        c = _selftest_skill(tmp, "selftest-d7", _FIX_SKILL_D7)
        if c.get("D7 tool refs qualified (Server:tool)", True):
            errs.append("D7: bare `create_issue` not flagged")

        # 7. D9 — a dangling references/ pointer must fail
        c = _selftest_skill(tmp, "selftest-d9", _FIX_SKILL_D9)
        if c.get("D9 referenced files exist (no dangling pointers)", True):
            errs.append("D9: dangling references/ghost.md not flagged")

        # 8. D9 links — a dangling RELATIVE markdown link in a bundle .md must fail; the fixture
        #    plants it in references/guide.md, so this also locks containing-file resolution
        c = _selftest_skill(tmp, "selftest-d9link", _FIX_SKILL_D9LINK,
                            extra={"references/guide.md": _FIX_D9LINK_REF_BAD})
        if c.get("D9 in-bundle markdown links resolve", True):
            errs.append("D9 links: dangling [.](missing.md) in references/guide.md not flagged")

        # 9. D9 links reverse control — resolving links plus the exclusion classes (scheme URL,
        #    mailto:, pure #anchor, #fragment stripping, code span/fence) must hold EVERY gate
        c = _selftest_skill(tmp, "selftest-d9link-ok", _FIX_SKILL_D9LINK_OK,
                            extra={"references/guide.md": _FIX_D9LINK_REF_OK})
        bad = [k for k, ok in c.items() if not ok]
        if bad:
            errs.append("D9 links reverse control: resolving-links bundle failed gates: %s" % bad)

        # 10. D10 — name != directory must fail identity
        c = _selftest_skill(tmp, "selftest-d10", _FIX_SKILL_D10)
        if c.get("D10 name matches directory (or omit it)", True):
            errs.append("D10: name/directory mismatch not flagged")

        # 11. D11 — both invocation flags set must fail (unreachable by user AND model)
        c = _selftest_skill(tmp, "selftest-d11", _FIX_SKILL_D11)
        if c.get("D11 invocation posture not contradictory", True):
            errs.append("D11: both invocation flags set (unreachable skill) not flagged")

    # 12. agent fixtures — the passing one holds every agent gate; the failing one trips them all
    c = _selftest_agent(_FIX_AGENT_PASS)
    bad = [k for k, ok in c.items() if not ok]
    if bad:
        errs.append("passing agent fixture failed gates: %s" % bad)
    c = _selftest_agent(_FIX_AGENT_FAIL)
    for label in ("D2 tools scoped (not omitted)", "D5 model set",
                  "D1 description states a trigger", "D7 no enforcement-in-prose"):
        if c.get(label, True):
            errs.append("agent fail-fixture: '%s' did not fire" % label)

    # 12b. D9 placement — role registry and concept-folder registry are independent gates now;
    #      folder no longer needs to match role, so prove both directions plus the cross case.
    # (i) a valid role suffix in ANY registered concept folder passes.
    c = _selftest_agent_placement("design/foo-reviewer.md", _FIX_AGENT_PLACEMENT_OK)
    if not c.get("D9 name suffix is a registered role", False):
        errs.append("D9 placement: registered role 'reviewer' wrongly flagged in design/")
    if not c.get("D9 folder is a registered concept", False):
        errs.append("D9 placement: registered folder 'design/' wrongly flagged")

    # (ii) an unregistered role suffix fails regardless of folder.
    c = _selftest_agent_placement("corpus/foo-frobnicator.md", _FIX_AGENT_PLACEMENT_BAD_ROLE)
    if c.get("D9 name suffix is a registered role", True):
        errs.append("D9 placement: unregistered role suffix 'frobnicator' not flagged")
    if not c.get("D9 folder is a registered concept", False):
        errs.append("D9 placement: registered folder 'corpus/' wrongly flagged alongside bad role")

    # (iii) a registered role suffix in an UNregistered (legacy role-name) folder fails.
    c = _selftest_agent_placement("reviewer/foo-reviewer.md", _FIX_AGENT_PLACEMENT_OK)
    if not c.get("D9 name suffix is a registered role", False):
        errs.append("D9 placement: registered role 'reviewer' wrongly flagged in legacy reviewer/")
    if c.get("D9 folder is a registered concept", True):
        errs.append("D9 placement: legacy role-folder 'reviewer/' not flagged as unregistered")

    # 13. every other mode — pass/trip fixture pairs + the goal word-boundary negative control
    _selftest_modes(errs)
    return errs


def selftest_main():
    errs = selftest()
    if errs:
        print("harness_checks selftest: FAIL (%d)" % len(errs))
        for e in errs:
            print("  - %s" % e)
        return 1
    print("harness_checks selftest: OK — skill gates D1/D2/D5/D7/D9/D10/D11 fire and hold (incl. the "
          "D9 in-bundle markdown-link gate + its resolving-links reverse control), agent gates "
          "fire and hold (incl. D9 placement's independent role-registry + concept-folder-"
          "registry checks), prd/spec/lld/rubric/claude-md/reference/llms-txt/goal fixtures fire and "
          "hold (incl. rubric D3 anchors + D5 evidence column, claude-md D-labels), comment-trap "
          "and cleanup-trap negative controls bite")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "selftest":
        return selftest_main()
    if len(argv) < 3 or argv[1] not in CHECKS:
        print(f"usage: harness_checks.py <{'|'.join(CHECKS)}|selftest> <file|string>")
        return 2
    kind, arg = argv[1], argv[2]
    text = read(arg)
    r = Result()
    if kind == "skill":
        check_skill(text, r, arg)  # path-aware: D9 checks the sibling references/ bundle
    else:
        CHECKS[kind](text, r)
    if kind == "agent":
        p = Path(arg)
        if p.exists():
            check_agent_placement(p, r)  # D9: name<->folder coherence + tree-wide uniqueness
    return r.report(kind)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
