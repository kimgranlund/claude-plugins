#!/usr/bin/env python3
"""release_gate — the plugin release ritual as code.

Usage:
  release_gate.py <plugin-root> [--package]   run the gate; --package also writes
                                              dist/<name>-<version>.plugin on a clean gate
  release_gate.py selftest                    prove the checks on a temp fixture plugin

Gate order (plugin-writing-rules §Release discipline):
  G1 manifest: .claude-plugin/plugin.json valid, kebab name, semver version
  G2 structure: only the manifest in .claude-plugin/; every skills/* dir has SKILL.md;
     skill subfolders outside {evals,references,scripts,assets} -> WARN (ruled 2026-07-15)
  G3 full lint: every SKILL.md, agents/*.md, hooks.json, plugin.json via skill_lint (FAIL fails)
  G4 bundled selftests: every scripts/*.py|*.mjs|*.js exposing a selftest mode must exit 0
     (py via this interpreter, js via node; js with node absent -> WARN, unproven;
      exit 2 = SKIP, runtime dependency absent -> disclosed in the ok line, not failed)
  G5 phantom sweep: [[handle]] refs in live .md (CHANGELOG excluded) — WARN, counted
  G6 package (--package): dist/<name>-<version>.plugin, excluding dist/, .claude/, and the
     repo's root CLAUDE.md (dev harness != distribution); a same-version artifact FAILS
     (the version is the update cache key — same version means nobody receives the ship)
  G7 evals: every suite passes eval_check; model-invocable skills without a suite WARN
  G10 docs: README/MANUAL cover every skill, README ledger version matches the manifest,
      CLAUDE.md counts reconcile (composes docs_check.py; accuracy stays human)
  G9 packs: every skill with references/INDEX.md passes corpus_check (K1 FAILs fail the gate)
  G8 sibling names: kebab tokens in SKILL.md files that carry one of this plugin's own
     name-suffixes but match no installed skill -> WARN (rename drift, phantom prose siblings)
  G11 style lint (ADR-0002): ruff over .py / eslint over .mjs|.js, workspace-root configs;
      run when a runner is reachable, WARN when not (CI enforces); no config -> not applicable

Exit 0 clean (warnings allowed), 1 on any FAIL.
"""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_lint  # the check tier composes; it is not restated
import eval_check
import corpus_check
import docs_check

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PHANTOM_RE = re.compile(r"\[\[[a-z0-9-]+\]\]")


def gate(root: Path, package: bool = False):
    fails, warns, lines = [], [], []
    ok = lambda m: lines.append(f"  ok    {m}")
    def fail(code, m):
        fails.append(code); lines.append(f"  FAIL  {code}  {m}")
    def warn(code, m):
        warns.append(code); lines.append(f"  warn  {code}  {m}")

    # G1 manifest
    mf = root / ".claude-plugin" / "plugin.json"
    name = version = None
    if not mf.is_file():
        fail("G1", f"missing {mf} -> the manifest is the plugin")
    else:
        try:
            m = json.loads(mf.read_text())
            name, version = m.get("name", ""), m.get("version", "")
            if not KEBAB_RE.match(name or ""):
                fail("G1", f"name `{name}` -> kebab-case required")
            if not SEMVER_RE.match(version or ""):
                fail("G1", f"version `{version}` -> semver required; the version is the update cache key")
            if not fails:
                ok(f"manifest {name} v{version}")
        except (json.JSONDecodeError, ValueError) as e:
            fail("G1", f"plugin.json invalid JSON ({e})")

    # G2 structure
    cp = root / ".claude-plugin"
    if cp.is_dir():
        strays = [p.name for p in cp.iterdir() if p.name not in ("plugin.json",)]
        if strays:
            fail("G2", f"components inside .claude-plugin/ ({strays[:3]}) -> only the manifest lives there")
    skills_dir = root / "skills"
    SANCTIONED_SUBDIRS = {"evals", "references", "scripts", "assets"}  # ruled 2026-07-15
    rogue_dirs = []
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and not (d / "SKILL.md").is_file():
                fail("G2", f"skills/{d.name}/ has no SKILL.md")
            if d.is_dir():
                rogue_dirs += [f"{d.name}/{s.name}" for s in sorted(d.iterdir())
                               if s.is_dir() and s.name not in SANCTIONED_SUBDIRS]
    if rogue_dirs:
        warn("G2", f"{len(rogue_dirs)} skill subfolder(s) outside the sanctioned set "
                   f"(evals/references/scripts/assets): {', '.join(rogue_dirs[:4])} "
                   "-> topical data dirs live under assets/<topic>/ (ruled 2026-07-15)")
    # Broken symlinks FAIL: a rename sweep cannot see a symlink's target text, so a renamed
    # target dir silently strands the link — locally masked by macOS glob behavior, then a
    # FileNotFoundError crash on the Linux CI runner (bitten 2026-07-21, ADR-0006 harness merge:
    # make-llms-txt's best-practices.md pointed at the renamed reference-forge/).
    broken_links = [str(p.relative_to(root)) for p in root.rglob("*")
                    if p.is_symlink() and not p.resolve().exists()]
    if broken_links:
        fail("G2", f"{len(broken_links)} broken symlink(s): {', '.join(broken_links[:3])} "
                   "-> repoint the target; symlink targets are invisible to rename sweeps")
    if "G2" not in fails:
        ok("structure: manifest isolated; every skill dir carries SKILL.md"
           + ("" if rogue_dirs else "; subfolders conform") + "; no broken symlinks")

    # G3 full lint via skill_lint
    targets = (sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md"))
               + sorted(root.glob("hooks/hooks.json")) + ([mf] if mf.is_file() else []))
    lint_failed = []
    for t in targets:
        _, failed = skill_lint.lint_path(str(t))
        if failed:
            lint_failed.append(str(t.relative_to(root)))
    if lint_failed:
        fail("G3", f"skill_lint FAIL in: {', '.join(lint_failed)} -> run skill_lint.py on each for the repair list")
    else:
        ok(f"lint clean across {len(targets)} files")

    # G4 bundled selftests — py via the running interpreter, js/mjs via node (parity, 2026-07-14:
    # the original .py-only rglob left every .mjs selftest in the estate unrun at the gate)
    import shutil
    node = shutil.which("node")
    scripts = sorted(p for pat in ("scripts/*.py", "scripts/*.mjs", "scripts/*.js")
                     for p in root.rglob(pat) if "dist" not in p.parts)
    tested, js_skipped, dep_skipped = 0, 0, []
    for s in scripts:
        if "selftest" not in s.read_text(encoding="utf-8", errors="replace"):
            continue
        if s.resolve() == Path(__file__).resolve():
            continue  # the gate proves itself via its own selftest mode, not recursively
        if s.suffix == ".py":
            runner = [sys.executable]
        elif node:
            runner = [node]
        else:
            js_skipped += 1
            continue
        r = subprocess.run([*runner, str(s), "selftest"], capture_output=True, text=True, timeout=120)
        if r.returncode == 2:
            # ratified tri-state (2026-07-14, pioneered by ui-probe.mjs): exit 2 = SKIP,
            # the selftest cannot prove itself here (runtime dependency absent) — disclosed, not failed
            dep_skipped.append(s.name)
            continue
        tested += 1
        if r.returncode != 0:
            fail("G4", f"{s.relative_to(root)} selftest exit {r.returncode} -> a shipped script proves its counters or does not ship")
    if js_skipped:
        warn("G4", f"{js_skipped} js script(s) expose a selftest but node is not on PATH -> unproven, install node to run them")
    if "G4" not in fails:
        skipnote = f"; {len(dep_skipped)} skipped, dependency absent: {', '.join(dep_skipped)}" if dep_skipped else ""
        ok(f"bundled selftests green ({tested} scripts{skipnote})")

    # G5 phantom sweep — backticked/fenced [[handles]] are mentions, not routing.
    # Sibling-aware (2026-07-09, same rule as G8): a [[handle]] naming a real skill anywhere
    # in the workspace is the ported corpus's link STYLE, not rot — only handles resolving
    # to nothing warn. Style-only handles are reported as an ok-line count.
    g5_inventory = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    for sib in root.parent.glob("*/.claude-plugin/plugin.json"):
        g5_inventory |= {p.parent.name for p in sib.parent.parent.glob("skills/*/SKILL.md")}
    phantom_hits, style_refs = [], 0
    inline_code = re.compile(r"`[^`]*`")
    handle_re = re.compile(r"\[\[([a-z0-9-]+)\]\]")
    for md in root.rglob("*.md"):
        if "CHANGELOG" in md.name or "dist" in md.parts:
            continue
        if md.is_symlink() and not md.resolve().exists():
            continue  # broken symlink — already FAILED at G2; reading it would crash the sweep
        fenced = False
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for h in handle_re.findall(inline_code.sub("", line)):
                if h in g5_inventory:
                    style_refs += 1
                else:
                    phantom_hits.append(f"{md.relative_to(root)}:{i} [[{h}]]")
    if phantom_hits:
        warn("G5", f"{len(phantom_hits)} dangling [[handle]] refs ({phantom_hits[:3]}...) -> they resolve to no skill anywhere in the workspace; repoint or cut")
    elif style_refs:
        ok(f"no dangling [[handles]] ({style_refs} style refs resolve to workspace skills)")
    else:
        ok("no phantom [[handles]] in live markdown")

    # G7 evals — schema FAILs, coverage gaps WARN
    suite_fail, suites = [], sorted(root.glob("skills/*/evals/evals.json"))
    for s in suites:
        fs = eval_check.check_suite_text(s.read_text(encoding="utf-8", errors="replace"), s.parent.parent.name)
        if any(f[0] == "FAIL" for f in fs):
            suite_fail.append(str(s.relative_to(root)))
    if suite_fail:
        fail("G7", f"eval_check FAIL in: {', '.join(suite_fail)} -> run eval_check.py on each")
    gaps = eval_check.check_coverage(root)
    if gaps:
        warn("G7", f"{len(gaps)} model-invocable skills without eval suites -> descriptions untuned: "
                   + ", ".join(g[2].split(':')[0] for g in gaps))
    if not suite_fail:
        ok(f"evals: {len(suites)} suites valid" + ("" if gaps else "; coverage complete"))

    # G9 corpus reconciliation for knowledge packs
    pack_fail, packs_seen = [], 0
    for sk in sorted(root.glob("skills/*")):
        fs = corpus_check.check_pack(sk) if sk.is_dir() else None
        if fs is None:
            continue
        packs_seen += 1
        if any(f[0] == "FAIL" for f in fs):
            pack_fail.append(sk.name)
    if pack_fail:
        fail("G9", f"corpus_check FAIL in: {', '.join(pack_fail)} -> run corpus_check.py on each")
    else:
        ok(f"packs reconciled ({packs_seen} with INDEX)")

    # G10 docs freshness
    dfs = docs_check.check(root)
    d_fail = [f for f in dfs if f[0] == "FAIL"]
    if d_fail:
        fail("G10", f"{len(d_fail)} docs finding(s): " + "; ".join(f[2] for f in d_fail[:3]) + " -> run docs_check.py")
    else:
        for f in dfs:
            warn("G10", f[2])
        if not dfs:
            ok("docs cover every artifact; ledger matches manifest")

    # G8 stale sibling names — deliberately does NOT strip code spans: a backticked
    # stale name is still rot on a routing-bearing surface (contrast G5's mention rule).
    # Sibling-aware (2026-07-09): cross-plugin soft mentions are doctrine-legal, so tokens
    # resolve against every workspace sibling's skills too before warning — only TRUE
    # phantoms (matching no skill anywhere in the workspace) remain findings.
    inventory = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    for sib in root.parent.glob("*/.claude-plugin/plugin.json"):
        inventory |= {p.parent.name for p in sib.parent.parent.glob("skills/*/SKILL.md")}
    suffixes = {n.rsplit("-", 1)[-1] for n in inventory}
    # verified prose-compound false positives (hyphenated phrases sharing a real suffix)
    allow = {"nested-intake",  # the [nested-intake] seed-marker literal (docs/teamwork protocol), suffix went live with lead-intake
             "per-ticket", "feature-ticket",  # prose compounds sharing dispatch-ticket's suffix (ADR-0010)
             # dispatch-feature: ADR-0010's retired name, kept only in dated rename annotations —
             # fix_old_names.py's manifest (L1) still catches any LIVE typed-slot use of it
             "dispatch-feature",
             "re-run", "dry-run", "no-split", "keep-separate", "cross-cite",
             "deep-review", "data-not-markup", "color-accessibility", "geometry-not-perception",
             "from-color-perception-facts", "from-color-space-facts", "neutral-by-design",
             "orphaned-tokens", "over-tokens", "prose-over-tokens", "ultimate-tokens",
             "change-verify", "composition-patterns", "macro-patterns", "micro-patterns",
             "state-patterns", "live-agent", "routing-corpus", "training-corpus",
             "catalog-design", "conversational-agent",
             # widened by sibling-aware suffixes (2026-07-09) — verified prose, not names:
             "agent-vs-agent", "fork-vs-agent", "per-agent", "sub-agent", "single-agent",
             "non-agent", "multi-agent", "whole-corpus", "thin-corpus", "source-corpus",
             "skill-corpus", "knowledge-corpus", "rubric-agent-corpus", "rubric-skill-corpus",
             "anti-patterns", "component-patterns", "contrast-standards", "audit-report",
             "lossy-by-design", "first-run", "material-design", "color-tokens",
             "figma-make", "google-stitch",
             # figma-plugin-facts joining the estate added the -api suffix (2026-07-09):
             "attributes-as-api",
             # the mechanization pair (2026-07-14): "hand-run" is prose ("a hand-run check",
             # -run suffix from check-routing); "selftest-patterns" is a references file:
             "hand-run", "selftest-patterns",
             # the #78 ship-leg capture (2026-07-21): "parallel-session pulls" is prose in
             # big-change-git-rules' re-budgeted description; "writing-rules" is the
             # *-writing-rules family glob (successor of the *-authoring-standards form):
             "parallel-session", "writing-rules",
             # the #79 description diet (2026-07-22): trimmed-description prose compounds:
             "pre-task", "squash-merge",
             # the four UI/design knowledge skills (2026-07-15): "container-patterns" and
             # "scale-theory" are references files (ui-pattern-facts, size-and-shape-rules); "design"
             # is the sibling PLUGIN's name, caught by size-and-shape-rules' own "-systems" suffix;
             # "box-model-and-flow" is a references file (dom-layout-facts); "mid-flow" is prose
             # ("mid-flow" in the hook skills), caught once dom-layout-facts added the -flow suffix:
             "container-patterns", "scale-theory", "design", "box-model-and-flow",
             # prose compounds newly caught by the same two suffixes (-flow, -systems):
             "mid-flow", "cross-flow", "self-orchestrated-looping-agentic-systems",
             # a2a-protocol-facts's references file (2026-07-15) — the estate's last standing G8 warn:
             "transport-and-streaming",
             # check-state joining the estate added the -state suffix (2026-07-29) — all four
             # are prose compounds, the 1.25.1 class: "work-state" (check-state's own subject),
             # "tri-state" (the exit-code doctrine), "world-state" (stopping predicates),
             # "dead-state" (thinking-depth prose):
             "work-state", "tri-state", "world-state", "dead-state",
             # same class, sibling plugins' first re-gate after check-state (2026-07-30):
             # "end-state" (loop-rules/file-bug prose), "living-state" (doc lifecycle prose):
             "end-state", "living-state",
             # entry-file-rules' mechanize-first bullet (2026-07-29): prose compound,
             # "before prose-as-skill is considered" — not a sibling name:
             "prose-as-skill",
             # verify-family judgment rule-ID slugs (2026-07-16, Issue #8) — findings
             # vocabulary, not skill names:
             "order-vs-task-flow",
             # big-change-git-rules (2026-07-17, Issue #24): "authoring-standards" is the
             # `*-authoring-standards` glob in prose; "merge-semantics" is a references file
             # (references/merge-semantics.md) — the standing references-file false-positive
             # class, same shape as container-patterns/scale-theory/box-model-and-flow:
             "authoring-standards", "merge-semantics",
             # github-facts (2026-07-17): "lifecycle-and-review" is the tail of a
             # references-file mention (`pr-lifecycle-and-review.md`) whose 2-char "pr-" prefix
             # falls below the token regex's 3-char first-segment floor, same class as
             # merge-semantics above; "sub-issue" is GitHub's own singular terminology in a
             # trigger phrase, colliding with scribe's `issue` skill's no-hyphen name (its own
             # suffix IS "issue" under rsplit) — legitimate prose, not a phantom sibling ref:
             "lifecycle-and-review",
             # sub-issue pruned 2026-07-21: the docs rename retired the `issue` skill (now
             # file-task), so GitHub's singular "sub-issue" no longer collides with any name.
             # a2a-* skill names: the token regex skips the digit-bearing "a2a-" segment and
             # "sees" the tail of legitimate full names; plus that plugin's prose compounds
             # and a references file (2026-07-09):
             "agent-design", "isolation-verify", "agent-to-agent", "inter-agent",
             "clean-run", "halt-and-report", "report-format",
             # the `llm` plugin's chat-harness-* family (2026-07-13): "chat-agent" is the
             # family's own shared framing phrase ("a chat-agent harness"), tripping the
             # `-agent` suffix a2ui-chat-agent-facts already owns; "hardcoded-feature" is
             # ordinary prose in chat-harness-routing-facts's own axis description:
             "chat-agent", "hardcoded-feature",
             # parallel-work-rules (2026-07-17): "self-report" is prose ("never act on either
             # side's self-report") tripping the `-report` suffix write-handoff already owns:
             "self-report",
             # checking-rules (2026-07-18, Issue #39) added the `-discipline` suffix to the
             # estate inventory: "self-review" is this skill's own prose ("steelman self-review"),
             # and "load-discipline" is plan-skill-split's pre-existing, unrelated prose (a
             # references/best-practices.md phrase about corpus load pressure) newly caught by
             # the same suffix — the standing false-positive class, same shape as -flow/-systems:
             "self-review", "load-discipline",
             # the 2026-08-11 check-everything sweep, four standing G8 warns triaged — all the
             # established classes: "custom-state" is the web-components CustomStateSet term of
             # art (make-component's platform-baseline row); "screen-state" is motion-rules
             # prose ("screen-state grammar"); "fill-as-state" is icon-rules' named design
             # concept (filled variant signals selection); the two long tokens are references
             # FILES (turn-session-and-input-intent.md, durable-memory-vs-ephemeral-task-state.md),
             # the merge-semantics/transport-and-streaming class:
             "custom-state", "screen-state", "fill-as-state",
             "turn-session-and-input-intent", "durable-memory-vs-ephemeral-task-state",
             # pack-writing-rules (2026-07-19): "knowledge-forge" is a deliberate historical
             # citation of a now-retired scribe skill (folded into this plugin's own make-pack),
             # not rename drift — the sentence explains provenance, it doesn't point at a live sibling:
             "knowledge-forge",
             # naming-rules (2026-07-20) added the `-rules` suffix to the estate inventory: the
             # skill's own illustrative paradigm names are deliberate examples, not phantom
             # siblings (doc-rules is its labeled counter-example; doc-writing-rules,
             # entry-file-rules, icon-rules, file-feature, sort-issues are proposed-name
             # demonstrations), and three pre-existing prose compounds are newly caught by the
             # widened inventory — path-scoped-rules (skill-writing-rules' frontmatter
             # prose), folder-taxonomy (check-all-agents prose), planner (an orchestration
             # AGENT cited in prose, not a skill) — the standing false-positive class, same
             # shape as -flow/-systems/-discipline:
             "doc-rules", "doc-writing-rules", "entry-file-rules", "icon-rules", "file-feature",
             "sort-issues", "path-scoped-rules", "folder-taxonomy", "planner",
             # same 2026-07-20 estate-wide sweep, other plugins' pre-existing prose newly caught
             # by suffixes added in recent ships (-rules here; -routing/-sweep/-orchestrator from
             # llm's chat-harness family and forge 1.39.0's ops pair): "three-hard-rules" is
             # design-md-rules's own named block, "mis-routing" is issue's prose,
             # "threshold-sweep" cites a research-methods references FILENAME
             # (threshold-sweep-2026-07-04.md), "repo-orchestrator" is a hypothetical agent in
             # parallel-work-rules's worked example:
             "three-hard-rules", "mis-routing", "threshold-sweep", "repo-orchestrator",
             # ADR-0006 color rename (2026-07-21) added the -facts/-colors/-palette suffixes to
             # the inventory: "forced-colors" and "font-palette" are CSS terms of art (the media
             # query / property), "tonal-palette" is Material's own term — pre-existing prose
             # newly caught, the standing false-positive class. "github-facts" and
             # "material-color-facts" are naming-rules' illustrative shape-table examples —
             # phantom until the llm/design rename PRs mint them for real (remove from this
             # set then):
             "forced-colors", "font-palette", "tonal-palette",
             # github-facts pruned 2026-07-21: the harness rename made it a real skill.
             # material-color-facts removed 2026-07-21: the design rename made it a real skill.
             # ADR-0006 screens rename (2026-07-21): the plugin + 15 members add the -ui /
             # -component / -change / -focus suffixes and the *-facts tails to the inventory,
             # flagging three standing false-positive classes. (a) pre-existing prose compounds:
             # "font-ui" (the ui FONT-role compound in typography/design), "agent-ui"
             # (a2ui-world prose + the historical component-builder agent mention), "shadcn-ui"
             # (external library), "per-component"/"one-mark-per-component"/"cross-component"/
             # "multi-component" (per-unit prose), "version-change"/"background-change"/
             # "route-change" (event prose), "default-focus" (state prose). (b) the 2-char-prefix
             # tokenizer floor (lifecycle-and-review class): "genre-facts"/"pattern-facts" are the
             # tails of the REAL ui-genre-facts/ui-pattern-facts whose "ui-" prefix falls below
             # the 3-char first-segment floor:
             "font-ui", "agent-ui", "shadcn-ui", "per-component", "one-mark-per-component",
             "cross-component", "multi-component", "version-change", "background-change",
             "route-change", "default-focus", "genre-facts", "pattern-facts",
             # ADR-0006 teamwork rename (2026-07-21): close-session / grill-the-ask / lead-team /
             # build-feature add the -session / -ask / -team / -feature suffixes to the inventory,
             # flagging pre-existing prose compounds — the standing false-positive class:
             "future-session", "per-session", "this-session", "cross-session", "same-session",
             "authoring-session", "mid-session", "making-ask", "resolve-vs-ask",
             "subagent-vs-team", "whole-team",
             # ADR-0006 docs rename (2026-07-21): file-task / make-doc / check-doc /
             # make-reference / file-bug add the -task / -doc(s) / -reference / -bug suffixes
             # to the inventory, flagging pre-existing prose compounds — the standing class:
             "mid-task", "scheduled-task", "single-purpose-task", "vendor-doc", "design-doc",
             "self-doc", "corpus-docs", "project-docs", "cross-reference", "dangling-reference",
             "extend-reference", "inbound-reference", "plugins-reference", "hard-bug",
             # ADR-0006 harness rename (2026-07-21): make-skill/-agent/-pack/-plugin/-script,
             # plan-*-split/-merge, clean-repo, entry-file-rules et al. add the estate's most
             # generic suffixes (-skill/-pack/-plugin/-file/-script/-repo/-split/-merge) to the
             # inventory, flagging ~60 pre-existing prose compounds in one wave — the standing
             # false-positive class at its structural worst. Allowlisted wholesale; FOLLOW-UP
             # (watch item): G8's suffix heuristic may need a generic-suffix exemption tier now
             # that single-word suffixes dominate the inventory.
             "cross-pack", "non-skill", "token-file", "multi-script", "per-file", "per-script",
             "knowledge-pack", "one-skill", "pre-split", "single-skill", "sub-agents",
             "mini-skills", "single-file", "regime-split", "entry-file", "multi-skill",
             "agent-skills", "agent-to-skill", "agent-vs-preloaded-skill", "bundled-script",
             "check-script", "chosen-skill", "claude-plugin", "cross-plugin", "external-skill",
             "global-skill", "knowledge-skill", "linguistic-techniques-for-agents",
             "mega-plugin", "merge-skills", "multi-repo", "new-consolidated-pack",
             "new-reference-file", "new-skill", "non-agent-file", "non-knowledge-pack",
             "old-skill", "one-pack", "one-plugin", "out-of-repo", "per-plugin", "per-skill",
             "post-merge", "preloaded-skill", "return-by-file", "shared-file", "single-plugin",
             "some-plugin", "some-plugin-repo", "standards-skill", "sub-split", "target-repo",
             "whole-pack",
             # Post-merge main sweep (2026-07-21): docs-plugin prose compounds surfaced once the
             # full merged state gated together — same class:
             "design-docs", "force-file", "non-bug", "whole-file",
             # path-tokenizer artifacts of "…/references/rubric.md" citations inside the make-*
             # skills ("llms.txt by `make-llms-txt/references/rubric.md`" etc.):
             "rubric-llms-txt", "rubric-reference", "rubric-rubric",
             # ADR-0008 design merge (2026-07-21): make-design-system adds the -system suffix
             # to the inventory, flagging pre-existing prose compounds — the standing class
             # ("design-system" itself is the bare prose noun, e.g. "a design-system export"):
             "design-system", "icon-system", "per-system", "scorable-system", "cross-system",
             "geometry-system", "shipped-system",
             # "llms-txt" is the FILE format (llms.txt) named in naming-rules' shapes table,
             # not a phantom sibling of make-llms-txt:
             "llms-txt",
             # ADR-0006 agent-protocols rename (2026-07-21): the a2a-*/a2ui-* digit-prefix
             # tokenizer artifact (1.20.1 class — the regex skips digit-bearing segments), now
             # over the renamed -facts members: catalog-facts/chat-agent-facts/protocol-facts/
             # training-facts are the tails of full a2a-/a2ui- names, not phantom siblings:
             "catalog-facts", "chat-agent-facts", "protocol-facts", "training-facts",
             # ADR-0006 design rename (2026-07-21): the -kit and -isolation suffixes joined
             # the inventory — "bidi-isolation" is the Unicode/CSS term of art in check-translations's
             # prose, "adia-ui-kit" cites an external package in pack-writing-rules; the
             # standing false-positive class:
             "bidi-isolation", "adia-ui-kit",
             # fix-old-names (2026-07-26, issue #97): this skill's subject matter IS retired
             # names, so it necessarily cites them in prose. G8 is right that `ops-issues`
             # matches no installed skill — that is precisely the point being illustrated.
             # A structural exemption is wrong here (the skill should still be policed for
             # phantom LIVE siblings), so the retired names it quotes are named one by one:
             "ops-issues",
             # the new issue-sorter COMMAND skill (2026-07-20) added the "-issues" suffix to this
             # plugin's own inventory for the first time: "sub-issues" is github-facts'
             # pre-existing, unrelated prose (GitHub's own plural term, cited from a real
             # references/sub-issues-and-task-lists.md file) newly caught by that suffix — the
             # standing false-positive class, same shape as -flow/-systems/-discipline above:
             "sub-issues"}
    token_re = re.compile(r"\b([a-z]{3,}(?:-[a-z]{2,})+)\b")
    stale = {}
    for sk in sorted(root.glob("skills/*/SKILL.md")):
        for tok in set(token_re.findall(sk.read_text(encoding="utf-8", errors="replace"))):
            if tok in inventory or tok in allow or tok.rsplit("-", 1)[-1] not in suffixes:
                continue
            stale.setdefault(tok, []).append(sk.parent.name)
    if stale:
        detail = "; ".join(f"`{t_}` in {', '.join(v[:3])}" for t_, v in sorted(stale.items()))
        warn("G8", f"{len(stale)} skill-like name(s) matching no installed skill -> {detail} "
                   "(rename drift or phantom prose sibling; fix or allowlist)")
    else:
        ok("no stale sibling names in any SKILL.md")

    # G11 style lint (ADR-0002, 2026-07-15) — ruff for .py, eslint for .mjs/.js, configs at the
    # WORKSPACE root (ruff.toml / eslint.config.mjs beside the plugin dirs). Behavior stays G4's
    # job (selftests); this layer catches unused/undefined names and dead code. Run-if-reachable,
    # WARN-if-not (same posture as G4's node leg) — CI installs both, so absence only softens
    # local runs. No workspace config = the check doesn't apply (a standalone plugin checkout).
    ws = root.parent
    if (ws / "ruff.toml").is_file():
        ruff_cmd = [shutil.which("ruff")] if shutil.which("ruff") else (
            [shutil.which("uvx"), "ruff"] if shutil.which("uvx") else None)
        if ruff_cmd:
            r = subprocess.run([*ruff_cmd, "check", str(root)], capture_output=True, text=True,
                               cwd=ws, timeout=300)
            if r.returncode != 0:
                head = (r.stdout or r.stderr).strip().splitlines()
                fail("G11", f"ruff findings in {root.name} -> {'; '.join(head[-2:])}")
            else:
                ok("style lint: ruff clean")
        else:
            warn("G11", "ruff.toml present but no ruff/uvx on PATH -> .py style lint unproven locally (CI enforces)")
    if (ws / "eslint.config.mjs").is_file():
        npx = shutil.which("npx")
        has_js = any(root.rglob("scripts/*.mjs")) or any(root.rglob("scripts/*.js"))
        if not has_js:
            pass  # nothing for eslint to check in this plugin
        elif npx:
            r = subprocess.run([npx, "--yes", "eslint", "--no-error-on-unmatched-pattern", str(root)],
                               capture_output=True, text=True, cwd=ws, timeout=300)
            if r.returncode != 0:
                head = (r.stdout or r.stderr).strip().splitlines()
                fail("G11", f"eslint findings in {root.name} -> {'; '.join(head[-2:])}")
            else:
                ok("style lint: eslint clean")
        else:
            warn("G11", "eslint.config.mjs present but no npx on PATH -> .mjs style lint unproven locally (CI enforces)")

    # G6 package
    artifact = None
    if package and name and version and not fails:
        dist = root / "dist"; dist.mkdir(exist_ok=True)
        artifact = dist / f"{name}-{version}.plugin"
        if artifact.exists():
            fail("G6", f"{artifact.name} already exists -> bump the version (same version = update skipped as current)")
            artifact = None
        else:
            with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as z:
                for p in sorted(root.rglob("*")):
                    if p.is_dir() or "dist" in p.parts or p.name == ".DS_Store":
                        continue
                    rel = p.relative_to(root)
                    if rel.parts[0] == ".claude" or str(rel) == "CLAUDE.md":
                        continue  # repo dev harness, not a plugin component
                    z.write(p, p.relative_to(root))
            ok(f"packaged {artifact.relative_to(root)}")

    verdict = "FAIL" if fails else "CLEAN"
    head = f"release_gate · {root} · {verdict} · {len(fails)} fail / {len(warns)} warn"
    print("\n".join([head, *lines]))
    return (1 if fails else 0), artifact


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td) / "demo-plugin"
        (r / ".claude-plugin").mkdir(parents=True)
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "demo-plugin", "version": "0.1.0"}')
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_lint.GOOD_FIXTURE)
        (r / "README.md").write_text("demo-plugin map: demo-review\n\nv0.1.0 · initial\n")
        code, _ = gate(r)
        assert code == 0, "clean fixture plugin must pass"
        body = (r / "skills" / "demo-review" / "SKILL.md")
        body.write_text(body.read_text() + "\nsee ancient-review for history\n")
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            gate(r)
        assert "G8" in buf.getvalue() and "ancient-review" in buf.getvalue(), "stale sibling name must warn G8"
        body.write_text(body.read_text().replace("\nsee ancient-review for history\n", ""))
        # G2 subfolder conformance: a rogue topical dir warns; a sanctioned one doesn't
        rogue = r / "skills" / "demo-review" / "recipes"
        rogue.mkdir()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "demo-review/recipes" in buf.getvalue(), "rogue skill subfolder must WARN G2, not fail"
        rogue.rmdir()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert "recipes" not in buf.getvalue(), "removed rogue dir must clear the G2 warn"
        # G2 broken-symlink control: a link to a missing target must FAIL; repointed, it clears
        link = r / "skills" / "demo-review" / "references"
        link.mkdir()
        (link / "ghost.md").symlink_to("../../retired-skill/references/ghost.md")
        code, _ = gate(r)
        assert code == 1, "broken symlink must FAIL G2 (the CI FileNotFoundError class)"
        (link / "ghost.md").unlink()
        code, _ = gate(r)
        assert code == 0, "removed broken symlink must restore a clean gate"
        link.rmdir()
        (r / "skills" / "demo-review" / "evals").mkdir()
        (r / "skills" / "demo-review" / "evals" / "evals.json").write_text('{"skill": "wrong-owner", "cases": [{"id": "t0", "prompt": "x", "expect": "trigger"}]}')
        code, _ = gate(r)
        assert code == 1, "owner-mismatched suite must fail G7"
        (r / "skills" / "demo-review" / "evals" / "evals.json").write_text(json.dumps({"skill": "demo-review", "cases": (
            [{"id": f"t{i}", "prompt": f"p{i}", "expect": "trigger"} for i in range(5)]
          + [{"id": f"n{i}", "prompt": f"m{i}", "expect": "no-trigger"} for i in range(3)])}))
        code, _ = gate(r)
        assert code == 0, "valid suite must restore a clean gate"
        # G4 js leg: a failing .mjs selftest must bite; a passing one must not flag
        import shutil as _sh
        if _sh.which("node"):
            js = r / "skills" / "demo-review" / "scripts"
            js.mkdir()
            (js / "demo-check.mjs").write_text("if (process.argv[2] === 'selftest') process.exit(1)\n")
            code, _ = gate(r)
            assert code == 1, "failing .mjs selftest must fail G4"
            (js / "demo-check.mjs").write_text("if (process.argv[2] === 'selftest') { console.log('ok'); process.exit(0) }\n")
            code, _ = gate(r)
            assert code == 0, "passing .mjs selftest must keep the gate clean"
            (js / "demo-skip.mjs").write_text("if (process.argv[2] === 'selftest') process.exit(2)\n")
            import io as _io
            import contextlib as _ctx
            _buf = _io.StringIO()
            with _ctx.redirect_stdout(_buf):
                code, _ = gate(r)
            assert code == 0 and "demo-skip.mjs" in _buf.getvalue(), "exit-2 selftest must SKIP disclosed, not fail"
            (js / "demo-skip.mjs").unlink()
        # G11 ruff leg: a workspace-root ruff.toml + a defective .py must bite; fixing restores clean
        if _sh.which("ruff") or _sh.which("uvx"):
            ws_cfg = r.parent / "ruff.toml"
            ws_cfg.write_text('extend-exclude = ["*/dist"]\n[lint]\nignore = ["E702", "E731"]\n')
            lintdir = r / "skills" / "demo-review" / "scripts"
            lintdir.mkdir(exist_ok=True)
            (lintdir / "demo_lint.py").write_text("import os\nprint('hi')\n")  # F401 unused import
            code, _ = gate(r)
            assert code == 1, "ruff F401 in a bundled script must fail G11"
            (lintdir / "demo_lint.py").write_text("print('hi')\n")
            code, _ = gate(r)
            assert code == 0, "clean script must restore a clean G11"
            (lintdir / "demo_lint.py").unlink()
            ws_cfg.unlink()
        code, art = gate(r, package=True)
        assert code == 0 and art and art.exists(), "clean plugin must package"
        code, _ = gate(r, package=True)
        assert code == 1, "same-version repackage must FAIL G6"
        (r / "README.md").write_text("demo-plugin map: demo-review, claude-helper\n\nv0.1.0 · initial\n")
        (r / "skills" / "claude-helper").mkdir()
        (r / "skills" / "claude-helper" / "SKILL.md").write_text(skill_lint.GOOD_FIXTURE)
        code, _ = gate(r)
        assert code == 1, "reserved-word skill dir must fail via G3/F8"
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "Demo Plugin", "version": "1"}')
        code, _ = gate(r)
        assert code == 1, "bad manifest must fail G1"
    print("release_gate selftest · PASS · clean passes, packages once, refuses same-version, catches F8 and bad manifest")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    code, _ = gate(Path(args[0]).resolve(), package="--package" in args[1:])
    sys.exit(code)
