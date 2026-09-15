# Rough shape gallery

Placeholders so the layout candidates can be looked at rather than read about. Open [gallery.html](gallery.html), or view [gallery.png](gallery.png).

Seven DAG shapes at 360 px under one treatment — compression to a floor, with cards carrying a budgeted state floored larger. Identifier prefixes are real values from `corpus/`. Everything else is deliberately unfinished: no type hierarchy, no spacing refinement, no state vocabulary beyond what each shape needs to read as a shape.

[arm-b-at-360px.png](arm-b-at-360px.png) is the top of the compression arm from [../layout-comparison/](../layout-comparison/), rendered in Chrome at 360 px, for comparison against these placeholders.

## What the coordinates are, and are not

`76×44` and `150×72` appear throughout as though they were findings. They are **design choices embodied in the mocks**, not measured legibility floors. Every derived figure — area per object, the ratios between arms — is arithmetic on those choices. The claim that 76×44 is *where legibility gives out* is perceptual and requires a human to look; nobody has, and the small-n probe the principles call for has not been run.

What has been measured, in Chrome at 360 px, is total rendered content height per arm: layering 5,304 px, degree-of-interest 4,214 px, compression 2,347 px. That corroborates the *ordering* the recommendation rests on, and nothing finer.

## What the pictures show that the prose did not

A 76×44 chip holds an identifier prefix and one short word. Seeing it makes the stress board's finding — that the floor holds states but not parameters — concrete in a way the sentence does not: there is visibly nowhere to put a policy window, a horizon, or a cardinality bound.

The second floor at 150×72 is not a marginal upgrade over the chip. It is the difference between a token and a card that can say something. Panel 7 puts them side by side.

## Two things the gallery got wrong on the first pass

**Edges were drawn unlabelled.** ACDC edges carry a label — it is the map key in the `e` section — and the label is where the meaning lives. Real examples from `corpus/`: `auth`, `le`, `qvi`, `waypoint`, `sourceA`/`sourceB`, and an edge group whose members are `unanimous`, `anyOne`, `average`, `weightedAverage`. Two edges leaving one node can mean entirely different things, so an unlabelled arrow says "related somehow" where the credential said something specific. Panels 2–6 now carry labels alongside the derived operator.

A consequence worth carrying into the design: **an edge label is issuer-chosen text**, so it is untrusted content under P11. It must render inside the issuer-controlled boundary rather than as viewer chrome, or an issuer can label an edge "verified by GLEIF" and have it read as the component's own words.

**Orientation was picked without noticing there is a convention.** Panel 8 draws the same chain both ways. The ecosystem's own diagrams — the ASCII in keripy's guardianship worked examples — put the **presented node at the bottom with references ascending**, and carry the edge label on the arrow beside the operator. The first pass of this gallery did the opposite.

This is logged as an open question rather than a recommendation, because the obvious justification for the ecosystem convention is wrong. "Authority flows downward" is false for `NI2I`, which explicitly means *not* issuer-to-issuee, and for `E1E`, which relates two issuees and transfers no authority at all. If presented-at-bottom is adopted it should be defended as *start from what you were handed and look at what it points to* — a reading-order argument that holds for every edge type — rather than as an authority gradient that holds for one.
