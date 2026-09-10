# Research plan: visualizing ACDCs

*Draft 2, 2026-09-04. Home: this repository, `arcviz`, modeled on [entviz](https://github.com/dhh1128/entviz) for structure and rigor and on [entviz-js](https://github.com/dhh1128/entviz-js) for the JS/React shape.*

## Decisions taken 2026-09-04

- **Name: `arcviz`.** An *arc* is both an electric arc and a directed edge in a graph, which is precisely the thing that makes ACDCs hard to draw. The bare name `arc` is unavailable on both PyPI and npm, so the suffixed form is required for packages anyway, and it makes the family symmetric: `arcviz` on PyPI, `@arcviz/core` and `@arcviz/react` on npm, alongside entviz's identical pattern.
- **Deliverable: specification + Python reference implementation + React implementation.** Python earns its place twice — it lets CI prove the spec against a conformance corpus without a browser, and it lets system tooling generate credential views outside a web context. This is exactly entviz's shape.
- **Rendering authority is deferred to Phase 3.** Whether the issuer supplies a rendering template (the W3C path) or the viewer derives everything from the schema is the sharpest architectural fork in the project, and it will be decided on the audit's evidence rather than on a prior. Phase 1A is scoped to gather exactly what that decision needs.
- **Open, deferred:** whether the JS/React implementation lives in this repository under `impl/` (the COIA pattern) or in a sibling `arcviz-js` repository (the entviz pattern). npm packaging argues for the sibling; simplicity argues for one repo. Decide at implementation time, not now.

## Decisions taken 2026-09-05 (second set)

- **Freshness policy is supplied by the host, per credential — not by arcviz, and not globally.** Daniel's ruling. The significant refinement is that **different credentials may have different revocation-freshness profiles**, so the interface cannot be a single window: a policy is resolved per credential, presumably keyed by schema, registry, or governance framework. Where no policy is supplied for a given credential, "no freshness policy supplied" is its own visible state, not a silent default.
- **Unknown operators: the ruling stands, but only for operators the governing profile defines.** *Revised 2026-09-06 after adjudication — see [`../../reviews/2026-09-06-operator-semantics-adjudication.md`](../../reviews/2026-09-06-operator-semantics-adjudication.md).* Where an operator is defined by the applicable spec but not implemented by arcviz, the honest render is "unknown operator, constraint unevaluated" — the `unperformable` outcome on axis V — and it suppresses nothing, because arcviz has no verdict to suppress. Where a token is defined by *no* table, the spec's default-injection clause fires, the constraint is evaluated, and it can fail; rendering that as unevaluated would hide a real negative, so this case is excluded from the ruling. Edge-*group* operators are a third case governed by their own default (`AND`), not by the unary injection clause at all.
- **~~The governing operator profile is a host-supplied input, per credential.~~ RETRACTED 2026-09-10.** This was built on the premise that two spec branches define different operator tables. They do not. `main` and `v1.1` both declare "Specification Status: v1.1" and both describe ACDC protocol 2.x; our own fixtures decode to `pvrsn: 2.0`. The branches have diverged editorially — 22 commits on `v1.1` absent from `main`, 11 the other way, neither an ancestor of the other — and the substantive content is all on `v1.1`, where `E1E`, the `dp` disclosure-paths construct, the field-label restrictions and the UUID-to-unique-entropy rename were merged. `main` is behind on content and ahead on tooling. That is an unreconciled repository state, not a protocol ambiguity, and no governance input should be designed around it. **arcviz implements the operator table as `v1.1` states it, including `E1E`.** See [`../../reviews/2026-09-06-operator-semantics-adjudication.md`](../../reviews/2026-09-06-operator-semantics-adjudication.md).
- **Detect the ACDC protocol version from the DAG.** Daniel's mechanism, and it is the right one for what it governs: scan the graph for the highest protocol version present and require the reader to support it, since both branches oblige a v2 implementation to parse v1 version strings and the field vocabularies genuinely differ (v1 `ri`, no `t`, no `A`; v2 `rd`, `t`, `A`). Derivable from the artifact, so it costs no host input. One refinement: highest-in-the-DAG governs *reader capability*, while an edge's operator semantics are those of the ACDC that **contains** the edge, so per-node version governs meaning.
- **Revocation phrasing: "no revocation as of ⟨horizon⟩", never "not revoked".** *Retraction of the stated grounds.* An earlier draft justified this by claiming `keri-primer.md:269` and `acdc-and-mtc.md:134` contradict each other on revocation currency. Both passages were read directly on 2026-09-05 and **they do not conflict.** The primer's "real-time status checks without privacy leaks" is a comparison against X.509/OCSP — the point is that checking costs no privacy — while `acdc-and-mtc.md` is comparing against Merkle Tree Certificates and describing the *mechanism*, event reconciliation rather than a live query. Achievable currency and the means of achieving it are not competing claims. The rule stands on the simpler ground that reconciliation has a horizon by construction: "Freshness here is about continuity rather than immediacy" (`acdc-and-mtc.md:132`), so a viewer knows only as much as the events it has replicated.

## Decisions taken 2026-09-05

- **Correlation: surface perfect correlators.** See the principle below. This corrects an earlier draft rule ("render disclosed structure, never compute new structure") that would have suppressed facts and manufactured a false sense of security.
- **Affordance scope: arcviz may make disclosure-side rules, flagged as new.** Sharing, printing and fetch-on-expand are real affordances of the component, so ducking them would leave holes in the inventory. `sda.md:107` names the outbound attribute-disclosure axis — what a delegate may reveal about its principal, to whom, and unlinkably — and explicitly declines to specify it. Where arcviz's affordance work writes rules on that axis, they are marked as arcviz's own contribution rather than inherited doctrine, so they can be lifted back into the paper or rejected on their merits.
- **Corpus sources.** A real vLEI ECR chain at `/home/daniel/xfer/credential.cesr` — four ACDCs, three edge sections, four registries, seven delegated inceptions, 341 anchoring interaction events. **It contains personal information and is never copied into this repository, including into `.ignored/`;** it is analyzed in place, and a de-identified synthetic equivalent is regenerated from its shape. Plus keripy's worked examples in `tests/acdc/`, including the ward-presents guardianship example from PR #1577 and its sibling from #1530.

## The shape of the proposal, in one paragraph

Six phases, with the cheap-to-discard artifacts deliberately front-loaded: a home and a citation discipline; five parallel prior-art streams that capture verbatim sources rather than summaries; a domain-constraint pass that turns ACDC's disclosure modes into an explicit display-state matrix; a synthesis pass that names principles and a threat model; an affordance inventory mapped to Norman and to intent boundaries; and an adversarial review of the research corpus *before* any design work begins. Design and implementation follow as separate commissions, each with its own adversarial gate. Two structural commitments run through it: publish a language-independent **rendering spec** with a Python reference implementation and a React implementation held to one conformance corpus (entviz's proven pattern), and build a **corpus of real and adversarial ACDCs early**, because it is what makes design claims falsifiable and it doubles as that conformance fixture set.

---

## Phase 0 — Home, and the rules of evidence

Small, mechanical, done first because everything else writes into it.

**Repo scaffold**, modeled on `~/code/me/entviz`: Apache-2.0 `LICENSE`, `README.md`, `SECURITY.md`, the `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` trio, `.github/workflows/` (CI, docs deploy, release) with every action pinned to a `node24` runtime, a `docs/` site, `.tick` ledger, `refs/`, `reviews/`, `.ignored/`.

**Directory contract** — this is the part worth arguing about now rather than later:

| Path | Holds | Public? |
|---|---|---|
| `docs/research/` | Synthesized findings, principles, threat model, affordance inventory | yes |
| `docs/spec.md` | The rendering spec, once it exists | yes |
| `refs/sources.yaml` | One record per cited source: URL, title, author, retrieval date, local capture path, and *what claim it supports* | yes |
| `refs/captures/` | Verbatim captures — PDF/HTML/`.mhtml` — of public specs and papers | yes, where license permits |
| `refs/screenshots/` | Screenshots of public documentation and open-source UIs | yes, where license permits |
| `.ignored/private-refs/` | Anything we may not republish: Provenant `origin-voice` screenshots, Apple/Google Wallet UI captures, paywalled papers | **no** — gitignored |

**The republication split is load-bearing and easy to get wrong.** This repo is public, on Daniel's personal GitHub. Screenshots of Provenant's product are proprietary; Apple Wallet and Google Wallet UI captures carry trademark and copyright exposure; several HCI papers are paywalled. Those go in `.ignored/private-refs/`, are cited by description and public URL in the public research notes, and are never committed. Getting this wrong is not recoverable by a later `git rm`.

**Citation discipline.** Every substantive claim in `docs/research/` carries a `sources.yaml` key. A source is only usable if someone on this project has read the cited section — relaying another author's summary of a primary source is the failure mode to design against. Each research agent is required to quote the sentence it is relying on, with a locator, into its report.

**Naming.** Settled — see the decisions at the top of this file.

---

## Phase 1 — Prior-art audit, five parallel streams

Each stream produces: a structured report in `docs/research/prior-art/<stream>.md`, captures in `refs/`, and a short "what we should steal / what we should refuse" verdict. Fact-gathering models (Sonnet 5, Haiku 4.5 for the mechanical captures); synthesis held back to Phase 3.

### 1A. W3C / CCG credential rendering

Daniel's recollection is of a W3C task force producing a spec for rendering VCs as SVG. **Treat that as a lead, not a fact.** The leads to run down, each verified against the primary document:

- The W3C Credentials Community Group **"Verifiable Credential Rendering Methods"** work, which (from memory, unverified) defines a `renderMethod` property with an SVG-template rendering type. Confirm it exists, confirm its status (CG report vs. Rec-track), confirm the template mechanism.
- VC Data Model 2.0 itself — what it does and does not say about display. Local vendored copy: `~/code/me/vc-data-model`.
- CCG mailing-list and minutes archives for the task-force history and the arguments that were had.
- Any reference implementations or sample templates linked from the above (Digital Bazaar and the CCG's own repos are the likely sources).

**The security question this stream must answer:** if the issuer supplies the rendering template, the issuer supplies *content that runs in the verifier's viewer*. SVG carries script, external references, and enough expressive power to counterfeit the viewer's own security chrome. Capture what the spec says about sanitization, and what the reference implementations actually do. This is the single biggest architectural fork for our component, and by decision it is settled in Phase 3 on this stream's evidence — so this stream is scoped to gather exactly what that decision needs.

### 1B. Overlays Capture Architecture (OCA)

The other major prior art for credential display, and the one most likely to be missed. OCA separates a capture base from overlays, several of which are presentational (labels, formats, branding, character encoding). Sources: the HGF/Human Colossus OCA specification, the Aries RFCs on OCA for Aries — local vendored copy at `~/code/me/aries-rfcs` — and BC Gov's wallet, which shipped it. Verdict needed on whether OCA's overlay model is a better substrate for our schema-driven prettification than anything W3C has.

### 1C. Wallet paradigms: Apple, Google, mDL

The pass/card paradigm as actually shipped to hundreds of millions of people. Sources: Apple's Wallet and PassKit human interface guidelines and ID-in-Wallet documentation; Google Wallet passes API and its generic/ID pass types; ISO/IEC 18013-5 (mDL) and 18013-7 (online presentation) for what the data model permits; the EUDI Wallet Architecture and Reference Framework's UX guidance. Locally relevant: `~/code/bakobo/eidas-eudi`, `~/code/bakobo/arf-interop`, `~/code/bakobo/mdoc-interop`.

What we want from this stream is specific, not general: how do shipped wallets handle **selective disclosure** in the UI (what does the user see about what they did not send), how do they signal **verification state**, how do they handle a card that is one of many, and what is the print/screenshot story. Captures of Apple/Google UI go to `.ignored/private-refs/`.

### 1D. Local codebases

Read, screenshot, and characterize the four implementations we already own:

- `~/code/provenant/origin-voice` — the accordion view. Entry points: `src/components/organisms/credential-details.tsx`, `credential-card.tsx`, `dossier-credentials.tsx`, `credential-badges.tsx`, `credential-details-modal.tsx`. Run it if it runs cheaply; otherwise read plus any Storybook. Screenshots are proprietary.
- `~/code/me/veridian-wallet` — credential card and detail views; a real KERI/ACDC wallet, so its handling of chained credentials is directly on point.
- `~/code/me/entviz-js` — the existing React surface we intend to consume: `packages/react/src/EntvizPill.ts` and the event model in `events.ts` (`DisclosureState`, `Provenance`, `Medium`, `VerdictState`, `EntvizSensitivity`). This vocabulary already anticipates most of what we need; the report should say where it fits and where it is short.
- `~/code/me/coia` — the alias convention, its flag registry (notably the unverified flag), and the six reference implementations. This defines the interface we need for AID → alias resolution.

### 1E. Academic and practitioner literature

A genuine survey, not a gesture at one. Four clusters:

1. **Credential and consent UX** in digital identity — including work on over-disclosure in mDL presentation and on consent-screen comprehension.
2. **Security indicators and their failure** — the literature on whether users notice, understand, and act on trust chrome. Schechter et al.'s study of security indicators and the phishing-warning literature are the canonical entry points; this cluster is what disciplines any claim we make that "the user will see that it is unverified."
3. **Graph and DAG readability** — node-link versus matrix representations, edge-crossing and layout effects on task performance, and techniques for disambiguating edges without relying on color. Ghoniem/Fekete/Castagliola is a standard entry point for the node-link/matrix tradeoff.
4. **Design theory we will be held to** — Norman's affordances, signifiers, constraints, mappings, feedback, and conceptual models; progressive disclosure; Nielsen's heuristics; Tufte for the print/static case. These are the vocabulary Phase 4 uses.

Deliverable includes a bibliography with retrieval dates and, where the license allows, local captures.

---

## Phase 2 — What an ACDC actually is, as a display problem

The audit above is about other people's credentials. This phase is about ours, and it is where the real difficulty lives.

**2A. Field and section inventory.** *Completed 2026-09-05 — see [acdc-inventory.md](acdc-inventory.md). The field list below was written from recollection before the spec was read, and got the registry field wrong: it is `rd` (Registry Digest SAID), not `ri`. Left uncorrected in place as a marker, since the same habit produced the amp-diff error recorded in EVIDENCE.md.* Every ACDC section and what it means for display: `v`, `d`, `u`, `i`, `ri`, `s`, `a` / `A`, `e`, `r`. Edge semantics: the edge block's own SAID, edge operators and their meaning (`I2I`, `NI2I`, `DI2I`), weights, and the `o` operator forms. Rules as human-readable legal prose that must render as prose. Sources: `~/code/me/kswg-acdc-specification` (vendored spec), `~/code/me/ovc-spec`, and real corpora from keripy/keria test fixtures and the vLEI credential family.

**2B. The disclosure-state matrix.** The deliverable that everything downstream depends on. For each section, and each of ACDC's disclosure modes — full, compact, metadata, partial (blinded), selective — state exactly three things: what the viewer *knows*, what the viewer *cannot* know, and what a naïve renderer would wrongly imply. The security core of this whole project is a single rule falling out of that matrix:

> **Absent, undisclosed, redacted, and unverified are four different states, and the rendering must never let any of them be mistaken for another, or for "fine".**

That rule is the display-layer restatement of `~/code/me/papers/oia.md:66`'s proved-versus-guessed distinction, and violating it is exactly the man-in-the-middle affordance that paper warns about.

**2C. The corpus.** Assemble 20–40 ACDCs as fixtures, deliberately including the cases that break layouts: an eight-deep chain, wide fan-out, a node appearing in two branches (a DAG, not a tree), a chain where an intermediate node is undisclosed, an ACDC whose issuer AID has no alias, one with a very long rules section, one in a non-Latin script, one with a schema we do not have. Real ones where possible; synthesized-but-valid where not. This corpus is a research instrument now and the conformance fixture set later — building it in Phase 2 rather than Phase 7 is the single biggest sequencing improvement in this plan.

---

## Phase 3 — Synthesis: principles and threat model

Frontier model (Fable 5), working from Phases 1–2, producing `docs/research/principles.md` and `docs/research/threat-model.md`. Each principle is named, argued, cited, and stated so that it can be *violated* — a principle no design could fail is not a principle.

Candidates already visible from the material, offered as hypotheses to be tested rather than conclusions:

- **Disclosure honesty.** The 2B rule above.
- **Provenance honesty.** An alias is a private nickname, not evidence [`oia-alias-not-evidence`]. Where an alias is shown for a remote party, the proved/guessed distinction must be visible in the UI — not merely present in the data [`oia-proved-vs-guessed`]. COIA's flag registry is the data-layer hook, and it carries a normative display rule arcviz inherits rather than invents: "*Absence is never a guarantee.* For every flag, absence means only that the flag was not set; it never asserts the negation. An application MUST NOT render an absent flag as a positive assurance" (`~/code/me/coia/README.md:268-270`, repeated at `APPENDIX-D.md:25`). The render must not silently drop a flag, and must not treat an unflagged alias as a verified one.
- **Verification's last step stays human.** `~/code/me/papers/oia.md:86` — automate the introduction, automate the evidence-gathering, never automate the human's act of deciding the evidence suffices. A component that renders a green check has made that decision on the user's behalf.
- **A pill rules out; it does not rule in.** Every SAID and AID renders as an entviz pill, so an honest substitution disturbs a picture rather than hiding in a string nobody reads. But a pill is a *glance*, and `amp-diff.md:324` (§4.3.9) measures that regime and is blunt about it: against an adversary who has ground offline, "casual comparison is not marginally weak… it is broken," and a seeded comparison walk is "a requirement, not an enhancement." So the pill's job is cheap rejection and recognition, and arcviz must keep a route to a real comparison ceremony — `EntvizCompare` / `EntvizWalk` / `EntvizVoiceCompare` — reachable rather than letting the pill imply the ceremony already happened. `trust.ts` states the same rule in four words: rule-out, never rule-in. [`amp-diff`, `amp-diff-walk-required`]
- **Security-relevant state rides on discrete symbols, never on color — and a symbol is not sufficient either.** Two constraints from two literatures. They are *not* the same finding, and an earlier draft of this bullet claimed they were; the citation audit at [`../../reviews/2026-09-05-citation-audit.md`](../../reviews/2026-09-05-citation-audit.md) caught it, and the corrected version is worse news than the overreach was.

  The first constraint is about **capacity**. `amp-diff.md:390` (Principle 5) argues from psychophysics that an analog quantity is recognized with tolerance, saturates near a few bits per dimension, and leaves an adversary a margin to hide in, while a discrete symbol is read without tolerance and certifies its bits exactly. So color, size and shape cannot carry security-relevant *bits* against an adversary who grinds. If arcviz color-codes anything, it spaces the palette by CIELAB lightness and never by ΔE76, which rewards exactly the channel colour-vision deficiency destroys. [`amp-diff-principle-5`, `amp-diff-no-color-alone`, `amp-diff-de76-trap`]

  The second constraint is about **attention**, and it applies to discrete symbols too. The security-indicator literature finds that passive indicators go unnoticed regardless of what channel carries them — Schechter et al. found 92% of participants entered passwords with the site-authentication image removed entirely, and Felt et al. found a deliberate best-practice warning redesign that changed behavior without producing comprehension (see [`prior-art/literature.md`](prior-art/literature.md) cluster 2). A small text label reading "unverified" is a discrete symbol and would also be missed.

  Taken together they do not converge on "use a symbol instead of a color." They bound the design from two sides: color cannot carry the bits, and no small passive indicator of any kind reliably carries the meaning. **Whatever communicates a security-relevant state in arcviz must be structural — placement, layout, an interruption, a shape of the whole card — rather than a badge in a corner.** That is a harder requirement than the one the overreaching version implied, and it is the version design must satisfy.
- **Accessibility and adversarial robustness are one design move, not a tradeoff.** `amp-diff.md:372` (§5.4): the property that makes verification secure against a habituated attacker — hard bits riding on discrete symbols — is the same property that makes it accessible. This reframes the print, monochrome and colour-vision requirements as reinforcing the security posture rather than competing with it. [`amp-diff-accessibility`]
- **Issuer content is untrusted content.** Any issuer-supplied branding, template, or SVG is an attack surface: script execution, external resource loads (which are also a privacy beacon), and counterfeiting of the viewer's own chrome. There must be a hard, visible boundary between the issuer-controlled canvas and the viewer-controlled frame around it.
- **Expansion is local; acquisition is a protocol act.** An earlier draft of this bullet said every expansion is a potential disclosure, on the assumption that following an edge fetches over the network. In the KERIA/signify stack that is false, and the reason is structural: KERIA will not save a credential whose chain does not resolve, so the far nodes of any credential a wallet holds are already local and embedded in the response. Expanding an edge costs nothing and leaks nothing there [`keria-signify-surface`]. Acquiring a credential the wallet does *not* hold is the opposite extreme — there is no generic fetch-by-SAID, only a full IPEX exchange, which is a negotiation rather than a silent fetch and cannot be triggered by a hover.

  So the intent boundary sits at acquisition, not at expansion, and hover-to-highlight and click-to-expand are safe affordances against this substrate. The general principle survives for hosts that *do* resolve references over the network — a verifier-side viewer, or any future fetch-by-SAID — so the rule is conditional on the host, and the affordance inventory must ask which regime it is in rather than assuming. `~/code/me/papers/intent-boundaries.md:84`'s corollary applies directly here: don't imagine boundaries where they don't exist, because pretending not to know the user's intent adds friction for nothing.
- **Correlation honesty — surface perfect correlators, never manufacture them.** A perfect correlator is a fact, not an inference, and hiding one from the viewer does not remove it from the world; it only tells the viewer that privacy exists where it does not. Two credentials issued to the same AID have the same subject, with certainty — treating that as a probabilistic signal to be withheld undersells what the viewer already holds. The EFF primer on information theory and privacy [`eff-info-theory`] gives the scale: the identity of a random person on Earth carries just under 33 bits, and partial facts stack toward it (birthday 8.51 + ZIP 23.81 + gender ≈ 33.32). A name match is a partial correlator to be labelled as an inference with its strength; an AID match is not a narrowing but a landing.

  Three consequences. **arcviz surfaces the perfect correlators present in what it has been shown, and does not go hunting for more** — no fetching or joining against material the viewer was not given. **A format's residual correlators are worth rendering**, because credential systems attempt to hide correlators with poor success: a fully-disclosed and a selectively-disclosed W3C VC are perfectly correlated through the signature, and the revocation-registry link is another perfect correlator, so a viewer that renders selective disclosure as though privacy had been achieved is lying about the residual. Showing what a format leaks *despite* its disclosure machinery is a thing arcviz can do that nothing audited in Phase 1 does. And **the negative claim stays forbidden**, on completeness rather than correlation grounds: "this AID appears in no other credential" is a claim about a corpus we do not have, so the view must always be labelled partial.

  This is consistent with the component we are building on: entviz's collapsed pill is deliberately constructed so that identical SAIDs render identically, which makes it a correlator-surfacing device by design. A rule that suppressed correlation would have arcviz fighting its own pill.
- **Redundant encoding.** Edge coding cannot rest on color alone: print may be monochrome, hover does not exist on paper or touch, and color-vision deficiency is common. Color plus shape plus label, or it does not ship.
- **Honest degradation.** A printed or screenshotted credential carries no verification. The static render must not look more authoritative than it is, and should carry what a re-verifier would need.

The threat model enumerates adversaries and their goals: a malicious issuer, a malicious holder presenting a doctored render, a man in the middle substituting an AID, a phishing verifier, and a curious network observer watching expansion traffic.

---

## Phase 4 — Affordance inventory

A table, in `docs/research/affordances.md`, with one row per affordance the component must offer, and these columns: the affordance; its signifier; the user intent it presumes; whether an intent boundary sits there and where; the treatment (move the boundary, peek across it, or confirm); the Norman concept it rests on; and the failure mode if it is done badly.

Known rows to start from: bring a card to the top of the pile; expand a card to full detail; follow an edge; hover an edge to highlight its endpoints; toggle raw versus pretty field rendering; copy a SAID or AID; compare two identifiers; reveal that a node exists but is undisclosed; present or share; print.

The hover-to-highlight idea from the brain dump is a good test case for the discipline: it is a pure affordance on desktop, absent on touch, absent in print, and — if it triggers a fetch — a boundary crossing. The inventory is where that gets decided rather than assumed.

---

## Phase 5 — Adversarial review of the research, before any design

Three independent passes, run in parallel, on the Phase 1–4 output:

1. **Citation audit.** A dedicated agent verifies that every `sources.yaml` entry exists, resolves, and actually says what it is cited for. This is a known repeat failure mode and gets its own pass rather than being folded into a general review.
2. **Domain correctness.** The `keri-review-panel` skill, on the disclosure-state matrix and the principles, to check that the ACDC semantics are right in KERI's own terms.
3. **Outside models.** An OpenRouter panel (`panel -m ds`, `kimi`, `glm`, `qwen`) prompted to *refute* the principles against the stated evidence, plus `codex exec` or `gemini -p` as a non-Claude reader. Agreement here is weak evidence; dissent is the signal and gets chased.

The gate: no design work starts until the surviving principles are written down and the refuted ones are struck with a note saying why.

---

## Phase 6 and beyond — design, then implementation

Out of scope for this commission, sketched so the sequence is visible.

**Design** produces wireframes and an interaction spec, tested against the Phase 2C corpus at three breakpoints and in print. Recommended inner loop: a **static gallery of hand-built SVG/HTML mocks first**, reviewed adversarially and thrown away, before any React exists. Mocks are cheap to discard; components are not. Layout work on the DAG (how do you lay out a partially-disclosed DAG so the holes are legible as holes?) belongs here and is likely the hardest single problem in the project.

**Implementation** as a monorepo modeled on `entviz-js`: a core package plus a React package, authored so consumers inherit no JSX-transform requirement, with the Phase 2C corpus as golden fixtures, Playwright visual regression across mobile/desktop/print media, accessibility tests, and a docs playground site.

**Structural split, matching entviz (decided):** a language-independent **rendering spec** plus a conformance corpus, with a **Python reference implementation** and a **React implementation** both held to that corpus. Python is not decoration here — it lets CI prove conformance headlessly and lets system tooling render credential views outside a browser. entviz has six conformant ports held to one corpus, and that is why it is credible. A React component alone is a component; a spec with conformant implementations is a standard other people can adopt.

---

## Model allocation and orchestration

- **Opus 5 (this session):** orchestration, integration, decisions, and writing anything that goes into the repo's own voice.
- **Fable 5:** Phase 3 synthesis, Phase 4 Norman mapping, Phase 5 adjudication, and later the spec prose.
- **Sonnet 5 / Haiku 4.5:** Phase 1 fact-gathering, capture mechanics, code reading, fixture assembly.
- **OpenRouter panel + codex/gemini:** Phase 5 refutation, where correlated error between Claude instances is the specific risk.

Concurrency is capped per this box's limits: at most 4 general-purpose agents at once, 6–8 with read-only explorers, chunked. Any agent that builds, tests, or runs a broad search runs under `nice -n 19` / `ionice -c 3`, stated in its prompt. Long-running agents stream to `/tmp/subagent-<role>-status.log` with named milestones.

## Rough cost

Phases 0–2 are the bulk of the token spend: five parallel research streams plus a corpus build. Phases 3–5 are fewer agents but higher-tier models. Expect the research commission to run in the range of a few hours of wall clock with meaningful token cost, dominated by Phase 1's captures and Phase 5's panels. I will report actual spend at each phase boundary rather than estimating precisely up front.
