# Arm B rebuilt responsively — what survives when width is a variable

[arm-b-responsive.html](arm-b-responsive.html) is the first artifact in this repository with no authoring width. It carries the same thirteen objects as [arm-b-compression.html](arm-b-compression.html) and the same host stubs, but every position in it is produced by a packing rule evaluated against the width the component is given, and every connector is routed after layout against measured geometry. [DD-10](../decisions.md) called for exactly this before anything else, on the ground that the 320 retest was measuring conformance failure and layout suboptimality with one instrument: the defect was fixed-width authoring, and picking a different fixed number would have reproduced it.

This document states what the rebuild measured. Captures are in [responsive-sweep/](responsive-sweep/).

## 1 · Method, so the numbers can be audited

Headless Chrome 153 on Linux, driven through the DevTools protocol (`puppeteer-core` against `/usr/bin/google-chrome`), viewport set via `Emulation.setDeviceMetricsOverride` rather than a window size — which is why no iframe trick is needed here and the retest's 500 px clamp does not apply. Element boxes from `getBoundingClientRect`, overflow from `documentElement.scrollWidth − clientWidth`, content bleed from each object's `scrollWidth/scrollHeight` against its client box. Every figure below is a render, not a reconstruction.

**Instrument validation, before any new claim.** Three checks against published numbers:

- The instrument reproduces the retest's §1 conformance result for the *existing* arm B file exactly: at a 320 px viewport `arm-b-compression.html` has `scrollWidth` 360 and 40 px of horizontal overflow.
- It reproduces the 360 px document height the shape gallery published for the compression arm: 2,371 px measured on `documentElement`, against 2,347 px plus the 24 px body margin the gallery's README records.
- The rebuilt packing rule reproduces the authored mock's hand-set coordinates. At 360 px the thirteen objects land at x = 22, 106, 190, 274 — the mock's own four column positions, byte-for-byte — with no coordinate anywhere in the new file. The rule and the hand-placement agree, which is the strongest evidence available that the rule is the one the mock was expressing.

Where a number below differs from the retest's, the retest's was a reconstruction (it re-flowed extracted elements and recomposed columns arithmetically) and this one is a render. Both are stated.

## 2 · Conformance: the file passes, at every width tested

Zero horizontal overflow from 300 px to 800 px, in every mode — rest and focus, both packing rules, one floor and two, glyphs and words. Nothing paints outside the gate. No object's content exceeds its box. The two reported `scrollWidth` excesses at items 10 and 11 are the new perimeter glyphs sitting *on* the border line at −1.5 px, which is where they are meant to be, not content escaping.

This is the certification surface the retest's first required change asked for. **DD-2's "consequence for work already done" no longer applies to everything in the repository — it now applies to everything except this file.**

## 3 · The packing rule, stated as a rule

DD-5's price list is void because every figure in it was 360-specific. The rule the responsive build makes explicit:

> **Chips across a row: `n = ⌊(W − 24) / 84⌋`**, where `W` is the width given to the component. 84 px is the 76 px chip plus the 8 px inter-object gap; 24 px is the 10 px gate border plus the 14 px frontier gutter, minus the gap that the last chip in a row does not pay.

Measured breakpoints, by sweeping every integer width from 300 to 800: the first width at which each packing appears is **360, 444, 528, 612, 696, 780** — that is `84n + 24` at every step, with no deviation.

**Marginal column per added object = `62 / n` px**, where 62 px is the row pitch (44 px chip + 18 px row gap). That gives 20.7 px at 3-across and 15.5 px at 4-across, which reproduces both figures the retest and the arms README circulate (≈20.7 and ≈15.5) from the rule rather than from arithmetic on a fixed frame.

For DD-5's second floor, measured the same way with `?floor=two`:

- **Mids across a row: `⌊(W − 24) / 158⌋`.** Two mids first share a row at **W = 340**, verified by sweeping single pixels across the boundary: at 339 the register is 761.8 px and at 340 it drops to 581.8 px. The retest's "two mid forms need 308 px and can never share a row at 320" is correct, and now has its boundary. The thing to carry forward is the threshold, not the width it was discovered at — 320 happens to sit below it, and so does every viewport down to the conformance floor, but 360 and 375 do not.
- **Mixed rows: one mid plus `⌊(W − 182) / 84⌋` chips.** One mid and one chip fit at 320 (234 px of 288 available), which is what the retest measured.

| viewport | across | board column | object extent | marginal px/object | overflow |
|---|---|---|---|---|---|
| 320 | 3 | 379.8 | 292 | 20.7 | 0 |
| 360 | 4 | 308.1 | 230 | 15.5 | 0 |
| 480 | 5 | 246.1 | 168 | 12.4 | 0 |
| 768 | 8 | 163.5 | 106 | 7.8 | 0 |

Rest register, global packing. "Object extent" is first-row top to last-row bottom, which is the figure to compare across modes because it excludes the caption's own text reflow.

## 4 · The registers, all four modes

| mode | 320 | 360 | 480 | 768 | 320 over 360 |
|---|---|---|---|---|---|
| rest, global packing | 379.8 | 308.1 | 246.1 | 163.5 | +23.3% |
| rest, band packing | 495.8 | 362.1 | 362.1 | 341.5 | +36.9% |
| rest, two floors, global | 761.8 | 600.1 | 420.1 | 309.5 | +26.9% |
| focus on ITEM 08, global | 756.9 | 700.7 | 569.1 | 548.5 | +8.0% |
| focus, band packing | 934.9 | 754.7 | 685.1 | 664.5 | +23.9% |
| focus, two floors, global | 1,110.9 | 964.7 | 715.1 | 632.5 | +15.2% |

Board column in CSS pixels. The rest-register growth of +23.3% and +36.9% lands inside the retest's predicted +22–39% band at both ends, which is the fourth instrument check.

**Two results that correct published figures.**

**The retest over-predicted the focus register's growth at 320.** It reported +22–30%; the measured figure is **+8.0%** under global packing and +23.9% under band packing. The reconstruction added a chip row at 320 that a real reflow does not add: the expanded card already forces a row break, so the objects around it were never packed four-across in the first place and lose nothing when the width drops. Most of the growth that does occur is the card itself getting taller as it narrows (374.6 px at 360, 421.1 px at 320), not the chips repacking.

**Band packing throws away width above 360 and global packing does not.** Band packing's rest register is 362 px at 360, 362 px at 480 and 341 px at 768 — it stops improving, because the band boundaries force four rows no matter how much room there is. Global packing goes 308 → 246 → 163 over the same range. Below 360 the ordering inverts: band packing costs **+30.5%** more column than global at 320 (495.8 against 379.8).

## 5 · Findings only a responsive render could produce

**F1 — DD-1's orientation does not survive packing, and the violation is not a narrow-width artifact.** DD-1 is *Ratified*: the presented node sits at the top and edges point downward, from a node to whatever its `e` section references. Measured direction of the eight drawn edges:

| width | descending | horizontal | ascending |
|---|---|---|---|
| 360 | 2 | 6 | 0 |
| 320 | 3 | 4 | **1** |

At 320 the `qvi` edge from ITEM 02 to ITEM 01 is drawn **ascending** — a reference edge pointing up the page, which is the thing DD-1 forbids. At 360 the same edge is horizontal. And the inversion is not confined to narrow widths: at 480 the `shortPath` edge from ITEM 04 to ITEM 05 ascends instead. Any wrap boundary that falls between an edge's two endpoints can invert its drawn direction, so this is a property of wrap-packing, not of 320.

Worth stating plainly even at the authored width: **arm B already honours DD-1 for only 2 of its 8 edges at 360.** Six are drawn horizontally, three of those leftward. Compression's floor packing and DD-1's orientation are in tension at every width; the fixed-width mock hid that because a horizontal edge does not look like a violation the way an upward one does.

**F2 — the frontier gutter's locality guarantee is a property of the 360 packing, not of the design.** The stress board's README records that blinded edges and hole fringes "enter it locally, keeping structure's sublinearity at mobile aspect ratio". That holds at 360 because both frontier-bearing objects — ITEM 09 and the second hole — happen to land in column one, adjacent to the gutter. At 320 the packing moves them away, and a stub drawn all the way to the gutter would either pass behind the objects in between or assert a path through them. The first build did exactly that, and the result was worse than a lost line: the open arrowheads emerged at the gutter beside a *different* object, so the render appeared to attribute two blinded edges to ITEM 06.

The rebuild routes a **near-node nub** instead whenever the object is not adjacent to the gutter. That is consistent with the band's own wording inside the render ("entry points are near-node facts") and with arm C's rule that the edge is drawn to the frontier boundary at every tier of its near node. It is nonetheless this rebuild's coinage, forced by responsiveness, with one exhibit behind it.

**F3 — DD-3 cannot be satisfied at the 76×44 floor, at any width.** DD-3 is *Ratified*: every drawn edge carries its label. ITEM 04 (`diamond_depth_origin`) has two out-edges whose real labels are `shortPath` and `longPath`. One label plus its direction glyph already spends most of the chip's ~65 px of content width; two do not fit, and the floor form is fixed, so no viewport width repairs it. The authored mock shed both labels silently and drew two bare arrows. This rebuild shows `⋯2 edges` instead — neither label, and a mark saying how many are not being shown.

The mid form carries both labels comfortably. **So DD-5's second floor is not only about parameters: it is the only non-expanded tier at which DD-3 holds for a multi-edge node.** That is an argument for the second floor that DD-5 does not currently make.

Marking the shed rather than dropping it silently is an **inference, flagged**: no source requires it. It follows from applying the matrix's refusal to let one kind of not-showing pass for another to a kind the matrix does not contain — the same move DD-8 makes for collapse, applied at the floor instead.

**F4 — the port's direction glyph is a derived fact that was being authored by hand.** In the fixed-width mock, ITEM 05's port reads `baseline ↘` in frame B1 and `baseline ↓` in frame B2 — the same edge, two glyphs, because the frames have different geometry and the arrow was written to match. A responsive render has no such moment: the glyph is computed from the routed path or it is wrong. It is computed here.

**F5 — a connector hidden behind an opaque object is a disclosure defect, not an aesthetic one.** A line that disappears under a card reads as a line that *ends* there. The rebuild therefore routes horizontal runs only in the gaps between rows and vertical runs only in a lane that is free of objects in every row it crosses, searching the gap midpoints of the intervening rows for the one nearest the target. This belongs in the rendering specification: *no connector segment may be occluded by a drawn object*.

**F6 — the element floor is now instrumented, and it is not the viewport floor.** DD-10 leaves open that we have been using one word for two numbers. `?hostw=` pins the component's own width independently of the viewport, which is the instrument that question needs: an inner component can be narrower than the conformance width without the viewport ever being so, and the sliver's 248 px inside a 320 px viewport is exactly that case. Swept a pixel at a time from 170 px to 360 px at a 768 px viewport, nothing clips anywhere and the floor forms are unchanged by construction; what changes is the expanded card, at two measured points. **At a component width of 283 px and above** (card 251 px) the stale banner's full form holds one line. **From 209 px to 282 px** (card 177–250 px) the short form holds one line. **At 208 px and below** the short form wraps, and keeps wrapping down to 170 px without ever clipping. So arm B has no element floor in the sense of a width where it breaks; it has two thresholds where a form changes, and both are in §8.

## 6 · What this means for the decisions under review

**DD-4 — the retest's range was not measurement error, it was an unmade decision.** The retest could not choose between 399 px (global repack) and 453 px (rank-row-preserving) for arm B's rest register at 320, and reported the band, which put arm B inside arm A's error band and dissolved the height ordering. Rendered, the two rules give **379.8 px and 495.8 px** — and arm A's reconstructed 436 px sits *between* them. So the comparison does not have an answer until the packing rule has one. With global packing arm B is clearly shorter than arm A at 320; with band packing it is clearly taller. **DD-4's height argument cannot be re-argued before the packing rule is settled**, which makes the packing question the blocking one, not an implementation detail.

Nothing here touches DD-4's actual reversal condition, which is legibility of the compact floor and belongs to the small-n probe.

**DD-5 — the mechanism survives, the price is restated, and there is a new argument for it.** The packing rules in §3 are the restatement the retest asked for, expressed as functions of width rather than as figures. The price of the second floor measured on this rebuild is a **doubling** of the rest register — 761.8 against 379.8 at 320 (+100.6%), 600.1 against 308.1 at 360 (+94.8%). That is steeper than the ≈46% the arms README records, and it should not be read as contradicting it: this is arm B plus DD-5's floor exception on arm B's own content, not arm C, which has a distance term and different card content. The comparable claim is the one against this rebuild's own baseline.

Against that price, F3 adds a benefit DD-5 does not currently claim: the second floor is where DD-3 becomes satisfiable for multi-edge nodes.

**DD-6 — not re-tested here.** This rebuild has no central-ledger variant, so nothing in it bears on the per-card-versus-central question. The retest found DD-6 ratifiable as written and its argument is width-independent; that stands untouched.

**DD-1 — newly at risk, from F1.** It is *Ratified*, and arm B violates it at 320 and honours it for only a quarter of its edges at 360. Either the orientation claim is narrowed to "no edge ascends" — which packing can be constrained to guarantee — or DD-1 is understood to govern rank assignment rather than drawn direction, which is a real weakening and should be written down as one.

## 7 · The perimeter-class floor glyphs for H6 and H2

The stress board recorded the wound: of the three card-level deformations only the stale frame-break survives the floor, because it is a perimeter event, while the corner-withdrawn frame and the transparent `a`-region are area signatures. At 76×44 items 10 and 11 kept their budgeted states as six-point words, which is the P9 failure mode exactly. The retest sharpened it — words die at 320 by clipping or shedding, geometry survives — and made the glyphs load-bearing rather than an improvement.

The design principle is that a rectangle's perimeter offers a small number of **independent channels**, and each state gets one, so states compose instead of competing:

| state | channel | treatment | scope |
|---|---|---|---|
| H7 — not in hand | multiplicity + fill | double border, shared hatch | whole object |
| stale | top edge, interrupted | break carrying its word | whole artifact |
| **H6-possibly** | **completeness** | **frame withdrawn to four corner ticks** — 11 px at chip and mid, 16 px at card | whole artifact |
| **H2-guessable** | **bottom edge, continuity** | **porous bottom rule**, 3 px on / 4 px off | the unit |

H6's treatment is the stress board's own coinage scaled down rather than a new invention, which is the right call: it was already perimeter-class and the claim that it "does not read at 76 px" turns out to be false once it is drawn there. See `responsive-sweep/rest-320.png`, item 10.

H2's is new. It is chosen against three constraints at once. Rule 8 forbids any privacy-asserting treatment for H2, so it cannot be a lock or anything lock-adjacent. Rule 1 requires H2 and H3 to be pairwise distinct, and a single channel with two values gives that cleanly: **H2 is the porous bottom edge and H3 is the doubled bottom edge** — the wall is either leaky or reinforced. And it has to survive at 44 px of height, which a bottom edge does and an interior region does not.

**Scope, declared rather than glossed.** H6 is a whole-artifact state, so corner withdrawal is correctly scoped at every tier. H2 is a *unit* state. Above the floor the porous edge marks the unit's own region — the `a` block's boundary inside the expanded card, the mini region inside the mid form. Only at 76×44, where there is no room for a region, does it move onto the whole box. That is a widening of scope: the chip says "something in here is guessable" where the card says "this block is". It is recorded here because a reader could otherwise take the chip to mean the whole credential is guessable.

**Composition limit.** A withdrawn frame has no continuous bottom edge, so an object that is both H6-possibly and H2-guessable cannot carry both glyphs. No corpus fixture is both, and the combination may be incoherent in any case, but it is not ruled out by anything and the vocabulary should say so.

**Channels still free** for states not yet designed: the left edge, the right edge, stroke weight, and corner *radius*. The doubled bottom edge is reserved for H3 and should not be spent on anything else.

**What is not claimed.** The glyphs carry state *presence* and are distinguishable from their neighbours and from a plain chip — that is geometry and it is demonstrated. Whether a viewer can *identify* which state a glyph means without having learned the vocabulary is perceptual, is exactly the question P9 reserves, and nothing here substitutes for the small-n probe. `?h6h2=words` renders the words-only floor beside it for the probe to compare against; see `responsive-sweep/words-320.png`.

## 8 · The stale banner's width-dependent form

The retest found that the full banner overflows a 248 px card by about 3 px and that nothing in the vocabulary defines a shorter form. Measured here at the card's own 8.5 px type, including the text's 8 px of horizontal padding:

| form | text width | row needed |
|---|---|---|
| `STALE — as-of 2026-06-14 · age 92 d exceeds policy PT72H` | 239.0 px | 247 px |
| `STALE — age 92 d exceeds policy PT72H` | 166.1 px | 174 px |
| `STALE — age 92 d > policy PT72H` | 139.0 px | 147 px |
| `STALE · 92 d > PT72H` | 90.5 px | 98 px |
| `stale` (the chip floor's existing form) | 26.9 px | 35 px |

The 239.0 px measurement corroborates the retest's 240.5 px to within 1.5 px, which is the fifth instrument check.

**The rule, in three tiers.**

1. **Banner row ≥ 247 px** — the full form.
2. **174 px ≤ row < 247 px** — the as-of sheds: `STALE — age 92 d exceeds policy PT72H`. This is the 248 px form the retest asked for; at a 248 px card the row is 245 px and the short form fits with 71 px to spare.
3. **Below 174 px** — the same short form, wrapped. It never clips at any width: the banner text is `white-space: normal` with `overflow-wrap: anywhere`, so overflow is structurally impossible and the conformance floor is met by the wrap rather than by the shed.

**Why shedding the as-of loses nothing, and the condition on that.** The card's T-line carries `as-of 2026-06-14T00:00Z` verbatim, so the fact stays in the card and SC 1.4.10's "without loss of information" is satisfied. **A card with no T-line may not use the short form** — the shed is conditional on the redundancy, not on the width alone.

Implemented as a container query on the card (`max-width: 230px` against its content box; the banner row is the content box plus 18 px). The threshold is set two pixels above the 229 px physical requirement so that no width falls in a band where the full form wraps instead of shedding — verified by sweeping the element width one pixel at a time: at a 251 px card the full form is one line, at 250 px the short form is one line, and there is no width in between at which anything wraps unnecessarily.

**A correction to where the retest's finding applies.** Arm B's responsive card is inset only by the gutter and its padding, so at a 320 px viewport it is **288 px wide** and the full banner fits with 38 px to spare. The 248 px card is the *stress board's* geometry — its cards sit at a 46 px left inset — so the overflow the retest found is a fact about that inset, not about 320 px. Both statements matter: the short form is needed, and it is not needed at 320 in this arm. The general rule is stated against available run for that reason.

Item 09's abbreviated cardinality line, which the retest measured clipping by ~1 px at 248, is an arm A sliver form and does not exist in arm B at any tier; at the chip floor item 09 carries `1–2 dest.` only. It is untouched here.

## 9 · What this does not do

- **Arm A is not rebuilt**, so the DD-4 comparison is still arm-B-rendered against arm-A-reconstructed. §6 argues that the packing question blocks the comparison anyway.
- **No central-ledger variant**, so DD-6 is not re-measured.
- **The shape gallery has no 320 variant yet**, and its width-specific captions are still wrong at 320.
- **The two files that fail their own width claims at 360** — focus-sequence's gauge row and arm A's gauge commentary — are untouched.
- **Nothing here is a legibility finding.** Every floor coordinate in this file is still a design choice embodied in a mock, exactly as the shape gallery's README records, and the new glyphs add two more. The small-n probe is the only instrument that can discharge any of it.

## 10 · Open, and needing a ruling

1. **Which packing rule — global or band?** Global treats rows as pure viewport economy, which is what the caption inside the render says, and spends extra width; band preserves the authored bands so that a row means something, and ignores width above 360. It decides DD-4's height comparison (§6), and it decides whether a reader who infers meaning from rows is reading correctly or being misled.
2. **DD-1 under wrap-packing.** Accept that a drawn edge may ascend, constrain packing so none does, or narrow DD-1 to govern rank rather than drawn direction.
3. **The near-node nub** (F2) — a coinage with one exhibit.
4. **The marked shed `⋯N edges`** (F3) — an inference, and a decision about whether marking a shed is better than showing one of several labels.
5. **The H2 porous-bottom glyph and its reserved H3 partner** (§7) — new design, no precedent in any audited product, and the H2 scope widening at the chip floor is declared rather than resolved.
