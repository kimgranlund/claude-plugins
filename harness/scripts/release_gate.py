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
      CLAUDE.md counts reconcile, and no two adr/idr/lld/rdd records under `.claude/docs`
      collide on (family, number) (R7, closes #633) — composes docs_check.py; accuracy stays
      human
  G9 packs: every skill with references/INDEX.md passes corpus_check (K1 FAILs fail the gate)
  G8 sibling names: kebab tokens in SKILL.md files that carry one of this plugin's own
     name-suffixes but match no installed skill OR agent -> WARN (rename drift, phantom
     prose siblings; issue #497 widened the inventory to sweep agents/*.md alongside
     skills/*/SKILL.md, so a live agent name no longer needs its own allowlist entry)
  G11 style lint (ADR-0002): ruff over .py / eslint over .mjs|.js, workspace-root configs;
      run when a runner is reachable, WARN when not (CI enforces); no config -> not applicable
  G12 naming grammar (ADR-0011/D9, wired 2026-08-14): authorkit's naming-audit validator run
      in --scope grammar over a repo-root naming.manifest.json; gates naming-grammar findings
      only, structural (schema/provenance) findings stay informational; no manifest or no
      validator on this checkout -> not applicable
  G12b bundled-manifest parity (issue #562): when the gated plugin ships its OWN bundled
      naming.manifest.json (today: authorkit's self-dogfood copy), the same validator is
      re-run BARE (no --manifest, so it discovers that bundled copy) in --scope grammar --
      catches a root-manifest entry the plugin's own artifact names need but the bundled
      copy never mirrored (the drift PR #560 found by hand twice); schema_scope full-vs-
      grammar is a deliberate divergence this leg never grades (the explicit --scope grammar
      overrides it); no bundled copy on this plugin -> not applicable
  G13 marketplace coverage (2026-08-14): when the workspace root carries
      .claude-plugin/marketplace.json, the gated plugin must appear in its plugins list
      (the authorkit-invisible-in-/plugin incident); no manifest -> not applicable
  G14 version monotonicity (2026-08-16, issue #445): a touched plugin's version must exceed
      origin/main's, and the README ledger's newest line must name that version
      (version_monotonic_check.py; complements version_claim_check.py's cross-open-PR tier);
      no origin/main, untouched, or a brand-new plugin -> not applicable
  G15 harness overlay freshness (LLD-0025, gh#885/#886/#890/#891, 2026-08-23): runs
      `harness_emit.py <root> --verify --harness <G15_HARNESSES>` as a subprocess (the gate
      never imports the emitter — same exit-code-contract relationship G4 has to a bundled
      selftest); exit 1 -> FAIL listing each stale/unexpected/marketplace-mismatch path; exit 2
      -> FAIL "emitter setup error"; no harness_emit.py on this checkout -> not applicable.
      G15_HARNESSES = codex,hermes,pi as of W3 (gh#891).
  G15b Claude-only body-token inventory (issue #1008, author-cross-harness-plugins'
      surface-matrix.md rule 5): WARN-only, NEVER FAIL — runs
      `harness_emit.py <root> --scan-tokens --harness <G15_HARNESSES>` as a subprocess (same
      never-import relationship G15 has to the emitter) and lists every skill whose SKILL.md
      body carries a Claude-only substitution token (${CLAUDE_PLUGIN_ROOT}, $ARGUMENTS) that a
      non-Claude harness reads verbatim; sourced from the SAME scan HARNESS-NOTES.md's own
      degradation-inventory section renders, never a second implementation; a token-bearing
      body is a known, recorded degradation, not a release blocker. No harness_emit.py on this
      checkout -> not applicable.

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
import version_monotonic_check

# G15 harness set — a one-line constant each wave widens (LLD-0025 Resolution 5): W1 codex,
# W2 +hermes, W3 (T-6, gh#891) +pi. Kept local (not imported from harness_emit) so the gate never imports
# the emitter — subprocess only, same as G4's relationship to a bundled selftest.
G15_HARNESSES = "codex,hermes,pi"

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
    # "agents" added 2026-08-31 (adiahealth/adia-harness#23): skills/<name>/agents/openai.yaml is
    # harness_emit.py's OWN Codex-overlay output — the estate carries 200+ such dirs; warning on
    # the sanctioned generator's output was a G2/G15 self-contradiction, not a rogue topical dir.
    SANCTIONED_SUBDIRS = {"evals", "references", "scripts", "assets", "agents"}  # ruled 2026-07-15
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

    # G3 full lint via skill_lint. Cross-harness adapter-tree convention (author-cross-harness-
    # plugins, gh adia-harness#35): when a skill's Claude-only invocation dials
    # (disable-model-invocation, user-invocable) live on adapters/claude/skills/<name>/SKILL.md
    # instead of the shared root, the ADAPTER is what Claude actually reads — lint that instead
    # of the root for such a skill (never both: the two bodies are required byte-identical by
    # the adapter-fidelity rule, so linting the root too would just double-report the same body
    # AND wrongly flag the root's own deliberately-absent invocation dials as missing). A skill
    # with no adapter (no Claude-only fields needed) is unaffected -- root lints as before.
    skill_targets = []
    for skill_md in sorted(root.glob("skills/*/SKILL.md")):
        adapter = root / "adapters" / "claude" / "skills" / skill_md.parent.name / "SKILL.md"
        skill_targets.append(adapter if adapter.is_file() else skill_md)
    # Same convention for hooks: adapters/claude/hooks.json is the Claude-facing file when the
    # adapter tree is in use; hooks/hooks.json is the older pre-adapter-tree convention. Prefer
    # the former, fall back to the latter, never both.
    claude_hooks = root / "adapters" / "claude" / "hooks.json"
    hooks_targets = [claude_hooks] if claude_hooks.is_file() else sorted(root.glob("hooks/hooks.json"))
    targets = (skill_targets + sorted(root.glob("agents/*.md"))
               + hooks_targets + ([mf] if mf.is_file() else []))
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
    # issue #497: the inventory sweeps agents/*.md alongside skills/*/SKILL.md (own plugin
    # and every workspace sibling) — a live agent's name (e.g. `estate-audit-agent`) now
    # resolves directly, the same way a live skill name does, with no allowlist entry owed.
    inventory = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    inventory |= {p.stem for p in root.glob("agents/*.md")}
    # per-plugin allow file (2026-08-31, adiahealth/adia-harness#25): a plugin's own domain
    # vocabulary (its gate/hook/compound-term names that read skill-shaped but aren't skills)
    # lives in ITS repo as <plugin-root>/.release-gate-g8-allow.json — a flat JSON array of
    # kebab tokens — instead of growing this file's estate-wide allow set with another
    # plugin's domain terms. Malformed file -> ignored with a warn, never a crash.
    g8_allow_file = root / ".release-gate-g8-allow.json"
    if g8_allow_file.is_file():
        try:
            plugin_allow = json.loads(g8_allow_file.read_text(encoding="utf-8"))
            if isinstance(plugin_allow, list):
                inventory |= {t for t in plugin_allow if isinstance(t, str)}
            else:
                warn("G8", f"{g8_allow_file.name} is not a JSON array -> ignored")
        except (json.JSONDecodeError, OSError) as e:
            warn("G8", f"{g8_allow_file.name} unreadable ({e}) -> ignored")
    for sib in root.parent.glob("*/.claude-plugin/plugin.json"):
        inventory |= {p.parent.name for p in sib.parent.parent.glob("skills/*/SKILL.md")}
        inventory |= {p.stem for p in sib.parent.parent.glob("agents/*.md")}
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
             # naming-rules tests table (2026-08-12): the labeled Bad: counterexamples restored
             # after the ADR-0006 rename sweep was found to have rewritten retired names INSIDE
             # the counterexample cells, collapsing them to Bad==Good (check-everything follow-up
             # audit) — same deliberate-historical-citation class as knowledge-forge above:
             "skill-forge", "docs-alignment",
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
            # gen-ui-kit (2026-08-13, PR #201 follow-up): dispatch-ticket/file-bug's teardown
            # doctrine cites the adiahealth/gen-ui-kit host repo by name — same external-package
            # false-positive class as adia-ui-kit above:
            "gen-ui-kit",
            # ADR-0012 quick-build auto-merge (2026-08-14, issue #244): "auto-merge" is the
            # feature's own name AND the literal grant line `auto-merge: authorized` that
            # dispatch-ticket stage 2b greps for — unrenameable prose tripping the `-merge`
            # suffix plan-skill-merge owns; "quick-build" is ADR-0012's own name tripping the
            # `-build` suffix lead-build owns. Same standing false-positive class:
            "auto-merge", "quick-build",
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
             "sub-issues",
             # issue #433's fleet-lead renames (2026-08-16, issue #450): `lead-planning`,
             # `lead-review`, `lead-product` are teamwork's own COMMAND names
             # (commands/lead-*.md), not skills — G8's inventory only sweeps `skills/*/SKILL.md`,
             # so a live command name is a structural false positive here, same class as every
             # other command-not-skill citation this list already carries.
             # `product-leader-agent` is docs' AGENT name (docs/agents/product-leader-agent.md),
             # cited in prose describing the dispatched sibling seat — not a skill.
             # `product-authoring` is leading-product's own PRE-RENAME name (issue #433 moved
             # it from docs to teamwork and renamed it), cited as deliberate historical
             # provenance — the knowledge-forge/skill-forge class above.
             # `same-plugin` is prose ("now same-plugin", "a same-plugin command") describing
             # the #433 move, not a sibling name.
             # `big-feature` is prose ("a task or big-feature dispatch") describing a Size-class
             # dispatch, not a skill name.
             # `index-bootstrap` is prose ("gates its index-bootstrap offer") describing
             # file-feature's own optional offer, not a skill name.
             # `fleet-state` is prose ("naming one of the three fleet-state files") describing
             # the fleet manifest's on-disk state, not a skill name.
             "lead-planning", "lead-review", "lead-product", "product-leader-agent",
             "product-authoring", "same-plugin", "big-feature", "index-bootstrap",
             "fleet-state",
             # issue #488 (2026-08-17): the G8 sweep's standing 14-item warn, triaged item by
             # item — every one a false positive, none an actual rename-drift repoint target.
             # agent-writing-rules' checker-seat-consolidation section (issue #293) deliberately
             # cites three now-RETIRED agent names while explaining the merge — the same
             # deliberate-historical-citation class as knowledge-forge/product-authoring above:
             "attention-audit-agent", "bloat-audit-agent", "naming-audit-agent",
             # "batch-audit" is the same section's own prose category noun ("Authorkit's three
             # single-instrument batch-audit agents"), not a name:
             "batch-audit",
             # "estate-audit-agent" allowlist entry removed (issue #497): G8's inventory now
             # sweeps `agents/*.md` too, so authorkit's real, LIVE agent (authorkit/agents/
             # estate-audit-agent.md) resolves directly against the widened inventory —
             # no allowlist entry owed any more.
             # clean-git's Done-when line ("every inventoried worktree/branch/PR/claimed-ticket")
             # is a per-unit prose compound sharing dispatch-ticket's "-ticket" suffix, same class
             # as per-ticket/feature-ticket above:
             "claimed-ticket",
             # clean-git's/watch-tickets' "host-repo"/"per-repo" are per-unit prose compounds
             # sharing clean-repo's "-repo" suffix, same class as target-repo/multi-repo/
             # out-of-repo above:
             "host-repo", "per-repo",
             # watch-tickets' "interactive-session" ("richer interactive-session access") is a
             # per-unit prose compound sharing close-session's "-session" suffix, same class as
             # per-session/this-session/cross-session above:
             "interactive-session",
             # skill-writing-rules' "marker-agent" is a literal quoted field value from a
             # measured spawn record (issue #308's F4 finding) — an ephemeral throwaway test
             # agent's name from that experiment, not a live sibling reference:
             "marker-agent",
             # plan-skill-merge's "pack-authoring" ("route to a pack-authoring research wave") is
             # prose naming make-pack's own domain of work, sharing manifest-authoring's
             # "-authoring" suffix — not a skill name, same class as product-authoring above:
             "pack-authoring",
             # checking-rules' "per-flow" ("the per-flow contracts that apply it") is a per-unit
             # prose compound sharing break-down-flow's "-flow" suffix, same class as
             # cross-flow/mid-flow above:
             "per-flow",
             # watch-tickets' "source-file" ("no source-file edits") is a per-unit prose compound
             # sharing entry-file's "-file" suffix, same class as single-file/shared-file/
             # entry-file above:
             "source-file",
             # check-everything's "harness-audit" is its OWN report-directory naming convention
             # (`<root>/harness-audit-<date>/`), not a citation of any sibling skill:
             "harness-audit",
             # issue #497's own G8 widening (agents/*.md now feeds the inventory) pulled five
             # NEW agent-owned suffixes into `suffixes` (-runner from fact-finder's family,
             # -finder, -checker from the *-checker seats, -judge from routing-judge) — each
             # newly catching pre-existing, unrelated prose, the standing false-positive class:
             # "backfill-runner" is skill-writing-rules' illustrative NOT-for example (a
             # hypothetical sibling in a "Good (trigger contract)" teaching block, never a real
             # skill); "candidate-finder" is plan-skill-merge's own self-descriptive negative
             # ("Not a candidate-finder"); "decision-checker" and "corpus-checker" are
             # agent-writing-rules' generic lifecycle-stage role labels for design-system-checker/
             # font-choice-checker ("a pre-export decision-checker and a post-export
             # corpus-checker"), not citations of any real sibling; "single-judge" is
             # check-routing's own named concept (its single-judge-noise voting-round rationale),
             # not a skill or agent name:
             "backfill-runner", "candidate-finder", "decision-checker", "corpus-checker",
             "single-judge",
             # same #497 widening, caught in OTHER plugins once their own gate runs against the
             # now-larger cross-workspace suffix set: "single-writer" (agent-protocols'
             # a2a-training-facts, "all-or-nothing single-writer import tool") is a term-of-art
             # phrase, not a sibling name; "ops-planner" (authorkit's fix-old-names, an
             # illustrative retired-agent error message: "Agent type 'ops-planner' not found") is
             # a deliberate historical citation, the same class as `ops-issues` already above:
             "single-writer", "ops-planner",
             # ADR-0020 wave 4 (#522) minted `fleet-orchestration` as a real installed skill,
             # which widened the `-orchestration` suffix into G8's live inventory and caught two
             # pre-existing, unrelated prose compounds now in fleet-rules (ADR-0020 D5 merged
             # them in from team-or-solo-rules, #524): "over-orchestration"
             # (its own routing-rubric warning against over-delegating a task one context could
             # hold) and "rubric-orchestration" (a rubric-name label in its handoff table, not a
             # citation of any sibling):
             "over-orchestration", "rubric-orchestration",
             # ADR-0020 D5 (#524) merged team-or-solo-rules into fleet-rules; the retired name
             # survives as a historical citation in fleet-rules' own body/README/CHANGELOG
             # provenance notes, not a live sibling reference:
             "team-or-solo-rules",
             # #620's check-state --fleet scope widened the `-repo` suffix (already live via
             # authorkit's repo-audit) into two ordinary prose compounds in check-state's own
             # SKILL.md: "cross-repo" (the rollup's own adjective, e.g. "cross-repo rollup") and
             # "source-repo" ("not-a-source-repo", the marketplace-drift N/A status value) —
             # neither names any sibling skill or agent:
             "cross-repo", "source-repo",
             # brand-design's Phase 3 migration (2026-08-19): 11 G8 warns triaged, all verified
             # against the actual prose (no drift found, every one is a concept/prose compound
             # or an intentional cross-marketplace mention):
             # "brand-council"/"sub-council"/"orchestration-rubric" are check-brand-council's own
             # prose (an agent-seat name in attribution frontmatter, the legacy retired
             # `/brand-council` command cited historically, the sub-council concept, and
             # `teamwork:fleet-rules`' rule-ID slug) — no skill named `brand-council` exists,
             # the skill IS `check-brand-council`, same class as order-vs-task-flow above;
             # "brand-stack"/"expression-system" are brand-methodology-rules'/brand-rubrics' own
             # named concepts (the one-page Brand Stack condensation rendered by the REAL
             # `make-brand-stack` skill; a rubric dimension) — the bare noun isn't the skill name;
             # "cloud-skill" is file-brand's own prose ("the plugin form never carries the
             # cloud-skill... packaging"), not a literal skill reference;
             # "main-agent" is make-brand-muse's prose ("keeps main-agent judgment in the loop"),
             # not a literal agent reference;
             # "per-stage"/"real-brand" are brand-corpus's/brand-guidelines' own prose
             # ("per-stage detail", "which real-brand exemplar");
             # "design-skills"/"nonoun-skills" are the intentional, disclosed cross-marketplace
             # mention of `design-skills:brand-decomposer` (a different marketplace, per
             # brand-guidelines' own stated MAKES-vs-GRADES split) — same external-package class
             # as adia-ui-kit/gen-ui-kit above, not a workspace sibling this estate installs:
             "brand-council", "sub-council", "orchestration-rubric", "brand-stack",
             "expression-system", "cloud-skill", "main-agent", "per-stage", "real-brand",
             "design-skills", "nonoun-skills",
             # frontend's new reactivity-facts pack (2026-08-20, issue #805): "tier-split" is a
             # references FILE (references/tier-split.md, cited from the SKILL.md consult table
             # and its own boundaries section) — the standing references-file false-positive
             # class, same shape as container-patterns/scale-theory/box-model-and-flow/
             # merge-semantics above; "whole-component" is prose ("per-part reactivity vs
             # whole-component re-render" in the description) sharing make-component's own
             # "-component" suffix, same class as per-component/cross-component/multi-component:
             "tier-split", "whole-component"}
    token_re = re.compile(r"\b([a-z]{3,}(?:-[a-z]{2,})+)\b")
    stale = {}
    for sk in sorted(root.glob("skills/*/SKILL.md")):
        text = sk.read_text(encoding="utf-8", errors="replace")
        for tok in set(token_re.findall(text)):
            if tok in inventory or tok in allow or tok.rsplit("-", 1)[-1] not in suffixes:
                continue
            # verbatim file-citation class (2026-08-20, issue #814): a token immediately
            # glued to a literal ".md" anywhere in the file (`<tok>.md`) is citing a FILE
            # by name — this pack's own `references/<tok>.md` (the tier-split/scale-theory/
            # container-patterns/box-model-and-flow/merge-semantics/transport-and-streaming
            # class already hand-allowlisted above) or a verbatim external-repo filename kept
            # for grounding fidelity (agent-ui's `select-menu-name-bug.md`, adia-v2's
            # `url-state-sync.md`) — never a phantom SKILL name, since an installed skill is
            # cited by its bare kebab name, never with a literal `.md` extension appended.
            # Mechanism over allowlist growth for this class going forward; existing entries
            # above are left in place (redundant-but-harmless, not a regression to clean up
            # here). G8 still does NOT strip code spans generally — a bare backticked stale
            # name with no `.md` glued to it is still rot and still fires (proven by the
            # selftest's own "ancient-review"/"phantom-old-rule" negative controls) — only a
            # token directly glued to `.md` is exempted.
            if re.search(re.escape(tok) + r"\.md\b", text):
                continue
            # namespaced-citation class (2026-08-31, adiahealth/adia-harness#25): a token the
            # file cites as `<plugin>:<tok>` (e.g. `teamwork:loop-rules`) is an EXPLICIT
            # cross-plugin reference — the author named the owning plugin, so the sibling
            # lookup's physical-co-location requirement doesn't apply (the cited plugin may
            # live in a different repo entirely, as adia-sdlc's do). A bare token with no
            # namespace anywhere in the file still fires — this trusts only the namespaced form.
            if re.search(r"[a-z0-9][a-z0-9-]*:" + re.escape(tok) + r"\b", text):
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

    # G12 naming grammar (ADR-0011/D9, wired 2026-08-14, issue #197) — authorkit's
    # naming-audit validator, run in --scope grammar: gates ONLY naming-grammar findings
    # (name production, lexicon disjointness, the reserved -agent head), the slice D8's
    # grandfather+ratchet exemptions cover and skill_lint's retired W4/W5 used to police.
    # Structural findings (author/date provenance, kind-declared policy, reference-index
    # completeness) are a BROADER schema this estate never ratified adopting — measured
    # empirically wiring this ticket: gating on them estate-wide fails hundreds of findings
    # that are not naming issues at all. They print via the validator's own report and are
    # counted here for visibility, never gated. Feature-detected: a plugin repo without the
    # repo-root manifest or without authorkit installed skips this check entirely (same
    # posture as G11's missing-config case) — not applicable, not a failure.
    naming_manifest = ws / "naming.manifest.json"
    naming_validator = ws / "authorkit" / "skills" / "naming-audit" / "scripts" / "validate.py"
    if naming_manifest.is_file() and naming_validator.is_file():
        r = subprocess.run(
            [sys.executable, str(naming_validator), "--target", str(root),
             "--manifest", str(naming_manifest), "--json", "--scope", "grammar"],
            capture_output=True, text=True, cwd=ws, timeout=60)
        try:
            d = json.loads(r.stdout)
        except (json.JSONDecodeError, ValueError):
            fail("G12", f"naming-audit validator produced no parseable JSON -> {(r.stdout or r.stderr)[-300:]}")
        else:
            g_errs = d.get("grammar_errors", [])
            s_count = len(d.get("structural_errors", []))
            if g_errs:
                detail = "; ".join(f"{n}: {m}" for n, _, m, _ in g_errs[:3])
                fail("G12", f"{len(g_errs)} naming-grammar finding(s) -> {detail} "
                            "-> run authorkit's naming-audit --scope grammar for the full list")
            else:
                ok(f"naming grammar clean (scope=grammar; {s_count} structural finding(s) "
                   "tracked separately, informational-only pending estate-wide schema adoption)")
    elif naming_manifest.is_file() and not naming_validator.is_file():
        warn("G12", "naming.manifest.json present but authorkit's validator is not on this checkout "
                    "-> naming-grammar gate unproven locally")

    # G12b bundled-manifest parity (issue #562) — a plugin that ships its OWN bundled
    # naming.manifest.json (today: authorkit's self-dogfood copy) dogfoods that bundled
    # copy directly; G12 above only ever validates against the WORKSPACE-ROOT manifest
    # explicitly passed via --manifest, so a bundled copy drifting stale (5 object_vocab
    # entries missing at PR #560's build, grown from 3 at LLD-0004's -- both times a
    # HAND-noticed incident, never gate-caught) never failed a run. Re-running the SAME
    # validator BARE (no --manifest) makes it discover and grade the plugin's OWN bundled
    # copy instead. --scope grammar is explicit here, never inherited from the bundled
    # manifest's own schema_scope field (deliberately "full" -- authorkit's own stricter
    # self-dogfood tier, ADR-0011/D9's structural-schema divergence): grading that broader
    # tier here would fail this gate on authorkit's deliberate stricter posture instead of
    # an actual naming-grammar drift ("schema_scope full-vs-grammar is a KNOWN deliberate
    # divergence, never a failure" -- issue #562's own acceptance). A vocab entry the
    # plugin's own artifact names actually need, but the bundled copy never mirrored,
    # surfaces as a grammar_errors finding exactly the way #560's drift did -- grounded in
    # real usage, not a structural diff of the two files (which has no way to define
    # "scoped to this plugin" for a lexicon entry the plugin's own names never exercise).
    # No bundled copy for this plugin -> not applicable, skip silently (most plugins carry
    # none).
    bundled_manifest = root / "naming.manifest.json"
    if bundled_manifest.is_file() and naming_validator.is_file():
        rb = subprocess.run(
            [sys.executable, str(naming_validator), "--target", str(root),
             "--json", "--scope", "grammar"],
            capture_output=True, text=True, cwd=ws, timeout=60)
        try:
            db = json.loads(rb.stdout)
        except (json.JSONDecodeError, ValueError):
            fail("G12b", f"bundled-manifest validator produced no parseable JSON -> "
                          f"{(rb.stdout or rb.stderr)[-300:]}")
        else:
            gb_errs = db.get("grammar_errors", [])
            if gb_errs:
                detail = "; ".join(f"{n}: {m}" for n, _, m, _ in gb_errs[:3])
                fail("G12b", f"{len(gb_errs)} bundled-manifest parity finding(s) -> {detail} "
                            f"-> {bundled_manifest} is missing vocab {root.name}'s own artifacts "
                            "need; resync it from the root manifest")
            else:
                ok(f"bundled naming.manifest.json parity clean ({bundled_manifest.name} self-check)")
    elif bundled_manifest.is_file() and not naming_validator.is_file():
        warn("G12b", "bundled naming.manifest.json present but authorkit's validator is not on "
                     "this checkout -> bundled-manifest parity gate unproven locally")

    # G13 marketplace coverage (2026-08-14: authorkit shipped through the gate, landed on main,
    # and was invisible in /plugin for a day — the root marketplace.json enumerates plugins
    # explicitly, exactly like gate.yml's loop, and nothing checked it; the same
    # hardcoded-list-goes-stale class REVIEW-209 caught in CI). Feature-detected: no root
    # marketplace manifest -> not applicable (a standalone plugin repo), never a failure.
    mkt = ws / ".claude-plugin" / "marketplace.json"
    if mkt.is_file() and name:
        try:
            listed = [p.get("name") for p in json.loads(mkt.read_text()).get("plugins", [])]
        except (json.JSONDecodeError, ValueError) as e:
            fail("G13", f"root marketplace.json unparseable ({e}) -> the marketplace serves nothing")
        else:
            if name in listed:
                ok(f"marketplace.json lists {name} ({len(listed)} plugins listed)")
            else:
                fail("G13", f"{name} missing from root marketplace.json -> installed users never "
                            "see it in /plugin; add its entry (name/displayName/source/description)")

    # G14 version monotonicity (issue #445): a touched plugin's version must strictly exceed
    # origin/main's, and the README ledger's newest line must name that version — the pre-merge,
    # CI-visible tier of version discipline (version_claim_check.py's cross-open-PR tier is the
    # coordinator-run complement CI cannot see). Feature-detected via version_monotonic_check's
    # own SKIP path: no origin/main reachable, this plugin untouched relative to it, or the
    # plugin absent from origin/main entirely (brand new) -> not applicable, never a false red.
    vmc = version_monotonic_check
    top = vmc._git(["rev-parse", "--show-toplevel"], root)
    if top.returncode != 0:
        warn("G14", "not inside a git checkout -> version-monotonicity check not applicable")
    else:
        git_root = Path(top.stdout.strip())
        rel = root.resolve().relative_to(git_root).as_posix()
        if not vmc._origin_main_available(git_root):
            warn("G14", "origin/main unavailable in this checkout (no fetch, or the ref is "
                        "missing) -> version-monotonicity check skipped, not failed")
        elif not vmc._plugin_touched(git_root, rel):
            ok("G14 not applicable: no diff against origin/main for this plugin")
        else:
            manifest_rel = f"{rel}/.claude-plugin/plugin.json"
            main_manifest_text = vmc._file_at_main(git_root, manifest_rel)
            if main_manifest_text is None:
                ok("G14 not applicable: no baseline on origin/main (new plugin)")
            else:
                main_version = vmc.parse_version(main_manifest_text)
                if main_version is None or version is None:
                    fail("G14", f"origin/main's {manifest_rel} has no readable \"version\" field")
                else:
                    mono_ok, mono_msg = vmc.check_monotonic(version, main_version)
                    readme_text = (root / "README.md").read_text(encoding="utf-8", errors="replace") \
                        if (root / "README.md").is_file() else ""
                    ledger_ok, ledger_msg = vmc.check_ledger(version, readme_text)
                    if mono_ok and ledger_ok:
                        ok(f"G14 version monotonicity: {mono_msg}; {ledger_msg}")
                    if not mono_ok:
                        fail("G14", mono_msg)
                    if not ledger_ok:
                        fail("G14", ledger_msg)

    # G15 harness overlay freshness (LLD-0025, gh#885/#886) — verify-only; the writer runs in
    # /ship-plugin's own preflight, never here (a gate that rewrites committed source hides a
    # write inside a read — Resolution 5). Subprocess only: the gate never imports the emitter,
    # same relationship G4 has to a bundled selftest.
    emit_script = Path(__file__).resolve().parent / "harness_emit.py"
    if not emit_script.is_file():
        warn("G15", "harness_emit.py not present on this checkout -> overlay freshness not applicable")
    else:
        r = subprocess.run(
            [sys.executable, str(emit_script), str(root), "--verify", "--harness", G15_HARNESSES],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            ok(f"G15 harness overlay freshness: clean ({G15_HARNESSES})")
        elif r.returncode == 1:
            findings = [ln for ln in r.stdout.splitlines() if ln.strip().startswith(("stale:", "unexpected:", "marketplace-mismatch:"))]
            detail = "; ".join(findings[:5]) if findings else r.stdout.strip()[-300:]
            fail("G15", f"{len(findings) or 1} stale/unexpected overlay finding(s) -> {detail}")
        else:
            fail("G15", f"emitter setup error -> {(r.stdout + r.stderr).strip()[-300:]}")

    # G15b Claude-only body-token inventory (issue #1008, author-cross-harness-plugins'
    # surface-matrix.md rule 5) — WARN-only, never FAIL: a Claude-only token in a skill body
    # is a known, recorded degradation (HARNESS-NOTES.md already names it), not a release
    # blocker. Subprocess only, same as G15 — sources its finding list from the SAME scan
    # `harness_emit.py --scan-tokens` runs for HARNESS-NOTES.md's own section, never a second
    # implementation to drift apart from it.
    if not emit_script.is_file():
        warn("G15b", "harness_emit.py not present on this checkout -> token inventory not applicable")
    else:
        r15b = subprocess.run(
            [sys.executable, str(emit_script), str(root), "--scan-tokens", "--harness", G15_HARNESSES],
            capture_output=True, text=True,
        )
        if r15b.returncode != 0:
            warn("G15b", f"scan setup error -> {(r15b.stdout + r15b.stderr).strip()[-300:]}")
        else:
            findings = [ln.strip() for ln in r15b.stdout.splitlines() if ln.strip().startswith("token-degradation:")]
            if findings:
                warn("G15b", f"{len(findings)} skill(s) carry Claude-only body tokens -> {'; '.join(findings)}")
            else:
                ok("G15b Claude-only body-token inventory: clean")

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
        (r / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "demo-plugin", "version": "0.1.0", "description": "A demo plugin."}')
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text(skill_lint.GOOD_FIXTURE)
        (r / "README.md").write_text("demo-plugin map: demo-review\n\nv0.1.0 · initial\n")
        emit_script = Path(__file__).resolve().parent / "harness_emit.py"
        def w(root=r):
            # best-effort overlay write, ignoring failures (a deliberately-broken fixture
            # manifest can't emit — those legs already expect code==1 from another gate,
            # so a stale/unwritten G15 riding along changes nothing they assert)
            subprocess.run([sys.executable, str(emit_script), str(root)], capture_output=True)
        w()
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
        # G8 agent-name widening (issue #497): a live agent cited in a SKILL.md must resolve
        # against agents/*.md too, not just skills/*/SKILL.md — clean with NO allowlist entry
        # proves the widened inventory actually fired, not a coincidence of the allow set.
        agents_dir = r / "agents"
        agents_dir.mkdir()
        (agents_dir / "demo-auditor.md").write_text(skill_lint.GOOD_AGENT_FIXTURE)
        body.write_text(body.read_text() + "\nsee demo-auditor for the dispatched review seat\n")
        w()  # a new agent changes HARNESS-NOTES.md's dropped-agents ledger; resync before G15 checks it
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "G8" not in buf.getvalue(), \
            "a live agent name must resolve via the widened G8 inventory, no allowlist needed"
        body.write_text(body.read_text().replace("\nsee demo-auditor for the dispatched review seat\n", ""))
        (agents_dir / "demo-auditor.md").unlink()
        agents_dir.rmdir()
        w()  # the agent is gone again; resync the ledger before the next code==0 assertion
        # G8 verbatim file-citation class (issue #814, select-menu-name-bug/url-state-sync):
        # a token glued to a literal ".md" must go quiet with no allowlist entry — the
        # false-positive class this ticket fixes. Same "ancient-review" token the plain
        # positive-fire test above already proves fires bare (suffix "-review" matches the
        # fixture's only live skill, demo-review) — here it's glued to ".md", the only
        # variable changed, isolating the mechanism under test:
        body.write_text(body.read_text() +
                         "\nsee agent-ui's `ancient-review.md` for the incident\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "G8" not in buf.getvalue(), \
            "a token glued to a literal .md file citation must not warn G8, no allowlist needed"
        body.write_text(body.read_text().replace(
            "\nsee agent-ui's `ancient-review.md` for the incident\n", ""))
        # G8 namespaced-citation class (adiahealth/adia-harness#25): a token cited as
        # `<plugin>:<tok>` must go quiet with no allowlist entry — the author named the
        # owning plugin, so co-location isn't required. Same "ancient-review" token proven
        # to fire bare above; here it's namespaced, the only variable changed:
        body.write_text(body.read_text() +
                         "\nroute deep dives to otherplugin:ancient-review per doctrine\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "G8" not in buf.getvalue(), \
            "a namespaced plugin:name citation must not warn G8, no allowlist needed"
        body.write_text(body.read_text().replace(
            "\nroute deep dives to otherplugin:ancient-review per doctrine\n", ""))
        # G8 per-plugin allow file (adiahealth/adia-harness#25): a token in the plugin's own
        # .release-gate-g8-allow.json must go quiet; removing the file makes it fire again.
        body.write_text(body.read_text() + "\nsee ancient-review for history\n")
        (r / ".release-gate-g8-allow.json").write_text('["ancient-review"]')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert "G8" not in buf.getvalue() or "ancient-review" not in buf.getvalue(), \
            "a token in the plugin's own g8 allow file must not warn G8"
        (r / ".release-gate-g8-allow.json").unlink()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            gate(r)
        assert "ancient-review" in buf.getvalue(), \
            "removing the g8 allow file must make the token fire again (reverse control)"
        body.write_text(body.read_text().replace("\nsee ancient-review for history\n", ""))
        # Negative control: a genuine phantom name inside a sources.md-shaped table row
        # (pipe-delimited, backticked, "primary"/provenance vocabulary) but with NO ".md"
        # glued to it must still fire — proves the fix targets the literal ".md" glue, not
        # table-row shape or citation context generally.
        body.write_text(body.read_text() +
                         "\n| `some-repo` | `phantom-old-review` (primary — the case study) |\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert "G8" in buf.getvalue() and "phantom-old-review" in buf.getvalue(), \
            "a phantom name with no .md glue must still warn G8 even in a sources.md-shaped row"
        body.write_text(body.read_text().replace(
            "\n| `some-repo` | `phantom-old-review` (primary — the case study) |\n", ""))
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
            # select mirrors the real workspace ruff.toml (E4/E7/E9/F only) — a bare `ignore=`
            # with no `select=` pulls in ruff's full default rule set (N999/I001 among them),
            # which fires on the Hermes __init__.py's plugin-root package name (hyphenated,
            # like every real plugin dir) for reasons that have nothing to do with G11's own
            # F401 leg below; matching production scope keeps this fixture honest.
            ws_cfg.write_text(
                'extend-exclude = ["*/dist"]\n[lint]\nselect = ["E4", "E7", "E9", "F"]\n'
                'ignore = ["E702", "E731"]\n'
            )
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
        # G12 naming-grammar leg: a workspace-root naming.manifest.json + a stub validator
        # prove THIS gate's own wiring (JSON parse, fail/ok decision) — authorkit's own
        # selftest proves the real validator's grammar/structural partition is correct.
        naming_mf = r.parent / "naming.manifest.json"
        naming_mf.write_text('{"exemptions": []}')
        stub_dir = r.parent / "authorkit" / "skills" / "naming-audit" / "scripts"
        stub_dir.mkdir(parents=True)
        stub = stub_dir / "validate.py"
        stub.write_text(
            "import json, os, sys\n"
            "target = sys.argv[sys.argv.index('--target') + 1]\n"
            "bare = '--manifest' not in sys.argv\n"
            "trigger = 'BUNDLED_TRIGGER' if bare else 'TRIGGER'\n"
            "bad = os.path.exists(os.path.join(target, trigger))\n"
            "out = {'grammar_errors': [['x', 'error', 'stub grammar violation', 'grammar']] if bad else [],\n"
            "       'structural_errors': []}\n"
            "print(json.dumps(out))\n"
        )
        code, _ = gate(r)
        assert code == 0, "clean G12 stub (no trigger file) must keep the gate clean"
        (r / "TRIGGER").write_text("x")
        code, _ = gate(r)
        assert code == 1, "G12 stub grammar_errors must fail the gate"
        (r / "TRIGGER").unlink()
        code, _ = gate(r)
        assert code == 0, "removing the trigger file restores a clean G12"
        # G12b bundled-manifest parity leg (issue #562): a plugin's OWN
        # naming.manifest.json (self-dogfood copy, today only authorkit's) is graded by a
        # BARE (no --manifest) call to the same validator — the seeded-drift negative
        # control this ticket's acceptance names. BUNDLED_TRIGGER is deliberately a
        # DIFFERENT file than G12's own TRIGGER (the stub's `bare` branch above), so the
        # two legs stay independently provable and never cross-fire each other.
        bundled_mf = r / "naming.manifest.json"
        bundled_mf.write_text('{"exemptions": []}')
        code, _ = gate(r)
        assert code == 0, "synced bundled manifest (no seeded drift) must keep the gate clean"
        (r / "BUNDLED_TRIGGER").write_text("x")
        code, _ = gate(r)
        assert code == 1, "seeded bundled-manifest drift must fail G12b (the negative control)"
        (r / "BUNDLED_TRIGGER").unlink()
        code, _ = gate(r)
        assert code == 0, "removing the seeded drift restores a clean G12b"
        bundled_mf.unlink()
        code, _ = gate(r)
        assert code == 0, "no bundled manifest -> G12b not applicable, gate stays clean"
        stub.unlink()
        stub_dir.rmdir()
        (r.parent / "authorkit" / "skills" / "naming-audit").rmdir()
        (r.parent / "authorkit" / "skills").rmdir()
        (r.parent / "authorkit").rmdir()
        naming_mf.unlink()
        # G13 marketplace-coverage leg: a root marketplace.json that omits the plugin must
        # FAIL (the 2026-08-14 authorkit-invisible-in-/plugin incident); listing it restores
        # clean; removing the manifest restores not-applicable — the negative control.
        mkt_dir = r.parent / ".claude-plugin"
        mkt_dir.mkdir()
        mkt = mkt_dir / "marketplace.json"
        mkt.write_text('{"name": "demo-market", "plugins": [{"name": "other-plugin"}]}')
        code, _ = gate(r)
        assert code == 1, "plugin absent from root marketplace.json must FAIL G13"
        mkt.write_text('{"name": "demo-market", "plugins": [{"name": "other-plugin"}, {"name": "demo-plugin"}]}')
        w()  # a root marketplace.json now exists; resync the estate .agents/plugins mirror G15 also checks
        code, _ = gate(r)
        assert code == 0, "plugin listed in root marketplace.json must pass G13"
        mkt.unlink()
        mkt_dir.rmdir()
        w()  # the marketplace name feeds HARNESS-NOTES (3.19.3); removing it changes the overlay too
        code, _ = gate(r)
        assert code == 0, "no root marketplace.json -> G13 not applicable, gate stays clean"
        # G15 harness overlay freshness leg (LLD-0025, gh#885/#886, 2026-08-23): a stale overlay
        # must fail G15, a fresh one must pass — the same bite-proof pattern G4's .mjs leg uses.
        w()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15" in buf.getvalue(), "a freshly-written overlay must pass G15"
        (r / ".codex-plugin" / "plugin.json").write_text('{"drifted": true}')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 1 and "FAIL  G15" in buf.getvalue(), "a hand-edited overlay must FAIL G15"
        w()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15" in buf.getvalue(), "rewriting the overlay must restore a clean G15"
        # G15 Hermes leg (W2, gh#890): a hand-edited Hermes overlay file must FAIL G15 too —
        # G15_HARNESSES now covers codex,hermes, not just codex.
        (r / "__init__.py").write_text("# hand-edited\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 1 and "FAIL  G15" in buf.getvalue(), "a hand-edited Hermes __init__.py must FAIL G15"
        w()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15" in buf.getvalue(), "rewriting the Hermes overlay must restore a clean G15"
        # G15 Pi leg (W3, gh#891): a hand-edited Pi overlay file must FAIL G15 too —
        # G15_HARNESSES now covers codex,hermes,pi.
        (r / "package.json").write_text('{"drifted": true}')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 1 and "FAIL  G15" in buf.getvalue(), "a hand-edited Pi package.json must FAIL G15"
        w()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15" in buf.getvalue(), "rewriting the Pi overlay must restore a clean G15"
        # G15b Claude-only body-token inventory (issue #1008): WARN, never FAIL — a
        # token-free body stays quiet, a token-bearing body warns and names the carrying
        # skill, and adding the token must never fail the gate outright the way a hand-edit
        # fails G15.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15b" in buf.getvalue(), "a token-free body must stay quiet on G15b"
        body.write_text(body.read_text() + "\nSee ${CLAUDE_PLUGIN_ROOT}/scripts/x.mjs for the script.\n")
        w()  # HARNESS-NOTES.md's own degradation-inventory section derives from body content
             # too (item 2) -> resync the overlay so this leg tests ONLY G15b, not a stale G15
             # riding along as a side effect of the same body edit.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0, "G15b is WARN-only -> a Claude-only body token must never FAIL the gate"
        assert "warn  G15b" in buf.getvalue() and "demo-review" in buf.getvalue(), \
            "a Claude-only body token must WARN G15b and name the carrying skill"
        body.write_text(body.read_text().replace("\nSee ${CLAUDE_PLUGIN_ROOT}/scripts/x.mjs for the script.\n", ""))
        w()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, _ = gate(r)
        assert code == 0 and "ok    G15b" in buf.getvalue(), "removing the token must restore a clean, quiet G15b"
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
