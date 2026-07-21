# Typography token semantics — what each `--md-sys-typescale-*` voice MEANS

One line per voice. Thirteen voices ride the SAME three levels (SM/MD/LG); **`ui-control` and
`ui-widget` are the exception**, each riding its OWN full six-level ramp (XS/SM/MD/LG/XL/2XL,
TKT-0008, 2026-07-16). Every voice derives `size · line · tracking · weight · para` from its level
alone — this file only answers "what is this voice FOR," never the binding grammar or the box/prose
mechanics (`material-type-facts` owns those).

| Voice | Font role | Flow | What it's FOR |
|---|---|---|---|
| `display` | display | prose | The one big hero statement on a view — a marketing headline, a splash title. Tuned for ONE short line (negative tracking, sub-1.0 leading); never long-running text. |
| `headline` | heading | prose | Real document headings — page titles, section headings, card/dialog titles. The default "this is a heading" voice. |
| `sub-heading` | heading | prose | A wide-tracked, UPPERCASE label sitting ABOVE a headline (e.g. "PRICING") — a section marker, not a heading itself. |
| `title` | heading | prose | A smaller headline — one rung below `headline` for a card or dialog's own title when a full headline would be too loud. |
| `sub-title` | mono | prose | A small heading in an ALTERNATE face (the mono role) — a quieter section marker that wants a different typographic texture, not a control label. |
| `lead` | body | prose | A standfirst / intro paragraph — larger and lighter than body, the one paragraph that introduces a piece before regular body copy takes over. Also the home for a set-apart pull-quote/blockquote treatment. |
| `body` | body | prose | Running prose — the default for paragraphs and long-form reading. |
| `body-mono` | mono | prose | Body-sized text in the mono face — metadata rows, tabular prose-adjacent copy that wants monospace figures. Reads as a wrapping run (changed 2026-07-16 — used to be **box**). |
| `label` | ui | prose | The STATIC label voice — text you read but don't operate: table cells, standalone labels, tooltips, form field labels. Reads, doesn't box (changed 2026-07-16 — used to be **box** and cover control text too; a control's own text is `ui-control` now). |
| `label-mono` | mono | prose | Label-sized text in the mono face — a mono metadata chip, a tabular value you read. Reads, doesn't box (changed 2026-07-16 — used to be **box**). |
| `kicker` | mono | **box** | The smallest overline / metadata tag — UPPERCASE, tracked open, single-line by nature. |
| `tiny` | ui | prose | The smallest READING text — fine print, footnotes, disclaimers. Despite riding the `ui` font role, it's PROSE (wraps, no single-line height) — don't mistake it for `label`. |
| `tiny-mono` | mono | prose | `tiny`-sized reading text in the mono face — a mono-styled disclaimer or legal ID that still wraps as prose. |
| `ui-control` | ui | **box** | Text FOR a control you operate — buttons, inputs, selects, menu items. The interactive-text voice that took over control chrome from `label` (TKT-0008, 2026-07-16); composes DIRECTLY into geometry's control-box `-font` field at every one of geometry's six steps, so tuning this voice flows straight into every button/input's rendered size. |
| `ui-widget` | ui | **box** | Text FOR a compact widget you operate but don't type into — tags, badges, switches, radio/checkbox labels. Its own smaller six-level size table (TKT-0008); unlike `ui-control`, it does NOT compose into geometry. |

## The BOX voices, restated

Exactly three voices are **box**: `kicker`, `ui-control`, `ui-widget`. Every other voice — including
`label`, `body-mono`, and `label-mono`, which used to be box before 2026-07-16 — is prose: it wraps,
uses the ordinary multi-line leading, and has no single-line (`-line-single`) token even for a
visually single-line use like a table cell.

## The two axes, restated as a decision

Ask **what is this text's job** first (prose you read vs. a control you operate vs. a compact widget
you operate), THEN which voice fits that job, THEN the level for its rank (SM/MD/LG for thirteen
voices; XS…2XL for `ui-control`/`ui-widget`). Never pick a voice to hit a size — if a size feels wrong,
the level is wrong, not the voice.

## Sibling weights — a meaning, not just a mechanic

A voice's auto-populated sibling weights (`-weight-{slug}`, e.g. `-weight-medium`, `-weight-semi-bold`)
mean "the same voice, more emphasis" — reach for one instead of hand-picking a heavier number when you
need emphasis WITHIN a voice's own job (a bolded word in body prose, a heavier state in a label). They
don't change what the voice is FOR, only how loud it reads.
