/**
 * Bundles entry.ts (and with it @entviz/react, @entviz/core and React) into a single IIFE,
 * then injects it into the mock's <script id="entviz-bundle"> element in place.
 *
 * Why inject rather than emit a sibling .js: the mocks are downloaded and opened as ONE
 * file. A second file to fetch is exactly the friction that has already cost this work
 * several rounds. So the HTML stays hand-authored and self-contained, and this script only
 * ever rewrites the contents of that one element — it is idempotent and touches nothing else.
 *
 * Run:  npm --prefix tools/pill install && npm --prefix tools/pill run build
 */
import { build } from "esbuild";
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const TARGETS = [resolve(here, "../../docs/design/layout-comparison/arm-b-responsive.html")];
const MARKER = 'id="entviz-bundle"';

const result = await build({
  entryPoints: [resolve(here, "entry.ts")],
  bundle: true,
  format: "iife",
  minify: true,
  target: ["chrome111", "firefox110", "safari16"],
  define: { "process.env.NODE_ENV": '"production"' },
  legalComments: "none",
  write: false,
});

const code = result.outputFiles[0].text.trim();
if (code.includes("</script")) throw new Error("bundle contains </script — cannot inline safely");

for (const file of TARGETS) {
  const html = readFileSync(file, "utf8");
  const open = html.indexOf(MARKER);
  if (open === -1) throw new Error(`no ${MARKER} element in ${file}`);
  const start = html.indexOf(">", open) + 1;
  const end = html.indexOf("</script>", start);
  if (end === -1) throw new Error(`unterminated bundle script in ${file}`);
  const next = html.slice(0, start) + "\n" + code + "\n" + html.slice(end);
  if (next !== html) writeFileSync(file, next);
  const kb = (Buffer.byteLength(code) / 1024).toFixed(1);
  console.log(`${next === html ? "unchanged" : "injected"}  ${kb} KB  →  ${file}`);
}
