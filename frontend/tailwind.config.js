/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx,vue}',
    './components/**/*.{ts,tsx,vue}',
    './app/**/*.{ts,tsx,vue}',
    './src/**/*.{ts,tsx,vue}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        border: "#cbc4d2", // outline-variant
        input: "#cbc4d2",
        ring: "#4f378a", // primary
        background: "#fdf7ff",
        foreground: "#1d1b20",
        primary: {
          DEFAULT: "#4f378a",
          foreground: "#ffffff",
          container: "#6750a4",
        },
        secondary: {
          DEFAULT: "#63597c",
          foreground: "#ffffff",
        },
        destructive: {
          DEFAULT: "#ba1a1a",
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#f2ecf4", // surface-container
          foreground: "#494551", // on-surface-variant
        },
        accent: {
          DEFAULT: "#e1d4fd", // secondary-container
          foreground: "#645a7d",
        },
        popover: {
          DEFAULT: "#ffffff",
          foreground: "#1d1b20",
        },
        card: {
          DEFAULT: "#ffffff",
          foreground: "#1d1b20",
        },
      },
      borderRadius: {
        lg: "12px",
        md: "8px",
        sm: "4px",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [],
}
