#!/usr/bin/env node
// dimension-check.mjs — consumer-side gate for a Material `--md-sys-*` (nonoun / ADIA) GEOMETRY export.
// Zero-dependency, Node ESM. Two jobs:
//   BIND CHECK  — parse the bound geometry CSS and verify it carries the whole dimensional system the
//                 skill's recipes assume: the control ramp (xs…2xl × 9 fields), the M3 radius scale, the
//                 space-0…9 ladder, and the inset / gap / border / focus primitives — so every
//                 `var(--md-sys-{size|radius|space|inset|gap|border|focus-ring}-…)` you write resolves.
//   LINT        — scan UI files for the defect this skill forbids: a hardcoded px/rem/em length literal on
//                 a dimensional property (height, padding, margin, gap, border-radius, outline, border
//                 width) that isn't var-backed. Known limit: matches CSS-property syntax (`prop: <n>px|rem|em`,
//                 quoted or not); camelCase JSX style keys (`marginTop`) and unitless numeric props
//                 (`height={40}`) are NOT caught.
//
// Usage:
//   node dimension-check.mjs <geometry.css>                 # bind check only
//   node dimension-check.mjs <geometry.css> <file|dir> ...  # bind check + lint the given UI sources
//   node dimension-check.mjs selftest                       # prove the checker's own counters
// Exit 0 = clean; 1 = a token is missing OR a lint violation was found; 2 = usage / read error.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const args = process.argv.slice(2);
if (!args.length) { console.error("usage: node dimension-check.mjs <geometry.css> [file|dir ...]"); process.exit(2); }
const [exportPath, ...targets] = args;

// ── the expected dimensional system (names AFTER the `--md-sys-` prefix) ───────────────────────────────
const STEPS  = ["xs", "sm", "md", "lg", "xl", "2xl"];
const FIELDS = ["height", "icon", "caret", "font", "gap", "pad", "pad-edge", "min", "radius"]; // 9
const RAMP   = STEPS.flatMap((s) => FIELDS.map((f) => `size-${s}-${f}`)); // 54
const GROUPS = [
  ["control ramp (6 steps × 9 fields)", RAMP],
  ["radius scale",  ["none", "xs", "sm", "md", "lg", "xl", "full", "default"].map((r) => `radius-${r}`)],
  ["space ladder",  Array.from({ length: 10 }, (_, i) => `space-${i}`)],
  ["insets",        ["control-group", "card", "panel", "dialog", "page"].map((n) => `inset-${n}`)],
  ["gaps",          ["cluster", "stack-tight", "stack", "stack-loose", "grid", "section"].map((n) => `gap-${n}`)],
  ["border",        ["border-thin", "border-thick"]],
  ["focus",         ["focus-ring-width", "focus-ring-offset"]],
];

// ── selftest ─────────────────────────────────────────────────────────────────────────────────────
if (args[0] === "selftest") {
  const { mkdtempSync, writeFileSync, rmSync } = await import("node:fs");
  const { tmpdir } = await import("node:os");
  const { execFileSync } = await import("node:child_process");
  const { fileURLToPath } = await import("node:url");
  const self = fileURLToPath(import.meta.url);
  const dir = mkdtempSync(join(tmpdir(), "dimension-check-selftest-"));
  const allNames = GROUPS.flatMap(([, names]) => names);
  const goodCss = [":root {", ...allNames.map((n) => `  --md-sys-${n}: 4px;`), "}"].join("\n");
  const badCss = goodCss.replace(/  --md-sys-radius-full: [^\n]*\n/, ""); // drop one token
  writeFileSync(join(dir, "good.css"), goodCss);
  writeFileSync(join(dir, "bad.css"), badCss);
  writeFileSync(join(dir, "ok-ui.css"), ".card { padding: var(--md-sys-size-md-pad); }\n");
  writeFileSync(join(dir, "bad-ui.css"), ".card { padding: 16px; }\n");
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
    badBindNamesRadius: /radius scale/.test(badBind.out),
    goodLintExit0: goodLint.code === 0,
    badLintExit1: badLint.code === 1,
    badLintCatchesPx: /hardcoded padding length/.test(badLint.out),
  };
  const ok = Object.values(r).every(Boolean);
  console.log(`dimension-check selftest · ${ok ? "PASS" : "FAIL"} · a full dimensional export binds clean, one dropped radius token fails, var()-wrapped padding lints clean, a hardcoded px length is caught`);
  if (!ok) console.log("  " + JSON.stringify(r));
  process.exit(ok ? 0 : 1);
}

let failed = false;

// ── BIND CHECK ─────────────────────────────────────────────────────────────────────────────────────
let css;
try { css = readFileSync(exportPath, "utf8"); }
catch { console.error(`✗ cannot read export: ${exportPath}`); process.exit(2); }

if (!/--md-sys-(?:size|radius|space|inset|gap|border|focus-ring)-/.test(css)) {
  console.error(`✗ ${exportPath} defines no --md-sys-{size|radius|space|…}-* tokens — is this the geometry export? (a --size-*/--space-* kit is the ultimate-tokens geometry-tokens skill's job)`);
  process.exit(1);
}
// every defined token name, prefix stripped, up to the `:`
const defined = new Set([...css.matchAll(/--md-sys-([a-z0-9-]+)\s*:/g)].map((m) => m[1]));

console.log(`bind: ${exportPath}`);
for (const [label, names] of GROUPS) {
  const missing = names.filter((n) => !defined.has(n));
  if (missing.length) { failed = true; console.log(`  ✗ ${label}: missing ${missing.length}/${names.length} → ${missing.slice(0, 8).join(", ")}${missing.length > 8 ? " …" : ""}`); }
  else console.log(`  ✓ ${label}: all ${names.length} present`);
}
// echo the per-step control heights actually bound — a density/treatment re-export changes these VALUES
// while the token NAMES (and thus the bind above) stay green; re-binding surfaces the real numbers the
// reference value tables cite, so a table that has drifted is visible here.
const heights = STEPS.map((s) => { const m = css.match(new RegExp(`--md-sys-size-${s}-height\\s*:\\s*([^;]+)`)); return `${s}=${m ? m[1].trim() : "?"}`; });
console.log(`  heights (bound): ${heights.join(" · ")}`);
console.log(defined.has("density") ? "  ✓ density knob present" : "  · density knob absent (optional)");

// ── LINT (optional) ────────────────────────────────────────────────────────────────────────────────
const UI_EXT = new Set([".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".html", ".astro"]);
function walk(path, out) {
  const st = statSync(path);
  if (st.isDirectory()) { if (/node_modules|\.git|dist|build/.test(path)) return; for (const e of readdirSync(path)) walk(join(path, e), out); }
  else if (UI_EXT.has(extname(path))) out.push(path);
}
// dimensional properties the skill forbids hardcoding (height/padding/margin/gap/border-radius/outline/border-width)
const PROP = new RegExp(
  "(?:^|[\\s;{('\"])(" + [
    "height", "min-height", "max-height", "block-size", "min-block-size", "max-block-size",
    "padding", "padding-(?:inline|block|top|right|bottom|left)",
    "margin", "margin-(?:inline|block|top|right|bottom|left)",
    "gap", "row-gap", "column-gap",
    "border-radius", "outline", "outline-width",
    "border", "border-(?:top|right|bottom|left|inline|block)?-?width",
  ].join("|") + ")\\s*:", "");
const LEN = /(?:^|[\s:(,'"])\d*\.?\d+(?:px|rem|em)\b/; // a bare length literal (quote chars count as a boundary — JSX/inline-style)
function stripVars(v) { let p; do { p = v; v = v.replace(/var\([^()]*\)/g, " "); } while (v !== p); return v; }

if (targets.length) {
  const files = []; for (const t of targets) walk(t, files);
  console.log(`\nlint: ${files.length} UI file(s)`);
  let hits = 0;
  for (const f of files) {
    const lines = readFileSync(f, "utf8").split("\n");
    lines.forEach((ln, i) => {
      if (/^\s*(\/\/|\*|<!--)/.test(ln)) return;   // skip obvious comment lines
      const m = PROP.exec(ln);
      if (!m) return;
      const value = stripVars(ln.slice(m.index + m[0].length)); // value after the property's `:`, vars removed
      if (LEN.test(value)) { console.log(`  ✗ ${f}:${i + 1}  hardcoded ${m[1]} length (use a --md-sys-* token)\n      ${ln.trim().slice(0, 100)}`); hits++; failed = true; }
    });
  }
  console.log(hits ? `  ${hits} violation(s)` : "  ✓ no hardcoded dimensional literals in UI code");
}

console.log(failed ? "\nFAIL" : "\nPASS");
process.exit(failed ? 1 : 0);
