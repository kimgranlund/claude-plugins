# Behavioral assertions (Phase 2)
1. The report contains a **probe evidence block** — the script's JSON (or the named prose-probe
   fallback) with real measured numbers (load, indexer CPU, process counts, worktree census),
   never invented figures.
2. Every finding row carries ALL FIVE fields: measured number · mechanism (why it hurts) · THE
   fix command · severity (high/med/low) · warning tier (safe / needs-sudo /
   changes-system-behavior).
3. The audit performs **zero mutations** — no fix command is executed by the skill; sudo-tier and
   behavior-changing commands are printed for the user with their warnings.
4. Non-macOS hosts get a named honest gap ("probes unverified on this platform"), never
   improvised equivalents presented as verified.
5. A healthy host yields a short all-clear report (the measured numbers + "no action"), never a
   padded checklist of unnecessary fixes.
