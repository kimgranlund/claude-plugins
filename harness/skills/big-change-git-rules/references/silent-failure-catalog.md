# The silent-failure catalog — verify by re-reading, never by a command's print

The single doctrine every entry below instantiates: **a command's own stdout/exit-code report is
a CLAIM, not evidence.** The state it claims to have produced must be independently re-read
before the session proceeds as if the claim were true. Five real, dated instances of the same
mechanism, at five different layers (a shell pipe, a `str.replace` call, a git subcommand's own
quiet-success behavior, a hand-rolled argv parser, and git's own `status` under skip-worktree) —
proof this is a class, not a one-off. Count amended 2026-07-29: it read "three" while four entries
were already present, the fourth having landed without updating this line.

## A truncated pipe swallows a command's real exit state

[incident, 2026-07-17] `git pull ... | tail -1` on a checkout with foreign uncommitted work
ABORTED the pull silently — `git pull` refuses to run over unresolved local changes and prints a
multi-line error, but `tail -1` showed only its final, innocuous-looking line. The abort was
misread as success; the diagnosis that followed worked against stale pre-merge files for several
steps before the failure was traced back to the swallowed pipe. **The general form:** any
pipeline that filters a command's output for readability can also filter out the ONE line that
would have revealed failure. Never pipe a state-changing command's output through a filter that
could plausibly discard its error signal; if output must be trimmed, check the exit code
separately and unconditionally.

## A string-replace that silently matches nothing looks identical to success

[incident, 2026-07-16, two separate instances the same day — no shipped commit for either;
both were within-session authoring-time failures caught and corrected before commit, unlike
this file's other incidents which cite a landed SHA] Editing `release_gate.py`'s G8
allowlist via a `str.replace()`-shaped edit failed silently when the target string's indentation
didn't match exactly (12 vs. 13 spaces) — the call returned the original text unchanged, the
script reported "done," and the gate kept warning on the next run, discovered only because the
gate was re-run immediately after. The same failure class recurred hours later reconciling
docs' sibling-fence edits (`feature`/`file-bug` SKILL.md descriptions): two `str.replace`
calls printed success while matching nothing, and a git-merge-conflict cross-check (see
`parallel-session-reconcile.md`) initially diagnosed the WRONG cause before the actual gap was
found. **The fix pattern used successfully in both cases:** after any programmatic text edit,
assert the change by RE-READING the file from disk and checking the expected string is present —
never trust the edit call's own return value or the absence of an exception.

## A `git stash push` on a clean tree exits 0, claiming nothing happened when in fact NOTHING happened for a DIFFERENT reason than expected

[incident, 2026-07-17, caught pre-ship by a fresh-context audit of `sync_main.py`] `git stash
push -u -m <label>` exits 0 both when it genuinely creates a new stash AND when there is nothing
to stash ("No local changes to save"). A script that assumes "exit 0 → my stash exists" and then
blindly reads `git stash list`'s top entry can misattribute a FOREIGN, pre-existing stash to its
own run — reproduced live: a foreign stash already on top, `git stash push` reports "nothing to
save," and a naive script would report "quarantined your work" while pointing at someone else's
stash. Fixed in `sync_main.py` (forge 1.30.0, `ce05fcb`) with `verify_stash_created`: capture the
stash list's length and top-entry label BEFORE the push, and after, confirm the list grew by
exactly one AND the new top entry carries the expected label — the state is re-read and checked
against a specific, falsifiable expectation, not inferred from the push command's exit code.

## An unknown CLI flag is silently discarded and the script runs against the wrong target

[incident, 2026-07-21, Issue #74 — benign outcome only by luck] `sync_main.py` invoked with
`--repo-dir /path/to/target` (the real flag is `--repo-root`) silently ignored the unknown token
and ran its quarantine/pull sequence against cwd — which was a session worktree, not the intended
main checkout. The hand-rolled parser (`if "--repo-root" in args`) probes for known flags and
treats everything else as not-there; no usage error, no warning. The run failed harmlessly only
because the worktree's branch happened to be deleted remotely — against a live branch it would
have quarantined and pulled the wrong repo while reporting success. **The general form:** a
script's silent acceptance of your arguments is itself a CLAIM ("I understood the invocation");
a git-mutating script must reject unknown argv tokens loudly before touching state. Fixed same
day in `sync_main.py`'s strict `parse_cli` (harness 2.0.5, PR #86, closing Issue #74): any
unknown or malformed argv token exits with usage text before any git operation, selftest-proven.

## `git status` reports a clean tree while tracked files are absent from disk — skip-worktree hides the difference

[incident, 2026-07-29, `~/.claude`; the only entry here whose false claim came from git's own
STATUS report rather than from a mutating command] A sparse-checkout cone was set to
`plugins/marketplaces/.../packages/plugins` — a path that repo never tracked at all — so the cone
matched nothing and git set **skip-worktree** on every tracked file. skip-worktree instructs git
to treat the index as authoritative and stop comparing against disk, so for the whole affected
tree `git status` reported clean while the files were simply not there. Three whole skills
(`accounting-studio`, `port-zombie-sweep`, `session-review-artifact`) plus
`adhd-output/references/audit-report.md` were absent from disk and never once appeared as deleted. Two further symptoms compounded it: `git add <newfile>` in that
tree refused with a sparse-checkout advisory rather than staging (needing `--sparse`), and a
`UserPromptSubmit` hook broke because its `compact-contract.md` was among the missing files. The
cause was mis-diagnosed TWICE — first as "a stray `.zip` in the skills dir", then as "`/plugin
update` pruned them" — before `git ls-files -v | grep ^S` revealed the `S` flag. Worse, the
missing hook file was rebuilt by hand from conversation context when `git show
HEAD:<path>` had the original all along (the reconstruction happened to be byte-identical —
luck, not method). **The general form:** `git status`'s silence is a claim like any other, and
skip-worktree/sparse-checkout is the one configuration that makes it a lie *by design*. Before
concluding a tracked file was deleted — and always before reconstructing one — run `git ls-files
-v` for `S`/`h` flags and `git cat-file -e HEAD:<path>` to ask whether git still holds it. Fixed
by `git sparse-checkout disable` (verified first that no on-disk file differed from its indexed
copy, so materializing could clobber nothing).

## The general pattern, stated once

Every incident above has the same shape: **a git or shell operation reports success (exit 0, no
exception, clean stdout — or, in the skip-worktree case, a clean `status`) → state is not what the
report implies → session proceeds on the false premise.** The counter-pattern, applied identically
in every fix: capture the relevant state BEFORE the operation, perform the operation, capture the
state AFTER, and assert the delta matches what was actually intended — never the operation's own
self-report. The skip-worktree entry extends the doctrine one step: where no operation ran at all,
the *absence* of a reported difference is still a claim, and configuration can make it false.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| A diagnosis session works from stale data for several steps before catching the error | a pull/fetch aborted silently under a filtering pipe | never filter a state-changing command's output without checking its exit code separately |
| A gate keeps warning after an edit that "succeeded" | a `str.replace`/regex edit silently matched nothing (whitespace, quoting, or content drift from what was read) | re-read the file after every programmatic edit and assert the expected content is present |
| A script reports it quarantined/created/moved something that isn't actually there | the underlying command's "no-op success" case wasn't distinguished from its "real work done" case | capture before/after state and assert the specific expected delta, not just the exit code |
| A git-mutating script runs against the wrong repo while reporting success | a hand-rolled argv parser probed for known flags and silently discarded an unknown one (`--repo-dir` for `--repo-root`) | reject unknown argv tokens with usage text before touching state; never infer "understood" from "didn't complain" |
| Tracked files are missing from disk but `git status` says clean; `git add` refuses a new file in that tree | skip-worktree set on the whole tree (usually by a sparse-checkout cone that matches nothing) tells git to stop comparing index against disk | `git ls-files -v` and look for `S`/`h` flags; `git cat-file -e HEAD:<path>` before ever concluding a file is gone or rebuilding it by hand |
