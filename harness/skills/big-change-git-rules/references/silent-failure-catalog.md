# The silent-failure catalog — verify by re-reading, never by a command's print

The single doctrine every entry below instantiates: **a command's own stdout/exit-code report is
a CLAIM, not evidence.** The state it claims to have produced must be independently re-read
before the session proceeds as if the claim were true. Three real, dated instances of the same
mechanism, at three different layers (a shell pipe, a `str.replace` call, and a git subcommand's
own quiet-success behavior) — proof this is a class, not a one-off.

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
a git-mutating script must reject unknown argv tokens loudly before touching state. Fix tracked
in Issue #74 (reject-unknown-args + selftest fixture); until it ships, re-read the script's own
banner line (`sync_main · <root>`) and verify the target it names is the one you meant.

## The general pattern, stated once

Every incident above has the same shape: **command reports success (exit 0, no exception, clean
stdout) → state did not change as expected → session proceeds on the false premise.** The
counter-pattern, applied identically in every fix: capture the relevant state BEFORE the
operation, perform the operation, capture the state AFTER, and assert the delta matches what was
actually intended — never the operation's own self-report.

## Failure catalog

| Symptom | Cause | Fix |
|---|---|---|
| A diagnosis session works from stale data for several steps before catching the error | a pull/fetch aborted silently under a filtering pipe | never filter a state-changing command's output without checking its exit code separately |
| A gate keeps warning after an edit that "succeeded" | a `str.replace`/regex edit silently matched nothing (whitespace, quoting, or content drift from what was read) | re-read the file after every programmatic edit and assert the expected content is present |
| A script reports it quarantined/created/moved something that isn't actually there | the underlying command's "no-op success" case wasn't distinguished from its "real work done" case | capture before/after state and assert the specific expected delta, not just the exit code |
