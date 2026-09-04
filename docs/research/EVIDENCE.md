# Rules of evidence

Everything written into `docs/research/` is held to these rules. They exist because the failure mode this project is most likely to suffer is not being wrong about graphics — it is citing a source that does not say what we claim it says.

## 1. Every substantive claim carries a source key

A claim about what a specification requires, what a shipped product does, or what a study found must reference a key in [`../../refs/sources.yaml`](../../refs/sources.yaml). Claims about our own design reasoning do not need a key, but must be visibly marked as ours.

## 2. Quote the sentence

A source is only usable if someone on this project read the cited passage. Every source record carries a `supports` field naming the claim, and a `quote` field with the actual sentence relied upon plus a locator (section number, page, line). Relaying another author's summary of a primary source, as though it were the source, is prohibited.

## 3. Capture it locally

Links rot. Public specifications and open-access papers are captured to `refs/captures/`; screenshots of public documentation and open-source UIs to `refs/screenshots/`. The `sources.yaml` record names the capture path and the retrieval date.

## 4. Know what may not be republished

This repository is public. The following are cited by public URL and description only, and their captures live in `.ignored/private-refs/`, which is gitignored:

- Screenshots or code excerpts from Provenant's `origin-voice` — proprietary.
- Apple Wallet, Google Wallet, and other third-party product UI captures — trademark and copyright exposure.
- Paywalled papers.

A mistake here is not undone by a later `git rm`. When in doubt, it goes in `.ignored/private-refs/`.

## 5. Mark the epistemic status

Distinguish, explicitly and in the text: what a primary source establishes; what a secondary source reports; what we inferred; and what we are guessing. A confident sentence must not carry a shaky one along with it.

## 6. Recollection is not a source

Nothing enters `docs/research/` on the strength of a model's memory. If a document is believed to exist, it is a *lead* until someone has fetched it.

### A worked example, from this repository's first day

Rule 6 was broken by the author of rule 6, in the commit that created rule 6.

The first draft of `PLAN.md` cited `~/code/me/papers/amp-diff.md` in support of the principle that every SAID and AID should render as an entviz pill so that substitution becomes visible. The paper had not been read — only its line count had been checked. The citation rested on a general impression of what entviz is for.

Reading it produced the opposite of what had been asserted. The paper measures the glance regime that a pill occupies and concludes that against an adversary who has ground offline, "casual comparison is not marginally weak against such an adversary; it is broken" (`amp-diff.md:324`), and that a seeded comparison walk is therefore "a requirement, not an enhancement." The plan had recruited the paper as support for a design the paper argues is insufficient on its own.

Two things are worth extracting. First, the failure was not laziness about a marginal citation — it was the *most* load-bearing source in the section, and its unread state was invisible because the surrounding sentence sounded right. A citation that confirms your prior is the one least likely to get checked, which is exactly why it needs checking. Second, a whole category of source was skipped without anyone noticing: the papers corpus had no records at all until it was audited as its own stream, because it had been treated as a few files that happened to be named rather than as a body of prior work. Ask what category you have not looked at, not only whether each claim has a key.
