# The `blocked-by` dependency convention (issue #193)

A minimal, machine-readable way to declare that one ticket can't be built until another closes —
nothing more. Built because this repo already had three edges hand-encoded only in issue comments
(#197 blocked-by #196, #190 serial-after #191, #192/#198 queued behind both) with no convention a
script could read; `mobilize-chores` step 2 and harness's `chore-planner` both need the same fact,
so it is written down once, here — the ONE canonical definition (#193's own acceptance) — rather
than re-derived per consumer. This file states the format and its per-backend realization only;
the two consumers' own read/exclude/order logic lives in their own procedures (`mobilize-chores`
step 2 below, and harness's `blocked-by-rules` skill, preloaded by `chore-planner`), which cite
this file rather than duplicating its authority.

## The format

One body line, anywhere in the ticket's body text:

```
Blocked-by: #196
```

Multiple blockers, comma-separated:

```
Blocked-by: #196, #201
```

- Case-insensitive key (`blocked-by:`, `Blocked-by:`, `BLOCKED-BY:` all match).
- Each value is `#` followed by digits — an issue number on this workspace's git-native backend
  (ADR-0002). On the local backend (Option A), the same `#NN` form cross-references a git-native
  issue; a `TKT-####` form is also accepted where the blocker is itself a local TICKET file.
- Recommended placement: its own `## Blocked-by` section, so a human skimming the issue sees the
  dependency as a first-class fact rather than a phrase buried in `Scope/Open` prose. Not a
  machine requirement — a line living anywhere in the body still greps and still resolves; the
  dedicated section is a courtesy to the next reader, not a parsing rule.
- Hand-editable, hand-removable. Nothing infers this line from PR references, commit text, or
  issue mentions — a human (or an agent editing on a human's behalf) writes it, and removes it
  once the blocker closes. Auto-detection is explicitly out of scope (#193's own non-goals).

## Realization per backend

| Backend | Where the line lives | How a consumer reads it |
|---|---|---|
| **Git-native (Option B)** — this workspace's own ADR-0002 instance | The issue body (`gh issue edit --body`, adding or editing a `## Blocked-by` section) | `gh issue view <id> --json body --jq .body`, grep the `Blocked-by:` line, parse the `#NN` list, then `gh issue view <NN> --json state` per named blocker |
| **Local (Option A)** | The identical line convention, in the TICKET file's own body (not frontmatter — one line format across both backends, not two) | `Read` the file, grep the same line, resolve each `#NN`/`TKT-####` against `docs/tickets/` |
| **External adapter (Option C)** | Not realized today — the same disclosed gap as `doc-writing-rules`' `backend-resolver.md` `discover` primitive on this backend | Report UNMEASURED, naming the resolved adapter; never guessed |

## The two named consumers (no others, per #193's own scope)

1. **`mobilize-chores` step 2** (this skill) — exclusion semantics: that skill's own step 2, above.
2. **`chore-planner`** (harness) — ordering semantics: harness's preloaded `blocked-by-rules`
   skill.

Both cite this file for the format; neither's own read/exclude/order logic is restated here.

## Non-goals (explicit, per #193's own Scope/Open)

No graph tooling, no visualization, no auto-detection. This file is the format's one canonical
definition — a consumer's own procedure cites it, it never re-defines a second, competing shape.
