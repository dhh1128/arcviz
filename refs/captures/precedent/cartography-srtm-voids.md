# SRTM data voids and void-fill provenance flagging — capture

Retrieved: 2026-09-14. Status: primary (USGS EROS page fetched directly; LP DAAC SRTM
Collection User Guide V3 PDF downloaded and extracted with pdftotext).

## Source records

- **key**: usgs-eros-srtm-void
  **title**: "USGS EROS Archive - Digital Elevation - Shuttle Radar Topography Mission (SRTM) Void Filled"
  **body**: U.S. Geological Survey, Earth Resources Observation and Science (EROS) Center
  **url**: https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm-void
  **status**: primary — fetched directly

- **key**: lpdaac-srtm-userguide-v3
  **title**: "The Shuttle Radar Topography Mission (SRTM) Collection User Guide", Revised October 2015 (V3 / "SRTM Plus")
  **body**: NASA Land Processes Distributed Active Archive Center (LP DAAC), USGS EROS
  **url**: https://lpdaac.usgs.gov/documents/179/SRTM_User_Guide_V3.pdf
  **status**: primary — downloaded PDF, extracted with `pdftotext -layout`; local copy /tmp/srtm_guide.pdf / /tmp/srtm_guide.txt (ephemeral, not committed)

## What a "void" is, and why it happens (USGS EROS page, primary quote)

> "The voids occur in areas where the initial processing did not meet quality specifications."

> "the NGA filled the voids using interpolation algorithms in conjunction with other sources of elevation data"

So USGS itself ships (and names) **two distinct products** for the same underlying survey: a
"Non-Void Filled" collection that leaves the gaps as gaps, and a separate "Void Filled"
collection where the gaps have been patched. The void is not hidden by default — a user has to
affirmatively choose the void-filled product to get a value where there wasn't one.

## The provenance mechanism: the "NUM" file (per-pixel source tracking)

This is the strongest, most directly transferable primary finding for the "interpolated vs
measured" flagging question. From the LP DAAC User Guide (§2.1.2, p.5):

> "Scientists produced an ancillary 1-byte (0 to 255) 'NUM' (number) file... for each SRTM NASA Version 3.0 elevation file. The separate NUM file indicates the source of each DEM pixel, as well as the number of ASTER scenes used (up to 100), if ASTER GDEMV2 was the pixel source, and the number of SRTM data takes (up to 24), if SRTM was the pixel source... The NUM files have names corresponding to the elevation files, except with the extension '.NUM' (such as N37W105.NUM). The elevation files use the extension '.HGT', meaning height (such as N37W105.HGT)."

Crucially, the NUM file is not a single "confidence score" — it is a **coded provenance
value naming which dataset produced this specific pixel**, per "Table 2: Fill Values of the
'.NUM' files" (User Guide, p.6):

> "1 = Water-masked SRTM void *
> 2 = Water-masked SRTM non-void *
> 5 = GDEM elevation = 0 in SRTM void (helped correct ocean masking)
> 11 = NGA-interpolated SRTM (were very small voids in SRTMv1)
> 21 = GMTED2010 oversampled from 7.5 arc-second postings
> 25 = SRTM within GDEM **
> 31 = NGA fill of SRTM via GDEM ***
> 51 = USGS NED
> 52 = USGS NED via GDEM
> 53 = Alaska USGS NED via GDEM
> 72 = Canadian Digital Elevation Data (CDED) via GDEM
> 101-200 = ASTER scene count (count limited to 100)
> 201-224 = SRTM swath count (non-voided swaths) Actual maximum = 24"

with footnotes: "* Water-masked in SRTMv2 by [NGA] using its SRTM Water Body Database (SWBD)."
"** GDEM used SRTM 3 arc-second data, oversampled to 1 arc-second postings, as fill at some
locations. Rarely some of these interpolations are at locations of void within the original
1 arc-second SRTM." "*** GDEM used a version of SRTM supplied by NGA that included elevation
measurements from undisclosed sources."

This means: for **every single pixel**, a downstream user can look up (in a companion file,
not baked irreversibly into the displayed value) exactly which of ~13 named provenance classes
produced that number — genuine SRTM radar measurement, vs. ASTER optical stereo fill, vs.
GMTED2010 fill, vs. national DEM fill, vs. an NGA-applied small-void nearest-neighbor
interpolation. "Measured" and "interpolated" are not a binary flag here — they are a **named,
enumerated provenance taxonomy** that also records *which* secondary source was used, an even
finer grain than CATZOC's letter grades.

## The interpolation method itself, for very large voids (Delta Surface Fill)

Method summary, LP DAAC User Guide §2.1.2 (steps 4-6, p.7), given because it demonstrates the
lengths taken to make a *filled* value track the statistical behavior of a *real* one rather
than silently substitute a guess:

> "A modified Delta Surface Fill method was applied to fill SRTM voids with ASTER GDEM2... SRTM elevations were subtracted from ASTER GDEM2 elevations, but retain the SRTM voids... This is the ASTER GDEM2-SRTM delta surface. GDEM2-SRTM delta surface voids were filled mostly via iterative edge-growing interpolation: In each iteration, each void pixel that bordered any non-void pixel was interpolated from the nearest non-void pixels in each of 16 different directions... weighted by the inverse square root of its distance... This edge-growing interpolation was applied in 50 iterations."

And the explicit acknowledgment that even the *fill quality itself* is error-checked and can be
rejected, rather than accepted uncritically (§2.1.2 step 7, p.7):

> "Technicians experimented greatly to determine an optimum threshold to reject some void fills as errors. A threshold of 80 m caught most obvious errors while minimizing the rejection of apparently good elevation values. Using this threshold, voids were reintroduced to the ASTER GDEM2-filled SRTM DEM where the delta surface was equal to or outside +/-80 m."

I.e., a fill can itself fail and get **turned back into an explicit void** (reintroduced),
rather than a bad guess being allowed to stand just because *some* number is better than none.

## Design takeaway (Inference (ours))

Inference (ours): SRTM's NUM-file pattern is the cleanest transferable model for arcviz's
state #1 (contents withheld) and state #3 (blinded edge) simultaneously: keep the **displayed
value and its provenance/confidence tag as separate channels** — the elevation number renders
identically regardless of source, but a companion, explicitly-named provenance code is always
available on demand (not merged into, or inferred from, the primary display). Applied to
arcviz: a node/edge's *rendered* state (exists, unknown contents) should carry a queryable,
enumerated provenance tag — "we hold a raw commitment only," "we hold a commitment plus a
disclosed edge count but not targets," "we hold nothing, this is inferred from a chain we do
have" — exactly the way NUM codes 1/11/21/25/31/51/etc. tell you *which kind* of not-quite-real
this pixel is, rather than one boolean "trust me" bit. The reintroduce-as-void-on-failed-fill
behavior (§2.1.2 step 7) is also a caution: arcviz should be equally willing to fall back to
"unknown" display when a heuristic guess about a blinded edge's likely target is not
well-supported, rather than always rendering *some* placeholder guess.
