# arcviz-fixtures

A dev-time generator for the ACDC fixtures in `../../corpus/`. It exists because seven rendering states that `docs/research/disclosure-matrix.md` §d binds by rule are currently testable against nothing (§e) — no observed artifact in the vLEI or keripy corpora exercises them — and hand-writing ACDC JSON is not viable: every field is folded into a SAID, so editing one attribute by hand invalidates every digest above it in the chain.

## This is a dev tool, not part of the renderer

This package depends on [keripy](https://github.com/WebOfTrust/keripy) (`~/code/wot/keripy`, referenced as a local editable path dependency in `pyproject.toml`) to compute real SAIDs — keripy is the reference KERI/ACDC implementation, so anything it saidifies is valid by construction. keripy is a large, native-extension-heavy (lmdb, pysodium, blake3) full KERI node implementation. **The arcviz renderer must never depend on it** — a program that draws an already-issued, already-disclosed ACDC has no business linking a KERI keystore. That is the entire reason this is its own `uv` project under `tools/fixtures/` rather than a dependency group of some future top-level arcviz package: the boundary is a separate `pyproject.toml`, a separate lockfile, a separate virtualenv.

Regenerate the corpus after changing a fixture:

```
cd tools/fixtures
uv sync
nice -n 19 ionice -c 3 uv run arcviz-fixtures
nice -n 19 ionice -c 3 uv run pytest
```

`uv run arcviz-fixtures` writes into `../../corpus/` (override with `--corpus-dir`). It is deterministic: the same code always produces byte-identical output, because every "random" value (`u` nonces, AID placeholders, timestamps) is a blake3 digest of a fixed seed string plus a label (`src/arcviz_fixtures/determinism.py`), never real entropy or the wall clock.

## What this does not model

To keep ~30 fixtures tractable, this generator computes ACDC- and registry-inception-level SAIDs only. It does **not**:

- Simulate a KERI keystore, keypairs, or signatures. Every issuer/issuee AID is a deterministic blake3 digest formatted as a valid CESR self-addressing identifier (`determinism.aid()`) — structurally indistinguishable from a real delegated/multisig AID, but anchored to no inception event. Nothing here is signed.
- Construct KEL events (`icp`/`dip`/`drt`/`ixn`) or TEL events beyond registry inception (`rip`). Where a real credential's KEL matters — weighted multisig, key rotation, an absent delegator's KEL, witness thresholds — see the note in `src/arcviz_fixtures/fixtures/fx_vlei.py`'s module docstring for exactly what corpus-vlei-chain.md asks for that this generator does not attempt, and why.
- Round-trip any fixture through keripy's own `Reger.sources`/`Verifier.processCredential`. `working_edge_group` in `fx_edges.py` is a real, resolvable, correctly-SAIDed multi-credential edge-group scenario, generated directly via `keri.acdc.messaging.acdcmap` + `keri.core.mapping.Compactor` — but it has not been proven to traverse keripy's own verifier, which is documented (corpus-keripy-examples.md §(b)5) as unable to walk edge-groups at all (`KeyError: 'n'`). That is a keripy gap this generator does not work around, not something this corpus claims to have fixed.

None of this affects whether the SAIDs are real (they are — this is not a shortcut on the cryptography) or whether the disclosure states these fixtures target are faithfully represented. It only means "does this credential's *KEL* verify" is out of scope for every fixture here; "does this ACDC's *SAID chain* resolve and recompute" is exactly what `tests/test_fixtures_valid.py` checks.

## Schema fidelity

Every fixture's top-level shape and its `a`/`A` section's own properties are typed precisely (`additionalProperties: false`, explicit `required`). The `e` (edge) and `r` (rule) sections are typed loosely (`oneOf` [string, object], no nested property schema) rather than reproduced with the ACDC spec's own worked-example fidelity (compare `keripy/tests/spec/acdc/test_acdc_examples.py`, whose edge/rule schemas are fully elaborated). A loose schema still validates every fixture correctly; it just doesn't independently constrain edge/rule internals. See `src/arcviz_fixtures/schemas.py`'s module docstring.

## Licensing note

Fixture *content* here (attribute values, schema titles, entity names) is entirely invented — nothing is copied from keripy's test corpus or the real vLEI chain. keripy itself is Apache-2.0 (confirmed by reading `LICENSE` at its repo root); this package depends on it as a library, which Apache-2.0 permits without further obligation beyond what `pyproject.toml`'s own license already satisfies.

## Layout

- `src/arcviz_fixtures/determinism.py` — the only source of "randomness"; everything is a deterministic digest of a fixed seed.
- `src/arcviz_fixtures/schemas.py` — minimal, self-SAIDed JSON Schema builders.
- `src/arcviz_fixtures/common.py` — thin wrappers over `keri.acdc.messaging.acdcmap`/`acdcagg`/`regcept`. Read the module-level comment on `compactify` before touching any fixture that partially discloses a nested block — its semantics (collapse every direct child of the ACDC root vs. preserve exactly the shape you hand in) are the single easiest thing to get backwards here.
- `src/arcviz_fixtures/registry.py` — the `@fixture(name, depends_on=[...])` decorator; `generate.py` topologically sorts on `depends_on`.
- `src/arcviz_fixtures/fixtures/*.py` — one module per family of targets (see each module's docstring for which disclosure-matrix cells/corpus gaps it addresses).
- `src/arcviz_fixtures/generate.py` — the CLI; also writes `corpus/README.md`.
- `tests/test_fixtures_valid.py` — recomputes every fixture's SAID from its saved JSON and fails if it doesn't match; validates each fixture's schema; checks that edges naming another fixture as `n` actually resolve to that fixture's SAID.
