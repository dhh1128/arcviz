// PLACEHOLDER, not a proposal. iconography.md designs the glyph channel and explicitly does not
// design the colour-or-pattern channel, so something had to be drawn. The hues start from the
// Okabe-Ito set because it was built for colour-vision deficiency, and are stretched to ten
// values, which that set does not cover -- so at least two pairs here will be confusable for
// some viewers. The pattern rides with the colour so the band is not colour-only.

export interface Swatch {
  color: string;
  pattern: "solid" | "diag" | "back" | "horiz" | "vert" | "dots" | "cross" | "grid" | "zigzag" | "none";
}

export const PALETTE: Record<string, Swatch> = {
  identity: { color: "#0072B2", pattern: "solid" },
  "org-identity": { color: "#56B4E9", pattern: "diag" },
  humanness: { color: "#B8A500", pattern: "dots" },
  financial: { color: "#009E73", pattern: "horiz" },
  qualification: { color: "#E69F00", pattern: "vert" },
  health: { color: "#D55E00", pattern: "cross" },
  affiliation: { color: "#CC79A7", pattern: "back" },
  authority: { color: "#6A4C9C", pattern: "grid" },
  "civil-status": { color: "#8C6D1F", pattern: "zigzag" },
  misc: { color: "#8A8A8A", pattern: "none" },
};

export const CATEGORY_ORDER = [
  "identity", "org-identity", "humanness", "financial", "qualification",
  "health", "affiliation", "authority", "civil-status", "misc",
];

export function patternCss(s: Swatch): string {
  const c = s.color;
  const w = "rgba(255,255,255,0.55)";
  switch (s.pattern) {
    case "diag": return `repeating-linear-gradient(45deg, ${c} 0 4px, ${w} 4px 6px)`;
    case "back": return `repeating-linear-gradient(-45deg, ${c} 0 4px, ${w} 4px 6px)`;
    case "horiz": return `repeating-linear-gradient(0deg, ${c} 0 4px, ${w} 4px 6px)`;
    case "vert": return `repeating-linear-gradient(90deg, ${c} 0 3px, ${w} 3px 5px)`;
    case "dots": return `radial-gradient(${w} 1.2px, ${c} 1.6px) 0 0 / 5px 5px`;
    case "cross": return `repeating-linear-gradient(45deg, ${c} 0 3px, ${w} 3px 4px), ${c}`;
    case "grid": return `linear-gradient(${w} 1px, transparent 1px) 0 0 / 5px 5px, linear-gradient(90deg, ${w} 1px, ${c} 1px) 0 0 / 5px 5px`;
    case "zigzag": return `repeating-linear-gradient(60deg, ${c} 0 3px, ${w} 3px 5px), ${c}`;
    case "none": return `repeating-linear-gradient(90deg, ${c} 0 1px, #ddd 1px 3px)`;
    default: return c;
  }
}

// The structural axes. `ordinary` is the unmarked default; everything else is a deviation the
// viewer should notice. How `unknown` differs from `ordinary` is the PLACEHOLDER that
// credential-categories.md calls the highest-stakes rendering question the scheme raises.
export const SUBJECT_TEXT: Record<string, string | null> = {
  party: null,
  thing: "about a thing",
  occurrence: "about an event",
  evidence: "points at other evidence",
  apparatus: "about a device or key",
  agent: "about an AI agent",
  none: "bearer: no subject",
  unknown: "subject unknown",
};

export const ALIGNMENT_TEXT: Record<string, string | null> = {
  ordinary: null,
  "self-attested": "self-attested",
  "other-party": "about someone other than the holder",
  inverted: "issuance inverted",
  "not-a-party": null, // already said by the subject tag
  unknown: "alignment unknown",
};
