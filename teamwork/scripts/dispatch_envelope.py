#!/usr/bin/env python3
"""dispatch_envelope — pre-compute a build dispatch's fixed setup, once, before the Agent call.

Usage:
  dispatch_envelope.py <ticket-id> [--plugin <name>] [--scratch-dir <path>]
  dispatch_envelope.py --help | -h
  dispatch_envelope.py selftest

Ticket #758 (2026-08-19, lever 2 of Kim's turnaround review): every `build-leader` dispatch
re-derives the same fixed setup from scratch — the version slot (`version_claim_check`-equivalent
+ an `origin/main` re-read), the decided branch name, `pin_check.py`, a scratch clone, and a
collision look — measured at 15-25% of total dispatch time, identical every time (#750: 58 min
builder time; #751: ~26 min resume). This is the DISPATCHER-side script (`mobilize-chores` step
5, `/build-feature`, a marshal dispatching `build-leader`) that runs ONCE before the `Agent` call
and hands the dispatched seat a JSON envelope it verifies by one re-read rather than re-deriving
(`dispatch-ticket` Phase 3's "envelope present" branch).

Emits (stdout, one JSON object):
  { "ticket": <id>, "kind": "<bug|feature|task|null>", "plugin": "<name-or-null>",
    "slot": {"current": "<main's version>", "next": "<slot to claim>",
              "claim_clean": <bool>, "checked_at": "<origin/main HEAD sha>"} | null,
    "branch": "<decided-branch-name>",
    "clone": "<abs path to a pre-made shallow scratch clone, branch already checked out>",
    "pin_check": "pass" | "fail",
    "collision": {"open_pr_branches": [...], "claimed_no_pr": [...]} }

Deliberately self-contained rather than shelling out to `harness/scripts/version_claim_check.py`
— a bundled script's own subprocess call hardcoding a path into a SIBLING plugin's scripts/ is
the same hard cross-plugin coupling `plugin-authoring.md`'s boundary rule already forbids for
preloads and `${CLAUDE_PLUGIN_ROOT}` paths; the small amount of duplicated version-collision logic
buys full plugin-boundary independence. `pin_check.py` is same-plugin (this file's own sibling in
`teamwork/scripts/`) and IS invoked directly.

Plugin inference: `--plugin` wins when given; absent, the `<plugin>: <rest>` ticket-title
convention (`teamwork:`, `harness:`, ...) is tried ONLY when the repo itself has a plugin-repo
layout — a `.claude-plugin/` directory at the git toplevel, the home of both a single-plugin
repo's `plugin.json` and a marketplace repo's `marketplace.json` (ticket #784: layout is a
property of the REPO, never of a ticket title — in agent-ui a `ui-rating: ...` prefix is a
component name, and inferring a plugin from it sent `gh api contents
ui-rating/.claude-plugin/plugin.json` into a 404, exit 2). In a non-plugin repo, or when the
title carries no prefix, `plugin` and `slot` both emit `null`, the plugin.json lookup is skipped
entirely, and the run still exits 0 — the builder decides, never a guess (branch, clone,
pin_check, and the collision look are all plugin-independent and still run).

Scratch-clone location (ticket #766): `--scratch-dir <path>` wins when given; absent, the
`CLAUDE_SCRATCHPAD` env var wins when set (this workspace's own session-scoped scratchpad,
the directory `repo-cleaner` already knows to sweep); absent both, the clone lands in the
current `$TMPDIR`/`tempfile.gettempdir()` default, unchanged from before this fix — so an
un-configured caller sees no behavior change at all.

Scratch-clone occupancy (ticket #784): a pre-existing destination never fails the run. A prior
aborted run's own clone — matching `origin` URL, clean working tree, the decided branch either
already current or not yet created — is REUSED as-is; anything else (a foreign directory, a
dirty tree, another remote, the branch parked non-current) is left untouched and a fresh unique
sibling directory is cut instead (`tempfile.mkdtemp`, the `mktemp -d` shape — never a delete,
since host permission walls can prevent even the CALLER cleaning `/var/folders` paths). The
envelope's `clone` field is always the directory actually used.

  E1 [FAIL->exit1] slot.claim_clean is false — a sibling open PR already claims this plugin's
            next version (the CLAIM race `version_claim_check.py` itself catches); envelope is
            still emitted in full, `next` advanced past every already-claimed version, so the
            dispatcher has real data to hand off a rebase-and-rebump instruction with
  E2 [FAIL->exit1] pin_check reports fail against the freshly-made clone (should not happen in
            the ordinary path — the clone was just cut from this branch — but a same-named branch
            already existing on the remote, fetched into the clone, would land here)
  E3 [FAIL->exit1] the decided branch name collides with an existing open PR's own head branch

`--help`/`-h` (ticket #766, first-use finding): exits 0 with this usage text, checked BEFORE
any argument parsing — the fix for a bare `--help` previously being read as the ticket-id
itself, reaching `gh issue view --help`, and crashing on the resulting non-JSON output. A
ticket-id that isn't a bare non-negative integer is likewise rejected before any `gh` call —
exit 2, never a network round-trip spent finding out.

Exit 0 clean envelope (incl. the plugin-unresolved null branch above, and `--help`/`-h`), 1 on
E1/E2/E3 (envelope still printed — the caller reads it for the actionable detail), 2 on a usage
error (a non-integer ticket-id, an unrecognized flag, a flag missing its value) or the envelope
couldn't be built at all (ticket unreadable, clone/git failure, no `gh` auth).

Network: `run()` calls `gh`/`git` live, same discipline as `version_claim_check.py`'s own
`_gh_json` and `merge_queue_watch.py`'s own docstring. `selftest` never touches the network or a
real GitHub remote — every pure helper (`infer_plugin`, `resolve_plugin`, `repo_layout_is_plugin`,
`decide_branch_name`, `version_tuple`, `compute_next_version`, `compute_slot`,
`find_claimed_no_pr`) is proven on fixtures, and the clone mechanics (`_do_clone`, incl. both
#784 occupancy regressions: reuse of a prior run's own clone, and a fresh unique dir beside a
foreign occupant) are proven against a REAL local git repo used as the "remote" (a `file://`
absolute path — no network), the same technique `pin_check.py`'s own selftest uses for its real
`git worktree add` proof.
"""
import json
import os
import re
import subprocess
import sys
import tempfile


PLUGIN_PREFIX_RE = re.compile(r"^([a-z][a-z0-9-]*):\s*")
_WORD_RE = re.compile(r"[a-z0-9]+")
_TICKET_ID_RE = re.compile(r"^\d+$")
HELP_FLAGS = ("--help", "-h")


def parse_args(args):
    """Returns (ticket_id, plugin, scratch_dir). Raises ValueError on any unrecognized token, a
    flag missing its value, or a ticket-id that isn't a bare non-negative integer (ticket #766 —
    the caller must never reach a `gh` call on a malformed id, `--help` included; that flag is
    intercepted by the caller BEFORE parse_args ever runs, so it never lands here at all) — the
    #188-class silent-argument-swallowing defect this house style always rejects rather than
    risks."""
    if not args:
        raise ValueError("ticket-id is required")
    ticket_id = args[0]
    if not _TICKET_ID_RE.match(ticket_id):
        raise ValueError(f"ticket-id must be a bare integer, got {ticket_id!r}")
    plugin = None
    scratch_dir = None
    i = 1
    while i < len(args):
        flag = args[i]
        if flag == "--plugin":
            if i + 1 >= len(args):
                raise ValueError("--plugin requires a value")
            plugin = args[i + 1]
            i += 2
        elif flag == "--scratch-dir":
            if i + 1 >= len(args):
                raise ValueError("--scratch-dir requires a value")
            scratch_dir = args[i + 1]
            i += 2
        else:
            raise ValueError(f"unrecognized argument: {flag!r}")
    return ticket_id, plugin, scratch_dir


def resolve_dest_root(scratch_dir_arg):
    """Pure: --scratch-dir wins when given; else CLAUDE_SCRATCHPAD when set; else today's
    $TMPDIR/tempfile.gettempdir() default, unchanged — ticket #766's clone-location fix."""
    if scratch_dir_arg:
        return scratch_dir_arg
    env = os.environ.get("CLAUDE_SCRATCHPAD")
    if env:
        return env
    return tempfile.gettempdir()


def infer_plugin(title):
    """Pure: this workspace's own '<plugin>: <rest>' ticket-title convention. None on no match —
    never guessed further than the literal prefix."""
    if not title:
        return None
    m = PLUGIN_PREFIX_RE.match(title.strip())
    return m.group(1) if m else None


def repo_layout_is_plugin(root):
    """Ticket #784: plugin-repo layout is a property of the REPO, decided by the repo's own
    toplevel — a `.claude-plugin/` directory there (the manifest home: `plugin.json` in a
    single-plugin repo, `marketplace.json` in a marketplace repo) — NEVER by a ticket-title
    prefix. An unknown/absent root reads as non-plugin: can't verify → never guess."""
    if not root:
        return False
    return os.path.isdir(os.path.join(root, ".claude-plugin"))


def resolve_plugin(plugin_arg, title, is_plugin_repo):
    """Pure (ticket #784): `--plugin` always wins; the '<plugin>: <rest>' title inference runs
    ONLY in a plugin-layout repo. In an ordinary repo a `ui-rating: ...`-style prefix is a
    component name, not a plugin — inferring one sent `gh api contents
    ui-rating/.claude-plugin/plugin.json` into a 404 on the 2026-08-19 agent-ui mobilize run."""
    if plugin_arg:
        return plugin_arg
    if not is_plugin_repo:
        return None
    return infer_plugin(title)


def slugify(title, max_words=4, max_chars=30):
    """Pure: a ticket title -> a short branch slug. Strips a leading 'plugin:' prefix and any
    trailing ' (...)' or ' -- ...'/' - ...' commentary, then keeps the first few meaningful
    words. Never empty — falls back to 'ticket'.

    Ticket #766: a slug over `max_chars` truncates at the LAST HYPHEN BOUNDARY under the cap,
    never mid-word — a naive `slug[:max_chars]` cut previously landed on fragments like
    'audit-gains-a' or '...-pre' (a half-eaten word); this drops the trailing partial word
    whole instead of slicing into it."""
    text = PLUGIN_PREFIX_RE.sub("", title.strip())
    text = re.split(r"\s+[—-]\s+|\s+\(", text, maxsplit=1)[0]
    words = _WORD_RE.findall(text.lower())
    slug = "-".join(words[:max_words])
    if len(slug) > max_chars:
        truncated = slug[:max_chars]
        last_hyphen = truncated.rfind("-")
        slug = truncated[:last_hyphen] if last_hyphen > 0 else truncated
    return slug or "ticket"


def decide_branch_name(ticket_id, title):
    """Pure: dispatch-ticket Phase 3's own issue-mapped '<id>-<short-slug>' convention."""
    return f"{ticket_id}-{slugify(title)}"


def version_tuple(v):
    """Pure: '2.28.11' -> (2, 28, 11). A non-numeric segment maps to -1 so a malformed version
    never silently outranks a well-formed one."""
    return tuple(int(seg) if seg.isdigit() else -1 for seg in v.split("."))


def compute_next_version(v):
    """Pure: bump the patch component. '2.28.11' -> '2.28.12'."""
    parts = v.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def compute_slot(main_version, open_claims):
    """Pure: open_claims is [{'number':.., 'version': '<claimed or None>'}, ...] — open PRs
    already touching this plugin's own manifest. Returns {'current', 'next', 'claim_clean'}
    (caller fills in 'checked_at' — that's the one impure fact, the sha this was read at).

    A taken slot never blocks the envelope — 'next' advances past every already-claimed version
    (not just main's +1), so the dispatcher has a real number to hand off a rebase-and-rebump
    instruction with rather than a number that would just collide again."""
    if not open_claims:
        return {"current": main_version, "next": compute_next_version(main_version),
                "claim_clean": True}
    highest = version_tuple(main_version)
    for c in open_claims:
        if c.get("version") and version_tuple(c["version"]) > highest:
            highest = version_tuple(c["version"])
    bumped = list(highest)
    bumped[-1] += 1
    next_version = ".".join(str(p) for p in bumped)
    return {"current": main_version, "next": next_version, "claim_clean": False}


def find_claimed_no_pr(open_issues, open_prs, exclude_number=None):
    """Pure: open_issues is [{'number':.., 'assignees': [...]}, ...]; open_prs is
    [{'number':.., 'body': '...'}, ...]. Returns the issue numbers that are claimed (an
    assignee present) but no open PR's body closes them (case-insensitive 'closes #<n>') — the
    #184 claimed-no-PR window, scanned once by the dispatcher instead of re-derived per build."""
    closed_by_pr = set()
    for pr in open_prs:
        for m in re.finditer(r"closes?\s+#(\d+)", pr.get("body") or "", re.IGNORECASE):
            closed_by_pr.add(int(m.group(1)))
    out = []
    for issue in open_issues:
        n = issue.get("number")
        if n == exclude_number:
            continue
        if issue.get("assignees") and n not in closed_by_pr:
            out.append(n)
    return out


def _run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {r.stderr.strip()}")
    return r


def _gh_json(args, repo=None):
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    r = _run(cmd)
    return json.loads(r.stdout)


def _resolve_repo():
    r = _run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
    return r.stdout.strip()


def _remote_url(repo):
    r = _run(["gh", "repo", "view", repo, "--json", "sshUrl", "-q", ".sshUrl"])
    return r.stdout.strip()


def _file_at_ref(repo, path, ref):
    r = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={ref}", "--jq", ".content"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh api contents {path}@{ref} failed: {r.stderr.strip()}")
    import base64
    return base64.b64decode(r.stdout.strip()).decode()


def _main_sha(repo):
    r = _run(["gh", "api", f"repos/{repo}/commits/main", "--jq", ".sha"])
    return r.stdout.strip()


def _git_toplevel():
    """Impure, local-only: the invoking checkout's own toplevel (`git rev-parse
    --show-toplevel`), the directory `repo_layout_is_plugin` reads. None outside a work tree —
    which downgrades layout detection to non-plugin rather than crashing (ticket #784)."""
    r = _run(["git", "rev-parse", "--show-toplevel"], check=False)
    if r.returncode != 0:
        return None
    top = r.stdout.strip()
    return top or None


def _reusable_clone(dest, remote_url, branch):
    """Impure, local-only (ticket #784): True iff an EXISTING dest is a prior run's own clone,
    safe to hand out again — a git work tree whose `origin` matches remote_url, whose working
    tree is clean, and whose decided branch is either already current (aborted after checkout,
    or resumed work — both correct to continue) or not yet created (aborted between clone and
    checkout). Anything else — a foreign directory, another remote, a dirty tree, the branch
    parked non-current (state this function can't safely reconcile) — is NOT reusable."""
    if not os.path.isdir(os.path.join(dest, ".git")):
        return False
    r = _run(["git", "remote", "get-url", "origin"], cwd=dest, check=False)
    if r.returncode != 0 or r.stdout.strip() != remote_url:
        return False
    r = _run(["git", "status", "--porcelain"], cwd=dest, check=False)
    if r.returncode != 0 or r.stdout.strip():
        return False
    r = _run(["git", "branch", "--show-current"], cwd=dest, check=False)
    if r.returncode != 0:
        return False
    if r.stdout.strip() == branch:
        return True
    r = _run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"],
             cwd=dest, check=False)
    return r.returncode != 0


def _do_clone(remote_url, dest, branch):
    """Impure but network-optional: `git clone --depth 1` + `checkout -b`, returning the
    directory ACTUALLY used. Ticket #784: a pre-existing dest never fails the run — a prior
    run's own clean clone is reused (branch checked out if the earlier run died between clone
    and checkout); any other occupant is left untouched and a fresh unique sibling is cut via
    `tempfile.mkdtemp` (never a delete — host permission walls can prevent even the caller
    cleaning these paths). Proven in selftest against a real local repo used as the remote (a
    file:// absolute path), so this function itself needs no network to verify.
    Ticket #927: `--depth 1` implies `--single-branch`, whose narrow fetch refspec
    (`+refs/heads/main:...`) makes a bare `gh pr create` in the clone fail with "you must
    first push" even after the branch IS pushed — so the refspec is widened right after the
    clone (and on reuse of a prior run's clone, which shares the defect)."""
    if os.path.exists(dest):
        if _reusable_clone(dest, remote_url, branch):
            _widen_fetch_refspec(dest)
            current = _run(["git", "branch", "--show-current"], cwd=dest).stdout.strip()
            if current != branch:
                _run(["git", "checkout", "-b", branch], cwd=dest)
            return dest
        parent = os.path.dirname(dest) or tempfile.gettempdir()
        dest = tempfile.mkdtemp(prefix=os.path.basename(dest) + "-", dir=parent)
    _run(["git", "clone", "--depth", "1", remote_url, dest])
    _widen_fetch_refspec(dest)
    _run(["git", "checkout", "-b", branch], cwd=dest)
    return dest


def _widen_fetch_refspec(dest):
    """Ticket #927: replace the single-branch fetch refspec a `--depth 1` clone gets with the
    full-remote form, so pushed branches are visible to `gh pr create` without --head/--base."""
    _run(["git", "config", "remote.origin.fetch",
          "+refs/heads/*:refs/remotes/origin/*"], cwd=dest)


def _pin_check(branch, cwd):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pin_check.py")
    r = subprocess.run([sys.executable, script, branch, "--cwd", cwd],
                        capture_output=True, text=True)
    return "pass" if r.returncode == 0 else "fail"


def run(ticket_id, plugin_arg=None, dest_root=None):
    repo = _resolve_repo()
    ticket = _gh_json(["issue", "view", ticket_id, "--json", "title,labels,number"], repo=repo)
    title = ticket.get("title", "")
    number = ticket.get("number")
    label_names = {lbl.get("name") for lbl in ticket.get("labels", [])}
    kind = next((k for k in ("bug", "feature", "task") if k in label_names), None)

    plugin = resolve_plugin(plugin_arg, title, repo_layout_is_plugin(_git_toplevel()))
    branch = decide_branch_name(ticket_id, title)

    findings = []

    slot = None
    if plugin:
        manifest_path = f"{plugin}/.claude-plugin/plugin.json"
        main_json = _file_at_ref(repo, manifest_path, "main")
        main_version = json.loads(main_json)["version"]
        checked_at = _main_sha(repo)
        prs = _gh_json(["pr", "list", "--state", "open", "--json",
                         "number,url,headRefName,files"], repo=repo)
        claiming = [pr for pr in prs
                    if manifest_path in {f.get("path") for f in pr.get("files", [])}]
        claims = []
        for pr in claiming:
            content = _file_at_ref(repo, manifest_path, pr["headRefName"])
            claims.append({"number": pr["number"],
                            "version": json.loads(content).get("version")})
        slot = compute_slot(main_version, claims)
        slot["checked_at"] = checked_at
        if not slot["claim_clean"]:
            findings.append("E1")
    else:
        prs = _gh_json(["pr", "list", "--state", "open", "--json",
                         "number,url,headRefName,files,body"], repo=repo)

    open_pr_branches = [pr["headRefName"] for pr in prs]
    if branch in open_pr_branches:
        findings.append("E3")

    open_issues = _gh_json(["issue", "list", "--state", "open", "--json",
                             "number,assignees"], repo=repo)
    prs_with_body = prs if any("body" in pr for pr in prs) else \
        _gh_json(["pr", "list", "--state", "open", "--json", "number,body"], repo=repo)
    claimed_no_pr = find_claimed_no_pr(open_issues, prs_with_body, exclude_number=number)

    dest_root = dest_root or resolve_dest_root(None)
    repo_name = repo.split("/")[-1]
    clone_dest = os.path.join(dest_root, f"{repo_name}-{ticket_id}")
    remote_url = _remote_url(repo)
    # #784: the returned path is the one actually used — a pre-existing dest is reused when it
    # is verifiably this run's own prior clone, else a fresh unique sibling is cut beside it.
    clone_dest = _do_clone(remote_url, clone_dest, branch)

    pin_result = _pin_check(branch, clone_dest)
    if pin_result == "fail":
        findings.append("E2")

    envelope = {
        "ticket": number,
        "kind": kind,
        "plugin": plugin,
        "slot": slot,
        "branch": branch,
        "clone": clone_dest,
        "pin_check": pin_result,
        "collision": {"open_pr_branches": open_pr_branches, "claimed_no_pr": claimed_no_pr},
    }
    print(json.dumps(envelope, indent=2))
    return 1 if findings else 0


def selftest():
    fails = 0

    # infer_plugin — the workspace's own '<plugin>: <rest>' convention, and the negative control
    if infer_plugin("teamwork: pre-computed dispatch envelope") != "teamwork":
        print("FAIL infer_plugin/match"); fails += 1
    else:
        print("ok    infer_plugin/match")
    if infer_plugin("a title with no plugin prefix at all") is not None:
        print("FAIL infer_plugin/none (no prefix must never be guessed)"); fails += 1
    else:
        print("ok    infer_plugin/none")

    # repo_layout_is_plugin — ticket #784: layout read from the REPO root, on real directories
    with tempfile.TemporaryDirectory() as tmp:
        plugin_root = os.path.join(tmp, "plugin-repo")
        os.makedirs(os.path.join(plugin_root, ".claude-plugin"))
        plain_root = os.path.join(tmp, "plain-repo")
        os.makedirs(plain_root)
        if not repo_layout_is_plugin(plugin_root):
            print("FAIL repo_layout_is_plugin/plugin (a root .claude-plugin/ dir must read as "
                  "plugin layout)")
            fails += 1
        else:
            print("ok    repo_layout_is_plugin/plugin (root .claude-plugin/ detected)")
        if repo_layout_is_plugin(plain_root):
            print("FAIL repo_layout_is_plugin/plain (no root .claude-plugin/ must read as "
                  "non-plugin)")
            fails += 1
        else:
            print("ok    repo_layout_is_plugin/plain")
    if repo_layout_is_plugin(None):
        print("FAIL repo_layout_is_plugin/unknown (unknown root must never guess plugin)")
        fails += 1
    else:
        print("ok    repo_layout_is_plugin/unknown (can't verify → non-plugin)")

    # resolve_plugin — ticket #784's own regression: a `word:` title prefix in a NON-plugin repo
    # (agent-ui's `ui-rating: ...`) must resolve to None, never to a phantom plugin lookup
    if resolve_plugin(None, "ui-rating: value renders stale on rerate", False) is not None:
        print("FAIL resolve_plugin/non_plugin_repo (a title prefix in a non-plugin repo must "
              "never be read as a plugin — the #784 agent-ui crash)")
        fails += 1
    else:
        print("ok    resolve_plugin/non_plugin_repo (ui-rating: prefix ignored outside a "
              "plugin-layout repo)")
    if resolve_plugin(None, "teamwork: some scripted fix", True) != "teamwork":
        print("FAIL resolve_plugin/plugin_repo (the title convention must still work in a "
              "plugin-layout repo)")
        fails += 1
    else:
        print("ok    resolve_plugin/plugin_repo (title convention intact where it belongs)")
    if resolve_plugin("harness", "ui-rating: whatever", False) != "harness":
        print("FAIL resolve_plugin/explicit_flag (--plugin must win regardless of layout)")
        fails += 1
    else:
        print("ok    resolve_plugin/explicit_flag (--plugin wins regardless of layout)")

    # slugify / decide_branch_name — drops the plugin prefix and trailing commentary
    got = decide_branch_name(
        "758", "teamwork: pre-computed dispatch envelope — slot, branch, scratch clone ready")
    if not got.startswith("758-pre-computed-dispatch-envelope"):
        print(f"FAIL decide_branch_name: {got!r}"); fails += 1
    else:
        print("ok    decide_branch_name (prefix stripped, commentary dropped)")
    if slugify("") != "ticket":
        print("FAIL slugify/empty (must never be empty)"); fails += 1
    else:
        print("ok    slugify/empty")

    # slugify — ticket #766's own negative control: a title whose plugin-stripped slug WOULD
    # truncate mid-word under a naive slug[:max_chars] cut must instead land on the last full
    # hyphen boundary under the cap
    got = slugify("othersystem: extraordinarily long branch slugname (extra commentary)")
    if got != "extraordinarily-long-branch":
        print(f"FAIL slugify/hyphen_boundary_truncation (must truncate at the last hyphen "
              f"boundary under the cap, never mid-word): {got!r}")
        fails += 1
    else:
        print("ok    slugify/hyphen_boundary_truncation (mid-word cut avoided, plugin prefix "
              "and commentary stripped)")

    # version_tuple / compute_next_version
    if version_tuple("2.28.11") != (2, 28, 11):
        print("FAIL version_tuple"); fails += 1
    else:
        print("ok    version_tuple")
    if compute_next_version("2.28.11") != "2.28.12":
        print("FAIL compute_next_version"); fails += 1
    else:
        print("ok    compute_next_version")

    # compute_slot — the reverse control: no open claims, clean slot, simple +1 bump
    slot = compute_slot("2.28.11", [])
    if slot != {"current": "2.28.11", "next": "2.28.12", "claim_clean": True}:
        print(f"FAIL compute_slot/clean: {slot}"); fails += 1
    else:
        print("ok    compute_slot/clean")

    # compute_slot — the negative control the acceptance criteria names explicitly: a taken slot
    # must report claim_clean:false, envelope still fully populated, 'next' advanced PAST the
    # taken claim (not a bare main+1, which would just collide again)
    slot = compute_slot("2.28.11", [{"number": 757, "version": "2.28.12"}])
    if slot["claim_clean"] is not False or slot["next"] != "2.28.13":
        print(f"FAIL compute_slot/taken (must be claim_clean:false, next advanced past the "
              f"claim): {slot}")
        fails += 1
    else:
        print("ok    compute_slot/taken (claim_clean:false, next advanced past the claim)")

    # find_claimed_no_pr — an assigned issue with no closing open PR is caught; one WITH a
    # closing PR, and the excluded ticket itself, are both correctly left out
    issues = [{"number": 100, "assignees": [{"login": "kim"}]},
              {"number": 101, "assignees": [{"login": "kim"}]},
              {"number": 102, "assignees": []},
              {"number": 758, "assignees": [{"login": "kim"}]}]
    prs = [{"number": 1, "body": "Closes #101"}]
    got = find_claimed_no_pr(issues, prs, exclude_number=758)
    if got != [100]:
        print(f"FAIL find_claimed_no_pr: {got}"); fails += 1
    else:
        print("ok    find_claimed_no_pr (claimed+no-PR caught, PR-linked and self excluded)")

    # _do_clone + _pin_check — real local git, no network: a local repo stands in as "the
    # remote" via an absolute file path, same technique pin_check.py's own selftest uses
    with tempfile.TemporaryDirectory() as tmp:
        remote = os.path.join(tmp, "origin")
        os.makedirs(remote)
        _run(["git", "init", "-q"], cwd=remote)
        _run(["git", "config", "user.email", "t@example.com"], cwd=remote)
        _run(["git", "config", "user.name", "t"], cwd=remote)
        with open(os.path.join(remote, "f.txt"), "w") as f:
            f.write("x")
        _run(["git", "add", "."], cwd=remote)
        _run(["git", "commit", "-q", "-m", "init"], cwd=remote)
        _run(["git", "branch", "-M", "main"], cwd=remote)

        dest = os.path.join(tmp, "clone")
        try:
            got = _do_clone(remote, dest, "758-dispatch-envelope")
            r = _run(["git", "branch", "--show-current"], cwd=dest)
            if got != dest or r.stdout.strip() != "758-dispatch-envelope":
                print(f"FAIL _do_clone (wrong branch/path: {r.stdout.strip()!r}, {got!r})")
                fails += 1
            else:
                print("ok    _do_clone (real local clone, branch cut off main)")
            # ticket #927: the --depth-1 clone's narrow single-branch refspec must have been
            # widened, else a bare `gh pr create` in the clone can't see pushed branches
            r = _run(["git", "config", "remote.origin.fetch"], cwd=dest, check=False)
            if r.stdout.strip() != "+refs/heads/*:refs/remotes/origin/*":
                print(f"FAIL _do_clone/refspec (narrow fetch refspec survived — the #927 "
                      f"gh-pr-create failure: {r.stdout.strip()!r})")
                fails += 1
            else:
                print("ok    _do_clone/refspec (single-branch refspec widened, #927)")
        except RuntimeError as e:
            print(f"FAIL _do_clone (raised: {e})"); fails += 1

        # _do_clone — ticket #784 regression 1: the SAME dest again (a retry after an aborted
        # dispatch) must reuse the prior run's own clean clone, never fail on its existence
        try:
            got = _do_clone(remote, dest, "758-dispatch-envelope")
            r = _run(["git", "branch", "--show-current"], cwd=dest)
            if got != dest or r.stdout.strip() != "758-dispatch-envelope":
                print(f"FAIL _do_clone/reuse (expected the same clone back on its branch, got "
                      f"{got!r} on {r.stdout.strip()!r})")
                fails += 1
            else:
                print("ok    _do_clone/reuse (pre-existing own clone reused on retry, no crash)")
        except RuntimeError as e:
            print(f"FAIL _do_clone/reuse (raised on a pre-existing scratch clone — the #784 "
                  f"retry crash: {e})")
            fails += 1

        # _do_clone — ticket #784 regression 2: a FOREIGN occupant at dest (not a reusable
        # clone) is left untouched; a fresh unique sibling is cut and returned instead
        occupied = os.path.join(tmp, "occupied")
        os.makedirs(occupied)
        stray = os.path.join(occupied, "stray.txt")
        with open(stray, "w") as f:
            f.write("not a clone")
        try:
            got = _do_clone(remote, occupied, "758-dispatch-envelope")
            r = _run(["git", "branch", "--show-current"], cwd=got)
            if got == occupied or not got.startswith(os.path.join(tmp, "occupied-")):
                print(f"FAIL _do_clone/occupied (expected a fresh unique sibling dir, got "
                      f"{got!r})")
                fails += 1
            elif r.stdout.strip() != "758-dispatch-envelope":
                print(f"FAIL _do_clone/occupied (fresh clone on wrong branch: "
                      f"{r.stdout.strip()!r})")
                fails += 1
            elif not os.path.exists(stray):
                print("FAIL _do_clone/occupied (the foreign occupant must be left untouched, "
                      "never deleted)")
                fails += 1
            else:
                print("ok    _do_clone/occupied (foreign occupant untouched, fresh unique "
                      "sibling cloned and returned)")
        except RuntimeError as e:
            print(f"FAIL _do_clone/occupied (raised on an occupied dest — the #784 "
                  f"stale-dir crash: {e})")
            fails += 1

        pin_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pin_check.py")
        if os.path.exists(pin_script):
            result = _pin_check("758-dispatch-envelope", dest)
            if result != "pass":
                print(f"FAIL _pin_check/match (expected pass, got {result})"); fails += 1
            else:
                print("ok    _pin_check/match (sibling script, matching branch)")
            result = _pin_check("some-other-branch", dest)
            if result != "fail":
                print(f"FAIL _pin_check/mismatch (expected fail, got {result})"); fails += 1
            else:
                print("ok    _pin_check/mismatch")
        else:
            print("FAIL _pin_check (sibling pin_check.py not found next to this script)")
            fails += 1

    # parse_args — the #188-class negative control
    tid, plugin, scratch_dir = parse_args(["758", "--plugin", "teamwork"])
    if (tid, plugin, scratch_dir) != ("758", "teamwork", None):
        print("FAIL parse_args/full"); fails += 1
    else:
        print("ok    parse_args/full")
    tid, plugin, scratch_dir = parse_args(["758"])
    if (tid, plugin, scratch_dir) != ("758", None, None):
        print("FAIL parse_args/bare"); fails += 1
    else:
        print("ok    parse_args/bare")
    tid, plugin, scratch_dir = parse_args(["758", "--scratch-dir", "/tmp/somewhere"])
    if (tid, plugin, scratch_dir) != ("758", None, "/tmp/somewhere"):
        print("FAIL parse_args/scratch_dir"); fails += 1
    else:
        print("ok    parse_args/scratch_dir")
    try:
        parse_args(["758", "--bogus", "x"])
        print("FAIL parse_args/bogus (unrecognized flag must be rejected)"); fails += 1
    except ValueError as e:
        if "--bogus" not in str(e):
            print("FAIL parse_args/bogus (error must name the bad flag)"); fails += 1
        else:
            print("ok    parse_args/bogus")
    try:
        parse_args(["758", "--plugin"])
        print("FAIL parse_args/missing-value"); fails += 1
    except ValueError as e:
        if "--plugin" not in str(e):
            print("FAIL parse_args/missing-value (error must name the flag)"); fails += 1
        else:
            print("ok    parse_args/missing-value")
    try:
        parse_args(["758", "--scratch-dir"])
        print("FAIL parse_args/scratch_dir-missing-value"); fails += 1
    except ValueError as e:
        if "--scratch-dir" not in str(e):
            print("FAIL parse_args/scratch_dir-missing-value (error must name the flag)")
            fails += 1
        else:
            print("ok    parse_args/scratch_dir-missing-value")
    try:
        parse_args([])
        print("FAIL parse_args/empty"); fails += 1
    except ValueError:
        print("ok    parse_args/empty")

    # parse_args — ticket #766's own two first-use findings: a non-integer ticket-id must be
    # rejected before any gh call could ever be attempted, never silently swallowed
    try:
        parse_args(["abc"])
        print("FAIL parse_args/non_integer_ticket (a non-integer ticket-id must be rejected)")
        fails += 1
    except ValueError as e:
        if "bare integer" not in str(e):
            print("FAIL parse_args/non_integer_ticket (error must name the requirement)")
            fails += 1
        else:
            print("ok    parse_args/non_integer_ticket")

    # resolve_dest_root — --scratch-dir wins, then CLAUDE_SCRATCHPAD, then today's default
    if resolve_dest_root("/explicit/dir") != "/explicit/dir":
        print("FAIL resolve_dest_root/explicit"); fails += 1
    else:
        print("ok    resolve_dest_root/explicit (--scratch-dir wins)")
    old_env = os.environ.get("CLAUDE_SCRATCHPAD")
    try:
        with tempfile.TemporaryDirectory() as fake_scratchpad:
            os.environ["CLAUDE_SCRATCHPAD"] = fake_scratchpad
            if resolve_dest_root(None) != fake_scratchpad:
                print("FAIL resolve_dest_root/env (CLAUDE_SCRATCHPAD must win over the default)")
                fails += 1
            else:
                print("ok    resolve_dest_root/env (honors CLAUDE_SCRATCHPAD, a real tmp dir "
                      "standing in as the scratchpad)")
    finally:
        if old_env is None:
            os.environ.pop("CLAUDE_SCRATCHPAD", None)
        else:
            os.environ["CLAUDE_SCRATCHPAD"] = old_env
    os.environ.pop("CLAUDE_SCRATCHPAD", None)
    if resolve_dest_root(None) != tempfile.gettempdir():
        print("FAIL resolve_dest_root/default (neither flag nor env set must keep today's "
              "$TMPDIR behavior)")
        fails += 1
    else:
        print("ok    resolve_dest_root/default (unchanged $TMPDIR behavior when unset)")

    # --help / -h — end-to-end against the real script file: must exit 0 with usage text,
    # checked BEFORE argument parsing so it can never reach a `gh` call (the original crash:
    # `--help` read as the ticket-id, `gh issue view --help` returning non-JSON)
    script_path = os.path.abspath(__file__)
    for flag in HELP_FLAGS:
        r = subprocess.run([sys.executable, script_path, flag],
                            capture_output=True, text=True, timeout=10)
        if r.returncode != 0 or "Usage" not in r.stdout:
            print(f"FAIL help/{flag} (expected exit 0 + usage text, got rc={r.returncode})")
            fails += 1
        else:
            print(f"ok    help/{flag} (exit 0, usage text printed, never reaches a gh call)")

    # non-integer ticket-id, end-to-end: exit 2, never a gh call
    r = subprocess.run([sys.executable, script_path, "abc"],
                        capture_output=True, text=True, timeout=10)
    if r.returncode != 2 or "bare integer" not in r.stderr:
        print(f"FAIL non_integer_ticket/end_to_end (expected exit 2 naming the requirement, "
              f"got rc={r.returncode} stderr={r.stderr!r})")
        fails += 1
    else:
        print("ok    non_integer_ticket/end_to_end (exit 2, never reaches a gh call)")

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        return 1
    print("dispatch_envelope selftest · PASS · plugin inference + branch slug (incl. the "
          "hyphen-boundary truncation control), the #784 layout gate (repo-root .claude-plugin/ "
          "detection, title-prefix-in-a-non-plugin-repo resolves to None), the taken-slot "
          "negative control (claim_clean:false, next advanced past the claim), the "
          "claimed-no-PR scan, --help/non-integer-ticket-id guards, "
          "CLAUDE_SCRATCHPAD/--scratch-dir resolution, and a REAL local clone + sibling "
          "pin_check.py wiring — incl. the #784 occupancy pair (own-clone reuse on retry, "
          "fresh unique sibling beside a foreign occupant) — all proved with no network")
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(2)
    if argv[0] in HELP_FLAGS:
        # ticket #766: checked BEFORE parse_args ever runs, so `--help` can never be read as a
        # ticket-id and reach a `gh` call — exit 0, never 2, since asking for usage isn't an error.
        print(__doc__)
        sys.exit(0)
    if argv[0] == "selftest":
        sys.exit(selftest())
    try:
        ticket_id, plugin, scratch_dir_arg = parse_args(argv)
    except ValueError as e:
        print(f"dispatch_envelope: {e}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(run(ticket_id, plugin, dest_root=resolve_dest_root(scratch_dir_arg)))
    except RuntimeError as e:
        print(f"dispatch_envelope: {e}", file=sys.stderr)
        sys.exit(2)
