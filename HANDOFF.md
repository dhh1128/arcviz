# Handoff

Written 2026-09-15, at the close of the session that produced everything here. Read this before anything else in the repository.

## Start from this decision

**320 CSS pixels is a correctness floor, not a design target** ([DD-10](docs/design/decisions.md)). Nothing may break, clip, lose information or require horizontal scrolling at 320 — that is WCAG SC 1.4.10, Level AA, unchanged in WCAG 2.2, and it is testable in CI. But the layout is *not designed to* 320. Packing rules are width-dependent: three compact chips across at 320, four at 360, mid-floor cards sharing a row above some threshold and not below it.

The distinction matters because a 320 px retest reported **every artifact in this repository as failing**, and that reads as a verdict on the design. It is not. The real defect is that every artifact was **authored at a fixed width** — gate rails plus a hard-coded 350 px board. A responsive component has no authoring width, and choosing a different fixed number would reproduce the same fault. Conformance failure and layout suboptimality were being measured by one instrument and reported as one thing.

So the first substantive work is not a redesign. It is rebuilding at least one artifact **responsively**, and seeing which of the recorded findings survive when width is a variable rather than a constant.

## What arcviz is

A React and Python component that visualizes ACDCs: chainable, selectively-disclosed credentials. The hard part is not drawing a card. It is drawing a partially-disclosed directed acyclic graph without ever letting one kind of absence pass for another, or for *fine*.

The intended deliverable is a language-independent rendering specification with a shared conformance corpus, a Python reference implementation and a React component — entviz's shape, for entviz's reason.

## Reading order

1. **[docs/design/decisions.md](docs/design/decisions.md)** — ten decisions, each with what it forbids and what would reverse it. This is the constraint record; read it before proposing anything.
2. **[docs/research/principles.md](docs/research/principles.md)** — sixteen principles in dependency order, six acknowledged tensions, and a *retired claims* list. Four claims have been withdrawn after review and each was re-derivable from material still in the corpus; that list is the guard against re-importing one.
3. **[docs/research/disclosure-matrix.md](docs/research/disclosure-matrix.md)** — the keystone. Six axes, twelve indistinguishable pairs, nineteen rendering rules each with a compliance test.
4. **[docs/design/shape-catalog.md](docs/design/shape-catalog.md)** — fourteen layout cases forming a minimal covering set, each with an observable that constitutes failing it. This is the instrument design proposals are tested against.
5. **[docs/research/threat-model.md](docs/research/threat-model.md)** — nine adversaries attacking the renderer specifically.
6. Everything else as needed. `docs/research/prior-art/` holds ten audited streams; `docs/design/charrette/` holds four independent design proposals plus their adversarial verification and synthesis.

## Decision status

**Ratified** — DD-1 orientation (presented node at top, references descend), DD-2 the 320 minimum, DD-3 edge labels rendered inside the issuer boundary, DD-7 vertical primary axis, DD-9 holder and verifier both first-tier, DD-10 the floor-versus-target distinction.

**Proposed, and each needs work before it can be ratified** —

- **DD-4**, the pile is refuted and focus is in place. *Its stated reasoning no longer holds.* Layering was retired on a measurement that reverses at 320: compression packs three chips across rather than four, so its rest register is 399–453 px against layering's width-indifferent 436, and the "34% taller" ordering is gone. Layering now survives retirement only because it silently clips about 20 px of a state word — which is disqualifying on its own terms, but is not the argument the decision makes. **Re-argue it on the clipping ground or reopen it.**
- **DD-5**, compression with a second floor for budgeted states. Its *justification* stands (both floors are fixed forms carrying the same content at any width). Its *pricing* is void — every cost figure is 360-specific, and at 320 two mid-floor cards need 308 px against 288 available, so budgeted cards can never share a row. **Restate the costs as width-dependent rules.**
- **DD-6**, verification renders per card. **Ratifiable as written** — the ledger saving is 30.2% at 320 against 29.4% at 360, and the co-visibility argument that decided it is width-independent.
- **DD-8**, intra-card collapse. Newly opened, unbuilt, and its central claim is marked as inference: UI collapse introduces a kind of not-showing the matrix does not contain — *present, disclosed, hidden by the viewer's own interface* — reversible by the viewer where undisclosed is not reversible at all. Attack that before building on it.

**Open** — the holder-facing presenter indicator, where the full-apparatus ruling collides with AF17's "no presenter indicator at all"; and the element floor, which has never been stated (the sliver measures 248 px inside a 320 px viewport, so inner components already go narrower than the conformance width, and we have been using one word for two numbers).

## The immediate work

1. **Rebuild one artifact responsively** rather than at a fixed frame. This is what DD-10 demands and it precedes everything else.
2. **Design the perimeter-class floor glyphs.** The sliver finding made them load-bearing: at 248 px, perimeter states survive where area-class states degrade into words.
3. **Define a 248 px stale-banner form.** The full banner overflows an expanded card at that width by about 11 px of run.
4. **Re-argue DD-4, restate DD-5's costs, ratify DD-6.**
5. **Add a shape-catalog case for a card with more content than the viewport.** SC7 covers card-internal *disclosure states*; nothing covers card-internal *volume*, and a credential with forty attributes is the ordinary case rather than an edge one.
6. Then the wireframe and interaction spec — deliberately not started here, because it deserves a session that can iterate rather than one landing it in a single pass.

Twelve fixture gaps remain, listed in the shape catalog's §(d), with the generator at `tools/fixtures/` ready to close them.

## Disciplines that were earned expensively

Each of these exists because it was violated first.

**Recollection is a lead, not a source.** A paper was cited in a plan on the strength of its line count; reading it produced the opposite of what had been asserted. The worked example is in [docs/research/EVIDENCE.md](docs/research/EVIDENCE.md).

**Read the `v1.1` branch of the ACDC spec, not `main`.** They have diverged, both declare the same version, and `v1.1` is ahead on content. Reading `main` as "the spec" produced two wrong review findings from a panel that verifies its own work — verification could not catch it, because both quoted `main` accurately. The error was in which artifact to read.

**Nothing inside a render may name a fixture or state a fact the geometry withholds.** All four charrette designers solved the convergence geometry correctly and then leaked the answer through labels, one of them in a caption directly contradicting its own claim.

**Derive credential facts; never assert them.** A proposal printed `I2I` on five diamond edges and footnoted it as computed by the injection rule; no diamond fixture carries an operator or an issuee, so the correct default is `NI2I`.

**Say how a number was obtained.** Two figures circulated as measurements and were not: the compact-floor dimensions are design choices embodied in the mocks, and a 352 px run-length could not be reproduced. **Validate the instrument before trusting it** — the 320 retest checked that its method reproduced published 360 figures to within 2 px before reporting anything new.

**Never rank the two audiences** (DD-9). Holder and verifier are co-equal; a tension between them is resolved by serving both or by a grounded difference, never by priority.

## What only Daniel can do

The small-n legibility probe. Every floor figure in this repository is a design choice, and the claim that any particular size is where legibility gives out is perceptual and has never been tested on a human. It is the only instrument that can discharge DD-4's actual reversal condition, and no agent can run it.

## State

53+ commits, working tree clean, pushed to `github.com/dhh1128/arcviz` (public). 35 research and design documents, 29 generated fixtures with a passing test suite at `tools/fixtures/`, and captured sources under `refs/` with a citation record. Non-republishable material — proprietary UI analysis, anything derived from the PII-bearing credential chain — is under `.ignored/` and gitignored; the real chain lives outside the repository at `/home/daniel/xfer/credential.cesr` and is never copied in.
