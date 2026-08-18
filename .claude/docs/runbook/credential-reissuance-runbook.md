# Runbook — credential re-issuance (skeleton)

Owed-at-lock mitigation for ADR-0022 ("the repo is the backup") exception 3 — credentials
(gh auth, API keys, `.env`-class material) — never committed, by standing deny rules
(`.claude/rules/dotenv-deny-rules.md` at user scope; memory: `dotenv-deny-rules.md`). Source:
`.claude/docs/adr/0022-repo-is-the-backup.md`, seeded at gh#627's third comment (PR #628's
repair pass). **This document names credential CLASSES and where each is re-obtained — never a
secret, token, or key value itself.** A future edit that adds an actual credential value here is
a defect this runbook exists specifically to prevent, not an update to accept.

## Skeleton — one row per load-bearing credential class

| # | Credential class | Used for | Where re-obtained | Scope |
|---|---|---|---|---|
| 1 | GitHub CLI auth (`gh auth login`) | Every `gh issue`/`gh pr`/`gh api` call this repo's own build/dispatch procedures run (claims, comments, PR open/merge, `version_claim_check.py`, `campaign_close.py`) | Re-run `gh auth login` on the fresh machine; authenticates interactively via the browser OAuth flow or a personal access token entered at the prompt — GitHub's own account settings issue the token, this repo never stores or transmits it | Local, per-machine, per-user |
| 2 | SSH key for `git@github.com` | `git clone`/`git push`/`git fetch` against `origin` (this repo's remote is the SSH form — verified: `git remote -v` on the primary checkout) | Generate a fresh keypair (`ssh-keygen`) and register the PUBLIC half under the GitHub account's Settings → SSH and GPG keys; the private half never leaves the machine that generated it and is never committed | Local, per-machine, per-user |
| 3 | `CLAUDE_CODE_OAUTH_TOKEN` | The `Claude Code` GitHub Action (`.github/workflows/claude.yml`, `.github/workflows/claude-code-review.yml`) — lets the `anthropics/claude-code-action` step authenticate as Claude Code when `@claude` is mentioned on an issue/PR | Re-issued from Claude Code's own account/OAuth settings, then stored as a GitHub **repository secret** named `CLAUDE_CODE_OAUTH_TOKEN` (Settings → Secrets and variables → Actions on the GitHub repo) — never a repo file | GitHub repo secret (Actions scope only) |
| 4 | Default `GITHUB_TOKEN` (Actions built-in) | `.github/workflows/gate.yml`'s CI run (`release_gate.py` sweep) — no additional secret configured beyond GitHub's own auto-issued, per-run token | Nothing to re-obtain — GitHub mints and scopes this automatically for every workflow run; named here only so the table's own completeness (every workflow's credential surface) is auditable at a glance | GitHub-managed, ephemeral per run |

## What "skeleton" means here

This is the shape ADR-0022's acceptance owed at lock — every credential class load-bearing to
this repo's own workflows named, with its re-obtain path. It is deliberately NOT a fully
narrated incident-response runbook (rotation cadence, revocation-on-compromise steps, who to
notify) — that depth is future work once a real re-issuance event gives it a worked case to
generalize from (Rejected alternatives, this ticket's PR body). Additions to this table follow
the same rule as row 1–4: class + purpose + re-obtain path + scope, never a value.

## Verification

`harness:check-reconstructibility`'s audit script checks for this file's own presence at
`.claude/docs/runbook/credential-reissuance-runbook.md` as exception 3's mitigation-doc gate,
and separately sweeps the repo tree for any stray `.env*` file (which should never exist, per the
standing deny rules) — either gap reports as a DEFECT; this file's presence with no stray `.env`
file reports exception 3 as enrolled-with-mitigation.
