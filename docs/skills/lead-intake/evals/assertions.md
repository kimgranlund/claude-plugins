# lead-intake — behavioral assertions (Phase 2)

Checked with/without in Phase 5's behavior check. "The session" = a session that ran /lead-intake.

1. **Adoption acknowledgment:** immediately after /lead-intake, the session's reply contains a
   standing acknowledgment naming (a) the adopted contract file, (b) the three host deltas, and
   (c) the duration rule — before any seed is processed.
2. **Record contract:** a raw bug report given to the session ends in a durable record on the
   resolved backend, and the reply carries the verdict line ("N records minted, M blocked") plus
   the per-record line (id/URL · kind · status · named gaps) — not an investigation, not a fix.
3. **Clarify discipline:** a genuinely ambiguous seed gets exactly ONE batched AskUserQuestion
   round before capture; a clear seed gets zero rounds; a still-vague seed after the round is
   captured with gaps named — never stalled, never re-asked.
4. **Intake-only held:** an ask to build/fix/investigate inside the session is declined with the
   named resume pointer (/build-feature <id>, or /file-bug <id> for the investigation half) —
   the session never dispatches a build or investigation itself.
