# Adjudication: SEC-F1, the unknown-operator ruling

The KERI doctrine panel raised SEC-F1 (HIGH, CONFIRMED, reported by three lenses): the decision that unknown edge operators render as *unevaluated, never invalid* is contradicted by the ACDC spec's default-injection requirement. Daniel Hardman rejected the analysis on 2026-09-06, on the grounds that operator semantics are in flux across open and recently-merged work in the spec, keripy, and the dossier spec, and that the panel was likely reasoning from v1 doctrine now under review for v2.

**The objection holds. SEC-F1 is downgraded, and a larger finding replaces it.** The evidence below was gathered directly from the repositories and the GitHub API on 2026-09-06.

## The ACDC specification is forked, and the two lines disagree about operators

There is no single "the ACDC spec" to reason from. Two branches of `trustoverip/kswg-acdc-specification` are live and carry **different normative unary operator tables**:

| | `main` (`f0bd097de`, 2026-08-28) | `v1.1` (`910c74afc`, 2026-08-27) |
|---|---|---|
| Unary operator table | `I2I`, `NI2I`, `DI2I`, `NOT` | the same **plus `E1E`** (`:1206`) |
| Default-injection clause | fires when `o` "does not include any of the `I2I`, `NI2I` or `DI2I` Operators" (`:1197`) | fires when `o` "does not include any of the `I2I`, `NI2I`, `DI2I`, **or `E1E`** Operators" (`:1209`) |
| Occurrences of `E1E` | 0 | 3 |

PR #197, "Add E1E identity edge operator to the unary Operator table", merged 2026-08-11 — **into `v1.1`, not `main`** (`baseRefName: "v1.1"`, merge commit `906e2829`). That is why a search of `main` finds nothing and the panel concluded E1E was unspecified.

The distinction is decisive for SEC-F1. On `v1.1` the injection clause was **explicitly amended to include `E1E`**, so an edge carrying `o: "E1E"` does *not* trigger default injection there; the operator governs, and `v1.1:1223` gives it full normative semantics as an identity relation between the two ACDCs' Issuee AIDs. SEC-F1's core argument — that an unrecognized token always yields a determinate verdict via injection — is true on `main` and **false on `v1.1` for the one operator the argument was built around**.

## Three further sources of operator churn

- **keripy is ahead of `main` and behind `v1.1`.** `src/keri/vdr/verifying.py:41` at `upstream/main` reads `UnaryOps = ('I2I', 'NI2I', 'DI2I', 'E1E', 'NOT')`, and the comment at `:40` — "E1E is a keripy extension not yet in the spec's normative operator table" — is itself now stale, since `v1.1` adopted it. The comment at `:38` records that "DI2I and NOT are recognized but unimplemented".
- **DI2I is not implemented yet.** `WebOfTrust/keripy` PR #1564, "Implement the DI2I edge operator", is **open** (last updated 2026-08-09). So a normative operator present in *both* spec lines has no working implementation in the reference codebase.
- **The dossier spec is minting operators into the same field.** `kswg-dossier-specification` defines four threshold operators — `MxN`, `RMxN`, `MxQ`, `RMxQ` — placed "in the operator field (`o`) of an edge group within the dossier's edges block, following ACDC operator conventions" (`spec/dossier-spec-body.md:351`, enumerated at `:369-372`). None appears in the ACDC spec's m-ary table (`AND`, `OR`, `NAND`, `NOR`, `AVG`, `WAVG`, `main:1103-1108`). A sibling specification is extending the operator vocabulary of a field the ACDC spec defines.

## What actually follows for arcviz

The flat ruling "unknown operators render unevaluated" and the flat objection "unknown operators are always determinate by injection" are both wrong, because they collapse three different situations:

1. **Known to a spec line, unknown to arcviz.** `E1E` under `main`-only knowledge. The applicable spec gives it meaning; arcviz simply cannot evaluate it. **Unevaluated** is correct, and suppresses nothing — there is no determinate verdict to suppress.
2. **Unknown to every table.** A token such as `I1I`. Here SEC-F1 is right: injection fires on both branches, the constraint is evaluated, and it can fail. Rendering "unevaluated" would suppress a real negative. **This is the case the ruling must exclude.**
3. **An m-ary group operator from a sibling spec.** `MxQ` and friends sit on an edge *group*, where the default is `AND`; the unary injection clause does not apply at all. Treating these under a unary rule is a category error, and they are the operators most likely to be met in practice as "unknown".

## The finding that replaces SEC-F1

**arcviz cannot render an edge operator without knowing which governing profile applies, and it has no way to learn that.** Two spec branches with different operator tables, a reference implementation matching neither exactly, and a sibling spec extending the same field mean the effective operator set is a property of the *deployment*, not of the artifact. Nothing in an ACDC names its governing profile; the version string `v` gives the ACDC serialization version, not the operator vocabulary in force.

This is a new host-interface input, of the same kind as the freshness policy and for the same reason: it is governance state the component cannot derive and must not guess. It should be resolved per credential, like freshness, since a dossier and a vLEI credential in one view may answer to different profiles.

Practical consequence for the rendering rule: classify the operator against the *supplied* profile, then render (1) as unevaluated with the operator token shown verbatim, (2) as the determinate injected verdict, and (3) as an edge-group operator evaluated under its own spec or unevaluated if that spec is unknown. Where no profile is supplied, "governing profile unsupplied" is its own visible state, and every operator-dependent claim inherits it.

## Process failures this exposes

- **The vendored spec is six weeks stale** (`651df33`, 2026-07-21) and `AGENTS.md` points every agent at it as the source of truth. Phase 2A's inventory was built on it. The 2A agent did cross-check against `trustoverip/*@main`, which is why nothing worse resulted — but checking one branch of a two-branch repository is not a cross-check.
- **A panel that verifies its own findings can still be wrong in a way verification will not catch**, when the error is in the choice of source rather than in the reading of it. SEC-F1's verification pass re-anchored the citation at `f0bd097` and confirmed the quoted text. Both were correct. The branch was not.
- **Recency was assumed rather than checked.** Every claim in this project's corpus that cites the ACDC spec should be re-checked against both live branches, not only `main`.

---

## Correction (2026-09-10): there is no version fork, and the profile input was invented

Daniel Hardman asked the obvious question this document failed to ask: if every ACDC declares the spec version it conforms to, how can the operator question be undefined? Checking it properly overturns this document's central framing.

**Both branches declare the same version.** `spec-head.md` on `main` and on `v1.1` both read "**Specification Status**: v1.1", and both bodies describe ACDC protocol 2.x. Our fixtures decode to `pvrsn: 2.0, gvrsn: 2.0`. There is one declared specification version in play, not two.

**The branches have diverged editorially, not versioned apart.** Neither is an ancestor of the other: 22 commits sit on `v1.1` and not on `main`, 11 on `main` and not on `v1.1`. The substantive divergence is entirely on `v1.1`, and it is Daniel's own merged PRs — #197 (`E1E`), #203 (the `dp` disclosure-paths construct), #202 (field-label restrictions), #194 (renaming the `u` field's term from "UUID" to "unique entropy"). What `main` carries that `v1.1` lacks is tooling and boilerplate.

So `v1.1` is **ahead on content**, and this document's earlier characterisation — `main` as the current line, `v1.1` as a maintenance branch — was backwards.

**The consequence: the profile input does not exist and should be retracted.** The finding that "the effective operator set is a property of the deployment rather than the artifact, so the governing profile is a host-supplied input" was built on the premise that two versions define different operator tables. They do not. One version defines one table; one git branch has not yet received an additive operator its sibling merged. That is an unreconciled repository state, not a protocol ambiguity, and designing a governance input around it would be building permanent machinery for a temporary editorial condition.

`E1E` is part of ACDC as specified at status v1.1, merged deliberately under a PR titled "Add E1E identity edge operator to the unary Operator table", with the default-injection clause amended in the same change to include it. `main` is simply behind. arcviz should implement the operator table as `v1.1` states it.

**A second panel finding falls to the same cause.** SPC-F4 held that pair 3's separator "rests on `dp`, an unresolvable reference: an unmerged construct from a keripy discussion, mis-tiered as worked-example-attested." But `dp` is in the specification — 16 occurrences and four section headings on `v1.1`, merged as PR #203. The panel read `main`, where it appears zero times. The finding is withdrawn.

**The generalisable lesson, which is now the important part.** Two independent HIGH/MEDIUM findings from a panel that verifies its own work were both wrong, by the same mechanism: `main` was taken to be the specification. Verification caught neither, because both quoted `main` accurately — the error was in which artifact to read, and a verification step that re-checks a quotation cannot see it. Any process that resolves "the spec says X" against a single default branch will keep producing this class of error silently.
