#!/usr/bin/env node
// type-check.mjs — consumer-side gate for a Material `--md-sys-typescale-*` (nonoun / ADIA) type export.
// Zero-dependency, Node ESM. Two jobs:
//   BIND CHECK  — parse the bound export CSS, list the VOICES and their LEVELS, and verify each
//                 voice×level carries the five core props (size · line · tracking · weight · para) the
//                 skill's recipes assume (so a `var(--md-sys-typescale-{voice}-{level}-…)` you write
//                 will resolve). Box voices (any level declaring `-line-single`) must carry
//                 `-line-single` on EVERY level. Also confirm the five `--font-*` family roles exist.
//   LINT        — scan UI files for hardcoded type the skill forbids: a `font-size` / `font-family` /
//                 `line-height` / `letter-spacing` / `font-weight` (or the `font` shorthand) whose
//                 value is NOT `var(...)` (and not a bare keyword like inherit/normal). Matches both
//                 the kebab CSS form and the camelCase JS-style-object form (`fontSize: '14px'`).
//                 `/* … */` comments are stripped first. Caveat: styles built dynamically (template
//                 strings, values behind a variable, a computed `style={…}`) aren't visible to a
//                 static scan — a green lint is necessary, not sufficient.
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

const CORE = ["size", "line", "tracking", "weight", "para"];      // every voice×level carries these five
const FONT_ROLES = ["display", "heading", "body", "ui", "mono"];  // the five --font-* family roles

// ── selftest ─────────────────────────────────────────────────────────────────────────────────────
if (args[0] === "selftest") {
  const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const { execFileSync } = await import("node:child_process");
  const { fileURLToPath } = await import("node:url");
  const self = fileURLToPath(import.meta.url);
  const dir = mkdtempSync(join(tmpdir(), "type-check-selftest-"));
  const fontLines = FONT_ROLES.map((f) => `  --font-${f}: system-ui;`).join("\n");
  const voiceLines = CORE.map((p) => `  --md-sys-typescale-body-md-${p}: ${p === "size" ? "1rem" : p === "weight" ? "400" : "normal"};`).join("\n");
  const goodCss = `:root {\n${fontLines}\n${voiceLines}\n}\n`;
  const badCss = goodCss.replace(/  --md-sys-typescale-body-md-para: [^\n]*\n/, ""); // drop one prop
  writeFileSync(join(dir, "good.css"), goodCss);
  writeFileSync(join(dir, "bad.css"), badCss);
  writeFileSync(join(dir, "ok-ui.css"), ".p { font-size: var(--md-sys-typescale-body-md-size); }\n");
  writeFileSync(join(dir, "bad-ui.css"), ".p { font-size: 14px; }\n");
  const run = (a) => {
    try { const out = execFileSync(process.execPath, [self, ...a], { stdio: ["ignore", "pipe", "pipe"] }); return { code: 0, out: out.toString() }; }
    catch (e) { return { code: e.status ?? 1, out: (e.stdout || Buffer.alloc(0)).toString() + (e.stderr || Buffer.alloc(0)).toString() }; }
  };
  const goodBind = run([join(dir, "good.css")]);
  const badBind = run([join(dir, "bad.css")]);
  const goodLint = run([join(dir, "good.css"), join(dir, "ok-ui.css")]);
  const badLint = run([join(dir, "good.css"), join(dir, "bad-ui.css")]);
  rmSync(dir, { recursive: true, force: true });
  const r = {
    goodBindExit0: goodBind.code === 0,
    badBindExit1: badBind.code === 1,
    badBindNamesGap: /missing/.test(badBind.out),
    goodLintExit0: goodLint.code === 0,
    badLintExit1: badLint.code === 1,
    badLintCatchesSize: /hardcoded font-size/.test(badLint.out),
  };
  const ok = Object.values(r).every(Boolean);
  console.log(`type-check selftest · ${ok ? "PASS" : "FAIL"} · a full body voice + all five font roles binds clean, one dropped prop (para) fails, var()-wrapped font-size lints clean, a hardcoded px size is caught`);
  if (!ok) console.log("  " + JSON.stringify(r));
  process.exit(ok ? 0 : 1);
}

let failed = false;

// ── BIND CHECK ────────────────────────────────────────────────────────────────────────────────────
let css;
try { css = readFileSync(exportPath, "utf8"); }
catch { console.error(`✗ cannot read export: ${exportPath}`); process.exit(2); }

if (!/--md-sys-typescale-/.test(css)) {
  console.error(`✗ ${exportPath} defines no --md-sys-typescale-* tokens — is this the right export? (a --type-* kit is the plugin typography-tokens skill's job)`);
  process.exit(1);
}

// Parse `--md-sys-typescale-{voice}-{level}-{prop}:` — `line-single` FIRST so it wins over `line`; the
// captured head is `{voice}-{level}`, split at the LAST hyphen (voice names carry hyphens: sub-heading).
const TOKEN = /--md-sys-typescale-([a-z0-9-]+)-(line-single|size|line|tracking|weight|para)\s*:/g;
const voices = new Map(); // voice -> Map(level -> Set(prop))
for (const m of css.matchAll(TOKEN)) {
  const head = m[1], prop = m[2];
  const i = head.lastIndexOf("-");
  if (i < 1) continue;
  const voice = head.slice(0, i), level = head.slice(i + 1);
  if (!voices.has(voice)) voices.set(voice, new Map());
  const levels = voices.get(voice);
  if (!levels.has(level)) levels.set(level, new Set());
  levels.get(level).add(prop);
}

console.log(`bind: ${exportPath}`);

// font-family roles
const fonts = new Set([...css.matchAll(/--font-([a-z]+)\s*:/g)].map((m) => m[1]));
const missingFonts = FONT_ROLES.filter((f) => !fonts.has(f));
if (missingFonts.length) { failed = true; console.log(`  ✗ font roles: missing --font-${missingFonts.join(", --font-")}`); }
else console.log(`  ✓ font roles: --font-${FONT_ROLES.join(", --font-")} all present`);

// voices × levels × props
const voiceNames = [...voices.keys()].sort();
console.log(`  voices (${voiceNames.length}): ${voiceNames.join(" · ")}`);
let classes = (css.match(/\.md-sys-typescale-[a-z0-9-]+\s*\{/g) || []).length;
for (const voice of voiceNames) {
  const levels = voices.get(voice);
  const boxVoice = [...levels.values()].some((s) => s.has("line-single"));
  const need = boxVoice ? [...CORE, "line-single"] : CORE;
  const gaps = [];
  for (const [level, props] of [...levels].sort()) {
    const miss = need.filter((p) => !props.has(p));
    if (miss.length) gaps.push(`${level}(${miss.join(",")})`);
  }
  const ramp = [...levels.keys()].sort().join("/");
  if (gaps.length) { failed = true; console.log(`  ✗ ${voice} [${ramp}]${boxVoice ? " +line-single" : ""}: missing → ${gaps.join(" ")}`); }
  else console.log(`  ✓ ${voice} [${ramp}]: all ${need.length} props on every level${boxVoice ? " (incl. line-single)" : ""}`);
}
console.log(`  utility classes: ${classes} × .md-sys-typescale-{voice}-{level}`);

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
function violation(line) {
  for (const [prop, re, keyword] of RULES) {
    const m = re.exec(line);
    if (!m) continue;
    const val = m[1].trim();
    if (/var\(/.test(val)) continue;   // var-backed → ok
    if (keyword.test(val)) continue;   // bare keyword → ok
    return `hardcoded ${prop}: ${val.slice(0, 40)}`;
  }
  return null;
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
      const v = violation(ln);
      if (v) { console.log(`  ✗ ${f}:${i + 1}  ${v}\n      ${ln.trim().slice(0, 100)}`); hits++; failed = true; }
    });
  }
  console.log(hits ? `  ${hits} violation(s)` : "  ✓ no hardcoded font-size/family/line-height/letter-spacing/weight/font shorthand in UI code");
}

console.log(failed ? "\nFAIL" : "\nPASS");
process.exit(failed ? 1 : 0);
