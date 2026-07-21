# a2ui-catalog-facts — corpus index

7 reference files. Entered by SEARCH, not linear read: Grep the term first, then Read the matched
file with `offset`. Each row is `ask-class → axis → file`.

| Ask class | Axis | File |
|---|---|---|
| "what does one catalog row declare?" · properties, value mark, child model, `checks` | Component definition contract | `component-definition-contract.md` |
| "how does a type become a `ui-*` control?" · "how does the renderer resolve a type to a widget?" · `WidgetFactory`, `accessorFactory` vs bespoke, sanctioned primitives, the bijection | Factory pattern & widget resolution | `factory-and-widget-resolution.md` |
| "how do I register a project catalog?" · "extend vs replace the default" · `register`, last-wins, `CATALOG_UNKNOWN`, `callableFrom` floor | Two-tier extensibility | `two-tier-extensibility.md` |
| "what should this bindable prop be named?" · "why `checked` not `value`?" · one-mark-per-component, type↔tag bijection, UAX-31 | The naming law | `naming-law.md` |
| "what is our coverage policy?" · "why is this control uncatalogued?" · CI-silent vs fleet-derived gate, allowlist, seed-and-drain | Coverage policy & drift gates | `coverage-policy-and-drift-gates.md` |
| "why did this payload fail `CATALOG`?" · "what makes the catalog a security boundary?" · conformance, RESERVED keys, bindings, validator parity | Security allowlist & conformance | `security-allowlist-and-conformance.md` |
| "where does this claim come from?" · provenance, trust order | Sources | `sources.md` |
