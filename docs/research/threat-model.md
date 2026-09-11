# Threat model

Phase 3. Adversaries and what each can do against a *renderer* — not against KERI, whose protocol-level threat model (duplicity, key compromise, witness collusion) is a different and already-modelled problem this document takes as substrate. The question here is narrower and has had no prior art at all in the audited field: what can each adversary make a *rendering* say, imply, or leak that the evidence does not warrant? Every audited ecosystem assumes the verification channel is the rendering channel and none designed for the moment those separate ([prior-art/wallets.md](prior-art/wallets.md) §5), so most of the defences below are arcviz's own rules rather than inherited practice.

**Citation discipline.** As in [principles.md](principles.md): spec claims cite `spec-body.md:NNN` / `v1.1:NNN`; papers and literature by `refs/sources.*.yaml` key with locator; implementation claims via the sibling audits by section; matrix rules as "Rule N" and sections as "§x" into [disclosure-matrix.md](disclosure-matrix.md); principles as "P*n*" into [principles.md](principles.md). Unmarked reasoning is this document's own and is flagged where it goes beyond the sources.

**Structure.** Modeled on the W3C render-method threat model's typed-response discipline, which the W3C audit recommended stealing ([prior-art/w3c.md](prior-art/w3c.md) §"What we should steal" 4): each threat carries a response typed **eliminate**, **reduce**, **transfer**, or **accept**, and "accept" with a stated reason is a legitimate answer. Residual risk is stated for every threat, because a threat model that ends every row with "mitigated" is advertising, not analysis.

**Coverage honesty, stated before any threat.** The fixture corpus exercises *structure*, not KEL/TEL facts: no signing, no witnesses, no inception or rotation events, no TEL simulation ([corpus/README.md](../../corpus/README.md) "Known limitations"; §e's fixture-attested tier). Every signature, anchoring, delegation, and revocation cell — V checks 3–5, 8, 9, R0's warrants, R8's staleness, pairs 6 and 7 — is exercised by no fixture. The defences below that rest on those cells are spec- and implementation-attested but untested against artifacts, and claims in this document about them inherit that limit. Several absences are additionally flagged as absence-of-evidence rather than confirmed absence: whether KERIA's escrow/notification layer deduplicates replayed grants ([presenter-control.md](presenter-control.md) §(g)2), and whether a host can build pair 10's fail/not-yet separator from its own store (the refutation's open lead, §c pair 10).

---

## A1 — The malicious or careless issuer

**Capability.** Authors everything inside the artifact: attribute labels and values, rules prose, schema content (title, descriptions, `anyOf` candidates), edge structure, and — in ecosystems that carry them — branding, templates, or embedded URIs. A careless issuer produces the same hazards without intent: keripy's own builders emit the metadata-ACDC discriminator (`u=''`) on ordinary issued credentials (§B1's H6 note, SKP-F2).

**Goal.** Execute code in the viewer; counterfeit the viewer's own trust chrome; exfiltrate view-time data through external references; or, more cheaply, deceive through content — misleading field names, a schema title asserting authority, rules prose that reads as the viewer's endorsement.

**Surface.** The rendered canvas; any template path; the schema as rendering input; every string arcviz displays.

**Defence.** P11 (no execution, no content-initiated network activity, hard frame/canvas boundary, SAID-verified schema input); P12 (issuer-authored names carry their provenance); Rule 19 (reserved-label hygiene — `_` and `-` violations render as structure or parse error, never data, `v1.1:55,63,65`); Rule 17 (no fetch, which closes the beacon channel the W3C model calls T3 — [vcrm-t3] via [prior-art/w3c.md](prior-art/w3c.md)); Rule 12 as conditioned (the careless-issuer case: the metadata marker fires only with corroboration, so an issuer's unset `u` cannot make arcviz stamp a false "issuer-uncommitted" state).

**Response.** **Eliminate** for code execution and content-initiated fetches in arcviz's default path — SD-JWT VC's flat MUST-NOT-execute posture, adopted deliberately over the W3C sandbox ([sdjwtvc-security]; [prior-art/w3c.md](prior-art/w3c.md) §"What we should steal" 5). **Reduce** for chrome counterfeiting: the frame/canvas boundary is arcviz's own invention, because the W3C threat model nowhere names chrome-spoofing — a confirmed gap in the prior art, verified by search ([prior-art/w3c.md](prior-art/w3c.md) §"What we should refuse" 3).

**Residual.** Text-level deception inside the issuer's own canvas is not preventable by a renderer: authenticity and veracity are orthogonal, and a credential can be authentic and false at once ([avv2025-orthogonality], `authenticity-vs-veracity.md:35`). arcviz can bound *where* issuer content appears and *what authority it wears*, not what it says. Homoglyph and misleading-label attacks inside attribute values remain; the defence is P12's provenance visibility, which reduces but does not remove them. Users fooled by well-executed visual counterfeits are the documented norm, not the exception ([dhamija2006phishing]).

## A2 — The holder presenting a doctored or stale render

**Capability.** Screenshots, prints, edits, or re-displays arcviz output outside the live session; presents an old render whose checks were true when captured; or fabricates an image imitating arcviz's chrome entirely. Costs nothing and requires no key compromise.

**Goal.** Have a static artifact accepted as live verification — the "flash pass," which the mDL ecosystem names and prohibits at the protocol level: presenting "an image of a credential to a verifier" is explicitly forbidden by the AAMVA guidelines ([presenter-control.md](presenter-control.md) §(e)).

**Surface.** Static output: print CSS, exports, screenshots — and, indirectly, the verifier's willingness to accept them.

**Defence.** P15 / Rule 15: every V and P indicator in static output renders as a historical record ("checked ⟨scope⟩ by ⟨tool⟩"), never live; P4's as-of scoping makes even the live render date its claims, so a stale capture carries its own age on its face; Rule 4 makes staleness a first-class symbol under a host-supplied per-credential policy.

**Response.** **Reduce** (arcviz's static output never *claims* live state) plus **transfer** (a verifier who accepts a static render as live verification is acting against what the render itself says; the acceptance decision is the verifier's, per P7 — the last step was always theirs). **Accept** for the fabricated-image case, with reason: no rendering discipline can prevent an image editor from imitating chrome. The defence against fabricated proof is re-verification from the underlying material, which is a protocol act outside the renderer (and what a re-verifier needs in hand is deliberately unresolved — §f question 10).

**Residual.** The sharpest residual in the whole model, and the corpus states it without resolution: an export carrying transferable proof removes the holder's control over resharing, while an export carrying none is a forgeable claim of verification — "Both are bad in different directions, and 'no export' is not obviously survivable in a real tool" ([prior-art/papers-intent.md](prior-art/papers-intent.md) §(g) Q5). Rule 15 governs what the export *says*; what it *carries* is an open design decision.

## A3 — The man in the middle substituting an AID

**Capability.** Has ground offline: prepared a substitute AID or SAID whose casual appearance approximates the genuine one, and can place it in material the viewer renders (a doctored document, a swapped payload, a copied string).

**Goal.** Have the substitution survive a glance, so the viewer's trust in the genuine identifier transfers to the substitute.

**Surface.** The identifier rendering — the entviz pill — and the viewer's comparison behavior.

**Defence.** P8: every SAID and AID renders as a pill, so an honest substitution disturbs a picture rather than hiding in a string nobody reads; P9's capacity constraint keeps the security bits on discrete symbols an adversary cannot hide inside; Rule 7 keeps AGIDs out of SAID pills so a match never overstates what it proves; and the route to a real comparison ceremony (`EntvizCompare`/`EntvizWalk`/`EntvizVoiceCompare`) stays reachable.

**Response.** **Reduce**, with the reduction quantitatively bounded — this is the best-measured threat in the corpus. Against a ground-offline adversary, "casual comparison is not marginally weak… it is broken" ([amp-diff], `amp-diff.md:324`); the habituated one-glance read carries only low-to-mid teens of bits ([mglance2026], `m-glance.md:16,240-245`). The seeded comparison walk is "a requirement, not an enhancement" ([amp-diff-walk-required]) — but it is the *ceremony's* property, not the pill's.

**Residual.** The pill rules out; it cannot rule in. A viewer who never invokes the ceremony gets teens-of-bits protection, full stop, and arcviz cannot force the ceremony without violating P7 in the other direction (deciding for the user that this comparison matters). The residual is a habituated user accepting a glance-passing substitute; the design lever is keeping the ceremony one gesture away and never implying it already ran.

## A4 — The phishing verifier

**Capability.** Presents itself to a holder as a legitimate relying party — or presents a counterfeit viewer imitating arcviz — to solicit disclosure. Controls its own request framing, branding, and stated purpose.

**Goal.** Over-disclosure: obtain fields, or the forced correlators that ride along with fields, that the holder would not knowingly release.

**Surface.** Holder-facing views: the pre-presentation rendering of what is about to be disclosed, and the holder's comprehension of it.

**Defence.** In arcviz's scope: the holder-facing render must show what disclosure actually costs — including the forced transitions the format imposes: disclosing any `a` sub-block moves `a.i` and `a.dt` to H1, so the strongest correlator in the artifact goes out with the first field and cannot be withheld (§B1's forced-transition note, PRV-F1; the spec gates exactly this disclosure behind Chain-Link Confidentiality, `v1.1:355`). Sibling-label leakage renders as leaked (Rule 6). Whether arcviz *warns* pre-presentation is parked as an affordance question (§f question 7, widened), but the state rendering itself is settled.

**Response.** **Reduce** for over-disclosure comprehension; **accept**, with reason, for verifier authentication: arcviz is a renderer, not a presentation protocol, and authenticating the requesting party is the host's and protocol's job (EUDI puts relying-party trust in its own badge infrastructure — [prior-art/wallets.md](prior-art/wallets.md) §2). **Accept** also for counterfeit-viewer phishing, same reason as A2's fabricated image.

**Residual.** Two empirical limits the literature forbids designing around. Comprehension is not achievable on demand: a professional team applying best practice moved adherence but "ultimately failed at our goal of a well-understood warning" ([felt2015sslwarnings]). And no verified study exists either way on whether mDL-style selective-disclosure users understand what they released ([prior-art/literature.md](prior-art/literature.md) cluster 1) — so arcviz must not claim its holder-facing view *solves* over-disclosure; it can only make the cost visible and interruptive where it matters (P9). Selective-disclosure controls are not self-explanatory, and users may believe they cannot decline at all ([korir2022wallet]).

## A5 — The network observer

**Capability.** Watches traffic from the viewer's environment: schema dereferences, TEL queries, OOBI resolutions, image loads. Includes the issuer's own infrastructure as a privileged observer of queries addressed to it.

**Goal.** A per-view usage timeline: which credential is being viewed, when, by whom — the OCSP-style leak the substrate was architected against.

**Surface.** Any network act correlated with rendering.

**Defence.** P14 / Rule 17: arcviz initiates no network activity as a side effect of rendering — an unresolved unit renders as H7/unperformable instead. Where the *host* fetches, the freshness input names the surface class, because the spec's Registrar/Observer split exists precisely so "a validator queries its Observer, not the Registrar… no forced phone home validation" (`v1.1:1707`), and a witness is issuer-side infrastructure (§B4's caveat, PRV-F3).

**Response.** **Eliminate** for arcviz-initiated traffic (testable: render with a network monitor, any request fails Rule 17). **Transfer** for host-initiated traffic: the host owns fetch policy; arcviz's obligation is to render the horizon it was given and to scope claims to the surface class the host declares.

**Residual.** arcviz cannot prevent a host from phoning home on its own schedule, and the Observer role the spec commits to is, per the keripy trace, not yet implemented anywhere in that repository ([keria-signify-surface.md](keria-signify-surface.md) Correction, "Observer: not found") — so today's hosts wanting fresh TEL horizons have mostly issuer-side surfaces to ask. Until verifier-side observers exist, the practical choice is stale-but-private or fresh-but-observed, and arcviz can only make that trade visible, not remove it.

## A6 — The presenter of a stolen credential

**Capability.** Possesses a credential's raw bytes without controlling the AID it names as holder — a leaked export, a forwarded copy, an intercepted presentation. Can submit them through `POST /credentials/verify`, deliver them inside a grant it constructs itself, or hand them over out of band ([presenter-control.md](presenter-control.md) §(b)).

**Goal.** Have the bytes accepted, and rendered, as a legitimate presentation.

**Surface.** The verifier-facing render — specifically the gap three independent models found: every check in the V vector is issuer-side, so a stolen credential "is green on all five axes" ([reviews/2026-09-05-outside-model-refutation.md](../../reviews/2026-09-05-outside-model-refutation.md) §(b)1, adjudicated VALID).

**Defence.** Axis P and P6: the presenter question renders before, and at least as prominently as, the V vector; P = unknown is the default and the truth of the default transport, which strips presentation context entirely ([presenter-control.md](presenter-control.md) §(c)); Rule 18's tests; R9 and §c pair 12 name the indistinguishability. P = attested requires host-fetched exchange evidence *plus* host-authored reconciliation of the grant's sender against the credential's holder field — reconciliation nothing in keripy, KERIA, or signify-ts performs anywhere in the traced surface ([presenter-control.md](presenter-control.md) §(a),(c)).

**Response.** **Reduce**, by refusing the lie of omission: arcviz cannot perform the binding check, but it can ensure no render implies the question was asked when it was not. **Transfer** for the check itself: the reconciliation is host work, of the same kind as keripy's own `_verify_representation` test helper, which its docstring says implementers "must port rather than copy" ([presenter-control.md](presenter-control.md) §(a-cont)).

**Residual.** Substantial and honestly stated. Even P = attested is bounded: IPEX's session id is sender-generated, not a verifier-issued challenge, so it is not a freshness proof the recipient can independently confirm was never reused ([presenter-control.md](presenter-control.md) §(e)); whether KERIA's escrow layer deduplicates replayed grants is unconfirmed (§(g)2); and whether presenter binding is even constructible for a bare grant of a pre-existing credential — as opposed to the mint-fresh-per-presentation pattern — is an open implementation question (§(g)3). A fabricated host attestation renders as attested (see A9). This adversary is why Rule 18 exists, and the rule's whole power is making the unanswered question visible.

## A7 — The schema substituter

**Capability.** Controls the schema-resolution path of a host that resolves schemas without SAID verification — a browser-side host dereferencing a URL, a compromised cache. Supplies, for a committed schema SAID, a different schema.

**Goal.** Flip a rendering decision through the renderer's own input. The sharpest instance: supply a schema that reserves a `u` for a block that has none, so an H2 rainbow-attackable unit renders with H3's lock — "asserting privacy protection that does not exist… reached through Rule 8's own input" (SEC-F2's failure scenario). Subtler instances: substituted titles, labels, and `anyOf` candidates that change what the render implies (the H2/H3 privacy distinction is read from a schema whose integrity nothing in the original host interface required — the finding's own title).

**Surface.** The schema input to Rules 6 and 8 and to every schema-shaped rendering decision.

**Defence.** The SAID-verification gate, folded into §c pair 5 and Rule 8: a resolved schema is admissible input only if it verifies against the committed schema SAID; the mandate is normative — "Schemas MUST be SADs and therefore verifiable against their SAIDs" (`v1.1:211`), non-local URI references "MUST NOT be used" (`v1.1:217`). A host that cannot demonstrate SAID-verified resolution supplies "hidden; protection unknown" instead. Stock keripy verifies (`CacheResolver.add` refuses a mismatched schema, `src/keri/core/scheming.py:47-48` per SEC-F2's verification), which is exactly why the requirement lives in the host interface: browser-side and KERIA-side hosts have no such gate by construction.

**Response.** **Eliminate** through the gate, for the classification flip. **Accept**, with the named-ambiguity treatment, for what no gate can fix: a *verified* schema that makes `u` optional leaves H2/H3 genuinely undecidable (§c pair 11), and the honest render is "protection undecidable (permissive schema)," distinct from pair 5's "protection unknown (schema unresolved)."

**Residual.** A host that claims SAID verification falsely defeats the gate (A9's problem); and the gate protects classification, not content — a genuine, verified schema whose *issuer* chose misleading titles is A1's residual, not this one's.

## A8 — The correlating verifier

**Capability.** Runs arcviz legitimately, on material legitimately received, and uses the viewer itself as a correlation engine: loads multiple presentations, joins on shared identifiers, retains renders and exports across sessions. Needs no protocol violation — the correlators are genuinely in its hands (§B5).

**Goal.** Assemble cross-context profiles cheaply; establish negative facts ("this AID appears nowhere else I've seen"); defeat holder-side protections — blinded blocks, bulk instances, per-facet AIDs — viewer-side, where the evidence lives only on the verifier's disk (PRV-F4's failure scenario).

**Surface.** Correlators within one presentation; exports carrying `a.i` and their lifetime; any empty state readable as exhaustive. *Cross-presentation joins and the join log were this threat's largest surface and are gone by scope (2026-09-11) — arcviz loads one presentation at a time.*

**Defence.** P13, strengthened by scope: arcviz loads one presentation at a time and draws no edge between presentations at all (Rule 14 as amended 2026-09-11; [affordances.md](affordances.md) AF14, retired), so the join is eliminated rather than governed; no corpus-level negatives (Rule 13); "unlinkable"/"anonymous" never rendered as absolutes; The papers corpus supplies the reasoning: making correlation cheap *is* the harm ([hardman-wbca-expense]), negative facts are its sharpest form ([hardman-wbca-negative]), and linking facets is "never a default, never an inference a stranger is meant to draw" ([hardman-if-owner]).

**Response.** **Reduce** for the default posture — arcviz refuses to cheapen correlation silently. **Accept**, with reason, for the determined case: an open-source viewer cannot restrict who runs it or what a motivated operator does by hand or by fork ([hardman-wbca-who] — democratized lookup power is the named cost of democratized tooling). What arcviz controls is defaults, prominence, and the trace an explicit join leaves.

**Residual.** The verifier who wants the join still gets it, by hand or by forking the component — but not from arcviz, and not by default. Eliminating the affordance moves this from *mitigated* to *out of scope*: what a determined operator does outside the component was never a threat arcviz could carry. The viewer-side-accumulation branch closes with it, since one-presentation-at-a-time leaves nothing to accumulate.

## A9 — The careless or compromised host

**Capability.** Sits between the substrate and arcviz and supplies every input P16 enumerates: verification vectors, outcome-space declarations, store identity, schemas, freshness policies, cause attestations, presentation-provenance evidence. Can misdeclare any of them — carelessly (feeding arcviz from the unvalidated `reger.creds` table that `vc export` enumerates, SEC-F3) or maliciously (fabricating a P attestation, declaring fail-capability it lacks, asserting SAID-verified schemas unverified).

**Goal.** (Careless) inherit warrants the material never earned. (Malicious) launder arbitrary claims through arcviz's honest-looking chrome.

**Surface.** The entire host interface.

**Defence.** Fail-safe defaults throughout, per P3 and P16: undeclared store identity gets the weaker reading (§B6's store-identity amendment — presence in a raw credential log warrants SAID self-consistency alone); no fail glyph without a fail declaration (Rule 2 amendment (c)); unsupplied channels render their defined absent-state, so a lazy host degrades precision, never honesty (SKP-F3's folded baseline, §c). Host-supplied claims render *with their own provenance and scope* — an attested cause carries its attestation's provenance (Rule 5), an attested P names who attested, over what signature, addressed to whom, as of when (Rule 18) — so a fabricated claim is at least a *traceable* fabrication.

**Response.** **Reduce** for carelessness — the defaults are built so the common failure (declaring nothing) is honest. **Accept**, with reason, for the malicious host: arcviz is a rendering library inside the host's process and cannot audit its inputs; a host that lies to it can make it lie. This is the trust boundary of the component, stated plainly rather than papered over. The scoping requirements convert undetectable fabrication into attributable assertion, which is the most a renderer can do.

**Residual.** All of it, for a fully malicious host — the same residual every UI library carries. The meaningful design output is that arcviz's interface makes the honest path the path of least resistance: a host must do *extra work* (declarations, attestations, provenance) to make arcviz claim more, and zero work to have it claim honestly less.

---

## Accepted gaps and open items

Recorded so the model's edges are decisions, not omissions.

- **Algorithm rot.** A single outside seat raised cryptographic-algorithm deprecation as a T/V state distinct from stale and failed ([reviews/2026-09-05-outside-model-refutation.md](../../reviews/2026-09-05-outside-model-refutation.md) §(b)8, adjudicated valid-but-minor and filed as a candidate open question). Not modeled here; if a host's policy deprecates an algorithm, today's honest render path is a host-declared unperformable with cause. Accepted as future work.
- **Fulfillment matching** (does the credential satisfy the verifier's request) was ruled out of the matrix's scope and stays out of this document's: it is a query-evaluation problem, not a rendering-state problem (refutation §"Objections checked and found INVALID").
- **KEL/TEL-dependent defences are untested.** Repeated from the head of this document because it bears on A2, A5, and A6 specifically: staleness, anchoring, delegation-reach, and revocation-horizon rendering have spec and implementation grounding but no exercising fixtures yet (§e). The threat rows above do not claim otherwise.
- **Pair 10's separator lead is open.** Whether a host can distinguish edge-constraint failure from far-node absence using its own store remains flagged, not adjudicated (§c pair 10's open lead). If it closes in the host's favor, A9's careless-host row gains a cheap mitigation (hosts could declare fail-capability for check 6 more often); nothing above depends on either outcome.
- **Export payload.** What a static export should carry for re-verification is parked (§f question 10), which leaves A2's doctored-render residual governed by labeling only. A demand test naming the re-verifier is the unblocking event.
- **Retention bounds, narrowed.** The join-log half of §f question 11 lapsed with AF14's retirement on 2026-09-11 — no join, no log, and one presentation at a time leaves no joinable store. Export lifetime and per-credential export permission remain undecided, with no-persistence the default posture.
