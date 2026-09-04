# Prior art we already own: four local codebases

Audited 2026-09-04. Read-only exploration of four codebases on this machine, three of them open source and quotable, one proprietary and not.

The headline is that **nobody has built the thing arcviz is for.** One of these is a production KERI wallet and one is a production credential console, and neither renders an ACDC edge. Neither has any vocabulary for "this exists but was not disclosed." The pieces we need exist — an identifier pill, an alias convention, a status model — but the graph and the disclosure honesty are unbuilt everywhere we looked.

---

## 1. origin-voice (Provenant, proprietary — not republished)

Audited, but the analysis is not published here. `origin-voice` is Provenant's proprietary code; the detailed findings live in `.ignored/private-refs/origin-voice/analysis.md`, which is gitignored. What follows is the generalizable lesson only, with no implementation detail attributed.

A production console for chained credentials, built by a team working with them daily, showed a credential's issuance lineage as a **linear timeline** and showed the several credentials composing a larger unit as **a list with a status chip and no relationship visualization at all**. That is the finding worth carrying forward: the linear case gets built because it is tractable; the graph case does not get built. It also handled identifiers exactly as everyone else does — truncate, tooltip, copy — and passed backend-computed status through to a two-value trust chip without verifying anything client-side.

---

## 2. veridian-wallet — a production KERI/ACDC holder wallet

Open source (Cardano Foundation). Local checkout at `~/code/me/veridian-wallet`.

**Information architecture.** Not a list of accordions but a single scrolling page built from flat card blocks — About, type, description, Attributes, issuance/issuer/id/schema-version/status. Accordions appear *inside* the attributes section only, and only for object-valued ACDC attributes: `CardDetailsExpandAttributes` walks the ACDC's `a` block and renders a genuinely recursive `IonAccordion` per object-typed value, with `deepLevel` incrementing per nesting level. Default-open depth is a prop; the credential content passes `openLevels={[1]}`, so first-level nested groups start expanded and deeper ones start collapsed. `IGNORE_KEYS = ["i","dt","d","u"]` strips the ACDC's own issuee, date, digest and UUID fields from that generic walk, because each has a dedicated block elsewhere on the page.

**The edge finding — the most important result in this whole audit.** ACDC edges are parsed and reasoned about **only in the IPEX exchange layer, never in the UI**. `src/core/agent/services/ipexCommunicationService.ts` resolves chained ACDC schemas during offer/apply/grant handshakes, handling saidified and non-saidified edge sections, the M-ary operator field `o`, multiple edges, and edge groups; its test suite covers chains deeper than two. Two limits are named in the source itself: recursive schema resolution for edge groups is not supported, and an edge that does not explicitly reference the schema SAID of the far node is not supported.

But that parsing serves schema resolution for the exchange protocol, not display. The UI-facing `ACDCDetails` type (`src/core/agent/services/credentialService.types.ts:26-42`) **has no `e` field at all**. `getCredentialDetailsById` builds the display object from `sad.i`, `sad.a`, `schema.{title,description,version}` and `status.{s,dt}`, and deliberately does not carry the edges block forward. A sweep of the entire `src/ui` tree for edge or chain rendering finds nothing.

So the one shipped, open-source, real KERI wallet parses the DAG and then throws it away before drawing anything. **The chaining problem is not solved-and-improvable; it is unattempted.**

**Raw values.** SAID truncation is first-5 / last-5, inside a card block that exposes copy-to-clipboard. No raw/pretty toggle. ISO-8601 attribute values matching a date regex are auto-reformatted to short date plus time plus UTC offset — the closest thing to field prettification found in any audited codebase, and it is a regex on the value, not schema-driven.

**Verification state.** A closed three-value enum, `CredentialStatus.{CONFIRMED, PENDING, REVOKED}`, copied straight from the signify/KERIA client response — `"0"` issued, `"1"` revoked — with no client-side check. A naming trap worth recording: there is a component called `Verification`, and it is biometric/passcode re-authentication gating destructive UI actions, entirely unrelated to credential verification.

**Absent versus undisclosed.** No selective-disclosure vocabulary anywhere in the tree. Consistent with its role — a holder wallet displays credentials that are, by definition, fully disclosed to their own holder — but it means the wallet offers arcviz nothing on the problem.

---

## 3. entviz-js — the identifier pill we intend to consume

Open source, ours. `~/code/me/entviz-js`.

**`EntvizPillProps`** (`packages/react/src/EntvizPill.ts:55-134`, signature at `:275`) carries: `value` (required); rendering passthroughs `targetAr`, `fontSizePt`, `note`, `maxWidth`; `label` — documented as first-party custom text shown after the type, *host-set and trusted*, unlike the note; `typeSignal` (`"none" | "icon" | "text" | "autoCombo"`, default `"autoCombo"`); `corner` (`"sharp" | "leaf" | "round"`, default `"round"`); `highlight`; `trust`; i18n via `locale`, `dir`, `messages`; controlled-popover `open` / `onOpenChange`; and callbacks `onExpand`, `onCompare`, `onLocate`, `onCopy`, `onError`, plus the typed `onEvent` firehose. `showCompareAffordance` and `showLocateAffordance` default to true when their handler is supplied.

**The event vocabulary** (`packages/react/src/events.ts`) is the part arcviz should build on rather than reinvent:

| Type | Members | Meaning |
|---|---|---|
| `EntvizSource` | `entviz`, `pill`, `compare`, `walk`, `voice` | which component emitted |
| `EntvizSensitivity` | `plain`, `network`, `content` | host routing hint, explicitly **not** a security boundary |
| `DisclosureState` | `pill`, `visualize`, `compare` | the three-stage disclosure lifecycle a value moves through |
| `Provenance` | `pasted`, `file`, `url`, `dropped`, `provided` | how a reference value was acquired |
| `Medium` | `text`, `svg`, `raster`, `ambiguous` | the form a compared value took |
| `VerdictState` | `pending`, `different`, `no-difference`, `identical`, `unknown` | comparison outcome |

Events are notify-only; only `fetch.start` carries `preventDefault`. There is a documented *absence* worth noting as a design precedent: there is deliberately no `voice.step` event, because the live authenticator-selected cell order must never leave the endpoint.

**The alias resolver is reserved but unbuilt — and it is exactly what arcviz needs.** There is no resolver hook today, only the static `label` prop (host-supplied constant text, no lookup semantics) and the deterministic value-derived mnemonic channel. `packages/core/src/trust.ts:45-49` names the gap:

> idea (tick ~43ml): an `autoLabel` RESOLVER — a (possibly async, lazy) function that looks a value up (registry / address book / KEL alias table) and returns a human name for the pill's label slot. Unlike the deterministic mnemonic channel (mmtxrg4w), this is a host-supplied LOOKUP, not value-derived; still corpus-gated and rule-out-never-rule-in (a looked-up name is not verification). Not built.

That comment already contains the two constraints arcviz must honor: corpus-gated, and rule-out-never-rule-in. A looked-up name is not verification.

**Trust and characterization.** `characterize.ts:59-86` is pure recognition — it classifies encoding, scheme, role (`key | signature | digest | address | identifier`), qualifiers, size basis and parts, changes no pixel, and asserts no validity. `trust.ts:29-76` defines `TrustAssumption { posture: "wild" | "corpus"; mnemonic?; icon?; autoColor?; palette? }` and a pure gate: outside `posture: "corpus"` every value-derived recognition channel is forced off regardless of flags. **The pill renders nothing about cryptographic trust today** — verification lives in the separate `EntvizCompare` / `EntvizWalk` / `EntvizVoiceCompare` ceremony components.

**What a consumer inherits.** Confirmed from source: `package.json` points `main`, `types` and `exports` at `src/index.ts` with no build step, and `index.ts:4-5` states the package ships raw `.ts` and is authored with `React.createElement` so it carries no JSX-transform requirement onto consumers. A consumer therefore needs a toolchain that ingests `.ts` directly; there is no prebuilt `dist`. Peer deps are React `>=17`, developed against `^19`. Icons are vendored Lucide path data (ISC) rather than a runtime icon dependency.

---

## 4. coia — the alias convention

Open source, ours. `~/code/me/coia`.

**JS API** (`impl/js/coia.js`): `normalize(s)`, `template(who, role, scope)`, `PRONOUNS`, `createAlias(lang, who, role, scope, flags, privateFlags)`, `parseAlias(s) -> [body, flags, privateFlags]`, `matches(query, alias)`, `search(query, aliases)`, and a `ME` symbol sentinel passed as `who` for a reflexive alias. The sentinel is deliberate: a generator must not accept `""` for that purpose, so an accidentally-empty `who` cannot silently mint a reflexive alias for someone else's identifier.

**The flag registry**, sorted descending by seriousness, is richer than the two-state proved/guessed model and is directly reusable as display vocabulary:

| Digit | Name | Meaning |
|---|---|---|
| `0` | unverified | doubt about the alias assertion is unresolved — absence of confirming evidence, not evidence of a problem. Default on every generated non-reflexive alias; must not appear on a reflexive one. |
| `1` | pairwise | intended for exactly one relationship; sharing or reuse is against creator intent |
| `2`, `3` | reserved | unassigned; a reader must surface, not ignore |
| `4` | unfit | technical posture weaker than local policy requires. The only flag that is local-policy-dependent rather than portable. |
| `5` | second-hand | imported, restored, synced or accepted from elsewhere |
| `6` | test | throwaway or demo, no real-world consequence |
| `7` | do-not-use | creator decided not to transact; asserts nothing about soundness |
| `8` | retired | rotated to null or written off; historical resolution still valid |
| `9` | compromised | positive evidence another party controls it |

The `0` / `9` contrast is the sharp one: absence of evidence versus evidence of absence. And there is a **normative display rule already on the books**, which arcviz inherits rather than invents:

> Absence is never a guarantee... An application MUST NOT render an absent flag as a positive assurance.

Flags are further split into creator-indexed (a decision, which may legitimately differ between two people holding the same identifier) and referent-indexed (a fact, which should be agreed by all).

**Two corrections to our working assumptions.** First, flags are a **trailing** group after a comma in COIA 2.0 — `cecilia-ceo-acme,0` — not the leading `0-` of COIA 1.x. The `oia.md` paper still describes the 1.x form. Second, the flag that carries the man-in-the-middle language most directly is arguably `5` (second-hand), not `0`: the appendix identifies it as the case that makes the claim "reflexive aliases face no MITM risk" too strong.

**What a UI may not assume.** Normalization is NFKC, full non-Turkic case-fold, a character allowlist, whitespace runs to single hyphens, and is idempotent. Flag groups must be split off *before* normalizing the body — the reverse order destroys the delimiter. Matching is substring-of-hyphen-term, not prefix and not whole-word, deliberately, because scriptio-continua aliases are a single unsegmented token. Aliases are **not unique per identifier**; the user searches, receives several, and chooses. A flagged alias may not be used as a DNS or IDNA label.

**Resolution is out of scope by design.** COIA defines the string format only — generation, normalization, flags, matching — and explicitly disclaims storage, lookup and collision resolution. `search()` and `matches()` operate over an in-memory array the caller already holds. There is no AID-to-alias map anywhere in any implementation.

---

## Interfaces arcviz will need to define

1. **AID → label resolution.** Every project either hardcodes a synchronous dictionary lookup coupled to its own store, or reserves the generic version without building it (entviz's `autoLabel`), or declines to define it (COIA). arcviz should define an async, cacheable resolver — roughly `resolveLabel(aid) => Promise<{ alias, flags?, source } | null>` — returning COIA-formatted strings, entviz-trust-gated, and never conflated with verification.

2. **A first-class undisclosed-node type.** Nothing distinguishes "absent from the schema" from "present but redacted" from "revoked" from "never fetched." arcviz needs a distinct type and a distinct visual treatment for a node that carries only a SAID and no revealed content.

3. **An edge-DAG renderer with operators.** Multiple parents per node, operator glyphs, and per-edge disclosed-versus-SAID-only rendering. Veridian's IPEX fixtures supply useful vocabulary — edge section SAID, M-ary operator, weight — but there is no UI code anywhere to reuse.

4. **An honest verification model.** Every audited product passes backend-computed status through to a chip. arcviz needs its own state model — SAID matches, chain anchored to KEL, signature verified at seal time, revoked — wired to a check it actually performs, and must inherit COIA's discipline that absence is never a guarantee.
