# Credential types from W3C VC use-case documents and the OpenWallet Foundation

Compiled 2026-09-21 by extraction from fetched web sources. Every entry below was read from a page actually retrieved during this pass; nothing is filled in from memory except the clearly-headed final section. No deduplication has been applied, either within or across sources — the same real-world credential (a passport, a birth certificate) appears once per place a source names it, because the wording and the assertion differ each time and the orchestrator may want to see the variation.

## Fetches performed, and their outcome

| URL | Outcome |
| --- | --- |
| https://www.w3.org/TR/vc-use-cases/ | HTTP 200, 308 KB, read in full |
| https://www.w3.org/TR/vc-overview/ | HTTP 200, read |
| https://www.w3.org/TR/vc-imp-guide/ | HTTP 200, read |
| https://www.w3.org/TR/vc-data-model-2.0/ | HTTP 200, read (examples and relevant prose) |
| https://w3c.github.io/vc-recognized-entities/ | HTTP 200, read (Use Cases and Data Model sections) |
| https://www.w3.org/TR/vc-use-cases-2/ | HTTP 404 — no such document; probe only, nothing drawn from it |
| https://openwallet.foundation/ | HTTP 200, read |
| https://openwallet.foundation/projects/ | HTTP 200, read in full |
| https://openwallet.foundation/our-projects/ | HTTP 404 |
| https://openwallet.foundation/use-cases/ | HTTP 404 — OWF publishes no use-case page under that path |
| https://tac.openwallet.foundation/projects/ | HTTP 200, read |
| https://raw.githubusercontent.com/openwallet-foundation/tac/main/docs/projects/*.md | HTTP 200 for identity-credential, fwos, credo-ts, aca-py, vc-api, wallet-framework-dotnet, tuvali, vcx, multiformat-vc-ios, sd-jwt-js, didcomm-mediator; HTTP 404 for credhub |
| https://raw.githubusercontent.com/openwallet-foundation/multipaz/main/... (doctypes and utopia knowntypes, strings.json) | HTTP 200, read |
| https://raw.githubusercontent.com/openwallet-foundation/{eudiplo,credo-ts,bifold-wallet}/main/README.md | HTTP 200, read |
| https://multipaz.org/ | **FETCH FAILED** — TLS handshake error (`TLSV1_ALERT_INTERNAL_ERROR`) via both curl and WebFetch. Nothing recorded from it; the Multipaz material below comes from the OWF TAC page and the GitHub source tree instead. |
| https://eudiplo.de/ | **FETCH FAILED** — TLS certificate hostname mismatch. The EUDIPLO README on GitHub was read instead. |
| https://openwallet.foundation/2026/05/21/keyring-issuing-peer-to-peer-relationship-credentials-on-top-of-bifold/ | HTTP 200, but thin — see the KEYRING entry. |

## W3C Verifiable Credentials use-case and companion documents

The primary source is the W3C Group Note **"Verifiable Credentials Use Cases", 18 March 2026** (editors Joe Andrieu and Kevin Dean), at https://www.w3.org/TR/vc-use-cases/. Note that this is materially newer than the 2019 version that is widely mirrored: it has been re-edited, the Devices domain and two focal use cases (GS1 chain, Certificate of Origin) are recent additions, and the section anchors used in the citations below were verified against the fetched HTML rather than guessed.

### From the User Needs user stories (section 3)

Each user need carries an identifier of the form `E.1`, `R.2` etc., which the document uses as its own cross-reference scheme; those identifiers are given in the citations alongside the section anchor.

**Extended transcript / digital transcript credential**
- Asserts — that the named learner holds the standard set of course grades plus supplementary information on learner competencies, including work experiences and non-educational but marketable skills.
- Key fields — not stated as field names; the document describes the content as "course grades", "learner competencies", "work experiences", "marketable skills".
- Issuee? — yes (the student, at whose request the registrar issues it).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-1-education, need E.1.
- Status — stated ("Joleen issues a digital credential that includes an extended transcript").

**Government-issued identity certificate (test-centre identification)**
- Asserts — the attributes a testing centre requires to identify a candidate, in a form that is difficult to counterfeit.
- Key fields — not stated.
- Issuee? — yes (the test candidate).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-1-education, need E.2.
- Status — stated ("Her government-issued identity certificate is acceptable").

**Test result credential**
- Asserts — the results of a test taken in an online learning system by an identified participant.
- Key fields — not stated.
- Issuee? — yes (the course participant).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-1-education, need E.4.
- Status — stated ("allow the system to issue a verifiable credential regarding the results of his test").

**Verifiable address credential**
- Asserts — that a shipping address is accurate and belongs to the customer.
- Key fields — not stated in this story; the Implementation Guidelines give `address` / `PostalAddress` fields for its own address credential (see the companion-document section below).
- Issuee? — yes (the shopper).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-2-retail, need R.1.
- Status — inferred — the story says the merchant offers a discount "for customers who make verifiable addresses available" and that "Francis offers his certificate"; the credential is not given a type name.

**Identity credential used as proof of age**
- Asserts — that the holder is over 21, without revealing actual date of birth, address, or state ID number.
- Key fields — the story names what is *withheld*: date of birth, address, state ID number.
- Issuee? — yes (the purchaser).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-2-retail, need R.2.
- Status — stated ("She submits her identity credential that lets the liquor store owner know that she is over 21").

**Chamber-of-commerce proof of legitimacy (business legitimacy credential)**
- Asserts — that a web shop is a legitimate business; the credential "contains proof of legitimacy".
- Key fields — not stated.
- Issuee? — yes, but the subject is an organization (the web shop), not a person.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-2-retail, need R.3.
- Status — stated ("a credential issued by the chamber of commerce, that contains proof of legitimacy").

**Wholesale purchase entitlement credential (non-transferable)**
- Asserts — that the subject is entitled to enter a wholesaler's warehouse and purchase goods not available to the general public.
- Key fields — not stated, but the credential is explicitly "marked 'non-transferable'".
- Issuee? — yes (the registered trade customer).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-2-retail, need R.4.
- Status — stated.

**Postal-address confirmation credential (government-supplied, KYC input)**
- Asserts — that the subject receives postal mail at a certain address.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, need F.1.
- Status — stated ("government-supplied verifiable credentials that confirm she receives postal mail at a certain address").

**National ID card credential**
- Asserts — that the subject holds a national ID card.
- Key fields — not stated here; need F.5 adds "address, national identity number, etc." for the analogous government-issued certificate.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, need F.1.
- Status — stated ("that she has a national ID card").

**Bank / checking account credential (KYC-reusable)**
- Asserts — that the subject has an account at a named bank and has access to the associated checking account; that the bank verified the subject's identity; and, because the issuing bank is required to perform Know Your Customer checks, the credential "can also be treated as sufficient verification by other financial institutions".
- Key fields — not stated as field names. The document notes it "is issued to a controlled identifier over which Jane has demonstrated proof-of-control", and that proof-of-control is re-demonstrated at presentation.
- Issuee? — yes (the account holder).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, needs F.1 and F.3 (F.3 phrases the same credential as "indicating that the account exists, that the bank verified John's identity, and that John has access to the account", and is the revocation example).
- Status — stated.

**Identity profile (finance)**
- Asserts — an identity profile shareable with a money-transfer service so it can verify the source of funds.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, need F.2.
- Status — inferred — the story says "verifiable credentials in her credential repository that can be used to share her identity profile"; "identity profile" names an aggregate rather than a single credential type.

**Banking information credential (third-party, family-issued)**
- Asserts — the banking information of the recipient family, verifying the destination of a funds transfer.
- Key fields — not stated.
- Issuee? — yes; notable because the subject is the sender's family, not the holder presenting it.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, need F.2.
- Status — stated ("She has also been sent a credential from her family verifying their banking information").

**Government-issued identity certificate (remote account opening)**
- Asserts — the subject's identity for the purpose of opening a bank account remotely.
- Key fields — "address, national identity number, etc." (the document's own parenthetical).
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-3-finance, need F.5.
- Status — stated.

**State medical board certification (licence to practise medicine)**
- Asserts — that the subject is certified to practise medicine in a named state, and by extension may write prescriptions and referrals.
- Key fields — not stated.
- Issuee? — yes (the physician).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-4-healthcare, need H.1; the revocation case is at #x3-5-professional-credentials, need C.2, where lapsed certification means verifiers "will automatically be aware that he can no longer issue prescriptions or perform medical procedures".
- Status — stated.

**Electronic prescription**
- Asserts — a prescription for a named patient, written by a named physician; it carries a credential about the physician and one about the patient.
- Key fields — not stated.
- Issuee? — yes (the patient), with the prescriber also identified.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-4-healthcare, need H.2.
- Status — inferred — the prescription is described as the thing received and as the carrier of two certificates; the document does not explicitly call the prescription itself a verifiable credential.

**Insurance coverage / proof of insurance credential**
- Asserts — that the subject holds health insurance cover, such that a clinic can submit a claim for payment.
- Key fields — not stated.
- Issuee? — yes (the patient).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-4-healthcare, needs H.2 ("Bob's insurance coverage") and H.3 ("her verifiable credential that demonstrates her identity and her proof of insurance").
- Status — stated.

**Identity credential with selective disclosure and expiring disclosure (travelling patient)**
- Asserts — the subject's name and address, while withholding marital status and social security number; the disclosure is marked as expiring in 30 days.
- Key fields — name, address, marital status, social security number (the last two named as withheld).
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-4-healthcare, need H.4.
- Status — stated.

**Government-issued disability credential**
- Asserts — that the subject maintains legal disability status, without disclosing the specific disability.
- Key fields — not stated; the document is explicit that the specific disability is *not* disclosed, "as this could put her at personal risk".
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-4-healthcare, need H.5.
- Status — stated ("Trina provides her government-issued disability credential").

**Physician education credential**
- Asserts — the subject's education/schooling as a medical practitioner.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, needs C.1 and C.4.
- Status — stated ("verifiable credentials about their education, board certification, and continuing education").

**Board certification credential**
- Asserts — that the subject is board-certified in a medical specialty; revocable by the board, so lapse is automatically visible to verifiers.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, needs C.1, C.2, C.4.
- Status — stated.

**Continuing education credential**
- Asserts — the subject's continuing education achievements, which a professional board requires to maintain certification.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, needs C.1 and C.4.
- Status — stated.

**Professional training certificate (Project Manager)**
- Asserts — that the subject was trained as a Project Manager by a named training company.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.3.
- Status — stated ("Jane was issued a certificate by BigTraining Co., indicating that she was a trained Project Manager").

**Organizational accreditation credential**
- Asserts — that a training organization is accredited; revoking it invalidates credentials the organization issued.
- Key fields — not stated; the revocation source is named as "the US Department of Education's Accreditation Database".
- Issuee? — yes, an organization rather than a person.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.3.
- Status — stated ("their organization's certificate was revoked").

**Digital badge**
- Asserts — a qualification listed on a professional social network alongside degrees and certificates; in the second paragraph, a badge "based upon real-world certifications" that can be attached to forum posts.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.5.
- Status — stated ("degrees, certificates, and digital badges").

**Aid worker certification**
- Asserts — that the subject has been certified as an aid worker; presented in a minimized form that reveals only that she is the holder, that she is the subject, and that she is an aid worker, preserving pseudonymity on a controversial forum.
- Key fields — not stated; the three disclosed facts are enumerated in prose.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.5.
- Status — stated ("Paula has been certified as an aid worker").

**College degree credential**
- Asserts — that the subject holds a college degree, attached to a job application and evaluated automatically.
- Key fields — not stated here; see `ExampleDegreeCredential` under the Data Model 2.0 entries below for concrete fields.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.6.
- Status — stated ("her education credentials—college degree, additional specific software training").

**Software training credential**
- Asserts — that the subject completed specific software training.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-5-professional-credentials, need C.6.
- Status — stated.

**Digital driving licence**
- Asserts — a claim that the subject "has right to drive a car", usable to prove validity to a police officer.
- Key fields — not stated in the user story. Section 4.4 adds a caution that a DMV "should probably not be treated as authoritative for an individual's hair color or current address, even though such claims are often included in today's driver's licenses", which implies hair colour and current address as customary fields.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-6-legal-identity, need L.1; the authority caveat is at https://www.w3.org/TR/vc-use-cases/#x4-4-validate-credential.
- Status — stated.

**Self-issued driver's licence**
- Asserts — the same content as a driving licence, but issued by the subject to themselves; verification succeeds while validation would fail for a car rental, yet may be acceptable at a go-cart facility "for the purpose of leaderboards, announcements, and correspondence".
- Key fields — name and image are named as the fields a go-cart facility would use.
- Issuee? — yes (issuer and subject are the same party).
- Cite — https://www.w3.org/TR/vc-use-cases/#x4-4-validate-credential.
- Status — stated, as a worked validation example rather than a user story.

**Digital passport**
- Asserts — the subject's identity and citizenship for immigration purposes; the digital version "retains a history of all the places he visits", and immigration officials add the details of each new visit to it.
- Key fields — not stated in the user story; Appendix B.1 gives `givenName`, `familyName`, `citizenship` for its `PassportCredential` example.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-6-legal-identity, need L.2.
- Status — stated.

**Air travel Identity Profile**
- Asserts — an assembled collection of verifiable credentials sufficient for airport security to identify a passenger immediately and automatically.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-6-legal-identity, need L.3.
- Status — inferred — "a collection of verifiable credentials that are assembled into his air travel Identity Profile"; the profile is an aggregate presented as a unit, not a single issued credential.

**Self-sovereign proof of birth**
- Asserts — the subject's birth, with the proof of birth and proof of marriage of her parents attached; retrievable from many places over the Internet, which is what makes it usable by a refugee with no other documentation.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-6-legal-identity, need L.4.
- Status — stated.

**Proof of marriage (parents')**
- Asserts — the marriage of the subject's parents, attached to the proof of birth.
- Key fields — not stated.
- Issuee? — yes (the parents).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-6-legal-identity, need L.4.
- Status — stated ("the proof of birth and marriage for her parents").

**Device-identifying credential (IDevID, IAK)**
- Asserts — the manufacturing-time identity of an IoT device, issued at the factory by the manufacturer, verified at installation to establish the identity of the device during onboarding.
- Key fields — not stated; the document names the credential kinds as "IDevID, IAK".
- Issuee? — yes, but the subject is a device rather than a person or organization.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-7-devices, need D.1.
- Status — stated ("issues a device-identifying verifiable credential (e.g. IDevID, IAK) at the factory").

**Specification-compliance certification credential (device)**
- Asserts — that a device complies with a specification; verified to demonstrate "the controller's Energy-Star compliance".
- Key fields — not stated.
- Issuee? — yes (the device), issued by a certification testing lab.
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-7-devices, need D.1.
- Status — stated.

**Evidence-of-possession credential (supply chain custody)**
- Asserts — that a named reseller had possession of the device, and what software additions were made to it.
- Key fields — not stated.
- Issuee? — yes (the device).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-7-devices, need D.2.
- Status — stated ("verifiable credentials that establish evidence of possession by VAR Resellers and the software additions Vince made to the device").

**Owner-issued device trust / authorization credential**
- Asserts — trust attributes for a specific device and which other devices it is authorized to interact with.
- Key fields — "device manufacturer model/version, software manufacturer model/version, security versions of components TCB, and associated devices the fan controller is authorized to interact with including thermostat-board-room".
- Issuee? — yes (the device, subject; issued by its new owner).
- Cite — https://www.w3.org/TR/vc-use-cases/#x3-7-devices, need D.3.
- Status — stated.

### From the Focal Use Cases (section 5)

**Birth Certificate (Citizenship by Parentage)**
- Asserts — "Establishes relationship to mother with maiden name".
- Key fields — not stated in 5.1; Appendix B.1's `BirthCertificate` example gives `citizenship`, `birthDate`, `birthPlace` (with a nested `Hospital` and `address`), `givenName`, `familyName`, and a `parent` array of persons each with `givenName`, `familyName` and optionally `maidenName`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-1-4-verifiable-credentials; example at https://www.w3.org/TR/vc-use-cases/#example-anand-s-birth-certificate.
- Status — stated.

**Marriage License**
- Asserts — "Establishes mother's name change"; it carries the mother's maiden and married names.
- Key fields — not stated; the prose names maiden name and married name.
- Issuee? — yes (the two spouses).
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-1-4-verifiable-credentials.
- Status — stated.

**Mother's Passport**
- Asserts — "Establishes mother's US citizenship".
- Key fields — not stated.
- Issuee? — yes; notable because the holder presenting it (Sam) is not the subject (his mother).
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-1-4-verifiable-credentials.
- Status — stated.

**Sam's Passport**
- Asserts — "Establishes Sam is the child in the birth certificate".
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-1-4-verifiable-credentials.
- Status — stated.

**Advanced Open Water Instructor**
- Asserts — instructor-level dive certification, issued by a PADI-licensed dive school; described as public record, and required to be maintained for employment as a NOAA Dive Instructor.
- Key fields — not stated; the document notes each credential has an independent expiration cycle.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Drysuit Dive Certification**
- Asserts — specialist diver certification in dry suit diving; private, because it is for personal diving rather than instructing.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Night Diving Certification**
- Asserts — specialist diver certification in night diving; private.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Search & Recovery Dive Certification**
- Asserts — specialist diver certification in search and recovery; private.
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Fiji PADI School Affiliation Certification**
- Asserts — that a named dive school in Fiji is licensed by PADI to issue diving certifications in PADI's name.
- Key fields — not stated.
- Issuee? — yes, an organization (the dive school). Verifiers are expected to check both the certification's and the school's revocation services.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Australia PADI School Affiliation Certification**
- Asserts — the same, for a dive school in Australia; the pair exist separately because certification spans two jurisdictions.
- Key fields — not stated.
- Issuee? — yes (an organization).
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials.
- Status — stated.

**Signed log entry of dive event**
- Asserts — the roster of divers on a NOAA-sanctioned dive and their diving certifications; the dive master issues "a verifiable credential including those credentials" and signs and archives it. Threat responses propose that listed divers counter-sign, that divers mutually sign each other's log entries, and that the boat owner sign the log.
- Key fields — not stated.
- Issuee? — no single subject party; the credential is about an event and the set of credentials recorded at it. This is a credential whose subject is other credentials.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-4-verifiable-credentials, with the mechanics at #x5-2-3-scenario.
- Status — stated.

**Revocable status-check token (capability granted to an employer)**
- Asserts — a capability allowing NOAA to check the current status of all of Pat's certifications, not just the status of a single credential; renewing a certification makes the next check return the renewed one. Pat revokes it on retirement.
- Key fields — not stated.
- Issuee? — yes, but inverted: the individual issues it to his employer, so the recipient is an organization and the credential grants a permission rather than describing the subject.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-2-3-scenario; the capability framing is restated at #x5-2-2-distinction.
- Status — stated ("Pat issues NOAA a revocable token").

**Malathi's passport**
- Asserts — "Establishes identity of the traveling parent".
- Key fields — from the Appendix B.1 example, type `["VerifiableCredential", "PassportCredential"]` with `credentialSubject` carrying `givenName`, `familyName`, `citizenship`. A second variant models the passport as a document: `credentialSubject.passport` of `type: "Passport"` containing a nested `traveler` object with the same three fields.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-3-4-verifiable-credentials; examples at #example-malathi-s-passport-simple-model and #example-malathi-s-passport-passport-is-a-document-model.
- Status — stated.

**Anand's passport (minor's passport)**
- Asserts — "Establishes identity of the minor".
- Key fields — `givenName`, `familyName`, `citizenship`; type `["VerifiableCredential", "PassportCredential"]`.
- Issuee? — yes, and explicitly a case where the subject is not the holder: "The holder of the passport is a parent, not the minor."
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-3-4-verifiable-credentials; example at #example-anand-s-passport; the subject/holder distinction at #x5-3-2-distinction.
- Status — stated.

**Anand's Birth Certificate**
- Asserts — "Establishes relationship to parents and provides link from Rajesh to Anand that qualifies the permission to travel".
- Key fields — see the Birth Certificate entry above; type `["VerifiableCredential", "BirthCertificate"]`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-3-4-verifiable-credentials.
- Status — stated.

**Permission to travel (ChildTravelPass)**
- Asserts — that the non-traveling parent grants permission for the minor to travel out of the country with the other parent; the identity in it matches the parent named in the birth certificate, "establishing relevance". The document notes the DID system "replaces the role of the notary in the paper/physical world".
- Key fields — from the example, type `["VerifiableCredential", "ChildTravelPass"]`, `credentialSubject.potentialAction` of `type: "TravelAction"` with `agent`, `participant`, and `location` (a `Country` with `address.addressCountry`). It expires.
- Issuee? — yes, the minor is the subject; the issuer is the non-traveling parent, i.e. a private individual issuing about his own child.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-3-4-verifiable-credentials; example at #example-permission-to-travel-from-rajesh-using-schema-org-vocab.
- Status — stated.

**Upgrade coupon for first class ticket (frequent flyer coupon)**
- Asserts — redeemability for a first class upgrade on an international flight; the document's own gloss is that it "Introduces commercial value in a verifiable credential". The airline is liable for accepting it at ticketing; a threat response has the travel agent verify the coupon "through a distributed status registry".
- Key fields — not stated.
- Issuee? — yes, but it is a bearer-style entitlement whose value is the redemption right rather than a fact about the subject.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-3-4-verifiable-credentials.
- Status — stated.

**GS1 Prefix license**
- Asserts — "Issued by GS1 Global Office to GS1 Utopia (a GS1 Member Organization operating in the region of Utopia). Grants GS1 Utopia the right to issue GS1 Company Prefix licenses within the range of the GS1 Prefix in the license."
- Key fields — from the example, type `["VerifiableCredential", "GS1PrefixLicenseCredential"]`; `credentialSubject` has `organization` (with `gs1:partyGLN`, `gs1:organizationName`) and `licenseValue` (e.g. `"952"`); `credentialStatus` is a `BitstringStatusListEntry` with `statusPurpose: "revocation"`. Issued with `validFrom` but deliberately no `validUntil`.
- Issuee? — yes, an organization.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-4-4-verifiable-credentials; example at #example-gs1-prefix-952-licensed-by-gs1-global-office-to-gs1-utopia.
- Status — stated.

**GS1 Company Prefix license**
- Asserts — "Issued by GS1 Utopia to Healthy Tots. Grants Healthy Tots the right to issue GS1 identification keys within the range of the GS1 Company Prefix in the license." It is transferable to another user company on merger or acquisition, and can be revoked, suspended or replaced.
- Key fields — type `["VerifiableCredential", "GS1CompanyPrefixLicenseCredential"]`; `credentialSubject` has `organization`, `extendsCredential` (the ID of the prior credential) and `licenseValue` (e.g. `"9521234"`).
- Issuee? — yes, an organization.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-4-4-verifiable-credentials; example at #example-gs1-company-prefix-9521234-licensed-by-gs1-utopia-to-healthy-tots; transfer semantics at #x5-4-9-variation-license-transfer.
- Status — stated.

**Key (GTIN) credential**
- Asserts — "Issued by Healthy Tots to declare the existence of a GS1 identification key, typically a GTIN, within the range of the GS1 Company Prefix." It "will remain valid in perpetuity, long after trade items identified by the GTIN are no longer in the supply chain".
- Key fields — type `["VerifiableCredential", "KeyCredential"]`; `credentialSubject.id` is the GTIN as a GS1 Digital Link URI (e.g. `https://id.gs1.org/01/09521234555551`) and `credentialSubject.extendsCredential` points at the company prefix licence.
- Issuee? — no. The subject is the GTIN, i.e. a trade item identifier, not a party: "For the trade item Verifiable Credential, the subject is the GTIN represented as a GS1 Digital Link URI."
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-4-4-verifiable-credentials; example at #example-gtin-9521234555551-issued-by-healthy-tots; subject statement at #x5-4-5-2-subject.
- Status — stated.

**Product recall notice**
- Asserts — a recall, linked to a GTIN key credential.
- Key fields — not stated.
- Issuee? — no (it is about a trade item).
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-4-9-1-revocation.
- Status — inferred — named only in passing, as an example of "Other dependent credentials that are created after revocation [that] may be valid, such as a product recall notice linked to a GTIN key credential".

**Trade item data credential (product description, recycling instructions)**
- Asserts — data about the trade item identified by a GTIN: "brand, size and unit of measure, ingredients, dimensions and weights", and elsewhere "those that describe the product or that provide information such as recycling instructions".
- Key fields — the attribute list just quoted; no formal field names given.
- Issuee? — no (subject is the trade item).
- Cite — https://www.w3.org/TR/vc-use-cases/#b-2-focal-use-case-chain-of-gs1-credentials-to-identify-a-trade-item and #x5-4-9-1-revocation.
- Status — inferred — the document describes the class of credentials issued "around" the GTIN key credential without naming a single type.

**Certificate of Origin**
- Asserts — "the origin of the goods"; used by importers "to claim tariff exemptions, demonstrate compliance with trade agreements like Free Trade Agreements (FTAs) or to meet the importing regulations". It is progressively redacted as it moves downstream: the exporter redacts manufacturer details before sending to the importer, and the importer further redacts exporter details before sharing with retailers.
- Key fields — not stated.
- Issuee? — the document makes an unusual claim here: "The Subject of the CO is the certificate itself, which confirms that the goods being exported originate from a specific country." So the stated subject is neither a person nor the goods but the document. Recorded as stated, but flagged; it reads as an editing artefact rather than a considered modelling choice.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-5-3-trade-flow and #x5-5-4-2-subject.
- Status — stated.

**Bill of Lading**
- Asserts — issued by the shipping company to the exporter "for claiming goods in the importing country"; one of the documents customs requires.
- Key fields — not stated.
- Issuee? — unknown; the document names it as a required document without modelling its subject.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-5-3-trade-flow, step 7; listed at #x5-5-1-background.
- Status — stated (named as one of the documents in the flow), though the document never explicitly says it is expressed as a verifiable credential.

**Exporter's Invoice**
- Asserts — the commercial terms of the export sale; submitted with the import declaration.
- Key fields — not stated; pricing is named as information the exporter may redact.
- Issuee? — unknown.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-5-1-background and #x5-5-3-trade-flow, step 8.
- Status — stated as a document in the flow; same caveat as the Bill of Lading.

**Product Test Report**
- Asserts — that goods meet required safety and quality standards, "issued by a testing laboratory from manufacturer"; redacted of manufacturer details before travelling downstream.
- Key fields — not stated; "product details, quality, and safety report" is the closest the document comes.
- Issuee? — no; the subject is the product.
- Cite — https://www.w3.org/TR/vc-use-cases/#x5-5-1-background and #x5-5-3-trade-flow, steps 1–2.
- Status — stated.

### From companion W3C documents

Four companion documents were checked. Two of them — the Overview and the Implementation Guidelines — turned out to be much thinner on credential *types* than expected, and that is itself worth recording; see the closing notes.

**`ExampleDegreeCredential` (university degree)**
- Asserts — that the subject holds a named degree.
- Key fields — `credentialSubject.id`, `credentialSubject.degree` (an object with `type`, e.g. `"ExampleBachelorDegree"`, and `name`, e.g. `"Bachelor of Science and Arts"`); issued by a university with `validFrom`. One example combines it with `ExamplePersonCredential` and adds `alumniOf.name`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/ (Verifiable Credentials Data Model v2.0), the running example throughout §4 and the media-type examples in §6.
- Status — stated (a credential type used in the specification's normative examples, with the `Example` prefix marking it as illustrative vocabulary).

**`ExampleAlumniCredential`**
- Asserts — that the subject is an alumnus of a named university. The Overview's gloss: "It states that the person named 'Pat' … is an alumni of the Example University".
- Key fields — `credentialSubject.id`, `name`, `alumniOf` (an object with `id` and `name`).
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-overview/ (the document's single running example, repeated across every securing mechanism) and https://www.w3.org/TR/vc-data-model-2.0/.
- Status — stated.

**`ExampleDrivingLicenseCredential`**
- Asserts — a licence to drive; the example's whole point is that it carries two status entries at once.
- Key fields — `credentialSubject.license` (an object with `type: "ExampleDrivingLicense"` and `name: "License to Drive a Car"`); `credentialStatus` is an array of two `BitstringStatusListEntry` objects with `statusPurpose` `"revocation"` and `"suspension"` respectively.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Example 13 ("Use of multiple entries for the status property").
- Status — stated.

**`PermanentResidentCard`**
- Asserts — permanent residency; `name: "Permanent Resident Card"`, `description: "Government of Utopia Permanent Resident Card."`
- Key fields — `credentialSubject.type` is `["PermanentResident", "Person"]` with `givenName`, `familyName`, `gender`, `image`, `residentSince`, `lprCategory`, `lprNumber`, `commuterClassification`, `birthCountry`, `birthDate`; the credential carries `identifier`, `validFrom`, `validUntil`. Its context is `https://w3id.org/citizenship/v3`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Examples 30 and 31 (the BBS unlinkable selective-disclosure pair; the derived presentation discloses only `birthCountry`).
- Status — stated.

**`AgeVerificationCredential`**
- Asserts — that the subject is over a given age; `name: "Age Verification Credential"`.
- Key fields — `credentialSubject.overAge` (value `21` in the example); `validFrom`, `validUntil`, and a `refreshService` of type `VerifiableCredentialRefreshService2021`. Context `https://w3id.org/age/v1`. The specification notes "this particular verifiable credential is not intended to be shared with anyone except for the original issuer".
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Example 27 ("Use of the refreshService property by an issuer").
- Status — stated.

**`RelationshipCredential`**
- Asserts — that two named people are spouses; the example exists to show multiple subjects in one credential.
- Key fields — `credentialSubject` is an array of two objects, each with `id`, `name`, `spouse`.
- Issuee? — yes, two of them.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Example 10 ("Specifying multiple subjects in a verifiable credential").
- Status — stated.

**`OpenBadgeCredential`**
- Asserts — not stated; it appears as the specification's canonical illustration of "a more specific verifiable credential type" in the type-requirements table, and in a JWT-claims example.
- Key fields — not stated.
- Issuee? — unknown.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, the table of objects that must have a type specified.
- Status — stated (named only).

**`ExampleAchievementCredential`**
- Asserts — an achievement, in the multilingual example: `"Successful installation of the Example application"` / `"Instalación exitosa de la aplicación Example"`.
- Key fields — `credentialSubject.type` is `["AchievementSubject"]` containing an `achievement` object with `id`, `type: ["Achievement"]`, a language-mapped `name`, and `criteria.narrative`; the issuer is an object with `type: "Profile"`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Example 40 ("Example dual language credential").
- Status — stated.

**`ExampleFoodPreferenceCredential`**
- Asserts — a self-asserted food preference: `credentialSubject.favoriteCheese: "Gouda"`. Notable because issuer and holder are the same DID and there is no subject `id` at all.
- Key fields — `favoriteCheese`.
- Issuee? — no; the example deliberately omits a subject identifier.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, the self-asserted-credential examples in §4 (Example 20).
- Status — stated.

**`ExampleAssertCredential`**
- Asserts — a self-asserted claim *about a verifiable presentation*: `"This VP is submitted by the subject as evidence of a legal right to drive"`.
- Key fields — `credentialSubject.id` (the presentation's URN) and `assertion` (the sentence above).
- Issuee? — no; the subject is a presentation, not a party.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, Example 21.
- Status — stated.

**`ExampleMatrixCredential`**
- Asserts — nothing meaningful; it exists to show that a claim value can be a nested array. Recorded only because the extraction brief asks for every named type.
- Key fields — `credentialSubject.matrix`, an array of arrays of integers.
- Issuee? — yes nominally (`credentialSubject.id` is a DID), but the credential has no semantic content.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, the JSON-LD/media-type discussion in §6.
- Status — stated; flagged as a syntax fixture rather than a realistic credential.

**`MyPrototypeCredential`**
- Asserts — nothing; it is a placeholder the specification tells developers to rename: "A developer will change MyPrototypeCredential below to the type of credential they would like to create."
- Key fields — none.
- Issuee? — unknown.
- Cite — https://www.w3.org/TR/vc-data-model-2.0/, §4 getting-started prose.
- Status — stated; a template, not a credential type.

**`JsonSchemaCredential`**
- Asserts — a JSON Schema against which other credentials are validated; the Overview's example has `title: "ExampleAlumniCredential"`, `description: "Alumni Credential using JsonSchema"`.
- Key fields — a schema document as the credential subject.
- Issuee? — no; the subject is a schema.
- Cite — https://www.w3.org/TR/vc-overview/, the section on validation via `credentialSchema`.
- Status — stated. This is infrastructure — a credential whose subject is metadata about other credentials — not a credential about a person or thing in the world.

**`BitstringStatusListCredential`**
- Asserts — the revocation/suspension status of a large set of credentials, encoded as a compressed bitstring; the Overview notes "the default status list size is 131,072 entries".
- Key fields — a bitstring; referenced from other credentials by `credentialStatus.statusListCredential` and `statusListIndex`.
- Issuee? — no; the subject is a set of credential statuses.
- Cite — https://www.w3.org/TR/vc-overview/, the status-list section.
- Status — stated. Infrastructure, like `JsonSchemaCredential`.

**`DisputeCredential`**
- Asserts — that a specific other credential is disputed. Two shapes are given: a subject disputing a claim made about them ("the address property is incorrect or out of date"), and a third party disputing a claim made about someone else ("an imposter has claimed the social security number for an entity").
- Key fields — `credentialSubject.id` is the identifier of the *disputed credential*; `currentStatus: "Disputed"`; `statusReason` (a language-tagged value, e.g. `"Address is out of date"` or `"Credential contains disputed statements"`); optionally `disputedClaim`, itself an object naming the subject and the wrong claim.
- Issuee? — no; the subject is another credential. The document notes that where the disputed credential has no identifier, "a content-addressed identifier can be used".
- Cite — https://www.w3.org/TR/vc-imp-guide/ (Verifiable Credentials Implementation Guidelines 1.0, 24 September 2019), §6 Disputes.
- Status — stated. Genuinely unusual: a credential that contradicts another credential.

**`ExampleAddressCredential`**
- Asserts — the subject's postal address.
- Key fields — `credentialSubject.type: "Person"` with an `address` object of `type: "PostalAddress"` carrying `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry`.
- Issuee? — yes.
- Cite — https://www.w3.org/TR/vc-imp-guide/, the JSON-LD context section (Examples 8–10).
- Status — stated.

**`RecognizedEntityCredential`**
- Asserts — that the issuer "knows of one or more entities that are recognized to perform specific actions", such as issuing or verifying a particular type of verifiable credential. Recognition chains are traversable via a `recognizedIn` property, so one recognition credential can be recognized by another.
- Key fields — `credentialSubject` is an array of `RecognizedEntity` objects, each with `id`, `type`, `name`, `legalName`, `image`, `url`, `description`; each entity may carry `recognizedTo`, a list of `RecognizedAction` objects with an `action` value and optional `outputValidation` schemas; the issuer object may carry `type: "RecognizedIssuer"` and `recognizedIn`.
- Issuee? — yes, typically many organizations in one credential.
- Cite — https://w3c.github.io/vc-recognized-entities/ (Verifiable Credentials Recognized Entities; an **experimental editor's draft**, self-described as "not fit for production deployment" — not a TR-space document).
- Status — stated. The most structurally unusual type in this whole sweep: its subject is a *set of issuers*, and it exists to make trust registries expressible as credentials.

**Vital records: birth certificate, marriage certificate, death certificate**
- Asserts — each is a vital record a regional office may be recognized to issue for its jurisdiction; the recognition credential names "the type of vital record it might issue and the schema that record conforms to".
- Key fields — not stated.
- Issuee? — yes.
- Cite — https://w3c.github.io/vc-recognized-entities/, Use Cases → Vital Records.
- Status — inferred — named as examples of what a recognized agency issues, not defined as credential types by this document.

**Commercial invoice**
- Asserts — the commercial terms of an export sale, issued by the exporter's DID and presented by the importer to customs and to a trade-finance lender. The document gives volumes: "Roughly five billion commercial invoices are exchanged annually among approximately 50 million trading entities worldwide", with "a lifecycle of weeks to months".
- Key fields — not stated.
- Issuee? — no; the subject is a transaction. Verification turns on matching the DID in the invoice against the subject of the exporter's recognition credential.
- Cite — https://w3c.github.io/vc-recognized-entities/, Use Cases → Cross-border Trade.
- Status — inferred — described in a use-case narrative rather than defined.

**Certificate of conformity (CoC)**
- Asserts — "that a product meets specific safety or quality standards", issued by a conformity assessment body (CAB) and accompanying the product through the supply chain.
- Key fields — not stated.
- Issuee? — no; the subject is a product.
- Cite — https://w3c.github.io/vc-recognized-entities/, Use Cases → Product Conformity.
- Status — inferred — same basis.

**Accreditation scope credential (for a conformity assessment body)**
- Asserts — "that the CAB is accredited to perform conformity assessments within a defined scope", issued by a national accreditation authority.
- Key fields — not stated; it is a `RecognizedEntityCredential` specialised to this purpose.
- Issuee? — yes (the CAB, an organization).
- Cite — https://w3c.github.io/vc-recognized-entities/, Use Cases → Product Conformity.
- Status — inferred.

## OpenWallet Foundation

**An important framing caveat, because it changes how this section should be read.** OWF is organized around credential *formats* and wallet plumbing, not credential *types*. The projects page and the TAC project register enumerate SD-JWT implementations in four languages, DIDComm mediators, OpenID4VC libraries, a VC API implementation, agent frameworks and so on — none of which names a single real-world credential. Across the whole foundation, exactly one project maintains a catalogue of concrete credential types: **Multipaz** (formerly Identity Credential, contributed by Google), whose `multipaz-doctypes` and `multipaz-utopia` modules define document types with doctype identifiers, field lists and localized display names. That catalogue supplies nearly every entry below. Where a format family is all a project offers, it is recorded once at the end rather than as a credential type.

Display names below are quoted verbatim from the English string resources at `multipaz-doctypes/src/commonMain/lokalize/values/strings.json` and `multipaz-utopia/src/commonMain/lokalize/values/strings.json`; identifiers are quoted from the Kotlin sources.

**Driving license (`org.iso.18013.5.1.mDL`)**
- Asserts — a mobile driving licence per ISO/IEC 18013-5:2021; display name `"Driving license"`.
- Key fields — mdoc namespace `org.iso.18013.5.1` plus an AAMVA namespace `org.iso.18013.5.1.aamva`; attribute identifiers include `family_name`, `given_name`, `birth_date`, `administrative_number`, `age_in_years`, `age_birth_year`, and a ladder of age predicates `age_over_13`, `age_over_16`, `age_over_18`, `age_over_21`, `age_over_25`, `age_over_60`, `age_over_62`, `age_over_65`, plus `aamva_version`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/DrivingLicense.kt; also named at https://tac.openwallet.foundation/projects/ (Multipaz) and in the TAC project description at https://github.com/openwallet-foundation/tac/blob/main/docs/projects/identity-credential.md as "`org.iso.18013.5.1.mDL`: Mobile Driving License".
- Status — stated.

**Personal ID / EU PID (`eu.europa.ec.eudi.pid.1`, VCT `urn:eudi:pid:1`)**
- Asserts — EU Personal Identification Data; display name `"Personal ID"`. Defined against the EUDI PID Rulebook (annex 6 of the EU architecture and reference framework), which the source file cites directly.
- Key fields — `family_name`, `given_name`, `birthdate`, `place_of_birth`, `nationalities`, `date_of_expiry`, `issuing_authority`. Registered both as an mdoc doctype and as a JSON/SD-JWT document type (`addJsonDocumentType(type = EUPID_VCT, keyBound = true)`).
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/EUPersonalID.kt. An older doctype string, `eu.europa.ec.eudiw.pid.1`, appears in the TAC project page at https://github.com/openwallet-foundation/tac/blob/main/docs/projects/identity-credential.md as "mdoc for Personal Identification".
- Status — stated.

**Photo ID (`org.iso.23220.photoid.1`)**
- Asserts — a photo identity document per ISO/IEC 23220-4 Annex C; display name `"Photo ID"`. The source notes it is "based on ISO/IEC JTC 1/SC 17/WG 4 N 4862 from 2025-12-04".
- Key fields — three namespaces (`org.iso.23220.1`, `org.iso.23220.photoid.1`, `org.iso.23220.datagroups.1`); attributes include `family_name`, `family_name_viz` (the visual-inspection-zone variant), `given_names`, `given_name_viz`, `birth_date`, `birth_city`, `birth_state`, `birth_country`, `birthplace`, `portrait`/photo of holder, `date_of_issue`, `date_of_expiry`, `issuing_authority`, `issuing_country`, `age_in_years`, `age_birth_year`, a generated ladder of `age_over_NN` predicates, `administrative_number`, `travel_document_type`, and MRTD-style datagroups `dg1` through `dg12`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/PhotoID.kt.
- Status — stated.

**Vaccination document (`org.micov.1`)**
- Asserts — vaccination and test status; display name `"Vaccination document"`. Named attributes cover yellow fever vaccination, COVID-19 vaccination and COVID-19 test.
- Key fields — namespaces `org.micov.attestation.1` and `org.micov.vtr.1`; identifiers include `1D47_vaccinated` (yellow fever), `RA01_vaccinated`-style COVID entries, `dob`, `fn`, `gn`, `fni`, `gni` (name initials), `bd`, `bm`, `by` (birth day/month/year), `fac` (facial image), `pid_DL` and `pid_PPN` (person identifiers tied to a driving licence or passport).
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/VaccinationDocument.kt; listed on the TAC page as "`org.micov.1`: mdoc for eHealth".
- Status — stated.

**Vehicle registration (`nl.rdw.mekb.1`)**
- Asserts — registration of a vehicle; display name `"Vehicle registration"`.
- Key fields — `registration_info`, `issue_date`, `registration_holder`, `basic_vehicle_info`, `vin`.
- Issuee? — mixed: the credential is about a *vehicle*, but carries a `registration_holder`. Recorded as yes, with the subject being the vehicle and the holder named inside it.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/VehicleRegistration.kt; listed on the TAC page as "`nl.rdw.mekb.1`: mdoc for Vehicle Registration".
- Status — stated.

**Age verification (`eu.europa.ec.av.1`)**
- Asserts — age predicates only; display name `"Age verification"`. The source points to https://ageverification.dev/ for the document type.
- Key fields — `age_over_18`, `age_over_21` and a generated ladder of `age_over_NN`; request profiles distinguish a plain predicate from a zero-knowledge-proof variant (`AGE_VERIFICATION_REQUEST_AGE_OVER_18_ZKP`, `..._AGE_OVER_21_ZKP`), plus an "all data elements" request.
- Issuee? — yes, though the credential carries nothing identifying beyond the predicate.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/AgeVerification.kt.
- Status — stated.

**Aadhaar (`in.gov.uidai.aadhaar.1`)**
- Asserts — Indian Aadhaar identity as an ISO 18013-5 mdoc; the source cites the UIDAI specification at https://docs.uidai.gov.in/readme/verifiable-credential-specifications/iso-18013-5-aadhaar-mdoc-specs. The `DocumentType.Builder` name is the literal string `"Aadhaar"`.
- Key fields — `CredentialIssuingDate`, `AadhaarExpiresOn`, `AadhaarType`, enrollment date and number, `Name`, local-language name, `Dob`, gender, `Photo`, `Address` broken out into `Building`, `District` and further components, `Email`, `IsNRI` (non-resident Indian), and age predicates `AgeAbove18`, `AgeAbove50`, `AgeAbove60`, `AgeAbove75`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/Aadhaar.kt.
- Status — stated. Worth noting: the age ladder goes up to 75, unlike the driving-licence ladder, because Indian entitlements key off senior-citizen thresholds.

**Google Wallet ID pass (`com.google.wallet.idcard.1`)**
- Asserts — an identity pass as defined by Google Wallet; display name `"Google Wallet ID pass"`. The source cites https://developers.google.com/wallet/identity/verify/supported-credential-attributes#id-pass-fields.
- Key fields — defined as request profiles rather than a flat attribute list: age over 18, age over 21, ZKP variants of each, "age over 18 and portrait", "age over 21 and portrait", a mandatory-data-elements request and an all-data-elements request.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/IDPass.kt.
- Status — stated.

**Certificate of residency (`eu.europa.ec.eudi.cor.1`, VCT `https://example.eudi.ec.europa.eu/cor/1`)**
- Asserts — EU certificate of residence; display name `"Certificate of residency"`. The source is candid that "This definition is ad hoc and added to facilitate interoperability testing" and carries a TODO asking whether the document type still exists.
- Key fields — `family_name`, `given_name`, `birth_date`, `age_over_18`, `issuance_date`, `expiry_date`, `issuing_authority`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/EUCertificateOfResidence.kt.
- Status — stated, with the source's own uncertainty recorded.

**German personal ID (VCT `https://example.bmi.bund.de/credential/pid/1.0`)**
- Asserts — a German national personal ID; display name `"German personal ID"`. The source notes "For now, this is a copy of EUPersonaID [sic]".
- Key fields — as EU PID.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/GermanPersonalID.kt.
- Status — stated.

**Loyalty card (`org.multipaz.loyalty.1`)**
- Asserts — membership in a loyalty programme at a given tier; display name `"Loyalty card"`.
- Key fields — `membership_number`, `family_name`, `given_name`, `portrait`, `tier`, `issue_date`, `expiry_date`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/Loyalty.kt.
- Status — stated.

**Boarding pass (`org.multipaz.example.boarding-pass.1`)**
- Asserts — a flight boarding entitlement; display name `"Boarding pass"`. The source calls it "An example of what a boarding pass doctype could look like."
- Key fields — `passenger_name`, `flight_number`, `departure_time`, `seat_number`.
- Issuee? — yes (the passenger).
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/UtopiaBoardingPass.kt.
- Status — stated, explicitly as an illustrative document type.

**Movie ticket (VCT `https://utopia.example.com/vct/movieticket`)**
- Asserts — admission to a specific screening; display name `"Movie ticket"`.
- Key fields — `ticket_id`, `movie`, `movie_rating`, `cinema`, `theater_id`, `show_date_time`, `seat_id`, `parking_option`, `poster`.
- Issuee? — no strong subject; it is an entitlement to attend a screening, with no identifying attributes of the bearer.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/UtopiaMovieTicket.kt.
- Status — stated.

**Naturalization certificate (VCT `http://utopia.example.com/vct/naturalization`)**
- Asserts — naturalization as a citizen; the source says "Naturalization Certificate of the fictional State of Utopia". Display name `"Naturalization certificate"`.
- Key fields — `family_name`, `given_name`, `birth_date`, `naturalization_date`.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/UtopiaNaturalization.kt.
- Status — stated.

**Payment card — mdoc profile (`org.multipaz.payment.sca.1`)**
- Asserts — a card-based digital payment credential supporting Strong Customer Authentication; display name `"Payment card"`. The source flags it as "a mock credential used for testing in a closed ecosystem and is non-normative", against the EUDI technical specification TS12 on electronic payments SCA implementation with the wallet.
- Key fields — `payment_instrument_id`, `masked_account_reference`, `holder_name`, `issuer_name`, `issue_date`, `expiry_date`.
- Issuee? — yes (the cardholder).
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/DigitalPaymentCredential.kt.
- Status — stated.

**Payment card — SD-JWT profile (VCT `urn:emvco:dpc:card:1`)**
- Asserts — the EMVCo Digital Payment Credential (DPC) card profile; "Compliant with the EMVCo DPC Card Credential JSON Schema". Same display name, `"Payment card"`.
- Key fields — `Credential ID`, `Card Network`, `Last Four Digits` (verbatim display names from the source), alongside the SD-JWT profile's own structure.
- Issuee? — yes.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/DigitalPaymentCredentialSdJwt.kt.
- Status — stated. Recorded separately from the mdoc profile because the two are distinct definitions with different identifiers and fields, per the no-deduplication instruction.

**Payment transaction**
- Asserts — not a credential about a party but a *transaction* type used at presentment; `displayName = "Payment"`, defined against the EUDI technical specification TS12 on SCA implementation with the wallet.
- Key fields — not enumerated as claims in the same way; it is a transaction descriptor rather than a document type.
- Issuee? — no.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-doctypes/src/commonMain/kotlin/org/multipaz/documenttype/knowntypes/PaymentTransaction.kt.
- Status — stated, but flagged: Multipaz's registry holds "document and transaction data types", and this is the transaction half. It is not a credential and should probably be excluded from a credential-kind taxonomy.

**Ping transaction**
- Asserts — nothing; `displayName = "Ping"`, "Transaction type that round-trips some data through the presentment process for testing."
- Key fields — none meaningful.
- Issuee? — no.
- Cite — https://github.com/openwallet-foundation/multipaz/blob/main/multipaz-utopia/src/commonMain/kotlin/org/multipaz/utopia/knowntypes/PingTransaction.kt.
- Status — stated; a test fixture, recorded only for completeness.

**Peer-to-peer relationship credential (KEYRING)**
- Asserts — not stated. The OWF front page links a talk titled "KEYRING: Issuing Peer-to-Peer Relationship Credentials on top of Bifold"; the post itself gives no credential definition, no claim names and no subject, and defers to a linked Atlassian wiki page for slides.
- Key fields — not stated.
- Issuee? — unknown.
- Cite — https://openwallet.foundation/2026/05/21/keyring-issuing-peer-to-peer-relationship-credentials-on-top-of-bifold/.
- Status — inferred, and thin. The name is real and fetched; everything else about it is absent from the source. Recorded so the orchestrator knows the idea exists, not as a usable entry.

### OWF credential *formats*, recorded once because they are not credential types

These are what the rest of the foundation's projects actually enumerate, and listing them here prevents them being mistaken for types. Bifold's README states its supported "Credential Formats: Hyperledger Anoncreds, IETF SD-JWT, ISO/IEC 18013-5 mDOC, W3C VCDM 1.1/2.0 JWT/SD-JWT" (https://github.com/openwallet-foundation/bifold-wallet/blob/main/README.md). EUDIPLO's README states support for "**OID4VCI**, **OID4VP**, **SD-JWT VC**, **mDOC (ISO 18013-5)**, and **OAuth Token Status**" (https://github.com/openwallet-foundation/eudiplo/blob/main/README.md). Multipaz's README describes support "for ISO mdoc and IETF SD-JWT VC credential formats". The TAC register also lists a Lab project named "MDL Implementation In Javascript" (https://github.com/openwallet-foundation/tac/blob/main/docs/projects/index.md), whose subject is the mDL type above. Four SD-JWT reference implementations (.NET, Python, Rust, JavaScript), the VC API implementation, Credo, ACA-Py, VCX, Tuvali, the DIDComm Mediator, TRS and Wallet Framework .NET define no credential types at all.

## Notes and surprises worth the orchestrator's attention

The W3C use-cases document is at once richer and poorer than its reputation. It is rich in the User Needs section, where 27 short user stories name or imply roughly 40 distinct credentials across seven domains. It is poor in one specific place: **section 6, "Extant Use Cases", contains exactly one sentence** — "Extant Use Cases are illustrative of market adoption, i.e., examples of the use of verifiable credentials in real-world applications" — and then nothing. The section that would have listed deployed credentials is an empty stub, which is the single largest gap in the source.

The Overview note is similarly thin for this purpose. Despite being 1,345 lines, it uses exactly one credential type — `ExampleAlumniCredential` — repeated verbatim through every securing mechanism, plus the two infrastructure types. Its prose names a driver's licence, a university degree, a government passport and a marriage certificate, but only as illustrations in a sentence.

Several types here have no subject party at all, and they cluster into a recognizable group: `DisputeCredential` (subject is another credential), the GS1 `KeyCredential` (subject is a GTIN), the dive log entry (subject is an event plus a set of credentials), `JsonSchemaCredential` and `BitstringStatusListCredential` (subjects are schemas and status bitstrings), `ExampleAssertCredential` (subject is a presentation), and `RecognizedEntityCredential` (subject is a set of issuers). If arcviz's coarse kinds are drawn only from person-shaped credentials, all of these will be misfiled.

Two entitlement-shaped credentials also sit awkwardly against the rest: the first-class upgrade coupon, which the W3C document itself flags as introducing "commercial value in a verifiable credential", and Multipaz's movie ticket, which carries no attribute identifying its bearer. The dive instructor's revocable status-check token is a third oddity — a credential issued *by* an individual *to* his employer that grants a standing permission rather than asserting a fact.

Finally, the Certificate of Origin's stated subject is worth a second look before it is used: the document says "The Subject of the CO is the certificate itself". That reads as an error rather than a deliberate model, since no other credential in the document is its own subject, but it is what the source says and it has been recorded verbatim rather than corrected.

## From memory, UNVERIFIED — discard unless independently checked

Nothing in this section was fetched during this pass. It is recorded only because the brief asks that training-derived knowledge be separated rather than silently omitted, and the orchestrator should treat every line as unconfirmed.

- The 2019 edition of the VC use-cases note is widely cited and may differ in its user-story identifiers from the 18 March 2026 edition used above. If any downstream work cites `E.1`/`R.2`-style identifiers from an older copy, the mapping should be re-checked. `Status: from-memory-UNVERIFIED`.
- I believe OWF has hosted or discussed additional projects beyond those on the fetched register (a credential-format library contributed by Ping Identity, and archived projects such as Credhub), and the TAC index does list Credhub as archived, but the Credhub project page returned HTTP 404 so I could not read what credential types, if any, it defined. `Status: from-memory-UNVERIFIED`.
- I did not locate any W3C Credentials Community Group use-case document distinct from the four W3C documents above. My recollection is that the CCG maintains use-case material for education (`vc-ed`) and for DIDs (`did-use-cases`), but I did not fetch either, so neither is represented here and neither should be assumed to exist in the form I have described. `Status: from-memory-UNVERIFIED`.
