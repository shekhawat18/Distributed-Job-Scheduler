import forms from "@tailwindcss/forms";

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  darkMode: "class",

  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },

      colors: {
        background: "#09090b",
        foreground: "#fafafa",
        muted: "#a1a1aa",
        border: "#27272a",
        card: "#18181b",

        primary: {
          DEFAULT: "#ffffff",
          foreground: "#09090b",
        },

        success: "#22c55e",
        warning: "#eab308",
        danger: "#ef4444",
        info: "#3b82f6",
      },

      boxShadow: {
        glow: "0 0 20px rgba(255,255,255,0.05)",
      },
    },
  },

  plugins: [forms],
};