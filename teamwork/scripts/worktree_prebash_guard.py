#!/usr/bin/env python3
"""worktree-prebash-guard — flags a Bash command that cd's (or -C/--prefix's) out of a
worktree cwd into the PRIMARY checkout, or across into a SIBLING worktree, and then runs a
further command in the same call.

Repo-side mitigation for issue #139 (worktree -> primary direction): a dispatched worktree
seat ran `cd <primary-checkout> && node scripts/build/components.mjs` and the platform's
git-only worktree-isolation guard didn't bind it (it binds git commands, not arbitrary
compound commands that cd into the shared checkout). Extended for issue #198 (worktree ->
SIBLING worktree direction): a session pinned to worktree A writing into worktree B is the
same escape wearing a different target (field evidence from issue #189, external and
CLI-tracked; this ticket is the estate-side lever). Both directions are deliberately ASK,
never BLOCK (hook-writing-rules: judgment-shaped rules are wrong often and unoverridable
always as a hard block) — the hook flags for confirmation, it does not enforce isolation on
its own.

Detection is possible without any external knowledge of "the primary checkout path" or "the
sibling worktree names" because EnterWorktree worktrees always live IN-REPO at
<primary-root>/.claude/worktrees/<name> (this workspace's own convention, CLAUDE.md). The
primary root is therefore always a deterministic string-prefix of the worktree cwd handed to
every hook event — no config, no external lookup — and the session's OWN worktree name is
just the first path segment after that marker. Any OTHER first-segment name resolved by a
cd/-C/--prefix target under .claude/worktrees/ is a sibling escape by the same construction.

Known blind spots (disclosed, not silently papered over — identical for both directions):
  - Dynamic cd targets ($(...), `...`, $VAR) cannot be resolved without executing the
    shell — such segments are treated as unknown and pass silently (fail open, not fail
    closed: a hard block on an unprovable case is the judgment-in-a-hook antipattern).
  - Only `cd`, `-C`, and `--prefix` path-target forms are recognized; other path-bearing
    flags (`-w`, `--cwd`, tool-specific flags) are not scanned.
  - A bare `cd <target>` with no chained command in the same Bash call is out of scope for
    the cd-based check — the disclosed gap is specifically the COMPOUND escape (git-only
    guard already binds plain git commands cd'd into primary or a sibling).
  - No nested-subshell paren tracking; a `(cd /x && ...)` is scanned the same as a flat
    compound, which is usually right but not guaranteed for deeply nested forms.
  - A shell-wrapper string (`sh -c "cd ... && ..."`, `bash -c`, `zsh -c`) is a single opaque
    token to the segment splitter — its inner cd is not scanned and passes silently (the
    dynamic-target class: resolving it means executing the shell).
  - `pushd` and `command cd`/`builtin cd` ARE recognized (added 2026-08-11 after a live
    hook-checker probe found all three bypassing silently); `popd`/`dirs` stack tricks
    beyond the first pushd are not tracked.

Persisted worktree-identity pin (issue #363, #359's follow-up): the compound-cd check above
only catches an escape WITHIN one Bash call. #359's own headline pattern is a DIFFERENT call
arriving with a cwd that's already wrong — no cd anywhere in it, because the drift happened
between calls, not inside one. That needs state that survives across hook invocations, which
this script previously had none of (#359's own Findings verified it stateless).

Wiring decision (recorded, not guessed): the natural site would be a PostToolUse(EnterWorktree)
matcher writing the pin the moment a session enters a fresh worktree. `EnterWorktree` is a TOOL
name in this workspace's own tool contract (`big-change-git-rules/references/
worktree-mechanics.md`), not a documented top-level hook EVENT (hook-writing-rules' verified
event list: PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd,
UserPromptSubmit, PreCompact, Notification). A `PostToolUse` hook COULD in principle be
matcher-scoped to `"EnterWorktree"` the same way this file's own PreToolUse hook is already
matcher-scoped to `"Bash"` — but there is no verified precedent anywhere in this estate of a
PostToolUse hook actually firing for that specific tool, nor documentation of what fields its
tool_input/tool_response payload carries (worktree name? path? both?). Building a hook against
an unverified event/payload risks one that silently never fires — worse than none
(hook-writing-rules' own flaky-is-worse-than-none doctrine) — and this build has no way to
exercise `EnterWorktree` live to confirm it. The fallback the ticket names is taken instead:
**first-call pin-write inside this file's own PreToolUse(Bash) hook**, the one call site already
proven to fire reliably on every Bash call in a worktree, with a verified `cwd` field.

Persistence spot: the PreToolUse(Bash) event payload is verified (hook-writing-rules' Mechanics
section) to carry `session_id` alongside `cwd` — so the pin is keyed by session_id, one JSON file
per session, under `${CLAUDE_PLUGIN_DATA}/worktree-pins/<session_id>.json` (same
`CLAUDE_PLUGIN_DATA`-with-a-`~/.claude/plugins/data/teamwork` fallback pattern already proven in
this plugin's own `session_end_worktree_check.py`) — this survives across hook invocations of
one session (each call re-reads/re-writes the same file) but not across sessions (a fresh
session_id gets a fresh, empty pin file; nothing durable is shared cross-session by design).

Agent-scoped pin (issue #375, this ticket's own follow-up): the assumption above — one
session_id names one actor — breaks under this workspace's own multi-agent teams feature. A
coordinator dispatching several build agents in parallel, each in its OWN `EnterWorktree`
worktree, hands every one of them the SAME `session_id` (verified live, 2026-08-16, building
THIS fix: this build's own `env | grep CLAUDE_CODE_SESSION_ID` was identical across every
sibling seat named in the dispatching session, while each ran as a distinct OS process — and
this build's own `cwd`, reported per Bash call by the host, was independently observed to jump
between worktrees across *consecutive* calls with zero `cd` in any of them, a host-level
cwd-reporting race distinct from the session/agent-identity bug). Agent A's first Bash call
pins the shared file to A's worktree; Agent B's very next call — in B's OWN worktree, no cd
anywhere — reads that file, finds a "mismatch", and false-positives exactly the #359 pattern
this pin exists to catch, on a completely correct command (screenshot evidence, issue date). No
`CLAUDE_AGENT_ID` or equivalent platform-documented per-agent field exists on the PreToolUse
event JSON or in the hook subprocess's own environment (verified live in the same probe: swept
the full env for every `CLAUDE_`/`CMUX_`/`AI_AGENT` key). The one signal that DID differ between
sibling agent processes in that probe was the invoking Claude process's own PID (`CLAUDE_PID`,
mirrored by this host's `CMUX_CLAUDE_PID`) — stable for one agent's whole lifetime (unlike
`os.getpid()` of the hook's own short-lived subprocess, which changes every call), but disclosed
as host/wrapper-specific, not a documented cross-platform contract; an install without it
degrades to the old session-only keying, unchanged.

Two independent layers respond, matching the ticket's own "AND/OR" allowance: (1)
`resolve_agent_key()` folds a best-effort per-agent discriminator into the pin's file key so two
agents sharing a session_id get two separate pin files instead of one shared one — the direct
fix for the reported symptom, byte-identical to today's behavior when no discriminator is
available. (2) independently, and more load-bearing given the second live finding above —
`check_identity_pin` no longer ASKs on a no-escape-attempt call (no cd/pushd/-C/--prefix token
anywhere in the command) as long as the current cwd resolves to a syntactically valid worktree
name under this repo's own `.claude/worktrees/`: a command that never tried to go anywhere,
sitting in a real worktree of this repo, isn't evidence of drift — it self-heals the pin
silently instead of asking. The compound-cd/-C escape detection (`analyze_command`, above) is
completely untouched by either layer: a genuine cd-then-write into the primary checkout or a
sibling still asks exactly as before, pin or no pin.

Drift response and re-pin path: on the FIRST PreToolUse(Bash) call this session/agent, or
whenever no pin file exists yet, the pin is written silently (nothing to compare against yet) —
the `pin-write` fixture. On every later call, the pin is compared against the current call's own
worktree name; a match stays silent (`match-silent`). A mismatch WITH a cd/pushd token present in
the triggering command emits an ASK, reusing this file's existing message format/posture
(`mismatch-asks`). REVISED by issue #375: a mismatch with NO cd/pushd token anywhere in the
command — #359's own original headline case — no longer asks; see the "Agent-scoped pin (issue
#375)" section above for why (live evidence that this host's own cwd reporting can move between
consecutive same-agent calls with nothing in the command to explain it, making "no cd, cwd moved"
alone an unreliable signal — the carve-out narrows the ask to calls that at least contain a
cd/pushd token, even one that resolves entirely within the call's own reported worktree). Pin
invalidation is handled by self-healing: the very same call that
flags a mismatch ALSO rewrites the pin to the current worktree, so a LEGITIMATE worktree change
(the session genuinely finished one campaign and moved into another) asks exactly once, then goes
quiet for the new location on every subsequent call (`legitimate-repin`) — never permanently
poisoning the pin into asking forever for a state the session has already moved into. The ASK
message itself names this: "the pin has been updated to this worktree" — the reset path IS the
message, no separate re-pin command needed. This trades a false negative (a second, later drift
into the wrong tree right after a legitimate one goes unflagged until the state changes again)
for never nagging a legitimate re-pin on every subsequent write — deliberate, matching the
existing guard's ASK-once, not-BLOCK-forever posture.

Modes:
  worktree_prebash_guard.py --hook   PreToolUse(Bash) hook: reads event JSON on stdin;
                                      silent exit 0 unless a hit is found, then emits
                                      {"hookSpecificOutput": {"permissionDecision": "ask", ...}}
  worktree_prebash_guard.py selftest proves the detection logic on embedded fixtures
                                      (0 pass / 1 fail / 2 skip)
"""
import json
import os
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HOOK_NAME = "worktree-prebash-guard"

WORKTREE_MARKER = "/.claude/worktrees/"

# Persisted worktree-identity pin (issue #363) — one JSON file per session_id, under
# ${CLAUDE_PLUGIN_DATA} (fallback matches session_end_worktree_check.py's own precedent).
PIN_SUBDIR = "worktree-pins"

# Read-only carve-out (added 2026-08-15): a compound command whose ENTIRE tail after the
# escaping cd is provably read-only never needs a human's eyes — the actual risk this guard
# exists for is a WRITE landing outside the session's own worktree, not a read. Kept
# deliberately narrow and allowlist-shaped (fail toward still-asking, never toward silently
# passing something ambiguous): non-git commands here never touch the filesystem in a way
# that could escape the tree; git subcommands here are ones that never mutate a repo
# regardless of what flags/args follow them. Notably excluded even though often safe:
# `git branch`, `git worktree`, `git remote`, `git config` — each has a real mutating form
# under the same subcommand name (`-d`, `add`, `set-url`, `user.name ...`), so arg-aware
# safety would be needed and isn't implemented; they still fall through to ASK.
# `log`/`diff`/`show` are deliberately EXCLUDED despite never mutating a git repo's history:
# all three share diff-formatting machinery that accepts `--output=<path>` (git >=2.19),
# which writes arbitrary content to an arbitrary filesystem path — a real write, same
# arg-aware-safety gap as `branch`/`worktree`/`remote`/`config` below, just less obvious
# (hook-checker critic finding, 2026-08-15: confirmed live against --hook, `git log
# --output=<path>` after an escaping cd passed completely silently — worse than pre-carve-out
# behavior, which at least always asked).
READ_ONLY_COMMANDS = {"pwd", "ls", "true"}
READ_ONLY_GIT_SUBCOMMANDS = {
    "status",
    "rev-parse",
    "ls-files",
    "describe",
}
# Any of these appearing as a standalone token means the segment writes somewhere or pipes
# into something unverifiable — disqualifies the read-only carve-out outright.
UNSAFE_TOKENS = {"|", ">", ">>", "<", "<<"}
# Raw-substring metacharacter rejection (second critic round, 2026-08-15): shell operators are
# NOT shlex words, so a token-equality check alone misses every attached form — `>/x`, `2>/x`,
# `&>/x`, `$(...)` or backticks inside an allowlisted command's args, process substitution
# `>(...)`, and a single `&` smuggling a second command into one segment (split_segments only
# splits on `&&`). Any of these characters appearing ANYWHERE in the segment disqualifies the
# carve-out before tokenizing. Over-asks on quoted literals containing them — exactly the
# stated fail-toward-asking posture. UNSAFE_TOKENS above stays as belt-and-braces.
UNSAFE_SUBSTRING_CHARS = "|&<>`$"


def find_primary_root(cwd):
    """Return the primary checkout root if cwd is inside <root>/.claude/worktrees/..., else None."""
    if not cwd or WORKTREE_MARKER not in cwd:
        return None
    root = cwd.split(WORKTREE_MARKER, 1)[0]
    return root or None


def find_own_worktree_name(cwd):
    """Return this session's own worktree name (first path segment after the marker), else None."""
    if not cwd or WORKTREE_MARKER not in cwd:
        return None
    remainder = cwd.split(WORKTREE_MARKER, 1)[1]
    return remainder.split("/", 1)[0] if remainder else None


def resolve_agent_key():
    """Best-effort per-agent discriminator, for folding into the pin key alongside session_id.

    No platform-documented per-agent field exists (verified live, issue #375: swept the full
    hook-subprocess environment on this host, found no `CLAUDE_AGENT_ID` or equivalent). Checked
    in order of how likely a future harness version is to set it deliberately, down to what THIS
    host actually provides today: `CLAUDE_AGENT_ID` (aspirational — not currently set anywhere
    observed, kept first so a future host that adds it needs no code change here), then
    `CLAUDE_PID` / `CMUX_CLAUDE_PID` (verified live on this host: the invoking Claude process's
    own PID, stable for one agent's whole lifetime, distinct between sibling agent processes in a
    parallel dispatch — NOT `os.getpid()`, which would be this short-lived hook subprocess's own
    PID and differ on every single call). Returns None when nothing is found — the pin then keys
    on session_id alone, identical to pre-#375 behavior (the disclosed no-discriminator fallback).
    """
    for var in ("CLAUDE_AGENT_ID", "CLAUDE_PID", "CMUX_CLAUDE_PID"):
        val = os.environ.get(var)
        if val:
            return val
    return None


def pin_key_for(session_id, agent_key):
    """Compose the pin's identity key. Falls back to bare session_id when agent_key is absent —
    byte-identical to pre-#375 pin filenames for any install without a resolvable discriminator."""
    if not session_id:
        return session_id
    return f"{session_id}__{agent_key}" if agent_key else session_id


def has_cd_or_flag_target(command):
    """True if this command contains any cd/pushd token at all, regardless of whether it
    resolves or escapes anywhere. Used only to gate the no-escape-attempt auto-pass below — a
    command that never tries to go anywhere is not evidence of drift.

    Deliberately checks cd/pushd only, NOT -C/--prefix (hook-checker finding, 2026-08-16): a
    genuine -C/--prefix escape is already independently caught by analyze_command's own
    flag-based hits regardless of this carve-out (run_hook asks whenever `hits` is non-empty,
    pin or no pin) — so gating the carve-out on -C too would buy nothing there, while it WOULD
    reintroduce host-level noise for the common non-path use of `-C` (e.g. `rg -C 3 foo`,
    `grep -C2`, `diff -C 5` — a numeric context-line flag scan_path_flags can't tell apart from a
    real path target without resolving it, and resolving a bare "3" always lands inside the
    caller's own cwd anyway, never a real escape)."""
    return any(parse_cd_target(segment) is not None for segment in split_segments(command))


def resolve_data_dir():
    """${CLAUDE_PLUGIN_DATA}, falling back to a fixed dir when unset — same pattern already
    proven in this plugin's session_end_worktree_check.py (the unset-env-var incident, #262-era
    fix disclosed in that script's own header)."""
    default_dir = os.path.expanduser(os.path.join("~", ".claude", "plugins", "data", "teamwork"))
    return os.environ.get("CLAUDE_PLUGIN_DATA", default_dir)


def pin_file_path(data_dir, session_id):
    """Path for one session's pin file. Sanitized so a hostile/malformed session_id can't
    escape PIN_SUBDIR via path traversal. Disclosed limitation (hook-checker nit, 2026-08-16):
    the sanitizer maps every non-alnum/-/_ char to '_', so two distinct session_ids differing
    only in punctuation (e.g. "a.b" and "a/b") collide onto the same pin file — harmless in
    practice (a real session_id is a platform-issued opaque token, not adversarially chosen to
    collide) but disclosed rather than silently assumed collision-free."""
    safe_id = "".join(c if (c.isalnum() or c in "-_") else "_" for c in (session_id or "unknown"))
    return os.path.join(data_dir, PIN_SUBDIR, f"{safe_id}.json")


def read_pin(data_dir, session_id):
    """Return the pin dict for this session, or None if absent/unreadable (never raises)."""
    path = pin_file_path(data_dir, session_id)
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def write_pin(data_dir, session_id, worktree_name):
    """Write (or overwrite) this session's pin. Atomic via a per-call unique tmp file (never a
    fixed name — two concurrent same-session writers must not race the same tmp path) +
    os.replace, so a hook racing a concurrent Bash call from the same session never observes a
    half-written file. NEVER RAISES: an unwritable data dir, full disk, or any other OSError
    fails open and silently, returning None — same disclosed posture as this file's other
    unprovable/exceptional paths (fresh-context hook-checker finding, 2026-08-16: an uncaught
    write error previously crashed the hook on EVERY subsequent Bash call once the dir was
    unwritable — worse than the guard doing nothing at all, hook-writing-rules' own
    flaky-is-worse-than-none doctrine)."""
    path = pin_file_path(data_dir, session_id)
    pin_dir = os.path.dirname(path)
    payload = {
        "worktree": worktree_name,
        "pinned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    tmp_path = None
    try:
        os.makedirs(pin_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=pin_dir, prefix=".pin-", suffix=".tmp")
        with os.fdopen(fd, "w") as f:
            json.dump(payload, f)
        os.replace(tmp_path, path)
    except OSError:
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return None
    return payload


def check_identity_pin(data_dir, session_id, cwd, agent_key=None, command=None):
    """Compare this call's own worktree identity against the session's persisted pin.

    `agent_key` (issue #375) folds a best-effort per-agent discriminator into the pin's file key
    so parallel agents sharing one session_id get separate pins instead of aliasing onto a
    single shared one — see resolve_agent_key(). `command`, when given, gates a second,
    independent carve-out: a call with no cd/pushd/-C/--prefix token anywhere in it never tried
    to go anywhere, so a "mismatch" against the pin isn't evidence of drift — it self-heals the
    pin silently instead of flagging (issue #375's ticket-endorsed alternative fix). Passing
    `command=None` (e.g. a caller that never has it) preserves the original always-compare
    behavior for that call.

    Returns None when there's nothing to flag: cwd isn't inside a worktree at all (out of this
    guard's scope, same as analyze_command's own applicability window), no session_id was on the
    event (can't key a pin — fails open, not closed), the first call this session/agent ever
    sees for a fresh worktree (pin-write, nothing yet to compare), the pin already matches
    (match-silent), or the no-escape-attempt carve-out applies. Returns {"pinned": <old>,
    "current": <new>} on a drift hit — and, as a side effect, self-heals the pin to <new> right
    then (see module docstring: the legitimate-repin path IS the ask-once-then-adopt behavior,
    not a separate re-pin command).
    """
    if find_primary_root(cwd) is None or not session_id:
        return None
    current_name = find_own_worktree_name(cwd)
    if current_name is None:
        return None
    pin_key = pin_key_for(session_id, agent_key)
    pin = read_pin(data_dir, pin_key)
    if pin is None:
        write_pin(data_dir, pin_key, current_name)
        return None
    pinned_name = pin.get("worktree")
    if pinned_name == current_name:
        return None
    if command is not None and not has_cd_or_flag_target(command):
        write_pin(data_dir, pin_key, current_name)
        return None
    write_pin(data_dir, pin_key, current_name)
    return {"pinned": pinned_name, "current": current_name}


def worktree_name_of(path, worktrees_root):
    """Return the immediate child dir name under worktrees_root if path resolves inside it, else None.

    Comparing exact path segments (not a raw string prefix) is what keeps a name like
    `seat1` from false-positiving against a sibling `seat10` — the boundary this mirrors
    from find_primary_root's own prefix-boundary discipline (fixture3).
    """
    if path is None or worktrees_root is None:
        return None
    prefix = worktrees_root.rstrip("/") + "/"
    if not path.startswith(prefix):
        return None
    remainder = path[len(prefix) :]
    return remainder.split("/", 1)[0] if remainder else None


def split_segments(command):
    """Split a shell command into segments on unquoted &&, ||, ; and newlines."""
    segments = []
    buf = []
    quote = None
    i = 0
    n = len(command)
    while i < n:
        ch = command[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch in ("\n", ";"):
            segments.append("".join(buf))
            buf = []
            i += 1
            continue
        if command[i : i + 2] in ("&&", "||"):
            segments.append("".join(buf))
            buf = []
            i += 2
            continue
        buf.append(ch)
        i += 1
    segments.append("".join(buf))
    return [s.strip().lstrip("(").strip() for s in segments if s.strip().strip("()")]


def parse_cd_target(segment):
    """Return the raw cd/pushd argument for a `cd ...`/`pushd ...` segment, '~' for bare cd, else None."""
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None
    if not tokens:
        return None
    # `command cd ...` / `builtin cd ...` are the same escape wearing a prefix
    if tokens[0] in ("command", "builtin") and len(tokens) > 1:
        tokens = tokens[1:]
    if tokens[0] not in ("cd", "pushd"):
        return None
    return tokens[1] if len(tokens) > 1 else "~"


def scan_path_flags(segment):
    """Return raw path arguments following -C or --prefix in this segment."""
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return []
    targets = []
    for i, tok in enumerate(tokens):
        if tok in ("-C", "--prefix") and i + 1 < len(tokens):
            targets.append(tokens[i + 1])
    return targets


def is_read_only_segment(segment):
    """True only if this single segment is unambiguously non-mutating (see carve-out note above)."""
    # Raw-substring check FIRST — shell operators aren't shlex words, so attached forms
    # (`>/x`, `2>/x`, `$(...)`, `` ` ``, `>(...)`, a lone `&`) never surface as equal tokens.
    if any(ch in segment for ch in UNSAFE_SUBSTRING_CHARS):
        return False
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return False
    if not tokens:
        return False
    if any(tok in UNSAFE_TOKENS for tok in tokens):
        return False
    if tokens[0] in READ_ONLY_COMMANDS:
        return True
    if tokens[0] == "git" and len(tokens) > 1 and tokens[1] in READ_ONLY_GIT_SUBCOMMANDS:
        return True
    return False


def is_read_only_tail(segments):
    """True only if EVERY segment in the tail is individually read-only (empty tail: True)."""
    return all(is_read_only_segment(s) for s in segments)


def resolve_target(target, current_dir):
    """Resolve a cd/-C target to an absolute path, or None if it can't be resolved statically."""
    if target is None or current_dir is None:
        return None
    if "$" in target or "`" in target:
        return None  # dynamic — cannot resolve without executing the shell
    expanded = os.path.expanduser(target)
    if os.path.isabs(expanded):
        return os.path.normpath(expanded)
    return os.path.normpath(os.path.join(current_dir, expanded))


def is_within(path, root):
    if path is None or root is None:
        return False
    return path == root or path.startswith(root.rstrip("/") + "/")


def analyze_command(command, cwd):
    """Return a list of (kind, resolved_path, segment) hits, or [] if not applicable / no hit.

    kind is "cd"/"flag" for a worktree -> PRIMARY-checkout escape (issue #139), or
    "cd-sibling"/"flag-sibling" for a worktree -> SIBLING-worktree escape (issue #198) —
    the same construction, just compared against a different other-worktree name instead
    of the primary root.
    """
    primary_root = find_primary_root(cwd)
    if primary_root is None:
        return []
    worktrees_root = os.path.join(primary_root, ".claude", "worktrees")
    own_name = find_own_worktree_name(cwd)

    segments = split_segments(command)
    hits = []
    current_dir = cwd
    for i, seg in enumerate(segments):
        cd_target = parse_cd_target(seg)
        if cd_target is not None:
            resolved = resolve_target(cd_target, current_dir)
            if resolved is None:
                current_dir = None  # unknown from here on — stay quiet, don't guess
                continue
            current_dir = resolved
            escapes_primary = is_within(resolved, primary_root) and not is_within(resolved, worktrees_root)
            sibling_name = worktree_name_of(resolved, worktrees_root)
            escapes_sibling = sibling_name is not None and sibling_name != own_name
            has_follow_on = i < len(segments) - 1
            tail_is_read_only = has_follow_on and is_read_only_tail(segments[i + 1 :])
            if escapes_primary and has_follow_on and not tail_is_read_only:
                hits.append(("cd", resolved, segments[i + 1]))
            if escapes_sibling and has_follow_on and not tail_is_read_only:
                hits.append(("cd-sibling", resolved, segments[i + 1]))
            continue
        for flag_target in scan_path_flags(seg):
            resolved = resolve_target(flag_target, current_dir or cwd)
            sibling_name = worktree_name_of(resolved, worktrees_root)
            if is_within(resolved, primary_root) and not is_within(resolved, worktrees_root):
                hits.append(("flag", resolved, seg))
            if sibling_name is not None and sibling_name != own_name:
                hits.append(("flag-sibling", resolved, seg))
    return hits


def format_reason(primary_root, own_name, hits, drift=None):
    """Build the ASK message. Sibling hits name BOTH worktrees — the session's own and the
    target sibling — not just a raw resolved path, so the reviewer sees exactly which two
    checkouts are involved without re-deriving it from the path. `drift` (optional) is a
    check_identity_pin() hit — the persisted-pin mismatch case (issue #363), appended as its
    own section so a hit that carries BOTH a compound-cd escape and a pin drift reports both in
    one ASK rather than one silently winning.
    """
    worktrees_root = os.path.join(primary_root, ".claude", "worktrees")
    header = "compound command reaches outside this session's own worktree" if hits else (
        "worktree-identity pin drift — this call's cd stayed in-tree, but the cwd moved anyway"
    )
    lines = [
        f"{HOOK_NAME} · {header}",
        f"primary checkout: {primary_root}",
        f"this session's worktree: {own_name or '(none — primary checkout)'}",
    ]
    for kind, resolved, seg in hits:
        via = "cd" if kind.startswith("cd") else "-C/--prefix"
        if kind.endswith("-sibling"):
            sibling = worktree_name_of(resolved, worktrees_root) or "?"
            lines.append(f"  via {via} -> sibling worktree '{sibling}' ({resolved}) · then: {seg.strip()}")
        else:
            lines.append(f"  via {via} -> primary checkout ({resolved}) · then: {seg.strip()}")
    if drift:
        lines.append(
            f"  pinned identity was '{drift['pinned']}', this call is running from "
            f"'{drift['current']}' — this call's own cd resolved inside '{drift['current']}', "
            "so the earlier move into it wasn't caught by anything in this command"
        )
        lines.append(
            "  pin updated to this worktree — if this was a deliberate Exit/EnterWorktree "
            "into a new tree, proceed and this won't ask again for it; if not, stop and check "
            "your cwd before writing."
        )
    lines.append("If intentional, proceed. If not, cd back into your own worktree checkout first.")
    return "\n".join(lines)


def run_hook():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed event: a flaky hook is worse than none — stay quiet
    if event.get("tool_name") != "Bash":
        return 0
    command = (event.get("tool_input") or {}).get("command", "")
    cwd = event.get("cwd") or ""
    if not command or not cwd:
        return 0

    primary_root = find_primary_root(cwd)
    own_name = find_own_worktree_name(cwd)
    hits = analyze_command(command, cwd)

    session_id = event.get("session_id")
    drift = check_identity_pin(
        resolve_data_dir(), session_id, cwd, agent_key=resolve_agent_key(), command=command
    )

    if not hits and not drift:
        return 0

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": format_reason(primary_root, own_name, hits, drift),
                }
            }
        )
    )
    return 0


def selftest():
    fails = 0

    def check(name, command, cwd, expect_hit):
        hits = analyze_command(command, cwd)
        got_hit = bool(hits)
        if got_hit != expect_hit:
            print(f"FAIL {name} (expected hit={expect_hit}, got={got_hit}, hits={hits})")
            return False
        print(f"ok    {name} (hit={got_hit})")
        return True

    cases = [
        # positive: the disclosed #139 pattern — compound cd into primary + mutating command
        (
            "fixture1_disclosed_pattern",
            "cd /repo && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # negative control: cd within the SAME worktree must never flag
        (
            "fixture2_in_worktree_cd",
            "cd /repo/.claude/worktrees/seat1/sub && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # boundary control: a sibling dir that string-prefixes primary_root must not false-positive
        (
            "fixture3_prefix_boundary",
            "cd /repo-backup && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # relative-path escape must resolve via normpath, not just literal string match
        (
            "fixture4_relative_escape",
            "cd ../.. && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # dynamic/unresolvable target: documented blind spot, must stay quiet (fail open)
        (
            "fixture5_dynamic_target",
            "cd $(git rev-parse --show-toplevel) && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # not a worktree session at all: guard is not applicable
        (
            "fixture6_primary_cwd_not_applicable",
            "cd /repo && node scripts/build/components.mjs",
            "/repo",
            False,
        ),
        # bare cd with no chained command: out of scope (compound-only per issue #139)
        (
            "fixture7_bare_cd_no_followon",
            "cd /repo",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # flag-based escape: git -C / make -C / npm --prefix targeting primary in one shot
        (
            "fixture8_dash_C_flag",
            "make -C /repo build",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # numeric -C (ripgrep context flag) must not false-positive against a path compare
        (
            "fixture9_dash_C_numeric_not_path",
            "rg -C 3 foo",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # pushd is cd wearing a stack (undisclosed bypass, hook-checker probe 2026-08-11)
        (
            "fixture10_pushd_escape",
            "pushd /repo && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # `command cd` prefix is the same escape wearing a builtin-bypass prefix (same probe)
        (
            "fixture11_command_cd_prefix",
            "command cd /repo && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # sh -c wrapping stays a DISCLOSED blind spot: inner cd is one opaque token (fail open)
        (
            "fixture12_sh_c_wrap_disclosed_blind",
            'sh -c "cd /repo && node scripts/build/components.mjs"',
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # sibling positive: issue #198 — seat1 cd's into seat2's tree and runs a follow-on
        (
            "fixture13_sibling_escape",
            "cd /repo/.claude/worktrees/seat2/sub && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # negative control: a relative cd that resolves back into the session's OWN
        # worktree must not false-positive the new sibling-comparison logic
        (
            "fixture14_relative_cd_stays_in_own_worktree",
            "cd ../seat1/sub && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # boundary control for the new direction: seat1 vs seat10 must not false-positive
        # (mirrors fixture3_prefix_boundary's discipline, one level down at the name segment)
        (
            "fixture15_sibling_prefix_boundary",
            "cd /repo/.claude/worktrees/seat10/sub && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,  # seat10 IS a real sibling of seat1 — this proves it still hits, just correctly
        ),
        # read-only carve-out (2026-08-15): the exact reported barrage pattern — build-lead's
        # routine primary-checkout status check — must NOT hit anymore.
        (
            "fixture18_readonly_carveout_pwd_git_status",
            "cd /repo && pwd && git status --short",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # regression guard: the ORIGINAL disclosed #139 pattern (a real mutation) must still hit —
        # the carve-out must never swallow a genuine write.
        (
            "fixture19_readonly_carveout_does_not_swallow_mutation",
            "cd /repo && git commit -am wip",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # partial safety is not enough: if ANY segment in the tail is not read-only, still hit —
        # proves the carve-out requires the WHOLE tail, not just the first follow-on.
        (
            "fixture20_readonly_carveout_requires_whole_tail",
            "cd /repo && git status && node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # redirection defeats the carve-out even though `git status` alone would qualify —
        # a write can hide behind an otherwise-safe command via `>`.
        (
            "fixture21_readonly_carveout_redirection_disqualifies",
            "cd /repo && git status > /repo/out.txt",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # the carve-out applies identically on the sibling-escape direction (#198).
        (
            "fixture22_readonly_carveout_applies_to_sibling",
            "cd /repo/.claude/worktrees/seat2 && git status --short",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
        # hook-checker critic finding (2026-08-15): git log/diff/show share diff-formatting
        # machinery that accepts `--output=<path>` — a real arbitrary-path write. Excluded
        # from the safe list entirely (same posture as branch/worktree/remote/config) rather
        # than special-cased, so a plain `git log`/`git diff`/`git show` still always asks.
        (
            "fixture23_readonly_carveout_excludes_diff_family",
            "cd /repo && git log --output=/repo/scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        (
            "fixture24_readonly_carveout_excludes_diff_family_plain",
            "cd /repo && git diff",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # Second critic round (code-checker, 2026-08-15): shell operators aren't shlex words,
        # so the token-equality check alone missed every ATTACHED form. Each probe class that
        # passed silently pre-fix gets its own fixture (fixtures 25-29), plus the stderr
        # attached form (30). All must hit via the raw-substring rejection.
        (
            "fixture25_attached_redirection",
            "cd /repo && git status >/repo/pwned.txt",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        (
            "fixture26_command_substitution_in_args",
            "cd /repo && git status $(rm -rf scripts)",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        (
            "fixture27_backtick_substitution_in_args",
            "cd /repo && ls `touch /repo/pwned`",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        (
            "fixture28_process_substitution",
            "cd /repo && ls >(tee /repo/pwned.txt)",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # a single `&` smuggles a second command into one segment — split_segments only
        # splits on `&&`, so `git status & node build.mjs` is ONE segment
        (
            "fixture29_single_ampersand_backgrounding",
            "cd /repo && git status & node scripts/build/components.mjs",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        (
            "fixture30_attached_stderr_redirection",
            "cd /repo && git status 2>/repo/err.txt",
            "/repo/.claude/worktrees/seat1",
            True,
        ),
        # negative control: the plain reported pattern must STILL pass silently after the
        # substring rejection (no metacharacters anywhere in its tail)
        (
            "fixture31_plain_readonly_still_passes",
            "cd /repo && pwd && git status --short && git rev-parse HEAD",
            "/repo/.claude/worktrees/seat1",
            False,
        ),
    ]
    for name, command, cwd, expect_hit in cases:
        if not check(name, command, cwd, expect_hit):
            fails += 1

    # fixture16: seat1 itself must NOT be mistaken for a sibling of seat10 (the actual
    # boundary bite — a naive string-prefix compare of "seat1" against "seat10" would
    # wrongly treat seat1's own cwd as outside itself; worktree_name_of's exact-segment
    # compare must return "seat1", matching own_name, so no hit)
    no_bite_hits = analyze_command(
        "cd /repo/.claude/worktrees/seat1/sub && node scripts/build/components.mjs",
        "/repo/.claude/worktrees/seat1",
    )
    if no_bite_hits:
        print(f"FAIL fixture16_own_name_not_shadowed_by_prefix (expected no hit, got {no_bite_hits})")
        fails += 1
    else:
        print("ok    fixture16_own_name_not_shadowed_by_prefix (hit=False)")

    # fixture17: the ASK message for a sibling hit must name BOTH worktrees by identifier,
    # not just a raw resolved path — mechanizes the "names both worktrees" requirement
    # instead of leaving it as an unverified prose claim
    reason = format_reason(
        "/repo",
        "seat1",
        [("cd-sibling", "/repo/.claude/worktrees/seat2/sub", "node scripts/build/components.mjs")],
    )
    if "seat1" in reason and "seat2" in reason:
        print("ok    fixture17_message_names_both_worktrees")
    else:
        print(f"FAIL fixture17_message_names_both_worktrees (reason={reason!r})")
        fails += 1

    # --- Persisted worktree-identity pin fixtures (issue #363, #359's follow-up) ---
    with tempfile.TemporaryDirectory() as pin_tmp:
        # fixture32: first call this session ever makes -- nothing to compare against yet,
        # so it must pin silently (no drift hit) and the pin file must actually land on disk.
        drift = check_identity_pin(pin_tmp, "sess-A", "/repo/.claude/worktrees/seat1")
        pinned = read_pin(pin_tmp, "sess-A")
        if drift is not None or pinned is None or pinned.get("worktree") != "seat1":
            print(f"FAIL fixture32_pin_write_first_call (drift={drift!r}, pinned={pinned!r})")
            fails += 1
        else:
            print("ok    fixture32_pin_write_first_call")

        # fixture33: same session, same worktree on a LATER call -- pin already matches,
        # must stay silent (match-silent).
        drift = check_identity_pin(pin_tmp, "sess-A", "/repo/.claude/worktrees/seat1")
        if drift is not None:
            print(f"FAIL fixture33_pin_match_silent (expected no hit, got {drift!r})")
            fails += 1
        else:
            print("ok    fixture33_pin_match_silent")

        # fixture34: same session, a LATER call arrives from a DIFFERENT worktree -- this is
        # the #359 headline pattern itself: no cd anywhere in this check (check_identity_pin
        # never inspects the command string at all), cwd is just already wrong. Must flag.
        drift = check_identity_pin(pin_tmp, "sess-A", "/repo/.claude/worktrees/seat2")
        if drift != {"pinned": "seat1", "current": "seat2"}:
            print(f"FAIL fixture34_pin_mismatch_asks (got {drift!r})")
            fails += 1
        else:
            print("ok    fixture34_pin_mismatch_asks")

        # fixture35: legitimate-repin path -- the very next call from that SAME new worktree
        # (seat2) must NOT re-ask; the mismatch above already self-healed the pin to seat2.
        # This is what keeps a genuine Exit/EnterWorktree move from permanently poisoning the
        # pin into asking on every subsequent write.
        drift = check_identity_pin(pin_tmp, "sess-A", "/repo/.claude/worktrees/seat2")
        if drift is not None:
            print(f"FAIL fixture35_pin_legitimate_repin (expected silence after repin, got {drift!r})")
            fails += 1
        else:
            print("ok    fixture35_pin_legitimate_repin")

        # fixture36: a DIFFERENT session_id gets its OWN pin, unaffected by sess-A's history
        # above -- proves the pin is keyed per-session, not global.
        drift = check_identity_pin(pin_tmp, "sess-B", "/repo/.claude/worktrees/seat9")
        if drift is not None:
            print(f"FAIL fixture36_pin_keyed_per_session (sess-B's first call should pin silently, got {drift!r})")
            fails += 1
        else:
            print("ok    fixture36_pin_keyed_per_session")

        # fixture37: no session_id on the event -- fails OPEN (can't key a pin without one),
        # never guessed. Matches this file's own disclosed-blind-spot posture elsewhere.
        drift = check_identity_pin(pin_tmp, None, "/repo/.claude/worktrees/seat1")
        if drift is not None:
            print(f"FAIL fixture37_pin_no_session_id_fails_open (expected None, got {drift!r})")
            fails += 1
        else:
            print("ok    fixture37_pin_no_session_id_fails_open")

        # fixture38: cwd not inside any worktree at all -- out of scope, same applicability
        # window as analyze_command's own primary_root check.
        drift = check_identity_pin(pin_tmp, "sess-C", "/repo")
        if drift is not None:
            print(f"FAIL fixture38_pin_not_applicable_outside_worktree (expected None, got {drift!r})")
            fails += 1
        else:
            print("ok    fixture38_pin_not_applicable_outside_worktree")

        # fixture39: the drift message names both the pinned and current worktree, and the
        # re-pin language, so a human reading the ASK sees the recovery path inline.
        reason = format_reason(
            "/repo", "seat2", [], drift={"pinned": "seat1", "current": "seat2"}
        )
        if "seat1" in reason and "seat2" in reason and "pin updated" in reason:
            print("ok    fixture39_drift_message_names_both_and_repin_path")
        else:
            print(f"FAIL fixture39_drift_message_names_both_and_repin_path (reason={reason!r})")
            fails += 1

    # fixture40 (revised for #375): end-to-end via the real --hook subprocess entrypoint. Two
    # separate Bash calls, same session_id, NO cd anywhere in either command -- the second
    # call's cwd is just already a different worktree with nothing in the command itself to
    # catch it. Pre-#375 this was the #359 headline pattern and had to ASK. Post-#375 it is
    # EXACTLY the reported false-positive (a parallel agent's correct, escape-free command in
    # its own worktree) -- the no-escape-attempt carve-out means it must now stay SILENT on
    # both calls instead.
    with tempfile.TemporaryDirectory() as hook_data_dir:
        script_path = os.path.abspath(__file__)
        env = dict(os.environ, CLAUDE_PLUGIN_DATA=hook_data_dir)
        for var in ("CLAUDE_AGENT_ID", "CLAUDE_PID", "CMUX_CLAUDE_PID"):
            env.pop(var, None)  # isolate this fixture from whatever agent runs the selftest

        def run_hook_subprocess(cwd, command, session_id="sess-e2e", extra_env=None):
            event = {
                "tool_name": "Bash",
                "tool_input": {"command": command},
                "cwd": cwd,
                "session_id": session_id,
            }
            call_env = dict(env, **(extra_env or {}))
            return subprocess.run(
                [sys.executable, script_path, "--hook"],
                input=json.dumps(event),
                capture_output=True,
                text=True,
                env=call_env,
                timeout=10,
            )

        first = run_hook_subprocess("/repo/.claude/worktrees/seat1", "npm test")
        second = run_hook_subprocess("/repo/.claude/worktrees/seat2", "npm test")
        first_silent = first.returncode == 0 and first.stdout.strip() == ""
        second_silent = second.returncode == 0 and second.stdout.strip() == ""
        if first_silent and second_silent:
            print("ok    fixture40_no_escape_attempt_stays_silent_across_worktrees_e2e")
        else:
            print(
                "FAIL fixture40_no_escape_attempt_stays_silent_across_worktrees_e2e "
                f"(first_rc={first.returncode!r} first_out={first.stdout!r} "
                f"second_rc={second.returncode!r} second_out={second.stdout!r})"
            )
            fails += 1

        # fixture42: a GENUINE escape -- a real compound cd into a sibling worktree with a
        # follow-on mutating command -- must still ASK. Proves the carve-out only swallows
        # no-escape-attempt calls; it never blinds analyze_command's own compound-cd detection,
        # pin or no pin.
        third = run_hook_subprocess(
            "/repo/.claude/worktrees/seat1",
            "cd /repo/.claude/worktrees/seat2 && npm test",
        )
        third_asks = third.returncode == 0 and '"permissionDecision": "ask"' in third.stdout
        if third_asks:
            print("ok    fixture42_genuine_cross_worktree_write_still_asks_e2e")
        else:
            print(
                "FAIL fixture42_genuine_cross_worktree_write_still_asks_e2e "
                f"(rc={third.returncode!r} out={third.stdout!r})"
            )
            fails += 1

        # fixture43 (the #375 regression itself): two agents sharing ONE session_id -- the
        # exact coordinator-with-parallel-build-agents shape -- each with its OWN CLAUDE_PID,
        # each in its OWN worktree, no cd in either command. Pre-#375 the second agent's call
        # false-positived against the first agent's pin (same session_id, shared file). Both
        # must now be silent, on the agent-scoped-pin mechanism alone (each gets its own pin
        # file via CLAUDE_PID) -- proven independent of the command-based carve-out by using a
        # command that DOES touch a cd token but stays inside the caller's own worktree, so the
        # carve-out above does not apply and only the agent-scoped key can save it.
        agent_a = run_hook_subprocess(
            "/repo/.claude/worktrees/seat1",
            "cd /repo/.claude/worktrees/seat1/sub && npm test",
            session_id="sess-shared",
            extra_env={"CLAUDE_PID": "1111"},
        )
        agent_b = run_hook_subprocess(
            "/repo/.claude/worktrees/seat2",
            "cd /repo/.claude/worktrees/seat2/sub && npm test",
            session_id="sess-shared",
            extra_env={"CLAUDE_PID": "2222"},
        )
        agent_a_silent = agent_a.returncode == 0 and agent_a.stdout.strip() == ""
        agent_b_silent = agent_b.returncode == 0 and agent_b.stdout.strip() == ""
        if agent_a_silent and agent_b_silent:
            print("ok    fixture43_parallel_agents_disjoint_worktrees_shared_session_both_pass_e2e")
        else:
            print(
                "FAIL fixture43_parallel_agents_disjoint_worktrees_shared_session_both_pass_e2e "
                f"(a_rc={agent_a.returncode!r} a_out={agent_a.stdout!r} "
                f"b_rc={agent_b.returncode!r} b_out={agent_b.stdout!r})"
            )
            fails += 1

        # fixture44: no-agent-id fallback still behaves like pre-#375 for the residual case the
        # carve-out does NOT cover -- a call that carries a cd/-C token but the cd stays wholly
        # WITHIN the (already-drifted) cwd's own tree, so analyze_command finds no escape hit of
        # its own, yet the pin still disagrees with where this call is actually running. No
        # agent discriminator is set (env stripped above), so this is the original
        # session-only pin, unchanged: first call pins seat9 with no cd (silent); second call,
        # same session, now genuinely running from seat3 with an in-tree-only cd -- the carve-out
        # doesn't apply (a cd token IS present) so the drift must still ask.
        fallback_first = run_hook_subprocess("/repo/.claude/worktrees/seat9", "npm test", session_id="sess-fallback")
        fallback_second = run_hook_subprocess(
            "/repo/.claude/worktrees/seat3",
            "cd sub && npm test",
            session_id="sess-fallback",
        )
        fallback_asks = fallback_second.returncode == 0 and '"permissionDecision": "ask"' in fallback_second.stdout
        if fallback_first.stdout.strip() == "" and fallback_asks:
            print("ok    fixture44_no_agent_id_fallback_unchanged_e2e")
        else:
            print(
                "FAIL fixture44_no_agent_id_fallback_unchanged_e2e "
                f"(first_out={fallback_first.stdout!r} second_out={fallback_second.stdout!r})"
            )
            fails += 1

    # fixture45: resolve_agent_key() precedence -- CLAUDE_AGENT_ID (aspirational, not currently
    # set by any observed host) wins over CLAUDE_PID/CMUX_CLAUDE_PID when both are present; each
    # of the three is individually picked up when it's the only one set; none set -> None (the
    # documented fallback path).
    orig_env = {
        k: os.environ.get(k) for k in ("CLAUDE_AGENT_ID", "CLAUDE_PID", "CMUX_CLAUDE_PID")
    }
    try:
        for k in orig_env:
            os.environ.pop(k, None)
        cases_45 = [
            ({}, None),
            ({"CMUX_CLAUDE_PID": "999"}, "999"),
            ({"CLAUDE_PID": "111"}, "111"),
            ({"CLAUDE_PID": "111", "CMUX_CLAUDE_PID": "999"}, "111"),
            ({"CLAUDE_AGENT_ID": "agent-x", "CLAUDE_PID": "111"}, "agent-x"),
        ]
        fixture45_ok = True
        for env_vars, expected in cases_45:
            for k in orig_env:
                os.environ.pop(k, None)
            os.environ.update(env_vars)
            got = resolve_agent_key()
            if got != expected:
                print(f"FAIL fixture45_agent_key_precedence (env={env_vars!r}, expected={expected!r}, got={got!r})")
                fixture45_ok = False
                fails += 1
        if fixture45_ok:
            print("ok    fixture45_agent_key_precedence")
    finally:
        for k, v in orig_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # fixture41: an unwritable data dir must fail OPEN, never crash the hook (hook-checker
    # Major, 2026-08-16 — live probe found write_pin's os.makedirs/open/os.replace raising
    # uncaught through check_identity_pin into run_hook, so an unwritable dir took the whole
    # guard down with rc=1 + a traceback on EVERY subsequent Bash call, worse than not having
    # the guard at all). Skipped, not falsely failed, when running as root (root ignores the
    # chmod below, so the write would actually succeed and the fixture couldn't prove anything).
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        print("skip  fixture41_unwritable_data_dir_fails_open (running as root — chmod is a no-op)")
    else:
        with tempfile.TemporaryDirectory() as ro_tmp:
            pins_dir = os.path.join(ro_tmp, PIN_SUBDIR)
            os.makedirs(pins_dir)
            os.chmod(pins_dir, 0o500)  # read+execute, no write
            try:
                result = write_pin(ro_tmp, "sess-ro", "seat1")
                drift = check_identity_pin(ro_tmp, "sess-ro", "/repo/.claude/worktrees/seat1")
                if result is not None or drift is not None:
                    print(
                        "FAIL fixture41_unwritable_data_dir_fails_open "
                        f"(expected None/None, got write_pin={result!r} drift={drift!r})"
                    )
                    fails += 1
                else:
                    print("ok    fixture41_unwritable_data_dir_fails_open")
            except OSError as e:
                print(f"FAIL fixture41_unwritable_data_dir_fails_open (raised {e!r} instead of failing open)")
                fails += 1
            finally:
                os.chmod(pins_dir, 0o700)  # restore write so TemporaryDirectory cleanup can remove it

    if fails:
        print(f"-- {fails} fixture(s) failed --")
        sys.exit(1)
    print("-- all fixtures passed --")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "--hook":
        sys.exit(run_hook())
    else:
        print(__doc__)
        sys.exit(2)
