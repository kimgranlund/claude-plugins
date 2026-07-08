#!/usr/bin/env node
// token-check.mjs — consumer-side gate for a Material `--md-sys-color-*` (nonoun / ADIA) color export.
// Zero-dependency, Node ESM. Two jobs:
//   BIND CHECK  — parse the bound export CSS, list its palettes, and verify each carries the full 59-role
//                 set the skill's recipes assume (so a `var(--md-sys-color-{p}-…)` you write will resolve).
//   LINT        — scan UI files for the four defects this skill forbids: literal #hex / rgb()/hsl() / oklch()
//                 in a color position, RAW stops (`--md-sys-color-{p}-<digit>`), and an unwrapped custom
//                 property (a `--md-sys-color-…` not inside `var(...)`).
//
// Usage:
//   node token-check.mjs <export.css>                 # bind check only
//   node token-check.mjs <export.css> <file|dir> ...  # bind check + lint the given UI sources
// Exit 0 = clean; 1 = a palette is missing roles OR a lint violation was found.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const args = process.argv.slice(2);
if (!args.length) { console.error("usage: node token-check.mjs <export.css> [file|dir ...]"); process.exit(2); }
const [exportPath, ...targets] = args;

// ── the 59 role suffixes (per palette `p`); `{p}` marks the on-accent family that carries the slug ──
const SUFFIXES = [
  "", "-dim", "-bright", "-low", "-high",
  "-hover", "-active", "-disabled",
  "-on-{p}", "-on-{p}-variant", "-on-{p}-hover", "-on-{p}-active", "-on-{p}-disabled",
  "-on-surface", "-on-surface-variant", "-on-surface-hover", "-on-surface-active", "-on-surface-disabled",
  "-on-surface-variant-hover", "-on-surface-variant-active", "-on-surface-variant-disabled",
  "-placeholder",
  "-outline", "-outline-variant", "-outline-hover", "-outline-active", "-outline-disabled",
  "-outline-variant-hover", "-outline-variant-active", "-outline-variant-disabled",
  "-container", "-container-low", "-container-high", "-container-hover", "-container-active", "-container-disabled",
  "-inverse-surface", "-inverse-on-surface",
  "-background", "-surface",
  "-surface-dimmest", "-surface-dimmer", "-surface-dim", "-surface-bright", "-surface-brighter", "-surface-brightest",
  "-surface-lowest", "-surface-lower", "-surface-low", "-surface-high", "-surface-higher", "-surface-highest",
  "-scrim-weakest", "-scrim-weaker", "-scrim-weak", "-scrim", "-scrim-strong", "-scrim-stronger", "-scrim-strongest",
]; // 59

let failed = false;

// ── BIND CHECK ────────────────────────────────────────────────────────────────────────────────────
let css;
try { css = readFileSync(exportPath, "utf8"); }
catch { console.error(`✗ cannot read export: ${exportPath}`); process.exit(2); }

if (!/--md-sys-color-/.test(css)) {
  console.error(`✗ ${exportPath} defines no --md-sys-color-* tokens — is this the right export? (a --c-* kit is the plugin color-tokens skill's job)`);
  process.exit(1);
}
// palettes = slugs that own a raw -050 stop
const palettes = [...new Set([...css.matchAll(/--md-sys-color-([a-z]+)-050\s*:/g)].map((m) => m[1]))].sort();
// the set of every defined role name (strip the `--md-sys-color-` prefix, up to the `:`)
const defined = new Set([...css.matchAll(/--md-sys-color-([a-z0-9-]+)\s*:/g)].map((m) => m[1]));

console.log(`bind: ${exportPath}`);
console.log(`  palettes (${palettes.length}): ${palettes.join(" · ")}`);
for (const p of palettes) {
  const missing = SUFFIXES.map((s) => p + s.replace(/\{p\}/g, p)).filter((name) => !defined.has(name));
  if (missing.length) { failed = true; console.log(`  ✗ ${p}: missing ${missing.length}/59 roles → ${missing.slice(0, 6).join(", ")}${missing.length > 6 ? " …" : ""}`); }
  else console.log(`  ✓ ${p}: all 59 roles present`);
}

// ── LINT (optional) ─────────────────────────────────────────────────────────────────────────────────
const UI_EXT = new Set([".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".html", ".astro"]);
function walk(path, out) {
  const st = statSync(path);
  if (st.isDirectory()) { if (/node_modules|\.git|dist|build/.test(path)) return; for (const e of readdirSync(path)) walk(join(path, e), out); }
  else if (UI_EXT.has(extname(path))) out.push(path);
}
const RULES = [
  [/#[0-9a-fA-F]{3,8}\b/, "literal hex color"],
  [/\b(?:rgb|rgba|hsl|hsla|oklch|oklab)\s*\(/, "literal color function"],
  [/--md-sys-color-[a-z]+-\d{2,3}(?![a-z-])/, "RAW stop (use a semantic role, not a raw stop)"],
  [/(?<!var\(\s*)--md-sys-color-[a-z0-9-]+(?=\s*[;),])/, "unwrapped custom property (wrap in var(...))"],
];
if (targets.length) {
  const files = []; for (const t of targets) walk(t, files);
  console.log(`\nlint: ${files.length} UI file(s)`);
  let hits = 0;
  for (const f of files) {
    const lines = readFileSync(f, "utf8").split("\n");
    lines.forEach((ln, i) => {
      if (/^\s*(\/\/|\*|<!--)/.test(ln)) return; // skip obvious comment lines
      for (const [re, msg] of RULES) if (re.test(ln)) { console.log(`  ✗ ${f}:${i + 1}  ${msg}\n      ${ln.trim().slice(0, 100)}`); hits++; failed = true; break; }
    });
  }
  console.log(hits ? `  ${hits} violation(s)` : "  ✓ no raw/hex/unwrapped color in UI code");
}

console.log(failed ? "\nFAIL" : "\nPASS");
process.exit(failed ? 1 : 0);
