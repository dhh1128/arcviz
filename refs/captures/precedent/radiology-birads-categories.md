# BI-RADS assessment categories (0–6) — ACR primary source

## Source record
- Key: `radiology-birads-categories`
- Title: "The American College of Radiology BI-RADS® ATLAS and MQSA: Frequently Asked Questions"
- Body: American College of Radiology (ACR)
- URL: https://cs.acr.org/-/media/ACR/Files/RADS/BI-RADS/Mammography-FAQ.pdf (server 302-redirects a browser to an ACR/Sitecor login shell, but the PDF itself was fetched directly and is freely downloadable — not paywalled)
- Document date: header says "Updated: DRAFT 11/29/12"; footer file metadata says "Revised: 8/11/11". Pre-dates the 5th edition (2013) and v2025, but the category structure (0–6) and the "incomplete vs. final" split it documents are unchanged in later editions per secondary sources below.
- Retrieved: 2026-09-14
- Status: **PRIMARY** (ACR's own document, fetched directly, full text captured — not a paraphrase)
- Capture: this file (verbatim transcription of the relevant tables/paragraphs, from the fetched PDF, pages 1–5)

## The category table, verbatim

The document's own table is split into two labeled sub-sections — this split is itself the load-bearing structural fact:

> **Breast Imaging Reporting and Database System (BI-RADS®)**
> **a. Assessment is Incomplete**
> | Category | Assessment | Follow-up Recommendations |
> |---|---|---|
> | 0 | Need Additional Imaging Evaluation and/or Prior Mammograms for Comparison | Additional imaging and/or prior images are needed before a final assessment can be assigned |
>
> **b. Assessment is Complete – Final Categories**
> | Category | Assessment | Follow-up Recommendations |
> |---|---|---|
> | 1 | Negative | Routine annual screening mammography (for women over age 40) |
> | 2 | Benign Finding(s) | Routine annual screening mammography (for women over age 40) |
> | 3 | Probably Benign Finding – Initial Short-Interval Follow-Up Suggested | Initial short-term follow up (usually 6-month) examination |
> | 4 | Suspicious Abnormality – Biopsy Should Be Considered. Optional subdivisions: 4A (low suspicion), 4B (intermediate suspicion), 4C (moderate concern, not classic for malignancy) | Usually requires biopsy |
> | 5 | Highly Suggestive of Malignancy – Appropriate Action Should Be Taken | Requires biopsy or surgical treatment |
> | 6 | Known Biopsy-Proven Malignancy – Appropriate Action Should Be Taken | Category reserved for lesions identified on imaging study with biopsy proof of malignancy prior to definitive therapy |

## Count: how many categories are genuinely "we don't know yet" vs. "we know"

Only **Category 0** is the "incomplete / unknown" grade — a single category, explicitly bucketed by ACR itself under the header "a. Assessment is Incomplete," separate from a second header "b. Assessment is Complete – Final Categories" that covers 1 through 6. So the system is 1-of-7 "incomplete," not several — the "0 through 6" framing in the assignment overstates how many grades represent uncertainty. Categories 1–2 are "known and fine" (negative/benign); 3 is "known, probably fine, verify"; 4–5 are "known, probably not fine"; 6 is not really an assessment of ambiguity at all — it's a bookkeeping category for something *already biopsy-confirmed malignant*, used only to keep already-diagnosed cases out of the assessment/audit pipeline (see rationale below). So structurally: **1 unknown grade (0), 5 known grades (1,2,3,4,5), 1 non-assessment bookkeeping grade (6)**.

## Category 6's rationale — a distinct design lesson (topology-adjacent)

> "A major rationale for adding Category 6 is that examinations meriting this assessment should be excluded from auditing. Auditing that includes such examinations would inappropriately indicate inflated cancer detection rates, positive predictive values, and other outcomes parameters."
> — same document, "General" section, answer to "What is BI-RADS Category 6 ... and when would a facility use it?"

Inference (ours): this is a caution about conflating a *known-answer* state with the *general population of assessments*, for measurement-integrity reasons — not directly analogous to arcviz's three states, but a reminder that a "special" grade can exist purely to prevent statistical/визual pollution of the "normal" pool.

## FDA-approved final assessment text (verbatim options)

The MQSA/FDA regulates the literal wording a report may use per category. For Category 0, the FDA-approved options include (verbatim bullet list from the ACR document, page 4):

> - Incomplete: Need Additional Imaging Evaluation
> - Incomplete: Needs Additional Imaging Evaluation
> - Incomplete: Additional Imaging Evaluation Needed
> - Incomplete: Need Additional Imaging Evaluation - Comparison with Prior Studies
> - Incomplete: Need Additional Imaging Evaluation and/or Prior Mammograms for Comparison
> - Incomplete: Need Prior Mammograms for Comparison
> - Need Additional Imaging Evaluation *(the term "Incomplete" can be inferred in this example as this is the only Incomplete BI-RADS® assessment category)*
> - Incomplete Mammogram: Need Additional Imaging Evaluation

Every single FDA-approved variant for Category 0 keeps the word "Incomplete" (or lets it be inferred as unique), and none of them use language that could be mistaken for "Negative" or "Benign." This is the mechanism that prevents an incomplete study from reading as a clean bill of health — the standardized vocabulary itself is a controlled, closed list; a radiologist cannot free-text a Category-0 assessment that sounds like Category 1.

## A limitation ACR itself documents: BI-RADS 0 conflates two different "unknown" causes

> "Q. Does BI-RADS® Category 0 ... have a subcategory that addresses technical errors on mammograms (e.g., motion, artifacts, insufficient tissue, etc.) to indicate that the mammogram needs repeating (i.e., 'technical recall')?
> A. No, there is no official subcategory for technical errors in BI-RADS® Category 0. You may create your own subcategory for internal analysis purposes... Keep in mind that the FDA regulations require you to assign only the FDA-approved categories as final assessments."
> — same document, "Mammography" section

Inference (ours): this is directly relevant to arcviz's HP1 distinction between "we don't have this node" (missing referent) and "we have a blinded pointer" (topology unknown) — BI-RADS 0 does NOT distinguish "we saw something ambiguous and need a better look" from "the image itself was technically inadequate" (motion, insufficient tissue). Both collapse into the same single code. This is evidence that even a well-regarded, decades-old standardized system did not fully solve the N-way-distinction problem — it solved the 2-way problem (incomplete vs. complete) cleanly, but left a known internal conflation. Worth citing as a boundary condition on how far the precedent goes, not a demonstration that N>2 distinctions are solved.

## Also on this page: the "universal disclaimer" question (relevant to "normal ≠ nothing bad" epistemics)

> "Page 4 of the introduction to the 2003 ACR BI-RADS® Atlas states: '…universal disclaimers are not necessary since it is well established that a negative mammogram cannot exclude cancer and a clinically suspicious area should be biopsied even if the mammogram is negative.'"

This is a second-hand quote (the FAQ quoting the Atlas), so it is itself primary-adjacent (ACR quoting ACR) but the ultimate Atlas text is paywalled — mark the Atlas itself as a **lead**, not independently verified.
