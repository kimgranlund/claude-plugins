#!/usr/bin/env python3
"""alias_guard — a PreToolUse hook that catches a dispatch to a RETIRED name at runtime.

The static sweep (`fix_old_names.py`) fixes what it can see in files. This catches what it
cannot: a name the model composes at runtime, a name in a file outside the scan scope, a repo
nobody swept. Without it those fail SILENTLY — `subagent_type: "ops-issues"` errors with no hint
that the seat still exists under another name.

Usage (registered as a hook, reads the event on stdin):
  alias_guard.py --manifest <renames.json>     PreToolUse guard for Task | Skill
  alias_guard.py selftest                      prove the counters bite

Registration (in the CONSUMER repo's .claude/settings.json):
  {"hooks": {"PreToolUse": [{"matcher": "Task|Skill", "hooks": [{"type": "command",
    "command": "python3 <path>/alias_guard.py --manifest <path>/renames.json",
    "timeout": 10, "statusMessage": "retired-name-guard"}]}]}}

WHAT THIS CANNOT DO, and why it is shaped this way: a PreToolUse hook returns
allow | deny | ask — it cannot REWRITE the tool input [verified, hook-writing-rules, this
estate's hook contract]. So a retired name cannot be transparently resolved to its replacement;
the honest realizable form is to DENY and name the replacement, turning a silent failure into an
actionable one. The rejected alternative — a stub skill/agent per retired name, which WOULD
resolve transparently — costs resident listing budget per stub, and this estate has already
breached that budget four times (issues #76, #79, #80, #82) with far fewer than the 288 retired
names in the manifest.

Exit 0 always (a guard that crashes the session is worse than the stale name it guards against);
the verdict travels in the JSON on stdout.
"""
import json
import sys
from pathlib import Path


def build_lookup(manifest: dict):
    """old name -> list of (kind, new_plugin, new).

    The manifest's `match` field is load-bearing here, not decoration. Most CURRENT names in
    this estate were ALSO old names: a plugin-prefix-only rename (`forge:skill-checker` ->
    `harness:skill-checker`) leaves the bare name completely valid. Indexing those under the
    bare key denies live dispatches — a first cut of this function did exactly that, and the
    smoke test before registering the hook caught `skill-checker`, a real current agent, being
    refused with "use harness:skill-checker instead" (2026-07-26). A guard that denies working
    names is far worse than the silent failure it was built to replace.

    So: only `match == "token"` entries are reachable bare. Everything else must arrive
    qualified, where the old plugin prefix is what proves the reference is actually stale."""
    by_name = {}
    for e in manifest["renames"]:
        keys = [f'{e["old_plugin"]}:{e["old"]}']
        if e.get("match") == "token":
            keys.append(e["old"])
        for key in keys:
            by_name.setdefault(key, []).append((e["kind"], e["new_plugin"], e["new"]))
    return by_name


def dispatched_name(event: dict):
    """The name this event is about, and which kind the SLOT proves it is."""
    tool = event.get("tool_name", "")
    ti = event.get("tool_input") or {}
    if tool == "Task":
        return ti.get("subagent_type"), "agent"
    if tool == "Skill":
        return ti.get("skill"), "skill"
    return None, None


def verdict(event: dict, by_name: dict):
    """None = allow silently. Otherwise the deny reason."""
    name, kind = dispatched_name(event)
    if not name:
        return None
    hits = by_name.get(name)
    if not hits:
        return None
    # The slot proves the kind, so prefer the matching one; fall back to naming every candidate.
    typed = [h for h in hits if h[0] == kind]
    chosen = typed or hits
    opts = ", ".join(f"{p}:{n}" + ("" if typed else f" ({k})") for k, p, n in chosen)
    return (f"`{name}` is a RETIRED name — it was renamed and no longer resolves. "
            f"Use {opts} instead. "
            f"If this repo still has retired names in its files, run /fix-old-names to sweep them.")


def run(manifest_path: Path):
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0                      # a malformed event is not this guard's business
    try:
        by_name = build_lookup(json.loads(manifest_path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError):
        return 0                      # an unreadable manifest must never block a dispatch
    reason = verdict(event, by_name)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))
    return 0


FIXTURE = {
    "schema": "renames/v1",
    "plugins": {"forge": "harness"},
    "renames": [
        {"old": "ops-issues", "new": "sort-issues", "kind": "skill",
         "old_plugin": "forge", "new_plugin": "harness", "match": "token"},
        {"old": "ops-issues", "new": "issue-sorter", "kind": "agent",
         "old_plugin": "forge", "new_plugin": "harness", "match": "token"},
        {"old": "token-builder", "new": "token-builder", "kind": "agent",
         "old_plugin": "color", "new_plugin": "design", "match": "qualified"},
        # The identity class the first cut got wrong: a name that is BOTH a former old name and
        # a current live one. Without this row the fixture cannot see the bug (the original
        # fixture had no such entry, which is precisely why the selftest stayed green while the
        # real 288-entry manifest denied working dispatches).
        {"old": "skill-checker", "new": "skill-checker", "kind": "agent",
         "old_plugin": "forge", "new_plugin": "harness", "match": "qualified"},
    ],
}


def selftest():
    by = build_lookup(FIXTURE)

    # negative control — a retired AGENT dispatch must be denied, naming the agent replacement
    r = verdict({"tool_name": "Task", "tool_input": {"subagent_type": "ops-issues"}}, by)
    assert r and "harness:issue-sorter" in r, f"retired agent must deny with the seat name: {r}"
    assert "sort-issues" not in r, "the slot proves it is an agent — do not offer the command too"

    # ...and the SAME retired name via the Skill slot resolves to the command instead
    r2 = verdict({"tool_name": "Skill", "tool_input": {"skill": "ops-issues"}}, by)
    assert r2 and "harness:sort-issues" in r2, f"retired skill must deny with the command: {r2}"

    # qualified form, incl. the plugin-prefix-only class
    r3 = verdict({"tool_name": "Task", "tool_input": {"subagent_type": "color:token-builder"}}, by)
    assert r3 and "design:token-builder" in r3, f"prefix-only rename must deny: {r3}"

    # REVERSE control — a current name must pass silently, or the guard is a wall
    for good in ("issue-sorter", "code-checker", "builder"):
        assert verdict({"tool_name": "Task", "tool_input": {"subagent_type": good}}, by) is None, \
            f"a live name must never be denied: {good}"

    # THE NEAR-MISS CONTROL (2026-07-26): `skill-checker` is a current agent AND a former old
    # name under forge:. Bare, it must pass silently; qualified with the retired plugin, it must
    # still deny. Registering the hook with this backwards would have refused most dispatches in
    # the estate.
    assert verdict({"tool_name": "Task", "tool_input": {"subagent_type": "skill-checker"}}, by) is None, \
        "a CURRENT name that was also an old name must dispatch freely — the guard is not a wall"
    rq = verdict({"tool_name": "Task", "tool_input": {"subagent_type": "forge:skill-checker"}}, by)
    assert rq and "harness:skill-checker" in rq, \
        f"the same name QUALIFIED by the retired plugin is genuinely stale and must deny: {rq}"

    # unrelated tools are none of this guard's business
    assert verdict({"tool_name": "Bash", "tool_input": {"command": "ops-issues"}}, by) is None, \
        "only the dispatch slots are guarded — not every mention of a retired word"
    assert verdict({"tool_name": "Task", "tool_input": {}}, by) is None, "no name, no verdict"

    # an unreadable manifest must never block a dispatch (fail-open is the only safe default)
    import io
    saved = sys.stdin
    try:
        sys.stdin = io.StringIO(json.dumps(
            {"tool_name": "Task", "tool_input": {"subagent_type": "ops-issues"}}))
        assert run(Path("/nonexistent/renames.json")) == 0, "must exit 0 on a missing manifest"
    finally:
        sys.stdin = saved

    # REAL-MANIFEST control. The fixture above proves the rule; this proves the SHIPPED data
    # obeys it. Scoped to this plugin's own members, which always sit beside this script (a
    # sibling-plugin sweep would be flaky from an installed cache). Had this existed first, the
    # near-miss would have been caught by the gate rather than by a hand smoke test.
    root = Path(__file__).resolve().parent.parent
    mf = root / "renames.json"
    if mf.is_file():
        real = build_lookup(json.loads(mf.read_text(encoding="utf-8")))
        denied = []
        for a in sorted((root / "agents").glob("*.md")):
            if verdict({"tool_name": "Task", "tool_input": {"subagent_type": a.stem}}, real):
                denied.append(f"agent {a.stem}")
        for s in sorted((root / "skills").glob("*/SKILL.md")):
            if verdict({"tool_name": "Skill", "tool_input": {"skill": s.parent.name}}, real):
                denied.append(f"skill {s.parent.name}")
        assert not denied, ("the SHIPPED manifest denies currently-live names — this guard is "
                            f"registered globally and would block real dispatches: {denied}")
        checked = len(list((root / "agents").glob("*.md"))) + len(list((root / "skills").glob("*/SKILL.md")))
    else:
        checked = 0

    print("alias_guard selftest · PASS · retired dispatch denied with the replacement named, "
          "slot picks the right kind, prefix-only class caught, a CURRENT name that was also an "
          "old name dispatches freely (bare) yet denies when qualified by its retired plugin, "
          f"fail-open on a bad manifest, {checked} shipped names verified against the real manifest")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "--manifest" and len(args) > 1:
        sys.exit(run(Path(args[1])))
    print(__doc__)
    sys.exit(2)
