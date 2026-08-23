# Audit — `cross_repo_coordination` participants[] migration (issue #878)

Skill: `teamwork/skills/fleet-bootstrap` · Standards: skill-writing-rules · Lint: clean
(`skill-postwrite-invocation-lint · clean · SKILL.md`)
Verdict: **PASS with findings** (1 MAJOR, 1 MINOR — no blocking finding; nothing crashes, nothing
mis-lints, the shipped runtime paths in `SKILL.md` are internally consistent)

Scope: targeted semantic-edit review of the `repos[]`/`marshal_roles[]` → `participants[]` shape
change across `references/fleet-manifest-schema.md`, `SKILL.md` Phase 0, and this repo's own
`.claude/ops/fleet.json`.

| ID | Verdict | Severity | Evidence (file:line) | Fix |
|----|---------|----------|----------------------|-----|
| S1 — example ↔ Fields agreement | PASS | — | `references/fleet-manifest-schema.md:37-49` (illustrative JSON) matches the `participants[]` shape documented at `:177-186` field-by-field (`repo`/`app`?/`role`); the 4-participant example (2 repo-scoped + 1 app-scoped pair) is reused consistently | none |
| S2 — retirement language | PASS | — | `references/fleet-manifest-schema.md:204-207`: "The old `repos[]`/`marshal_roles[]` pair is **retired, not kept as an alias**... never a mixed fleet where some copies read the old shape and some the new" — unambiguous, no aliasing claimed | none |
| S3 — collision-rule precision | **FAIL** | **MAJOR** | `references/fleet-manifest-schema.md:209-218` ("Two-holder liveness rule") cites "the existing one-live-holder-per-role collision rule (the `live_state.joined[].action` liveness field, above)" as the mechanism now scoped to "the `(role, app)` pair." But (a) `live_state.joined`'s own schema (`:106-120`, same file) has **no `app` field** anywhere, and `SKILL.md`'s own bind-collision check, Phase 1 step 1 (`SKILL.md:69-76`), still tests only "a still-live `agent` entry" with zero app-scoping — so if this rule means to extend that mechanism, nothing in this edit actually wires the extension; a `signup-marshal` session binding adiav2's `agent` seat via `/fleet-bootstrap` would still be treated as a takeover of `adiav2-marshal`'s seat by the unmodified Phase 1 logic, contradicting this new rule's own claim that the two are "not a collision." (b) The rule's collision formula itself doesn't type-check against the schema it's actually attached to: the participant object's own `role` field is defined two paragraphs up (`:183-186`) as the **session name** (`"signup-marshal"`, `"adiav2-marshal"`) — necessarily unique per participant — not the seat role-key (`"agent"`) used in `live_state.joined`. "Two participants collide only when both `role` AND `app` match" is therefore either vacuous (two participants sharing a session-name `role` are already the same entry) or silently means something different from what it cites. | Either (1) actually extend `live_state.joined`'s schema with an `app` field and update `SKILL.md` Phase 1 step 1 to scope its collision check by `(role, app)`, and re-word this paragraph to point at the now-real mechanism — or (2) if this rule is meant to govern `cross_repo_coordination.participants[]` bookkeeping only (which has no runtime collision check at all, just append-only), say so explicitly, drop the `live_state.joined[].action` citation, and restate the collision key in terms participants[] actually has (`repo`+`app`, not `role`+`app`) |
| S4 — SKILL.md Phase 0 field names | PASS | — | `SKILL.md:43-55` prints/appends `participants` (each `repo`, `app` when sub-app-scoped, `role`) — matches the new schema exactly, no residual `repos`/`marshal_roles` vocabulary | none |
| S5 — leftover old-shape references | PASS | — | Grepped the skill dir and repo: only hits are the historical "landed at #871/#866... retired" sentence (`references/fleet-manifest-schema.md:198,204`) and the README ledger line describing the migration (`teamwork/README.md:113`) — both intentionally describe the retired shape, not live leftovers | none |
| S6 — illustrative example ↔ live fleet.json fidelity | WARN | MINOR | Doc header (`references/fleet-manifest-schema.md:10-13`) frames the example as "shown populated with this repo's own real standing channel... for concreteness," implying a mirror. `authorized_by` text differs: schema example (`:46`) omits "motivating example gen-ui-kit gh#1836/#1839," present in the live file (`.claude/ops/fleet.json:80`). Free text, non-schema-breaking. | Sync the example's `authorized_by` string to the live file's, or soften the header's "shown populated with this repo's own real standing channel" claim to allow drift |

## Steelman check (checking-rules discipline)

Considered whether S3 is a false alarm: could `participants[].role` plausibly mean the seat
role-key after all? No — `:183-186` defines it explicitly as "the session name authorized to
relay... mirrors the printed orchestrator session name, not the schema's `agent` role key,"
which rules that reading out in the schema's own words. Considered whether `live_state.joined`
gaining an `app` field was simply out of this edit's stated scope (participants[] only): plausible,
but then the paragraph should not cite `live_state.joined[].action` as the rule being extended —
that citation is what creates the false precision. Finding stands.

## Top findings
1. **MAJOR** — S3: the Two-holder liveness rule cites a `live_state.joined` mechanism that was not
   updated (no `app` field, `SKILL.md` Phase 1 unchanged) and its own collision formula doesn't
   match the participant object's own `role`-as-session-name definition. Fix: wire the extension
   for real, or rescope the rule's citation to what participants[] actually has.
2. **MINOR** — S6: illustrative example's `authorized_by` text has drifted slightly from the live
   `fleet.json` it claims to mirror.

Everything else audited (example/Fields agreement, retirement-not-aliased language, SKILL.md
Phase 0 field names, leftover-reference sweep) is clean.
