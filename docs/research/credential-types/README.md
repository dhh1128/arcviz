# The credential-type catalog

A compiled list of credential types that are realistically imagined today, drawn from eleven sources across five ecosystems. Its purpose is to be a **test set**: any scheme arcviz adopts for telling a viewer what *kind* of evidence they are looking at has to survive this list, not a handful of convenient examples. It is not a taxonomy and it deliberately proposes none — grouping below is by where a type was found, never by what kind of thing it is.

Compiled 2026-09-21. Source records with quotes and locators are in [`refs/sources.credential-types.yaml`](../../../refs/sources.credential-types.yaml); the raw per-source harvests, with a per-entry citation for every row here, are in [`sources/`](sources/).

## How to read it

**One row per type, not per appearance.** An earlier plan kept a separate row each time a source named a driver's licence; that was changed once the harvests came in, because the `Sources` column carries the same frequency signal in less space. Where two sources name the same type but disagree materially — different subject, different field set, different direction — the row says so rather than smoothing it.

**`Subject` is derived, and is the one column that is not the source's own words.** It records what the credential is *about*, read from the subject the source itself states or from the field set it declares. It is here because the sweep's most consequential finding turns on it, and it is marked as derived so nothing downstream mistakes it for evidence. Everything else — the type name, what it asserts, whether an issuee exists — comes from the source.

**`Issuee` answers a structural question, not a semantic one.** `yes` means the source declares a subject party (an ACDC `a.i`, a `credentialSubject`, a holder-bound key). It does not mean the issuee is what the credential is about — see rows 15, 92 and 208, where those come apart.

**Epistemic status.** Every row traces to a document someone on this project fetched or read; nothing here rests on a model's recollection. The harvest files mark each entry `stated` or `inferred` and carry the citation. Two known weaknesses, both recorded rather than papered over: the First Person material from Medium came through a reader proxy because medium.com returns 403 to direct fetches, so the same substance is cited to `firstperson.network/white-paper`, which fetched directly; and ISO's own text was unreachable (HTTP 403), so every ISO doctype string here is quoted from a party *using* it rather than from ISO.

**One source is private and is recorded but not reproduced.** The verifiable-IBAN material in `~/code/tti/` is internal client work in private repositories. Its publishable half — a live EU IBAN attestation obtained from the Commission's public reference issuer — is row 88 and is cited to that public endpoint. The concepts around it that exist only in the internal analysis are rows 192 to 195, recorded by name and assertion with no detail and no quotation, because this repository is public.

## Ecosystem 1 — KERI / ACDC-native

Sources: `bakobo` (`~/code/bakobo/schema`), `pschema` (`provenant-dev/public-schema`), `dossier` (the ToIP dossier specification), `vvp` (Verifiable Voice Protocol drafts), `ev-life` (`~/code/me/papers/ev-life.md`).

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 1 | `SEDI_Identity` | The state verifies and endorses exactly the statutory attribute set — name, birth date, image, residence address | person | yes | bakobo |
| 2 | `SEDI_Age` | Individually-blinded age-threshold predicates (13/16/18/21/55/65) as of a date; birth date never involved | person | yes, in the `A` aggregate | bakobo |
| 3 | `SEDI_Guardian` | A guardian holds recognized authority to act for a ward — statutory basis, powers, appointment | person (guardian); ward named by edge | yes, the guardian | bakobo |
| 4 | `SEDI_AgePortraitPresentation` | Holder-issued presentation combining an identity and an age credential for the "over 21 plus photo" pattern | the disclosure act | yes — **the issuee is the verifier**, inverting the usual direction | bakobo |
| 5 | `FaceToFaceCredential` | The issuer knows the issuee to be a human being, based on one or more face-to-face interactions | person (humanness) | yes | bakobo, pschema |
| 6 | `ProofOfControlCredential` | The issuee demonstrated the ability to control a digital resource — website, social handle, email address | person ↔ resource | yes | bakobo, pschema |
| 7 | `gcd-credential` (Generalized Cooperative Delegation) | The authorizations, duties and constraints of a delegate receiving delegated authority | delegation relationship | yes, the delegate | bakobo, pschema, vvp |
| 8 | `AwardCredential` | Confers an award on a staff member or other associated person or group | person or group | yes | bakobo, pschema |
| 9 | `ai-coder-license` | Certifies a developer is committed to and capable of using AI coding tools with appropriate guard rails | person | yes | bakobo, pschema |
| 10 | `ai-user-coca` | The issuer commits to a code of conduct for their personal use of AI | issuer (self-attestation) | declared, but the field's own description contradicts the credential's — see `F-PFK0` | bakobo, pschema |
| 11 | `orgVet` | Authenticates an org with an explicit level of assurance | legal entity | **no** — the vetted org is identified through a `lids` array, not as an issuee | bakobo, pschema |
| 12 | `citation` | Formally reference non-ACDC content — a hyperlink that carries its content's digest and type | external content | no | bakobo, pschema |
| 13 | `foreign-artifact-affidavit` / Foreign Artifact ACDC | Gives arbitrary binary data a tamper-evident cryptographic identity so it can be cited as evidence | artifact (photo, audio, PDF, genomic data) | no | bakobo, pschema, dossier |
| 14 | `DataAttestation` | Verifiable attestation of a cryptographic digest of data by the issuer | data | no | bakobo, pschema |
| 15 | `BindKeyAttestation` | The issuer uses a cryptographic key not directly managed by its KEL, making the binding provable and revocable | key | no | bakobo, pschema |
| 16 | Dossier (Base) | An issuer-curated collection of evidence; attests to the collection's composition, not the veracity of what it links | the collection | no, by design | bakobo, pschema, dossier, vvp, ev-life |
| 17 | `a2p-campaign-credential` | A brand's A2P 10DLC messaging campaign — campaign id, type, numbers, authorized service provider | campaign (held by an org) | yes | pschema |
| 18 | `AegisStdVetCredential` | Results of a standard vetting of an org, as a 0–100 score | legal entity | no | pschema |
| 19 | `BrandOwnerCredential` | A legal entity has the right to use a brand as direct owner or licensee | legal entity ↔ brand | yes | pschema |
| 20 | `TCRVettingCredential` | The Campaign Registry's vetting of a brand — legal name, address, tax id, vetting score, LEI | legal entity | yes | pschema |
| 21 | `TNAllocationCredential` | An enterprise has the right to use specific telephone numbers, from a regulator or a number provider | legal entity ↔ phone numbers | yes | pschema, vvp, dossier |
| 22 | `TelephoneNumberCredential` | A telephone number issued to a brand for A2P 10DLC campaigns (same field set as row 21) | legal entity ↔ phone numbers | yes | pschema |
| 23 | `VvpDossierCredential` | Assembles all evidence required by the Verifiable Voice Protocol; payload is in the edges, not the attributes | the collection | no | pschema |
| 24 | `LegalEntityvLEICredential` | A vLEI credential issued by a Qualified vLEI Issuer to a legal entity | legal entity | yes | pschema |
| 25 | `QualifiedvLEIIssuervLEICredential` | GLEIF authorizes a QVI to issue, verify and revoke legal-entity and OOR vLEI credentials | legal entity (as issuer) | yes | pschema, vvp |
| 26 | `LegalEntityOfficialOrganizationalRolevLEICredential` | A role credential for official representatives of a legal entity | person in an org role | yes | pschema |
| 27 | `LegalEntityEngagementContextRolevLEICredential` | A role credential for representatives in functional or other engagement contexts | person in an org role | yes | pschema |
| 28 | `OORAuthorizationvLEICredential` | A legal entity authorizes a QVI to issue OOR credentials | authorization relationship | yes | pschema |
| 29 | `ECRAuthorizationvLEICredential` | A legal entity authorizes a QVI to issue ECR credentials | authorization relationship | yes | pschema |
| 30 | `iXBRLDataAttestation` | A data attestation against an iXBRL report, linked to a vLEI OOR or ECR credential | financial report | no | pschema |
| 31 | `iXBRLDataD6Attestation` | The same under the Digital Signatures in XBRL (D6) specification | financial report | no | pschema |
| 32 | Endorsement ACDC | A candidate records a disposition (`endorse`) toward a subject SAID for a named act | **another ACDC** | no; the subject is named by SAID | dossier |
| 33 | Declination | The same ACDC with `disp: decline` — an authenticated refusal to endorse, recording attributable dissent | **another ACDC** | no | dossier |
| 34 | Bridge wrapper | "I verified this foreign credential on date X according to policy Y" — standardizes a non-ACDC credential into the trust model | **another credential**, foreign | unknown | dossier |
| 35 | Observation Attestation | A dynamic value observed at a specific time — "I observed Account X having Balance Y at Block Height Z" | an observation event | unknown | dossier |
| 36 | Qualification proof | The endorser is qualified to act on the subject — e.g. "any licensed physician in good standing" | person | unknown | dossier |
| 37 | Mortgage Creditworthiness Dossier | A borrower's qualification for a mortgage, with funds-available pinned at the moment of application | the collection | no | dossier |
| 38 | Court Case Dossier | Chain of custody for evidence moving through `Marked` → `Offered` → `Admitted` → `Stricken` | the collection | no | dossier |
| 39 | Redacted Dossier | Existence and provenance of source material without revealing the source's identity | the collection | no | dossier |
| 40 | Predicate Dossier | Eligibility or factual status proved through a ZKP edge rather than the raw evidence — e.g. `inclusion_criteria_met: true` | the collection | no | dossier |
| 41 | Open-Endorsement Dossier | A threshold of endorsements from a distributed, potentially dynamic set of qualified signers | the collection | no | dossier |
| 42 | Token (derivative) | Between `iat` and `exp`, the bearer acts under the authority of the dossier named in `evd` | bearer | no — explicitly bearer-shaped | dossier, ev-life, vvp |
| 43 | Citation (derivative / OOBI) | A resolvable identifier that lets a verifier fetch the full dossier | the dossier | no | dossier |
| 44 | Bespoke ACDC | A direct response to a specific verifier's query, as opposed to a pre-curated dossier | varies | unknown | dossier |
| 45 | Vetting credential | The formal and legal attributes of a unique legal entity, including a jurisdiction-unique legal identifier | legal entity | yes | vvp, dossier, ev-life |
| 46 | Brand credential | The issuee has the right to use a described brand, by virtue of a trademark search — brand name, logo, chatbot URL, social handle, domain | legal entity ↔ brand | yes | vvp, dossier, ev-life |
| 47 | Brand proxy credential | An outsourced provider may project the brand of an accountable party when making calls, within constraints | delegation relationship | yes | vvp |
| 48 | Delegated signer credential | Automation under an operator's control is authorized by the accountable party to originate traffic on its behalf | delegation relationship | yes | vvp |
| 49 | SHAKEN attestation credential | Telephony attestation evidence flowing into a dossier through the foreign-artifact bridge | call / originator | unknown | vvp |
| 50 | RCD / CTIA-BCID vetting credential | Rich call data or brand-identity vetting from an adjacent ecosystem, incorporated by wrapper | legal entity / brand | unknown | vvp |
| 51 | Settlement credential | Documents the relationship between a party and one or more financial clearinghouses, so the terminating provider is paid | commercial relationship | unknown | vvp, ev-life |
| 52 | AI-agent authorization credential | A party empowered an AI agent to act (make calls) on its behalf | **AI agent**, bound to a principal | unknown | vvp |
| 53 | Personhood / human-not-AI credential | The caller is a human being rather than an AI | person (humanness) | unknown | vvp, ev-life |
| 54 | Phone number credential | The right to use the phone number that will be the source of a business's calls, issued by the rangeholder | legal entity ↔ number | yes | ev-life |
| 55 | Business identity credential | The link between a business's control mechanism and its defining legal attributes in a jurisdiction | legal entity | yes | ev-life |
| 56 | X.509 certificate | Named as "generation-1" evidence, contrasted with ACDCs; no assertion content given | varies | not stated | ev-life, tti |

Recorded in the harvests but not credential types, and excluded from the test set: `Targeted credential` and `Bearer token` (classes of binding, not subject matter), Accountable Party Evidence and Delegation Evidence (named groupings of other credentials), and `forensicReport_01` / `lunarPropertyDeed` (illustrative edge labels the dossier spec uses precisely to show that a verifier cannot know what an arbitrary label means).

## Ecosystem 2 — EU digital identity (eIDAS 2 / EUDI)

Sources: `eudi-iss` (the Commission's reference issuer metadata, 27 configurations), `arf` (Architecture and Reference Framework), `rulebook` (the attestation rulebooks catalog), `tti` (private, recorded not reproduced).

Format pairs are collapsed: where the issuer advertises the same subject matter as both `mso_mdoc` and `dc+sd-jwt`, that is one row, noted. The claim sets differ between the two forms for PID, which is noted on its row rather than smoothed.

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 57 | Person Identification Data (PID) | A set of data issued under Union or national law that establishes the identity of a natural or legal person | person | yes | eudi-iss, arf, rulebook, multipaz, verifier |
| 58 | Mobile Driving Licence (mDL) | Driving privileges held by the named person, in the ISO/IEC 18013-5 doctype | person ↔ privilege | yes | eudi-iss, arf, rulebook, google, apple, multipaz, aamva |
| 59 | Photo ID | A photographic identity document per ISO/IEC 23220, with civil identity in Unicode and Latin-1 transcriptions | person | yes | eudi-iss, apple, multipaz, verifier |
| 60 | Certificate of Residence | The named person resides at a stated address in a stated country from a stated arrival date | person ↔ address | yes | eudi-iss, multipaz |
| 61 | Diploma | Educational affiliation and identity within a home organization, with an assurance level | person ↔ institution | yes | eudi-iss |
| 62 | Learning Credential | The named learner achieved a titled learning achievement, with outcomes, grade, level, study time, prerequisites | person ↔ achievement | yes | eudi-iss |
| 63 | European Health Insurance Card (EHIC) | Entitlement to healthcare under a competent institution for a stated period | person ↔ entitlement | yes | eudi-iss |
| 64 | Health ID | A health insurance and patient identifier, plus a block of `matching_*` attributes for record linkage | person | yes | eudi-iss |
| 65 | Employee ID | The named person is an employee of a named employer under a stated employment type | person ↔ employer | yes | eudi-iss |
| 66 | PDA1 (Portable Document A1) | Which member state's social security legislation applies to the holder's employment, confirmed by a competent institution | person ↔ jurisdiction | yes | eudi-iss |
| 67 | Power of Representation | The holder may represent a named legal person, with full powers or a scoped eService, for a stated period | **relation to a third party** | yes | eudi-iss |
| 68 | Seafarer certificate | The capacities the named seafarer may serve in under an STCW code, countersigned by a named issuing officer | person ↔ qualification | yes — and the only entry naming a *human signatory of the issuer* as claims | eudi-iss |
| 69 | Tax Number | The holder's tax number in an affiliation country, optionally with a church tax ID and a linked IBAN | person ↔ tax authority | yes | eudi-iss |
| 70 | Tax Residency | A taxpayer of a stated type was tax-resident for a requested period under a stated legal framework | person or entity | yes | eudi-iss |
| 71 | MSISDN | A named mobile number is contracted to and in use by the named person with a named operator | person ↔ number | yes | eudi-iss |
| 72 | Loyalty (EUDI) | The named person is a client of a named company under a client identifier | person ↔ merchant | yes | eudi-iss, multipaz |
| 73 | Reservation | A booking held by the named person with a service provider — dates, location, guests, rooms, car rental | booking | yes | eudi-iss |
| 74 | Wallet Unit Attestation (WUA) | Describes the components of a Wallet Unit, or allows authentication and validation of those components | **the wallet** | yes, but the subject is software and hardware | arf |
| 75 | Wallet Instance Attestation (WIA) | The integrity and authenticity of a Wallet Instance, with a revocation reference and solution name/version/certification | **the wallet instance** | yes | arf |
| 76 | Key Attestation (KA) | The certification and properties of a secure cryptographic device or keystore, with the public keys it holds | **a key / keystore** | yes | arf |
| 77 | Pseudonym | Data uniquely representing a User that does not by itself allow the User's attributes to be inferred | person, zero-attribute | yes | arf |
| 78 | Wallet-relying party registration certificate | The attributes a relying party has registered an intent to request from users | **the verifier** | yes — **held by the party doing the asking**, constraining what it may ask | arf |
| 79 | Basic Identification Data Attestation (BIDA) | Named as a sibling EUDI doctype; no field set published in any source fetched | person | yes | verifier |
| 80 | EU Age Verification attestation | Age predicates only — `age_over_18`, `age_over_21` and a generated ladder, with a ZKP variant | person, predicate-only | unknown; may be deliberately unlinkable | multipaz, verifier |
| 81 | Vaccination document (mICOV) | Vaccination and test status — yellow fever, COVID vaccination, COVID test — with person identifiers tied to a licence or passport | person ↔ health event | yes | multipaz, verifier |
| 82 | German personal ID | A national personal ID; the source says it is presently a copy of EU PID | person | yes | multipaz |
| 83 | Naturalization certificate | Naturalization as a citizen, with a naturalization date | person ↔ state | yes | multipaz |
| 84 | Payment card (EMVCo DPC) | A card-based digital payment credential supporting Strong Customer Authentication | person ↔ account | yes | multipaz |
| 85 | Vehicle registration | Registration of a vehicle — registration info, VIN, basic vehicle info, and a registration holder | **the vehicle**, with a holder named inside | mixed | multipaz, verifier |
| 86 | Bicycle ID card | Bicycle owner data | **the bicycle**, straddling into its owner | unknown | verifier |
| 87 | Student card | A student card from a national issuer; no field set published in any source fetched | person ↔ institution | yes | verifier |
| 88 | IBAN attestation (`urn:eu.europa.ec.eudi:iban:1`) | Binds an IBAN to a **natural** person — with currency, account status, payment possibility, co-owner and disponent flags. Carries no legal-person claim at all: no LEI, no registration number | person ↔ account | yes, holder-key-bound | eudi-iss, tti |
| 89 | Aadhaar | Indian Aadhaar identity as an mdoc, with four age-threshold predicates (18/50/60/75) and paired masked/unmasked contact fields | person | yes | google, multipaz |

Recorded but excluded from the test set: the four **legal categories** of attestation (PID, QEAA, PuB-EAA, non-qualified EAA), which the ARF is explicit are "purely legal" distinctions orthogonal to subject matter — the same diploma is a QEAA or an EAA depending on who issued it; and the **catalogue of attributes** and **catalogue of schemes**, which are registration mechanisms. Worth knowing for calibration: as fetched, the ARF's attestation catalogue contains exactly two rulebooks, PID and mDL, while the reference issuer advertises 27 configurations — the implementation is far ahead of the framework meant to catalogue it, and the ARF's own discussion paper lists the catalogue requirements for removal as outdated.

## Ecosystem 3 — W3C Verifiable Credentials

Sources: `w3c-uc` (Verifiable Credentials Use Cases, W3C Group Note of 18 March 2026 — materially newer than the widely-mirrored 2019 text), `w3c-dm2` (Data Model 2.0), `w3c-ig` (Implementation Guidelines), `w3c-ov` (Overview), `w3c-re` (Recognized Entities, an experimental editor's draft self-described as not fit for production).

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 90 | Extended / digital transcript | Course grades plus learner competencies, work experiences and non-educational marketable skills | person ↔ institution | yes | w3c-uc |
| 91 | Test result credential | The results of a test taken in an online learning system by an identified participant | person ↔ assessment | yes | w3c-uc |
| 92 | College degree credential (`ExampleDegreeCredential`) | The subject holds a named degree from a named university | person ↔ institution | yes | w3c-uc, w3c-dm2 |
| 93 | Alumni credential (`ExampleAlumniCredential`) | The subject is an alumnus of a named university | person ↔ institution | yes | w3c-dm2, w3c-ov |
| 94 | Achievement credential (`ExampleAchievementCredential`) | A named achievement with criteria narrative, shown multilingually | person ↔ achievement | yes | w3c-dm2 |
| 95 | Open badge (`OpenBadgeCredential`) / digital badge | A qualification displayable on a professional network or attached to forum posts | person ↔ achievement | yes | w3c-uc, w3c-dm2 |
| 96 | Software training credential | The subject completed specific software training | person ↔ training | yes | w3c-uc |
| 97 | Professional training certificate | The subject was trained as a named professional by a named training company | person ↔ training | yes | w3c-uc |
| 98 | Continuing education credential | Continuing-education achievements a professional board requires to maintain certification | person ↔ achievement | yes | w3c-uc |
| 99 | Board certification credential | The subject is board-certified in a medical specialty; lapse is automatically visible to verifiers | person ↔ privilege | yes | w3c-uc |
| 100 | State medical board licence | The subject is certified to practise medicine in a named state, and may write prescriptions and referrals | person ↔ privilege | yes | w3c-uc |
| 101 | Physician education credential | The subject's schooling as a medical practitioner | person ↔ institution | yes | w3c-uc |
| 102 | Aid worker certification | The subject is a certified aid worker, presentable minimally to preserve pseudonymity | person ↔ role | yes | w3c-uc |
| 103 | Organizational accreditation credential | A training organization is accredited; revoking it invalidates credentials that organization issued | **legal entity as issuer** | yes | w3c-uc |
| 104 | Dive instructor certification | Instructor-level dive certification issued by a licensed dive school, required for employment | person ↔ privilege | yes | w3c-uc |
| 105 | Specialist dive certifications (drysuit, night, search & recovery) | Specialist diver certification; private, because for personal diving rather than instructing | person ↔ privilege | yes | w3c-uc |
| 106 | Dive school affiliation certification | A named dive school is licensed by a certifying body to issue certifications in its name | **legal entity as issuer** | yes | w3c-uc |
| 107 | Signed log entry of a dive event | The roster of divers on a sanctioned dive and their certifications, signed and archived by the dive master | **an event plus a set of credentials** | no single subject party | w3c-uc |
| 108 | Revocable status-check token | A standing capability to check the current status of all of a person's certifications, not just one | **a permission** | yes, but **inverted** — the individual issues it to his employer | w3c-uc |
| 109 | Verifiable address credential (`ExampleAddressCredential`) | A postal address belonging to the subject | person ↔ address | yes | w3c-uc, w3c-ig |
| 110 | Postal-address confirmation credential | The subject receives postal mail at a certain address; a KYC input | person ↔ address | yes | w3c-uc |
| 111 | Identity credential used as proof of age | The holder is over 21, without revealing date of birth, address or state ID number | person, predicate | yes | w3c-uc |
| 112 | Age verification credential (`AgeVerificationCredential`) | The subject is over a given age; carries a refresh service and is not intended to be shared with anyone but the issuer | person, predicate | yes | w3c-dm2 |
| 113 | Chamber-of-commerce legitimacy credential | A web shop is a legitimate business | legal entity | yes | w3c-uc |
| 114 | Wholesale purchase entitlement | The subject may enter a wholesaler's warehouse and buy goods unavailable to the public; marked non-transferable | person ↔ entitlement | yes | w3c-uc |
| 115 | Bank / checking account credential | The subject has an account at a named bank, the bank verified their identity, and the KYC is reusable by other institutions | person ↔ account | yes | w3c-uc |
| 116 | Banking information credential (third-party) | The banking details of the *recipient* family, verifying the destination of a funds transfer | **a third party's account** | yes; the holder presenting it is not the subject | w3c-uc |
| 117 | National ID card credential | The subject holds a national ID card | person | yes | w3c-uc |
| 118 | Government identity certificate | The subject's identity for remote account opening or test-centre identification — address, national identity number | person | yes | w3c-uc |
| 119 | Digital passport (`PassportCredential`) | Identity and citizenship for immigration; the digital version retains a history of the places visited | person ↔ state | yes | w3c-uc |
| 120 | Digital driving licence (`ExampleDrivingLicenseCredential`) | The subject has the right to drive a car; the example carries revocation and suspension status at once | person ↔ privilege | yes | w3c-uc, w3c-dm2 |
| 121 | Self-issued driver's licence | The same content issued by the subject to themselves — verification succeeds, validation fails for a car rental but may pass at a go-cart track | person (self-asserted) | yes; issuer and subject are the same party | w3c-uc |
| 122 | Permanent resident card (`PermanentResidentCard`) | Permanent residency, with resident-since date, category and number | person ↔ state | yes | w3c-dm2 |
| 123 | Birth certificate | Birth and relationship to parents, with the mother's maiden name; the link that qualifies citizenship by parentage | person ↔ parents | yes | w3c-uc, w3c-re |
| 124 | Marriage licence / certificate | The marriage of two parties; establishes a name change | two people | yes, both | w3c-uc, w3c-re |
| 125 | Death certificate | A vital record a regional office may be recognized to issue | person | yes | w3c-re |
| 126 | Self-sovereign proof of birth | Birth, with the parents' proof of birth and marriage attached; retrievable from many places, usable by a refugee with no other documents | person ↔ parents | yes | w3c-uc |
| 127 | Permission to travel (`ChildTravelPass`) | The non-travelling parent grants permission for a minor to travel abroad with the other parent; replaces the notary | **a permitted action** | yes, the minor; issued by a private individual | w3c-uc |
| 128 | Relationship credential (`RelationshipCredential`) | Two named people are spouses; the example exists to show multiple subjects in one credential | two people | yes, two of them | w3c-dm2 |
| 129 | Government disability credential | The subject maintains legal disability status, without disclosing the specific disability | person ↔ status | yes | w3c-uc |
| 130 | Insurance coverage credential | The subject holds health insurance cover, so a clinic can submit a claim | person ↔ entitlement | yes | w3c-uc |
| 131 | Electronic prescription | A prescription for a named patient written by a named physician; carries a credential about each | person ↔ authorization | yes | w3c-uc |
| 132 | Identity profile (aggregate) | A collection of credentials assembled for a purpose — a money-transfer source-of-funds check, or airport security | the collection | yes | w3c-uc |
| 133 | Upgrade coupon (frequent flyer) | Redeemable for a first-class upgrade; the document flags it as introducing commercial value into a credential | **an entitlement**, bearer-shaped | nominally yes | w3c-uc |
| 134 | Device-identifying credential (IDevID, IAK) | The manufacturing-time identity of an IoT device, issued at the factory and verified at onboarding | **a device** | yes | w3c-uc |
| 135 | Specification-compliance certification (device) | A device complies with a specification — e.g. Energy-Star compliance — per a certification testing lab | **a device** | yes | w3c-uc |
| 136 | Evidence-of-possession credential (supply chain) | A named reseller had possession of a device, and what software was added to it | **a device's custody history** | yes | w3c-uc |
| 137 | Owner-issued device trust credential | Trust attributes for a device and which other devices it is authorized to interact with | **a device** | yes; issued by its new owner | w3c-uc |
| 138 | GS1 Prefix licence | A member organization may issue company-prefix licences within a prefix range | legal entity ↔ authority | yes | w3c-uc |
| 139 | GS1 Company Prefix licence | A company may issue identification keys within its prefix range; transferable on merger or acquisition | legal entity ↔ authority | yes | w3c-uc |
| 140 | GS1 Key credential (GTIN) | Declares the existence of a GS1 identification key; remains valid in perpetuity, long after the trade item is gone | **a product identifier** | **no** — the subject is the GTIN | w3c-uc |
| 141 | Trade item data credential | Data about the item a GTIN identifies — brand, size, ingredients, dimensions, recycling instructions | **a product** | no | w3c-uc |
| 142 | Product recall notice | A recall, linked to a GTIN key credential | **a product** | no | w3c-uc |
| 143 | Product test report | Goods meet required safety and quality standards, per a testing laboratory | **a product** | no | w3c-uc |
| 144 | Certificate of conformity | A product meets specific safety or quality standards, per a conformity assessment body | **a product** | no | w3c-re |
| 145 | Accreditation scope credential | A conformity assessment body is accredited to assess within a defined scope | legal entity | yes | w3c-re |
| 146 | Certificate of Origin | The origin of exported goods, for tariff exemptions and trade-agreement compliance; progressively redacted downstream | the document states **the certificate itself** — flagged as probable editing error | unclear | w3c-uc |
| 147 | Bill of lading | Issued by a shipping company to the exporter for claiming goods in the importing country | a shipment | unknown | w3c-uc |
| 148 | Commercial invoice / exporter's invoice | The commercial terms of an export sale; roughly five billion are exchanged annually among ~50 million trading entities | **a transaction** | no | w3c-uc, w3c-re |
| 149 | Dispute credential (`DisputeCredential`) | A specific other credential is disputed — by its subject, or by a third party alleging an imposter | **another credential** | no | w3c-ig |
| 150 | Assert credential (`ExampleAssertCredential`) | A self-asserted claim *about a verifiable presentation* — "this VP is submitted as evidence of a legal right to drive" | **a presentation** | no | w3c-dm2 |
| 151 | JSON schema credential (`JsonSchemaCredential`) | A JSON Schema against which other credentials are validated | **a schema** | no | w3c-ov |
| 152 | Bitstring status list credential | The revocation and suspension status of a large set of credentials, as a compressed bitstring | **a set of credential statuses** | no | w3c-ov, w3c-uc |
| 153 | Recognized entity credential (`RecognizedEntityCredential`) | The issuer knows of entities recognized to perform specific actions — issuing or verifying a credential type; chains through `recognizedIn` | **a set of issuers** — a trust registry as a credential | yes, often many orgs at once | w3c-re |
| 154 | Food preference credential (`ExampleFoodPreferenceCredential`) | A self-asserted preference, with issuer and holder the same DID and no subject id at all | person (self-asserted) | no | w3c-dm2 |

Excluded from the test set as syntax fixtures or templates rather than credentials: `ExampleMatrixCredential` (a nested-array demonstration with no semantic content) and `MyPrototypeCredential` (a placeholder the specification tells developers to rename). Worth recording about the source itself: section 6 of the use-cases Note, "Extant Use Cases" — the section that would have listed actually-deployed credentials — is a one-sentence stub, so the document that looks most authoritative on real-world adoption contributes nothing on it.

## Ecosystem 4 — Consumer wallets and passes

Sources: `apple` (PassKit and Apple Wallet), `google` (Google Wallet API and identity documentation), `multipaz` (the one OpenWallet Foundation project that maintains a type catalogue), `aamva`.

Two unrelated type systems run through this ecosystem, and the distinction is the sources' own. A **pass style or class** is a presentation template with free-form issuer text and no claim vocabulary; a **doctype** is a reverse-DNS identifier with standardized namespaced elements. Treating `eventTicket` and `org.iso.18013.5.1.mDL` as peers conflates them. Doctypes appear above in ecosystems 2 and 3; pass types are here.

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 155 | `boardingPass` / `flightobject` | Transit for a single trip with a specific start and end point | a journey | unknown — the format defines no holder field | apple, google |
| 156 | `eventTicket` / `eventticketobject` | Entry to a specific event, or several under a season ticket | an event admission | unknown | apple, google |
| 157 | `coupon` / `offerobject` | A discount or special offer, updatable with a new offer and expiration | **an offer** | no | apple, google |
| 158 | `storeCard` / `loyaltyobject` | An account the holder has with a company, usable for payment or discount, possibly carrying a balance | person ↔ account | yes | apple, google |
| 159 | `generic` / `genericobject` | Anything not fitting a more specific style — gym cards, coat-check tickets, metro passes with a balance | residual | unknown | apple, google |
| 160 | `giftcardobject` | A gift card | **a stored value** | unknown | google |
| 161 | `transitobject` | A transit ticket, replacing paper and reducing fraud | a journey or period | unknown | google |
| 162 | Season pass | A standing entitlement across a season | an entitlement | unknown | google |
| 163 | Utility bill | A bill, carried in a wallet as a pass | **a transaction/statement** | unknown | google |
| 164 | Parking pass | An entitlement to park | an entitlement | unknown | google |
| 165 | Voucher | A redeemable value | **a redeemable claim** | unknown | google |
| 166 | Gym membership | Membership of a gym | person ↔ organization | unknown | google, apple |
| 167 | Library membership | Membership of a library | person ↔ organization | unknown | google |
| 168 | Reservation (pass) | A held booking | a booking | unknown | google |
| 169 | Auto insurance card | Proof of motor insurance | person ↔ policy | unknown | google |
| 170 | Home insurance card | Proof of home insurance | person ↔ policy | unknown | google |
| 171 | Entry ticket | Admission to a venue | an admission | unknown | google |
| 172 | Receipt | Evidence of a completed purchase | **a transaction** | unknown | google |
| 173 | Driver's licence / state ID in Apple Wallet | A state-issued licence or ID card, added by scanning the physical credential plus a live selfie; "not a replacement for a physical ID" | person ↔ privilege | yes | apple |
| 174 | Digital ID (Apple) | An Apple-issued credential **derived from** a government passport — "not itself a government-issued passport", unusable for border crossing | person | yes; **the wallet issuer is not the source document's issuer** | apple |
| 175 | Google Wallet ID pass (`com.google.wallet.idcard.1`) | A vendor-minted identity doctype that borrows the ISO mDL namespace for its attributes, with `original_document_issue_date` distinct from `issue_date` | person | yes; same derived-credential shape as row 174 | google, multipaz |
| 176 | My Number Card (Japan) | Mobile identity combined with Japan Public Key Infrastructure functionality | person | yes; carries a signing PKI rather than only attributes | apple |
| 177 | Digital car key | Authority to unlock and start a specific vehicle | **a capability over a thing** | unknown | apple, google |
| 178 | Home key | Authority to unlock a residence | **a capability over a thing** | unknown | apple |
| 179 | Hotel key | Authority to unlock a hotel room for a stay | **a capability over a thing** | unknown | apple, google |
| 180 | Campus / student ID | Campus access and payment | person ↔ institution | unknown | apple, google |
| 181 | Corporate badge | Office or facility access | person ↔ employer | unknown | apple, google |
| 182 | Theme-park pass | Admission and entitlements within a park | an entitlement | unknown | apple |
| 183 | Payment card (wallet) | A credit or debit card provisioned into a wallet | person ↔ account | unknown | apple, google |
| 184 | Transit card (stored value) | A transit account, tapped at a gate | person ↔ account | unknown | apple, google |
| 185 | Order tracking | Merchant and tracking details from an order confirmation | **a transaction** | unknown | apple |
| 186 | Movie ticket | Admission to a specific screening — cinema, theatre, seat, show time | an admission, with **no identifying attribute of the bearer** | no | multipaz |
| 187 | Health insurance card | Health cover carried as a pass | person ↔ policy | unknown | google |
| 188 | Test record / COVID card | A test result or vaccination record carried as a pass | person ↔ health event | unknown | google |

The `GenericType` enum (rows 162–172) is the single richest ready-made list of coarse kinds either wallet publishes, and its membership is the finding: a utility bill, a receipt, a reservation and an insurance card sit in one enumeration beside a gym membership. Google's own type system does not separate proof of a relationship, proof of a transaction and proof of an entitlement.

**The type identifier itself is not stable, which matters if a renderer keys anything off it.** The photo-ID doctype has three spellings in circulation and nothing adjudicates between them: Apple's documentation names none at all, an open-source verifier writes `org.iso.23220.photoid.1`, and the EU reference issuer's metadata writes `org.iso.23220.2.photoid.1` — while using `org.iso.23220.photoid.1`, without the `.2`, as the namespace for that same entry's claim paths. ISO's pages return HTTP 403 and the standard is sold, so the registry that would settle it is unreachable. Row 57 has the same problem from the other direction: one credential, two type identifiers, chosen by serialization format — `eu.europa.ec.eudi.pid.1` as an mdoc doctype and `urn:eudi:pid:1` as an SD-JWT VC type. And in the KERI corpus, `credentialType` is not a unique key: two distinct schemas with different SAIDs in `provenant-dev/public-schema` reuse the strings `BrandOwnerCredential` and `orgVet`. Whatever carries kind to a viewer, it cannot be the type string.

## Ecosystem 5 — Personhood and AI agents

Source: `fpp` (the First Person Project's white-paper page, and a Medium article retrieved through a reader proxy).

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 189 | Personhood credential (PHC) | Issued by any qualified entity that can attest the holder is "a real unique person **within that ecosystem**" — uniqueness scoped to a community, not global | person (humanness + uniqueness) | yes | fpp |
| 190 | Verifiable relationship credential (VRC) | Issued peer-to-peer between holders of personhood credentials, attesting a first-person trust relationship | **a relationship between two people** | yes; both parties must already hold a PHC | fpp |
| 191 | First Person Certified AI agent | Binds a personal AI agent to the human who delegates to it — the answer to "who does this agent work for" | **an AI agent** | yes, and explicitly not human | fpp |

## Addendum — types recorded by name only

These are real proposals from the financial-instrument literature that reached this catalog through material that cannot be reproduced here. They are in the test set because a classifier has to handle them; they carry no quotation and no detail, and anyone building on them should go to the named primary source rather than to this row.

| # | Type | Asserts | Subject *(derived)* | Issuee | Sources |
|---|---|---|---|---|---|
| 192 | Name-to-IBAN credential | An IBAN belongs to a named **legal** person — the conventional framing of a "verifiable IBAN", and the one the internal analysis argues against as adding little beyond existing verification-of-payee | legal entity ↔ account | unknown | tti |
| 193 | Beneficial-ownership attestation | The beneficial owners of a legal entity, attested against a state register at a threshold (10% in the proposal) | legal entity ↔ owners | unknown | tti |
| 194 | Supervisory licence attestation (bank licence, fit-and-proper) | A bank's licence and its officers' fit-and-proper standing, attested by its supervisor and terminating in a CA that supervisor already operates | legal entity ↔ regulator | unknown | tti |
| 195 | PSD2 qualified certificate (ETSI TS 119 495) | A competent authority's identifier, a payment institution's authorisation number and its licensed roles, with a national revocation path | legal entity ↔ regulator | yes | tti |

Row 195 is worth more than its size: it is a production, EU-wide instance of a credential outliving the fact it asserts. There is no obligation on national authorities to revoke the certificate when a provider's role is withdrawn, so holding a valid qualified certificate does not establish that the entity is still regulated. Any rendering that treats "signature valid, not expired, not revoked" as "the claim holds" is wrong about this credential specifically, and it is not a hypothetical.

## What this corpus is thin on, and where it is thick

**Thick:** identity documents about a natural person. Counting rows, roughly a third of the catalog asserts civil identity attributes about a person, and the ecosystems converge on nearly the same field set — the mDL, PID, Photo ID, Aadhaar and SEDI identity credentials differ more in namespace than in substance. A classifier that only had to distinguish identity documents from each other would have plenty of material and would be solving the wrong problem.

**Thin:** anything asserting something about a **legal person** in a consumer wallet. The EU IBAN attestation binds an account to a *natural* person and carries no LEI, no registration number, nothing corporate (row 88). Organizational credentials exist in quantity only in the KERI/ACDC ecosystem, and there they dominate.

**Absent from most sources, present in a few:** proof of humanness. It arrives from three unrelated directions — a face-to-face attestation, a personhood credential with ecosystem-scoped uniqueness, and a telephony "human not AI" credential — and no source treats it as a settled kind.

**The stress cases, which are the reason this list exists.** Counting rows whose subject is not a party at all gives a substantial minority: another credential (32, 33, 34, 149), a presentation (150), a schema (151), a status list (152), a set of issuers (153), a product or product identifier (140–144), a device (134–137), a vehicle or bicycle (85, 86), an event (107), a transaction (148, 163, 172, 185), a wallet or key (74–76, 15), and a verifier (78). Two further rows invert the direction of issuance — a presentation whose issuee is the verifier (4) and a status-check capability an individual issues to his employer (108). Any scheme that asks first "what does this assert about its issuee" has no answer for a quarter of this catalog.

## Sources

Full records with quotes and locators are in [`refs/sources.credential-types.yaml`](../../../refs/sources.credential-types.yaml). The per-source harvests, each carrying a citation per row above, are:

| File | Covers |
|---|---|
| [`sources/keri-vvp.md`](sources/keri-vvp.md) | `~/code/me/papers/ev-life.md`, the `vvp` repo and its archived drafts, `kswg-dossier-specification`, `~/code/bakobo/schema` |
| [`sources/provenant-tti.md`](sources/provenant-tti.md) | `provenant-dev/public-schema` (29 schemas), and the verifiable-IBAN sweep, redacted |
| [`sources/w3c-owf.md`](sources/w3c-owf.md) | W3C use cases, Data Model 2.0, Implementation Guidelines, Overview, Recognized Entities; the OpenWallet Foundation and Multipaz |
| [`sources/eudi-firstperson.md`](sources/eudi-firstperson.md) | `issuer.eudiw.dev` metadata, the EUDI ARF, the First Person Project |
| [`sources/wallets.md`](sources/wallets.md) | Apple Wallet and PassKit, Google Wallet, ISO mdoc doctypes, AAMVA |

Two sources named in the original brief produced nothing and the negative result is worth keeping: the OpenWallet Foundation publishes no use-case page and no credential-type catalogue outside Multipaz, and ISO's own standard pages are unreachable without payment, so every ISO doctype string in this catalog is quoted from a party using it rather than from ISO.
