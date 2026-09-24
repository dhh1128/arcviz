# Integration notes for arcviz's sibling projects

arcviz depends on work that lives in other repositories — `entviz` and `@entviz/react` for identifier visualization, `coia` for alias conventions, the vLEI schemas for what a credential type implies. Reading those sources is not optional, and doing it from memory has been wrong every time it was tried.

These notes exist because that knowledge was being rediscovered. During the 2026-09-23/24 descriptor session, the pill's label mechanics were got wrong twice and corrected twice, and COIA was cited secondhand for an entire session before anyone opened the spec. The findings then lived in a prototype module's docstrings and in `tagged` items — which sit in `~/.local/state/`, survive no clone, and are invisible to anyone who does not think to query them.

| File | Covers |
|---|---|
| [entviz.md](entviz.md) | The pill's label slot and its precedence, the mnemonic and its trust gate, why `label` and `note` are separate, which surprises cost time |
| [coia.md](coia.md) | Consuming aliases without claiming conformance, the flag registry, the ordering rule that protects it, the three-channel separation |

**Every claim carries a file and line so it can be rechecked rather than believed.** These are sibling projects under active development; a note without a citation becomes a confident lie the first time something moves. If you find one of these stale, fix it here rather than working around it in code — the whole point is that the next reader does not repeat the discovery.

Schema knowledge has its own home: [`refs/schema-registry.json`](../../refs/schema-registry.json) carries the sources, the known SAIDs, the four resolution states, and the reasoning about why a registry of hints is safe for content-addressed documents.
