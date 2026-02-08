import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "hsl(var(--brand))",
          foreground: "hsl(var(--brand-foreground))"
        },
        surface: {
          DEFAULT: "hsl(var(--surface))",
          secondary: "hsl(var(--surface-2))"
        },
        border: "hsl(var(--border))",
        text: {
          DEFAULT: "hsl(var(--text))",
          muted: "hsl(var(--text-muted))"
        }
      },
      boxShadow: {
        soft: "0 12px 30px -18px rgba(5, 150, 105, 0.6)"
      }
    }
  },
  plugins: []
};

export default config;
