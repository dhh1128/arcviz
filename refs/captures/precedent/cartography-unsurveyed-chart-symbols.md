# Unsurveyed-area and depth-reliability chart symbology — capture

Retrieved: 2026-09-14. Status: PRIMARY (U.S. Chart No. 1 PDF fetched and extracted with
pdftotext; NGA's own MSI copy returned an HTTP 503 at fetch time, noted as a lead below).

## Source records

- **key**: uschartno1
  **title**: "U.S. Chart No. 1: Symbols, Abbreviations and Terms" (13th ed.) — a joint NOAA/NGA publication that is the U.S. national implementation of the IHO's international symbol set (INT1, part of IHO publication S-4)
  **body**: NOAA Office of Coast Survey / National Geospatial-Intelligence Agency (NGA)
  **url (mirror actually fetched)**: https://www.cal-sailing.org/images/Cruising%20Skipper%20Resources/ChartNo1.pdf
  **url (canonical, not fetchable at capture time)**: https://nauticalcharts.noaa.gov/publications/us-chart-1.html ; https://msi.nga.mil/api/publications/download?key=16694005%2FSFH00000%2FSec_I.pdf (returned HTTP 503; treat NGA's own hosted copy as a LEAD, not verified at this URL today) ; https://repository.library.noaa.gov/view/noaa/2719/noaa_2719_DS1.pdf (returned "Access Denied" / Akamai edge block at capture time — also a LEAD, not the source actually used)
  **status**: primary for content (the cal-sailing.org mirror is a faithful copy of the official NOAA/NGA U.S. Chart No. 1 publication; content cross-matches the symbol numbering — I13/I14/I25 — reported independently by search-engine summaries of the NGA and Indian INT1 editions), but note the URL actually fetched is a third-party mirror, not NOAA's or NGA's own server, because both official servers refused the direct fetch at capture time.
  **local capture**: /tmp/chartno1.txt (pdftotext -layout extraction of the fetched PDF; not committed — ephemeral working file)

## The three depth/coverage symbols, Section I "Depths"

Quoted directly from the extracted table (Section I, "Depths", entries 13/14/25 in the
No./INT column):

> **13 — "No bottom found at depth shown."** ECDIS remark: "Status of no bottom found is obtained by cursor pick."

This is a **measured negative result**: a sounding line was actually run to a stated depth and nothing was struck — a "we looked, and found no floor at this depth" statement, not an absence of a measurement.

> **14 — "Soundings which are unreliable or taken from a smaller scale source"** — "(NOAA shows unreliable soundings in fathoms and feet with sloping numbers and in meters with vertical numbers)". ECDIS remark: "Sounding of low accuracy."

This is a **measured but low-confidence value**, distinguished from a fully-trusted sounding purely by numeral typography (sloping vs upright digits) — the number itself is not different, only its rendered style is, so the reader is meant to read the same fact ("32 m here") at two different trust levels depending on font slant alone.

> **25 — "Unsurveyed or inadequately surveyed area; area with inadequate depth information."** Rendered/labelled on the chart face (per the extracted legend) as "Unsurveyed", "Inadequately surveyed", "Incompletely surveyed area", "Unsurveyed area" — with a cross-reference "(see ZOC Diagram)" tying the area label back to the CATZOC symbology described in `cartography-catzoc.md`.

This is the **true data-void**: not merely a low-confidence number, but literally no depth information recorded for the region, distinguished from #14 by having no numeral in the area at all rather than an untrustworthy one.

(All three, U.S. Chart No. 1, Section I "Depths", pp. 44-46 of the pagination in the fetched
PDF — page numbers are the document's own printed folio numbers, not PDF page indices.)

## The 3-way distinction this gives cartography, and why it is not quite arcviz's 3 states

Inference (ours): U.S. Chart No. 1 already encodes three pairwise-distinguishable depth
epistemic states in one section:

1. **I 13, "no bottom found"** — surveyed, with a definite (negative) result: depth exceeds
   the sounding line's length at that point. Analogous to arcviz's "we probed and got a
   definite null" — not one of arcviz's three, but worth noting as a 4th possible state
   cartography needed and arcviz might too (a definitively-absent edge is different again
   from a merely-uncollected one).
2. **I 14, "unreliable / low accuracy"** — surveyed, value present, but flagged low-confidence
   via typography alone (not a different color or shape family, just slanted vs upright
   digits). This is the closest analogue to a "confidence-graded but visible" state — CATZOC's
   A1..D ladder is the fuller version of the same idea (see `cartography-catzoc.md`).
3. **I 25, "unsurveyed or inadequately surveyed area"** — no data at all, called out by a
   named, bounded region with an explicit label plus a dashed/hachured boundary treatment
   (per the search-derived secondary descriptions of UK NP5011 and Indian INP5020 practice —
   NOT independently verified against the primary U.S. Chart No. 1 graphic in this capture,
   since pdftotext extracts text/labels, not the rendered line-style raster; flagged as **lead,
   not confirmed**, for the exact dash pattern/color).

None of the three is arcviz's "missing referent" (state #2 — we do have an edge naming a node
we don't hold) or "blinded edge" (state #3 — out-degree known, destination unknown).
Cartography's #25 (unsurveyed area) is closest to arcviz's state #1 (node known to exist,
contents withheld) or state #2 (missing referent) depending on framing — chart readers already
know the coastline continues past an unsurveyed patch (the "far node" — e.g. the shoreline —
is not in doubt), only the interior detail is missing, which is structurally more like arcviz's
state #1 than state #2. Cartography's #13 ("no bottom found") is a shape of knowledge arcviz's
three states don't currently have a slot for: a definite, confirmed negative.

## What could not be verified today (leads, not findings)

- The exact **line-style** (dash pattern, color: black vs magenta) used to bound an I-25
  unsurveyed area on the official U.S. Chart No. 1 graphic — search-engine summaries (not
  independently fetched primary text) describe UK Admiralty NP5011 practice as "surrounded by
  a bold dashed line (usually black, but on some charts magenta)" and "alternating bands of
  white and blue tint," but this capture did not independently confirm that specific line-style
  description against a primary NP5011 or U.S. Chart No. 1 rendering (only the text/label
  extraction above is confirmed primary). Mark as **lead**.
- NGA's own MSI-hosted `Sec_I.pdf` (the presumed authoritative NGA-hosted excerpt of Section I)
  returned HTTP 503 at fetch time; not retried. The content above was corroborated via a
  third-party mirror instead, so treat the *specific PDF pagination/page numbers* as
  mirror-specific, not necessarily NGA's own pagination.
