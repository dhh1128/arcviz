# Historic England — "Understanding Historic Buildings: A Guide to Good Recording Practice" (2016), Ch.7 Architectural Drawing Conventions

**Title**: Understanding Historic Buildings: A Guide to Good Recording Practice (HEAG099 / formerly NR83)
**Body**: Historic England (the UK national statutory heritage body; this guide replaced the earlier RCHME — Royal Commission on the Historical Monuments of England — recording guidelines)
**Published**: May 2016
**URL (mirror used)**: https://gat04-live-1517c8a4486c41609369c68f30c8-aa81074.divio-media.org/filer_public/1c/94/1c942b62-d945-4bde-b00a-fc0a273d168a/nr83_understanding_historic_buildings-_a_guide_to_good_recording_practice.pdf
**Canonical page**: https://historicengland.org.uk/images-books/publications/understanding-historic-buildings/
**Retrieved**: 2026-09-14
**Status**: PRIMARY — full page images/text read directly (pages 30-41) via the Read tool's PDF parser, after WebFetch's own summarizer failed on the binary stream (same failure mode as the Venice Charter and IFA paper fetches — WebFetch's small summarizer model cannot handle these PDFs' encoding; the Read tool's native PDF support works).

This is a **nationally codified standard from a statutory UK heritage body**, not a blog paraphrase — the strongest single find of this research pass for a documented, multi-grade certainty vocabulary, and it directly names the analogue to arcviz's "known to exist but unseen" case.

## Table 2: CAD layer conventions (p.36) — verbatim rows relevant to certainty

| Layer name | Description | Line Type | Line weight |
|---|---|---|---|
| 0A-Wall-Ground | Ground line at battered walls | continuous | 0.13 |
| 0A-Reconstruct | **Reconstruction or conjectural** | **dashed** | 0.13 |
| 0A-Hidden | Info masked by other details | dashed | 0.13 |

## Section 7.3 "Drawing conventions" — General (p.37), verbatim line-type key

> - Detail on cutting plane — *(solid line)*
> - Detail beyond or below cutting plane — *(solid line, same weight)*
> - **Former and conjectural line of building** — *(dashed line)*
> - Detail behind or above cutting plane — *(dashed line, different dash pattern)*
> - Centre line — *(dash-dot)*

## Section 7.3 "Plans → Walls" (p.37), verbatim four-way wall key

> - Walls — *(solid single line pair)*
> - **Former walls** — *(dashed line pair)*
> - Wall with plinth — *(solid, wider)*
> - **Wall of unknown thickness** — *(dashed outline where the plinth/thickness would be)*

"Wall of unknown thickness" is the closest documented analogue found anywhere in this research to arcviz's "node known to exist, contents withheld" case: the wall's EXISTENCE and rough position are asserted (drawn), but a specific attribute of it (thickness/extent) is explicitly marked unknown via a distinct dashed rendering, rather than either omitting the wall or drawing it as if fully known.

## Section 7.4 "Sample drawings" (p.40-41) — worked legend, THREE-way certainty distinction

The Waterloo House worked example (p.41) gives an explicit legend with three classes of evidential status for the same class of object (structural timber):

> - **■ Original timber in situ** (solid black square symbol)
> - **⊠ Timber deduced from peg evidence** (hatched/crossed square symbol)
> - **▭ Inserted timber** (open/outline square symbol)

This is a genuine three-way, pairwise-distinguishable symbol set for the same feature type, keyed to evidential basis rather than just presence/absence: (1) directly observed and present, (2) NOT present/not observed but its former existence is inferred from surviving INDIRECT evidence (a peg hole — a trace left by the thing, not the thing itself), and (3) present but of a different evidentiary class (known modern addition, not original). Class (2) — "deduced from peg evidence" — is a documented analogue for arcviz's "committed to but unseen" case: something is asserted to have existed at a specific place, on the strength of a trace/commitment elsewhere, without the object itself ever being observed.

## Annotation convention: "Site of X" — feature known to have existed, now entirely gone

The same sample drawing (p.40-41) labels several features textually rather than by line-type alone, all following the pattern **"Site of ______"**:

> - "Site of doorway"
> - "Site of window" (×2, at positions A-A1/D-D1 on the first-floor plan)
> - "Site of stair"
> - "groove of former partition" (×2 — the physical trace, a cut groove in a surviving timber, that is the EVIDENCE for the vanished partition)
> - "Former line of wall" (in cross-section B-B1, marked where a wall used to stand, now gone, inferred from the surviving roof/floor joints around the gap)

This is the clearest available analogue to "known to exist (or to have existed), but nothing of it survives to see" — the position is drawn (usually dashed), the label makes the evidential status explicit in words, and the drawing does NOT omit the feature just because nothing of it currently exists to look at. It differs from arcviz's case in one respect worth flagging: here the "unseen" thing is known through PHYSICAL trace evidence at the SAME location (a groove, a joint) rather than a separate commitment/reference naming it from elsewhere — arcviz's "missing referent" and "blinded edge" cases both involve the assertion coming from a different node than the missing one. Historic England's convention doesn't need to solve that separation because in a building, the trace and the vanished feature are always co-located.

## Assessment against arcviz's three states

- **State 1 (node known to exist, contents withheld)**: closest analogue = "Wall of unknown thickness" / "Timber deduced from peg evidence" — asserted to exist, rendered distinctly (dashed / hatched), specific content (thickness, or the timber itself) explicitly not shown.
- **State 2 (missing referent)**: **no direct analogue found** in this document. Building recording doesn't have an equivalent to "another record points here and we don't have what it points to" — every feature in a single building survey is either present, formerly-present-with-trace, or absent-without-comment. This gap is worth noting explicitly to the downstream document: it may be genuinely novel to arcviz's cross-document/cross-node referencing structure, which a single-building recording convention has no reason to need.
- **State 3 (blinded edge — topology known, destination unknown)**: **no direct analogue found.** Building conventions distinguish evidential grades of a THING, not of a RELATIONSHIP's endpoint. This is arguably the sharpest gap between arcviz's problem and the architectural/archaeological precedent: these conventions were built for single physical objects with one location, not for a graph of referential edges where the edge itself can be known while its target is not.

**Inference (ours):** states 2 and 3 do not have precedent in this body of convention because building/site recording has no structural equivalent to a directed edge whose destination is unresolved — every "unknown" in these drawings is an unknown ATTRIBUTE of a located thing, never an unknown REFERENT of a pointer. This is likely the actual reason no prior art exists for arcviz's full three-state problem: the graph-of-commitments structure (edges as first-class objects with their own uncertain resolution) has no counterpart in a discipline where the "graph" is just "this wall touches that wall."
