---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; the metrics and network-seeding-strategy sections dropped (the 90-9-1 citation folded into the creation-ladder pattern), UI conventions kept
coverage: foundational
primary_sources:
  - "Jakob N. \"Participation Inequality: The 90-9-1 Rule for Social Features and Online Communities.\" NN/g, 2006. https://www.nngroup.com/articles/participation-inequality/"
  - "Robert E. Kraut & Paul Resnick. *Building Successful Online Communities: Evidence-Based Social Design*. MIT Press, 2012. https://direct.mit.edu/books/monograph/2912/"
  - "Nir Eyal. *Hooked: How to Build Habit-Forming Products*. Portfolio/Penguin, 2014 (Hook Model: trigger → action → variable reward → investment)."
  - "Sarah T. Roberts. *Behind the Screen: Content Moderation in the Shadows of Social Media*. Yale University Press, 2019. https://yalebooks.yale.edu/book/9780300235883/behind-the-screen/"
  - "The Santa Clara Principles on Transparency and Accountability in Content Moderation (2.0, 2021). https://santaclaraprinciples.org/"
---

# Social Media as a Product Genre

A social product's value is almost entirely **other people**. Unlike a tool that's useful to one user alone, a social network is worth nothing to its first user and enormous to its millionth — its utility is a function of who else is there. That single fact drives the whole genre's UI: the first session must be alive before the user has a network, the **engagement loop** must bring people back without becoming manipulative or toxic, the **content-creation ladder** must give the watching majority a low-stakes way to participate, and **moderation, safety, and trust surfaces** must ship as core product — because the same user-generated content that is the product is also, inevitably, where abuse, harassment, and harm arrive. This reference centers consumer social products — networks, feeds, communities, creator platforms, and messaging with a public surface.

> The discipline in one line: a social product is a self-reinforcing loop where users supply the value for other users — so the first session must not be an empty room, the loops must bring people back without exploiting them, the lurker→creator ladder must be climbable one rung at a time, and trust & safety must be core product, not afterthought.

## Conventions: what a competent social product reliably does

- **Solves the empty-room problem at onboarding.** A new user is shown value before they have a network — interest-based suggestions, follow recommendations, seeded/curated content, or a clear first action — so the first session isn't a blank feed. The cold-start is fought per-user, not just at launch.
- **Makes the first contribution trivially low-stakes.** The cheapest possible participation (a like, a vote, a reaction, an emoji) exists as a rung _below_ commenting and posting, because almost everyone starts as a watcher.
- **Has a comprehensible engagement loop.** A trigger (notification, feed update) brings the user back, an easy action and a reward (new content, social response) pays it off, and the user leaves something behind (a post, a follow, a setting) that improves the next visit. This loop is the genre's engine — and its ethical fault line.
- **Surfaces social proof and reciprocity.** Followers/following, likes/reactions, "people you may know," who-responded — the signals that make participation feel seen and reciprocated, which is what actually pulls the next contribution.
- **Ships safety controls _to the user_, not just to moderators.** Block, mute, report, restrict, privacy/audience controls, and comment controls are first-class, discoverable, and on every relevant surface. Self-protection is part of the core loop.
- **Moderates, and is seen to moderate.** There are rules, enforcement, and — per emerging norms like the Santa Clara Principles — notice to affected users and some transparency about what was removed and why. "We have a policy" with invisible, unaccountable enforcement is not credible at scale.

## Signature patterns

The genre-specific moves.

### The engagement / habit loop

Most social products run Nir Eyal's **Hook Model** (from _Hooked_, 2014): **trigger → action → variable reward → investment**. An external trigger (push, email) or internal trigger (boredom, FOMO) prompts an easy **action** (open, scroll); a **variable reward** (you never know what's in the feed/inbox — the unpredictability is the pull) pays it off; and an **investment** (post, follow, customize) loads the next trigger and raises switching cost. The genre-defining tension: this loop is also the mechanism of compulsive use, and the line between "habit-forming" and "manipulative/addictive" is exactly where the ethical and (increasingly) regulatory scrutiny lives. Designing the loop responsibly — honest triggers, no dark-pattern variable rewards aimed at vulnerable users — is part of the craft, not a constraint on it.

### Climbing the content-creation ladder (lurker → contributor → creator)

The genre's most important participation structure. Participation is radically unequal — Jakob N.'s **90-9-1 rule** (NN/g, 2006): in many online communities ~90% lurk, ~9% contribute occasionally, and ~1% account for almost all contribution; the exact split varies by platform and is a heuristic, but the _shape_ (a vast silent base, a tiny creating top) is the defining reality. The product must therefore engineer a **ladder of escalating commitment**: cheap reactions → low-effort contributions (votes, short comments, reshares) → full creation (posts, threads, video). Kraut & Resnick's evidence-based design work frames this as the newcomer/commitment problem — getting people in, giving low-barrier first tasks, and building the reciprocity and identity that motivate deeper contribution. The non-obvious move is that **most design effort should target the rung-to-rung transitions** (lurker→reactor, reactor→commenter), not just the top creators.

```text
Content-creation ladder — design each rung-to-rung transition (illustrative)

  LURKER ───► REACTOR ───► COMMENTER ───► POSTER ───► CREATOR
  (watch)     (like/vote)  (reply)        (original)  (sustained, drives others)

  Roughly tracks the 90-9-1 distribution: the vast base watches, a slim middle
  contributes a little, a tiny top makes most of what everyone consumes.
  Growth = widening the funnel AND nudging users up one rung at a time.
```

### Trust, safety, and moderation at scale

The defensive half of the genre, and inseparable from it. User-facing controls (block/mute/report/restrict, audience and comment controls); the moderation pipeline (community guidelines, automated detection, human review, appeals); and transparency/due-process norms. Sarah T. Roberts' _Behind the Screen_ documents the human and structural reality: moderation is done by **100,000+ commercial moderators worldwide** at real psychological cost, and platforms are structurally **reactive** — the "whack-a-mole" problem means harm is typically addressed only _after_ it scales. The Santa Clara Principles codify the emerging expectation that enforcement come with notice to the user, an appeal, and aggregate transparency — moving moderation from invisible fiat toward accountable process.

## Pitfalls

- **Optimizing engagement into manipulation/toxicity.** Tuning the variable-reward loop and recommendation surface purely for time-on-app — the documented path to compulsive use, outrage amplification, and the harms that draw regulatory and reputational fire. The loop's power is exactly why it needs ethical guardrails.
- **Ignoring the creation ladder.** Building only for posting/creating and assuming users will climb on their own — leaving the 90% with no low-stakes rung, so the content base never grows and the network feels empty even when populated.
- **Treating safety as an afterthought.** Launching without block/mute/report, or with invisible, unaccountable moderation. At any scale, user-generated content _will_ include abuse; a product without safety controls is shipping a harassment tool. Roberts' work shows reactivity is structural — but the absence of any process is a choice.
- **Opaque, due-process-free enforcement.** Removing content or banning users with no notice, no reason, and no appeal. Beyond unfairness, it's now a transparency-norm and regulatory failure (cf. Santa Clara Principles, and emerging platform regulation).

## Good vs. bad

```text
Cold-start / onboarding
  BAD : New user lands on an empty feed, follows no one, sees nothing, leaves.
  GOOD: Interest pick → seeded/recommended content + suggested follows + one easy first
        action, so the first session is alive before the user has a network.

Engagement loop
  BAD : Maximize time-on-app at any cost: rage-bait ranking, manipulative streaks/badges,
        notifications engineered to exploit FOMO.
  GOOD: A genuine trigger→action→reward→investment loop with honest notifications,
        user-controllable, that brings people back to value rather than compulsion.

Creation ladder
  BAD : The only way to participate is to write a full post; 90% never do; feed stays thin.
  GOOD: A real ladder — react → vote → short reply → post — with design effort on each
        rung-to-rung nudge, widening who contributes.

Trust & safety
  BAD : No block/mute/report; moderation is invisible and unaccountable; bans arrive with
        no reason and no appeal.
  GOOD: Block/mute/report/restrict on every surface; clear guidelines; enforcement with
        notice, an appeal, and aggregate transparency (per Santa Clara Principles).
```

The throughline: social products win by **bootstrapping a self-reinforcing network and then sustaining it humanely** — a first session that is alive before the user has a network, engagement loops that bring people back without exploiting them, a deliberately climbable lurker→creator ladder, and trust, safety, and accountable moderation as core product surfaces. The genre punishes empty-room first sessions, manipulation-maximizing loops, creation funnels that ignore the silent 90%, and any product that ships user-generated content without the means to keep its users safe.
