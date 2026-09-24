import { useEffect, useLayoutEffect, useMemo, useRef, useState, createContext, useContext } from "react";
import { EntvizPill } from "@entviz/react";
import type { TrustAssumption } from "@entviz/core";
import { abbreviate, budgeted, ranks, type Tier, type CNode, type Component, type Data, type Descriptor, type Frame, type Party } from "./model.ts";
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
  photoglyph: {
    title: "Photograph glyph",
    body: "Photographs land in misc, and the generic document says nothing. Two candidates, switchable in the header: a picture pictograph (Phosphor 'image'), or the document with its lines removed and the file extension printed on it. The extension is read from the bytes, so a withheld picture shows '?'.",
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

function Glyph({ name, size = 32, color }: { name: string; size?: number; color?: string }) {
  const url = `glyphs/${name}.svg`;
  return (
    <span
      className="glyph"
      role="img"
      aria-label={name}
      title={name}
      style={{
        width: size, height: size, backgroundColor: color ?? "currentColor",
        WebkitMaskImage: `url(${url})`, maskImage: `url(${url})`,
      }}
    />
  );
}

type PhotoGlyph = "picture" | "extension" | "none";
const PhotoMode = createContext<PhotoGlyph>("picture");
// The host's trust posture for the AIDs in this presentation. Wild (entviz's default) gives an
// unnamed AID the type text; corpus opens the mnemonic, as bakobo/cesrview does. Whether a
// presentation is a corpus is the host's call, never arcviz's (docs/integration/entviz.md).
const Trust = createContext<TrustAssumption | undefined>(undefined);
const Lexicon = createContext<Data["abbreviations"]>({});

// The longest form of the type name that fits on one line of the space it has.
function TypeName({ name }: { name: string }) {
  const lex = useContext(Lexicon);
  const ref = useRef<HTMLSpanElement>(null);
  const [tier, setTier] = useState<Tier>("full");
  useLayoutEffect(() => {
    const el = ref.current?.parentElement;
    if (!el) return;
    const fit = () => {
      const cs = getComputedStyle(el);
      const ctx = document.createElement("canvas").getContext("2d")!;
      ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
      const room = el.clientWidth - (el.querySelector(".presented-tag")?.getBoundingClientRect().width ?? 0) - 8;
      const pick = (["full", "medium", "short"] as Tier[]).find((t) => ctx.measureText(abbreviate(name, lex, t)).width <= room) ?? "short";
      setTier(pick);
    };
    fit();
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return () => ro.disconnect();
  }, [name, lex]);
  const shown = abbreviate(name, lex, tier);
  return <span ref={ref} title={shown !== name ? name : undefined}>{shown}</span>;
}

function glyphsFor(n: CNode, photo: PhotoGlyph = "picture"): { category: string; glyph: string; override: boolean; ext?: string | null }[] {
  const cats = n.classified.categories.length ? n.classified.categories : ["misc"];
  return cats.map((c) => {
    if (n.glyph_override && n.glyph_override.category === c)
      return { category: c, glyph: n.glyph_override.glyph, override: true };
    if (c === "misc" && n.photo_glyph && photo === "picture")
      return { category: c, glyph: "misc.photo", override: true };
    if (c === "misc" && n.photo_glyph && photo === "extension")
      // The extension comes from the bytes, so a withheld picture has none to show.
      return { category: c, glyph: "misc.doc-blank", override: true, ext: n.image.media_type ?? null };
    return { category: c, glyph: c, override: false };
  });
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

function SaidHandle({ said }: { said: string }) {
  // A reference handle: displayed, copyable, and deliberately NOT wrapped in the comparison
  // ceremony. A SAID's integrity is settled by recomputation, not by a human glance.
  const [copied, setCopied] = useState(false);
  return (
    <button
      className="said"
      title={`SAID ${said} — a reference handle, not something to compare by eye. Click to copy.`}
      onClick={(e) => {
        e.stopPropagation();
        navigator.clipboard?.writeText(said).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1200); });
      }}
    >
      {copied ? "copied" : said.slice(0, 8)}
    </button>
  );
}

function PartyPill({ party }: { party?: Party }) {
  if (!party) return <span className="muted">(no party)</span>;
  const trust = useContext(Trust);
  return (
    <span className="party">
      <EntvizPill
        value={party.identifier}
        // undefined, never "": an empty string still wins the label precedence and blanks the pill.
        label={party.label ?? undefined}
        typeSignal="autoCombo"
        trust={trust}
        onCompare={() => {}}
        maxWidth="100%"
      />
    </span>
  );
}

const WHEN_TEXT = (band: string) =>
  band === "assembled-for-this-claim" ? "made for this claim" :
  band.startsWith("pre-existing-") ? `predates the claim (issuance cluster ${band.slice(-1)})` : band;

function ComponentLine({ c, frame, pictures }: { c: Component; frame: Frame; pictures: boolean }) {
  const why = `${c.kind} · ${c.gain.toFixed(2)} bits${c.issuer_claim ? " · the issuer's own words" : ""}${c.text_alternative ? " · carried so the label works without pictures" : ""}`;
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
  return <li className={"dline" + (c.negative ? " negative" : "")} title={why}>{body}</li>;
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

// Progressive disclosure for everything that explains rather than orients. Hover or focus
// shows it; click pins it open.
function Info({ notes }: { notes: string[] }) {
  const [pinned, setPinned] = useState(false);
  if (!notes.length) return null;
  return (
    <span className="info-wrap">
      <button className="info" aria-label="About this credential" aria-expanded={pinned} title={notes.join("\n\n")}
        onClick={() => setPinned(!pinned)}>
        <svg viewBox="0 0 16 16" width="15" height="15" aria-hidden><circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" strokeWidth="1.4" /><circle cx="8" cy="4.6" r="1" fill="currentColor" /><rect x="7.2" y="6.6" width="1.6" height="5.4" rx="0.8" fill="currentColor" /></svg>
      </button>
      {pinned && <div className="info-pop" role="note">{notes.map((t, i) => <p key={i}>{t}</p>)}</div>}
    </span>
  );
}

function Card({
  n, frame, desc, lines, pictures, incoming, register,
}: {
  n: CNode; frame: Frame; desc: Descriptor; lines: number; pictures: boolean;
  incoming: { label: string; from: CNode }[];
  register: (said: string, el: HTMLElement | null) => void;
}) {
  const [open, setOpen] = useState(false);
  const marks = useContext(Marks);
  const photoMode = useContext(PhotoMode);
  const glyphs = glyphsFor(n, photoMode);
  const cats = glyphs.map((g) => g.category);
  const primary = PALETTE[cats[0]] ?? PALETTE.misc;
  const typeName = n.type.name;
  const { kept, dropped } = budgeted(desc, lines);
  const unknown = n.classified.subject === "unknown" || n.classified.alignment === "unknown";
  const isPresented = frame.presented === n.said;

  const notes: string[] = [];
  notes.push(`Kind: ${cats.join(", ")}${n.classified.categories.length ? "" : " (nothing matched, so the residual)"}.`);
  if (unknown) notes.push("The classifier could not tell what this credential is about, so it cannot say whether it is evidence about the party presenting it. That is not the same as ordinary.");
  for (const e of incoming) notes.push(`Referenced as “${e.label}” by the ${e.from.type.name ?? "unresolved type"}. The label is the referring issuer's choice.`);
  if (desc.annotations.some((x) => x.kind === "subject_undetermined")) notes.push("This label tells it apart from its siblings but does not say what it is about.");
  if (desc.annotations.some((x) => x.kind === "image_committed_not_resolved")) notes.push("The credential commits to a picture that this presentation did not supply.");
  if (dropped.length) notes.push(`${dropped.length} weaker ${dropped.length === 1 ? "datum" : "data"} not shown: ${dropped.map((c) => c.kind).join(", ")}. Raise the line budget or open “more”.`);
  notes.push("No host judgement about this credential was supplied.");

  return (
    <article
      ref={(el) => register(n.said, el)}
      className={"card" + (unknown ? " card-unknown" : "") + (isPresented ? " presented" : "") + (open ? " open" : "")}
      aria-expanded={open}
    >
      <Band cats={cats} />
      <div className="card-body">
        <header className="card-head">
          <span className="glyph-row" style={{ color: primary.color }}>
            {glyphs.map((g) => (
              <span key={g.glyph} className={"glyph-slot" + (g.override && marks ? " glyph-override" : "")} title={`${g.category}${g.override ? " (glyph hand-assigned)" : ""} — matched on ${(n.classified.category_hits[g.category] ?? []).join(", ") || "nothing: residual"}`}>
                <Glyph name={g.glyph} color={(PALETTE[g.category] ?? PALETTE.misc).color} />
                {g.ext !== undefined && <span className="ext">{g.ext ? "." + g.ext : "?"}</span>}
              </span>
            ))}
            {unknown && <span className="unknown-badge" title="Subject unknown: the classifier could not tell what this is about. Not the same as ordinary.">?</span>}
          </span>
          <div className="type">
            <div className="type-name">
              {isPresented && <span className="presented-tag">presented</span>}
              {typeName ? <TypeName name={typeName} /> : <span className="muted">unresolved type</span>}
            </div>
          </div>
          <SaidHandle said={n.said} />
          <Info notes={notes} />
        </header>
        <AxisTags n={n} />
        {marks && unknown && <div><Ph id="unknown" /></div>}
        <div className="card-main">
          <Thumb n={n} pictures={pictures} />
          <ul className="desc">
            {kept.map((c, i) => <ComponentLine key={i} c={c} frame={frame} pictures={pictures} />)}
          </ul>
        </div>
        {!desc.distinguishing && <div className="annotation">⚠ not distinguishable from {desc.indistinguishable_from.length} other(s)</div>}
        {!pictures && !desc.distinguishing_as_text && <div className="annotation">⚠ cannot be told apart without its picture</div>}
        {marks && (
          <div className="review-marks">
            <span className="reputation" title={PLACEHOLDERS.reputation.body}>host's stance: not supplied</span>
            {n.image.state === "committed-not-resolved" && <Ph id="thumbs" />}
            {n.photo_glyph && <Ph id="photoglyph" />}
          </div>
        )}
        <footer className="card-foot">
          <button className="more" onClick={() => setOpen(!open)}>{open ? "less" : "more"}</button>
        </footer>
        {open && <Details n={n} frame={frame} desc={desc} />}
      </div>
    </article>
  );
}

function Details({ n, frame, desc }: { n: CNode; frame: Frame; desc: Descriptor }) {
  const c = n.classified;
  return (
    <div className="details">
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
      <section>
        <h4>Parties</h4>
        <p>Issuer: <PartyPill party={frame.parties[n.issuer]} /></p>
        {n.issuee ? <p>Issuee: <PartyPill party={frame.parties[n.issuee]} /></p> : <p className="muted">No issuee.</p>}
      </section>
      <section>
        <h4>Disclosed attributes <span className="hint">(the issuer's words)</span></h4>
        <table className="attrs">
          <tbody>
            {Object.entries(n.attrs).filter(([k]) => !["d", "u"].includes(k)).map(([k, v]) => (
              <tr key={k}><td><code>{k}</code></td><td className="issuer-text">{typeof v === "string" ? v : JSON.stringify(v)}</td></tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="instrument">
        <h4>Instrument, not arcviz: what the fixture intended</h4>
        <p>{n.fixture_summary}</p>
      </section>
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
  const [paths, setPaths] = useState<{ d: string; key: string; label: string; lx: number; ly: number }[]>([]);
  const [size, setSize] = useState({ w: 0, h: 0 });

  const incoming = (said: string) =>
    frame.nodes.flatMap((m) => m.edges.filter((e) => e.target === said).map((e) => ({ label: e.label, from: m })));

  // One arrow per edge, labelled with the edge's own label (DD-3: "we need to expose that
  // label"). Every arrow arrives at the top-left of its target with the label beside the
  // arrowhead. A target on the first line of its rank is reached directly. A target further
  // down a wrapped rank is reached along the band's left gutter, so the line never threads
  // through a sibling above it and makes siblings read as a chain.
  const measure = () => {
    const root = box.current;
    if (!root) return;
    const r0 = root.getBoundingClientRect();
    const rankOf = new Map<string, number>();
    rows.forEach((row, i) => row.forEach((s) => rankOf.set(s, i)));
    const firstTop = rows.map((row) => Math.min(...row.map((s) => els.current.get(s)?.getBoundingClientRect().top ?? Infinity)));
    const arrivals = new Map<string, number>();
    const out: { d: string; key: string; label: string; lx: number; ly: number }[] = [];
    for (const m of frame.nodes) {
      for (const e of m.edges) {
        const a = els.current.get(m.said)?.getBoundingClientRect();
        const b = els.current.get(e.target)?.getBoundingClientRect();
        const r = rankOf.get(e.target);
        const band = r !== undefined ? bands.current[r]?.getBoundingClientRect() : undefined;
        if (!a || !b || r === undefined) continue;
        const k = arrivals.get(e.target) ?? 0;
        arrivals.set(e.target, k + 1);
        const x1 = a.left + a.width / 2 - r0.left, y1 = a.bottom - r0.top;
        const ax = b.left - r0.left + 22 + k * 16, ay = b.top - r0.top;
        let d: string;
        if (!band || Math.abs(b.top - firstTop[r]) < 2) {
          const my = (y1 + ay) / 2;
          d = `M${x1},${y1} C${x1},${my} ${ax},${my} ${ax},${ay}`;
        } else {
          const gx = band.left - r0.left + 10, ty = band.top - r0.top + 9, hy = ay - 20;
          d = `M${x1},${y1} L${x1},${ty} L${gx},${ty} L${gx},${hy} L${ax},${hy} L${ax},${ay}`;
        }
        out.push({ key: m.said + e.label, d, label: e.label, lx: ax + 6, ly: ay - 6 - k * 11 });
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
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,1 L9,5 L0,9 z" className="arrowhead" />
          </marker>
        </defs>
        {paths.map((p) => <path key={p.key} d={p.d} markerEnd="url(#arrow)" />)}
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
  const photoMode = useContext(PhotoMode);
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
        const g = glyphsFor(n, photoMode)[0];
        return (
          <span className="kind" key={k}>
            <Glyph name={g.glyph} size={24} color={(PALETTE[g.category] ?? PALETTE.misc).color} />
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

      <h4 id="ph-photoglyph">Photograph glyph <Ph id="photoglyph" /></h4>
      <div className="row-demo">
        <div><Glyph name="misc.photo" size={32} color={PALETTE.misc.color} /> <span className="demo-label-inline">picture</span></div>
        <div><span className="glyph-slot"><Glyph name="misc.doc-blank" size={32} color={PALETTE.misc.color} /><span className="ext">.png</span></span>
          <span className="glyph-slot"><Glyph name="misc.doc-blank" size={32} color={PALETTE.misc.color} /><span className="ext">?</span></span>
          <span className="demo-label-inline">document + extension; ? when the picture is withheld</span></div>
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
  const [photo, setPhoto] = useState<PhotoGlyph>("picture");
  const [corpus, setCorpus] = useState(false);
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
    <Marks.Provider value={marks}><PhotoMode.Provider value={photo}><Trust.Provider value={corpus ? { posture: "corpus", mnemonic: true } : undefined}><Lexicon.Provider value={data.abbreviations}>
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
            <label title="The host's trust posture for these AIDs. Wild: an unnamed AID shows its type text. Corpus: it shows the mnemonic built from its value.">
              <input type="checkbox" checked={corpus} onChange={(e) => setCorpus(e.target.checked)} /> host treats AIDs as a corpus
            </label>
            <label title="Candidates for the photograph glyph">
              photo glyph
              <select value={photo} onChange={(e) => setPhoto(e.target.value as PhotoGlyph)}>
                <option value="picture">picture</option>
                <option value="extension">document + extension</option>
                <option value="none">generic document</option>
              </select>
            </label>
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

        <main className="layout">
          <section className="frame">
            <Kinds frame={frame} />
            {marks && frame.supplied_by_hand.length > 0 && (
              <p className="hand">Supplied by hand for this sample: {frame.supplied_by_hand.join("; ")}.{" "}
                {frame.id === "vlei" && <Ph id="borrowed" />}</p>
            )}
            <Graph frame={frame} desc={desc} lines={lines === 4 ? 99 : lines} pictures={pictures} />
          </section>
          <Legend />
        </main>
      </div>
    </Lexicon.Provider></Trust.Provider></PhotoMode.Provider></Marks.Provider>
  );
}
