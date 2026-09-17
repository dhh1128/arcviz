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

Zero horizontal overflow from 300 px to 1,920 px, in every mode — rest and focus, both packing rules, one floor and two, glyphs and words, capped and uncapped. Nothing paints outside the gate. No object's content exceeds its box. The two reported `scrollWidth` excesses at items 10 and 11 are the new perimeter glyphs sitting *on* the border line at −1.5 px, which is where they are meant to be, not content escaping.

This is the certification surface the retest's first required change asked for. **DD-2's "consequence for work already done" no longer applies to everything in the repository — it now applies to everything except this file.**

**One correction, recorded because the mistake is the interesting part.** The first version of this file was swept from 300 px to 800 px only, and passed. It was never opened at a desktop width, where two separate things were wrong — §10. And when the reader's key and the width readout were added to fix the second of them, the readout was `white-space: nowrap` and overflowed a 320 px page by 61 px. That is the retest's own required change 6 — apparatus that makes a document's width claim false while the render inside it passes — reproduced in the file written to fix it, within a day. The audit now covers the whole page at nine widths in seven modes rather than the component alone, which is what should have been measured from the start.

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

Rest register, global packing. "Object extent" is first-row top to last-row bottom, which is the figure to compare across modes because it excludes the caption's own text reflow. **The 768 px row is the packing rule's behaviour, not the component's:** the component now caps at 480 px by default and turns surplus width into margin, for the reason in §10. Every figure in these tables is a property of the rule and remains true of it; what changed is which widths the rule is allowed to see.

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

## 10 · The maximum width, and the two things that were wrong above 800 px

The first version of this file had no upper bound, on the reasoning that a responsive component has no authoring width. That reasoning is right about the *floor* and wrong about the ceiling, and the error was caught the only way it could be — by opening the file at an ordinary desktop width, which the width sweep never did.

**The layout degenerates into the axis DD-7 refused.** `n = ⌊(W − 24)/84⌋` keeps growing, so at 1,280 px and above all thirteen objects land in **one row**, 102 px tall. The diamond is gone, the shared ancestor is gone, both descending edges have nowhere to descend to, and the router's lane system has no channels because there are no inter-row gaps left. What remains is a horizontal strip of thirteen tokens.

This is not merely ugly. DD-7 is *Ratified*, and it chose a vertical primary axis on the ground that a horizontal one cannot work at narrow widths; unbounded global packing converges on exactly that horizontal axis, and does so at every ordinary desktop width. **A responsive layout can violate a ratified decision by having no ceiling just as surely as by having no floor.** DD-7's own text anticipates the remedy — it says a desktop or landscape variant "would be a second layout rather than a reversal" — so the conservative move is to refuse the fan-out rather than to invent that second layout by accident.

The component therefore caps at **480 px** and centres, turning surplus width into margin. At this load that gives five across and three rows, so the graph stays a vertical stack at every width from 300 px upward. **The number is a design choice nobody has ruled on**, which is why it is `?maxw=`: `?maxw=none` renders the degeneration, `?maxw=360` pins the packing every earlier artifact was authored at, `?maxw=443` is the widest value that still gives four across.

**The second thing wrong above 800 px was that the exhibit was unreadable.** The component was a full-bleed sibling of an 860 px centred prose column, so it did not even align with the text; and nothing anywhere on the page said what a box was, what the hatched strip meant, or what any mark stood for. The page now opens with a plain-language orientation, states the two interactions, carries a live width readout, and has a reader's key — all outside the gate.

**The key deserves a note, because it sits against a decision.** The design's own rule is point-of-use captions and no legend, inherited from the print charrette, and the component still carries none. A key on the *exhibit page* is not a reversal of that: the component is read by someone holding a credential, while this page is read by someone auditing a mechanism, and they need different things. But the distinction is worth stating rather than assuming, because there is a version of this where the key is evidence against the design — if a reader who knows the domain cannot tell what the marks mean, the vocabulary is failing, and no amount of apparatus fixes that. Which of the two it is, is exactly the small-n probe's question, and this file now renders `?h6h2=words` beside the glyphs so the probe has something to compare.

## 11 · The type floor, and the co-presence property that does not survive it

Daniel Hardman opened the rebuilt file and said the type is far too small to ever work — his estimate was about 6 pt. The base size in every floor form in this repository is **8 CSS px**, with 6.5 px item tags and 6 px state words. So the estimate is right.

**The derivation ran backwards, and it ran backwards from the wrong object.** The 76×44 floor was chosen and the type was shrunk until it fit. What it was shrunk to fit is a **placeholder the specification forbids** — see §13, which should be read before any number in this section is used. The measurements below are retained because the *shape* of the trade is right and the method is sound, but every absolute figure here is against the placeholder and is superseded.

Measured, the chip's obligatory content as the mocks draw it — a ten-character SAID teaser, a separate item tag, one port label with its direction glyph — needs:

| type base | pill | port | chip must be | fits 76×44 |
|---|---|---|---|---|
| 8 px | 65.0 | 48.0 | 73 × 44 | yes, with 3 px to spare |
| 9 px | 71.6 | 53.8 | 80 × 47 | no |
| 10 px | 78.2 | 59.5 | 86 × 53 | no |
| 12 px | 91.5 | 70.9 | 100 × 59 | no |
| 14 px | 104.7 | 82.4 | 113 × 68 | no |

**The 76×44 floor holds its own content at exactly one type size, and it is the smallest one anybody tried.** One pixel larger and it does not fit. That is the signature of a form that was fixed first and had its contents fitted to it.

**A contradiction already in the repository, now resolved.** [../stress-board/README.md](../stress-board/README.md) asserts "There is a legible floor form: 76×44 px … an 8 px ten-character SAID pill, a 6.5 px item tag". [../shape-gallery/README.md](../shape-gallery/README.md) says the opposite, and says it carefully: the coordinates "are **design choices embodied in the mocks**, not measured legibility floors … The claim that 76×44 is *where legibility gives out* is perceptual and requires a human to look; nobody has." A human has now looked. The word "legible" in the stress board's sentence is not supported and should come out.

**What a legible floor costs.** The component now carries a type scale (`?type=8|10|12|14`); each step states a base size and the chip and mid dimensions *measured as necessary to carry the same content at it*, so the form follows the type rather than the reverse. Rendered:

| type | viewport | across | rows | board column | whole component | fits a 320×568 screen |
|---|---|---|---|---|---|---|
| 8 px | 320 | 3 | 5 | 380 | 452 | yes |
| 10 px | 320 | 3 | 5 | 451 | 523 | yes |
| 12 px | 320 | 2 | 7 | 665 | 740 | **no — 1.30 screens** |
| 14 px | 320 | 2 | 7 | 765 | 870 | **no — 1.53 screens** |
| 12 px | 360 | 3 | 5 | 496 | 571 | **no, by 3 px** |

**This is the finding, and it is not about this file.** Arm B's central claim is that all thirteen objects stay co-present at rest — the property the arms README's question 4 rests on ("at this load every arm keeps everything co-present … so the stress board's fatal finding does not recur in any arm"), and one of the two things that retired layering under DD-4. **Co-presence holds at 8 and 10 px type and fails at 12.** At a legible size the stress board's fatal finding — budgeted markers scrolled off-viewport with no surviving trace — comes back, for arm B as much as for the others.

So the co-presence argument does not discriminate between the arms at a legible type size, because it fails for all of them. DD-4 was decided partly on a property that may not exist. That is a second, independent reason the DD-4 re-argument is blocked (the first is the packing rule, §6).

**Superseded in magnitude by §13.** The identifier pill is the widest obligatory element in the chip, so it sets the floor's width — and the pill the mocks draw is not the pill arcviz is specified to use. The correct one is *narrower* at every type size, by 7 px at an 8 px host rising to 20 px at 16 px, and it removes a stacked line as well. Re-measured against it, a 12 px host gives a chip about 86 px wide rather than 100 px, which is 3 chips across a 320 px viewport rather than 2. **Most of what legible type appeared to cost was the placeholder's fault, not legibility's.** The table above therefore states the trade too pessimistically, and the co-presence claim below needs re-testing before it is relied on in either direction.

**What this does not establish.** Which size is the floor. 8, 10, 12 and 14 are steps for looking at, not a finding; nothing here measures comprehension or legibility, and one expert's reaction at one viewing distance on one display is an observation, not a probe. What it does establish is the *shape* of the trade — every step up in type buys readability and spends co-presence — and that the trade was previously invisible because the type size was not a variable. `responsive-sweep/type8-320.png` and `type12-320.png` are the same load at the two ends of it.

It also gives DD-4's reversal condition its first evidence. DD-4 reverses if "the compact floor proves illegible at 320 px". Nobody had looked; the first person to look said it was illegible. That is not sufficient to fire the condition — it is one person — but it is no longer true that there is nothing.

## 12 · Overwhelm as a security failure, and where that question already lives

Daniel's second reaction: the amount of detail is overwhelming, an expert in the domain finds it overwhelming, and overwhelming a reader so that they cannot tell what to attend to — or so that every render shows frustrating gaps until they stop attending at all — is itself a security failure, not merely a usability one.

**This is [Q-8Y3M], already open, and it is his own ruling being revisited in the presence of the rendered consequence.** The charrette synthesis ([../charrette/synthesis.md](../charrette/synthesis.md)) states it almost exactly: "The composite as specified is tuned to the verifier and the adversary: identity pills outrank human-legible names, cards read as instrument panels, and a first-time holder looking for 'what does my credential say' reads past apparatus erected against an adversary they have never met." It names the two options — a single register everywhere, or a holder-facing register that "promotes `a`-section content and **demotes — never removes** — the apparatus" — records that "nothing in the research fixes where the dial belongs", and says it "should be decided before that phase starts." The stress board's own README already reported the board is "tuned to the far end of the [Q-8Y3M] dial by inheritance, and it quantifies what that costs but cannot adjudicate the dial."

And [PLAN.md](../../research/PLAN.md) records the ruling that put it there: "**Scaffolding: full apparatus always.** Daniel Hardman's ruling. Every render carries the same structural honesty machinery regardless of audience — one code path, consistent, never under-warns, **at the cost of legibility on the common case.**" The cost was accepted in advance, in writing. What is new is seeing what it actually looks like.

**Three things from the corpus that should discipline the response.** These come from [../../research/prior-art/literature.md](../../research/prior-art/literature.md), which is an audit with the relied-upon sentences quoted in it; I have read the audit and not the underlying papers, and anything load-bearing should be checked against them before it is built on.

- The audit's own constraint on this exact pattern, under `[nngroup_progressive_disclosure]`: progressive disclosure "is a legitimate pattern for *complexity* (advanced/rarely-used features), but it must not be reached for as the solution to *disclosure-state honesty*. Deferring 'this field is redacted' to a secondary screen the user must actively navigate to would misuse the pattern — that information is not an advanced feature to hide, it is system status." So the answer cannot be a toggle that hides state.
- `[schechter2007emperor]`: passive indicators whose *absence* produces no interruption are simply not noticed — 92% of participants entered passwords with the indicator removed. Demoting a marker toward passivity has a measured failure mode.
- `[felt2015sslwarnings]`: a professional team applying warning best practice "ultimately failed at our goal of a well-understood warning", but did move adherence substantially through *opinionated design* — visual cues promoting a recommended action. The lever that works is prominence ordering, not explanation and not concealment.

**Which suggests the distinction the design needs.** Full apparatus is a claim about *presence*, not about *equal prominence*. A render in which every fact is equally loud does not over-warn; it under-warns, because nothing in it is distinguishable — which is the failure Daniel's own ruling was written to prevent. So "demote, never remove" is not a weakening of the full-apparatus ruling but a condition on satisfying it, and the thing to design is an attention ordering over material that all stays present.

**And the two reactions are one defect.** Everything is rendered at the floor size, so there is no hierarchy anywhere — nothing can be demoted, because everything is already at the bottom. The project spent its entire prominence budget on fitting thirteen objects onto a phone before any single state needed to be prominent. That is why §11's type finding and this section are the same problem seen twice: a legible type floor is what creates the headroom that an attention ordering would spend.

**Not designed here, deliberately.** The charrette says [Q-8Y3M] is Daniel's to decide before the wireframe phase, and it shapes every subsequent artifact. Proposing a register split as though it were settled would be exactly the move this repository's own disciplines warn against.

## 13 · The identifier pill: the specification is right and every artifact violates it

Daniel Hardman: entviz already has a pill, its design encodes deliberate security/usability tradeoffs, and the pill drawn here ignores it.

**arcviz's research layer already says the right thing.** [principles.md](../../research/principles.md):71 — "Every SAID and AID renders as an **entviz pill**, so an honest substitution disturbs a picture rather than hiding in a string nobody reads — but the pill's job is cheap rejection and recognition only." It already cites entviz's `trust.ts` for *rule-out, never rule-in*, and [threat-model.md](../../research/threat-model.md)'s substitution adversary already bounds the habituated glance at low-to-mid teens of bits. **Nothing in the research is wrong.** What went wrong is that every mock substituted a placeholder — a rounded rectangle containing `EGDKB8m5pt…` — and then the whole geometry was derived from the placeholder's dimensions.

**The placeholder is the one thing the pill design names as prohibited.** `entviz-js/packages/react/docs/pill-design.md` §3.3: "**No SHORT truncated value chars inline** (`014d…b5e2`): an ~8-char head+tail teaser is both glanceable *and* grindable (a ~48-bit prefix collision is feasible), so it **trains the prefix/suffix heuristic vanity-grinding defeats** (threat-model T1/T6; paper §5.1)." The harm is not only the leaked bits. It is that a reader shown thirteen prefixes per render, every render, learns to identify credentials by prefix — and that learned heuristic is precisely what an adversary who grinds a colliding prefix exploits. A component built to defend against an issuer-controlled adversary is training the habit that defeats it. Note the boundary the same clause draws: a **full-value hover preview is fine** and is not grindable (§14 of that doc); the prohibition is on the short inline teaser.

**What the pill actually is** (§3.1). Leading cap, empty in the wild posture. A label slot. A trailing role icon — `key · signature · digest · address · identifier · raw` — carrying the *type*, never the value, zero value-identity bits. A copy kebab on hover/focus. The value on hover, and on expand.

**The label slot is the part I read wrongly first.** It is not "the slot that is notably not a value prefix". It is the **human-meaningful name** slot: explicit host text wins; failing that, and only under a corpus posture, a mnemonic; and the type text ("cesr key") is a *fallback so the pill is never empty*, not the design. **arcviz already has exactly the right content for it** — the opaque host load label, `ITEM 03`, which it currently renders as a separate 6.5 px tag beside a teaser that should not exist. Putting the label where it belongs removes a stacked line and the teaser at once.

**The posture gate, as actually designed** (§13, `this.i ujdwjtex`, `core/src/trust.ts`).

- The gate is a **`TrustAssumption` object**, host-declared and immutable, passed per pill. Provenance is **per-value, not per-viewport**: one assumption for a same-origin set, referenced from each of its pills; foreign entropy gets a different assumption or none. It is deliberately greppable — a reviewer can find every pill referencing a trusting assumption and ask whether that origin is really trusted. `resolveChannels(trust)` is the pure gate: outside `posture:"corpus"` **every** value-derived channel is off regardless of flags.
- Three channels, all corpus-only and each opt-in: the **auto-mnemonic**, built *only from cells the entviz itself displays* so it can never show a character the visualization does not — the honest `…` marks omitted cells that are all present on expand; the **auto-color tint**, 16 hues as a soft pre-filter, never a partition; and the **colorbar icon** in the leading cap.
- **Rule-out, never rule-in** (`uibwfl47`) is what makes them safe: a deterministic low-entropy function of the value is a *difference detector*. Two different displays prove different values; two matching displays prove nothing. Low entropy is therefore a feature, because the rule-in is never sold.
- **The posture is never an end-user affordance.** "Trust is asserted by the party that *knows* the provenance (the host, in code), not by the reader deciding whether to trust." The pill exposes no control over its own posture, because a "mark as trusted" button would be a one-click false-reassurance vector. The only runtime elevation is **earned promotion** — wild → trusting by the user *completing a successful formal comparison* — reserved for v2.

**arcviz is a wild-posture consumer, and its own gate says so.** The corpus posture was introduced for cesrview, a KEL viewer over *the user's own machine's* microledger. arcviz renders a presentation whose gate header states `P — PRESENTER: UNKNOWN · no evidence binds the presenting party to any holder AID below`. That is the definition of the adversarial case. Every value-derived channel is therefore off, and the mnemonic is doubly unavailable: it may only show cells the entviz displays, and arcviz currently displays no entviz at all.

**One thing that survives, with its reasoning sharpened.** The `×N` recurrence marks are a *machine* comparison of full values, not a human glance judgment, so they are verification rather than recognition and rule-out-never-rule-in does not forbid them. What made them hazardous is the teaser beside them, which invites a reader to believe they could have reached the same judgment by eye.

**Consequence for the floor, and for §11.** The pill is the widest obligatory element in the chip, so **the 76×44 floor was sized around an object the specification forbids.** Measured against a faithful wild pill — label slot, role icon, no value characters, no separate tag line — the chip is narrower at every type size:

| host type | placeholder (teaser + tag) | entviz wild pill | chip as built | chip per spec |
|---|---|---|---|---|
| 8 px | 65.0 | 58.1 | 73 | 66 |
| 12 px | 91.5 | 78.2 | 100 | 86 |
| 16 px | 118.0 | 98.2 | 126 | 106 |

So the correct component is *cheaper* than the placeholder, and the gap widens as type grows — which is the opposite of what §11's table implies. At a 12 px host the chip is about 86 px, giving three across a 320 px viewport rather than two.

**These numbers are a stand-in measurement and should not be built on.** They model the pill from its design document; they are not the component. Given that the last two rounds of work were built on unexamined stand-ins, the next step is to embed `@entviz/react` and measure the real thing, not to refine the model.

**Open.** Whether the mocks should embed the real component or continue to draw a faithful static stand-in of it; and whether the type scale should follow entviz's convention — `text-scale.ts` makes text the *inherited host running size* with named steps at 1, 0.85 and 0.72 em, and explicitly forbids "ad-hoc per-element magic numbers", which is exactly what arcviz's 8 / 6.5 / 6 px are. If arcviz embeds the pill, the pill inherits arcviz's font size, so arcviz's floor form has to be big enough to hold a pill at a legible host size. On that reading the type floor is not arcviz's to choose independently at all.

## 14 · Open, and needing a ruling

0. **The identifier pill (§13).** Embed `@entviz/react` in the mocks, or draw a faithful static stand-in of the wild pill? And does arcviz adopt entviz's type convention — inherited host running size, steps at 1 / 0.85 / 0.72 em — which would mean the floor form is sized by the pill rather than the reverse?
0. **[Q-8Y3M], the scaffolding dial (§12).** Already yours to decide, per the charrette; the full-apparatus ruling is the current answer and this is the first look at what it costs.
0. **The component's maximum width, and what to do with surplus width at all.** It is capped at 480 px so the graph stays a vertical stack, which is the conservative reading of DD-7; the alternatives are pinning it to 360 px so every artifact stays directly comparable, or spending desktop width on a genuinely different layout, which DD-7's own text calls a second layout rather than a reversal. `?maxw=` renders any of them. Nothing above the cap has been designed.
1. **Which packing rule — global or band?** Global treats rows as pure viewport economy, which is what the caption inside the render says, and spends extra width; band preserves the authored bands so that a row means something, and ignores width above 360. It decides DD-4's height comparison (§6), and it decides whether a reader who infers meaning from rows is reading correctly or being misled.
2. **DD-1 under wrap-packing.** Accept that a drawn edge may ascend, constrain packing so none does, or narrow DD-1 to govern rank rather than drawn direction.
3. **The near-node nub** (F2) — a coinage with one exhibit.
4. **The marked shed `⋯N edges`** (F3) — an inference, and a decision about whether marking a shed is better than showing one of several labels.
5. **The H2 porous-bottom glyph and its reserved H3 partner** (§7) — new design, no precedent in any audited product, and the H2 scope widening at the chip floor is declared rather than resolved.
