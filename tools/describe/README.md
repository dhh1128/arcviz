# describe

An executable answer to "given a DAG, what should each credential's label say?", plus the vectors that hold it honest. Run `python3 test_describe.py` (or under pytest). Standard library only — this is renderer-side code, and `tools/fixtures/README.md` is explicit that the renderer must never link a KERI node.

The reasoning is in [`docs/design/description-evaluation-set.md`](../../docs/design/description-evaluation-set.md); the module docstring in `describe.py` says what the algorithm is and, more importantly, what it refuses to guess. `vectors.json` carries one `defends` field per vector, because a vector whose intent is unrecorded cannot be maintained — the next reader cannot tell an intended result from an accident.

Three things it will not do, each of which an implementation is likely to "fix" by accident:

- **It does not guess which attribute is the subject.** `credential-categories.md` measured that field presence tells you what a credential carries, not what it is for. So the subject field is an input; absent it, the gap is annotated on the nodes it actually damages.
- **It does not name a type it cannot resolve.** No schema in this corpus resolves, so the type component carries `name: null` and stays present. A render printing "unknown type" is telling the truth; one omitting the component is not.
- **It does not invent a label when nodes are genuinely identical.** `distinguishing` goes false and every colliding sibling is named. That is the petition case, and a label that looked like an answer there would be the worst failure available, because it would be invisible.

Two results came out of running it rather than out of reasoning, and both are recorded in the vectors: an edge label's trailing index (`licenceA`/`licenceB`) made the role channel spuriously unique, so the algorithm stopped before consulting anything meaningful and emitted `ITEM 03` under a longer name; and a committed-but-unresolved image is an effective discriminator that must not be used, because whether a portrait was disclosed is an accident of the presentation rather than a fact about whose licence it is.
