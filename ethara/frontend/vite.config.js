import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // In development, proxy /api/* requests to the FastAPI backend.
      // This avoids CORS issues when running `npm run dev` locally.
      "/api": {
        target: process.env.VITE_API_URL || "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
