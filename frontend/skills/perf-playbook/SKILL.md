---
name: perf-playbook
description: >-
  Fix one page fully, write the playbook, then fan the fixes out to every other page without
  fresh reports. Use when the user asks to "apply the perf fixes to all pages", "roll this out
  across the site", "same fixes on the other routes", "write down what we changed so it can be
  repeated": one entry per fix (audit id, cause, files, verify command, shared vs page-local),
  remaining pages handled in parallel with disjoint files, each ending with lh-diff. NOT for
  the first page's own fix loop (perf-loop); NOT for the route inventory, scoreboard, or
  budgets (perf-sweep).
disable-model-invocation: false
user-invocable: true
---

# perf-playbook, one page fully, then fan out

The only thread with a verified multi-page procedure (1tfjlbk's linked source) did it in two
phases: fix one page against its report until the score was good, ask the model to "write down
everything we changed into a .md file", then give the remaining pages plus that file, with no
fresh report, and the instruction "use this as a checklist, don't redo shared stuff that was
already fixed." This skill is that procedure with the record made explicit.

## Procedure

1. **Phase 1, one page.** Run `perf-audit` on the page with the most shared surface (the
   shell, the layout, the bundle every route loads), `perf-triage` for the brief, and
   `perf-loop` until it is green. Every iteration appends an entry to
   `perf-playbook.md` (template: `assets/perf-playbook.template.md`), one per fix:
   - issue: the audit id and the item the report named;
   - cause in this codebase: the file or config that produced it, in the source, not the
     build output;
   - files touched;
   - how to verify: the exact command (usually `lh-diff` against the page's before-report, or
     a curl for a header);
   - shared vs page-local: shared means every route inherits it (headers, bundler config, the
     shell component); page-local means the fix lives in that page's own markup or assets.
2. **Phase 2, fan out.** Give each remaining page plus the playbook to a worker. No fresh
   Lighthouse report per page at this stage ("w/o PSI report"); the playbook is the checklist.
   The instruction to each worker: use the playbook as a checklist, do not redo shared fixes,
   apply page-local ones where the page has the same pattern, record anything new as a new
   entry with `shared: no`.
3. **Parallel by page, disjoint files.** One subagent or one worktree per page; the file sets
   must not overlap (shared files were already fixed in phase 1 and are off limits in phase 2).
   Two workers editing one shared file is the failure the phase split exists to prevent.
4. **Each page ends with `lh-diff`** against its own before-report (run `perf-audit` on the
   page before its worker starts; the after-run comes from the worker). A page with no
   before-report has no gate and is not done.
5. **Merge the playbook** entries from every worker back into one file; a fix two workers
   both recorded is a shared fix that was missed in phase 1, promote it.

## Caveats named, not adopted

- The linked source reports "Opus created three subagents by itself", "15 minutes later they
  had touched 41 frontend files", and "Basically perfect Lighthouse numbers again." No commit
  log, trace, or per-page score set is attached; the counts are the author's claim. The
  procedure is adopted, the numbers are not a target.
- The playbook's own content in that thread is not shown ("specific content and structure… are
  not detailed"); the entry shape here comes from the author's description of what it
  recorded ("what the issue was, what caused it in my codebase, what files were touched, how to
  check it after") plus this repo's shared/page-local field.

## Done

A merged `perf-playbook.md` with one entry per fix, every remaining page gated by its own
`lh-diff` exit 0, and no shared file touched in phase 2. NOT done: pages "fixed" from the
checklist with no before-report, or a playbook that lists changes without the verify command.

## Provenance

- 1tfjlbk (r/ClaudeWorkflows, bot-generated post) and its linked first-person source
  (r/ClaudeAI 1tfgq66, "Opus is ridiculous for frontend cleanup"): "I took one page, ran it
  through PageSpeed Insights", "pasted all the PSI issues into Opus", "fixed them one by one
  until the score was good", "asked Opus to write down everything we changed into a .md file",
  the record shape "what the issue was, what caused it in my codebase, what files were touched,
  how to check it after", "I gave Claude (w/o PSI report) all other frontend pages in repo +
  that playbook", "use this as a checklist, don't redo shared stuff that was already fixed".
  Unverified: three subagents, about 15 minutes, 41 files, the exact scores on the remaining
  pages, the prompts.
- 1taw297 (r/ClaudeCode), commenter: "Run audits from a no context session from a blind
  worktree", the isolation this skill's phase 2 borrows for its workers.
- The disjoint-files rule, the per-page before-report requirement, and the shared/page-local
  field are this repo's additions.
