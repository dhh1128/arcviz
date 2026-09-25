import { useEffect, useLayoutEffect, useMemo, useRef, useState, createContext, useContext } from "react";
import { EntvizPill } from "@entviz/react";
import type { TrustAssumption } from "@entviz/core";
import { abbreviations, budgeted, ranks, type CNode, type Component, type Data, type Descriptor, type Frame, type Party } from "./model.ts";
import { ALIGNMENT_TEXT, CATEGORY_ORDER, PALETTE, SUBJECT_TEXT, patternCss } from "./palette.ts";

// ---------------------------------------------------------------------------------------------
// Placeholders. Each is something this sample had to draw that nobody has decided. They are
// marked where they appear, so what is being asked for a ruling is visible on the artifact.

export const PLACEHOLDERS: Record<string, { title: string; body: string }> = {
  palette: {
    title: "Category colour and pattern",
    body: "iconography.md designs the glyph and explicitly does not design the colour-or-pattern channel. These ten hues and patterns were picked so something could be drawn: Okabe-Ito stretched past the eight values it was built for.",
  },
  unknown: {
    title: "unknown against ordinary",
    body: "ordinary is unmarked. Every deviation gets a tag. unknown gets a tag, an amber dotted outline on the whole card, and a '?' — three cues, so it cannot pass for ordinary. credential-categories.md calls this the highest-stakes rendering question the scheme raises.",
  },
  glyphrow: {
    title: "Four or more glyphs",
    body: "Nothing is decided at four or more. Two candidates from iconography.md are drawn in the legend: cap at three with the rest in hover text, or show two plus a count. Nothing in these two frames needs more than two.",
  },
  thumbs: {
    title: "Thumbnails and the three image states",
    body: "Resolved: the picture. Committed but not resolved: a hatched frame naming the digest, because the credential commits to a picture this presentation did not supply. No image: nothing at all. Size, crop and position are all unconsidered.",
  },
  reputation: {
    title: "Reputation channel",
    body: "credential-descriptors.md section 1 requires assessment to ride in its own channel, never the name slot, and does not design it. This slot shows where the host's evidentiary stance on the credential would go. No host stance is supplied.",
  },
  subglyph: {
    title: "Subcategory glyph, hand-assigned",
    body: "Nothing selects a subcategory. The licences show the car because it was hand-assigned for this sample (Q-D4RX). The classifier alone would give the qualification rosette.",
  },
  borrowed: {
    title: "Schema entailments borrowed",
    body: "The corpus vLEI chain was generated with stand-in schema SAIDs. The entailments and type names shown are those of the real vLEI schemas in refs/schema-registry.json, mapped by hand onto the stand-ins.",
  },
  host: {
    title: "Host alias lookup is fictional",
    body: "Party names come from samples/accident/host.json, invented for this sample. Some AIDs are left unnamed on purpose, and one alias carries COIA flag 0.",
  },
};

const Marks = createContext(true);

function Ph({ id, inline = true }: { id: keyof typeof PLACEHOLDERS; inline?: boolean }) {
  const on = useContext(Marks);
  if (!on) return null;
  const p = PLACEHOLDERS[id];
  return (
    <a className={"ph" + (inline ? "" : " ph-block")} href={`#ph-${id}`} title={`PLACEHOLDER — ${p.title}. ${p.body}`}>
      placeholder: {p.title.toLowerCase()}
    </a>
  );
}

// ---------------------------------------------------------------------------------------------
// Small pieces

function Glyph({ name, size = 32, color, title }: { name: string; size?: number; color?: string; title?: string }) {
  const url = `glyphs/${name}.svg`;
  return (
    <span
      className="glyph"
      role="img"
      aria-label={title ?? name}
      title={title ?? name}
      style={{
        width: size, height: size, backgroundColor: color ?? "currentColor",
        WebkitMaskImage: `url(${url})`, maskImage: `url(${url})`,
      }}
    />
  );
}

function glyphsFor(n: CNode): { category: string; glyph: string; override: boolean; ext?: string | null }[] {
  const cats = n.classified.categories.length ? n.classified.categories : ["misc"];
  return cats.map((c) => {
    if (n.glyph_override && n.glyph_override.category === c)
      return { category: c, glyph: n.glyph_override.glyph, override: true };
    if (c === "misc" && n.photo_glyph)
      // Daniel, 2026-09-24: the document with the extension on it. The extension comes from the
      // bytes, so a withheld picture has none, and then the page is left blank (Daniel, turn 24).
      return { category: c, glyph: "misc.file", override: false, ext: n.image.media_type ?? null };
    return { category: c, glyph: c, override: false };
  });
}

// An AID's trust posture is PER VALUE, decided by whether the host's alias lookup knows it
// (Daniel, turn 21: "Deciding whether an AID is part of the corpus is supposed to be determined
// by whether the AID is found in the alias lookup -- and this might be different from one AID to
// the next"). That is also how entviz frames it: "Provenance is per-VALUE, not per-viewport...
// foreign entropy gets a different assumption (or none)" (@entviz/core trust.ts:12-15). So an
// aliased AID gets HOST_CORPUS, and an AID the lookup does not know gets none, which is wild.
const HOST_CORPUS: TrustAssumption = { posture: "corpus", mnemonic: true };
const Lexicon = createContext<Data["abbreviations"]>({});
const Meanings = createContext<Record<string, string>>({});

// Hover text for a kind glyph: its label, what the category means (from
// credential-categories.md), and why this credential got it.
function glyphTitle(g: { category: string; glyph: string; override: boolean }, meanings: Record<string, string>, evidence?: string[]): string {
  const label = g.glyph.replace(".", ": ");
  const lines = [label, meanings[g.category] ?? ""];
  if (evidence?.length) lines.push(`On this credential because of: ${evidence.join(", ")}.`);
  if (g.override) lines.push("The subcategory glyph was assigned by hand for this sample.");
  return lines.filter(Boolean).join("\n\n");
}

// The longest form of the type name that fits on one line of the space it has.
function TypeName({ name }: { name: string }) {
  const lex = useContext(Lexicon);
  const ref = useRef<HTMLSpanElement>(null);
  const forms = useMemo(() => abbreviations(name, lex), [name, lex]);
  const [shown, setShown] = useState(name);
  useLayoutEffect(() => {
    const el = ref.current?.parentElement;
    if (!el) return;
    const fit = () => {
      const cs = getComputedStyle(el);
      const ctx = document.createElement("canvas").getContext("2d")!;
      ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
      const room = el.clientWidth - (el.querySelector(".presented-tag")?.getBoundingClientRect().width ?? 0) - 8;
      setShown(forms.find((f) => ctx.measureText(f).width <= room) ?? forms[forms.length - 1]);
    };
    fit();
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return () => ro.disconnect();
  }, [name, forms]);
  return <span ref={ref} title={shown !== name ? name : undefined}>{shown}</span>;
}


function Band({ cats }: { cats: string[] }) {
  return (
    <div className="band" aria-hidden>
      {cats.map((c) => (
        <div key={c} className="band-seg" style={{ background: patternCss(PALETTE[c] ?? PALETTE.misc) }} title={c} />
      ))}
    </div>
  );
}

// A SAID is shown in an entviz pill (Daniel, turn 17), for the copy menu, the visualization and
// the value-preview hover it brings, and for entviz's own shortening. No `onCompare`, so it
// offers no comparison: "The SAID keeps the display and loses the ceremony"
// (credential-descriptors.md section 1). Always corpus posture, because "SAIDs don't have a
// MITM risk and should never be 'wild'" (Daniel, turn 21). entviz has no notion of that: its
// gate is per value set, not per kind of value, so every SAID pill has to be told.
const SAID_TRUST: TrustAssumption = { posture: "corpus", mnemonic: true };

// On permanently (Daniel, turn 42): entviz's colorbar icon, a miniature of the visualization's
// colorbar that replaces the pill's constant 2x2 badge. It is value-derived and entviz only
// draws it under corpus posture: on every SAID, and on an AID only when the host's lookup knows it.
const PillIcons = createContext(false);

// Cross-reference, copied from bakobo/cesrview (CesrView.tsx useCrossRef, decision c7vn4k): the
// pill's "Find other occurrences…" action selects an AID, and every pill showing the same AID
// is highlighted by entviz's own `highlight` ring. Choosing it again clears it. AIDs only
// (Daniel, turn 47): a SAID appears once per render and is never located.
const CrossRef = createContext<{ selected: string | null; locate: (v: string) => void }>({ selected: null, locate: () => {} });

function SaidHandle({ said }: { said: string }) {
  const icons = useContext(PillIcons);
  return (
    <span className="said-pill">
      <EntvizPill value={said} trust={icons ? { ...SAID_TRUST, icon: true } : SAID_TRUST} typeSignal="icon" maxWidth="100%" />
    </span>
  );
}

function PartyPill({ party }: { party?: Party }) {
  if (!party) return <span className="muted">(no party)</span>;
  const icons = useContext(PillIcons);
  const trust = party.aliasState === "none" ? undefined : HOST_CORPUS;
  const xref = useContext(CrossRef);
  return (
    <span className="party">
      <EntvizPill
        value={party.identifier}
        // undefined, never "": an empty string still wins the label precedence and blanks the pill.
        label={party.label ?? undefined}
        typeSignal="autoCombo"
        trust={trust && icons ? { ...trust, icon: true } : trust}
        onCompare={() => {}}
        onLocate={() => xref.locate(party.identifier)}
        highlight={xref.selected === party.identifier}
        maxWidth="100%"
      />
    </span>
  );
}

const WHEN_TEXT = (band: string) =>
  band === "assembled-for-this-claim" ? "made for this claim" :
  band.startsWith("pre-existing-") ? `predates the claim (issuance cluster ${band.slice(-1)})` : band;

function ComponentLine({ c, frame, pictures }: { c: Component; frame: Frame; pictures: boolean }) {
  let body: React.ReactNode;
  switch (c.kind) {
    case "role": return null; // carried by the labelled arrow
    case "image": return null; // the thumbnail is this component
    case "parties": {
      const [i, e] = c.value as [string, string | null];
      body = <>from <PartyPill party={frame.parties[i]} />{e && <> to <PartyPill party={frame.parties[e]} /></>}</>;
      break;
    }
    case "subject": body = <q className="issuer-text">{String(c.value)}</q>; break;
    case "party_field": body = <>of <q className="issuer-text">{String(c.value)}</q></>; break;
    case "locus": body = <>at <q className="issuer-text">{String(c.value)}</q></>; break;
    case "collected": body = <>collected {String(c.value)}</>; break;
    case "when": body = <>{WHEN_TEXT(String(c.value))}</>; break;
    case "issuer": body = <>issued by <PartyPill party={frame.parties[c.value]} /></>; break;
    case "issuee": body = c.negative ? <>with no issuee</> : <>to <PartyPill party={frame.parties[c.value]} /></>; break;
    default: body = <>{c.kind}: {String(c.value)}</>;
  }
  return <li className={"dline" + (c.negative ? " negative" : "")}>{body}</li>;
}

// Issuer and issuee, always shown (Daniel, turn 54), one per line so they align at the left, with
// no "from" or "to": a drawn arrow looping from the issuer's line to the issuee's says it instead,
// and a drawing needs no translation. With no issuee there is one line and no arrow. The relation
// is still spoken to a screen reader, and that text will need localizing like any other.
function Parties({ n, frame }: { n: CNode; frame: Frame }) {
  return (
    <div className={"parties" + (n.issuee ? " two" : "")}>
      {n.issuee && (
        <svg className="issue-arrow" viewBox="0 0 16 48" width="16" height="48" aria-hidden>
          {/* Angular, not curved, so it is never mistaken for an edge connector, and drawn like
              the field tree: its 1 px guide line and a filled triangle like its disclosure marker. */}
          <path d="M13.5,12.5 L5.5,12.5 L5.5,36.5 L9,36.5" />
          <path d="M9,32 L15,36.5 L9,41 z" className="head" />
        </svg>
      )}
      <div className="party-row"><PartyPill party={frame.parties[n.issuer]} /></div>
      {n.issuee && (
        <div className="party-row"><span className="sr-only">issued to </span><PartyPill party={frame.parties[n.issuee]} /></div>
      )}
    </div>
  );
}

function Thumb({ n, pictures }: { n: CNode; pictures: boolean }) {
  const img = n.image;
  if (img.state === "none") return null;
  if (!pictures) return null;
  if (img.state === "resolved") {
    return (
      <figure className="thumb" title={`Picture committed by digest ${img.digest} and supplied with this presentation. ${img.manifest?.note ?? ""}`}>
        <img src={img.src} alt={`picture: ${n.attrs.depicts ?? img.manifest?.depicts ?? "attached image"}`} />
      </figure>
    );
  }
  return (
    <figure className="thumb withheld" title={`This credential commits to a picture (digest ${img.digest}) that this presentation did not supply. Not the same as having no picture.`}>
      <span>picture committed, not supplied</span>
    </figure>
  );
}

// ---------------------------------------------------------------------------------------------
// The card

function AxisTags({ n }: { n: CNode }) {
  // Deviations get words, because they say something. `unknown` gets no words on the face of
  // the card (Daniel, turn 4: "do we need text for the absence of something?"); it gets the
  // dotted outline and the '?' badge in the header, and its explanation lives in the (i).
  const { subject, alignment } = n.classified;
  const tags: { text: string; why: string }[] = [];
  const s = subject === "unknown" ? null : SUBJECT_TEXT[subject];
  if (s) tags.push({ text: s, why: n.classified.subject_why });
  const a = alignment === "unknown" ? null : ALIGNMENT_TEXT[alignment];
  if (a) tags.push({ text: a, why: n.classified.alignment_why });
  if (!tags.length) return null;
  return (
    <div className="axis-tags">
      {tags.map((t) => (
        <span key={t.text} className="axis-tag" title={`${t.why}. Computed by the synthesized classifier, not ratified.`}>{t.text}</span>
      ))}
    </div>
  );
}


// The card's own action menu: copy the credential as disclosed, as pretty JSON; show its details.
function CardMenu({ n, notes }: { n: CNode; notes: string[] }) {
  const [open, setOpen] = useState(false);
  const [details, setDetails] = useState(false);
  const [done, setDone] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!open && !details) return;
    const close = () => { setOpen(false); setDetails(false); };
    const away = (e: MouseEvent) => { if (!ref.current?.contains(e.target as Node)) close(); };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") close(); };
    document.addEventListener("mousedown", away);
    document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("mousedown", away); document.removeEventListener("keydown", esc); };
  }, [open, details]);
  const act = (fn: () => Promise<void>) => async () => {
    setOpen(false);
    await fn();
    setDone(true);
    setTimeout(() => setDone(false), 1400);
  };
  const actions: [string, () => void][] = [
    ["Copy JSON", act(() => navigator.clipboard.writeText(JSON.stringify(n.sad, null, 2)))],
    ["Details", () => { setOpen(false); setDetails(true); }],
  ];
  return (
    <span className="card-menu" ref={ref}>
      <button className="kebab" aria-label="Credential actions" aria-haspopup="menu" aria-expanded={open}
        onClick={() => setOpen(!open)}>⋮</button>
      {open && (
        <div className="card-menu-list" role="menu">
          {actions.map(([label, fn]) => (
            <button key={label} role="menuitem" onClick={fn}>{label}</button>
          ))}
        </div>
      )}
      {done && <span className="card-menu-done" role="status">copied</span>}
      {details && <div className="info-pop card-details" role="note">{notes.map((t, i) => <p key={i}>{t}</p>)}</div>}
    </span>
  );
}

function Card({
  n, frame, desc, lines, pictures, incoming, register, raised, onRaise,
}: {
  n: CNode; frame: Frame; desc: Descriptor; lines: number; pictures: boolean;
  raised: boolean; onRaise: () => void;
  incoming: { label: string; from: CNode }[];
  register: (said: string, el: HTMLElement | null) => void;
}) {
  const [open, setOpen] = useState(false);
  const marks = useContext(Marks);
  const glyphs = glyphsFor(n);
  const meanings = useContext(Meanings);
  const cats = glyphs.map((g) => g.category);
  const primary = PALETTE[cats[0]] ?? PALETTE.misc;
  const typeName = n.type.name;
  const { kept, dropped } = budgeted(desc, lines);
  const unknown = n.classified.subject === "unknown" || n.classified.alignment === "unknown";
  const isPresented = frame.presented === n.said;

  const notes: string[] = [];
  notes.push(`Kind: ${cats.join(", ")}.`);
  if (unknown) notes.push("It is not known what this credential is about, so it cannot be assumed to be about the party presenting it.");
  for (const e of incoming) notes.push(`Referenced as “${e.label}” by the ${e.from.type.name ?? "unresolved type"}.`);
  // Reviewer-only notes (Daniel, turn 50: everything visible by default is what a user sees).
  if (marks && desc.annotations.some((x) => x.kind === "subject_undetermined")) notes.push("This label tells it apart from its siblings but does not say what it is about.");
  if (desc.annotations.some((x) => x.kind === "image_committed_not_resolved")) notes.push("The credential commits to a picture that this presentation did not supply.");
  if (marks && dropped.length) notes.push(`${dropped.length} weaker ${dropped.length === 1 ? "datum" : "data"} not shown: ${dropped.map((c) => c.kind).join(", ")}. Raise the line budget or open “more”.`);
  if (marks) notes.push("No host judgement about this credential was supplied.");

  return (
    <article
      ref={(el) => register(n.said, el)}
      className={"card" + (unknown ? " card-unknown" : "") + (isPresented ? " presented" : "") + (open ? " open" : "") + (raised ? " raised" : "")}
      onPointerDown={onRaise}
      aria-expanded={open}
    >
      <Band cats={cats} />
      <div className="card-body">
        {/* Daniel, turn 10: the top of a credential is its SAID and the (i); kind goes to the bottom. */}
        {/* Daniel, turn 58: a kebab menu of actions at the card's upper right. Its "Details" item
            shows what the (i) used to. */}
        <header className="card-top">
          {isPresented && <span className="presented-tag">presented</span>}
          <span className="said-slot"><SaidHandle said={n.said} /></span>
          <CardMenu n={n} notes={notes} />
        </header>
        <div className="type-name">
          {typeName ? <TypeName name={typeName} /> : <span className="muted">unresolved type</span>}
        </div>
        <AxisTags n={n} />
        {marks && unknown && <div><Ph id="unknown" /></div>}
        <div className="card-main">
          <Thumb n={n} pictures={pictures} />
          <div className="desc-col">
            <Parties n={n} frame={frame} />
            <ul className="desc">
              {kept.map((c, i) => <ComponentLine key={i} c={c} frame={frame} pictures={pictures} />)}
            </ul>
          </div>
        </div>
        {!desc.distinguishing && <div className="annotation">⚠ not distinguishable from {desc.indistinguishable_from.length} other(s)</div>}
        {!pictures && !desc.distinguishing_as_text && <div className="annotation">⚠ cannot be told apart without its picture</div>}
        {marks && (
          <div className="review-marks">
            <span className="reputation" title={PLACEHOLDERS.reputation.body}>host's stance: not supplied</span>
            {n.image.state === "committed-not-resolved" && <Ph id="thumbs" />}
          </div>
        )}
        <footer className="card-foot">
            <span className="glyph-row" style={{ color: primary.color }}>
            {glyphs.map((g) => (
              <span key={g.glyph} className={"glyph-slot" + (g.override && marks ? " glyph-override" : "")}>
                <Glyph name={g.glyph} color={(PALETTE[g.category] ?? PALETTE.misc).color}
                  title={glyphTitle(g, meanings, n.classified.category_hits[g.category] ?? [])} />
                {g.ext && <span className="ext">{g.ext}</span>}
              </span>
            ))}
            {unknown && <span className="unknown-badge" title="Subject unknown: the classifier could not tell what this is about. Not the same as ordinary.">?</span>}
          </span>
          {/* A chevron, not "more"/"less", so there is nothing to translate on the face; the
              screen-reader name still is. */}
          <button className="more chevron" aria-expanded={open} aria-label={open ? "Show less" : "Show more"}
            onClick={() => setOpen(!open)}>
            <svg viewBox="0 0 12 8" width="12" height="8" aria-hidden><path d={open ? "M1,7 L6,2 L11,7" : "M1,1 L6,6 L11,1"} /></svg>
          </button>
        </footer>
        {open && <Details n={n} frame={frame} desc={desc} />}
      </div>
    </article>
  );
}

// ---------------------------------------------------------------------------------------------
// The credential's content as a tree (Daniel, turn 51): attribute values can be JSON objects with
// fields of their own. Four top-level nodes, with Fields open and the rest closed. Edges and Rules
// hold those sections. Undisclosed holds only what the credential COMMITS to but this presentation
// does not show: a section given as a bare SAID (compact form), or an attachment committed by digest
// and not supplied. It never lists a field the schema allows and the credential simply lacks.
// That is absent, not undisclosed, and conflating the two is the failure AGENTS.md names first.

const CESR_DIGEST = /^[A-Za-z0-9_-]{44}$/;

// ISO 8601 timestamps, whatever the field is called (Daniel, turn 60). Show only the precision
// the value has: T becomes a space, then a zero fraction, zero seconds, and a 00:00 time are
// dropped in turn. The offset is dropped only with the time. A time shown without its offset
// would be read as the viewer's local time, so a UTC time keeps a "Z" (ISO's own mark, not a
// word to translate) and any other offset stays as written. The full value is the hover text.
const ISO_8601 = /^(\d{4}-\d{2}-\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-]\d{2}:\d{2})?)?$/;

export function prettyDate(v: string): string | null {
  const m = ISO_8601.exec(v);
  if (!m) return null;
  const [, date, hh, mm, ss, frac, zone] = m;
  if (hh === undefined) return date;
  // No offset at all is not UTC: it is an unstated zone, and it is shown as unstated.
  const utc = zone === "Z" || zone === "+00:00" || zone === "-00:00";
  const fracZero = !frac || /^0+$/.test(frac);
  const secZero = fracZero && (!ss || ss === "00");
  if (secZero && hh === "00" && mm === "00" && (utc || !zone)) return date;
  let t = `${hh}:${mm}`;
  if (!secZero) t += `:${ss}`;
  if (!fracZero) t += `.${frac.replace(/0+$/, "")}`;
  return `${date} ${t}${utc ? "Z" : zone ?? ""}`;
}

function Leaf({ v }: { v: any }) {
  if (typeof v === "string" && CESR_DIGEST.test(v)) return <SaidHandle said={v} />;
  if (v === null) return <span className="muted">null</span>;
  if (typeof v === "string") {
    const d = prettyDate(v);
    if (d !== null && d !== v) return <span className="issuer-text date" title={v}>{d}</span>;
  }
  return <span className="issuer-text">{typeof v === "string" ? v : JSON.stringify(v)}</span>;
}

function TreeNode({ label, value, open = false, mono = true }: { label: string; value: any; open?: boolean; mono?: boolean }) {
  const isBranch = value !== null && typeof value === "object";
  if (!isBranch) {
    return (
      <li className="tree-leaf">
        <span className="tree-key">{label}</span><Leaf v={value} />
      </li>
    );
  }
  const entries: [string, any][] = Array.isArray(value) ? value.map((x, i) => [`[${i}]`, x]) : Object.entries(value);
  return (
    <li className="tree-branch">
      <details open={open}>
        <summary>{label} <span className="muted tree-count">{entries.length}</span></summary>
        <ul className="tree">
          {entries.length ? entries.map(([k, v]) => <TreeNode key={k} label={k} value={v} />)
            : <li className="tree-leaf muted">none</li>}
        </ul>
      </details>
    </li>
  );
}

function FieldTree({ n }: { n: CNode }) {
  const sec = n.sections ?? {};
  const strip = (o: any, keys: string[]) =>
    o && typeof o === "object" ? Object.fromEntries(Object.entries(o).filter(([k]) => !keys.includes(k))) : o;
  const undisclosed: Record<string, any> = {};
  for (const k of ["a", "A", "e", "r"] as const)
    if (typeof sec[k] === "string") undisclosed[{ a: "attribs", A: "attribs", e: "edges", r: "rules" }[k] + " (compact)"] = sec[k];
  if (n.image.state === "committed-not-resolved") undisclosed["picture (committed, not supplied)"] = n.image.digest;
  const fields = typeof sec.a === "object" ? strip(sec.a, ["d", "u", "i"]) : typeof sec.A === "object" ? sec.A : {};
  return (
    <section>
      <ul className="tree tree-root">
        <TreeNode label="Attribs" value={fields} open mono={false} />
        {Object.keys(undisclosed).length > 0 && <TreeNode label="Undisclosed" value={undisclosed} mono={false} />}
        {/* A section the credential does not have is said to be absent, not shown as an empty,
            openable node that could pass for a hidden one. */}
        {typeof sec.e === "object" ? <TreeNode label="Edges" value={strip(sec.e, ["d"])} mono={false} />
          : !("e" in sec) && <li className="tree-leaf tree-absent">Edges <span className="muted">none</span></li>}
        {typeof sec.r === "object" ? <TreeNode label="Rules" value={strip(sec.r, ["d"])} mono={false} />
          : !("r" in sec) && <li className="tree-leaf tree-absent">Rules <span className="muted">none</span></li>}
      </ul>
    </section>
  );
}

function Details({ n, frame, desc }: { n: CNode; frame: Frame; desc: Descriptor }) {
  const marks = useContext(Marks);
  const c = n.classified;
  return (
    <div className="details">
      <FieldTree n={n} />
      {/* Reviewer-only: how the label and the kind were computed, and what the fixture intended. */}
      {marks && (
        <div className="reviewer">
      <section>
        <h4>Why this label</h4>
        <p className="hint">Each datum earns its place by surprisal: how much it tells you that the type and the rest of the page did not. The line budget drops the weakest first.</p>
        <table className="gains">
          <tbody>
            {desc.components.map((x, i) => (
              <tr key={i}>
                <td>{x.kind}</td>
                <td className="num">{x.gain.toFixed(2)} bits</td>
                <td>{x.issuer_claim ? "issuer's words" : x.role_bearing ? "role" : "discriminator"}{x.text_alternative ? ", text alternative" : ""}{x.negative ? ", by absence" : ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section>
        <h4>What kind of evidence this is</h4>
        <p>Categories: <b>{c.categories.join(", ") || "none matched (misc)"}</b>. Subject: <b>{c.subject}</b> — {c.subject_why}. Alignment: <b>{c.alignment}</b> — {c.alignment_why}.</p>
        <p className="hint">Computed by the synthesized classifier from {c.input}. Field presence says what a credential carries, not what it is for.</p>
        {n.glyph_override && <p className="hint">{n.glyph_override.why}. <Ph id="subglyph" /></p>}
        {n.borrowed_schema && (
          <p className="hint">
            Type and entailments from real schema <code>{n.borrowed_schema.real_schema.slice(0, 12)}…</code> ({n.borrowed_schema.state}): issuer is “{n.borrowed_schema.issuer_role}”, issuee is “{n.borrowed_schema.issuee_role}”
            {n.borrowed_schema.pinned_edges?.length ? `, pinned edges ${n.borrowed_schema.pinned_edges.join(", ")}` : ""}. <Ph id="borrowed" />
          </p>
        )}
      </section>
      <section className="instrument">
        <h4>Instrument, not arcviz: what the fixture intended</h4>
        <p>{n.fixture_summary}</p>
      </section>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------------------------
// The graph: rows by longest-path rank, edges drawn over them.

function Graph({ frame, desc, lines, pictures }: { frame: Frame; desc: Record<string, Descriptor>; lines: number; pictures: boolean }) {
  const rows = useMemo(() => ranks(frame), [frame]);
  const bySaid = useMemo(() => new Map(frame.nodes.map((n) => [n.said, n])), [frame]);
  const els = useRef(new Map<string, HTMLElement>());
  const box = useRef<HTMLDivElement>(null);
  const bands = useRef<(HTMLDivElement | null)[]>([]);
  const [paths, setPaths] = useState<{ d: string; key: string; label: string; lx: number; ly: number; bx: number; by: number }[]>([]);
  const [raised, setRaised] = useState<string | null>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  const incoming = (said: string) =>
    frame.nodes.flatMap((m) => m.edges.filter((e) => e.target === said).map((e) => ({ label: e.label, from: m })));

  // One curved connector per edge, labelled with the edge's own label (DD-3: "we need to
  // expose that label"). Daniel, turn 11: curves everywhere, drawn over the cards, ending in a
  // small box at the middle of the target's top edge. A clicked card rises above the lines.
  // Closed cards on one visual line share a height, so their footers line up (turn 18). An opened
  // card does not raise its neighbours to its own height (Daniel, turn 59): they keep theirs and sit
  // top-aligned beside it. Done here rather than by flex stretch, which cannot leave one item out.
  const equalize = () => {
    const cards = [...(box.current?.querySelectorAll<HTMLElement>(".card") ?? [])];
    cards.forEach((c) => { c.style.minHeight = ""; });
    const lines = new Map<number, HTMLElement[]>();
    for (const c of cards) {
      if (c.classList.contains("open")) continue;
      const top = Math.round(c.getBoundingClientRect().top);
      lines.set(top, [...(lines.get(top) ?? []), c]);
    }
    for (const line of lines.values()) {
      const h = Math.max(...line.map((c) => c.offsetHeight));
      line.forEach((c) => { c.style.minHeight = `${h}px`; });
    }
  };

  const measure = () => {
    const root = box.current;
    if (!root) return;
    equalize();
    const r0 = root.getBoundingClientRect();
    const arrivals = new Map<string, number>();
    const out: { d: string; key: string; label: string; lx: number; ly: number; bx: number; by: number }[] = [];
    for (const m of frame.nodes) {
      for (const e of m.edges) {
        const a = els.current.get(m.said)?.getBoundingClientRect();
        const b = els.current.get(e.target)?.getBoundingClientRect();
        if (!a || !b) continue;
        const k = arrivals.get(e.target) ?? 0;
        arrivals.set(e.target, k + 1);
        const x1 = a.left + a.width / 2 - r0.left, y1 = a.bottom - r0.top;
        const x2 = b.left + b.width / 2 - r0.left, y2 = b.top - r0.top;
        const bend = Math.max(30, (y2 - y1) / 2);
        // The box and its label sit wholly above the target's top border: the label's baseline is
        // placed so its whole text box, descent included, clears the border by 1 px (Daniel, turn 14). A second edge
        // into the same target stacks its box and label higher.
        const by = y2 - 9 - k * 17;
        const d = `M${x1},${y1} C${x1},${y1 + bend} ${x2},${by - bend} ${x2},${by}`;
        out.push({ key: m.said + e.label, d, label: e.label, lx: x2 + 7, ly: by + 4, bx: x2 - 3.5, by: by - 3.5 });
      }
    }
    // Only set state when the geometry actually moved, or measuring re-renders forever.
    const sig = out.map((p) => p.d).join("|") + `|${r0.width}x${r0.height}`;
    if (sig === lastSig.current) return;
    lastSig.current = sig;
    setPaths(out);
    setSize({ w: r0.width, h: r0.height });
  };
  const lastSig = useRef("");
  const measureRef = useRef(measure);
  measureRef.current = measure;

  useLayoutEffect(() => measure());
  useEffect(() => {
    const run = () => measureRef.current();
    const ro = new ResizeObserver(run);
    if (box.current) {
      ro.observe(box.current);
      box.current.querySelectorAll(".card").forEach((c) => ro.observe(c));
    }
    window.addEventListener("resize", run);
    return () => { ro.disconnect(); window.removeEventListener("resize", run); };
  }, [frame, desc, lines, pictures]);

  return (
    <div className="graph" ref={box}>
      <svg className="edges" width={size.w} height={size.h} aria-hidden>
        {paths.map((p) => <path key={p.key} d={p.d} />)}
      </svg>
      {/* Terminators and labels sit above everything, including a raised card, so covering the
          lines never hides where an edge lands or what it is called. */}
      <svg className="edge-ends" width={size.w} height={size.h} aria-hidden>
        {paths.map((p) => <rect key={p.key + ":b"} x={p.bx} y={p.by} width={7} height={7} className="edge-box" />)}
        {paths.map((p) => <text key={p.key + ":t"} x={p.lx} y={p.ly} className="edge-label">{p.label}</text>)}
      </svg>
      {rows.map((row, i) => (
        <div className="rank" key={i} ref={(el) => { bands.current[i] = el; }}>
          {i > 0 && (
            <div className="rank-label">
              {i === 1 ? "referenced by the presented credential" : `${i} references away`} · {row.length}
            </div>
          )}
          {row.map((said) => {
            const n = bySaid.get(said)!;
            return (
              <Card
                key={said} n={n} frame={frame} desc={desc[said]} lines={lines} pictures={pictures}
                incoming={incoming(said)}
                raised={raised === said}
                onRaise={() => setRaised(said)}
                register={(s, el) => { if (el) els.current.set(s, el); else els.current.delete(s); }}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
}

// First glance, posture point 5: what kinds of evidence are there?
function Kinds({ frame }: { frame: Frame }) {
  const meanings = useContext(Meanings);
  const groups = new Map<string, { n: CNode; count: number }>();
  for (const n of frame.nodes) {
    const k = n.type.name ?? `unresolved type ${n.schema.slice(0, 8)}`;
    const g = groups.get(k);
    if (g) g.count++; else groups.set(k, { n, count: 1 });
  }
  return (
    <div className="kinds" aria-label="What kinds of evidence are here">
      <Ph id="palette" />
      {[...groups.entries()].map(([k, { n, count }]) => {
        const g = glyphsFor(n)[0];
        return (
          <span className="kind" key={k}>
            <Glyph name={g.glyph} size={24} color={(PALETTE[g.category] ?? PALETTE.misc).color} title={glyphTitle(g, meanings)} />
            {k}{count > 1 ? ` ×${count}` : ""}
          </span>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------------------------
// Legend: what each channel means, and the placeholders gathered in one place.

function Legend() {
  const sampleRow = ["financial", "qualification", "affiliation", "identity"];
  return (
    <aside className="legend">
      <h3>Reading this</h3>
      <p>The coloured band and the glyph both say what kind of evidence a credential is: two channels for one signal, so colour is never the only cue. The text under each card says what part it plays in this particular set of evidence. A dotted amber outline means the classifier could not tell what the credential is about. It does not mean the credential is ordinary.</p>

      <h4 id="ph-palette">Categories <Ph id="palette" /></h4>
      <ul className="swatches">
        {CATEGORY_ORDER.map((c) => (
          <li key={c}>
            <span className="swatch" style={{ background: patternCss(PALETTE[c]) }} />
            <Glyph name={c} size={24} color={PALETTE[c].color} /> {c}
          </li>
        ))}
      </ul>

      <h4 id="ph-unknown">Structural axes <Ph id="unknown" /></h4>
      <div className="axis-demo">
        <div className="mini">ordinary <span className="muted">(nothing drawn)</span></div>
        <div className="mini"><span className="axis-tag">about an event</span> a deviation</div>
        <div className="mini card-unknown-demo"><span className="unknown-badge" style={{ marginTop: 0 }}>?</span> unknown: the dotted outline and the ? badge, no words</div>
      </div>

      <h4 id="ph-glyphrow">Four or more glyphs <Ph id="glyphrow" /></h4>
      <div className="row-demo">
        <div>
          <span className="demo-label">cap at three, rest in hover</span>
          <span title={`also: ${sampleRow.slice(3).join(", ")}`}>
            {sampleRow.slice(0, 3).map((c) => <Glyph key={c} name={c} size={24} color={PALETTE[c].color} />)}
            <span className="more-glyphs">…</span>
          </span>
        </div>
        <div>
          <span className="demo-label">two plus a count</span>
          {sampleRow.slice(0, 2).map((c) => <Glyph key={c} name={c} size={24} color={PALETTE[c].color} />)}
          <span className="more-glyphs" title={sampleRow.slice(2).join(", ")}>+{sampleRow.length - 2}</span>
        </div>
      </div>

      <h4 id="ph-thumbs">Pictures <Ph id="thumbs" /></h4>
      <p>Three states: the picture; a hatched frame when the credential commits to a picture this presentation did not supply; nothing when there is no picture.</p>

      <h4>Identifiers</h4>
      <p>A SAID (the short monospace token) is a reference handle. Copy it, cite it, but don't compare it by eye, because software settles whether it matches. An AID is shown in the entviz pill, whose menu offers comparison against a reference. Where the host can name the party, the name is in the pill. <Ph id="host" /></p>

      <h4 id="ph-reputation">Reputation <Ph id="reputation" /></h4>
      <p>A name says who a party is, not whether to believe them. The “host's stance” slot on each card is where that judgement would go.</p>

      <h4 id="ph-subglyph">Other placeholders</h4>
      <p><Ph id="subglyph" /> <span id="ph-borrowed" /><Ph id="borrowed" /> <span id="ph-host" /></p>
    </aside>
  );
}

// ---------------------------------------------------------------------------------------------

export default function App() {
  const [data, setData] = useState<Data | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [frameId, setFrameId] = useState("accident");
  const [lines, setLines] = useState(2);
  const [pictures, setPictures] = useState(true);
  const [marks, setMarks] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const locate = (v: string) => setSelected((cur) => (cur === v ? null : v));
  useEffect(() => setSelected(null), [frameId]);
  const icons = true; // Daniel, turn 42: colorbar icons on permanently (on SAIDs, and on AIDs the lookup knows)
  const [variant, setVariant] = useState<Record<string, string>>({ vlei: "no-aliases" });

  useEffect(() => {
    fetch("data.json").then((r) => r.json()).then(setData).catch((e) => setErr(String(e)));
  }, []);

  if (err) return <p>Could not load data.json: {err}. Run <code>python3 build_data.py</code> first.</p>;
  if (!data) return <p>Loading…</p>;
  const frame = data.frames.find((f) => f.id === frameId)!;
  const v = variant[frame.id] ?? frame.descriptor_variants[0];
  const desc = frame.descriptors[v];

  return (
    <Marks.Provider value={marks}><Lexicon.Provider value={data.abbreviations}><PillIcons.Provider value={icons}><CrossRef.Provider value={{ selected, locate }}><Meanings.Provider value={data.category_meanings}>
      <div className="page">
        <header className="page-head">
          <h1>arcviz sample</h1>
          <nav className="tabs">
            {data.frames.map((f) => (
              <button key={f.id} className={f.id === frameId ? "on" : ""} onClick={() => setFrameId(f.id)}>{f.title}</button>
            ))}
          </nav>
          <div className="controls">
            <label>
              descriptor lines
              <input type="range" min={1} max={4} value={lines} onChange={(e) => setLines(+e.target.value)} />
              <span className="num">{lines === 4 ? "all" : lines}</span>
            </label>
            <label><input type="checkbox" checked={pictures} onChange={(e) => setPictures(e.target.checked)} /> pictures</label>
            <label><input type="checkbox" checked={marks} onChange={(e) => setMarks(e.target.checked)} /> reviewer marks</label>
            {frame.descriptor_variants.length > 1 && (
              <label title="Whether the host can put names to the AIDs. A schema can entail that the issuee is a legal entity, not which one, so named parties bring the party relation back.">
                <input type="checkbox" checked={v === "host-aliases"}
                  onChange={(e) => setVariant({ ...variant, [frame.id]: e.target.checked ? "host-aliases" : "no-aliases" })} />
                {" "}host names the parties
              </label>
            )}
          </div>
        </header>

        <div className="evaluation" role="status">
          <b>Not evaluated.</b> This sample checks no signatures, key event logs or revocation status, so nothing on this page means “fine”.
        </div>

        <main className={"layout" + (marks ? "" : " no-legend")}>
          <section className="frame">
            <Kinds frame={frame} />
            {marks && frame.supplied_by_hand.length > 0 && (
              <p className="hand">Supplied by hand for this sample: {frame.supplied_by_hand.join("; ")}.{" "}
                {frame.id === "vlei" && <Ph id="borrowed" />}</p>
            )}
            <Graph frame={frame} desc={desc} lines={lines === 4 ? 99 : lines} pictures={pictures} />
          </section>
          {marks && <Legend />}
        </main>
      </div>
    </Meanings.Provider></CrossRef.Provider></PillIcons.Provider></Lexicon.Provider></Marks.Provider>
  );
}
