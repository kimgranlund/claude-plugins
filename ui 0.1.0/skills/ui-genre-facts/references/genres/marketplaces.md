---
date: 2026-06-03
curated: 2026-07-02 — harvested from the product-forge product-genres corpus; heavily curated — the metrics, cold-start-strategy, growth-pattern, and take-rate-economics sections dropped, the UI-surface conventions kept
coverage: expanded
primary_sources:
  - "Andrew Chen, *The Cold Start Problem: How to Start and Scale Network Effects* (Harper Business, 2021) — lineage of the two-sided / liquidity frame retained in the intro"
  - "Andrew Chen, 'On Marketplaces' (Stripe Atlas guide). https://stripe.com/guides/atlas/andrew-chen-marketplaces"
---

# Marketplaces

Marketplaces — Airbnb, Uber, eBay, Etsy, DoorDash, Upwork, Vinted — connect two distinct populations (supply and demand: hosts/guests, drivers/riders, sellers/buyers) and facilitate transactions between them. They are governed by network effects: each side's value rises with the size of the _other_ side. The UI consequence is that a marketplace is really **two products sharing an inventory** — a demand-side surface built around search, comparison, and a trustworthy first transaction with a stranger, and a supply-side surface built around listing, fulfillment, and getting paid — plus the trust machinery that makes strangers willing to transact at all.

## Conventions: what these apps have in common

- **Two-sided structure.** Two populations with opposite needs, each with its own home surface: demand gets search/browse → listing detail → book/buy; supply gets a listing editor, an inventory/booking manager, and an earnings/payout view. Auditing one side by the other side's conventions misreads both.
- **Trust and safety machinery.** Strangers transacting money and goods/services need a trust substitute for the reputation a local relationship would provide: **ratings and reviews**, verification/identity badges, escrow or held payments, insurance/guarantees, and dispute resolution. Trust infrastructure is not a feature bolted on; it is what makes transactions between strangers possible at all — and its surfaces (review counts, verified marks, guarantee statements) are expected at the point of decision, on the listing card and detail page.
- **Search, match, and discovery.** The mechanism that pairs the right demand with the right supply (search, ranking, recommendations, or active dispatch as in ride-hail). The comparable-listing card — price, rating, key attributes, availability — is the genre's atomic UI unit.
- **Payments and disbursement.** Collecting from demand, paying out supply, holding funds in between. On the UI: total price before commit, a durable receipt/confirmation for the buyer, and an earnings/payout history for the seller.

## Pitfalls

- **Trust under-built.** Skimping on reviews, verification, guarantees, or dispute resolution caps the first-transaction conversion — the moment a stranger decides whether to hand money to another stranger. Trust cues absent from the listing card and the point of commit are the observable symptom.
- **One side's surface neglected.** A polished buyer experience over a supply side that is a spreadsheet-grade afterthought (or vice versa). Both constituencies are daily users of their own plane; the genre expects each to get a real product.
- **Match context hidden.** Listings that omit the deciding attributes (total price with fees, availability, rating, distance/delivery) force a click-through per candidate and break the comparison the genre is built on.

## Good vs. bad (for a genre-fit dimension)

| Dimension | Good (high genre-fit) | Bad (low genre-fit) |
| --- | --- | --- |
| Trust surfaces | Reviews, verification, guarantees at the point of decision | Trust cues buried or absent; first transaction is a leap of faith |
| Listing card | Comparable at a glance: total price, rating, key attributes | Deciding attributes hidden behind click-through |
| Two sides | Each side has a real home surface for its own job | One side polished, the other an afterthought |
| Money flow | Total before commit; receipts for buyers, payouts for sellers | Fee surprises; no durable record of the transaction |

The single most diagnostic question for genre-fit: **could a first-time buyer and a first-time seller each complete their first transaction with a stranger, confident at every step about what they're getting, what it costs, and what happens if it goes wrong?**
