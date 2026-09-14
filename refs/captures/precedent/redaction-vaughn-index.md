# Vaughn v. Rosen and the Vaughn index — capture

Status: PRIMARY (court opinion text, fetched via Justia mirror of the D.C. Circuit reporter text).
Case: Vaughn v. Rosen, 484 F.2d 820, 157 U.S.App.D.C. 340 (D.C. Cir. 1973), cert. denied, 415 U.S. 977 (1974).
Retrieved: 2026-09-14. Source URL: https://law.justia.com/cases/federal/appellate-courts/F2/484/820/195226/ (fetched via r.jina.ai reader proxy after direct WebFetch/curl were blocked by the host; text below is the reader-extracted plain text of the Justia page, spot-checked against the case's well-known holding as independently summarized by multiple secondary sources — treat as primary but reader-mediated).

## The problem the court identified (Part II, "Judicial Rewiew of Exemption Claims")

> "The simple fact is that existing customary procedures foster inefficiency and create a situation in which the Government need only carry its burden of proof against a party that is effectively helpless and a court system that is never designed to act in an adversary capacity. It is vital that some process be formulated that will (1) assure that a party's right to information is not submerged beneath governmental obfuscation and mischaracterization, and (2) permit the court system effectively and efficiently to evaluate the factual nature of disputed information."

This is the structural diagnosis: the requester cannot see what was withheld, so ordinary adversarial fact-finding collapses. The remedy is Part III.B.

## The holding — Part III.B, "Specificity, Separation, and Indexing"

> "The need for adequate specificity is closely related to assuring a proper justification by the governmental agency. In a large document it is vital that the agency specify in detail which portions of the document are disclosable and which are allegedly exempt. This could be achieved by formulating a system of itemizing and indexing that would correlate statements made in the Government's refusal justification with the actual portions of the document."

> "Such an indexing system would subdivide the document under consideration into manageable parts cross-referenced to the relevant portion of the Government's justification. Opposing counsel should consult with a view toward eliminating from consideration those portions that are not controverted and narrowing the scope of the court's inquiry. After the issues are focused, the District Judge may examine and rule on each element of the itemized list. When appealed, such an itemized ruling should be much more easily reviewed than would be the case if the government agency were permitted to make a generalized argument in favor of exemption."

## Why itemization, specifically (the court's own reasoning against blanket withholding)

> "While it is not impossible, it seems highly unlikely that a particular element of the information sought would be exempt under both exemptions. Even if isolated portions of the document are exempt under more than one exemption, it is preposterous to contend that all of the information is equally exempt under all of the alleged exemptions. It seems probable that some portions may fit under one exemption, while other segments fall under another, while still other segments are not exempt at all and should be disclosed. The itemization and indexing that we herein require should reflect this."

## Part III.C, "Adequate Adversary Testing" — the purpose clause

> "Given more adequate, or rather less conclusory, justification in the Government's legal claims, and more specificity by separating and indexing the assertedly exempt documents themselves, a more adequate adversary testing will be produced."

## The remand order (operative holding)

> "Upon remand the Government should undertake to justify in much less conclusory terms its assertion of exemption and to index the information in a manner consistent with Part III above."

## Structural analogue to arcviz (Inference (ours))

The Vaughn index is "known to exist, contents withheld, but attested by an external, itemized index that names WHICH exemption/reason applies to WHICH specific withheld portion." It is the closest legal precedent to arcviz state 1 (a node known to exist, contents withheld) — the index is a structured, machine/human-checkable commitment about the shape and reason for the withholding, without revealing the withheld content itself. The court's stated purposes — (a) let a judge rule without personally inspecting every withheld item, (b) support appellate/external review, (c) give the disadvantaged party enough to contest the withholding — map onto why arcviz should attest a withheld node/edge with a typed commitment rather than leaving it as silent absence: it lets a verifier reason about the shape of what's missing without having the content.

## Later confirmation that Vaughn indices are a LITIGATION-stage remedy, not automatic

Per secondary commentary (LLRX "FOIA Facts," foia.wiki) not independently re-verified here: a requester whose FOIA request is still at the administrative (pre-litigation) stage is not entitled to a Vaughn index — it only issues once a case is in court. This qualifies any claim that "every withholding is always indexed" — flag as SECONDARY, not verified against primary source in this pass.
