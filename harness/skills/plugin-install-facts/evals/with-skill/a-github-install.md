# With-skill A — 2026-07-25

Two commands, in order, from `references/install-commands.md`:

```
/plugin marketplace add owner/repo
/plugin install <plugin-name>@<marketplace-name>
```

Concrete example (same file): `/plugin marketplace add kimgranlund/claude-plugins` then
`/plugin install harness@nonoun-plugins`.

Preconditions and failure modes that bite next:

- There is no one-step install from a repo URL — a plugin always installs FROM a marketplace,
  so the repo must be added as a marketplace first (Step 1) before `/plugin install` (Step 2)
  can resolve it.
- The GitHub repo must contain a `.claude-plugin/marketplace.json` at its root. A bare
  single-plugin repo without one needs a wrapper catalog — that's a separate job
  (`adopt-plugin`), not this install flow.
- `<plugin-name>` in Step 2 is the manifest's `name` field — never guess it from the repo or
  URL.
- First use of a new marketplace/plugin source prompts for trust (installing runs code) —
  expect and confirm it.

`/plugin market` ≡ `/plugin marketplace` if you want the short form.
