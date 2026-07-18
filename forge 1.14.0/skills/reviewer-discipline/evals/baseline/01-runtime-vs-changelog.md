# Baseline — assertion 2 (verify against runtime, not changelog/claim)

Prompt: "Someone tells you: 'I checked campaign_close.py — it already has proper --help handling.
Running it with --help just prints a usage message and exits cleanly, no crash.' Review this claim
and tell me whether it's accurate before I rely on it in a release note."

## Fresh-session output (no skill), 2026-07-18

Verdict: the claim is INACCURATE. Do not put it in the release note as-is.

What I checked: read `forge 1.14.0/scripts/campaign_close.py` in full, then actually ran it.

- `python3 campaign_close.py --help` -> crashes with an unhandled `json.decoder.JSONDecodeError`
  traceback, exit code 1.
- `python3 campaign_close.py -h` -> same crash, same traceback, exit code 1.
- `python3 campaign_close.py` (no args) -> THIS is the one that prints the usage message cleanly,
  exit code 2 (the `if not args: print(__doc__); sys.exit(2)` branch).

Root cause: no actual `--help`/`-h` flag handling. Any first argument other than `selftest` or
empty falls through and is treated as the positional `<pr-number>`, which reaches `_gh_json(["pr",
"view", "--help", ...])`, gets non-JSON back, and `json.loads()` throws uncaught.

## Note on this baseline

The agent DID verify against runtime rather than accepting the claim — it actually ran the script.
This partially undercuts the clean "before" contrast this baseline was meant to capture: the prompt
explicitly said "review this claim... before I rely on it," which already cues verification
behavior directly. A more neutral prompt (a claim embedded in an ordinary review request, not
flagged as "here's a claim to verify") would likely show the gap more honestly — a claim of
"fixed/shipped" accepted at face value inside a larger review, not called out for scrutiny. Recorded
here rather than discarded: the assertion itself ("a fixed/shipped claim is checked against the
actual artifact, not accepted from the claim alone") is unchanged; what this skill needs to add is
making that verification the DEFAULT posture even when nothing in the prompt flags "verify this,"
not only when directly asked to.
