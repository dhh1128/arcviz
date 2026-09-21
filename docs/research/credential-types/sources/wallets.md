# Wallet-carried credential types — Apple Wallet, Google Wallet, ISO mdoc doctypes

Retrieved 2026-09-21. Wallet support lists change often; every jurisdiction/availability claim below is as of that date and from the cited page only.

Scope note: this file records *types as the sources name them*. It proposes no categories. Where a source does not state something, the field says `not stated`; where a judgement was made from the source's own text, `Status` says `inferred` and gives the reason. No Apple or Google image, screenshot or code excerpt is stored here — URLs and extracted text only.

An important shape distinction runs through the whole file, and it is the sources' own, not mine: Apple and Google both operate **two unrelated type systems**. One is a *pass* system (PassKit pass styles; Google Wallet pass classes) whose "types" are presentation templates with free-form issuer-defined text fields and no standardized claim vocabulary. The other is an *identity document* system (mdoc/ISO 18013-5) whose types are reverse-DNS doctypes with standardized, namespaced data elements. A pass style says nothing about what is asserted; a doctype says quite a lot.

---

## Apple Wallet

### A1. PassKit pass styles

These are the five styles defined by the `pass.json` format. The archive guide is explicit that the set is closed: "Unlike pass type identifiers, which you define, pass styles are part of the API, as is their meaning — you can't change them or add new ones."

All five share the same field-group structure and none of them defines semantic claim names — an issuer puts arbitrary labelled key/value pairs into the groups. So "Key fields" below is the structural field set, identical across styles, and the *semantic* answer is `not stated` for every one of them.

Shared field groups (all styles): `headerFields`, `primaryFields`, `secondaryFields`, `auxiliaryFields`, `backFields`. Shared top-level pass keys: `description`, `formatVersion`, `organizationName`, `passTypeIdentifier`, `serialNumber`, `teamIdentifier`, plus optional `barcodes` (`barcode` deprecated), `locations`, `beacons`, `relevantDates` (`relevantDate` deprecated), `maxDistance`, `webServiceURL`, `authenticationToken`, `appLaunchURL`, `associatedStoreIdentifiers`, `userInfo`, `voided`, `sharingProhibited`, `backgroundColor`, `foregroundColor`, `labelColor`, `logoText`, `footerBackgroundColor`.

- **Name** — `boardingPass`
  - **Asserts** — "appropriate for passes used with transit systems such as train tickets, airline boarding passes, and other types of transit. Typically, each pass corresponds to a single trip with a specific starting and ending point."
  - **Key fields** — shared field groups above, plus a required `transitType` key. The archive page names `PKTransitTypeAir` but does not enumerate the full set on that page; the Apple Developer JSON reference names airline/transit contact URLs (`transitProviderEmail`, `contactVenueEmail`, `contactVenuePhoneNumber` and siblings) as pass-specific optional keys.
  - **Issuee?** — `unknown`
  - **Cite** — https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html §"Pass Styles"; https://developer.apple.com/documentation/walletpasses/pass (fetched as https://developer.apple.com/tutorials/data/documentation/walletpasses/pass.json)
  - **Status** — `stated` for the style and abstract. `Issuee?` is `unknown` because the format defines no holder field; a passenger name is conventional but the spec does not require or name one.

- **Name** — `coupon`
  - **Asserts** — "appropriate for coupons, special offers, and other discounts. If an offer has expired, the coupon can be updated with a new offer and expiration date."
  - **Key fields** — shared field groups above; no style-specific keys named.
  - **Issuee?** — `no`
  - **Cite** — https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html §"Pass Styles"
  - **Status** — `stated` for the abstract; `Issuee?` `no` is `inferred` — the description frames the pass around an offer, not a person, and no holder field exists.

- **Name** — `eventTicket`
  - **Asserts** — "appropriate for passes used to gain entry to an event like a concert, a movie, a play, or a sporting event. Typically, each pass corresponds to a specific event, but you can also use a single pass for several events as in a season ticket."
  - **Key fields** — shared field groups above; the JSON reference names event-related contact keys (`contactVenueEmail`, `contactVenuePhoneNumber`) among pass-specific optional URLs.
  - **Issuee?** — `unknown`
  - **Cite** — https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html §"Pass Styles"
  - **Status** — `stated`; `Issuee?` `unknown` for the same reason as `boardingPass`.

- **Name** — `storeCard`
  - **Asserts** — "appropriate for store loyalty cards, discount cards, points cards, and gift cards. Typically, a store identifies an account the user has with your company that can be used to make payments or receive discounts. When the account carries a balance, show the current balance on the pass."
  - **Key fields** — shared field groups above; no style-specific keys named.
  - **Issuee?** — `yes`
  - **Cite** — https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html §"Pass Styles"
  - **Status** — `stated` for the abstract; `Issuee?` `yes` is `inferred` from "a store identifies an account the user has with your company" — an account is subject-bound — though the format still names no holder field.

- **Name** — `generic`
  - **Asserts** — "appropriate for any pass that doesn't fit into one of the other more specific styles—for example, gym membership cards, coat-check claim tickets, and metro passes that carry a balance."
  - **Key fields** — shared field groups above; no style-specific keys named.
  - **Issuee?** — `unknown`
  - **Cite** — https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/PassKit_PG/Creating.html §"Pass Styles"
  - **Status** — `stated`. Explicitly the residual category, so nothing about it constrains the subject.

### A2. Identity documents in Apple Wallet (product-level)

- **Name** — "Driver's License and ID Cards" / driver's license and state ID
  - **Asserts** — a state-issued driver's license or state identification card, added by scanning the front and back of the physical credential plus a Live Photo/selfie. Apple states it is "not a replacement for a physical ID."
  - **Key fields** — `not stated` on the support/security pages; the machine-readable answer is the `org.iso.18013.5.1` element set requestable via `PKIdentityDriversLicenseDescriptor` (see A3).
  - **Issuee?** — `yes`
  - **Cite** — https://support.apple.com/guide/security/ids-in-apple-wallet-secc50cff810/web (Apple Platform Security, "IDs in Apple Wallet"); https://support.apple.com/en-us/111803 ("Add your driver's license to Apple Wallet")
  - **Status** — `stated`. The security guide states transmission "follows the ISO/IEC 18013-5 standard."

- **Name** — "Digital ID"
  - **Asserts** — an Apple-issued ID credential derived from a government-issued, ICAO-compliant U.S. passport, created by scanning the passport's machine-readable zone and reading its chip. Apple states it "is derived from your government-issued passport but is not itself a government-issued passport, and can't be used for international travel or border crossing."
  - **Key fields** — the ISO 23220_1 element set requestable via `PKIdentityPhotoIDDescriptor` (see A3).
  - **Issuee?** — `yes`
  - **Cite** — https://support.apple.com/en-us/123719 ("Use your Digital ID in Apple Wallet"); https://support.apple.com/guide/security/ids-in-apple-wallet-secc50cff810/web; https://developer.apple.com/documentation/passkit/pkidentityphotoiddescriptor
  - **Status** — `stated`. The security guide names "ICAO 9303 specified protocols" for the passport chip read. Interesting as a corpus case: the issuer of the wallet credential (Apple) is not the issuer of the source document (the State Department), and Apple says so.

- **Name** — Japanese My Number Card
  - **Asserts** — "combining mobile identity and Japan Public Key Infrastructure functionality," supported on iPhone with iOS 18.5 or later.
  - **Key fields** — `not stated`
  - **Issuee?** — `yes`
  - **Cite** — https://support.apple.com/guide/security/ids-in-apple-wallet-secc50cff810/web
  - **Status** — `stated`. Notable as the one non-US national ID card named in Apple's security guide, and as a credential that carries a signing PKI rather than only attributes.

Jurisdiction coverage is deliberately not enumerated here. Apple's own support pages did not return a canonical state list on this retrieval, and the secondary tech-press counts that searches surfaced disagree with each other (14 states plus Puerto Rico in one August 2026 report, 15 in another, 12 in an Apple-hosted figure). Treat any count as stale on sight.

### A3. PassKit identity request descriptors (what a verifier may ask for)

`PKIdentityDocumentDescriptor` is "a type that describes the structure and behavior of an identity document." Its conforming types are the closest thing Apple publishes to a credential-type enumeration on the verifier side.

- **Name** — `PKIdentityDriversLicenseDescriptor`
  - **Asserts** — "An object for requesting information from a user's driver's license or equivalent document."
  - **Key fields** — maps `PKIdentityElement` names onto ISO namespace `org.iso.18013.5.1` elements: `given_name`, `family_name`, `portrait`, `resident_address`, `resident_city`, `resident_country`, `resident_postal_code`, `issuing_authority`, `issuing_jurisdiction`, `issuing_country`, `un_distinguishing_sign`, `expiry_date`, `document_issue_date`, `document_number`, `driving_privileges`, `age_in_years`, `birth_date`, `age_over_XX`; and onto AAMVA namespace `org.iso.18013.5.1.aamva`: `given_name_truncation`, `aka_given_name`, `name_suffix`, `aka_suffix`, `family_name_truncation`, `aka_family_name`, `domestic_driving_privileges`.
  - **Issuee?** — `yes`
  - **Cite** — https://developer.apple.com/documentation/passkit/pkidentitydriverslicensedescriptor (fetched as https://developer.apple.com/tutorials/data/documentation/passkit/pkidentitydriverslicensedescriptor.json)
  - **Status** — `stated`.

- **Name** — `PKIdentityPhotoIDDescriptor`
  - **Asserts** — "An object you use to request information from a user's photo ID or equivalent document."
  - **Key fields** — maps onto the ISO 23220_1 namespace: `family_name_unicode`, `family_name_latin1`, `given_name_unicode`, `given_name_latin1`, `portrait` ("Portrait data as specified in ISO/IEC 18013-2:2020"), `resident_address_unicode`, `resident_city_unicode`, `resident_city_latin1`, `resident_postal_code`, `resident_country`, `issuing_authority_unicode`, `issuing_subdivision`, `issuing_country`, `issue_date`, `expiry_date`, `document_number`, `sex_unicode` ("Sex per ISO/IEC 5218"), `birth_date_unicode`, `age_in_years`, `age_over_NN`.
  - **Issuee?** — `yes`
  - **Cite** — https://developer.apple.com/documentation/passkit/pkidentityphotoiddescriptor (fetched as the `.json` route above). **CORRECTED 2026-09-21 on independent re-fetch — this file originally said "the page names the doctype `org.iso.23220.photoID.1`", and it does not.** The fetched document contains the phrase `ISO 23220_1 namespace` and no reverse-DNS doctype string anywhere, so Apple must not be cited for that identifier; see the correction note at the foot of this file. The page does state the class is used for "a digital ID in Wallet, which is an Apple-issued ID credential based on government-issued ICAO-compliant passport." Availability iOS 26.0+.
  - **Status** — `stated`.

- **Name** — `PKIdentityNationalIDCardDescriptor`
  - **Asserts** — "An object for requesting information from a user's national ID card."
  - **Key fields** — `not stated` (the page documents only a `region` / `regionCode` property for selecting the region associated with the ID). No doctype string is given.
  - **Issuee?** — `yes`
  - **Cite** — https://developer.apple.com/documentation/passkit/pkidentitynationalidcarddescriptor
  - **Status** — `stated` for the abstract; the absence of an element table is itself the finding — national ID content is region-dependent and Apple does not publish a common schema for it. Availability iOS 18.0+, and building requires "a special entitlement from Apple."

- **Name** — `PKIdentityAnyOfDescriptor`
  - **Asserts** — "An object you use to request information from multiple identity documents."
  - **Key fields** — `not stated`
  - **Issuee?** — `unknown`
  - **Cite** — https://developer.apple.com/documentation/passkit/pkidentitydocumentdescriptor §"Conforming Types"
  - **Status** — `stated`. Not a credential type; it is a disjunction over types. Recorded because a type enumeration that includes an "any of these" member tells you the verifier-side model expects substitutable credentials.

The `PKIdentityElement` type enumerates the requestable elements independent of document type: `address`, `dateOfBirth`, `dhsTemporaryLawfulStatus`, `documentDHSComplianceStatus`, `documentIssueDate`, `documentExpirationDate`, `documentNumber`, `drivingPrivileges`, `eyeColor`, `familyName`, `givenName`, `hairColor`, `height`, `issuingAuthority`, `name`, `nationality`, `organDonorStatus`, `placeOfBirth`, `portrait`, `sex`, `signatureUsualMark`, `weight`, `veteranStatus`, `age`, `age(atLeast:)`. Cite: https://developer.apple.com/documentation/passkit/pkidentityelement. Status: `stated`. `age(atLeast:)` is worth noting — a predicate rather than an attribute.

### A4. Other item categories Apple names for Wallet (marketing page, not an API enumeration)

These have no PassKit pass style and are not identity documents; they are separate Wallet features. Recorded because they are credential-shaped things a wallet carries.

Payment cards ("credit and debit cards"); transit cards (Express Transit); student ID (campus access and payment); employee badge (office/facility access); theme-park passes (named example: Disney MagicMobile); home keys; hotel keys; car key; loyalty/rewards cards; order tracking ("merchant and tracking details from your eligible order confirmations"); Apple Cash. **Asserts**: `not stated` in credential terms — the page describes each by use, not by claim. **Key fields**: `not stated`. **Issuee?**: `unknown` for all. **Cite**: https://www.apple.com/wallet/. **Status**: `stated` that Wallet holds these; everything about their internal structure is `not stated`.

---

## Google Wallet

### G1. Pass verticals (product taxonomy)

The Google Wallet developer landing page groups supported pass types into categories. Names verbatim, `Asserts`/`Key fields` `not stated` at this level, `Issuee?` `unknown` throughout, all `stated`, all cited to https://developers.google.com/wallet:

- Access: Digital Car Keys, Campus IDs, Corporate Badges, Hotel Keys, Multi-family Keys
- Health: Health Insurance Cards, Test Records, COVID Cards
- Identity: Digital Credentials
- Retail: Gift Cards, Loyalty Cards, Offers, In-store payments
- Tickets and Transit: Boarding Passes, Event Tickets, Closed Loop Transit Passes, Open Loop Transit Passes, Transit Passes
- Generic: Generic pass, Generic private pass

The page describes the generic option as covering use cases outside the predefined types, "such as gym memberships to library cards, insurance cards to parking passes."

### G2. Google Wallet API pass classes (the actual type system, v1 REST)

Seven class/object pairs. A *class* is the issuer's template; an *object* is the instance held by one user. As with PassKit, the content is issuer-defined text/image modules rather than a standardized claim vocabulary — so "Key fields" for all seven is the shared module set, and the semantic answer is `not stated`.

Shared object structure (documented on `genericobject`, and the module types recur across verticals): `id`, `classId`, `state`, `barcode`, `rotatingBarcode`, `smartTapRedemptionValue`, `validTimeInterval`, `imageModulesData[]`, `textModulesData[]`, `linksModuleData`, `appLinkData`, `groupingInfo`, `messages[]`, `passConstraints`, `notifications`, `saveRestrictions`, `valueAddedModuleData[]`, `linkedObjectIds[]`, `merchantLocations[]`, `heroImage`, `logo`, `wideLogo`, `hexBackgroundColor`, `hasUsers`.

- **Name** — `eventticketclass` / `eventticketobject`. **Asserts** — event ticket passes. **Key fields** — shared module set. **Issuee?** — `unknown`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated` (name and resource); the abstract on the index page is a one-liner, so the assertion semantics are `inferred` from the resource name.
- **Name** — `flightclass` / `flightobject`. **Asserts** — boarding pass data. **Key fields** — shared module set. **Issuee?** — `unknown`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated`. Worth flagging for the corpus: Google's boarding-pass resource is named `flight`, not `boardingPass` as Apple's is — same real-world credential, different type name.
- **Name** — `genericclass` / `genericobject`. **Asserts** — "Create your own unique pass experiences in Google Wallet." **Key fields** — shared module set plus `cardTitle` (required), `header` (required), `subheader`, `genericType`. **Issuee?** — `unknown`. **Cite** — https://developers.google.com/wallet/reference/rest/v1/genericobject, https://developers.google.com/wallet/reference/rest/v1/genericclass. **Status** — `stated`.
- **Name** — `giftcardclass` / `giftcardobject`. **Asserts** — gift card passes. **Key fields** — shared module set. **Issuee?** — `unknown`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated` (name); assertion `inferred` from the resource name.
- **Name** — `loyaltyclass` / `loyaltyobject`. **Asserts** — loyalty program passes; "Access rewards and purchase history." **Key fields** — shared module set. **Issuee?** — `yes`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated` for the quoted phrase; `Issuee?` `yes` is `inferred` — a purchase history is account-bound.
- **Name** — `offerclass` / `offerobject`. **Asserts** — "Add offers from your web site or app." **Key fields** — shared module set. **Issuee?** — `no`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated` for the phrase; `Issuee?` `no` is `inferred` — an offer is about a discount, not a person.
- **Name** — `transitclass` / `transitobject`. **Asserts** — "Replace paper tickets and reduce fraud." **Key fields** — shared module set; `media` resource exists to "Download and upload rotating barcode values for transit objects." **Issuee?** — `unknown`. **Cite** — https://developers.google.com/wallet/reference/rest. **Status** — `stated`.

Non-pass administrative resources on the same API, recorded for completeness: `issuer`, `jwt`, `permissions` ("Returns the permissions for the given issuer id"), `smarttap` ("Enable pass redemption via NFC tap"), `media`. Cite: https://developers.google.com/wallet/reference/rest. Status: `stated`.

### G3. `GenericType` enum (subtypes of the generic pass)

Verbatim values with Google's own glosses. All `Issuee?` `unknown`, all `stated`, all cited to https://developers.google.com/wallet/reference/rest/v1/genericobject §GenericType.

`GENERIC_TYPE_UNSPECIFIED` (unspecified); `GENERIC_SEASON_PASS`; `GENERIC_UTILITY_BILLS`; `GENERIC_PARKING_PASS`; `GENERIC_VOUCHER`; `GENERIC_GYM_MEMBERSHIP` (gym membership cards); `GENERIC_LIBRARY_MEMBERSHIP` (library membership cards); `GENERIC_RESERVATIONS`; `GENERIC_AUTO_INSURANCE` (auto-insurance cards); `GENERIC_HOME_INSURANCE` (home-insurance cards); `GENERIC_ENTRY_TICKET`; `GENERIC_RECEIPT`; `GENERIC_LOYALTY_CARD` (loyalty cards — the docs note the dedicated loyalty type is recommended instead); `GENERIC_OTHER`.

This enum is the single richest ready-made list of "coarse kinds" either wallet publishes, and its membership is revealing: a utility bill, a receipt, a reservation and an insurance card sit in the same enumeration as a gym membership. Google's own type system does not separate *proof of a relationship*, *proof of a transaction* and *proof of an entitlement*.

### G4. Digital identity credentials in Google Wallet (doctypes)

Google's "Supported attributes for credentials in Google Wallet" page documents exactly three credential doctypes.

- **Name** — `org.iso.18013.5.1.mDL` (mDL)
  - **Asserts** — a mobile driving licence per ISO/IEC 18013-5.
  - **Key fields** — namespace `org.iso.18013.5.1`: `family_name`, `given_name`, `birth_date`, `issue_date`, `expiry_date`, `issuing_country`, `issuing_authority`, `document_number`, `portrait`, `administrative_number`, `sex`, `height`, `weight`, `eye_colour`, `hair_colour`, `birth_place`, `resident_address`, `portrait_capture_date`, `age_in_years`, `age_birth_year`, `age_over_NN`, `issuing_jurisdiction`, `nationality`, `resident_city`, `resident_state`, `resident_postal_code`, `resident_country`, `biometric_template_xx`, `family_name_national_character`, `given_name_national_character`, `signature_usual_mark`, `driving_privileges`, `un_distinguishing_sign`. Namespace `org.iso.18013.5.1.aamva`: `organ_donor`, `DHS_compliance`, `given_name_truncation`, `family_name_truncation`, `domestic_driving_privileges`, `EDL_credential`, `veteran`.
  - **Issuee?** — `yes`
  - **Cite** — https://developers.google.com/wallet/identity/verify/supported-credential-attributes
  - **Status** — `stated`.

- **Name** — `com.google.wallet.idcard.1` (ID pass)
  - **Asserts** — an ID pass in Google Wallet. Google defines this doctype itself (the reverse-DNS prefix is `com.google`, not `org.iso`).
  - **Key fields** — namespace `org.iso.18013.5.1`: `family_name`, `given_name`, `birth_date`, `issue_date`, `expiry_date`, `issuing_country`, `issuing_authority`, `document_number`, `portrait`, `sex`, `age_over_18`, `age_over_21`, `nationality`, `original_document_issue_date`.
  - **Issuee?** — `yes`
  - **Cite** — https://developers.google.com/wallet/identity/verify/supported-credential-attributes; also named in the DCQL examples at https://developers.google.com/wallet/identity/verify/accepting-ids-from-wallet-online
  - **Status** — `stated`. Two things stand out. It is a vendor-minted doctype that borrows the ISO mDL *namespace* for its attributes — type and vocabulary come apart. And `original_document_issue_date` is a distinct claim from `issue_date`, which is the derived-credential problem (Apple's Digital ID has the same shape) surfacing as a field.

- **Name** — `in.gov.uidai.aadhaar.1` (Aadhaar)
  - **Asserts** — an Indian Aadhaar credential.
  - **Key fields** — namespace `in.gov.uidai.aadhaar.1`: `credential_issuing_date`, `enrolment_date`, `enrolment_number`, `is_nri`, `resident_image`, `resident_name`, `local_resident_name`, `age_above18`, `age_above50`, `age_above60`, `age_above75`, `dob`, `gender`, `building`, `local_building`, `locality`, `local_locality`, `street`, `local_street`, `landmark`, `local_landmark`, `vtc`, `local_vtc`, `sub_district`, `local_sub_district`, `district`, `local_district`, `state`, `local_state`, `po_name`, `local_po_name`, `pincode`, `address`, `local_address`, `mobile`, `masked_mobile`, `email`, `masked_email`, `masked_uid`, `aadhaar_type`.
  - **Issuee?** — `yes`
  - **Cite** — https://developers.google.com/wallet/identity/verify/supported-credential-attributes
  - **Status** — `stated`. A national-issuer doctype under the issuer's own domain, with four separate age-threshold predicates (18/50/60/75) and paired masked/unmasked contact fields — evidence that predicate and redaction variants show up as distinct *fields* rather than as separate types.

Formats and protocols Google names for these: `mso_mdoc` and its zero-knowledge variant `mso_mdoc_zk` (with a `zk_system_type` such as `longfellow-libzk-v1`); requests expressed as DCQL with `meta.doctype_value` and claims paths of the form `["org.iso.18013.5.1", "<element>"]` each carrying an `intent_to_retain` flag; OpenID4VP and the W3C Digital Credentials API for online presentation; ISO/IEC 18013-5 for in-person (NFC/QR, CBOR `DeviceRequest`/`DeviceResponse`, MSO). Cite: https://developers.google.com/wallet/identity/verify and https://developers.google.com/wallet/identity/verify/accepting-ids-from-wallet-online. Status: `stated`. The overview page also names, in prose, "mobile Driver's Licenses (mDLs), digital passports, and ID passes" as what resides in digital wallets — "digital passports" has no doctype on the supported-attributes page, so treat it as marketing scope, not an available type.

Availability: https://support.google.com/wallet/answer/12436402 is geo-gated and returned "US Driver's License or State IDs aren't available in Google Wallet for your country or region" on this retrieval, naming "US Driver's License or State ID", "Aadhaar card" and "ID pass" as the digital-ID options but listing no supported states or countries. Status: `stated` (including the non-answer).

---

## ISO mDL / mdoc doctypes

Direct citation to ISO text was not possible — https://www.iso.org/standard/69084.html returned **HTTP 403** and the standards themselves are paywalled. Everything below is cited to public documentation that *uses* the identifiers, not to ISO. That is a real limitation and the doctype strings below should be treated as `stated` by the citing party, not by ISO.

- **Name** — `org.iso.18013.5.1.mDL`
  - **Asserts** — a mobile driving licence. Namespace `org.iso.18013.5.1`; AAMVA sibling namespace `org.iso.18013.5.1.aamva`.
  - **Key fields** — see G4 above for the enumerated element set.
  - **Issuee?** — `yes`
  - **Cite** — https://developers.google.com/wallet/identity/verify/supported-credential-attributes (doctype + full element list); https://developer.apple.com/documentation/passkit/pkidentitydriverslicensedescriptor (namespaces + element mapping)
  - **Status** — `stated` by Apple and Google. AAMVA's own guidelines (r1.6, July 2026) state "The mDL data elements shall be as defined in Table 5 belong to namespace 'org.iso.18013.5.1'" but the extracted text of that document does **not** contain the doctype string `org.iso.18013.5.1.mDL` — it works at namespace granularity. Cite: https://aamva.org/getmedia/1bc1f2b3-bc7b-4e44-8112-127a4110ad94/mDLImplementationGuidelines-16.pdf, §§ qualifying ISO/IEC 18013-5.

- **Name** — `org.iso.18013.5.1.aamva` (namespace, not a doctype)
  - **Asserts** — the North American extension element set carried inside an mDL.
  - **Key fields** — per AAMVA r1.6, the identifiers in this namespace include `domestic_driving_privileges`, `name_suffix`, `organ_donor`, `veteran`, `family_name_truncation`, `given_name_truncation`, `aka_family_name`, `aka_given_name.v2`, `aka_suffix`, `race_ethnicity`, `sex`, `first_name`, `middle_names`, `EDL_credential`, `EDL_credential.v2`, `DHS_compliance`, `resident_county`, `CDL_indicator`, `DHS_temporary_lawful_status`, plus further `CDL_non_*`, `first_name_*`, `middle_names_*`, `hazmat_*` and `resident_*` identifiers whose full names the PDF's table layout splits across lines.
  - **Issuee?** — `yes`
  - **Cite** — https://aamva.org/getmedia/1bc1f2b3-bc7b-4e44-8112-127a4110ad94/mDLImplementationGuidelines-16.pdf, "Mobile Driver's License (mDL) Implementation Guidelines, Version 1.6", July 2026, § qualifying ISO/IEC 18013-5 Table 5
  - **Status** — `stated` for the namespace and the identifiers listed unsplit. The split names are honestly incomplete rather than guessed. The document also records a deliberate collision: "An additional element for sex is defined in the 'org.iso.18013.5.1.aamva' namespace… Verifying entities shall treat org.iso.18013.5.1.aamva.sex as the primary source" — the same claim name means different things in two namespaces of one credential.

- **Name** — `org.iso.23220.photoID.1`
  - **Asserts** — a photo ID or equivalent document, per the ISO/IEC 23220 series.
  - **Key fields** — ISO 23220_1 namespace, see A3 (`family_name_unicode`, `given_name_unicode`, `portrait`, `birth_date_unicode`, `sex_unicode`, `age_in_years`, `age_over_NN`, `document_number`, `issue_date`, `expiry_date`, `issuing_authority_unicode`, `issuing_subdivision`, `issuing_country`, resident address fields, and Latin-1 variants of the name fields).
  - **Issuee?** — `yes`
  - **Cite** — https://developer.apple.com/documentation/passkit/pkidentityphotoiddescriptor
  - **Status** — **CORRECTED 2026-09-21.** This entry originally recorded a two-way casing discrepancy and attributed `org.iso.23220.photoID.1` to Apple. An independent re-fetch found no doctype string on Apple's page at all, and found a *third* spelling elsewhere. The state of the evidence is: Apple names no doctype; the open-source verifier writes `org.iso.23220.photoid.1`; the EU reference issuer's metadata writes `org.iso.23220.2.photoid.1`, with an extra `.2` segment — and that same metadata entry uses `org.iso.23220.photoid.1`, without the `.2`, as the namespace for its own claim paths. ISO is unreachable (HTTP 403, the standard is sold), so nothing adjudicates between them. Treat the photo-ID doctype string as unsettled, and do not cite Apple for any spelling of it.

- **Sibling doctypes named by a public open-source ISO 18013-5 verifier.** Recorded as one entry because they share a single citation and a single evidential weight — a third-party implementation's list, not a registry.
  - **Names** — `org.iso.18013.5.1.mDL` (Mobile Driving Licence); `eu.europa.ec.eudi.pid.1` (EU Person Identification Data); `eu.europa.ec.eudi.bida.1` (Basic Identification Data Attestation); `eu.europa.ec.av.1` (EU Age Verification — "age-only attestations such as age_over_18"); `org.iso.23220.photoid.1` (Photo ID); `org.micov.1` (mICOV — vaccination/test attestations); `org.iso.7367.2.1.mVC` (vehicle card); `fr.idak.mbicycle.1` (Bicycle ID card — bicycle owner data); `fr.ft.hsc.1` (Student Card).
  - **Asserts** — as labelled above.
  - **Key fields** — `not stated` in the fetched README beyond the doctype labels.
  - **Issuee?** — `yes` for the person-identifying ones (mDL, PID, BIDA, Photo ID, Student Card, mICOV); `unknown` for `eu.europa.ec.av.1` (an age-only attestation may be deliberately unlinkable); `no` for `org.iso.7367.2.1.mVC` and `fr.idak.mbicycle.1`, which are about a *thing* rather than a person — though the bicycle card is described as carrying "bicycle owner data", so it straddles.
  - **Cite** — https://raw.githubusercontent.com/stelauconseil/mdoc-web-verifier/main/README.md
  - **Status** — `inferred` weight. The strings are `stated` in that README, but a single open-source verifier's recognized-doctype list is weaker evidence than an issuer's or a standards body's, and the README itself warns that wallets may not support all of these. Treated as leads, not as a registry. The commonly-cited `org.iso.7367.1.mVRC` (mobile vehicle registration certificate) did **not** appear in any source I fetched — this README names `org.iso.7367.2.1.mVC` instead. Do not assume `mVRC` without a fetch that shows it.

Note on the registry question: several secondary sources describe ISO/IEC 23220-7 as the doctype registry for ISO mobile documents, and AAMVA r1.6 says "components of this interaction will be standardized in the ISO/IEC 23220 series" with a footnote that "The ISO/IEC 23220 series of standards is not yet sufficiently stable for use by Issuing Authorities." So there is no fetchable authoritative doctype registry as of this retrieval — which is itself the finding.

---

## Other current enumerations

### EU Digital Identity Wallet — attestation rulebooks catalog

The EUDI ARF moved its attestation rulebooks into a dedicated public repository. As of retrieval it contains exactly two: `rulebooks/pid` and `rulebooks/mdl`. Cite: https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog. Status: `stated`.

- **Name** — `eu.europa.ec.eudi.pid.1` (Person Identification Data, natural person)
  - **Asserts** — person identification data for a natural person, as mandated by CIR 2024/2977. The rulebook states: "'eu.europa.ec.eudi.pid.1' will be used as the attestation type for [ISO/IEC 18013-5]-compliant PIDs" and "Similarly, 'eu.europa.ec.eudi.pid.1' will be used for the namespace of the attributes specified below."
  - **Key fields** — mandatory: `family_name`, `given_name`, `birth_date`, `birth_place`, `nationality`, `portrait`. Optional (per CIR 2024/2977): `resident_address`, `resident_country`, `resident_state`, `resident_city`, `resident_postal_code`, `resident_street`, `personal_administrative_number`, `family_name_birth`, `given_name_birth`, `sex`, `email_address`, `mobile_phone_number`. Issuer metadata: `issuing_authority`, `issuing_country`, `expiry_date`, `document_number`, `issuing_jurisdiction`, `issuance_date`, `trust_anchor`, `attestation_legal_category`.
  - **Issuee?** — `yes`
  - **Cite** — https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog/blob/main/rulebooks/pid/pid-rulebook.md §2 (attribute tables), §3.1 (mdoc encoding), §4.1 (SD-JWT VC encoding). Version history in the document runs to 1.7, 17 Jul 2026.
  - **Status** — `stated`. Two details worth carrying: the same string serves as both docType and mdoc namespace; and the SD-JWT VC encoding uses a *different* identifier shape entirely — "Requirement PID_14 in ARF Annex 2 defines the base type to be 'urn:eudi:pid:1'. As a convention, all PIDs must use types in the namespace 'urn:eudi:pid:'", with the German national PID shown as `"vct": "urn:eudi:pid:de:1"`. One credential, two type identifiers, chosen by serialization format. Also note `attestation_legal_category`, which the rulebook glosses as indicating "that a PID has indeed been issued as a PID" — a claim whose whole job is to assert the credential's own kind.

- **Name** — EUDI mDL (ARF Annex 3.02)
  - **Asserts** — a mobile driving licence within the EUDI Wallet ecosystem, legally specified by the proposed 4th Driving Licence Regulation.
  - **Key fields** — none of its own: "The data model for ISO/IEC 18013-5-encoded mDLs is fully specified in ISO/IEC 18013-5. No changes need to be made to this data model for an mDL attestation within the EUDI Wallet ecosystem."
  - **Issuee?** — `yes`
  - **Cite** — https://github.com/eu-digital-identity-wallet/eudi-doc-attestation-rulebooks-catalog/blob/main/rulebooks/mdl/mdl-rulebook.md §2
  - **Status** — `stated`. Notable for the negative constraint: "mDLs issued to a Wallet Unit SHALL NOT be implemented as [SD-JWT VC]-compliant attestations" — the Regulation names only ISO/IEC 18013-5, so serialization is pinned by law rather than by preference. The document carries the ARF's standing disclaimer that it "holds no legal value and does not reflect any common agreement or position of the co-legislators."

---

## Failed and partial fetches

- **https://www.iso.org/standard/69084.html** — HTTP 403 Forbidden. No ISO text is cited anywhere in this file; every ISO identifier here is quoted from a party using it, never from ISO. The full formal title of ISO/IEC 18013-5:2021 is therefore **not recorded** rather than reconstructed.
- **https://developer.apple.com/documentation/...** (the human-facing pages) — returned title-only shells; Apple's documentation is client-rendered. Worked around by fetching the same pages' JSON backing route, `https://developer.apple.com/tutorials/data/documentation/<path>.json`, which is what the citations note. Content is Apple's own, not a mirror.
- **https://www.aamva.org/getmedia/8d8fbb1f-.../mdl-implementation-guidelines-v1-4.pdf** — 404. The v1.4 URL that searches surface is dead; the live document is v1.6 at the `aamva.org/getmedia/1bc1f2b3-...` URL cited above.
- **AAMVA r1.6 PDF table extraction** — the document was fetched and its text extracted successfully, but several AAMVA-namespace element identifiers are split across lines by the PDF's table layout (`CDL_non_…`, `first_name_…`, `middle_names_…`, `hazmat_…`, `resident_…`, `DHS_…`). Those are recorded as truncated rather than completed from the cleaner list on Google's page, since the two sources do not necessarily agree on the full set.
- **https://eudi.dev/latest/annexes/annex-3/annex-3.01-pid-rulebook/** — the ARF site now only says "The PID rulebook has been moved to a dedicated repository." Redirected to the GitHub catalog, which is what is cited.
- **https://openid.net/specs/openid-4-verifiable-presentations-1_0.html** — fetched, but the mdoc appendix (B.2, "Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)") was truncated by length before any doctype string appeared. No OpenID4VP doctype claims are made in this file.
- **https://support.google.com/wallet/answer/12436402** — fetched but geo-gated; returned an availability refusal rather than a jurisdiction list. Recorded as such in G4.
- **Apple jurisdiction list** — no Apple-hosted canonical list of supported states was retrieved. Secondary tech-press counts conflict and are not recorded as facts.

---

## from-memory-UNVERIFIED

Nothing. Every type, field, identifier and quotation above came from a page fetched during this session. Where a source was unreachable (ISO) or truncated (OpenID4VP, the AAMVA tables), the gap is left open in the sections above rather than filled from training memory — including the formal title of ISO/IEC 18013-5, the complete ISO 18013-5 Table 5 element list, and the `org.iso.7367.1.mVRC` doctype string, none of which any fetch in this session established.

---

## Correction note, 2026-09-21

This file was written from a first pass and then checked against independently re-fetched captures while the source records in `refs/sources.credential-types.yaml` were being built. One claim did not survive that check and has been corrected in place, above, with the original wording shown rather than deleted.

**The claim:** that Apple's `PKIdentityPhotoIDDescriptor` documentation names the doctype `org.iso.23220.photoID.1`. **The finding:** it does not. The fetched document contains `ISO 23220_1 namespace` and no reverse-DNS doctype string anywhere. The identifier had been carried in from elsewhere and attributed to the nearest page that discussed photo IDs — which is precisely the failure EVIDENCE.md rule 2 exists to catch, and it survived the first pass because the sentence around it sounded right.

**What it exposes, and why it is worth more than the correction.** There are now three spellings of the photo-ID doctype in circulation with no source that adjudicates between them: none from Apple, `org.iso.23220.photoid.1` from an open-source verifier, and `org.iso.23220.2.photoid.1` from the EU reference issuer's own metadata — whose claim paths then use `org.iso.23220.photoid.1`, without the `.2`, for the very same credential. ISO's pages return HTTP 403 and the standard is sold, so the registry that would settle it is not reachable. A credential *type identifier*, the thing a renderer would key a glyph or a colour off, is not stable across the parties implementing it.
