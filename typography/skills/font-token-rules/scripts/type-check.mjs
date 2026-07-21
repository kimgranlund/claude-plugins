#!/usr/bin/env node
// type-check.mjs — consumer-side gate for a default `--type-*` (Ultimate-Tokens-style, prefix
// CONFIGURABLE) type export. Zero-dependency, Node ESM. Two jobs:
//   BIND CHECK  — auto-detect the export's scale prefix (default "type", but a branded kit may use
//                 "brand-type" or anything else — the grammar after it is fixed), list the VOICES
//                 and their STEPS, and verify each voice×step carries the five core props
//                 (size · line · tracking · weight · para) the skill's recipes assume (so a
//                 `var(--{prefix}-{voice}-{step}-…)` you write will resolve). Box voices (any step
//                 declaring `-line-single`) must carry `-line-single` on EVERY step. Also confirm
//                 the five `--font-*` family roles exist.
//   LINT        — scan UI files for hardcoded type the skill forbids: a `font-size` / `font-family`
//                 / `line-height` / `letter-spacing` / `font-weight` (or the `font` shorthand)
//                 whose value is NOT `var(...)` (and not a bare keyword like inherit/normal).
//                 Matches both the kebab CSS form and the camelCase JS-style-object form
//                 (`fontSize: '14px'`). `/* … */` comments are stripped first. Caveat: styles built
//                 dynamically (template strings, values behind a variable, a computed `style={…}`)
//                 aren't visible to a static scan — a green lint is necessary, not sufficient.
//
// Usage:
//   node type-check.mjs <type.css>                 # bind check only
//   node type-check.mjs <type.css> <file|dir> ...  # bind check + lint the given UI sources
//   node type-check.mjs selftest                   # prove the checker's own counters
// Exit 0 = clean; 1 = a voice is missing props / a font role is missing OR a lint violation was found; 2 = usage/read error.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const args = process.argv.slice(2);
if (!args.length) { console.error("usage: node type-check.mjs <type.css> [file|dir ...]"); process.exit(2); }
const [exportPath, ...targets] = args;

const CORE = ["size", "line", "tracking", "weight", "para"];      // every voice×step carries these five
const FONT_ROLES = ["display", "heading", "body", "ui", "mono"];  // the five --font-* family roles
// Closed voice registry, LONGEST FIRST so "sub-heading" and "sub-title" are preferred over the
// "heading"/"title" suffixes they contain — prefix detection below depends on trying the longer
// voice name first.
const VOICES = ["display", "headline", "sub-heading", "title", "sub-title", "lead", "body", "code", "label", "kicker", "tiny"]
  .sort((a, b) => b.length - a.length);
// The three voices the grammar REQUIRES to carry -line-single — seeded, not inferred, so a kit
// that drops -line-single entirely from label/code/kicker still fails instead of silently passing.
const BOX_VOICES = new Set(["label", "code", "kicker"]);
// "line-single" MUST be tried before "line" or it would only ever match the "line" prefix of it.
const PROPS = ["line-single", "size", "line", "tracking", "weight", "para"];

// ── selftest ─────────────────────────────────────────────────────────────────────────────────────
if (args[0] === "selftest") {
  const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const { execFileSync } = await import("node:child_process");
  const { fileURLToPath } = await import("node:url");
  const self = fileURLToPath(import.meta.url);
  const dir = mkdtempSync(join(tmpdir(), "type-check-selftest-"));
  const fontLines = FONT_ROLES.map((f) => `  --font-${f}: system-ui;`).join("\n");
  const voiceLines = CORE.map((p) => `  --type-body-md-${p}: ${p === "size" ? "1rem" : p === "weight" ? "400" : "normal"};`).join("\n");
  const goodCss = `:root {\n${fontLines}\n${voiceLines}\n}\n`;
  const badCss = goodCss.replace(/  --type-body-md-para: [^\n]*\n/, ""); // drop one prop
  const materialCss = ":root {\n  --md-sys-typescale-body-md-size: 1rem;\n}\n";
  writeFileSync(join(dir, "good.css"), goodCss);
  writeFileSync(join(dir, "bad.css"), badCss);
  writeFileSync(join(dir, "material.css"), materialCss);
  writeFileSync(join(dir, "ok-ui.css"), ".p { font-size: var(--type-body-md-size); }\n");
  writeFileSync(join(dir, "bad-ui.css"), ".p { font-size: 14px; }\n");
  const run = (a) => {
    try { const out = execFileSync(process.execPath, [self, ...a], { stdio: ["ignore", "pipe", "pipe"] }); return { code: 0, out: out.toString() }; }
    catch (e) { return { code: e.status ?? 1, out: (e.stdout || Buffer.alloc(0)).toString() + (e.stderr || Buffer.alloc(0)).toString() }; }
  };
  const goodBind = run([join(dir, "good.css")]);
  const badBind = run([join(dir, "bad.css")]);
  const materialRedirect = run([join(dir, "material.css")]);
  const goodLint = run([join(dir, "good.css"), join(dir, "ok-ui.css")]);
  const badLint = run([join(dir, "good.css"), join(dir, "bad-ui.css")]);
  rmSync(dir, { recursive: true, force: true });
  const r = {
    goodBindExit0: goodBind.code === 0,
    badBindExit1: badBind.code === 1,
    badBindNamesGap: /missing/.test(badBind.out),
    materialRedirects: materialRedirect.code === 1 && /material-type-facts/.test(materialRedirect.out),
    goodLintExit0: goodLint.code === 0,
    badLintExit1: badLint.code === 1,
    badLintCatchesSize: /hardcoded font-size/.test(badLint.out),
  };
  const ok = Object.values(r).every(Boolean);
  console.log(`type-check selftest · ${ok ? "PASS" : "FAIL"} · a full body voice + five font roles binds clean under the type- prefix, one dropped prop fails, a Material export redirects instead of false-gapping, var()-wrapped font-size lints clean, a hardcoded px size is caught`);
  if (!ok) console.log("  " + JSON.stringify(r));
  process.exit(ok ? 0 : 1);
}

let failed = false;

// ── BIND CHECK ────────────────────────────────────────────────────────────────────────────────────
let css;
try { css = readFileSync(exportPath, "utf8"); }
catch { console.error(`✗ cannot read export: ${exportPath}`); process.exit(2); }

// Parses a custom-property NAME (the text after "--", before ":") into {prefix, voice, step, prop}.
// The prefix is UNKNOWN (configurable per project) and may itself contain hyphens (e.g.
// "brand-type"), and voice names may also contain hyphens ("sub-heading") — so neither boundary is
// fixed. The split that IS fixed: prop is a closed, small alternation checked at the very end;
// step never contains a hyphen (xs, sm, md, 3xs, 2xl, …). Strategy: peel prop off the end, then
// split the remainder at its LAST hyphen to get step, then match the longest known voice as a
// SUFFIX of what's left — whatever remains before that suffix is the prefix.
function parseToken(name) {
  for (const prop of PROPS) {
    const suf = "-" + prop;
    if (!name.endsWith(suf)) continue;
    const head1 = name.slice(0, -suf.length); // prefix-voice-step
    const lastDash = head1.lastIndexOf("-");
    if (lastDash < 1) continue;
    const step = head1.slice(lastDash + 1);
    const head2 = head1.slice(0, lastDash); // prefix-voice
    for (const voice of VOICES) {
      if (head2 === voice) return { prefix: "", voice, step, prop };
      if (head2.endsWith("-" + voice)) {
        const prefix = head2.slice(0, head2.length - voice.length - 1);
        if (prefix) return { prefix, voice, step, prop };
      }
    }
  }
  return null;
}

// Parses a utility CLASS name (no leading "."), e.g. "type-sub-heading-md" -> {prefix, voice, step}.
function parseClass(name) {
  const lastDash = name.lastIndexOf("-");
  if (lastDash < 1) return null;
  const step = name.slice(lastDash + 1);
  const head2 = name.slice(0, lastDash); // prefix-voice
  for (const voice of VOICES) {
    if (head2 === voice) return { prefix: "", voice, step };
    if (head2.endsWith("-" + voice)) {
      const prefix = head2.slice(0, head2.length - voice.length - 1);
      if (prefix) return { prefix, voice, step };
    }
  }
  return null;
}

console.log(`bind: ${exportPath}`);

// A Material `--md-sys-typescale-*` export is out of scope for THIS (generic) checker even though
// "md-sys-typescale" would otherwise parse as just another custom prefix (its voice names are real
// words too) — catch it explicitly and redirect rather than emitting a confusing generic-gap report.
if (/--md-sys-typescale-/.test(css)) {
  failed = true;
  console.log("  ✗ this export uses Material's `--md-sys-typescale-*` namespace — bind it with the " +
    "material-type-facts skill instead (this checker is for the default `--type-*` grammar)");
  console.log("\nFAIL");
  process.exit(1);
}

const PROP_TOKEN = /--([a-z][a-z0-9-]*)\s*:/g;
const voices = new Map(); // voice -> Map(step -> Set(prop))
const prefixesSeen = new Set();
for (const m of css.matchAll(PROP_TOKEN)) {
  const parsed = parseToken(m[1]);
  if (!parsed) continue;
  prefixesSeen.add(parsed.prefix);
  if (!voices.has(parsed.voice)) voices.set(parsed.voice, new Map());
  const steps = voices.get(parsed.voice);
  if (!steps.has(parsed.step)) steps.set(parsed.step, new Set());
  steps.get(parsed.step).add(parsed.prop);
}

if (voices.size === 0) {
  failed = true;
  console.log("  ✗ no --{prefix}-{voice}-{step}-{prop} tokens found — is this the right export?");
  console.log("\nFAIL");
  process.exit(1);
}

console.log(`  detected prefix(es): ${[...prefixesSeen].map((p) => p || "(none)").join(", ")}`);

// font-family roles
const fonts = new Set([...css.matchAll(/--font-([a-z]+)\s*:/g)].map((m) => m[1]));
const missingFonts = FONT_ROLES.filter((f) => !fonts.has(f));
if (missingFonts.length) { failed = true; console.log(`  ✗ font roles: missing --font-${missingFonts.join(", --font-")}`); }
else console.log(`  ✓ font roles: --font-${FONT_ROLES.join(", --font-")} all present`);

// voices × steps × props
const voiceNames = [...voices.keys()].sort();
console.log(`  voices (${voiceNames.length}): ${voiceNames.join(" · ")}`);
let classes = 0;
for (const m of css.matchAll(/\.([a-z][a-z0-9-]*)\s*\{/g)) if (parseClass(m[1])) classes++;
for (const voice of voiceNames) {
  const steps = voices.get(voice);
  const boxVoice = BOX_VOICES.has(voice) || [...steps.values()].some((s) => s.has("line-single"));
  const need = boxVoice ? [...CORE, "line-single"] : CORE;
  const gaps = [];
  for (const [step, props] of [...steps].sort()) {
    const miss = need.filter((p) => !props.has(p));
    if (miss.length) gaps.push(`${step}(${miss.join(",")})`);
  }
  const ramp = [...steps.keys()].sort().join("/");
  if (gaps.length) { failed = true; console.log(`  ✗ ${voice} [${ramp}]${boxVoice ? " +line-single" : ""}: missing → ${gaps.join(" ")}`); }
  else console.log(`  ✓ ${voice} [${ramp}]: all ${need.length} props on every step${boxVoice ? " (incl. line-single)" : ""}`);
}
console.log(`  utility classes: ${classes} × .{prefix}-{voice}-{step}`);

// ── LINT (optional) ─────────────────────────────────────────────────────────────────────────────────
const UI_EXT = new Set([".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".html", ".astro"]);
function walk(path, out) {
  const st = statSync(path);
  if (st.isDirectory()) { if (/node_modules|\.git|dist|build/.test(path)) return; for (const e of readdirSync(path)) walk(join(path, e), out); }
  else if (UI_EXT.has(extname(path))) out.push(path);
}
// Each rule matches a type property in EITHER the kebab CSS form or the camelCase JS-style-object
// form, and captures its value; a `var(...)` value or a bare keyword is allowed. The value capture
// stops at ; , { } so a multi-family list or a JSX object entry doesn't swallow the next declaration.
// The `font` shorthand is anchored `(?<![\w-])font\s*:` so it fires ONLY on the bare shorthand, never
// on font-size/-family/-weight (kebab or camel).
const RULES = [
  ["font-size", /(?<![\w-])(?:font-size|fontSize)\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert)\b/i],
  ["font-family", /(?<![\w-])(?:font-family|fontFamily)\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert)\b/i],
  ["line-height", /(?<![\w-])(?:line-height|lineHeight)\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert|normal)\b/i],
  ["letter-spacing", /(?<![\w-])(?:letter-spacing|letterSpacing)\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert|normal)\b/i],
  ["font-weight", /(?<![\w-])(?:font-weight|fontWeight)\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert|normal)\b/i],
  ["font (shorthand)", /(?<![\w-])font\s*:\s*([^;,{}]+)/i, /^(inherit|initial|unset|revert)\b/i],
];
function violations(line) {
  const hits = [];
  for (const [prop, re, keyword] of RULES) {
    const m = re.exec(line);
    if (!m) continue;
    const val = m[1].trim();
    // JS string values arrive quoted ("'normal'", '"var(--x)"') — strip the quotes before testing,
    // or a legitimate bare keyword / var() reference written as a JS string is misread as hardcoded.
    const bare = val.replace(/^['"`]|['"`]$/, "").replace(/['"`]$/, "");
    if (/var\(/.test(bare)) continue;   // var-backed → ok
    if (keyword.test(bare)) continue;   // bare keyword → ok
    hits.push(`hardcoded ${prop}: ${val.slice(0, 40)}`);
  }
  return hits;
}
if (targets.length) {
  const files = []; for (const t of targets) walk(t, files);
  console.log(`\nlint: ${files.length} UI file(s)`);
  let hits = 0;
  for (const f of files) {
    // Blank out /* … */ block comments (single- or multi-line) while preserving newlines, so a
    // commented-out declaration can't be flagged and line numbers still hold.
    const stripped = readFileSync(f, "utf8").replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, " "));
    stripped.split("\n").forEach((ln, i) => {
      if (/^\s*(\/\/|<!--)/.test(ln)) return; // skip line-comment / HTML-comment lines
      for (const v of violations(ln)) { console.log(`  ✗ ${f}:${i + 1}  ${v}\n      ${ln.trim().slice(0, 100)}`); hits++; failed = true; }
    });
  }
  console.log(hits ? `  ${hits} violation(s)` : "  ✓ no hardcoded font-size/family/line-height/letter-spacing/weight/font shorthand in UI code");
}

console.log(failed ? "\nFAIL" : "\nPASS");
process.exit(failed ? 1 : 0);
