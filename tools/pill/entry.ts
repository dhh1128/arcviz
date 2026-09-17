/**
 * arcviz ← @entviz/react
 *
 * arcviz's layout mocks drew their own identifier "pill": a rounded rectangle holding a
 * ten-character teaser of the SAID. That is the one form entviz's pill design explicitly
 * prohibits (pill-design.md §3.3) — a short inline teaser is glanceable AND grindable, so
 * it trains the prefix heuristic that vanity-grinding defeats. arcviz's own research layer
 * had always specified the real component (principles.md:71); only the mocks substituted
 * a stand-in, and then derived the floor form's width from the stand-in's dimensions.
 *
 * This bundles the real component so the mocks can stop modelling it.
 *
 * POSTURE. No `trust` prop is passed and none is accepted here. arcviz renders a
 * presentation whose own gate header reads "PRESENTER: UNKNOWN", which is the adversarial
 * case entviz's WILD posture is built for: every value-derived channel off, leading cap
 * empty, zero identity bits in the collapsed form. The corpus posture exists for a host
 * that owns a closed, single-origin, already-trusted body of values (cesrview over the
 * user's own KEL); arcviz is not that, and per pill-design.md §13 the posture is never an
 * end-user affordance in any case.
 *
 * LABEL. `label` carries arcviz's opaque host load label ("ITEM 03"). That is what the
 * label slot is for — first-party host-set text — and it is also what arcviz was already
 * rendering, as a separate 6.5 px tag beside the teaser. Using the slot removes both the
 * teaser and the extra line.
 */
import { createElement } from "react";
import { createRoot, type Root } from "react-dom/client";
import { flushSync } from "react-dom";
import { EntvizPill } from "@entviz/react";

export interface MountOptions {
  /** The full identifier. Never truncated for display; the pill shows no value chars. */
  value: string;
  /** Host-set label for the pill's label slot — arcviz's opaque load label. */
  label?: string;
  /** Defaults to "icon": arcviz supplies a label, so the type word would be redundant. */
  typeSignal?: "none" | "icon" | "text" | "autoCombo";
  maxWidth?: number | string;
}

const roots = new WeakMap<Element, Root>();

function mount(el: Element, opts: MountOptions): void {
  let root = roots.get(el);
  if (!root) {
    root = createRoot(el);
    roots.set(el, root);
  }
  // flushSync, deliberately: arcviz routes its connectors against MEASURED geometry
  // immediately after building the DOM, so a concurrent render would have it measuring
  // empty boxes for one frame. The ResizeObserver would heal it, but the harness that
  // takes every number in RESPONSIVE.md measures on load, and a measurement that is
  // right only after a repaint is a measurement waiting to be wrong.
  flushSync(() => root!.render(
    createElement(EntvizPill, {
      value: opts.value,
      label: opts.label,
      typeSignal: opts.typeSignal ?? "icon",
      maxWidth: opts.maxWidth,
      // trust: deliberately never set. See POSTURE above.
    }),
  ));
}

/** Mount every [data-entviz-pill] in a subtree. Value and label come from data attributes. */
function mountAll(scope: ParentNode = document): number {
  const nodes = Array.from(scope.querySelectorAll<HTMLElement>("[data-entviz-pill]"));
  for (const el of nodes) {
    mount(el, {
      value: el.dataset.value ?? "",
      label: el.dataset.label || undefined,
      typeSignal: (el.dataset.typeSignal as MountOptions["typeSignal"]) || undefined,
    });
  }
  return nodes.length;
}

(globalThis as Record<string, unknown>).ArcvizPill = { mount, mountAll };
