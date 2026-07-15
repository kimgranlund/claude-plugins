#!/usr/bin/env python3
"""agent_corpus_index.py — the deterministic Phase-0 index for an AGENT-corpus audit.

Reads every `*.md` **recursively** under an agents dir (so the canonical concept-subfoldered
layout — `design/…`, `corpus/…`, `delivery/…` — is covered, not just a flat dir) and emits the
mechanical facts the corpus-level audit dimensions lean on — the ones no single-agent review can see:

  N (naming strategy) → `<domain-noun>-<role>` grammar: role histogram + collisions (flagged
                        ARITHMETICALLY: a role repeats with a repeated domain — duplicate agents —
                        or with a member carrying no domain qualifier; a role family whose domains
                        are all distinct is domain-disambiguated, NOT a collision), redundant
                        `-agent` suffixes, name uniqueness (the flat per-scope namespace silently
                        drops a duplicate; a repo-local `.claude/agents` name shadows the
                        same-named user-scope agent), and non-agent files polluting the dir.
  F (routing differentiation, pairwise) → each agent's OWN quoted trigger phrases (the concrete
                        "…" examples its description cites) tested against every OTHER agent's
                        description via `${CLAUDE_PLUGIN_ROOT}/scripts/routing_eval.py`'s lexical-overlap
                        proxy. A hit — a sibling's description also fires on this agent's own
                        example trigger, with no NOT-for fence naming this agent — is a candidate
                        routing collision: [review], the rubric's F-row "differentiated from every
                        peer" leg, made deterministic instead of a hand read. Needs no external
                        corpus: each agent supplies its own test phrases.
  S (skill leverage)  → the agent → `skills:` preload graph: which global/project skills each agent
                        preloads, dangling preloads (a skill that does not exist), and agents that
                        preload NOTHING (candidate under-leverage — 1+1=3 left on the table).

Facts and unambiguous violations (non-agent file, duplicate name, dangling preload) are reported.
Whether an empty preload is a real *under-leverage*, whether a flagged N collision is a duplicate to
merge or a missing qualifier, and whether a flagged F collision needs a fence or is a benign shared-
domain proxy artifact, is a [review] call — the scorer judges; this tool lays out the graph. None of
these are hard violations (they don't set the exit code) — only structural hazards do.

Usage:  python agent_corpus_index.py <agents_dir> [skills_root ...]
        python agent_corpus_index.py selftest
        # default skills root: <agents_dir>/../skills (this plugin's own skills/ dir)
Exit 0 = no hard violation.  Exit 1 = at least one (non-agent file / duplicate name / dangling preload).
Selftest: negative controls (duplicate name, dangling preload, non-agent file — each must bite),
collision arithmetic (distinct domains suppressed, bare-role/repeated-domain flagged), F-differentiation
(an unfenced sibling collision must fire; the same pair with a truthful fence must be suppressed), and
a reverse control (this plugin's own real agents/ estate, when present, passes clean).
"""
import importlib.util
import io
import re
import sys
import tempfile
from pathlib import Path

F_THRESHOLD = 0.34  # matches routing_eval.py's own default routing threshold
# A short trigger phrase (after stopword-stripping) is almost always a generic domain word this
# whole corpus shares ("review"/"agent"/"score"/"skill" appear in nearly every reviewer's
# description) -- the exact "corpus-universal stopword" trap routing_eval's own doctrine warns
# against fencing. Empirically: on the real 13-agent estate, unfiltered F-differentiation produced
# 87 findings, almost entirely 2-token overlaps like "review this agent"; requiring >=3 content
# tokens cuts that to the phrases carrying real distinguishing signal.
F_MIN_PHRASE_TOKENS = 3


def _load_routing_eval():
    """Import routing_eval.py from this plugin's own scripts/ root, resolving from THIS file's
    location upward (works regardless of which plugin hosts it — forge keeps it at
    <plugin-root>/scripts/routing_eval.py, a sibling of skill_lint.py/release_gate.py, not nested
    under a per-skill directory). Returns the module, or None if unresolvable (F section then
    reports itself skipped — never a silent no-op posing as a clean pass)."""
    here = Path(__file__).resolve()
    candidates = [p / "scripts" / "routing_eval.py" for p in here.parents]
    for cand in candidates:
        if cand.is_file():
            spec = importlib.util.spec_from_file_location("routing_eval", cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None

FM = re.compile(r"^---\n(.*?)\n---", re.S)


def field(fm, key):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


def preload_list(fm):
    """Two valid YAML shapes for `skills:` — inline (`skills: [a, b]`) and block (`skills:` then
    indented `- a` / `- b` lines); `field()`'s same-line regex only sees the inline shape (its
    greedy `\\s*` swallows into a block list's first `- item` line otherwise, corrupting the
    return to a single dash-prefixed entry — the exact silent-corruption failure this function
    exists to prevent elsewhere). Detect the shape before parsing rather than assume one."""
    m = re.search(r"^skills:[ \t]*(\[.*\])?[ \t]*$", fm, re.M)
    if not m:
        return []
    inline = m.group(1)
    if inline is not None:
        return [s.strip() for s in inline.strip("[]").split(",") if s.strip()]
    block = []
    for line in fm[m.end():].split("\n"):
        bm = re.match(r"^[ \t]+-[ \t]*(\S.*)$", line)
        if bm:
            block.append(bm.group(1).strip())
            continue
        if line.strip() == "":
            continue
        break
    return block


def full_description(fm):
    """The full `description:` value, folding a YAML block scalar (`>-`/`>`/`|-`/`|`) if the
    frontmatter uses one — `field()` only sees the same-line text, so a folded description (the
    house style for anything past one line) reads as empty there. Good enough for this corpus's
    actual frontmatter shapes; not a general YAML parser."""
    lines = fm.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^description:\s*(.*)$", line)
        if not m:
            continue
        rest = m.group(1).strip()
        if rest in (">", ">-", ">+", "|", "|-", "|+"):
            block = []
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "":
                    block.append("")
                    continue
                if not lines[j].startswith((" ", "\t")):
                    break
                block.append(lines[j].strip())
            if rest.startswith("|"):
                return "\n".join(block)
            return " ".join(seg for seg in block if seg)
        return rest.strip('"').strip("'")
    return ""


_QUOTED = re.compile(r'"([^"]{3,})"')


def quoted_triggers(description):
    """The concrete '…' example phrases a description cites — used as F-differentiation's own
    per-agent test corpus (no external corpus needed: each agent supplies its own probes)."""
    return [m.strip() for m in _QUOTED.findall(description)]


def load(agents_dir):
    """-> (agents: list — one entry PER FILE, so same-name duplicates survive to be flagged —
    and nonagents: rel paths of *.md files with no frontmatter/name)."""
    agents, nonagents = [], []
    for p in sorted(agents_dir.rglob("*.md")):
        if p.name == "README.md":
            continue
        rel = str(p.relative_to(agents_dir))
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = FM.match(text)
        fm = m.group(1) if m else ""
        name = field(fm, "name")
        if not m or not name:
            nonagents.append(rel)
            continue
        agents.append({
            "file": rel,
            "name": name,
            "has_desc": bool(re.search(r"^description:", fm, re.M)),
            "description": full_description(fm),
            "tools": field(fm, "tools"),
            "model": field(fm, "model"),
            "preloads": preload_list(fm),
            "role": name.split("-")[-1],
            "domain": "-".join(name.split("-")[:-1]) or "(none)",
        })
    return agents, nonagents


def role_collides(members):
    """ARITHMETIC collision test for one role's members (no judgment): a role family collides iff
    a domain repeats (duplicate agents) or a member carries no domain qualifier (bare role name).
    All-distinct domains = domain-disambiguated = NOT a collision (8 reviewers with 8 domains are
    one grammar, not 8 duplicates)."""
    if len(members) < 2:
        return False
    domains = [m["domain"] for m in members]
    return len(set(domains)) < len(domains) or "(none)" in domains


def run_index(agents_dir, roots, out):
    """The index body. Writes the report to `out`; returns 0 (clean) or 1 (hard violation)."""
    known = set()
    for r in roots:
        if r.is_dir():
            known |= {d.name for d in r.iterdir() if d.is_dir()}

    agents, nonagents = load(agents_dir)
    violation = False
    out.write(f"== agent-corpus index: {len(agents)} agents under {agents_dir} ==\n")
    out.write(f"   skill roots: {', '.join(str(r) for r in roots if r.is_dir()) or '(none found)'}\n\n")

    # ---- N: naming --------------------------------------------------------
    out.write("-- N: naming grammar --\n")
    roles = {}
    for a in agents:
        roles.setdefault(a["role"], []).append(a)
    for role, members in sorted(roles.items()):
        names = sorted(m["name"] for m in members)
        if role_collides(members):
            mark = "   <-- ROLE COLLISION (duplicate agent, or add a domain-qualifier)"
        elif len(members) > 1:
            mark = "   (domain-disambiguated)"
        else:
            mark = ""
        out.write(f"  role '{role}': {', '.join(names)}{mark}\n")
    suffixed = sorted({a["name"] for a in agents if a["name"].endswith("-agent")})
    if suffixed:
        out.write(f"  [smell] redundant '-agent' suffix (every agent is an agent): {suffixed}\n")
    # domain-prefix families → surfaces a grammar split (product-prefixed vs bare function-role)
    doms = {}
    for a in agents:
        doms.setdefault(a["domain"], []).append(a["name"])
    multi = {d: ns for d, ns in doms.items() if len(ns) > 1}
    if multi:
        out.write("  domain families (>1 member):\n")
        for d, ns in sorted(multi.items()):
            out.write(f"    {d}-*: {', '.join(sorted(ns))}\n")

    # uniqueness (flat per-scope namespace → silent drop; cross-scope → shadowing)
    lower = {}
    for a in agents:
        lower.setdefault(a["name"].lower(), []).append(a["file"])
    dupes = {k: v for k, v in lower.items() if len(v) > 1}
    if dupes:
        violation = True
        out.write(f"  [DUPLICATE NAME] silently dropped in the flat namespace: {dupes}\n")
    else:
        out.write("  [ok] all names unique (in THIS scope — a repo-local .claude/agents twin "
                  "would shadow a user-scope name; check both scopes)\n")
    if nonagents:
        violation = True
        out.write(f"  [NON-AGENT] files in the agents dir with no frontmatter/name: {nonagents}\n")
    else:
        out.write("  [ok] every file is a real agent\n")

    # ---- F: pairwise routing differentiation ------------------------------
    out.write("\n-- F: pairwise routing collision (each agent's own triggers vs every sibling) --\n")
    re_mod = _load_routing_eval()
    if re_mod is None:
        out.write("  [skip] routing_eval.py not resolvable from this plugin's scripts/ root "
                  "— F-differentiation not run (never a silent clean pass)\n")
    else:
        collisions = []
        for a in agents:
            a_triggers = [p for p in quoted_triggers(a["description"])
                          if len(re_mod.tokenize(p)) >= F_MIN_PHRASE_TOKENS]
            a_name_toks = set(re_mod.tokenize(a["name"]))
            for b in agents:
                if b is a:
                    continue
                bt = re_mod.description_tokens(b["description"])
                bf = re_mod.fenced_tokens(b["description"])
                if a_name_toks & bf:
                    continue  # b already fences a by name — not a collision
                for phrase in a_triggers:
                    ok, score = re_mod.routes_here(phrase, bt, F_THRESHOLD, bf)
                    if ok:
                        collisions.append((b["name"], a["name"], phrase, score))
        if not collisions:
            out.write("  [ok] no sibling's description fires on another agent's own example "
                      "trigger without a fence naming it\n")
        else:
            for bn, an, phrase, score in sorted(set(collisions)):
                out.write(f"  [REVIEW] {bn}'s description also fires ({score:.2f}) on "
                          f"{an}'s own trigger: \"{phrase}\" — no fence names {an}\n")
        out.write("  (a [review] signal, not a hard violation: a real collision needs a fence "
                  "or a scope split; a shared-domain-vocabulary proxy artifact needs neither)\n")

    # ---- S: skill-leverage graph -----------------------------------------
    out.write("\n-- S: global-skill leverage (agent -> skills: preload) --\n")
    empty = []
    for a in sorted(agents, key=lambda x: x["name"]):
        if not a["preloads"]:
            empty.append(a["name"])
            continue
        marks = []
        for s in a["preloads"]:
            marks.append(s if s in known else f"{s}❌DANGLING")
            if s not in known:
                violation = True
        out.write(f"  {a['name']:<26} -> {', '.join(marks)}\n")
    out.write(f"  [no preload] {empty or 'none'}  (candidate under-leverage — a [review] call)\n")

    out.write(f"\n-- {'VIOLATIONS PRESENT (non-agent / duplicate / dangling)' if violation else 'no hard violations'} --\n")
    out.write("   (flagged-collision intent, F-differentiation, grammar-split, and under-leverage "
              "judgment are [review] — this is the graph.)\n")
    return 1 if violation else 0


# --- selftest --------------------------------------------------------------------------------
_AGENT_TPL = """---
name: {name}
description: >-
  {description}
{skills_line}---

Fixture body.
"""


def _write_agent(root, relpath, name, skills=None, description="fixture agent", block_style=False):
    p = root / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    if not skills:
        skills_line = ""
    elif block_style:
        skills_line = "skills:\n" + "".join(f"  - {s}\n" for s in skills)
    else:
        skills_line = f"skills: [{', '.join(skills)}]\n"
    p.write_text(_AGENT_TPL.format(name=name, description=description, skills_line=skills_line),
                 encoding="utf-8")


def _run_fixture(build, skills=()):
    """Build a fixture agents dir + skills root, run the index, return (exit code, output)."""
    with tempfile.TemporaryDirectory() as td:
        agents_dir = Path(td) / "agents"
        agents_dir.mkdir()
        skills_root = Path(td) / "skills"
        skills_root.mkdir()
        for s in skills:
            (skills_root / s).mkdir()
        build(agents_dir)
        out = io.StringIO()
        code = run_index(agents_dir, [skills_root], out)
        return code, out.getvalue()


def selftest():
    errs = []

    # negative control 1: duplicate agent name (two FILES, same name) must bite
    def dup(d):
        _write_agent(d, "reviewer/foo-reviewer.md", "foo-reviewer")
        _write_agent(d, "misc/foo-reviewer-copy.md", "foo-reviewer")
    code, out = _run_fixture(dup)
    if code != 1 or "[DUPLICATE NAME]" not in out:
        errs.append("duplicate agent name must exit 1 with [DUPLICATE NAME], got %d:\n%s" % (code, out))
    if "ROLE COLLISION" not in out:  # same role, same domain twice = arithmetic collision too
        errs.append("duplicate name (repeated domain) must also flag ROLE COLLISION:\n%s" % out)

    # negative control 2: dangling `skills:` preload must bite
    def dangling(d):
        _write_agent(d, "a-reviewer.md", "a-reviewer", skills=["ghost-skill"])
    code, out = _run_fixture(dangling, skills=["real-skill"])
    if code != 1 or "ghost-skill❌DANGLING" not in out:
        errs.append("dangling preload must exit 1 with ❌DANGLING, got %d:\n%s" % (code, out))

    # positive control: block-style `skills:\n  - a\n  - b` must resolve BOTH entries against
    # real skills, not corrupt to a single dash-prefixed dangling entry (the exact bug the greedy
    # same-line regex in an earlier version of this parser had — forge's own agents, including
    # its pre-existing skill-auditor, use this YAML shape, not the inline `[a, b]` form)
    def block_style(d):
        _write_agent(d, "a-reviewer.md", "a-reviewer", skills=["real-skill", "real-skill-two"],
                     block_style=True)
    code, out = _run_fixture(block_style, skills=["real-skill", "real-skill-two"])
    if code != 0 or "DANGLING" in out or "real-skill-two" not in out:
        errs.append("block-style `skills:` list must resolve every entry, none dangling, "
                    "got %d:\n%s" % (code, out))

    # negative control 3: a non-agent file in the dir must bite
    def nonagent(d):
        _write_agent(d, "a-reviewer.md", "a-reviewer")
        (d / "notes.md").write_text("just some notes, no frontmatter\n", encoding="utf-8")
    code, out = _run_fixture(nonagent)
    if code != 1 or "[NON-AGENT]" not in out:
        errs.append("non-agent file must exit 1 with [NON-AGENT], got %d:\n%s" % (code, out))

    # collision arithmetic: all-distinct domains are domain-disambiguated, NOT a collision
    def disamb(d):
        _write_agent(d, "layout-reviewer.md", "layout-reviewer")
        _write_agent(d, "flow-reviewer.md", "flow-reviewer")
    code, out = _run_fixture(disamb)
    if code != 0 or "ROLE COLLISION" in out or "(domain-disambiguated)" not in out:
        errs.append("distinct-domain role family must pass with (domain-disambiguated), "
                    "no ROLE COLLISION, got %d:\n%s" % (code, out))

    # collision arithmetic: a bare role name (no domain qualifier) in a family MUST flag
    def bare(d):
        _write_agent(d, "reviewer.md", "reviewer")
        _write_agent(d, "code-reviewer.md", "code-reviewer")
    code, out = _run_fixture(bare)
    if "ROLE COLLISION" not in out:
        errs.append("bare role name beside a qualified twin must flag ROLE COLLISION:\n%s" % out)

    # F-differentiation: routing_eval must be resolvable in this test environment, or the whole
    # F leg is meaningfully untestable here — skip with a clear note rather than silently passing.
    re_mod = _load_routing_eval()
    if re_mod is None:
        errs.append("F-differentiation: routing_eval.py not resolvable — cannot verify the "
                    "collision-detection controls in this environment")
    else:
        # negative control: an unfenced sibling whose description overlaps another agent's own
        # quoted trigger must be flagged as a collision.
        def collide(d):
            _write_agent(d, "alpha-reviewer.md", "alpha-reviewer",
                         description='Reviews alpha widgets. Use when asked to '
                                     '"review this alpha widget for defects".')
            _write_agent(d, "beta-reviewer.md", "beta-reviewer",
                         description="Reviews widgets for defects across the board, "
                                     "alpha or otherwise.")
        code, out = _run_fixture(collide)
        if "[REVIEW]" not in out or "beta-reviewer" not in out or "alpha-reviewer" not in out:
            errs.append("F: an unfenced sibling overlapping another agent's own trigger must be "
                        "flagged [REVIEW], got:\n%s" % out)
        if code != 0:
            errs.append("F: a [review]-tier collision must NOT set exit 1 (it's not a hard "
                        "violation), got %d" % code)

        # reverse control: the SAME pair, but beta's description now truthfully fences alpha by
        # name — the collision must be suppressed (a real fence repels, per routing_eval's own
        # doctrine; this tool must respect that, not re-flag what the fence already resolved).
        def fenced(d):
            _write_agent(d, "alpha-reviewer.md", "alpha-reviewer",
                         description='Reviews alpha widgets. Use when asked to '
                                     '"review this alpha widget for defects".')
            _write_agent(d, "beta-reviewer.md", "beta-reviewer",
                         description="Reviews widgets for defects across the board. "
                                     "NOT for alpha widgets specifically (alpha-reviewer).")
        code2, out2 = _run_fixture(fenced)
        if "[REVIEW]" in out2 and "alpha-reviewer" in out2.split("-- F:")[1].split("-- S:")[0]:
            errs.append("F: a truthful fence naming the sibling must suppress the collision "
                        "flag, got:\n%s" % out2)

    # reverse control: the CURRENT real estate passes clean (skipped if not present)
    real = Path(__file__).resolve().parents[3] / "agents"
    real_skills = Path(__file__).resolve().parents[3] / "skills"
    if real.is_dir():
        out = io.StringIO()
        code = run_index(real, [real_skills], out)
        if code != 0:
            errs.append("reverse control: real estate %s must pass clean, got %d:\n%s"
                        % (real, code, out.getvalue()))
        if "ROLE COLLISION" in out.getvalue():
            errs.append("reverse control: real estate's domain-disambiguated roles must not "
                        "flag ROLE COLLISION:\n%s" % out.getvalue())
        reverse_note = f"reverse control ran against {real}"
    else:
        reverse_note = "reverse control SKIPPED (no real agents dir at %s)" % real

    if errs:
        sys.stderr.write("agent_corpus_index: FAIL (%d)\n" % len(errs))
        for e in errs:
            sys.stderr.write("  - %s\n" % e)
        return 1
    print("agent_corpus_index: OK — duplicate-name / dangling-preload / non-agent controls bite; "
          "collision arithmetic (distinct domains suppressed, bare/repeated flagged) verified; "
          "F-differentiation (unfenced sibling collision fires, truthfully fenced pair suppressed) "
          "verified; " + reverse_note)
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "selftest":
        return selftest()
    if len(argv) < 2:
        print("usage: agent_corpus_index.py <agents_dir> [skills_root ...] | selftest")
        return 2
    agents_dir = Path(argv[1])
    if not agents_dir.is_dir():
        print(f"no such dir: {agents_dir}")
        return 2
    roots = [Path(a) for a in argv[2:]] or [agents_dir.parent / "skills"]
    return run_index(agents_dir, roots, sys.stdout)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
