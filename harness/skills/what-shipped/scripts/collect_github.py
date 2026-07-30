#!/usr/bin/env python3
"""collect_github.py — GitHub PR + issue activity for a date window, bot noise separated.

Usage:
  collect_github.py [SINCE] [UNTIL]   SINCE/UNTIL are YYYY-MM-DD (UTC), inclusive;
                                      both default to today. Repo comes from the cwd's
                                      `gh repo view` unless WHAT_SHIPPED_REPO is set.
  collect_github.py selftest          prove the classifiers and guards on inline fixtures

Emits five TSV sections to stdout, each headed `## NAME (count)`:
  PR_MERGED · PR_OPENED · PR_OPEN_NOW · ISSUE_OPENED · ISSUE_CLOSED
plus a `## BOT_NOISE (...)` tally naming what was filtered, and — only when every
query succeeded — the `## OK — all queries succeeded` trailer. The trailer's ABSENCE
is the failure signal: a truncated run cannot print it, so an all-zero report and a
broken fetch can never look alike.

Bot separation reads `.author.type == "Bot"` (plus a `[bot]` login suffix), never
title patterns (they drift) and never `.author.is_bot` alone — `gh search` reports
is_bot FALSE for GitHub App authors even where `gh pr list` reports true for the
same PR (verified 2026-07-25, gh 2.x). `gh pr list` rows additionally honor is_bot.
This mechanic is mirrored in SKILL.md §Collect — an edit to either owes the other.

A result set that fills its --limit is truncated-or-exactly-full, and the two are
indistinguishable — saturation is a FAILURE (narrow the window), not a big day.

Exit: 0 report printed · 1 a gh query failed or saturated · 2 usage error.
Selftest: 0 proven · 1 a control failed.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

PR_SEARCH_LIMIT = 1000  # gh search's hard ceiling (REST search API max)
ISSUE_SEARCH_LIMIT = 500
OPEN_LIST_LIMIT = 100


def fail(msg):
    print(
        "\n## ERROR — collection FAILED; results are incomplete and must not be "
        "reported as a summary\n" + msg,
        file=sys.stderr,
    )
    sys.exit(1)


def is_bot(author, honor_is_bot=False):
    """author = {"login": ..., "type": ..., "is_bot": ...} (fields optional)."""
    if (author.get("type") or "") == "Bot":
        return True
    if (author.get("login") or "").endswith("[bot]"):
        return True
    if honor_is_bot and author.get("is_bot"):
        return True
    return False


def cap_guard(name, rows, limit):
    if len(rows) >= limit:
        fail(
            f"{name} returned {len(rows)} rows, saturating its limit {limit} — "
            "results may be truncated; narrow the window and re-run"
        )


def run_gh(args):
    try:
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        fail("gh not installed")
    except subprocess.TimeoutExpired:
        fail(f"gh timed out: gh {' '.join(args)}")
    if r.returncode != 0:
        fail(f"command failed: gh {' '.join(args)} :: {r.stderr.strip() or r.stdout.strip()}")
    try:
        return json.loads(r.stdout or "[]")
    except json.JSONDecodeError as e:
        fail(f"unparseable gh output for: gh {' '.join(args)} :: {e}")


def split_rows(rows, honor_is_bot=False):
    humans = [r for r in rows if not is_bot(r.get("author") or {}, honor_is_bot)]
    bots = [r for r in rows if is_bot(r.get("author") or {}, honor_is_bot)]
    return humans, bots


def emit(name, lines):
    print(f"## {name} ({len(lines)})")
    for ln in lines:
        print(ln)
    print()


def pr_line(r):
    return f"{r['number']}\t{(r.get('author') or {}).get('login', '?')}\t{r.get('title', '')}"


def issue_line(r):
    a = (r.get("author") or {}).get("login", "?")
    return f"{r['number']}\t{r.get('state', '?').lower()}\t{a}\t{r.get('title', '')}"


def open_line(r):
    state = "draft" if r.get("isDraft") else "ready"
    a = (r.get("author") or {}).get("login", "?")
    return f"{r['number']}\t{state}\t{a}\t{r.get('title', '')}"


def collect(argv):
    if len(argv) > 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    since = argv[0] if len(argv) >= 1 else today
    until = argv[1] if len(argv) == 2 else since
    if not (date_re.match(since) and date_re.match(until)):
        print(f"dates must be YYYY-MM-DD, got: {since} {until}", file=sys.stderr)
        sys.exit(2)

    repo = os.environ.get("WHAT_SHIPPED_REPO", "")
    if not repo:
        data = run_gh(["repo", "view", "--json", "nameWithOwner"])
        repo = data.get("nameWithOwner") or fail("cannot resolve repo from cwd")

    rng = f"{since}..{until}"
    print(f"# repo: {repo}    window: {since} .. {until} (UTC, inclusive)\n")

    def search_prs(flag):
        rows = run_gh(
            ["search", "prs", "--repo", repo, "--limit", str(PR_SEARCH_LIMIT),
             "--json", "number,title,author", flag, rng]
        )
        cap_guard(f"PR search {flag}", rows, PR_SEARCH_LIMIT)
        return split_rows(rows)

    merged_h, merged_b = search_prs("--merged-at")
    opened_h, opened_b = search_prs("--created")
    emit("PR_MERGED", [pr_line(r) for r in merged_h])
    emit("PR_OPENED", [pr_line(r) for r in opened_h])

    open_rows = run_gh(
        ["pr", "list", "--repo", repo, "--state", "open", "--limit", str(OPEN_LIST_LIMIT),
         "--json", "number,title,author,isDraft"]
    )
    cap_guard("open-PR list", open_rows, OPEN_LIST_LIMIT)
    open_h, open_b = split_rows(open_rows, honor_is_bot=True)
    emit("PR_OPEN_NOW", [open_line(r) for r in open_h])

    def search_issues(flag):
        rows = run_gh(
            ["search", "issues", "--repo", repo, "--limit", str(ISSUE_SEARCH_LIMIT),
             "--json", "number,title,author,state", flag, rng]
        )
        cap_guard(f"issue search {flag}", rows, ISSUE_SEARCH_LIMIT)
        return split_rows(rows)

    iopen_h, iopen_b = search_issues("--created")
    iclosed_h, iclosed_b = search_issues("--closed")
    emit("ISSUE_OPENED", [issue_line(r) for r in iopen_h])
    emit("ISSUE_CLOSED", [issue_line(r) for r in iclosed_h])

    # Report the filtered volume rather than hiding it — a day that is 70% release
    # bumps is itself a finding, and a silent filter reads as "nothing happened".
    print(
        f"## BOT_NOISE ({len(merged_b)} PRs merged, {len(opened_b)} PRs opened, "
        f"{len(open_b)} PRs open now, {len(iopen_b)} issues opened, "
        f"{len(iclosed_b)} issues closed) — excluded from the sections above"
    )
    by_login = {}
    for r in merged_b:
        login = (r.get("author") or {}).get("login", "?")
        by_login[login] = by_login.get(login, 0) + 1
    for login, n in sorted(by_login.items(), key=lambda kv: -kv[1])[:5]:
        print(f"  {n} {login}")
    print("\n## OK — all queries succeeded")


def selftest():
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")

    # Bot classification: type wins even when is_bot lies (the gh search quirk).
    check("app-author-type-Bot", is_bot({"login": "adiahealth", "type": "Bot", "is_bot": False}), True)
    check("bot-suffix", is_bot({"login": "renovate[bot]", "type": "User"}), True)
    check("human", is_bot({"login": "kim", "type": "User", "is_bot": False}), False)
    # Negative control: is_bot alone must NOT classify under search semantics...
    check("is-bot-ignored-under-search", is_bot({"login": "x", "type": "User", "is_bot": True}), False)
    # ...and MUST classify under list semantics.
    check("is-bot-honored-under-list", is_bot({"login": "x", "type": "User", "is_bot": True}, honor_is_bot=True), True)

    rows = [
        {"number": 1, "title": "fix", "author": {"login": "kim", "type": "User"}},
        {"number": 2, "title": "bump", "author": {"login": "rel", "type": "Bot"}},
    ]
    h, b = split_rows(rows)
    check("split-humans", [r["number"] for r in h], [1])
    check("split-bots", [r["number"] for r in b], [2])

    # Saturation is a failure, not a big day.
    try:
        cap_guard("probe", list(range(10)), 10)
        fails.append("cap_guard: saturation did not fail")
    except SystemExit as e:
        check("cap-guard-exit", e.code, 1)
    try:
        cap_guard("probe", list(range(9)), 10)
    except SystemExit:
        fails.append("cap_guard: under-limit failed")

    if fails:
        print(f"collect_github · selftest FAIL · {len(fails)} fail")
        for f in fails:
            print(f"  {f}")
        sys.exit(1)
    print("collect_github · selftest OK · 8 checks")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    else:
        collect(sys.argv[1:])
