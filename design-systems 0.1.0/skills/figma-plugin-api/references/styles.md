# Figma Styles — paint + text styles that BIND to variables (and the traps)

Provenance: the nonoun-color-tokens styles feature, PRs #231–#238 (2026-07-09), including one bug
caught only by real-Figma validation. Confidence markers per claim.

## How do I create a paint style bound to a color variable?

```js
const st = existingByName || figma.createPaintStyle();
st.name = "Primary/onPrimary";           // "/" segments render as folders in the Styles panel
st.paints = [figma.variables.setBoundVariableForPaint(
  { type: "SOLID", color: { r: 0, g: 0, b: 0 }, opacity: 1 },  // placeholder — the variable overrides
  "color",
  variableObject                          // a Variable OBJECT, never an id string
)];
```

- `setBoundVariableForPaint` **returns a new paint** — assign the return value, it does not mutate
  in place [verified].
- The placeholder color/opacity are irrelevant at render; **a translucent color's alpha lives in
  the variable's RGBA value**, not the paint's `opacity` [verified].
- Bound to a variable in a moded collection, the style **tracks Light/Dark automatically** —
  confirmed in real Figma (mode flip re-paints every swatch) [verified 2026-07-09].

## How do I set a text style's font WITHOUT leaving a broken default behind? (the Inter-Regular-12 bug)

**The incident** [verified — real-Figma validation 2026-07-09, fixed in PR #238]: the executor
created + named the text style, then tried `loadFontAsync` with *guessed* face names ("Bold",
"Regular"…). When every guess missed the family's real face strings, it skipped — abandoning a
fresh style at **Figma's defaults (Inter Regular 12 / Auto / 0%)**, unregistered and invisible to
pruning. The two rules that fix the whole class:

1. **Resolve the face from reality, never guess**: `figma.listAvailableFontsAsync()` once → a
   `family → [style strings]` map. Pick the requested styleName if present; else the style whose
   **name-implied weight** is nearest the requested numeric weight (Thin 100 · ExtraLight 200 ·
   Light 300 · Regular/Normal/Book 400 · Medium 500 · SemiBold/DemiBold 600 · Bold 700 ·
   ExtraBold 800 · Black/Heavy 900), preferring upright over italic. **Match compound names before
   their substrings** (ExtraBold before Bold, ExtraLight before Light) or every ExtraBold reads as
   700 [verified — `resolveFace` + its e2e].
2. **Create/name/mutate ONLY after `loadFontAsync` succeeds.** A load failure must never create or
   reset a style. Report skipped families (a `missingFonts` list surfaced in a friendly toast) —
   silence turns a font-availability issue into "the feature is broken" [verified].

Bonus of find-or-create-by-name: styles broken by an earlier bad run **self-heal** on the next
apply (found by name, then correctly populated).

## Which text-style fields can bind to variables?

`TextStyle.setBoundVariable(field, variable)` accepts the `VariableBindableTextField`s:
`fontFamily`, `fontStyle` (STRING vars), `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`,
`paragraphSpacing`, `paragraphIndent` (FLOAT vars) [verified against the API typings 2026-07-09;
real-Figma confirmation of fontFamily/fontStyle/fontWeight binding still pending — guard every
bind in its own try and fall back to the literal].

**The unit trap**: a FLOAT variable bound to `lineHeight`/`letterSpacing` is read as **px** — if
your token system carries leading/tracking as a *percent of size* (the sane relative form), a
binding mis-sets them. Ship those two as **literal `{ unit: "PERCENT", value }`** instead, and
bind only the unambiguous fields [inferred from the API's unit-less FLOAT + percent-carrying
tokens; the reason nonoun v1 keeps leading/tracking literal — revisit with a real-Figma probe].

## What literals does a text style need, and in what shapes?

After the font is loaded [verified]:

```js
st.fontName = { family, style };                      // requires the loadFontAsync FIRST
st.fontSize = sizePx;
st.lineHeight = { unit: "PERCENT", value: (lineHeightPx / sizePx) * 100 };   // or PIXELS/AUTO
st.letterSpacing = { unit: "PERCENT", value: (trackingPx / sizePx) * 100 };  // or PIXELS
st.paragraphSpacing = px;
st.textCase = cssTransform === "uppercase" ? "UPPER" : "ORIGINAL";           // guard: older API
```

## How do I prune styles safely?

Same provenance discipline as variables: a **style registry** (`root.setPluginData`, `{name → id}`
for paints and texts separately). Prune only registry entries absent from the current plan, via
`getStyleByIdAsync` + `style.remove()`; a user's own styles are structurally untouchable
[verified — the repo's `STYLE_REGISTRY_KEY` + provenance e2e: a hand-made style survives a full
apply-prune cycle]. Prefer editing an existing style over delete+create — deletion breaks
existing references [verified — also the guidance in Figma's docs].

## Naming/grouping conventions that read well in the Styles panel

- `Family/token` → one folder level; `Family/group/token` → two. Group ONLY where the panel
  benefits (the repo folders `scrims/` and `surfaces/`; on-colors stay flat) [battle-tested].
- Give the CORE variant the bare name (`Display/xl`) and suffix only true variants
  (`Display/xl/Bold`) — a `/Regular` suffix on every core doubles the tree for nothing
  [battle-tested, ratified 2026-07-09].
