# Integrating entviz: what the pill actually does

Written 2026-09-24 from the entviz and entviz-js sources and from `bakobo/cesrview`'s real usage, after getting it wrong twice from memory. Everything below carries a file and line so it can be rechecked rather than believed; entviz moves, and this document will go stale.

arcviz consumes `@entviz/react`. This is about the parts that surprised us.

## The two labels are different things, and conflating them cost two turns

`entviz/docs/integration-guide.md` §"The visible label" describes a **characterization strip** — `ETH, 0x`, `CESR, Blake3-256`, `hex, 256-bit`, `text, 56-byte` — following the grammar `[+hash ]PRIMARY[, MOD][, SIZE][, PREFIX]`. That belongs to the **entviz drawing**. It is computed from the identifier's bytes, it describes scheme and encoding, and it is not settable. The eight characterization fields are also emitted as `data-*` attributes on the root `<svg>`, so a consumer never string-parses it.

The **pill** is a different component with its own chrome, and it has a host-settable slot. If you are looking for "where does our text go", it is the pill's, not the drawing's.

## The pill's label slot, and its precedence

`EntvizPill.ts:62` — `label?: string`, documented as *"First-party custom text shown after the type (host-set, trusted — unlike the note)."*

The slot fills by precedence (`EntvizPill.ts:499-505`):

```
explicit `label`   →   the gated mnemonic   →   the type text ("cesr key")
```

`typeSignal` defaults to `autoCombo`, which shows the type text **only** when the slot is otherwise empty — "so a pill is never empty".

**Pass `None`/`undefined`, never the empty string.** An empty string is still a label: it wins the precedence with nothing in it, suppresses the type text, and leaves a pill with no text at all. "Blank" has to mean *absent*, not *empty*.

## The mnemonic is the value, and it is gated

`describe.ts:428`. The mnemonic is built **only from the entviz's own displayed cells** and returns `first…middle…last` for a value of 256 bits or more (`first…last` below that). Cell texts are chunks of the value, so a CESR AID renders as something like `EKx4…vq_o…It3`.

That is the thing that reads as "the raw value with ellipses". It is not `valuePreview` — that is a different string at `EntvizPill.ts:517`, the **hover tooltip**, which shows the *full* value up to 100 characters, deliberately, with a comment defending the choice against the grinding vector a short head-and-tail teaser would create.

**The mnemonic is gated on the `corpus` trust posture.** `bakobo/cesrview` is the worked example: its `StreamPill` passes no label and declares `STREAM_TRUST = {posture: 'corpus', mnemonic: true, icon: true, autoColor: true}` under a recorded decision (`e5vk7n`), reasoning that a pasted CESR stream is a single-origin body of values. Its own test comment reads *"The entviz pill never draws the raw value; the value lives on cesrview's own wrapper"* — what a reader takes for the value **is** the mnemonic, which is made of the value.

**Consequence for arcviz.** `credential-identity.md` §2 records arcviz as *wild* by its own gate header, so today arcviz gets no mnemonic and a pill with no alias falls all the way to `cesr key`. Whether a presented dossier is a corpus is **the host application's** decision, not arcviz's — see [coia.md](coia.md) and `credential-descriptors.md` §1 — and entviz's own docs say never to expose the setting to an end user.

## `label` is trusted; `note` is not

`EntvizPill.ts:522` is explicit that the label is *"never the note (self-declared) on the pill"*. entviz keeps two slots precisely so first-party text and self-declared text cannot be confused.

So **COIA flags never go in the label.** A flag is a warning *about* the value, not part of anybody's name for it; concatenating `,9` would launder a compromise warning into trusted chrome and make it read as part of the party's name. Return flags separately and let the host render them as its own chrome.

## Props worth knowing about

`trust: TrustAssumption` gates the value-derived channels — mnemonic, colorbar icon, auto-colour tint. Absent or `posture: "wild"` keeps them all off, which is the maximum-safety default. `highlight` is host-driven, not value-derived. `onLocate` surfaces a *recognition* affordance ("find other occurrences") and is explicitly not an equality verdict; `onCompare` is the reference-requiring path to one. `corner` no longer derives from the value's type — the trailing role icon carries that cue.

## What this document does not cover

The compare flow (`EntvizCompare`), the walk (`EntvizWalk`), the SVG rendering itself, and the characterization algorithm. Read the integration guide for those. Also: none of the above was exercised in a React build from arcviz, because arcviz has no React yet — this is source reading plus one real consumer, not integration testing.
