// Style/static lint for the estate's bundled .mjs scripts (ruled 2026-07-15, ADR-0002).
// Runs in CI (.github/workflows/gate.yml) and locally via release_gate G11 when eslint is
// reachable. Deliberately import-free — every rule below is an eslint CORE rule, so
// `npx eslint .` works with no node_modules and no committed dependencies. Selftests prove
// BEHAVIOR (G4); this layer catches the defect classes selftests miss (undefined/unused
// names, unreachable code, dead conditions).

export default [
  {
    // Workflow-tool scripts (**/workflows/*.js) are governed by the Workflow tool's own loader
    // contract, not this repo's JS/ESM conventions (issue #529): the loader extracts a leading
    // `meta` literal, then runs the rest of the file as the body of an async function it supplies
    // itself — top-level `return`/`await` are valid there and a second top-level `export` is not,
    // the opposite of what this file's `sourceType: "module"` block would enforce. Excluded
    // rather than special-cased so this gate never contradicts that contract.
    ignores: ["**/dist/**", "**/node_modules/**", "**/workflows/*.js"],
  },
  {
    files: ["**/scripts/*.mjs", "**/scripts/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        process: "readonly", console: "readonly", Buffer: "readonly", URL: "readonly",
        setTimeout: "readonly", clearTimeout: "readonly",
        setInterval: "readonly", clearInterval: "readonly",
        TextEncoder: "readonly", TextDecoder: "readonly", fetch: "readonly",
      },
    },
    rules: {
      "no-undef": "error",
      "no-unused-vars": ["error", { args: "after-used", caughtErrors: "none" }],
      "no-unreachable": "error",
      "no-dupe-keys": "error",
      "no-dupe-args": "error",
      "no-constant-condition": ["error", { checkLoops: false }],
      "no-self-assign": "error",
      "no-unsafe-negation": "error",
      "use-isnan": "error",
      "valid-typeof": "error",
      "no-empty": ["error", { allowEmptyCatch: true }],
    },
  },
  {
    // ui-probe drives a real browser via playwright — its page.evaluate() callbacks execute in
    // the PAGE, where browser globals are the environment, not an error.
    files: ["**/check-whole-ui/scripts/ui-probe.mjs"],
    languageOptions: {
      globals: {
        window: "readonly", document: "readonly", performance: "readonly",
        MutationObserver: "readonly", requestAnimationFrame: "readonly",
        getComputedStyle: "readonly", location: "readonly", navigator: "readonly",
        PerformanceObserver: "readonly", NodeFilter: "readonly",
      },
    },
  },
];
