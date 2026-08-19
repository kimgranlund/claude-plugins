# Refresh procedure — keeping a shipped artifact from going stale

The question this file answers: **once an Artifact/report page is built and shipped, how does it
get refreshed when its sources change — and how would anyone even notice it's gone stale?** This
resolves #619 Scope/Open item (d), naming the Estate Handbook's own maintainer mechanism.

## The provenance footer — the machine-readable interface a refresh reads

Every artifact page `make-artifact` emits carries a **provenance footer** naming:

1. The source DESIGN.md path (and/or tokens.json path) it was built from — or, when no design
   system was found (lld-0013 v2 Resolution 9), the state instead: **SYNTHESIZED** (with the
   generator line naming which `design` skills produced it), or **none — doctrine-neutral
   fallback** (naming the gap explicitly: "install the design plugin to synthesize one"). Never a
   silent absence of this line, whichever of the three states applies.
2. The tokens.json `$generator` line (verbatim), when tokens.json was an input.
3. The content source (path or description) it was assembled from — or, when the composition phase
   degraded to the prose-draft path over a non-canonical records tree (`composition-model.md`'s
   Degradation section, R-6), that degradation named explicitly.
4. The build date.
5. The exact `css_build.py` invocation used to produce the CSS — so any reader, human or agent,
   can re-run the identical build.

This is the whole mechanism: staleness is *detectable* (a reader compares the footer's named
source paths' current state against what the footer recorded) without any automation watching
the page.

## The refresh trigger

Re-run `/make-artifact` against the **current** DESIGN.md/tokens.json and **current** content —

- at each release boundary of the source design system (a new tokens.json/DESIGN.md version), or
- whenever the source content (the report/handbook prose itself) changes.

This is the same doctrine this workspace's own CLAUDE.md already states for every other kind of
snapshot ("stale context is a defect, equal in severity to a bug"; "sources of record flow
outward… snapshots refresh FROM them at release boundaries") — an artifact page is a snapshot of
a design system + content, and this procedure is that doctrine applied to this one artifact
class, not a new rule invented for it.

## Explicitly NOT a hook

Hooks are fully retired in this workspace (the remove-all-hooks directive, #466, 2026-08-17).
Even if they were not, a hook could at best **nag** that a source changed — it could never
perform the rebuild itself (assembling a shell, choosing narrative-vs-tabbed, re-running
`css_build.py`, stamping a fresh footer all take judgment a hook cannot carry). The refresh is
therefore a **named procedure a human or a dispatched session runs**, not automation: the
provenance footer is what makes the trigger detectable; re-running `/make-artifact` is the whole
refresh.

## The Estate Handbook's own refresh

Resolves #619 (d): the Estate Handbook's refresh mechanism is exactly this procedure — re-run
`/make-artifact` with the inputs its own current provenance footer names, whenever the design
system or the handbook's content changes. No separate, handbook-specific mechanism is needed or
built; the general procedure above already covers the specific case that motivated it.
