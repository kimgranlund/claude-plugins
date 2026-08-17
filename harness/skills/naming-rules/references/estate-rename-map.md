# Estate rename map — the paradigm applied at scale (worked example, 2026-07-20)

> **Amendment, 2026-07-26 (issue #97):** this is the map as PLANNED, and execution later drifted
> from it — ADR-0008 merged color, typography and design-systems into `design` (this file still
> says "keep color", "keep typography", `design-kits`), and three member names landed differently
> (`make-design-kit` shipped as `make-design-system`, `design-kit-checker` as
> `design-system-checker`). Treat this file as the historical record of the DECISION, not as a
> lookup table for what shipped. The executed mapping is `renames.json`, derived from git
> rename detection by `fix_old_names.py derive` — moved from `harness/` to `authorkit/` 2026-08-14
> (issue #197, ADR-0011/D9); this file's own citation predates that move.

Status: **fully ruled 2026-07-20; ratification pending ADR-0006.** This is the full-estate
review that motivated `naming-rules` — 9 plugins, ~130 members, mapped from the legacy grammar
to the simple paradigm. Every row has a human ruling (the four originally-open rows were ruled
2026-07-20: `checking-rules`, the chore family, `agent-residency-facts`, `break-down-*`).
Executing the map is governed by ADR-0006 (the rename campaign); names are APIs until it is
accepted. Kind letters: C command · P procedural · K knowledge · A agent.

## Findings that motivated the paradigm

1. One "check" concept spelled four ways — review / audit / verify / judge — across ~20 names;
   zero names use "check".
2. One "make" concept spelled five ways — 12 `-forge` names plus `-design`, `-author`, `build`,
   `-compose` — with the plugin itself named forge (lore doubled).
3. `decompose` carries two unrelated meanings: decide-whether-to-split (`skill-decompose`,
   `plugin-decompose`) vs two-axis analysis (`system-`/`layout-`/`flow-decompose`).
4. Three runnables with no verb: `build`, `feature`, `issue`.
5. Four skill↔agent twins sharing one literal name: `ops-issues`, `ops-planner`,
   `ops-orchestrator`, `orchestration-coordinator`.

## Plugin layer (settled with the user, 2026-07-20)

| Now | Paradigm name |
|---|---|
| forge | `harness` |
| scribe | `docs` |
| orchestration | `teamwork` |
| ui | `screens` |
| color | `color` (keep) |
| typography | `typography` (keep) |
| design-systems | `design-kits` |
| agentic-ui | `agent-protocols` |
| llm | `llm` (keep — term of art; the `llm-facts`/`llm-protocols` candidates ratified OUT by ADR-0006: each stutters against every member, and the stutter exception (ADR-0006 Decision 7) covers the kept name) |

## forge → harness

| Now | Kind | Paradigm name |
|---|---|---|
| skill-forge / agent-forge / hook-forge / plugin-forge / pack-forge / script-forge | P/C | `make-skill` / `make-agent` / `make-hook` / `make-plugin` / `make-pack` / `make-script` |
| skill-review / skills-audit / agents-audit / harness-audit / entry-file-audit / eval-run | P/C | `check-skill` / `check-all-skills` / `check-all-agents` / `check-everything` / `check-entry-file` / `check-routing` |
| skill-decompose / skill-synthesize / plugin-decompose / skill-refactor | P/C | `plan-skill-split` / `plan-skill-merge` / `plan-plugin-split` / `reshape-skill` |
| plugin-release / repo-alignment / plugin-onboard | C | `ship-plugin` / `clean-repo` / `adopt-plugin` |
| system-decompose / intent-extract / knowledge-harvest / handoff-compose / open-questions-sweep | P | `break-down-problem` / `find-the-ask` / `save-lessons` / `write-handoff` / `find-open-questions` |
| ops-issues / ops-planner / ops-orchestrator (commands) | C | `sort-issues` / `plan-chores` / `sweep-chores` |
| skill-/agent-/hook-/pack-/plugin-/script-authoring-standards | K | `skill-/agent-/hook-/pack-/plugin-/script-writing-rules` |
| entry-file-standards / linguistic-techniques / reasoning-orders / reviewer-discipline / git-campaign-workflows / github-issue-pr-primitives | K/P | `entry-file-rules` / `prompt-wording-rules` / `thinking-depth-rules` / `checking-rules` / `big-change-git-rules` / `github-facts` |
| skill-auditor / agent-reviewer / hook-reviewer / plugin-reviewer / linguistics-reviewer / eval-judge / pack-researcher | A | `skill-checker` / `agent-checker` / `hook-checker` / `plugin-checker` / `wording-checker` / `routing-judge` / `fact-finder` |
| ops-repo / ops-adr / ops-issues / ops-planner / ops-orchestrator | A | `repo-cleaner` / `decision-watcher` / `issue-sorter` / `chore-planner` / `chore-lead` |

## scribe → docs

| Now | Kind | Paradigm name |
|---|---|---|
| doc-forge / doc-review / doc-authoring-standards | P/K | `make-doc` / `check-doc` / `doc-writing-rules` |
| bug-report / feature / issue / docs-alignment | P/C | `file-bug` / `file-feature` / `file-task` / `tidy-docs` |
| llms-txt-forge / reference-forge / rubric-forge / vision-memo-forge | P | `make-llms-txt` / `make-reference` / `make-rubric` / `make-vision-memo` |
| research-methods / html-to-markdown / markdown-to-markup | K/P | keep — already literal |
| doc-reviewer / researcher | A | `doc-checker` / `experiment-runner` |

## orchestration → teamwork

| Now | Kind | Paradigm name |
|---|---|---|
| build / orchestration-coordinator (cmd) / session-close | C/P | `build-feature` / `leading-teams` / `close-session` |
| orchestration-design / loop-design / concurrency-design / intent-grill | P | `team-or-solo-rules` / `loop-rules` / `parallel-work-rules` / `grill-the-ask` (overlaps forge's `find-the-ask` — merge candidate) |
| orchestration-coordinator / system-planner / system-builder / code-reviewer / orchestration-reviewer / docs-writer | A | `team-lead` / `planner` / `builder` / `code-checker` / `wiring-checker` / keep `docs-writer` |

## ui → screens

| Now | Kind | Paradigm name |
|---|---|---|
| component-forge / layout-decompose / flow-decompose | P | `make-component` / `break-down-layout` / `break-down-flow` |
| focus-/i18n-/perf-/safety-verify / ui-audit / ui-change-verify | P | `check-focus` / `check-translations` / `check-speed` / `check-safety` / `check-whole-ui` / `check-ui-change` |
| ui-genres / ui-patterns / dom-block-flow / geometry-systems / mobile-hig-patterns / motion-design | K | `ui-genre-facts` / `ui-pattern-facts` / `dom-layout-facts` / `size-and-shape-rules` / `apple-mobile-facts` / `motion-rules` |
| component-/flow-/layout-reviewer | A | `component-/flow-/layout-checker` |

## color · typography · design-kits · agent-protocols · llm-facts

| Now | Kind | Paradigm name |
|---|---|---|
| palette-design / color-verify / color-science-{perception,spaces,materials,accessibility} / color-theory | P/K | `make-palette` / `check-colors` / `color-{perception,space,material,contrast}-facts` / `color-theory-facts` · `token-builder` (A) keep |
| typography-system-design / typography-tokens / typography-lettering / typography-system-reviewer | P/K/A | `pick-fonts` / `font-token-rules` / `lettering-facts` / `font-choice-checker` |
| design-system-hub / -author-{dscard,figma-make,google-stitch} / design-md-format / iconography / figma-plugin-api / material-design-*-tokens / design-system-reviewer | P/K/A | `make-design-kit` / `make-{dscard,figma-make,stitch}-kit` / `design-md-rules` / `icon-rules` / `figma-plugin-facts` / `material-{color,shape,motion,type,token}-facts` / `design-kit-checker` |
| a2a-agent-design / a2a-isolation-verify / a2a+a2ui knowledge ×6 | P/K | `make-a2a-agent` / `check-a2a-isolation` / `a2a-/a2ui-{protocol,training,catalog,chat-agent}-facts` |
| agent-residency-taxonomy / chat-harness-* ×6 / llm-jsonl-streaming / llm-provider-gateway | K | `agent-residency-facts` / `chat-harness-{guardrail,memory,logging,workflow,routing,tool}-facts` / `llm-streaming-facts` / `llm-gateway-facts` |

## Rulings closing the originally-open rows (2026-07-20, one batched round)

- reviewer-discipline → `checking-rules` (activity-carrying `-rules`, over `checker-rules`).
- Ops family → the chore family: agents `repo-cleaner` / `decision-watcher` / `issue-sorter` /
  `chore-planner` / `chore-lead`; commands `/sort-issues` / `/plan-chores` / `/sweep-chores`.
- agent-residency-taxonomy → `agent-residency-facts` (sober `-facts` shape over the cuter
  `where-agents-live`).
- Analysis-sense decompose trio → `break-down-problem` / `break-down-layout` /
  `break-down-flow` (wordy but unmistakable; `map-*` rejected for the sitemap/roadmap
  collision).
