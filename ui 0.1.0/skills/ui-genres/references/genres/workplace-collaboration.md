---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; the metrics and PLG-growth-pattern sections dropped, UI conventions and the admin-vs-user split kept
coverage: expanded
primary_sources:
  - "Sujeet Jaiswal, 'Figma: Building Multiplayer Infrastructure for Real-Time Design Collaboration'. https://sujeet.pro/articles/figma-multiplayer-infrastructure"
  - "Slack, 'An introduction to Slack Enterprise Grid' and 'Manage members with SCIM provisioning'. https://slack.com/resources/why-use-slack/slack-enterprise-grid"
  - "Jay Kapoor, 'Consumerization of Enterprise Software — Part I', Medium. https://medium.com/jaykapoornyc/consumerization-of-enterprise-software-part-i-7b48274889f6 — the buyer-vs-user split"
---

# Workplace collaboration

Workplace-collaboration apps — Figma, Notion, Slack, Linear, Miro, Google Docs — are tools whose value comes from being used _together_. The defining property is that a single user gets little value; a team gets compounding value. This reverses the design center of gravity of single-player software: the surfaces that matter most are the multiplayer ones — presence, permissions, comments, notifications — and the structural tension every one of these products must resolve is that the person who pays is rarely the person who uses.

## Conventions: what these apps have in common

A handful of capabilities recur across the genre because they are load-bearing for _multiplayer_ value, not because they are fashionable. Treat their absence as a smell, not their presence as a feature.

- **Multiplayer-by-default editing.** Two or more people can act in the same artifact at once. The hard engineering problem is conflict resolution: when two people change the same thing, whose change wins? Figma's published architecture keeps authoritative document state on a central server as a map of object → property → value, resolves conflicts **last-write-wins at the property level**, and only uses CRDT-like structures where the domain needs them — a deliberately _simpler_ choice than full operational transform, justified by Figma's having both a central server and natural property-level granularity (Jaiswal, Figma multiplayer infrastructure). The lesson is architectural humility: pick the weakest consistency model the domain tolerates.
- **Presence.** Who else is here, where are they, what are they doing. Figma coalesces cursor movements and ships them at roughly 33 ms intervals to keep presence frames small and avoid head-of-line blocking on the document socket, then interpolates client-side inside `requestAnimationFrame` for smooth ~60 Hz cursors over a ~30 Hz wire rate (Jaiswal). Presence is cheap to underbuild and expensive to retrofit: it is the signal that makes a space feel _inhabited_.
- **Permissions and roles (RBAC).** Who can view, comment, edit, share, administer. Role-based access control groups permissions into roles (viewer / commenter / editor / admin / owner) rather than assigning them per-user, which is what makes permissioning tractable as a workspace grows. Sharing scope (private → team → org → public-link) is the other half and is a frequent source of security incidents when defaults are too open.
- **Comments, mentions, and async threads.** Collaboration is mostly asynchronous; synchronous co-editing is the exception. The comment-and-`@mention` surface is where most collaboration actually happens — and the `@mention` also pulls a not-yet-active colleague into the artifact.
- **Notifications.** The nervous system connecting async work — and the most over-used surface in the genre (see Pitfalls).
- **An admin/governance plane.** Distinct from the user plane: SSO, SCIM provisioning, audit logs, retention policies, role administration. This is what an org buys; it is invisible to the daily user (see the admin-vs-user split).

## Pitfalls

- **Notification fatigue.** The fastest way to kill engagement while believing you are driving it. Over-notification trains users to ignore, mute, or disable alerts; opt-out / unsubscribe rate is the canary, and it moves _after_ the damage is done. Digesting and batching notifications is widely reported to lift engagement while cutting opt-outs (single-source figures circulate; treat as illustrative, not a benchmark). The dark-pattern version — vague "you have a message waiting" bait, buried unsubscribe — buys short-term clicks and burns long-term trust.
- **Permissions too open by default.** Convenient sharing defaults (anyone-with-the-link-can-edit, org-wide visibility) are a recurring security-incident source; the safe default is least-privilege, with widening as an explicit act.
- **Building admin features the buyer wants but no user will ever see, while the daily experience rots** — or the inverse, a beloved tool that no enterprise will buy because it has no governance plane. Both are failures of the buyer-vs-user split below.

## The admin-vs-user split (the genre's defining tension)

Collaboration software almost always has **two distinct constituencies whose interests diverge**, and resolving that divergence _is_ the product design problem.

- **The end user** wants speed, beauty, zero friction, and to invite whomever they need. They adopt bottom-up, and their experience must feel like consumer software.
- **The admin / economic buyer** wants control, security, compliance, and predictable cost: SSO and SCIM provisioning, audit logs, data-retention and DLP policy, role administration, and a single bill. They frequently **never use the core product** — Slack's Enterprise Grid, SSO, and SCIM surfaces exist almost entirely for this constituency (Slack). As Kapoor puts it, the long-standing enterprise-SaaS problem is that "the buyer persona and user persona are actually different people" — it is hard to sell value to someone who will never touch the product.

The structural consequence: these are effectively **two products sharing a database** — a delightful user plane and a trustworthy admin plane (Kapoor; Slack Enterprise Grid). A product that serves only one constituency stalls: all-user-no-admin can't close enterprise deals; all-admin-no-user gets bought, ignored, and churned.

## Good vs. bad

| Dimension | Good | Bad |
| --- | --- | --- |
| **Notifications** | Batched, relevant, opt-out respected; opt-out rate watched as a canary | Maximized for clicks; vague bait; opt-out treated as a loss to prevent |
| **Permissions** | RBAC roles, least-privilege defaults, sharing widened explicitly | Anyone-with-link-can-edit by default; org-wide visibility on by default |
| **Two constituencies** | Delightful user plane _and_ a real admin/governance plane (SSO, SCIM, audit) | One served, the other ignored — can't sell, or gets bought and churned |
| **Consistency model** | Weakest the domain tolerates (Figma's property-level LWW), presence built early | Over-engineered CRDTs where LWW would do; presence retrofitted late |

The single most diagnostic question for genre-fit: **does a second person in the same artifact make the first more productive — visibly (presence), safely (permissions), and without drowning either in notifications — and does the org that pays get a governance plane of its own?**
