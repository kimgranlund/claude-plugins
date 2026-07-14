# Typography token semantics — what each `--md-sys-typescale-*` voice MEANS

One line per voice. Every voice rides the SAME three levels (SM/MD/LG) and derives `size · line ·
tracking · weight · para` from that alone — this file only answers "what is this voice FOR," never the
binding grammar or the box/prose mechanics (`material-design-typography-tokens` owns those).

| Voice | Font role | Flow | What it's FOR |
|---|---|---|---|
| `display` | display | prose | The one big hero statement on a view — a marketing headline, a splash title. Tuned for ONE short line (negative tracking, sub-1.0 leading); never long-running text. |
| `headline` | heading | prose | Real document headings — page titles, section headings, card/dialog titles. The default "this is a heading" voice. |
| `sub-heading` | heading | prose | A wide-tracked, UPPERCASE label sitting ABOVE a headline (e.g. "PRICING") — a section marker, not a heading itself. |
| `title` | heading | prose | A smaller headline — one rung below `headline` for a card or dialog's own title when a full headline would be too loud. |
| `sub-title` | mono | prose | A small heading in an ALTERNATE face (the mono role) — a quieter section marker that wants a different typographic texture, not a control label. |
| `lead` | body | prose | A standfirst / intro paragraph — larger and lighter than body, the one paragraph that introduces a piece before regular body copy takes over. Also the home for a set-apart pull-quote/blockquote treatment. |
| `body` | body | prose | Running prose — the default for paragraphs and long-form reading. |
| `body-mono` | mono | **box** | Body-sized text in the mono face — metadata rows, tabular prose-adjacent copy that wants monospace figures. |
| `label` | ui | **box** | Interface chrome you OPERATE, not read — menu items, table cells, standalone labels, badges, tooltips, and a control's own character (never its size — that's geometry's). The "default UI text" voice. |
| `label-mono` | mono | **box** | Label-sized text in the mono face — a mono metadata chip, a tabular UI value. |
| `kicker` | mono | **box** | The smallest overline / metadata tag — UPPERCASE, tracked open, single-line by nature. |
| `tiny` | ui | prose | The smallest READING text — fine print, footnotes, disclaimers. Despite riding the `ui` font role, it's PROSE (wraps, no single-line height) — don't mistake it for `label`. |
| `tiny-mono` | mono | prose | `tiny`-sized reading text in the mono face — a mono-styled disclaimer or legal ID that still wraps as prose. |

## The two axes, restated as a decision

Ask **what is this text's job** first (prose you read vs. chrome you operate), THEN which voice fits
that job, THEN the level (SM/MD/LG) for its rank. Never pick a voice to hit a size — if a size feels
wrong, the level is wrong, not the voice.

## Sibling weights — a meaning, not just a mechanic

A voice's auto-populated sibling weights (`-weight-{slug}`, e.g. `-weight-medium`, `-weight-semi-bold`)
mean "the same voice, more emphasis" — reach for one instead of hand-picking a heavier number when you
need emphasis WITHIN a voice's own job (a bolded word in body prose, a heavier state in a label). They
don't change what the voice is FOR, only how loud it reads.
