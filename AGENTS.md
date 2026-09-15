# AGENTS.md

Orientation and mandatory rules for anyone — human or model — working in this repository.

## What this project is

arcviz visualizes ACDCs: chainable, selectively-disclosed credentials. The hard part is not drawing a card. It is drawing a partially-disclosed directed acyclic graph without ever letting *absent*, *undisclosed*, *redacted* and *unverified* be mistaken for one another, or for *fine*.

The project is in its research phase. Read [docs/research/PLAN.md](docs/research/PLAN.md) for the phased plan and [docs/research/EVIDENCE.md](docs/research/EVIDENCE.md) for the rules of evidence, which are binding.

## Mandatory rules

1. **Evidence discipline.** Every substantive claim in `docs/research/` carries a key in [refs/sources.yaml](refs/sources.yaml), with the sentence actually relied upon quoted in the record. A model's recollection that a document exists makes it a *lead*, not a source. See EVIDENCE.md.
2. **Publication hygiene.** This repository is public. Proprietary UI captures, third-party wallet screenshots, and paywalled papers go in `.ignored/private-refs/`, which is gitignored, and are cited by public URL only. This is not recoverable after the fact.
3. **Markdown is never hard-wrapped.** One line per paragraph, however long.
4. **Sign off every commit** (`git commit -s`). No `Co-Authored-By` trailers.
5. **Nothing is asserted about ACDC semantics without checking the specification — and "the specification" is two branches, not one.** `trustoverip/kswg-acdc-specification` has two diverged branches of the **same declared version** ("Specification Status: v1.1", ACDC protocol 2.x on both). **Read `v1.1` — it is ahead on content**, carrying `E1E`, the `dp` disclosure-paths construct, the field-label restrictions and the unique-entropy rename; `main` is behind on substance and ahead only on tooling. Reading `main` as "the spec" has already produced two wrong review findings (see [reviews/2026-09-06-operator-semantics-adjudication.md](reviews/2026-09-06-operator-semantics-adjudication.md)). The vendored copy at `~/code/me/kswg-acdc-specification` goes stale — confirm its date before relying on it, and cite the branch and commit you read. Real credentials live in the keripy and keria test corpora and in the vLEI family.

## Layout

| Path | Holds |
|---|---|
| `docs/design/decisions.md` | **The design constraint record.** Read before proposing any layout or treatment. |
| `docs/research/` | Findings, principles, threat model, affordance inventory |
| `docs/research/prior-art/` | One report per audited source of prior art |
| `refs/sources.yaml` | The citation record |
| `refs/captures/`, `refs/screenshots/` | Republishable local captures |
| `.ignored/private-refs/` | Captures that may not be republished — gitignored |
| `corpus/` | ACDC fixtures: research instrument now, conformance corpus later |

## Sibling projects

`~/code/me/entviz` and `~/code/me/entviz-js` (identifier visualization; arcviz consumes `@entviz/react`), `~/code/me/coia` (alias convention), `~/code/me/papers` (the essays this design rests on: `oia.md`, `amp-diff.md`, `intent-boundaries.md`).
