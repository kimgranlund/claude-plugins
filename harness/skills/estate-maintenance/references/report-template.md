# Estate maintenance report — template + `findings.json` schema

Verdict-first, findings table, then the diff bundle and ticket list. Nothing lands in the repo
until Phase 5's confirm — Phase 4 renders all three artifacts to the session scratchpad only.

```markdown
# Estate maintenance retrospective — <root> — <date>

🟢/🟡/🔴 <one-sentence verdict: the single most load-bearing finding, or "nothing over the bar">

## Findings
| id | class | severity | evidence | artifact | owning command | size |
|---|---|---|---|---|---|---|
...one row per finding, `status` shown only when not `proposed`. A finding with neither artifact
nor owning_command renders `status: unrouted` in the size column instead of a size value — never
silently dropped.

## Unmeasured
One line per absent registered input and its reason (never rendered as zero or skipped silently).

## Diff bundle
One unified diff per `size: diff` finding, headed by its finding id and target path. Capped at
8 (R-5); remainder rendered as ticket lines below instead.

## Ticket list
One `file-bug`/`file-feature`/`file-task` line per `size: ticket` finding — named, never minted
here (Procedure Phase 4).

## Confirm
The AskUserQuestion payload as posed (interactive) or the held-items entry filed (unattended,
Resolution e §2) — recorded verbatim so a later reader can see exactly what was offered.
```

## `findings.json` schema

```json
{
  "run": {"date": "2026-08-18", "root": "/abs/path", "window_days": 90},
  "findings": [
    {
      "id": "D1-1",
      "class": "D1 | D2 | D3 | D4 | J-generalization | J-root-source",
      "severity": "blocking | major | minor | nit",
      "summary": "one sentence, the class + the concrete numbers that fired it",
      "evidence": [
        {"path": "/abs/path", "locator": "line:N | lines:N | csv-row:N | issue:NNN", "quote": "..."}
      ],
      "artifact": {"path": "/abs/path", "kind": "memory-entry | issue-pair | trend-csv | entry-file | context-surface-census"},
      "owning_command": "the one command/seat that owns the fix, or null with status:unrouted",
      "proposed_diff": "unified diff text, or null (Phase 4 fills this for size:diff findings)",
      "size": "diff | ticket",
      "status": "proposed | confirmed | applied | queued | declined | unrouted"
    }
  ],
  "fix_clusters": [
    {"members": [{"kind": "issue | memory | decision", "ref": "#NNN | /path | adr-NNNN", "title": "..."}],
     "shared_tokens": ["..."]}
  ],
  "unmeasured": [{"input": "memory | issues | attention_trend | recurrence_trend | cost_ledger | rent | adr_queue | revalidation_queue | plan", "reason": "..."}]
}
```

Locator schemes (`detect.py --verify` re-opens every one of these mechanically — never re-derived
by eye):

- `line:N` — line N (1-based) of a text file must contain `quote` as a substring.
- `lines:N` — the file has exactly N lines (a whole-file line-count assertion, valid for the run
  it was computed in — a proxy metric, not a stable long-term citation).
- `csv-row:N` — the Nth data row (1-based, excluding header, file order) of a CSV must render
  `quote` somewhere among its cells.
- `issue:NNN` — issue number NNN in the issues JSON at `path` must exist with `quote` as a
  substring of its title.

`class` values `J-generalization`/`J-root-source` are Phase 3's own additions (the judgment
layer) — `detect.py` emits only `D1`-`D4`; a run's final `findings.json` (post-Phase-3) may carry
either class appended by the session, never by the script.
