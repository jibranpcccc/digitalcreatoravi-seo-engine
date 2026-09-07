/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        quant: {
          bg: '#080C14',
          surface: '#0D1322',
          card: '#121A2F',
          cardHover: '#182442',
          border: '#1E2C4A',
          borderLight: '#2D3F68',
          accent: '#10B981',
          accentHover: '#059669',
          cyan: '#06B6D4',
          indigo: '#6366F1',
          violet: '#8B5CF6',
          amber: '#F59E0B',
          rose: '#F43F5E'
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif']
      }
    },
  },
  plugins: [],
}
