# Feedback — intents, toasts, banners, overlays, loading

## The intent palettes

`info · success · warning · danger` are FULL palettes — every role exists on each, and the names ARE
the meanings (info · success · warning · error-as-`danger`). Where M3 carries a single `error`
color, nonoun extends all four intents into complete 59-role palettes, so a callout can tint, outline,
fill, and state exactly like the accent.
The rule: an intent palette appears **only when the UI means it** (state, result, risk), never as
decoration. Recipes are the same shapes as everywhere else, with `{p}` = the intent:

| Element | Recipe |
|---|---|
| status banner / callout | bg `--md-sys-color-{p}-container` · border `--md-sys-color-{p}-outline` · title `--md-sys-color-{p}-on-surface` · body `--md-sys-color-{p}-on-surface-variant` |
| filled status chip / badge | bg `--md-sys-color-{p}` · text `--md-sys-color-{p}-on-{p}` |
| soft chip / badge | bg `--md-sys-color-{p}-container` · text `--md-sys-color-{p}-on-surface` |
| status text / icon inline | `--md-sys-color-{p}` (bare accent as fg) |
| status border on a field | `--md-sys-color-{p}-outline` (see interactive.md error state) |
| destructive button | interactive.md's filled/outlined recipes with `{p} = danger` |

Because containers/outlines are translucent 500-ramp roles, intent callouts tint correctly on any
surface tier. Text on the container is the intent's `-on-surface`, not an `-on-container` (no such
role). **Do not "fix" white-on-warning text** — on-colors are fixed light by design (SKILL.md
law 6); if a filled warning chip bothers you, use the soft-chip recipe instead.

## Toasts & snackbars

The inverse pair, so they read on top of anything:
bg `--md-sys-color-neutral-inverse-surface` · text `--md-sys-color-neutral-inverse-on-surface` · the
action link inside a toast: use bare `--md-sys-color-{p}` only if it clears the inverse background;
otherwise `--md-sys-color-neutral-inverse-on-surface` underlined. An intent stripe/icon on the
toast: bare `--md-sys-color-{intent}`.

## Overlays & scrims — the seven-strength ladder

`--md-sys-color-neutral-scrim-weakest` … `-weak` … the base `--md-sys-color-neutral-scrim` … `-strongest`
— a translucent ladder of the palette's 500 stop (5%→60% alpha), mode-flat. It's a nonoun extension of
M3's single `scrim`. Pick by job, not by taste:

| Job | Role |
|---|---|
| hover wash on media / image darkening for text legibility | `-scrim-weak` … `-scrim` |
| modal/dialog backdrop | `--md-sys-color-neutral-scrim-strong` |
| drawer backdrop (content stays glanceable) | `--md-sys-color-neutral-scrim` |
| full blocking overlay (loading a whole view) | `-scrim-stronger` / `-strongest` |
| tinted brand/intent overlay (marketing hero, danger zone) | the SAME suffixes on that palette: `--md-sys-color-danger-scrim-weak` |

Scrims stack with the elevation ladder: backdrop = scrim, the floating panel = `-surface-highest`.

## Loading & skeletons

| Element | Role |
|---|---|
| skeleton block | `--md-sys-color-neutral-container-low`, shimmer highlight `--md-sys-color-neutral-container` |
| indeterminate bar/spinner track | `--md-sys-color-neutral-container` |
| spinner/bar fill | `--md-sys-color-{p}` (accent) |
| progress with meaning (upload ok/failed) | swap `{p}` to the intent |

Skeletons are containers (translucent) so they read on any tier — not gray raws, not opacity hacks.

## Empty / error states (full-pane)

Pane bg `--md-sys-color-neutral-surface-low` (a recessed well) · illustration strokes
`--md-sys-color-neutral-outline` · title `-on-surface` · body `-on-surface-variant` · the CTA = a
normal filled button. A full-pane ERROR state colors only its icon/title accents with
`--md-sys-color-danger` — not the whole pane.
