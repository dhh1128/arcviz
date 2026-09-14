# The Glomar response ("neither confirm nor deny") — capture

Status: PRIMARY (court opinion text, fetched directly from CourtListener via reader proxy after direct fetch was blocked by CourtListener's bot-challenge; opinion ID confirmed via CourtListener's own citation search, cross-checked against the reporter citation 546 F.2d 1009).
Case: Phillippi v. Central Intelligence Agency, 546 F.2d 1009, 178 U.S.App.D.C. 243 (D.C. Cir. 1976) (Wright, J.; MacKinnon, J., dissenting).
Retrieved: 2026-09-14. Source URL: https://www.courtlistener.com/opinion/341477/harriet-ann-phillippi-v-central-intelligence-agency-and-george-h-bush/

NOTE ON A MIS-FETCH DURING RESEARCH: an earlier fetch of a *different* CourtListener opinion ID (7897441) returned a LATER, related Phillippi opinion (the post-remand D.C. Cir. decision, apparently ~1981, discussing the Carter-administration disclosures and Military Audit Project v. Casey). That opinion is NOT the 1976 originating Glomar opinion and is not relied on for the Glomar formulation below, though it confirms the case's subsequent history (CIA abandoned the Glomar position in 1977 after the Carter administration took office). The correct originating-opinion ID, verified via CourtListener's citation search for "546 F.2d 1009," is 341477.

## The agency's original response (quoted in the opinion)

> "Mr. Duckett has determined that, in the interest of national security, involvement by the U.S. Government in the activities which are the subject matter of your request can neither be confirmed nor denied. Therefore, he has determined that the fact of the existence or non-existence of any material or documents that may exist which would reveal any CIA connection or interest in the activities of the Glomar Explorer is duly classified Secret in accordance with criteria established by Executive Order 11652."

## The court's formulation of the doctrine (the load-bearing passage)

> "Thus we are dealing with a case in which the Agency has refused to confirm or deny the existence of materials requested under the FOIA, and its refusal has been upheld by the District Court. In effect, the situation is as if appellant had requested and been refused permission to see a document which says either 'Yes, we have records related to contacts with the media concerning the Glomar Explorer' or 'No, we do not have any such records.'"

This is the exact "third state" formulation: the withheld thing is not a document's contents, but the yes/no fact of the document's existence itself. Confirming would leak precisely what the exemption protects; so would denying (since a denial in some cases would itself be informative by elimination, when the agency answers "no" for genuinely empty requests but "NCND" for sensitive ones — differential responses leak information). Hence the response must be constant regardless of the true state.

## Why this required special procedure at all (in camera problem)

> "When the Agency's position is that it can neither confirm nor deny the existence of the requested records, there are no relevant documents for the court to examine other than the affidavits which explain the Agency's refusal."

> "Adapting these procedures to the present case would require the Agency to provide a public affidavit explaining in as much detail as is possible the basis for its claim that it can be required neither to confirm nor to deny the existence of the requested records."

## Explicit distinction from the Vaughn index — Glomar is a DIFFERENT, prior-order state

> "Since the 'document' the Agency is currently asserting the right to withhold is confirmation or denial of the existence of the requested records, we stress that we are not requiring, at this stage, the Vaughn index requested by appellant. If the District Court should decide on remand that the Agency's refusal to confirm or deny the existence of the requested records is unjustified, the standard Vaughn procedures, including preparation of a detailed index to the requested records, if any, would then apply."

This sentence is doing exactly the structural work arcviz needs cited: the court treats "produced-with-a-Vaughn-index" (known to exist, itemized, contents withheld) and "Glomar/NCND" (cannot even confirm existence) as two DIFFERENT DOCTRINAL TIERS, not two flavors of the same withholding. A Vaughn index answers "yes, and here is why we're not showing you." A Glomar response refuses to answer "yes or no" at all, because doing so would itself disclose the protected fact. That is a strict superset/different-kind relationship, not a matter of degree.

## Legal classification: Exemption 1 (national security) / Exemption 3 (statutorily-protected sources & methods)

The 1976 opinion resolves the case on the basis that the CIA's underlying refusal could be grounded in FOIA Exemption 3 via the National Security Act (50 U.S.C. § 403(d)(3), protection of "intelligence sources and methods"), with Exemption 1 (classified information) also implicated. Per the same source, the case was later mooted when "the newly installed Carter administration abandoned the position that the CIA could neither confirm nor deny even the existence of records" (1977) and the CIA admitted 154 responsive documents existed — illustrating that a Glomar response is a *position*, not an immutable fact about the world; it can be officially withdrawn once the sensitive fact is no longer sensitive.

## Why this is structurally distinct from BOTH "produced" and "no record exists" (synthesis, grounded in the quotes above)

- "Produced" (possibly redacted, Vaughn-indexed) = the agency affirms the record's existence and gives a typed, itemized reason for what's withheld.
- "No responsive record" = the agency affirms the record's NON-existence — an ordinary negative.
- Glomar/NCND = the agency refuses to assert EITHER of the above, because doing so would collapse a binary the requester cannot otherwise resolve, and that binary is itself the protected fact. Structurally this is not "no answer" (silence) — it is a distinct, deliberate, affirmatively-labeled non-answer that itself carries information ("this category of question is one I will always decline to resolve") without carrying the object-level answer.

## Inference (ours) — mapping to arcviz's "blinded edge"

Glomar is the closer analogue to arcviz's blinded edge (state 3: out-degree known, destination unknown) than to the missing-referent state (state 2), because Glomar is not "we don't have it" — it is "resolving whether-and-where would itself leak the topology." A missing referent (state 2, "an edge names a far node we don't have") is closer to an FOIA agency saying "yes, a responsive record exists elsewhere (a sibling agency, e.g.), but we cannot produce it" — the existence is conceded, only the *content* is unreachable. Glomar denies you even the existence-fact. arcviz's blinded edge is a hybrid: we know a relationship commitment exists (so we are not doing full Glomar — we don't deny existence) but we cannot resolve its destination(s), which is a narrower withholding than full NCND. This makes it worth distinguishing in the arcviz visual vocabulary from pure Glomar, not just borrowing the icon directly — flag this nuance for the design document.

## Known limits / commentary on public comprehension (secondary, but from an official body)

FOIA Advisory Committee (2020–2022 term), as reported by the Yale Journal on Regulation Notice & Comment blog (https://www.yalejreg.com/nc/shhh-dont-say-glomar-anymore/, retrieved 2026-09-14) and by the National Archives' own FOIA blog (https://foia.blogs.archives.gov/2024/01/25/what-the-foia-is-glomar, retrieved 2026-09-14):

> "the term 'Glomar' is opaque to ordinary citizens. Moreover, 'Glomar' suggests that the response may only be used when invoking the (b)(1) exemption protecting classified information, despite its current use in conjunction with several other FOIA exemptions."

> "Members of the 2020-2022 FAC felt strongly that the term 'Glomar' was jargon – making it more difficult for ordinary citizens to interact with and participate in government."

The Committee's recommendation was that agencies use "neither confirm nor deny" (NCND) rather than "Glomar" in citizen-facing responses. This is direct, official-body evidence that even the NAME of the third state is acknowledged (by the government body that oversees FOIA administration) to confuse ordinary requesters — a caution for arcviz: whatever visual/verbal label is chosen for the "blinded edge" state needs a plain-language gloss, not just a term of art, if it's meant to be understood without training.
