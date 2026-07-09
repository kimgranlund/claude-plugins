#!/usr/bin/env python3
"""corpus_index.py — the deterministic Phase-0 index for a skills corpus audit.

Reads every `<dir>/SKILL.md` under a skills root and emits the mechanical facts the
two *corpus-level* audit dimensions lean on — the ones no single-skill review can see:

  N (naming strategy)  → leading-token grammar histogram, family grouping,
                         within-family second-token grammar consistency, reserved-command shadowing.
  P (peer leverage)    → the [[wikilink]] + `skills:` composition graph: edges, isolated
                         nodes, one-way edges, dangling targets (a [[link]] or `skills:`
                         preload naming no skill).

It reports facts and unambiguous violations (shadowing, dangling links/preloads). Whether
"two grammars" or "a one-way edge" is a DEFECT is a [review] call — the scorer judges; this
tool only lays the graph and the histogram on the table.

Usage:  python corpus_index.py [skills_root]     # default: the script's own ../.. (the skills/ dir)
        python corpus_index.py selftest          # fixture-locked proof of the corpus gates
Exit 0 = no hard violation (no shadow, no dangling link/preload).  Exit 1 = at least one.

Selftest: drives the SAME main() over fixture corpora in a temp dir (harness_checks.py's
selftest discipline). Negative controls that must BITE: a planted reserved-name shadow, a
dangling [[wikilink]] target, a dangling `skills:` preload, and a diverged RESERVED twin.
Reverse control: a clean two-skill corpus with a healthy maker→critic edge passes with zero
findings.
"""
import re
import sys
from pathlib import Path

# Bundled command tokens a skill directory must not silently shadow (a shadow is a hard
# violation). The CANON is harness_checks.RESERVED_SKILLS (forge's scripts/) — parsed at
# runtime by _harness_reserved(); this literal survives ONLY as the offline fallback, and the
# fact×fact twin gate in _twin_gate() fails loudly (exit 2) the moment the two sets diverge,
# at normal runtime and in the selftest alike.
RESERVED = {"code-review", "debug", "run", "verify", "loop", "batch",
            "claude-api", "run-skill-generator"}

_RESERVED_SET_RE = re.compile(r"RESERVED_SKILLS\s*=\s*\{([^}]*)\}", re.S)


def _harness_reserved():
    """RESERVED_SKILLS parsed from the canonical harness_checks.py, or None if unreachable.
    __file__ is resolved first, so invocation through a symlinked sibling scripts/ dir still
    lands on the real tree. forge keeps harness_checks.py at <plugin-root>/scripts/, a sibling
    of skill_lint.py/release_gate.py — walk upward from this file looking for that, rather than
    assume a fixed depth or a per-skill "skill-author" directory that doesn't exist here."""
    here = Path(__file__).resolve().parent
    candidates = [here / "harness_checks.py"] + [p / "scripts" / "harness_checks.py" for p in here.parents]
    for cand in candidates:
        try:
            m = _RESERVED_SET_RE.search(cand.read_text(encoding="utf-8"))
        except OSError:
            continue
        if m:
            return set(re.findall(r"['\"]([^'\"]+)['\"]", m.group(1)))
    return None


def _twin_gate(canon, local):
    """fact×fact consistency gate: the harness canon and the local fallback must agree.
    canon None (harness unreachable) → run on the fallback; divergence → fail loudly."""
    if canon is None:
        return local
    if canon != local:
        print("corpus_index: RESERVED twin diverged from harness_checks.RESERVED_SKILLS — "
              f"only-here={sorted(local - canon)}, only-harness={sorted(canon - local)}; "
              "update RESERVED in corpus_index.py to match the canon.", file=sys.stderr)
        raise SystemExit(2)
    return canon


def reserved_set():
    """The operative reserved set, twin-gated against the canon on every run."""
    return _twin_gate(_harness_reserved(), RESERVED)

LINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
# `skills:` preload — a YAML list, inline `[a, b]` or block `- a`. We only need presence + members.
# [ \t]* not \s*: with re.M a greedy \s* eats the newline and swallows a block list's first item
# as the "inline" value (bug caught by the selftest's dangling-preload control).
SKILLS_KEY = re.compile(r"^skills:[ \t]*(.*)$", re.M)


def read_frontmatter_and_body(text):
    """Split leading `--- … ---` frontmatter from the body. Returns (fm, body)."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def first_description(fm):
    """The description field's text, flattened — the routing interface. ~200 char lead."""
    m = re.search(r"^description:\s*(.*)$", fm, re.M)
    if not m:
        return ""
    # capture the block scalar / folded lines that follow the key
    lines = fm[m.start():].splitlines()
    out = [re.sub(r"^description:\s*[>|]?-?\s*", "", lines[0])]
    for ln in lines[1:]:
        if re.match(r"^\S", ln):            # next top-level key ends the value
            break
        out.append(ln.strip())
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def preloads(fm):
    m = SKILLS_KEY.search(fm)
    if not m:
        return []
    inline = m.group(1).strip()
    if inline.startswith("["):
        return [s.strip() for s in inline.strip("[]").split(",") if s.strip()]
    # block list on following lines
    out = []
    for ln in fm[m.end():].splitlines():
        b = ln.strip()
        if b.startswith("- "):
            out.append(b[2:].strip())
        elif re.match(r"^\S", ln):
            break
    return out


def grammar_of(token):
    """Classify a single hyphen-token: gerund (…ing) vs plain noun."""
    return "gerund" if token.endswith("ing") else "noun"


def load(root):
    skills = {}
    for skill_md in sorted(root.glob("*/SKILL.md")):
        d = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm, body = read_frontmatter_and_body(text)
        nm = NAME.search(fm)
        skills[d] = {
            "dir": d,
            "name": nm.group(1).strip() if nm else None,
            "desc": first_description(fm),
            "links": sorted(set(LINK.findall(body)) | set(LINK.findall(fm))),
            "preloads": preloads(fm),
            "lead": d.split("-")[0],
            "tail": d.split("-")[-1],
            "body": body,
        }
    return skills


# --- selftest ------------------------------------------------------------------------------------
# Fixture-locked proof of the corpus gates (harness_checks.py's selftest discipline): it drives
# the SAME main() the CLI uses over fixture corpora written to a temp dir, plus the twin gate's
# own controls. Purely ADDITIVE — the normal-run surface is untouched.

# Negative control: the directory name shadows a reserved bundled command ([SHADOW] must bite).
_FIX_BAD_SHADOW = """---
name: verify
description: Fixture that shadows a reserved bundled command for the selftest.
---
# Shadow fixture
Hand the result to the reviewer.
"""

# Negative control: both composition surfaces dangle — a [[wikilink]] to no skill and a
# `skills:` preload naming no skill ([DANGLING] must bite on each target).
_FIX_BAD_LINKER = """---
name: fixture-author
description: Fixture whose wikilink and preload both dangle for the selftest.
skills:
  - missing-preload
---
# Linker fixture
Route depth to [[ghost-skill]]; hand the result to the reviewer.
"""

# Reverse control: a clean two-skill corpus — one grammar, one family, a healthy maker→critic
# edge wired BOTH ways, the maker naming its critic route — must pass with zero findings.
_FIX_OK_AUTHOR = """---
name: demo-author
description: Fixture maker for the selftest reverse control.
---
# Demo author
Draft the artifact, then hand it to the reviewer seat via [[demo-verify]].
"""

_FIX_OK_VERIFY = """---
name: demo-verify
description: Fixture critic for the selftest reverse control.
---
# Demo verify
Grade the draft from [[demo-author]] and return a gap-map.
"""


def _run_fixture_corpus(fixtures):
    """Write {dirname: SKILL.md text} as a corpus in a temp dir, run the SAME main() on it,
    and return (exit_code, stdout)."""
    import contextlib
    import io
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for d, text in fixtures.items():
            (root / d).mkdir()
            (root / d / "SKILL.md").write_text(text, encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(["corpus_index.py", str(root)])
    return code, buf.getvalue()


def selftest():
    import contextlib
    import io
    errs = []

    # 1. negative controls — shadow, dangling [[wikilink]], dangling `skills:` preload all BITE
    code, out = _run_fixture_corpus({"verify": _FIX_BAD_SHADOW, "fixture-author": _FIX_BAD_LINKER})
    if code != 1:
        errs.append("violations corpus: expected exit 1, got %s" % code)
    if "[SHADOW]" not in out or "'verify'" not in out.replace('"', "'"):
        errs.append("shadow control: planted reserved-name shadow 'verify' not flagged")
    if "[DANGLING]" not in out:
        errs.append("dangling control: no [DANGLING] section emitted")
    if "ghost-skill" not in out:
        errs.append("dangling control: [[ghost-skill]] wikilink target not flagged")
    if "missing-preload" not in out:
        errs.append("dangling control: `skills:` preload 'missing-preload' not flagged")

    # 2. reverse control — a clean two-skill corpus with a healthy maker→critic edge:
    #    zero findings (no shadow/dangling/advisory/mixed-grammar/inconsistent-family), exit 0
    code, out = _run_fixture_corpus({"demo-author": _FIX_OK_AUTHOR, "demo-verify": _FIX_OK_VERIFY})
    if code != 0:
        errs.append("clean corpus: expected exit 0, got %s" % code)
    for token in ("[SHADOW]", "[DANGLING]", "[advisory]", "[mixed]", "INCONSISTENT"):
        if token in out:
            errs.append("clean corpus: unexpected finding %s" % token)
    if "no hard violations" not in out:
        errs.append("clean corpus: verdict line missing 'no hard violations'")

    # 3. twin gate — the harness canon must be reachable, and today's sets must agree
    canon = _harness_reserved()
    if canon is None:
        errs.append("twin gate: canonical harness_checks.RESERVED_SKILLS unreachable/unparsable")
    if reserved_set() != RESERVED:
        errs.append("twin gate: reserved_set() does not match the local RESERVED fallback")

    # 4. twin gate divergence must fail loudly (exit 2), and the None-canon fallback must hold
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            _twin_gate({"only-in-harness"}, RESERVED)
        errs.append("twin gate: diverged sets did not fail loudly")
    except SystemExit as e:
        if e.code != 2:
            errs.append("twin gate: divergence exited %s, expected 2" % e.code)
    if _twin_gate(None, RESERVED) != RESERVED:
        errs.append("twin gate: None-canon fallback did not return the local set")

    return errs


def selftest_main():
    errs = selftest()
    if errs:
        print("corpus_index selftest: FAIL (%d)" % len(errs))
        for e in errs:
            print("  - %s" % e)
        return 1
    print("corpus_index selftest: OK — reserved-name shadow, dangling [[wikilink]], and dangling "
          "`skills:` preload controls bite; the clean maker→critic corpus passes with zero "
          "findings; the RESERVED twin gate reads the harness canon, agrees today, fails loudly "
          "(exit 2) on divergence, and falls back cleanly when the canon is unreachable")
    return 0


def main(argv):
    if len(argv) > 1 and argv[1] == "selftest":
        return selftest_main()
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[2]
    if not root.is_dir():
        print(f"no such dir: {root}")
        return 2
    skills = load(root)
    if not skills:
        print(f"no */SKILL.md under {root}")
        return 2
    names = set(skills)
    violation = False

    print(f"== corpus index: {len(skills)} skills under {root} ==\n")

    # ---- N: naming ----------------------------------------------------------
    print("-- N: naming grammar --")
    lead_gram = {}
    for d in sorted(skills):
        g = grammar_of(skills[d]["lead"])
        lead_gram.setdefault(g, []).append(d)
    for g, ds in sorted(lead_gram.items()):
        print(f"  leading-token {g}: {len(ds)}")
    if len(lead_gram) > 1:
        print(f"  [mixed] {len(lead_gram)} leading-token grammars coexist "
              f"(gerund-activity vs noun-phrase) — a [review] coherence call")

    fams = {}
    for d in skills:
        fams.setdefault(skills[d]["lead"], []).append(d)
    print("  families (by leading token):")
    for lead, members in sorted(fams.items()):
        if len(members) > 1:
            tails = {grammar_of(skills[m]["tail"]) for m in members}
            flag = "  <-- INCONSISTENT second-token grammar" if len(tails) > 1 else ""
            print(f"    {lead}-* ({len(members)}): {', '.join(sorted(members))}{flag}")

    shadows = sorted(names & reserved_set())
    if shadows:
        violation = True
        print(f"  [SHADOW] directories shadow a reserved command: {shadows}")
    else:
        print("  [ok] no reserved-command shadowing")

    # ---- P: peer graph ------------------------------------------------------
    print("\n-- P: peer-leverage graph --")
    out_edges = {d: set(skills[d]["links"]) for d in skills}
    in_edges = {d: set() for d in skills}
    dangling = {}
    for d, outs in out_edges.items():
        for t in outs:
            if t in in_edges:
                in_edges[t].add(d)
            else:
                dangling.setdefault(d, []).append(t)
    # a `skills:` preload naming no skill dangles just like a wikilink (preloads stay out of
    # the edge counts — static wiring is not a prose edge; only the dangle is a violation)
    for d in sorted(skills):
        for t in skills[d]["preloads"]:
            if t not in names:
                dangling.setdefault(d, []).append(t)

    linked = {d for d in skills if out_edges[d] or in_edges[d]}
    isolated = sorted(set(skills) - linked)
    print(f"  edges: {sum(len(v) for v in out_edges.values())}   "
          f"participating: {len(linked)}/{len(skills)}")
    print(f"  [preloads] skills using `skills:` static wiring: "
          f"{[d for d in skills if skills[d]['preloads']] or 'NONE'}")
    print(f"  isolated (no in/out [[link]]): {isolated or 'none'}")

    print("  one-way edges (A->B, no B->A):")
    ow = [(a, b) for a in sorted(out_edges) for b in sorted(out_edges[a])
          if b in names and a not in out_edges[b]]
    for a, b in ow:
        print(f"    {a} -> {b}")
    if not ow:
        print("    none")

    if dangling:
        violation = True
        print("  [DANGLING] links to a non-existent skill:")
        for d, ts in sorted(dangling.items()):
            print(f"    {d} -> {ts}")
    else:
        print("  [ok] no dangling [[link]] targets")

    # -- B: bi-directionality (advisory) -----------------------------------
    import re as _re
    VERBS = {"author","review","audit","score","evaluate","design","decompose","extract","compose",
             "build","orient","init","seed","run","advance","distill","edit","verify","refactor","grill"}
    CRITIC = _re.compile(r"reviewer|generator ≠ critic|generator≠critic|\[\[ui-audit\]\]|\[\[color-verify\]\]|round-trip|fresh-context", _re.I)
    print("\n-- B: bi-directionality (advisory — create↔evaluate wiring) --")
    findings = []
    for d, s in sorted(skills.items()):
        tail, body_ = s["tail"], s.get("body", "")
        is_transform = "-to-" in d
        if tail in {"author", "design", "compose"} and not CRITIC.search(body_):
            findings.append(f"{d}: maker names no critic route (reviewer / gen≠crit / verify pair)")
        if tail not in VERBS and not is_transform and "knowledge-forge" not in body_:
            findings.append(f"{d}: knowledge pack names no factory route ([[knowledge-forge]])")
    for f_ in findings:
        print(f"  [advisory] {f_}")
    if not findings:
        print("  [ok] every maker names a critic route; every pack names its factory")

    print(f"\n-- {'VIOLATIONS PRESENT (shadow/dangling)' if violation else 'no hard violations'} --")
    print("   (grammar coherence & missing-edge judgment are [review] — this is the graph, not the verdict.)")
    return 1 if violation else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
