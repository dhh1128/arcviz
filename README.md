# arcviz

*Visualizing ACDCs — chainable, selectively-disclosed credentials — honestly.*

**Status: design. There is no implementation yet.** Research is complete; design is in progress. If you are picking this up, start at **[HANDOFF.md](HANDOFF.md)** — it says what is settled, what is provisional, and what to do next. The decision record is [docs/design/decisions.md](docs/design/decisions.md); the research corpus and its rules of evidence are under [docs/research/](docs/research/).

## What this is for

An [ACDC](https://trustoverip.github.io/tswg-acdc-specification/) (Authentic Chained Data Container) is harder to draw than an ordinary verifiable credential, for two reasons. It is **chainable**: a credential points at other credentials through edges, so what you are really looking at is a directed acyclic graph, not a card. And it supports **graduated disclosure**: any part of that graph may be present in full, present in compact form, blinded, or withheld entirely — so the picture must distinguish *absent*, *undisclosed*, *redacted* and *unverified* without letting any of them pass for another.

Most of the difficulty is not graphics. It is refusing to draw things you do not know.

The intended deliverable is a language-independent rendering specification with a shared conformance corpus, a Python reference implementation, and a React component — the same shape as [entviz](https://github.com/dhh1128/entviz), and for the same reason: a component is a component, but a spec with conformant implementations is something other people can adopt.

## Related work in this family

- [entviz](https://github.com/dhh1128/entviz) — rendering high-entropy values as pictures a human can compare. arcviz renders every SAID and AID as an entviz pill.
- [COIA](https://github.com/dhh1128/coia) — the convention for human-friendly aliases attached to opaque identifiers, including the flag that marks an identifier as unverified.
- [Opaque Identifier Aliases](https://dhh1128.github.io/papers/oia.html) — why an alias is a private nickname and never evidence.
- [Amplifying Difference](https://dhh1128.github.io/papers/amp-diff.html) — the perceptual argument behind entviz.
- [Intent and Boundaries](https://dhh1128.github.io/papers/intent-boundaries.html) — the framework this project uses to decide when a click may act and when it must ask.

## License

Apache 2.0. See [LICENSE](LICENSE).
