# Baseline — clean session, no skill installed

## Setup
A session did read-only exploration and answered questions; nothing was changed, nothing is
uncommitted, no finding or follow-up surfaced. Prompted with the same prior phrasing: "write any
new issues or PR otherwise prepare to close this session."

## Observed behavior (no skill)
Claude, reading "write any new issues or PR" as an instruction to comply with rather than a
condition to check, manufactures a low-value Issue summarizing the session's own Q&A — because the
prompt's "otherwise" branch ("prepare to close") reads as the fallback for *nothing to write*, and
writing *something* felt like the safer way to satisfy the literal ask.

## Gap this baseline demonstrates
The old prompt has no way to represent "genuinely nothing to capture" as a valid, first-class
outcome — it either writes something (even manufactured) or is silent about having checked at
all. A materiality floor is missing entirely.
