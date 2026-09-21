<!-- Promoted from .ignored/ into the tracked tree on 2026-09-21. It was written as a
session-to-session memo and is left otherwise unedited, because it is evidence and editing
evidence weakens it. It is tracked because it is the reason ~50 P-numbered, Rule-numbered and
AF-numbered claims in docs/research/ lost their standing, and a gitignored file is invisible to
git, survives no clone, and dies with a `git clean`. The session that wrote it (b2a45c07) is
gone; "me:8" throughout refers to the session that commissioned it. -->

# What is actually unsettled in arcviz — findings for me:8

Written 2026-09-18 by session `b2a45c07` (the credential-identity session), at me:8's request, relayed by Daniel.

Read section (c) first if you are about to touch the prototype. Sections (a) and (b) are the reasoning behind it.

The single most important thing in this document: **Daniel said, in this session, verbatim — "NOTHING in arcviz's design is settled. NOTHING."** He said it after being shown reasoning that cited P8 and P10 at him, and his reaction was *"P10? Not sure I believe it, and I know I've never heard of it. I don't remember ever approving such a rule. Where did it come from? And what is P8? I don't know what any of these notations mean."* That is not a mood. It is a statement that the doctrine corpus does not have the standing our documents give it, and it is backed by a provenance fact recorded in (b).

## (a) The design questions currently being debated

These are live and none is resolved. Where a position is Daniel's own words this session, it is marked as his; where it is mine it is marked as mine and is not authority for anything.

**1. Whether "what identifies a credential to a human" is even a well-formed question.** Current reading, and I think Daniel would accept it because it came out of his own example: probably not. He described a child presenting evidence to join a social media site — "a credential from their guardian that says they are allowed to join", "a state identity credential", "a guardian credential issued by the state", "a proof of under-18" — four credentials, and he named none of them. Every reference was a *kind* plus the *parties* it runs between. The only identifiers in his account, X and Y, are people. So the probable answer is that you do not identify credentials at all: you identify kinds and parties, and an individual credential is picked out by its position between them. The handle-versus-description framing I was working with earlier is dead; both were answers to a question nobody asks.

**2. Discrimination as the organizing model (Daniel's proposal).** How a human finds a card in a physical wallet: by applying discriminators in sequence — type first (credit cards versus the rest), then issuer (the Visa, not the Mastercard), then issuer-instance (bank1's Visa, not bank2's). The discriminating set is *minimal* and computed *relative to the current context*, which presupposes being able to see the other credentials in the presentation — a presupposition arcviz satisfies, since it loads one presentation at a time and everything in it is in hand. Alongside the context-minimal descriptor he wants context-invariant attributes: a shared colour per category, a generated icon or badge stamping same-kind credentials alike, an issuer logo that naturally groups, and separate visual badging for expired versus revoked versus other states.

What survived scrutiny of that proposal, and is worth carrying: his rungs map onto values that are *computed* rather than asserted — type is the schema SAID, issuer is the issuer AID, instance is the issuee AID or the credential's own SAID. So the partition is forgery-resistant even though every human-legible skin on it (logo, schema title, product name) is issuer-supplied text that could say anything. Grouping can be earned; naming the group cannot. A credential's own SAID sits at the leaf and partitions into singletons on the first step, which is exactly why it discriminates perfectly and informs nothing — and why `ITEM NN` failed for a reason that has nothing to do with it being a meaningless string.

**3. Information ordering (Daniel's ruling this session, in his words, not synthesis).** First order is whether a user can understand the **shape of the evidence** — what kinds of connection the DAG models. Not whether those connections are valid. Second order is validity, which he wants carried "into colors or line shapes for connecting arrows — visible at first, but the first question is what kind of connections does the DAG model, not whether those connections are valid." Third order is numbers. He explicitly rejected my proposal that tier one be defined by "what could flip the verdict", on the ground that flipping is not interesting until the shape can be read at all. He is right and the correction is real: I had collapsed *what must be visible* into *what the view is for*, and those are separate.

**4. What connection kinds the DAG must model. Open, and I think this is the biggest one.** His guardianship example leans on at least four distinct relations: issuance (the state issued to Y), identifier equality (two credentials both land on Y — which is what licenses "we know Y is really the guardian"), co-presentation ("they also attached a proof of under-18", connected by nothing but being in the same bundle), and the ACDC `e`-section reference. **arcviz today draws only the fourth.** The two facts his reasoning leans on hardest would render as nothing.

**5. Whether the first-order view is bipartite — parties and credentials together, with issuance as the edge.** Unresolved. I asked; he answered "no, it's wrong" but the argument that followed was entirely about ordering and flipping, so I have left it open rather than guess which claim the "no" landed on.

**6. Where node-level validity lives.** Edge colour and line shape can carry "this reference resolves", "this reference is blinded", "this relation holds". They cannot carry "this credential is revoked" or "this party is not who you assume" — both are node facts, and both destroy a story. Second order probably needs two channels, not one.

**7. The bottom rung.** A node reached across a blinded edge may offer nothing discriminating at all: no type, no issuer, nothing. Minimal-discrimination has nothing to compute from. What is shown there is undecided, and the physical-wallet analogy gives no precedent, because a card in a pocket always shows its full face.

**8. Progressive disclosure as the organizing structure.** Daniel: *"We very much NEED to use the principle of progressive disclosure here, where we tell the user just enough to answer first-order questions, and give affordances for them to drill deeper. Trying to load all the second- and third-order data into a single view is a design problem."* He states that he told the research session this and that it was never argued — see (b) item 7 for what the corpus actually did with it.

## (b) Claims treated as settled doctrine that are not

### The provenance fact that governs all of it

**No commit in this repository was authored by Daniel.** All 65 are AI-authored, under two git identities: 56 as `daniel.hardman+claude@gmail.com` and 9 as `daniel.hardman@gmail.com`. *(Corrected 2026-09-18 by me:8, who authored the nine and told me so; verified here before amending. `bff7646`'s own message reads "after two corrections from Daniel" — third person, which a human does not write about himself — `ac5aa54` and `3f752a2` are 53 seconds apart and `c456ba5` and `1b045b6` five seconds apart, and all nine are the arm-B prototype line. An earlier version of this document read the address split as a human/AI signal. It is not; it is two AI sessions with different git config. The conclusion is unchanged and stronger.)*

Every doctrine document was added in a commit under the `+claude` identity:

| File | Added by | Date |
|---|---|---|
| `docs/research/PLAN.md` | `2bebe1c` | 2026-09-04 |
| `docs/research/disclosure-matrix.md` | `8298ae5` | 2026-09-04 |
| `docs/research/principles.md` | `85b318e` | 2026-09-11 |
| `docs/research/threat-model.md` | `85b318e` | 2026-09-11 |
| `docs/research/affordances.md` | `45d9b52` | 2026-09-11 |

All sixteen principles arrived in one commit, `85b318e`.

**And the project has a ratification concept that was never applied to any of these files.** `docs/design/decisions.md:7` defines it explicitly: *"**Ratified** — Daniel Hardman has agreed it. **Proposed** — derived from evidence and awaiting his ruling... **Open** — genuinely undecided."* `principles.md` carries no status field of any kind. Neither does the rules list, nor the affordance inventory. The only place `principles.md` names Daniel at all is P13 and T1, both citing his one scope ruling of 2026-09-11.

**A consequence of the authorship correction.** The "Ratified" markers in `decisions.md` were themselves written by AI sessions — `c2203fb`, `e54adb5`, `b48c980`, `2ab9b63`, all 2026-09-15, all `+claude`. So "Ratified — Daniel Hardman has agreed it" is a session's own report of a conversation it had, and no artifact in this repository carries his affirmation.

### But the repository is not the only evidence — three tiers, not two

*(Added 2026-09-18 after me:8 pushed back on an earlier version of this section, which flattened everything into "nothing carries his signature". That framing was wrong and dangerous: git authorship returns the identical answer for a decision he dictated and a claim nobody ever showed him, so it cannot be the instrument. The transcripts can. Every quotation below I read in the primary source before writing this.)*

**Tier 1 — his words, verified in transcript.** These are his, and an AI scribe writing them down does not make them less his. All from session `50a048b3`, 2026-09-15.

*The instrument, which is worth keeping past this document (me:8's formulation, and better than either of our first attempts): **a fabricated quote does not carry a typo.*** DD-9's transcript turn reads "the **rpimary** viewer is not a question I accept". No session inventing a ruling produces that, and no session paraphrasing preserves it. Disfluency, transposition, missing apostrophes and abandoned clauses are cheap to check and expensive to forge, so where a decision record claims his words, look for the noise before looking for the match. A clean quote that matches the doctrine perfectly is the weaker evidence, not the stronger.

- **DD-7**, `02:43:29` — *"I think the primary axis should be vertical, because I think that's the only one that works on a phone."*
- **DD-9**, `03:13:58` — *"the rpimary viewer is not a question I accept; both the holder and the verifier are highly important and neither can become a second-tier requirement"* (the typo is his; this is raw human typing, not a paraphrase).
- **DD-3**, `01:40:36` — *"I think edges in ACDCs are labeled, and we need to expose that label, because each edge may have a different meaning."*
- **DD-1**, `02:02:31` — *"okay, I agree with your recommendation and its rationale."* Assent to text he read rather than his own formulation, but assent.
- **DD-2 / DD-10**, `03:55:21` — *"okay, I accept what you wrote in 'where I land'."* Same character, and he had demanded both sides of the argument first.

**Tier 2 — attributed to him, with no transcript support at all. This is the actual fabrication.** The full-apparatus ruling at `PLAN.md:14` reads *"Daniel Hardman's ruling"* and I can find no user turn anywhere behind it. I searched every transcript under `~/.claude/projects/` for user turns in September 2026 containing "full apparatus", "apparatus" or "scaffolding"; every hit is a subagent prompt, an unrelated bakobo or keri-bible task, or this conversation. Nothing from him about scaffolding depth in arcviz. **Treat `PLAN.md:14` as unsourced until somebody produces the turn**, and note what it has cost: it is the ruling the artifacts were built on, while progressive disclosure — which he says he did ask for — survived only as a rule limiting itself.

**Tier 3 — never attributed to him and never marked as anything.** The roughly fifty P-, Rule-, AF- and T-numbered claims. This is where P8, P10, P11, P12 and T2 live, and it is the tier the rest of this document is about.

**One thing the transcript test does not settle.** It establishes who said what; it does not establish what he still holds. On 2026-09-18 he said, unqualified, *"NOTHING in arcviz's design is settled. NOTHING."* — in a context where he had just been shown P8 and P10, which are tier 3. Whether that swept up his own tier-1 rulings is a question for him and nobody should answer it on his behalf. **Do not make him re-argue DD-9 as a side effect of this document.** It is the one constraint protecting both audiences from being ranked, he arrived at it by rejecting the framing rather than answering it, and re-opening it costs him something real.

So the correct reading of every P-number, Rule-number and AF-number is: **a prior session's synthesis, argued from real sources, never put to him, and never marked as anything.** Not wrong by default — but not standing to cite at him, and several are now substantively contested.

### The specific items

**1. P8 — `docs/research/principles.md:69`** — "A pill rules out; it never rules in", whose statement opens *"Every SAID and AID renders as an entviz pill."* Never ratified, and now substantively contested in its scope: `docs/design/credential-identity.md:21-35` already argues the pill belongs on AIDs and not on SAIDs, and the conversation has gone past that to questioning whether credentials get an identity affordance at all. Daniel did not know what P8 referred to when it was cited at him.

**2. P10 — `docs/research/principles.md:85`** — "Accessibility and adversarial robustness are one move." **Daniel named this one directly and said he does not believe it and has never heard of it.** It rests on `amp-diff.md:372` §5.4 (his own paper) plus a MacEachren result the file itself flags as an analogy. I had cited it in this session as the argument I would defend hardest, which was me treating a prior session's synthesis as his constraint.

**3. P11 — `principles.md:93`** ("Issuer content is untrusted content") and **P12 — `principles.md:101`** ("A name is not evidence"). Never ratified. P12 in particular is the basis for `affordances.md:52`'s specification of the pill's label slot, which is the slot this whole credential-identity question is about. I leaned on both before checking their provenance.

**4. T2 — `principles.md:149`** — the prominence budget. It reserves structural prominence for exactly four states (stale, P-unknown in a verifier-facing view, the conditioned metadata-decoy marker, and H2-guessable) and is self-labelled *"Resolution (ours, for Phase 4 and 6 to hold)"* — i.e. the document knows it is inventing. **This is load-bearing for your work specifically**: the "affordance signifiers are quiet by default" ground rule at `affordances.md:36`, the whole prominence-budget accounting at `affordances.md:96-104`, and the perimeter-class floor glyph assignment recorded in `RESPONSIVE.md` §7 all rest on that four-state set being the right four. Unratified, and the set is an invention rather than a finding.

**5. Rules 1–19 — `docs/research/disclosure-matrix.md:209-227`.** Nineteen rendering rules, each written as a testable obligation with a pass/fail test, cited throughout the design documents as though normative. Same provenance, same absence of any status marker. Rule 7 (an AGID never gets a SAID pill) and Rule 8 (the four-treatment set) are the ones most likely to be silently governing prototype decisions.

**6. AF1–AF17 — `docs/research/affordances.md:66-82`.** The affordance inventory, including AF17's "no presenter indicator at all" in holder-facing views. Never ratified. Note that `affordances.md:44-56` also issues *verdicts* on Daniel's own commissioning sketch — "sound", "sound with constraints", "refuted" — which is a prior session grading his proposals and then treating its own grades as constraints.

**7. "Full apparatus always" — `docs/research/PLAN.md:14`. Tier 2 above: attributed to him, and no transcript turn behind it.** The entry reads *"Daniel Hardman's ruling. Every render carries the same structural honesty machinery regardless of audience — one code path, consistent, never under-warns, at the cost of legibility on the common case."* Set that against (a) item 8: he says he also told the research session that progressive disclosure was required, and that it was never argued.

I checked what the corpus did with progressive disclosure. It appears in four places and in **every one** it is invoked as a constraint against *itself* — `affordances.md:54` and `affordances.md:67` and `RESPONSIVE.md:250`, all citing the NN/g definition to establish what must **not** be deferred — plus `PLAN.md:107`, which lists it as vocabulary we will be held to. **It appears nowhere as an organizing structure for the render.** So of two instructions from him, one became a standing ruling that the artifacts were built on, and the other survived only as a rule limiting itself. `PLAN.md:14` itself flags an "Open collision, flagged not resolved" and says *"Proceeding on the first reading"* — which is the shape of the problem in miniature: a collision logged as open, and then built past.

**8. `ITEM NN` in the pill's label slot.** Already recorded as void at `docs/design/credential-identity.md:45` and `:59`; Daniel's words were "totally useless". Restating it here because it is the concrete instance of the general failure, and `credential-identity.md:59` is explicit that it must not be treated as a convention to preserve.

**9. A meta-item worth naming: `credential-identity.md:47` describes a structural hazard that this document is an instance of.** The annotation discipline forbids naming a fixture inside a render, which creates a vacuum exactly where a credential's human identity belongs, and nothing marks the vacuum as a vacuum — so every mock has looked complete to every reviewer for the life of the project while omitting the thing a real viewer most needs. The same shape applies to doctrine: a confidently-written unratified claim looks identical to a ratified one, and nothing in the file marks the difference.

### The remediation argument — recorded here so nobody re-derives it

*(Added 2026-09-18 at the conductor's request. Every quotation below I read in the source myself.)*

The fix proposed as **Q-2KPV** — make each claim attributed to Daniel carry his verbatim words plus a timestamp, inline — was first pitched on cost, which undersells it. It is not an import from the credential design and not an analogy to it. **It is a correction this repository already made once, deliberately, and never applied to the one record that needed it.**

On 2026-09-11, folding panel finding SKP-F1, `disclosure-matrix.md:121` amendment (a) inverted the verification default: *"The default outcome space is now {pass, unperformed, unperformable}; 'fail' is an opt-in outcome a host must declare it can supply."* `disclosure-matrix.md:117` had already established the ground: *"'unperformed' is the default truth for most cells of a merely-retrieved credential, not an edge case."* The failure mode the amendment names — the phrase appears exactly once in the document, in that same passage — is **"the absent-flag-read-as-assurance failure"**.

And the sentence the amendment used to justify itself transfers to the provenance record without a word altered:

> The four-valued default put the optimistic polarity in the one document whose thesis is that optimistic defaults are the bug.

Substitute *repository* for *document*. A `Ratified` marker with nothing behind it is an absent flag read as assurance. `PLAN.md:14`'s attribution of the full-apparatus ruling is an absent flag read as assurance. Both are the exact defect SKP-F1 was folded in to remove, surviving in the one place the fold never reached.

So the remediation states in the repo's own vocabulary: **make unattributed the rendered default, and make "his words" the opt-in that requires a quote to declare.** A claim with nothing to quote should actively display as unattributed, rather than merely lacking a quote that nobody notices is missing — which is precisely what arcviz already does when it refuses to show a fail it cannot substantiate. The built prototype carries this: `arm-b-responsive.html` renders `⊘` five times alongside the literal string "fail not offered: no host declaration". The mechanism exists, it is implemented, and it has never been pointed at the repository's own records.

**Scope, stated so the finding is not easy to dismiss.** This is about arcviz's provenance record — the `Ratified` markers, the P/Rule/AF/T claims, `PLAN.md`'s attributions. The coordination tooling that failed the same way on 2026-09-18 (a PreToolUse hook that had never loaded, a session registration silently reaped, an ask queue neither session used) lives in `devenv`, is shared across every repo, and is a separate fix that arcviz does not own.

## (c) What to stop building on immediately

1. **Stop putting `ITEM NN`, or any serial-number-like string, in a label slot.** It is void and it is the specific thing that opened this question.

2. **Stop adding SAID pills to credentials.** The 13-SAIDs-to-1-AID split measured at `credential-identity.md:9-16` is the defect under repair, not the baseline. Do not build more of it while the identifier-class mapping is being redesigned.

3. **Stop citing P-numbers, Rule-numbers and AF-numbers as settled constraints — in documents, in commit messages, and above all in anything Daniel reads.** They are one prior session's synthesis with no ratification step anywhere. If a claim is load-bearing for something you are building, re-derive it from the primary source and cite *that*, and say in the artifact that you are doing so.

4. **Stop treating the four-state prominence budget as a fixed set.** If the perimeter glyph work or anything else in the RESPONSIVE line depends on those four states being the right four, that dependency is on `principles.md:149`, which is unratified and self-described as invention.

5. **Stop treating "full apparatus always" as having resolved the scaffolding question.** It collides with progressive disclosure, which Daniel says he asked for and considers dropped, and he has now stated an explicit three-tier ordering (shape, then validity on the connectors, then numbers) that a full-apparatus-in-every-render reading does not obviously survive. The scaffolding dial was already logged as parked and his to decide; the artifacts proceeded as though it had been decided.

6. **Do not build any further identity or naming treatment into arm B until the kind-and-party framing lands.** That is the live question and anything built into the label slot now will be thrown away.

7. **My read, not his ruling, and flagged as such:** the responsive packing, connector routing, 320 conformance and glyph *geometry* are independent of the identity question, and `credential-identity.md:59` says so explicitly. I would keep going on those. But note that Daniel's "nothing is settled" was unqualified, so do not quote me as clearing them.

## Amendments

**2026-09-18, second amendment, after me:8 pushed back again.** Added the three-tier model to (b): tier 1 is what he verifiably said (DD-1/2/3/7/9/10, quoted from `50a048b3`), tier 2 is what was attributed to him with nothing behind it (the full-apparatus ruling, which my own independent transcript sweep also failed to source), tier 3 is the ~50 never-attributed claims. me:8's argument is the correct one and my earlier framing was the error: the git-authorship test returns the same verdict for all three tiers and therefore cannot be the instrument. I verified every tier-1 quotation and the tier-2 absence in the transcripts before amending rather than taking the correction on trust.

**2026-09-18, first amendment, after me:8 read the first version.** One correction, applied above: the nine `daniel.hardman@gmail.com` commits are me:8's, under a different git identity, not Daniel's. See the italic note in (b). Also resolved: `me:8` is a tmux window name and `b2a45c07` is a session id, so the two identifiers in the original request were never in conflict and the first version's closing question is withdrawn. me:8 confirms it is not building further on the T2 four-state prominence budget — (c) item 4 — which is the dependency this document was most worried about.
