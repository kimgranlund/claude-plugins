# @dsCard preview cards

Component preview cards are small, self-contained HTML files that ride alongside a DESIGN.md and render its system visually. Claude Design's Design System tab renders every tagged card; they also work as plain HTML anywhere.

## The tag

Line 1 of the file, exactly:

```html
<!-- @dsCard group="<Group>" viewport="<WxH>" name="<Card name>" subtitle="<one line>" -->
```

- `group` — cards are grouped verbatim by this string. Title-case, consistent: "Colors", "Type", "Spacing", "Shape", "Components", "Brand".
- `viewport` — the rendered size, e.g. `700x150`. Target ~700×150; 400px height max. The card name renders OUTSIDE the card — no titles or framing inside, just the specimens.

## Self-containment (the DESIGN.md-bundle rule)

Cards shipped with a DESIGN.md carry **no external imports** — each card inlines a single `:root` block with `color-scheme: light dark` and the `light-dark(oklch, oklch)` custom properties it uses, built from the frontmatter pairs. No media-query fork, no linked stylesheet, no CDN fonts required to hold the layout (declare the family stack; degrade gracefully). This is what lets a bundle travel as loose files.

```html
<!-- @dsCard group="Components" viewport="700x150" name="Buttons" subtitle="Primary states" -->
<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{
  color-scheme: light dark;
  --md-sys-color-primary: light-dark(oklch(0.6498 0.1222 224.12), oklch(0.6498 0.1222 224.12));
  --md-sys-color-primary-hover: light-dark(oklch(0.496 0.0966 227.89), oklch(0.7657 0.1409 221.45));
  --md-sys-color-primary-on-primary: light-dark(oklch(1 0 89.88), oklch(1 0 89.88));
  --md-sys-color-neutral-background: light-dark(oklch(0.9551 0 89.88), oklch(0.2241 0.006 236.83));
}
body{margin:0;background:var(--md-sys-color-neutral-background);padding:24px;display:flex;gap:12px;}
.btn{font:480 14px/1 Inter,system-ui,sans-serif;padding:0 18px;height:36px;border:none;border-radius:12px;
     background:var(--md-sys-color-primary);color:var(--md-sys-color-primary-on-primary);}
.btn:hover{background:var(--md-sys-color-primary-hover);}
</style></head><body>
<button class="btn">Primary</button>
<button class="btn" disabled style="opacity:.6">Disabled</button>
</body></html>
```

## What a bundle's card set covers

Err toward **more small cards**, split at the sub-concept level — one concept per card:

- one card per color story: primary states · signature families · status · surfaces · text-and-hairline
- one card per type voice group: display/headings (headline · sub-heading · title) · body/lead · label/tiny · mono (code · kicker · sub-title) — use the bound kit's own voice names; a pre-2026-07 export still says ui/caption/legal/quote
- spacing ladder · radii map
- one dense card per component recipe in the frontmatter, showing states (default/hover/disabled) side by side — a component card with a single default render is under-built
- brand cards (wordmark, app icon) when assets exist — never draw a mark that wasn't provided

A typical bundle: 7–20 cards. Each card must render correctly in BOTH schemes — that's the point of the `light-dark()` inlining.
