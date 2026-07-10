# intent.md — figma-plugin-api

Minted 2026-07-09 from the ultimate-tokens Figma work (variables + moded collections + the
styles feature, PRs #231–#238) via an intent-extraction fork; placement (design-systems plugin)
ratified by the owner the same day.

## Record
- **Trigger:** Figma Plugin-API questions — variables/aliasing/modes, paint+text styles bound to
  variables, sandbox/VM constraints and testing, token interchange JSON, pluginData/clientStorage.
- **Behavior delta:** without this pack Claude answers from generic API docs — it misses the
  jsvm-cpp parse trap (`catch {`), the defaultModeId anchor, the alias-only live cascade, the
  Inter-Regular-12 style-abandonment class (resolve-from-reality, mutate-after-success), the
  provenance-registry prune discipline, the FLOAT-reads-px leading/tracking trap, and the working
  interchange shapes — each one a shipped incident or verified behavior, not doc-derivable.
- **Species + dials:** knowledge pack (answers-only, cited corpus, consult table);
  model-invocable, `user-invocable: true`, `disable-model-invocation: false`.
- **Freedom:** low — claims carry confidence markers ([verified]/[inferred]/[drift-prone]);
  corrections amend in place with a dated note, never silently rewrite.
- **Fences:** NOT the nonoun repo's binder/apply procedure + parity lockstep
  (maintaining-figma-plugins, repo-local — this pack cites, never duplicates); NOT design-md-format
  / material-design-*-tokens (same plugin, different namespaces); NOT the Figma MCP tools; NOT the
  REST API/widgets/scene graph (document axis explicitly partial — no scene-node knowledge earned).
- **Done-when:** a plugin-API question routes here and is answered from the references with its
  confidence visible; the pack never claims scene-graph coverage it doesn't have.

## Axes (5)
sandbox-vm · variables · styles · interchange-schemas · document-plugindata (partial)
