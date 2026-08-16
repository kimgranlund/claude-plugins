#!/usr/bin/env python3
"""collide_hook.py — PostToolUse write-time collision pre-lint (issue #294).

Wires `collide.py --against` (v0.10.0's write-time capability, never invoked
by anything until now) into the SAME derive-target-from-write plumbing PR
#287 built for the naming-grammar hook (issue #276's `resolve_hook_target`
shape): a written file's own path decides the checkout root, worktree or
primary alike — no `$CLAUDE_PROJECT_DIR`, no hardcoded plugin list.

Scope, deliberately narrower than the naming hook: fires ONLY when the
written file is a `SKILL.md` AND its `description:` field actually changed
(a body-only edit, or a re-write with an identical description, is a no-op
here — a collision score is a function of the description text alone, so
checking it after a no-op edit would be pure latency with no new signal).
The prior description comes from `git show HEAD:<path>`; a file with no
HEAD blob (brand new) is always treated as changed.

Judgment-shaped, never a hard block (hook-writing-rules' routing test — a
collision SCORE is not a pass/fail check, it's evidence a human/model has
to weigh: rename, fence with a NOT-clause, or leave it, depending on
context this script cannot see). Exit 2 is used here in its PostToolUse
"ask" sense — it feeds the finding back to Claude as something to
consider, exactly like the naming-grammar hook's transport, but the
MESSAGE itself never says "fix this"; it says "classify this and decide".
Nothing here ever re-blocks a write that already landed.

Fail-open discipline (#287's shape guards, carried forward verbatim): a
malformed event, a non-dict shape, a missing/non-string file_path, no
derivable git root, or ANY unexpected exception from the collide sweep
itself all exit 0 silently. A flaky governance hook is worse than none.

Usage:
  collide_hook.py                    PostToolUse entry point, reads the hook
                                      event off stdin
  collide_hook.py selftest           prove the counters bite

Exit: 0 no-op or clean · 2 collision finding(s) surfaced (advisory, not a
block) · never anything else — an internal error still exits 0.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import collide  # noqa: E402  (sibling module, same scripts/ dir)
except Exception:
    # hook-checker finding (2026-08-16): a broken sibling module must never surface as an
    # uncaught ImportError/traceback on every single write — fail open at import time too,
    # not just inside run_hook's own try/except (which never even gets a chance to run).
    collide = None


def short_name(qualified: str) -> str:
    """'plugin:skill-name' or 'plugin:agent-name (agent)' -> just the artifact's own name,
    stripped of both the plugin prefix and the ' (agent)' suffix collide.py's own gather()
    appends — the exact component `--against` is meant to match, never a raw substring
    (hook-checker finding, 2026-08-16: 'audit' as a substring over-matched 'bloat-audit',
    'pattern-audit', etc. for any skill whose own name merely contained it)."""
    return qualified.split(":")[-1].replace(" (agent)", "")


def find_repo_root(path: Path):
    """Same shape as naming-audit's validate.py::find_repo_root (issue #276):
    ask git which checkout the write physically landed in — worktree-correct
    by construction, no env var, no marker-file walk. Fail open (None) on
    any git failure."""
    cwd = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return Path(out.stdout.strip())


def prior_description(repo_root: Path, rel: Path):
    """The written file's description as of HEAD, or None when there is no
    HEAD blob to compare against (a brand-new file — always treated as
    'changed', since a fresh description has never been checked before)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "show", f"HEAD:{rel.as_posix()}"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    _, desc, _ = collide.parse_desc(out.stdout)
    return desc


def format_findings(plugin: str, against: str, hits: list) -> str:
    hits = sorted(hits, key=lambda x: -x["score"])
    lines = [f"attention-audit-collide-postwrite: {len(hits)} potential description "
             f"collision(s) for {plugin}:{against} — judgment call, not a hard block:"]
    for x in hits[:5]:
        other = x["b"] if short_name(x["a"]) == against else x["a"]
        ev = ", ".join(x["shared"][:4] + [f'"{b}"' for b in x["shared_bigrams"][:2]])
        scope = "cross-plugin" if x["cross_plugin"] else "same-plugin"
        lines.append(f"  {x['score']:.1f} {scope} vs {other} — shared: {ev}")
    lines.append(
        "Classify each: routing twin (needs a NOT-fence naming the sibling, or a rename) / "
        "boilerplate tax (shared template sentences) / coincidence. Never required to change "
        "anything on this signal alone — it's evidence for the judgment layer, same as a "
        "manual `collide.py --against` run."
    )
    return "\n".join(lines)


def run_hook(file_path: str) -> int:
    """Core logic, factored out of stdin parsing so selftest can drive it
    directly against fixture paths without faking a stdin event."""
    if collide is None:
        return 0  # sibling module failed to import — fail open, nothing else can run
    if not file_path.endswith("SKILL.md"):
        return 0
    p = Path(file_path)
    if not p.is_absolute() or not p.is_file():
        return 0
    try:
        new_text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    name, desc, dmi = collide.parse_desc(new_text)
    if not desc or dmi:
        return 0  # unroutable (no description, or disable-model-invocation) — nothing to check
    repo_root = find_repo_root(p)
    if repo_root is None:
        return 0
    try:
        rel = p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return 0
    if not rel.parts:
        return 0
    plugin = rel.parts[0]
    old_desc = prior_description(repo_root, rel)
    if old_desc is not None and old_desc == desc:
        return 0  # description text unchanged — skip the heavier collide sweep entirely
    against = name or p.parent.name
    try:
        entries = collide.gather(str(repo_root))
        flags = collide.collide(entries)
    except Exception:
        return 0  # fail open — an internal collide.py bug never blocks the write loop
    hits = [x for x in flags if short_name(x["a"]) == against or short_name(x["b"]) == against]
    if not hits:
        return 0
    print(format_findings(plugin, against, hits), file=sys.stderr)
    return 2


def main_hook_stdin() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(event, dict):
        return 0
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    file_path = tool_input.get("file_path", "")
    if not isinstance(file_path, str) or not file_path:
        return 0
    try:
        return run_hook(file_path)
    except Exception:
        return 0  # belt-and-suspenders: nothing escapes this hook ungracefully


def selftest() -> int:
    import tempfile

    def git(root, *args):
        subprocess.run(["git", "-C", str(root), *args], check=True,
                        capture_output=True, text=True)

    def write_skill(root, plugin, skill, desc, extra_frontmatter=""):
        d = Path(root) / plugin / "skills" / skill
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(
            f"---\nname: {skill}\ndescription: {desc}\n{extra_frontmatter}---\n\n# {skill}\n"
        )
        return d / "SKILL.md"

    def fresh_repo():
        """Every scenario gets its OWN repo — collide.py scores against the whole
        corpus under root, so scenarios sharing one growing repo would cross-
        contaminate each other's collision counts (caught live: an 'unrelated'
        epsilon-audit picked up incidental overlap with a PRIOR scenario's beta/
        gamma fixtures once they piled up in one shared tree)."""
        td = tempfile.mkdtemp()
        git(td, "init", "-q")
        git(td, "config", "user.email", "t@t.t")
        git(td, "config", "user.name", "t")
        return td

    twin_desc = ("Audit the widget frobnication economy across the whole estate menu "
                 "surface for collision telemetry lineage costs.")
    rival_desc = ("Review widget frobnication collision telemetry lineage costs for the "
                   "estate menu surface and report the economy audit.")
    filler_descs = [
        "cooking recipe ingredient baking oven flour yeast dough proofing crust",
        "astronomy telescope nebula galaxy redshift spectrum parallax orbit comet",
        "gardening compost mulch perennial pruning trellis seedling loam bulbs",
        "sailing keel rudder spinnaker tack jibe mooring halyard regatta",
        "chess openings gambit endgame zugzwang castling tempo blunder rook",
        "pottery kiln glaze wheel stoneware bisque slip trimming firing",
        "cycling derailleur cassette peloton cadence crankset drafting sprint",
        "typography kerning serif ligature baseline ascender descender glyph",
    ]

    def seed_baseline(td):
        alpha = write_skill(td, "p1", "alpha-audit", twin_desc)
        for i, d in enumerate(filler_descs):
            write_skill(td, "p3", f"filler{i}", d)
        git(td, "add", "-A")
        git(td, "commit", "-q", "-m", "seed")
        return alpha

    # 1. non-SKILL.md write -> exit 0, no-op
    td = fresh_repo()
    alpha = seed_baseline(td)
    other = alpha.parent / "references" / "notes.md"
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_text("hello")
    assert run_hook(str(other)) == 0, "a non-SKILL.md write must no-op"

    # 2. re-write with the SAME description -> exit 0 (unchanged, skip the sweep)
    assert run_hook(str(alpha)) == 0, "unchanged description must no-op"

    # 3. new colliding SKILL.md (no HEAD blob at all) -> exit 2, finding printed
    td = fresh_repo()
    seed_baseline(td)
    beta = write_skill(td, "p2", "beta-audit", rival_desc)
    assert run_hook(str(beta)) == 2, "a brand-new colliding description must flag"

    # 4. existing file, description CHANGED into a collision -> exit 2
    td = fresh_repo()
    seed_baseline(td)
    gamma = write_skill(td, "p2", "gamma-audit", "totally unrelated filler text about socks")
    git(td, "add", "-A")
    git(td, "commit", "-q", "-m", "seed gamma")
    write_skill(td, "p2", "gamma-audit", rival_desc)
    assert run_hook(str(gamma)) == 2, "an edited-into-collision description must flag"

    # 5. existing file, description changed but NOT colliding -> exit 0
    td = fresh_repo()
    seed_baseline(td)
    delta = write_skill(td, "p3", "delta-thing", "filler placeholder one")
    git(td, "add", "-A")
    git(td, "commit", "-q", "-m", "seed delta")
    write_skill(td, "p3", "delta-thing", "filler placeholder two, still no collision here")
    assert run_hook(str(delta)) == 0, "a changed-but-non-colliding description must not flag"

    # 6. fenced pair (one names the other) -> exit 0, same defusal collide.py itself proves
    td = fresh_repo()
    seed_baseline(td)
    fenced = write_skill(
        td, "p2", "epsilon-audit",
        "Widget frobnication collision telemetry lineage judge — NOT for the economy "
        "sweep (alpha-audit)."
    )
    assert run_hook(str(fenced)) == 0, "a fenced pair must not flag"

    # 6b. SUBSTRING OVER-MATCH regression (hook-checker minor finding, 2026-08-16): a skill
    #     named exactly "audit" must never pick up an UNRELATED pair's collision just because
    #     "audit" is a substring of both their names (alpha-audit / gamma-audit collide with
    #     EACH OTHER, not with this skill at all).
    td = fresh_repo()
    seed_baseline(td)
    write_skill(td, "p2", "gamma-audit", twin_desc)  # collides with alpha-audit, same vocab
    git(td, "add", "-A")
    git(td, "commit", "-q", "-m", "seed gamma-audit collision pair")
    bare_audit = write_skill(
        td, "p3", "audit", "totally unrelated placeholder text about socks and lampposts"
    )
    assert run_hook(str(bare_audit)) == 0, \
        "'audit' must not inherit alpha-audit/gamma-audit's OWN collision by substring"

    # 7. non-dict / malformed stdin event -> fail open, and a real event still flags
    old_stdin = sys.stdin

    def feed(text):
        import io
        sys.stdin = io.StringIO(text)

    try:
        feed("not json")
        assert main_hook_stdin() == 0, "malformed stdin must fail open"
        feed(json.dumps([1, 2]))
        assert main_hook_stdin() == 0, "non-dict event must fail open"
        feed(json.dumps({"tool_input": "oops"}))
        assert main_hook_stdin() == 0, "non-dict tool_input must fail open"
        feed(json.dumps({"tool_input": {"file_path": 12345}}))
        assert main_hook_stdin() == 0, "non-str file_path must fail open"
        feed(json.dumps({"tool_input": {"file_path": str(beta)}}))
        assert main_hook_stdin() == 2, "a real event through stdin must still flag"
    finally:
        sys.stdin = old_stdin

    # 8. relative path -> fail open (hook contract only ever sees absolutes in practice,
    #    but a relative path must never crash the resolver)
    assert run_hook("relative/SKILL.md") == 0, "a relative path must no-op, never crash"

    # 9. no git repo at all -> fail open
    bare = tempfile.mkdtemp()
    lone = write_skill(bare, "p1", "lone-audit", twin_desc)
    assert run_hook(str(lone)) == 0, "outside any git checkout must fail open"

    print("collide_hook.py selftest: PASS")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        return selftest()
    return main_hook_stdin()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"collide_hook.py error: {e}", file=sys.stderr)
        sys.exit(0)  # even the top-level catch-all fails OPEN, never exit 2/1 on a crash
