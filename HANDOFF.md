# Handoff

Written 2026-09-15, at the close of the session that produced everything here. Read this before anything else in the repository.

## Start from this decision

**320 CSS pixels is a correctness floor, not a design target** ([DD-10](docs/design/decisions.md)). Nothing may break, clip, lose information or require horizontal scrolling at 320 — that is WCAG SC 1.4.10, Level AA, unchanged in WCAG 2.2, and it is testable in CI. But the layout is *not designed to* 320. Packing rules are width-dependent: three compact chips across at 320, four at 360, mid-floor cards sharing a row above some threshold and not below it.

The distinction matters because a 320 px retest reported **every artifact in this repository as failing**, and that reads as a verdict on the design. It is not. The real defect is that every artifact was **authored at a fixed width** — gate rails plus a hard-coded 350 px board. A responsive component has no authoring width, and choosing a different fixed number would reproduce the same fault. Conformance failure and layout suboptimality were being measured by one instrument and reported as one thing.

So the first substantive work is not a redesign. It is rebuilding at least one artifact **responsively**, and seeing which of the recorded findings survive when width is a variable rather than a constant.

**Done, 2026-09-15.** Arm B is rebuilt with no authoring width — [docs/design/layout-comparison/arm-b-responsive.html](docs/design/layout-comparison/arm-b-responsive.html), results in [RESPONSIVE.md](docs/design/layout-comparison/RESPONSIVE.md). It is the repository's first artifact that passes at 320, and at every width from 300 to 800. Read that file before the retest, which it partly supersedes. The short version: the packing rules are now rules (`n = ⌊(W−24)/84⌋` chips across, `62/n` px of column per object), the retest over-predicted the focus register's growth at 320 by a factor of three, and its 399–453 px range for the rest register turned out to be an unmade decision about packing rather than measurement uncertainty. Four things the fixed-width mocks could not show came out of it, listed under "What the rebuild found" below.

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

- **DD-4**, the pile is refuted and focus is in place. *Its stated reasoning no longer holds.* Layering was retired on a measurement that reverses at 320: compression packs three chips across rather than four, so the "34% taller" ordering is gone. Layering now survives retirement only because it silently clips about 20 px of a state word — which is disqualifying on its own terms, but is not the argument the decision makes. **Updated 2026-09-15:** the 399–453 px range that produced this was not measurement uncertainty. Rendered responsively, the two candidate packing rules give 379.8 px and 495.8 px, and layering's 436 px sits between them — so **the comparison cannot be re-argued until the packing rule is decided.** Re-argue it on the clipping ground, or reopen it, but settle packing first.
- **DD-5**, compression with a second floor for budgeted states. Its *justification* stands (both floors are fixed forms carrying the same content at any width). Its *pricing* was void — every cost figure was 360-specific. **Restated 2026-09-15** as width-dependent rules, measured on a render: `⌊(W−24)/84⌋` chips across a row at `62/n` px of column per object, `⌊(W−24)/158⌋` mid forms, two mids first sharing a row at 340 px. The price of the second floor is a **doubling** of the rest register at both 320 and 360, steeper than the ≈46% on record. Against it, a new argument in its favour: the mid form is the only non-expanded tier at which DD-3 holds for a node with more than one out-edge.
- **DD-6**, verification renders per card. **Ratifiable as written** — the ledger saving is 30.2% at 320 against 29.4% at 360, and the co-visibility argument that decided it is width-independent.
- **DD-8**, intra-card collapse. Newly opened, unbuilt, and its central claim is marked as inference: UI collapse introduces a kind of not-showing the matrix does not contain — *present, disclosed, hidden by the viewer's own interface* — reversible by the viewer where undisclosed is not reversible at all. Attack that before building on it.

**Open** — the holder-facing presenter indicator, where the full-apparatus ruling collides with AF17's "no presenter indicator at all"; the packing rule, global or band, which blocks DD-4; and the element floor, which has never been stated (the sliver measures 248 px inside a 320 px viewport, so inner components already go narrower than the conformance width, and we have been using one word for two numbers). The element floor now has an instrument — `arm-b-responsive.html?hostw=` pins the component's width independently of the viewport — and arm B turns out not to have a floor in the sense of a width where it breaks: swept to 170 px nothing clips, and what changes is the stale banner's form at two measured thresholds.

## What the rebuild found

Four things, all in [RESPONSIVE.md](docs/design/layout-comparison/RESPONSIVE.md) §5, and each needs a ruling.

**DD-1 is at risk, and it is Ratified.** It says edges point downward, from a node to whatever its `e` section references. At 320 arm B's packing draws the `qvi` edge from ITEM 02 to ITEM 01 **ascending** — and this is not a narrow-width artifact, because at 480 a different edge ascends instead. Any wrap boundary falling between an edge's endpoints can invert its drawn direction. Worse at the authored width than anyone noticed: arm B honours DD-1 for only 2 of its 8 edges at 360, with six drawn horizontally. Either the claim narrows to "no edge ascends", or packing is constrained to guarantee it, or DD-1 governs rank rather than drawn direction — which is a real weakening and should be written down as one.

**The packing rule is an open decision, and it blocks DD-4.** Rows are either pure viewport economy (wrap globally, which is what the caption inside the render says) or they preserve the authored bands so a row means something. Rendered, the two give 379.8 px and 495.8 px at 320, and arm A's reconstructed 436 px sits *between* them. DD-4's height comparison has no answer until this one does.

**DD-3 cannot be satisfied at the 76×44 floor, at any width.** ITEM 04 has two real edge labels (`shortPath`, `longPath`) and the chip fits one. The old mock shed both silently and drew bare arrows; the rebuild marks the shed. The mid form carries both — so DD-5's second floor is the only non-expanded tier at which DD-3 holds for a multi-edge node, which is an argument DD-5 does not currently make.

**The frontier gutter's locality guarantee was a property of the 360 packing.** At 360 both frontier-bearing objects land in column one, adjacent to the gutter. At 320 they do not, and the first build drew their stubs across the intervening objects, so the render appeared to attribute two blinded edges to the wrong item. It now routes a near-node nub instead — a coinage with one exhibit.

## The immediate work

1. ~~Rebuild one artifact responsively.~~ Done — arm B. Arm A is still fixed-width, so the DD-4 comparison is rendered against reconstructed.
2. ~~Design the perimeter-class floor glyphs.~~ Done — H6-possibly withdraws the frame to four corner ticks, H2-guessable makes the bottom edge porous, with the doubled bottom edge reserved for H3 as its contrast partner. RESPONSIVE.md §7 has the channel assignment, the declared scope widening at the chip floor, and the one composition limit. Whether a viewer can *identify* them is still the small-n probe's question and is not claimed.
3. ~~Define a 248 px stale-banner form.~~ Done — three tiers by available run, measured, in RESPONSIVE.md §8. The 248 px form sheds the as-of, which costs nothing because the card's T-line carries it; a card with no T-line may not use it. Note the correction: the overflow is the stress board's 46 px inset, not a 320 px fact — arm B's own card is 288 px at 320 and the full banner fits.
4. **Re-argue DD-4, restate DD-5's costs, ratify DD-6.** DD-5's restatement now has its rules and its price (a doubling of the rest register, steeper than the ≈46% on record). DD-4 waits on the packing decision above.
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
