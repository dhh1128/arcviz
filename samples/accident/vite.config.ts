import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// @entviz/react ships raw .ts source with no build step, so it must not be pre-bundled as if
// it were compiled JavaScript; Vite transforms it like our own source.
export default defineConfig({
  base: "./",
  plugins: [react()],
  optimizeDeps: { exclude: ["@entviz/react", "@entviz/core"] },
});
