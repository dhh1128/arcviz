# Sample: the accident claim file and the vLEI chain

An instrument, not arcviz. It exists so Daniel can react to every designed principle at once, and so the decisions that are still open are forced onto the screen where they can be ruled on. Nothing here is the implementation.

Every value on screen comes from `public/data.json`, which `build_data.py` computes from the corpus. Descriptors come from `tools/describe` (the spec is `vectors.json`). Categories and the structural axes come from the synthesized `classify.py`, run over disclosed attribute names because no schema resolves. Party names come from `host.json`, which is fictional. The React side does layout and the line budget and computes nothing else.

```
python3 build_data.py      # regenerate public/data.json, glyphs and attachments
npm install
npm run dev                # or: npm run build && npx vite preview
```

Anything drawn that nobody has decided carries a magenta dashed `placeholder:` mark, and the legend collects them. The "placeholder marks" checkbox hides them so you can see the page without them. `shots/` holds screenshots at 1400 px and 320 px, taken 2026-09-24.
