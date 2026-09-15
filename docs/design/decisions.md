# Design decisions

The constraint record for the design phase. Research-phase rulings live in [../research/PLAN.md](../research/PLAN.md)'s dated decision sections; everything that constrains *how arcviz draws* lives here.

Each entry carries its status, the decision, why it beat the alternatives, what it now forbids, and **what would reverse it**. That last field is the point: a decision whose reversal condition cannot be stated was not a decision, it was a preference.

**Status vocabulary.** **Ratified** — Daniel Hardman has agreed it. **Proposed** — derived from evidence and awaiting his ruling; may be built against provisionally, and is marked as provisional wherever it is relied upon. **Open** — genuinely undecided, recorded so it is not settled by accident.

---

## DD-1 — Graph orientation: presented node at top, references descend · **Ratified 2026-09-15**

The node the viewer was handed sits at the top. Edges point downward, from a node to whatever its `e` section references. Rank is by longest path, so a node reachable at two different depths sits at its deepest.

**Why.** An ACDC chain is a *dependency* graph, not a hierarchy, and the domains split cleanly on that distinction: org charts, family trees and filesystems put the root on top because they encode descent or authority, while `git log --graph`, `npm ls` and stack traces put the subject on top because they encode "this thing and what it rests on." Structurally we are the second kind, and git is the closest match anyone has — a DAG of nodes referencing ancestors, diamonds included.

The stronger argument is about where absence accumulates. The presented node is the only guaranteed-present node in any render; the ancestry is where material goes missing — the production chain's delegation root is simply not there, and the whole H7 case exists because referents vanish. Both print and scroll privilege the top, so whatever sits there is what most viewers actually see. Putting the reliably-present thing at the top and letting increasingly uncertain ancestry trail downward into holes is better than putting a hole above the fold and the credential below it.

**What it forbids.** Defending the *opposite* orientation as an authority gradient. "Authority flows downward" is true for `I2I` and false for `NI2I` — which explicitly means not-issuer-to-issuee — and for `E1E`, which relates two issuees and transfers no authority at all. Any orientation argument must hold for every operator in the table, not for the one that happens to describe vLEI.

It also forbids the inconsistency the first gallery contained: holes at the bottom of a descending chain while the blinded-edge frontier sat at the top. **The unknown accumulates at the far end of a reference**, so holes and frontier belong at the same end, which under DD-1 is downward.

**Departure from existing practice, noted.** keripy's guardianship worked examples draw the presented node at the *bottom* with references ascending. That is the ecosystem's only extant convention and DD-1 contradicts it. The divergence is accepted because that ASCII addresses developers reading test docstrings rather than users reading a component, and because its implicit authority reading does not survive the operator table.

**Reversed if.** The primary viewer turns out to be a verifier auditing provenance rather than someone examining a presented credential — burying the root is hostile to that use. Or if ecosystem consistency is judged to outweigh the reasoning, which is a legitimate call.

---

## DD-2 — Minimum viewport: 320 CSS pixels · **Ratified 2026-09-15**

Every layout must present without loss of information or functionality, and without two-dimensional scrolling, at 320 CSS pixels of width.

**Why.** WCAG 2.1 Success Criterion 1.4.10 Reflow, Level AA: "Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions for: Vertical scrolling content at a width equivalent to 320 CSS pixels." The figure is not a device measurement — the same document states that "320 CSS pixels generally corresponds to a desktop browser window set to a width of 1280px and the browser viewport then zoomed to 400%." The binding case is a low-vision user at 400% zoom, and devices are the easier constraint: 375 for the smallest current iPhone, 360 for the common Android baseline, both covered.

This also aligns with P10, which holds that accessibility and adversarial robustness are one design move rather than competing ones.

**What it forbids.** Invoking the criterion's exception for "parts of the content which require two-dimensional layout for usage or meaning" to excuse the graph view. The exception exists for maps and data tables; our layout is a vertical stack with connectors rather than an irreducibly two-dimensional artifact, and a component claiming AA while carving out its primary view would be making exactly the kind of quiet overclaim this project exists to refuse.

**Consequence for work already done.** Every artifact built so far — the stress board, the three-arm comparison, the shape gallery — was built at **360 px, 11% wider than the obligation**. None has been tested at 320. The compact-chip floor, the second floor, and the sliver run-room are all unverified at the width that actually binds.

**Reversed if.** A later WCAG revision moves the figure, or the component's conformance target is deliberately set below AA — which would need saying out loud.

---

## DD-3 — Edge labels are rendered, inside the issuer boundary · **Ratified 2026-09-15**

Every drawn edge carries its label. The label is the map key in the ACDC's `e` section — real examples from the corpus are `auth`, `le`, `qvi`, `waypoint`, `sourceA`/`sourceB`, and an edge group of `unanimous`, `anyOne`, `average`, `weightedAverage`.

**Why.** The label is where an edge's meaning lives. Two edges leaving one node can mean entirely different things, and the diamond's two paths to a shared ancestor differ not merely in length but in claim. An unlabelled arrow says "related somehow" where the credential said something specific.

**What it forbids.** Rendering a label as viewer chrome. An edge label is **issuer-chosen text**, so it is untrusted content under P11 and must sit inside the issuer-controlled boundary — otherwise an issuer labels an edge `verified-by-GLEIF` and the component appears to be saying it. The same restriction makes the field-label rules from the spec's `v1.1` branch load-bearing: a label may not contain `-`, and a bare `_` is a reserved virtual DAG-hop label that must never render as data.

**Reversed if.** Nothing foreseeable; the label is part of the artifact's meaning.

---

## DD-4 — The pile is refuted; focus is in place · **Proposed**

Cards are not stacked with occlusion. Focus is achieved by expanding a card where it sits, with everything else reflowed to a compact floor.

**Why.** Two independent arguments. Structurally, a pile is defined by occlusion, and in any diamond two nodes each carry an edge to the shared ancestor — so raising that ancestor forces either un-occluding both, which is a spread rather than a pile, or attaching edges to hidden geometry, which erases the path-length distinction. And by measurement, layering costs 1.55× the area per object for one line of content against three, renders taller than compression at both rest and focus, and linearizes the diamond.

**Standing caveat.** Daniel's layering proposal was *not* refuted by the structural argument — a visible sliver is a visible attachment point, which is what that argument assumed was unavailable. It lost on measurement instead. The distinction matters if the measurements are revisited.

**Reversed if.** The compact floor proves illegible at 320 px (DD-2), which would remove focus-in-place's replacement for the pile and reopen the question.

---

## DD-5 — Compression to a floor, with a second floor for budgeted states · **Proposed**

Non-focused cards reflow to a compact floor. Cards carrying one of the four budgeted prominence states — stale, presenter-unknown, metadata-decoy, guessable-but-looks-private — floor at a larger size instead.

**Why.** The stress board found a floor that holds *states* but not *parameters*: at the compact size, a policy window, a horizon, or a cardinality bound has nowhere to go. A second floor repairs exactly that wound, and needs no distance term.

**Explicitly not measured.** The figures circulating for these floors — 76×44 and 150×72 — are **design choices embodied in the mocks, not measured legibility findings**, and every derived area and ratio is arithmetic on them. The claim that any particular size is where legibility gives out is perceptual, requires a human to look, and no such probe has been run. See [shape-gallery/README.md](shape-gallery/README.md).

**Reversed if.** A small-n legibility probe at 320 px finds a different floor, or finds that no floor carries enough to be worth the mechanism.

---

## DD-6 — Verification renders per card, not as a central ledger · **Proposed**

**Why.** Measured on the stress board: centralizing saves 29% of column height and pays for it by exiling every blocking identifier into three-hop footnotes and destroying co-visibility between a check and the card it concerns. Compact cards never carry a ledger anyway, so the per-card cost is paid only at expanded scale. The central matrix earns a different job — print flattening, and an optional summary at the enclosure.

**Reversed if.** The 320 px retest changes the height economics enough to make the saving decisive.

---

---

## DD-7 — The primary axis is vertical · **Ratified 2026-09-15**

The graph lays out vertically. Fan-out wraps rather than extending horizontally.

**Why.** Daniel Hardman's ruling: it is the only axis that works on a phone. DD-2 makes that concrete — at 320 CSS pixels there is no horizontal budget to spend, so a horizontal primary axis would require two-dimensional scrolling, which SC 1.4.10 forbids outright.

**What it costs, recorded rather than glossed.** A wide fan-out becomes a long vertical run, so the widest graphs render as the tallest ones — the inverse of what their shape suggests. The corpus does not tell us how often that bites: production supplied depth without branching, keripy branching without depth.

**Reversed if.** Nothing foreseeable at 320 px. A desktop-only or landscape-tablet variant could differ, but it would be a second layout rather than a reversal.

---

## DD-8 — Intra-card disclosure: collapse follows the artifact, and never resembles non-disclosure · **Proposed**

A card needs to collapse and expand its own contents, because credentials carry more fields than a viewport holds, and a focused card may need internal scrolling. Four constraints govern it.

**Collapsed is a distinct state from undisclosed, and must look it.** This is the sharpest point and the one most likely to be lost. The matrix exists to stop one kind of absence passing for another; UI collapse introduces a new kind — *present, disclosed, hidden by the viewer's own interface* — which is reversible by the viewer alone, where undisclosed is not reversible at all. A collapsed section that resembles a compact one would be a twelfth indistinguishable pair, created by us rather than inherited from the format. **Inference, flagged:** no source states this; it follows from applying the matrix's own commitment to a state the matrix does not contain.

**Collapse follows the artifact's nesting, never a designer's grouping.** The ACDC supplies the tree: top-level sections, sub-blocks within `a`, elements of `A`. Grouping fields for tidiness can place two differently-disclosed things behind one toggle, and the toggle then asserts a relationship the credential never made. Veridian's `CardDetailsExpandAttributes` already does the structural version, recursing on object-valued attributes with a depth counter and opening the first level.

**The prominence budget propagates upward through collapse.** A collapsed header carries the budgeted states of everything beneath it. This is the stress board's off-viewport finding at a different scale: if a stale marker or a guessable-but-looks-private field sits inside a collapsed section, collapsing hides exactly what must not be hidden.

**Internal scroll is bounded.** Nested scroll regions capture the outer scroll on touch devices, so at most the focused card scrolls internally. And a card with internal scroll cannot print: under Rule 15 print expands everything, which means the rules section — 300 to 500 characters against data fields of 12 to 44 — renders in full on paper regardless of its screen treatment.

**Reversed if.** A legibility probe shows that carrying propagated state on collapsed headers costs more than it saves, or that the artifact's own nesting produces a tree too deep to navigate at 320 px.

**Unresolved.** The shape catalog's SC7 covers card-internal *disclosure states* and not card-internal *volume*; a case for "a card with more content than the viewport" does not exist and should be added.

## Open

- **Who the primary viewer is.** Holder examining their own credential, or verifier auditing provenance. It swings DD-1 and the scaffolding question, and nothing in the research settles it.
- **The holder-facing presenter indicator.** The full-apparatus ruling and AF17's "no presenter indicator at all, positive or negative" collide on exactly one axis; see PLAN.md's 2026-09-14 entry.
