# intent — plugin-onboard
status: shipped
species: procedural
dials: { disable-model-invocation: false, user-invocable: true }
freedom: medium
type: capability-uplift

## trigger
should:
  - "add this plugin to the repo so contributors can install it"
  - "declare this plugin marketplace in settings.json"
  - "how do I set up extraKnownMarketplaces"
  - "onboard this list of plugin/skill URLs"
  - "wire up these external skills as a plugin dependency"
should_not:
  - "change the default model / a permission / an env var in settings.json" (→ update-config)

## delta
Without this skill, Claude reliably gets three things wrong when asked to declare an external
plugin in a consuming repo's `.claude/settings.json`:
1. It assumes `extraKnownMarketplaces` can point at any plugin repo, and produces a broken
   entry for a single-plugin repo that has no `.claude-plugin/marketplace.json` of its own
   (confirmed failure mode: `mattpocock/skills`, alex-prds PR #2365 commit e3561c8cc).
2. It guesses the `enabledPlugins` key as `<repo-name>@<marketplace-id>` instead of reading the
   plugin's own manifest `name` field — the plugin silently never appears in `/plugin`.
3. It omits `path`/`sparsePaths` for marketplaces whose `marketplace.json` isn't at the repo
   root, and forgets `/reload-plugins` is required for anything but a live SKILL.md edit.
Deleted after a month: settings.json entries for new plugin URLs would again need manual
per-case reasoning about which of the two declaration shapes applies.

## fences
- NOT for authoring a NEW plugin's own manifest/structure (`plugin-authoring-standards`)
- NOT for general non-plugin settings.json edits — permissions, env vars, hooks, model choice
  (`update-config`, external skill)
- NOT for building a plugin's actual skills/agents content (`plugin-forge`)
- NOT for deciding how an existing local surface should partition into plugins
  (`plugin-decompose`)

## assertions
1. Every produced `extraKnownMarketplaces` entry has a `source` object with a valid `source`
   type (`github` | `git` | `directory`) and the subkeys that type requires.
2. A single-plugin repo (no root `marketplace.json`) is never given a direct
   `extraKnownMarketplaces` entry — it is added to a self-hosted wrapper catalog's `plugins[]`.
3. Every `enabledPlugins` key is `<plugin-name>@<marketplace-id>`, with `<plugin-name>` read
   from that plugin's own `plugin.json`/`marketplace.json` entry, never assumed from the URL.
4. The output names the verification step (`/reload-plugins`, `/plugin`,
   `installed_plugins.json`) so a silent misconfiguration doesn't read as "done".

## gates
P0 route:      PASS — knowledge/procedure needed on demand, not a mechanical hook check, not an
                always-true project fact, no tool-wall/parallelism need for an agent. 2026-07-15.
P1 intent:     PASS — all slots filled from the requesting conversation (a live campaign example,
                a verified generic write-up already produced and reviewed inline); user asked
                directly for this skill in forge, confirming intent without a separate interview
                round (interview.md: "skip any slot the user's opening request already answers").
                2026-07-15.
P2 evals:      PASS — evals/evals.json authored; baseline captured via a fresh no-skill agent run
                (see rulings). 2026-07-15.
P3 draft:      PASS — SKILL.md drafted from the Procedural skeleton, 134 lines. 2026-07-15.
P4 language:   PASS — potency_lint.py: prohibitions 11→3 (budget 5), NEVER 6→3 (budget cap,
                exactly at the line — the three load-bearing invariants: no-inline-marketplace
                fact, single-plugin-must-wrap gate, plugin-name-never-guessed gate); all other
                categories 0. 2026-07-15.
P5 validate:   PASS — lint clean; skill-auditor (FLOOR) fresh-context review: PASS, zero
                blocking findings, R1-R8 all cite evidence, all 4 sibling fences verified
                real by reading the sibling skills (not just trusting the declared NOT-for
                clauses). Two non-blocking notes, both fixed same-session: (1) the
                `update-config` fence qualified as "the separate skill, where installed" —
                it is not a forge-corpus sibling; (2) behavior check completed — see below.
                2026-07-15.

## rulings
- Baseline (Phase 2, live run 2026-07-15): dispatched a fresh general-purpose agent with no
  skill context, asked to make `mattpocock/skills` (single-plugin repo, no marketplace.json)
  installable via settings.json. It did NOT merely guess a direct `extraKnownMarketplaces`
  entry — it fabricated a nonexistent `"source": "settings"` inline-marketplace type with a
  `plugins[]` array nested inside the marketplace source object, invented wholesale and
  presented with full confidence ("documented under extraKnownMarketplaces in the settings
  reference" — it is not). Sharper evidence than the predicted delta: the failure mode isn't
  only "picks the wrong of two known shapes", it's "invents a plausible-sounding third shape
  that doesn't exist." Confirms assertion 2 is load-bearing, not a nicety. Transcript: agent
  a2713708957032e3c, this session.
- Name: `plugin-onboard` chosen over `marketplace-declare` to match this plugin's existing
  `plugin-<verb>` family (`plugin-decompose`, `plugin-forge`, `plugin-release`) rather than
  introducing a new `marketplace-` domain prefix for a single skill.
- With-skill behavior check (Phase 5.3, live run 2026-07-15): dispatched a fresh
  general-purpose agent carrying the full SKILL.md body verbatim as its only procedure, given
  the identical `mattpocock/skills` onboarding task from the baseline run. It did NOT
  reproduce the fabricated `"source": "settings"` shape — it followed step 1's fetch-before-
  classify instruction, discovered the repo now carries a real `marketplace.json` (a genuine
  drift from when the baseline/campaign evidence was gathered), correctly re-routed to step 2
  instead of step 3, and reported the discrepancy against the task's premise rather than
  silently complying with a stale assumption. Assertion 1 and the fetch-first discipline both
  demonstrated with the skill; assertion 2 (never-guessed plugin-name) demonstrated by the
  correct `mattpocock-skills@mattpocock` key, read from the fetched manifest.
- Self-caught staleness (same run): the live re-check also proved the shipped SKILL.md's own
  Example section was citing `mattpocock/skills` as a single-plugin-repo illustration that had
  since become inaccurate — fixed in the same change by genericizing the example to a
  placeholder repo and adding one sentence naming classification as a live fetch, never a
  cached label. Left as evidence that this skill's own "verify, don't assume" discipline
  applies to itself, not only to what it teaches.
