# CATZOC / Zone of Confidence — capture

Retrieved: 2026-09-14. Status: PRIMARY (IHO S-68, S-67 texts downloaded and locally
extracted with pdftotext; Teledyne CARIS S-57 attribute page fetched directly).

## Source records

- **key**: iho-s68
  **title**: Guidelines and Recommendations for HOs for the Allocations of CATZOC/QOBD Values from Survey Data (S-68, Edition 1.1.0, March 2025)
  **body**: International Hydrographic Organization (IHO), Data Quality Working Group
  **url**: https://iho.int/uploads/user/pubs/standards/S-68/S-68_Guidelines_for_Allocation_of_CATZOC_Ed_1.1.0.pdf
  **status**: primary — downloaded PDF, extracted with `pdftotext -layout`, local copy at /tmp/s68.pdf (ephemeral, not committed)

- **key**: iho-s67
  **title**: Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts (ENC) (S-67, Edition 1.0.0, October 2020)
  **body**: International Hydrographic Organization (IHO)
  **url**: https://iho.int/uploads/user/Services%20and%20Standards/HSSC/HSSC12/S-67%20Ed%20100%20Mariners%20Guide%20to%20Accuracy%20of%20Depth%20Information%20in%20ENC.pdf
  **status**: primary — downloaded PDF, extracted with `pdftotext -layout`, local copy at /tmp/s67.pdf (ephemeral, not committed)

- **key**: caris-s57-catzoc
  **title**: "Category of zone of confidence in data" (S-57 object catalogue attribute page, attribute code 72)
  **body**: Teledyne CARIS (S-57 object catalogue documentation, mirrors the IHO S-57 Ed 3.1 attribute definitions)
  **url**: https://docs.teledynecaris.com/s-57/S57Cat/S57CatSite/attribut/catzoc.htm
  **status**: secondary (a documentation vendor's mirror of the S-57 spec text, not the IHO S-57 document itself) — used only to corroborate enumerated values, not as the primary quote

- **key**: admiralty-catzoc-myths
  **title**: "Category Zones of Confidence (CATZOC) – dispelling the myths"
  **body**: UK Admiralty (UKHO)
  **url**: https://www.admiralty.co.uk/news/CATZOC-dispelling-the-myths
  **status**: secondary — practitioner explainer, not the standard itself; used only for the mariner-facing framing

## 1. CATZOC category definitions — the actual table

Quoted verbatim from **S-68 Annex A, "Table A-1 – Zones of Confidence categories"**, itself
sourced (per its own footer) from **IHO S-57 Ed 3.1 Supp 3 (Jun 2014), pp 13-14**. Six
categories total — five "assessed" grades plus one "unassessed" grade:

> **A1** — Position Accuracy ± 5 m + 5% depth. Depth Accuracy = 0.50 + 1%d. Seafloor Coverage: "Full area search undertaken. Significant seafloor features detected (note 4) and depths measured." Typical Survey Characteristics: "Controlled, systematic survey (note 6) high position and depth accuracy achieved using DGPS or a minimum three high quality lines of position (LOP) and a multibeam, channel or mechanical sweep system."

> **A2** — Position Accuracy ± 20 m. Depth Accuracy = 1.00 + 2%d. Seafloor Coverage: "Full area search undertaken. Significant seafloor features detected (note 4) and depths measured." Typical Survey Characteristics: "Controlled, systematic survey (note 6) achieving position and depth accuracy less than ZOC A1 and using a modern survey echo-sounder (note 7) and a sonar or mechanical sweep system."

> **B** — Position Accuracy ± 50 m. Depth Accuracy = 1.00 + 2%d. Seafloor Coverage: "Full area search not achieved; uncharted features, hazardous to surface navigation are not expected but may exist." Typical Survey Characteristics: "Controlled, systematic survey (note 6) achieving similar depth but lesser position accuracies than ZOC A2, using a modern survey echo-sounder (note 7), but no sonar or mechanical sweep system."

> **C** — Position Accuracy ± 500 m. Depth Accuracy = 2.00 + 5%d. Seafloor Coverage: "Full area search not achieved, depth anomalies may be expected." Typical Survey Characteristics: "Low accuracy survey or data collected on an opportunity basis such as soundings on passage."

> **D** — Position Accuracy "Worse than ZOC C". Depth Accuracy "Worse than ZOC C." Seafloor Coverage: "Full area search not achieved, large depth anomalies may be expected." Typical Survey Characteristics: "Poor quality data or data that cannot be quality assessed due to lack of information."

> **U** — "Unassessed - The quality of the bathymetric data has yet to be assessed."

(S-68, pp. 21-22, Annex A / Table A-1; column footer: "Source: IHO S-57 Ed 3.1 Supp 3 (Jun 2014), pp 13-14.")

The main body (S-68 §5, p.2) frames the six-way split explicitly:

> "CATZOC for assessed data (A1, A2, B, C and D) and a sixth category (U) for data which has not been assessed (see Table 5-1 below). The attribute CATZOC is a mandatory attribute in the S-57 Meta Object class M_QUAL (Quality of Data). The Meta Object M_QUAL is mandatory for areas containing depth data; that is, CATZOC indication covers all areas of the ENC that contain bathymetry. CATZOC sectors may never overlap and/or have gaps between them."

Note the last sentence: coverage is a *partition*, not an opt-in overlay — every charted area, including "we don't really know" areas, is required to carry an explicit confidence grade. There is no "unmarked = fine" default state available to the cartographer.

Explanatory notes (S-68 Annex A, Notes 1-2, p.22) are important for the "what does the number actually promise" question:

> "Note 1: The allocation of a ZOC indicates that particular data meets minimum criteria for position and depth accuracy and seafloor coverage defined in this Table. ZOC categories reflect a charting standard and not just a hydrographic survey standard. Depth and position accuracies specified for each ZOC category refer to the errors of the final depicted soundings and include not only survey errors but also other errors introduced in the chart production process."

> "Note 2: Position accuracy of depicted soundings at 95% CI (2.45 sigma) with respect to the given datum. It is the cumulative error and includes survey, transformation and digitizing errors etc. Position accuracy need not be rigorously computed for ZOCs B, C and D but may be estimated based on type of equipment, calibration regime, historical accuracy etc."

> "Note 4: Significant seafloor features are defined as those rising above depicted depths by more than: a. <40m: 2 m; b. >40m: 10% depth. A full seafloor search indicates that a systematic survey was conducted using detection systems, depth measurement systems, procedures, and trained personnel designed to detect and measure depths on significant seafloor features... It is impossible to guarantee that no significant feature could remain undetected, and significant features may have become present in the area since the time of the survey."

## 2. S-101 successor scheme (numeric, not just alphanumeric)

S-68 §5, p.2:

> "In S-101 QoBD, the CATZOC alphanumeric codes (A1, A2, B, C, D and U) are supplemented by a numerical scheme (1 for best quality data and 5 for worst, as well as 6 for unassessed areas). In addition to one attribute (CATZOC) defining all aspects of data quality, each data quality component (for example, position, depth, and coverage) are independently evaluated."

So the newer standard (S-101 "Quality of Bathymetric Data", QoBD) goes further than a single scalar grade: position accuracy, depth accuracy, and coverage are tracked as **independent** confidence axes rather than folded into one letter. Directly relevant to arcviz if it ever wants a multi-axis confidence signal rather than one enum.

## 3. Visual symbology (how the grade is actually drawn)

S-67 §5, p.13-14 ("Zones of Confidence symbols in ENCs"):

> "There are two validations of Zones of Confidence: Assessed / Unassessed. Areas that have been assessed are symbolized by the number of stars. Areas which have not been assessed are symbolized by the letter U. The number of stars is an indication of the CATZOC value: 6 stars = A1 (in a triangle); 5 stars = A2 (in a triangle); 4 stars = B (in a triangle); 3 stars = C (in a horizontal bar); 2 stars = D (in a horizontal bar)."

> "The boundary of the CATZOC areas is defined by a dashed line."

Note the shape change, not just star-count: A1/A2/B render in a **triangle**, C/D render in a **horizontal bar** — the container shape itself steps down at the "full area search not achieved" threshold (between B and C), so the symbol family is doing double duty (count = grade, shape = a coarser "was this actually surveyed properly" bit).

## 4. The documented failure mode — a live critique that the graded signal is often ignored

S-67 §5, p.14, describing operational reality in ECDIS (electronic chart) use:

> "This kind of symbology tends to clutter the screen, therefore during execution of a voyage mariners will most likely de-activate this setting. However, when planning a new route or changing an existing route whilst en-route, mariners are recommended to activate the CATZOC display and use the information provided to support their decision making process before accepting the new route in the ECDIS system."

This is a documented, IHO-published admission that the confidence layer is **opt-in and routinely switched off** during the riskiest phase (real-time transit) — it survives mainly at planning time. Directly relevant to "will a user actually see/understand the distinction" (assignment point 6).

S-67 §5.1, p.14, on what the grades *mean* operationally (worth quoting because it shows the standard doesn't stop at a number — it tells you what to do with it):

> "Put in simple terms, mariners should be able to navigate with confidence in areas with ZOC A1 and A2 classifications. It is possible, but unlikely, that an uncharted danger affecting surface navigation exists in ZOC B areas. In ZOC C areas mariners should exercise caution since hazardous uncharted features may be expected, particularly in or near reef and rocky areas. A very high degree of caution is required for areas assessed as ZOC D, as these contain either very sparse data or may not have been surveyed at all. Finally, it is good practice to treat ZOC U areas with the same degree of caution as ZOC D areas."

And a real coverage snapshot (S-67 Table 5-1, p.14) — CATZOC "U" (unassessed) is not a rare edge case in practice:

> World's coastal ENC (32 nations, ~14.2M km², from 2015 Navigation Purpose 3/4 ENC): A1 0.7%, A2 1.0%, B 30.5%, C 21.8%, D 20.5%, **Unassessed (U) 25.4%** — labelled "Poor" confidence.

A quarter of surveyed coastal chart area is formally "unassessed," which is itself evidence the "we haven't graded this yet" state is common enough to need first-class, unmissable symbology, not an edge case.

## 5. Secondary corroboration (S-57 attribute enumeration, via CARIS mirror)

Not independently verified against the IHO S-57 document itself (paywalled/binary), so treat
as **secondary**, consistent with the S-68 table above:

> "CATZOC ... Code: 72 ... Type: E (Enumerated)." Values: A1 "Position ±5m + 5% depth; Depth =0.50 + 1%d; Full area search with significant seafloor features detected." A2 "...controlled systematic survey." B "...Full area search not achieved but uncharted hazards unlikely." C "...depth anomalies may exist." D "...Position/depth worse than C...large anomalies expected." U "zone of confidence U (data not assessed) - Bathymetric quality remains unassessed."

(https://docs.teledynecaris.com/s-57/S57Cat/S57CatSite/attribut/catzoc.htm)

## Design takeaways (Inference (ours) — not asserted by any source above)

Inference (ours): CATZOC is arcviz's strongest precedent because it is a **live, multi-grade,
mandatory-coverage confidence rating** baked into the data model itself (an S-57 attribute),
not just a rendering choice — every bathymetric area *must* carry one of six values, so "we
didn't grade this" is impossible to represent as silence. That maps onto HP1's requirement
that "contents withheld" not be visually or structurally indistinguishable from "no data
recorded." The A1..D ladder is a confidence-in-measurement axis (closer to "how much do we
trust the value") rather than a existence/topology axis, so it maps most directly onto a
richer version of arcviz's node-state #1 (something is known to exist, but how much do we
actually know about it) rather than directly onto states #2 or #3, which are more about
absence and blindness respectively — CATZOC doesn't have a category for "we know something
is there but literally cannot see it," which is closer to arcviz's blinded-edge state (#3).
