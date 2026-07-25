# Behavioral assertions — plugin-install-facts (Phase 2, 2026-07-25)

Checked with/without the skill in Phase 5 against the same prompts as `baseline/`.

1. **Exact syntax, cited.** Every install answer gives the verbatim verified command form(s)
   for the chosen channel and cites the corpus file it came from — never an improvised or
   npm-style-guessed command.
2. **Channel routed by situation.** When more than one channel fits, the answer picks via the
   decision table (e.g. SSH `git@` over HTTPS per the 2026-07-22/25 host-flakiness ruling;
   local path for plugin development; marketplace for multi-plugin distribution) and says why
   in one line.
3. **Preconditions in order.** Any command with a precondition (marketplace add before plugin
   install, trust prompt on first use) appears as an ordered sequence, never a lone command
   that fails cold.
4. **Invented forms corrected.** A prompt presupposing a nonexistent form (e.g. bare
   `npm install <plugin>` as a Claude Code plugin install) is corrected to the real channel,
   not echoed.
5. **README sections copy-pasteable.** A generated README install section has one fenced,
   runnable block per supported channel, ordered most-common-first.
