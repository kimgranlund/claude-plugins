#!/usr/bin/env python3
"""detect.py — D1-D4 deterministic negative-pattern detectors + fix_clusters over a
`collect.py` bundle (gh#629, lld-0019). Emits `findings.json` in
`references/report-template.md`'s schema. Every finding carries `artifact` + `owning_command`,
or renders `status: unrouted` when detect.py itself cannot name one (never silently dropped) —
the actual RIGHT/WRONG judgment of a finding is Phase 3/5's job (the confirm gate), not this
script's; this script is arithmetic, not judgment (script-writing-rules' mechanization test).

Usage:
  detect.py <bundle.json> [--json] [--window-days N] [--now YYYY-MM-DD] [--out findings.json]
  detect.py --verify <findings.json>
  detect.py selftest

Exit: 0 clean run (findings may be 0 or more; that's not a failure) · 1 --verify found a broken
evidence pointer · 2 usage error.

Detector thresholds (flag-tunable via the constants below, cited beside every finding they fire):
  D1 — memory entries `metadata.type: feedback`, clustered on (name+description) token OVERLAP
       COEFFICIENT (shared tokens / min(len_a, len_b), NOT Jaccard — raw Jaccard punishes length
       asymmetry between a short first-telling and a long third-telling too hard to ever fire on
       real prose, gh#645 MAJOR-2) >= OVERLAP_D1 (0.2) with >= MIN_SHARED_D1 (3) shared
       non-stopword tokens; a cluster of size >= 2, OR a single entry whose description matches
       RECURRENCE_LEXICON, is a finding. Matches the DESCRIPTION only, never the body (LLD
       lld-0019 said body; description-only is what shipped and is cheaper to keep correct —
       body text pulls in template boilerplate ("Why:", "How to apply:", dates) that inflates
       overlap between otherwise-unrelated entries; dated correction on the LLD itself, 2026-08-18).
  D2 — issue titles normalized (lowercase, punctuation/stopwords/#NNN stripped), pairwise
       Jaccard >= JACCARD_D2 (0.5) -> a cluster; a member created after another member's
       `closedAt` = re-filed (major); same-window overlap with no created-after-closed edge =
       dedup-miss (minor). Two exclusions (gh#694, run-2 finding: 4/5 D2 hits were false
       positives) run before/during clustering: (a) a title carrying a FIXTURE prefix or "do not
       build" marker is filtered out before any comparison — a deliberate probe fixture, never a
       real near-dup candidate; (b) a pairwise edge is never unioned, even at Jaccard >=
       JACCARD_D2, when both titles share an identical wave NUMBER ("wave N") or an identical
       ADR-id token — a deliberate same-campaign wave-sibling/multi-ADR capture set, not a
       dedup-search miss.
  D3 — per METRIC_REGISTRY key present in the bundle: rows are GROUPED by that key's own
       registered `key_columns` first (e.g. one series per `plugin` for attention_trend — never
       iterated ungrouped across interleaved rows from multiple keys, gh#645 MAJOR-1), then for
       each `series_columns` entry: a column monotonic non-decreasing within its group across
       >= MIN_ROWS_D3 (3) rows with >= GROWTH_PCT_D3 (5%) total growth -> rent-growth (one finding
       per key+column); a column `absent` in 100% of >= MIN_ROWS_D3 rows across the WHOLE source
       (never never-fed-ness is a per-key question) -> instrument-half-blind; a source with
       exactly 1 row older than `--window-days` -> series-not-firing; recurrence_trend's latest
       row `seeded_classes == 0` -> ratchet-unadopted.
  D4 — entry files (any `CLAUDE.md` under root) > ENTRY_FILE_LINE_THRESHOLD (200, skill_lint.py
       C1's own constant) -> entry-file-oversized (one finding per file); the rest of the
       census (rules count/total lines, MEMORY.md index lines, per-plugin routable+agent char
       sum) renders as ONE context-surface-census finding per run, `nit` severity — detect.py
       names the surface and its raw number; judging whether the number is a problem is
       `/check-entry-file` / `bloat-audit`'s job, never invented here as an unstated threshold.
"""
import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import ENTRY_FILE_LINE_THRESHOLD  # noqa: E402  (sibling, same scripts/ dir)

OVERLAP_D1 = 0.2  # overlap coefficient (gh#645 MAJOR-2), NOT Jaccard — see module docstring
MIN_SHARED_D1 = 3
JACCARD_D2 = 0.5
MIN_ROWS_D3 = 3
GROWTH_PCT_D3 = 5.0

RECURRENCE_LEXICON = re.compile(
    r"\bthird time\b|\bagain\b|\brepeatedly\b|\bnever re-ask\b|\bstop (doing|proposing)\b", re.I
)  # word-bounded (2026-08-18 fix): an unbounded `again` false-positived on "against" against
   # this repo's own real memory corpus — caught by AC-1's real-estate dry run, not the fixture

STOPWORDS = set("""a an and are as at be but by can do for from has have how i in is it its my
not of on one or our so that the their these this those to use used using we what when where
which who will with you your never always only also this's it's fix fixes fixed add adds added
closes close closed update updates updated bug feature issue ticket demo per via""".split())
# "per"/"via" added (gh#645 MAJOR-2): generic prepositions, not informative shared vocabulary —
# they inflated overlap between otherwise-unrelated memory entries under the new D1 calibration.

ISSUE_HEAD_RE = re.compile(r"#\d+")
WORD_RE = re.compile(r"[a-z0-9]+")


# ------------------------------------------------------------------ shared token/cluster helpers
def tokenize(text):
    if not text:
        return set()
    text = ISSUE_HEAD_RE.sub(" ", text.lower())
    return {t for t in WORD_RE.findall(text) if len(t) > 2 and t not in STOPWORDS}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def overlap_coefficient(a, b):
    """shared tokens / min(len_a, len_b) — unlike Jaccard, doesn't punish a short first-telling
    paired against a long third-telling description (gh#645 MAJOR-2: real feedback-memory pairs
    run 20-30 informative tokens with wildly different lengths; Jaccard's union-sized denominator
    made a real third-telling trio invisible)."""
    if not a or not b:
        return 0.0
    minlen = min(len(a), len(b))
    return len(a & b) / minlen if minlen else 0.0


def cluster_pairs(items, get_tokens, threshold, min_shared=0, metric=jaccard, exclude_edge=None):
    """items: list of arbitrary objects. get_tokens(item) -> set of tokens.
    Returns a list of clusters (each a list of the original items), connected-components style
    over the "collides" graph (pairwise `metric` >= threshold AND shared-token count >= min_shared,
    AND, when `exclude_edge` is given, `not exclude_edge(items[i], items[j])` — an edge that would
    otherwise cluster but is known to be a deliberate same-source pair, e.g. D2's fixture/wave-
    sibling exclusions, never unions). Deterministic: items processed in input order, clusters
    returned in first-member order."""
    n = len(items)
    toks = [get_tokens(it) for it in items]
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for i in range(n):
        for j in range(i + 1, n):
            shared = toks[i] & toks[j]
            if len(shared) >= min_shared and metric(toks[i], toks[j]) >= threshold:
                if exclude_edge and exclude_edge(items[i], items[j]):
                    continue
                union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(items[i])
    return [g for g in groups.values() if len(g) >= 1]


# ------------------------------------------------------------------------------- evidence pointers
def make_line_evidence(path, text, needle):
    lines = text.splitlines() if text else []
    for i, line in enumerate(lines, start=1):
        if needle and needle in line:
            return {"path": str(path), "locator": f"line:{i}", "quote": line.strip()[:200]}
    first = lines[0].strip()[:200] if lines else ""
    return {"path": str(path), "locator": "line:1", "quote": first}


def make_lines_evidence(path, total_lines, note=None):
    return {"path": str(path), "locator": f"lines:{total_lines}",
            "quote": note or f"{total_lines} lines total"}


def make_csv_row_evidence(path, row_index_1based, quote):
    return {"path": str(path), "locator": f"csv-row:{row_index_1based}", "quote": quote}


def make_issue_evidence(path, number, title):
    return {"path": str(path), "locator": f"issue:{number}", "quote": title}


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def verify_pointer(evidence):
    """Re-open one evidence pointer against the real filesystem. Returns (ok: bool, why: str)."""
    path = Path(evidence.get("path", ""))
    locator = evidence.get("locator", "")
    quote = (evidence.get("quote") or "").strip()
    if not path.is_file():
        return False, f"file not found: {path}"
    if locator.startswith("line:"):
        n = int(locator.split(":", 1)[1])
        lines = (_read(path) or "").splitlines()
        if not (1 <= n <= len(lines)):
            return False, f"line {n} out of range (file has {len(lines)} lines)"
        line = lines[n - 1].strip()
        if quote and quote not in line and line not in quote:
            return False, f"quote mismatch at line {n}: {quote!r} vs {line!r}"
        return True, None
    if locator.startswith("lines:"):
        n = int(locator.split(":", 1)[1])
        lines = (_read(path) or "").splitlines()
        if len(lines) != n:
            return False, f"line count changed: claimed {n}, now {len(lines)}"
        return True, None
    if locator.startswith("csv-row:"):
        n = int(locator.split(":", 1)[1])
        rows = list(csv.DictReader((_read(path) or "").splitlines()))
        if not (1 <= n <= len(rows)):
            return False, f"csv row {n} out of range ({len(rows)} data rows)"
        rendered = ",".join(f"{k}={v}" for k, v in rows[n - 1].items())
        if quote and quote not in rendered:
            return False, f"quote {quote!r} not found in row {n}: {rendered}"
        return True, None
    if locator.startswith("issue:"):
        num = locator.split(":", 1)[1]
        try:
            items = json.loads(_read(path) or "[]")
        except json.JSONDecodeError:
            return False, "issues.json unparseable"
        match = next((it for it in items if str(it.get("number")) == num), None)
        if match is None:
            return False, f"issue #{num} not found in {path}"
        if quote and quote not in (match.get("title") or ""):
            return False, f"title mismatch for #{num}: {quote!r} vs {match.get('title')!r}"
        return True, None
    return False, f"unknown locator scheme: {locator}"


# ------------------------------------------------------------------------------------------- D1
def detect_d1(bundle):
    findings = []
    entries = [e for e in bundle.get("memory", {}).get("entries", []) if e.get("type") == "feedback"]

    def get_tokens(e):
        return tokenize((e.get("name") or "") + " " + (e.get("description") or ""))

    clusters = cluster_pairs(entries, get_tokens, OVERLAP_D1, MIN_SHARED_D1, metric=overlap_coefficient)
    seen_files = set()
    idx = 0
    memory_path = bundle.get("memory", {}).get("path")

    for cluster in clusters:
        if len(cluster) >= 2:
            idx += 1
            ev = []
            for e in cluster:
                fpath = str(Path(memory_path) / e["file"]) if memory_path else e["file"]
                ev.append(make_line_evidence(fpath, _read(fpath) or "", e.get("description") or e.get("name") or ""))
                seen_files.add(e["file"])
            findings.append({
                "id": f"D1-{idx}",
                "class": "D1",
                "severity": "major",
                "summary": f"Repeated user nudge: {len(cluster)} feedback memory entries cluster on "
                           f"shared vocabulary ({', '.join(sorted(get_tokens(cluster[0]) & get_tokens(cluster[1])))[:120]})"
                           f" — a third-telling pattern not yet promoted to a durable rule/skill line.",
                "evidence": ev,
                "artifact": {"path": ev[0]["path"], "kind": "memory-entry"},
                "owning_command": "harness:save-lessons",
                "proposed_diff": None,
                "size": "diff",
                "status": "proposed",
            })

    # single-entry lexicon match, for any feedback entry not already claimed by a >=2 cluster
    for e in entries:
        if e["file"] in seen_files:
            continue
        desc = e.get("description") or ""
        if RECURRENCE_LEXICON.search(desc):
            idx += 1
            fpath = str(Path(memory_path) / e["file"]) if memory_path else e["file"]
            ev = [make_line_evidence(fpath, _read(fpath) or "", desc)]
            findings.append({
                "id": f"D1-{idx}",
                "class": "D1",
                "severity": "major",
                "summary": f"Repeated user nudge: '{e.get('name')}' matches the recurrence lexicon "
                           f"in its own description — a correction already restated on record.",
                "evidence": ev,
                "artifact": {"path": ev[0]["path"], "kind": "memory-entry"},
                "owning_command": "harness:save-lessons",
                "proposed_diff": None,
                "size": "diff",
                "status": "proposed",
            })
    return findings


# ------------------------------------------------------------------------------------------- D2
FIXTURE_MARKER_RE = re.compile(r"^\s*FIXTURE\b|do not build", re.I)
# gh#694 exclusion (a): a title carrying a FIXTURE prefix or a "do not build" marker is a
# deliberate probe fixture, never a real near-duplicate candidate — the run-2 false positive was
# exactly two such fixtures (#617/#616) clustering with EACH OTHER, not with anything real.

WAVE_TOKEN_RE = re.compile(r"\bwave\s*#?\s*(\d+)\b", re.I)
ADR_TOKEN_RE = re.compile(r"\bADR-(\d{3,5})\b", re.I)
# gh#694 exclusion (b): same-campaign wave siblings. Raw-text regexes, not `tokenize()` — a bare
# wave NUMBER ("2") is 1 char and `tokenize()`'s `len(t) > 2` filter would silently drop it, so the
# wave-number identity has to be read straight off the title text instead.


def _is_fixture_marked(title):
    """D2 exclusion (a) predicate — see FIXTURE_MARKER_RE above."""
    return bool(FIXTURE_MARKER_RE.search(title or ""))


def _campaign_token_sets(title):
    """Extract same-campaign identity tokens from a raw title: wave numbers and ADR ids."""
    title = title or ""
    waves = set(WAVE_TOKEN_RE.findall(title))
    adrs = {m.upper() for m in ADR_TOKEN_RE.findall(title)}
    return waves, adrs


def _same_campaign(item_a, item_b):
    """D2 exclusion (b) predicate: a shared wave NUMBER or a shared ADR-id token in both titles
    means the pair is a deliberate multi-wave/multi-ADR capture set, not a dedup-search miss —
    the run-2 false positives were #613/#612 (sibling captures) and #523/#520 + #522/#521
    (ADR-0020 wave tickets)."""
    waves_a, adrs_a = _campaign_token_sets(item_a.get("title"))
    waves_b, adrs_b = _campaign_token_sets(item_b.get("title"))
    return bool(waves_a & waves_b) or bool(adrs_a & adrs_b)


def _norm_title_tokens(title):
    return tokenize(title or "")


def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def detect_d2(bundle):
    findings = []
    items = bundle.get("issues", {}).get("items", [])
    issues_path = bundle.get("issues", {}).get("path")
    if not items:
        return findings

    # exclusion (a): fixture-marked titles never enter clustering at all — filtered before any
    # pairwise comparison runs, so two fixtures can never cluster with each other or with anything
    # real.
    items = [it for it in items if not _is_fixture_marked(it.get("title"))]
    if not items:
        return findings

    clusters = cluster_pairs(items, lambda it: _norm_title_tokens(it.get("title")), JACCARD_D2, 1,
                              exclude_edge=_same_campaign)
    idx = 0
    for cluster in clusters:
        if len(cluster) < 2:
            continue
        # re-filed: any member created after another member's closedAt
        refiled_pair = None
        for later in cluster:
            later_created = _parse_dt(later.get("createdAt"))
            if later_created is None:
                continue
            for earlier in cluster:
                if earlier is later:
                    continue
                earlier_closed = _parse_dt(earlier.get("closedAt"))
                if earlier_closed and later_created > earlier_closed:
                    refiled_pair = (earlier, later)
                    break
            if refiled_pair:
                break

        idx += 1
        ev = [make_issue_evidence(issues_path, it.get("number"), it.get("title")) for it in cluster]
        if refiled_pair:
            earlier, later = refiled_pair
            findings.append({
                "id": f"D2-{idx}",
                "class": "D2",
                "severity": "major",
                "summary": f"Re-filed near-duplicate: #{later.get('number')} ({later.get('title')!r}) "
                           f"opened after #{earlier.get('number')} ({earlier.get('title')!r}) closed — "
                           f"the same fix was not found by dedup search before re-filing.",
                "evidence": ev,
                "artifact": {"path": issues_path, "kind": "issue-pair"},
                "owning_command": "docs:file-bug|file-feature (dedup-search step) or harness:issue-sorter",
                "proposed_diff": None,
                "size": "ticket",
                "status": "proposed",
            })
        else:
            findings.append({
                "id": f"D2-{idx}",
                "class": "D2",
                "severity": "minor",
                "summary": f"Same-window near-duplicate titles ({', '.join('#' + str(it.get('number')) for it in cluster)}) "
                           f"— a dedup-search miss, not (yet) a re-filed pattern.",
                "evidence": ev,
                "artifact": {"path": issues_path, "kind": "issue-pair"},
                "owning_command": "docs:file-bug|file-feature (dedup-search step) or harness:issue-sorter",
                "proposed_diff": None,
                "size": "ticket",
                "status": "proposed",
            })
    return findings


# ------------------------------------------------------------------------------------------- D3
OWNING_INSTRUMENT = {
    "attention_trend": "authorkit:attention-audit (step 6, the trend-append step)",
    "recurrence_trend": "authorkit:recurrence-audit (step 6, the trend-append step)",
    "cost_ledger": "the #624 cost-ledger build, once shipped",
}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _group_rows(rows, key_columns):
    """[(key_tuple_or_None, [(orig_idx0based, row), ...])] — groups `rows` (in append order) by
    `key_columns` (e.g. ["plugin"]), preserving first-seen-group order. `orig_idx0based` is the
    row's index into the FULL `rows` list (never a group-relative index) so evidence pointers
    (`csv-row:N`) stay verifiable against the real file, which `detect.py --verify` re-reads
    whole (gh#645 MAJOR-1). An empty `key_columns` (no grouping registered, e.g. recurrence_trend)
    yields exactly one group spanning all rows — the pre-fix, ungrouped behavior."""
    if not key_columns:
        return [(None, list(enumerate(rows)))]
    groups = {}
    order = []
    for i, row in enumerate(rows):
        key = tuple(row.get(c) for c in key_columns)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append((i, row))
    return [(k, groups[k]) for k in order]


def _group_label(key_columns, gkey):
    if not key_columns or gkey is None:
        return ""
    return " (" + ", ".join(f"{k}={v}" for k, v in zip(key_columns, gkey)) + ")"


def detect_d3(bundle, window_days, now):
    findings = []
    metrics = bundle.get("metrics", {})
    idx = 0

    for key, source in metrics.items():
        if not source.get("present"):
            continue
        rows = source.get("rows", [])
        path = source.get("path")
        series_columns = source.get("series_columns") or []
        key_columns = source.get("key_columns") or []

        # instrument-half-blind: a registered series column literally "absent" in every row of
        # the WHOLE source — never-fed-ness is a source-wide question, not a per-key one, so this
        # check stays ungrouped (gh#645 MAJOR-1's fix only groups the MONOTONIC-GROWTH check).
        if len(rows) >= MIN_ROWS_D3:
            for col in series_columns:
                values = [row.get(col) for row in rows]
                if values and all(v == "absent" for v in values):
                    idx += 1
                    ev = [make_csv_row_evidence(path, i + 1, f"{col}=absent")
                          for i in range(min(3, len(rows)))]
                    findings.append({
                        "id": f"D3-{idx}", "class": "D3", "severity": "major",
                        "summary": f"instrument-half-blind: '{col}' is `absent` in {len(rows)}/{len(rows)} "
                                   f"rows of {Path(path).name} — the column is registered but never fed.",
                        "evidence": ev,
                        "artifact": {"path": path, "kind": "trend-csv"},
                        "owning_command": OWNING_INSTRUMENT.get(key, "the owning instrument's own procedure step"),
                        "proposed_diff": None, "size": "ticket", "status": "proposed",
                    })
                    continue

                # rent-growth: monotonic non-decreasing GROUPED by key_columns (gh#645 MAJOR-1) —
                # e.g. one series per `plugin`, never iterated across interleaved rows from
                # multiple plugins (the bug: growth is real per-key but invisible ungrouped).
                for gkey, indexed in _group_rows(rows, key_columns):
                    if len(indexed) < MIN_ROWS_D3:
                        continue
                    nums = [_num(row.get(col)) for _, row in indexed]
                    if any(v is None for v in nums):
                        continue
                    monotonic = all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1))
                    if not monotonic or nums[0] == 0:
                        continue
                    growth_pct = (nums[-1] - nums[0]) / nums[0] * 100 if nums[0] else 0
                    if growth_pct >= GROWTH_PCT_D3:
                        idx += 1
                        first_i, _ = indexed[0]
                        last_i, _ = indexed[-1]
                        ev = [make_csv_row_evidence(path, first_i + 1, f"{col}={nums[0]:g}"),
                              make_csv_row_evidence(path, last_i + 1, f"{col}={nums[-1]:g}")]
                        label = _group_label(key_columns, gkey)
                        findings.append({
                            "id": f"D3-{idx}", "class": "D3", "severity": "minor",
                            "summary": f"rent-growth: '{col}' in {Path(path).name}{label} grew "
                                       f"{growth_pct:.1f}% ({nums[0]:g} -> {nums[-1]:g}) "
                                       f"monotonically over {len(indexed)} rows, no decrease.",
                            "evidence": ev,
                            "artifact": {"path": path, "kind": "trend-csv"},
                            "owning_command": "authorkit:attention-audit (structural-fix set: reciprocal "
                                              "fence / demote-to-wiring / merge / centralize-boilerplate / retire)",
                            "proposed_diff": None, "size": "ticket", "status": "proposed",
                        })

        # series-not-firing: exactly 1 row, older than window_days
        if len(rows) == 1:
            row_date = _parse_dt(rows[0].get("date"))
            now_dt = _parse_dt(now) or datetime.now()
            if row_date and (now_dt.replace(tzinfo=None) - row_date.replace(tzinfo=None)).days > window_days:
                idx += 1
                ev = [make_csv_row_evidence(path, 1, f"date={rows[0].get('date')}")]
                findings.append({
                    "id": f"D3-{idx}", "class": "D3", "severity": "major",
                    "summary": f"series-not-firing: {Path(path).name} has exactly 1 row, dated "
                               f"{rows[0].get('date')} — older than the {window_days}-day window; "
                               f"the loop that appends it isn't firing.",
                    "evidence": ev,
                    "artifact": {"path": path, "kind": "trend-csv"},
                    "owning_command": OWNING_INSTRUMENT.get(key, "the owning instrument's own procedure step"),
                    "proposed_diff": None, "size": "ticket", "status": "proposed",
                })

        # ratchet-unadopted: recurrence_trend's latest row seeded_classes == 0
        if key == "recurrence_trend" and rows:
            latest = rows[-1]
            if _num(latest.get("seeded_classes")) == 0:
                idx += 1
                ev = [make_csv_row_evidence(path, len(rows), "seeded_classes=0")]
                findings.append({
                    "id": f"D3-{idx}", "class": "D3", "severity": "major",
                    "summary": "ratchet-unadopted: recurrence-trend's latest row has "
                               "`seeded_classes=0` — the LEDGER-CLASS: ratchet is live but unadopted.",
                    "evidence": ev,
                    "artifact": {"path": path, "kind": "trend-csv"},
                    "owning_command": "authorkit:recurrence-audit",
                    "proposed_diff": None, "size": "ticket", "status": "proposed",
                })
    return findings


# ------------------------------------------------------------------------------------------- D4
def detect_d4(bundle):
    findings = []
    census = bundle.get("census", {})
    idx = 0

    for ef in census.get("entry_files", []):
        if ef.get("over_threshold"):
            idx += 1
            findings.append({
                "id": f"D4-{idx}", "class": "D4", "severity": "minor",
                "summary": f"entry-file-oversized: {ef['path']} is {ef['lines']} lines "
                           f"(> {ENTRY_FILE_LINE_THRESHOLD}, skill_lint.py C1's own threshold).",
                "evidence": [make_lines_evidence(ef["path"], ef["lines"])],
                "artifact": {"path": ef["path"], "kind": "entry-file"},
                "owning_command": "/check-entry-file",
                "proposed_diff": None, "size": "ticket", "status": "proposed",
            })

    memory = bundle.get("memory", {})
    plugin_chars = census.get("plugin_chars", {})
    idx += 1
    ev = []
    if memory.get("index_lines") is not None and memory.get("path"):
        ev.append(make_lines_evidence(str(Path(memory["path"]) / "MEMORY.md"), memory["index_lines"]))
    for rf in census.get("rules_files", []):
        ev.append(make_lines_evidence(rf["path"], rf["lines"]))
    top_plugins = sorted(plugin_chars.items(), key=lambda kv: -kv[1])[:5]
    summary = (
        f"context-surface census: {census.get('rules_count', 0)} rules files "
        f"({census.get('rules_total_lines', 0)} lines total), memory index "
        f"{memory.get('index_lines')} lines, top plugin rent (routable+agent chars): "
        f"{', '.join(f'{p}={c}' for p, c in top_plugins) or 'none measured'}. "
        f"Surface named; judging whether any number is a problem is /check-entry-file / "
        f"bloat-audit's call, not decided here."
    )
    if ev:
        findings.append({
            "id": f"D4-{idx}", "class": "D4", "severity": "nit",
            "summary": summary,
            "evidence": ev,
            "artifact": {"path": ev[0]["path"], "kind": "context-surface-census"},
            "owning_command": "/check-entry-file or authorkit:bloat-audit",
            "proposed_diff": None, "size": "ticket", "status": "proposed",
        })
    return findings


# --------------------------------------------------------------------------------- fix_clusters
def compute_fix_clusters(bundle, window_days, now):
    """Non-finding helper block (Procedure Phase 3a): closed issues + feedback memories inside
    `window_days` of `now`, plus every known ADR/IDR id (no collect.py-tracked date to window-
    filter them by — included unconditionally), clustered by title-token Jaccard. The judgment
    layer (Phase 3) reads this to infer which sibling areas a fix generalizes to."""
    now_dt = _parse_dt(now) or datetime.now()
    items = []

    for it in bundle.get("issues", {}).get("items", []):
        closed = _parse_dt(it.get("closedAt"))
        if closed and (now_dt.replace(tzinfo=None) - closed.replace(tzinfo=None)).days <= window_days:
            items.append({"kind": "issue", "ref": f"#{it.get('number')}", "title": it.get("title") or ""})

    memory_path = bundle.get("memory", {}).get("path")
    for e in bundle.get("memory", {}).get("entries", []):
        if e.get("type") != "feedback":
            continue
        modified = _parse_dt(e.get("modified"))
        if modified and (now_dt.replace(tzinfo=None) - modified.replace(tzinfo=None)).days <= window_days:
            items.append({"kind": "memory", "ref": str(Path(memory_path) / e["file"]) if memory_path else e["file"],
                          "title": e.get("description") or e.get("name") or ""})

    for a in bundle.get("decisions", {}).get("adrs", []) + bundle.get("decisions", {}).get("idrs", []):
        items.append({"kind": "decision", "ref": a["id"], "title": a["id"]})

    clusters = cluster_pairs(items, lambda it: tokenize(it["title"]), JACCARD_D2, 1)
    return [{"members": c, "shared_tokens": sorted(tokenize(c[0]["title"]) & tokenize(c[1]["title"]))
             if len(c) >= 2 else []}
            for c in clusters if len(c) >= 2]


# ------------------------------------------------------------------------------------------ core
def detect(bundle, window_days=None, now=None):
    window_days = window_days if window_days is not None else bundle.get("run", {}).get("window_days", 90)
    now = now or bundle.get("run", {}).get("date") or date.today().isoformat()

    findings = []
    findings.extend(detect_d1(bundle))
    findings.extend(detect_d2(bundle))
    findings.extend(detect_d3(bundle, window_days, now))
    findings.extend(detect_d4(bundle))

    unmeasured = [{"input": k, "reason": v["reason"]} for k, v in bundle.get("inputs", {}).items()
                  if not v.get("present")]

    return {
        "run": bundle.get("run", {}),
        "findings": findings,
        "fix_clusters": compute_fix_clusters(bundle, window_days, now),
        "unmeasured": unmeasured,
    }


def do_verify(findings_path):
    data = json.loads(Path(findings_path).read_text(encoding="utf-8"))
    total, failed = 0, []
    for f in data.get("findings", []):
        for ev in f.get("evidence", []):
            total += 1
            ok, why = verify_pointer(ev)
            if not ok:
                failed.append((f["id"], ev, why))
    print(f"detect.py --verify: {total - len(failed)}/{total} evidence pointers resolve")
    for fid, ev, why in failed:
        print(f"  FAIL {fid}: {ev.get('path')}#{ev.get('locator')} — {why}", file=sys.stderr)
    return 1 if failed else 0


def selftest():
    import collect as collect_mod
    fixture = Path(__file__).resolve().parents[1] / "assets" / "fixture-estate"
    bundle = collect_mod.collect(
        fixture, memory_dir=fixture / "memory", issues_path=fixture / "issues.json",
        window_days=3, now="2026-08-25",
    )
    result = detect(bundle, window_days=3, now="2026-08-25")
    classes = {f["class"] for f in result["findings"]}
    assert classes == {"D1", "D2", "D3", "D4"}, f"missing seeded classes: {classes}"

    d1 = [f for f in result["findings"] if f["class"] == "D1"]
    assert len(d1) >= 1, "D1 must fire on the fixture's feedback trio"

    # gh#645 MAJOR-2: the realistic (long, varied-length) model-tiering trio must cluster into
    # ONE D1 finding spanning all three files — proving the overlap-coefficient calibration, not
    # just the near-identical toy trio, which any threshold would catch.
    tiering_files = {"feedback-model-tiering-1.md", "feedback-model-tiering-2.md",
                     "feedback-model-tiering-3.md"}
    tiering_finding = next(
        (f for f in d1 if tiering_files <= {Path(ev["path"]).name for ev in f["evidence"]}), None)
    assert tiering_finding is not None, \
        f"the realistic model-tiering trio must cluster as one D1 finding: {d1}"

    # regression proof, mechanical not asserted-by-eye: under the OLD calibration (raw Jaccard
    # >= 0.3) this exact trio would NEVER have clustered — every pairwise Jaccard stays below the
    # old threshold, while the new overlap coefficient clears 0.2 with >= 3 shared tokens on
    # every pair. This is the concrete "old missed it, new catches it" evidence gh#645 asked for.
    tiering_descs = {
        "1": "checker-model-pin-note Checker agents already pin fable at medium in their own "
             "frontmatter; a per-dispatch model override on a checker is redundant and can "
             "detach effort from the agent definition.",
        "2": "orchestration-model-drift-report Kim observed several subagents riding the "
             "orchestrating session's higher-priced model tier during a busy stretch; the root "
             "cause traced back to per-dispatch model overrides plus inherit-class agents that "
             "carry no pin of their own.",
        "3": "review-tier-pin-reminder Review and critic agents should run at their own "
             "already-pinned tier — never pass a model override on a checker dispatch, only pin "
             "the model explicitly on ad-hoc general-purpose calls.",
    }
    tiering_toks = {k: tokenize(v) for k, v in tiering_descs.items()}
    for a, b in (("1", "2"), ("1", "3"), ("2", "3")):
        old_jaccard = jaccard(tiering_toks[a], tiering_toks[b])
        new_overlap = overlap_coefficient(tiering_toks[a], tiering_toks[b])
        shared_n = len(tiering_toks[a] & tiering_toks[b])
        assert old_jaccard < 0.3, \
            f"regression fixture {a}-{b} must stay BELOW the old raw-Jaccard 0.3 bar: {old_jaccard}"
        assert new_overlap >= OVERLAP_D1 and shared_n >= MIN_SHARED_D1, \
            f"regression fixture {a}-{b} must clear the new calibration: overlap={new_overlap} shared={shared_n}"

    d2 = [f for f in result["findings"] if f["class"] == "D2"]
    assert any("re-filed" in f["summary"].lower() or "Re-filed" in f["summary"] for f in d2), d2

    # gh#694 positive control: the real re-filed near-dup (#501/#588, the #332/#318 class) must
    # still fire after the two exclusions below are wired in — proving neither exclusion is
    # overbroad.
    d2_issue_numbers = {int(ev["locator"].split(":", 1)[1])
                        for f in d2 for ev in f["evidence"]}
    assert {501, 588} <= d2_issue_numbers, \
        f"the real re-filed near-dup #501/#588 must still fire: {d2_issue_numbers}"

    # gh#694 exclusion (a): fixture-marked probe pair (#900/#901) — near-identical titles that
    # would otherwise cluster (same Jaccard shape as #501/#588) — must NEVER appear in a D2
    # finding at all.
    assert not ({900, 901} & d2_issue_numbers), \
        f"fixture-marked titles #900/#901 must be excluded from D2 entirely: {d2_issue_numbers}"

    # gh#694 exclusion (b): same-campaign wave siblings (#910/#911, both ADR-0020 wave 2) share
    # enough vocabulary to clear JACCARD_D2 on raw tokens alone — proven by the negative control
    # below — yet must NEVER appear in a D2 finding once the exclusion is wired in.
    wave_a_tokens = _norm_title_tokens("ADR-0020 wave 2: fleet orchestrator seat rollout")
    wave_b_tokens = _norm_title_tokens("ADR-0020 wave 2: build-leader seat rollout")
    assert jaccard(wave_a_tokens, wave_b_tokens) >= JACCARD_D2, \
        "the wave-sibling fixture must genuinely clear JACCARD_D2 on tokens alone — otherwise " \
        "the exclusion test proves nothing"
    assert _same_campaign({"title": "ADR-0020 wave 2: fleet orchestrator seat rollout"},
                           {"title": "ADR-0020 wave 2: build-leader seat rollout"}), \
        "_same_campaign must fire on a shared wave number and a shared ADR-id token"
    assert not ({910, 911} & d2_issue_numbers), \
        f"same-campaign wave siblings #910/#911 must be excluded from D2 entirely: {d2_issue_numbers}"

    # negative control: _same_campaign must NOT fire on two unrelated titles sharing neither a
    # wave number nor an ADR-id token (the exclusion predicate must not be so loose it eats real
    # near-dups too — this is the reverse of the #501/#588 positive control above).
    assert not _same_campaign({"title": "flaky retry timeout sweep guard keeps firing"},
                               {"title": "Fix flaky retry timeout in sweep guard"}), \
        "_same_campaign must not fire on a real near-dup pair with no wave/ADR token at all"

    # _is_fixture_marked — direct unit coverage, including the negative control (a title merely
    # containing "fixture" as a normal English word, not the marker, must not match)
    assert _is_fixture_marked("FIXTURE #890 — D2 near-duplicate probe seed (do not build)")
    assert _is_fixture_marked("some title mentioning we should do not build this yet")
    assert not _is_fixture_marked("Add a fixture-loading helper to the test harness"), \
        "a title merely mentioning 'fixture' as an ordinary word must not match the marker"

    d3 = [f for f in result["findings"] if f["class"] == "D3"]
    d3_kinds = {f["summary"].split(":")[0] for f in d3}
    assert {"rent-growth", "instrument-half-blind", "series-not-firing", "ratchet-unadopted"} <= d3_kinds, d3_kinds

    # gh#645 MAJOR-1: rent-growth must fire PER PLUGIN GROUP, not once for an ungrouped blob —
    # both fixture plugins' routable_chars growth show up as distinct findings.
    rent_growth = [f for f in d3 if f["summary"].startswith("rent-growth")]
    rent_growth_routable = [f for f in rent_growth if "'routable_chars'" in f["summary"]]
    assert any("plugin=demo-plugin)" in f["summary"] and "demo-plugin-two" not in f["summary"]
               for f in rent_growth_routable), rent_growth_routable
    assert any("plugin=demo-plugin-two)" in f["summary"] for f in rent_growth_routable), rent_growth_routable

    # negative-control proof that grouping is load-bearing: the UNGROUPED interleaved series
    # (both plugins' routable_chars in raw file order) is NOT monotonic — if detect_d3 iterated
    # rows ungrouped (the pre-fix bug) it could never find this growth at all.
    at_rows = bundle["metrics"]["attention_trend"]["rows"]
    ungrouped_routable = [int(r["routable_chars"]) for r in at_rows]
    assert not all(ungrouped_routable[i] <= ungrouped_routable[i + 1]
                   for i in range(len(ungrouped_routable) - 1)), \
        f"fixture must exercise the ungrouped-is-not-monotonic case: {ungrouped_routable}"

    d4 = [f for f in result["findings"] if f["class"] == "D4"]
    assert any("entry-file-oversized" in f["summary"] for f in d4), d4

    # every finding: evidence non-empty, artifact+owning_command OR status:unrouted
    for f in result["findings"]:
        assert f["evidence"], f
        assert (f["artifact"] and f["owning_command"]) or f["status"] == "unrouted", f

    # evidence-pointer completeness: every pointer re-opens clean against the real fixture files
    for f in result["findings"]:
        for ev in f["evidence"]:
            ok, why = verify_pointer(ev)
            assert ok, f"{f['id']}: {ev} -> {why}"

    # same-date-row ordering (append order, never date sort) — attention_trend's rows preserve
    # file order regardless of any date value. gh#645 minor-8: the fixture's rows 1-2 (and every
    # subsequent pair) genuinely share the same `date` — this is the real CSV's actual shape
    # (multiple plugins logged the same day), not an untested claim.
    assert [r["routable_chars"] for r in at_rows] == \
        ["10000", "5000", "10300", "5400", "10600", "5900", "10800", "6200"], at_rows
    assert at_rows[0]["date"] == at_rows[1]["date"], "fixture must have a same-date row pair"
    assert at_rows[0]["plugin"] != at_rows[1]["plugin"], at_rows[:2]

    # negative control: an empty bundle -> zero findings
    empty_bundle = collect_mod.collect(Path(__file__).resolve().parent, memory_dir=None,
                                        issues_path=None, window_days=90, now="2026-08-25")
    empty_result = detect(empty_bundle, window_days=90, now="2026-08-25")
    assert empty_result["findings"] == [], empty_result["findings"]

    # determinism
    result2 = detect(bundle, window_days=3, now="2026-08-25")
    assert [f["id"] for f in result["findings"]] == [f["id"] for f in result2["findings"]]

    print("detect.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("target", nargs="?")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--window-days", type=int, default=None)
    ap.add_argument("--now")
    ap.add_argument("--out")
    ap.add_argument("-h", "--help", action="store_true")
    args = ap.parse_args()

    if args.help or args.target is None:
        print(__doc__)
        return 2
    if args.target == "selftest":
        return selftest()

    if args.verify:
        p = Path(args.target)
        if not p.is_file():
            print(f"detect.py --verify: findings file not found: {p}", file=sys.stderr)
            return 2
        return do_verify(p)

    p = Path(args.target)
    if not p.is_file():
        print(f"detect.py: bundle not found: {p}", file=sys.stderr)
        return 2
    bundle = json.loads(p.read_text(encoding="utf-8"))
    result = detect(bundle, window_days=args.window_days, now=args.now)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"detect.py error: {e}", file=sys.stderr)
        sys.exit(2)
