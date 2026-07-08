---
name: safety-verify
description: Reason about and verify blast radius, reversibility, and friction for every destructive or high-consequence action a UI exposes — the UI safety layer. Use for destructive verbs a product ships (delete/send/publish/revoke) — undo over confirm, type-to-confirm for irreversible, bulk preview/dry-run, audit-trail UX, recall windows, re-auth, two-person approval, and destructive-default posture — when under-specified, dialogs proliferate, or recovery is missing. NOT for the whole-product sweep (ui-audit); NOT for cross-screen recovery (flow-decompose); NOT for text/background contrast, palette, or color-blind safety (color-verify); NOT for focus order, keyboard nav, hit-targets, or focus rings (focus-verify); NOT for RTL/bidi, locale Intl formatting, or text-expansion (i18n-verify); NOT for loading skeleton/spinner, CLS, or latency budgets (perf-verify); NOT for color-space theory or palette math (color-science-spaces); NOT for prompt-injection/authz design; NOT for a confirm-dialog component (component-author).
disable-model-invocation: false
user-invocable: true
---

# safety-verify — destructive-action invariants, card-gated

Owns the trust layer of a product UI: every action has a (blast radius × reversibility)
coordinate, and its friction is a function of that coordinate — not of anxiety. The verify
contract: **declare each action's coordinate and friction in a card → the checker gates the
coordinate-friction arithmetic → judgment covers only what code cannot see** (whether the blast
was counted honestly, whether the recovery path is real).

## The card

A **destructive-action card** (`*.action.json`) declares one action's coordinate and friction:
`name`, `verb`, `blast_radius: low|medium|high|critical` (a COUNT — affected entities and
observers — not an adjective), `reversibility: instant|session|minutes|days|irreversible` (a
DURATION, not a boolean), `has_confirm`, `confirm_type: type-to-confirm|reauth|confirm|click|none`,
`has_undo`, `ops_reversible` (the reversal is an ops/support process — the ops-reversible species
below), `has_audit_event`, `bulk`, `has_preview`, `default_focus: cancel|destructive`. If no
inventory exists, enumerate every mutating verb from the codebase (delete, send, publish, invite,
revoke, …) — an action with no coordinate cannot be placed on the plane, and that is the first
finding. The card never carries the judgment tier: an honest blast COUNT and the reality of the
recovery path are step-3 judgment — `blast_radius` declares a coordinate, it cannot attest its
own honesty.

## Procedure

1. **Enumerate** the actions; build one card per action with its coordinate.
2. **Gate:** `python3 scripts/safety-check.py <card.json | dir>` — a FAIL blocks the emit; fix the
   surface, not the card. `selftest` proves the checker itself.
3. **Judge what the checker can't:** was the blast radius *counted* honestly (`self,1` ≠
   `org,10k`)? Does the confirm copy name a truthful consequence? Is the recovery path real or a
   flag set to `true` on paper? Is the audit event *surfaced* to the user or merely logged? Does
   type-to-confirm name the resource, not the user's email?
4. **Emit** the verdict — every violation cites the action/affordance it evaluates and routes its
   fix to the artifact that can make it — plus per-action treatments where asked:
   `{action, treatment, recallWindowS, reauthWindowMin, auditEvent}`.

## Invariants (the numbers)

| Invariant | Value | Source |
|---|---|---|
| Undo toast | ≥ 6s visible; 12–30s for bulk-destructive (durations + bulk rationale canonical in the file) | `friction/recipes.json` |
| Re-auth window | ≤ 15 minutes within the session — session-wide re-auth defeats the purpose | `friction/recipes.json` |
| Recall windows | declared in seconds per action type (send, publish, invite); countdown rendered ("Undo send (10s)"); recall needs no re-confirmation | `recall/windows.json` |
| Bulk preview | count ("Delete 42 items") + sampled preview of up to 10 affected entities before executing; dry-run where the API allows | — |
| Confirm posture | default focus on Cancel; Escape closes without executing; destructive CTA styled danger + a non-color cue; Enter never executes unless the destructive CTA is intentionally focused | `defaults/confirm-posture.json` |
| Audit events | every high-blast or irreversible action emits a user-visible `{actor, verb, target, at, before/after, recoverable, recoveryDeadline}` — filterable, searchable, exportable | `audit/event-schema.json` |
| Permission failures | name the missing permission, the role that holds it, and a request-access CTA — never a silently disabled affordance | `permissions/error-ux.json` |

**The plane and the friction ladder** (`blast-reversibility/matrix.json` ·
`friction/recipes.json`) — undo > confirm for anything **user-reversible in-app**; friction
escalates only with the coordinate. Reversibility has two species: *user-reversible in-app*
(undo genuinely available to the user — the undo>confirm rule applies) vs *ops-reversible*
(refunds, support processes — review-then-commit is the domain norm and NO_UNDO is not a defect;
payments live here). Classify which species before applying the ladder:

| blast × reversibility | treatment |
|---|---|
| low × instant/session | silent action + undo toast |
| medium × instant/days | undo, no confirm (confirm only on modifying a shared item) |
| medium × irreversible | confirm with named consequence |
| high × days | confirm with named consequence + audit event |
| high × irreversible | type-to-confirm (user types the resource name; CTA disabled until match) + re-auth + audit event |
| critical × any | type-to-confirm + re-auth + 2-person approval (initiator proposes, approver resolves, both recorded) + audit event |

Coordinates the matrix doesn't enumerate take the **nearest higher-friction neighbor's**
treatment — step reversibility toward irreversible, then blast upward, until an enumerated row
matches (`matrix.json`'s `default` rule); never resolve downward to lighter friction.

## Detection catalog (what a review hunts)

Confirm dialog on every mutation (confirmation fatigue) · silent irreversible delete ·
destructive CTA default-focused · "Are you sure?" naming neither consequence nor resource · bulk
delete without count + preview · silently disabled affordance with no explanation · undo toast
dismissing in < 3s (unusable on touch / screen reader) · audit events stored but never surfaced ·
type-to-confirm on the user's email (trivially known) instead of the resource · re-auth scoped to
the whole session · stacked confirmations ("Are you *really* sure?") — fix the default instead.

## Mechanism gate — `scripts/safety-check.py`

Placing an action on the plane is judgment; checking that the declared friction matches the
declared coordinate is arithmetic — routed to code, never inference. The checker (stdlib-only,
selftest-locked):

| Check | Severity | Fires when |
|---|---|---|
| `UNGUARDED_DESTRUCTIVE` | gate | high-blast **or** irreversible action with no confirm **and** no undo |
| `NO_UNDO` | gate / advisory | irreversible + no undo + no confirm → gate; a *reversible* action lacking undo → advisory (undo > confirm); `ops_reversible: true` (refunds, payments) downgrades either to an advisory **note** — review-then-commit is that species' norm |
| `WEAK_CONFIRM` | gate / advisory | high-blast guarded only by a bare click — gate when irreversible (the matrix mandates type-to-confirm), advisory otherwise |
| `DEFAULT_DESTRUCTIVE` | gate | confirm dialog default-focuses the destructive CTA |
| `OVER_CONFIRM` | advisory | low-blast reversible action gated by heavy friction |
| `NO_AUDIT` / `NO_PREVIEW` | advisory | high/irreversible with no audit event; bulk with no count + preview |

Absent data is **skipped and reported**, never silently passed — an action with no coordinate
cannot be placed, and an undeclared `has_audit_event`/`has_preview` is never assumed clean; a
malformed card errors cleanly. The gate is **necessary, not sufficient** — it proves the declared
friction matches the declared coordinate, not that the action is safe; step 3 confirms the
dangerous case (high-blast / irreversible) adversarially.

## Material & routing

| Path / peer | Use |
|---|---|
| `blast-reversibility/matrix.json` | the canonical (blast × reversibility) → treatment table |
| `friction/recipes.json` | undo toast, confirm, type-to-confirm, re-auth, 2-person recipes |
| `recall/windows.json` | recall-window durations per action type |
| `audit/event-schema.json` | AuditEvent schema + user-visibility requirements |
| `permissions/error-ux.json` | permission-failure copy + affordance pattern |
| `defaults/confirm-posture.json` | destructive-confirm default posture (focus, keyboard, styling) |
| [[focus-verify]] | enforces Cancel-as-default-focus and Escape handling |
| [[component-author]] | fix owner for affordance findings — the confirm dialog, undo toast, or type-to-confirm input a verdict prescribes is built there |
| [[ui-audit]] | the set-scoped sweep that composes this verifier |

**Done** = every mutating verb carded with a coordinate, `safety-check.py` green, step 3 judged
per action (blast counted honestly · recovery real · audit surfaced · consequence named), every
finding routed to its fix owner. **NOT done** = a green gate with step 3 unwalked (necessary, not
sufficient), an uncoordinated action left off the plane, or a finding left without an owner.
