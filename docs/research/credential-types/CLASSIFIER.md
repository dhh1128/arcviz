# Can a deterministic classifier categorize the catalog?

A measured answer, not an argued one. The scheme sketched during the 2026-09-21/22 categorization session was written as executable rules in [`classify.py`](classify.py), run against all 195 rows of [the catalog](README.md) via a machine-readable fixture in [`rows.json`](rows.json), and scored by [`evaluate.py`](evaluate.py) against a hand reading. Everything here is **synthesized and unratified** — the only ruling in it is Daniel's requirement that the ordinary bucket be subdivided by domain rather than left whole.

**What "deterministic" means here, because it decides the result.** A rule may test the field names a SAID-verified schema declares and a few structural facts about the payload — whether an issuee is declared, whether the payload lives in the edge section, whether it references another credential. A rule may *not* consult a description, a title or a human gloss. That is the only version that could run inside arcviz, and it is also the harsh version: a credential type whose source never published a field list cannot be classified at all.

**What ground truth means here, because it is weaker than the word suggests.** It is one person's reading — the catalog's derived `Subject` column plus a twelve-row override table for the cases where the issuer/holder/subject configuration is the point, and a hand label set over the 111 party-subject rows. It is not an authority. Several disagreements below are cases where the classifier is arguably more right than the truth file.

## The headline

| | decided | undecidable | agreement |
|---|---|---|---|
| single spine, willing to guess | 147 | 48 | 105/147 = **71%** |
| single spine, declines when blind | 84 | 111 | 61/84 = **72%** |
| **two axes — subject** | 75 | 120 | 70/75 = **93%** |
| **two axes — alignment** | 62 | 63 | 57/62 = **91%** |

## Finding 1 — the ceiling is input, not rules

**Only 85 of 195 rows publish a field list at all.** By ecosystem: keri 40 of 56, eudi 25 of 33, w3c 18 of 65, wallet 2 of 34, personhood 0 of 3. The W3C corpus is largely user stories and the wallet corpus is largely product pages and pass templates, and neither names a claim vocabulary. So more than half of the credential types that are realistically imagined today are *invisible* to any rule that reads schema fields — not misclassified, unseeable.

This is not a defect of the catalog. It is a fact about the ecosystems: a pass style is deliberately a presentation template with issuer-defined text and no semantics, and a use-case narrative is deliberately not a schema. Any classification scheme arcviz ships has to state what it does when handed one of these, and "assume it is ordinary" is the answer this experiment ruled out.

## Finding 2 — the single spine was conflating two axes, and that cost 19 points

The three-fork spine returned one value per credential, mixing two questions that are independent:

- **subject** — what the credential is about: `party`, `thing`, `occurrence`, `evidence`, `apparatus`, `agent`, `none`, `unknown`.
- **alignment** — how issuer, holder and subject line up: `ordinary`, `self-attested`, `other-party`, `inverted`, `not-a-party`, `unknown`.

A key-binding attestation is a *self-attestation* whose *subject is a key*. A single-valued spine has to discard one of those, and `BindKeyAttestation`, `ai-user-coca` and `orgVet` all failed for exactly that reason rather than because any rule misread them. Split into two axes, each single-valued, agreement went from 71% to 93% and 91% — with no new evidence and no cleverer rules. The gain came entirely from no longer forcing one answer where the artifact has two.

Each axis is MECE on its own. They are not MECE jointly, and that is the point rather than a defect.

## Finding 3 — the unsafe default, which would have shipped looking fine

In the guessing variant, 19 of 42 misses came from a single rule: *an issuee is declared and no fields are published, therefore ordinary.* That rule renders a Wallet Unit Attestation, a device credential, and a relying party's own registration certificate as ordinary evidence about the person presenting them. It is silent, it is confident, and it fails in the one direction that matters — telling a viewer that a credential is about the person in front of them when it is about their wallet, their phone, or the verifier's own permissions.

Replacing it with a refusal is what dropped coverage from 147 to 84. That trade is the right way round: the cost of declining is a viewer who is told nothing, and the cost of guessing is a viewer who is told something false with no signal that it was guessed.

## Finding 4 — field presence tells you what a credential CARRIES, not what it is FOR

Scored over the 54 rows that are both hand-labelled and field-bearing, the category pass reaches **per-label recall 0.94 and precision 0.77**, with exact label-set agreement on 32 of 54. The figures before the 2026-09-23 collapse to nine categories were recall 0.88, precision 0.64 and 19 of 54; the collapse did most of that work, because several of the merged pairs were exactly the ones the vocabularies could not separate.

The asymmetry is the finding. Recall near 0.9 means field presence almost never *misses* a domain that is genuinely there. Precision below 1 means it adds categories that are present but not the point, and before the collapse the false positives clustered exactly where you would predict: residence 6, licence 6, age 5, identity 5. A PID carries a residential address; an mDL carries `age_over_18`. Neither tag was *wrong* about the contents, and both were wrong about the point. Folding residence and age into `identity` removed that whole class of error, which is why the collapse raised precision by 13 points without touching a rule.

This is the quantitative form of a defect the project had already named qualitatively: presence is not aboutness. The hand rule that demotes `identity` when it co-occurs was an intuitive instance of the missing mechanism, which is a notion of **dominance** — which fields are the payload's purpose versus which are supporting attributes. Nothing in a JSON Schema expresses that today.

The false negatives are few (4 after the collapse, 9 before) and almost all sat on pre-collapse labels with no distinctive vocabulary to match — travel, control, award and the residual — and three of those four were folded away by the collapse. Those are a labelling problem, not a classifier problem.

## Finding 5 — a residual will appear; name it honestly

An early version had a `none`/bearer bucket catching anything with no issuee and no matched vocabulary, and dossiers, disputes and iXBRL attestations fell into it. That is a residual wearing a category's name, which is worse than a residual, because it asserts something. It now requires positive evidence — ticket, coupon, voucher, seat, barcode vocabulary — and anything else returns `unknown`.

## What would have to change for this to work

The rules are not the bottleneck and refining them further has low returns. Three things would move the number, in descending order of payoff.

**Fall back to something other than schema fields when there is no schema.** Two thirds of the wallet and W3C corpus has none. A type identifier, an issuer identity, or a registry lookup would cover cases no field predicate can reach — with the caveat the catalog already records, that the type identifier is itself unstable.

**Express dominance.** Precision sits at 0.77 while every declared field counts equally, and the remaining errors are all of this kind. A schema convention marking which attributes are the payload's purpose, or a per-schema curated genus, would lift it; deriving it from field order or from required-versus-optional was not tested and is the cheapest thing to try next.

**Decide what a classifier owes when it cannot answer.** `unknown` is currently 120 of 195 rows on the subject axis. That is not a failure to be engineered away — it is the honest state for a credential whose schema says nothing — but it does mean the rendering question is not "which of eight colours" but "what does the unmarked, unknown case look like, and how does it differ from the ordinary one". Those must not look alike.

## Reproducing

```
cd docs/research/credential-types
python3 test_classify.py     # 30 hand-built vectors plus regression floors over the catalog
python3 evaluate.py          # single-spine variants, coverage and per-row misses
```

`classify.py` carries both spine variants behind keyword arguments (`safe_default`, `narrow_assembly`) and the two-axis functions (`subject_axis`, `alignment_axis`) side by side, so the numbers in the table above can each be reproduced without editing it. `domain_truth.json` holds the hand labels; `rows.json` holds inputs only and was extracted without reference to any category, so the rules are tested rather than confirmed.
