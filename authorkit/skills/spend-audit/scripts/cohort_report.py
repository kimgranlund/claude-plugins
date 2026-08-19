#!/usr/bin/env python3
"""cohort_report.py — spend-audit's PR-label split axis (gh#763).

gh#759 (measuring the live lane once >=12 `live-lane` PRs exist) names `spend-audit` as
its instrument and assumes it can split merged PRs by label. Before this script,
spend-audit only listed merged PRs by date window (the Collector/backfill step's raw
`gh pr list --state merged --search "merged:><date>"`) with no cohort axis. This script
adds it, without changing the ledger schema (`validate.py` stays the schema canon; this
is a separate report over live `gh` data, not a ledger row) — this ticket's own Non-goal.

The I/O boundary is exactly one function, `fetch_merged_prs()` (a live `gh pr list` call).
Everything downstream — `compute_cohorts()` and its per-PR helpers — is pure and fully
selftest-covered with fixture PR dicts, no network call.

Cohort split: `--label <name>` (repeatable) partitions the window's merged PRs into a
`labeled` cohort (any PR carrying ANY of the named labels) and an `unlabeled` cohort (the
rest); each cohort reports the same metrics side by side. No `--label` given -> today's
unchanged single `all` cohort (this ticket's own Acceptance: "absent flag -> unchanged
single-cohort report").

Per-cohort metrics (this ticket's own Proposal, no new metrics beyond these):
  - open->merge wall-clock (hours, averaged)
  - additions / deletions (averaged)
  - checker-verdict-in-body rate (a PR body citing a checker's own verdict — a heuristic
    regex, not a certified parse; see CHECKER_VERDICT_RE)
  - revert-mention rate (title or body mentions "revert")
  - 48h follow-up-fix rate: the fraction of a cohort's PRs for which a DIFFERENT merged PR,
    merged strictly after it and within 48h, shares >=1 changed file — a file-overlap
    proxy for "this PR needed a quick follow-up fix", computed against the FULL fetched
    window (both cohorts), never cohort-scoped alone, so a labeled PR's follow-up fix
    landing in the unlabeled cohort (or vice versa) still counts.

Usage:
  cohort_report.py --since YYYY-MM-DD [--label <name>]... [--repo <owner/repo>] [--json]
  cohort_report.py selftest

Exit codes: 0 report printed (or selftest PASS) / 2 usage error (`--since` missing, or the
live `gh pr list` call itself failed).
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta

GH_FIELDS = "number,title,createdAt,mergedAt,additions,deletions,labels,body,files"

# Heuristic, not a certified parse: a body citing a checker's own verdict near the word
# "checker" (e.g. "checker: PASS", "code-checker verdict: green"). Documented behaviour,
# selftest-pinned — never silently changed without moving the fixture assertions too.
CHECKER_VERDICT_RE = re.compile(r"checker[^\n]{0,200}?\b(pass|fail|green|red|verdict)\b",
                                 re.IGNORECASE)
REVERT_RE = re.compile(r"\brevert(ed|s)?\b", re.IGNORECASE)


def fetch_merged_prs(since, repo=None):
    """The one I/O boundary — a live `gh pr list` call. Returns the parsed JSON list of
    PR dicts (gh's own shape for GH_FIELDS)."""
    cmd = ["gh", "pr", "list", "--state", "merged", "--search", f"merged:>={since}",
           "--json", GH_FIELDS, "--limit", "500"]
    if repo:
        cmd += ["--repo", repo]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"gh pr list failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def pr_files(pr):
    return {f["path"] for f in (pr.get("files") or [])}


def pr_labels(pr):
    return {label["name"] for label in (pr.get("labels") or [])}


def has_checker_verdict(pr):
    return bool(CHECKER_VERDICT_RE.search(pr.get("body") or ""))


def mentions_revert(pr):
    text = f"{pr.get('title') or ''}\n{pr.get('body') or ''}"
    return bool(REVERT_RE.search(text))


def open_to_merge_hours(pr):
    created, merged = pr.get("createdAt"), pr.get("mergedAt")
    if not created or not merged:
        return None
    c = datetime.fromisoformat(created.replace("Z", "+00:00"))
    m = datetime.fromisoformat(merged.replace("Z", "+00:00"))
    return (m - c).total_seconds() / 3600.0


def has_48h_follow_up_fix(pr, all_prs):
    """A DIFFERENT merged PR, merged strictly after `pr` and within 48h, sharing >=1
    changed file with it. `all_prs` is always the full fetched window, never one cohort
    alone (a follow-up fix can land in the other cohort)."""
    merged = pr.get("mergedAt")
    my_files = pr_files(pr)
    if not merged or not my_files:
        return False
    m = datetime.fromisoformat(merged.replace("Z", "+00:00"))
    window_end = m + timedelta(hours=48)
    for other in all_prs:
        if other.get("number") == pr.get("number"):
            continue
        other_merged = other.get("mergedAt")
        if not other_merged:
            continue
        om = datetime.fromisoformat(other_merged.replace("Z", "+00:00"))
        if m < om <= window_end and (pr_files(other) & my_files):
            return True
    return False


def _avg(values):
    values = [v for v in values if v is not None]
    return (sum(values) / len(values)) if values else None


def compute_cohorts(prs, labels):
    """Pure, selftest-covered: split `prs` (gh pr list --json dicts) into a labeled vs.
    unlabeled cohort pair (or a single `all` cohort when `labels` is empty), then compute
    the fixed metric set per cohort. `follow_up_fix_rate_48h` is checked against the FULL
    `prs` window regardless of the split."""
    label_set = set(labels or [])
    if not label_set:
        cohorts = {"all": list(prs)}
    else:
        labeled, unlabeled = [], []
        for pr in prs:
            (labeled if pr_labels(pr) & label_set else unlabeled).append(pr)
        cohorts = {"labeled": labeled, "unlabeled": unlabeled}

    report = {}
    for name, cohort_prs in cohorts.items():
        n = len(cohort_prs)
        report[name] = {
            "count": n,
            "open_to_merge_hours_avg": _avg([open_to_merge_hours(p) for p in cohort_prs]),
            "additions_avg": _avg([p.get("additions") for p in cohort_prs]),
            "deletions_avg": _avg([p.get("deletions") for p in cohort_prs]),
            "checker_verdict_rate": (
                sum(1 for p in cohort_prs if has_checker_verdict(p)) / n if n else None
            ),
            "revert_mention_rate": (
                sum(1 for p in cohort_prs if mentions_revert(p)) / n if n else None
            ),
            "follow_up_fix_rate_48h": (
                sum(1 for p in cohort_prs if has_48h_follow_up_fix(p, prs)) / n if n else None
            ),
        }
    return report


def render_report(report):
    def fmt(v, suffix=""):
        return "n/a" if v is None else f"{v:.2f}{suffix}"

    lines = ["spend-audit cohort report"]
    for name in sorted(report):
        m = report[name]
        lines.append(
            f"  {name}: n={m['count']} "
            f"open->merge={fmt(m['open_to_merge_hours_avg'], 'h')} "
            f"additions={fmt(m['additions_avg'])} deletions={fmt(m['deletions_avg'])} "
            f"checker-verdict={fmt(m['checker_verdict_rate'])} "
            f"revert-mentions={fmt(m['revert_mention_rate'])} "
            f"followup-fix-48h={fmt(m['follow_up_fix_rate_48h'])}"
        )
    return "\n".join(lines)


def build_arg_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--since")
    ap.add_argument("--label", action="append", default=[])
    ap.add_argument("--repo")
    ap.add_argument("--json", action="store_true")
    return ap


def selftest():
    pr_a = {
        "number": 1, "title": "feat: add thing", "createdAt": "2026-08-01T00:00:00Z",
        "mergedAt": "2026-08-02T00:00:00Z", "additions": 100, "deletions": 10,
        "labels": [{"name": "live-lane"}], "body": "checker verdict: PASS",
        "files": [{"path": "a.py"}],
    }
    pr_b = {
        "number": 2, "title": "fix: unrelated", "createdAt": "2026-08-03T00:00:00Z",
        "mergedAt": "2026-08-04T00:00:00Z", "additions": 5, "deletions": 5,
        "labels": [], "body": "no checker mention here", "files": [{"path": "b.py"}],
    }

    # Two fake PRs, one labeled -> two cohorts (this ticket's own selftest-fixture line).
    report = compute_cohorts([pr_a, pr_b], ["live-lane"])
    assert set(report) == {"labeled", "unlabeled"}, report
    assert report["labeled"]["count"] == 1, report
    assert report["unlabeled"]["count"] == 1, report
    assert report["labeled"]["checker_verdict_rate"] == 1.0, report
    assert report["unlabeled"]["checker_verdict_rate"] == 0.0, report
    assert report["labeled"]["additions_avg"] == 100.0, report
    assert report["unlabeled"]["revert_mention_rate"] == 0.0, report

    # Label absent everywhere -> one cohort, no crash (this ticket's own negative control).
    report2 = compute_cohorts([pr_a, pr_b], [])
    assert set(report2) == {"all"}, report2
    assert report2["all"]["count"] == 2, report2

    # A requested label matching NOTHING in the set -> still a clean split, all unlabeled,
    # never a crash (reverse control on the split itself).
    report3 = compute_cohorts([pr_a, pr_b], ["nonexistent-label"])
    assert report3["labeled"]["count"] == 0, report3
    assert report3["unlabeled"]["count"] == 2, report3
    assert report3["labeled"]["checker_verdict_rate"] is None, report3  # n=0 -> n/a, never 0

    # 48h follow-up-fix: pr_c merges 10h after pr_a and touches the same file -> pr_a
    # counts; pr_c itself has no later same-file PR -> it does not.
    pr_c = {
        "number": 3, "title": "fix: quick patch", "createdAt": "2026-08-02T05:00:00Z",
        "mergedAt": "2026-08-02T10:00:00Z", "additions": 2, "deletions": 1,
        "labels": [], "body": "", "files": [{"path": "a.py"}],
    }
    report4 = compute_cohorts([pr_a, pr_c], [])
    assert report4["all"]["follow_up_fix_rate_48h"] == 0.5, report4

    # A same-file PR merged AFTER the 48h window does not count.
    pr_d = {
        "number": 4, "title": "fix: late patch", "createdAt": "2026-08-05T00:00:00Z",
        "mergedAt": "2026-08-05T00:00:00Z", "additions": 1, "deletions": 1,
        "labels": [], "body": "", "files": [{"path": "a.py"}],
    }
    report5 = compute_cohorts([pr_a, pr_d], [])
    assert report5["all"]["follow_up_fix_rate_48h"] == 0.0, report5

    # render_report names every cohort, never crashes on an all-None (n=0) cohort.
    text = render_report(report)
    assert "labeled" in text and "unlabeled" in text, text
    text3 = render_report(report3)
    assert "n=0" in text3 and "n/a" in text3, text3

    # CLI-surface: --label is repeatable and accumulates (usage-surface check, no gh call).
    args = build_arg_parser().parse_args(["--since", "2026-08-01", "--label", "a", "--label", "b"])
    assert args.label == ["a", "b"], args.label
    args_absent = build_arg_parser().parse_args(["--since", "2026-08-01"])
    assert args_absent.label == [], args_absent.label

    # Missing --since at the main()-level CLI surface -> exit 2, never a crash or a
    # silent no-op.
    proc = subprocess.run([sys.executable, __file__], capture_output=True, text=True)
    assert proc.returncode == 2, (proc.returncode, proc.stdout, proc.stderr)

    print("cohort_report.py selftest: PASS")
    return 0


def main():
    a = build_arg_parser().parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.since:
        print("cohort_report.py: --since YYYY-MM-DD is required (or `selftest`)", file=sys.stderr)
        return 2

    try:
        prs = fetch_merged_prs(a.since, repo=a.repo)
    except RuntimeError as e:
        print(f"cohort_report.py: {e}", file=sys.stderr)
        return 2

    report = compute_cohorts(prs, a.label)
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_report(report))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"cohort_report.py error: {e}", file=sys.stderr)
        sys.exit(2)
